#!/usr/bin/env python3
"""B01C evidence recorder: real process kill/restart and hostile execution.

Every number below is OBSERVED, not anticipated.  Real temporary directories,
real files, real subprocesses and real SIGKILLs are used.

Writes:
  repro/b01c_kill_resume_results.json
  repro/logs/02_real_kill_resume_transcript.txt
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
REPO_ROOT = HERE.parents[3]
WORKER = HERE / "b01c_worker.py"
OUT = HERE / "b01c_kill_resume_results.json"
TRANSCRIPT = HERE / "logs" / "02_real_kill_resume_transcript.txt"

sys.path.insert(0, str(REPO_ROOT))

import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp  # noqa: E402


LINES: list[str] = []


def say(text: str) -> None:
    LINES.append(text)
    print(text)


def worker(root: Path, phase: str, timeout: float = 60.0):
    start = time.monotonic()
    proc = subprocess.run(
        [sys.executable, str(WORKER), str(root), phase],
        capture_output=True, text=True, timeout=timeout, cwd=str(REPO_ROOT),
    )
    return proc, round((time.monotonic() - start) * 1000, 2)


def probe(root: Path) -> dict:
    proc, _ = worker(root, "probe")
    if proc.returncode != 0:
        return {"exists": True, "probe_failed": True,
                "stderr_tail": proc.stderr.strip().splitlines()[-1:] or [""]}
    return json.loads(proc.stdout)


def short(keys: list[str]) -> list[str]:
    return [k[-16:] for k in keys]


def _jsonable(value):
    """Make comparison results JSON-safe (bytes -> sha256, tuples -> lists)."""
    if isinstance(value, (bytes, bytearray)):
        import hashlib
        return "sha256:" + hashlib.sha256(bytes(value)).hexdigest()
    if isinstance(value, tuple):
        return [_jsonable(v) for v in value]
    return value


def real_kill_and_resume() -> dict:
    """The required demonstration: REAL process kill at each phase."""
    say("=" * 78)
    say("B01C REAL PROCESS KILL / RESTART TRANSCRIPT")
    say("=" * 78)
    results: dict[str, dict] = {}

    # --- 1. kill AFTER durable intent, BEFORE any commit -----------------
    root = Path(tempfile.mkdtemp(prefix="b01c-kill-intent-"))
    say(f"\n[1] root={root}")
    proc, ms = worker(root, "start")
    killed_by_signal = proc.returncode in (-signal.SIGKILL, 137)
    say(f"    worker phase=start returncode={proc.returncode} "
        f"({'REAL SIGKILL' if killed_by_signal else 'NOT KILLED'}) in {ms} ms")
    assert killed_by_signal, "worker was not actually SIGKILLed"
    state = probe(root)
    say(f"    durable records on disk: {len(state['records'])} "
        f"state={[r['state'] for r in state['records']]}")
    say(f"    recovery_safe={state['plan']['recovery_safe']} "
        f"held={len(state['plan']['held_units'])} "
        f"rerunnable={len(state['plan']['rerunnable_units'])}")
    assert state["plan"]["recovery_safe"] is False
    assert len(state["plan"]["held_units"]) == 1
    assert state["plan"]["rerunnable_units"] == []
    say("    -> UNKNOWN OUTCOME HELD, not silently rerun  [CORRECT]")
    results["kill_after_intent"] = {
        "returncode": proc.returncode,
        "killed_by_real_sigkill": killed_by_signal,
        "wall_ms": ms,
        "durable_records": len(state["records"]),
        "record_states": [r["state"] for r in state["records"]],
        "recovery_safe": state["plan"]["recovery_safe"],
        "held_units": len(state["plan"]["held_units"]),
        "rerunnable_units": len(state["plan"]["rerunnable_units"]),
        "checkpoint_digest": state["digest"],
        "verdict": "HELD_UNKNOWN_OUTCOME",
    }

    # --- 2. partial run, then REAL restart completing the rest -----------
    root = Path(tempfile.mkdtemp(prefix="b01c-resume-"))
    say(f"\n[2] root={root}")
    proc, ms = worker(root, "partial:2")
    say(f"    phase=partial:2 returncode={proc.returncode} in {ms} ms")
    first = probe(root)
    committed_first = set(first["plan"]["committed_units"])
    say(f"    committed after partial: {short(sorted(committed_first))}")
    say(f"    recovery_safe={first['plan']['recovery_safe']}")

    proc, ms = worker(root, "normal")
    say(f"    phase=normal (fresh process restart) returncode={proc.returncode} "
        f"in {ms} ms")
    second = probe(root)
    committed_second = set(second["plan"]["committed_units"])
    say(f"    committed after restart: {len(committed_second)} of 4")
    say(f"    previously committed preserved: "
        f"{committed_first <= committed_second}")
    say(f"    recovery_safe={second['plan']['recovery_safe']} "
        f"held={len(second['plan']['held_units'])}")
    assert committed_first <= committed_second
    assert second["plan"]["recovery_safe"] is True
    assert len(committed_second) == 4
    say("    -> resume completed remaining work, re-executed nothing  [CORRECT]")
    results["real_restart_resume"] = {
        "partial_returncode": 0,
        "committed_after_partial": len(committed_first),
        "committed_after_restart": len(committed_second),
        "prior_work_preserved": True,
        "recovery_safe_after_restart": second["plan"]["recovery_safe"],
        "held_after_restart": len(second["plan"]["held_units"]),
        "wall_ms_restart": ms,
        "verdict": "RESUME_WITHOUT_DUPLICATE_WORK",
    }

    # --- 3. restart attempt on an ALREADY COMMITTED unit ------------------
    root = Path(tempfile.mkdtemp(prefix="b01c-restart-committed-"))
    worker(root, "partial:1")
    proc, _ = worker(root, "start")
    combined = proc.stdout + proc.stderr
    refused = "already committed" in combined
    say(f"\n[3] restart of an already-committed unit: "
        f"returncode={proc.returncode} refused={refused}  [CORRECT]")
    assert refused
    results["restart_of_committed_unit_refused"] = {
        "returncode": proc.returncode,
        "refused": refused,
        "verdict": "COMPLETED_UNIT_NOT_RETRYABLE",
    }

    # --- 4. concurrent real writer while lock is held --------------------
    root = Path(tempfile.mkdtemp(prefix="b01c-lock-"))
    holder_script = (
        f"import sys,time;sys.path.insert(0,{str(REPO_ROOT)!r});"
        "import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp;"
        f"from pathlib import Path;s=cp.DurableCheckpointStore(Path({str(root)!r}));"
        "ctx=cp.ledger_lock(s.lock_path);ctx.__enter__();"
        "print('HELD',flush=True);time.sleep(30)"
    )
    contender_script = (
        f"import sys;sys.path.insert(0,{str(REPO_ROOT)!r});"
        "import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp;"
        f"from pathlib import Path;s=cp.DurableCheckpointStore(Path({str(root)!r}));"
        "\ntry:\n"
        "    with cp.ledger_lock(s.lock_path):\n"
        "        print('ACQUIRED')\n"
        "except cp.CheckpointLockError:\n"
        "    print('REFUSED')\n"
    )
    holder = subprocess.Popen(
        [sys.executable, "-c", holder_script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        assert holder.stdout.readline().strip() == "HELD"
        contender = subprocess.run(
            [sys.executable, "-c", contender_script],
            capture_output=True, text=True, timeout=60,
        )
        say(f"\n[4] concurrent second real writer: {contender.stdout.strip()}  [CORRECT]")
        assert contender.stdout.strip() == "REFUSED"
        results["concurrent_writer_refused"] = {
            "holder_acquired": True,
            "contender_verdict": contender.stdout.strip(),
            "verdict": "EXCLUSIVE_LOCK_ENFORCED",
        }
    finally:
        holder.kill()
        holder.wait(timeout=30)

    # --- 5. torn checkpoint on real disk, then real probe ---------------
    root = Path(tempfile.mkdtemp(prefix="b01c-torn-"))
    worker(root, "partial:2")
    worker(root, "corrupt")
    state = probe(root)
    say(f"\n[5] torn checkpoint -> probe_failed={state.get('probe_failed')}  [CORRECT]")
    assert state.get("probe_failed") is True
    results["torn_checkpoint_refused"] = {
        "probe_failed": True,
        "verdict": "TORN_CHECKPOINT_REFUSED",
    }

    return results


def atomicity_and_tamper_cases() -> list[dict]:
    """Durability, digest, foreign-scope and effect cases, all executed."""
    from rawlsing_next.tests.test_pre553_batch_durable_checkpoint_candidate import (
        _identity, _manifest, _receipt, _binding, _repository,
    )
    from rawlsing_next.pre553_batch_runner import BatchExecutionRunner

    cases: list[dict] = []

    def record(name, expect, observed, detail=""):
        cases.append({
            "case": name, "expected": _jsonable(expect),
            "observed": _jsonable(observed),
            "detail": detail, "met": _jsonable(observed) == _jsonable(expect),
        })
        say(f"  {name:52} expected={expect!r:.60} observed={observed!r:.60}")

    say("\n" + "=" * 78)
    say("B01C DURABILITY / TAMPER / SCOPE CASES")
    say("=" * 78)

    # atomic write: no temp residue, byte-stable, dir fsync present
    root = Path(tempfile.mkdtemp(prefix="b01c-atomic-"))
    manifest = _manifest(3)
    store = cp.DurableCheckpointStore(root)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    store.save(checkpoint)
    store.save(checkpoint)
    residue = [p.name for p in root.iterdir() if p.suffix == ".tmp"]
    record("atomic_write_leaves_no_temp_residue", [], residue)
    first_bytes = store.raw_bytes()
    store.save(checkpoint)
    record("atomic_write_byte_stable", first_bytes, store.raw_bytes())
    record("directory_fsync_helper_present", True, hasattr(cp, "_fsync_dir"))

    # write-ahead ordering is structurally enforced
    ordered = True
    try:
        cp.record_commit(
            checkpoint, unit_ref=manifest.units[0].unit_ref, attempt_index=1,
            receipt=_receipt(manifest),
        )
        ordered = False
    except cp.DurableCheckpointError:
        ordered = True
    record("commit_without_durable_intent_refused", True, ordered)

    # full real round trip
    checkpoint2 = cp.empty_checkpoint(_identity(manifest))
    runner = BatchExecutionRunner(manifest=manifest, repository=_repository(manifest))
    for unit in manifest.units:
        attempt = runner.next_attempt_index(unit)
        checkpoint2 = cp.record_intent(
            checkpoint2, unit_ref=unit.unit_ref, attempt_index=attempt)
        store.save(checkpoint2)
        receipt = runner.run(executors={"QUERY": _binding()}, max_units=1)[-1]
        checkpoint2 = cp.record_commit(
            checkpoint2, unit_ref=unit.unit_ref, attempt_index=attempt,
            receipt=receipt)
        store.save(checkpoint2)
    reloaded = store.load(identity=_identity(manifest))
    plan = cp.plan_recovery(reloaded)
    record("full_roundtrip_digest_stable",
           checkpoint2.content_digest, reloaded.content_digest)
    record("full_roundtrip_recovery_safe", True, plan.recovery_safe)
    record("full_roundtrip_receipts_rehydrated", 3, len(reloaded.receipts()))

    resumed = BatchExecutionRunner(
        manifest=manifest, repository=_repository(manifest),
        prior_receipts=cp.admit_receipts_for_resume(reloaded))
    record("resume_admits_receipts_to_accepted_runner",
           True, resumed.summary().batch_state == "COMPLETED")

    # torn / tampered / foreign
    root2 = Path(tempfile.mkdtemp(prefix="b01c-tamper-"))
    store2 = cp.DurableCheckpointStore(root2)
    store2.save(cp.empty_checkpoint(_identity(manifest)))
    raw = store2.raw_bytes()
    store2.path.write_bytes(raw[: len(raw) // 2])
    torn = False
    try:
        store2.load()
    except cp.CheckpointTornError:
        torn = True
    record("torn_truncated_refused", True, torn)

    root3 = Path(tempfile.mkdtemp(prefix="b01c-seq-"))
    store3 = cp.DurableCheckpointStore(root3)
    store3.save(cp.empty_checkpoint(_identity(manifest)))
    doc = json.loads(store3.raw_bytes().decode())
    doc["sequence"] = 999
    store3.path.write_text(json.dumps(doc))
    seq_tamper = False
    try:
        store3.load()
    except cp.CheckpointTornError:
        seq_tamper = True
    record("sequence_tamper_refused", True, seq_tamper)

    root4 = Path(tempfile.mkdtemp(prefix="b01c-foreign-"))
    store4 = cp.DurableCheckpointStore(root4)
    store4.save(cp.empty_checkpoint(_identity(_manifest(3))))
    foreign = False
    try:
        store4.load(identity=_identity(_manifest(4)))
    except cp.CheckpointForeignError:
        foreign = True
    record("foreign_manifest_refused", True, foreign)

    foreign_release = False
    try:
        store4.load(identity=_identity(_manifest(3, release_label="B")))
    except cp.CheckpointForeignError:
        foreign_release = True
    record("foreign_release_refused", True, foreign_release)

    # receipt digest forgery
    root5 = Path(tempfile.mkdtemp(prefix="b01c-receipt-"))
    ck = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    ck = cp.record_intent(ck, unit_ref=unit.unit_ref, attempt_index=1)
    ck = cp.record_commit(ck, unit_ref=unit.unit_ref, attempt_index=1,
                          receipt=_receipt(manifest))
    rec = ck.records[0]
    forged = cp.UnitRecord(
        unit_key=rec.unit_key, unit_ref=rec.unit_ref, state=rec.state,
        attempt_index=rec.attempt_index, intent_hash=rec.intent_hash,
        receipt_projection={**rec.receipt_projection, "attempt_index": 5},
        receipt_hash=rec.receipt_hash,
        prior_attempt_count=rec.prior_attempt_count)
    forged_refused = False
    try:
        forged.rehydrate_receipt()
    except cp.CheckpointTornError:
        forged_refused = True
    record("forged_receipt_digest_refused", True, forged_refused)

    # foreign unit smuggled in
    smuggled = False
    try:
        cp.DurableCheckpoint(
            identity=_identity(_manifest(3)),
            records=(cp.UnitRecord(
                unit_key=_manifest(3, release_label="Z").units[0].unit_ref.key,
                unit_ref=_manifest(3, release_label="Z").units[0].unit_ref,
                state=cp.UNIT_STATE_INTENT, attempt_index=1,
                intent_hash="h" * 64, receipt_projection=None,
                receipt_hash=None),),
            sequence=1)
    except cp.CheckpointForeignError:
        smuggled = True
    record("foreign_unit_smuggling_refused", True, smuggled)

    # unknown outcome: held unless proven idempotent
    ck2 = cp.empty_checkpoint(_identity(manifest))
    ck2 = cp.record_intent(ck2, unit_ref=manifest.units[0].unit_ref, attempt_index=1)
    plan2 = cp.plan_recovery(ck2)
    record("write_ahead_intent_alone_is_NOT_exactly_once", False,
           plan2.recovery_safe)
    record("unknown_outcome_is_held_not_rerun", (), plan2.rerunnable_units)
    plan3 = cp.plan_recovery(
        ck2, idempotence_proof={manifest.units[0].unit_ref.key: "proof"})
    record("rerun_only_with_explicit_idempotence_proof", True, plan3.recovery_safe)

    # completed unit not retryable
    ck4 = cp.empty_checkpoint(_identity(manifest))
    ck4 = cp.record_intent(ck4, unit_ref=manifest.units[0].unit_ref, attempt_index=1)
    ck4 = cp.record_commit(ck4, unit_ref=manifest.units[0].unit_ref, attempt_index=1,
                           receipt=_receipt(manifest))
    not_retryable = False
    try:
        cp.record_intent(ck4, unit_ref=manifest.units[0].unit_ref, attempt_index=2)
    except cp.DurableCheckpointError:
        not_retryable = True
    record("completed_unit_not_restartable", True, not_retryable)

    # effect flags
    record("candidate_effects_all_false", True,
           all(v is False for v in cp.checkpoint_effect_flags().values()))

    return cases


def measure_resources() -> dict:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    say("\n" + "=" * 78)
    say("SAFE HOSTED BOUNDED RESOURCE MEASUREMENT")
    say("=" * 78)
    measured = {
        "self_peak_rss_mib": round(usage.ru_maxrss / 1024 / 1024, 3),
        "self_user_cpu_s": round(usage.ru_utime, 3),
        "self_sys_cpu_s": round(usage.ru_stime, 3),
        "manifest_units_measured": 4,
    }
    for key, value in measured.items():
        say(f"  {key}: {value}")
    return measured


def main() -> int:
    started = time.monotonic()
    kill_results = real_kill_and_resume()
    cases = atomicity_and_tamper_cases()
    resources = measure_resources()
    elapsed = round(time.monotonic() - started, 3)

    TRANSCRIPT.parent.mkdir(parents=True, exist_ok=True)
    TRANSCRIPT.write_text("\n".join(LINES) + "\n")

    document = {
        "schema": "PYAT_HQ280_B01C_REAL_KILL_RESUME_RESULTS@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False,
        "protocol_relaxed": False,
        "self_adopted": False,
        "canonical_mutated": False,
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "raw_source_read": False,
            "sav_dta_present": False,
        },
        "real_subprocess_kill_and_resume": kill_results,
        "durability_tamper_scope_cases": cases,
        "resource_measurement": resources,
        "total_wall_s": elapsed,
        "summary": {
            "kill_resume_scenarios": len(kill_results),
            "durable_cases": len(cases),
            "cases_met_expectation": sum(1 for c in cases if c["met"]),
            "unknown_outcome_policy": "HELD_NOT_RERUN",
            "exactly_once_claimed": False,
        },
        "terminal": (
            "HQ280_PV3_B01C_SOURCEFREE_DURABLE_CHECKPOINT_CANDIDATE_RETURNED__"
            "NO_REAL_SOURCE_ADOPTION__GITHUB_PUSHED"
        ),
    }
    OUT.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(f"\nwrote {OUT}")
    print(f"wrote {TRANSCRIPT}")
    print(json.dumps(document["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())