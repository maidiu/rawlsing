"""Exact C11 indexing and empirical predicate evaluation for PRE553 I03."""
from rawlsing_next._pre553_query_common import *
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet

def _question_matches(event: RespondentEvent | RoutingEligibilityFact, target: ExactRef) -> bool:
    if isinstance(event, RoutingEligibilityFact):
        return _ref_field(event, "question_or_target_ref") == target
    native = _ref_field(event, "native_question_ref")
    canonical = _ref_field(event, "canonical_question_ref_if_authorized", allow_none=True)
    return target == native or (canonical is not None and target == canonical)


def _coordinate_matches(coordinate: EmpiricalCoordinateFact, ref: ExactRef) -> bool:
    native = _ref_field(coordinate, "native_coordinate_ref")
    canonical = _ref_field(coordinate, "canonical_coordinate_ref_if_authorized", allow_none=True)
    return ref == native or (canonical is not None and ref == canonical)


def _build_release_index(release: C11LogicalRelease, universe_ref: ExactRef) -> _ReleaseIndex:
    universes = [o for o in release.public_objects if isinstance(o, EmpiricalUniverse) and o.ref == universe_ref]
    if len(universes) != 1:
        raise EmpiricalQueryResolutionError("exact universe must resolve once inside sealed C11 release")
    universe = universes[0]
    respondents: dict[str, RespondentIdentity] = {}
    for record in release.internal_records:
        if isinstance(record, RespondentIdentity) and record.empirical_universe_ref == universe_ref:
            key = record.ref.key
            if key in respondents and respondents[key] != record:
                raise EmpiricalQueryResolutionError("conflicting exact respondent identity")
            respondents[key] = record
    if not respondents:
        respondents = {}

    events: dict[str, list[RespondentEvent]] = {key: [] for key in respondents}
    coords: dict[str, list[EmpiricalCoordinateFact]] = {key: [] for key in respondents}
    routing: dict[str, list[RoutingEligibilityFact]] = {key: [] for key in respondents}
    weights: dict[str, list[WeightMeasureFact]] = {key: [] for key in respondents}
    relations: list[SourceUniverseRelation] = []
    for obj in release.public_objects:
        if isinstance(obj, SourceUniverseRelation):
            if universe_ref.as_dict() in tuple(obj.source_universe_refs):
                relations.append(obj)
            continue
        if not isinstance(obj, (RespondentEvent, EmpiricalCoordinateFact,
                                RoutingEligibilityFact, WeightMeasureFact)):
            continue
        if _object_universe_ref(obj) != universe_ref:
            continue
        respondent_ref = _object_respondent_ref(obj)
        if respondent_ref.key not in respondents:
            raise EmpiricalQueryResolutionError(
                "public respondent-grain object references respondent absent from C11 RespondentIdentity")
        if isinstance(obj, RespondentEvent):
            events[respondent_ref.key].append(obj)
        elif isinstance(obj, EmpiricalCoordinateFact):
            coords[respondent_ref.key].append(obj)
        elif isinstance(obj, RoutingEligibilityFact):
            routing[respondent_ref.key].append(obj)
        else:
            weights[respondent_ref.key].append(obj)
    for mapping in (events, coords, routing, weights):
        for key in mapping:
            mapping[key].sort(key=lambda obj: obj.ref.key)
    return _ReleaseIndex(
        release=release,
        universe=universe,
        respondents=respondents,
        events_by_respondent=events,
        coordinates_by_respondent=coords,
        routing_by_respondent=routing,
        weights_by_respondent=weights,
        source_relations=tuple(sorted(relations, key=lambda r: r.ref.key)),
    )


_PUBLIC_AUTHORITY_VALIDATION_CACHE: dict[tuple[int, str], tuple[AuthorityRef, ...]] = {}


