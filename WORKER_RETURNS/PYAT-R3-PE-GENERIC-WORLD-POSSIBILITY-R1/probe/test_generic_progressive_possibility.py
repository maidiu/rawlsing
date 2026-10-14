"""P-E independent, source-free generic service tests. NOT_EXECUTED in Browser/GitHub.

These tests reuse actual N10E provider and AT07 synthetic producer in the
current canonical code; no test provides any probability geometry as input.

The fwd/reverse case changes BOTH the condition and target role. It cannot be
construed as statistical inversion P(D|A) from P(A|D): each is computed by a
separate explicitly authorized TEST_ONLY synthetic producer query.
"""
from __future__ import annotations

from dataclasses import replace
import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import (
    provide_empirical_possibility_slice,
)
from rawlsing_next.tests import n10e_empirical_slice_fixture as fx

from generic_progressive_possibility import (
    CONTRACT, GRADE, EmpiricalOption, GenericPossibilityRefusal,
    GenericRequest, WorldCondition, WorldFact, WorldSnapshot,
    evaluate_generic_progressive, verify_generic_replay,
)


def ref(label: str, kind: str = "P_E_TEST_REF") -> ExactRef:
    material = {"scope": "TEST_ONLY", "label": label, "kind": kind}
    return ExactRef(kind, "urn:test:pyat-pe:" + label, semantic_hash(material))


SUBJECT = ref("scenario-subject")
PLACE = ref("synthetic-region")
SITE_P = ref("test-scenario-criterion")
ROUTE_P = ref("test-empirical-question-role")
SITE_V = ref("eligible-context")
FORWARD_V = ref("forward-question")
REVERSE_V = ref("reverse-question")
SITE_FACT = ref("exact-test-premise-site")
FORWARD_FACT = ref("exact-test-premise-forward")
REVERSE_FACT = ref("exact-test-premise-reverse")


def provider(direction, variant=None):
    case = fx.build_provider_case(direction, variant=variant)
    product = provide_empirical_possibility_slice(
        repository=case["source"]["repo"],
        empirical_query=case["empirical_query"],
        predicate=case["predicate"],
        authority_registry=case["registry"],
        release_refs=case["release_refs"],
        consumer_query=case["consumer_query"],
        model_rule=case["model_rule"],
        condition_binding_witness=case["condition_binding_witness"],
    )
    return case["consumer_query"], product


def world(role: str = "forward", *, issuer="TEST_ONLY_CONTEXT",
          asof=2008, selection=2008, currentness="CURRENT_AT_SELECTED_AS_OF"):
    role_ref = FORWARD_V if role == "forward" else REVERSE_V
    role_fact = FORWARD_FACT if role == "forward" else REVERSE_FACT
    facts = (
        WorldFact(SITE_FACT, SITE_P, SITE_V, 2000, 2015, issuer),
        WorldFact(role_fact, ROUTE_P, role_ref, 2000, 2015, issuer),
    )
    return WorldSnapshot(
        snapshot_ref=ref("world-" + role),
        subject_ref=SUBJECT, geography_ref=PLACE,
        as_of_year=asof, publication_year=2007, selection_year=selection,
        currentness_state=currentness, facts=facts,
    )


def option(direction, *, variant=None):
    q, p = provider(direction, variant=variant)
    role = (FORWARD_V if direction == "forward" else REVERSE_V)
    fact = (FORWARD_FACT if direction == "forward" else REVERSE_FACT)
    return EmpiricalOption(
        option_id=direction,
        consumer_query=q,
        computed_provider=p,
        world_conditions=(
            WorldCondition("available-site", SITE_P, SITE_V, SITE_FACT),
            WorldCondition("question-role", ROUTE_P, role, fact),
        ),
    )


def request(role="forward", *, consumer="NONPARENT_SERVICE", variant=None,
            world_override=None):
    options = (option("forward", variant=variant),
               option("reverse", variant=variant))
    return GenericRequest(
        request_id="P-E-AT07-TEST", consumer_id=consumer,
        subject_ref=SUBJECT,
        world=world_override or world(role),
        options=options, expected_as_of_year=2008,
    )


