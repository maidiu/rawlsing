import hashlib
from dataclasses import replace

import pytest

from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
    assert_zero_actor_v3_v2_effect,
    make_empirical_predicate,
)
from rawlsing_next.pre553_empirical_query import (
    EmpiricalQueryExecutionError,
    EmpiricalQueryResolutionError,
    execute_empirical_query,
    replay_empirical_query,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:i03:{kind.lower()}:{tag}", _h(f"i03:{kind}:{tag}"))


def _auth(tag: str, kind: str, *, families) -> AuthoritySnapshot:
    digest = _h(f"i03-authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"I03-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"I03-OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"i03-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _query_authority(tag: str = "query") -> AuthoritySnapshot:
    return _auth(
        tag,
        "PREDICATE_GRAMMAR",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    )


def _build_source(
    tag: str,
    rows,
    *,
    question_namespace: str = "shared",
    risk_sets=None,
    weights=None,
    reverse_sections: bool = False,
    risk_namespace: str | None = None,
    topology_by_question=None,
    nonmember_routing_state: str = "NOT_ELIGIBLE",
):
    source_auth = _auth(
        f"source-{tag}",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    routing_auth = _auth(
        f"routing-{tag}", "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    coord_auth = _auth(
        f"coord-{tag}", "COORDINATE_SEMANTICS",
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    replay_auth = _auth(
        f"replay-{tag}", "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    weight_auth = (
        _auth(f"weight-{tag}", "WEIGHT_DESIGN_ESTIMAND", families=("WeightMeasureFact@1.0.0",))
        if weights is not None else None
    )
    authorities = (source_auth, coord_auth, routing_auth, replay_auth) + ((weight_auth,) if weight_auth else ())
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{tag}"),
        raw_source_identity=f"RAW-{tag}",
        source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1",
        instrument_release=f"INST-{tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-I03",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    question_names = sorted({q for row in rows for q in row.get("responses", {})})
    coordinate_names = sorted({c for row in rows for c in row.get("coords", {})})
    qrefs = {q: _ref("QUESTION_NATIVE", f"{question_namespace}-{q}") for q in question_names}
    crefs = {c: _ref("COORDINATE_NATIVE", f"{question_namespace}-{c}") for c in coordinate_names}
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[q],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for q in question_names
    )
    respondents = []
    respondent_by_id = {}
    for row in rows:
        respondent = RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=row["id"],
            source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{tag}-{row['id']}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        respondents.append(respondent)
        respondent_by_id[row["id"]] = respondent

    if risk_sets is None:
        risk_sets = {"R": {q: {row["id"] for row in rows} for q in question_names}}
    routing = []
    for risk_name, per_question in sorted(risk_sets.items()):
        risk_ref = _ref("RISK_SET", f"{risk_namespace or tag}-{risk_name}")
        for row in rows:
            respondent = respondent_by_id[row["id"]]
            for q in question_names:
                members = per_question.get(q, set())
                state = "ELIGIBLE_APPLICABLE" if row["id"] in members else nonmember_routing_state
                routing.append(RoutingEligibilityFact(
                    typed_state=state,
                    authority_snapshot_refs=(routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT", f"routing-{tag}-{risk_name}-{row['id']}-{q}"
                    ),
                    empirical_universe_ref=universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=qrefs[q],
                    risk_set_ref=risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{risk_name}-{q}"),
                    applicability_state=state,
                    routing_state=state,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{tag}-{risk_name}-{q}-{'-'.join(sorted(members)) or 'EMPTY'}"
                    ),
                ))

    events = []
    coordinates = []
    weight_facts = []
    for row in rows:
        respondent = respondent_by_id[row["id"]]
        for q, value in sorted(row.get("responses", {}).items()):
            topology_kind = (topology_by_question or {}).get(q, "SCALAR_SINGULAR")
            events.append(RespondentEvent(
                typed_state="SUBSTANTIVE_RESPONSE",
                authority_snapshot_refs=(source_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"event-{tag}-{row['id']}-{q}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_question_ref=qrefs[q],
                canonical_question_ref_if_authorized=None,
                component_or_subitem_ref=None,
                event_group_id=f"GROUP-{tag}-{row['id']}-{q}",
                response_event_id_or_deterministic_index=f"{row['id']}-{q}",
                raw_response_value=str(value),
                canonical_response_value_if_authorized=None,
                value_transform_authority_ref=None,
                response_topology_ref=_ref("TOPOLOGY", f"{question_namespace}-{q}-{topology_kind}"),
                multiplicity_order_rank_fields={"kind": topology_kind, "index": 0},
                response_state="SUBSTANTIVE_RESPONSE",
            ))
        for coord, value in sorted(row.get("coords", {}).items()):
            coordinates.append(EmpiricalCoordinateFact(
                typed_state="OBSERVED_COORDINATE",
                authority_snapshot_refs=(coord_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"coord-{tag}-{row['id']}-{coord}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_coordinate_ref=crefs[coord],
                canonical_coordinate_ref_if_authorized=None,
                raw_coordinate_value=str(value),
                canonical_coordinate_value_if_authorized=None,
                unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{question_namespace}-{coord}"),
                effective_or_reference_time="2026-01",
                coordinate_state="OBSERVED_COORDINATE",
                normalization_crosswalk_authority_ref=None,
                source_semantic_authority_ref=coord_auth.authority_ref,
            ))
        if weights is not None:
            state, value = weights[row["id"]]
            weight_facts.append(WeightMeasureFact(
                typed_state=state,
                authority_snapshot_refs=(weight_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"weight-{tag}-{row['id']}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                weight_basis_id="W",
                exact_weight_value_representation=value,
                weight_state=state,
                weight_source_ref=_ref("WEIGHT_SOURCE", f"{tag}-W"),
                design_authority_ref=weight_auth.authority_ref,
                estimand_authority_ref=weight_auth.authority_ref,
                normalization_or_recalibration_rule_ref=None,
                effective_scope_ref=_ref("SCOPE", f"{tag}-W"),
            ))

    if not coordinates:
        crefs["INERT"] = _ref("COORDINATE_NATIVE", f"{question_namespace}-INERT")
        for row in rows:
            respondent = respondent_by_id[row["id"]]
            coordinates.append(EmpiricalCoordinateFact(
                typed_state="OBSERVED_COORDINATE",
                authority_snapshot_refs=(coord_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"coord-{tag}-{row['id']}-INERT"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_coordinate_ref=crefs["INERT"],
                canonical_coordinate_ref_if_authorized=None,
                raw_coordinate_value="1",
                canonical_coordinate_value_if_authorized=None,
                unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{question_namespace}-INERT"),
                effective_or_reference_time="2026-01",
                coordinate_state="OBSERVED_COORDINATE",
                normalization_crosswalk_authority_ref=None,
                source_semantic_authority_ref=coord_auth.authority_ref,
            ))

    if reverse_sections:
        respondents = list(reversed(respondents))
        events = list(reversed(events))
        routing = list(reversed(routing))
        coordinates = list(reversed(coordinates))
        weight_facts = list(reversed(weight_facts))

    source_hash = _h(f"source-artifact:{tag}")
    counts = {
        "EmpiricalUniverse": 1,
        "RespondentIdentity": len(respondents),
        "QuestionVariableBinding": len(questions),
        "RespondentEvent": len(events),
        "RoutingEligibilityFact": len(routing),
        "EmpiricalCoordinateFact": len(coordinates),
        "WeightMeasureFact": len(weight_facts),
        "AuthoritySnapshot": len(authorities),
        "SourceUniverseRelation": 0,
        "EmpiricalPredicateReplayBinding": 0,
        "ComparatorReplayBinding": 0,
        "DiscoveryBranchReplayBinding": 0,
        "StructuralAdmissionReplayBinding": 0,
        "ReplayManifest": 1,
    }
    manifest = SourceReleaseManifest(
        source_artifact_id=f"SOURCE-{tag}",
        source_artifact_content_hash=source_hash,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}",
        instrument_release_id=f"INST-{tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:i03:source-snapshot:{tag}", source_hash
        ),
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        empirical_universes=(universe,),
        respondent_identities=tuple(respondents),
        question_variable_bindings=questions,
        respondent_events=tuple(events),
        routing_eligibility_facts_or_exact_rules=tuple(routing),
        empirical_coordinate_facts=tuple(coordinates),
        weight_measure_facts_or_typed_absence=(
            tuple(weight_facts) if weights is not None else TypedAbsence("NOT_APPLICABLE")
        ),
        authority_snapshots=authorities,
        source_universe_relations_or_explicit_distinct_default=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence("NOT_APPLICABLE"),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=replay_auth.authority_ref,
        deterministic_tie_order_rules_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    assert result.accepted, result.errors
    return {
        "repo": repo,
        "release_ref": result.release_ref,
        "universe": universe,
        "respondents": respondent_by_id,
        "qrefs": qrefs,
        "crefs": crefs,
        "risk_refs": {name: _ref("RISK_SET", f"{risk_namespace or tag}-{name}") for name in risk_sets},
        "source_auth": source_auth,
        "coord_auth": coord_auth,
        "routing_auth": routing_auth,
        "weight_auth": weight_auth,
        "authorities": authorities,
    }


def _registry(source, *extra):
    return AuthorityRegistry((*source["authorities"], *extra))


def _branch_predicate(source, qauth, members=None, *, tag="all"):
    if members is None:
        members = tuple(source["respondents"].values())
    refs = tuple(sorted((member.ref for member in members), key=lambda ref: ref.key))
    membership = _ref("BRANCH_MEMBERSHIP", f"{tag}-{_h('|'.join(ref.key for ref in refs))[:12]}")
    ast = {
        "op": "LEAF",
        "leaf_type": "DERIVED_BRANCH_COHORT",
        "branch_definition_id": f"BRANCH-{tag}",
        "resolved_predicate_hash_or_exact_membership_ref": membership,
        "parent_ancestry_ref": _ref("BRANCH_PARENT", tag),
        "branch_algorithm_authority_ref": qauth.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", tag),
        "branch_source_scope_ref": source["universe"].ref,
        "exact_member_respondent_refs": refs,
    }
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"predicate-{tag}"),
        grammar_authority_ref=qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(source["risk_refs"].values()),
        scope_refs=(source["universe"].ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _response_leaf(source, qauth, q, value):
    return {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": source["qrefs"][q],
        "component_or_event_selector_ref": _ref("EVENT_SELECTOR", f"{q}-ANY"),
        "response_value_or_state_ref": _ref("VALUE_REF", f"{q}-{value}"),
        "response_topology_authority_ref": source["source_auth"].authority_ref,
        "response_semantic_authority_ref": source["source_auth"].authority_ref,
        "operator": "EQ",
        "exact_value": str(value),
    }


def _coordinate_leaf(source, coord, value):
    return {
        "op": "LEAF",
        "leaf_type": "EMPIRICAL_POSITION_COORDINATE",
        "coordinate_semantic_ref": source["crefs"][coord],
        "value_or_value_set_ref": _ref("VALUE_REF", f"{coord}-{value}"),
        "comparison_operator_ref": _ref("COMPARISON_OPERATOR", "EQ"),
        "typed_state_policy_ref": _ref("STATE_POLICY", "OBSERVED_ONLY"),
        "coordinate_authority_ref": source["coord_auth"].authority_ref,
        "operator": "EQ",
        "exact_value": str(value),
    }


def _predicate(source, qauth, ast, *, tag):
    return make_empirical_predicate(
        predicate_ast=ast,
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"predicate-{tag}"),
        grammar_authority_ref=qauth.authority_ref,
        coordinate_question_value_refs=(),
        risk_set_refs=tuple(source["risk_refs"].values()),
        scope_refs=(source["universe"].ref,),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )


def _query(
    source,
    qauth,
    predicate,
    targets,
    *,
    risk="R",
    measure="RAW",
    source_mode="SINGLE_UNIVERSE",
    universe_refs=None,
    tag="q",
    diagnostic_kind=None,
    target_authority_refs=None,
):
    if universe_refs is None:
        universe_refs = (source["universe"].ref,)
    if target_authority_refs is None:
        target_authority_refs = (source["source_auth"].authority_ref,)
    components = [
        {
            "target_ref": source["qrefs"][target],
            "topology": "SCALAR_SINGULAR",
            "domain": ["0", "1"],
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{target}-01"),
            "topology_authority_refs": list(target_authority_refs),
            "response_semantic_authority_refs": list(target_authority_refs),
            "included_states": ["SUBSTANTIVE_RESPONSE"],
        }
        for target in targets
    ]
    grain = {
        "source_scope_mode": source_mode,
        "measure_kind": measure,
        "risk_set_type": "COMMON_ELIGIBLE_RISK_SET" if len(targets) > 1 else "WHOLE_QUESTION_RISK_SET",
        "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
        "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
    }
    if measure == "GOVERNED_WEIGHTED":
        grain["weight_basis_id"] = "W"
    if diagnostic_kind is not None:
        grain["diagnostic_kind"] = diagnostic_kind
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=tuple(source["qrefs"][target] for target in targets),
        target_arity_and_topology={
            "arity": len(targets),
            "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": components,
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=source["risk_refs"][risk],
        empirical_universe_refs=tuple(universe_refs),
        scope_refs=tuple(universe_refs),
        measure_basis_ref=_ref("MEASURE_BASIS", measure),
        requested_output_grain=grain,
        query_authority_refs=(qauth.authority_ref,),
    )


def _cell_map(fact):
    return {
        row["cell"] if isinstance(row["cell"], str) else tuple(row["cell"]): row
        for row in fact.target_topology["complete_cell_semantic_projection"]
    }


def _run(source, qauth, predicate, query, *, registry=None):
    if registry is None:
        registry = _registry(source, qauth)
    return execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )


def test_unary_distribution_and_observed_zero_are_exact():
    source = _build_source("unary", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa = _query_authority("unary")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",), tag="unary")
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "SUPPORTED"
    cells = _cell_map(fact)
    assert cells["0"]["raw_numerator_support"] == 2
    assert cells["1"]["raw_numerator_support"] == 0
    assert cells["1"]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"


def test_observed_zero_is_not_zero_support():
    source = _build_source("zero", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa = _query_authority("zero")
    full = _branch_predicate(source, qa, tag="full")
    empty = _branch_predicate(source, qa, members=(), tag="empty")
    observed = _run(source, qa, full, _query(source, qa, full, ("Y",), tag="observed")).facts[0]
    zero_support = _run(source, qa, empty, _query(source, qa, empty, ("Y",), tag="support0")).facts[0]
    assert observed.typed_state == "SUPPORTED"
    assert _cell_map(observed)["1"]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    assert zero_support.typed_state == "ZERO_SUPPORT"
    assert zero_support.raw_denominator_support == 0
    assert observed.ref != zero_support.ref


def test_arbitrary_coordinate_conjunction_and_response_position_condition():
    source = _build_source("conjunction", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A", "H": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A", "H": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B", "H": 1}},
    ])
    qa = _query_authority("conjunction")
    coord_ast = {"op": "AND", "children": [_coordinate_leaf(source, "G", "A"), _coordinate_leaf(source, "H", 1)]}
    coord_pred = _predicate(source, qa, coord_ast, tag="coords")
    coord_fact = _run(source, qa, coord_pred, _query(source, qa, coord_pred, ("Y",), tag="coords")).facts[0]
    assert coord_fact.raw_denominator_support == 1
    assert _cell_map(coord_fact)["1"]["raw_numerator_support"] == 1

    rp_ast = {"op": "AND", "children": [_response_leaf(source, qa, "X", 1), _coordinate_leaf(source, "G", "A")]}
    rp_pred = _predicate(source, qa, rp_ast, tag="response-position")
    rp_fact = _run(source, qa, rp_pred, _query(source, qa, rp_pred, ("Y",), tag="response-position")).facts[0]
    assert rp_fact.raw_denominator_support == 1
    assert _cell_map(rp_fact)["1"]["raw_numerator_support"] == 1


def test_response_response_xor_uses_same_respondent_incidence():
    source = _build_source("xor", [
        {"id": "R00", "responses": {"X": 0, "Y": 0, "Z": 0}},
        {"id": "R01", "responses": {"X": 0, "Y": 1, "Z": 1}},
        {"id": "R10", "responses": {"X": 1, "Y": 0, "Z": 1}},
        {"id": "R11", "responses": {"X": 1, "Y": 1, "Z": 0}},
    ])
    qa = _query_authority("xor")
    x = _response_leaf(source, qa, "X", 1)
    y = _response_leaf(source, qa, "Y", 1)
    ast = {"op": "AND", "children": [
        {"op": "OR", "children": [x, y]},
        {"op": "NOT", "children": [{"op": "AND", "children": [x, y]}]},
    ]}
    pred = _predicate(source, qa, ast, tag="xor")
    fact = _run(source, qa, pred, _query(source, qa, pred, ("Z",), tag="xor")).facts[0]
    assert fact.raw_denominator_support == 2
    cells = _cell_map(fact)
    assert cells["1"]["raw_numerator_support"] == 2
    assert cells["0"]["raw_numerator_support"] == 0


def test_k_way_parity_full_joint_is_not_pairwise_or_unary_synthesis():
    source = _build_source("parity", [
        {"id": f"R{x}{y}", "responses": {"X": x, "Y": y, "Z": x ^ y}}
        for x in (0, 1) for y in (0, 1)
    ])
    qa = _query_authority("parity")
    pred = _branch_predicate(source, qa)
    fact = _run(source, qa, pred, _query(source, qa, pred, ("X", "Y", "Z"), tag="parity")).facts[0]
    cells = _cell_map(fact)
    assert fact.raw_denominator_support == 4
    assert len(cells) == 8
    for x in (0, 1):
        for y in (0, 1):
            z = x ^ y
            assert cells[(str(x), str(y), str(z))]["raw_numerator_support"] == 1
            assert cells[(str(x), str(y), str(1 - z))]["raw_numerator_support"] == 0


def test_same_marginals_different_joint_are_distinct_source_indexed_facts():
    left = _build_source("joint-left", [
        {"id": "R1", "responses": {"X": 0, "Y": 0}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
        {"id": "R3", "responses": {"X": 1, "Y": 1}},
        {"id": "R4", "responses": {"X": 1, "Y": 1}},
    ], question_namespace="joint-shared", risk_namespace="joint-shared")
    right = _build_source("joint-right", [
        {"id": "R1", "responses": {"X": 0, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 1}},
        {"id": "R3", "responses": {"X": 1, "Y": 0}},
        {"id": "R4", "responses": {"X": 1, "Y": 0}},
    ], question_namespace="joint-shared", risk_namespace="joint-shared")
    repo = C11Repository((
        left["repo"].resolve_release_exact(left["release_ref"]),
        right["repo"].resolve_release_exact(right["release_ref"]),
    ))
    qa = _query_authority("joint-multi")
    members = tuple(left["respondents"].values()) + tuple(right["respondents"].values())
    refs = tuple(sorted((member.ref for member in members), key=lambda ref: ref.key))
    ast = {
        "op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT", "branch_definition_id": "ALL-SOURCES",
        "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", "all-sources"),
        "parent_ancestry_ref": _ref("BRANCH_PARENT", "all-sources"),
        "branch_algorithm_authority_ref": qa.authority_ref,
        "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "all-sources"),
        "branch_source_scope_ref": _ref("SOURCE_SCOPE", "joint-multi"),
        "exact_member_respondent_refs": refs,
    }
    pred = make_empirical_predicate(
        predicate_ast=ast, typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qa.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "predicate-joint-multi"),
        grammar_authority_ref=qa.authority_ref, coordinate_question_value_refs=(),
        risk_set_refs=(left["risk_refs"]["R"],),
        scope_refs=(left["universe"].ref, right["universe"].ref),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    query = _query(
        left, qa, pred, ("X", "Y"), source_mode="SOURCE_INDEXED_MULTI_UNIVERSE",
        universe_refs=(left["universe"].ref, right["universe"].ref), tag="joint-multi",
        target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref),
    )
    registry = AuthorityRegistry((*left["authorities"], *right["authorities"], qa))
    result = execute_empirical_query(
        repository=repo, query=query, predicate=pred, authority_registry=registry,
        release_refs=(left["release_ref"], right["release_ref"]),
    )
    assert len(result.facts) == 2
    by_universe = {fact.empirical_universe_refs[0]["object_id"]: fact for fact in result.facts}
    lf = by_universe[left["universe"].object_id]
    rf = by_universe[right["universe"].object_id]
    assert lf.ref != rf.ref
    assert _cell_map(lf)[("0", "0")]["raw_numerator_support"] == 2
    assert _cell_map(rf)[("0", "0")]["raw_numerator_support"] == 0
    assert sum(_cell_map(lf)[cell]["raw_numerator_support"] for cell in (("0", "0"), ("0", "1"))) == 2
    assert sum(_cell_map(rf)[cell]["raw_numerator_support"] for cell in (("0", "0"), ("0", "1"))) == 2


def test_equal_denominator_counts_different_risk_member_sets_do_not_collapse():
    rows = [{"id": f"R{i}", "responses": {"Y": i % 2}} for i in range(1, 5)]
    risk_sets = {
        "R": {"Y": {"R1", "R2"}},
        "S": {"Y": {"R3", "R4"}},
    }
    source = _build_source("risk-identity", rows, risk_sets=risk_sets)
    qa = _query_authority("risk-identity")
    pred = _branch_predicate(source, qa)
    q1 = _query(source, qa, pred, ("Y",), risk="R", tag="risk-r")
    q2 = _query(source, qa, pred, ("Y",), risk="S", tag="risk-s")
    f1 = _run(source, qa, pred, q1).facts[0]
    f2 = _run(source, qa, pred, q2).facts[0]
    assert f1.raw_denominator_support == f2.raw_denominator_support == 2
    assert f1.denominator_member_refs != f2.denominator_member_refs
    assert f1.ref != f2.ref


def test_routed_common_eligibility_zero_overlap_is_typed():
    rows = [
        {"id": "R1", "responses": {"X": 0, "Y": 0}},
        {"id": "R2", "responses": {"X": 1, "Y": 1}},
        {"id": "R3", "responses": {"X": 0, "Y": 1}},
        {"id": "R4", "responses": {"X": 1, "Y": 0}},
    ]
    risk_sets = {"R": {"X": {"R1", "R2"}, "Y": {"R3", "R4"}}}
    source = _build_source("zero-overlap", rows, risk_sets=risk_sets)
    qa = _query_authority("zero-overlap")
    pred = _branch_predicate(source, qa)
    fact = _run(source, qa, pred, _query(source, qa, pred, ("X", "Y"), tag="zero-overlap")).facts[0]
    assert fact.typed_state == "ZERO_OVERLAP"
    assert fact.raw_denominator_support == 0


def test_raw_and_authorized_weighted_measure_are_distinct_exact_facts():
    rows = [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ]
    source = _build_source(
        "weighted", rows,
        weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "1"), "R2": ("WEIGHT_VALID_AUTHORIZED", "1")},
    )
    qa = _query_authority("weighted")
    pred = _branch_predicate(source, qa)
    raw = _run(source, qa, pred, _query(source, qa, pred, ("Y",), measure="RAW", tag="raw")).facts[0]
    weighted = _run(source, qa, pred, _query(source, qa, pred, ("Y",), measure="GOVERNED_WEIGHTED", tag="weighted")).facts[0]
    assert raw.ref != weighted.ref
    assert raw.measure_kind == "RAW"
    assert weighted.measure_kind == "GOVERNED_WEIGHTED"
    assert weighted.weighted_denominator_support_if_authorized == {"$exact_fraction": [2, 1]}


def test_missing_or_invalid_weight_fails_closed_without_default_one():
    rows = [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
    ]
    source = _build_source(
        "weight-missing", rows,
        weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "2"), "R2": ("WEIGHT_MISSING", None)},
    )
    qa = _query_authority("weight-missing")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",), measure="GOVERNED_WEIGHTED", tag="weight-missing")
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.p02_failure_state == "MEASURE_UNAVAILABLE"
    assert fact.raw_denominator_support == 0


