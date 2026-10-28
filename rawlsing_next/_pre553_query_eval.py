"""Exact denominator, target, measure and EmpiricalFact construction for PRE553 I03."""
from rawlsing_next._pre553_query_common import *
from rawlsing_next._pre553_query_predicate import (
    _compile_derived_branch_memberships,
    _coordinate_matches,
    _eval_predicate,
    _question_matches,
    _validate_public_object_authorities,
)
from rawlsing_next.pre553_observed_response import (
    OBSERVED_RESPONSE_RISK_SET_TYPES,
    ObservedResponseContract,
    contract_for_query,
    topology_binding_for,
)


class _UsedObjectAccumulator(list[CanonicalSemanticObject | C11InternalRecord]):
    """Append-compatible exact-ref deduplication for evaluation provenance."""

    def __init__(self) -> None:
        super().__init__()
        self._seen_keys: set[str] = set()

    def append(self, obj: CanonicalSemanticObject | C11InternalRecord) -> None:
        key = obj.ref.key
        if key in self._seen_keys:
            return
        self._seen_keys.add(key)
        super().append(obj)

    def extend(self, objects: Iterable[CanonicalSemanticObject | C11InternalRecord]) -> None:
        for obj in objects:
            self.append(obj)


class _UsedAuthorityAccumulator(list[AuthorityRef]):
    """Append-compatible exact-authority deduplication for evaluation closure."""

    def __init__(self) -> None:
        super().__init__()
        self._seen_keys: set[str] = set()

    def append(self, ref: AuthorityRef) -> None:
        if ref.key in self._seen_keys:
            return
        self._seen_keys.add(ref.key)
        super().append(ref)

    def extend(self, refs: Iterable[AuthorityRef]) -> None:
        for ref in refs:
            self.append(ref)


def _routing_fact_for(
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    *,
    target_ref: ExactRef,
    risk_set_ref: ExactRef,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
) -> RoutingEligibilityFact:
    matches = [
        fact for fact in index.routing_by_respondent[respondent.ref.key]
        if _question_matches(fact, target_ref)
        and _ref_field(fact, "risk_set_ref") == risk_set_ref
    ]
    if not matches:
        raise EmpiricalQueryResolutionError(
            "exact routing/risk-set membership fact is unavailable; absence is not zero membership"
        )
    states = {(fact.routing_state, fact.applicability_state) for fact in matches}
    member_sets = {_ref_field(fact, "member_set_replay_ref").key for fact in matches}
    if len(states) != 1 or len(member_sets) != 1:
        raise EmpiricalQueryResolutionError(
            "conflicting exact routing/risk-set facts for one respondent and target"
        )
    routing_authority_seen = False
    for fact in matches:
        used.append(fact)
        refs = _validate_public_object_authorities(fact, registry)
        used_auth.extend(refs)
        if any(registry.resolve_exact(ref).snapshot.authority_kind == "ROUTING_RISK_SET" for ref in refs):
            routing_authority_seen = True
    if not routing_authority_seen:
        raise Pre553AuthorityError("routing/risk-set fact lacks exact ROUTING_RISK_SET authority")
    return sorted(matches, key=lambda fact: fact.ref.key)[0]


def _risk_membership(
    routing_states: Sequence[str],
    *,
    profile: _ExecutionProfile,
) -> tuple[bool, bool]:
    """Return membership from routing states already resolved and authority-validated."""
    statuses = [str(state) for state in routing_states]
    for state in statuses:
        if state in UNRESOLVED_ROUTING_STATES:
            raise EmpiricalQueryResolutionError(
                "routing/risk-set state is unresolved; it may not be coerced to nonmembership"
            )
        if state not in ELIGIBLE_ROUTING_STATES | EXPLICIT_NONMEMBER_ROUTING_STATES:
            raise EmpiricalQueryResolutionError(f"unknown exact routing state {state!r}")

    if profile.risk_set_type == "COMMON_ELIGIBLE_RISK_SET":
        member = all(state in ELIGIBLE_ROUTING_STATES for state in statuses)
    elif len(statuses) != 1:
        if len(set(statuses)) != 1:
            raise EmpiricalQueryResolutionError(
                "multi-target non-common risk set has target-specific membership disagreement"
            )
        member = statuses[0] in ELIGIBLE_ROUTING_STATES
    else:
        member = statuses[0] in ELIGIBLE_ROUTING_STATES
    explicitly_inapplicable = bool(statuses) and all(state == "INAPPLICABLE" for state in statuses)
    return member, explicitly_inapplicable


