"""PYAT HQ280 PV3 B01C - durable WRITE_AHEAD batch checkpoint CANDIDATE.

Development-only standalone adapter around the ACCEPTED, UNMODIFIED
``rawlsing_next.pre553_batch_runner`` owner.  It supplies the capability B01
measured as absent (F-01) and that the execution protocol mandates for
REAL_EXECUTION (F-02): a versioned, content-addressed, atomically persisted
write-ahead checkpoint with ``durable_checkpoint_ref``.

What this candidate does
-----------------------
* binds a checkpoint to ONE exact ``BatchManifest`` identity (manifest hash and
  ref) plus the exact release refs it carries;
* records a durable **START / write-ahead intent** record BEFORE any owner side
  effect, then a durable **COMMITTED** record carrying the owner's real
  ``UnitExecutionReceipt`` projection and its content digest;
* persists through ``write temp -> fsync(file) -> os.replace -> fsync(dir)`` so
  a torn or half-written checkpoint is never observable at the live path;
* rehydrates typed ``ExactRef`` / ``UnitExecutionReceipt`` values with full
  digest verification (the owner exposes ``projection()`` but no ``from_dict``);
* holds an exclusive ``fcntl.flock`` ledger lock so concurrent writers cannot
  interleave;
* refuses torn, truncated, corrupt, digest-mismatched, foreign-manifest and
  foreign-scope checkpoints.

The exactly-once hazard (deliberate, not a defect)
--------------------------------------------------
Write-ahead intent ALONE does NOT prove exactly-once external execution.  If a
process dies between an owner side effect and the durable COMMITTED record, the
true outcome is UNKNOWN.  This candidate therefore classifies that case as
``RecoveryDisposition.UNKNOWN_OUTCOME`` and **holds the unit** rather than
silently rerunning it.

B01D fail-closed repair: a caller-supplied ``idempotence_proof`` mapping can
NEVER promote an unknown outcome, no matter what keys or values it carries —
not even a non-empty string.  Caller assertion is not proof.  ``RERUN_SAFE``
is currently UNREACHABLE: no accepted owner issues a verifiable idempotence
credential, so the automatic upgrade path is DISABLED and every
START-without-COMMIT unit stays HELD.  Presented caller proofs are recorded
as disregarded evidence, never honored.  See ``plan_recovery`` and
``IDEMPOTENCE_ISSUER_HOLD``.

Scope ceiling
-------------
Source-free development only.  This adapter does NOT relax or replace
``rabochii_execution_protocol``, does NOT grant REAL_EXECUTION approval, does
NOT adopt itself, and is NOT a scientific issuer.  A source-free PASS here is
explicitly **not** protocol approval; that remains a competent owner's act.
"""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_batch_runner import (
    BatchIntegrityError,
    BatchManifest,
    UnitExecutionReceipt,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


CHECKPOINT_CONTRACT_ID = "PYAT_HQ280_B01C_DURABLE_CHECKPOINT_CANDIDATE@1.0.0"
CHECKPOINT_SCHEMA_ID = "PYAT_HQ280_B01C_DURABLE_CHECKPOINT@1.0.0"
CHECKPOINT_STATE_VERSION = "1.0.0"

#: Units are identified by kind + ref key; these mirror the accepted owner.
UNIT_STATE_INTENT = "START_INTENT_WRITTEN"
UNIT_STATE_COMMITTED = "COMMITTED"


class DurableCheckpointError(ValueError):
    """The durable checkpoint candidate refuses this request."""


class CheckpointLockError(DurableCheckpointError):
    """Another writer holds the exclusive ledger lock."""


class CheckpointTornError(DurableCheckpointError):
    """The checkpoint is torn, truncated, corrupt or digest-mismatched."""


class CheckpointForeignError(DurableCheckpointError):
    """The checkpoint belongs to a different manifest, release or scope."""


class RecoveryDisposition(str, Enum):
    """What recovery may lawfully do with one unit.

    ``RERUN_SAFE`` is currently UNREACHABLE (see ``IDEMPOTENCE_ISSUER_HOLD``):
    no accepted owner issues a verifiable idempotence credential, so no
    START-without-COMMIT unit may be proposed for rerun.  ``UNKNOWN_OUTCOME``
    is a HOLD: the side effect may or may not have landed.
    """

    ALREADY_COMMITTED = "ALREADY_COMMITTED"
    RERUN_SAFE = "RERUN_SAFE"
    UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME"
    NEVER_STARTED = "NEVER_STARTED"


#: Explicit issuance hold: no accepted, competent existing owner supplies a
#: verifiable, exact unit/release/manifest/side-effect/idempotence attestation
#: (exact ref + issuer + verified signature/schema).  Until such a credential
#: exists and verifies, the UNKNOWN_OUTCOME -> RERUN_SAFE upgrade path is
#: DISABLED and every unknown outcome stays HELD.  A caller-supplied mapping,
#: string or object is never a substitute.
IDEMPOTENCE_ISSUER_HOLD = MappingProxyType({
    "hold_id": "IDEMPOTENCE_ISSUER_HOLD",
    "state": "HELD__NO_VERIFIED_IDEMPOTENCE_ISSUER",
    "automatic_rerun_upgrade": "DISABLED",
    "caller_proofs_honored": False,
    "required_future_credential": {
        "exact_unit_key": "the precise unit_ref.key the claim covers",
        "exact_release_refs": "the C11LogicalRelease refs the claim covers",
        "exact_manifest_hash": "the BatchManifest the claim covers",
        "executor_identity": "the exact executor whose side effect is claimed idempotent",
        "side_effect_classification": "a verifiable statement of what the side effect is",
        "issuer": "an already-accepted, demonstrably competent existing owner",
        "verification": "signature/schema check against that owner's accepted contract",
    },
    "forbidden_substitutes": [
        "caller mapping key presence",
        "caller string value (including non-empty strings)",
        "caller dict/object shape",
        "content hash alone",
        "claimed issuer name alone",
        "dataclass type alone",
    ],
})


@dataclass(frozen=True)
class CheckpointIdentity:
    """Exact identity a checkpoint is bound to.  Drift is always refused."""

    manifest_hash: str
    manifest_ref: ExactRef
    release_refs: tuple[ExactRef, ...]
    unit_keys: tuple[str, ...]
    protocol_profile: str = "DEVELOPMENT_SOURCE_FREE"

    @classmethod
    def from_manifest(cls, manifest: BatchManifest) -> "CheckpointIdentity":
        if not isinstance(manifest, BatchManifest):
            raise DurableCheckpointError("exact BatchManifest is required")
        releases = tuple(
            ref for unit in manifest.units for ref in unit.release_refs
        )
        return cls(
            manifest_hash=manifest.manifest_hash,
            manifest_ref=manifest.manifest_ref,
            release_refs=tuple(sorted({ref.key: ref for ref in releases}.values(),
                                      key=lambda r: r.key)),
            unit_keys=tuple(unit.unit_ref.key for unit in manifest.units),
        )

    def projection(self) -> dict[str, Any]:
        return {
            "manifest_hash": self.manifest_hash,
            "manifest_ref": self.manifest_ref.as_dict(),
            "release_refs": [ref.as_dict() for ref in self.release_refs],
            "unit_keys": list(self.unit_keys),
            "protocol_profile": self.protocol_profile,
        }

    @classmethod
    def from_projection(cls, value: Mapping[str, Any]) -> "CheckpointIdentity":
        try:
            return cls(
                manifest_hash=str(value["manifest_hash"]),
                manifest_ref=_ref(value["manifest_ref"]),
                release_refs=tuple(_ref(x) for x in value["release_refs"]),
                unit_keys=tuple(str(x) for x in value["unit_keys"]),
                protocol_profile=str(value.get("protocol_profile",
                                               "DEVELOPMENT_SOURCE_FREE")),
            )
        except (KeyError, TypeError) as exc:
            raise CheckpointTornError(
                f"checkpoint identity projection is incomplete: {exc}"
            ) from exc


@dataclass(frozen=True)
class UnitRecord:
    """One durable per-unit record: write-ahead intent, then commit."""

    unit_key: str
    unit_ref: ExactRef
    state: str
    attempt_index: int
    intent_hash: str
    receipt_projection: dict[str, Any] | None
    receipt_hash: str | None
    prior_attempt_count: int = 0

    def __post_init__(self) -> None:
        if self.state not in {UNIT_STATE_INTENT, UNIT_STATE_COMMITTED}:
            raise DurableCheckpointError(f"unknown unit state {self.state!r}")
        if not isinstance(self.attempt_index, int) or isinstance(
            self.attempt_index, bool
        ) or self.attempt_index < 1:
            raise DurableCheckpointError("attempt_index must be a positive integer")
        if self.state == UNIT_STATE_COMMITTED:
            if not isinstance(self.receipt_projection, Mapping):
                raise DurableCheckpointError(
                    "COMMITTED record requires the owner's receipt projection"
                )
            if not self.receipt_hash:
                raise DurableCheckpointError(
                    "COMMITTED record requires the receipt content digest"
                )
        elif self.receipt_projection is not None or self.receipt_hash is not None:
            raise DurableCheckpointError(
                "START intent record may not carry a committed receipt"
            )

    def projection(self) -> dict[str, Any]:
        return {
            "unit_key": self.unit_key,
            "unit_ref": self.unit_ref.as_dict(),
            "state": self.state,
            "attempt_index": self.attempt_index,
            "intent_hash": self.intent_hash,
            "receipt_projection": self.receipt_projection,
            "receipt_hash": self.receipt_hash,
            "prior_attempt_count": self.prior_attempt_count,
        }

    @classmethod
    def from_projection(cls, value: Mapping[str, Any]) -> "UnitRecord":
        try:
            return cls(
                unit_key=str(value["unit_key"]),
                unit_ref=_ref(value["unit_ref"]),
                state=str(value["state"]),
                attempt_index=int(value["attempt_index"]),
                intent_hash=str(value["intent_hash"]),
                receipt_projection=(
                    dict(value["receipt_projection"])
                    if value.get("receipt_projection") is not None else None
                ),
                receipt_hash=(
                    str(value["receipt_hash"])
                    if value.get("receipt_hash") is not None else None
                ),
                prior_attempt_count=int(value.get("prior_attempt_count", 0)),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise CheckpointTornError(
                f"unit record projection is incomplete: {exc}"
            ) from exc

    def rehydrate_receipt(self) -> UnitExecutionReceipt:
        """Rebuild the owner's typed receipt and verify its exact identity."""
        if self.state != UNIT_STATE_COMMITTED or self.receipt_projection is None:
            raise DurableCheckpointError("unit record holds no committed receipt")
        projection = self.receipt_projection
        digest = _sha256_json(projection)
        if digest != self.receipt_hash:
            raise CheckpointTornError(
                "committed receipt digest mismatch; refusing rehydration"
            )
        try:
            return UnitExecutionReceipt(
                manifest_hash=projection["manifest_hash"],
                unit_ref=_ref(projection["unit_ref"]),
                attempt_index=int(projection["attempt_index"]),
                state=str(projection["state"]),
                execution_performed=bool(projection["execution_performed"]),
                executor_ref=(
                    _ref(projection["executor_ref"])
                    if projection.get("executor_ref") is not None else None
                ),
                result_refs=tuple(_ref(r) for r in projection["result_refs"]),
                provenance_refs=tuple(
                    _ref(r) for r in projection["provenance_refs"]
                ),
                failure_code=projection.get("failure_code"),
                detail_hash=projection.get("detail_hash"),
            )
        except (BatchIntegrityError, KeyError, TypeError, ValueError) as exc:
            raise CheckpointTornError(
                f"committed receipt failed exact owner reconstruction: {exc}"
            ) from exc

    def rehydrate_verified(self) -> UnitExecutionReceipt:
        """Rehydrate AND prove the owner accepted the same identity."""
        receipt = self.rehydrate_receipt()
        if _sha256_json(receipt.projection()) != self.receipt_hash:
            raise CheckpointTornError(
                "rehydrated receipt does not reproduce its recorded digest"
            )
        if receipt.unit_ref.key != self.unit_key:
            raise CheckpointForeignError(
                "rehydrated receipt unit identity does not match its record"
            )
        return receipt


@dataclass(frozen=True)
class DurableCheckpoint:
    """One atomically persisted checkpoint document."""

    identity: CheckpointIdentity
    records: tuple[UnitRecord, ...]
    sequence: int
    checkpoint_version: str = CHECKPOINT_STATE_VERSION

    def __post_init__(self) -> None:
        if self.checkpoint_version != CHECKPOINT_STATE_VERSION:
            raise DurableCheckpointError("unsupported checkpoint state version")
        if not isinstance(self.sequence, int) or isinstance(
            self.sequence, bool
        ) or self.sequence < 0:
            raise DurableCheckpointError("sequence must be a nonnegative integer")
        keys = [r.unit_key for r in self.records]
        if len(set(keys)) != len(keys):
            raise DurableCheckpointError("duplicate unit key in checkpoint")
        unknown = sorted(set(keys) - set(self.identity.unit_keys))
        if unknown:
            raise CheckpointForeignError(
                f"checkpoint carries units outside its manifest: {unknown}"
            )

    def by_unit(self, unit_key: str) -> UnitRecord | None:
        for record in self.records:
            if record.unit_key == unit_key:
                return record
        return None

    def content_material(self) -> dict[str, Any]:
        return {
            "schema": CHECKPOINT_SCHEMA_ID,
            "contract": CHECKPOINT_CONTRACT_ID,
            "checkpoint_version": self.checkpoint_version,
            "identity": self.identity.projection(),
            "sequence": self.sequence,
            "records": [r.projection() for r in self.records],
        }

    @property
    def content_digest(self) -> str:
        return _sha256_json(self.content_material())

    @property
    def checkpoint_ref(self) -> ExactRef:
        return ExactRef(
            "PYAT_HQ280_B01C_DURABLE_CHECKPOINT@1.0.0",
            f"urn:rawlsing:hq280:b01c:durable-checkpoint:sha256:{self.content_digest}",
            self.content_digest,
        )

    def projection(self) -> dict[str, Any]:
        return {**self.content_material(), "content_digest": self.content_digest}

    def verify_self_consistency(self) -> None:
        material = self.content_material()
        observed = _sha256_json(material)
        if observed != self.content_digest:
            raise CheckpointTornError("checkpoint content digest self-mismatch")

    @classmethod
    def from_projection(cls, value: Mapping[str, Any]) -> "DurableCheckpoint":
        try:
            checkpoint = cls(
                identity=CheckpointIdentity.from_projection(value["identity"]),
                records=tuple(
                    UnitRecord.from_projection(r) for r in value["records"]
                ),
                sequence=int(value["sequence"]),
                checkpoint_version=str(
                    value.get("checkpoint_version", CHECKPOINT_STATE_VERSION)
                ),
            )
        except DurableCheckpointError:
            raise
        except (KeyError, TypeError, ValueError) as exc:
            raise CheckpointTornError(
                f"checkpoint document is structurally torn: {exc}"
            ) from exc
        checkpoint.verify_self_consistency()
        recorded = value.get("content_digest")
        if recorded is not None and str(recorded) != checkpoint.content_digest:
            raise CheckpointTornError(
                "checkpoint document digest does not match its content"
            )
        return checkpoint

    def assert_bound_to(self, identity: CheckpointIdentity) -> None:
        if self.identity.projection() != identity.projection():
            raise CheckpointForeignError(
                "checkpoint is bound to a different manifest/release/scope; "
                "refusing foreign checkpoint"
            )

    def receipts(self) -> tuple[UnitExecutionReceipt, ...]:
        return tuple(
            r.rehydrate_verified()
            for r in self.records
            if r.state == UNIT_STATE_COMMITTED
        )

    def next_sequence(self) -> int:
        return self.sequence + 1


# --------------------------------------------------------------------------
# Atomic durable persistence
# --------------------------------------------------------------------------
def _sha256_json(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _fsync_dir(directory: Path) -> None:
    """Persist a directory entry.

    ``os.replace`` is only durable once the containing directory is fsynced.
    The existing EE-P2X ``_atomic_write_bytes`` omits this step; this candidate
    closes that gap.
    """
    fd = os.open(str(directory), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic_write_bytes(path: Path, data: bytes) -> str:
    """write -> fsync(file) -> replace -> fsync(dir). Returns the sha256."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        _fsync_dir(path.parent)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()
    return _sha256_bytes(data)


def _encode(projection: Mapping[str, Any]) -> bytes:
    return json.dumps(projection, sort_keys=True, indent=2).encode() + b"\n"


def _ref(value: Any) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if not isinstance(value, Mapping):
        raise CheckpointTornError("reference projection must be a mapping")
    if set(value) != {"kind", "object_id", "content_hash"}:
        raise CheckpointTornError("reference projection has the wrong shape")
    try:
        return ExactRef(value["kind"], value["object_id"], value["content_hash"])
    except Exception as exc:  # noqa: BLE001 - fail closed on any ref defect
        raise CheckpointTornError(f"reference projection is invalid: {exc}") from exc


@contextlib.contextmanager
def ledger_lock(lock_path: Path, *, blocking: bool = False):
    """Exclusive advisory lock so concurrent writers cannot interleave."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+")
    try:
        flags = fcntl.LOCK_EX if blocking else fcntl.LOCK_EX | fcntl.LOCK_NB
        try:
            fcntl.flock(handle.fileno(), flags)
        except BlockingIOError as exc:
            raise CheckpointLockError(
                "another writer holds the durable checkpoint ledger lock"
            ) from exc
        yield
    finally:
        with contextlib.suppress(Exception):
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


class DurableCheckpointStore:
    """Atomic, locked, digest-verified durable checkpoint persistence."""

    def __init__(self, root: Path, *, filename: str = "b01c_checkpoint.json"):
        if not filename or "/" in filename or filename.startswith("."):
            raise DurableCheckpointError("checkpoint filename must be a plain name")
        self.root = Path(root)
        self.path = self.root / filename
        self.lock_path = self.root / f".{filename}.lock"
        self.root.mkdir(parents=True, exist_ok=True)

    # -- persistence ------------------------------------------------------
    def save(self, checkpoint: DurableCheckpoint) -> ExactRef:
        if not isinstance(checkpoint, DurableCheckpoint):
            raise DurableCheckpointError("exact DurableCheckpoint is required")
        checkpoint.verify_self_consistency()
        payload = _encode(checkpoint.projection())
        written = _atomic_write_bytes(self.path, payload)
        if written != _sha256_bytes(payload):
            raise CheckpointTornError("checkpoint write digest mismatch")
        on_disk = _sha256_bytes(self.path.read_bytes())
        if on_disk != written:
            raise CheckpointTornError("checkpoint bytes changed after durable write")
        return checkpoint.checkpoint_ref

    def load(self, *, identity: CheckpointIdentity | None = None) -> DurableCheckpoint:
        if not self.path.is_file():
            raise CheckpointTornError("no durable checkpoint present")
        raw = self.path.read_bytes()
        try:
            document = json.loads(raw.decode())
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CheckpointTornError(
                f"durable checkpoint is not readable JSON: {exc}"
            ) from exc
        if not isinstance(document, Mapping):
            raise CheckpointTornError("durable checkpoint is not a JSON object")
        if document.get("schema") != CHECKPOINT_SCHEMA_ID:
            raise CheckpointForeignError("durable checkpoint schema mismatch")
        checkpoint = DurableCheckpoint.from_projection(document)
        if identity is not None:
            checkpoint.assert_bound_to(identity)
        return checkpoint

    def exists(self) -> bool:
        return self.path.is_file()

    def raw_bytes(self) -> bytes:
        return self.path.read_bytes()


# --------------------------------------------------------------------------
# Write-ahead session
# --------------------------------------------------------------------------
def empty_checkpoint(identity: CheckpointIdentity) -> DurableCheckpoint:
    return DurableCheckpoint(identity=identity, records=(), sequence=0)


def record_intent(
    checkpoint: DurableCheckpoint,
    *,
    unit_ref: ExactRef,
    attempt_index: int,
) -> DurableCheckpoint:
    """Append a durable START intent.  MUST precede any owner side effect."""
    unit_key = unit_ref.key
    if unit_key not in checkpoint.identity.unit_keys:
        raise CheckpointForeignError("unit is not part of the bound manifest")
    existing = checkpoint.by_unit(unit_key)
    if existing is not None and existing.state == UNIT_STATE_COMMITTED:
        raise DurableCheckpointError(
            "unit is already committed; a completed unit is not re-startable"
        )
    intent_material = {
        "schema": "PYAT_HQ280_B01C_WRITE_AHEAD_INTENT@1.0.0",
        "manifest_hash": checkpoint.identity.manifest_hash,
        "unit_key": unit_key,
        "attempt_index": attempt_index,
    }
    record = UnitRecord(
        unit_key=unit_key,
        unit_ref=unit_ref,
        state=UNIT_STATE_INTENT,
        attempt_index=attempt_index,
        intent_hash=semantic_hash(intent_material),
        receipt_projection=None,
        receipt_hash=None,
        prior_attempt_count=0 if existing is None else existing.prior_attempt_count + 1,
    )
    kept = tuple(r for r in checkpoint.records if r.unit_key != unit_key)
    return DurableCheckpoint(
        identity=checkpoint.identity,
        records=tuple(sorted(kept + (record,), key=lambda r: r.unit_key)),
        sequence=checkpoint.next_sequence(),
    )


def record_commit(
    checkpoint: DurableCheckpoint,
    *,
    unit_ref: ExactRef,
    attempt_index: int,
    receipt: UnitExecutionReceipt,
) -> DurableCheckpoint:
    """Commit the owner's real receipt durably."""
    unit_key = unit_ref.key
    intent = checkpoint.by_unit(unit_key)
    if intent is None or intent.state != UNIT_STATE_INTENT:
        raise DurableCheckpointError(
            "COMMIT requires a prior durable START intent for this unit"
        )
    if intent.attempt_index != attempt_index:
        raise DurableCheckpointError(
            "COMMIT attempt index does not match the durable START intent"
        )
    if receipt.unit_ref.key != unit_key:
        raise CheckpointForeignError("receipt unit identity does not match intent")
    projection = receipt.projection()
    record = UnitRecord(
        unit_key=unit_key,
        unit_ref=unit_ref,
        state=UNIT_STATE_COMMITTED,
        attempt_index=attempt_index,
        intent_hash=intent.intent_hash,
        receipt_projection=projection,
        receipt_hash=_sha256_json(projection),
        prior_attempt_count=intent.prior_attempt_count,
    )
    kept = tuple(r for r in checkpoint.records if r.unit_key != unit_key)
    return DurableCheckpoint(
        identity=checkpoint.identity,
        records=tuple(sorted(kept + (record,), key=lambda r: r.unit_key)),
        sequence=checkpoint.next_sequence(),
    )


# --------------------------------------------------------------------------
# Recovery
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class RecoveryPlan:
    """What recovery may lawfully do, per unit.  HELD is a first-class result."""

    dispositions: Mapping[str, RecoveryDisposition]
    held_units: tuple[str, ...]
    rerunnable_units: tuple[str, ...]
    committed_units: tuple[str, ...]
    receipt_units: tuple[str, ...]
    rehydration_errors: Mapping[str, str] = field(default_factory=dict)
    disregarded_caller_proofs: Mapping[str, str] = field(default_factory=dict)

    @property
    def recovery_safe(self) -> bool:
        return not self.held_units

    def summary(self) -> dict[str, Any]:
        return {
            "recovery_safe": self.recovery_safe,
            "held_units": list(self.held_units),
            "rerunnable_units": list(self.rerunnable_units),
            "committed_units": list(self.committed_units),
            "dispositions": {
                k: v.value for k, v in sorted(self.dispositions.items())
            },
            "rehydration_errors": dict(self.rehydration_errors),
            "disregarded_caller_proofs": dict(self.disregarded_caller_proofs),
            "idempotence_issuer_hold": dict(IDEMPOTENCE_ISSUER_HOLD),
        }


def plan_recovery(
    checkpoint: DurableCheckpoint,
    *,
    idempotence_proof: Mapping[str, str] | None = None,
) -> RecoveryPlan:
    """Classify every manifest unit.  Unknown outcomes are HELD, never rerun.

    A unit whose durable record is a START intent with no matching COMMITTED
    receipt may have had its owner side effect land and then lost the receipt.
    That outcome is UNKNOWN and stays HELD.

    B01D fail-closed repair: the ``idempotence_proof`` argument is retained
    ONLY for backward call-compatibility and is NEVER honored.  The presence
    of any caller-provided mapping, key, string or object — empty or not,
    well-formed or not — cannot promote an unknown outcome.  Presented proofs
    are recorded under ``disregarded_caller_proofs`` as auditable evidence
    that a promotion was attempted and refused.  ``RERUN_SAFE`` is currently
    unreachable; see ``IDEMPOTENCE_ISSUER_HOLD``.
    """
    presented = dict(idempotence_proof or {})
    disregarded: dict[str, str] = {}
    for key, value in presented.items():
        disregarded[str(key)] = (
            f"disregarded: caller-asserted proof is never honored "
            f"(presented value type={type(value).__name__}); "
            f"see IDEMPOTENCE_ISSUER_HOLD"
        )
    dispositions: dict[str, RecoveryDisposition] = {}
    errors: dict[str, str] = {}
    held: list[str] = []
    rerunnable: list[str] = []
    committed: list[str] = []

    for unit_key in checkpoint.identity.unit_keys:
        record = checkpoint.by_unit(unit_key)
        if record is None:
            dispositions[unit_key] = RecoveryDisposition.NEVER_STARTED
            continue
        if record.state == UNIT_STATE_COMMITTED:
            try:
                record.rehydrate_verified()
            except DurableCheckpointError as exc:
                errors[unit_key] = f"{type(exc).__name__}: {exc}"
                dispositions[unit_key] = RecoveryDisposition.UNKNOWN_OUTCOME
                held.append(unit_key)
                continue
            dispositions[unit_key] = RecoveryDisposition.ALREADY_COMMITTED
            committed.append(unit_key)
            continue
        # START intent without a durable COMMIT: side effect may have landed.
        # Fail closed: caller proofs are recorded above and never honored.
        dispositions[unit_key] = RecoveryDisposition.UNKNOWN_OUTCOME
        held.append(unit_key)

    receipts = ()
    try:
        receipts = checkpoint.receipts()
    except DurableCheckpointError as exc:
        errors["__receipts__"] = f"{type(exc).__name__}: {exc}"

    return RecoveryPlan(
        dispositions=dispositions,
        held_units=tuple(sorted(held)),
        rerunnable_units=tuple(sorted(rerunnable)),
        committed_units=tuple(sorted(committed)),
        receipt_units=tuple(r.unit_ref.key for r in receipts),
        rehydration_errors=errors,
        disregarded_caller_proofs=disregarded,
    )


def admit_receipts_for_resume(
    checkpoint: DurableCheckpoint,
) -> tuple[UnitExecutionReceipt, ...]:
    """Prior receipts to hand back to the ACCEPTED, UNMODIFIED batch runner."""
    return checkpoint.receipts()


def checkpoint_effect_flags() -> dict[str, bool]:
    return {
        "relaxed_execution_protocol": False,
        "granted_real_execution_approval": False,
        "semantic_truth_effect": False,
        "learned_product_publication_effect": False,
        "actor_v3_effect": False,
        "invented_scientific_issuer": False,
        "claims_exactly_once_external_execution": False,
        "honors_caller_idempotence_proof": False,
    }


__all__ = [
    "CHECKPOINT_CONTRACT_ID",
    "CHECKPOINT_SCHEMA_ID",
    "CHECKPOINT_STATE_VERSION",
    "UNIT_STATE_INTENT",
    "UNIT_STATE_COMMITTED",
    "DurableCheckpointError",
    "CheckpointLockError",
    "CheckpointTornError",
    "CheckpointForeignError",
    "RecoveryDisposition",
    "IDEMPOTENCE_ISSUER_HOLD",
    "CheckpointIdentity",
    "UnitRecord",
    "DurableCheckpoint",
    "DurableCheckpointStore",
    "RecoveryPlan",
    "ledger_lock",
    "empty_checkpoint",
    "record_intent",
    "record_commit",
    "plan_recovery",
    "admit_receipts_for_resume",
    "checkpoint_effect_flags",
]