def test_branch_cohort_membership_is_exact_and_replayable():
    source = _build_source("branch", [
        {"id": "R1", "responses": {"Y": 0}},
        {"id": "R2", "responses": {"Y": 1}},
        {"id": "R3", "responses": {"Y": 1}},
    ])
    qa = _query_authority("branch")
    members = (source["respondents"]["R1"], source["respondents"]["R3"])
    pred = _branch_predicate(source, qa, members=members, tag="selected")
    fact = _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="branch-selected")).facts[0]
    assert fact.raw_denominator_support == 2
    assert tuple(sorted(ref["object_id"] for ref in fact.denominator_member_refs)) == tuple(
        sorted(member.ref.object_id for member in members)
    )


def _rate(fact):
    cells = _cell_map(fact)
    return cells["1"]["raw_numerator_support"], fact.raw_denominator_support


def test_simpson_reversal_preserves_pooled_and_conditioned_query_identity():
    rows = []
    for i in range(3): rows.append({"id": f"A1-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "A"}})
    for i in range(8): rows.append({"id": f"A0s-{i}", "responses": {"X": 0, "Y": 1}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"A0f-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "A"}})
    for i in range(2): rows.append({"id": f"B1s-{i}", "responses": {"X": 1, "Y": 1}, "coords": {"G": "B"}})
    for i in range(8): rows.append({"id": f"B1f-{i}", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}})
    for i in range(2): rows.append({"id": f"B0-{i}", "responses": {"X": 0, "Y": 0}, "coords": {"G": "B"}})
    source = _build_source("simpson", rows)
    qa = _query_authority("simpson")

    def fact_for(x, group=None):
        children = [_response_leaf(source, qa, "X", x)]
        if group is not None:
            children.append(_coordinate_leaf(source, "G", group))
        ast = children[0] if len(children) == 1 else {"op": "AND", "children": children}
        pred = _predicate(source, qa, ast, tag=f"x{x}-{group or 'pool'}")
        return _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag=f"x{x}-{group or 'pool'}")).facts[0]

    p1, p0 = fact_for(1), fact_for(0)
    a1, a0 = fact_for(1, "A"), fact_for(0, "A")
    b1, b0 = fact_for(1, "B"), fact_for(0, "B")
    assert _rate(p1) == (5, 13) and _rate(p0) == (8, 12)
    assert _rate(a1) == (3, 3) and _rate(a0) == (8, 10)
    assert _rate(b1) == (2, 10) and _rate(b0) == (0, 2)
    assert p1.ref != a1.ref != b1.ref


def test_storage_order_permutations_replay_identically():
    rows = [
        {"id": "R1", "responses": {"X": 0, "Y": 1}, "coords": {"G": "A"}},
        {"id": "R2", "responses": {"X": 1, "Y": 0}, "coords": {"G": "B"}},
    ]
    left = _build_source("order", rows, reverse_sections=False)
    right = _build_source("order", list(reversed(rows)), reverse_sections=True)
    assert left["release_ref"] == right["release_ref"]
    qa = _query_authority("order")
    lp = _branch_predicate(left, qa)
    rp = _branch_predicate(right, qa)
    assert lp.ref == rp.ref
    lq = _query(left, qa, lp, ("X", "Y"), tag="order")
    rq = _query(right, qa, rp, ("X", "Y"), tag="order")
    assert lq.ref == rq.ref
    lf = _run(left, qa, lp, lq).facts[0]
    rf = _run(right, qa, rp, rq).facts[0]
    assert lf.ref == rf.ref


def test_tampered_query_predicate_or_replay_reference_fails_closed():
    source = _build_source("tamper", [
        {"id": "R1", "responses": {"Y": 1}},
        {"id": "R2", "responses": {"Y": 0}},
    ])
    qa = _query_authority("tamper")
    pred = _branch_predicate(source, qa, tag="original")
    query = _query(source, qa, pred, ("Y",), tag="original")
    tampered = _branch_predicate(source, qa, tag="tampered-replay")
    with pytest.raises(EmpiricalQueryResolutionError):
        _run(source, qa, tampered, query)
    result = _run(source, qa, pred, query)
    with pytest.raises(EmpiricalQueryExecutionError):
        replay_empirical_query(
            repository=source["repo"], query=query, predicate=pred,
            authority_registry=_registry(source, qa), release_refs=(source["release_ref"],),
            expected_fact_refs=(_ref("EmpiricalFact@1.0.0", "wrong"),),
        )
    assert result.facts


def test_diagnostic_score_cannot_masquerade_as_empirical_fact():
    source = _build_source("diagnostic", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("diagnostic")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",), tag="diagnostic", diagnostic_kind="MI")
    with pytest.raises(Pre553SemanticCollapseError):
        _run(source, qa, pred, query)


def test_query_execution_has_zero_structural_actor_v3_v2_effect():
    source = _build_source("noncollapse", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("noncollapse")
    pred = _branch_predicate(source, qa)
    fact = _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="noncollapse")).facts[0]
    assert_zero_actor_v3_v2_effect(fact)
    forbidden = {"structural_interpretation_payload", "actor_state_effect", "v3_state_effect", "v2_state_effect", "persona_effect", "belief_effect"}
    assert forbidden.isdisjoint(fact.semantic_fields)


def test_authorized_composite_without_exact_relation_bundle_is_noncomparable():
    left = _build_source(
        "composite-left", [{"id": "L1", "responses": {"Y": 1}}],
        question_namespace="composite-shared", risk_namespace="composite-shared",
    )
    right = _build_source(
        "composite-right", [{"id": "R1", "responses": {"Y": 0}}],
        question_namespace="composite-shared", risk_namespace="composite-shared",
    )
    repo = C11Repository((
        left["repo"].resolve_release_exact(left["release_ref"]),
        right["repo"].resolve_release_exact(right["release_ref"]),
    ))
    qa = _query_authority("composite")
    members = tuple(left["respondents"].values()) + tuple(right["respondents"].values())
    refs = tuple(sorted((member.ref for member in members), key=lambda ref: ref.key))
    pred = make_empirical_predicate(
        predicate_ast={
            "op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT",
            "branch_definition_id": "COMPOSITE-ALL",
            "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", "composite-all"),
            "parent_ancestry_ref": _ref("BRANCH_PARENT", "composite-all"),
            "branch_algorithm_authority_ref": qa.authority_ref,
            "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "composite-all"),
            "branch_source_scope_ref": _ref("SOURCE_SCOPE", "composite-all"),
            "exact_member_respondent_refs": refs,
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qa.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "predicate-composite"),
        grammar_authority_ref=qa.authority_ref, coordinate_question_value_refs=(),
        risk_set_refs=(left["risk_refs"]["R"],),
        scope_refs=(left["universe"].ref, right["universe"].ref),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    query = _query(
        left, qa, pred, ("Y",), source_mode="AUTHORIZED_COMPOSITE",
        universe_refs=(left["universe"].ref, right["universe"].ref), tag="composite",
        target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref),
    )
    registry = AuthorityRegistry((*left["authorities"], *right["authorities"], qa))
    fact = execute_empirical_query(
        repository=repo, query=query, predicate=pred, authority_registry=registry,
        release_refs=(left["release_ref"], right["release_ref"]),
    ).facts[0]
    assert fact.typed_state == "NONCOMPARABLE"
    assert fact.p02_failure_state == "UNRESOLVED_SOURCE_RELATION"


