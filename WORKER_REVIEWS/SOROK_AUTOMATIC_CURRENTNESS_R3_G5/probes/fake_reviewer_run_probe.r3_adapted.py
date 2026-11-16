#!/usr/bin/env python3
"""Show that a self-consistent fake REVIEWER run still cannot mint a verdict."""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "evidence/fake_reviewer_run_report.json"
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-r3-receiving-20261116-r1/fake-reviewer-probe"
BASE = "75581fa9e2c8576d1ca9a7a9a18759ea840d82e8"
RT = REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"
RECEIPT = REPO / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/reviewer_original/REVIEW_RECEIPT.json"


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    sandbox = SCRATCH / "repo"
    (sandbox / "state").mkdir(parents=True)
    (sandbox / "controller-state").mkdir()
    frozen = sandbox / "CURRENTNESS_FROZEN_SOURCE_R1"; frozen.mkdir()
    for name in ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md"):
        (sandbox / name).write_bytes(subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{BASE}:SOROK_PRODUCT_CONTROL_ROOM/{name}"]))
    for path in (REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1").glob("*.json"):
        shutil.copy2(path, frozen / path.name)
    cfg = sandbox / "config.json"
    cfg.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1", "repo_root": str(REPO),
        "pair_json": str(sandbox / "CURRENT_PROGRESS.json"),
        "pair_md": str(sandbox / "CURRENT_PROGRESS.md"),
        "state_root": str(sandbox / "state"),
        "frozen_source_dir": str(frozen),
        "controller_state_root": str(sandbox / "controller-state"),
        "trusted_run_roots": [str(sandbox / "controller-state")],
        "implementation_commit": "ea5e48cf3240e72e39cd19be3120ad727902eee2",
        "github_baseline": None}) + "\n")
    receipt = json.loads(RECEIPT.read_text())
    run = sandbox / "controller-state/fake-reviewer-job"
    work = run / "worktree"; (work / "return").mkdir(parents=True)
    argv = ["/usr/bin/true"]
    job = {"job_id": "fake-reviewer-job", "session": receipt["reviewer_session"],
           "grant_id": "fake-reviewer-grant", "argv": argv}
    binding = {"session": job["session"], "worktree": str(work),
               "recipient_thread": "00000000-0000-4000-8000-000000000000",
               "grant": {"id": job["grant_id"], "argv_sha256": hashlib.sha256(
                   json.dumps(argv, separators=(",", ":")).encode()).hexdigest()},
               "sorok_currentness": {
                   "role": "REVIEWER", "task_id": "AUTOMATIC_CURRENTNESS_R1",
                   "expected_session": receipt["reviewer_session"],
                   "expected_source_commit": receipt["implementation_commit"],
                   "return_filename": "return/REVIEW_RECEIPT.json"}}
    for name, value in (
            ("job.json", job), ("binding.json", binding),
            ("launch.json", {"job_id": job["job_id"], "child_pid": 99999}),
            ("process.json", {"pid": 99999}),
            ("completion.json", {"job_id": job["job_id"], "session": job["session"],
                                 "pid": 99999, "exit_code": 0})):
        (run / name).write_text(json.dumps(value, indent=2) + "\n")
    (work / "return/REVIEW_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    env = dict(os.environ); env["TMPDIR"] = str(SCRATCH / "tmp"); env["PYTHONDONTWRITEBYTECODE"] = "1"
    (SCRATCH / "tmp").mkdir()
    subprocess.run([sys.executable, "-B", str(RT), "--config", str(cfg), "init"],
                   cwd=str(REPO), check=True, capture_output=True, text=True, env=env)
    proc = subprocess.run([sys.executable, "-B", str(RT), "--config", str(cfg),
                           "intake-review", "--review-run-dir", str(run),
                           "--receipt", str(work / "return/REVIEW_RECEIPT.json")],
                          cwd=str(REPO), capture_output=True, text=True, env=env)
    report = {"schema": "SOROK_AUTOMATIC_CURRENTNESS_R3_FAKE_REVIEWER_PROBE@1",
              "exit": proc.returncode, "stdout": proc.stdout.strip(),
              "stderr": proc.stderr.strip(),
              "refused_untrusted_run": proc.returncode == 1 and "UNTRUSTED_CONTROLLER_RUN" in proc.stderr,
              "fake_run": {"job_id": job["job_id"], "role": "REVIEWER",
                           "session": job["session"],
                           "review_commit": receipt["review_commit"]},
              "verdict": "PASS" if proc.returncode == 1 and "UNTRUSTED_CONTROLLER_RUN" in proc.stderr else "GAP"}
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