@pytest.mark.parametrize("consumer", [
    "CONCEPTION_SCENARIO_DOWNSTREAM__NO_PRE_V3_PARENT_SEMANTICS",
    "NONPARENT_COMMUNITY_OUTREACH_PLANNING",
])
def test_same_generic_api_both_consumers_and_exact_computed_forward(consumer):
    result = evaluate_generic_progressive(request(consumer=consumer))
    assert result["contract"] == CONTRACT
    assert result["status"] == "SELECTED"
    assert result["selected_option_id"] == "forward"
    assert len(result["progressive_steps"]) == 3
    assert result["progressive_steps"][1]["possible_option_ids"] == [
        "forward", "reverse"
    ]
    assert result["progressive_steps"][2]["possible_option_ids"] == ["forward"]
    geo = result["selected_computed_empirical_evidence"]["geometry"]
    assert geo["denominator"]["raw_denominator_support"] == 60
    assert {x["cell"]: x["raw_numerator_support"] for x in geo["cells"]} == {
        "yes": 54, "no": 6
    }
    assert result["actor_generations"] == result["model_calls"] == 0
    assert result["real_world_promotion"] is False
    assert result["grade"] == GRADE
    assert verify_generic_replay(result, request(consumer=consumer)) == result


def test_world_premise_change_reselects_computed_question_not_just_sidecar():
    a = evaluate_generic_progressive(request("forward"))
    b = evaluate_generic_progressive(request("reverse"))
    assert a["selected_option_id"] == "forward"
    assert b["selected_option_id"] == "reverse"
    assert a["selected_computed_empirical_evidence"]["raw_support"] == 60
    assert b["selected_computed_empirical_evidence"]["raw_support"] == 62
    assert a["selected_computed_empirical_evidence"]["target_ref"] != (
        b["selected_computed_empirical_evidence"]["target_ref"]
    )
    # Both exact original producer results remain held in all_evidence:
    assert a["all_computed_empirical_evidence"] == b["all_computed_empirical_evidence"]
    # This is a different lawful QUESTION, not a counterfactual causal effect
    # or same-target shift in P(ANSWER) induced by a world premise.


def test_source_law_change_recomputes_exact_fractions_not_world_conditions():
    original = evaluate_generic_progressive(request("forward"))
    changed = evaluate_generic_progressive(
        request("forward", variant=fx.CHANGED_SOURCE_VARIANT)
    )
    assert original["world_snapshot_hash"] == changed["world_snapshot_hash"]
    assert original["selected_option_id"] == changed["selected_option_id"]
    g0 = original["selected_computed_empirical_evidence"]["geometry"]
    g1 = changed["selected_computed_empirical_evidence"]["geometry"]
    assert g0["denominator"]["raw_denominator_support"] == 60
    assert g1["denominator"]["raw_denominator_support"] == 70
    assert {c["cell"]: c["raw_numerator_support"] for c in g1["cells"]} == {
        "yes": 54, "no": 16
    }
    assert original["progressive_steps"] == changed["progressive_steps"]
    assert original["selected_computed_empirical_evidence"]["release_ref"] != (
        changed["selected_computed_empirical_evidence"]["release_ref"]
    )


def test_replay_and_targeted_invalidation():
    old_request = request("forward")
    old_result = evaluate_generic_progressive(old_request)
    assert verify_generic_replay(old_result, old_request) == old_result
    changed_request = request("reverse")
    with pytest.raises(GenericPossibilityRefusal, match="PROGRESSIVE_REPLAY_MISMATCH"):
        verify_generic_replay(old_result, changed_request)


def test_wrong_world_currentness_denied():
    stale = world(currentness="STALE")
    with pytest.raises(GenericPossibilityRefusal, match="WORLD_CURRENTNESS_NOT_CURRENT"):
        evaluate_generic_progressive(request(world_override=stale))