def _validate_public_object_authorities(
    obj: CanonicalSemanticObject,
    registry: AuthorityRegistry,
) -> tuple[AuthorityRef, ...]:
    cache_key = (id(registry), obj.ref.key)
    cached = _PUBLIC_AUTHORITY_VALIDATION_CACHE.get(cache_key)
    if cached is not None:
        return cached
    runtime = None
    try:
        from rawlsing_next.pre553_runtime_context import current_runtime_authorities
        runtime = current_runtime_authorities()
    except ImportError:
        runtime = None

    resolved: list[AuthorityRef] = []
    for raw_ref in obj.authority_snapshot_refs:
        ref = _authority(raw_ref, f"{obj.schema_id}.authority_snapshot_ref")
        try:
            snapshot = registry.resolve_exact(ref).snapshot
        except Pre553AuthorityError:
            if runtime is None or not runtime.is_positive_runtime_predicate_authority(ref):
                raise
            resolved.append(ref)
            continue
        if snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError(
                f"{obj.schema_id} authority closure contains nonpositive exact snapshot")
        resolved.append(snapshot.authority_ref)
    if obj.schema_id != "AuthoritySnapshot" and not resolved:
        raise Pre553AuthorityError("public semantic object lacks authority closure")
    result = tuple(resolved)
    _PUBLIC_AUTHORITY_VALIDATION_CACHE[cache_key] = result
    return result


def _leaf_exact_values(
    node: Mapping[str, Any], *, exact_ref_field: str
) -> tuple[Any, ...]:
    _exact(node.get(exact_ref_field), exact_ref_field)
    values = node.get("exact_values")
    if values is None:
        if "exact_value" not in node:
            raise EmpiricalQueryResolutionError("predicate value leaf requires exact_value(s)")
        values = [node["exact_value"]]
    values = _require_sequence(values, "predicate exact_values")
    return tuple(canonicalize(v) for v in values)