def _event_matches_target(event: RespondentEvent, target_ref: ExactRef) -> bool:
    if _question_matches(event, target_ref):
        return True
    component = _ref_field(event, "component_or_subitem_ref", allow_none=True)
    return component is not None and component == target_ref


def _event_cell_value(event: RespondentEvent) -> Any:
    if event.typed_state == "SUBSTANTIVE_RESPONSE":
        return canonicalize(_semantic_value(event))
    return canonicalize({"typed_response_state": event.typed_state})


def _semantic_order_key(event: RespondentEvent) -> tuple[int, Any, str]:
    fields = event.multiplicity_order_rank_fields
    if not isinstance(fields, Mapping):
        raise UnsupportedResponseTopology("ordered/repeated target requires exact multiplicity/order/rank fields")
    for name in ("semantic_ordinal", "semantic_order", "semantic_order_key", "ordinal", "order", "rank", "index", "multiplicity_index"):
        if name in fields:
            value = fields[name]
            if isinstance(value, bool) or not isinstance(value, (int, str)):
                raise UnsupportedResponseTopology(
                    f"{name} must be exact integer or string for deterministic semantic order"
                )
            return (0 if isinstance(value, int) else 1, value, event.ref.key)
    raise UnsupportedResponseTopology(
        "ordered/repeated target lacks an exact semantic order/rank/multiplicity key"
    )


def _carrier_topology_kind(event: RespondentEvent) -> str:
    fields = event.multiplicity_order_rank_fields
    if not isinstance(fields, Mapping):
        raise UnsupportedResponseTopology("response event lacks exact topology mapping")
    kind = fields.get("kind") or fields.get("topology_kind")
    if not isinstance(kind, str) or not kind.strip():
        raise UnsupportedResponseTopology("response event lacks explicit carrier topology kind")
    return kind.strip()


def _topology_compatible(requested: str, carrier: str) -> bool:
    accepted = {
        "SCALAR_SINGULAR": {"SCALAR_SINGULAR"},
        "UNORDERED_MULTISELECT_SET": {"UNORDERED_MULTISELECT_SET"},
        "UNORDERED_MULTISELECT": {"UNORDERED_MULTISELECT", "MULTISELECT"},
        "MULTISELECT": {"MULTISELECT", "UNORDERED_MULTISELECT"},
        "ORDERED_SEQUENCE": {"ORDERED_SEQUENCE"},
        "REPEATED_EVENT": {"REPEATED_EVENT"},
        "REPEATED_MEASUREMENT": {"REPEATED_MEASUREMENT"},
        "RANKED_RESPONSE": {"RANKED_RESPONSE"},
        "ROUTED_RESPONSE": {"ROUTED_RESPONSE", "SCALAR_SINGULAR"},
        "COMPONENTIZED_RESPONSE": {"COMPONENTIZED_RESPONSE"},
    }
    return carrier in accepted.get(requested, set())


