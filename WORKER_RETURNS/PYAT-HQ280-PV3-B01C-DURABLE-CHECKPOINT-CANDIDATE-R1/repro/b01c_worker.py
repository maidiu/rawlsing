#!/usr/bin/env python3
"""B01C durable-checkpoint worker: executes real batch units with a real
write-ahead intent on disk, and can be SIGKILLed at an exact phase.

Phases (argv[2]):
  start    - begin: write durable START intent, then SIGKILL self via os.kill
  commit   - begin + write durable COMMIT receipt for every unit
  partial:N- execute exactly N units then exit 0
  normal   - execute every unit, commit each
  probe    - report checkpoint state as JSON on stdout, change nothing
  corrupt  - corrupt the checkpoint file on disk (torn-write simulation)

Nothing here simulates: the parent kills this process with a real signal, and
the on-disk state is a real file written through the candidate's atomic path.
"""
from __future__ import annotations

import json
import os
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from rawlsing_next.pre553_batch_durable_checkpoint_candidate import (  # noqa: E402
    CheckpointIdentity,
    DurableCheckpointStore,
    admit_receipts_for_resume,
    empty_checkpoint,
    ledger_lock,
    plan_recovery,
    record_commit,
    record_intent,
)
from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchExecutionRunner,
    BatchManifest,
    BatchUnitSpec,
    ExecutionOutcome,
    ExecutorBinding,
)
from rawlsing_next.pre553_c11_repository import C11Repository  # noqa: E402
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402


def _h(label: str) -> str:
    import hashlib
    return hashlib.sha256(label.encode()).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:b01c:{kind.lower()}:{label}", _h(f"{kind}:{label}"))


def _release(label: str) -> ExactRef:
    return ExactRef("C11LogicalRelease", f"release-{label}", _h(f"release:{label}"))


def build_manifest(n: int = 4) -> BatchManifest:
    release = _release("A")
    units = tuple(
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", f"q{i}"),
            release_refs=(release,),
            semantic_input_refs=(_ref("EmpiricalPredicate@1.0.0", f"p{i}"),),
        )
        for i in range(n)
    )
    return BatchManifest(units)


def build_repository(manifest: BatchManifest) -> C11Repository:
    """The accepted runner only calls the accepted exact release resolver."""
    repository = C11Repository()
    for unit in manifest.units:
        for ref in unit.release_refs:
            repository._by_ref[ref.key] = object()
    return repository


def executor_for(unit: BatchUnitSpec) -> ExecutionOutcome:
    return ExecutionOutcome(
        result_refs=(_ref("RESULT", unit.unit_hash),),
        provenance_refs=(_ref("EXECUTION_TRACE", unit.unit_hash),),
    )


def main() -> int:
    root = Path(sys.argv[1])
    phase = sys.argv[2]
    store = DurableCheckpointStore(root)
    manifest = build_manifest()
    identity = CheckpointIdentity.from_manifest(manifest)

    if phase == "probe":
        if not store.exists():
            print(json.dumps({"exists": False}))
            return 0
        checkpoint = store.load(identity=identity)
        plan = plan_recovery(checkpoint)
        print(json.dumps({
            "exists": True,
            "sequence": checkpoint.sequence,
            "digest": checkpoint.content_digest,
            "records": [r.projection() for r in checkpoint.records],
            "plan": plan.summary(),
        }, sort_keys=True))
        return 0

    if phase == "corrupt":
        raw = store.path.read_bytes()
        store.path.write_bytes(raw[: len(raw) // 2])
        print(json.dumps({"corrupted": True, "bytes": len(raw) // 2}))
        return 0

    with ledger_lock(store.lock_path):
        if store.exists():
            checkpoint = store.load(identity=identity)
            prior = admit_receipts_for_resume(checkpoint)
        else:
            checkpoint = empty_checkpoint(identity)
            prior = ()

        if phase == "start":
            # Durable START intent FIRST, then die for real.
            unit = manifest.units[0]
            checkpoint = record_intent(
                checkpoint, unit_ref=unit.unit_ref, attempt_index=1
            )
            store.save(checkpoint)
            sys.stdout.write("INTENT_DURABLE\n")
            sys.stdout.flush()
            os.kill(os.getpid(), signal.SIGKILL)
            return 0

        limit = len(manifest.units)
        if phase.startswith("partial:"):
            limit = int(phase.split(":", 1)[1])

        runner = BatchExecutionRunner(
            manifest=manifest,
            repository=build_repository(manifest),
            prior_receipts=prior,
        )
        bindings = {
            "QUERY": ExecutorBinding(_ref("EXECUTOR", "query"), executor_for),
        }
        for unit in manifest.units[:limit]:
            if unit in runner.pending_units():
                attempt = runner.next_attempt_index(unit)
                # WRITE-AHEAD: durable intent BEFORE the owner side effect.
                checkpoint = record_intent(
                    checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt
                )
                store.save(checkpoint)
                outcome = executor_for(unit)
                receipt = None
                # replay through the accepted runner so the receipt is REAL
                receipts = runner.run(executors=bindings, max_units=1)
                for candidate in receipts:
                    if candidate.unit_ref.key == unit.unit_ref.key:
                        receipt = candidate
                if receipt is None:
                    print(json.dumps({"error": "no receipt"}))
                    return 1
                checkpoint = record_commit(
                    checkpoint, unit_ref=unit.unit_ref,
                    attempt_index=attempt, receipt=receipt,
                )
                store.save(checkpoint)
                del outcome

        plan = plan_recovery(checkpoint)
        print(json.dumps({
            "phase": phase,
            "sequence": checkpoint.sequence,
            "digest": checkpoint.content_digest,
            "batch_state": runner.summary().batch_state,
            "plan": plan.summary(),
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())