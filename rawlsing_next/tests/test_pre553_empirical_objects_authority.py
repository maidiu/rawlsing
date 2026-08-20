import hashlib
from decimal import Decimal

import pytest

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityConflict,
    Pre553AuthorityError,
    require_exact_authority_ref,
    require_positive_authority,
    validate_object_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    DiscoveryAuthority,
    EmpiricalFact,
    EmpiricalPredicate,
    EmpiricalQuerySpec,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    RespondentEvent,
    SourceUniverseRelation,
    StructuralEmpiricalAdmission,
    WeightMeasureFact,
    assert_zero_actor_v3_v2_effect,
    canonical_json,
    canonicalize_predicate_ast,
    make_empirical_predicate,
    require_public_object_family,
    semantic_hash,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _aref(tag: str = "base", *, version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", version, _h(f"authority:{tag}:{version}"))


def _root(tag: str = "root") -> ExactRef:
    return _ref("REPLAY_ROOT", tag)


def _universe(tag: str = "u1", *, source_relations=(), authority_refs=None, **extra):
    authority_refs = tuple(authority_refs or (_aref("source"),))
    fields = dict(
        raw_source_identity=f"RAW-{tag}",
        source_family="SURVEY",
        study_product_release=f"REL-{tag}",
        instrument_release=f"INST-{tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave=f"W-{tag}",
        canonical_wave_if_governed=f"CW-{tag}",
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-A",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SRC-{tag}",
        harmonization_authority_ref=_aref("harm"),
        source_relation_refs=source_relations,
    )
    fields.update(extra)
    return EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=authority_refs,
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"universe-{tag}"),
        **fields,
    )


def _authority(
    tag: str = "source",
    *,
    state: str = "ALLOW",
    kind: str = "SOURCE_SEMANTICS_TOPOLOGY",
    operations=("INTERPRET_SOURCE_SEMANTICS",),
    families=("EmpiricalUniverse@1.0.0",),
    source_refs=(),
):
    content_hash = _h(f"authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"authority-{tag}"),
        authority_id=f"AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=content_hash,
        authority_kind=kind,
        decision_state=state,
        governed_operations=operations,
        governed_object_families=families,
        scope_envelope={
            "source_universe_refs": tuple(source_refs),
            "target_use_refs": ("STRUCTURAL_MEDIATION_INPUT",),
        },
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _query(tag: str = "q", *, targets=None, authority_refs=None):
    targets = list(targets or [_ref("QUESTION", "Q1"), _ref("QUESTION", "Q2")])
    authority_refs = tuple(authority_refs or (_aref("query"),))
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=authority_refs,
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"query-{tag}"),
        target_refs=targets,
        target_arity_and_topology={"arity": len(targets), "topology": "ORDERED_TARGET_TUPLE"},
        condition_predicate_ref=_ref("EMPIRICAL_PREDICATE", tag),
        risk_set_ref=_ref("RISK_SET", tag),
        empirical_universe_refs=[_ref("EMPIRICAL_UNIVERSE", tag)],
        scope_refs=[_ref("SCOPE", tag)],
        measure_basis_ref=_ref("MEASURE", "RAW"),
        requested_output_grain="FULL_TARGET_DISTRIBUTION",
        query_authority_refs=[_aref("query")],
    )