def _target_component_value(
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    component: _TargetComponent,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
    *,
    topology_binding=None,
) -> tuple[bool, Any]:
    events = [
        event for event in index.events_by_respondent[respondent.ref.key]
        if _event_matches_target(event, component.target_ref)
        and event.typed_state in component.included_states
    ]
    for event in events:
        if topology_binding is not None:
            if _ref_field(event, "response_topology_ref") != topology_binding.source_native_topology_ref:
                raise UnsupportedResponseTopology(
                    "observed-response event response_topology_ref differs from exact contract binding")
            if _carrier_topology_kind(event) != topology_binding.source_native_kind:
                raise UnsupportedResponseTopology(
                    "observed-response event carrier topology kind differs from exact contract binding")
            if component.topology != topology_binding.i03_topology:
                raise UnsupportedResponseTopology(
                    "observed-response target topology differs from exact contract binding")
        else:
            carrier_topology = _carrier_topology_kind(event)
            if not _topology_compatible(component.topology, carrier_topology):
                raise UnsupportedResponseTopology(
                    f"query target topology {component.topology!r} cannot collapse exact C11 carrier topology {carrier_topology!r}"
                )
        if not any(ref in event.authority_snapshot_refs for ref in component.topology_authority_refs):
            raise Pre553AuthorityError(
                "target topology authority bundle does not bind matched C11 response event"
            )
        if not any(ref in event.authority_snapshot_refs for ref in component.response_semantic_authority_refs):
            raise Pre553AuthorityError(
                "target response-semantic authority bundle does not bind matched C11 response event"
            )
        used.append(event)
        used_auth.extend(_validate_public_object_authorities(event, registry))

    topology = component.topology
    if topology == "SCALAR_SINGULAR":
        if not events:
            return False, None
        if len(events) != 1:
            raise UnsupportedResponseTopology(
                "SCALAR_SINGULAR target resolved more than one exact respondent event"
            )
        return True, _event_cell_value(events[0])

    if topology == "ROUTED_RESPONSE":
        if not events:
            return False, None
        if len(events) != 1:
            raise UnsupportedResponseTopology(
                "ROUTED_RESPONSE target requires one exact response event after routing"
            )
        return True, _event_cell_value(events[0])

    if topology == "COMPONENTIZED_RESPONSE":
        if not events:
            return False, None
        if len(events) == 1:
            return True, _event_cell_value(events[0])
        ordered = sorted(events, key=lambda event: event.ref.key)
        return True, canonicalize([
            {
                "component_or_subitem_ref": _ref_field(event, "component_or_subitem_ref", allow_none=True),
                "value": _event_cell_value(event),
            }
            for event in ordered
        ])

    if topology == "UNORDERED_MULTISELECT_SET":
        return True, canonicalize(list(canonical_set(_event_cell_value(event) for event in events)))

    if topology in {"UNORDERED_MULTISELECT", "MULTISELECT"}:
        values = [_event_cell_value(event) for event in events]
        return True, canonicalize(sorted(values, key=canonical_json))

    if topology in {"ORDERED_SEQUENCE", "RANKED_RESPONSE"}:
        ordered = sorted(events, key=_semantic_order_key)
        return True, canonicalize([_event_cell_value(event) for event in ordered])

    if topology in {"REPEATED_EVENT", "REPEATED_MEASUREMENT"}:
        ordered = sorted(events, key=_semantic_order_key)
        return True, canonicalize([
            {
                "event_id": event.response_event_id_or_deterministic_index,
                "multiplicity_order_rank_fields": event.multiplicity_order_rank_fields,
                "value": _event_cell_value(event),
            }
            for event in ordered
        ])

    raise UnsupportedResponseTopology(f"unsupported target topology {topology!r}")


def _target_configuration(
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    *,
    plan: _TargetPlan,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
    observed_contract: ObservedResponseContract | None = None,
) -> tuple[bool, Any]:
    values: list[Any] = []
    for component in plan.components:
        binding = (
            topology_binding_for(observed_contract, component.target_ref)
            if observed_contract is not None else None
        )
        resolved, value = _target_component_value(
            respondent, index, component, registry, used, used_auth,
            topology_binding=binding,
        )
        if not resolved:
            return False, None
        values.append(value)
    if plan.arity == 1:
        return True, canonicalize(values[0])
    return True, canonicalize(values)


def _weight_for(
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    *,
    profile: _ExecutionProfile,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
) -> Fraction:
    if profile.measure_kind == "RAW":
        return Fraction(1, 1)
    matches = [
        fact for fact in index.weights_by_respondent[respondent.ref.key]
        if fact.weight_basis_id == profile.weight_basis_id
    ]
    if len(matches) != 1:
        raise EmpiricalQueryResolutionError(
            "weighted query requires exactly one exact governed weight per denominator member"
        )
    fact = matches[0]
    used.append(fact)
    used_auth.extend(_validate_public_object_authorities(fact, registry))
    if fact.typed_state != "WEIGHT_VALID_AUTHORIZED":
        raise Pre553AuthorityError(
            f"weighted query cannot use exact weight state {fact.typed_state!r}"
        )
    for name in ("design_authority_ref", "estimand_authority_ref"):
        ref = _authority_field(fact, name)
        snapshot = registry.resolve_exact(ref).snapshot
        if snapshot.typed_state != "ALLOW" or snapshot.authority_kind != "WEIGHT_DESIGN_ESTIMAND":
            raise Pre553AuthorityError(f"{name} lacks exact positive WEIGHT_DESIGN_ESTIMAND authority")
        used_auth.append(ref)
    value = _fraction_from_exact(fact.exact_weight_value_representation, "exact_weight_value_representation")
    if value < 0:
        raise EmpiricalQueryExecutionError("negative governed respondent weights are unsupported")
    return value


def _observed_target_observed(
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    *,
    plan: _TargetPlan,
    contract: ObservedResponseContract,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
) -> bool:
    """Require at least one observed event per target before resolution."""
    for component in plan.components:
        observed_events = [
            event for event in index.events_by_respondent[respondent.ref.key]
            if _event_matches_target(event, component.target_ref)
            and event.typed_state in contract.observed_states
        ]
        if not observed_events:
            return False
        binding = topology_binding_for(contract, component.target_ref)
        resolved, _ = _target_component_value(
            respondent, index, component, registry, used, used_auth,
            topology_binding=binding,
        )
        if not resolved:
            return False
    return True


