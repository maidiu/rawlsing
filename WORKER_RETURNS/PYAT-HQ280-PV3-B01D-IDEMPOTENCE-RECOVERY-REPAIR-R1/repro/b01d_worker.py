#!/usr/bin/env python3
"""B01D idempotence-repair worker: real crash AFTER a durable external side
effect but BEFORE the durable COMMIT, with a tangible side-effect counter.

Phases (argv[2]):
  side_effect_then_die - durable START intent, then a DURABLE external side
                         effect (atomic counter increment + fsync), then
                         SIGKILL self before COMMIT.  Models a crash in the
                         exact window B01CR proved dangerous.
  read_counter         - print the durable side-effect counter, change nothing.
  unsafe_rerun_demo    - DEMONSTRATION ONLY of the OLD B01C defect: re-execute
                         the side effect for a HELD unit exactly as the old
                         `if key in proofs: RERUN_SAFE` rule would have
                         permitted.  Proves duplication is real, in a tmpdir.
  probe                - report checkpoint state + recovery plan as JSON.

Nothing here simulates the crash or the filesystem: the parent observes a
real signal exit, and every state change goes through real files with fsync.
"""
from __future__ import annotations

import contextlib
import json
import os
import signal
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from rawlsing_next.pre553_batch_durable_checkpoint_candidate import (  # noqa: E402
    CheckpointIdentity,
    DurableCheckpointStore,
    empty_checkpoint,
    ledger_lock,
    plan_recovery,
    record_commit,
    record_intent,
)
from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_empirical_objects import ExactRef  # noqa: E402


def _h(label: str) -> str:
    import hashlib
    return hashlib.sha256(label.encode()).hexdigest()


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:b01d:{kind.lower()}:{label}", _h(f"{kind}:{label}"))


def _release(label: str) -> ExactRef:
    return ExactRef("C11LogicalRelease", f"release-{label}", _h(f"release:{label}"))


def build_manifest() -> BatchManifest:
    release = _release("A")
    return BatchManifest((
        BatchUnitSpec(
            job_kind="QUERY",
            job_ref=_ref("EmpiricalQuerySpec@1.0.0", "q0"),
            release_refs=(release,),
            semantic_input_refs=(_ref("EmpiricalPredicate@1.0.0", "p0"),),
        ),
    ))


def _fsync_dir(directory: Path) -> None:
    fd = os.open(str(directory), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic_write_text(path: Path, text: str) -> None:
    """Durable atomic write for the side-effect counter file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp = Path(name)
    try:
        with os.fdopen(fd, "w") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        _fsync_dir(path.parent)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()


def counter_path(root: Path) -> Path:
    return root / "side_effect_counter.txt"


def read_counter(root: Path) -> int:
    path = counter_path(root)
    if not path.is_file():
        return 0
    return int(path.read_text().strip())


def durable_side_effect(root: Path) -> int:
    """The modeled EXTERNAL side effect: durably increments a counter.

    Once this returns, the effect has landed and cannot be rolled back —
    exactly like sending a message, charging an account, or publishing a row.
    """
    value = read_counter(root) + 1
    _atomic_write_text(counter_path(root), f"{value}\n")
    return value


def main() -> int:
    root = Path(sys.argv[1])
    phase = sys.argv[2]
    store = DurableCheckpointStore(root, filename="b01d_checkpoint.json")
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
            "side_effect_counter": read_counter(root),
        }, sort_keys=True))
        return 0

    if phase == "read_counter":
        print(json.dumps({"side_effect_counter": read_counter(root)}))
        return 0

    if phase == "unsafe_rerun_demo":
        # DEMONSTRATION ONLY of the pre-B01D defect: re-run the side effect
        # for the HELD unit, as the old caller-proof rule permitted.
        value = durable_side_effect(root)
        print(json.dumps({"unsafe_rerun_performed": True, "counter": value}))
        return 0

    if phase == "side_effect_then_die":
        with ledger_lock(store.lock_path):
            checkpoint = (
                store.load(identity=identity)
                if store.exists() else empty_checkpoint(identity)
            )
            unit = manifest.units[0]
            # 1. durable WRITE-AHEAD START intent, strictly first.
            checkpoint = record_intent(
                checkpoint, unit_ref=unit.unit_ref, attempt_index=1
            )
            store.save(checkpoint)
            # 2. the EXTERNAL side effect lands durably.
            value = durable_side_effect(root)
            sys.stdout.write(f"SIDE_EFFECT_DURABLE counter={value}\n")
            sys.stdout.flush()
            # 3. die BEFORE the durable COMMIT: the receipt is lost, the
            #    effect is not.  Recovery must see UNKNOWN_OUTCOME/HELD.
            os.kill(os.getpid(), signal.SIGKILL)
        return 0

    print(json.dumps({"error": f"unknown phase {phase!r}"}))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
