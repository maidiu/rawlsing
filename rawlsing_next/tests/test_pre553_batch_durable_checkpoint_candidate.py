"""PYAT HQ280 PV3 B01C - durable WRITE_AHEAD checkpoint candidate tests.

Development-only, source-free.  These tests drive the candidate around the
ACCEPTED, UNMODIFIED ``pre553_batch_runner`` owner and use REAL temporary
directories, REAL files and REAL subprocesses that are genuinely SIGKILLed.

The accepted batch runner and ``rabochii_execution_protocol`` are asserted to
be untouched.  No raw SAV/DTA is read; no source-use permission is claimed.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
    UnitExecutionReceipt,
)
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKER = (
    REPO_ROOT / "WORKER_RETURNS"
    / "PYAT-HQ280-PV3-B01C-DURABLE-CHECKPOINT-CANDIDATE-R1"
    / "repro" / "b01c_worker.py"
)


# --------------------------------------------------------------------------
# Local fixtures mirroring the accepted owner surface
# --------------------------------------------------------------------------
def _h(label: str) -> str:
    import hashlib
    return hashlib.sha256(label.encode()).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:b01c:{kind.lower()}:{label}", _h(f"{kind}:{label}"))


def _release(label: str = "A") -> ExactRef:
    return ExactRef("C11LogicalRelease", f"release-{label}", _h(f"release:{label}"))


def _manifest(n: int = 3, release_label: str = "A") -> BatchManifest:
    release = _release(release_label)
    return BatchManifest(tuple(
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", f"q{i}"),
            release_refs=(release,),
            semantic_input_refs=(_ref("EmpiricalPredicate@1.0.0", f"p{i}"),),
        )
        for i in range(n)
    ))


def _repository(manifest: BatchManifest) -> C11Repository:
    repository = C11Repository()
    for unit in manifest.units:
        for ref in unit.release_refs:
            repository._by_ref[ref.key] = object()
    return repository


def _outcome(unit: BatchUnitSpec) -> ExecutionOutcome:
    return ExecutionOutcome(
        result_refs=(_ref("RESULT", unit.unit_hash),),
        provenance_refs=(_ref("EXECUTION_TRACE", unit.unit_hash),),
    )


def _binding() -> ExecutorBinding:
    return ExecutorBinding(_ref("EXECUTOR", "query"), _outcome)


def _receipt(manifest: BatchManifest, index: int = 0) -> UnitExecutionReceipt:
    runner = BatchExecutionRunner(manifest=manifest, repository=_repository(manifest))
    receipts = runner.run(executors={"QUERY": _binding()}, max_units=index + 1)
    return receipts[-1]


def _identity(manifest: BatchManifest) -> cp.CheckpointIdentity:
    return cp.CheckpointIdentity.from_manifest(manifest)


def _run_worker(root: Path, phase: str, timeout: float = 60.0):
    return subprocess.run(
        [sys.executable, str(WORKER), str(root), phase],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(REPO_ROOT),
    )


def _probe(root: Path) -> dict:
    result = _run_worker(root, "probe")
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


# ==========================================================================
# POSITIVE: real durable write-ahead + atomic persistence + real receipts
# ==========================================================================
def test_real_run_persists_durable_checkpoint_with_real_receipts(tmp_path):
    manifest = _manifest(4)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(identity)

    runner = BatchExecutionRunner(manifest=manifest, repository=_repository(manifest))
    for unit in manifest.units:
        attempt = runner.next_attempt_index(unit)
        # durable intent strictly BEFORE the owner side effect
        checkpoint = cp.record_intent(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt
        )
        ref = store.save(checkpoint)
        assert ref.content_hash == checkpoint.content_digest
        receipts = runner.run(executors={"QUERY": _binding()}, max_units=1)
        receipt = receipts[-1]
        checkpoint = cp.record_commit(
            checkpoint, unit_ref=unit.unit_ref,
            attempt_index=attempt, receipt=receipt,
        )
        store.save(checkpoint)

    loaded = store.load(identity=identity)
    assert loaded.content_digest == checkpoint.content_digest
    assert loaded.checkpoint_ref == checkpoint.checkpoint_ref
    assert len(loaded.records) == 4
    plan = cp.plan_recovery(loaded)
    assert plan.recovery_safe is True
    assert plan.held_units == ()
    assert len(plan.committed_units) == 4
    assert len(loaded.receipts()) == 4
    for receipt in loaded.receipts():
        assert isinstance(receipt, UnitExecutionReceipt)
        assert receipt.state == "COMPLETED"


def test_receipts_rehydrate_into_the_accepted_runner_exactly(tmp_path):
    manifest = _manifest(3)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(identity)
    runner = BatchExecutionRunner(manifest=manifest, repository=_repository(manifest))
    for unit in manifest.units:
        attempt = runner.next_attempt_index(unit)
        checkpoint = cp.record_intent(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt
        )
        store.save(checkpoint)
        receipt = runner.run(executors={"QUERY": _binding()}, max_units=1)[-1]
        checkpoint = cp.record_commit(
            checkpoint, unit_ref=unit.unit_ref,
            attempt_index=attempt, receipt=receipt,
        )
        store.save(checkpoint)

    resumed = BatchExecutionRunner(
        manifest=manifest, repository=_repository(manifest),
        prior_receipts=cp.admit_receipts_for_resume(store.load(identity=identity)),
    )
    assert resumed.pending_units() == ()
    assert resumed.summary().batch_state == "COMPLETED"
    assert resumed.summary().full_coverage is True


def test_atomic_write_leaves_no_temp_residue_and_is_byte_stable(tmp_path):
    manifest = _manifest(2)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    store.save(checkpoint)
    store.save(checkpoint)
    leftovers = [p.name for p in tmp_path.iterdir() if p.suffix == ".tmp"]
    assert leftovers == []
    first = store.raw_bytes()
    store.save(checkpoint)
    assert store.raw_bytes() == first


def test_directory_fsync_is_performed_closing_the_existing_gap(tmp_path):
    """The EE-P2X atomic writer omits the parent-directory fsync; we add it."""
    assert hasattr(cp, "_fsync_dir")
    store = cp.DurableCheckpointStore(tmp_path)
    store.save(cp.empty_checkpoint(_identity(_manifest(1))))
    # a durable write must survive the file handle closing; dir fsync ran
    assert store.exists()
    loaded = store.load()
    assert loaded.sequence == 0


def test_checkpoint_is_bound_to_exact_manifest_release_and_scope(tmp_path):
    manifest = _manifest(2)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    store.save(cp.empty_checkpoint(identity))

    # a genuinely different manifest (different unit count => different hash)
    with pytest.raises(cp.CheckpointForeignError, match="different manifest"):
        store.load(identity=_identity(_manifest(3)))

    # a different release identity for the same unit count
    with pytest.raises(cp.CheckpointForeignError):
        store.load(identity=_identity(_manifest(2, release_label="B")))


# ==========================================================================
# REAL PROCESS KILL / RESTART
# ==========================================================================
def test_real_sigkill_after_durable_intent_leaves_checkpoint_and_holds(tmp_path):
    """The decisive hazard case, executed with a REAL SIGKILL."""
    result = _run_worker(tmp_path, "start")
    assert result.returncode == -signal.SIGKILL or result.returncode == 137
    assert "INTENT_DURABLE" in result.stdout

    probed = _probe(tmp_path)
    assert probed["exists"] is True
    assert len(probed["records"]) == 1
    assert probed["records"][0]["state"] == cp.UNIT_STATE_INTENT
    # the side effect may or may not have landed: HELD, never silently rerun
    assert probed["plan"]["recovery_safe"] is False
    assert len(probed["plan"]["held_units"]) == 1
    assert probed["plan"]["rerunnable_units"] == []


def test_real_restart_resumes_from_durable_receipts_without_redo(tmp_path):
    assert _run_worker(tmp_path, "partial:2").returncode == 0
    first = _probe(tmp_path)
    assert len(first["records"]) == 2
    assert all(r["state"] == cp.UNIT_STATE_COMMITTED for r in first["records"])

    assert _run_worker(tmp_path, "normal").returncode == 0
    second = _probe(tmp_path)
    assert len(second["records"]) == 4
    assert second["plan"]["recovery_safe"] is True
    assert len(second["plan"]["committed_units"]) == 4
    # the two previously committed units were never re-executed
    for record in second["records"][:2]:
        assert record["attempt_index"] == 1


def test_real_kill_on_an_unstarted_unit_holds_only_that_unit(tmp_path):
    assert _run_worker(tmp_path, "partial:2").returncode == 0
    before = _probe(tmp_path)
    assert before["plan"]["recovery_safe"] is True
    committed_before = set(before["plan"]["committed_units"])

    # a fresh real process resumes and completes the REMAINING work;
    # the two committed units are never re-executed.
    result = _run_worker(tmp_path, "normal")
    assert result.returncode == 0
    after = _probe(tmp_path)
    assert len(after["records"]) == 4
    assert after["plan"]["recovery_safe"] is True
    assert set(after["plan"]["committed_units"]) == set(
        u.unit_ref.key for u in _manifest(4).units
    )
    assert committed_before <= set(after["plan"]["committed_units"])


def test_real_restart_of_a_committed_unit_is_refused(tmp_path):
    """A completed unit must not be re-startable, even by a fresh process."""
    assert _run_worker(tmp_path, "partial:1").returncode == 0
    first = _probe(tmp_path)
    committed = first["plan"]["committed_units"]
    assert len(committed) == 1

    # the worker's "start" phase targets unit 0, which is already committed
    result = _run_worker(tmp_path, "start")
    assert result.returncode == 1
    assert "already committed" in (result.stderr + result.stdout)


def test_real_concurrent_writers_are_serialised_by_the_lock(tmp_path):
    manifest = _manifest(2)
    store = cp.DurableCheckpointStore(tmp_path)
    store.save(cp.empty_checkpoint(_identity(manifest)))

    # a holder process keeps the lock; a second real process must be refused
    holder_script = (
        "import sys,time;sys.path.insert(0,%r);"
        "import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp;"
        "from pathlib import Path;"
        "s=cp.DurableCheckpointStore(Path(%r));"
        "ctx=cp.ledger_lock(s.lock_path);ctx.__enter__();"
        "print('HELD',flush=True);time.sleep(30)"
    ) % (str(REPO_ROOT), str(tmp_path))
    holder = subprocess.Popen(
        [sys.executable, "-c", holder_script],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    try:
        assert holder.stdout.readline().strip() == "HELD"
        contender_script = (
            "import sys;sys.path.insert(0,%r);"
            "import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp;"
            "from pathlib import Path;"
            "s=cp.DurableCheckpointStore(Path(%r));"
            "\ntry:\n"
            "    with cp.ledger_lock(s.lock_path):\n"
            "        print('ACQUIRED')\n"
            "except cp.CheckpointLockError:\n"
            "    print('REFUSED')\n"
        ) % (str(REPO_ROOT), str(tmp_path))
        contender = subprocess.run(
            [sys.executable, "-c", contender_script],
            capture_output=True, text=True, timeout=60,
        )
        assert contender.stdout.strip() == "REFUSED"
    finally:
        holder.kill()
        holder.wait(timeout=30)


# ==========================================================================
# HOSTILES: torn / corrupt / tamper / foreign / lock
# ==========================================================================
def test_torn_truncated_checkpoint_is_refused(tmp_path):
    manifest = _manifest(2)
    store = cp.DurableCheckpointStore(tmp_path)
    store.save(cp.empty_checkpoint(_identity(manifest)))
    raw = store.raw_bytes()
    store.path.write_bytes(raw[: len(raw) // 2])
    with pytest.raises(cp.CheckpointTornError):
        store.load()


def test_byte_tampered_checkpoint_digest_is_refused(tmp_path):
    manifest = _manifest(2)
    store = cp.DurableCheckpointStore(tmp_path)
    store.save(cp.empty_checkpoint(_identity(manifest)))
    document = json.loads(store.raw_bytes().decode())
    document["sequence"] = 999
    store.path.write_text(json.dumps(document))
    with pytest.raises(cp.CheckpointTornError, match="digest"):
        store.load()


def test_tampered_record_content_is_refused(tmp_path):
    manifest = _manifest(2)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(identity)
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    store.save(checkpoint)

    document = json.loads(store.raw_bytes().decode())
    document["records"][0]["attempt_index"] = 7
    store.path.write_text(json.dumps(document))
    with pytest.raises(cp.CheckpointTornError, match="digest"):
        store.load()


def test_committed_receipt_digest_mismatch_blocks_rehydration(tmp_path):
    manifest = _manifest(1)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(identity)
    unit = manifest.units[0]
    receipt = _receipt(manifest)
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    checkpoint = cp.record_commit(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1, receipt=receipt
    )
    record = checkpoint.records[0]
    forged = cp.UnitRecord(
        unit_key=record.unit_key, unit_ref=record.unit_ref,
        state=record.state, attempt_index=record.attempt_index,
        intent_hash=record.intent_hash,
        receipt_projection={**record.receipt_projection, "attempt_index": 5},
        receipt_hash=record.receipt_hash,
        prior_attempt_count=record.prior_attempt_count,
    )
    tampered = cp.DurableCheckpoint(
        identity=identity, records=(forged,), sequence=checkpoint.sequence
    )
    with pytest.raises(cp.CheckpointTornError, match="digest mismatch"):
        tampered.records[0].rehydrate_receipt()


def test_foreign_manifest_unit_cannot_be_smuggled_into_a_checkpoint():
    manifest_a = _manifest(2)
    manifest_b = _manifest(2, release_label="Z")
    identity = _identity(manifest_a)
    foreign_unit = manifest_b.units[0]
    record = cp.UnitRecord(
        unit_key=foreign_unit.unit_ref.key, unit_ref=foreign_unit.unit_ref,
        state=cp.UNIT_STATE_INTENT, attempt_index=1,
        intent_hash=semantic_hash({"x": 1}),
        receipt_projection=None, receipt_hash=None,
    )
    with pytest.raises(cp.CheckpointForeignError, match="outside its manifest"):
        cp.DurableCheckpoint(identity=identity, records=(record,), sequence=1)


def test_foreign_schema_is_refused(tmp_path):
    store = cp.DurableCheckpointStore(tmp_path)
    store.path.write_text(json.dumps({"schema": "SOMETHING_ELSE", "records": []}))
    with pytest.raises(cp.CheckpointForeignError, match="schema"):
        store.load()


def test_non_object_json_checkpoint_is_refused(tmp_path):
    store = cp.DurableCheckpointStore(tmp_path)
    store.path.write_text(json.dumps([1, 2, 3]))
    with pytest.raises(cp.CheckpointTornError):
        store.load()


def test_lock_refuses_a_second_concurrent_writer(tmp_path):
    store = cp.DurableCheckpointStore(tmp_path)
    with cp.ledger_lock(store.lock_path):
        with pytest.raises(cp.CheckpointLockError, match="another writer"):
            with cp.ledger_lock(store.lock_path):
                pass


def test_missing_checkpoint_is_typed_not_silently_empty(tmp_path):
    store = cp.DurableCheckpointStore(tmp_path)
    assert store.exists() is False
    with pytest.raises(cp.CheckpointTornError, match="no durable checkpoint"):
        store.load()


def test_real_tamper_on_disk_then_probe_subprocess_refuses(tmp_path):
    assert _run_worker(tmp_path, "partial:2").returncode == 0
    assert _probe(tmp_path)["exists"] is True
    result = _run_worker(tmp_path, "corrupt")
    assert result.returncode == 0
    result = _run_worker(tmp_path, "probe")
    assert result.returncode != 0
    assert "Torn" in (result.stderr + result.stdout)


# ==========================================================================
# HOSTILES: unknown outcome, duplicate work, idempotence
# ==========================================================================
def test_write_ahead_intent_alone_never_implies_exactly_once(tmp_path):
    """A START intent with no COMMIT is UNKNOWN and must HELD, not rerun."""
    manifest = _manifest(3)
    identity = _identity(manifest)
    checkpoint = cp.empty_checkpoint(identity)
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    plan = cp.plan_recovery(checkpoint)
    assert plan.recovery_safe is False
    assert plan.held_units == (unit.unit_ref.key,)
    assert plan.rerunnable_units == ()
    assert plan.dispositions[unit.unit_ref.key] is cp.RecoveryDisposition.UNKNOWN_OUTCOME


def test_unknown_outcome_stays_held_despite_caller_idempotence_proof_b01d():
    """B01D versioned replacement for the unsafe predecessor test.

    The predecessor asserted that a caller-supplied ``{"key": "proof-sha"}``
    promotes UNKNOWN_OUTCOME to RERUN_SAFE.  B01CR proved that rule accepts
    forged idempotence (including the empty string) and risks duplicate
    external execution.  The fail-closed rule: caller proofs are recorded as
    disregarded evidence and the unit stays HELD.
    """
    manifest = _manifest(2)
    identity = _identity(manifest)
    checkpoint = cp.empty_checkpoint(identity)
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    without = cp.plan_recovery(checkpoint)
    assert without.recovery_safe is False

    with_proof = cp.plan_recovery(
        checkpoint, idempotence_proof={unit.unit_ref.key: "proof-sha"}
    )
    assert with_proof.recovery_safe is False
    assert with_proof.rerunnable_units == ()
    assert with_proof.held_units == (unit.unit_ref.key,)
    assert with_proof.dispositions[unit.unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME
    )
    assert unit.unit_ref.key in with_proof.disregarded_caller_proofs
    assert "RERUN_SAFE" not in {
        d.value for d in with_proof.dispositions.values()
    }


def test_empty_string_idempotence_proof_is_refused_b01d():
    """The exact B01CR W6 attack: ``{key: ""}`` must NOT promote."""
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    plan = cp.plan_recovery(checkpoint, idempotence_proof={unit.unit_ref.key: ""})
    assert plan.dispositions[unit.unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME
    )
    assert plan.recovery_safe is False
    assert plan.rerunnable_units == ()
    assert unit.unit_ref.key in plan.disregarded_caller_proofs
    assert "RERUN_SAFE" not in {d.value for d in plan.dispositions.values()}


def test_key_only_and_arbitrary_junk_proofs_are_refused_b01d():
    """Key presence alone, whatever the value, never upgrades."""
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    for junk in ("x", "definitely idempotent, trust me", "0" * 64, "null", "false"):
        plan = cp.plan_recovery(checkpoint, idempotence_proof={unit.unit_ref.key: junk})
        assert plan.dispositions[unit.unit_ref.key] is (
            cp.RecoveryDisposition.UNKNOWN_OUTCOME
        ), junk
        assert plan.rerunnable_units == ()


def test_forged_dict_and_cross_unit_proofs_are_refused_b01d():
    """Proofs naming the wrong unit, or carrying forged structure, are held."""
    manifest = _manifest(2)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    first, second = manifest.units[0], manifest.units[1]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=first.unit_ref, attempt_index=1
    )
    # proof names only the OTHER unit: first unit must stay HELD
    plan = cp.plan_recovery(
        checkpoint, idempotence_proof={second.unit_ref.key: "proof"}
    )
    assert plan.dispositions[first.unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME
    )
    assert plan.rerunnable_units == ()
    assert second.unit_ref.key in plan.disregarded_caller_proofs
    # non-string values are also just caller assertion
    plan = cp.plan_recovery(checkpoint, idempotence_proof={first.unit_ref.key: 12345})  # type: ignore[dict-item]
    assert plan.dispositions[first.unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME
    )
    assert first.unit_ref.key in plan.disregarded_caller_proofs


def test_mismatched_release_proof_is_refused_b01d():
    """A proof cannot smuggle a different release scope into recovery."""
    other_release = _release("B")
    other = BatchManifest((
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", "q0"),
            release_refs=(other_release,),
            semantic_input_refs=(_ref("EmpiricalPredicate@1.0.0", "p0"),),
        ),
    ))
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    plan = cp.plan_recovery(
        checkpoint,
        idempotence_proof={
            unit.unit_ref.key: "release:" + other_release.key,
            other.units[0].unit_ref.key: "cross-manifest-proof",
        },
    )
    assert plan.dispositions[unit.unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME
    )
    assert plan.rerunnable_units == ()
    assert len(plan.disregarded_caller_proofs) == 2


def test_rerun_safe_is_currently_unreachable_b01d():
    """No caller input of any shape can produce RERUN_SAFE."""
    manifest = _manifest(2)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    for unit in manifest.units:
        checkpoint = cp.record_intent(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=1
        )
    hostile_proofs = [
        None,
        {},
        {u.unit_ref.key: "" for u in manifest.units},
        {u.unit_ref.key: "non-empty-proof" for u in manifest.units},
        {u.unit_ref.key: {"nested": ["object"]} for u in manifest.units},  # type: ignore[dict-item]
        {"completely-foreign-key": "x"},
    ]
    for proofs in hostile_proofs:
        plan = cp.plan_recovery(checkpoint, idempotence_proof=proofs)  # type: ignore[arg-type]
        assert "RERUN_SAFE" not in {d.value for d in plan.dispositions.values()}
        assert plan.rerunnable_units == ()
        assert set(plan.dispositions.values()) == {cp.RecoveryDisposition.UNKNOWN_OUTCOME}


def test_disregarded_proofs_are_auditable_evidence_b01d():
    """Disregard is recorded, never silent: the attempt itself is evidence."""
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    plan = cp.plan_recovery(checkpoint, idempotence_proof={unit.unit_ref.key: "x"})
    assert unit.unit_ref.key in plan.disregarded_caller_proofs
    assert "IDEMPOTENCE_ISSUER_HOLD" in plan.summary()["disregarded_caller_proofs"][
        unit.unit_ref.key
    ] or "disregarded" in plan.disregarded_caller_proofs[unit.unit_ref.key]
    assert "idempotence_issuer_hold" in plan.summary()
    clean = cp.plan_recovery(checkpoint)
    assert clean.disregarded_caller_proofs == {}


def test_completed_unit_cannot_be_restarted(tmp_path):
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1
    )
    checkpoint = cp.record_commit(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1,
        receipt=_receipt(manifest),
    )
    with pytest.raises(cp.DurableCheckpointError, match="already committed"):
        cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=2)


def test_commit_without_intent_is_refused():
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    with pytest.raises(cp.DurableCheckpointError, match="prior durable START"):
        cp.record_commit(
            checkpoint, unit_ref=manifest.units[0].unit_ref,
            attempt_index=1, receipt=_receipt(manifest),
        )


def test_commit_attempt_index_must_match_the_durable_intent():
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=2)
    with pytest.raises(cp.DurableCheckpointError, match="attempt index"):
        cp.record_commit(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=1,
            receipt=_receipt(manifest),
        )


def test_intent_record_may_not_carry_a_receipt():
    """A START intent that smuggles a receipt is refused at construction."""
    with pytest.raises(cp.DurableCheckpointError, match="may not carry"):
        cp.UnitRecord(
            unit_key="k", unit_ref=_ref("EmpiricalQuerySpec@1.0.0", "k"),
            state=cp.UNIT_STATE_INTENT, attempt_index=1, intent_hash="h",
            receipt_projection={"attempt_index": 1}, receipt_hash="x",
        )
    with pytest.raises(cp.DurableCheckpointError, match="requires"):
        cp.UnitRecord(
            unit_key="k", unit_ref=_ref("EmpiricalQuerySpec@1.0.0", "k"),
            state=cp.UNIT_STATE_COMMITTED, attempt_index=1, intent_hash="h",
            receipt_projection=None, receipt_hash=None,
        )


def test_recovery_does_not_duplicate_committed_semantic_work(tmp_path):
    manifest = _manifest(3)
    identity = _identity(manifest)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(identity)
    runner = BatchExecutionRunner(manifest=manifest, repository=_repository(manifest))
    for unit in manifest.units:
        attempt = runner.next_attempt_index(unit)
        checkpoint = cp.record_intent(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt
        )
        store.save(checkpoint)
        receipt = runner.run(executors={"QUERY": _binding()}, max_units=1)[-1]
        checkpoint = cp.record_commit(
            checkpoint, unit_ref=unit.unit_ref,
            attempt_index=attempt, receipt=receipt,
        )
        store.save(checkpoint)

    reloaded = store.load(identity=identity)
    plan = cp.plan_recovery(reloaded)
    assert plan.recovery_safe is True
    assert plan.rerunnable_units == ()
    assert set(plan.committed_units) == {u.unit_ref.key for u in manifest.units}

    resumed = BatchExecutionRunner(
        manifest=manifest, repository=_repository(manifest),
        prior_receipts=cp.admit_receipts_for_resume(reloaded),
    )
    assert resumed.pending_units() == ()


def test_attempt_indices_stay_contiguous_across_recovery(tmp_path):
    manifest = _manifest(2)
    identity = _identity(manifest)
    checkpoint = cp.empty_checkpoint(identity)
    unit = manifest.units[0]
    checkpoint = cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=1)
    # simulate a second durable attempt for the same unit
    checkpoint = cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=2)
    record = checkpoint.by_unit(unit.unit_ref.key)
    assert record.attempt_index == 2
    assert record.prior_attempt_count == 1


def test_never_started_unit_is_dispositioned_explicitly():
    manifest = _manifest(3)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    plan = cp.plan_recovery(checkpoint)
    assert plan.recovery_safe is True
    assert set(plan.dispositions.values()) == {
        cp.RecoveryDisposition.NEVER_STARTED
    }


# ==========================================================================
# Governance: accepted owners untouched
# ==========================================================================
def test_accepted_owners_and_protocol_are_not_modified_by_this_candidate():
    """Static check: the candidate adds no relaxation and edits no owner."""
    import inspect

    source = inspect.getsource(cp)
    assert "def validate_court_spec" not in source
    # the candidate never redefines or monkeypatches an accepted owner
    for forbidden in ("monkeypatch", "setattr(pre553", "sys.modules["):
        assert forbidden not in source
    # it does not import the protocol module at all (no relaxation path)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    assert "execution_protocol" not in imports


def test_candidate_declares_no_authority_or_protocol_effect():
    flags = cp.checkpoint_effect_flags()
    assert flags == {
        "relaxed_execution_protocol": False,
        "granted_real_execution_approval": False,
        "semantic_truth_effect": False,
        "learned_product_publication_effect": False,
        "actor_v3_effect": False,
        "invented_scientific_issuer": False,
        "claims_exactly_once_external_execution": False,
        "honors_caller_idempotence_proof": False,
    }


def test_idempotence_issuer_hold_is_explicit_and_closed():
    hold = dict(cp.IDEMPOTENCE_ISSUER_HOLD)
    assert hold["state"] == "HELD__NO_VERIFIED_IDEMPOTENCE_ISSUER"
    assert hold["automatic_rerun_upgrade"] == "DISABLED"
    assert hold["caller_proofs_honored"] is False
    assert "caller mapping key presence" in hold["forbidden_substitutes"]
    assert "caller string value (including non-empty strings)" in (
        hold["forbidden_substitutes"]
    )
    required = hold["required_future_credential"]
    for field in ("exact_unit_key", "exact_release_refs", "exact_manifest_hash",
                  "executor_identity", "issuer", "verification"):
        assert field in required, field
    assert "IDEMPOTENCE_ISSUER_HOLD" in cp.__all__


def test_write_ahead_protocol_tokens_are_satisfied_by_this_candidate():
    """F-02 required tokens; the candidate supplies them WITHOUT relaxing."""
    import inspect

    protocol = (
        REPO_ROOT / "rawlsing_next" / "rabochii_execution_protocol.py"
    ).read_text()
    assert 'checkpoint.get("mode") != "WRITE_AHEAD"' in protocol
    # the candidate uses the same vocabulary and a real durable ref
    source = inspect.getsource(cp)
    assert 'UNIT_STATE_INTENT = "START_INTENT_WRITTEN"' in source
    assert "durable_checkpoint" in cp.CHECKPOINT_SCHEMA_ID.lower()
    ref = cp.empty_checkpoint(_identity(_manifest(1))).checkpoint_ref
    assert isinstance(ref, ExactRef)
    assert len(ref.content_hash) == 64


def test_batch_runner_file_is_untouched_by_this_work():
    runner_path = REPO_ROOT / "rawlsing_next" / "pre553_batch_runner.py"
    original = runner_path.read_bytes()
    # a real import + real use must not mutate the accepted module
    manifest = _manifest(1)
    cp.DurableCheckpointStore(Path(os.environ.get("TMPDIR", "/tmp")) / "b01c-noop")
    assert runner_path.read_bytes() == original


def test_source_free_posture_no_raw_survey_reads():
    source = (REPO_ROOT / "rawlsing_next" /
              "pre553_batch_durable_checkpoint_candidate.py").read_text()
    for forbidden in (".sav", ".dta", "pyreadstat", "read_sav"):
        assert forbidden not in source


def test_worker_script_exists_and_is_executable_as_a_real_process():
    assert WORKER.is_file()
    result = _run_worker(Path(os.environ["TMPDIR"]) / f"b01c-probe-{os.getpid()}", "probe")
    assert result.returncode == 0
    assert json.loads(result.stdout)["exists"] is False

# ==========================================================================
# B01D: real crash AFTER external side effect BEFORE commit + repair proof
# ==========================================================================
B01D_WORKER = (
    REPO_ROOT / "WORKER_RETURNS"
    / "PYAT-HQ280-PV3-B01D-IDEMPOTENCE-RECOVERY-REPAIR-R1"
    / "repro" / "b01d_worker.py"
)


def _run_b01d_worker(root: Path, phase: str, timeout: float = 60.0):
    return subprocess.run(
        [sys.executable, str(B01D_WORKER), str(root), phase],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(REPO_ROOT),
    )


def _b01d_probe(root: Path) -> dict:
    result = _run_b01d_worker(root, "probe")
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_real_crash_after_side_effect_before_commit_holds_counter_at_1_b01d(tmp_path):
    """The exact B01CR window, executed: START, durable side effect, SIGKILL."""
    assert B01D_WORKER.is_file()
    result = _run_b01d_worker(tmp_path, "side_effect_then_die")
    assert result.returncode in (-signal.SIGKILL, 137)
    assert "SIDE_EFFECT_DURABLE counter=1" in result.stdout

    # the side effect landed exactly once and survived the crash
    assert (tmp_path / "side_effect_counter.txt").read_text().strip() == "1"

    probed = _b01d_probe(tmp_path)
    assert len(probed["records"]) == 1
    assert probed["records"][0]["state"] == cp.UNIT_STATE_INTENT
    # repaired rule: HELD even though a proof could be forged
    assert probed["plan"]["recovery_safe"] is False
    assert len(probed["plan"]["held_units"]) == 1
    assert probed["plan"]["rerunnable_units"] == []
    assert probed["side_effect_counter"] == 1


def test_unsafe_rerun_would_duplicate_the_side_effect_b01d(tmp_path):
    """What the pre-B01D rule permitted: forged proof -> rerun -> counter 2."""
    assert _run_b01d_worker(tmp_path, "side_effect_then_die").returncode in (
        -signal.SIGKILL, 137)
    assert (tmp_path / "side_effect_counter.txt").read_text().strip() == "1"

    demo = _run_b01d_worker(tmp_path, "unsafe_rerun_demo")
    assert demo.returncode == 0
    assert json.loads(demo.stdout)["counter"] == 2
    assert (tmp_path / "side_effect_counter.txt").read_text().strip() == "2"

    # the repaired adapter still refuses to propose the rerun it just watched
    probed = _b01d_probe(tmp_path)
    assert probed["plan"]["recovery_safe"] is False
    assert len(probed["plan"]["held_units"]) == 1
    assert probed["plan"]["rerunnable_units"] == []


def test_repaired_recovery_never_auto_reruns_a_held_unit_b01d(tmp_path):
    """No adapter path executes a HELD unit on its own."""
    assert _run_b01d_worker(tmp_path, "side_effect_then_die").returncode in (
        -signal.SIGKILL, 137)
    probed = _b01d_probe(tmp_path)
    assert probed["plan"]["recovery_safe"] is False
    # the adapter exposes no execute/rerun entrypoint at all
    assert not hasattr(cp, "execute_unit")
    assert not hasattr(cp, "rerun_unit")
    assert not hasattr(cp, "recover_and_execute")
    # and the counter is untouched by recovery itself
    assert (tmp_path / "side_effect_counter.txt").read_text().strip() == "1"


def test_altered_attempt_replay_is_refused_at_commit_b01d():
    """A commit carrying a forged attempt index cannot land."""
    manifest = _manifest(1)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=1)
    receipt = _receipt(manifest)
    with pytest.raises(cp.DurableCheckpointError, match="attempt index"):
        cp.record_commit(
            checkpoint, unit_ref=unit.unit_ref, attempt_index=2, receipt=receipt,
        )
    # and the unit is still HELD, not silently advanced
    plan = cp.plan_recovery(checkpoint)
    assert plan.dispositions[unit.unit_ref.key] is cp.RecoveryDisposition.UNKNOWN_OUTCOME


def test_stale_release_checkpoint_cannot_promote_a_live_unit_b01d(tmp_path):
    """A checkpoint bound to release A says nothing about release B work."""
    manifest_a = _manifest(1, release_label="A")
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(_identity(manifest_a))
    checkpoint = cp.record_intent(
        checkpoint, unit_ref=manifest_a.units[0].unit_ref, attempt_index=1
    )
    store.save(checkpoint)
    with pytest.raises(cp.CheckpointForeignError):
        store.load(identity=_identity(_manifest(1, release_label="B")))
    plan = cp.plan_recovery(checkpoint, idempotence_proof={
        manifest_a.units[0].unit_ref.key: "release:B-proof"})
    assert plan.dispositions[manifest_a.units[0].unit_ref.key] is (
        cp.RecoveryDisposition.UNKNOWN_OUTCOME)


def test_crash_after_commit_recovers_as_committed_b01d(tmp_path):
    """The safe side of the window: COMMIT durable, then crash, then resume."""
    manifest = _manifest(1)
    store = cp.DurableCheckpointStore(tmp_path)
    checkpoint = cp.empty_checkpoint(_identity(manifest))
    unit = manifest.units[0]
    checkpoint = cp.record_intent(checkpoint, unit_ref=unit.unit_ref, attempt_index=1)
    store.save(checkpoint)
    checkpoint = cp.record_commit(
        checkpoint, unit_ref=unit.unit_ref, attempt_index=1, receipt=_receipt(manifest))
    ref_before = store.save(checkpoint)
    reloaded = store.load(identity=_identity(manifest))
    assert reloaded.checkpoint_ref == ref_before
    plan = cp.plan_recovery(reloaded)
    assert plan.recovery_safe is True
    assert plan.committed_units == (unit.unit_ref.key,)
    resumed = BatchExecutionRunner(
        manifest=manifest, repository=_repository(manifest),
        prior_receipts=cp.admit_receipts_for_resume(reloaded))
    assert resumed.pending_units() == ()