def _condition_observed(
    node: Mapping[str, Any],
    *,
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    contract: ObservedResponseContract,
) -> bool:
    """Conservative condition co-observation: every referenced position must be observed.

    This deliberately does not apply three-valued shortcut logic for OR/AND.  The
    contract policy is all referenced response/coordinate variables observed, so
    a condition is evaluated only when every referenced position is observed.
    """
    op = node.get("op")
    if op == "LEAF":
        leaf_type = node.get("leaf_type")
        if leaf_type in {"SURVEY_RESPONSE_EVENT", "TYPED_RESPONSE_STATE"}:
            question_ref = _exact(node.get("question_semantic_ref"), "question_semantic_ref")
            return any(
                _question_matches(event, question_ref)
                and event.typed_state in contract.observed_states
                for event in index.events_by_respondent[respondent.ref.key]
            )
        if leaf_type == "EMPIRICAL_POSITION_COORDINATE":
            coordinate_ref = _exact(
                node.get("coordinate_semantic_ref"), "coordinate_semantic_ref")
            effective_time = node.get("effective_or_reference_time")
            matches = [
                coordinate for coordinate in index.coordinates_by_respondent[respondent.ref.key]
                if _coordinate_matches(coordinate, coordinate_ref)
                and (
                    effective_time is None
                    or coordinate.effective_or_reference_time == canonicalize(effective_time)
                )
            ]
            return bool(matches)
        if leaf_type == "ROUTING_APPLICABILITY_STATE":
            raise Pre553AuthorityError(
                "observed-response condition may not use routing/applicability predicates")
        if leaf_type == "DERIVED_BRANCH_COHORT":
            return True
        raise EmpiricalQueryResolutionError("unknown observed-response condition leaf")
    if op == "NOT":
        children = _require_sequence(node.get("children"), "NOT children")
        if len(children) != 1:
            raise EmpiricalQueryResolutionError("NOT requires exactly one child")
        return _condition_observed(
            _require_mapping(children[0], "NOT child"),
            respondent=respondent, index=index, contract=contract,
        )
    if op in {"AND", "OR"}:
        children = _require_sequence(node.get("children"), f"{op} children")
        return all(
            _condition_observed(
                _require_mapping(child, f"{op} child"),
                respondent=respondent, index=index, contract=contract,
            )
            for child in children
        )
    raise EmpiricalQueryResolutionError("predicate op must be AND/OR/NOT/LEAF")


