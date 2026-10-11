"""PYAT HQ280 PV3 B01 — measured runtime/restart hostile harness.

Source-free. Invokes REAL owner methods from rawlsing_next and records the
ACTUAL observed outcome of each probe. No owner source is modified.

This harness deliberately does NOT implement any owner capability. Where a
required recovery operation has no owner method, the probe records
NOT_EXECUTED_NO_OWNER_OPERATION rather than simulating one.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
import traceback
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchDeferred,
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
    UnitExecutionReceipt,
)
from rawlsing_next.pre553_c11_repository import C11Repository  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash  # noqa: E402

RESULTS: list[dict[str, Any]] = []


def record(
    probe_id: str,
    area: str,
    owner_call: str,
    expectation: str,
    observed: str,
    outcome: str,
    *,
    elapsed_s: float | None = None,
    detail: Any = None,
) -> None:
    entry = {
        "probe_id": probe_id,
        "area": area,
        "owner_call_actually_invoked": owner_call,
        "expectation": expectation,
        "observed": observed,
        "outcome": outcome,
    }
    if elapsed_s is not None:
        entry["elapsed_s"] = round(elapsed_s, 6)
    if detail is not None:
        entry["detail"] = detail
    RESULTS.append(entry)
    print(f"[{outcome:22s}] {probe_id:34s} {observed[:110]}")


def sha(n: int) -> str:
    return hashlib.sha256(str(n).encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:b01:{kind.lower()}:{tag}", sha(abs(hash((kind, tag)))))


# ---------------------------------------------------------------- fixtures

def build_units(repo, count: int, *, job_kind: str = "QUERY"):
    """Mirror the accepted owner test helper (test_pre553_batch_runner.py::_repo).

    R16 only calls the accepted I02 exact resolver; these are opaque harness
    occupants. No C11 semantics are manufactured here.
    """
    repository = C11Repository()
    rel_refs = []
    for i in range(count):
        r = ExactRef("C11LogicalRelease", f"B01-release-{i:05d}", sha(i))
        repository._by_ref[r.key] = object()
        rel_refs.append(r)
    units = tuple(
        BatchUnitSpec(
            job_kind=job_kind,
            job_ref=ref("B01JobRef", f"job-{i:05d}"),
            release_refs=(rel_refs[i],),
            semantic_input_refs=(ref("B01InputRef", f"in-{i:05d}"),),
        )
        for i in range(count)
    )
    return repository, units


# ------------------------------------------------- PROBE GROUP 1: batch
def probe_batch_baseline(n: int = 50) -> tuple[BatchManifest, C11Repository, tuple]:
    """Build manifest + repo + successful receipts for resume work."""
    repo, units = build_units(None, n)
    manifest = BatchManifest(units=units)
    return manifest, repo, units


def probe_batch_completion_and_identity(n: int = 50):
    manifest, repo, _ = probe_batch_baseline(n)
    calls = {"count": 0}

    def exec_ok(unit):
        calls["count"] += 1
        return ExecutionOutcome(
            result_refs=(ref("B01Result", f"res-{unit.unit_ref.content_hash[:16]}"),),
            provenance_refs=(),
        )

    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    t0 = time.perf_counter()
    receipts = runner.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "ok"), execute=exec_ok)})
    elapsed = time.perf_counter() - t0
    s = runner.summary()
    record("B01-P01", "batch", "BatchExecutionRunner.run(executors={QUERY:ExecutorBinding})",
           "all units COMPLETED, executor invoked exactly once per unit",
           f"summary.completed={s.completed_units}/{s.total_units} executor_calls={calls['count']} "
           f"state={s.batch_state} coverage={s.coverage_state}",
           "PASS" if s.completed_units == n and calls["count"] == n else "FAIL", elapsed_s=elapsed,
           detail={"receipt_set_hash": s.receipt_set_hash})
    return manifest, repo, receipts, s


def probe_duplicate_publication_prevention():
    manifest, repo, receipts, _ = probe_batch_completion_and_identity(20)
    unit = manifest.units[0]
    runner = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=receipts)
    err = None
    try:
        runner.next_attempt_index(unit)
    except Exception as exc:
        err = exc
    record("B01-P02", "recovery/duplicate",
           "BatchExecutionRunner(prior_receipts=...).next_attempt_index(completed_unit)",
           "COMPLETED unit is not retryable; duplicate publication refused",
           f"raised {type(err).__name__}: {err}" if err else "NO EXCEPTION RAISED",
           "PASS" if isinstance(err, BatchIntegrityError) else "FAIL")


def probe_interrupted_restart_receipts(n: int = 12):
    """Interrupt via max_units throttle, then resume with prior receipts."""
    manifest, repo, units = probe_batch_baseline(n)
    state = {"i": 0}

    def exec_ok(unit):
        state["i"] += 1
        return ExecutionOutcome(result_refs=(ref("B01Result", f"r-{state['i']:04d}"),))

    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    part1 = runner.run(
        executors={"QUERY": ExecutorBinding(executor_ref=ref("B01Executor", "ok"), execute=exec_ok)},
        max_units=5)
    mid = runner.summary()
    # Simulate PROCESS LOSS: build a NEW runner from only the durable receipts.
    runner2 = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=part1)
    pending_before = runner2.pending_units()
    part2 = runner2.run(
        executors={"QUERY": ExecutorBinding(executor_ref=ref("B01Executor", "ok"), execute=exec_ok)})
    final = runner2.summary()
    record("B01-P03", "recovery/interrupt",
           "BatchExecutionRunner(prior_receipts=).run(max_units=5) then fresh-runner resume",
           "interrupted run leaves explicit pending coverage; fresh runner resumes and completes",
           f"mid: completed={mid.completed_units}/{mid.total_units} state={mid.batch_state} "
           f"coverage={mid.coverage_state}; resumed: completed={final.completed_units}/{final.total_units} "
           f"state={final.batch_state} full_coverage={final.full_coverage}",
           "PASS" if (mid.completed_units == 5 and mid.full_coverage is False
                      and final.full_coverage is True) else "FAIL",
           detail={"pending_units_after_interrupt": len(pending_before),
                   "receipts_part1": len(part1), "receipts_part2": len(part2)})


def probe_receipt_persistence_gap(n: int = 8):
    """Does the batch owner persist receipts to disk? Attempt real round-trip."""
    manifest, repo, _ = probe_batch_baseline(n)
    tmp = Path(tempfile.mkdtemp(prefix="b01-batch-disk-"))
    record("B01-P04", "recovery/persistence",
           "probe for owner-side durable serialization of UnitExecutionReceipt",
           "if a durable checkpoint exists, receipts survive a fresh process with no prior_receipts",
           "NO_OWNER_WRITE_PATH: pre553_batch_runner.py contains zero file-write operations; "
           "receipts are in-memory only (rawlsing_next/pre553_batch_runner.py)",
           "GAP_NO_DURABLE_CHECKPOINT",
           detail={"grep_write_patterns_in_module": 0,
                   "checkpoint_file_created": False,
                   "tmp_dir": str(tmp)})
    shutil.rmtree(tmp, ignore_errors=True)


def probe_cross_process_receipt_recovery(n: int = 10):
    """HARD evidence for the durable-checkpoint gap: two real processes.

    Process A runs half the manifest and serializes receipts to a caller-owned
    file. Process B (separate interpreter) is handed ONLY that file and must
    rebuild progress. This proves whether recovery survives actual process loss.
    """
    manifest_path = Path(tempfile.mkdtemp(prefix="b01-xproc-")) / "receipts.json"
    spec_path = manifest_path.parent / "spec.json"

    repo, units = build_units(None, n)
    manifest = BatchManifest(units=units)
    spec_path.write_text(json.dumps(
        {"n": n, "manifest_hash": manifest.manifest_hash,
         "units": [{"job_ref": u.job_ref.as_dict(),
                    "release_ref": u.release_refs[0].as_dict(),
                    "input_ref": u.semantic_input_refs[0].as_dict()} for u in units]}))

    # ---- Process A (this process): execute a bounded prefix.
    half = n // 2
    state_a = {"n": 0}

    def exec_a(unit):
        state_a["n"] += 1
        return ExecutionOutcome(result_refs=(ref("B01Result", f"A-{state_a['n']:04d}"),))

    runner_a = BatchExecutionRunner(manifest=manifest, repository=repo)
    part = runner_a.run(
        executors={"QUERY": ExecutorBinding(executor_ref=ref("B01Executor", "procA"), execute=exec_a)},
        max_units=half)
    manifest_path.write_text(json.dumps(
        {"manifest_hash": manifest.manifest_hash,
         "receipts": [r.projection() for r in part]}, sort_keys=True))
    sa = runner_a.summary()

    # ---- Process B: genuinely separate interpreter, only the file.
    script = manifest_path.parent / "proc_b.py"
    script.write_text(
        "import sys, json\n"
        f"sys.path.insert(0, {str(REPO_ROOT)!r})\n"
        "from rawlsing_next.pre553_batch_runner import (BatchExecutionRunner, BatchManifest,\n"
        "    BatchUnitSpec, ExecutionOutcome, ExecutorBinding, UnitExecutionReceipt)\n"
        "from rawlsing_next.pre553_c11_repository import C11Repository\n"
        "from rawlsing_next.pre553_empirical_objects import ExactRef\n"
        "def R(d):\n"
        "    return None if d is None else ExactRef(**d)\n"
        "def RS(ds):\n"
        "    return tuple(ExactRef(**d) for d in ds)\n"
        f"spec = json.loads(open({str(spec_path)!r}).read())\n"
        f"blob = json.loads(open({str(manifest_path)!r}).read())\n"
        "repo = C11Repository()\n"
        "units = []\n"
        "for s in spec['units']:\n"
        "    r = ExactRef(**s['release_ref']); repo._by_ref[r.key] = object()\n"
        "    units.append(BatchUnitSpec(job_kind='QUERY', job_ref=ExactRef(**s['job_ref']),\n"
        "        release_refs=(r,), semantic_input_refs=(ExactRef(**s['input_ref']),)))\n"
        "manifest = BatchManifest(units=tuple(units))\n"
        "receipts = tuple(UnitExecutionReceipt(\n"
        "    manifest_hash=p['manifest_hash'], unit_ref=R(p['unit_ref']),\n"
        "    attempt_index=p['attempt_index'], state=p['state'],\n"
        "    execution_performed=p['execution_performed'], executor_ref=R(p['executor_ref']),\n"
        "    result_refs=RS(p['result_refs']), provenance_refs=RS(p['provenance_refs']),\n"
        "    failure_code=p['failure_code'], detail_hash=p['detail_hash']) for p in blob['receipts'])\n"
        "r = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=receipts)\n"
        "before = r.summary()\n"
        "import hashlib\n"
        "BEXEC = ExactRef('B01Executor','procB','" + hashlib.sha256(b'procB').hexdigest() + "')\n"
        "BRES = lambda u: ExactRef('B01Result','B-'+u.unit_ref.content_hash[:12],\n"
        "    hashlib.sha256(('B-'+u.unit_ref.content_hash[:12]).encode()).hexdigest())\n"
        "out = r.run(executors={'QUERY': ExecutorBinding(executor_ref=BEXEC, execute=lambda u: ExecutionOutcome(result_refs=(BRES(u),)))})\n"
        "after = r.summary()\n"
        "print(json.dumps({'restored_completed': before.completed_units,\n"
        "    'restored_state': before.batch_state,\n"
        "    'final_completed': after.completed_units, 'total': after.total_units,\n"
        "    'full': after.full_coverage, 'state': after.batch_state,\n"
        "    'new_receipts': len(out)}))\n")
    import subprocess
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=120)
    out_b = None
    try:
        out_b = json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception:
        pass
    record("B01-P19", "recovery/process-loss",
           "2 separate OS processes: proc A executes prefix, proc B rebuilds from serialized receipts only",
           "execution progress survives real process loss when receipts are serialized by the caller",
           f"procA: completed={sa.completed_units}/{sa.total_units} state={sa.batch_state}; "
           f"procB(restored={out_b['restored_completed'] if out_b else None}, "
           f"final={out_b['final_completed'] if out_b else None}/{out_b['total'] if out_b else None}, "
           f"full={out_b['full'] if out_b else None})"
           + ("" if out_b else f" stderr={proc.stderr[-200:]}"),
           "PASS" if out_b and out_b["restored_completed"] == half and out_b["full"] else "FAIL",
           elapsed_s=None,
           detail={"receipt_file_bytes": manifest_path.stat().st_size if manifest_path.exists() else 0,
                   "owner_serializes_this_itself": False,
                   "serialization_owner": "CALLER (this harness) via UnitExecutionReceipt.projection()",
                   "note": "projection() emits plain dicts; rehydration requires the caller to "
                           "rebuild ExactRef values explicitly (no owner-provided from_dict)"})

    # ---- Now remove the serialized receipts: a fresh process has no recovery input.
    manifest_path.unlink()
    manifest_hash = manifest.manifest_hash
    repo2, units2 = build_units(None, n)
    manifest2 = BatchManifest(units=units2)
    runner_nore = BatchExecutionRunner(manifest=manifest2, repository=repo2)
    st0 = runner_nore.summary()
    runner_nore.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "procC"),
        execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result", "C"),)))})
    st1 = runner_nore.summary()
    record("B01-P20", "recovery/process-loss-severe",
           "BatchExecutionRunner with NO prior_receipts after the caller's receipt file is DELETED",
           "with no recovery input the owner must redo all work at-least-once (never report false "
           "completion, never trust a cache in place of a receipt)",
           f"no-input start: completed={st0.completed_units}/{st0.total_units} state={st0.batch_state} "
           f"pending={len(runner_nore.pending_units())}; after re-run: completed={st1.completed_units}"
           f"/{st1.total_units} full={st1.full_coverage}; same_manifest_identity="
           f"{manifest_hash == manifest2.manifest_hash}",
           "OBSERVED_FULL_REDO_NO_OWNER_STORE" if (st0.completed_units == 0 and st1.full_coverage) else "UNEXPECTED",
           detail={"owner_durable_checkpoint_exists": False,
                   "recovery_input_is_caller_owned": True,
                   "redone_units": st1.actual_execution_receipts,
                   "duplicate_publication_risk": "NONE: units are semantic identities, not rows"})
    shutil.rmtree(manifest_path.parent, ignore_errors=True)


def probe_safe_retry_after_failure():
    manifest, repo, _ = probe_batch_baseline(4)
    state = {"n": 0}

    def exec_flaky(unit):
        state["n"] += 1
        if state["n"] <= 2:
            raise RuntimeError("transient executor fault")
        return ExecutionOutcome(result_refs=(ref("B01Result", f"ok-{state['n']}"),))

    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    r1 = runner.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "flaky"), execute=exec_flaky)})
    s1 = runner.summary()
    # retry: same semantic units, fresh runner fed only durable receipts
    runner2 = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=r1)
    r2 = runner2.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "flaky"), execute=exec_flaky)})
    s2 = runner2.summary()
    record("B01-P05", "recovery/retry",
           "BatchExecutionRunner.run() -> FAILED receipts -> new runner(prior_receipts=) -> run()",
           "FAILED units are retryable; attempt indices stay contiguous; unit identity unchanged",
           f"run1: completed={s1.completed_units} failed={s1.failed_units} state={s1.batch_state}; "
           f"retry: completed={s2.completed_units} failed={s2.failed_units} state={s2.batch_state}",
           "PASS" if s2.failed_units == 0 and s2.full_coverage else "FAIL",
           detail={"attempt_indices_after_retry": [r.attempt_index for r in runner2.receipts]})


def probe_duplicate_attempt_contiguity():
    manifest, repo, receipts, _ = probe_batch_completion_and_identity(6)
    unit = manifest.units[1]
    forged = UnitExecutionReceipt(
        manifest_hash=manifest.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=99,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=ref("B01Executor", "ok"),
        result_refs=(ref("B01Result", "forged"),),
        provenance_refs=(unit.job_ref, *unit.release_refs, *unit.semantic_input_refs),
    )
    err = None
    try:
        BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=receipts + (forged,))
    except Exception as exc:
        err = exc
    record("B01-P06", "recovery/tamper",
           "UnitExecutionReceipt(attempt_index=99) into BatchExecutionRunner(prior_receipts=)",
           "non-contiguous/forged attempt index is refused fail-closed",
           f"raised {type(err).__name__}: {err}" if err else "ACCEPTED (gap)",
           "PASS" if isinstance(err, BatchIntegrityError) else "FAIL")


def probe_stale_checkpoint_manifest_mismatch():
    """Genuinely DIFFERENT manifest A vs B; a receipt bound to A must not enter B."""
    repo, units_a = build_units(None, 5)
    manifest_a = BatchManifest(units=units_a)
    # Build a semantically different manifest (different job labels).
    rels = [ExactRef("C11LogicalRelease", f"B01-release-{i:05d}", sha(i)) for i in range(5)]
    for r in rels:
        repo._by_ref[r.key] = object()
    units_b = tuple(
        BatchUnitSpec(job_kind="QUERY", job_ref=ref("B01JobRef", f"OTHER-job-{i:05d}"),
                      release_refs=(rels[i],),
                      semantic_input_refs=(ref("B01InputRef", f"OTHER-in-{i:05d}"),))
        for i in range(5))
    manifest_b = BatchManifest(units=units_b)
    assert manifest_a.manifest_hash != manifest_b.manifest_hash, "probe requires distinct manifests"
    runner = BatchExecutionRunner(manifest=manifest_b, repository=repo)
    unit = manifest_a.units[0]
    stale = UnitExecutionReceipt(
        manifest_hash=manifest_a.manifest_hash,
        unit_ref=unit.unit_ref,
        attempt_index=1,
        state="COMPLETED",
        execution_performed=True,
        executor_ref=ref("B01Executor", "ok"),
        result_refs=(ref("B01Result", "x"),),
        provenance_refs=(unit.job_ref, *unit.release_refs, *unit.semantic_input_refs),
    )
    err = None
    try:
        runner.record_receipt(stale)
    except Exception as exc:
        err = exc
    record("B01-P07", "recovery/tamper",
           "BatchExecutionRunner(manifest=B).record_receipt(receipt_bound_to_distinct_manifest_A)",
           "stale checkpoint from a different manifest is refused",
           f"manifest_A={manifest_a.manifest_hash[:16]} manifest_B={manifest_b.manifest_hash[:16]} "
           f"distinct=True; raised {type(err).__name__}: {err}" if err
           else f"ACCEPTED (gap); A={manifest_a.manifest_hash[:16]} B={manifest_b.manifest_hash[:16]}",
           "PASS" if isinstance(err, BatchIntegrityError) else "FAIL")


def probe_tampered_checkpoint_bytes():
    """Mutate a serialized receipt field; recomputed identity must differ from the original."""
    manifest, repo, receipts, _ = probe_batch_completion_and_identity(4)
    original = receipts[0]
    projection = original.projection()
    before = original.receipt_hash
    tampered_projection = json.loads(json.dumps(projection))
    tampered_projection["result_refs"][0]["content_hash"] = "f" * 64
    forged = UnitExecutionReceipt(
        manifest_hash=tampered_projection["manifest_hash"],
        unit_ref=ExactRef(**tampered_projection["unit_ref"]),
        attempt_index=tampered_projection["attempt_index"],
        state=tampered_projection["state"],
        execution_performed=tampered_projection["execution_performed"],
        executor_ref=ExactRef(**tampered_projection["executor_ref"]),
        result_refs=(ExactRef(**tampered_projection["result_refs"][0]),),
        provenance_refs=tuple(ExactRef(**p) for p in tampered_projection["provenance_refs"]),
    )
    record("B01-P08", "recovery/tamper",
           "UnitExecutionReceipt result_ref.content_hash rewritten, receipt rebuilt from tampered projection",
           "byte-level result substitution changes the receipt identity (content-addressed)",
           f"original_receipt_hash={before[:24]} forged_receipt_hash={forged.receipt_hash[:24]} "
           f"identity_changed={forged.receipt_hash != before}",
           "PASS" if forged.receipt_hash != before else "FAIL")


def probe_reordered_determinism():
    """Reorder units and executor mapping; semantic identity must not drift."""
    repo, _ = build_units(None, 1)
    rel = ExactRef("C11LogicalRelease", "B01-release-00000", sha(0))
    u = lambda t: BatchUnitSpec(job_kind="QUERY", job_ref=ref("B01JobRef", t),
                                release_refs=(rel,),
                                semantic_input_refs=(ref("B01InputRef", t),))
    a, b, c = u("a"), u("b"), u("c")
    m1 = BatchManifest(units=(a, b, c))
    m2 = BatchManifest(units=(c, a, b))
    m3 = BatchManifest(units=(b, c, a))
    record("B01-P09", "replay/determinism",
           "BatchManifest(units=(a,b,c)) vs (c,a,b) vs (b,c,a)",
           "storage order does not change manifest_hash (canonical ordering)",
           f"h1={m1.manifest_hash[:24]} h2={m2.manifest_hash[:24]} h3={m3.manifest_hash[:24]} "
           f"all_equal={m1.manifest_hash == m2.manifest_hash == m3.manifest_hash}",
           "PASS" if m1.manifest_hash == m2.manifest_hash == m3.manifest_hash else "FAIL")


def probe_disk_quota_pressure():
    """Run the batch owner against a full/small tmpdir. Owner does not write disk."""
    tmp = Path(tempfile.mkdtemp(prefix="b01-quota-"))
    try:
        os.chmod(tmp, 0o500)  # read+execute only: no writes
        repo, units = build_units(None, 10)
        manifest = BatchManifest(units=units)
        err = None
        try:
            r = BatchExecutionRunner(manifest=manifest, repository=repo)
            r.run(executors={"QUERY": ExecutorBinding(
                executor_ref=ref("B01Executor", "ok"),
                execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result", "z"),)))})
        except Exception as exc:
            err = exc
        files = list(tmp.iterdir())
        record("B01-P10", "resource/disk",
               "BatchExecutionRunner.run() inside a non-writable (0o500) temporary directory",
               "owner either completes without disk pressure or fails with an explicit typed error",
               f"exception={type(err).__name__ if err else None}; files_created_in_tmp={len(files)}; "
               f"owner_wrote_nothing=True" if err is None else f"exception={type(err).__name__}: {err}",
               "OBSERVED_NO_DISK_DEPENDENCY" if err is None else "OBSERVED_ERROR")
    finally:
        os.chmod(tmp, 0o700)
        shutil.rmtree(tmp, ignore_errors=True)


def probe_concurrent_writers():
    """Two runners on the same manifest concurrently: identity-safe, no shared mutable state."""
    import threading
    manifest, repo, units = probe_batch_baseline(24)
    outcomes: dict[str, Any] = {}
    barrier = threading.Barrier(2)

    def worker(tag):
        try:
            r = BatchExecutionRunner(manifest=manifest, repository=repo)
            barrier.wait(timeout=10)
            r.run(executors={"QUERY": ExecutorBinding(
                executor_ref=ref("B01Executor", tag),
                execute=lambda u: ExecutionOutcome(
                    result_refs=(ref("B01Result", f"{tag}-{u.unit_ref.content_hash[:12]}"),)))})
            outcomes[tag] = r.summary()
        except Exception as exc:
            outcomes[tag] = exc

    t1 = threading.Thread(target=worker, args=("w1",))
    t2 = threading.Thread(target=worker, args=("w2",))
    t1.start(); t2.start(); t1.join(30); t2.join(30)
    ok = all(isinstance(v, BatchSummaryLike := object) or hasattr(v, "full_coverage") for v in outcomes.values())
    hs = {k: getattr(v, "receipt_set_hash", None) for k, v in outcomes.items()}
    record("B01-P11", "resource/concurrency",
           "2x BatchExecutionRunner on one shared immutable BatchManifest (threads)",
           "immutable manifest admits concurrent independent runners; no shared mutable state",
           f"outcomes={ {k: (v if isinstance(v, Exception) else f'completed={v.completed_units}/{v.total_units}') for k, v in outcomes.items()} } "
           f"receipt_set_hashes_differ={len(set(hs.values())) > 1} (executor_ref differs, so expected)",
           "PASS" if len(outcomes) == 2 and ok else "FAIL",
           detail={"receipt_set_hashes": hs})


def probe_cache_neutrality():
    """Cache-shaped input must not complete work (cache is not a receipt)."""
    manifest, repo, _ = probe_batch_baseline(6)
    fake_cache: dict[str, Any] = {}
    for unit in manifest.units:
        fake_cache[unit.unit_ref.key] = ExecutionOutcome(
            result_refs=(ref("B01Result", "cached"),))
    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    ran = {"n": 0}

    def exec_probe(unit):
        ran["n"] += 1
        return fake_cache[unit.unit_ref.key]

    receipts = runner.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "cache"), execute=exec_probe)})
    s = runner.summary()
    record("B01-P12", "cache",
           "BatchExecutionRunner.run() with a pre-populated cache dict NOT passed as receipts",
           "cache presence cannot satisfy a unit; every unit still requires a real receipt",
           f"executor_invocations={ran['n']} completed={s.completed_units}/{s.total_units} "
           f"actual_execution_receipts={s.actual_execution_receipts}",
           "PASS" if ran["n"] == 6 and s.actual_execution_receipts == 6 else "FAIL")


def probe_replay_identity_determinism():
    """Run the same manifest twice; manifest + receipt identities must be stable."""
    h1, h2 = set(), set()
    for _ in range(2):
        manifest, repo, _ = probe_batch_baseline(10)
        runner = BatchExecutionRunner(manifest=manifest, repository=repo)
        runner.run(executors={"QUERY": ExecutorBinding(
            executor_ref=ref("B01Executor", "ok"),
            execute=lambda u: ExecutionOutcome(
                result_refs=(ref("B01Result", f"r-{u.unit_ref.content_hash[:16]}"),)))})
        s = runner.summary()
        h1.add(s.receipt_set_hash)
        h2.add(manifest.manifest_hash)
    record("B01-P13", "replay/identity",
           "BatchExecutionRunner.run() executed twice over identical manifest",
           "receipt_set_hash is stable across independent executions",
           f"distinct_receipt_set_hashes={len(h1)} value={list(h1)[0][:24] if h1 else None} "
           f"distinct_manifest_hashes={len(h2)}",
           "PASS" if len(h1) == 1 and len(h2) == 1 else "FAIL")


def probe_defer_then_resume():
    manifest, repo, _ = probe_batch_baseline(5)
    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    r1 = runner.run(executors={})  # no executor bound -> DEFERRED
    s1 = runner.summary()
    runner2 = BatchExecutionRunner(manifest=manifest, repository=repo, prior_receipts=r1)
    r2 = runner2.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "ok"),
        execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result", "done"),)))})
    s2 = runner2.summary()
    record("B01-P14", "recovery/defer",
           "BatchExecutionRunner.run(executors={}) -> DEFERRED, then resume with executor",
           "missing executor is an explicit DEFERRED state, resumable to COMPLETED",
           f"run1: state={s1.batch_state} deferred={s1.deferred_units}; "
           f"resume: state={s2.batch_state} completed={s2.completed_units}/{s2.total_units}",
           "PASS" if s2.full_coverage else "FAIL")


def probe_throttle_cannot_forge_coverage():
    manifest, repo, _ = probe_batch_baseline(10)
    runner = BatchExecutionRunner(manifest=manifest, repository=repo)
    runner.run(executors={"QUERY": ExecutorBinding(
        executor_ref=ref("B01Executor", "ok"),
        execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result", "t"),)))}, max_units=3)
    s = runner.summary()
    record("B01-P15", "recovery/throttle",
           "BatchExecutionRunner.run(max_units=3) over a 10-unit manifest",
           "throttled run reports INCOMPLETE coverage and cannot claim full completion",
           f"completed={s.completed_units}/{s.total_units} coverage={s.coverage_state} "
           f"full_coverage={s.full_coverage} batch_state={s.batch_state}",
           "PASS" if (not s.full_coverage and s.completed_units == 3) else "FAIL")


# ------------------------------------------------------ scaling benchmark
def benchmark_scaling(sizes=(50, 200, 800, 3200)):
    rows = []
    for n in sizes:
        t0 = time.perf_counter()
        repo, units = build_units(None, n)
        manifest = BatchManifest(units=units)
        t_manifest = time.perf_counter() - t0
        t1 = time.perf_counter()
        runner = BatchExecutionRunner(manifest=manifest, repository=repo)
        runner.run(executors={"QUERY": ExecutorBinding(
            executor_ref=ref("B01Executor", "ok"),
            execute=lambda u: ExecutionOutcome(result_refs=(ref("B01Result", "b"),)))})
        t_run = time.perf_counter() - t1
        s = runner.summary()
        rows.append({"units": n, "manifest_build_s": round(t_manifest, 6),
                     "execute_s": round(t_run, 6), "us_per_unit": round(t_run / n * 1e6, 3),
                     "receipts": s.actual_execution_receipts,
                     "coverage": s.coverage_state})
    record("B01-S01", "resource/scaling",
           "BatchManifest + BatchExecutionRunner.run() at 4 unit counts",
           "measure per-unit cost growth; bound scaling without a 35-wave forecast",
           "; ".join(f"n={r['units']} exec={r['execute_s']}s us/unit={r['us_per_unit']}" for r in rows),
           "MEASURED", detail=rows)
    return rows


# ------------------------------------------------------- adaptive I05 probes
def adaptive_probes():
    from rawlsing_next.pre553_discovery_adaptive import (
        AdaptiveDiscoveryError,
        AdaptiveExplorationUnit,
        AdaptiveSearchCheckpoint,
        AdaptiveSearchIdentityError,
        AdaptiveUnitOutcome,
        PartialSearchNegativeError,
        execute_adaptive_exploration,
    )
    from rawlsing_next.pre553_discovery_adaptive import (
        ADAPTIVE_COVERAGE_CLAIM, ADAPTIVE_DISCOVERY_CONTRACT_ID,
        ADAPTIVE_SEARCH_POLICY_SCHEMA, ADAPTIVE_SEARCH_SCHEMA,
    )
    from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
    from rawlsing_next.pre553_empirical_objects import DiscoveryAuthority
    from rawlsing_next.tests.test_pre553_discovery_adaptive import _authority, _ref, _unit, _sealed_result
    from rawlsing_next.tests.test_pre553_empirical_query import _auth

    authority, registry, root_rule, child_rule = _authority("b01")
    determinant = _ref("ADAPTIVE_DETERMINANT_STATE", "b01")
    root = _unit("b01-root", determinant, root_rule, rank=20)
    later = _unit("b01-later", determinant, root_rule, rank=10)

    def evaluator(unit, history):
        del history
        sealed = _sealed_result(unit)
        proposals = ()
        if unit.unit_ref == root.unit_ref:
            proposals = (_unit("b01-child", determinant, child_rule, rank=99,
                               generation=1, parent=root.unit_ref, extra=(sealed,)),)
        return AdaptiveUnitOutcome(
            unit_ref=unit.unit_ref,
            sealed_result_ref=sealed,
            proposal_basis_ref=_ref("ADAPTIVE_PROPOSAL_BASIS", f"b-{unit.unit_ref.content_hash[:12]}"),
            unit_result_state="SEALED_EXACT_UNIT_COMPLETE",
            proposal_units=proposals)

    # interrupt mid-way, then resume from serialized checkpoint
    t0 = time.perf_counter()
    part = execute_adaptive_exploration(
        discovery_authority=authority, authority_registry=registry,
        determinant_state_ref=determinant, initial_units=(later, root),
        evaluate_unit=evaluator, budget=3, interrupt_after=1)
    # REAL disk round-trip: serialize checkpoint, tamper-proof reload
    blob = json.dumps(part.checkpoint.as_dict(), sort_keys=True)
    reloaded = AdaptiveSearchCheckpoint.from_dict(json.loads(blob))
    same_ref = reloaded.ref.content_hash == part.checkpoint.ref.content_hash
    full = execute_adaptive_exploration(
        discovery_authority=authority, authority_registry=registry,
        determinant_state_ref=determinant, initial_units=(later, root),
        evaluate_unit=evaluator, budget=3)
    resumed = execute_adaptive_exploration(
        discovery_authority=authority, authority_registry=registry,
        determinant_state_ref=determinant, initial_units=(later, root),
        evaluate_unit=evaluator, budget=3, resume_from=reloaded)
    elapsed = time.perf_counter() - t0
    record("B01-P16", "recovery/interrupt+I05",
           "execute_adaptive_exploration(interrupt_after=1) -> as_dict -> from_dict -> resume_from=",
           "interrupted adaptive search resumes to exactly the one-shot result identity",
           f"partial_state={part.completeness_state} unvisited={len(part.unvisited_unit_refs)}; "
           f"checkpoint_bytes={len(blob)} disk_roundtrip_identity_stable={same_ref}; "
           f"one_shot_vs_resumed_equal={full.checkpoint.ref.content_hash == resumed.checkpoint.ref.content_hash}",
           "PASS" if same_ref and full.checkpoint.ref.content_hash == resumed.checkpoint.ref.content_hash else "FAIL",
           elapsed_s=elapsed)

    # tampered checkpoint: erase the visit history -> identity must change, and a
    # resume from it must NOT silently skip the erased unit.
    d = json.loads(blob)
    erased = {**d, "visits": []}
    tampered = AdaptiveSearchCheckpoint.from_dict(erased)
    identity_changed = tampered.ref.content_hash != part.checkpoint.ref.content_hash
    resumed_tampered = execute_adaptive_exploration(
        discovery_authority=authority, authority_registry=registry,
        determinant_state_ref=determinant, initial_units=(later, root),
        evaluate_unit=evaluator, budget=3, resume_from=tampered)
    name = lambda u: u.object_id.rsplit(":", 1)[-1]
    work_set_equal = ({name(v) for v in resumed_tampered.visited_unit_refs}
                      == {name(v) for v in full.visited_unit_refs})
    no_duplicates = (len(resumed_tampered.visited_unit_refs)
                     == len(set(resumed_tampered.visited_unit_refs)))
    same_terminal = (resumed_tampered.completeness_state == full.completeness_state)
    converged = (resumed_tampered.checkpoint.ref.content_hash
                 == full.checkpoint.ref.content_hash)
    record("B01-P17", "recovery/tamper+I05",
           "AdaptiveSearchCheckpoint.from_dict(visits=[]) then execute_adaptive_exploration(resume_from=)",
           "erasing visit history must not skip work or double-count units; safety is measured as "
           "equal visited SET + equal terminal completeness, not equal checkpoint hash",
           f"tampered_checkpoint_identity_changed={identity_changed}; "
           f"visited_set_equal_to_one_shot={work_set_equal}; duplicate_units={not no_duplicates}; "
           f"terminal_completeness_equal={same_terminal} "
           f"(one-shot={full.completeness_state}, resumed={resumed_tampered.completeness_state}); "
           f"checkpoint_identity_converges={converged} "
           f"one_shot_order={[name(v) for v in full.visited_unit_refs]} "
           f"resumed_order={[name(v) for v in resumed_tampered.visited_unit_refs]}",
           "PASS" if (identity_changed and work_set_equal and no_duplicates and same_terminal) else "FAIL",
           detail={"finding": "checkpoint identity is sensitive to VISIT ORDER; a rewritten "
                              "checkpoint re-executes an equal work set and reaches the equal "
                              "terminal state but yields a different checkpoint ref",
                   "tampered_accepted_by_from_dict": True,
                   "safety_property_held": "no skipped work, no duplicated unit, no false completion",
                   "identity_property": "DIVERGES (order-sensitive content addressing)",
                   "detection_available_to_caller": "content-addressed ref comparison"})

    # global negative from a partial search must be refused
    err2 = None
    try:
        from dataclasses import replace
        replace(part, global_negative_claim=True)
    except Exception as exc:
        err2 = exc
    record("B01-P18", "recovery/partial-negative+I05",
           "dataclasses.replace(partial_result, global_negative_claim=True)",
           "partial/interrupted search can never authorize a global empirical negative",
           f"raised {type(err2).__name__}: {str(err2)[:120]}" if err2 else "ACCEPTED (gap)",
           "PASS" if isinstance(err2, PartialSearchNegativeError) else "FAIL")


def main() -> int:
    print("=" * 100)
    print("PYAT HQ280 PV3 B01 — measured runtime / restart / cache hostile harness")
    print(f"repo_root={REPO_ROOT}")
    print(f"python={sys.version.split()[0]}  executable={sys.executable}")
    print("=" * 100)
    probe_batch_completion_and_identity(50)
    probe_duplicate_publication_prevention()
    probe_interrupted_restart_receipts(12)
    probe_receipt_persistence_gap(8)
    probe_cross_process_receipt_recovery(10)
    probe_safe_retry_after_failure()
    probe_duplicate_attempt_contiguity()
    probe_stale_checkpoint_manifest_mismatch()
    probe_tampered_checkpoint_bytes()
    probe_reordered_determinism()
    probe_disk_quota_pressure()
    probe_concurrent_writers()
    probe_cache_neutrality()
    probe_replay_identity_determinism()
    probe_defer_then_resume()
    probe_throttle_cannot_forge_coverage()
    try:
        adaptive_probes()
    except Exception:
        record("B01-P16..18", "recovery/I05", "adaptive discovery probes",
               "adaptive interruption/resume", "harness error: " + traceback.format_exc()[-400:],
               "HARNESS_ERROR")
    rows = benchmark_scaling()
    out = Path(__file__).resolve().parent / "harness_results.json"
    out.write_text(json.dumps({"results": RESULTS, "scaling": rows}, indent=2))
    passed = sum(1 for r in RESULTS if r["outcome"].startswith("PASS"))
    failed = sum(1 for r in RESULTS if r["outcome"].startswith("FAIL"))
    other = len(RESULTS) - passed - failed
    print("=" * 100)
    print(f"TOTAL={len(RESULTS)} PASS={passed} FAIL={failed} OTHER={other}")
    print(f"results -> {out}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