def test_unsupported_response_topology_is_typed_unresolved_not_collapsed():
    source = _build_source("unsupported-topology", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("unsupported-topology")
    pred = _branch_predicate(source, qa)
    base = _query(source, qa, pred, ("Y",), tag="unsupported-base")
    fields = dict(base.semantic_fields)
    target = dict(fields["target_arity_and_topology"])
    components = [dict(component) for component in target["components"]]
    components[0]["topology"] = "LOSSY_UNKNOWN_TOPOLOGY"
    target["components"] = components
    fields["target_arity_and_topology"] = target
    bad = EmpiricalQuerySpec(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query-unsupported"),
        **fields,
    )
    fact = _run(source, qa, pred, bad).facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert fact.p02_failure_state == "UNSUPPORTED_RESPONSE_TOPOLOGY"


def test_realized_cell_outside_exact_declared_domain_is_integrity_failure():
    source = _build_source("domain-integrity", [{"id": "R1", "responses": {"Y": 2}}])
    qa = _query_authority("domain-integrity")
    pred = _branch_predicate(source, qa)
    fact = _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="domain-integrity")).facts[0]
    assert fact.typed_state == "INTEGRITY_FAILURE"
    assert fact.p02_failure_state == "INTEGRITY_FAILURE"


def test_missing_exact_c11_release_is_typed_unavailable_without_latest_fallback():
    source = _build_source("missing-release", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("missing-release")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",), tag="missing-release")
    missing = _ref("C11LogicalRelease", "missing")
    fact = execute_empirical_query(
        repository=source["repo"], query=query, predicate=pred,
        authority_registry=_registry(source, qa), release_refs=(missing,),
    ).facts[0]
    assert fact.typed_state == "UNAVAILABLE"
    assert fact.p02_failure_state == "SOURCE_SCOPE_UNAVAILABLE"


def test_scalar_query_cannot_collapse_multiselect_carrier_even_with_one_event():
    source = _build_source(
        "carrier-topology", [{"id": "R1", "responses": {"Y": 1}}],
        topology_by_question={"Y": "UNORDERED_MULTISELECT_SET"},
    )
    qa = _query_authority("carrier-topology")
    pred = _branch_predicate(source, qa)
    query = _query(source, qa, pred, ("Y",), tag="carrier-topology")
    fact = _run(source, qa, pred, query).facts[0]
    assert fact.typed_state == "UNRESOLVED"
    assert fact.p02_failure_state == "UNSUPPORTED_RESPONSE_TOPOLOGY"


def test_exact_empty_target_domain_is_valid_empty_not_zero_support():
    source = _build_source("valid-empty", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("valid-empty")
    pred = _branch_predicate(source, qa)
    base = _query(source, qa, pred, ("Y",), tag="valid-empty-base")
    fields = dict(base.semantic_fields)
    target = dict(fields["target_arity_and_topology"])
    components = [dict(component) for component in target["components"]]
    components[0]["domain"] = []
    target["components"] = components
    fields["target_arity_and_topology"] = target
    empty_query = EmpiricalQuerySpec(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query-valid-empty"),
        **fields,
    )
    fact = _run(source, qa, pred, empty_query).facts[0]
    assert fact.typed_state == "VALID_EMPTY"
    assert fact.raw_denominator_support == 1
    assert fact.target_topology["complete_cell_semantic_projection"] == []


def test_exact_all_inapplicable_routing_is_not_applicable_not_zero_support():
    rows = [{"id": "R1", "responses": {"Y": 1}}, {"id": "R2", "responses": {"Y": 0}}]
    source = _build_source(
        "not-applicable",
        rows,
        risk_sets={"R": {"Y": set()}},
        nonmember_routing_state="INAPPLICABLE",
    )
    qa = _query_authority("not-applicable")
    pred = _branch_predicate(source, qa)
    fact = _run(source, qa, pred, _query(source, qa, pred, ("Y",), tag="not-applicable")).facts[0]
    assert fact.typed_state == "NOT_APPLICABLE"
    assert fact.raw_denominator_support == 0


def test_authorized_composite_requires_and_uses_operation_specific_positive_authority():
    left = _build_source(
        "composite-ok-left", [{"id": "L1", "responses": {"Y": 1}}],
        question_namespace="composite-ok-shared", risk_namespace="composite-ok-shared",
    )
    right = _build_source(
        "composite-ok-right", [{"id": "R1", "responses": {"Y": 0}}],
        question_namespace="composite-ok-shared", risk_namespace="composite-ok-shared",
    )
    repo = C11Repository((
        left["repo"].resolve_release_exact(left["release_ref"]),
        right["repo"].resolve_release_exact(right["release_ref"]),
    ))
    qa = _query_authority("composite-ok")
    pool = _auth("composite-pool", "SOURCE_COMPOSITION_POOLING", families=("EmpiricalFact@1.0.0",))
    nondup = _auth("composite-nondup", "SOURCE_UNIVERSE_RELATION", families=("EmpiricalFact@1.0.0",))
    estimand = _auth("composite-estimand", "SOURCE_COMPOSITION_POOLING", families=("EmpiricalFact@1.0.0",))
    members = tuple(left["respondents"].values()) + tuple(right["respondents"].values())
    refs = tuple(sorted((member.ref for member in members), key=lambda ref: ref.key))
    pred = make_empirical_predicate(
        predicate_ast={
            "op": "LEAF", "leaf_type": "DERIVED_BRANCH_COHORT",
            "branch_definition_id": "COMPOSITE-OK-ALL",
            "resolved_predicate_hash_or_exact_membership_ref": _ref("BRANCH_MEMBERSHIP", "composite-ok-all"),
            "parent_ancestry_ref": _ref("BRANCH_PARENT", "composite-ok-all"),
            "branch_algorithm_authority_ref": qa.authority_ref,
            "branch_membership_replay_ref": _ref("BRANCH_REPLAY", "composite-ok-all"),
            "branch_source_scope_ref": _ref("SOURCE_SCOPE", "composite-ok-all"),
            "exact_member_respondent_refs": refs,
        },
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(qa.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "predicate-composite-ok"),
        grammar_authority_ref=qa.authority_ref, coordinate_question_value_refs=(),
        risk_set_refs=(left["risk_refs"]["R"],),
        scope_refs=(left["universe"].ref, right["universe"].ref),
        same_respondent_binding_semantics="EXACT_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OPERATOR_SEMANTICS", "BOOLEAN-AND-OR-NOT"),),
    )
    base = _query(
        left, qa, pred, ("Y",), source_mode="AUTHORIZED_COMPOSITE",
        universe_refs=(left["universe"].ref, right["universe"].ref), tag="composite-ok",
        target_authority_refs=(left["source_auth"].authority_ref, right["source_auth"].authority_ref),
    )
    fields = dict(base.semantic_fields)
    grain = dict(fields["requested_output_grain"])
    grain["authorized_composite_authority_refs"] = {
        "pooling": {"authority_ref": pool.authority_ref, "operation": "I03-OP-composite-pool"},
        "nonduplication": {"authority_ref": nondup.authority_ref, "operation": "I03-OP-composite-nondup"},
        "estimand_composition": {"authority_ref": estimand.authority_ref, "operation": "I03-OP-composite-estimand"},
    }
    fields["requested_output_grain"] = grain
    query = EmpiricalQuerySpec(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "query-composite-ok-authorized"),
        **fields,
    )
    registry = AuthorityRegistry((*left["authorities"], *right["authorities"], qa, pool, nondup, estimand))
    fact = execute_empirical_query(
        repository=repo, query=query, predicate=pred, authority_registry=registry,
        release_refs=(left["release_ref"], right["release_ref"]),
    ).facts[0]
    assert fact.typed_state == "SUPPORTED"
    assert fact.raw_denominator_support == 2
    cells = _cell_map(fact)
    assert cells["0"]["raw_numerator_support"] == 1
    assert cells["1"]["raw_numerator_support"] == 1
    assert len(fact.empirical_universe_refs) == 2


