#!/usr/bin/env python3
"""B01E integration worker: REAL C11 -> Route B/I03/I05 -> Batch units with
durable write-ahead intents, killable at exact crash windows.

Usage: b01e_worker.py <root> <phase> [variant] [n]

Phases:
  run_all            - full chain + session + run_to_completion; print report.
  run_partial        - complete exactly [n] units, exit 0.
  kill_after_commit  - complete [n] units, then SIGKILL self.
  kill_after_start   - durable START intent for unit 0, then SIGKILL self
                       BEFORE any owner execution (no side effect; recovery
                       must still HELD: absence is unprovable from the journal).
  kill_in_window     - durable START, REAL owner execution, durable
                       side-effect journal append, then SIGKILL self BEFORE
                       the durable COMMIT.  The exact B01CR window.
  resume             - fresh-process recover + run_to_completion to finish.
  probe              - report checkpoint + plan + journal + reconciliation.
  tamper_checkpoint  - truncate the checkpoint file on disk.
  flip_byte          - flip one byte of the checkpoint file (digest mismatch).
  hold_lock          - acquire the ledger lock, print LOCKED, sleep 30s.

Variants ([variant], default "normal"):
  normal         - standard fixture; all facts SUPPORTED/DISCOVERED.
  missing_weight - weighted Y fact is UNAVAILABLE (typed negative conserved).
  defer_one      - QUERY executor raises BatchDeferred for unit 0 on attempt 1.

Nothing here simulates the crash, the filesystem or the owners: the parent
observes real signal exits, and every state change goes through real files
with fsync and the REAL accepted owners.
"""
from __future__ import annotations

import json
import os
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

import rawlsing_next.pre553_governed_batch_checkpoint_integration_candidate as G  # noqa: E402
from rawlsing_next.pre553_batch_durable_checkpoint_candidate import (  # noqa: E402
    DurableCheckpointStore, empty_checkpoint, ledger_lock, plan_recovery,
    record_commit, record_intent,
)
from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchDeferred, BatchExecutionRunner, BatchManifest, BatchUnitSpec,
    ExecutionOutcome, ExecutorBinding,
)
from rawlsing_next.pre553_route_b_production import (  # noqa: E402
    execute_route_b_production,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture  # noqa: E402


def _build_chain(variant: str):
    """Real source-free C11 -> Route B -> manifest + real executors."""
    fx = _fixture(missing_weight=(variant == "missing_weight"))
    production = execute_route_b_production(
        source=fx["stream"],
        projection=fx["projection"],
        runtime_catalog=fx["catalog"],
        i03_requests=fx["requests"],
        discovery_authority_ref=fx["discovery_authority"].ref,
    )
    release_ref = production.c11_release.release_ref
    repository = production.repository_binding.executor.repository
    route_executor = production.repository_binding.executor
    defer_state = {"deferred_once": False}

    def _query_execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        if variant == "defer_one" and not defer_state["deferred_once"]:
            if unit.job_ref == fx["raw_query"].ref:
                defer_state["deferred_once"] = True
                raise BatchDeferred("B01E_DEFER_ONCE", "first attempt deferred")
        predicates = [r for r in unit.semantic_input_refs
                      if r.kind == "EmpiricalPredicate@1.0.0"]
        outcome = route_executor.execute_i03(
            query_ref=unit.job_ref, predicate_ref=predicates[0])
        return ExecutionOutcome(
            result_refs=tuple(f.ref for f in outcome.facts),
            provenance_refs=(unit.job_ref, *unit.semantic_input_refs))

    def _discovery_execute(unit: BatchUnitSpec) -> ExecutionOutcome:
        outcome = route_executor.execute_i05(discovery_authority_ref=unit.job_ref)
        return ExecutionOutcome(
            result_refs=tuple(r.ref for r in outcome.receipts),
            provenance_refs=(unit.job_ref, *unit.semantic_input_refs))

    manifest = BatchManifest((
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=fx["raw_query"].ref,
            release_refs=(release_ref,),
            semantic_input_refs=(fx["all_p"].ref, fx["qauth"].ref),
        ),
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=fx["weighted_query"].ref,
            release_refs=(release_ref,),
            semantic_input_refs=(fx["all_p"].ref, fx["qauth"].ref),
        ),
        BatchUnitSpec(
            job_kind="DISCOVERY",
            job_ref=fx["discovery_authority"].ref,
            release_refs=(release_ref,),
            semantic_input_refs=(fx["dauth"].ref,),
        ),
    ))
    executors = {
        "QUERY": ExecutorBinding(fx["qauth"].ref, _query_execute),
        "DISCOVERY": ExecutorBinding(fx["dauth"].ref, _discovery_execute),
    }
    return {
        "manifest": manifest,
        "repository": repository,
        "executors": executors,
        "source_sha": fx["stream"].source_sha256,
        "production": production,
    }


def _open(root: Path, variant: str):
    chain = _build_chain(variant)
    session = G.open_session(
        manifest=chain["manifest"],
        repository=chain["repository"],
        executors=chain["executors"],
        root=root,
        source_sha256=chain["source_sha"],
    )
    return chain, session


def _report(root: Path, session, extra=None) -> dict:
    report = G.recover(session)
    journal = G._read_journal(session.side_effect_journal_path)
    out = {
        "manifest_hash": session.identity.manifest_hash,
        "checkpoint_sequence": report.checkpoint_sequence,
        "recovery_safe": report.plan.recovery_safe,
        "held_units": list(report.plan.held_units),
        "rerunnable_units": list(report.plan.rerunnable_units),
        "committed_units": list(report.plan.committed_units),
        "pending_unit_keys": list(report.pending_unit_keys),
        "reconciliation_ok": report.reconciliation.ok,
        "reconciliation_failures": [dict(f) for f in report.reconciliation.failures],
        "journal_entry_count": len(journal),
        "journal_unit_keys": [e["unit_key"] for e in journal],
        "disregarded_caller_proofs": dict(report.plan.disregarded_caller_proofs),
    }
    if extra:
        out.update(extra)
    return out