def _evaluate_index_group(
    indices: Sequence[_ReleaseIndex],
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    plan: _TargetPlan,
    profile: _ExecutionProfile,
    registry: AuthorityRegistry,
) -> _Evaluation:
    risk_set_ref = _exact(query.risk_set_ref, "query.risk_set_ref")
    raw_cells = {canonical_json(cell): 0 for cell in plan.full_domain}
    cell_material = {canonical_json(cell): cell for cell in plan.full_domain}
    weighted_cells: dict[str, Fraction] | None = (
        {canonical_json(cell): Fraction(0, 1) for cell in plan.full_domain}
        if profile.measure_kind == "GOVERNED_WEIGHTED" else None
    )
    used: list[CanonicalSemanticObject | C11InternalRecord] = _UsedObjectAccumulator()
    used_auth: list[AuthorityRef] = _UsedAuthorityAccumulator()
    risk_members: list[ExactRef] = []
    denominator_members: list[ExactRef] = []
    raw_resolved = 0
    weighted_denominator = Fraction(0, 1) if weighted_cells is not None else None
    weighted_resolved = Fraction(0, 1) if weighted_cells is not None else None
    inapplicable_count = 0
    component_positive = [False] * plan.arity
    derived_branch_memberships = _compile_derived_branch_memberships(predicate.predicate_ast)
    observed_ledger: dict[str, Any] | None = None
    if profile.observed_response_contract_ref is not None:
        observed_ledger = {
            "contract_ref": profile.observed_response_contract_ref.as_dict(),
            "risk_set_type": profile.risk_set_type,
            "denominator_policy": (
                "PER_TARGET_OBSERVED"
                if profile.risk_set_type == "OBSERVED_RESPONSE_RISK_SET"
                else "CO_OBSERVED_TARGETS"
            ),
            "condition_observation_policy": "ALL_REFERENCED_RESPONSE_VARIABLES_OBSERVED",
            "not_eligible_population_estimate": True,
            "scoped_respondents": sum(len(index.respondents) for index in indices),
            "target_observed": 0,
            "target_unobserved": 0,
            "condition_unobserved": 0,
            "condition_false": 0,
            "denominator": 0,
            "resolved_targets": 0,
            "unresolved_after_denominator": 0,
        }

    try:
        from rawlsing_next.pre553_runtime_context import current_runtime_binding
        runtime_binding = current_runtime_binding()
    except ImportError:
        runtime_binding = None
    if runtime_binding is not None:
        for index in indices:
            index.runtime_authorities = runtime_binding.authorities
            index.runtime_repository = runtime_binding.repository
            index.runtime_predicate_grammar_authority_ref = predicate.grammar_authority_ref

    for index in sorted(indices, key=lambda item: item.universe.ref.key):
        used.extend([index.universe, index.release.replay_manifest])
        used_auth.extend(_validate_public_object_authorities(index.universe, registry))
        observed_contract = None
        exact_risk_set_contract = None
        if profile.observed_response_contract_ref is not None:
            observed_contract = contract_for_query(
                profile=profile,
                query=query,
                plan=plan,
                predicate=predicate,
                release=index.release,
                universe=index.universe,
                registry=registry,
            )
        elif runtime_binding is not None:
            exact_risk_set_contract = (
                runtime_binding.authorities.resolve_exact_risk_set_successor(
                    query=query,
                    release_ref=index.release.release_ref,
                    source_universe_ref=index.universe.ref,
                    risk_set_ref=risk_set_ref,
                    target_refs=tuple(component.target_ref for component in plan.components),
                )
            )
        for respondent in sorted(index.respondents.values(), key=lambda item: item.ref.key):
            if observed_contract is not None:
                target_observed = _observed_target_observed(
                    respondent,
                    index,
                    plan=plan,
                    contract=observed_contract,
                    registry=registry,
                    used=used,
                    used_auth=used_auth,
                )
                if not target_observed:
                    observed_ledger["target_unobserved"] += 1
                    continue
                observed_ledger["target_observed"] += 1
                risk_members.append(respondent.ref)
                if not _condition_observed(
                    predicate.predicate_ast,
                    respondent=respondent,
                    index=index,
                    contract=observed_contract,
                ):
                    observed_ledger["condition_unobserved"] += 1
                    continue
                condition = _eval_predicate(
                    predicate.predicate_ast,
                    respondent=respondent,
                    index=index,
                    registry=registry,
                    used=used,
                    used_auth=used_auth,
                    derived_branch_memberships=derived_branch_memberships,
                )
                if not condition:
                    observed_ledger["condition_false"] += 1
                    continue
            else:
                per_target_states: list[str] = []
                for i, component in enumerate(plan.components):
                    fact = _routing_fact_for(
                        respondent,
                        index,
                        target_ref=component.target_ref,
                        risk_set_ref=risk_set_ref,
                        registry=registry,
                        used=used,
                        used_auth=used_auth,
                    )
                    per_target_states.append(str(fact.routing_state))
                    if fact.routing_state in ELIGIBLE_ROUTING_STATES:
                        component_positive[i] = True
                member, explicitly_inapplicable = _risk_membership(
                    per_target_states,
                    profile=profile,
                )
                if exact_risk_set_contract is not None:
                    exact_member = exact_risk_set_contract.is_member(
                        respondent_key=respondent.respondent_key,
                        target_refs=tuple(component.target_ref for component in plan.components),
                    )
                    if exact_member and not member:
                        raise Pre553AuthorityError(
                            "exact adopted risk-set member conflicts with C11 routing authority"
                        )
                    member = exact_member
                    if not member:
                        explicitly_inapplicable = False
                if explicitly_inapplicable:
                    inapplicable_count += 1
                if not member:
                    continue
                risk_members.append(respondent.ref)
                condition = _eval_predicate(
                    predicate.predicate_ast,
                    respondent=respondent,
                    index=index,
                    registry=registry,
                    used=used,
                    used_auth=used_auth,
                    derived_branch_memberships=derived_branch_memberships,
                )
                if not condition:
                    continue
            denominator_members.append(respondent.ref)
            weight = _weight_for(
                respondent,
                index,
                profile=profile,
                registry=registry,
                used=used,
                used_auth=used_auth,
            )
            if weighted_denominator is not None:
                weighted_denominator += weight
            if not plan.full_domain:
                continue
            resolved, cell = _target_configuration(
                respondent,
                index,
                plan=plan,
                registry=registry,
                used=used,
                used_auth=used_auth,
                observed_contract=observed_contract,
            )
            if not resolved:
                continue
            key = canonical_json(cell)
            if key not in raw_cells:
                raise EmpiricalQueryExecutionError(
                    "realized exact target cell is absent from the query-declared full target domain"
                )
            raw_resolved += 1
            raw_cells[key] += 1
            if weighted_cells is not None and weighted_resolved is not None:
                weighted_resolved += weight
                weighted_cells[key] += weight

    risk_refs = _canonical_refs(risk_members)
    denominator_refs = _canonical_refs(denominator_members)
    raw_denominator = len(denominator_refs)
    if observed_ledger is not None:
        observed_ledger["denominator"] = raw_denominator
        observed_ledger["resolved_targets"] = raw_resolved
        observed_ledger["unresolved_after_denominator"] = raw_denominator - raw_resolved
        observed_ledger["risk_member_count"] = len(risk_refs)
        observed_ledger["denominator_member_count"] = len(denominator_refs)

    if not risk_refs:
        if profile.risk_set_type == "COMMON_ELIGIBLE_RISK_SET" and all(component_positive):
            state = "ZERO_OVERLAP"
            detail = "each target has eligible respondents but exact common risk-set overlap is zero"
        elif inapplicable_count > 0 and inapplicable_count == sum(len(index.respondents) for index in indices):
            state = "NOT_APPLICABLE"
            detail = "exact routing/applicability law marks the target inapplicable for the scoped respondent domain"
        else:
            state = "ZERO_SUPPORT"
            detail = "exact risk set resolves to zero members"
    elif raw_denominator == 0:
        state = "ZERO_SUPPORT"
        detail = "exact risk set is nonempty but the condition-selected denominator has zero members"
    elif not plan.full_domain:
        state = "VALID_EMPTY"
        detail = "query-declared exact target domain is empty"
    elif raw_resolved != raw_denominator:
        state = "UNRESOLVED"
        detail = "positive denominator exists but exact target configuration is unresolved for one or more denominator members"
    else:
        state = "SUPPORTED"
        detail = "exact governed target distribution resolved"

    return _Evaluation(
        fact_state=state,
        detail=detail,
        risk_members=risk_refs,
        denominator_members=denominator_refs,
        raw_denominator=raw_denominator,
        raw_resolved_target_support=raw_resolved,
        raw_cells=MappingProxyType(dict(sorted(raw_cells.items()))),
        cell_material=MappingProxyType(dict(sorted(cell_material.items()))),
        weighted_denominator=weighted_denominator,
        weighted_cells=(MappingProxyType(dict(sorted(weighted_cells.items())))
                        if weighted_cells is not None else None),
        used_objects=tuple(sorted({obj.ref.key: obj for obj in used}.values(), key=lambda obj: obj.ref.key)),
        used_authority_refs=_canonical_authorities(used_auth),
        observed_response_ledger=(
            MappingProxyType(dict(sorted(observed_ledger.items())))
            if observed_ledger is not None else None
        ),
    )


