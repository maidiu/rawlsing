"""Deterministic non-semantic PRE553 batch orchestration.

Wave-03 R16 schedules already-authorized semantic work. It never creates query
or discovery authority, defines discovery candidates, certifies sources,
admits structural facts, mutates V553+, infers source relations, or upgrades
cache/materialization presence into semantic authority.

Only exact identities enter the manifest. Retry and resume are operational
events over an immutable semantic unit identity.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
import re
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
JOB_KINDS = frozenset({"QUERY", "DISCOVERY"})
UNIT_STATES = frozenset({"COMPLETED", "FAILED", "DEFERRED"})
BATCH_STATES = frozenset({"READY", "IN_PROGRESS", "COMPLETED", "FAILED", "DEFERRED"})
FORBIDDEN_SELECTOR_TOKENS = frozenset({"latest", "default", "fuzzy", "nearest", "*"})


class BatchIntegrityError(ValueError):
    """Operational batch identity/receipt integrity is invalid."""


class BatchExecutionError(RuntimeError):
    """Non-semantic execution orchestration failed."""


class BatchDeferred(RuntimeError):
    """An executor explicitly deferred one exact unit without completing it."""

    def __init__(self, code: str, detail: str = "") -> None:
        code = _text(code, "deferred code")
        detail = str(detail)
        super().__init__(detail or code)
        self.code = code
        self.detail = detail


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BatchIntegrityError(f"{name} must be a non-empty string")
    return value.strip()


def _sha(value: Any, name: str) -> str:
    value = _text(value, name)
    if not SHA256_RE.fullmatch(value):
        raise BatchIntegrityError(f"{name} must be a lowercase sha256")
    return value


def _reject_selector_ref(ref: ExactRef, name: str) -> None:
    raw = ref.object_id.strip().lower()
    if raw in FORBIDDEN_SELECTOR_TOKENS:
        raise BatchIntegrityError(f"{name} may not use latest/default/fuzzy/nearest selection")
    for token in ("latest:", "default:", "fuzzy:", "nearest:"):
        if raw.startswith(token):
            raise BatchIntegrityError(f"{name} may not use mutable/fuzzy selector syntax")


def _exact_ref(value: ExactRef, name: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise BatchIntegrityError(f"{name} must be an exact ExactRef")
    _reject_selector_ref(value, name)
    return value


def _canonical_refs(values: Iterable[ExactRef], name: str) -> tuple[ExactRef, ...]:
    by_key: dict[str, ExactRef] = {}
    for value in values:
        ref = _exact_ref(value, name)
        by_key[ref.key] = ref
    return tuple(by_key[key] for key in sorted(by_key))


def _unit_projection(
    *,
    job_kind: str,
    job_ref: ExactRef,
    release_refs: tuple[ExactRef, ...],
    semantic_input_refs: tuple[ExactRef, ...],
) -> dict[str, Any]:
    return {
        "job_kind": job_kind,
        "job_ref": job_ref.as_dict(),
        "release_refs": [ref.as_dict() for ref in release_refs],
        "semantic_input_refs": [ref.as_dict() for ref in semantic_input_refs],
    }


@dataclass(frozen=True, slots=True)
class BatchUnitSpec:
    """One exact already-authorized semantic job, represented opaquely to R16."""

    job_kind: str
    job_ref: ExactRef
    release_refs: tuple[ExactRef, ...]
    semantic_input_refs: tuple[ExactRef, ...] = ()
    unit_hash: str = field(init=False)
    unit_ref: ExactRef = field(init=False)

    def __post_init__(self) -> None:
        kind = _text(self.job_kind, "job_kind").upper()
        if kind not in JOB_KINDS:
            raise BatchIntegrityError(f"unsupported job_kind {kind!r}")
        job_ref = _exact_ref(self.job_ref, "job_ref")
        releases = _canonical_refs(self.release_refs, "release_refs")
        if not releases:
            raise BatchIntegrityError("each batch unit requires one or more exact C11 release refs")
        for ref in releases:
            if ref.kind != "C11LogicalRelease":
                raise BatchIntegrityError("release_refs must be exact C11LogicalRelease refs")
        inputs = _canonical_refs(self.semantic_input_refs, "semantic_input_refs")
        projection = _unit_projection(
            job_kind=kind,
            job_ref=job_ref,
            release_refs=releases,
            semantic_input_refs=inputs,
        )
        digest = semantic_hash(projection)
        object.__setattr__(self, "job_kind", kind)
        object.__setattr__(self, "job_ref", job_ref)
        object.__setattr__(self, "release_refs", releases)
        object.__setattr__(self, "semantic_input_refs", inputs)
        object.__setattr__(self, "unit_hash", digest)
        object.__setattr__(
            self,
            "unit_ref",
            ExactRef(
                "PRE553BatchUnit@1.0.0",
                f"urn:rawlsing:pre553:batch-unit:sha256:{digest}",
                digest,
            ),
        )

    def semantic_projection(self) -> dict[str, Any]:
        return _unit_projection(
            job_kind=self.job_kind,
            job_ref=self.job_ref,
            release_refs=self.release_refs,
            semantic_input_refs=self.semantic_input_refs,
        )


@dataclass(frozen=True, slots=True)
class BatchManifest:
    """Immutable, storage-order-independent manifest of exact work units."""

    units: tuple[BatchUnitSpec, ...]
    manifest_version: str = "1.0.0"
    manifest_hash: str = field(init=False)
    manifest_ref: ExactRef = field(init=False)

    def __post_init__(self) -> None:
        version = _text(self.manifest_version, "manifest_version")
        if isinstance(self.units, (str, bytes, bytearray)):
            raise BatchIntegrityError("units must be BatchUnitSpec values")
        by_hash: dict[str, BatchUnitSpec] = {}
        for unit in self.units:
            if not isinstance(unit, BatchUnitSpec):
                raise BatchIntegrityError("manifest units must be BatchUnitSpec")
            prior = by_hash.get(unit.unit_hash)
            if prior is not None and prior.semantic_projection() != unit.semantic_projection():
                raise BatchIntegrityError("unit hash collision with conflicting semantic projection")
            by_hash[unit.unit_hash] = unit
        if not by_hash:
            raise BatchIntegrityError("batch manifest must contain at least one unit")
        canonical_units = tuple(by_hash[key] for key in sorted(by_hash))
        projection = {
            "manifest_version": version,
            "units": [
                {
                    "unit_ref": unit.unit_ref.as_dict(),
                    "semantic_projection": unit.semantic_projection(),
                }
                for unit in canonical_units
            ],
        }
        digest = semantic_hash(projection)
        object.__setattr__(self, "manifest_version", version)
        object.__setattr__(self, "units", canonical_units)
        object.__setattr__(self, "manifest_hash", digest)
        object.__setattr__(
            self,
            "manifest_ref",
            ExactRef(
                "PRE553BatchManifest@1.0.0",
                f"urn:rawlsing:pre553:batch-manifest:sha256:{digest}",
                digest,
            ),
        )

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "manifest_version": self.manifest_version,
            "units": [
                {
                    "unit_ref": unit.unit_ref.as_dict(),
                    "semantic_projection": unit.semantic_projection(),
                }
                for unit in self.units
            ],
        }


@dataclass(frozen=True, slots=True)
class ExecutionOutcome:
    """Completed executor output. Typed semantic negatives remain normal result refs."""

    result_refs: tuple[ExactRef, ...] = ()
    provenance_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "result_refs", _canonical_refs(self.result_refs, "result_refs"))
        object.__setattr__(
            self, "provenance_refs", _canonical_refs(self.provenance_refs, "provenance_refs")
        )


@dataclass(frozen=True, slots=True)
class ExecutorBinding:
    """Operational binding of one job kind to an exact executor identity."""

    executor_ref: ExactRef
    execute: Callable[[BatchUnitSpec], ExecutionOutcome] = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "executor_ref", _exact_ref(self.executor_ref, "executor_ref"))
        if not callable(self.execute):
            raise BatchIntegrityError("ExecutorBinding.execute must be callable")


@dataclass(frozen=True, slots=True)
class UnitExecutionReceipt:
    """Immutable operational receipt for one exact attempt."""

    manifest_hash: str
    unit_ref: ExactRef
    attempt_index: int
    state: str
    execution_performed: bool
    executor_ref: ExactRef | None = None
    result_refs: tuple[ExactRef, ...] = ()
    provenance_refs: tuple[ExactRef, ...] = ()
    failure_code: str | None = None
    detail_hash: str | None = None
    receipt_hash: str = field(init=False)
    receipt_ref: ExactRef = field(init=False)

    def __post_init__(self) -> None:
        manifest_hash = _sha(self.manifest_hash, "manifest_hash")
        unit_ref = _exact_ref(self.unit_ref, "unit_ref")
        if unit_ref.kind != "PRE553BatchUnit@1.0.0":
            raise BatchIntegrityError("receipt unit_ref must be PRE553BatchUnit@1.0.0")
        if (
            not isinstance(self.attempt_index, int)
            or isinstance(self.attempt_index, bool)
            or self.attempt_index < 1
        ):
            raise BatchIntegrityError("attempt_index must be a positive integer")
        state = _text(self.state, "state").upper()
        if state not in UNIT_STATES:
            raise BatchIntegrityError(f"unknown unit execution state {state!r}")
        executor_ref = (
            None if self.executor_ref is None else _exact_ref(self.executor_ref, "executor_ref")
        )
        results = _canonical_refs(self.result_refs, "result_refs")
        provenance = _canonical_refs(self.provenance_refs, "provenance_refs")
        failure_code = None if self.failure_code is None else _text(self.failure_code, "failure_code")
        detail_hash = None if self.detail_hash is None else _sha(self.detail_hash, "detail_hash")

        if state == "COMPLETED":
            if not self.execution_performed:
                raise BatchIntegrityError("COMPLETED requires actual execution evidence")
            if executor_ref is None:
                raise BatchIntegrityError("COMPLETED requires exact executor_ref")
            if not provenance:
                raise BatchIntegrityError("COMPLETED requires exact provenance closure")
            if failure_code is not None or detail_hash is not None:
                raise BatchIntegrityError("COMPLETED may not carry failure fields")
        elif state == "FAILED":
            if not self.execution_performed:
                raise BatchIntegrityError("FAILED requires an attempted executor invocation")
            if executor_ref is None or failure_code is None or detail_hash is None:
                raise BatchIntegrityError("FAILED requires executor_ref/failure_code/detail_hash")
            if results:
                raise BatchIntegrityError("FAILED may not publish result_refs")
        else:
            if failure_code is None or detail_hash is None:
                raise BatchIntegrityError("DEFERRED requires explicit reason code/detail hash")
            if self.execution_performed and executor_ref is None:
                raise BatchIntegrityError("executed DEFERRED receipt requires exact executor_ref")
            if results:
                raise BatchIntegrityError("DEFERRED may not publish result_refs")

        projection = {
            "manifest_hash": manifest_hash,
            "unit_ref": unit_ref.as_dict(),
            "attempt_index": self.attempt_index,
            "state": state,
            "execution_performed": bool(self.execution_performed),
            "executor_ref": None if executor_ref is None else executor_ref.as_dict(),
            "result_refs": [ref.as_dict() for ref in results],
            "provenance_refs": [ref.as_dict() for ref in provenance],
            "failure_code": failure_code,
            "detail_hash": detail_hash,
        }
        digest = semantic_hash(projection)
        object.__setattr__(self, "manifest_hash", manifest_hash)
        object.__setattr__(self, "unit_ref", unit_ref)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "executor_ref", executor_ref)
        object.__setattr__(self, "result_refs", results)
        object.__setattr__(self, "provenance_refs", provenance)
        object.__setattr__(self, "failure_code", failure_code)
        object.__setattr__(self, "detail_hash", detail_hash)
        object.__setattr__(self, "receipt_hash", digest)
        object.__setattr__(
            self,
            "receipt_ref",
            ExactRef(
                "PRE553BatchExecutionReceipt@1.0.0",
                f"urn:rawlsing:pre553:batch-receipt:sha256:{digest}",
                digest,
            ),
        )

    def projection(self) -> dict[str, Any]:
        return {
            "manifest_hash": self.manifest_hash,
            "unit_ref": self.unit_ref.as_dict(),
            "attempt_index": self.attempt_index,
            "state": self.state,
            "execution_performed": self.execution_performed,
            "executor_ref": None if self.executor_ref is None else self.executor_ref.as_dict(),
            "result_refs": [ref.as_dict() for ref in self.result_refs],
            "provenance_refs": [ref.as_dict() for ref in self.provenance_refs],
            "failure_code": self.failure_code,
            "detail_hash": self.detail_hash,
        }


@dataclass(frozen=True, slots=True)
class BatchSummary:
    manifest_ref: ExactRef
    batch_state: str
    coverage_state: str
    full_coverage: bool
    total_units: int
    completed_units: int
    failed_units: int
    deferred_units: int
    pending_units: int
    actual_execution_receipts: int
    receipt_set_hash: str
    populated_data_execution_claim: bool = False

    def __post_init__(self) -> None:
        if self.batch_state not in BATCH_STATES:
            raise BatchIntegrityError("invalid batch_state")
        if self.coverage_state not in {
            "FULL_MANIFEST_COVERAGE",
            "INCOMPLETE_MANIFEST_COVERAGE",
        }:
            raise BatchIntegrityError("invalid coverage_state")
        if self.populated_data_execution_claim:
            raise BatchIntegrityError(
                "R16 cannot claim populated-data execution; receipts are exact execution evidence only"
            )


def _detail_hash(detail: Any) -> str:
    return semantic_hash({"detail": str(detail)})


class BatchExecutionRunner:
    """Deterministic sequential scheduler over an immutable batch manifest.

    The runner never accepts source/query/discovery selectors or cache hits as
    authority. Only exact C11 release resolution and immutable execution
    receipts can remove a unit from the pending set.
    """

    def __init__(
        self,
        *,
        manifest: BatchManifest,
        repository: C11Repository,
        prior_receipts: Iterable[UnitExecutionReceipt] = (),
    ) -> None:
        if not isinstance(manifest, BatchManifest):
            raise BatchIntegrityError("manifest must be immutable BatchManifest")
        if not isinstance(repository, C11Repository):
            raise BatchIntegrityError("repository must be accepted I02 C11Repository")
        self.manifest = manifest
        self.repository = repository
        self._units_by_key = MappingProxyType({unit.unit_ref.key: unit for unit in manifest.units})
        self._receipts: dict[str, dict[int, UnitExecutionReceipt]] = {
            unit.unit_ref.key: {} for unit in manifest.units
        }

        for unit in manifest.units:
            for release_ref in unit.release_refs:
                try:
                    repository.resolve_release_exact(release_ref)
                except KeyError as exc:
                    raise BatchIntegrityError(
                        "exact C11 release unavailable; no latest/default/fuzzy/nearest fallback"
                    ) from exc

        for receipt in prior_receipts:
            self.record_receipt(receipt)

    @property
    def schedule(self) -> tuple[BatchUnitSpec, ...]:
        """Immutable deterministic scheduling order."""
        return self.manifest.units

    @property
    def receipts(self) -> tuple[UnitExecutionReceipt, ...]:
        items = [
            receipt
            for unit_attempts in self._receipts.values()
            for receipt in unit_attempts.values()
        ]
        return tuple(
            sorted(items, key=lambda receipt: (receipt.unit_ref.key, receipt.attempt_index, receipt.receipt_hash))
        )

    def _history(self, unit: BatchUnitSpec) -> tuple[UnitExecutionReceipt, ...]:
        return tuple(
            self._receipts[unit.unit_ref.key][index]
            for index in sorted(self._receipts[unit.unit_ref.key])
        )

    def _latest(self, unit: BatchUnitSpec) -> UnitExecutionReceipt | None:
        history = self._history(unit)
        return history[-1] if history else None

    def next_attempt_index(self, unit: BatchUnitSpec) -> int:
        if unit.unit_ref.key not in self._units_by_key:
            raise BatchIntegrityError("unit does not belong to this manifest")
        history = self._history(unit)
        if history and history[-1].state == "COMPLETED":
            raise BatchIntegrityError("completed unit is not retryable")
        return len(history) + 1

    def pending_units(self) -> tuple[BatchUnitSpec, ...]:
        """Units lacking a completed receipt, in deterministic scheduling order."""
        return tuple(
            unit
            for unit in self.schedule
            if self._latest(unit) is None or self._latest(unit).state != "COMPLETED"
        )

    def record_receipt(self, receipt: UnitExecutionReceipt) -> None:
        if not isinstance(receipt, UnitExecutionReceipt):
            raise BatchIntegrityError("prior receipt must be UnitExecutionReceipt")
        if receipt.manifest_hash != self.manifest.manifest_hash:
            raise BatchIntegrityError("receipt manifest hash mismatch")
        unit = self._units_by_key.get(receipt.unit_ref.key)
        if unit is None or receipt.unit_ref != unit.unit_ref:
            raise BatchIntegrityError("receipt unit identity is not in manifest")

        history_map = self._receipts[unit.unit_ref.key]
        expected_attempt = len(history_map) + 1
        if receipt.attempt_index != expected_attempt:
            raise BatchIntegrityError("receipt attempts must be contiguous and deterministic")
        prior = self._history(unit)
        if prior and prior[-1].state == "COMPLETED":
            raise BatchIntegrityError("receipt cannot retry an already completed unit")

        required_provenance = {
            ref.key
            for ref in (unit.job_ref, *unit.release_refs, *unit.semantic_input_refs)
        }
        if receipt.state == "COMPLETED":
            actual = {ref.key for ref in receipt.provenance_refs}
            missing = sorted(required_provenance - actual)
            if missing:
                raise BatchIntegrityError(
                    "completed receipt lacks exact job/release/input provenance closure"
                )

        history_map[receipt.attempt_index] = receipt

    def _make_receipt(
        self,
        *,
        unit: BatchUnitSpec,
        attempt_index: int,
        state: str,
        execution_performed: bool,
        executor_ref: ExactRef | None,
        result_refs: Iterable[ExactRef] = (),
        extra_provenance_refs: Iterable[ExactRef] = (),
        failure_code: str | None = None,
        detail: str = "",
    ) -> UnitExecutionReceipt:
        provenance = _canonical_refs(
            (
                unit.job_ref,
                *unit.release_refs,
                *unit.semantic_input_refs,
                *tuple(extra_provenance_refs),
                *((executor_ref,) if executor_ref is not None else ()),
            ),
            "provenance_refs",
        )
        return UnitExecutionReceipt(
            manifest_hash=self.manifest.manifest_hash,
            unit_ref=unit.unit_ref,
            attempt_index=attempt_index,
            state=state,
            execution_performed=execution_performed,
            executor_ref=executor_ref,
            result_refs=tuple(result_refs),
            provenance_refs=provenance,
            failure_code=failure_code,
            detail_hash=(
                None
                if state == "COMPLETED"
                else _detail_hash(detail or failure_code or state)
            ),
        )

    def run(
        self,
        *,
        executors: Mapping[str, ExecutorBinding],
        max_units: int | None = None,
    ) -> tuple[UnitExecutionReceipt, ...]:
        """Run pending exact units in deterministic order.

        `max_units` is an operational throttle only. Stopping early leaves
        explicit pending coverage and can never become FULL_MANIFEST_COVERAGE.
        """
        if not isinstance(executors, Mapping):
            raise BatchIntegrityError("executors must be a mapping by exact job kind")
        bindings: dict[str, ExecutorBinding] = {}
        for raw_kind, binding in executors.items():
            kind = _text(raw_kind, "executor job kind").upper()
            if kind not in JOB_KINDS or not isinstance(binding, ExecutorBinding):
                raise BatchIntegrityError(
                    "executors must map QUERY/DISCOVERY to ExecutorBinding"
                )
            bindings[kind] = binding
        if max_units is not None:
            if (
                not isinstance(max_units, int)
                or isinstance(max_units, bool)
                or max_units < 0
            ):
                raise BatchIntegrityError("max_units must be a nonnegative integer or None")

        created: list[UnitExecutionReceipt] = []
        candidates = self.pending_units()
        if max_units is not None:
            candidates = candidates[:max_units]

        for unit in candidates:
            attempt = self.next_attempt_index(unit)
            binding = bindings.get(unit.job_kind)
            if binding is None:
                receipt = self._make_receipt(
                    unit=unit,
                    attempt_index=attempt,
                    state="DEFERRED",
                    execution_performed=False,
                    executor_ref=None,
                    failure_code="EXECUTOR_UNAVAILABLE",
                    detail=f"no executor binding for {unit.job_kind}",
                )
                self.record_receipt(receipt)
                created.append(receipt)
                continue

            try:
                outcome = binding.execute(unit)
                if not isinstance(outcome, ExecutionOutcome):
                    raise BatchExecutionError("executor must return ExecutionOutcome")
                receipt = self._make_receipt(
                    unit=unit,
                    attempt_index=attempt,
                    state="COMPLETED",
                    execution_performed=True,
                    executor_ref=binding.executor_ref,
                    result_refs=outcome.result_refs,
                    extra_provenance_refs=outcome.provenance_refs,
                )
            except BatchDeferred as exc:
                receipt = self._make_receipt(
                    unit=unit,
                    attempt_index=attempt,
                    state="DEFERRED",
                    execution_performed=True,
                    executor_ref=binding.executor_ref,
                    failure_code=exc.code,
                    detail=exc.detail or str(exc),
                )
            except Exception as exc:
                receipt = self._make_receipt(
                    unit=unit,
                    attempt_index=attempt,
                    state="FAILED",
                    execution_performed=True,
                    executor_ref=binding.executor_ref,
                    failure_code=f"EXECUTOR_EXCEPTION:{type(exc).__name__}",
                    detail=str(exc),
                )
            self.record_receipt(receipt)
            created.append(receipt)

        return tuple(created)

    def summary(self) -> BatchSummary:
        latest = {unit.unit_ref.key: self._latest(unit) for unit in self.schedule}
        completed = sum(
            1 for receipt in latest.values() if receipt and receipt.state == "COMPLETED"
        )
        failed = sum(
            1 for receipt in latest.values() if receipt and receipt.state == "FAILED"
        )
        deferred = sum(
            1 for receipt in latest.values() if receipt and receipt.state == "DEFERRED"
        )
        pending = sum(1 for receipt in latest.values() if receipt is None)
        total = len(self.schedule)
        full = completed == total

        if full:
            batch_state = "COMPLETED"
        elif failed:
            batch_state = "FAILED"
        elif deferred:
            batch_state = "DEFERRED"
        elif completed:
            batch_state = "IN_PROGRESS"
        else:
            batch_state = "READY"

        receipt_set_hash = semantic_hash(
            {"receipts": [receipt.projection() for receipt in self.receipts]}
        )
        return BatchSummary(
            manifest_ref=self.manifest.manifest_ref,
            batch_state=batch_state,
            coverage_state=(
                "FULL_MANIFEST_COVERAGE"
                if full
                else "INCOMPLETE_MANIFEST_COVERAGE"
            ),
            full_coverage=full,
            total_units=total,
            completed_units=completed,
            failed_units=failed,
            deferred_units=deferred,
            pending_units=pending,
            actual_execution_receipts=sum(
                1 for receipt in self.receipts if receipt.execution_performed
            ),
            receipt_set_hash=receipt_set_hash,
            populated_data_execution_claim=False,
        )


__all__ = [
    "JOB_KINDS",
    "UNIT_STATES",
    "BATCH_STATES",
    "BatchIntegrityError",
    "BatchExecutionError",
    "BatchDeferred",
    "BatchUnitSpec",
    "BatchManifest",
    "ExecutionOutcome",
    "ExecutorBinding",
    "UnitExecutionReceipt",
    "BatchSummary",
    "BatchExecutionRunner",
]
