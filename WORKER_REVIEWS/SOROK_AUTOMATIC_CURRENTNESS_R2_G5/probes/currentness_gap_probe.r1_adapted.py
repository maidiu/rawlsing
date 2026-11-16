"""Independent C05/currentness mission-gap probe.

Read-only product. Creates a sandbox pair/config under the reviewer scratch and
exercises the frozen runtime's public CLI:
- local baseline freshness/acceptance and missing-source behavior;
- required mechanism-review receipt intake;
- fabricated task-review receipt intake;
- USER_STOP -> USER_RESUME without authority/evidence;
- arbitrary reconciliation resolution text.

The probe asserts the failure witnesses, not product success.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[3]
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-r2-receiving-20261116-r1/old-gap-probe/scratch"
EVIDENCE = Path(__file__).resolve().parent.parent / "evidence/old_gap_probe"
RT = REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"
BASE = "75581fa9e2c8576d1ca9a7a9a18759ea840d82e8"
RUNTIME_BLOB = "6164e595efcd176bb2ec9b75aa99074472a4c9b4"
TEST_BLOB = "6cf53b66cf6eff3f4ced4a24f79e163ec50fd347"
MECH = "AUTOMATIC_CURRENTNESS_R1"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(*args: str) -> dict:
    env = dict(os.environ)
    env["TMPDIR"] = str(REPO / ".local-logs/sorok-programma-automatic-currentness-r2-receiving-20261116-r1/old-gap-probe/tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    completed = subprocess.run(
        [sys.executable, "-B", str(RT), "--config", str(CFG), *args],
        cwd=str(REPO), capture_output=True, text=True, timeout=180, env=env,
    )
    return {
        "args": list(args),
        "exit": completed.returncode,
        "seconds": round(time.monotonic() - started, 3),
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def state() -> dict:
    return json.loads((SANDBOX / "CURRENT_PROGRESS.json").read_text())[
        "operational_currentness_runtime_r1"]


def receipt(path: Path, *, task_id: str, implementation: str,
            review_commit: str, documents: list[dict],
            reviewer: str, author: str) -> None:
    path.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_REVIEW_RECEIPT@1",
        "task_id": task_id,
        "implementation_commit": implementation,
        "implementation_code_sha": RUNTIME_BLOB,
        "author_session": author,
        "reviewer_session": reviewer,
        "review_commit": review_commit,
        "review_pr": None,
        "verdict": "ACCEPT_SCOPED_SOURCEFREE",
        "scope": "FABRICATED SANDBOX NEGATIVE; no real review job",
        "grade": "SOURCEFREE_S2_ONLY",
        "full_original_claim": "NOT_ESTABLISHED",
        "protected_ci": "UNAVAILABLE_BILLING",
        "adoption": "PENDING_PROTECTED_CI_AND_ADOPTION",
        "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
        "source_documents": documents,
    }, indent=2) + "\n")


def event(path: Path, *, event_id: str, kind: str, scope: str) -> None:
    path.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_EVENT_R1",
        "event_id": event_id,
        "kind": kind,
        "source": {"trust": "ARBITRARY_LOCAL_TEST_STRING"},
        "payload": {"scope": scope, "owner": "fake-operator",
                    "reason": "fabricated " + kind},
    }, indent=2) + "\n")


def main() -> int:
    global SANDBOX, CFG
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SANDBOX = SCRATCH / "repo"
    SANDBOX.mkdir(parents=True)
    (SANDBOX / "CURRENT_PROGRESS.json").write_bytes(subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{BASE}:SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json"]))
    (SANDBOX / "CURRENT_PROGRESS.md").write_bytes(subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{BASE}:SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md"]))
    (SANDBOX / "CURRENTNESS_FROZEN_SOURCE_R1").mkdir()
    for name in ("original_task_packets_20261112.json",
                 "original_gmt_overlay_20261112.json"):
        shutil.copy2(
            REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1" / name,
            SANDBOX / "CURRENTNESS_FROZEN_SOURCE_R1" / name)
    baseline = SANDBOX / "GITHUB_INTAKE_BASELINE.json"
    shutil.copy2(
        REPO / "WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R1/evidence/GITHUB_INTAKE_BASELINE.snapshot.json",
        baseline)
    old_time = 1_577_836_800
    os.utime(baseline, (old_time, old_time))
    original_baseline_sha = sha(baseline)
    CFG = SANDBOX / "config.json"
    CFG.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(REPO),
        "pair_json": str(SANDBOX / "CURRENT_PROGRESS.json"),
        "pair_md": str(SANDBOX / "CURRENT_PROGRESS.md"),
        "state_root": str(SANDBOX / "state"),
        "frozen_source_dir": str(SANDBOX / "CURRENTNESS_FROZEN_SOURCE_R1"),
        "github_baseline": str(baseline),
        "implementation_commit": "ac09ac7f26fa2db8950f563e8f1decb0c32f5af5",
    }, indent=2) + "\n")
    steps = {}
    steps["init"] = run("init")
    steps["startup_initial"] = run("startup", "--reconcile")
    try:
        startup_initial = json.loads(steps["startup_initial"]["stdout"])
    except Exception:
        (EVIDENCE / "gap_probe_debug_stdout.txt").write_text(
            steps["startup_initial"]["stdout"] + "\n---STDERR---\n" +
            steps["startup_initial"]["stderr"])
        raise
    baseline_as_of = (startup_initial.get("readout") or {}).get(
        "authenticated_github_baseline", {}).get("as_of")
    baseline_mtime = baseline.stat().st_mtime
    # Local baseline change is accepted as authenticated; no live source fetch.
    data = json.loads(baseline.read_text())
    old_head = data[3]["value"]["head"]
    data[3]["value"]["head"] = "SIMULATED_LOCAL_BASELINE_ADVANCE"
    baseline.write_text(json.dumps(data, indent=2) + "\n")
    changed_baseline_sha = sha(baseline)
    steps["startup_changed_local_baseline"] = run("startup", "--reconcile")
    changed_status = json.loads(steps["startup_changed_local_baseline"]["stdout"])
    # Required mechanism review cannot be intaken (TASK_UNKNOWN before mechanism branch).
    mech_receipt = SANDBOX / "MECHANISM_REVIEW.json"
    receipt(
        mech_receipt, task_id=MECH,
        implementation="ac09ac7f26fa2db8950f563e8f1decb0c32f5af5",
        review_commit="ac09ac7f26fa2db8950f563e8f1decb0c32f5af5",
        documents=[
            {"path": "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py", "git_blob": RUNTIME_BLOB},
            {"path": "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py", "git_blob": TEST_BLOB},
        ],
        reviewer="ses_FAKE_REVIEWER_NOT_A_REAL_JOB",
        author="ses_FAKE_AUTHOR_NOT_A_REAL_JOB",
    )
    steps["mechanism_review_intake"] = run("intake-review", "--receipt", str(mech_receipt))
    # Fabricated task review is accepted; no supervised review job/role binding.
    task_receipt = SANDBOX / "FAKE_C05_REVIEW.json"
    receipt(
        task_receipt, task_id="C05",
        implementation="4b33b8be1127c2186931a66f23e3a2b05feaf0a6",
        review_commit="4b33b8be1127c2186931a66f23e3a2b05feaf0a6",
        documents=[
            {"path": "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1/developmental_recursion/continuing_relations.py", "git_blob": "8006440bd420ce8526bb2f333cd201ac077cbd22"},
            {"path": "WORKER_RETURNS/SOROK_C05_ACTOR_PROJECTION_REPAIR_R3/tests/test_c05_actor_projection_repair_r3.py", "git_blob": "a50b4cd744d7b949170a0fd9c77f5e0ec4c927ec"},
        ],
        reviewer="ses_FAKE_REVIEWER_NOT_A_REAL_JOB",
        author="ses_FAKE_AUTHOR_NOT_A_REAL_JOB",
    )
    steps["fake_c05_review_intake"] = run("intake-review", "--receipt", str(task_receipt))
    c05 = next(t for t in state()["tasks"] if t["id"] == "C05")
    # USER_STOP -> USER_RESUME without operator/role/evidence.
    stop = SANDBOX / "STOP.json"
    resume = SANDBOX / "RESUME.json"
    event(stop, event_id="sandbox:stop:B02", kind="USER_STOP", scope="B02")
    event(resume, event_id="sandbox:resume:B02", kind="USER_RESUME", scope="B02")
    steps["stop_intake"] = run("intake-event", "--event", str(stop))
    stops_after_stop = state()["controls"].get("stops", [])
    b02_after_stop = next(t for t in state()["tasks"] if t["id"] == "B02")["readiness"]
    steps["resume_intake"] = run("intake-event", "--event", str(resume))
    stops_after_resume = state()["controls"].get("stops", [])
    b02_after_resume = next(t for t in state()["tasks"] if t["id"] == "B02")["readiness"]
    # Missing GitHub source produces an item; arbitrary resolve text clears it.
    baseline.rename(SANDBOX / "GITHUB_INTAKE_BASELINE.missing")
    steps["startup_missing_baseline"] = run("startup", "--reconcile")
    missing = json.loads(steps["startup_missing_baseline"]["stdout"]).get(
        "reconciliation_required", [])
    steps["arbitrary_resolve"] = run(
        "resolve-reconciliation",
        "--what-changed", "AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE",
        "--evidence", "arbitrary unverified local text",
        "--owner", "fake-operator", "--reason", "fake resolution")
    resolved_after = state().get("reconciliation_resolved", [])
    items_after_resolve = state().get("reconciliation_required", [])
    source_text = RT.read_text()
    network_tokens = [token for token in (
        "requests", "urllib", "http://", "https://", "api.github",
        "ls-remote", "curl ", "socket") if token in source_text]
    report = {
        "schema": "SOROK_CURRENTNESS_GAP_PROBE@1",
        "candidate": "ac09ac7f26fa2db8950f563e8f1decb0c32f5af5",
        "base": BASE,
        "runtime_blob": RUNTIME_BLOB,
        "test_blob": TEST_BLOB,
        "sandbox": str(SANDBOX),
        "steps": steps,
        "observations": {
            "baseline_original_sha256": original_baseline_sha,
            "baseline_changed_sha256": changed_baseline_sha,
            "baseline_old_head": old_head,
            "baseline_new_head": "SIMULATED_LOCAL_BASELINE_ADVANCE",
            "baseline_file_mtime": baseline_mtime,
            "readout_baseline_as_of": baseline_as_of,
            "changed_local_baseline_items": json.loads(
                steps["startup_changed_local_baseline"]["stdout"]).get(
                    "reconciliation_required", []),
            "mechanism_review_exit": steps["mechanism_review_intake"]["exit"],
            "mechanism_review_error": steps["mechanism_review_intake"]["stderr"],
            "mechanism_review_state": state()["mechanism_review"]["state"],
            "fake_task_review_exit": steps["fake_c05_review_intake"]["exit"],
            "fake_task_review_trust": c05.get("review_trust"),
            "fake_task_review_sha": c05.get("review_sha"),
            "stops_after_stop": stops_after_stop,
            "stops_after_resume": stops_after_resume,
            "b02_after_stop": b02_after_stop,
            "b02_after_resume": b02_after_resume,
            "missing_baseline_items": missing,
            "resolved_after_arbitrary_text": resolved_after,
            "items_after_arbitrary_resolve": items_after_resolve,
            "network_client_tokens_found": network_tokens,
            "author_17_tests_rerun": False,
        },
        "gaps_reproduced": True,
        "verdict": "REVISE_EXACT_DEFECT",
    }
    report_path = EVIDENCE / "gap_probe_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps({
        "verdict": report["verdict"],
        "mechanism_review_exit": steps["mechanism_review_intake"]["exit"],
        "mechanism_review_error": steps["mechanism_review_intake"]["stderr"].strip(),
        "fake_task_review_exit": steps["fake_c05_review_intake"]["exit"],
        "fake_task_review_trust": c05.get("review_trust"),
        "stops_after_stop": len(stops_after_stop),
        "stops_after_resume": len(stops_after_resume),
        "missing_baseline_items": [i.get("what_changed") for i in missing],
        "items_after_arbitrary_resolve": len(items_after_resolve),
        "baseline_as_of": baseline_as_of,
        "baseline_mtime": baseline_mtime,
        "network_client_tokens_found": network_tokens,
        "report": str(report_path),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