def _fact(tag: str = "f", *, state="SUPPORTED", numerator=2, denominator=4, diagnostic=None):
    extra = {} if diagnostic is None else {"diagnostic_kind": diagnostic}
    return EmpiricalFact(
        typed_state=state,
        authority_snapshot_refs=(_aref("query"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"fact-{tag}"),
        empirical_query_spec_ref=_ref("EMPIRICAL_QUERY_SPEC", tag),
        empirical_universe_refs=[_ref("EMPIRICAL_UNIVERSE", tag)],
        target_topology={"cells": ["A", "B"]},
        condition_predicate_ref=_ref("EMPIRICAL_PREDICATE", tag),
        risk_set_ref=_ref("RISK_SET", tag),
        raw_numerator_support=numerator,
        raw_denominator_support=denominator,
        weighted_numerator_support_if_authorized=None,
        weighted_denominator_support_if_authorized=None,
        measure_basis_ref=_ref("MEASURE", "RAW"),
        response_state_semantics_ref=_ref("STATE_SEMANTICS", tag),
        uncertainty_method_or_typed_state="UNCERTAINTY_UNQUANTIFIED",
        source_empirical_provenance_refs=[_ref("PROVENANCE", tag)],
        replay_ref=_ref("REPLAY", tag),
        **extra,
    )


def test_deterministic_content_identity_and_set_order_canonicalization():
    a = _ref("SOURCE_RELATION", "A")
    b = _ref("SOURCE_RELATION", "B")
    left = _universe("same", source_relations=[a, b])
    right = _universe("same", source_relations=[b, a, a])
    assert left.object_id == right.object_id
    assert left.content_hash == right.content_hash
    assert left.ref == right.ref


def test_semantically_ordered_target_sequence_is_not_sorted():
    q1 = _ref("QUESTION", "Q1")
    q2 = _ref("QUESTION", "Q2")
    left = _query("ordered", targets=[q1, q2])
    right = _query("ordered", targets=[q2, q1])
    assert left.object_id != right.object_id
    assert left.target_refs != right.target_refs


def test_float_rejected_but_exact_decimal_is_deterministic():
    with pytest.raises(Pre553IntegrityError):
        canonical_json({"lossy": 0.1})
    assert canonical_json({"exact": Decimal("1.2500")}) == canonical_json(
        {"exact": Decimal("1.25")}
    )


def test_typed_absence_and_observed_zero_do_not_collapse():
    missing = RespondentEvent(
        typed_state="MISSING",
        authority_snapshot_refs=(_aref("source"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("missing"),
        empirical_universe_ref=_ref("EMPIRICAL_UNIVERSE", "u"),
        scoped_respondent_ref=_ref("RESPONDENT", "r"),
        native_question_ref=_ref("QUESTION_NATIVE", "q"),
        canonical_question_ref_if_authorized=None,
        component_or_subitem_ref=None,
        event_group_id="g",
        response_event_id_or_deterministic_index="e",
        raw_response_value=None,
        canonical_response_value_if_authorized=None,
        value_transform_authority_ref=None,
        response_topology_ref=_ref("TOPOLOGY", "scalar"),
        multiplicity_order_rank_fields={"kind": "SCALAR_SINGULAR"},
        response_state="MISSING",
    )
    substantive = RespondentEvent(
        typed_state="SUBSTANTIVE_RESPONSE",
        authority_snapshot_refs=(_aref("source"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("substantive"),
        empirical_universe_ref=_ref("EMPIRICAL_UNIVERSE", "u"),
        scoped_respondent_ref=_ref("RESPONDENT", "r"),
        native_question_ref=_ref("QUESTION_NATIVE", "q"),
        canonical_question_ref_if_authorized=None,
        component_or_subitem_ref=None,
        event_group_id="g",
        response_event_id_or_deterministic_index="e",
        raw_response_value="0",
        canonical_response_value_if_authorized="0",
        value_transform_authority_ref=_aref("harm"),
        response_topology_ref=_ref("TOPOLOGY", "scalar"),
        multiplicity_order_rank_fields={"kind": "SCALAR_SINGULAR"},
        response_state="SUBSTANTIVE_RESPONSE",
    )
    assert missing.object_id != substantive.object_id
    observed_zero = _fact("zero", state="OBSERVED_ZERO", numerator=0, denominator=7)
    zero_support = _fact("support", state="ZERO_SUPPORT", numerator=0, denominator=0)
    assert observed_zero.object_id != zero_support.object_id
    with pytest.raises(Pre553IntegrityError):
        _fact("bad-zero", state="OBSERVED_ZERO", numerator=0, denominator=0)


def test_nonpositive_weight_cannot_be_repaired_to_one():
    common = dict(
        authority_snapshot_refs=(_aref("weight"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("weight"),
        empirical_universe_ref=_ref("EMPIRICAL_UNIVERSE", "u"),
        scoped_respondent_ref=_ref("RESPONDENT", "r"),
        weight_basis_id="W1",
        weight_source_ref=_ref("WEIGHT_SOURCE", "w"),
        design_authority_ref=_aref("design"),
        estimand_authority_ref=_aref("estimand"),
        normalization_or_recalibration_rule_ref=None,
        effective_scope_ref=_ref("SCOPE", "u"),
    )
    with pytest.raises(Pre553IntegrityError):
        WeightMeasureFact(
            typed_state="WEIGHT_MISSING",
            exact_weight_value_representation="1.0",
            weight_state="WEIGHT_MISSING",
            **common,
        )


def test_authority_lookup_is_exact_and_has_no_latest_default_or_fuzzy_lane():
    snapshot = _authority("source")
    registry = AuthorityRegistry([snapshot])
    assert registry.resolve_exact(snapshot.authority_ref).snapshot == snapshot
    with pytest.raises(Pre553AuthorityError):
        require_exact_authority_ref({
            "authority_id": snapshot.authority_id,
            "authority_version": "latest",
            "authority_content_hash": snapshot.authority_content_hash,
        })
    wrong = AuthorityRef(snapshot.authority_id, snapshot.authority_version, _h("wrong"))
    with pytest.raises(Pre553AuthorityError):
        registry.resolve_exact(wrong)


def test_same_id_version_conflicting_hashes_fail_registry_closed():
    a = _authority("same")
    b = AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("authority-conflict"),
        authority_id=a.authority_id,
        authority_version=a.authority_version,
        authority_content_hash=_h("different-content"),
        authority_kind=a.authority_kind,
        decision_state="ALLOW",
        governed_operations=("INTERPRET_SOURCE_SEMANTICS",),
        governed_object_families=("EmpiricalUniverse@1.0.0",),
        scope_envelope={"source_universe_refs": ()},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h("different-semantics"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", "different"),
    )
    with pytest.raises(Pre553AuthorityConflict):
        AuthorityRegistry([a, b])


def test_positive_authority_is_exact_operation_family_and_scope_bounded():
    universe_ref = _ref("EMPIRICAL_UNIVERSE", "U1")
    snapshot = _authority("source", source_refs=(universe_ref,))
    assert require_positive_authority(
        snapshot,
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        operation="INTERPRET_SOURCE_SEMANTICS",
        object_family="EmpiricalUniverse",
        source_universe_ref=universe_ref,
    ) == snapshot
    with pytest.raises(Pre553AuthorityError):
        require_positive_authority(snapshot, operation="POOL_SAMPLES")
    with pytest.raises(Pre553AuthorityError):
        require_positive_authority(snapshot, source_universe_ref=_ref("EMPIRICAL_UNIVERSE", "U2"))


def test_authority_closure_requires_exact_historical_snapshot():
    snapshot = _authority("source")
    universe = _universe("u", authority_refs=(snapshot.authority_ref,))
    registry = AuthorityRegistry([snapshot])
    assert validate_object_authority_closure(universe, registry) == (snapshot,)
    with pytest.raises(Pre553AuthorityError):
        validate_object_authority_closure(universe, AuthorityRegistry([]))


def test_source_universes_and_relation_kinds_do_not_collapse():
    u1 = _universe("U1")
    u2 = _universe("U2")
    assert u1.ref != u2.ref
    relation = SourceUniverseRelation(
        typed_state="DISTINCT_BY_DEFAULT",
        authority_snapshot_refs=(_aref("relation"),),
        dependency_refs=(u1.ref, u2.ref),
        producer_replay_locator_or_reference_root=_root("relation"),
        relation_id="R1",
        relation_kind="HARMONIZATION_ALIAS",
        source_universe_refs=(u1.ref, u2.ref),
        relation_authority_ref=_aref("relation"),
        effective_scope="ALL",
        overlap_or_nonduplication_evidence_refs=(),
        composition_estimand_refs=(),
        deduplication_rule_ref_if_any=None,
        negative_limit_refs=(),
        decision="NOT_APPLICABLE",
    )
    assert relation.typed_state == "DISTINCT_BY_DEFAULT"
    with pytest.raises(Pre553SemanticCollapseError):
        SourceUniverseRelation(
            typed_state="RELATION_AUTHORIZED_FOR_EXACT_KIND_AND_SCOPE",
            authority_snapshot_refs=(_aref("relation"),),
            dependency_refs=(u1.ref, u2.ref),
            producer_replay_locator_or_reference_root=_root("bad-relation"),
            relation_id="R2",
            relation_kind="HARMONIZATION_ALIAS",
            source_universe_refs=(u1.ref, u2.ref),
            relation_authority_ref=_aref("relation"),
            effective_scope="ALL",
            overlap_or_nonduplication_evidence_refs=(),
            composition_estimand_refs=(),
            deduplication_rule_ref_if_any=None,
            negative_limit_refs=(),
            decision="AUTHORIZED",
        )


def test_predicate_canonicalizes_commutative_children_but_not_semantic_leaf_meaning():
    a = {"op": "LEAF", "leaf_type": "EMPIRICAL_POSITION_COORDINATE", "ref": "A"}
    b = {"op": "LEAF", "leaf_type": "SURVEY_RESPONSE_EVENT", "ref": "B"}
    left = canonicalize_predicate_ast({"op": "AND", "children": [a, b]})
    right = canonicalize_predicate_ast({"op": "AND", "children": [b, a, a]})
    assert left == right
    pred = make_empirical_predicate(
        typed_state="PREDICATE_RESOLVED_AUTHORIZED",
        authority_snapshot_refs=(_aref("query"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("predicate"),
        predicate_ast={"op": "AND", "children": [b, a]},
        grammar_authority_ref=_aref("query"),
        coordinate_question_value_refs=(_ref("FIELD", "A"), _ref("FIELD", "B")),
        risk_set_refs=(_ref("RISK_SET", "r"),),
        scope_refs=(_ref("SCOPE", "s"),),
        same_respondent_binding_semantics="SAME_SCOPED_RESPONDENT",
        operator_semantics_refs=(_ref("OP", "boolean"),),
    )
    assert pred.predicate_hash == semantic_hash(pred.predicate_ast)
    with pytest.raises(Pre553SemanticCollapseError):
        canonicalize_predicate_ast({"op": "LEAF", "leaf_type": "GENERATED_ACTOR_POSITION", "ref": "X"})


def test_diagnostic_material_cannot_masquerade_as_empirical_fact():
    with pytest.raises(Pre553SemanticCollapseError):
        _fact("nmi", diagnostic="NMI")


def test_discovery_mode_coverage_pair_is_exact_and_no_search_is_executed():
    authority = DiscoveryAuthority(
        typed_state="EXACT_BOUNDED_AUTHORIZED",
        authority_snapshot_refs=(_aref("discovery"),),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("discovery"),
        candidate_grammar_ref=_ref("CANDIDATE_GRAMMAR", "g"),
        candidate_universe_definition={"finite": True, "count": 8},
        source_universe_scope=(_ref("EMPIRICAL_UNIVERSE", "u"),),
        risk_set_scope=(_ref("RISK_SET", "r"),),
        topology_scope=("SCALAR", "JOINT"),
        measure_scope=("RAW",),
        support_rules=_ref("SUPPORT_RULE", "s"),
        validation_rules=_ref("VALIDATION_RULE", "v"),
        coverage_claim="COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        pruning_contract="NO_UNRECORDED_PRUNING",
        algorithm_identity_if_semantically_required=_ref("ALGORITHM", "a"),
        tie_order_rules=_ref("TIE_RULE", "t"),
        rng_policy_if_any=None,
        mode="EXACT_BOUNDED",
    )
    assert authority.mode == "EXACT_BOUNDED"
    with pytest.raises(Pre553IntegrityError):
        DiscoveryAuthority(
            typed_state="EXACT_BOUNDED_AUTHORIZED",
            authority_snapshot_refs=(_aref("discovery"),),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_root("discovery-bad"),
            candidate_grammar_ref=_ref("CANDIDATE_GRAMMAR", "g"),
            candidate_universe_definition={"finite": True},
            source_universe_scope=(_ref("EMPIRICAL_UNIVERSE", "u"),),
            risk_set_scope=(_ref("RISK_SET", "r"),),
            topology_scope=("SCALAR",),
            measure_scope=("RAW",),
            support_rules=_ref("SUPPORT_RULE", "s"),
            validation_rules=_ref("VALIDATION_RULE", "v"),
            coverage_claim="EXACT_RESULTS__NONEXHAUSTIVE_FRONTIER_COVERAGE",
            pruning_contract="NONE",
            algorithm_identity_if_semantically_required=_ref("ALGORITHM", "a"),
            tie_order_rules=_ref("TIE_RULE", "t"),
            rng_policy_if_any=None,
            mode="EXACT_BOUNDED",
        )


def test_structural_admission_type_does_not_make_the_admission_decision():
    fields = dict(
        authority_snapshot_refs=(_aref("admission"),),
        dependency_refs=(_ref("EMPIRICAL_FACT", "f"),),
        producer_replay_locator_or_reference_root=_root("admission"),
        admission_decision_state="ADMITTED",
        decision_reason_code="RULE_EXACT_PASS",
        empirical_query_spec_ref=_ref("EMPIRICAL_QUERY_SPEC", "q"),
        empirical_fact_ref=_ref("EMPIRICAL_FACT", "f"),
        admission_authority_ref=_aref("admission"),
        source_universe_refs=(_ref("EMPIRICAL_UNIVERSE", "u"),),
        native_scope_identity_refs=(_ref("SCOPE", "native"),),
        target_use="STRUCTURAL_MEDIATION_INPUT",
        target_use_permission_refs=(_ref("TARGET_USE_PERMISSION", "p"),),
        focal_structural_proposition_ref=_ref("STRUCTURAL_PROPOSITION", "p"),
        structural_semantic_identity_refs=(_ref("STRUCTURAL_SEMANTICS", "s"),),
        effective_time_or_interval_refs_required_by_target_use=(_ref("TIME", "t"),),
        estimand_refs=(_ref("ESTIMAND", "e"),),
        measure_and_weight_authority_refs=(_aref("weight"),),
        support_uncertainty_state="SUPPORTED",
        support_uncertainty_refs=(_ref("SUPPORT", "s"),),
        applicable_negative_denial_noncomparability_refs=(),
        interpretation_critical_authority_refs=(_aref("interpretation"),),
        authority_closure_refs=(_aref("admission"), _aref("interpretation")),
        structural_interpretation_payload={"role": "EXACT_RULE_OWNED_STRUCTURAL_MEANING"},
    )
    admission = StructuralEmpiricalAdmission(
        typed_state="ADMITTED_FOR_EXACT_STRUCTURAL_USE", **fields)
    assert admission.admission_decision_state == "ADMITTED"
    assert_zero_actor_v3_v2_effect(admission)
    with pytest.raises(Pre553IntegrityError):
        StructuralEmpiricalAdmission(typed_state="ADMISSION_DENIED", **fields)


def test_carrier_internal_and_deferred_names_cannot_substitute_public_families():
    for name in ("RespondentIdentity", "ReplayManifest", "V3EmpiricalPossibilityInput"):
        with pytest.raises(Pre553SemanticCollapseError):
            require_public_object_family(name)
    assert require_public_object_family("EmpiricalFact") == "EmpiricalFact"


def test_zero_direct_actor_v3_v2_effect_is_enforced():
    good = _universe("inert")
    assert_zero_actor_v3_v2_effect(good)
    bad = _universe("bad-effect", actor_state_effect=True)
    with pytest.raises(Pre553SemanticCollapseError):
        assert_zero_actor_v3_v2_effect(bad)