def _leaf_match(
    node: Mapping[str, Any],
    *,
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
    predicate_grammar_authority_ref: AuthorityRef | Mapping[str, Any] | None = None,
    runtime_authorities: Pre553RuntimeAuthoritySet | None = None,
    repository: C11Repository | None = None,
    derived_branch_memberships: Mapping[ExactRef, frozenset[ExactRef]] | None = None,
) -> bool:
    leaf_type = node.get("leaf_type")
    respondent_key = respondent.ref.key
    leaf_scope = node.get("empirical_universe_ref")
    if leaf_scope is not None and _exact(leaf_scope, "leaf.empirical_universe_ref") != index.universe.ref:
        return False
    if leaf_type == "EMPIRICAL_POSITION_COORDINATE":
        coordinate_ref = _exact(node.get("coordinate_semantic_ref"), "coordinate_semantic_ref")
        _exact(node.get("comparison_operator_ref"), "comparison_operator_ref")
        _exact(node.get("typed_state_policy_ref"), "typed_state_policy_ref")
        auth_ref = _authority(node.get("coordinate_authority_ref"), "coordinate_authority_ref")
        snapshot = registry.resolve_exact(auth_ref).snapshot
        if snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("coordinate predicate authority is not positive")
        operator = node.get("operator")
        if operator not in {"EQ", "IN", "STATE_EQ"}:
            raise EmpiricalQueryResolutionError("coordinate predicate operator must be EQ/IN/STATE_EQ")
        values = _leaf_exact_values(node, exact_ref_field="value_or_value_set_ref") if operator != "STATE_EQ" else ()
        matches = [c for c in index.coordinates_by_respondent[respondent_key]
                   if _coordinate_matches(c, coordinate_ref)]
        effective_time = node.get("effective_or_reference_time")
        if effective_time is not None:
            matches = [c for c in matches if c.effective_or_reference_time == canonicalize(effective_time)]
        if not matches:
            return False
        if len({canonical_json(_semantic_value(c)) for c in matches}) > 1 and effective_time is None:
            raise EmpiricalQueryResolutionError(
                "coordinate predicate is temporally/value ambiguous without exact effective time")
        result = False
        for coordinate in matches:
            source_auth = _authority_field(coordinate, "source_semantic_authority_ref")
            if auth_ref != source_auth and auth_ref not in coordinate.authority_snapshot_refs:
                raise Pre553AuthorityError("predicate coordinate authority does not bind matched C11 fact")
            used.append(coordinate)
            used_auth.extend(_validate_public_object_authorities(coordinate, registry))
            if operator == "STATE_EQ":
                result = result or coordinate.typed_state == node.get("typed_state")
            else:
                semantic = canonicalize(_semantic_value(coordinate))
                result = result or semantic in values
        return result

    if leaf_type == "SURVEY_RESPONSE_EVENT" and node.get("operation") is not None:
        runtime_authorities = runtime_authorities or index.runtime_authorities
        predicate_grammar_authority_ref = (
            predicate_grammar_authority_ref or index.runtime_predicate_grammar_authority_ref
        )
        repository = repository or index.runtime_repository
        if runtime_authorities is None or predicate_grammar_authority_ref is None or repository is None:
            try:
                from rawlsing_next.pre553_runtime_context import current_runtime_binding
                binding = current_runtime_binding()
            except ImportError:
                binding = None
            if binding is not None:
                runtime_authorities = runtime_authorities or binding.authorities
                predicate_grammar_authority_ref = (
                    predicate_grammar_authority_ref
                    or binding.predicate_grammar_authority_ref
                )
                repository = repository or binding.repository
        if runtime_authorities is None or predicate_grammar_authority_ref is None:
            raise Pre553AuthorityError(
                "governed public predicate dialect requires exact interpreter authority")
        if repository is None:
            raise Pre553AuthorityError(
                "predicate dialect release realization requires exact C11Repository")
        contract = runtime_authorities.resolve_predicate_dialect(
            predicate_grammar_authority_ref, node
        )
        question_ref, response_ref, native_value, scope_ref = contract.validate_leaf(node)
        runtime_authorities.require_realized_release(
            scope_ref,
            repository=repository,
            runtime_release_ref=index.release.release_ref,
        )
        result = False
        for event in index.events_by_respondent[respondent_key]:
            if _ref_field(event, "native_question_ref") != question_ref:
                continue
            used.append(event)
            used_auth.extend(_validate_public_object_authorities(event, registry))
            if event.typed_state != "SUBSTANTIVE_RESPONSE":
                continue
            result = result or runtime_authorities.match_exact_event_representation(
                frozen_scope_ref=scope_ref,
                runtime_release_ref=index.release.release_ref,
                question_ref=question_ref,
                response_value_ref=response_ref,
                source_native_value=native_value,
                event_raw_response_value=event.raw_response_value,
            )
        return result

    if leaf_type == "SURVEY_RESPONSE_EVENT":
        question_ref = _exact(node.get("question_semantic_ref"), "question_semantic_ref")
        _exact(node.get("component_or_event_selector_ref"), "component_or_event_selector_ref")
        _exact(node.get("response_value_or_state_ref"), "response_value_or_state_ref")
        topo_auth = _authority(node.get("response_topology_authority_ref"),
                               "response_topology_authority_ref")
        response_auth = _authority(node.get("response_semantic_authority_ref"),
                                   "response_semantic_authority_ref")
        for ref in (topo_auth, response_auth):
            if registry.resolve_exact(ref).snapshot.typed_state != "ALLOW":
                raise Pre553AuthorityError("response predicate authority is not positive")
        operator = node.get("operator")
        if operator not in {"EQ", "IN", "STATE_EQ"}:
            raise EmpiricalQueryResolutionError("response predicate operator must be EQ/IN/STATE_EQ")
        values = _leaf_exact_values(node, exact_ref_field="response_value_or_state_ref") if operator != "STATE_EQ" else ()
        events = [e for e in index.events_by_respondent[respondent_key] if _question_matches(e, question_ref)]
        result = False
        for event in events:
            if response_auth not in event.authority_snapshot_refs or topo_auth not in event.authority_snapshot_refs:
                raise Pre553AuthorityError("predicate response/topology authority does not bind matched C11 event")
            used.append(event)
            used_auth.extend(_validate_public_object_authorities(event, registry))
            if operator == "STATE_EQ":
                result = result or event.typed_state == node.get("typed_state")
            else:
                result = result or canonicalize(_semantic_value(event)) in values
        return result

    if leaf_type == "ROUTING_APPLICABILITY_STATE":
        question_ref = _exact(node.get("question_semantic_ref"), "question_semantic_ref")
        _exact(node.get("routing_or_applicability_state_ref"), "routing_or_applicability_state_ref")
        routing_auth = _authority(node.get("routing_authority_ref"), "routing_authority_ref")
        if registry.resolve_exact(routing_auth).snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("routing predicate authority is not positive")
        desired = node.get("routing_state")
        if desired is None:
            raise EmpiricalQueryResolutionError("routing predicate requires exact routing_state")
        result = False
        for fact in index.routing_by_respondent[respondent_key]:
            if not _question_matches(fact, question_ref):
                continue
            if routing_auth not in fact.authority_snapshot_refs:
                raise Pre553AuthorityError("routing predicate authority does not bind matched C11 fact")
            used.append(fact)
            used_auth.extend(_validate_public_object_authorities(fact, registry))
            result = result or fact.routing_state == desired or fact.applicability_state == desired
        return result

    if leaf_type == "TYPED_RESPONSE_STATE":
        question_ref = _exact(node.get("question_semantic_ref"), "question_semantic_ref")
        _exact(node.get("typed_state_ref"), "typed_state_ref")
        state_auth = _authority(node.get("state_semantic_authority_ref"),
                                "state_semantic_authority_ref")
        if registry.resolve_exact(state_auth).snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("typed-response-state authority is not positive")
        desired = node.get("typed_state")
        if desired is None:
            raise EmpiricalQueryResolutionError("typed response predicate requires typed_state")
        result = False
        for event in index.events_by_respondent[respondent_key]:
            if not _question_matches(event, question_ref):
                continue
            if state_auth not in event.authority_snapshot_refs:
                raise Pre553AuthorityError("typed-state authority does not bind matched C11 event")
            used.append(event)
            used_auth.extend(_validate_public_object_authorities(event, registry))
            result = result or event.typed_state == desired
        return result

    if leaf_type == "DERIVED_BRANCH_COHORT":
        branch_id = node.get("branch_definition_id")
        if not isinstance(branch_id, str) or not branch_id.strip():
            raise EmpiricalQueryResolutionError("branch_definition_id is required")
        membership_ref = _exact(node.get("resolved_predicate_hash_or_exact_membership_ref"),
                                "resolved_predicate_hash_or_exact_membership_ref")
        _exact(node.get("parent_ancestry_ref"), "parent_ancestry_ref")
        branch_auth = _authority(node.get("branch_algorithm_authority_ref"),
                                 "branch_algorithm_authority_ref")
        _exact(node.get("branch_membership_replay_ref"), "branch_membership_replay_ref")
        _exact(node.get("branch_source_scope_ref"), "branch_source_scope_ref")
        if registry.resolve_exact(branch_auth).snapshot.typed_state != "ALLOW":
            raise Pre553AuthorityError("branch predicate authority is not positive")
        if derived_branch_memberships is not None and membership_ref in derived_branch_memberships:
            member_refs = derived_branch_memberships[membership_ref]
        else:
            member_values = _require_sequence(node.get("exact_member_respondent_refs"),
                                              "exact_member_respondent_refs", allow_empty=True)
            member_refs = frozenset(
                _canonical_refs(_exact(v, "branch member ref") for v in member_values)
            )
        used_auth.append(branch_auth)
        return respondent.ref in member_refs

    raise Pre553SemanticCollapseError("unknown or forbidden empirical predicate leaf")