def test_sealed_release_semantic_bodies_are_deeply_immutable_and_exports_detached():
    source = _build_source("astra001-deep-immutability", [
        {"id": "R1", "responses": {"X": 0, "Y": 0}},
        {"id": "R2", "responses": {"X": 1, "Y": 1}},
    ])
    qa = _query_authority("astra001-deep-immutability")
    predicate = _branch_predicate(source, qa, tag="astra001")
    query = _query(source, qa, predicate, ("X", "Y"), tag="astra001")
    registry = _registry(source, qa)

    before = _run(source, qa, predicate, query, registry=registry)
    before_fact_exports = tuple(fact.as_dict() for fact in before.facts)
    release = source["repo"].resolve_release_exact(source["release_ref"])
    release_ref_before = release.release_ref
    query_ref_before = query.ref

    event = next(obj for obj in release.public_objects if isinstance(obj, RespondentEvent))
    event_ref_before = event.ref
    event_projection_before = event.semantic_projection()

    # Direct semantic-field attributes are dict/list-compatible for existing
    # consumers, but identity-bearing descendants themselves are immutable.
    with pytest.raises(TypeError):
        event.scoped_respondent_ref["object_id"] = "urn:mutated"
    with pytest.raises(TypeError):
        event.multiplicity_order_rank_fields["kind"] = "RANKED_RESPONSE"

    # Explicit base-class mutation cannot bypass the immutable representation:
    # these values are not writable dict/list subclasses.
    with pytest.raises(TypeError):
        dict.__setitem__(event.multiplicity_order_rank_fields, "kind", "BASE_BYPASS")
    with pytest.raises(TypeError):
        dict.__setitem__(event.scoped_respondent_ref, "object_id", "urn:base-bypass")

    components = query.target_arity_and_topology["components"]
    assert not isinstance(components, list)
    with pytest.raises(TypeError):
        list.__setitem__(components, 0, {"mutated": True})
    with pytest.raises((AttributeError, TypeError)):
        object.__setattr__(components, "_items", ({"mutated": True},))

    # semantic_fields no longer exposes a writable nested alias.
    with pytest.raises(TypeError):
        event.semantic_fields["scoped_respondent_ref"]["content_hash"] = "0" * 64

    # semantic_projection()/as_dict() are detached exports. They remain ordinary
    # mutable representations, but mutation cannot alter the sealed object.
    projection_export = event.semantic_projection()
    projection_export["semantic_fields"]["scoped_respondent_ref"]["object_id"] = "urn:detached"
    projection_export["semantic_fields"]["multiplicity_order_rank_fields"]["kind"] = "DETACHED"
    dict_export = event.as_dict()
    dict_export["semantic_fields"]["scoped_respondent_ref"]["content_hash"] = "1" * 64
    dict_export["semantic_fields"]["multiplicity_order_rank_fields"]["kind"] = "DETACHED"

    assert event.ref == event_ref_before
    assert event.semantic_projection() == event_projection_before

    # Exact repository resolution returns the sealed immutable object, not a
    # writable identity-bearing body.
    resolved_event = source["repo"].resolve_object_exact(event.ref)
    assert isinstance(resolved_event, RespondentEvent)
    assert resolved_event.ref == event.ref
    assert resolved_event.as_dict() == event.as_dict()
    with pytest.raises(TypeError):
        resolved_event.multiplicity_order_rank_fields["kind"] = "REPOSITORY_MUTATION"

    source_authority = source["source_auth"]
    source_authority_ref_before = source_authority.authority_ref
    source_authority_projection_before = source_authority.semantic_projection()
    with pytest.raises(TypeError):
        source_authority.scope_envelope["source_universe_refs"] = "MUTATED"
    with pytest.raises(TypeError):
        source_authority.semantic_fields["scope_envelope"]["source_universe_refs"] = "MUTATED"
    authority_export = source_authority.as_dict()
    authority_export["semantic_fields"]["scope_envelope"]["source_universe_refs"] = "DETACHED"
    assert source_authority.authority_ref == source_authority_ref_before
    assert source_authority.semantic_projection() == source_authority_projection_before

    respondent = next(
        record for record in release.internal_records if isinstance(record, RespondentIdentity)
    )
    respondent_ref_before = respondent.ref
    respondent_projection_before = respondent.semantic_projection()
    with pytest.raises(AttributeError):
        respondent.empirical_universe_ref.object_id = "urn:mutated"
    respondent_export = respondent.as_dict()
    respondent_export["semantic_fields"]["empirical_universe_ref"]["object_id"] = "urn:detached"
    assert respondent.ref == respondent_ref_before
    assert respondent.semantic_projection() == respondent_projection_before
    assert source["repo"].resolve_object_exact(respondent.ref) is respondent

    # A reconstructed object whose body is changed while retaining the stale
    # sealed identity is rejected by the canonical constructor before it can
    # enter ordinary execution.
    corrupted = event.as_dict()
    corrupted_fields = corrupted["semantic_fields"]
    corrupted_fields["raw_response_value"] = "CHANGED"
    with pytest.raises(Pre553IntegrityError, match="object_id|content_hash"):
        RespondentEvent(
            typed_state=corrupted["typed_state"],
            authority_snapshot_refs=corrupted["authority_snapshot_refs"],
            dependency_refs=corrupted["dependency_refs"],
            producer_replay_locator_or_reference_root=corrupted[
                "producer_replay_locator_or_reference_root"
            ],
            object_id=corrupted["object_id"],
            content_hash=corrupted["content_hash"],
            schema_id=corrupted["schema_id"],
            schema_version=corrupted["schema_version"],
            **corrupted_fields,
        )

    after = _run(source, qa, predicate, query, registry=registry)
    assert after == before
    assert tuple(fact.as_dict() for fact in after.facts) == before_fact_exports
    assert query.ref == query_ref_before
    assert release.release_ref == release_ref_before
    assert event.ref == event_ref_before

    replayed = replay_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
        expected_fact_refs=tuple(fact.ref for fact in before.facts),
    )
    assert replayed == before