def _fraction_material(value: Fraction | None) -> Any:
    if value is None:
        return None
    return {"$exact_fraction": [value.numerator, value.denominator]}


def _cell_projection(evaluation: _Evaluation) -> tuple[Mapping[str, Any], ...]:
    rows: list[Mapping[str, Any]] = []
    for key in sorted(evaluation.cell_material):
        raw = evaluation.raw_cells[key]
        if evaluation.raw_denominator > 0 and raw == 0:
            cell_state = "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
        elif raw > 0:
            cell_state = "OBSERVED_POSITIVE"
        else:
            cell_state = "ZERO_SUPPORT"
        weighted = evaluation.weighted_cells[key] if evaluation.weighted_cells is not None else None
        rows.append(MappingProxyType({
            "cell": evaluation.cell_material[key],
            "cell_state": cell_state,
            "raw_numerator_support": raw,
            "weighted_numerator_support_if_authorized": _fraction_material(weighted),
        }))
    return tuple(rows)


def _make_execution_replay_ref(
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    indices: Sequence[_ReleaseIndex],
    plan: _TargetPlan,
    profile: _ExecutionProfile,
    evaluation: _Evaluation,
) -> ExactRef:
    material = {
        "contract": QUERY_EXECUTION_CONTRACT_ID,
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "release_refs": [index.release.release_ref.as_dict() for index in sorted(indices, key=lambda x: x.release.release_ref.key)],
        "release_replay_refs": [index.release.replay_manifest.ref.as_dict() for index in sorted(indices, key=lambda x: x.release.release_ref.key)],
        "source_scope_mode": profile.source_scope_mode,
        "measure_kind": profile.measure_kind,
        "risk_set_type": profile.risk_set_type,
        "observed_response_contract_ref": (
            profile.observed_response_contract_ref.as_dict()
            if profile.observed_response_contract_ref is not None else None
        ),
        "target_domain_identity": plan.domain_identity,
        "risk_member_refs": [ref.as_dict() for ref in evaluation.risk_members],
        "denominator_member_refs": [ref.as_dict() for ref in evaluation.denominator_members],
        "complete_cells": list(_cell_projection(evaluation)),
    }
    digest = semantic_hash(material)
    return ExactRef(
        "PRE553_I03_QUERY_REPLAY",
        f"urn:rawlsing:pre553:i03-query-replay:sha256:{digest}",
        digest,
    )


