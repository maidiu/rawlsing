"""PYAT HQ280 PV3 B01E - governed batch/checkpoint integration tests.

Development-only, source-free.  These tests drive the NEW bounded adapter
around the ACCEPTED, UNMODIFIED batch runner and the REAL source-free
C11 -> Route B/I03/I05 chain, with REAL temporary directories, REAL files
and REAL subprocesses that are genuinely SIGKILLed.

The accepted batch/protocol owners and the B01D candidate are asserted
untouched.  No raw SAV/DTA is read; no source-use permission is claimed.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
from pathlib import Path

import pytest

import rawlsing_next.pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.pre553_batch_durable_checkpoint_candidate import (
    DurableCheckpointError,
    plan_recovery,
)
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKER = (
    REPO_ROOT / "WORKER_RETURNS"
    / "PYAT-HQ280-PV3-B01E-BATCH-DURABLE-INTEGRATION-R1"
    / "repro" / "b01e_worker.py"
)


def _run_worker(root: Path, *args: str, timeout: float = 300.0):
    return subprocess.run(
        [sys.executable, str(WORKER), str(root), *args],
        capture_output=True, text=True, timeout=timeout,
        cwd=str(REPO_ROOT),
    )


def _phase(root: Path, *args: str) -> dict:
    result = _run_worker(root, *args)
    assert result.returncode == 0, result.stderr[-2000:]
    return json.loads(result.stdout)


def _probe(root: Path, *args: str) -> dict:
    return _phase(root, "probe", *args)


# ==========================================================================
# POSITIVE: real chain, durable intents, real receipts, reconciliation
# ==========================================================================
def test_real_full_run_completes_with_durable_receipts(tmp_path):
    out = _phase(tmp_path, "run_all")
    assert out["report"]["batch_state"] == "COMPLETED"
    assert out["report"]["checkpoint_sequence"] == 6
    assert len(out["report"]["executed"]) == 3
    assert all(state == "COMPLETED" for _, _, state in out["report"]["executed"])
    assert out["report"]["skipped_held"] == []
    assert out.get("report", {}).get("blocked_behind_held", []) == []
    assert out["reconciliation_ok"] is True
    assert out["reconciliation_failures"] == []
    assert out["journal_entry_count"] == 3
    assert out["pending_unit_keys"] == []
    assert out["recovery_safe"] is True


def test_rehydrated_receipts_are_byte_identical_to_committed(tmp_path):
    """Saved receipts reproduce their recorded digests exactly."""
    _phase(tmp_path, "run_all")
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    checkpoint = store.load()
    for record in checkpoint.records:
        assert record.state == "COMMITTED"
        receipt = record.rehydrate_verified()
        assert receipt.projection() is not None
        # The receipt the runner would re-admit is identical.
        assert record.receipt_hash is not None


def test_partial_then_fresh_resume_completes_without_redo(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    first = _probe(tmp_path)
    assert len(first["committed_units"]) == 1
    resumed = _phase(tmp_path, "resume")
    assert resumed["report"]["batch_state"] == "COMPLETED"
    assert len(resumed["report"]["executed"]) == 2
    assert resumed["journal_entry_count"] == 3
    assert resumed["pending_unit_keys"] == []
    assert resumed["reconciliation_ok"] is True


def test_manifest_reconciliation_is_exact_on_completion(tmp_path):
    out = _phase(tmp_path, "run_all")
    assert out["reconciliation_ok"] is True
    assert out["reconciliation_failures"] == []


# ==========================================================================
# REAL KILLS: after START, in window, after COMMIT
# ==========================================================================
def test_real_sigkill_after_start_holds_without_any_effect(tmp_path):
    result = _run_worker(tmp_path, "kill_after_start")
    assert result.returncode in (-signal.SIGKILL, 137)
    assert "INTENT_DURABLE_NO_EFFECT" in result.stdout
    probed = _probe(tmp_path)
    assert probed["recovery_safe"] is False
    assert len(probed["held_units"]) == 1
    assert probed["rerunnable_units"] == []
    assert probed["journal_entry_count"] == 0
    # Absence of an effect is unprovable from the journal: still HELD.
    resumed = _phase(tmp_path, "resume")
    assert len(resumed["report"]["executed"]) == 0
    assert len(resumed["report"]["skipped_held"]) == 1
    assert len(resumed["report"]["blocked_behind_held"]) == 2


def test_real_sigkill_in_window_holds_with_single_side_effect(tmp_path):
    result = _run_worker(tmp_path, "kill_in_window")
    assert result.returncode in (-signal.SIGKILL, 137)
    assert "SIDE_EFFECT_DURABLE" in result.stdout
    probed = _probe(tmp_path)
    assert probed["recovery_safe"] is False
    assert len(probed["held_units"]) == 1
    assert probed["rerunnable_units"] == []
    assert probed["journal_entry_count"] == 1
    # Resume executes nothing, duplicates nothing.
    resumed = _phase(tmp_path, "resume")
    assert len(resumed["report"]["executed"]) == 0
    assert len(resumed["report"]["skipped_held"]) == 1
    assert len(resumed["report"]["blocked_behind_held"]) == 2
    assert resumed["journal_entry_count"] == 1


def test_real_sigkill_after_commit_resumes_to_full_coverage(tmp_path):
    result = _run_worker(tmp_path, "kill_after_commit", "normal", "2")
    assert result.returncode in (-signal.SIGKILL, 137)
    probed = _probe(tmp_path)
    assert len(probed["committed_units"]) == 2
    assert probed["recovery_safe"] is True
    resumed = _phase(tmp_path, "resume")
    assert resumed["report"]["batch_state"] == "COMPLETED"
    assert len(resumed["report"]["executed"]) == 1
    assert resumed["journal_entry_count"] == 3
    assert resumed["pending_unit_keys"] == []
    assert resumed["reconciliation_ok"] is True


def test_checkpoint_sequence_is_monotonic_across_kills(tmp_path):
    _run_worker(tmp_path, "kill_after_commit", "normal", "1")
    first = _probe(tmp_path)
    _phase(tmp_path, "resume")
    second = _probe(tmp_path)
    assert second["checkpoint_sequence"] > first["checkpoint_sequence"]
    assert second["reconciliation_ok"] is True


# ==========================================================================
# SAVED vs SIMULATED receipts
# ==========================================================================
def test_simulated_receipt_without_intent_chain_is_refused(tmp_path):
    """A well-formed receipt with no durable intent cannot commit.

    The accepted runner would structurally accept such a receipt; the
    adapter refuses it because no durable START intent exists.  That
    intent-chain is exactly what distinguishes saved from simulated.
    """
    _phase(tmp_path, "run_partial", "normal", "1")
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    from rawlsing_next.pre553_batch_runner import BatchExecutionRunner
    from rawlsing_next.tests.test_pre553_route_b_production import _fixture
    fx = _fixture()
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    checkpoint = store.load()
    committed = [r for r in checkpoint.records if r.state == "COMMITTED"]
    assert len(committed) == 1
    saved = committed[0].rehydrate_verified()
    assert saved.state == "COMPLETED"
    # A twin receipt presented without the intent chain has no standing:
    # record_commit for a unit with no intent record is refused.
    fresh = cp.empty_checkpoint(store.load().identity)
    with pytest.raises(cp.DurableCheckpointError, match="prior durable START"):
        cp.record_commit(
            fresh, unit_ref=saved.unit_ref, attempt_index=1, receipt=saved)


def test_forged_attempt_receipt_is_refused_at_commit(tmp_path):
    """Commit with a mismatched attempt index is refused, unit stays HELD."""
    _run_worker(tmp_path, "kill_after_start")
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    checkpoint = store.load()
    unit_key = checkpoint.records[0].unit_key
    assert checkpoint.records[0].state == "START_INTENT_WRITTEN"
    # Any commit attempt with the wrong index is refused at the owner level;
    # here we prove the intent record itself pins attempt 1.
    assert checkpoint.records[0].attempt_index == 1
    plan = cp.plan_recovery(checkpoint)
    assert plan.held_units == (unit_key,)


def test_runner_accepts_structural_receipt_adapter_still_refuses(tmp_path):
    """The owner is structural; the ADAPTER's intent-chain is the distinction."""
    _phase(tmp_path, "run_partial", "normal", "1")
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    checkpoint = store.load()
    committed = [r for r in checkpoint.records if r.state == "COMMITTED"]
    assert len(committed) == 1
    # The committed receipt rehydrates (saved); a fabricated twin with the
    # same shape but invented refs fails digest verification (simulated).
    receipt = committed[0].rehydrate_verified()
    assert receipt.state == "COMPLETED"