# ASTRA-002 shared-boundary hostile controls.

def _astra_query_authority(
    tag: str,
    *,
    families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    source_universe_refs="EXPLICIT_UNRESTRICTED",
    state: str = "ALLOW",
) -> AuthoritySnapshot:
    digest = _h(f"astra002-i03-authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"astra002-authority-{tag}"),
        authority_id=f"ASTRA002-I03-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=digest,
        authority_kind="PREDICATE_GRAMMAR",
        decision_state=state,
        governed_operations=(f"ASTRA002-I03-OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": source_universe_refs},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"astra002-i03-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"astra002-{tag}"),
    )


def _astra_target_use_authority(
    source,
    tag: str,
    *,
    allowed_target_use_ref: ExactRef,
    operation: str,
    state: str = "ALLOW",
) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"astra002-target-use-{tag}"),
        authority_id=f"ASTRA002-TARGET-USE-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"astra002-target-use:{tag}:1.0.0"),
        authority_kind="TARGET_USE_PERMISSION",
        decision_state=state,
        governed_operations=(operation,),
        governed_object_families=("EmpiricalFact@1.0.0",),
        scope_envelope={
            "source_universe_refs": (source["universe"].ref.as_dict(),),
            "target_use_refs": (allowed_target_use_ref.as_dict(),),
        },
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"astra002-target-use-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"astra002-target-use-{tag}"),
    )


