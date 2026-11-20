"""C5: actual I03 -> S04/DHIKR -> FF01 -> C4 PREV3 -> continuing C5 sourcefree context.

This court is NOT an individual, an independent scientific discovery method,
a world/actor issuer, an original wave, or an unbound pseudo-respondent.
"""
from __future__ import annotations

from dataclasses import replace
from json import loads

import pytest

from rawlsing_next.pre553_empirical_objects import canonical_json, semantic_hash
from rawlsing_next.pre553_s04_cold_custody import SOURCEFREE_ASSERTION
from rawlsing_next.pre553_s04_dhikr_comparative import DHIKRComparisonRequest
from rawlsing_next.pre553_s04_field_forge_v3_bridge import (
    EmpiricalSeamError, V3SeamEnvelope, build_empirical_field_forge_v3_handoff,
    read_sourcefree_v3_handoff_private, write_sourcefree_v3_handoff_private,
)
from rawlsing_next.pre553_ff_prev3_possibility_navigation import (
    V3ContextNavigationError, V3ContextPath,
    plan_v3_sourcefree_context_branches, run_v3_sourcefree_context_path,
    replay_v3_sourcefree_context_path,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def _c4(tag="C5-SOURCEFREE-CONTINUING"):
    _, _, _, query, execution = _real(tag=tag)
    return build_empirical_field_forge_v3_handoff(
        query=query,
        execution=execution,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(0, 1),
            min_branch_n=2, max_depth=2, max_nodes=9,
            max_interaction_order=2, bootstrap_replicates=24,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )


def _plan(c4, conditions=None, axes=None, min_n=None):
    return plan_v3_sourcefree_context_branches(
        envelope=c4.envelope, external_pin=c4.external_pin,
        conditions={} if conditions is None else conditions,
        candidate_axes=axes, min_context_n=min_n,
    )


def _path(c4, steps, initial=None, seed=19, min_n=None):
    return run_v3_sourcefree_context_path(
        envelope=c4.envelope, external_pin=c4.external_pin,
        starting_conditions={} if initial is None else initial,
        steps=steps, seed=seed, min_context_n=min_n,
    )


def test_actual_joint_has_full_source_partition_each_axis_and_real_target_refs():
    c4 = _c4()
    plan = _plan(c4).material()
    assert plan["state"] == "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER"
    assert plan["base_raw_complete_case_n"] == 4
    assert plan["source_handoff_ref"] == c4.envelope.ref.as_dict()
    assert plan["source_ff01_ref"] == c4.first_consumer.ff01.ref.as_dict()
    assert plan["source_dhikr_ref"] == c4.comparison.ref.as_dict()
    assert plan["min_context_n"] == 2
    assert plan["new_i03_queries"] == 0
    assert len(plan["source_observed_axes"]) == 3
    for axis in plan["source_observed_axes"]:
        assert axis["partition_sum_conserves_base_full_cases"] is True
        assert len(axis["branches"]) == 2
        assert [b["raw_complete_case_n"] for b in axis["branches"]] == [2, 2]
        assert all(b["status"] == "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER"
                   for b in axis["branches"])
        assert all(b["not_a_population_probability"] is True for b in axis["branches"])


def test_conditional_target_alternatives_preserve_tied_modes_and_denominator():
    c4 = _c4("C5-ACTUAL-XOR-TIED")
    axis = _plan(c4, axes=(0,)).material()["source_observed_axes"][0]
    assert axis["axis"] == 0
    for branch in axis["branches"]:
        assert branch["source_target_conditional_support_ref"] is not None
        alternatives = branch["source_target_alternatives"]
        assert len(alternatives) == 2
        assert sum(x["raw_target_n"] for x in alternatives) == 2
        assert {x["observed_sample_status"] for x in alternatives} == {
            "TIED_SAMPLE_MODAL_NO_SINGLE_MAJORITY"
        }
        assert branch["target_alternative_grade"] == (
            "OBSERVED_RAW_SAMPLE_MODALITY__NOT_PERSONAL_TRAIT"
        )


def test_two_step_context_path_stops_on_low_n_without_inventing_case():
    c4 = _c4("C5-PATH-LOW")
    path = _path(c4, [(0, "0"), (1, "1")])
    m = path.material()
    assert len(m["history"]) == 2
    assert m["history"][0]["base_complete_case_n"] == 4
    assert m["history"][0]["next_complete_case_n"] == 2
    assert m["history"][0]["disposition"] == "CONTEXT_ELIGIBLE_FOR_SOURCEFREE_CASE_OFFER"
    assert m["history"][1]["base_complete_case_n"] == 2
    assert m["history"][1]["next_complete_case_n"] == 1
    assert m["history"][1]["disposition"] == "LOW_COMPLETE_CASE_N__NO_CANDIDATE_OFFER"
    assert m["status"] == "LOW_CONTEXT_SUPPORT__ABSTAIN"
    assert m["final_case_offer_payload"]["selected_complete_joint_cell"] == []
    assert m["final_case_offer_payload"]["sorok_v3_actor_mutation"] is None
    assert "V3_OR_SOROK_PERSON_OR_RECRUITMENT_AUTHORITY" in m["not_issued"]


def test_source_coherent_one_step_case_proposal_replay():
    c4 = _c4("C5-PATH-CASE")
    path = _path(c4, [(0, "0")], seed=27)
    m = path.material()
    assert m["status"] == "SOURCE_COHERENT_EXPLORATORY_CASE_OFFER"
    assert m["final_raw_complete_case_n"] == 2
    proposal = m["final_case_offer_payload"]["selected_complete_joint_cell"]
    assert len(proposal) == 3
    values = {s["source_dimension"]: s["candidate_state"] for s in proposal}
    assert values[0] == "0"
    assert int(values[2]) == int(values[0]) ^ int(values[1])
    assert m["final_case_offer_payload"]["source_handoff_ref"] == c4.envelope.ref.as_dict()
    assert m["object_scope"] == "HYPOTHETICAL_WHOLE_JOINT_CONFIGURATION_NOT_ACTOR"
    assert replay_v3_sourcefree_context_path(
        path=path, envelope=c4.envelope,
        external_pin=c4.external_pin,
    ).ref == path.ref


def test_empty_path_honors_initial_context_and_unconstrained_offer():
    c4 = _c4("C5-EMPTY")
    zero_steps = _path(c4, [], seed=100)
    assert zero_steps.material()["final_raw_complete_case_n"] == 4
    initial = _path(c4, [], initial={1: "1"}, seed=100)
    assert initial.material()["final_raw_complete_case_n"] == 2
    assert len(initial.material()["starting_context"]) == 1
    assert initial.ref != zero_steps.ref


def test_zero_complete_case_context_is_not_labeled_impossibility():
    c4 = _c4("C5-ZERO")
    result = _path(c4, [(2, "1")], initial={0: "0", 1: "0"})
    m = result.material()
    assert m["final_raw_complete_case_n"] == 0
    assert m["history"][0]["disposition"] == "OBSERVED_ZERO_IN_COMPLETE_CASE__NOT_IMPOSSIBLE"
    assert m["status"] == "ZERO_OBSERVED_CONTEXT__NOT_IMPOSSIBILITY"
    assert m["final_case_offer_payload"]["selected_complete_joint_cell"] == []
    # Source contains zero cells but cannot prove physical impossibility.
    assert m["object_scope"] == "HYPOTHETICAL_WHOLE_JOINT_CONFIGURATION_NOT_ACTOR"


def test_low_n_candidates_abstain_but_preserve_exact_counts_without_disclosed_target():
    c4 = _c4("C5-MINIMUM")
    plan = _plan(c4, conditions={0: "0"}, axes=(1,)).material()
    assert plan["base_raw_complete_case_n"] == 2
    axis = plan["source_observed_axes"][0]
    assert axis["partition_sum_conserves_base_full_cases"] is True
    assert [b["raw_complete_case_n"] for b in axis["branches"]] == [1, 1]
    assert all(b["status"] == "LOW_COMPLETE_CASE_N__NO_CANDIDATE_OFFER" for b in axis["branches"])
    assert all(b["source_target_conditional_support_ref"] is None for b in axis["branches"])
    assert all(b["source_target_alternatives"] == [] for b in axis["branches"])


def test_unbound_axis_after_target_binding_cannot_disclose_target_comparison():
    c4 = _c4("C5-TARGET-BOUND")
    plan = _plan(c4, conditions={2: "1"}, axes=(1,)).material()
    assert plan["base_raw_complete_case_n"] == 2
    assert all(b["source_target_conditional_support_ref"] is None
               for b in plan["source_observed_axes"][0]["branches"])


def test_no_extension_of_held_path_or_repeat_axis_no_forged_analogy():
    c4 = _c4("C5-STOP")
    with pytest.raises(V3ContextNavigationError, match="cannot extend"):
        _path(c4, [(0, "0"), (1, "0"), (2, "0")])
    with pytest.raises(V3ContextNavigationError, match="already conditioned"):
        _path(c4, [(0, "0"), (0, "1")])
    with pytest.raises(V3ContextNavigationError, match="already conditioned"):
        _path(c4, [(0, "0")], initial={0: "1"})


def test_reject_invalid_states_axes_budget_and_context_numeric_smuggling():
    c4 = _c4("C5-NEGATIVE")
    with pytest.raises(V3ContextNavigationError, match="outside actual"):
        _plan(c4, conditions={0: "UNKNOWN"})
    with pytest.raises(V3ContextNavigationError, match="axis"):
        _plan(c4, axes=(999,))
    with pytest.raises(V3ContextNavigationError, match="duplicate"):
        _plan(c4, axes=(0, 0))
    with pytest.raises(V3ContextNavigationError, match="conditioned"):
        _plan(c4, conditions={0: "0"}, axes=(0,))
    with pytest.raises(V3ContextNavigationError, match="minimum"):
        _plan(c4, min_n=1)
    with pytest.raises(V3ContextNavigationError):
        _path(c4, [(0, 0.0)])
    with pytest.raises(V3ContextNavigationError):
        _path(c4, [(0, "0")]*17)


def test_exact_pin_cannot_be_substituted_and_fake_path_cannot_replay():
    c4 = _c4("C5-FORGERY")
    with pytest.raises(V3ContextNavigationError, match="pin"):
        plan_v3_sourcefree_context_branches(
            envelope=c4.envelope, external_pin=None, conditions={},
        )
    pin = replace(c4.external_pin, ff01_ref=c4.external_pin.query_ref)
    with pytest.raises(EmpiricalSeamError, match="external/ff01_ref"):
        plan_v3_sourcefree_context_branches(
            envelope=c4.envelope, external_pin=pin, conditions={},
        )
    path = _path(c4, [(0, "0")], seed=4)
    fake = path.material()
    fake["seed"] = 123456
    forged = V3ContextPath(canonical_json(fake), semantic_hash(fake))
    with pytest.raises(V3ContextNavigationError, match="failed independently pinned replay"):
        replay_v3_sourcefree_context_path(
            path=forged, envelope=c4.envelope, external_pin=c4.external_pin,
        )


def test_actual_cold_c4_source_can_resume_C5_navigation_without_i03(tmp_path):
    c4 = _c4("C5-COLD-PORTABLE")
    store = tmp_path / "private"
    store.mkdir(mode=0o700)
    path = write_sourcefree_v3_handoff_private(store, c4.envelope)
    restored = read_sourcefree_v3_handoff_private(path, external_pin=c4.external_pin)
    plan = plan_v3_sourcefree_context_branches(
        envelope=restored, external_pin=c4.external_pin,
        conditions={0: "1"}, candidate_axes=(1,),
    )
    assert plan.material()["base_raw_complete_case_n"] == 2
    result = run_v3_sourcefree_context_path(
        envelope=restored, external_pin=c4.external_pin,
        starting_conditions={}, steps=[(1, "0")],
        seed=14,
    )
    assert result.material()["final_raw_complete_case_n"] == 2
    assert replay_v3_sourcefree_context_path(
        path=result, envelope=restored, external_pin=c4.external_pin
    ).ref == result.ref


def test_i05_valid_empty_candidate_retains_source_joint_for_dynamic_v3_context():
    """I05 VALID_EMPTY means a particular rule tested empty, not all I03 facts."""
    from rawlsing_next._pre553_query_common import QueryExecutionResult
    from rawlsing_next.pre553_empirical_objects import exact_ref
    from rawlsing_next.pre553_s04_i05_reception import receive_s04_i05_role
    from rawlsing_next.tests.test_pyat1009_ff01_i05_role_ingress import _real_frontier
    discovery = _real_frontier()
    receipt = next(x for x in discovery.receipts if x.typed_state == "VALID_EMPTY")
    knowledge, role = receive_s04_i05_role(
        discovery=discovery, candidate_receipt_ref=receipt.ref,
        query_role="BASE",
    )
    body = role.material()
    query_ref = exact_ref(body["query_ref"], "I05 selected query")
    fact_ref = exact_ref(body["fact_ref"], "I05 selected fact")
    release = exact_ref(body["source_release_ref"], "I05 release")
    query = next(q for q in discovery.executed_queries if q.ref == query_ref)
    fact = next(f for f in discovery.empirical_facts if f.ref == fact_ref)
    execution = QueryExecutionResult(
        query_ref=query_ref, facts=(fact,), source_scope_mode="SINGLE_UNIVERSE",
        release_refs=(release,),
    )
    c4 = build_empirical_field_forge_v3_handoff(
        query=query, execution=execution,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(0, 1),
            min_branch_n=2, max_depth=2, max_nodes=9,
            max_interaction_order=2, bootstrap_replicates=0,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )
    plan = _plan(c4, axes=(0, 1))
    body = plan.material()
    assert body["base_raw_complete_case_n"] == 4
    assert body["source_handoff_ref"] == c4.envelope.ref.as_dict()
    assert c4.envelope.material()["s04_ref"] == knowledge.ref.as_dict()
    assert body["source_ff01_ref"] == c4.first_consumer.ff01.ref.as_dict()
    assert all(item["partition_sum_conserves_base_full_cases"]
               for item in body["source_observed_axes"])


def test_actual_I03_majority_minority_and_tie_survive_v3_context_branching():
    """Beyond XOR ties: minority disagreement is real same-person full-case data."""
    from rawlsing_next.tests import test_pre553_empirical_query as native
    rows = []
    for x, y, z, n in (
        (0, 0, 0, 4),
        (0, 1, 1, 1),
        (0, 1, 0, 1),
        (1, 0, 1, 2),
        (1, 1, 0, 2),
    ):
        for j in range(n):
            rows.append({
                "id": f"R{x}{y}{z}_{j}",
                "responses": {"X": x, "Y": y, "Z": z},
            })
    source = native._build_source(
        "C5-TRUE-MINORITY", rows,
        question_namespace="C5-MINORITY-QUESTIONS",
    )
    qa = native._query_authority("C5-TRUE-MINORITY")
    predicate = native._branch_predicate(source, qa, tag="all")
    query = native._query(source, qa, predicate, ("X", "Y", "Z"), tag="joint")
    execution = native._run(source, qa, predicate, query)
    assert execution.facts[0].typed_state == "SUPPORTED"
    c4 = build_empirical_field_forge_v3_handoff(
        query=query, execution=execution,
        comparison_request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(0, 1),
            min_branch_n=2, max_depth=2, max_nodes=9,
            max_interaction_order=2, bootstrap_replicates=0,
        ),
        conditioner_index=0,
        sourcefree_origin_assertion=SOURCEFREE_ASSERTION,
    )
    plan = _plan(c4, axes=(0,)).material()
    assert plan["base_raw_complete_case_n"] == 10
    candidates = plan["source_observed_axes"][0]["branches"]
    assert [x["raw_complete_case_n"] for x in candidates] == [6, 4]
    minority = candidates[0]["source_target_alternatives"]
    assert [(x["source_target_state"], x["raw_target_n"]) for x in minority] == [
        ("0", 5), ("1", 1),
    ]
    assert {x["observed_sample_status"] for x in minority} == {
        "SAMPLE_UNIQUE_MODAL", "SAMPLE_NONMODAL_NOT_TRAIT_OR_COHORT",
    }
    tie = candidates[1]["source_target_alternatives"]
    assert {x["raw_target_n"] for x in tie} == {2}
    assert all(x["observed_sample_status"] ==
               "TIED_SAMPLE_MODAL_NO_SINGLE_MAJORITY" for x in tie)
    # Context X=0 remains eligible even though a nonmodal Y contributes.
    path = _path(c4, [(0, "0")], seed=27)
    assert path.material()["final_raw_complete_case_n"] == 6
    whole = path.material()["final_case_offer_payload"]["selected_complete_joint_cell"]
    assert len(whole) == 3
    assert whole[0]["candidate_state"] == "0"
    assert path.material()["final_case_offer_payload"]["sorok_v3_actor_mutation"] is None