def _build_fact(
    indices: Sequence[_ReleaseIndex],
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    plan: _TargetPlan,
    profile: _ExecutionProfile,
    evaluation: _Evaluation,
    registry: AuthorityRegistry,
    extra_authority_refs: Iterable[AuthorityRef] = (),
) -> EmpiricalFact:
    replay_ref = _make_execution_replay_ref(
        query=query,
        predicate=predicate,
        indices=indices,
        plan=plan,
        profile=profile,
        evaluation=evaluation,
    )
    query_auth = _validate_public_object_authorities(query, registry)
    predicate_auth = _validate_public_object_authorities(predicate, registry)
    grammar_auth = _authority(predicate.grammar_authority_ref, "predicate.grammar_authority_ref")
    try:
        grammar_snapshot = registry.resolve_exact(grammar_auth).snapshot
    except Pre553AuthorityError:
        try:
            from rawlsing_next.pre553_runtime_context import current_runtime_authorities
            runtime = current_runtime_authorities()
        except ImportError:
            runtime = None
        if runtime is None or not runtime.is_positive_runtime_predicate_authority(grammar_auth):
            raise
        runtime.validate_predicate(predicate)
    else:
        if grammar_snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("predicate grammar authority is not positive")
    semantic_query_auths = _canonical_authorities(
        _authority(value, "query.query_authority_refs") for value in query.query_authority_refs
    )
    for ref in semantic_query_auths:
        if registry.resolve_exact(ref).snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("exact query authority is not positive")

    all_auth = _canonical_authorities(
        (*query_auth, *predicate_auth, grammar_auth, *semantic_query_auths,
         *evaluation.used_authority_refs, *extra_authority_refs,
         *(ref for component in plan.components for ref in component.topology_authority_refs),
         *(ref for component in plan.components for ref in component.response_semantic_authority_refs))
    )
    provenance = _canonical_refs([
        *(index.release.release_ref for index in indices),
        *(index.release.replay_manifest.ref for index in indices),
        *(index.universe.ref for index in indices),
        *(obj.ref for obj in evaluation.used_objects),
    ])
    dependency_refs = _canonical_refs([query.ref, predicate.ref, replay_ref, *provenance])
    measure_ref = _exact(query.measure_basis_ref, "query.measure_basis_ref")
    risk_ref = _exact(query.risk_set_ref, "query.risk_set_ref")
    condition_ref = _exact(query.condition_predicate_ref, "query.condition_predicate_ref")
    universe_refs = _canonical_refs(index.universe.ref for index in indices)
    weighted_resolved = None
    if evaluation.weighted_cells is not None:
        weighted_resolved = sum(evaluation.weighted_cells.values(), Fraction(0, 1))

    return EmpiricalFact(
        typed_state=evaluation.fact_state,
        authority_snapshot_refs=all_auth,
        dependency_refs=dependency_refs,
        producer_replay_locator_or_reference_root=replay_ref,
        empirical_query_spec_ref=query.ref,
        empirical_universe_refs=universe_refs,
        target_topology={
            "arity": plan.arity,
            "joint_order_semantics": plan.joint_order_semantics,
            "target_domain_identity": plan.domain_identity,
            "complete_cell_semantic_projection": list(_cell_projection(evaluation)),
            "observed_response": (
                {
                    "contract_ref": profile.observed_response_contract_ref.as_dict(),
                    "status": "OBSERVED_RESPONSE_NOT_ELIGIBLE_POPULATION",
                    "not_eligible_population_estimate": True,
                    "ledger": dict(evaluation.observed_response_ledger),
                }
                if profile.observed_response_contract_ref is not None
                and evaluation.observed_response_ledger is not None
                else None
            ),
        },
        condition_predicate_ref=condition_ref,
        risk_set_ref=risk_ref,
        raw_numerator_support=evaluation.raw_resolved_target_support,
        raw_denominator_support=evaluation.raw_denominator,
        weighted_numerator_support_if_authorized=_fraction_material(weighted_resolved),
        weighted_denominator_support_if_authorized=_fraction_material(evaluation.weighted_denominator),
        measure_basis_ref=measure_ref,
        response_state_semantics_ref=profile.response_state_semantics_ref,
        uncertainty_method_or_typed_state=profile.uncertainty_method_or_typed_state,
        source_empirical_provenance_refs=provenance,
        replay_ref=replay_ref,
        query_execution_contract_id=QUERY_EXECUTION_CONTRACT_ID,
        execution_detail=evaluation.detail,
        source_scope_mode=profile.source_scope_mode,
        measure_kind=profile.measure_kind,
        risk_set_type=profile.risk_set_type,
        risk_set_member_refs=evaluation.risk_members,
        denominator_member_refs=evaluation.denominator_members,
        target_domain_identity=plan.domain_identity,
        raw_resolved_target_support=evaluation.raw_resolved_target_support,
    )


