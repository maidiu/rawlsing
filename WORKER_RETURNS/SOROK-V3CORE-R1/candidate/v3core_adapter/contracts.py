"""Typed records for the source-free historical-development adapter.

The adapter consumes actual actor-world event, access and response records. It
does not accept an event without an explicit source clock, provenance, bound
annual year, actor perception and performed response.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ClockDomain(str, Enum):
    """Clock domains that must never be collapsed into one numeric timeline."""

    CURRENT_C12_ACTOR_WORLD = "CURRENT_C12_ACTOR_WORLD_CLOCK"
    SOROK_NEO_N11_EVENT = "SOROK_NEO_N11_EVENT_RECURSION"
    PYAT_N11_OBJECTIVE_WORLD = "PYAT_N11_OBJECTIVE_WORLD_ACCEPTANCE"
    V3_M25_ANNUAL = "V3_M25_ANNUAL_SCHEDULE"


M25_SOURCE_CLOCKS = frozenset({ClockDomain.CURRENT_C12_ACTOR_WORLD})
FOREIGN_RECURSION_CLOCKS = frozenset(
    {ClockDomain.SOROK_NEO_N11_EVENT, ClockDomain.PYAT_N11_OBJECTIVE_WORLD}
)


class Status(str, Enum):
    """Terminal dispositions. A held state is distinct from an evaluated no-change."""

    APPLIED_TEST_ONLY_SOURCEFREE = "APPLIED_TEST_ONLY_SOURCEFREE"
    NO_CHANGE_EVALUATED = "NO_CHANGE_EVALUATED"
    DERIVED_EVALUATED_SCOPED = "DERIVED_EVALUATED_SCOPED"
    HELD_MISSING_RULE = "HELD_MISSING_RULE"
    HELD_RULE_NOT_ISSUED = "HELD_RULE_NOT_ISSUED"
    HELD_MISSING_PERCEPTION = "HELD_MISSING_PERCEPTION"
    HELD_MISSING_RESPONSE = "HELD_MISSING_RESPONSE"
    HELD_FOREIGN_ACTOR = "HELD_FOREIGN_ACTOR"
    HELD_CLOCK_MISMATCH = "HELD_CLOCK_MISMATCH"
    HELD_CLOCK_BINDING_MISMATCH = "HELD_CLOCK_BINDING_MISMATCH"
    HELD_SOURCE_EVENT_WITHDRAWN = "HELD_SOURCE_EVENT_WITHDRAWN"
    HELD_DUPLICATE_EVENT = "HELD_DUPLICATE_EVENT"
    HELD_ACCOUNTING_MISMATCH = "HELD_ACCOUNTING_MISMATCH"
    HELD_FORBIDDEN_DEFAULT = "HELD_FORBIDDEN_DEFAULT"
    HELD_RENDERER_MUTATION = "HELD_RENDERER_MUTATION"
    HELD_DERIVED_MUTATION = "HELD_DERIVED_MUTATION"
    HELD_TRANSACTION_ABORTED = "HELD_TRANSACTION_ABORTED"
    HELD_NO_EVENT_SOURCE = "HELD_NO_EVENT_SOURCE"
    HELD_NO_ADMITTED_EVENT = "HELD_NO_ADMITTED_EVENT"
    HELD_MISSING_ISSUED_RULE = "HELD_MISSING_ISSUED_RULE"
    HELD_CONSERVED_CHARGE_MODEL = "HELD_CONSERVED_CHARGE_MODEL"
    BLOCKED_AUTHORITY = "BLOCKED_AUTHORITY"


ANNUAL_STEP_IDS = (
    "field_update",
    "autonomy_safety_micro_drift",
    "event_sampling",
    "reproduction_constraints_update",
    "capacity_update",
    "health_drift_update",
    "buffers_update",
    "frameworks_update",
    "domains_update",
    "cracks_and_alienation_update",
    "plasticity_and_metabolization_update",
    "stability_inertia_dissipation",
    "striving_update",
    "practice_and_infrastructure_update",
    "topology_and_boundary_update",
    "attention_and_capture_update",
    "strategy_and_signal_effects",
    "style_trait_drift",
    "render_layer",
)

ADMITTED_STEP_IDS = frozenset({"event_sampling", "capacity_update", "render_layer"})


@dataclass(frozen=True)
class Provenance:
    """Origin of one source record. The adapter never fabricates missing fields."""

    source_system: str
    source_ref: str
    source_commit: str
    source_branch: str
    source_path: str
    source_sha256: str
    source_record_id: str
    captured_by: str
    captured_at: str
    native: bool = False
    authority: str = "TEST_ONLY_SOURCEFREE"

    def required_fields(self) -> dict[str, str]:
        return {
            "source_system": self.source_system,
            "source_ref": self.source_ref,
            "source_commit": self.source_commit,
            "source_branch": self.source_branch,
            "source_path": self.source_path,
            "source_sha256": self.source_sha256,
            "source_record_id": self.source_record_id,
            "captured_by": self.captured_by,
            "captured_at": self.captured_at,
        }

    def missing(self) -> tuple[str, ...]:
        return tuple(k for k, v in self.required_fields().items() if not str(v).strip())


@dataclass(frozen=True)
class ActorWorldEvent:
    """One actual world event. ``source_clock`` belongs to its own domain."""

    event_id: str
    actor_id: str
    world_id: str
    kind: str
    location: str
    source_clock_domain: ClockDomain
    source_clock: int
    body: Mapping[str, Any]
    provenance: Provenance
    owner_receipt_hash: str | None = None
    source_owned: bool = False


@dataclass(frozen=True)
class ActorAccess:
    """One actor's actual perception/access record for an event."""

    event_id: str
    actor_id: str
    channel: str
    perceived: bool
    source_clock_domain: ClockDomain
    source_clock: int
    provenance: Provenance


