"""HQ273 C01 — bounded source-free three-item fixture and true-conditional I03 adapter.

DEVELOPMENT_FIXTURE_ONLY.

This module deliberately reuses the accepted I03 sealed-C11 substrate
(``pre553_c11_ingest``/``pre553_c11_repository``) and the accepted public executor
(``pre553_empirical_query.execute_empirical_query``).  It does NOT invent a parallel
empirical substrate, and it does NOT bind, reference or derive from any real source
release, question implementation, risk set or target-use permission.

Every authority snapshot and exact ref minted here is fixture-intrinsic and carries
a ``urn:test:hq273-c01:...`` identity that no production issuer gate can accept.  In
particular nothing here may be read as an adopted Afrobarometer R5 permission, as an
I03 source release, or as a C1 selected-service join.

The single capability this adapter adds over the existing frozen GT12 wrapper is the
one the sealed HQ272 R01 hostile review proved missing: **two separately typed native
survey-response predicates** over the SAME sealed release, so that ``q(Y|A)`` and
``q(Y|A,B)`` are two independently replayable ``EmpiricalFact`` objects carrying their
OWN predicate-defined ``denominator_member_refs``.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    make_empirical_predicate,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query

FIXTURE_ID = "HQ273-C01-TRUE-CONDITIONAL-FIXTURE"
FIXTURE_MARKER = "DEVELOPMENT_FIXTURE_ONLY"
URI_PREFIX = "urn:test:hq273-c01"

#: Three distinct questions.  Generic synthetic labels; no real source item is named.
TARGET_Y = "Y"
CONDITION_A = "A"
CONDITION_B = "B"
FIXTURE_QUESTIONS = (TARGET_Y, CONDITION_A, CONDITION_B)

SUBSTANTIVE = "SUBSTANTIVE_RESPONSE"
ELIGIBLE = "ELIGIBLE_APPLICABLE"
RAW_MEASURE = "RAW"
SINGLE_UNIVERSE = "SINGLE_UNIVERSE"
TRUE_CONDITIONAL_OPERATION = "HQ273-C01-I03-TRUE-CONDITIONAL"
JOINT_ORDER = "SEMANTIC_ORDERED"

#: Deliberate native categorical domain.  The non-substantive native codes are the
#: realistic coercion hazard: a naive carrier that recodes them into a substantive
#: bucket keeps a typed non-substantive state while carrying a substantive raw value.
NATIVE_STATES = ("0", "1")


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"{URI_PREFIX}:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _authority(
    tag: str,
    kind: str,
    *,
    operation: str,
    families: Iterable[str],
    decision_state: str = "ALLOW",
    extra_scope: Mapping[str, Any] | None = None,
) -> AuthoritySnapshot:
    scope: dict[str, Any] = {"source_universe_refs": "EXPLICIT_UNRESTRICTED"}
    if extra_scope:
        scope.update(extra_scope)
    return AuthoritySnapshot(
        typed_state=decision_state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"HQ273-C01-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"authority:{tag}:1.0.0"),
        authority_kind=kind,
        decision_state=decision_state,
        governed_operations=(operation,),
        governed_object_families=tuple(families),
        scope_envelope=scope,
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _grammar_authority(tag: str) -> AuthoritySnapshot:
    return _authority(
        tag,
        "PREDICATE_GRAMMAR",
        operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0", "EmpiricalFact@1.0.0"),
    )


def _target_use_authority(tag: str) -> AuthoritySnapshot:
    return _authority(
        f"targetuse-{tag}",
        "TARGET_USE_PERMISSION",
        operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalFact@1.0.0",),
        extra_scope={"target_use_refs": "EXPLICIT_UNRESTRICTED"},
    )


@dataclass(frozen=True)
class TrueConditionalPlan:
    """One unary-target query plus its exact condition predicate."""

    claim_id: str
    predicate: Any
    query: EmpiricalQuerySpec
    condition_values: Mapping[str, str | None]


def build_three_item_fixture(
    rows: Sequence[Mapping[str, Any]],
    *,
    tag: str = "base",
    risk_sets: Mapping[str, Mapping[str, Iterable[str]]] | None = None,
) -> dict[str, Any]:
    """Ingest one synthetic source-free sealed C11 release carrying Y, A and B.

    Each row carries exactly one scalar ``RespondentEvent`` per question, with the
    typed response state and the stored native code kept separate so that a typed
    non-substantive state can coexist with a substantive-looking raw value.
    """
    source_auth = _authority(
        f"source-{tag}", "SOURCE_SEMANTICS_TOPOLOGY", operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    state_auth = _authority(
        f"state-{tag}", "SOURCE_SEMANTICS_TOPOLOGY", operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    routing_auth = _authority(
        f"routing-{tag}", "ROUTING_RISK_SET", operation=TRUE_CONDITIONAL_OPERATION,
        families=("RoutingEligibilityFact@1.0.0",),
    )
    coord_auth = _authority(
        f"coord-{tag}", "COORDINATE_SEMANTICS", operation=TRUE_CONDITIONAL_OPERATION,
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    replay_auth = _authority(
        f"replay-{tag}", "REPLAY_PROTOCOL", operation=TRUE_CONDITIONAL_OPERATION,
        families=("ReplayReceipt@1.0.0",),
    )
    target_use_auth = _target_use_authority(tag)
    authorities = (source_auth, state_auth, routing_auth, coord_auth, replay_auth, target_use_auth)

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"universe-{tag}"),
        raw_source_identity=f"HQ273-C01-RAW-{tag}",
        source_family="SURVEY",
        study_product_release=f"HQ273-C01-STUDY-{tag}/REL-1",
        instrument_release=f"HQ273-C01-INST-{tag}",
        country_geography="FIXTURE-ONLY",
        sampling_geography="FIXTURE-ONLY",
        raw_wave="W0",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01-01",
        target_population_and_sample_frame="SYNTHETIC-FIXTURE-ADULTS",
        sampling_design_regime="SYNTHETIC-FIXTURE-NO-INFERENCE",
        respondent_namespace=f"HQ273-C01-NS-{tag}",
        source_artifact_import_lineage=f"HQ273-C01-LINEAGE-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )

    qrefs = {q: _ref("QUESTION_NATIVE", f"{tag}-{q}") for q in FIXTURE_QUESTIONS}
    coordinate_names = sorted({c for row in rows for c in row.get("coords", {})})
    crefs = {c: _ref("COORDINATE_NATIVE", f"{tag}-{c}") for c in coordinate_names}
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[q],
            instrument_question_version="FIXTURE-1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for q in FIXTURE_QUESTIONS
    )

    respondents: dict[str, RespondentIdentity] = {}
    respondent_list: list[RespondentIdentity] = []
    for row in rows:
        respondent = RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=row["id"],
            source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{tag}-{row['id']}"),
            identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        )
        respondents[row["id"]] = respondent
        respondent_list.append(respondent)

    if risk_sets is None:
        risk_sets = {"R": {q: [row["id"] for row in rows] for q in FIXTURE_QUESTIONS}}

    routing: list[RoutingEligibilityFact] = []
    for risk_name, per_question in sorted(risk_sets.items()):
        risk_ref = _ref("RISK_SET", f"{tag}-{risk_name}")
        for row in rows:
            respondent = respondents[row["id"]]
            for q in FIXTURE_QUESTIONS:
                members = set(per_question.get(q, ()))
                declared = row.get("routing", {}).get(q, ELIGIBLE if row["id"] in members else "NOT_ELIGIBLE")
                routing.append(RoutingEligibilityFact(
                    typed_state=declared,
                    authority_snapshot_refs=(routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"routing-{tag}-{risk_name}-{row['id']}-{q}"),
                    empirical_universe_ref=universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=qrefs[q],
                    risk_set_ref=risk_ref,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{risk_name}-{q}"),
                    applicability_state=declared,
                    routing_state=declared,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET",
                        f"{tag}-{risk_name}-{q}-{'-'.join(sorted(members)) or 'EMPTY'}",
                    ),
                ))

    events: list[RespondentEvent] = []
    coordinates: list[EmpiricalCoordinateFact] = []
    for row in rows:
        respondent = respondents[row["id"]]
        for q in FIXTURE_QUESTIONS:
            state, native = row["responses"][q]
            events.append(RespondentEvent(
                typed_state=state,
                # Both source-topology and response-state semantics are bound per event so
                # that TYPED_RESPONSE_STATE and SURVEY_RESPONSE_EVENT leaves are separately
                # authority-checked rather than implicitly trusting one shared snapshot.
                authority_snapshot_refs=(source_auth.authority_ref, state_auth.authority_ref),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"event-{tag}-{row['id']}-{q}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                native_question_ref=qrefs[q],
                canonical_question_ref_if_authorized=None,
                component_or_subitem_ref=None,
                event_group_id=f"HQ273-C01-GROUP-{tag}-{row['id']}-{q}",
                response_event_id_or_deterministic_index=f"{row['id']}-{q}",
                raw_response_value=str(native),
                canonical_response_value_if_authorized=None,
                value_transform_authority_ref=None,
                response_topology_ref=_ref("TOPOLOGY", f"{tag}-{q}-SCALAR_SINGULAR"),
                multiplicity_order_rank_fields={"kind": "SCALAR_SINGULAR", "index": 0},
                response_state=state,
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
                unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{tag}-{coord}"),
                effective_or_reference_time="2026-01-01",
                coordinate_state="OBSERVED_COORDINATE",
                normalization_crosswalk_authority_ref=None,
                source_semantic_authority_ref=coord_auth.authority_ref,
            ))

    if not coordinates:
        crefs["STRATUM"] = _ref("COORDINATE_NATIVE", f"{tag}-STRATUM")
        for row in rows:
            coordinates.append(EmpiricalCoordinateFact(
                typed_state="OBSERVED_COORDINATE",
                authority_snapshot_refs=(coord_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"coord-{tag}-{row['id']}-STRATUM"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondents[row["id"]].ref,
                native_coordinate_ref=crefs["STRATUM"],
                canonical_coordinate_ref_if_authorized=None,
                canonical_coordinate_value_if_authorized=None,
                raw_coordinate_value="X",
                unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", f"{tag}-STRATUM"),
                effective_or_reference_time="2026-01-01",
                coordinate_state="OBSERVED_COORDINATE",
                normalization_crosswalk_authority_ref=None,
                source_semantic_authority_ref=coord_auth.authority_ref,
            ))

    counts = {
        "EmpiricalUniverse": 1,
        "RespondentIdentity": len(respondent_list),
        "QuestionVariableBinding": len(questions),
        "RespondentEvent": len(events),
        "RoutingEligibilityFact": len(routing),
        "EmpiricalCoordinateFact": len(coordinates),
        "WeightMeasureFact": 0,
        "AuthoritySnapshot": len(authorities),
        "SourceUniverseRelation": 0,
        "EmpiricalPredicateReplayBinding": 0,
        "ComparatorReplayBinding": 0,
        "DiscoveryBranchReplayBinding": 0,
        "StructuralAdmissionReplayBinding": 0,
        "ReplayManifest": 1,
    }
    manifest = SourceReleaseManifest(
        source_artifact_id=f"HQ273-C01-SOURCE-{tag}",
        source_artifact_content_hash=_h(f"source-artifact:{tag}"),
        source_family_id="SURVEY",
        study_product_id=f"HQ273-C01-STUDY-{tag}",
        release_id=f"HQ273-C01-REL-{tag}",
        instrument_release_id=f"HQ273-C01-INST-{tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=_ref("SOURCE_SNAPSHOT", f"{tag}-{_h(f'source-artifact:{tag}')[:12]}"),
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        empirical_universes=(universe,),
        respondent_identities=tuple(respondent_list),
        question_variable_bindings=questions,
        respondent_events=tuple(events),
        routing_eligibility_facts_or_exact_rules=tuple(routing),
        empirical_coordinate_facts=tuple(coordinates),
        weight_measure_facts_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
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
        deterministic_tie_order_rules_ref=_ref("ORDER_RULE", f"CANONICAL-REF-SORT-{tag}"),
        replay_protocol_version="1.0.0",
    )
    candidate = replace(candidate, candidate_replay_manifest=replay)
    repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    assert result.accepted, result.errors

    return {
        "fixture_id": FIXTURE_ID,
        "marker": FIXTURE_MARKER,
        "tag": tag,
        "repo": repo,
        "release_ref": result.release_ref,
        "universe": universe,
        "respondents": respondents,
        "respondent_list": tuple(respondent_list),
        "qrefs": qrefs,
        "crefs": crefs,
        "risk_refs": {name: _ref("RISK_SET", f"{tag}-{name}") for name in risk_sets},
        "source_auth": source_auth,
        "state_auth": state_auth,
        "routing_auth": routing_auth,
        "coord_auth": coord_auth,
        "replay_auth": replay_auth,
        "target_use_auth": target_use_auth,
        "authorities": authorities,
    }


# --------------------------------------------------------------------------
# native predicate leaves
# --------------------------------------------------------------------------

def typed_response_leaf(source: Mapping[str, Any], q: str, typed_state: str) -> dict[str, Any]:
    return {
        "op": "LEAF",
        "leaf_type": "TYPED_RESPONSE_STATE",
        "question_semantic_ref": source["qrefs"][q],
        "typed_state_ref": _ref("TYPED_STATE", f"{q}-{typed_state}"),
        "state_semantic_authority_ref": source["state_auth"].authority_ref,
        "typed_state": typed_state,
    }


def routing_leaf(source: Mapping[str, Any], q: str, routing_state: str = ELIGIBLE) -> dict[str, Any]:
    return {
        "op": "LEAF",
        "leaf_type": "ROUTING_APPLICABILITY_STATE",
        "question_semantic_ref": source["qrefs"][q],
        "routing_or_applicability_state_ref": _ref("ROUTING_STATE", f"{q}-{routing_state}"),
        "routing_authority_ref": source["routing_auth"].authority_ref,
        "routing_state": routing_state,
    }


def response_eq_leaf(source: Mapping[str, Any], q: str, native_value: str) -> dict[str, Any]:
    return {
        "op": "LEAF",
        "leaf_type": "SURVEY_RESPONSE_EVENT",
        "question_semantic_ref": source["qrefs"][q],
        "component_or_event_selector_ref": _ref("EVENT_SELECTOR", f"{q}-ANY"),
        "response_value_or_state_ref": _ref("VALUE_REF", f"{q}-{native_value}"),
        "response_topology_authority_ref": source["source_auth"].authority_ref,
        "response_semantic_authority_ref": source["source_auth"].authority_ref,
        "operator": "EQ",
        "exact_value": native_value,
    }


def coordinate_eq_leaf(source: Mapping[str, Any], coord: str, value: str) -> dict[str, Any]:
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


def and_node(children: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {"op": "AND", "children": list(children)}


def common_case_base_ast(source: Mapping[str, Any]) -> dict[str, Any]:
    """Complete-case eligibility AND substantive validity for Y, A and B.

    This is the declared predeclared analysis scope ``S`` of the sealed HQ272 R01
    review: every respondent must be independently routed eligible/applicable for all
    three items AND must carry a substantive native answer for all three.
    """
    return and_node(
        [routing_leaf(source, q) for q in FIXTURE_QUESTIONS]
        + [typed_response_leaf(source, q, SUBSTANTIVE) for q in FIXTURE_QUESTIONS]
    )


def true_conditional_predicate(
    source: Mapping[str, Any],
    qauth: AuthoritySnapshot,
    ast: Mapping[str, Any],
    *,
    tag: str,
) -> Any:
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


def true_conditional_query(
    source: Mapping[str, Any],
    qauth: AuthoritySnapshot,
    predicate: Any,
    *,
    tag: str,
    risk_set_type: str = "WHOLE_QUESTION_RISK_SET",
    joint_targets: Sequence[str] | None = None,
    query_authorities: Sequence[Any] | None = None,
) -> EmpiricalQuerySpec:
    """Unary-target ``q(Y | ...)`` query bound to an exact fixture target-use permission.

    ``joint_targets`` exists ONLY so the negative court can build the arity-3 joint
    tensor that the sealed HQ272 R01 review proved is not a substitute for two
    conditioned facts.
    """
    ordered = list(joint_targets) if joint_targets is not None else [TARGET_Y]
    components = [
        {
            "target_ref": source["qrefs"][q],
            "topology": "SCALAR_SINGULAR",
            "domain": list(NATIVE_STATES),
            "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"{tag}-{q}-01"),
            "topology_authority_refs": [source["source_auth"].authority_ref],
            "response_semantic_authority_refs": [source["source_auth"].authority_ref],
            "included_states": [SUBSTANTIVE],
        }
        for q in ordered
    ]
    target_use_ref = _ref("TARGET_USE", f"{tag}")
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qauth.authority_ref, source["target_use_auth"].authority_ref),
        dependency_refs=(predicate.ref, target_use_ref),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"query-{tag}"),
        target_refs=tuple(source["qrefs"][q] for q in ordered),
        target_arity_and_topology={
            "arity": len(ordered),
            "joint_order_semantics": JOINT_ORDER,
            "components": components,
        },
        condition_predicate_ref=predicate.ref,
        risk_set_ref=source["risk_refs"]["R"],
        empirical_universe_refs=(source["universe"].ref,),
        scope_refs=(source["universe"].ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", RAW_MEASURE),
        requested_output_grain={
            "source_scope_mode": SINGLE_UNIVERSE,
            "measure_kind": RAW_MEASURE,
            "risk_set_type": risk_set_type,
            "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", f"{tag}-SUBSTANTIVE"),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
            "query_operation": TRUE_CONDITIONAL_OPERATION,
            "target_use_ref": target_use_ref,
            "target_use_authority_ref": source["target_use_auth"].authority_ref,
            "target_use_operation": TRUE_CONDITIONAL_OPERATION,
            "fixture_marker": FIXTURE_MARKER,
        },
        query_authority_refs=tuple(a.authority_ref for a in (query_authorities or (qauth,))),
    )


def run_true_conditional(
    source: Mapping[str, Any],
    predicate: Any,
    query: EmpiricalQuerySpec,
    *,
    qauth: AuthoritySnapshot,
) -> Any:
    registry = AuthorityRegistry((*source["authorities"], qauth))
    return execute_empirical_query(
        repository=source["repo"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(source["release_ref"],),
    )


def two_nested_true_conditional_facts(source: Mapping[str, Any], qauth: AuthoritySnapshot):
    """Build BOTH ``q(Y|A=0)`` and ``q(Y|A=0,B=0)`` over one sealed fixture release.

    Two separately typed predicates, two separately typed queries, two separately
    replayable ``EmpiricalFact`` objects.  No joint target tensor is used anywhere.
    """
    base = common_case_base_ast(source)

    p1_ast = and_node([base, response_eq_leaf(source, CONDITION_A, "0")])
    p1 = true_conditional_predicate(source, qauth, p1_ast, tag="q1-a0")
    q1 = true_conditional_query(source, qauth, p1, tag="q1-a0")

    p2_ast = and_node([
        base,
        response_eq_leaf(source, CONDITION_A, "0"),
        response_eq_leaf(source, CONDITION_B, "0"),
    ])
    p2 = true_conditional_predicate(source, qauth, p2_ast, tag="q2-a0b0")
    q2 = true_conditional_query(source, qauth, p2, tag="q2-a0b0")

    f1 = run_true_conditional(source, p1, q1, qauth=qauth).facts[0]
    f2 = run_true_conditional(source, p2, q2, qauth=qauth).facts[0]
    return (TrueConditionalPlan("HQ273-C01-q1", p1, q1, {CONDITION_A: "0"}), f1), \
           (TrueConditionalPlan("HQ273-C01-q2", p2, q2, {CONDITION_A: "0", CONDITION_B: "0"}), f2)


def unguarded_condition_fact(source: Mapping[str, Any], qauth: AuthoritySnapshot):
    """Same conditioning but WITHOUT the declared complete-case validity policy.

    Used only to demonstrate that native value equality alone does not exclude typed
    non-substantive states; the exclusion is an operator-declared policy, not an
    engine guarantee.
    """
    p_ast = and_node([response_eq_leaf(source, CONDITION_A, "0")])
    pred = true_conditional_predicate(source, qauth, p_ast, tag="unguarded-a0")
    query = true_conditional_query(source, qauth, pred, tag="unguarded-a0")
    return run_true_conditional(source, pred, query, qauth=qauth).facts[0]


def zero_support_fact(source: Mapping[str, Any], qauth: AuthoritySnapshot):
    """A condition that no member of the complete-case base can satisfy."""
    ast = and_node([
        common_case_base_ast(source),
        response_eq_leaf(source, CONDITION_A, "0"),
        response_eq_leaf(source, CONDITION_B, "0"),
        coordinate_eq_leaf(source, "STRATUM", "NO_SUCH_STRATUM"),
    ])
    pred = true_conditional_predicate(source, qauth, ast, tag="zero-support")
    query = true_conditional_query(source, qauth, pred, tag="zero-support")
    return run_true_conditional(source, pred, query, qauth=qauth).facts[0]


def member_ref_ids(fact: Any, source: Mapping[str, Any]) -> tuple[str, ...]:
    """Translate denominator member refs back to fixture respondent ids, independently."""
    by_ref = {r.ref.object_id: rid for rid, r in source["respondents"].items()}
    return tuple(sorted(by_ref[r["object_id"]] for r in fact.denominator_member_refs))


def risk_ref_ids(fact: Any, source: Mapping[str, Any]) -> tuple[str, ...]:
    by_ref = {r.ref.object_id: rid for rid, r in source["respondents"].items()}
    return tuple(sorted(by_ref[r["object_id"]] for r in fact.risk_set_member_refs))


def cell_counts(fact: Any) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in fact.target_topology["complete_cell_semantic_projection"]:
        key = row["cell"] if isinstance(row["cell"], str) else tuple(row["cell"])
        out[key] = {
            "raw_numerator_support": row["raw_numerator_support"],
            "cell_state": row["cell_state"],
        }
    return out


__all__ = [
    "FIXTURE_ID", "FIXTURE_MARKER", "FIXTURE_QUESTIONS", "TARGET_Y", "CONDITION_A", "CONDITION_B",
    "SUBSTANTIVE", "ELIGIBLE", "RAW_MEASURE", "SINGLE_UNIVERSE", "TRUE_CONDITIONAL_OPERATION",
    "JOINT_ORDER", "NATIVE_STATES", "TrueConditionalPlan", "build_three_item_fixture",
    "typed_response_leaf", "routing_leaf", "response_eq_leaf", "coordinate_eq_leaf",
    "and_node", "common_case_base_ast", "true_conditional_predicate", "true_conditional_query",
    "run_true_conditional", "two_nested_true_conditional_facts", "unguarded_condition_fact",
    "zero_support_fact", "member_ref_ids", "risk_ref_ids", "cell_counts", "_grammar_authority",
]
