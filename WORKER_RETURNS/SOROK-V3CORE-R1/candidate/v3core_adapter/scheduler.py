"""Adapted M25 annual scheduler over actual source events.

The immutable 19-step core spine and its derived schedule are loaded from the
historical V3 YAML. Only three steps have admitted adapters:
``event_sampling`` (actual ingress, never sampling), ``capacity_update``
(recorded material accounting) and ``render_layer`` (nonmutating expression).
Every other step is a typed HELD with no durable mutation.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable

from v3.core.config_loader import (
    get_core_step_ids,
    get_derived_schedule,
    get_execution,
    get_extension_policy,
    get_step_list,
    load_step_order,
    load_v3config,
)
from v3.core.state import BackboneState

from .contracts import (
    ANNUAL_STEP_IDS,
    ADMITTED_STEP_IDS,
    AnnualBinding,
    ClockDomain,
    EventDisposition,
    M25_SOURCE_CLOCKS,
    Status,
    StepOutcome,
    YearInput,
    YearRecord,
    YearResult,
)
from .derived_scope import (
    DerivationOutcome,
    derive_scoped,
    material_capacity_index,
)
from .flow_quarantine import run_conserved_charge_flow_probe
from .ledger import HistoricalProjection
from .provenance import canonical_state_hash, digest, record_to_dict, source_hash
from .quarantine import assert_no_forbidden_defaults, ForbiddenDefaultError
from .readiness import HistoricalReadiness
from .render import Renderer, render_readonly
from .transitions import RuleRegistry, default_registry


class SchedulerRefusal(RuntimeError):
    """Raised when the immutable schedule or a transaction invariant is violated."""

    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class StepPlan:
    steps: tuple[dict[str, Any], ...]
    schedule: dict[str, dict[str, Any]]
    execution: dict[str, Any]
    core_ids: tuple[str, ...]


def validate_step_order(step_order: dict[str, Any]) -> StepPlan:
    """Validate the exact 19-step core spine, order and derived schedule."""
    core_ids = tuple(get_core_step_ids(step_order))
    if core_ids != ANNUAL_STEP_IDS:
        raise SchedulerRefusal(
            "CORE_STEP_IDS_MISMATCH",
            f"expected={ANNUAL_STEP_IDS!r} actual={core_ids!r}",
        )
    steps = tuple(get_step_list(step_order))
    ids = [str(step.get("id") or "") for step in steps if step.get("id")]
    if len(ids) != len(set(ids)):
        raise SchedulerRefusal("DUPLICATE_STEP_ID")
    cursor = 0
    for core in core_ids:
        try:
            position = ids.index(core, cursor)
        except ValueError as exc:
            raise SchedulerRefusal(
                "CORE_STEP_ORDER_MUTATED",
                f"missing_or_out_of_order:{core}",
            ) from exc
        cursor = position + 1
    policy = get_extension_policy(step_order)
    core_set = set(core_ids)
    if policy == "append_only":
        last_core = max(ids.index(core) for core in core_ids)
        for position, step_id in enumerate(ids):
            if step_id not in core_set and position <= last_core:
                raise SchedulerRefusal(
                    "EXTENSION_BEFORE_CORE_END",
                    f"{step_id}@{position}",
                )
    schedule = get_derived_schedule(step_order)
    for step in steps:
        step_id = str(step.get("id") or "")
        declared = {str(x) for x in (step.get("derived_compute") or [])}
        scheduled = {
            name
            for name, spec in schedule.items()
            if str((spec or {}).get("compute_after_step") or "") == step_id
        }
        if declared != scheduled:
            raise SchedulerRefusal(
                "DERIVED_SCHEDULE_MISMATCH",
                f"{step_id}:declared={sorted(declared)}:scheduled={sorted(scheduled)}",
            )
    return StepPlan(
        steps=steps,
        schedule=schedule,
        execution=get_execution(step_order),
        core_ids=core_ids,
    )


def load_plan() -> StepPlan:
    return validate_step_order(load_step_order())


def _event_body(event) -> dict[str, Any]:
    return {
        "event_id": event.event_id,
        "actor_id": event.actor_id,
        "world_id": event.world_id,
        "kind": event.kind,
        "location": event.location,
        "source_clock_domain": event.source_clock_domain.value,
        "source_clock": event.source_clock,
        "body": dict(event.body),
        "owner_receipt_hash": event.owner_receipt_hash,
        "source_owned": event.source_owned,
        "source_fact_hash": source_hash(
            {
                "event_id": event.event_id,
                "actor_id": event.actor_id,
                "kind": event.kind,
                "source_clock_domain": event.source_clock_domain.value,
                "source_clock": event.source_clock,
                "body": dict(event.body),
                "owner_receipt_hash": event.owner_receipt_hash,
            }
        ),
    }


def _find_access(year_input: YearInput, event_id: str, actor_id: str):
    for access in year_input.accesses:
        if access.event_id == event_id and access.actor_id == actor_id:
            return access
    return None


def _find_response(year_input: YearInput, event_id: str, actor_id: str):
    for response in year_input.responses:
        if response.event_id == event_id and response.actor_id == actor_id:
            return response
    return None


def _find_binding(year_input: YearInput, event_id: str) -> AnnualBinding | None:
    for binding in year_input.bindings:
        if binding.event_id == event_id:
            return binding
    return None


def _held(
    event_id: str,
    status: Status,
    reason: str,
    *,
    details: dict[str, Any] | None = None,
) -> EventDisposition:
    return EventDisposition(
        event_id=event_id,
        status=status,
        reason=reason,
        details=details or {},
    )


def _admit_events(
    projection: HistoricalProjection,
    year_input: YearInput,
    registry: RuleRegistry,
) -> tuple[list[EventDisposition], list[tuple[Any, Any, Any]]]:
    dispositions: list[EventDisposition] = []
    admitted: list[tuple[Any, Any, Any]] = []
    prior = year_input.prior_snapshot or projection.prior_snapshot
    post = year_input.post_snapshot
    for event in year_input.events:
        binding = _find_binding(year_input, event.event_id)
        if binding is None:
            dispositions.append(
                _held(event.event_id, Status.HELD_CLOCK_BINDING_MISMATCH, "no_annual_binding")
            )
            continue
        if event.actor_id != projection.actor_id:
            dispositions.append(
                _held(event.event_id, Status.HELD_FOREIGN_ACTOR, f"actor={event.actor_id}")
            )
            continue
        if event.source_clock_domain not in M25_SOURCE_CLOCKS:
            dispositions.append(
                _held(
                    event.event_id,
                    Status.HELD_CLOCK_MISMATCH,
                    f"source_clock_domain={event.source_clock_domain.value}",
                )
            )
            continue
        if binding.schedule_clock_domain != ClockDomain.V3_M25_ANNUAL:
            dispositions.append(
                _held(
                    event.event_id,
                    Status.HELD_CLOCK_MISMATCH,
                    f"binding_clock={binding.schedule_clock_domain.value}",
                )
            )
            continue
        if binding.annual_year != year_input.annual_year:
            dispositions.append(
                _held(
                    event.event_id,
                    Status.HELD_CLOCK_BINDING_MISMATCH,
                    f"binding_year={binding.annual_year} annual_year={year_input.annual_year}",
                )
            )
            continue
        if projection.is_applied(event.event_id):
            dispositions.append(
                _held(event.event_id, Status.HELD_DUPLICATE_EVENT, "already_applied")
            )
            continue
        access = _find_access(year_input, event.event_id, projection.actor_id)
        if access is None or not access.perceived:
            dispositions.append(
                _held(event.event_id, Status.HELD_MISSING_PERCEPTION, "no_perception_record")
            )
            continue
        if (
            access.source_clock != event.source_clock
            or access.source_clock_domain != event.source_clock_domain
        ):
            dispositions.append(
                _held(
                    event.event_id,
                    Status.HELD_CLOCK_MISMATCH,
                    "access_clock_differs_from_event",
                )
            )
            continue
        response = _find_response(year_input, event.event_id, projection.actor_id)
        if response is None:
            dispositions.append(
                _held(event.event_id, Status.HELD_MISSING_RESPONSE, "no_response_record")
            )
            continue
        if not response.performed:
            dispositions.append(
                _held(event.event_id, Status.HELD_MISSING_RESPONSE, "response_not_performed")
            )
            continue
        if (
            response.source_clock != event.source_clock
            or response.source_clock_domain != event.source_clock_domain
        ):
            dispositions.append(
                _held(
                    event.event_id,
                    Status.HELD_CLOCK_MISMATCH,
                    "response_clock_differs_from_event",
                )
            )
            continue
        rule = registry.lookup(event, response)
        if rule is None:
            dispositions.append(
                _held(event.event_id, Status.HELD_MISSING_RULE, "no_competent_transition_rule")
            )
            continue
        if rule.spec.scientific and not rule.spec.issued:
            dispositions.append(
                EventDisposition(
                    event_id=event.event_id,
                    status=Status.HELD_RULE_NOT_ISSUED,
                    reason=rule.spec.authority,
                    rule_id=rule.spec.rule_id,
                )
            )
            continue
        result = rule.evaluate(event, response, projection.state, prior, post)
        disposition = EventDisposition(
            event_id=event.event_id,
            status=result.status,
            reason=result.reason,
            rule_id=rule.spec.rule_id,
            source_fact_hash=source_hash(dict(event.body)),
            durable_mutation=result.status == Status.APPLIED_TEST_ONLY_SOURCEFREE,
            details={
                **dict(result.details),
                "event_kind": event.kind,
                "response_kind": response.kind,
            },
        )
        dispositions.append(disposition)
        if result.status in {Status.APPLIED_TEST_ONLY_SOURCEFREE, Status.NO_CHANGE_EVALUATED}:
            admitted.append((event, response, result))
    return dispositions, admitted


def _ensure_bound_events_present(year_input: YearInput) -> tuple[EventDisposition, ...]:
    event_ids = {event.event_id for event in year_input.events}
    held: list[EventDisposition] = []
    for binding in year_input.bindings:
        if binding.event_id not in event_ids:
            held.append(
                EventDisposition(
                    event_id=binding.event_id,
                    status=Status.HELD_SOURCE_EVENT_WITHDRAWN,
                    reason="binding_references_missing_source_event",
                )
            )
    return tuple(held)


def _apply_deltas(
    state: BackboneState,
    admitted: Iterable[tuple[Any, Any, Any]],
) -> tuple[list, dict[str, Any], list[dict[str, Any]]]:
    deltas: list = []
    facts: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    for event, response, result in admitted:
        for delta in result.material_deltas:
            field = delta.field.split(".")[-1]
            setattr(state.capacity, field, delta.after)
            deltas.append(delta)
            trace.append(record_to_dict(delta))
        facts.update(dict(result.material_facts))
    return deltas, facts, trace


def _result(
    *,
    status: Status,
    committed: bool,
    projection: HistoricalProjection,
    dispositions: list[EventDisposition],
    step_outcomes: list[StepOutcome],
    before_hash: str,
    after_hash: str,
    before_index: float,
    after_index: float,
    readiness: str,
    reason: str = "",
    year_record: YearRecord | None = None,
) -> YearResult:
    return YearResult(
        status=status,
        committed=committed,
        year_record=year_record,
        dispositions=tuple(dispositions),
        step_outcomes=tuple(step_outcomes),
        state_before_hash=before_hash,
        state_after_hash=after_hash,
        material_index_before=before_index,
        material_index_after=after_index,
        readiness=readiness,
        reason=reason,
    )


def run_year(
    projection: HistoricalProjection,
    year_input: YearInput,
    *,
    registry: RuleRegistry | None = None,
    renderer: Renderer | None = None,
    config: dict[str, Any] | None = None,
    plan: StepPlan | None = None,
    ledger_path: str | None = None,
    allow_pressure_flow_probe: bool = False,
) -> YearResult:
    """Attempt one M25 annual year over actual source records."""
    if year_input.schedule_clock_domain != ClockDomain.V3_M25_ANNUAL:
        return _result(
            status=Status.HELD_CLOCK_MISMATCH,
            committed=False,
            projection=projection,
            dispositions=[],
            step_outcomes=[],
            before_hash=projection.state_hash(),
            after_hash=projection.state_hash(),
            before_index=material_capacity_index(projection.state),
            after_index=material_capacity_index(projection.state),
            readiness="BLOCKED",
            reason="schedule_clock_domain_is_not_M25",
        )
    plan = plan or load_plan()
    registry = registry or default_registry()
    config = load_v3config() if config is None else config
    before_hash = projection.state_hash()
    before_index = material_capacity_index(projection.state)
    missing_bindings = _ensure_bound_events_present(year_input)
    if missing_bindings:
        return _result(
            status=Status.HELD_SOURCE_EVENT_WITHDRAWN,
            committed=False,
            projection=projection,
            dispositions=list(missing_bindings),
            step_outcomes=[],
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason="source_event_removed_no_fabricated_year_event",
        )
    if not year_input.events and not year_input.allow_empty_year:
        return _result(
            status=Status.HELD_NO_EVENT_SOURCE,
            committed=False,
            projection=projection,
            dispositions=[],
            step_outcomes=[],
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason="no_source_event_and_empty_year_not_admitted",
        )
    dispositions, admitted = _admit_events(projection, year_input, registry)
    if not admitted and not year_input.allow_empty_year:
        terminal = dispositions[0].status if dispositions else Status.HELD_NO_ADMITTED_EVENT
        return _result(
            status=terminal,
            committed=False,
            projection=projection,
            dispositions=dispositions,
            step_outcomes=[],
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason="no_admitted_actual_event_no_annual_developmental_occurrence",
        )
    working = deepcopy(projection.state)
    if year_input.age is not None:
        working.age = int(year_input.age)
    step_outcomes: list[StepOutcome] = []
    deltas: list = []
    facts: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    derivation: DerivationOutcome = derive_scoped(working)
    if derivation.live_state_mutated:
        return _result(
            status=Status.HELD_DERIVED_MUTATION,
            committed=False,
            projection=projection,
            dispositions=dispositions,
            step_outcomes=[],
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason="derived_computation_mutated_live_state",
        )
    try:
        for step in plan.steps:
            step_id = str(step.get("id") or "")
            if not step_id:
                continue
            step_status = Status.HELD_MISSING_ISSUED_RULE
            details: dict[str, Any] = {"admitted": False}
            if step_id == "event_sampling":
                if admitted:
                    working.events_this_year = [_event_body(item[0]) for item in admitted]
                    working.micro_trace_this_year = []
                    step_status = Status.APPLIED_TEST_ONLY_SOURCEFREE
                    details = {"admitted_event_ids": [item[0].event_id for item in admitted], "sampled": False}
                elif year_input.allow_empty_year:
                    working.events_this_year = []
                    working.micro_trace_this_year = []
                    step_status = Status.HELD_NO_EVENT_SOURCE
                    details = {"explicit_empty_year": True, "sampled": False}
                else:
                    step_status = Status.HELD_NO_ADMITTED_EVENT
                    details = {"sampled": False}
            elif step_id == "capacity_update":
                if any(item[2].material_deltas for item in admitted):
                    deltas, facts, trace = _apply_deltas(working, admitted)
                    working.micro_trace_this_year = list(trace)
                    working.yearly_integrity["material_accounting"] = {
                        "status": "clean",
                        "deltas": list(trace),
                        "source_event_ids": [delta.event_id for delta in deltas],
                        "authority": "TEST_ONLY_MATERIAL_ACCOUNTING_POLICY",
                    }
                    step_status = Status.APPLIED_TEST_ONLY_SOURCEFREE
                    details = {"delta_count": len(deltas)}
                elif admitted:
                    step_status = Status.NO_CHANGE_EVALUATED
                    details = {"delta_count": 0}
                elif year_input.allow_empty_year:
                    step_status = Status.HELD_NO_EVENT_SOURCE
                    details = {"explicit_empty_year": True}
                else:
                    step_status = Status.HELD_NO_ADMITTED_EVENT
            elif step_id == "render_layer":
                outcome = render_readonly(
                    working,
                    derivation.published,
                    renderer=renderer,
                    config=config,
                )
                step_status = outcome.status
                details = {
                    "backbone_hash_before": outcome.backbone_hash_before,
                    "backbone_hash_after": outcome.backbone_hash_after,
                    "reason": outcome.reason,
                }
                if outcome.status in {Status.HELD_RENDERER_MUTATION, Status.HELD_TRANSACTION_ABORTED}:
                    step_outcomes.append(StepOutcome(step_id, step_status, details=details))
                    return _result(
                        status=outcome.status,
                        committed=False,
                        projection=projection,
                        dispositions=dispositions,
                        step_outcomes=step_outcomes,
                        before_hash=before_hash,
                        after_hash=before_hash,
                        before_index=before_index,
                        after_index=before_index,
                        readiness="BLOCKED",
                        reason=outcome.reason,
                    )
            else:
                details = {"admitted": False, "reason": "no_issued_transition_rule"}
            step_outcomes.append(StepOutcome(step_id, step_status, details=details))
            declared = {str(x) for x in (step.get("derived_compute") or [])}
            if declared:
                expected = {
                    name
                    for name, spec in plan.schedule.items()
                    if str((spec or {}).get("compute_after_step") or "") == step_id
                }
                if declared != expected:
                    raise SchedulerRefusal("DERIVED_SCHEDULE_MISMATCH", step_id)
                derivation = derive_scoped(working)
                if derivation.live_state_mutated:
                    return _result(
                        status=Status.HELD_DERIVED_MUTATION,
                        committed=False,
                        projection=projection,
                        dispositions=dispositions,
                        step_outcomes=step_outcomes,
                        before_hash=before_hash,
                        after_hash=before_hash,
                        before_index=before_index,
                        after_index=before_index,
                        readiness="BLOCKED",
                        reason="derived_computation_mutated_live_state",
                    )
        if allow_pressure_flow_probe:
            probe = run_conserved_charge_flow_probe(working, explicitly_enabled=True)
            step_outcomes.append(
                StepOutcome(
                    "post_year_pressure_flow",
                    probe.status,
                    details={
                        "test_only_conserved_charge_model": True,
                        "live_state_mutated": probe.live_state_mutated,
                    },
                )
            )
        else:
            step_outcomes.append(
                StepOutcome(
                    "post_year_pressure_flow",
                    Status.HELD_CONSERVED_CHARGE_MODEL,
                    details={"conserved_charge_assumed": False},
                )
            )
        assert_no_forbidden_defaults(working)
        if year_input.age is not None:
            working.age += 1
        working.year += 1
        after_hash = canonical_state_hash(working)
        after_index = material_capacity_index(working)
        readiness = HistoricalReadiness()
        verdict = readiness.from_outcomes(dispositions, step_outcomes)
        if verdict["overall_status"] == "blocked":
            return _result(
                status=Status.BLOCKED_AUTHORITY,
                committed=False,
                projection=projection,
                dispositions=dispositions,
                step_outcomes=step_outcomes,
                before_hash=before_hash,
                after_hash=before_hash,
                before_index=before_index,
                after_index=before_index,
                readiness=verdict["readiness"],
                reason="generation_blocked",
            )
        record = YearRecord(
            schema="SOROK_V3CORE_R1_YEAR_RECORD@1",
            annual_year=year_input.annual_year,
            age=year_input.age,
            schedule_clock_domain=year_input.schedule_clock_domain,
            source_event_ids=tuple(item[0].event_id for item in admitted),
            state_before_hash=before_hash,
            state_after_hash=after_hash,
            derived_diagnostic_hash=derivation.diagnostic_hash,
            published_material_index_before=before_index,
            published_material_index_after=after_index,
            material_deltas=tuple(deltas),
            step_outcomes=tuple(step_outcomes),
            event_dispositions=tuple(dispositions),
            generation_status=str(verdict["overall_status"]),
            readiness=str(verdict["readiness"]),
        )
        old_state = projection.state
        old_years = list(projection.years)
        old_facts = dict(projection.material_facts)
        old_applied = list(projection.applied_event_ids)
        projection.state = working
        projection.years.append(record)
        projection.material_facts.update(facts)
        projection.applied_event_ids.extend(
            [item[0].event_id for item in admitted if item[2].status == Status.APPLIED_TEST_ONLY_SOURCEFREE]
        )
        if ledger_path:
            try:
                projection.save(ledger_path)
            except Exception:
                projection.state = old_state
                projection.years = old_years
                projection.material_facts = old_facts
                projection.applied_event_ids = old_applied
                return _result(
                    status=Status.HELD_TRANSACTION_ABORTED,
                    committed=False,
                    projection=projection,
                    dispositions=dispositions,
                    step_outcomes=step_outcomes,
                    before_hash=before_hash,
                    after_hash=before_hash,
                    before_index=before_index,
                    after_index=before_index,
                    readiness="BLOCKED",
                    reason="ledger_commit_failed",
                )
        overall_status = (
            Status.APPLIED_TEST_ONLY_SOURCEFREE
            if any(item[2].status == Status.APPLIED_TEST_ONLY_SOURCEFREE for item in admitted)
            else Status.NO_CHANGE_EVALUATED
        )
        return _result(
            status=overall_status,
            committed=True,
            projection=projection,
            dispositions=dispositions,
            step_outcomes=step_outcomes,
            before_hash=before_hash,
            after_hash=after_hash,
            before_index=before_index,
            after_index=after_index,
            readiness=str(verdict["readiness"]),
            year_record=record,
        )
    except ForbiddenDefaultError as exc:
        return _result(
            status=Status.HELD_FORBIDDEN_DEFAULT,
            committed=False,
            projection=projection,
            dispositions=dispositions,
            step_outcomes=step_outcomes,
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason=";".join(exc.reasons),
        )
    except SchedulerRefusal:
        raise
    except Exception as exc:
        return _result(
            status=Status.HELD_TRANSACTION_ABORTED,
            committed=False,
            projection=projection,
            dispositions=dispositions,
            step_outcomes=step_outcomes,
            before_hash=before_hash,
            after_hash=before_hash,
            before_index=before_index,
            after_index=before_index,
            readiness="BLOCKED",
            reason=f"{type(exc).__name__}:{exc}",
        )