@dataclass(frozen=True)
class ActorResponse:
    """One actor's actually performed response record for an event."""

    event_id: str
    actor_id: str
    kind: str
    performed: bool
    body: Mapping[str, Any]
    source_clock_domain: ClockDomain
    source_clock: int
    provenance: Provenance


@dataclass(frozen=True)
class AnnualBinding:
    """An explicit caller binding from an event to an M25 annual year.

    The binding is provenance, not a numeric conversion between clocks.
    """

    event_id: str
    schedule_clock_domain: ClockDomain
    annual_year: int
    bound_by: str
    provenance: Provenance


@dataclass(frozen=True)
class YearInput:
    """One M25 year request over actual source records."""

    annual_year: int
    schedule_clock_domain: ClockDomain
    events: tuple[ActorWorldEvent, ...] = ()
    accesses: tuple[ActorAccess, ...] = ()
    responses: tuple[ActorResponse, ...] = ()
    bindings: tuple[AnnualBinding, ...] = ()
    allow_empty_year: bool = False
    age: int | None = None
    age_provenance: Provenance | None = None
    prior_snapshot: SourceActorSnapshot | None = None
    post_snapshot: SourceActorSnapshot | None = None


@dataclass(frozen=True)
class SourceActorSnapshot:
    """Actual material facts read from the continuing-person consumer."""

    actor_id: str
    world_id: str
    source_clock_domain: ClockDomain
    source_clock: int
    position: str
    cash: float
    material_remaining: float
    free_hours: float
    completed_units: float
    skill: float
    debt_units: float
    tools_remaining: float
    projects: tuple[str, ...]
    provenance: Provenance


@dataclass(frozen=True)
class EventDisposition:
    """Admission result for one event. ``durable_mutation`` is factual, not inferred."""

    event_id: str
    status: Status
    reason: str
    rule_id: str = ""
    source_fact_hash: str = ""
    durable_mutation: bool = False
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepOutcome:
    """Execution result for one scheduled step."""

    step_id: str
    status: Status
    rule_id: str = ""
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MaterialDelta:
    """One applied material accounting delta with exact source provenance."""

    event_id: str
    field: str
    before: float
    delta: float
    after: float
    source_fact_hash: str
    authority: str = "TEST_ONLY_MATERIAL_ACCOUNTING_POLICY"


@dataclass(frozen=True)
class YearRecord:
    """Durable historical year record adapted from the V3 YearRecord snapshot.

    Derived output is recorded separately from stored state and is never written
    back into ``BackboneState`` by the adapter.
    """

    schema: str
    annual_year: int
    age: int | None
    schedule_clock_domain: ClockDomain
    source_event_ids: tuple[str, ...]
    state_before_hash: str
    state_after_hash: str
    derived_diagnostic_hash: str
    published_material_index_before: float
    published_material_index_after: float
    material_deltas: tuple[MaterialDelta, ...]
    step_outcomes: tuple[StepOutcome, ...]
    event_dispositions: tuple[EventDisposition, ...]
    generation_status: str
    readiness: str
    authority: str = "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE"
    canonical_c9_claimed: bool = False


@dataclass(frozen=True)
class YearResult:
    """Outcome of one M25 year commit attempt."""

    status: Status
    committed: bool
    year_record: YearRecord | None
    dispositions: tuple[EventDisposition, ...]
    step_outcomes: tuple[StepOutcome, ...]
    state_before_hash: str
    state_after_hash: str
    material_index_before: float
    material_index_after: float
    readiness: str
    reason: str = ""
    authority: str = "TEST_ONLY_SOURCEFREE_NO_SCIENCE_ISSUANCE"