def _astra_query_with_target_use(
    query: EmpiricalQuerySpec,
    *,
    query_authority: AuthoritySnapshot,
    target_use_authority: AuthoritySnapshot,
    target_use_ref: ExactRef,
    target_use_operation: str,
) -> EmpiricalQuerySpec:
    grain = dict(query.requested_output_grain)
    grain.update({
        "target_use_ref": target_use_ref,
        "target_use_authority_ref": target_use_authority.authority_ref,
        "target_use_operation": target_use_operation,
    })
    return EmpiricalQuerySpec(
        typed_state=query.typed_state,
        authority_snapshot_refs=(query_authority.authority_ref, target_use_authority.authority_ref),
        dependency_refs=tuple(query.dependency_refs) + (target_use_ref,),
        producer_replay_locator_or_reference_root=query.producer_replay_locator_or_reference_root,
        target_refs=query.target_refs,
        target_arity_and_topology=query.target_arity_and_topology,
        condition_predicate_ref=query.condition_predicate_ref,
        risk_set_ref=query.risk_set_ref,
        empirical_universe_refs=query.empirical_universe_refs,
        scope_refs=query.scope_refs,
        measure_basis_ref=query.measure_basis_ref,
        requested_output_grain=grain,
        query_authority_refs=(query_authority.authority_ref,),
    )


