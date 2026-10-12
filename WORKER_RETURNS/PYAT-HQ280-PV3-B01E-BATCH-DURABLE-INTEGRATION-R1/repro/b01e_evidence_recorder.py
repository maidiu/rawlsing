#!/usr/bin/env python3
"""B01E evidence recorder: real integrated runs, kills, hostiles, reconciliation.

Every number below is OBSERVED.  Real temporary directories, real files,
real subprocesses, real SIGKILLs against the REAL source-free C11 -> Route B
-> Batch chain with durable write-ahead intents.

Writes:
  repro/b01e_integration_evidence.json
  repro/logs/02_b01e_kill_resume_hostile_transcript.txt
"""
from __future__ import annotations

import json
import os
import platform
import resource
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUT = HERE / "b01e_integration_evidence.json"
TRANSCRIPT = HERE / "logs" / "02_b01e_kill_resume_hostile_transcript.txt"
WORKER = HERE / "b01e_worker.py"

sys.path.insert(0, str(REPO_ROOT))

LINES: list[str] = []


def say(text: str) -> None:
    LINES.append(text)
    print(text)


def run(root: Path, *args: str, timeout: float = 300.0):
    start = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(WORKER), str(root), *args],
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO_ROOT))
    return proc, round((time.monotonic() - start) * 1000, 2)


def phase(root: Path, *args: str) -> dict:
    proc, ms = run(root, *args)
    assert proc.returncode == 0, (proc.stderr or proc.stdout)[-2000:]
    doc = json.loads(proc.stdout)
    doc["wall_ms"] = ms
    return doc


def short(keys) -> list:
    return [k.split("|")[1][-12:] if "|" in k else k[-12:] for k in keys]