_COMPILED_BRANCH_MEMBERSHIP_CACHE: dict[int, tuple[Mapping[str, Any], dict[ExactRef, frozenset[ExactRef]]]] = {}


def _compile_derived_branch_memberships(
    node: Mapping[str, Any],
) -> dict[ExactRef, frozenset[ExactRef]]:
    """Compile exact derived-cohort membership once for one verified predicate AST.

    The predicate's semantic identity is verified before evaluation.  This cache is
    execution-local and nonauthoritative: it only avoids reparsing/re-sorting the
    same immutable exact member refs for every respondent and every query that
    shares one verified predicate object.
    """
    cached = _COMPILED_BRANCH_MEMBERSHIP_CACHE.get(id(node))
    if cached is not None and cached[0] is node:
        return cached[1]
    compiled: dict[ExactRef, frozenset[ExactRef]] = {}

    def walk(raw: Mapping[str, Any]) -> None:
        op = raw.get("op")
        if op == "LEAF":
            if raw.get("leaf_type") != "DERIVED_BRANCH_COHORT":
                return
            membership_ref = _exact(
                raw.get("resolved_predicate_hash_or_exact_membership_ref"),
                "resolved_predicate_hash_or_exact_membership_ref",
            )
            member_values = _require_sequence(
                raw.get("exact_member_respondent_refs"),
                "exact_member_respondent_refs",
                allow_empty=True,
            )
            member_refs = frozenset(
                _canonical_refs(_exact(v, "branch member ref") for v in member_values)
            )
            prior = compiled.get(membership_ref)
            if prior is not None and prior != member_refs:
                raise EmpiricalQueryResolutionError(
                    "one exact derived-branch membership ref resolves to conflicting member sets"
                )
            compiled[membership_ref] = member_refs
            return
        children = raw.get("children")
        if children is None:
            return
        for child in _require_sequence(children, f"{op} children", allow_empty=False):
            walk(_require_mapping(child, f"{op} child"))

    walk(node)
    _COMPILED_BRANCH_MEMBERSHIP_CACHE[id(node)] = (node, compiled)
    return compiled


