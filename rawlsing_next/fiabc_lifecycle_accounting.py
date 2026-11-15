"""FIABC lifecycle and preserved-work accounting.

This module implements the lifecycle/accounting slice of Wave-3 IMP11.  It does
not own process isolation (I06A) or resource instrumentation (I06B).  Instead it
consumes explicit receipts from those concerns and refuses to admit lifecycle
metrics unless a governed candidate action actually occurred.

The controlling Wave-2 law is FIABC-W2-B03:
  * semantic owner != cost owner;
  * candidate-neutral upstream capital is not reproduced for symmetry;
  * candidate-local lifecycle work must be actually executed;
  * preserved numeric credit is conditional, field-by-field;
  * missing or unreached telemetry is null, never numeric zero.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence


class AccountingContractError(RuntimeError):
    """Raised when a receipt would manufacture or misattribute lifecycle work."""


class LifecycleAction(str, Enum):
    COLD_FIRST_REALIZATION = "COLD_FIRST_REALIZATION"
    WARM_RETAINED_STATE_USE = "WARM_RETAINED_STATE_USE"
    DELETION_REGENERATION = "DELETION_REGENERATION"
    SOURCE_INVALIDATION = "SOURCE_INVALIDATION"
    AUTHORITY_SEMANTIC_INVALIDATION = "AUTHORITY_SEMANTIC_INVALIDATION"
    STALE_STATE_RECOVERY = "STALE_STATE_RECOVERY"
    CORRUPT_STATE_RECOVERY = "CORRUPT_STATE_RECOVERY"
    INTERRUPTION_RECOVERY = "INTERRUPTION_RECOVERY"
    FRESH_PROCESS_REPLAY = "FRESH_PROCESS_REPLAY"
    AUDIT_REVALIDATION = "AUDIT_REVALIDATION"


class AccountingDisposition(str, Enum):
    EXECUTED_NOW = "EXECUTED_NOW"
    LAWFULLY_PRESERVED_MEASURED_WORK = "LAWFULLY_PRESERVED_MEASURED_WORK"
    PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY = (
        "PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY"
    )
    NOT_REACHED = "NOT_REACHED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class MetricState(str, Enum):
    MEASURED = "MEASURED"
    MEASUREMENT_NOT_CAPTURED = "MEASUREMENT_NOT_CAPTURED"
    NOT_REACHED_AUTHORIZED_STOP = "NOT_REACHED_AUTHORIZED_STOP"
    NOT_APPLICABLE_BY_FROZEN_COURT = "NOT_APPLICABLE_BY_FROZEN_COURT"
    INVALID_MEASUREMENT_ACCOUNTING_CONTRACT_BREACH = (
        "INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH"
    )


class EvidenceKind(str, Enum):
    EXECUTED_CANDIDATE_ACTION = "EXECUTED_CANDIDATE_ACTION"
    FORMULA_DERIVED = "FORMULA_DERIVED"
    LAW_HASH_ONLY = "LAW_HASH_ONLY"
    GENERIC_TEMP_FILE = "GENERIC_TEMP_FILE"
    DECLARATIVE_ONLY = "DECLARATIVE_ONLY"


LIFECYCLE_METRIC_ACTIONS: Mapping[str, LifecycleAction] = {
    "build_or_open_wall_ns": LifecycleAction.COLD_FIRST_REALIZATION,
    "cold_i03_latency_ns": LifecycleAction.COLD_FIRST_REALIZATION,
    "warm_i03_latency_ns": LifecycleAction.WARM_RETAINED_STATE_USE,
    "warm_retained_state_bytes": LifecycleAction.WARM_RETAINED_STATE_USE,
    "delete_rebuild_wall_ns": LifecycleAction.DELETION_REGENERATION,
    "source_release_invalidation_recomputation_units": LifecycleAction.SOURCE_INVALIDATION,
    "semantic_authority_invalidation_recomputation_units": LifecycleAction.AUTHORITY_SEMANTIC_INVALIDATION,
    "stale_state_recovery_wall_ns": LifecycleAction.STALE_STATE_RECOVERY,
    "corrupt_state_recovery_wall_ns": LifecycleAction.CORRUPT_STATE_RECOVERY,
    "interruption_recovery_wall_ns": LifecycleAction.INTERRUPTION_RECOVERY,
    "fresh_process_replay_wall_ns": LifecycleAction.FRESH_PROCESS_REPLAY,
    "audit_wall_ns": LifecycleAction.AUDIT_REVALIDATION,
}


class PreservedPolicy(str, Enum):
    COMMON_UPSTREAM = "COMMON_UPSTREAM"
    CONDITIONAL_FIELDWISE_NUMERIC = "CONDITIONAL_FIELDWISE_NUMERIC"
    SEMANTIC_ONLY_NO_NUMERIC = "SEMANTIC_ONLY_NO_NUMERIC"
    CALIBRATION_ONLY = "CALIBRATION_ONLY"
    AUTHORIZED_STOP = "AUTHORIZED_STOP"


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _nonnull(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value:
        raise AccountingContractError(f"{field_name} must be a non-empty string")
    return value


@dataclass(frozen=True)
class ProcessIsolationReceipt:
    """Normalized I06A-facing isolation receipt.

    I06C does not create or police OS processes.  It requires I06A (or a
    mechanically compatible adapter) to prove the source x candidate process
    boundary and candidate-state isolation.
    """

    source_id: str
    candidate_id: str
    process_token: str
    candidate_root_identity: str
    fresh_process_for_cell: bool
    cross_candidate_state_reachable: bool = False
    isolation_contract_identity: str = ""

    def validate(self, source_id: str, candidate_id: str) -> None:
        if self.source_id != source_id or self.candidate_id != candidate_id:
            raise AccountingContractError(
                "I06A isolation receipt source/candidate does not match lifecycle binding"
            )
        _nonnull(self.process_token, "process_token")
        _nonnull(self.candidate_root_identity, "candidate_root_identity")
        if not self.fresh_process_for_cell:
            raise AccountingContractError("fresh source x candidate process not proved")
        if self.cross_candidate_state_reachable:
            raise AccountingContractError("cross-candidate state is reachable")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ProcessIsolationReceipt":
        """Integration adapter for the eventual I06A mapping shape."""
        return cls(
            source_id=str(value["source_id"]),
            candidate_id=str(value["candidate_id"]),
            process_token=str(value["process_token"]),
            candidate_root_identity=str(value["candidate_root_identity"]),
            fresh_process_for_cell=bool(value["fresh_process_for_cell"]),
            cross_candidate_state_reachable=bool(
                value.get("cross_candidate_state_reachable", False)
            ),
            isolation_contract_identity=str(
                value.get("isolation_contract_identity", "")
            ),
        )


@dataclass(frozen=True)
class LifecycleBinding:
    source_id: str
    source_sha256: str
    candidate_id: str
    candidate_owner_identity: str
    workload_id: str
    authority_set_identity: str
    runtime_binding_identity: str
    state_scope_identity: str
    expected_terminal_identity: str
    isolation: ProcessIsolationReceipt

    def validate(self) -> None:
        for name in (
            "source_id",
            "source_sha256",
            "candidate_id",
            "candidate_owner_identity",
            "workload_id",
            "authority_set_identity",
            "runtime_binding_identity",
            "state_scope_identity",
            "expected_terminal_identity",
        ):
            _nonnull(getattr(self, name), name)
        self.isolation.validate(self.source_id, self.candidate_id)

    @property
    def binding_id(self) -> str:
        self.validate()
        return _hash(
            {
                "source_id": self.source_id,
                "source_sha256": self.source_sha256,
                "candidate_id": self.candidate_id,
                "candidate_owner_identity": self.candidate_owner_identity,
                "workload_id": self.workload_id,
                "authority_set_identity": self.authority_set_identity,
                "runtime_binding_identity": self.runtime_binding_identity,
                "state_scope_identity": self.state_scope_identity,
                "expected_terminal_identity": self.expected_terminal_identity,
                "process_token": self.isolation.process_token,
                "candidate_root_identity": self.isolation.candidate_root_identity,
            }
        )


@dataclass(frozen=True)
class LifecycleActionRequest:
    binding: LifecycleBinding
    action: LifecycleAction
    governed_operation_id: str
    expected_metric_names: tuple[str, ...] = ()
    not_applicable_reason: str | None = None

    def validate(self) -> None:
        self.binding.validate()
        _nonnull(self.governed_operation_id, "governed_operation_id")
        if len(set(self.expected_metric_names)) != len(self.expected_metric_names):
            raise AccountingContractError("expected_metric_names contains duplicates")
        for metric_name in self.expected_metric_names:
            required_action = LIFECYCLE_METRIC_ACTIONS.get(metric_name)
            if required_action is not None and required_action is not self.action:
                raise AccountingContractError(
                    f"lifecycle metric {metric_name} belongs to {required_action.value}, not {self.action.value}"
                )


@dataclass(frozen=True)
class ActionObservation:
    """Evidence returned by the candidate-specific lifecycle implementation."""

    action: LifecycleAction
    binding_id: str
    source_id: str
    candidate_id: str
    performed: bool
    evidence_kind: EvidenceKind
    action_id: str
    state_before_id: str
    state_after_id: str
    terminal_identity: str

    candidate_state_object_ids_before: tuple[str, ...] = ()
    candidate_state_object_ids_after: tuple[str, ...] = ()
    deleted_object_ids: tuple[str, ...] = ()
    regenerated_object_ids: tuple[str, ...] = ()
    regeneration_lineage: tuple[tuple[str, str], ...] = ()

    retained_state_id: str | None = None
    retained_state_candidate_id: str | None = None
    cold_state_proven_absent: bool = False

    invalidation_trigger_identity: str | None = None
    invalidated_unit_ids: tuple[str, ...] = ()
    recomputed_unit_ids: tuple[str, ...] = ()

    stale_determinant_before: str | None = None
    stale_determinant_after: str | None = None
    stale_detected: bool = False

    corrupt_target_id: str | None = None
    corruption_injected: bool = False
    corrupt_detected: bool = False

    interrupted_operation_id: str | None = None
    interrupted_candidate_state_id: str | None = None
    interruption_injected: bool = False
    recovered_operation_id: str | None = None

    parent_process_token: str | None = None
    replay_process_token: str | None = None

    audit_primitive_identity: str | None = None
    recovery_performed: bool = False
    evidence_refs: tuple[str, ...] = ()

    @property
    def observed_recomputation_units(self) -> int:
        return len(self.recomputed_unit_ids)


@dataclass(frozen=True)
class TelemetryMetric:
    """Normalized I06B-facing metric.

    I06B may expose a different concrete recorder.  The CallableTelemetryAdapter
    below is the fan-in seam.  I06C requires every numeric lifecycle metric to
    bind both action_id and binding_id.
    """

    name: str
    state: MetricState
    value: int | float | None
    unit: str
    action_id: str
    binding_id: str

    def validate_measured(self) -> None:
        _nonnull(self.name, "metric name")
        _nonnull(self.unit, "metric unit")
        if self.state is not MetricState.MEASURED:
            raise AccountingContractError(
                f"executed-now telemetry {self.name} is not MEASURED"
            )
        if not isinstance(self.value, (int, float)) or isinstance(self.value, bool):
            raise AccountingContractError(
                f"executed-now telemetry {self.name} lacks numeric value"
            )
        if self.value < 0:
            raise AccountingContractError(
                f"executed-now telemetry {self.name} is negative"
            )
        _nonnull(self.action_id, "metric action_id")
        _nonnull(self.binding_id, "metric binding_id")


@dataclass(frozen=True)
class MetricAccounting:
    name: str
    state: MetricState
    value: int | float | None
    unit: str
    source_field: str | None = None
    reason: str | None = None


@dataclass(frozen=True)
class LifecycleAccountingReceipt:
    schema: str
    disposition: AccountingDisposition
    binding_id: str
    source_id: str
    source_sha256: str
    candidate_id: str
    candidate_owner_identity: str
    state_scope_identity: str
    action: LifecycleAction
    action_id: str | None
    governed_operation_id: str
    state_before_id: str | None
    state_after_id: str | None
    terminal_identity: str | None
    metrics: tuple[MetricAccounting, ...]
    evidence_refs: tuple[str, ...]
    reason: str | None = None
    preserved_work_id: str | None = None
    preserved_receipt_ref: str | None = None

    @property
    def receipt_id(self) -> str:
        return _hash(
            {
                "schema": self.schema,
                "disposition": self.disposition.value,
                "binding_id": self.binding_id,
                "source_id": self.source_id,
                "source_sha256": self.source_sha256,
                "candidate_id": self.candidate_id,
                "candidate_owner_identity": self.candidate_owner_identity,
                "state_scope_identity": self.state_scope_identity,
                "action": self.action.value,
                "action_id": self.action_id,
                "governed_operation_id": self.governed_operation_id,
                "state_before_id": self.state_before_id,
                "state_after_id": self.state_after_id,
                "terminal_identity": self.terminal_identity,
                "metrics": [
                    {
                        "name": m.name,
                        "state": m.state.value,
                        "value": m.value,
                        "unit": m.unit,
                        "source_field": m.source_field,
                        "reason": m.reason,
                    }
                    for m in self.metrics
                ],
                "evidence_refs": list(self.evidence_refs),
                "reason": self.reason,
                "preserved_work_id": self.preserved_work_id,
                "preserved_receipt_ref": self.preserved_receipt_ref,
            }
        )


class LifecycleActionPort(Protocol):
    def perform_lifecycle_action(
        self, request: LifecycleActionRequest
    ) -> ActionObservation:
        ...


class TelemetryPort(Protocol):
    def record_completed_lifecycle_action(
        self, request: LifecycleActionRequest, observation: ActionObservation
    ) -> Sequence[TelemetryMetric]:
        ...


class CallableLifecycleActionAdapter:
    """Mechanical fan-in adapter for a sibling/backend callable."""

    def __init__(
        self, callback: Callable[[LifecycleActionRequest], ActionObservation]
    ) -> None:
        self._callback = callback

    def perform_lifecycle_action(
        self, request: LifecycleActionRequest
    ) -> ActionObservation:
        return self._callback(request)


class CallableTelemetryAdapter:
    """Mechanical fan-in adapter for I06B without owning its recorder."""

    def __init__(
        self,
        callback: Callable[
            [LifecycleActionRequest, ActionObservation], Sequence[TelemetryMetric]
        ],
    ) -> None:
        self._callback = callback

    def record_completed_lifecycle_action(
        self, request: LifecycleActionRequest, observation: ActionObservation
    ) -> Sequence[TelemetryMetric]:
        return self._callback(request, observation)


def _require_terminal_identity(
    request: LifecycleActionRequest, observation: ActionObservation
) -> None:
    if observation.terminal_identity != request.binding.expected_terminal_identity:
        raise AccountingContractError(
            "lifecycle action did not reproduce governed terminal identity"
        )


def _validate_observation(
    request: LifecycleActionRequest, observation: ActionObservation
) -> None:
    request.validate()
    binding = request.binding

    if observation.action is not request.action:
        raise AccountingContractError("action observation names the wrong lifecycle action")
    if observation.binding_id != binding.binding_id:
        raise AccountingContractError("action observation binding_id mismatch")
    if observation.source_id != binding.source_id:
        raise AccountingContractError("action observation source mismatch")
    if observation.candidate_id != binding.candidate_id:
        raise AccountingContractError("action observation candidate mismatch")
    if not observation.performed:
        raise AccountingContractError("lifecycle action was not performed")
    if observation.evidence_kind is not EvidenceKind.EXECUTED_CANDIDATE_ACTION:
        raise AccountingContractError(
            "surrogate evidence cannot satisfy an executed lifecycle action"
        )
    for name in ("action_id", "state_before_id", "state_after_id"):
        _nonnull(getattr(observation, name), name)

    before = set(observation.candidate_state_object_ids_before)
    after = set(observation.candidate_state_object_ids_after)

    if request.action is LifecycleAction.COLD_FIRST_REALIZATION:
        if not observation.cold_state_proven_absent:
            raise AccountingContractError(
                "cold first realization lacks proved absent candidate-owned accelerating state"
            )

    elif request.action is LifecycleAction.WARM_RETAINED_STATE_USE:
        if not observation.retained_state_id:
            raise AccountingContractError("warm use lacks retained_state_id")
        if observation.retained_state_candidate_id != binding.candidate_id:
            raise AccountingContractError(
                "warm state is not owned by the current candidate"
            )
        if observation.retained_state_id not in before:
            raise AccountingContractError(
                "warm state was not present in the candidate-owned pre-action state"
            )

    elif request.action is LifecycleAction.DELETION_REGENERATION:
        deleted = set(observation.deleted_object_ids)
        regenerated = set(observation.regenerated_object_ids)
        if not deleted or not regenerated:
            raise AccountingContractError(
                "rebuild requires actual candidate state deletion and regeneration"
            )
        if not deleted.issubset(before):
            raise AccountingContractError(
                "rebuild claims deletion of state not present before the action"
            )
        if not regenerated.issubset(after):
            raise AccountingContractError(
                "rebuild claims regeneration absent from post-action candidate state"
            )
        lineage = set(observation.regeneration_lineage)
        if not all(any(old == d for old, _ in lineage) for d in deleted):
            raise AccountingContractError(
                "rebuild lacks deleted-object to regenerated-object lineage"
            )

    elif request.action in (
        LifecycleAction.SOURCE_INVALIDATION,
        LifecycleAction.AUTHORITY_SEMANTIC_INVALIDATION,
    ):
        _nonnull(
            observation.invalidation_trigger_identity or "",
            "invalidation_trigger_identity",
        )
        if not observation.invalidated_unit_ids:
            raise AccountingContractError("invalidation executed no governed invalidation")
        if not observation.recomputed_unit_ids:
            raise AccountingContractError("invalidation executed no governed recomputation")

    elif request.action is LifecycleAction.STALE_STATE_RECOVERY:
        if not observation.stale_determinant_before or not observation.stale_determinant_after:
            raise AccountingContractError("stale-state exercise lacks determinant identities")
        if observation.stale_determinant_before == observation.stale_determinant_after:
            raise AccountingContractError(
                "stale-state exercise did not alter/invalidate a governed determinant"
            )
        if not observation.stale_detected or not observation.recovery_performed:
            raise AccountingContractError(
                "stale-state exercise lacks detection and recovery"
            )

    elif request.action is LifecycleAction.CORRUPT_STATE_RECOVERY:
        if not observation.corrupt_target_id or observation.corrupt_target_id not in before:
            raise AccountingContractError(
                "corruption target is not candidate-owned state present before exercise"
            )
        if not observation.corruption_injected or not observation.corrupt_detected:
            raise AccountingContractError(
                "corrupt-state exercise lacks actual corruption and detection"
            )
        if not observation.recovery_performed:
            raise AccountingContractError("corrupt-state exercise lacks recovery")

    elif request.action is LifecycleAction.INTERRUPTION_RECOVERY:
        if observation.interrupted_operation_id != request.governed_operation_id:
            raise AccountingContractError(
                "interruption did not target the governed candidate build/session operation"
            )
        if not observation.interrupted_candidate_state_id:
            raise AccountingContractError(
                "interruption lacks candidate-state target identity"
            )
        if observation.interrupted_candidate_state_id not in before:
            raise AccountingContractError(
                "interruption target is not governed candidate state"
            )
        if not observation.interruption_injected:
            raise AccountingContractError("no interruption was actually injected")
        if observation.recovered_operation_id != request.governed_operation_id:
            raise AccountingContractError(
                "interruption recovery did not resume/rebuild the governed operation"
            )
        if not observation.recovery_performed:
            raise AccountingContractError("interruption recovery did not complete")

    elif request.action is LifecycleAction.FRESH_PROCESS_REPLAY:
        if not observation.parent_process_token or not observation.replay_process_token:
            raise AccountingContractError("fresh replay lacks process tokens")
        if observation.parent_process_token == observation.replay_process_token:
            raise AccountingContractError("fresh replay reused the parent process")

    elif request.action is LifecycleAction.AUDIT_REVALIDATION:
        if observation.audit_primitive_identity != request.governed_operation_id:
            raise AccountingContractError(
                "audit metric is not bound to the governed audit primitive"
            )

    _require_terminal_identity(request, observation)


def _validate_telemetry(
    request: LifecycleActionRequest,
    observation: ActionObservation,
    metrics: Sequence[TelemetryMetric],
) -> tuple[MetricAccounting, ...]:
    names: set[str] = set()
    result: list[MetricAccounting] = []
    for metric in metrics:
        metric.validate_measured()
        if metric.name in names:
            raise AccountingContractError(
                f"telemetry metric {metric.name} was emitted more than once"
            )
        names.add(metric.name)
        if metric.action_id != observation.action_id:
            raise AccountingContractError(
                f"telemetry metric {metric.name} is not bound to executed action"
            )
        if metric.binding_id != request.binding.binding_id:
            raise AccountingContractError(
                f"telemetry metric {metric.name} is not bound to exact candidate/source/state"
            )
        required_action = LIFECYCLE_METRIC_ACTIONS.get(metric.name)
        if required_action is not None and required_action is not request.action:
            raise AccountingContractError(
                f"telemetry metric {metric.name} is attached to the wrong lifecycle action"
            )

        if (
            request.action is LifecycleAction.SOURCE_INVALIDATION
            and metric.name == "source_release_invalidation_recomputation_units"
            and metric.value != observation.observed_recomputation_units
        ):
            raise AccountingContractError(
                "source invalidation recomputation metric is not the observed executed unit count"
            )
        if (
            request.action is LifecycleAction.AUTHORITY_SEMANTIC_INVALIDATION
            and metric.name == "semantic_authority_invalidation_recomputation_units"
            and metric.value != observation.observed_recomputation_units
        ):
            raise AccountingContractError(
                "authority invalidation recomputation metric is not the observed executed unit count"
            )

        result.append(
            MetricAccounting(
                name=metric.name,
                state=metric.state,
                value=metric.value,
                unit=metric.unit,
            )
        )

    missing = set(request.expected_metric_names) - names
    if missing:
        raise AccountingContractError(
            "executed lifecycle action lacks required I06B metrics: "
            + ",".join(sorted(missing))
        )
    return tuple(result)


def execute_lifecycle_action(
    request: LifecycleActionRequest,
    action_port: LifecycleActionPort,
    telemetry_port: TelemetryPort,
) -> LifecycleAccountingReceipt:
    """Execute, validate, then measure one governed lifecycle action.

    Ordering is intentional: telemetry can only be admitted after a real
    candidate action passes action-contract validation.
    """

    request.validate()
    if request.not_applicable_reason is not None:
        raise AccountingContractError(
            "execute_lifecycle_action cannot execute a request marked not applicable"
        )

    observation = action_port.perform_lifecycle_action(request)
    _validate_observation(request, observation)
    metrics = _validate_telemetry(
        request,
        observation,
        telemetry_port.record_completed_lifecycle_action(request, observation),
    )

    return LifecycleAccountingReceipt(
        schema="FIABC_W3_I06C_LIFECYCLE_RECEIPT@1.0.0",
        disposition=AccountingDisposition.EXECUTED_NOW,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        source_sha256=request.binding.source_sha256,
        candidate_id=request.binding.candidate_id,
        candidate_owner_identity=request.binding.candidate_owner_identity,
        state_scope_identity=request.binding.state_scope_identity,
        action=request.action,
        action_id=observation.action_id,
        governed_operation_id=request.governed_operation_id,
        state_before_id=observation.state_before_id,
        state_after_id=observation.state_after_id,
        terminal_identity=observation.terminal_identity,
        metrics=metrics,
        evidence_refs=observation.evidence_refs,
    )


def typed_unreached_receipt(
    request: LifecycleActionRequest,
    reason: str,
) -> LifecycleAccountingReceipt:
    request.validate()
    _nonnull(reason, "reason")
    metrics = tuple(
        MetricAccounting(
            name=name,
            state=MetricState.NOT_REACHED_AUTHORIZED_STOP,
            value=None,
            unit="",
            reason=reason,
        )
        for name in request.expected_metric_names
    )
    return LifecycleAccountingReceipt(
        schema="FIABC_W3_I06C_LIFECYCLE_RECEIPT@1.0.0",
        disposition=AccountingDisposition.NOT_REACHED,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        source_sha256=request.binding.source_sha256,
        candidate_id=request.binding.candidate_id,
        candidate_owner_identity=request.binding.candidate_owner_identity,
        state_scope_identity=request.binding.state_scope_identity,
        action=request.action,
        action_id=None,
        governed_operation_id=request.governed_operation_id,
        state_before_id=None,
        state_after_id=None,
        terminal_identity=None,
        metrics=metrics,
        evidence_refs=(),
        reason=reason,
    )


def typed_not_applicable_receipt(
    request: LifecycleActionRequest,
    reason: str,
) -> LifecycleAccountingReceipt:
    request.validate()
    _nonnull(reason, "reason")
    metrics = tuple(
        MetricAccounting(
            name=name,
            state=MetricState.NOT_APPLICABLE_BY_FROZEN_COURT,
            value=None,
            unit="",
            reason=reason,
        )
        for name in request.expected_metric_names
    )
    return LifecycleAccountingReceipt(
        schema="FIABC_W3_I06C_LIFECYCLE_RECEIPT@1.0.0",
        disposition=AccountingDisposition.NOT_APPLICABLE,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        source_sha256=request.binding.source_sha256,
        candidate_id=request.binding.candidate_id,
        candidate_owner_identity=request.binding.candidate_owner_identity,
        state_scope_identity=request.binding.state_scope_identity,
        action=request.action,
        action_id=None,
        governed_operation_id=request.governed_operation_id,
        state_before_id=None,
        state_after_id=None,
        terminal_identity=None,
        metrics=metrics,
        evidence_refs=(),
        reason=reason,
    )


@dataclass(frozen=True)
class PreservedWorkPolicy:
    work_id: str
    policy: PreservedPolicy
    source_id: str | None
    candidate_id: str | None
    evidence_ref: str
    rationale: str


WAVE2_PRESERVED_WORK_POLICIES: Mapping[str, PreservedWorkPolicy] = {
    "P001": PreservedWorkPolicy(
        "P001",
        PreservedPolicy.COMMON_UPSTREAM,
        None,
        None,
        "HQ_HANDOFF/CHETIRI_FINAL_P2_COURT_MANIFEST_R1",
        "Lock1/Lock2 workload and authority freeze is candidate-neutral upstream capital.",
    ),
    "P004": PreservedWorkPolicy(
        "P004",
        PreservedPolicy.COMMON_UPSTREAM,
        None,
        None,
        "FIABC-W2-B02 independent parity-oracle material",
        "Candidate-neutral oracle production is common upstream capital.",
    ),
    "P006": PreservedWorkPolicy(
        "P006",
        PreservedPolicy.CONDITIONAL_FIELDWISE_NUMERIC,
        "LITS_I",
        "A",
        "WORKER_RETURNS/EE-P2X/01_LITS_I_A_FIRST_BUILD_STAGE.json",
        "LiTS-A numeric fields are eligible only after exact field-by-field compatibility proof.",
    ),
    "P007": PreservedWorkPolicy(
        "P007",
        PreservedPolicy.SEMANTIC_ONLY_NO_NUMERIC,
        "LITS_I",
        "B",
        "WORKER_RETURNS/EE-P2X/03_LITS_I_B_CACHELESS_C11_STAGE.json",
        "LiTS-B telemetry was explicitly not captured; no numeric substitute is lawful.",
    ),
    "P008": PreservedWorkPolicy(
        "P008",
        PreservedPolicy.CALIBRATION_ONLY,
        "LITS_I",
        "A",
        "PRE-P2 R10L Candidate-A calibration build",
        "Pre-P2 calibration cannot be promoted into dispositive P2 telemetry.",
    ),
    "P009": PreservedWorkPolicy(
        "P009",
        PreservedPolicy.AUTHORIZED_STOP,
        None,
        None,
        "WORKER_RETURNS/EE-P2X/00_RETURN.md",
        "Authorized stops preserve reached evidence and leave unreached metrics null.",
    ),
}


@dataclass(frozen=True)
class PreservedMetricEvidence:
    canonical_name: str
    unit: str
    value: int | float | None
    historical_field: str
    directly_observed: bool


@dataclass(frozen=True)
class PreservedReceiptEvidence:
    work_id: str
    receipt_ref: str
    source_id: str
    source_sha256: str
    candidate_id: str
    operation: LifecycleAction
    semantic_identity: str
    terminal_identity: str | None
    stage_reached: bool
    metrics: tuple[PreservedMetricEvidence, ...] = ()


@dataclass(frozen=True)
class PreservedCompatibilityProof:
    """Final-court proof needed before historical numeric credit is admitted."""

    preserved_receipt_ref: str
    current_binding_id: str
    workload_compatible: bool
    runtime_binding_compatible: bool
    state_binding_compatible: bool
    isolation_compatible: bool
    operation_compatible: bool
    metric_definition_matches: frozenset[str] = field(default_factory=frozenset)
    proof_refs: tuple[str, ...] = ()

    def all_operation_bindings_compatible(self) -> bool:
        return all(
            (
                self.workload_compatible,
                self.runtime_binding_compatible,
                self.state_binding_compatible,
                self.isolation_compatible,
                self.operation_compatible,
            )
        )


def build_lits_a_preserved_receipt(
    *,
    source_sha256: str,
    semantic_identity: str,
    terminal_identity: str | None,
    telemetry: Mapping[str, int | float | None],
) -> PreservedReceiptEvidence:
    """Normalize the historical P006 LiTS-A field names without granting credit."""

    aliases = (
        ("build_or_open_wall_ns", "wall_ns", "ns"),
        ("cpu_user_ns", "cpu_user_ns", "ns"),
        ("cpu_system_ns", "cpu_system_ns", "ns"),
        ("peak_rss_bytes", "peak_rss_bytes", "bytes"),
        ("peak_scratch_bytes", "peak_scratch_bytes", "bytes"),
        ("peak_scratch_file_count", "peak_scratch_file_count", "count"),
        ("source_open_count", "source_open_count", "count"),
        ("source_decode_count", "source_decode_count", "count"),
        ("bytes_read", "bytes_read", "bytes"),
        ("bytes_written", "bytes_written", "bytes"),
        ("bytes_rewritten", "bytes_rewritten", "bytes"),
    )
    metrics = tuple(
        PreservedMetricEvidence(
            canonical_name=canonical,
            unit=unit,
            value=telemetry.get(historical),
            historical_field=historical,
            directly_observed=historical in telemetry and telemetry.get(historical) is not None,
        )
        for canonical, historical, unit in aliases
    )
    return PreservedReceiptEvidence(
        work_id="P006",
        receipt_ref=WAVE2_PRESERVED_WORK_POLICIES["P006"].evidence_ref,
        source_id="LITS_I",
        source_sha256=source_sha256,
        candidate_id="A",
        operation=LifecycleAction.COLD_FIRST_REALIZATION,
        semantic_identity=semantic_identity,
        terminal_identity=terminal_identity,
        stage_reached=True,
        metrics=metrics,
    )


def build_lits_b_semantic_only_receipt(
    *,
    source_sha256: str,
    semantic_identity: str,
    terminal_identity: str | None = None,
) -> PreservedReceiptEvidence:
    return PreservedReceiptEvidence(
        work_id="P007",
        receipt_ref=WAVE2_PRESERVED_WORK_POLICIES["P007"].evidence_ref,
        source_id="LITS_I",
        source_sha256=source_sha256,
        candidate_id="B",
        operation=LifecycleAction.COLD_FIRST_REALIZATION,
        semantic_identity=semantic_identity,
        terminal_identity=terminal_identity,
        stage_reached=True,
        metrics=(),
    )


def adjudicate_preserved_work(
    *,
    request: LifecycleActionRequest,
    preserved: PreservedReceiptEvidence,
    compatibility: PreservedCompatibilityProof | None,
) -> LifecycleAccountingReceipt:
    """Apply the Wave-2 preserved-work law to one lifecycle obligation."""

    request.validate()
    policy = WAVE2_PRESERVED_WORK_POLICIES.get(preserved.work_id)
    if policy is None:
        raise AccountingContractError("preserved work is not recognized by Wave-2 B03")

    if preserved.receipt_ref != policy.evidence_ref:
        raise AccountingContractError("preserved receipt ref does not match Wave-2 policy")

    if policy.source_id is not None and request.binding.source_id != policy.source_id:
        raise AccountingContractError(
            "preserved work cannot satisfy a different source obligation"
        )
    if policy.candidate_id is not None and request.binding.candidate_id != policy.candidate_id:
        raise AccountingContractError(
            "preserved work from one candidate cannot satisfy another candidate"
        )
    if preserved.source_id != request.binding.source_id:
        raise AccountingContractError("preserved receipt source mismatch")
    if preserved.source_sha256 != request.binding.source_sha256:
        raise AccountingContractError("preserved receipt source SHA mismatch")
    if preserved.candidate_id != request.binding.candidate_id:
        raise AccountingContractError("preserved receipt candidate mismatch")
    if preserved.operation is not request.action:
        raise AccountingContractError("preserved receipt operation mismatch")

    numeric_values = [m.value for m in preserved.metrics if m.value is not None]
    if not preserved.stage_reached:
        if numeric_values:
            raise AccountingContractError(
                "unreached lifecycle stage cannot emit ordinary numeric metrics"
            )
        return LifecycleAccountingReceipt(
            schema="FIABC_W3_I06C_PRESERVED_WORK_ADJUDICATION@1.0.0",
            disposition=AccountingDisposition.NOT_REACHED,
            binding_id=request.binding.binding_id,
            source_id=request.binding.source_id,
            source_sha256=request.binding.source_sha256,
            candidate_id=request.binding.candidate_id,
            candidate_owner_identity=request.binding.candidate_owner_identity,
            state_scope_identity=request.binding.state_scope_identity,
            action=request.action,
            action_id=None,
            governed_operation_id=request.governed_operation_id,
            state_before_id=None,
            state_after_id=None,
            terminal_identity=None,
            metrics=tuple(
                MetricAccounting(
                    name=name,
                    state=MetricState.NOT_REACHED_AUTHORIZED_STOP,
                    value=None,
                    unit="",
                    reason="authorized stop before lifecycle stage",
                )
                for name in request.expected_metric_names
            ),
            evidence_refs=(preserved.receipt_ref,),
            reason="authorized stop before lifecycle stage",
            preserved_work_id=preserved.work_id,
            preserved_receipt_ref=preserved.receipt_ref,
        )

    if policy.policy is PreservedPolicy.COMMON_UPSTREAM:
        if numeric_values:
            raise AccountingContractError(
                "candidate-neutral upstream capital cannot be emitted as candidate numeric work"
            )
        return typed_not_applicable_receipt(
            request,
            "candidate-neutral upstream capital is excluded from candidate numeric cost",
        )

    if policy.policy in (
        PreservedPolicy.SEMANTIC_ONLY_NO_NUMERIC,
        PreservedPolicy.CALIBRATION_ONLY,
    ):
        if numeric_values and policy.policy is PreservedPolicy.SEMANTIC_ONLY_NO_NUMERIC:
            raise AccountingContractError(
                "semantic-only preserved policy forbids numeric telemetry"
            )
        return _semantic_only_preserved_receipt(
            request=request,
            preserved=preserved,
            reason=policy.rationale,
        )

    if policy.policy is PreservedPolicy.AUTHORIZED_STOP:
        if numeric_values:
            raise AccountingContractError(
                "authorized-stop policy cannot manufacture unreached numeric telemetry"
            )
        return typed_unreached_receipt(request, policy.rationale)

    if policy.policy is not PreservedPolicy.CONDITIONAL_FIELDWISE_NUMERIC:
        raise AccountingContractError("unhandled preserved-work policy")

    if compatibility is None:
        return _semantic_only_preserved_receipt(
            request=request,
            preserved=preserved,
            reason="final accounting compatibility proof absent",
        )
    if compatibility.preserved_receipt_ref != preserved.receipt_ref:
        raise AccountingContractError("compatibility proof receipt ref mismatch")
    if compatibility.current_binding_id != request.binding.binding_id:
        raise AccountingContractError("compatibility proof current binding mismatch")

    compatible = compatibility.all_operation_bindings_compatible()
    by_name = {m.canonical_name: m for m in preserved.metrics}
    metric_records: list[MetricAccounting] = []
    numeric_credit_count = 0

    for name in request.expected_metric_names:
        item = by_name.get(name)
        if (
            compatible
            and item is not None
            and item.directly_observed
            and item.value is not None
            and name in compatibility.metric_definition_matches
        ):
            if not isinstance(item.value, (int, float)) or isinstance(item.value, bool):
                raise AccountingContractError(
                    f"preserved metric {name} is not a numeric observation"
                )
            numeric_credit_count += 1
            metric_records.append(
                MetricAccounting(
                    name=name,
                    state=MetricState.MEASURED,
                    value=item.value,
                    unit=item.unit,
                    source_field=item.historical_field,
                    reason="field-by-field preserved numeric credit passed final compatibility proof",
                )
            )
        else:
            metric_records.append(
                MetricAccounting(
                    name=name,
                    state=MetricState.MEASUREMENT_NOT_CAPTURED,
                    value=None,
                    unit=item.unit if item is not None else "",
                    source_field=item.historical_field if item is not None else None,
                    reason=(
                        "preserved numeric credit barred by incompatible binding/state/isolation/metric definition"
                        if not compatible
                        else "qualifying numeric telemetry absent for this field"
                    ),
                )
            )

    disposition = (
        AccountingDisposition.LAWFULLY_PRESERVED_MEASURED_WORK
        if numeric_credit_count
        else AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY
    )
    return LifecycleAccountingReceipt(
        schema="FIABC_W3_I06C_PRESERVED_WORK_ADJUDICATION@1.0.0",
        disposition=disposition,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        source_sha256=request.binding.source_sha256,
        candidate_id=request.binding.candidate_id,
        candidate_owner_identity=request.binding.candidate_owner_identity,
        state_scope_identity=request.binding.state_scope_identity,
        action=request.action,
        action_id=None,
        governed_operation_id=request.governed_operation_id,
        state_before_id=None,
        state_after_id=None,
        terminal_identity=preserved.terminal_identity,
        metrics=tuple(metric_records),
        evidence_refs=(preserved.receipt_ref,) + tuple(compatibility.proof_refs),
        reason=policy.rationale,
        preserved_work_id=preserved.work_id,
        preserved_receipt_ref=preserved.receipt_ref,
    )


def _semantic_only_preserved_receipt(
    *,
    request: LifecycleActionRequest,
    preserved: PreservedReceiptEvidence,
    reason: str,
) -> LifecycleAccountingReceipt:
    by_name = {m.canonical_name: m for m in preserved.metrics}
    metrics = tuple(
        MetricAccounting(
            name=name,
            state=MetricState.MEASUREMENT_NOT_CAPTURED,
            value=None,
            unit=by_name[name].unit if name in by_name else "",
            source_field=by_name[name].historical_field if name in by_name else None,
            reason=reason,
        )
        for name in request.expected_metric_names
    )
    return LifecycleAccountingReceipt(
        schema="FIABC_W3_I06C_PRESERVED_WORK_ADJUDICATION@1.0.0",
        disposition=AccountingDisposition.PRESERVED_SEMANTIC_EVIDENCE_WITHOUT_NUMERIC_TELEMETRY,
        binding_id=request.binding.binding_id,
        source_id=request.binding.source_id,
        source_sha256=request.binding.source_sha256,
        candidate_id=request.binding.candidate_id,
        candidate_owner_identity=request.binding.candidate_owner_identity,
        state_scope_identity=request.binding.state_scope_identity,
        action=request.action,
        action_id=None,
        governed_operation_id=request.governed_operation_id,
        state_before_id=None,
        state_after_id=None,
        terminal_identity=preserved.terminal_identity,
        metrics=metrics,
        evidence_refs=(preserved.receipt_ref,),
        reason=reason,
        preserved_work_id=preserved.work_id,
        preserved_receipt_ref=preserved.receipt_ref,
    )


def receipt_as_dict(receipt: LifecycleAccountingReceipt) -> Mapping[str, Any]:
    return {
        "schema": receipt.schema,
        "receipt_id": receipt.receipt_id,
        "disposition": receipt.disposition.value,
        "binding_id": receipt.binding_id,
        "source_id": receipt.source_id,
        "source_sha256": receipt.source_sha256,
        "candidate_id": receipt.candidate_id,
        "candidate_owner_identity": receipt.candidate_owner_identity,
        "state_scope_identity": receipt.state_scope_identity,
        "action": receipt.action.value,
        "action_id": receipt.action_id,
        "governed_operation_id": receipt.governed_operation_id,
        "state_before_id": receipt.state_before_id,
        "state_after_id": receipt.state_after_id,
        "terminal_identity": receipt.terminal_identity,
        "metrics": [
            {
                "name": m.name,
                "state": m.state.value,
                "value": m.value,
                "unit": m.unit,
                "source_field": m.source_field,
                "reason": m.reason,
            }
            for m in receipt.metrics
        ],
        "evidence_refs": list(receipt.evidence_refs),
        "reason": receipt.reason,
        "preserved_work_id": receipt.preserved_work_id,
        "preserved_receipt_ref": receipt.preserved_receipt_ref,
    }


__all__ = [
    "AccountingContractError",
    "AccountingDisposition",
    "ActionObservation",
    "CallableLifecycleActionAdapter",
    "CallableTelemetryAdapter",
    "EvidenceKind",
    "LifecycleAccountingReceipt",
    "LifecycleAction",
    "LifecycleActionPort",
    "LifecycleActionRequest",
    "LifecycleBinding",
    "LIFECYCLE_METRIC_ACTIONS",
    "MetricAccounting",
    "MetricState",
    "PreservedCompatibilityProof",
    "PreservedMetricEvidence",
    "PreservedPolicy",
    "PreservedReceiptEvidence",
    "ProcessIsolationReceipt",
    "TelemetryMetric",
    "TelemetryPort",
    "WAVE2_PRESERVED_WORK_POLICIES",
    "adjudicate_preserved_work",
    "build_lits_a_preserved_receipt",
    "build_lits_b_semantic_only_receipt",
    "execute_lifecycle_action",
    "receipt_as_dict",
    "typed_not_applicable_receipt",
    "typed_unreached_receipt",
]