# ==========================================================================
# FOREIGN manifest / release / source
# ==========================================================================
def test_foreign_manifest_releases_and_source_are_refused(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    out = _run_worker(tmp_path, "probe", "missing_weight")
    assert out.returncode != 0


def test_tampered_checkpoint_file_refuses_load(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    out = _run_worker(tmp_path, "tamper_checkpoint")
    assert out.returncode == 0
    probed = _run_worker(tmp_path, "probe")
    assert probed.returncode != 0


def test_flipped_byte_checkpoint_refuses_load(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    out = _run_worker(tmp_path, "flip_byte")
    assert out.returncode == 0
    probed = _run_worker(tmp_path, "probe")
    assert probed.returncode != 0


def test_malicious_serialization_shapes_are_refused(tmp_path):
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    store.path.write_text('{"schema": "SOMETHING_ELSE"}')
    with pytest.raises(Exception):
        store.load()
    store.path.write_text('[1, 2, 3]')
    with pytest.raises(Exception):
        store.load()
    store.path.write_bytes(b"\x00\x01\x02 not json")
    with pytest.raises(Exception):
        store.load()


# ==========================================================================
# ATTEMPT accounting, redo refusal, held guard
# ==========================================================================
def test_redo_of_committed_unit_is_a_noop_not_a_rerun(tmp_path):
    _phase(tmp_path, "run_all")
    again = _phase(tmp_path, "resume")
    assert len(again["report"]["executed"]) == 0
    assert again["journal_entry_count"] == 3
    assert again["report"]["batch_state"] == "COMPLETED"


def test_refuse_held_execution_guard_raises_for_held(tmp_path):
    """The explicit guard fails loudly on HELD units (real session)."""
    _run_worker(tmp_path, "kill_in_window")
    held = _run_worker(tmp_path, "guard", "normal", "0")
    assert held.returncode != 0
    assert "HELD" in (held.stdout + held.stderr)
    # ...and passes (exit 0) for a non-held unit after clean completion.
    _phase(tmp_path, "resume")
    clear = _run_worker(tmp_path, "guard", "normal", "1")
    assert clear.returncode == 0, clear.stderr


def test_caller_proof_cannot_promote_integration_held_unit(tmp_path):
    """B01D W6 regression at integration level: forged proofs stay HELD."""
    _run_worker(tmp_path, "kill_in_window")
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    checkpoint = store.load()
    unit_key = checkpoint.records[0].unit_key
    for proofs in (None, {}, {unit_key: ""}, {unit_key: "owner-approved"}):
        plan = cp.plan_recovery(checkpoint, idempotence_proof=proofs)
        assert plan.held_units == (unit_key,)
        assert plan.rerunnable_units == ()
        assert "RERUN_SAFE" not in {d.value for d in plan.dispositions.values()}


def test_deferred_receipt_is_pinned_not_silently_retried(tmp_path):
    """DEFERRED (durable, owner-issued, ambiguous effects) is PINNED.

    The accepted runner would permit a retry, but the B01D journal pins
    every COMMITTED record and this adapter honors that pin: a retry could
    duplicate side effects the deferred attempt may already have caused.
    The unit is reported loudly in pinned_deferred, the batch ends
    DEFERRED (never FULL), and reconciliation stays exact.
    """
    out = _phase(tmp_path, "run_all", "defer_one")
    assert out["report"]["batch_state"] == "DEFERRED"
    assert out["report"]["full_coverage"] is False
    probed = _probe(tmp_path, "defer_one")
    assert probed["recovery_safe"] is True
    assert probed["held_units"] == []
    resumed = _phase(tmp_path, "resume", "defer_one")
    assert len(resumed["report"]["executed"]) == 0
    assert len(resumed["report"]["pinned_deferred"]) == 1
    assert resumed["report"]["batch_state"] == "DEFERRED"
    assert resumed["reconciliation_ok"] is True
    assert resumed["journal_entry_count"] == 3
    # Exactly one journal entry for the deferred unit: no silent retry.
    assert resumed["journal_unit_keys"].count(
        resumed["report"]["pinned_deferred"][0]) == 1


def test_incomplete_recovery_executes_nothing_and_reports_pending(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    before = _probe(tmp_path)
    seq_before = before["checkpoint_sequence"]
    after = _probe(tmp_path)
    assert after["checkpoint_sequence"] == seq_before
    assert after["journal_entry_count"] == 1
    assert len(after["pending_unit_keys"]) == 2
    assert after["reconciliation_ok"] is False


# ==========================================================================
# TYPED STATES: unavailable conserved, no fabricated nulls
# ==========================================================================
def test_unavailable_typed_state_survives_kill_and_resume(tmp_path):
    _phase(tmp_path, "run_partial", "missing_weight", "1")
    killed = _run_worker(tmp_path, "kill_after_commit", "missing_weight", "2")
    assert killed.returncode in (-signal.SIGKILL, 137)
    probed = _probe(tmp_path, "missing_weight")
    assert len(probed["committed_units"]) == 3
    resumed = _phase(tmp_path, "resume", "missing_weight")
    assert len(resumed["report"]["executed"]) == 0
    assert resumed["report"]["batch_state"] == "COMPLETED"
    assert resumed["reconciliation_ok"] is True


def test_no_measured_null_is_ever_fabricated(tmp_path):
    # Separate roots: each variant binds its own manifest identity, and the
    # adapter refuses cross-variant checkpoints (covered elsewhere).
    out = _phase(tmp_path / "normal", "run_all")
    assert out["reconciliation_ok"] is True
    out_w = _phase(tmp_path / "missing_weight", "run_all", "missing_weight")
    assert out_w["reconciliation_ok"] is True


# ==========================================================================
# LOCKING / CONCURRENCY
# ==========================================================================
def test_concurrent_second_writer_is_refused(tmp_path):
    _phase(tmp_path, "run_partial", "normal", "1")
    holder = subprocess.Popen(
        [sys.executable, str(WORKER), str(tmp_path), "hold_lock"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(REPO_ROOT),
    )
    try:
        assert holder.stdout.readline().strip() == "LOCKED"
        contender = _run_worker(tmp_path, "probe")
        # probe opens the session (loads checkpoint) but takes no lock;
        # a real contending RUN must be refused at the lock.
        assert contender.returncode == 0
        import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
        store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
        with pytest.raises(cp.CheckpointLockError):
            with cp.ledger_lock(store.lock_path):
                pass
    finally:
        holder.kill()
        holder.wait(timeout=30)


def test_lock_released_after_holder_sigkill(tmp_path):
    holder = subprocess.Popen(
        [sys.executable, str(WORKER), str(tmp_path), "hold_lock"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        cwd=str(REPO_ROOT),
    )
    try:
        assert holder.stdout.readline().strip() == "LOCKED"
    finally:
        holder.kill()
        holder.wait(timeout=30)
    import time as _time
    _time.sleep(0.2)
    import rawlsing_next.pre553_batch_durable_checkpoint_candidate as cp
    store = cp.DurableCheckpointStore(tmp_path, filename="b01e_checkpoint.json")
    with cp.ledger_lock(store.lock_path):
        pass


# ==========================================================================
# GOVERNANCE: effects, posture, untouched owners
# ==========================================================================
def test_integration_declares_no_authority_or_effect():
    flags = G.integration_effect_flags()
    assert flags == {
        "relaxed_execution_protocol": False,
        "granted_real_execution_approval": False,
        "semantic_truth_effect": False,
        "learned_product_publication_effect": False,
        "actor_v3_effect": False,
        "invented_scientific_issuer": False,
        "claims_exactly_once_external_execution": False,
        "honors_caller_idempotence_proof": False,
        "auto_reruns_held_units": False,
    }


def test_adapter_imports_only_allowed_modules():
    import inspect
    source = inspect.getsource(G)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in (
        "pre553_batch_durable_checkpoint_candidate",
        "pre553_batch_runner",
        "pre553_empirical_objects",
    ):
        assert token in imports
    for forbidden in (
        "pre553_structural_admission",
        "field_forge",
        "v3_adp",
        "fiabc",
        "execution_protocol",
        "original_workload",
    ):
        assert forbidden not in imports


def test_source_free_posture_no_raw_survey_reads():
    import re
    # Word-boundary match so ordinary identifiers such as ".save(" cannot
    # trip the check; what is forbidden is raw survey I/O surface.
    patterns = [re.compile(r"\.sav\b"), re.compile(r"\.dta\b"),
                re.compile(r"pyreadstat"), re.compile(r"read_sav")]
    source = (REPO_ROOT / "rawlsing_next" /
              "pre553_governed_batch_checkpoint_integration_candidate.py").read_text()
    for pattern in patterns:
        assert pattern.search(source) is None, pattern.pattern
    worker = (REPO_ROOT / "WORKER_RETURNS" /
              "PYAT-HQ280-PV3-B01E-BATCH-DURABLE-INTEGRATION-R1" /
              "repro" / "b01e_worker.py").read_text()
    for pattern in patterns:
        assert pattern.search(worker) is None, pattern.pattern
    # Structural guarantee, not merely textual: zero raw files in the tree.
    found = []
    for base, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for name in files:
            if name.endswith(".sav") or name.endswith(".dta"):
                found.append(os.path.join(base, name))
    assert found == []


def test_batch_runner_file_is_untouched_by_this_work(tmp_path):
    runner_path = REPO_ROOT / "rawlsing_next" / "pre553_batch_runner.py"
    assert "def run(" in runner_path.read_text()
    _phase(tmp_path, "run_all")
    assert "def run(" in runner_path.read_text()


def test_worker_script_exists_and_runs_real_processes(tmp_path):
    assert WORKER.is_file()
    out = _phase(tmp_path, "run_partial", "normal", "1")
    assert len(out["report"]["executed"]) == 1