def _eval_predicate(
    node: Mapping[str, Any],
    *,
    respondent: RespondentIdentity,
    index: _ReleaseIndex,
    registry: AuthorityRegistry,
    used: list[CanonicalSemanticObject | C11InternalRecord],
    used_auth: list[AuthorityRef],
    derived_branch_memberships: Mapping[ExactRef, frozenset[ExactRef]] | None = None,
) -> bool:
    op = node.get("op")
    if op == "LEAF":
        return _leaf_match(
            node, respondent=respondent, index=index, registry=registry,
            used=used, used_auth=used_auth,
            derived_branch_memberships=derived_branch_memberships,
        )
    if op == "NOT":
        children = _require_sequence(node.get("children"), "NOT children")
        if len(children) != 1:
            raise EmpiricalQueryResolutionError("NOT requires exactly one child")
        return not _eval_predicate(
            _require_mapping(children[0], "NOT child"),
            respondent=respondent, index=index, registry=registry,
            used=used, used_auth=used_auth,
            derived_branch_memberships=derived_branch_memberships,
        )
    if op in {"AND", "OR"}:
        children = _require_sequence(node.get("children"), f"{op} children")
        values = [
            _eval_predicate(
                _require_mapping(child, f"{op} child"), respondent=respondent,
                index=index, registry=registry, used=used, used_auth=used_auth,
                derived_branch_memberships=derived_branch_memberships,
            )
            for child in children
        ]
        return all(values) if op == "AND" else any(values)
    raise EmpiricalQueryResolutionError("predicate op must be AND/OR/NOT/LEAF")


__all__ = ["_build_release_index", "_eval_predicate", "_question_matches", "_validate_public_object_authorities"]
