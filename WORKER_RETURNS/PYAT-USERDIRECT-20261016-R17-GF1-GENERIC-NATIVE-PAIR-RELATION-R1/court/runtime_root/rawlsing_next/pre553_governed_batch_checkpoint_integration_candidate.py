"""PYAT HQ280 PV3 B01E - governed batch/checkpoint integration CANDIDATE.

Development-only bounded adapter joining three already-accepted pieces that
are each insufficient alone (proven, not assumed):

* the ACCEPTED, UNMODIFIED ``BatchExecutionRunner`` executes real units and
  keeps prior receipts, but persists nothing (zero file-write operations —
  B01 F-01, re-verified);
* the B01D durable-checkpoint candidate journals write-ahead START intents
  and COMMITTED receipts atomically and fail-closes unknown outcomes, but
  never invokes the real C11/Route B/I03/I05 chain (no reference to it at
  all);
* no accepted owner binds manifest -> durable journal -> fresh-process
  resume -> manifest reconciliation in one governed flow.

This adapter supplies exactly that join and nothing else.  Per unit, in
order: durable START intent (fsync) BEFORE the owner call; the REAL owner
call through the caller-supplied executors; a durable side-effect journal
append modelling externalization; durable COMMIT of the owner's REAL receipt.
On recovery (fresh process, durable state only): rehydrate COMMITTED
receipts into a new accepted runner, resume pending non-held units, and
reconcile the manifest by outer join.  START-without-COMMIT units stay HELD
forever — no caller proof can promote them (B01D repair, inherited).

Honesty notes (deliberate, not defects)
---------------------------------------
* The side-effect journal models externalization (publication/delivery of a
  produced result).  Real external effects are publisher-specific; the
  journal proves the *window* and the *no-duplicate* property, not any
  particular publisher's semantics.
* A DEFERRED receipt (durable, owner-issued) is resumable: the owner, not
  the adapter, declared the work incomplete.  An UNKNOWN outcome (START with
  no durable receipt of any kind) is HELD and never auto-run.  The two must
  not be confused.
* Saved vs simulated receipts: only receipts with a durable intent->commit
  chain in THIS checkpoint identity are admitted by the adapter.  A
  well-formed receipt the accepted runner would structurally accept is still
  refused here without that chain.
* Schedule pinning (measured consequence, not a defect of this adapter):
  the accepted runner executes head-anchored with no per-unit selection, so
  a held-but-pending unit pins its entire schedule suffix: the adapter stops
  at the first held unit and reports the suffix explicitly as
  blocked-behind-held.  Selective resume past a held unit would require an
  owner-level per-unit execution entrypoint; that entrypoint does not exist
  and is recorded as future work, NOT simulated around (simulating it would
  mean inventing owner receipts).
* Exactly-once external execution is NOT claimed.  Only the safe HOLD and
  the demonstrated no-duplicate-externalization are proven.

Scope ceiling: source-free development only.  No REAL_EXECUTION approval, no
protocol relaxation, no authority invention, no self-adoption.  A source-free
PASS here is explicitly not protocol approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from rawlsing_next.pre553_batch_durable_checkpoint_candidate import (
    CheckpointIdentity,
    DurableCheckpoint,
    DurableCheckpointError,
    DurableCheckpointStore,
    RecoveryPlan,
    UnitExecutionReceipt,
    admit_receipts_for_resume,
    empty_checkpoint,
    ledger_lock,
    plan_recovery,
    record_commit,
    record_intent,
)
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner,
    BatchIntegrityError,
    BatchManifest,
    ExecutorBinding,
)
from rawlsing_next.pre553_empirical_objects import ExactRef


INTEGRATION_CONTRACT_ID = "PYAT_HQ280_B01E_GOVERNED_BATCH_CHECKPOINT@1.0.0"
INTEGRATION_SCHEMA = "PYAT_HQ280_B01E_GOVERNED_BATCH_CHECKPOINT@1.0.0"
SIDE_EFFECT_JOURNAL_FILENAME = "b01e_side_effects.jsonl"


class IntegrationError(ValueError):
    """The governed integration candidate refuses this request."""


class IntegrationForeignError(IntegrationError):
    """Manifest, release, source or authority identity drifted."""


class IntegrationHeldError(IntegrationError):
    """An execution was requested for a HELD unknown-outcome unit."""


def _sha256_json(value: Any) -> str:
    import hashlib
    import json
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _append_journal_line(path: Path, record: Mapping[str, Any]) -> int:
    """Durably append one side-effect record.  Returns the journal sequence."""
    import contextlib
    import json
    import os
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = 0
    if path.is_file():
        with open(path, "r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    existing += 1
    import tempfile
    fd, name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp = Path(name)
    try:
        previous = path.read_bytes() if path.is_file() else b""
        payload = (
            previous
            + json.dumps({**dict(record), "journal_seq": existing + 1},
                         sort_keys=True).encode() + b"\n"
        )
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        dir_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp.unlink()
    return existing + 1


def _read_journal(path: Path) -> list:
    import json
    if not path.is_file():
        return []
    return [json.loads(line) for line in
            path.read_text(encoding="utf-8").splitlines() if line.strip()]


@dataclass(frozen=True)
class GovernedBatchCheckpointSession:
    """One bound manifest + repository + executors + durable roots."""

    manifest: BatchManifest
    repository: Any
    executors: Mapping[str, ExecutorBinding]
    store: DurableCheckpointStore
    identity: CheckpointIdentity
    source_sha256: str
    side_effect_journal_path: Path

    def checkpoint(self) -> DurableCheckpoint:
        return self.store.load(identity=self.identity)


def open_session(
    *,
    manifest: BatchManifest,
    repository: Any,
    executors: Mapping[str, ExecutorBinding],
    root: str | Path,
    source_sha256: str,
    checkpoint_filename: str = "b01e_checkpoint.json",
    side_effect_journal_filename: str = SIDE_EFFECT_JOURNAL_FILENAME,
) -> GovernedBatchCheckpointSession:
    """Bind and validate every identity up front.  Fail closed, fail fast."""
    if not isinstance(manifest, BatchManifest):
        raise IntegrationError("exact BatchManifest is required")
    if not isinstance(executors, Mapping) or not executors:
        raise IntegrationError("caller-owned real executor bindings are required")
    if not isinstance(source_sha256, str) or not source_sha256:
        raise IntegrationError("declared source_sha256 must be a nonempty string")
    root_path = Path(root)
    store = DurableCheckpointStore(root_path, filename=checkpoint_filename)
    identity = CheckpointIdentity.from_manifest(manifest)

    # Fail fast: every release must resolve, and every resolved release must
    # name the declared source.  The accepted runner re-checks releases at
    # construction; the source check is this adapter's fidelity addition.
    try:
        runner_probe = BatchExecutionRunner(manifest=manifest, repository=repository)
    except BatchIntegrityError as exc:
        raise IntegrationForeignError(
            f"manifest releases do not resolve in the repository: {exc}"
        ) from exc
    for ref in identity.release_refs:
        try:
            release = repository.resolve_release_exact(ref)
        except (KeyError, AttributeError) as exc:
            raise IntegrationForeignError(
                f"exact C11 release unavailable: {exc}"
            ) from exc
        artifact = getattr(release, "source_artifact_ref", None)
        artifact_hash = getattr(artifact, "content_hash", None)
        if artifact_hash != source_sha256:
            raise IntegrationForeignError(
                "release source identity does not match the declared source"
            )
    del runner_probe

    session = GovernedBatchCheckpointSession(
        manifest=manifest,
        repository=repository,
        executors=dict(executors),
        store=store,
        identity=identity,
        source_sha256=source_sha256,
        side_effect_journal_path=root_path / side_effect_journal_filename,
    )
    if store.exists():
        # A pre-existing checkpoint must belong to THIS manifest/release set.
        try:
            store.load(identity=identity)
        except (DurableCheckpointError,) as exc:
            raise IntegrationForeignError(
                f"existing durable checkpoint is foreign or torn: {exc}"
            ) from exc
    return session


@dataclass(frozen=True)
class UnitRunRecord:
    unit_key: str
    attempt_index: int
    receipt_state: str
    checkpoint_sequence: int
    journal_seq: int | None


@dataclass(frozen=True)
class RunReport:
    executed_units: tuple[UnitRunRecord, ...]
    skipped_held_units: tuple[str, ...]
    pinned_deferred_units: tuple[str, ...]
    blocked_behind_held_units: tuple[str, ...]
    batch_state: str
    full_coverage: bool
    checkpoint_ref: ExactRef
    checkpoint_sequence: int

    def summary(self) -> dict[str, Any]:
        return {
            "executed": [(r.unit_key, r.attempt_index, r.receipt_state)
                         for r in self.executed_units],
            "skipped_held": list(self.skipped_held_units),
            "pinned_deferred": list(self.pinned_deferred_units),
            "blocked_behind_held": list(self.blocked_behind_held_units),
            "batch_state": self.batch_state,
            "full_coverage": self.full_coverage,
            "checkpoint_sequence": self.checkpoint_sequence,
        }


def _pinned_deferred_units(
    checkpoint: DurableCheckpoint, pending: Any
) -> set:
    """Units whose journal record is COMMITTED but whose receipt is not
    COMPLETED (DEFERRED or FAILED).

    The B01D journal pins every COMMITTED record: no re-intent is possible,
    so the adapter cannot journal a retry even though the accepted runner
    would permit one.  Retrying a DEFERRED/FAILED unit could duplicate side
    effects the failed or deferred attempt may already have caused, so the
    adapter holds them pinned instead — reported loudly, never silently
    dropped.  (Recovery from configuration errors such as a missing executor
    binding is a fresh checkpoint root, documented in the return.)
    """
    pending_keys = {unit.unit_ref.key for unit in pending}
    pinned = set()
    for record in checkpoint.records:
        if record.state != "COMMITTED":
            continue
        if record.unit_key not in pending_keys:
            continue
        try:
            receipt = record.rehydrate_verified()
        except DurableCheckpointError:
            continue
        if receipt.state != "COMPLETED":
            pinned.add(record.unit_key)
    return pinned


def _current_plan(session: GovernedBatchCheckpointSession) -> tuple[
        DurableCheckpoint, RecoveryPlan]:
    if session.store.exists():
        checkpoint = session.store.load(identity=session.identity)
    else:
        checkpoint = empty_checkpoint(session.identity)
    return checkpoint, plan_recovery(checkpoint)


def _executable_prefix(
    pending_units: Any,
    held: set,
    pinned: set,
) -> tuple[tuple, tuple[str, ...]]:
    """Leading pending units before the first non-progressable one.

    Returns (executable, blocked) where blocked holds the keys strictly
    after the stop point, excluding keys already named in the held/pinned
    buckets.  Together, executed-prefix + stop-unit-in-its-bucket +
    blocked account for every pending unit with no overlap and no silence.
    """
    pending_units = tuple(pending_units)
    executable: list = []
    blocked: list[str] = []
    stopped = False
    for unit in pending_units:
        key = unit.unit_ref.key
        if not stopped and (key in held or key in pinned):
            stopped = True
            continue
        if stopped:
            if key not in held and key not in pinned:
                blocked.append(key)
        else:
            executable.append(unit)
    return tuple(executable), tuple(blocked)


def run_to_completion(
    session: GovernedBatchCheckpointSession,
    *,
    max_units: int | None = None,
) -> RunReport:
    """Execute pending non-held units with durable intent->commit per unit.

    HELD unknown-outcome units are SKIPPED, never auto-run — even with caller
    proofs (the B01D repair is inherited, not re-decided here).  Each unit:
    durable START intent, real owner call via the accepted runner, durable
    side-effect journal append, durable COMMIT of the owner's real receipt.
    """
    if max_units is not None and (
        not isinstance(max_units, int) or isinstance(max_units, bool)
        or max_units < 0
    ):
        raise IntegrationError("max_units must be a nonnegative integer or None")
    checkpoint, plan = _current_plan(session)
    held = set(plan.held_units)
    runner = BatchExecutionRunner(
        manifest=session.manifest,
        repository=session.repository,
        prior_receipts=admit_receipts_for_resume(checkpoint),
    )
    pending_now = tuple(runner.pending_units())
    pinned_at_entry = _pinned_deferred_units(checkpoint, pending_now)
    executable, blocked = _executable_prefix(pending_now, held, pinned_at_entry)
    skipped = sorted(held)
    executed: list[UnitRunRecord] = []
    remaining = max_units
    for unit in executable:
        if remaining is not None:
            if remaining <= 0:
                break
            remaining -= 1
        # Checked invariant: the accepted runner is head-anchored, and the
        # executable prefix contains no held units, so pending[0] must be
        # exactly this unit.  If the owner ever changes scheduling, fail
        # loudly instead of executing the wrong unit.
        head = runner.pending_units()
        if not head or head[0].unit_ref.key != unit.unit_ref.key:
            raise IntegrationError(
                "runner schedule head is not the intended unit; refusing "
                "to execute out of order"
            )
        attempt = runner.next_attempt_index(unit)
        with ledger_lock(session.store.lock_path):
            checkpoint = record_intent(
                checkpoint, unit_ref=unit.unit_ref, attempt_index=attempt
            )
            session.store.save(checkpoint)
        receipts = runner.run(executors=session.executors, max_units=1)
        receipt = next(
            (r for r in receipts if r.unit_ref.key == unit.unit_ref.key), None
        )
        if receipt is None:
            raise IntegrationError("accepted runner produced no receipt for unit")
        journal_seq = _append_journal_line(
            session.side_effect_journal_path,
            {"unit_key": unit.unit_ref.key,
             "attempt_index": attempt,
             "result_refs": [ref.as_dict() for ref in receipt.result_refs],
             "receipt_state": receipt.state,
             "manifest_hash": session.identity.manifest_hash},
        )
        with ledger_lock(session.store.lock_path):
            checkpoint = record_commit(
                checkpoint, unit_ref=unit.unit_ref,
                attempt_index=attempt, receipt=receipt,
            )
            session.store.save(checkpoint)
        executed.append(UnitRunRecord(
            unit_key=unit.unit_ref.key,
            attempt_index=attempt,
            receipt_state=receipt.state,
            checkpoint_sequence=checkpoint.sequence,
            journal_seq=journal_seq,
        ))
    # Recompute pinned at the END: units that deferred or failed during this
    # run now carry COMMITTED records with non-COMPLETED receipts.
    pinned_at_exit = _pinned_deferred_units(
        checkpoint, tuple(runner.pending_units())
    )
    summary = runner.summary()
    return RunReport(
        executed_units=tuple(executed),
        skipped_held_units=tuple(skipped),
        pinned_deferred_units=tuple(sorted(pinned_at_exit)),
        blocked_behind_held_units=tuple(blocked),
        batch_state=summary.batch_state,
        full_coverage=summary.full_coverage,
        checkpoint_ref=checkpoint.checkpoint_ref,
        checkpoint_sequence=checkpoint.sequence,
    )


@dataclass(frozen=True)
class ManifestReconciliation:
    ok: bool
    failures: tuple[Mapping[str, Any], ...]
    expected_unit_keys: tuple[str, ...]
    recorded_unit_keys: tuple[str, ...]
    receipt_unit_keys: tuple[str, ...]
    omitted: tuple[str, ...]
    extra: tuple[str, ...]
    held_uncommitted: tuple[str, ...]

    def failure_codes(self) -> tuple[str, ...]:
        codes: list[str] = []
        for failure in self.failures:
            code = str(failure["code"])
            if code not in codes:
                codes.append(code)
        return tuple(codes)


def _failure(code: str, detail: Any) -> Mapping[str, Any]:
    from types import MappingProxyType
    return MappingProxyType({"code": code, "detail": detail})


def reconcile_manifest(
    *,
    manifest: BatchManifest,
    checkpoint: DurableCheckpoint,
    receipts: Any,
) -> ManifestReconciliation:
    """Outer-join manifest units vs durable records vs terminal receipts."""
    expected = tuple(unit.unit_ref.key for unit in manifest.units)
    recorded = tuple(r.unit_key for r in checkpoint.records)
    received = tuple(r.unit_ref.key for r in receipts)
    failures: list[Mapping[str, Any]] = []
    omitted = tuple(sorted(set(expected) - set(recorded)))
    if omitted:
        failures.append(_failure("EXPECTED_UNIT_WITHOUT_RECORD", list(omitted)))
    extra = tuple(sorted(set(recorded) - set(expected)))
    if extra:
        failures.append(_failure("RECORD_WITHOUT_EXPECTED_UNIT", list(extra)))
    held_uncommitted = tuple(sorted(
        r.unit_key for r in checkpoint.records
        if r.state != "COMMITTED"
    ))
    if held_uncommitted:
        failures.append(_failure("INTENT_WITHOUT_COMMIT_HELD", list(held_uncommitted)))
    committed_keys = {
        r.unit_key for r in checkpoint.records if r.state == "COMMITTED"
    }
    missing_receipts = tuple(sorted(committed_keys - set(received)))
    if missing_receipts:
        failures.append(
            _failure("COMMITTED_RECEIPT_UNREHYDRATABLE", list(missing_receipts))
        )
    return ManifestReconciliation(
        ok=not failures,
        failures=tuple(failures),
        expected_unit_keys=expected,
        recorded_unit_keys=recorded,
        receipt_unit_keys=received,
        omitted=omitted,
        extra=extra,
        held_uncommitted=held_uncommitted,
    )


@dataclass(frozen=True)
class RecoveryReport:
    plan: RecoveryPlan
    pending_unit_keys: tuple[str, ...]
    blocked_behind_held_units: tuple[str, ...]
    reconciliation: ManifestReconciliation
    journal_entries: tuple[Mapping[str, Any], ...]
    checkpoint_sequence: int
    checkpoint_ref: ExactRef

    def summary(self) -> dict[str, Any]:
        return {
            "recovery_safe": self.plan.recovery_safe,
            "held_units": list(self.plan.held_units),
            "rerunnable_units": list(self.plan.rerunnable_units),
            "committed_units": list(self.plan.committed_units),
            "pending_unit_keys": list(self.pending_unit_keys),
            "blocked_behind_held_units": list(self.blocked_behind_held_units),
            "reconciliation_ok": self.reconciliation.ok,
            "reconciliation_failures": [
                dict(failure) for failure in self.reconciliation.failures
            ],
            "journal_entry_count": len(self.journal_entries),
            "checkpoint_sequence": self.checkpoint_sequence,
        }


def recover(session: GovernedBatchCheckpointSession) -> RecoveryReport:
    """Fresh-process recovery from durable state ONLY.  Executes nothing."""
    checkpoint = session.store.load(identity=session.identity)
    plan = plan_recovery(checkpoint)
    receipts = admit_receipts_for_resume(checkpoint)
    runner = BatchExecutionRunner(
        manifest=session.manifest,
        repository=session.repository,
        prior_receipts=receipts,
    )
    pending_units = tuple(runner.pending_units())
    pending = tuple(unit.unit_ref.key for unit in pending_units)
    pinned = _pinned_deferred_units(checkpoint, pending_units)
    _, blocked = _executable_prefix(
        pending_units, set(plan.held_units), pinned
    )
    reconciliation = reconcile_manifest(
        manifest=session.manifest, checkpoint=checkpoint, receipts=receipts
    )
    return RecoveryReport(
        plan=plan,
        pending_unit_keys=pending,
        blocked_behind_held_units=tuple(blocked),
        reconciliation=reconciliation,
        journal_entries=tuple(_read_journal(session.side_effect_journal_path)),
        checkpoint_sequence=checkpoint.sequence,
        checkpoint_ref=checkpoint.checkpoint_ref,
    )


def admit_saved_receipts(session: GovernedBatchCheckpointSession) -> tuple:
    """Rehydrate durable receipts for a fresh accepted runner. Durable only."""
    return admit_receipts_for_resume(session.store.load(identity=session.identity))


def refuse_held_execution(
    session: GovernedBatchCheckpointSession, unit_key: str
) -> None:
    """Explicit guard: raise before any execution of a HELD unit is attempted.

    ``run_to_completion`` skips held units by construction; this guard exists
    so any other driver path fails loudly instead of silently rerunning an
    unknown outcome.
    """
    _, plan = _current_plan(session)
    if unit_key in set(plan.held_units):
        raise IntegrationHeldError(
            f"unit {unit_key} is HELD with unknown outcome; "
            f"no caller proof can authorize its execution"
        )


def integration_effect_flags() -> dict[str, bool]:
    return {
        **{key: False for key in (
            "relaxed_execution_protocol",
            "granted_real_execution_approval",
            "semantic_truth_effect",
            "learned_product_publication_effect",
            "actor_v3_effect",
            "invented_scientific_issuer",
            "claims_exactly_once_external_execution",
        )},
        "honors_caller_idempotence_proof": False,
        "auto_reruns_held_units": False,
    }


__all__ = [
    "INTEGRATION_CONTRACT_ID",
    "INTEGRATION_SCHEMA",
    "SIDE_EFFECT_JOURNAL_FILENAME",
    "IntegrationError",
    "IntegrationForeignError",
    "IntegrationHeldError",
    "GovernedBatchCheckpointSession",
    "open_session",
    "UnitRunRecord",
    "RunReport",
    "run_to_completion",
    "ManifestReconciliation",
    "reconcile_manifest",
    "RecoveryReport",
    "recover",
    "admit_saved_receipts",
    "refuse_held_execution",
    "integration_effect_flags",
]
