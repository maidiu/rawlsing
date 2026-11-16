#!/usr/bin/env python3
"""Independent R2 material-event and residual-authority probe.

Read-only product. Builds a reviewer-owned sandbox from the preserved base
pair and frozen source, then exercises the public CLI. The probe records
whether the R1 five reds are refused and whether additional material event
kinds remain caller-mintable. It is a review witness, not a product pass.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

REPO = Path(__file__).resolve().parents[3]
REV = Path(__file__).resolve().parent.parent
SCRATCH = REPO / ".local-logs/sorok-programma-automatic-currentness-r3-receiving-20261116-r1/material-auth-probe"
BASE = "75581fa9e2c8576d1ca9a7a9a18759ea840d82e8"
RT = REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"
PY = sys.executable


def run(*args: str) -> dict:
    env = dict(os.environ)
    env["TMPDIR"] = str(SCRATCH / "tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    started = time.monotonic()
    proc = subprocess.run([PY, "-B", str(RT), "--config", str(CFG), *args],
                          cwd=str(REPO), capture_output=True, text=True,
                          timeout=180, env=env)
    return {"args": list(args), "exit": proc.returncode,
            "seconds": round(time.monotonic() - started, 3),
            "stdout": proc.stdout, "stderr": proc.stderr}


def read_state() -> dict:
    value = json.loads((SANDBOX / "CURRENT_PROGRESS.json").read_text())
    return value["operational_currentness_runtime_r1"]


def write_event(name: str, kind: str, payload: dict, source=None) -> Path:
    path = SANDBOX / (name + ".json")
    path.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_EVENT_R1", "event_id": name,
        "kind": kind, "recorded_utc": "2026-11-16T06:30:00+00:00",
        "source": source or {"trust": "ARBITRARY_LOCAL_TEST_STRING"},
        "payload": payload,
    }, indent=2) + "\n")
    return path


def main() -> int:
    global SANDBOX, CFG
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SANDBOX = SCRATCH / "repo"
    SANDBOX.mkdir(parents=True)
    (SANDBOX / "state").mkdir()
    (SANDBOX / "controller-state").mkdir()
    frozen = SANDBOX / "CURRENTNESS_FROZEN_SOURCE_R1"
    frozen.mkdir()
    for name in ("CURRENT_PROGRESS.json", "CURRENT_PROGRESS.md"):
        (SANDBOX / name).write_bytes(subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{BASE}:SOROK_PRODUCT_CONTROL_ROOM/{name}"]))
    for path in (REPO / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1").glob("*.json"):
        shutil.copy2(path, frozen / path.name)
    CFG = SANDBOX / "config.json"
    CFG.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1",
        "repo_root": str(REPO),
        "pair_json": str(SANDBOX / "CURRENT_PROGRESS.json"),
        "pair_md": str(SANDBOX / "CURRENT_PROGRESS.md"),
        "state_root": str(SANDBOX / "state"),
        "frozen_source_dir": str(frozen),
        "controller_state_root": str(SANDBOX / "controller-state"),
        "implementation_commit": "ea5e48cf3240e72e39cd19be3120ad727902eee2",
        "github_baseline": None,
    }, indent=2) + "\n")
    (SCRATCH / "tmp").mkdir()
    steps = {"init": run("init")}
    gaps = []
    fixed = []

    # R1 red 2: a caller-provided receipt must not be enough without a
    # supervised REVIEWER run.
    fake_receipt = SANDBOX / "mechanism_receipt.json"
    fake_receipt.write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_REVIEW_RECEIPT@1",
        "task_id": "AUTOMATIC_CURRENTNESS_R1",
        "implementation_commit": "ea5e48cf3240e72e39cd19be3120ad727902eee2",
        "author_session": "ses_e21a481bfffefyvpxaeFaAOFvQ",
        "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
        "review_commit": "4de807fa3f27c3aab5d443083b6cb020c80fda31",
        "verdict": "REVISE_EXACT_DEFECT", "scope": "FAKE",
        "full_original_claim": "NOT_ESTABLISHED",
        "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
        "source_documents": [],
    }, indent=2) + "\n")
    steps["caller_only_mechanism_review"] = run(
        "intake-review", "--receipt", str(fake_receipt))
    if steps["caller_only_mechanism_review"]["exit"] == 1 and \
            "REVIEW_SUPERVISED_RUN_REQUIRED" in steps["caller_only_mechanism_review"]["stderr"]:
        fixed.append("caller-only mechanism review refused")
    else:
        gaps.append("caller-only mechanism review accepted")

    # R1 red 4: arbitrary STOP must not mint control authority.
    stop = write_event("evil-stop", "USER_STOP", {
        "scope": "B02", "owner": "fake", "reason": "arbitrary"})
    steps["arbitrary_stop"] = run("intake-event", "--event", str(stop))
    if steps["arbitrary_stop"]["exit"] == 1 and \
            "OPERATOR_AUTHORIZATION_UNAVAILABLE" in steps["arbitrary_stop"]["stderr"]:
        fixed.append("arbitrary STOP refused")
    else:
        gaps.append("arbitrary STOP accepted")

    # R1 red 5: arbitrary resolution text must not clear an item.
    steps["arbitrary_resolve"] = run(
        "resolve-reconciliation", "--what-changed", "LIVE_GITHUB_REF_FETCH_UNAVAILABLE")
    if steps["arbitrary_resolve"]["exit"] == 1 and \
            "RESOLUTION_AUTHENTICATION_REQUIRED" in steps["arbitrary_resolve"]["stderr"]:
        fixed.append("arbitrary resolution refused")
    else:
        gaps.append("arbitrary resolution accepted")

    # Material gap: rejection is an unauthenticated public event.
    reject = write_event("evil-reject", "REJECTION", {
        "task_id": "B01", "owner": "fake", "reason": "arbitrary"})
    steps["untrusted_rejection"] = run("intake-event", "--event", str(reject))
    b01 = next(t for t in read_state()["tasks"] if t["id"] == "B01")
    if steps["untrusted_rejection"]["exit"] == 0 and b01["execution_state"] == "REJECTED":
        gaps.append("untrusted REJECTION accepted and changed B01")
    else:
        fixed.append("untrusted REJECTION refused")

    # Material gap: protected integration is an unauthenticated public event.
    protect = write_event("evil-protected", "PROTECTED_INTEGRATION", {
        "task_id": "B05", "owner": "fake", "ci_state": "PASS",
        "merge_sha": "f" * 40})
    steps["untrusted_protected_integration"] = run(
        "intake-event", "--event", str(protect))
    b05 = next(t for t in read_state()["tasks"] if t["id"] == "B05")
    if steps["untrusted_protected_integration"]["exit"] == 0 and \
            b05.get("protected_integration") == "PROTECTED_SOURCEFREE" and \
            b05.get("protected_ci") == "PASS":
        gaps.append("untrusted PROTECTED_INTEGRATION accepted and minted PASS")
    else:
        fixed.append("untrusted PROTECTED_INTEGRATION refused")

    # Material gap: GITHUB_OBSERVATION is accepted from public CLI without
    # authenticating the observation or its digest.
    fake_live = {
        "schema": "SOROK_LIVE_GITHUB_OBSERVATION@1",
        "source_trust": "AUTHENTICATED_LIVE_GITHUB",
        "source_identity": "FAKE_SOURCE", "transport": "fake",
        "fetched_at_utc": "2026-11-16T06:30:00+00:00",
        "expires_at_utc": "2099-01-01T00:00:00+00:00", "ttl_seconds": 900,
        "refs": {}, "refs_digest": "0" * 64,
        "api": {"repo": {"http_status": 200}, "pulls": {}, "issues": {},
                "comments": {}, "commits": {}, "token_available": True,
                "token_error": None},
        "status_coverage": "REF_SHA_ONLY", "status_checks": 0,
        "status_success": 0, "credential_helper_used": True,
        "credential_error": None, "evidence_digest": "evil",
    }
    live_event = write_event("evil-live", "GITHUB_OBSERVATION",
                             {"live_observation": fake_live})
    steps["unauthenticated_live_observation"] = run(
        "intake-event", "--event", str(live_event))
    live = read_state()["authenticated_checkpoint"].get("live_github") or {}
    if steps["unauthenticated_live_observation"]["exit"] == 0 and \
            live.get("source_identity") == "FAKE_SOURCE":
        gaps.append("unauthenticated GITHUB_OBSERVATION accepted as live")
    else:
        fixed.append("unauthenticated GITHUB_OBSERVATION refused")

    # Material gap: a self-consistent local controller run can mint a worker
    # return; no actual process or trusted controller root is checked.
    fake_run = SCRATCH / "fake-worker-run"
    work = fake_run / "worktree"
    (work / "return").mkdir(parents=True)
    job = {"job_id": "fake-worker-job", "session": "ses_FAKE_WORKER_NO_PROCESS",
           "grant_id": "fake-grant", "argv": ["/usr/bin/true"]}
    binding = {"session": job["session"], "worktree": str(work),
               "recipient_thread": "00000000-0000-4000-8000-000000000000",
               "grant": {"id": "fake-grant", "argv_sha256": hashlib.sha256(
                   json.dumps(job["argv"], separators=(",", ":")).encode()).hexdigest()},
               "sorok_currentness": {"role": "IMPLEMENTER",
                   "task_id": "AUTOMATIC_CURRENTNESS_R1",
                   "return_filename": "return/WORKER_RETURN.json"}}
    for name, value in (
            ("job.json", job), ("binding.json", binding),
            ("launch.json", {"job_id": job["job_id"], "child_pid": 99999}),
            ("process.json", {"pid": 99999}),
            ("completion.json", {"job_id": job["job_id"], "session": job["session"],
                                 "pid": 99999, "exit_code": 0})):
        (fake_run / name).write_text(json.dumps(value, indent=2) + "\n")
    (work / "return/WORKER_RETURN.json").write_text(json.dumps({
        "schema": "SOROK_CURRENTNESS_WORKER_RETURN@1",
        "task_id": "AUTOMATIC_CURRENTNESS_R1", "role": "IMPLEMENTER",
        "session": "ses_FAKE_WORKER_NO_PROCESS",
        "implementation_commit": "ea5e48cf3240e72e39cd19be3120ad727902eee2",
        "runtime_blob": "d06cd8a9a736fac728ea6b5ea2c098aa4986cfa0",
        "test_blob": "202e81d85d78e4d158a43bfcfa55a818149bf8fd",
        "return_paths": {}, "scope": "FAKE"}, indent=2) + "\n")
    steps["fake_worker_return"] = run(
        "intake-completion", "--run-dir", str(fake_run))
    worker = read_state().get("mechanism_worker_return") or {}
    if steps["fake_worker_return"]["exit"] == 0 and \
            worker.get("session") == "ses_FAKE_WORKER_NO_PROCESS":
        gaps.append("self-consistent fake WORKER_RETURN accepted")
    else:
        fixed.append("self-consistent fake WORKER_RETURN refused")

    result = {"schema": "SOROK_AUTOMATIC_CURRENTNESS_R2_MATERIAL_AUTH_PROBE@1",
              "base": BASE,
              "implementation": "ea5e48cf3240e72e39cd19be3120ad727902eee2",
              "fixed": fixed, "gaps": gaps, "steps": steps,
              "state_snapshot": {
                  "generation": read_state()["generation"],
                  "checkpoint_id": read_state()["checkpoint_id"],
                  "b01": b01, "b05": b05,
                  "live": live,
                  "mechanism_worker_return": worker,
              },
              "verdict": "REVISE_EXACT_DEFECT" if gaps else "PASS",
              "note": "Probe asserts both repaired R1 reds and residual material-event authority gaps; existence of gaps is the review result."}
    out = REV / "evidence" / "material_auth_probe_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"verdict": result["verdict"], "fixed": fixed,
                      "gaps": gaps, "report": str(out)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
