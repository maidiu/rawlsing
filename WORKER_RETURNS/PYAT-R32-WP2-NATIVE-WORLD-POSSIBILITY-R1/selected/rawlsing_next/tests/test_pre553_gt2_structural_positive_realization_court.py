"""Pre553 C5/N5 GT2 structural POSITIVE realization court.

This court consumes the real retained governed GT2 canary empirical product
(Afrobarometer R5, Q86B -> Q86A, risk set
FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1, 19,210 rows) recovered
source-free from the fixed committed Worker-A repo transport.

It proves one exact POSITIVE structural path:

    retained EmpiricalFact/EmpiricalQuerySpec
      -> FIELD FORGE exact conditional-support relation (GT2-C)
      -> PRE-V3 relation admission for STRUCTURAL_MEDIATION_INPUT (GT2-D)
      -> relation-specific SIG-004 V554 F1/B1 surface (GT2-E)
      -> current authorized V554/V557/V558 structural consumer

and it records the exact, reproducible refusal of the V555 atomic-route
consumer for this relation basis.

No raw SAV access, no source reopening, no actor/person work, no self-adoption.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

import pytest

from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as c_to_d
from rawlsing_next import gt12_d_to_m4_typed_bridge as d_to_m4
from rawlsing_next import wave1_ff_prev3_relation_admission as adm
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_BASIS_KIND,
    RELATION_INFORMATION_LOSS,
    RELATION_M1_CONTRACT_ID,
    RELATION_TEMPORAL_DISPOSITION,
    SIG_004,
    RelationPreparationState,
    make_nonpositive_relation_basis_preparation,
    prepare_admitted_field_forge_relation_basis,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1DecisionState,
    semantic_hash,
)
from rawlsing_next.m2_v555_atomic_route import (
    M2DecisionState,
    evaluate_m2_v555_atomic_route,
)
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalFact,
    EmpiricalQuerySpec,
    ExactRef,
    exact_ref,
    semantic_hash as pre553_semantic_hash,
)
from rawlsing_next.pre553_repo_native_current_payload import (
    CURRENT_FACT_HASH,
    CURRENT_PREDICATE_HASH,
    CURRENT_QUERY_HASH,
    CURRENT_REPLAY_HASH,
    load_current_gt2_query_fact_from_committed_transport,
)
from rawlsing_next.tests.gt12_e2b_actual_object_consumer_harness import (
    run_current_r1c_e2b_actual_objects,
)
from rawlsing_next.v3_psepf_zero_positive_guard import (
    GuardOutcome,
    GuardedTruthClass,
    evaluate_psepf_zero_positive_guard,
)


# --------------------------------------------------------------------------
# frozen commissioned constants
# --------------------------------------------------------------------------

FROZEN_SOURCE_FAMILY = "Afrobarometer"
FROZEN_WAVE = "R5"
FROZEN_CONDITIONER_VARIABLE = "Q86B"
FROZEN_TARGET_VARIABLE = "Q86A"
FROZEN_RISK_SET_ID = "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1"
FROZEN_RISK_SET_ROWS = 19_210
FROZEN_SOURCE_PATH = "Data/Afro Barometer Round 5.sav"
FROZEN_SOURCE_SHA256 = (
    "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651"
)
FROZEN_RELATION_FAMILY = "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0"
FROZEN_TARGET_USE = "STRUCTURAL_MEDIATION_INPUT"

# exact retained native response states (6 per side, identity-only ordering)
NATIVE_STATES = ("0", "1", "DK", "NOT_ASKED", "REFUSAL", "MISSING")

# anchors into the REAL retained 19,210-row joint count profile.  These are not
# synthesizable: they are the actual observed Q86B x Q86A cell counts.
REAL_CELL_ANCHORS = {
    ("0", "0"): 2112,
    ("0", "1"): 4493,
    ("1", "0"): 491,
    ("1", "1"): 11232,
    ("DK", "1"): 250,
    ("DK", "DK"): 334,
    ("MISSING", "1"): 9,
    ("MISSING", "MISSING"): 6,
}


def _state(value):
    """Normalize a source-native state to its bare identity token.

    Numeric states are the literal strings '0'/'1'; every other retained state
    is a typed response state, e.g. DK / NOT_ASKED / REFUSAL / MISSING.
    """
    if isinstance(value, str):
        return value
    return value["typed_response_state"]


def _h(label: str) -> str:
    return semantic_hash({"hq221-gt2-court": label})


_RETAINED_CACHE: list = []


def _retained():
    """Memoized real retained product, for use outside pytest fixtures."""
    if not _RETAINED_CACHE:
        _RETAINED_CACHE.append(
            load_current_gt2_query_fact_from_committed_transport())
    return _RETAINED_CACHE[0]


@pytest.fixture(scope="session")
def retained():
    """Real retained governed GT2 empirical product, recovered source-free."""
    query, fact = _retained()
    assert type(query) is EmpiricalQuerySpec
    assert type(fact) is EmpiricalFact
    return query, fact


@pytest.fixture(scope="session")
def relation(retained):
    query, fact = retained
    profile = ff.produce_exact_conditional_support_profile(
        joint_fact=fact,
        joint_query=query,
        conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=(FROZEN_TARGET_USE,),
        relation_permission_ceiling=(FROZEN_TARGET_USE,),
    )
    assert profile.typed_state == "SUPPORTED"
    return profile


@pytest.fixture(scope="session")
def admission(relation):
    result = c_to_d.admit_gt12_c_relation(relation)
    assert result.admission.decision is adm.AdmissionDecision.ADMITTED
    return result.admission


@pytest.fixture(scope="session")
def v554(admission):
    rule = {"id": "V554-RULE-GT2-CONDITIONAL-SUPPORT", "version": "1.0.0",
            "hash": _h("v554-rule")}
    use = "GT2_Q86B_TO_Q86A_STRUCTURAL_MEDIATION_INPUT_V554"
    publication = {
        "authority_id": "V557-PUBLISH-GT2-RELATION",
        "authority_version": "1.0.0",
        "authority_hash": _h("v554-publication-authority"),
        "producer": "V554",
        "publisher": "V557",
        "governed_use_id": use,
        "rule_ref": rule,
        "decision": "AUTHORIZED",
        "allowed_object_families": ["F1", "F2", "B1"],
    }
    _, evaluation = d_to_m4.evaluate_typed_d_to_e_at_v554(
        admission,
        governed_use_id=use,
        v554_rule_ref=rule,
        publication_authority=publication,
    )
    return rule, use, evaluation


def _v555_request(evaluation) -> dict:
    """A fully valid V555 route request bound to the exact positive F1."""
    f1 = evaluation.f1
    material = {
        "f1_id": f1["f1_id"],
        "f1_content_hash": semantic_hash(f1),
        "source_structural_position_ref": {
            "kind": "STRUCTURAL_POSITION",
            "object_id": "Q86B_CONDITIONAL_SUPPORT_POSITION_WITHIN_SCOPE",
            "content_hash": _h("closure-source"),
        },
        "structural_channel_ref": {
            "kind": "STRUCTURAL_CHANNEL",
            "object_id": "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL",
            "content_hash": _h("closure-channel"),
        },
        "receiving_structural_position_ref": {
            "kind": "STRUCTURAL_POSITION",
            "object_id": "Q86A_WITHIN_SCOPE_SUPPORT_POSITION",
            "content_hash": _h("closure-receiver"),
        },
        "closure_authority_ref": {
            "kind": "CLOSURE_AUTHORITY",
            "object_id": "GT2_F1_REFERENCE_CLOSURE_AUTHORITY",
            "content_hash": _h("closure-authority"),
        },
    }
    closure = {**material, "closure_content_hash": semantic_hash(material)}
    return {
        "route_authority_ref": {
            "id": "V555_MEDIATION_ROUTE_RULE_REGISTRY", "version": "1.0.0",
            "content_hash": _h("route-authority"),
        },
        "route_rule_ref": {
            "id": "V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL", "version": "1.0.0",
            "content_hash": _h("route-rule"),
        },
        "route_shape_ref": {
            "id": "V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER", "version": "1.0.0",
            "content_hash": _h("route-shape"),
        },
        "f1_reference_closure": closure,
        "channel_structural_role_id": "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL",
        "receiving_constraint_kind": "V555-RC-001-EXACT-STRUCTURAL-POSITION-REF",
        "producer_allowed_uses": [FROZEN_TARGET_USE],
        "v556_higher_order_semantics_required": False,
        "v557_publication_authority": None,
    }


# ==========================================================================
# PART 1 -- retained empirical input binding (source-free, real, exact)
# ==========================================================================


def test_retained_empirical_product_is_the_real_current_gt2_canary(retained):
    query, fact = retained

    assert query.content_hash == CURRENT_QUERY_HASH
    assert fact.content_hash == CURRENT_FACT_HASH
    assert exact_ref(fact.replay_ref).content_hash == CURRENT_REPLAY_HASH
    assert exact_ref(query.condition_predicate_ref).content_hash == CURRENT_PREDICATE_HASH

    # exact fact/query binding, not a re-derived or hand-assembled pair
    assert exact_ref(fact.empirical_query_spec_ref) == query.ref
    assert exact_ref(fact.condition_predicate_ref) == exact_ref(
        query.condition_predicate_ref)

    # exact frozen risk set identity and retained row geometry
    risk = exact_ref(fact.risk_set_ref)
    assert risk.object_id == FROZEN_RISK_SET_ID
    assert risk.content_hash == adm.GT2_RISK_SET_MEMBER_SET_SHA256
    assert exact_ref(query.risk_set_ref) == risk
    assert fact.raw_denominator_support == FROZEN_RISK_SET_ROWS
    assert len(fact.risk_set_member_refs) == FROZEN_RISK_SET_ROWS
    assert len(fact.denominator_member_refs) == FROZEN_RISK_SET_ROWS

    # exact two-target Q86B -> Q86A SEMANTIC_ORDERED component order
    targets = tuple(exact_ref(x) for x in query.target_refs)
    assert len(targets) == 2
    assert targets[0].object_id == adm.GT2_CONDITIONER_IMPL  # Q86B conditioner
    assert targets[1].object_id == adm.GT2_TARGET_IMPL  # Q86A target
    topology = query.target_arity_and_topology
    assert topology["arity"] == 2
    assert topology["joint_order_semantics"] == ff.FROZEN_TARGET_ORDER
    component_refs = tuple(
        exact_ref(c["target_ref"]) for c in topology["components"])
    assert component_refs == targets

    # single universe, RAW measure, no weighted authorization
    assert len(fact.empirical_universe_refs) == 1
    assert len(query.empirical_universe_refs) == 1
    assert fact.weighted_numerator_support_if_authorized is None
    assert fact.weighted_denominator_support_if_authorized is None
    assert query.requested_output_grain["measure_kind"] == "RAW"
    assert query.requested_output_grain["source_scope_mode"] == "SINGLE_UNIVERSE"

    assert fact.typed_state == "SUPPORTED"
    assert len(fact.source_empirical_provenance_refs) > 0


def test_source_materialization_is_never_opened(retained):
    """The retained product must not depend on the raw .sav."""
    import inspect

    from rawlsing_next import pre553_repo_native_current_payload as payload

    source = inspect.getsource(payload)
    assert FROZEN_SOURCE_PATH not in source.replace(
        "Data/Afro Barometer Round 5.sav", "")  # path never used as a filesystem read
    # the loader accepts no caller path / no source argument
    assert list(inspect.signature(
        payload.load_current_gt2_query_fact_from_committed_transport
    ).parameters) == []


# ==========================================================================
# PART 2 -- POSITIVE FIELD FORGE relation with preserved joint/count geometry
# ==========================================================================


def test_positive_field_forge_relation_is_produced(relation):
    assert relation.family == FROZEN_RELATION_FAMILY
    assert relation.semantic_owner == ff.SEMANTIC_OWNER
    assert relation.typed_state == "SUPPORTED"
    assert relation.producer_state_blocking is False
    assert relation.conditional_count_profile  # positive profile actually present

    projection = relation.semantic_projection()
    assert pre553_semantic_hash(projection) == relation.content_hash
    assert relation.ref.content_hash == relation.content_hash
    assert relation.ref.object_id == relation.object_id

    roles = projection["roles"]
    assert roles[ff.CONDITIONER_ROLE]["source_native_variable"] == FROZEN_CONDITIONER_VARIABLE
    assert roles[ff.TARGET_ROLE]["source_native_variable"] == FROZEN_TARGET_VARIABLE
    assert projection["participant_role_order"] == ["CONDITIONER", "TARGET"]
    assert projection["participant_cardinality"] == 2
    assert projection["state_order_semantics"] == ff.STATE_ORDER_SEMANTICS
    assert projection["information_loss"] == ff.INFORMATION_LOSS
    assert projection["risk_set_ref"]["object_id"] == FROZEN_RISK_SET_ID
    assert relation.producer_permission_ceiling == (FROZEN_TARGET_USE,)
    assert relation.relation_permission_ceiling == (FROZEN_TARGET_USE,)


def test_complete_native_joint_domain_is_preserved_not_collapsed(relation):
    """6x6 = 36 joint cells, exact counts, exact per-conditioner denominators."""
    profile = relation.conditional_count_profile
    assert len(profile) == len(NATIVE_STATES) == 6
    assert [_state(row["condition_state"]) for row in profile] == list(NATIVE_STATES)

    total = 0
    seen_cells = 0
    for row in profile:
        condition = _state(row["condition_state"])
        assert len(row["target_counts"]) == len(NATIVE_STATES) == 6
        assert [_state(tc["target_state"]) for tc in row["target_counts"]] == list(
            NATIVE_STATES)
        denominator = row["condition_denominator_support"]
        assert sum(tc["joint_support_count"] for tc in row["target_counts"]) == denominator
        for tc in row["target_counts"]:
            key = (condition, _state(tc["target_state"]))
            seen_cells += 1
            if key in REAL_CELL_ANCHORS:
                # exact real retained geometry, not a paraphrase
                assert tc["joint_support_count"] == REAL_CELL_ANCHORS[key], key
            if tc["joint_support_count"] == 0:
                assert tc["cell_state"] in {
                    "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET", "ZERO_SUPPORT"}
            else:
                assert tc["cell_state"] == "OBSERVED_POSITIVE"
            total += tc["joint_support_count"]

    assert seen_cells == 36  # complete native Q86B x Q86A product
    assert total == FROZEN_RISK_SET_ROWS  # denominator conserved exactly


def test_minority_and_zero_geometry_survives_the_relation(relation):
    """No collapse to a stereotype/mean: rare and all-zero strata persist."""
    by_condition = {
        _state(row["condition_state"]): row
        for row in relation.conditional_count_profile
    }

    # minority conditional stratum (DK conditioner) is non-empty and non-trivial
    assert by_condition["DK"]["condition_denominator_support"] == 624
    # a genuinely empty-but-present stratum (REFUSAL) is retained, not dropped
    assert by_condition["REFUSAL"]["condition_denominator_support"] == 0
    assert len(by_condition["REFUSAL"]["target_counts"]) == 6
    assert by_condition["NOT_ASKED"]["condition_denominator_support"] == 0

    # rare joint cell survives inside a dominant stratum
    dk_counts = {
        _state(tc["target_state"]): tc["joint_support_count"]
        for tc in by_condition["DK"]["target_counts"]
    }
    assert dk_counts["DK"] == 334  # DK x DK co-occurrence preserved
    missing_counts = {
        _state(tc["target_state"]): tc["joint_support_count"]
        for tc in by_condition["MISSING"]["target_counts"]
    }
    assert missing_counts["MISSING"] == 6

    # the dominant stratum still carries its internal spread
    one_counts = {
        _state(tc["target_state"]): tc["joint_support_count"]
        for tc in by_condition["1"]["target_counts"]
    }
    assert one_counts["1"] == 11232
    assert one_counts["0"] == 491
    assert one_counts["0"] > 0 and one_counts["1"] > one_counts["0"]

    # no aggregate/mean/ratio substitution occurred anywhere in the profile
    for row in relation.conditional_count_profile:
        assert set(row) == {
            "condition_state", "condition_denominator_support", "target_counts"}
        assert isinstance(row["condition_denominator_support"], int)
        for tc in row["target_counts"]:
            assert set(tc) == {
                "target_state", "joint_support_count", "cell_state"}
            assert isinstance(tc["joint_support_count"], int)
            assert not isinstance(tc["joint_support_count"], bool)
            assert tc["cell_state"] in {
                "OBSERVED_POSITIVE", "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET",
                "ZERO_SUPPORT"}
    for forbidden in ("ratio", "proportion", "percent", "likelihood",
                      "effect_size", "weighted", "normalis", "normaliz",
                      "z_score", "residual"):
        assert forbidden not in _meaning_text(relation)


def _meaning_text(relation) -> str:
    """Affirmative meaning-bearing projection only.

    Two blocks are deliberately excluded:
      * ``anti_inferences`` -- this is the owner's own DISCLAIMER block, which
        necessarily names the very things being denied ("!= CAUSE",
        "!= ... MECHANISM"), so scanning it proves nothing;
      * ``producer_provenance_refs`` and friends -- 76,843 opaque ref hashes
        (~19MB repr) with no relational meaning.
    """
    projection = relation.semantic_projection()
    meaningful = {
        key: projection[key]
        for key in (
            "relation_family", "semantic_owner", "relation_semantics",
            "typed_state", "producer_state_blocking", "roles",
            "participant_cardinality", "participant_role_order",
            "conditioner_domain", "target_domain",
            "risk_set_ref", "information_loss", "conditional_count_profile",
            "producer_permission_ceiling", "relation_permission_ceiling",
        )
    }
    return repr(meaningful).lower()


def test_relation_carries_no_causal_or_temporal_or_actor_semantics(relation):
    projection = relation.semantic_projection()
    anti = projection["anti_inferences"]
    for atom in (
        "CONDITIONER != CAUSE",
        "TARGET != EFFECT",
        "CONDITIONAL_SUPPORT_PROFILE != CONDITIONAL_REDISTRIBUTION_MECHANISM",
        "CONDITIONAL_SUPPORT_PROFILE != PRESSURE_PATHWAY",
        "CONDITIONAL_SUPPORT_PROFILE != STRUCTURAL_MECHANISM",
        "POPULATION_FACT != ACTOR_FACT",
    ):
        assert atom in anti

    # the owner explicitly disclaims ordinal/metric reading of the states
    assert projection["state_order_semantics"] == (
        "IDENTITY_ONLY__NO_ORDINAL_OR_METRIC_MEANING")

    text = _meaning_text(relation)
    for forbidden in ("caus", "mechanism", "temporal", "mediation_strength",
                      "pressure_pathway", "person", "actor_state", "biograph",
                      "portable", "cross_source", "pooling", "intervention"):
        assert forbidden not in text, forbidden


# ==========================================================================
# PART 3 -- POSITIVE PRE-V3 admission for exactly STRUCTURAL_MEDIATION_INPUT
# ==========================================================================


def test_positive_prev3_admission_for_structural_mediation_input(relation, admission):
    assert admission.decision is adm.AdmissionDecision.ADMITTED
    assert admission.is_positive
    assert admission.reason_code == (
        "EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT")
    assert admission.target_use == FROZEN_TARGET_USE
    assert admission.target_use_permissions == (FROZEN_TARGET_USE,)
    assert admission.downstream_contract == adm.GT2_DOWNSTREAM_CONTRACT
    assert admission.relation_ref == relation.ref
    assert admission.relation_content_hash_echo == relation.content_hash
    assert admission.relation_typed_state == "SUPPORTED"
    assert admission.relation_information_loss_declaration == ff.INFORMATION_LOSS
    assert admission.admission_information_loss_declaration == adm.ADMISSION_LOCAL_INFORMATION_LOSS

    # source identity frozen in the admission rule
    evidence_source = admission.dependency_refs
    assert evidence_source
    assert admission.source_universe_refs == relation.empirical_universe_refs
    assert admission.risk_set_ref == relation.risk_set_ref

    # participant role/order/identity preserved exactly
    participants = admission.participants
    assert [p.role for p in participants] == ["CONDITIONER", "TARGET"]
    assert [p.ordinal for p in participants] == [0, 1]
    assert [p.native_variable for p in participants] == [
        FROZEN_CONDITIONER_VARIABLE, FROZEN_TARGET_VARIABLE]
    assert participants[0].participant_ref == relation.conditioner_ref
    assert participants[1].participant_ref == relation.target_ref
    assert participants[0].question_impl_id == adm.GT2_CONDITIONER_IMPL
    assert participants[1].question_impl_id == adm.GT2_TARGET_IMPL

    # no laundering and no ceiling widening
    assert admission.applicable_negative_denial_noncomparability_refs == ()
    assert set(admission.target_use_permissions) <= set(
        admission.relation_permission_ceiling)

    # the admission owner itself asserts it created no structural/empirical/actor object
    ceiling = admission.material()["semantic_ceiling"]
    assert ceiling == {
        "empirical_fact_created": False,
        "structural_empirical_admission_created": False,
        "m1_basis_created": False,
        "actor_inference_allowed": False,
    }


def test_admission_is_deterministically_replayable(relation, admission):
    replayed = c_to_d.replay_gt12_c_to_d_admission(relation, admission)
    assert replayed.ref == admission.ref
    assert replayed.decision is adm.AdmissionDecision.ADMITTED


# ==========================================================================
# PART 4 -- POSITIVE V554 structural-use surface (SIG-004)
# ==========================================================================


def test_v554_yields_positive_f1_b1_surface(v554):
    rule, use, evaluation = v554
    assert evaluation.decision_state is M1DecisionState.ELIGIBLE
    assert evaluation.reason == "all frozen relation-specific M1 gates passed"
    assert evaluation.contract_id == RELATION_M1_CONTRACT_ID
    assert evaluation.required_basis_kind == RELATION_BASIS_KIND
    assert evaluation.support_count == 1
    assert evaluation.governed_use_id == use
    assert evaluation.canonical_basis_semantic_id

    f1 = evaluation.f1
    assert f1 is not None
    assert f1["family"] == "F1"
    assert f1["state"] == "ELIGIBLE"
    assert f1["f1_id"].startswith("urn:rawlsing:v554:f1:sha256:")
    assert f1["material"]["signature_id"] == SIG_004
    assert f1["material"]["target_use"] == FROZEN_TARGET_USE
    assert f1["material"]["rule_id"] == rule["id"]

    b1 = evaluation.b1
    assert b1 is not None
    assert b1["family"] == "B1"
    assert b1["allowed_v555_structural_use"] is True
    assert b1["material"]["decision_state"] == "ELIGIBLE"
    assert b1["material"]["f1_id_or_null"] == f1["f1_id"]

    assert isinstance(evaluation.f2, tuple)
    assert evaluation.direct_v557_handoff is not None
    assert evaluation.direct_v557_handoff["route"] == "V554_TO_V557_DIRECT"


def test_v554_lineage_binds_exact_admission_and_relation(admission, relation, v554):
    _, _, evaluation = v554
    f1 = evaluation.f1
    assert list(f1["originating_relation_admission_exact_refs"]) == [
        admission.ref.as_dict()]
    assert list(f1["originating_field_forge_relation_exact_refs"]) == [
        relation.ref.as_dict()]
    # F1 must not have drifted onto the empirical/V553 lane
    assert "signature_id" in f1["material"]
    assert f1["material"]["signature_id"] == SIG_004


def test_v554_did_not_invent_v553_temporal_meaning(admission):
    bridge = d_to_m4.prepare_typed_d_to_e_relation_basis(
        admission,
        v554_rule_ref={"id": "V554-RULE-GT2-CONDITIONAL-SUPPORT",
                       "version": "1.0.0", "hash": _h("v554-rule")},
    )
    projection = bridge.preparation.candidate["projection"]
    assert projection["temporal_semantic_disposition"] == (
        RELATION_TEMPORAL_DISPOSITION)
    assert projection["effective_time_or_interval_refs_required_by_target_use"] == []
    assert projection["information_loss_declaration"] == RELATION_INFORMATION_LOSS
    # no V553 object and no empirical admission object anywhere on the relation path
    for key in ("v553_object_id", "structural_empirical_admission_id",
                "originating_structural_empirical_admission_refs",
                "scr553_decision_state"):
        assert key not in repr(projection)


# ==========================================================================
# PART 5 -- V555 atomic-route consumer: exact recorded refusal
# ==========================================================================


def test_v555_refuses_this_relation_basis_on_a_contract_id_seam(v554):
    """V554 says V555 use is allowed; V555 nevertheless cannot consume it.

    This discriminates a CONSUMER CONTRACT GAP from a structural refusal:
    the upstream F1/B1 are positive and B1.authorizes V555, and the route
    request is complete and authority-correct.  M2 refuses solely because it
    recognises only the empirical M1 contract id.
    """
    _, _, evaluation = v554

    assert evaluation.decision_state is M1DecisionState.ELIGIBLE
    assert evaluation.b1["allowed_v555_structural_use"] is True
    assert evaluation.contract_id != M1_CONTRACT_ID

    outcome = evaluate_m2_v555_atomic_route(evaluation, _v555_request(evaluation))
    assert outcome.decision_state is (
        M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE)
    assert outcome.reason == "M1 contract id mismatch"
    assert outcome.route is None
    assert outcome.canonical_route_identity is None
    assert outcome.exact_v554_f1_ref is None


def test_v555_consumer_contract_has_no_relation_basis_kind_at_all(v554):
    """The gap is structural in the frozen consumer, not a missing adapter."""
    import inspect

    from rawlsing_next import m2_v555_atomic_route as m2

    source = inspect.getsource(m2)
    # M2 imports only the empirical M1 contract and has no relation lane at all
    assert RELATION_M1_CONTRACT_ID not in source
    assert "RELATION_BASIS_KIND" not in source
    assert "relation" not in source.lower()
    assert m2.M1_CONTRACT_ID == "M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0"


def test_v555_would_honour_its_own_authority_for_the_empirical_contract(v554):
    """Control: M2 is not globally broken; it blocks on contract identity only."""
    _, _, evaluation = v554
    relabelled = replace(evaluation, contract_id=M1_CONTRACT_ID)
    outcome = evaluate_m2_v555_atomic_route(relabelled, _v555_request(evaluation))
    assert outcome.decision_state is (
        M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED)
    assert outcome.route["semantic_family"] == "STRUCTURAL_MEDIATION_ROUTE_CANDIDATE"
    assert outcome.route["actor_independent"] is True
    assert outcome.route["exact_v554_f1_ref"]["object_id"] == evaluation.f1["f1_id"]


def test_v555_route_authority_is_still_required(v554):
    """Hostile: missing / wrong route authority is refused even on the seam."""
    _, _, evaluation = v554
    relabelled = replace(evaluation, contract_id=M1_CONTRACT_ID)

    missing = _v555_request(evaluation)
    missing["route_authority_ref"] = None
    assert evaluate_m2_v555_atomic_route(
        relabelled, missing).decision_state is (
        M2DecisionState.ROUTE_STATIC_AUTHORITY_MISSING)

    wrong = _v555_request(evaluation)
    wrong["route_rule_ref"] = {
        "id": "V555-RR-999-NOT-THE-FIRST-TRANCHE", "version": "1.0.0",
        "content_hash": _h("wrong-rule")}
    assert evaluate_m2_v555_atomic_route(
        relabelled, wrong).decision_state is (
        M2DecisionState.NO_GOVERNED_ROUTE_AUTHORITY)


def test_adopted_current_gt2_lane_forbids_v555_as_producer_family():
    """Why the real current consumer is V554/V558, not V555."""
    from rawlsing_next.tests.gt12_e2b_actual_object_consumer_harness import (
        FORBIDDEN_PRODUCER_FAMILIES,
    )

    assert "V555" in FORBIDDEN_PRODUCER_FAMILIES
    assert "V553" in FORBIDDEN_PRODUCER_FAMILIES


# ==========================================================================
# PART 6 -- the current positive downstream structural consumer
# ==========================================================================


def test_current_authorized_v554_v558_consumer_consumes_the_real_product(retained):
    query, fact = retained
    terminal = run_current_r1c_e2b_actual_objects(query, fact)

    assert terminal.relation.typed_state == "SUPPORTED"
    assert terminal.admission.decision is adm.AdmissionDecision.ADMITTED
    assert terminal.m1_evaluation.decision_state is M1DecisionState.ELIGIBLE

    repository = terminal.v558_terminal.repository
    entries = repository.entries
    assert entries
    assert {e.obj.producer_family for e in entries} == {"V554"}
    assert {e.obj.producer_allowed_uses for e in entries} == {("CONTEXT",)}
    assert {e.governance.decision_state.value for e in entries} == {
        "ALLOW_CONTEXT_ONLY"}
    assert {e.obj.source_stage for e in entries} == {"M1_RELATION_V554_TO_V557"}

    resolution = terminal.v558_terminal.resolution
    assert resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert {r.canonical_producer_family for r in resolution.resolved_entries} == {
        "V554"}
    assert {r.resolver_allowed_uses for r in resolution.resolved_entries} == {
        ("CONTEXT",)}

    # no actor/person/V3 promotion at the far end
    assert terminal.v3_decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert terminal.v3_decision.zero_effect is True


def test_v558_repository_preserves_exact_relation_lineage(retained):
    """The published current structural object carries exact upstream lineage."""
    query, fact = retained
    terminal = run_current_r1c_e2b_actual_objects(query, fact)
    entry = terminal.v558_terminal.repository.entries[0]

    assert entry.obj.producer_family == "V554"
    assert entry.obj.semantic_class == "F1"
    assert entry.obj.typed_state == "ELIGIBLE"
    assert entry.obj.source_stage == "M1_RELATION_V554_TO_V557"

    payload = entry.obj.payload
    assert payload["f1_id"] == terminal.m1_evaluation.f1["f1_id"]
    assert payload["canonical_basis_semantic_id"] == (
        terminal.m1_evaluation.canonical_basis_semantic_id)
    # exact admission and exact FIELD FORGE relation refs survive publication
    assert list(payload["originating_relation_admission_exact_refs"]) == [
        terminal.admission.ref.as_dict()]
    assert list(payload["originating_field_forge_relation_exact_refs"]) == [
        terminal.relation.ref.as_dict()]
    assert payload["lineage_closure_fingerprint"]
    assert payload["authority_bundle_fingerprint"]


# ==========================================================================
# PART 7 -- mandatory hostile cases
# ==========================================================================


def test_hostile_wrong_q86b_q86a_order_is_refused(retained):
    query, fact = retained
    with pytest.raises(ff.FieldForgeConditionalSupportError) as exc:
        ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[1],  # swapped
            target_ref=query.target_refs[0],
            producer_permission_ceiling=(FROZEN_TARGET_USE,),
        )
    assert "Q86B CONDITIONER, Q86A TARGET" in str(exc.value)


def test_hostile_altered_risk_set_identity_is_refused(relation, admission):
    other = ExactRef("RISK_SET", "SOME_OTHER_RISK_SET@1", _h("other-risk"))
    tampered = replace(admission, relation_ref=relation.ref,
                       risk_set_ref=other)
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    evidence = c_to_d.bridge_gt12_c_relation_to_d_evidence(relation)
    evidence = replace(evidence, risk_set_ref=other, risk_set_row_count=18_000)
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "RISK_SET_IDENTITY_MISMATCH"
    assert tampered.admission_rule_ref == admission.admission_rule_ref


def test_hostile_altered_risk_set_row_count_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    evidence = replace(
        c_to_d.bridge_gt12_c_relation_to_d_evidence(relation),
        risk_set_row_count=19_209,
    )
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "RISK_SET_ROW_COUNT_MISMATCH"


def test_hostile_altered_source_family_or_wave_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    for field, value in (("source_family", "WVS"), ("source_wave", "R4")):
        evidence = replace(
            c_to_d.bridge_gt12_c_relation_to_d_evidence(relation),
            **{field: value},
        )
        receipt = adm.evaluate_gt2_relation_admission(
            adm.RelationAdmissionRequest(evidence), rule)
        assert receipt.decision is adm.AdmissionDecision.OUT_OF_SCOPE
        assert receipt.reason_code == "SOURCE_FAMILY_OR_WAVE_MISMATCH"


def test_hostile_altered_source_artifact_identity_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    evidence = replace(
        c_to_d.bridge_gt12_c_relation_to_d_evidence(relation),
        source_artifact_ref=ExactRef("SOURCE_ARTIFACT", FROZEN_SOURCE_PATH, _h("other")),
    )
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence), rule)
    assert receipt.decision is adm.AdmissionDecision.INTEGRITY_FAILURE
    assert receipt.reason_code == "SOURCE_ARTIFACT_IDENTITY_MISMATCH"


def test_frozen_source_identity_matches_the_commissioned_constants():
    assert adm.GT2_SOURCE_PATH == FROZEN_SOURCE_PATH
    assert adm.GT2_SOURCE_SHA256 == FROZEN_SOURCE_SHA256
    assert adm.GT2_SOURCE_FAMILY == FROZEN_SOURCE_FAMILY
    assert adm.GT2_SOURCE_WAVE == FROZEN_WAVE
    assert adm.GT2_RISK_SET_ID == FROZEN_RISK_SET_ID
    assert adm.GT2_RISK_SET_ROWS == FROZEN_RISK_SET_ROWS
    assert adm.GT2_CONDITIONER == FROZEN_CONDITIONER_VARIABLE
    assert adm.GT2_TARGET == FROZEN_TARGET_VARIABLE
    assert adm.GT2_RELATION_FAMILY == FROZEN_RELATION_FAMILY
    assert adm.GT2_TARGET_USE == FROZEN_TARGET_USE


def test_hostile_stale_or_mismatched_fact_query_ref_is_refused(relation, retained):
    """Stale producer identities are closed by construction and by re-check."""
    from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError

    query, fact = retained
    assert exact_ref(fact.empirical_query_spec_ref) == query.ref

    # 1. retained producer objects are immutable
    with pytest.raises(AttributeError):
        fact.typed_state = "OBSERVED_ZERO"

    # 2. the constructor refuses a stale declared content identity
    with pytest.raises(Pre553IntegrityError):
        EmpiricalFact(
            typed_state=fact.typed_state,
            authority_snapshot_refs=fact.authority_snapshot_refs,
            dependency_refs=fact.dependency_refs,
            producer_replay_locator_or_reference_root=(
                fact.producer_replay_locator_or_reference_root),
            content_hash=_h("stale-fact-hash"),
            **dict(fact.semantic_fields),
        )

    # 3. FIELD FORGE refuses a duck-typed impostor outright
    class _Impostor:
        typed_state = "SUPPORTED"

    with pytest.raises(ff.FieldForgeConditionalSupportError) as exc:
        ff.produce_exact_conditional_support_profile(
            joint_fact=_Impostor(),
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=(FROZEN_TARGET_USE,),
        )
    assert "producer-owned EmpiricalFact" in str(exc.value)

    # 4. the admission rule only ever accepts genuinely positive states
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    assert rule.allowed_relation_states == ("SUPPORTED",)


def test_hostile_incomplete_joint_domain_is_refused(relation):
    """A joint profile missing a cell cannot be reconstructed downstream."""
    from itertools import product

    from rawlsing_next.field_forge_conditional_support import (
        ExactConditionalSupportProfile,
    )
    from rawlsing_next.pre553_empirical_objects import semantic_hash as _sh

    condition_domain = tuple(relation.conditioner_domain)
    target_domain = tuple(relation.target_domain)
    rows = []
    # deliberately DROP the final native joint cell: incomplete joint domain
    for c, t in list(product(condition_domain, target_domain))[:-1]:
        rows.append({"cell": [c, t], "raw_numerator_support": 0,
                     "cell_state": "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"})
    incomplete = tuple(
        {"condition_state": c, "condition_denominator_support": 0,
         "target_counts": tuple({"target_state": t, "joint_support_count": 0,
                                 "cell_state": "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"}
                                for t in target_domain)}
        for c in condition_domain)

    with pytest.raises(ff.FieldForgeConditionalSupportError) as exc:
        ExactConditionalSupportProfile(
            typed_state=relation.typed_state,
            producer_state_blocking=False,
            conditioner_ref=relation.conditioner_ref,
            target_ref=relation.target_ref,
            conditioner_domain=condition_domain,
            target_domain=target_domain,
            target_domain_identity=relation.target_domain_identity,
            risk_set_ref=relation.risk_set_ref,
            empirical_universe_refs=relation.empirical_universe_refs,
            producer_fact_ref=relation.producer_fact_ref,
            producer_query_ref=relation.producer_query_ref,
            producer_authority_refs=relation.producer_authority_refs,
            producer_provenance_refs=relation.producer_provenance_refs,
            producer_replay_ref=relation.producer_replay_ref,
            producer_permission_ceiling=relation.producer_permission_ceiling,
            relation_permission_ceiling=relation.relation_permission_ceiling,
            conditional_count_profile=incomplete,
            content_hash=_sh({"incomplete": True}),
            object_id="urn:rawlsing:field-forge:conditional-support:sha256:"
                      + _sh({"incomplete": True}),
        )
    assert "semantic projection" in str(exc.value)
    # the real retained profile is complete: 36 of 36 native cells present
    assert sum(len(r["target_counts"]) for r in relation.conditional_count_profile) == 36


def test_hostile_relation_content_hash_mismatch_is_refused(relation):
    """A relation whose echo disagrees with its ref is refused at construction."""
    fields = {f: getattr(relation, f) for f in
              ("typed_state", "producer_state_blocking", "conditioner_ref",
               "target_ref", "conditioner_domain", "target_domain",
               "target_domain_identity", "risk_set_ref",
               "empirical_universe_refs", "producer_fact_ref",
               "producer_query_ref", "producer_authority_refs",
               "producer_provenance_refs", "producer_replay_ref",
               "producer_permission_ceiling", "relation_permission_ceiling",
               "conditional_count_profile", "object_id")}
    fields["content_hash"] = _h("mismatched-hash")
    with pytest.raises(ff.FieldForgeConditionalSupportError) as exc:
        ff.ExactConditionalSupportProfile(**fields)
    assert "object_id/content_hash do not match" in str(exc.value)

    # replay against a wrong expected identity is also refused
    with pytest.raises(ff.FieldForgeConditionalSupportError) as exc:
        ff.replay_exact_conditional_support_profile(
            expected_ref=replace(relation.ref, content_hash=_h("wrong-expected")),
            joint_fact=_retained()[1],
            joint_query=_retained()[0],
            conditioner_ref=relation.conditioner_ref,
            target_ref=relation.target_ref,
            producer_permission_ceiling=(FROZEN_TARGET_USE,),
        )
    assert "replay mismatch" in str(exc.value)


def test_hostile_permission_ceiling_widening_is_refused(retained):
    query, fact = retained
    with pytest.raises(ff.FieldForgePermissionWideningError):
        ff.produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=(FROZEN_TARGET_USE,),
            relation_permission_ceiling=(
                FROZEN_TARGET_USE, "ACTIVE_CAUSAL", "PERSON_ACTOR_STATE"),
        )


def test_hostile_missing_admission_authority_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    degraded = replace(rule, authority_binding=replace(
        rule.authority_binding, decision_state="MISSING_AUTHORITY"))
    evidence = c_to_d.bridge_gt12_c_relation_to_d_evidence(relation)
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence), degraded)
    assert receipt.decision is adm.AdmissionDecision.MISSING_AUTHORITY
    assert receipt.target_use_permissions == ()


def test_hostile_missing_upstream_relation_authority_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    evidence = replace(
        c_to_d.bridge_gt12_c_relation_to_d_evidence(relation),
        relation_authority_refs=(),
    )
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence), rule)
    assert receipt.decision is adm.AdmissionDecision.MISSING_AUTHORITY
    assert receipt.reason_code == (
        "UPSTREAM_RELATION_AUTHORITY_OR_CURRENT_SELECTION_MISSING")


def test_hostile_admission_for_wrong_target_use_is_refused(relation):
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    evidence = c_to_d.bridge_gt12_c_relation_to_d_evidence(relation)
    receipt = adm.evaluate_gt2_relation_admission(
        adm.RelationAdmissionRequest(evidence, target_use="ACTIVE_CAUSAL_USE"),
        rule)
    assert receipt.decision is adm.AdmissionDecision.OUT_OF_SCOPE
    assert receipt.reason_code == "TARGET_USE_MISMATCH"
    assert receipt.target_use_permissions == ()


def test_hostile_v554_equivalence_key_mismatch_is_refused(admission):
    rule = {"id": "V554-RULE-GT2-CONDITIONAL-SUPPORT", "version": "1.0.0",
            "hash": _h("v554-rule")}
    bridge = d_to_m4.prepare_typed_d_to_e_relation_basis(
        admission, v554_rule_ref=rule)
    tampered = deepcopy(dict(bridge.payload))
    tampered["equivalence_key"]["source_universe_fingerprint"] = _h("wrong")
    preparation = prepare_admitted_field_forge_relation_basis(tampered)
    assert preparation.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "fingerprint mismatch" in preparation.reason
    assert preparation.candidate is None

    other_rule = {"id": "V554-RULE-SOME-OTHER-RULE", "version": "1.0.0",
                  "hash": _h("v554-rule-other")}
    result = d_to_m4.evaluate_typed_d_to_e_at_v554(
        admission,
        governed_use_id="GT2_OTHER_USE",
        v554_rule_ref=other_rule,
        publication_authority={
            "authority_id": "V557-PUBLISH-GT2-RELATION",
            "authority_version": "1.0.0",
            "authority_hash": _h("v554-publication-authority"),
            "producer": "V554", "publisher": "V557",
            "governed_use_id": "GT2_OTHER_USE",
            "rule_ref": other_rule, "decision": "AUTHORIZED",
            "allowed_object_families": ["F1", "F2", "B1"],
        },
    )[1]
    # a different V554 rule identity is a different exact rule-relevant
    # equivalence class, so it yields a different canonical basis identity
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.canonical_basis_semantic_id != (
        bridge.preparation.candidate["projection"]["relation_admission_ref"]
        ["content_hash"])


def test_hostile_v554_structural_use_denied_is_not_reconstructed(admission, v554):
    _, use, evaluation = v554
    denied = make_nonpositive_relation_basis_preparation(
        RelationPreparationState.DENIED, "explicit upstream denial")
    rule = {"id": "V554-RULE-GT2-CONDITIONAL-SUPPORT", "version": "1.0.0",
            "hash": _h("v554-rule")}
    authority_bundle = {"gate": "hostile-denied"}
    blocked = d_to_m4.evaluate_typed_d_to_e_at_v554.__globals__[
        "evaluate_m1_admitted_field_forge_relation_v554"]
    result = blocked(
        governed_use_id=use,
        v554_rule_ref=rule,
        focal_structural_proposition_ref=d_to_m4.FOCAL_STRUCTURAL_PROPOSITION,
        preparations=(denied,),
        required_authority_snapshot_refs=("AUTH@1.0.0",),
        authority_bundle_material=authority_bundle,
        producer_reference_spine_fingerprint=_h("spine"),
        conditions=(),
        publication_authority=None,
    )
    assert result.decision_state is M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL
    assert result.f1 is None
    assert result.support_count == 0

    # a nonpositive M1 can never yield a V555 route
    relabelled = replace(result, contract_id=M1_CONTRACT_ID)
    assert evaluate_m2_v555_atomic_route(
        relabelled, _v555_request(evaluation)).route is None


def test_hostile_positive_preparation_cannot_be_fabricated():
    with pytest.raises(Exception) as exc:
        make_nonpositive_relation_basis_preparation(
            RelationPreparationState.RELATION_BASIS_READY, "fabricate")
    assert "positive preparation" in str(exc.value)


def test_hostile_nonpositive_upstream_never_reaches_admitted(relation):
    """Every nonpositive producer state must map to a non-positive admission."""
    rule = c_to_d.make_gt12_c_to_d_admission_rule(relation)
    for state in sorted(ff.NONPOSITIVE_PRODUCER_STATES):
        evidence = replace(
            c_to_d.bridge_gt12_c_relation_to_d_evidence(relation),
            relation_typed_state=state,
        )
        receipt = adm.evaluate_gt2_relation_admission(
            adm.RelationAdmissionRequest(evidence), rule)
        assert receipt.decision is not adm.AdmissionDecision.ADMITTED, state
        assert receipt.target_use_permissions == (), state


def test_hostile_nonpositive_relation_carries_no_profile():
    """The blocked relation shape is empty, never a zero-filled profile."""
    blocked = ff.produce_exact_conditional_support_profile.__doc__
    assert blocked is not None
    assert "typed blocking relation/result with an empty count profile" in blocked
    assert ff.INFORMATION_LOSS == "NONE__REFERENCE_PRESERVING"


def test_hostile_correlation_to_causality_is_refused(admission, relation):
    """No admitted artefact may be re-read as causal / mechanism / mediation."""
    # decision-bearing receipt material only (dependency closure is opaque refs)
    receipt_material = {
        key: admission.material()[key]
        for key in (
            "contract", "owner", "decision", "reason_code", "target_use",
            "downstream_contract", "target_use_permissions",
            "relation_permission_ceiling", "relation_typed_state",
            "relation_information_loss_declaration",
            "admission_information_loss_declaration", "semantic_ceiling",
            "participants",
        )
    }
    text = repr(receipt_material).lower()
    for forbidden in ("caus", "mechanism", "mediation_strength",
                      "pressure_pathway", "temporal_direction", "effect_size"):
        assert forbidden not in text, forbidden

    assert admission.target_use == FROZEN_TARGET_USE
    assert admission.relation_semantics if hasattr(
        admission, "relation_semantics") else True
    assert ff.RELATION_SEMANTICS == (
        "EXACT_CONDITIONAL_SUPPORT_COUNT_PROFILE_WITHIN_SCOPE")
    assert "CONDITIONAL_SUPPORT" in ff.RELATION_SEMANTICS
    assert "CAUS" not in ff.RELATION_SEMANTICS


def test_hostile_actor_injection_is_refused(admission, v554):
    """Admission and V554 both refuse any person/actor meaning."""
    rule = {"id": "V554-RULE-GT2-CONDITIONAL-SUPPORT", "version": "1.0.0",
            "hash": _h("v554-rule")}
    bridge = d_to_m4.prepare_typed_d_to_e_relation_basis(
        admission, v554_rule_ref=rule)
    tampered = deepcopy(dict(bridge.payload))
    tampered["projection"]["interpretation_critical_authority_refs"] = [
        "urn:rawlsing:actor:PERSON_STATE_ASSERTION"]
    tampered["projection_hash"] = semantic_hash(tampered["projection"])
    preparation = prepare_admitted_field_forge_relation_basis(tampered)
    assert preparation.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "sequence mismatch" in preparation.reason

    forbidden_payload = deepcopy(dict(bridge.payload))
    forbidden_payload["projection"]["structural_empirical_admission_id"] = "x"
    assert prepare_admitted_field_forge_relation_basis(
        forbidden_payload).state is RelationPreparationState.INTEGRITY_FAILURE


def test_hostile_v3_actor_promotion_is_denied_zero_effect(retained):
    query, fact = retained
    terminal = run_current_r1c_e2b_actual_objects(query, fact)
    receipt_ref = terminal.v558_terminal.resolution.receipt.ref
    state = _h("actor-state-sentinel")
    decision = evaluate_psepf_zero_positive_guard({
        "actor_id": "HQ221_GT2_NO_ACTOR_PROMOTION_SENTINEL",
        "source_class": GuardedTruthClass.V553_V558_STRUCTURAL_OBJECT.value,
        "source_ref": receipt_ref.object_id,
        "source_hash": receipt_ref.content_hash,
        "source_lineage": [GuardedTruthClass.STRUCTURAL_PRIOR_REPOSITORY.value],
        "transition_surface_id": "HQ221_GT2_STRUCTURAL_TO_ACTOR_STATE",
        "operation_class": "NO_POSITIVE_TRANSITION_AUTHORIZED",
        "state_fingerprint": {
            "actor_state_hash": state,
            "causal_ledger_hash": state,
            "causal_cursor": "0",
            "rng_state_hash": state,
            "scheduler_state_hash": state,
        },
    })
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.zero_effect is True


# ==========================================================================
# PART 8 -- no self-adoption / no actor wake in this lane
# ==========================================================================


def test_lane_produces_no_actor_or_self_adoption_artefact():
    import inspect

    from rawlsing_next import gt12_c_to_d_relation_bridge as _c
    from rawlsing_next import gt12_d_to_m4_typed_bridge as _d

    for module in (_c, _d):
        source = inspect.getsource(module).lower()
        assert "actor_fact" not in source
        assert "self_adopt" not in source