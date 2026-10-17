"""FIABC equal-work telemetry semantics.

This module implements only measurement/accounting semantics for FIABC IMP11.
It intentionally does not choose process-isolation policy or lifecycle policy.

I06A integration surface:
    TelemetryLedger.record_process_envelope(ProcessEnvelopeReceipt)

I06C integration surfaces:
    TelemetryLedger.bind_lifecycle_receipt(LifecycleActionReceipt)
    TelemetryLedger.record_observed_value(...)
    TelemetryLedger.record_duration(...)

All canonical metrics are immutable at their defined grain. Missing telemetry is
typed null. Candidate-total CPU/RSS/wall are derived from candidate-local
process envelopes; observed I/O and scratch peaks are derived from event
accounting, never from endpoint-size proxies.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple


CONTRACT_ID = "FIABC_W3_I06B_TELEMETRY_SEMANTICS@1.0.0"
CANDIDATE_ENVELOPE_PHASE = "__CANDIDATE_ENVELOPE__"
UNREACHED_PHASE = "__UNREACHED_OR_UNCAPTURED__"


class TelemetryContractError(ValueError):
    """Raised when an observation would violate the accounting constitution."""


class MetricState(str, Enum):
    MEASURED = "MEASURED"
    NOT_APPLICABLE_BY_FROZEN_COURT = "NOT_APPLICABLE_BY_FROZEN_COURT"
    NOT_REACHED_AUTHORIZED_STOP = "NOT_REACHED_AUTHORIZED_STOP"
    MEASUREMENT_NOT_CAPTURED = "MEASUREMENT_NOT_CAPTURED"
    INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH = (
        "INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH"
    )


class CostClass(str, Enum):
    C0 = "COMMON_UPSTREAM_PRODUCTION__EXCLUDED_FROM_CANDIDATE_COST"
    C1 = "CANDIDATE_ACCESS_TO_COMMON_INPUT__INCLUDED"
    C2 = "CANDIDATE_PHYSICAL_REALIZATION__INCLUDED"
    C3 = "COMMON_LOGICAL_OUTPUT_EXECUTION__INCLUDED"
    C4 = "COURT_ADMINISTRATION__EXCLUDED_FROM_CANDIDATE_COST"


class MetricGrain(str, Enum):
    CANDIDATE = "SOURCE_X_CANDIDATE"
    PHASE = "SOURCE_X_CANDIDATE_X_PHASE"
    LIFECYCLE = "SOURCE_X_CANDIDATE_X_LIFECYCLE_ACTION"


@dataclass(frozen=True)
class CellIdentity:
    source_id: str
    source_sha256: str
    candidate_id: str
    workload_id: str
    authority_set_id: str

    def __post_init__(self) -> None:
        for name in ("source_id", "source_sha256", "candidate_id", "workload_id", "authority_set_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise TelemetryContractError(f"{name} must be an exact non-empty identity")
        if len(self.source_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in self.source_sha256):
            raise TelemetryContractError("source_sha256 must be an exact 64-character SHA-256")
        if self.candidate_id not in {"A", "B", "C"}:
            raise TelemetryContractError("candidate_id must be one of frozen candidates A/B/C")


@dataclass(frozen=True)
class ObservationContext:
    source_id: str
    source_sha256: str
    candidate_id: str
    phase_id: str
    process_token: str
    cost_class: CostClass
    lifecycle_action_id: Optional[str] = None
    evidence_ref: Optional[str] = None

    def __post_init__(self) -> None:
        for name in ("source_id", "source_sha256", "candidate_id", "phase_id", "process_token"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise TelemetryContractError(
                    "metric observation requires exact candidate/source/phase/process identity"
                )


@dataclass(frozen=True)
class ProcessEnvelopeReceipt:
    """I06A -> I06B process accounting interface.

    Counters are cumulative process counters at the exact candidate-local start
    and stop boundaries. I06B computes deltas; callers never supply a purported
    CPU delta. RSS must already be process-local.
    """

    cell: CellIdentity
    phase_id: str
    process_token: str
    pid: int
    role: str  # MAIN or CHILD
    parent_process_token: Optional[str]
    cpu_scope: str  # PROCESS_SELF_ONLY
    rss_scope: str  # CANDIDATE_PROCESS_LOCAL
    cpu_user_start_ns: int
    cpu_user_stop_ns: int
    cpu_system_start_ns: int
    cpu_system_stop_ns: int
    wall_start_ns: int
    wall_stop_ns: int
    peak_rss_bytes: int
    evidence_ref: str

    def __post_init__(self) -> None:
        if self.role not in {"MAIN", "CHILD"}:
            raise TelemetryContractError("process role must be MAIN or CHILD")
        for name in ("phase_id", "process_token", "evidence_ref"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise TelemetryContractError(f"{name} is required")
        if not isinstance(self.pid, int) or self.pid <= 0:
            raise TelemetryContractError("pid must be a positive integer")
        for name in (
            "cpu_user_start_ns", "cpu_user_stop_ns",
            "cpu_system_start_ns", "cpu_system_stop_ns",
            "wall_start_ns", "wall_stop_ns", "peak_rss_bytes",
        ):
            value = getattr(self, name)
            if not isinstance(value, int) or value < 0:
                raise TelemetryContractError(f"{name} must be a non-negative integer")
        if self.cpu_user_stop_ns < self.cpu_user_start_ns:
            raise TelemetryContractError("user CPU counter moved backwards")
        if self.cpu_system_stop_ns < self.cpu_system_start_ns:
            raise TelemetryContractError("system CPU counter moved backwards")
        if self.wall_stop_ns < self.wall_start_ns:
            raise TelemetryContractError("wall clock moved backwards")


@dataclass(frozen=True)
class LifecycleActionReceipt:
    """I06C -> I06B lifecycle binding interface.

    I06B does not decide whether an action was required. It requires any
    lifecycle-scoped metric to point at an exact action receipt supplied by I06C.
    """

    cell: CellIdentity
    action_id: str
    action_type: str
    phase_id: str
    process_token: str
    outcome: str
    evidence_ref: str

    def __post_init__(self) -> None:
        for name in ("action_id", "action_type", "phase_id", "process_token", "outcome", "evidence_ref"):
            if not isinstance(getattr(self, name), str) or not getattr(self, name).strip():
                raise TelemetryContractError(f"{name} is required")


@dataclass(frozen=True)
class MetricDefinition:
    name: str
    unit: str
    grain: MetricGrain
    kind: str


def _defs() -> Tuple[MetricDefinition, ...]:
    C = MetricGrain.CANDIDATE
    L = MetricGrain.LIFECYCLE
    return (
        MetricDefinition("source_open_count", "count", C, "counter"),
        MetricDefinition("source_decode_count", "count", C, "counter"),
        MetricDefinition("source_reread_count", "count", C, "counter"),
        MetricDefinition("bytes_read", "bytes", C, "observed_io"),
        MetricDefinition("bytes_written", "bytes", C, "observed_io"),
        MetricDefinition("bytes_rewritten", "bytes", C, "observed_io"),
        MetricDefinition("candidate_total_wall_ns", "ns", C, "process_envelope"),
        MetricDefinition("build_or_open_wall_ns", "ns", C, "timer"),
        MetricDefinition("cpu_user_ns", "ns", C, "process_envelope"),
        MetricDefinition("cpu_system_ns", "ns", C, "process_envelope"),
        MetricDefinition("peak_rss_bytes", "bytes", C, "process_envelope"),
        MetricDefinition("peak_scratch_bytes", "bytes", C, "scratch_high_water"),
        MetricDefinition("peak_scratch_file_count", "count", C, "scratch_high_water"),
        MetricDefinition("durable_authoritative_bytes", "bytes", C, "state_size"),
        MetricDefinition("durable_transformed_regenerable_bytes", "bytes", C, "state_size"),
        MetricDefinition("warm_retained_state_bytes", "bytes", C, "state_size"),
        MetricDefinition("cold_i03_latency_ns", "ns", C, "timer"),
        MetricDefinition("warm_i03_latency_ns", "ns", C, "timer"),
        MetricDefinition("i05_learned_production_wall_ns", "ns", C, "timer"),
        MetricDefinition("i05_learned_production_throughput_per_s", "candidates/s", C, "derived"),
        MetricDefinition("repeated_research_source_open_count", "count", C, "counter"),
        MetricDefinition("repeated_research_source_redecode_count", "count", C, "counter"),
        MetricDefinition("repeated_research_source_reread_count", "count", C, "counter"),
        MetricDefinition("delete_rebuild_wall_ns", "ns", L, "timer"),
        MetricDefinition("source_release_invalidation_recomputation_units", "units", L, "counter"),
        MetricDefinition("source_release_invalidation_wall_ns", "ns", L, "timer"),
        MetricDefinition("source_release_invalidation_bytes_rewritten", "bytes", L, "observed_io"),
        MetricDefinition("semantic_authority_invalidation_recomputation_units", "units", L, "counter"),
        MetricDefinition("semantic_authority_invalidation_wall_ns", "ns", L, "timer"),
        MetricDefinition("semantic_authority_invalidation_bytes_rewritten", "bytes", L, "observed_io"),
        MetricDefinition("fresh_process_replay_wall_ns", "ns", L, "timer"),
        MetricDefinition("fresh_process_replay_cpu_ns", "ns", L, "process_envelope"),
        MetricDefinition("audit_wall_ns", "ns", C, "timer"),
        MetricDefinition("persistent_bytes_removable_with_zero_information_loss", "bytes", C, "state_size"),
        MetricDefinition("implementation_moving_parts_count", "count", C, "structural_count"),
    )


METRIC_DEFINITIONS: Mapping[str, MetricDefinition] = {d.name: d for d in _defs()}

DIRECT_WRITE_FORBIDDEN = frozenset({
    "bytes_read", "bytes_written", "bytes_rewritten",
    "candidate_total_wall_ns", "cpu_user_ns", "cpu_system_ns", "peak_rss_bytes",
    "peak_scratch_bytes", "peak_scratch_file_count", "fresh_process_replay_cpu_ns",
    "source_release_invalidation_bytes_rewritten",
    "semantic_authority_invalidation_bytes_rewritten",
})

NONNUMERIC_STATES = frozenset({
    MetricState.NOT_APPLICABLE_BY_FROZEN_COURT,
    MetricState.NOT_REACHED_AUTHORIZED_STOP,
    MetricState.MEASUREMENT_NOT_CAPTURED,
    MetricState.INVALID_MEASUREMENT__ACCOUNTING_CONTRACT_BREACH,
})


def metric_definition_manifest() -> Mapping[str, Mapping[str, str]]:
    return {
        name: {
            "unit": d.unit,
            "grain": d.grain.value,
            "kind": d.kind,
        }
        for name, d in sorted(METRIC_DEFINITIONS.items())
    }


METRIC_DEFINITION_HASH = hashlib.sha256(
    json.dumps(metric_definition_manifest(), sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()


@dataclass(frozen=True)
class MetricRecord:
    name: str
    state: MetricState
    value: Optional[float]
    unit: str
    source_id: str
    source_sha256: str
    candidate_id: str
    phase_id: str
    process_token: str
    cost_class: str
    lifecycle_action_id: Optional[str]
    evidence_kind: str
    evidence_ref: Optional[str]

    def as_dict(self) -> Mapping[str, Any]:
        out = asdict(self)
        out["state"] = self.state.value
        return out


@dataclass(frozen=True)
class PhaseCpuRecord:
    phase_id: str
    process_token: str
    user_cpu_ns: int
    system_cpu_ns: int
    parent_phase_id: Optional[str]
    evidence_ref: str

    def as_dict(self) -> Mapping[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IOEvent:
    ordinal: int
    operation: str
    byte_count: int
    object_id: str
    rewrite_of: Optional[str]
    source_id: str
    source_sha256: str
    candidate_id: str
    phase_id: str
    process_token: str
    cost_class: str
    lifecycle_action_id: Optional[str]
    evidence_ref: Optional[str]
    charged_to_candidate: bool

    def as_dict(self) -> Mapping[str, Any]:
        return asdict(self)


class TelemetryLedger:
    """Immutable telemetry ledger for exactly one source x candidate cell."""

    def __init__(self, cell: CellIdentity):
        self.cell = cell
        self._metrics: Dict[Tuple[Any, ...], MetricRecord] = {}
        self._phase_cpu: Dict[Tuple[str, str], PhaseCpuRecord] = {}
        self._processes: Dict[str, ProcessEnvelopeReceipt] = {}
        self._main_process_token: Optional[str] = None
        self._lifecycle: Dict[str, LifecycleActionReceipt] = {}
        self._io_events: list[IOEvent] = []
        self._io_sealed = False
        self._scratch_sizes: Dict[str, int] = {}
        self._scratch_peak_bytes = 0
        self._scratch_peak_files = 0
        self._scratch_observed = False
        self._scratch_sealed = False
        self._source_event_counts = {"open": 0, "decode": 0, "reread": 0}
        self._source_events_sealed = False

    # ---------- identity / provenance ----------

    def _validate_cell(self, other: CellIdentity) -> None:
        if other != self.cell:
            raise TelemetryContractError("cross-candidate/source/workload attribution rejected")

    def _validate_context(self, ctx: ObservationContext) -> None:
        if (
            ctx.source_id != self.cell.source_id
            or ctx.source_sha256 != self.cell.source_sha256
            or ctx.candidate_id != self.cell.candidate_id
        ):
            raise TelemetryContractError("observation identity does not match telemetry cell")
        if not ctx.phase_id.strip() or not ctx.process_token.strip():
            raise TelemetryContractError(
                "metric without exact candidate/source/phase/process identity fails closed"
            )
        if ctx.lifecycle_action_id is not None:
            receipt = self._lifecycle.get(ctx.lifecycle_action_id)
            if receipt is None:
                raise TelemetryContractError("lifecycle metric lacks bound I06C action receipt")
            if receipt.phase_id != ctx.phase_id:
                raise TelemetryContractError("lifecycle metric phase drifts from action receipt")
            if receipt.process_token != ctx.process_token:
                child = self._processes.get(ctx.process_token)
                child_bound = (
                    receipt.action_type == "FRESH_PROCESS_REPLAY"
                    and child is not None
                    and child.role == "CHILD"
                    and child.parent_process_token == receipt.process_token
                    and child.phase_id == receipt.phase_id
                )
                if not child_bound:
                    raise TelemetryContractError("lifecycle metric process provenance drifts from action receipt")

    def _slot(self, definition: MetricDefinition, ctx: ObservationContext) -> Tuple[Any, ...]:
        base = (
            definition.name,
            self.cell.source_id,
            self.cell.source_sha256,
            self.cell.candidate_id,
        )
        if definition.grain == MetricGrain.CANDIDATE:
            return base
        if definition.grain == MetricGrain.PHASE:
            return base + (ctx.phase_id,)
        if ctx.lifecycle_action_id is None:
            raise TelemetryContractError("lifecycle-grain metric requires lifecycle_action_id")
        return base + (ctx.lifecycle_action_id,)

    def _write(
        self,
        metric_name: str,
        ctx: ObservationContext,
        *,
        state: MetricState,
        value: Optional[float],
        evidence_kind: str,
        internal: bool = False,
    ) -> MetricRecord:
        self._validate_context(ctx)
        definition = METRIC_DEFINITIONS.get(metric_name)
        if definition is None:
            raise TelemetryContractError(f"unknown metric field: {metric_name}")
        if not internal and metric_name in DIRECT_WRITE_FORBIDDEN:
            raise TelemetryContractError(
                f"{metric_name} is derived from event/process accounting and cannot be directly assigned"
            )
        if state == MetricState.MEASURED:
            if value is None or isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TelemetryContractError("MEASURED metric requires a numeric observed value")
            if value < 0:
                raise TelemetryContractError("metric values cannot be negative")
        elif value is not None:
            raise TelemetryContractError("unavailable/unreached metric must carry typed null, never numeric zero")
        key = self._slot(definition, ctx)
        if key in self._metrics:
            raise TelemetryContractError(
                f"immutable metric already written at {definition.grain.value}: {metric_name}"
            )
        record = MetricRecord(
            name=metric_name,
            state=state,
            value=value,
            unit=definition.unit,
            source_id=self.cell.source_id,
            source_sha256=self.cell.source_sha256,
            candidate_id=self.cell.candidate_id,
            phase_id=ctx.phase_id,
            process_token=ctx.process_token,
            cost_class=ctx.cost_class.value,
            lifecycle_action_id=ctx.lifecycle_action_id,
            evidence_kind=evidence_kind,
            evidence_ref=ctx.evidence_ref,
        )
        self._metrics[key] = record
        return record

    # ---------- I06A process envelope ----------

    def record_process_envelope(self, receipt: ProcessEnvelopeReceipt) -> None:
        self._validate_cell(receipt.cell)
        if receipt.cpu_scope != "PROCESS_SELF_ONLY":
            raise TelemetryContractError(
                "cumulative/self+children CPU cannot be admitted as a process delta"
            )
        if receipt.rss_scope != "CANDIDATE_PROCESS_LOCAL":
            raise TelemetryContractError(
                "process-global/process-history RSS is forbidden for candidate-local RSS"
            )
        if receipt.process_token in self._processes:
            raise TelemetryContractError("process envelope is write-once")
        if receipt.role == "MAIN":
            if self._main_process_token is not None:
                raise TelemetryContractError("candidate cell may bind exactly one MAIN process")
            if receipt.parent_process_token is not None:
                raise TelemetryContractError("MAIN process may not have a parent process token")
            self._main_process_token = receipt.process_token
        else:
            if not receipt.parent_process_token:
                raise TelemetryContractError("CHILD process must identify its parent")
        self._processes[receipt.process_token] = receipt

    def observe_phase_cpu_counters(
        self,
        ctx: ObservationContext,
        *,
        user_start_ns: int,
        user_stop_ns: int,
        system_start_ns: int,
        system_stop_ns: int,
        parent_phase_id: Optional[str] = None,
        evidence_ref: str,
    ) -> PhaseCpuRecord:
        self._validate_context(ctx)
        for value in (user_start_ns, user_stop_ns, system_start_ns, system_stop_ns):
            if not isinstance(value, int) or value < 0:
                raise TelemetryContractError("phase CPU counters must be non-negative integers")
        if user_stop_ns < user_start_ns or system_stop_ns < system_start_ns:
            raise TelemetryContractError("phase CPU cumulative counter moved backwards")
        key = (ctx.phase_id, ctx.process_token)
        if key in self._phase_cpu:
            raise TelemetryContractError("phase CPU observation is immutable")
        rec = PhaseCpuRecord(
            phase_id=ctx.phase_id,
            process_token=ctx.process_token,
            user_cpu_ns=user_stop_ns - user_start_ns,
            system_cpu_ns=system_stop_ns - system_start_ns,
            parent_phase_id=parent_phase_id,
            evidence_ref=evidence_ref,
        )
        self._phase_cpu[key] = rec
        return rec

    def seal_process_metrics(self, *, evidence_ref: str) -> None:
        if self._main_process_token is None:
            raise TelemetryContractError("cannot seal candidate process metrics without MAIN envelope")
        main = self._processes[self._main_process_token]
        for rec in self._processes.values():
            if rec.role == "CHILD" and rec.parent_process_token not in self._processes:
                raise TelemetryContractError("child process parent is not bound to this cell")
        user = sum(r.cpu_user_stop_ns - r.cpu_user_start_ns for r in self._processes.values())
        system = sum(r.cpu_system_stop_ns - r.cpu_system_start_ns for r in self._processes.values())
        peak = max(r.peak_rss_bytes for r in self._processes.values())
        wall = main.wall_stop_ns - main.wall_start_ns
        ctx = ObservationContext(
            source_id=self.cell.source_id,
            source_sha256=self.cell.source_sha256,
            candidate_id=self.cell.candidate_id,
            phase_id=CANDIDATE_ENVELOPE_PHASE,
            process_token=main.process_token,
            cost_class=CostClass.C2,
            evidence_ref=evidence_ref,
        )
        self._write("cpu_user_ns", ctx, state=MetricState.MEASURED, value=user,
                    evidence_kind="NONOVERLAPPING_PROCESS_SELF_CPU_ENVELOPES", internal=True)
        self._write("cpu_system_ns", ctx, state=MetricState.MEASURED, value=system,
                    evidence_kind="NONOVERLAPPING_PROCESS_SELF_CPU_ENVELOPES", internal=True)
        self._write("peak_rss_bytes", ctx, state=MetricState.MEASURED, value=peak,
                    evidence_kind="MAX_CANDIDATE_LOCAL_PROCESS_RSS", internal=True)
        self._write("candidate_total_wall_ns", ctx, state=MetricState.MEASURED, value=wall,
                    evidence_kind="OUTER_MAIN_PROCESS_ENVELOPE", internal=True)

    def seal_fresh_process_replay_cpu(
        self,
        *,
        process_token: str,
        ctx: ObservationContext,
    ) -> MetricRecord:
        """Materialize M035 from an exact I06A child envelope bound to an I06C action."""
        self._validate_context(ctx)
        rec = self._processes.get(process_token)
        if rec is None or rec.role != "CHILD":
            raise TelemetryContractError("fresh replay CPU requires an exact CHILD process envelope")
        if ctx.process_token != process_token or rec.phase_id != ctx.phase_id:
            raise TelemetryContractError("fresh replay CPU provenance drifts from child envelope")
        if ctx.lifecycle_action_id is None:
            raise TelemetryContractError("fresh replay CPU requires an exact I06C lifecycle action")
        value = (
            rec.cpu_user_stop_ns - rec.cpu_user_start_ns
            + rec.cpu_system_stop_ns - rec.cpu_system_start_ns
        )
        return self._write(
            "fresh_process_replay_cpu_ns",
            ctx,
            state=MetricState.MEASURED,
            value=value,
            evidence_kind="I06A_CHILD_PROCESS_SELF_CPU_ENVELOPE",
            internal=True,
        )

    # ---------- I06C lifecycle receipt binding ----------

    def bind_lifecycle_receipt(self, receipt: LifecycleActionReceipt) -> None:
        self._validate_cell(receipt.cell)
        if receipt.action_id in self._lifecycle:
            raise TelemetryContractError("lifecycle action receipt is immutable")
        self._lifecycle[receipt.action_id] = receipt

    # ---------- direct observed values / timers ----------

    def record_observed_value(
        self,
        metric_name: str,
        ctx: ObservationContext,
        value: float,
        *,
        evidence_kind: str,
    ) -> MetricRecord:
        return self._write(
            metric_name,
            ctx,
            state=MetricState.MEASURED,
            value=value,
            evidence_kind=evidence_kind,
            internal=False,
        )

    def record_duration(
        self,
        metric_name: str,
        ctx: ObservationContext,
        *,
        monotonic_start_ns: int,
        monotonic_stop_ns: int,
        state_predicate_ref: str,
    ) -> MetricRecord:
        if metric_name not in METRIC_DEFINITIONS or METRIC_DEFINITIONS[metric_name].unit != "ns":
            raise TelemetryContractError("duration hook requires an ns metric")
        if metric_name in {"cpu_user_ns", "cpu_system_ns", "candidate_total_wall_ns", "fresh_process_replay_cpu_ns"}:
            raise TelemetryContractError("process-accounting metrics cannot be supplied as generic durations")
        if monotonic_start_ns < 0 or monotonic_stop_ns < monotonic_start_ns:
            raise TelemetryContractError("invalid monotonic interval")
        if not state_predicate_ref:
            raise TelemetryContractError("duration requires exact state/lifecycle predicate evidence")
        return self._write(
            metric_name,
            ctx,
            state=MetricState.MEASURED,
            value=monotonic_stop_ns - monotonic_start_ns,
            evidence_kind=f"MONOTONIC_INTERVAL::{state_predicate_ref}",
            internal=False,
        )

    def mark_unavailable(
        self,
        metric_name: str,
        ctx: ObservationContext,
        *,
        state: MetricState,
        reason: str,
    ) -> MetricRecord:
        if state not in NONNUMERIC_STATES:
            raise TelemetryContractError("mark_unavailable requires a typed nonnumeric state")
        if not reason:
            raise TelemetryContractError("typed unavailable metric requires a reason")
        return self._write(
            metric_name,
            ctx,
            state=state,
            value=None,
            evidence_kind=f"TYPED_NULL::{reason}",
            internal=True,
        )

    def mark_lifecycle_not_applicable(
        self,
        metric_name: str,
        ctx: ObservationContext,
        *,
        reason: str,
    ) -> MetricRecord:
        """Write a frozen-court N/A lifecycle slot without inventing an action receipt."""
        self._validate_context(ctx)
        definition = METRIC_DEFINITIONS.get(metric_name)
        if definition is None or definition.grain != MetricGrain.LIFECYCLE:
            raise TelemetryContractError("lifecycle N/A helper requires a lifecycle-grain metric")
        if ctx.lifecycle_action_id is not None:
            raise TelemetryContractError("lifecycle N/A cannot bind a performed action")
        if not reason:
            raise TelemetryContractError("lifecycle N/A requires exact frozen-court reason")
        key = (
            definition.name,
            self.cell.source_id,
            self.cell.source_sha256,
            self.cell.candidate_id,
            "__NOT_APPLICABLE_BY_FROZEN_COURT__",
        )
        if key in self._metrics:
            raise TelemetryContractError("immutable lifecycle N/A metric already written")
        record = MetricRecord(
            name=metric_name,
            state=MetricState.NOT_APPLICABLE_BY_FROZEN_COURT,
            value=None,
            unit=definition.unit,
            source_id=self.cell.source_id,
            source_sha256=self.cell.source_sha256,
            candidate_id=self.cell.candidate_id,
            phase_id=ctx.phase_id,
            process_token=ctx.process_token,
            cost_class=ctx.cost_class.value,
            lifecycle_action_id=None,
            evidence_kind=f"TYPED_NULL::{reason}",
            evidence_ref=ctx.evidence_ref,
        )
        self._metrics[key] = record
        return record

    # ---------- source counters ----------

    def observe_source_event(self, ctx: ObservationContext, *, event: str) -> None:
        self._validate_context(ctx)
        if ctx.cost_class in {CostClass.C0, CostClass.C4}:
            raise TelemetryContractError("candidate source counters cannot charge excluded C0/C4 work")
        if event not in self._source_event_counts:
            raise TelemetryContractError("source event must be open/decode/reread")
        self._source_event_counts[event] += 1

    def seal_source_event_counters(self, ctx: ObservationContext) -> None:
        self._validate_context(ctx)
        if self._source_events_sealed:
            raise TelemetryContractError("source event accounting already sealed")
        self._source_events_sealed = True
        mapping = {
            "open": "source_open_count",
            "decode": "source_decode_count",
            "reread": "source_reread_count",
        }
        for event, metric in mapping.items():
            self._write(
                metric, ctx, state=MetricState.MEASURED,
                value=self._source_event_counts[event],
                evidence_kind="OBSERVED_SOURCE_EVENT_ACCOUNTING",
                internal=True,
            )

    # ---------- observed I/O ----------

    def observe_io(
        self,
        ctx: ObservationContext,
        *,
        operation: str,
        byte_count: int,
        object_id: str,
        rewrite_of: Optional[str] = None,
    ) -> IOEvent:
        self._validate_context(ctx)
        if self._io_sealed:
            raise TelemetryContractError("I/O event stream is sealed")
        if operation not in {"READ", "WRITE"}:
            raise TelemetryContractError("I/O operation must be READ or WRITE")
        if not isinstance(byte_count, int) or byte_count < 0:
            raise TelemetryContractError("I/O byte_count must be a non-negative integer")
        if not object_id:
            raise TelemetryContractError("I/O event requires exact logical object identity")
        if rewrite_of is not None and operation != "WRITE":
            raise TelemetryContractError("rewrite lineage applies only to WRITE")
        charged = ctx.cost_class in {CostClass.C1, CostClass.C2, CostClass.C3}
        event = IOEvent(
            ordinal=len(self._io_events) + 1,
            operation=operation,
            byte_count=byte_count,
            object_id=object_id,
            rewrite_of=rewrite_of,
            source_id=self.cell.source_id,
            source_sha256=self.cell.source_sha256,
            candidate_id=self.cell.candidate_id,
            phase_id=ctx.phase_id,
            process_token=ctx.process_token,
            cost_class=ctx.cost_class.value,
            lifecycle_action_id=ctx.lifecycle_action_id,
            evidence_ref=ctx.evidence_ref,
            charged_to_candidate=charged,
        )
        self._io_events.append(event)
        return event

    def seal_lifecycle_rewrite_bytes(
        self,
        metric_name: str,
        ctx: ObservationContext,
    ) -> MetricRecord:
        """Seal a lifecycle rewrite metric from the exact bound WRITE event subset."""
        if metric_name not in {
            "source_release_invalidation_bytes_rewritten",
            "semantic_authority_invalidation_bytes_rewritten",
        }:
            raise TelemetryContractError("unsupported lifecycle rewrite metric")
        self._validate_context(ctx)
        if ctx.lifecycle_action_id is None:
            raise TelemetryContractError("lifecycle rewrite metric requires action id")
        value = sum(
            event.byte_count
            for event in self._io_events
            if event.charged_to_candidate
            and event.operation == "WRITE"
            and event.rewrite_of is not None
            and event.lifecycle_action_id == ctx.lifecycle_action_id
        )
        return self._write(
            metric_name,
            ctx,
            state=MetricState.MEASURED,
            value=value,
            evidence_kind="OBSERVED_LIFECYCLE_REWRITE_EVENT_ACCOUNTING_COMPLETE",
            internal=True,
        )

    def seal_io_accounting(self, ctx: ObservationContext) -> None:
        self._validate_context(ctx)
        if self._io_sealed:
            raise TelemetryContractError("I/O accounting already sealed")
        self._io_sealed = True
        included = [e for e in self._io_events if e.charged_to_candidate]
        bytes_read = sum(e.byte_count for e in included if e.operation == "READ")
        writes = [e for e in included if e.operation == "WRITE"]
        bytes_written = sum(e.byte_count for e in writes)
        bytes_rewritten = sum(e.byte_count for e in writes if e.rewrite_of is not None)
        for name, value in (
            ("bytes_read", bytes_read),
            ("bytes_written", bytes_written),
            ("bytes_rewritten", bytes_rewritten),
        ):
            self._write(
                name, ctx, state=MetricState.MEASURED, value=value,
                evidence_kind="OBSERVED_IO_EVENT_ACCOUNTING_COMPLETE",
                internal=True,
            )

    # ---------- scratch high-water ----------

    def observe_scratch_size(
        self,
        ctx: ObservationContext,
        *,
        object_id: str,
        current_size_bytes: int,
    ) -> None:
        self._validate_context(ctx)
        if self._scratch_sealed:
            raise TelemetryContractError("scratch high-water accounting already sealed")
        if ctx.cost_class not in {CostClass.C2, CostClass.C3}:
            raise TelemetryContractError("scratch state must be candidate-owned C2/C3")
        if not object_id or not isinstance(current_size_bytes, int) or current_size_bytes < 0:
            raise TelemetryContractError("scratch observation requires object id and non-negative size")
        self._scratch_observed = True
        self._scratch_sizes[object_id] = current_size_bytes
        self._update_scratch_peaks()

    def observe_scratch_remove(self, ctx: ObservationContext, *, object_id: str) -> None:
        self._validate_context(ctx)
        if self._scratch_sealed:
            raise TelemetryContractError("scratch high-water accounting already sealed")
        self._scratch_observed = True
        self._scratch_sizes.pop(object_id, None)
        self._update_scratch_peaks()

    def _update_scratch_peaks(self) -> None:
        current_bytes = sum(self._scratch_sizes.values())
        current_files = len(self._scratch_sizes)
        self._scratch_peak_bytes = max(self._scratch_peak_bytes, current_bytes)
        self._scratch_peak_files = max(self._scratch_peak_files, current_files)

    def observe_empty_scratch_baseline(self, ctx: ObservationContext) -> None:
        """Record an observed empty scratch state without inventing a file object."""
        self._validate_context(ctx)
        if self._scratch_sealed:
            raise TelemetryContractError("scratch high-water accounting already sealed")
        if ctx.cost_class not in {CostClass.C2, CostClass.C3}:
            raise TelemetryContractError("scratch state must be candidate-owned C2/C3")
        self._scratch_observed = True
        self._update_scratch_peaks()

    def seal_scratch_accounting(self, ctx: ObservationContext) -> None:
        self._validate_context(ctx)
        if self._scratch_sealed:
            raise TelemetryContractError("scratch accounting already sealed")
        if not self._scratch_observed:
            raise TelemetryContractError(
                "endpoint directory size cannot establish scratch peak without high-water observations"
            )
        self._scratch_sealed = True
        self._write(
            "peak_scratch_bytes", ctx, state=MetricState.MEASURED,
            value=self._scratch_peak_bytes,
            evidence_kind="SCRATCH_HIGH_WATER_EVENT_ACCOUNTING",
            internal=True,
        )
        self._write(
            "peak_scratch_file_count", ctx, state=MetricState.MEASURED,
            value=self._scratch_peak_files,
            evidence_kind="SCRATCH_HIGH_WATER_EVENT_ACCOUNTING",
            internal=True,
        )

    # ---------- receipt ----------

    def _candidate_metric(self, name: str) -> Optional[MetricRecord]:
        key = (name, self.cell.source_id, self.cell.source_sha256, self.cell.candidate_id)
        return self._metrics.get(key)

    def _missing_record(self, definition: MetricDefinition) -> Mapping[str, Any]:
        return MetricRecord(
            name=definition.name,
            state=MetricState.MEASUREMENT_NOT_CAPTURED,
            value=None,
            unit=definition.unit,
            source_id=self.cell.source_id,
            source_sha256=self.cell.source_sha256,
            candidate_id=self.cell.candidate_id,
            phase_id=UNREACHED_PHASE,
            process_token="__NO_QUALIFYING_OBSERVATION__",
            cost_class="UNASSIGNED__NO_QUALIFYING_OBSERVATION",
            lifecycle_action_id=None,
            evidence_kind="TYPED_NULL::NO_QUALIFYING_OBSERVATION",
            evidence_ref=None,
        ).as_dict()

    def receipt(self, *, candidate_semantic_state: str) -> Mapping[str, Any]:
        """Return telemetry evidence without altering semantic qualification."""
        if not isinstance(candidate_semantic_state, str) or not candidate_semantic_state.strip():
            raise TelemetryContractError("candidate_semantic_state must be supplied by semantic court")
        metrics: Dict[str, Any] = {}
        for name, definition in sorted(METRIC_DEFINITIONS.items()):
            if definition.grain == MetricGrain.CANDIDATE:
                rec = self._candidate_metric(name)
                metrics[name] = rec.as_dict() if rec else self._missing_record(definition)
            else:
                rows = [
                    rec.as_dict()
                    for key, rec in self._metrics.items()
                    if key[0] == name
                ]
                metrics[name] = rows if rows else [self._missing_record(definition)]
        measured = 0
        missing = 0
        for value in metrics.values():
            rows = value if isinstance(value, list) else [value]
            for row in rows:
                measured += int(row["state"] == MetricState.MEASURED.value)
                missing += int(row["state"] == MetricState.MEASUREMENT_NOT_CAPTURED.value)
        return {
            "schema": CONTRACT_ID,
            "metric_definition_hash": METRIC_DEFINITION_HASH,
            "metric_definitions": metric_definition_manifest(),
            "cell": asdict(self.cell),
            "candidate_semantic_state": candidate_semantic_state,
            "semantic_state_was_modified_by_telemetry": False,
            "telemetry_summary": {
                "measured_records": measured,
                "measurement_not_captured_records": missing,
                "io_event_stream_sealed": self._io_sealed,
                "scratch_high_water_sealed": self._scratch_sealed,
                "process_metrics_sealed": self._candidate_metric("cpu_user_ns") is not None,
            },
            "metrics": metrics,
            "phase_cpu": [
                rec.as_dict() for _, rec in sorted(self._phase_cpu.items())
            ],
            "process_envelopes": [
                {
                    **asdict(rec),
                    "cell": asdict(rec.cell),
                    "cpu_user_delta_ns": rec.cpu_user_stop_ns - rec.cpu_user_start_ns,
                    "cpu_system_delta_ns": rec.cpu_system_stop_ns - rec.cpu_system_start_ns,
                }
                for _, rec in sorted(self._processes.items())
            ],
            "lifecycle_action_receipts": [
                {**asdict(rec), "cell": asdict(rec.cell)}
                for _, rec in sorted(self._lifecycle.items())
            ],
            "io_events": [e.as_dict() for e in self._io_events],
        }


__all__ = [
    "CONTRACT_ID",
    "METRIC_DEFINITION_HASH",
    "METRIC_DEFINITIONS",
    "CANDIDATE_ENVELOPE_PHASE",
    "CellIdentity",
    "ObservationContext",
    "ProcessEnvelopeReceipt",
    "LifecycleActionReceipt",
    "MetricState",
    "CostClass",
    "MetricGrain",
    "TelemetryContractError",
    "TelemetryLedger",
    "metric_definition_manifest",
]