def main() -> int:
    root = Path(sys.argv[1])
    phase = sys.argv[2]
    variant = sys.argv[3] if len(sys.argv) > 3 else "normal"
    count = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    if phase == "guard":
        chain, session = _open(root, variant)
        index = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        unit = session.manifest.units[index]
        try:
            G.refuse_held_execution(session, unit.unit_ref.key)
        except G.IntegrationHeldError as exc:
            print(json.dumps({"guard": "REFUSED_HELD", "detail": str(exc)}))
            return 1
        print(json.dumps({"guard": "CLEAR", "unit_key": unit.unit_ref.key}))
        return 0

    if phase == "hold_lock":
        chain, session = _open(root, variant)
        with ledger_lock(session.store.lock_path):
            print("LOCKED", flush=True)
            import time
            time.sleep(30)
        return 0

    if phase == "probe":
        chain, session = _open(root, variant)
        print(json.dumps(_report(root, session), sort_keys=True))
        return 0

    if phase == "tamper_checkpoint":
        chain, session = _open(root, variant)
        raw = session.store.path.read_bytes()
        session.store.path.write_bytes(raw[: len(raw) // 2])
        print(json.dumps({"tampered": True, "bytes": len(raw) // 2}))
        return 0

    if phase == "flip_byte":
        chain, session = _open(root, variant)
        raw = bytearray(session.store.path.read_bytes())
        raw[len(raw) // 2] ^= 0x01
        session.store.path.write_bytes(bytes(raw))
        print(json.dumps({"flipped": True}))
        return 0

    if phase == "run_all":
        chain, session = _open(root, variant)
        report = G.run_to_completion(session)
        print(json.dumps({"phase": "run_all",
                          "report": report.summary(),
                          **_report(root, session)}, sort_keys=True))
        return 0

    if phase == "run_partial":
        chain, session = _open(root, variant)
        report = G.run_to_completion(session, max_units=count)
        print(json.dumps({"phase": f"partial:{count}",
                          "report": report.summary()}, sort_keys=True))
        return 0

    if phase == "kill_after_commit":
        chain, session = _open(root, variant)
        G.run_to_completion(session, max_units=count)
        sys.stdout.write(f"COMMITTED_{count}_THEN_DYING\n")
        sys.stdout.flush()
        os.kill(os.getpid(), signal.SIGKILL)
        return 0

    if phase == "kill_after_start":
        chain, session = _open(root, variant)
        checkpoint = (session.store.load(identity=session.identity)
                      if session.store.exists()
                      else empty_checkpoint(session.identity))
        runner = BatchExecutionRunner(
            manifest=session.manifest, repository=session.repository,
            prior_receipts=G.admit_saved_receipts(session)
            if session.store.exists() else ())
        pending = runner.pending_units()
        if not pending:
            print(json.dumps({"error": "nothing pending"}))
            return 1
        unit = pending[0]
        attempt = runner.next_attempt_index(unit)
        with ledger_lock(session.store.lock_path):
            checkpoint = record_intent(
                checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt)
            session.store.save(checkpoint)
        sys.stdout.write("INTENT_DURABLE_NO_EFFECT\n")
        sys.stdout.flush()
        os.kill(os.getpid(), signal.SIGKILL)
        return 0

    if phase == "kill_in_window":
        # Replicates run_to_completion's per-unit steps for unit 0 ONLY, so
        # the kill lands between the durable side-effect journal append and
        # the durable COMMIT.  Uses the same primitives (never a shortcut).
        chain, session = _open(root, variant)
        checkpoint = (session.store.load(identity=session.identity)
                      if session.store.exists()
                      else empty_checkpoint(session.identity))
        runner = BatchExecutionRunner(
            manifest=session.manifest, repository=session.repository,
            prior_receipts=G.admit_saved_receipts(session)
            if session.store.exists() else ())
        pending = runner.pending_units()
        if not pending:
            print(json.dumps({"error": "nothing pending"}))
            return 1
        unit = pending[0]
        attempt = runner.next_attempt_index(unit)
        with ledger_lock(session.store.lock_path):
            checkpoint = record_intent(
                checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt)
            session.store.save(checkpoint)
        receipts = runner.run(executors=session.executors, max_units=1)
        receipt = next(
            r for r in receipts if r.unit_ref.key == unit.unit_ref.key)
        journal_seq = G._append_journal_line(
            session.side_effect_journal_path,
            {"unit_key": unit.unit_ref.key, "attempt_index": attempt,
             "result_refs": [ref.as_dict() for ref in receipt.result_refs],
             "receipt_state": receipt.state,
             "manifest_hash": session.identity.manifest_hash})
        sys.stdout.write(f"SIDE_EFFECT_DURABLE journal_seq={journal_seq}\n")
        sys.stdout.flush()
        # Die BEFORE record_commit: the effect is journaled, the receipt lost.
        os.kill(os.getpid(), signal.SIGKILL)
        return 0

    if phase == "resume":
        chain, session = _open(root, variant)
        report = G.run_to_completion(session)
        print(json.dumps({"phase": "resume",
                          "report": report.summary(),
                          **_report(root, session)}, sort_keys=True))
        return 0

    print(json.dumps({"error": f"unknown phase {phase!r}"}))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
