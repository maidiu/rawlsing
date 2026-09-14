"""Production PRE553 integration for the source-state -> product-target contract.

The adapter is intentionally source agnostic.  It binds the generic contract to
existing exact PRE553 authority/query/C11 seams, performs the denominator gate
before calling the ordinary empirical-result producer, and never contains a
native-code/source-family semantic table.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_positive_authority,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    ExactRef,
    RespondentEvent,
    canonicalize,
    semantic_hash,
)
from rawlsing_next._pre553_query_common import (
    SOURCE_SCOPE_MODES,
    _authority,
    _canonical_authorities,
    _canonical_refs,
    _exact,
    _parse_target_plan,
    _profile,
)
from rawlsing_next._pre553_query_predicate import (
    _compile_derived_branch_memberships,
    _eval_predicate,
    _validate_public_object_authorities,
)
from rawlsing_next._pre553_query_eval import (
    _carrier_topology_kind,
    _event_matches_target,
    _risk_membership,
    _routing_fact_for,
    _topology_compatible,
)
from rawlsing_next.pre553_empirical_query import (
    QueryExecutionResult,
    _require_exact_i03_authority_fitness,
    _resolve_release_indices,
    _verify_public_identity,
    execute_empirical_query,
)
from rawlsing_next.source_state_target_disposition_contract import (
    AUTHORITY_PHASE,
    RESOLVED_NON_TARGET,
    TARGET_MEMBER,
    ContractExecutionReceipt,
    SourceStateDispositionContractError,
    audit_observation,
    authority_binding_for_universe,
    build_record_audit,
    canonical_json as contract_canonical_json,
    component_for_target,
    contract_hash,
    denominator_resolution_check,
    empirical_result_receipt,
    normalize_contract,
    replay_identity,
    unresolved_observation,
)

PRODUCTION_ADAPTER_ID = "PRE553_SOURCE_STATE_TARGET_DISPOSITION_ADAPTER@1.0.0"
CONTRACT_GRAIN_KEY = "source_state_target_disposition_contract"


class Pre553SourceStateDispositionError(SourceStateDispositionContractError):
    """Exact PRE553 binding or source-state disposition cannot be established."""


@dataclass(frozen=True)
class SourceStateTargetDispositionExecution:
    """Governed result envelope around the ordinary PRE553 query result."""

    query_result: QueryExecutionResult
    contract_receipt: ContractExecutionReceipt

    @property
    def replay_identity(self) -> str:
        return self.contract_receipt.replay_identity


@dataclass(frozen=True)
class _BoundComponent:
    target_ref: ExactRef
    target_domain_ref: ExactRef
    contract_component: Mapping[str, Any]


@dataclass(frozen=True)
class _BoundContract:
    normalized: Mapping[str, Any]
    components: tuple[_BoundComponent, ...]


def _contract_from_query(query: EmpiricalQuerySpec) -> Mapping[str, Any]:
    grain = query.requested_output_grain
    if not isinstance(grain, Mapping):
        raise Pre553SourceStateDispositionError("requested_output_grain must be an exact mapping")
    raw = grain.get(CONTRACT_GRAIN_KEY)
    if raw is None:
        raise Pre553SourceStateDispositionError(
            f"positive production integration requires requested_output_grain.{CONTRACT_GRAIN_KEY}"
        )
    if not isinstance(raw, Mapping):
        raise Pre553SourceStateDispositionError("source-state contract declaration must be a mapping")
    try:
        return normalize_contract(canonicalize(raw))
    except SourceStateDispositionContractError as exc:
        raise Pre553SourceStateDispositionError(str(exc)) from exc


def _query_universe_refs(query: EmpiricalQuerySpec) -> tuple[ExactRef, ...]:
    return _canonical_refs(
        _exact(value, "query.empirical_universe_refs") for value in query.empirical_universe_refs
    )


def _query_authority_closure(query: EmpiricalQuerySpec) -> tuple[AuthorityRef, ...]:
    return _canonical_authorities(
        _authority(value, "query.authority_snapshot_refs") for value in query.authority_snapshot_refs
    )


def _validate_authority_binding(
    *,
    registry: AuthorityRegistry,
    binding: Mapping[str, Any],
    universe_ref: ExactRef,
    risk_set_ref: ExactRef,
    target_domain_ref: ExactRef,
    query_authority_closure: tuple[AuthorityRef, ...],
    response_semantic_authorities: tuple[AuthorityRef, ...],
) -> None:
    source_ref = _authority(binding["source_semantic_authority_ref"], "source_semantic_authority_ref")
    target_ref = _authority(binding["target_use_authority_ref"], "target_use_authority_ref")
    risk_ref = _authority(binding["risk_set_authority_ref"], "risk_set_authority_ref")
    replay_ref = _authority(binding["replay_authority_ref"], "replay_authority_ref")

    if source_ref not in response_semantic_authorities:
        raise Pre553AuthorityError(
            "source-local semantic authority is not in the exact target response-semantic bundle"
        )
    for ref, name in (
        (target_ref, "target-use"),
        (risk_ref, "risk-set"),
        (replay_ref, "replay"),
    ):
        if ref not in query_authority_closure:
            raise Pre553AuthorityError(f"{name} authority is not in exact query authority closure")
    if target_ref == risk_ref:
        raise Pre553AuthorityError(
            "target-domain authority and denominator/risk-set authority must remain distinct"
        )

    source_snapshot = registry.resolve_exact(source_ref).snapshot
    require_positive_authority(
        source_snapshot,
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        operation=binding["source_semantic_operation"],
        object_family="RespondentEvent@1.0.0",
        source_universe_ref=universe_ref.as_dict(),
    )
    target_snapshot = registry.resolve_exact(target_ref).snapshot
    require_positive_authority(
        target_snapshot,
        authority_kind="TARGET_USE_PERMISSION",
        operation=binding["target_use_operation"],
        object_family="EmpiricalFact@1.0.0",
        source_universe_ref=universe_ref.as_dict(),
        target_use_ref=target_domain_ref.as_dict(),
    )
    risk_snapshot = registry.resolve_exact(risk_ref).snapshot
    require_positive_authority(
        risk_snapshot,
        authority_kind="ROUTING_RISK_SET",
        operation=binding["risk_set_operation"],
        object_family="RoutingEligibilityFact@1.0.0",
        source_universe_ref=universe_ref.as_dict(),
        predicate_or_risk_set_ref=risk_set_ref.as_dict(),
    )
    replay_snapshot = registry.resolve_exact(replay_ref).snapshot
    require_positive_authority(
        replay_snapshot,
        authority_kind="REPLAY_PROTOCOL",
        operation=binding["replay_operation"],
        source_universe_ref=universe_ref.as_dict(),
    )


def _bind_contract(
    *,
    query: EmpiricalQuerySpec,
    authority_registry: AuthorityRegistry,
    plan,
) -> _BoundContract:
    normalized = _contract_from_query(query)
    risk_set_ref = _exact(query.risk_set_ref, "query.risk_set_ref")
    contract_risk_ref = _exact(normalized["risk_set_ref"], "contract.risk_set_ref")
    if contract_risk_ref != risk_set_ref:
        raise Pre553SourceStateDispositionError(
            "contract risk_set_ref must exactly equal query risk_set_ref"
        )
    if normalized["authority_phase"] != AUTHORITY_PHASE:
        raise Pre553SourceStateDispositionError("risk-set authority must be frozen pre-outcome")

    query_universes = _query_universe_refs(query)
    query_universe_keys = {ref.key for ref in query_universes}
    query_closure = _query_authority_closure(query)
    bound: list[_BoundComponent] = []
    if len(normalized["components"]) != plan.arity:
        raise Pre553SourceStateDispositionError(
            "contract component count must exactly equal query target arity"
        )

    for component in plan.components:
        try:
            contract_component = component_for_target(normalized, component.target_ref.as_dict())
        except SourceStateDispositionContractError as exc:
            raise Pre553SourceStateDispositionError(str(exc)) from exc
        target_domain_ref = _exact(
            contract_component["target_domain_ref"], "contract.target_domain_ref"
        )
        if target_domain_ref != component.target_domain_replay_ref:
            raise Pre553SourceStateDispositionError(
                "contract target_domain_ref must equal query target_domain_replay_ref"
            )

        bound_universe_keys: set[str] = set()
        for row in contract_component["authority_bindings"]:
            universe_ref = _exact(row["empirical_universe_ref"], "authority binding universe")
            bound_universe_keys.add(universe_ref.key)
            if universe_ref.key not in query_universe_keys:
                raise Pre553SourceStateDispositionError(
                    "contract authority binding names universe outside exact query scope"
                )
            _validate_authority_binding(
                registry=authority_registry,
                binding=row,
                universe_ref=universe_ref,
                risk_set_ref=risk_set_ref,
                target_domain_ref=target_domain_ref,
                query_authority_closure=query_closure,
                response_semantic_authorities=component.response_semantic_authority_refs,
            )
        if bound_universe_keys != query_universe_keys:
            raise Pre553SourceStateDispositionError(
                "every exact query universe requires one source/risk/target/replay authority binding"
            )

        resolved_states = {
            row["response_state"]
            for row in contract_component["state_bindings"]
            if row["product_target_disposition"] in {TARGET_MEMBER, RESOLVED_NON_TARGET}
        }
        if not resolved_states.issubset(component.included_states):
            raise Pre553SourceStateDispositionError(
                "resolved target-specific source states must be included by query target topology"
            )
        bound.append(_BoundComponent(
            target_ref=component.target_ref,
            target_domain_ref=target_domain_ref,
            contract_component=contract_component,
        ))
    return _BoundContract(normalized=normalized, components=tuple(bound))


def _opaque_raw_state_hash(event: RespondentEvent) -> str:
    # Raw material participates in audit identity only.  It is never a lookup key.
    return semantic_hash({
        "event_ref": event.ref.as_dict(),
        "raw_response_value": event.raw_response_value,
    })


def _preflight_group(
    indices: Sequence[Any],
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    plan,
    profile,
    authority_registry: AuthorityRegistry,
    bound_contract: _BoundContract,
) -> Mapping[str, Any]:
    risk_set_ref = _exact(query.risk_set_ref, "query.risk_set_ref")
    used: list[Any] = []
    used_auth: list[AuthorityRef] = []
    expected_record_ids: list[str] = []
    record_audits: list[Mapping[str, Any]] = []
    derived_branch_memberships = _compile_derived_branch_memberships(predicate.predicate_ast)

    for index in sorted(indices, key=lambda item: item.universe.ref.key):
        universe_ref = index.universe.ref
        for respondent in sorted(index.respondents.values(), key=lambda item: item.ref.key):
            per_target_states: list[str] = []
            authority_bindings: list[Mapping[str, Any]] = []
            for component, bound_component in zip(plan.components, bound_contract.components):
                binding = authority_binding_for_universe(
                    bound_component.contract_component, universe_ref.as_dict()
                )
                authority_bindings.append(binding)
                routing_fact = _routing_fact_for(
                    respondent,
                    index,
                    target_ref=component.target_ref,
                    risk_set_ref=risk_set_ref,
                    registry=authority_registry,
                    used=used,
                    used_auth=used_auth,
                )
                required_risk_authority = _authority(
                    binding["risk_set_authority_ref"], "contract risk_set_authority_ref"
                )
                if required_risk_authority not in routing_fact.authority_snapshot_refs:
                    raise Pre553AuthorityError(
                        "routing fact is not bound by the contract's exact frozen risk-set authority"
                    )
                per_target_states.append(str(routing_fact.routing_state))

            member, _ = _risk_membership(per_target_states, profile=profile)
            if not member:
                # Pre-query exclusion/nonmembership is decided entirely by the
                # frozen risk-set layer and never by observed target state.
                continue

            condition = _eval_predicate(
                predicate.predicate_ast,
                respondent=respondent,
                index=index,
                registry=authority_registry,
                used=used,
                used_auth=used_auth,
                derived_branch_memberships=derived_branch_memberships,
            )
            if not condition:
                continue

            record_id = respondent.ref.key
            expected_record_ids.append(record_id)
            observations: list[Mapping[str, Any]] = []
            for component, bound_component, authority_binding in zip(
                plan.components, bound_contract.components, authority_bindings
            ):
                events = [
                    event
                    for event in index.events_by_respondent[respondent.ref.key]
                    if _event_matches_target(event, component.target_ref)
                ]
                if not events:
                    observations.append(unresolved_observation(
                        record_id=record_id,
                        target_ref=component.target_ref.as_dict(),
                        reason="TARGET_EVENT_UNAVAILABLE",
                    ))
                    continue

                required_source_authority = _authority(
                    authority_binding["source_semantic_authority_ref"],
                    "contract source_semantic_authority_ref",
                )
                for event in sorted(events, key=lambda item: item.ref.key):
                    if required_source_authority not in event.authority_snapshot_refs:
                        raise Pre553AuthorityError(
                            "target event is not bound by contract's exact source-local semantic authority"
                        )
                    _validate_public_object_authorities(event, authority_registry)
                    carrier_topology = _carrier_topology_kind(event)
                    if not _topology_compatible(component.topology, carrier_topology):
                        observations.append(unresolved_observation(
                            record_id=record_id,
                            target_ref=component.target_ref.as_dict(),
                            reason="SOURCE_TOPOLOGY_INCOMPATIBLE",
                        ))
                        continue

                    if event.typed_state == "SUBSTANTIVE_RESPONSE":
                        canonical_value = event.canonical_response_value_if_authorized
                    else:
                        # Non-substantive states are governed by their explicit
                        # typed state.  Native/special payload values are never a
                        # generic lookup key.
                        canonical_value = None
                    observation = audit_observation(
                        component=bound_component.contract_component,
                        record_id=record_id,
                        universe_ref=universe_ref.as_dict(),
                        event_ref=event.ref.as_dict(),
                        opaque_raw_state_hash=_opaque_raw_state_hash(event),
                        response_state=str(event.typed_state),
                        canonical_response_value=canonical_value,
                        source_semantic_authority_ref=required_source_authority.as_dict(),
                    )
                    disposition = observation["audit_trail"][2]["value"]
                    if (
                        disposition in {TARGET_MEMBER, RESOLVED_NON_TARGET}
                        and event.typed_state not in component.included_states
                    ):
                        raise Pre553SourceStateDispositionError(
                            "resolved source state cannot be removed from denominator by included_states filtering"
                        )
                    observations.append(observation)
            record_audits.append(build_record_audit(record_id, observations))

    scope_identity = {
        "adapter_id": PRODUCTION_ADAPTER_ID,
        "source_scope_mode": profile.source_scope_mode,
        "universe_refs": [index.universe.ref.as_dict() for index in sorted(indices, key=lambda x: x.universe.ref.key)],
        "risk_set_ref": risk_set_ref.as_dict(),
        "target_refs": [component.target_ref.as_dict() for component in plan.components],
        "authority_phase": AUTHORITY_PHASE,
    }
    return denominator_resolution_check(
        contract=bound_contract.normalized,
        scope_identity=scope_identity,
        expected_record_ids=expected_record_ids,
        record_audits=record_audits,
    )


def _group_indices(indices: tuple[Any, ...], source_scope_mode: str) -> tuple[tuple[Any, ...], ...]:
    if source_scope_mode not in SOURCE_SCOPE_MODES:
        raise Pre553SourceStateDispositionError("unknown source scope mode")
    if source_scope_mode == "SOURCE_INDEXED_MULTI_UNIVERSE":
        return tuple((index,) for index in indices)
    return (indices,)


def _fact_rows(result: QueryExecutionResult) -> tuple[Mapping[str, Any], ...]:
    rows: list[Mapping[str, Any]] = []
    for fact in result.facts:
        fields = fact.semantic_fields
        rows.append(MappingProxyType({
            "fact_ref": fact.ref.as_dict(),
            "typed_state": fact.typed_state,
            "raw_denominator_support": fields.get("raw_denominator_support"),
            "raw_resolved_target_support": fields.get(
                "raw_resolved_target_support", fields.get("raw_numerator_support")
            ),
        }))
    return tuple(rows)


def execute_source_state_target_disposition_query(
    *,
    repository: C11Repository,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    authority_registry: AuthorityRegistry,
    release_refs: Iterable[ExactRef],
) -> SourceStateTargetDispositionExecution:
    """Execute the PRE553 query only after the generic source-state gate passes."""
    if not isinstance(repository, C11Repository):
        raise Pre553SourceStateDispositionError("repository must be accepted C11Repository")
    if not isinstance(query, EmpiricalQuerySpec):
        raise Pre553SourceStateDispositionError("query must be EmpiricalQuerySpec@1.0.0")
    if not isinstance(predicate, EmpiricalPredicate):
        raise Pre553SourceStateDispositionError("predicate must be EmpiricalPredicate@1.0.0")
    if not isinstance(authority_registry, AuthorityRegistry):
        raise Pre553SourceStateDispositionError("authority_registry must be exact AuthorityRegistry")

    _verify_public_identity(query)
    _verify_public_identity(predicate)
    if query.typed_state != "QUERY_AUTHORIZED_RESOLVABLE":
        raise Pre553AuthorityError("source-state production query must be positively authorized")
    if predicate.typed_state != "PREDICATE_RESOLVED_AUTHORIZED":
        raise Pre553AuthorityError("source-state production predicate must be positively authorized")
    if _exact(query.condition_predicate_ref, "query.condition_predicate_ref") != predicate.ref:
        raise Pre553SourceStateDispositionError("query/predicate exact identity mismatch")

    profile = _profile(query)
    universe_refs = _query_universe_refs(query)
    _validate_public_object_authorities(query, authority_registry)
    _validate_public_object_authorities(predicate, authority_registry)
    _require_exact_i03_authority_fitness(
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        universe_refs=universe_refs,
    )
    plan = _parse_target_plan(query, authority_registry)
    bound_contract = _bind_contract(
        query=query, authority_registry=authority_registry, plan=plan
    )

    supplied_releases = _canonical_refs(_exact(ref, "release_refs") for ref in release_refs)
    resolved = _resolve_release_indices(
        repository, query=query, release_refs=supplied_releases
    )
    indices = tuple(item[1] for item in resolved)
    checks = tuple(
        _preflight_group(
            group,
            query=query,
            predicate=predicate,
            plan=plan,
            profile=profile,
            authority_registry=authority_registry,
            bound_contract=bound_contract,
        )
        for group in _group_indices(indices, profile.source_scope_mode)
    )
    failed = [row for row in checks if not row["passed"]]
    if failed:
        unresolved = sorted({
            record_id
            for row in failed
            for record_id in row["unresolved_record_ids"]
        })
        raise Pre553SourceStateDispositionError(
            "EMPIRICAL_RESULT blocked by unresolved source-state/product-target disposition for: "
            + ", ".join(unresolved)
        )

    # The ordinary PRE553 producer is invoked only after every exact generic
    # denominator gate has passed.  No learned/source-specific re-execution is
    # performed by this adapter itself.
    result = execute_empirical_query(
        repository=repository,
        query=query,
        predicate=predicate,
        authority_registry=authority_registry,
        release_refs=supplied_releases,
    )
    result_receipt = empirical_result_receipt(
        contract=bound_contract.normalized,
        denominator_checks=checks,
        query_ref=query.ref.as_dict(),
        release_refs=(ref.as_dict() for ref in result.release_refs),
        fact_rows=_fact_rows(result),
    )
    replay = replay_identity(
        contract=bound_contract.normalized,
        denominator_checks=checks,
        empirical_result=result_receipt,
    )
    receipt = ContractExecutionReceipt(
        contract_hash=contract_hash(bound_contract.normalized),
        denominator_checks=checks,
        empirical_result=result_receipt,
        replay_identity=replay,
    )
    return SourceStateTargetDispositionExecution(
        query_result=result,
        contract_receipt=receipt,
    )


def replay_source_state_target_disposition_query(
    *,
    expected_replay_identity: str,
    expected_fact_refs: Iterable[ExactRef],
    **kwargs: Any,
) -> SourceStateTargetDispositionExecution:
    """Replay the production adapter and require exact contract/fact identities."""
    if not isinstance(expected_replay_identity, str) or len(expected_replay_identity) != 64:
        raise Pre553SourceStateDispositionError("expected_replay_identity must be sha256 text")
    result = execute_source_state_target_disposition_query(**kwargs)
    if result.replay_identity != expected_replay_identity:
        raise Pre553SourceStateDispositionError("source-state contract replay identity mismatch")
    expected = _canonical_refs(_exact(ref, "expected_fact_refs") for ref in expected_fact_refs)
    actual = tuple(fact.ref for fact in result.query_result.facts)
    if actual != expected:
        raise Pre553SourceStateDispositionError("source-state contract fact replay mismatch")
    return result


__all__ = [
    "PRODUCTION_ADAPTER_ID", "CONTRACT_GRAIN_KEY",
    "Pre553SourceStateDispositionError", "SourceStateTargetDispositionExecution",
    "execute_source_state_target_disposition_query",
    "replay_source_state_target_disposition_query",
]