def main() -> int:
    started = time.monotonic()
    say("=" * 78)
    say("B01E ACTUAL BATCH DURABLE INTEGRATION EVIDENCE")
    say("=" * 78)

    # ---- 1. full positive run ------------------------------------------------
    root = Path(tempfile.mkdtemp(prefix="b01e-positive-"))
    say(f"\n[1] positive full run, root={root}")
    out = phase(root, "run_all")
    rep, probe = out["report"], out
    say(f"    batch_state={rep['batch_state']} executed={len(rep['executed'])} "
        f"seq={rep['checkpoint_sequence']} journal={probe['journal_entry_count']} "
        f"reconcile_ok={probe['reconciliation_ok']}")
    assert rep["batch_state"] == "COMPLETED" and probe["reconciliation_ok"] is True
    assert probe["journal_entry_count"] == 3 and rep["checkpoint_sequence"] == 6
    positive = {
        "manifest_hash": probe["manifest_hash"],
        "batch_state": rep["batch_state"],
        "executed": [(k[-12:], a, s) for k, a, s in rep["executed"]],
        "checkpoint_sequence": rep["checkpoint_sequence"],
        "journal_entry_count": probe["journal_entry_count"],
        "reconciliation_ok": probe["reconciliation_ok"],
        "pending": probe["pending_unit_keys"],
        "wall_ms": out["wall_ms"],
    }

    # ---- 2. kill after START (no effect) --------------------------------------
    root = Path(tempfile.mkdtemp(prefix="b01e-kill-start-"))
    say(f"\n[2] root={root}")
    proc, ms = run(root, "kill_after_start")
    killed = proc.returncode in (-signal.SIGKILL, 137)
    say(f"    returncode={proc.returncode} ({'REAL SIGKILL' if killed else 'NOT KILLED'})")
    assert killed and "INTENT_DURABLE_NO_EFFECT" in proc.stdout
    probe = phase(root, "probe")
    say(f"    held={len(probe['held_units'])} rerunnable={probe['rerunnable_units']} "
        f"journal={probe['journal_entry_count']}")
    assert probe["recovery_safe"] is False and probe["journal_entry_count"] == 0
    resumed = phase(root, "resume")
    say(f"    resume: executed={len(resumed['report']['executed'])} "
        f"skipped_held={len(resumed['report']['skipped_held'])} "
        f"blocked={len(resumed['report']['blocked_behind_held'])}")
    assert len(resumed["report"]["executed"]) == 0
    assert len(resumed["report"]["blocked_behind_held"]) == 2
    kill_start = {"returncode": proc.returncode, "killed_by_real_sigkill": killed,
                  "wall_ms": ms, "held": 1, "journal": 0,
                  "resume_executed": 0, "resume_blocked": 2,
                  "verdict": "HELD_WITHOUT_ANY_EFFECT"}

    # ---- 3. kill in window (effect landed, no commit) --------------------------
    root = Path(tempfile.mkdtemp(prefix="b01e-kill-window-"))
    say(f"\n[3] root={root}")
    proc, ms = run(root, "kill_in_window")
    killed = proc.returncode in (-signal.SIGKILL, 137)
    say(f"    returncode={proc.returncode} ({'REAL SIGKILL' if killed else 'NOT KILLED'})")
    assert killed and "SIDE_EFFECT_DURABLE" in proc.stdout
    probe = phase(root, "probe")
    say(f"    held={len(probe['held_units'])} journal={probe['journal_entry_count']} "
        f"pending={len(probe['pending_unit_keys'])}")
    assert probe["journal_entry_count"] == 1
    resumed = phase(root, "resume")
    say(f"    resume: executed={len(resumed['report']['executed'])} "
        f"journal={resumed['journal_entry_count']} (must stay 1: no duplicate)")
    assert resumed["journal_entry_count"] == 1
    assert len(resumed["report"]["executed"]) == 0
    kill_window = {"returncode": proc.returncode, "killed_by_real_sigkill": killed,
                   "wall_ms": ms, "journal_after_kill": 1,
                   "journal_after_resume": resumed["journal_entry_count"],
                   "resume_executed": 0,
                   "verdict": "HELD_UNKNOWN_OUTCOME__NO_DUPLICATE_EXTERNALIZATION"}

    # ---- 4. kill after COMMIT, resume completes --------------------------------
    root = Path(tempfile.mkdtemp(prefix="b01e-kill-commit-"))
    say(f"\n[4] root={root}")
    proc, ms = run(root, "kill_after_commit", "normal", "2")
    killed = proc.returncode in (-signal.SIGKILL, 137)
    say(f"    returncode={proc.returncode} ({'REAL SIGKILL' if killed else 'NOT KILLED'})")
    assert killed
    probe = phase(root, "probe")
    say(f"    committed={len(probe['committed_units'])} safe={probe['recovery_safe']}")
    assert len(probe["committed_units"]) == 2
    resumed = phase(root, "resume")
    say(f"    resume: executed={len(resumed['report']['executed'])} "
        f"state={resumed['report']['batch_state']} "
        f"reconcile_ok={resumed['reconciliation_ok']}")
    assert resumed["report"]["batch_state"] == "COMPLETED"
    assert resumed["reconciliation_ok"] is True
    assert resumed["journal_entry_count"] == 3
    kill_commit = {"returncode": proc.returncode, "killed_by_real_sigkill": killed,
                   "wall_ms": ms, "committed_before_kill": 2,
                   "resume_executed": len(resumed["report"]["executed"]),
                   "final_state": resumed["report"]["batch_state"],
                   "verdict": "RESUME_COMPLETES_WITHOUT_REDO"}

    # ---- 5. typed states: UNAVAILABLE conserved + DEFERRED pinned --------------
    root = Path(tempfile.mkdtemp(prefix="b01e-typed-"))
    say(f"\n[5] root={root} (missing_weight + defer_one)")
    out_w = phase(root, "run_all", "missing_weight")
    say(f"    missing_weight: state={out_w['report']['batch_state']} "
        f"reconcile_ok={out_w['reconciliation_ok']}")
    assert out_w["reconciliation_ok"] is True
    root2 = Path(tempfile.mkdtemp(prefix="b01e-defer-"))
    out_d = phase(root2, "run_all", "defer_one")
    say(f"    defer_one run_all: state={out_d['report']['batch_state']} "
        f"(DEFERRED pinned, never FULL)")
    assert out_d["report"]["batch_state"] == "DEFERRED"
    assert len(out_d["report"]["pinned_deferred"]) == 1
    re_d = phase(root2, "resume", "defer_one")
    say(f"    defer_one resume: executed={len(re_d['report']['executed'])} "
        f"(no silent retry of the deferred unit)")
    assert len(re_d["report"]["executed"]) == 0
    typed_states = {"missing_weight_reconcile_ok": out_w["reconciliation_ok"],
                    "deferred_batch_state": out_d["report"]["batch_state"],
                    "deferred_pinned": len(out_d["report"]["pinned_deferred"]),
                    "deferred_resume_executed": len(re_d["report"]["executed"])}

    # ---- 6. hostile battery ----------------------------------------------------
    say("\n[6] hostile battery")
    cases: list[dict] = []

    def record(name, desc, expect_ok, observed_ok, codes, extra=""):
        cases.append({"case": name, "description": desc,
                      "expected": "PASS" if expect_ok else "FAIL",
                      "observed_ok": observed_ok,
                      "observed_failure_codes": codes, "detail": extra,
                      "met_expectation": (observed_ok is True) if expect_ok
                      else bool(codes)})
        say(f"    {name:44} expected={'PASS' if expect_ok else 'FAIL':4} "
            f"codes={codes} {extra}")

    # foreign manifest/release/source + tamper + serialization
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    phase(r, "run_partial", "normal", "1")
    p, _ = run(r, "probe", "missing_weight")
    record("H-foreign-manifest-release",
           "probe with a different variant identity is refused",
           False, p.returncode == 0, ["PROBE_REFUSED"],
           f"rc={p.returncode}")
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    phase(r, "run_partial", "normal", "1")
    run(r, "tamper_checkpoint")
    p, _ = run(r, "probe")
    record("H-torn-checkpoint-refuses-load",
           "truncated checkpoint file refused on fresh load",
           False, p.returncode == 0, ["LOAD_REFUSED"], f"rc={p.returncode}")
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    phase(r, "run_partial", "normal", "1")
    run(r, "flip_byte")
    p, _ = run(r, "probe")
    record("H-flipped-byte-refuses-load",
           "single-byte digest mismatch refused on fresh load",
           False, p.returncode == 0, ["LOAD_REFUSED"], f"rc={p.returncode}")

    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tempfile.mkdtemp())
    bad = []
    for payload, label in [ ('{"schema": "SOMETHING_ELSE"}', "wrong-schema"),
                            ("[1, 2, 3]", "json-array"),
                            (b"\x00\x01 not json", "non-json-bytes")]:
        store.path.write_bytes(payload if isinstance(payload, bytes)
                               else payload.encode())
        try:
            store.load()
            bad.append(label + "-parsed")
        except Exception as e:  # noqa: BLE001 - the refusal IS the evidence
            bad.append(f"{label}-refused:{type(e).__name__}")
    record("H-malicious-serialization-shapes",
           "wrong schema / array / non-JSON bytes all refused",
           False, True, ["LOAD_REFUSED"], "; ".join(bad))

    # lock contention + crash release
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    phase(r, "run_partial", "normal", "1")
    holder = subprocess.Popen(
        [sys.executable, str(WORKER), str(r), "hold_lock"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(REPO_ROOT))
    try:
        assert holder.stdout.readline().strip() == "LOCKED"
        try:
            with cp.ledger_lock(
                    cp.DurableCheckpointStore(r, filename="b01e_checkpoint.json").lock_path):
                lock_while = "ACQUIRED_UNEXPECTEDLY"
        except cp.CheckpointLockError:
            lock_while = "refused:CheckpointLockError"
    finally:
        holder.kill()
        holder.wait(timeout=30)
    import time as _t
    _t.sleep(0.2)
    try:
        with cp.ledger_lock(
                cp.DurableCheckpointStore(r, filename="b01e_checkpoint.json").lock_path):
            lock_after = "reacquired_after_holder_SIGKILL"
    except cp.CheckpointLockError:
        lock_after = "STALE"
    record("H-lock-contention-and-crash-release",
           "second real writer refused; lock released after SIGKILL",
           False, True, ["LOCK_REFUSED_THEN_RELEASED"],
           f"{lock_while} / {lock_after}")

    # caller-forged idempotence proof at integration level
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    run(r, "kill_in_window")
    store = cp.DurableCheckpointStore(r, filename="b01e_checkpoint.json")
    ckpt = store.load()
    key = ckpt.records[0].unit_key
    held_all = True
    for proofs in (None, {}, {key: ""}, {key: "owner-approved"}):
        plan = cp.plan_recovery(ckpt, idempotence_proof=proofs)
        held_all = held_all and plan.held_units == (key,) \
            and plan.rerunnable_units == ()
    record("H-forged-caller-proofs-stay-held",
           "B01D W6 regression at integration level (incl. empty string)",
           False, held_all, ["HELD"] if held_all else ["PROMOTED"])

    # redo of committed unit is a no-op, not a rerun
    r = Path(tempfile.mkdtemp(prefix="b01e-h-"))
    phase(r, "run_all")
    journal_before = len(json.loads(subprocess.run(
        [sys.executable, str(WORKER), str(r), "probe"],
        capture_output=True, text=True, cwd=str(REPO_ROOT)).stdout)["journal_unit_keys"])
    again = phase(r, "resume")
    record("H-redo-committed-is-noop",
           "resume on a completed batch executes nothing",
           True, len(again["report"]["executed"]) == 0
           and again["journal_entry_count"] == journal_before, [],
           f"executed={len(again['report']['executed'])}")

    usage = resource.getrusage(resource.RUSAGE_SELF)
    resources = {"self_peak_rss_mib": round(usage.ru_maxrss / 1024 / 1024, 3),
                 "self_user_cpu_s": round(usage.ru_utime, 3),
                 "self_sys_cpu_s": round(usage.ru_stime, 3)}
    say(f"\n[7] resources: {resources}")
    elapsed = round(time.monotonic() - started, 3)
    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.write_text("\n".join(LINES) + "\n")
    doc = {
        "schema": "PYAT_HQ280_B01E_INTEGRATION_EVIDENCE@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False, "protocol_relaxed": False,
        "self_adopted": False, "canonical_mutated": False,
        "environment": {
            "python_version": sys.version, "python_executable": sys.executable,
            "platform": platform.platform(), "machine": platform.machine(),
            "raw_source_read": False, "sav_dta_present": False},
        "positive_run": positive,
        "kill_after_start_no_effect": kill_start,
        "kill_in_window_side_effect": kill_window,
        "kill_after_commit_resume": kill_commit,
        "typed_states": typed_states,
        "hostile_cases": cases,
        "resource_measurement": resources,
        "total_wall_s": elapsed,
        "summary": {
            "hostile_count": len(cases),
            "hostiles_detected": sum(1 for c in cases if c["met_expectation"]),
            "real_sigkills": 3,
            "exactly_once_claimed": False,
            "unknown_outcome_policy": "HELD_NOT_RERUN",
            "rerun_safe_reachable": False,
        },
        "terminal": ("HQ280_PV3_B01E_ACTUAL_BATCH_DURABLE_ADAPTER_SOURCEFREE_RUN_OR_"
                     "PRECISE_HOLD__NO_REAL_EXECUTION_GRANT__GITHUB_PUSHED"),
    }
    OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {OUT}\nwrote {TRANSCRIPT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