def _assert_no_supported(result) -> None:
    assert result.facts
    assert all(fact.typed_state != "SUPPORTED" for fact in result.facts)


def test_astra002_shared_i03_rejects_allow_authority_missing_fact_family():
    source = _build_source("astra002-wrong-family", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    qa = _astra_query_authority(
        "wrong-family",
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0"),
    )
    predicate = _branch_predicate(source, qa, tag="astra002-wrong-family")
    query = _query(source, qa, predicate, ("Y",), tag="astra002-wrong-family")
    result = _run(source, qa, predicate, query, registry=_registry(source, qa))
    _assert_no_supported(result)
    assert result.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"


def test_astra002_shared_i03_rejects_allow_authority_excluding_actual_universe():
    source = _build_source("astra002-wrong-source", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    wrong_universe = _ref("EmpiricalUniverse", "astra002-other-universe")
    qa = _astra_query_authority(
        "wrong-source",
        source_universe_refs=(wrong_universe.as_dict(),),
    )
    predicate = _branch_predicate(source, qa, tag="astra002-wrong-source")
    query = _query(source, qa, predicate, ("Y",), tag="astra002-wrong-source")
    result = _run(source, qa, predicate, query, registry=_registry(source, qa))
    _assert_no_supported(result)
    assert result.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"


def test_astra002_shared_i03_rejects_wrong_target_use_even_with_positive_authorities():
    source = _build_source("astra002-wrong-target-use", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    qa = _astra_query_authority("wrong-target-use")
    predicate = _branch_predicate(source, qa, tag="astra002-wrong-target-use")
    base = _query(source, qa, predicate, ("Y",), tag="astra002-wrong-target-use")
    allowed = _ref("TARGET_USE", "astra002-allowed")
    requested = _ref("TARGET_USE", "astra002-requested-other")
    operation = "ASTRA002-TARGET-USE-OP"
    target_auth = _astra_target_use_authority(
        source,
        "wrong-target-use",
        allowed_target_use_ref=allowed,
        operation=operation,
    )
    query = _astra_query_with_target_use(
        base,
        query_authority=qa,
        target_use_authority=target_auth,
        target_use_ref=requested,
        target_use_operation=operation,
    )
    registry = AuthorityRegistry((*source["authorities"], qa, target_auth))
    result = _run(source, qa, predicate, query, registry=registry)
    _assert_no_supported(result)
    assert result.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"


def test_astra002_shared_i03_preserves_exact_lawful_target_use():
    source = _build_source("astra002-good-target-use", [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    qa = _astra_query_authority("good-target-use")
    predicate = _branch_predicate(source, qa, tag="astra002-good-target-use")
    base = _query(source, qa, predicate, ("Y",), tag="astra002-good-target-use")
    target_use = _ref("TARGET_USE", "astra002-good")
    operation = "ASTRA002-GOOD-TARGET-USE-OP"
    target_auth = _astra_target_use_authority(
        source,
        "good-target-use",
        allowed_target_use_ref=target_use,
        operation=operation,
    )
    query = _astra_query_with_target_use(
        base,
        query_authority=qa,
        target_use_authority=target_auth,
        target_use_ref=target_use,
        target_use_operation=operation,
    )
    registry = AuthorityRegistry((*source["authorities"], qa, target_auth))
    result = _run(source, qa, predicate, query, registry=registry)
    assert result.facts[0].typed_state == "SUPPORTED"


@pytest.mark.parametrize(
    "authority_state",
    ("DENY", "OUT_OF_SCOPE", "SUPERSEDED_NOT_REPLAYABLE"),
)
def test_astra002_shared_i03_preserves_nonpositive_authority_as_nonpositive(authority_state):
    tag = f"astra002-nonpositive-{authority_state.lower()}"
    source = _build_source(tag, [
        {"id": "R1", "responses": {"Y": 1}},
    ])
    qa = _astra_query_authority(tag, state=authority_state)
    predicate = _branch_predicate(source, qa, tag=tag)
    query = _query(source, qa, predicate, ("Y",), tag=tag)
    result = _run(source, qa, predicate, query, registry=_registry(source, qa))
    _assert_no_supported(result)
    assert result.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"