def _build_negative_fact(
    *,
    query: EmpiricalQuerySpec,
    predicate: EmpiricalPredicate,
    profile: _ExecutionProfile,
    p01_state: str,
    p02_failure_state: str,
    detail: str,
    universe_refs: Iterable[ExactRef],
    release_refs: Iterable[ExactRef],
) -> EmpiricalFact:
    """Build a deterministic typed nonpositive fact from still-trustworthy exact inputs.

    Identity/hash tampering is never converted into a semantic negative; callers must
    invoke this helper only after query/predicate public identities and exact core refs
    have been verified.
    """
    universes = _canonical_refs(universe_refs)
    releases = _canonical_refs(release_refs)
    condition_ref = _exact(query.condition_predicate_ref, "query.condition_predicate_ref")
    risk_ref = _exact(query.risk_set_ref, "query.risk_set_ref")
    measure_ref = _exact(query.measure_basis_ref, "query.measure_basis_ref")
    replay_material = {
        "contract": QUERY_EXECUTION_CONTRACT_ID,
        "query_ref": query.ref.as_dict(),
        "predicate_ref": predicate.ref.as_dict(),
        "source_scope_mode": profile.source_scope_mode,
        "universe_refs": [ref.as_dict() for ref in universes],
        "release_refs": [ref.as_dict() for ref in releases],
        "p01_state": p01_state,
        "p02_failure_state": p02_failure_state,
        "detail": detail,
    }
    digest = semantic_hash(replay_material)
    replay_ref = ExactRef(
        "PRE553_I03_QUERY_REPLAY",
        f"urn:rawlsing:pre553:i03-query-replay:sha256:{digest}",
        digest,
    )
    provenance = _canonical_refs([*universes, *releases])
    authority_refs = _canonical_authorities([
        *query.authority_snapshot_refs, *predicate.authority_snapshot_refs
    ])
    return EmpiricalFact(
        typed_state=p01_state,
        authority_snapshot_refs=authority_refs,
        dependency_refs=_canonical_refs([query.ref, predicate.ref, replay_ref, *provenance]),
        producer_replay_locator_or_reference_root=replay_ref,
        empirical_query_spec_ref=query.ref,
        empirical_universe_refs=universes,
        target_topology={
            "requested_target_arity_and_topology": query.target_arity_and_topology,
            "p02_failure_state": p02_failure_state,
            "observed_response_contract_ref": (
                profile.observed_response_contract_ref.as_dict()
                if profile.observed_response_contract_ref is not None else None
            ),
        },
        condition_predicate_ref=condition_ref,
        risk_set_ref=risk_ref,
        raw_numerator_support=0,
        raw_denominator_support=0,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=measure_ref,
        response_state_semantics_ref=profile.response_state_semantics_ref,
        uncertainty_method_or_typed_state=profile.uncertainty_method_or_typed_state,
        source_empirical_provenance_refs=provenance,
        replay_ref=replay_ref,
        query_execution_contract_id=QUERY_EXECUTION_CONTRACT_ID,
        execution_detail=detail,
        source_scope_mode=profile.source_scope_mode,
        measure_kind=profile.measure_kind,
        risk_set_type=profile.risk_set_type,
        p02_failure_state=p02_failure_state,
    )


__all__ = ["_evaluate_index_group", "_build_fact", "_build_negative_fact"]