def test_wrong_world_asof_denied():
    stale = world(asof=2004)
    with pytest.raises(GenericPossibilityRefusal, match="WORLD_AS_OF_MISMATCH"):
        evaluate_generic_progressive(request(world_override=stale))


def test_four_clocks_refuse_publication_after_selection():
    future = world(selection=2006)
    with pytest.raises(GenericPossibilityRefusal, match="FOUR_CLOCKS_PUBLICATION_AS_OF_SELECTION_CONFLICT"):
        evaluate_generic_progressive(request(world_override=future))


def test_no_real_world_current_promotion():
    with pytest.raises(GenericPossibilityRefusal, match="UNISSUED_N9_CURRENT"):
        evaluate_generic_progressive(replace(request(), claim_current_n9=True))


def test_no_foreign_actor_output_request():
    with pytest.raises(GenericPossibilityRefusal, match="ACTOR_OR_FOREIGN_ONTOLOGY_FORBIDDEN"):
        evaluate_generic_progressive(
            replace(request(), requested_kind="GENERATED_PARENT")
        )


def test_unissued_world_fact_permission_excludes_both_options():
    denied = world(issuer="UNISSUED_CONTEXT")
    result = evaluate_generic_progressive(request(world_override=denied))
    assert result["status"] == "WORLD_BLOCKED"
    assert result["selected_computed_empirical_evidence"] is None
    assert all(
        item["geometry"]["denominator"]["raw_denominator_support"] in (60, 62)
        for item in result["all_computed_empirical_evidence"].values()
    )


def test_producer_identity_not_handwritten_geometry():
    opt = option("forward")
    # The existing provider result's own constructor refuses before the facade.
    with pytest.raises(Exception):
        replace(opt.computed_provider, generated_evidence_or_null=None)


def test_no_inference_from_reverse_direction():
    # Each direction has its own real synthetic I03/C1/provider query and receipt.
    a = option("forward")
    b = option("reverse")
    assert a.consumer_query.ref != b.consumer_query.ref
    assert a.computed_provider.provider_receipt.producer_fact_ref != (
        b.computed_provider.provider_receipt.producer_fact_ref
    )


def test_world_fact_change_with_constant_value_but_new_ref_is_not_silent():
    w = world()
    facts = list(w.facts)
    facts[1] = replace(facts[1], fact_ref=ref("a-different-provenance"))
    result = evaluate_generic_progressive(request(world_override=replace(w, facts=tuple(facts))))
    assert result["status"] == "WORLD_BLOCKED"


def test_no_multiconditioner_n10e_issuer_inferred():
    # Accepted C1 supports multi-binding; provider R1 does not. This test
    # safeguards the distinction rather than forging multi-source evidence.
    from rawlsing_next.pre553_empirical_possibility_provider import (
        EmpiricalPossibilityProviderRequest,
        ProviderRequestShapeError,
    )
    q, p = provider("forward")
    binding = q.conditioner_bindings[0]
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        PositionedSubjectPossibilityQuery,
    )
    q2 = PositionedSubjectPossibilityQuery(
        "pe-multiple-attempt", q.subject_ref, q.target_ref,
        q.source_universe_ref, q.release_ref,
        (binding, replace(binding, binding_id="second")), q.requested_projection,
    )
    case = fx.build_provider_case("forward")
    with pytest.raises(ProviderRequestShapeError):
        EmpiricalPossibilityProviderRequest(
            repository=case["source"]["repo"],
            empirical_query=case["empirical_query"], predicate=case["predicate"],
            authority_registry=case["registry"], release_refs=case["release_refs"],
            consumer_query=q2, model_rule=case["model_rule"],
            condition_binding_witness=case["condition_binding_witness"],
        )


def test_cross_release_option_pool_refused_without_ee_issuance():
    a = option("forward")
    b = option("reverse", variant=fx.CHANGED_SOURCE_VARIANT)
    request_broken = replace(request(), options=(a, b))
    with pytest.raises(GenericPossibilityRefusal, match="CROSS_SOURCE_OR_RELEASE_OPTION_POOL_FORBIDDEN"):
        evaluate_generic_progressive(request_broken)
