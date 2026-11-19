"""First-fault DHIKR sourcefree: actual original I03->S04->comparative consumer.

The same-person full joint is consumed once; no second estimator/source query.
Sample entropy and bootstrap scenarios are not source/science owner grants.
"""
import pytest

from rawlsing_next.pre553_s04_dhikr_comparative import (
    DHIKRComparisonRequest, DHIKRExplorationError,
    _association, _source_minority, _bootstrap_stability, compare_dhikr_from_i03,
)
from rawlsing_next.pre553_s04_observed_research import receive_s04_i03_research
from rawlsing_next.pre553_s04_general_joint_algebra import (
    S04GeneralJointWorkspace,
)
from rawlsing_next.tests.test_pre553_s04_observed_research import _real


def test_real_source_derived_xor_detects_pair_synergy_and_adaptive_context():
    _, _, _, query, execution = _real(tag="DHIKR-C3-NATIVE-XOR")
    request = DHIKRComparisonRequest(
        target_axis=2, predictor_axes=(0, 1),
        min_branch_n=2, max_depth=2, max_nodes=9,
        bootstrap_replicates=24,
    )
    receipt = compare_dhikr_from_i03(
        query=query, execution=execution, request=request,
    )
    m = receipt.material()
    assert m["state"] == "SOURCE_COHERENT_SAMPLE_COMPARISON"
    assert m["raw_original_full_joint_n"] == 4
    assert m["source_query_ref"] == query.ref.as_dict()
    assert m["source_fact_ref"] == execution.facts[0].ref.as_dict()
    root = m["nodes"][0]
    assert root["raw_same_case_n"] == 4
    assert [v["information_bits"] for v in root["sample_association_scores"]] == [0.0, 0.0]
    assert root["priority_group"] == [0, 1]
    assert root["pairwise_conditional_interactions"][0]["joint_information_bits"] == 1.0
    assert root["pairwise_conditional_interactions"][0]["sample_interaction_information_bits"] == 1.0
    assert root["split_axis"] == 0
    assert m["bootstrap_rank_instability"]["observed_priority_group"] == [0, 1]
    assert any(
        item["axes"] == [0, 1] and
        item["observed_information_bits"] == 1.0 and
        item["unique_top_group_fraction"] is not None
        for item in m["bootstrap_rank_instability"]["groups"]
    )
    assert root["pairwise_conditional_interactions"][0]["interpretation"] == "SAMPLE_SYNERGY__NONCAUSAL"
    assert len(m["nodes"]) >= 3
    assert {node["depth"] for node in m["nodes"]} >= {0, 1}
    assert m["no_new_I03_or_source_reads"] is True
    assert m["bootstrap_rank_instability"]["state"].startswith(
        "EXPLORATORY_IID_"
    )
    assert "NO_COMPLEX_SURVEY_VARIANCE_OR_POPULATION_RANK_AUTHORITY" in m["scientific_ceiling"]
    assert receipt.content_hash

    # The other public first reader is exactly the same S04 workspace; it
    # cannot create an alternative count or content identity.
    knowledge = receive_s04_i03_research(query=query, execution=execution)
    workspace = S04GeneralJointWorkspace(
        knowledge=knowledge, expected_knowledge_ref=knowledge.ref,
    )
    assert workspace.compare_dhikr(request).ref == receipt.ref


def test_native_xor_marginals_not_confused_with_joint_predictive_evidence():
    xor = [
        (("0", "0", "0"), 1), (("0", "1", "1"), 1),
        (("1", "0", "1"), 1), (("1", "1", "0"), 1),
    ]
    for axis in (0, 1):
        assert _association(xor, 2, (axis,))["information_bits"] == 0
    assert _association(xor, 2, (0, 1))["information_bits"] == 1
    assert _association(xor, 2, (0, 1))["normalized_reduction"] == 1


def test_actual_nonmodal_configuration_is_retained_not_silently_discarded():
    source = [
        (("worker", "yes"), 6),
        (("worker", "no"), 2),
        (("manager", "yes"), 1),
        (("manager", "no"), 5),
    ]
    negatives = _source_minority(source, target=1, axis=0)
    assert {(r["predictor_state"], r["target_state"], r["raw_contradictory_n"])
            for r in negatives} == {
                ("worker", "no", 2),
                ("manager", "yes", 1),
            }
    assert all(r["raw_group_n"] in (8, 6) for r in negatives)


def test_dhikr_refuses_target_leakage_and_unbounded_search():
    _, _, _, query, execution = _real(tag="DHIKR-C3-NEGATIVE")
    for request in (
        DHIKRComparisonRequest(target_axis=2, predictor_axes=(2,)),
        DHIKRComparisonRequest(target_axis=2, predictor_axes=(0, 1), max_nodes=0),
        DHIKRComparisonRequest(target_axis=2, predictor_axes=(0, 1),
                               fixed_context=((2, "0"),)),
        DHIKRComparisonRequest(target_axis=2, predictor_axes=(0, 1),
                               bootstrap_replicates=201),
    ):
        with pytest.raises(DHIKRExplorationError):
            compare_dhikr_from_i03(
                query=query, execution=execution, request=request,
            )


def test_contextual_subset_has_exact_same_case_denominator():
    _, _, _, query, execution = _real(tag="DHIKR-C3-CONTEXT")
    result = compare_dhikr_from_i03(
        query=query, execution=execution,
        request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(1,), fixed_context=((0, "0"),),
            max_depth=1, max_nodes=4, bootstrap_replicates=0,
        )
    ).material()
    assert result["nodes"][0]["raw_same_case_n"] == 2
    assert sum(x["n"] for x in result["nodes"][0]["raw_target_counts"]) == 2
    assert result["nodes"][0]["sample_association_scores"][0]["information_bits"] == 1
    assert result["bootstrap_rank_instability"]["state"] == (
        "NOT_REQUESTED__DESIGN_UNCERTAINTY_NOT_ESTABLISHED"
    )


def test_bootstrap_no_observed_context_does_not_attempt_empty_multinomial():
    result = _bootstrap_stability(
        [], target=2, predictors=(0, 1),
        repeats=16, case_cap=64, seed=24,
    )
    assert result["state"] == "ZERO_OBSERVED_CONTEXT_SUPPORT__NO_IID_RESAMPLING"
    assert result["repetitions_completed"] == 0

def test_group_bootstrap_ranks_the_same_interactions_recruited_by_search():
    xor = [
        (("0", "0", "0"), 1), (("0", "1", "1"), 1),
        (("1", "0", "1"), 1), (("1", "1", "0"), 1),
    ]
    result = _bootstrap_stability(
        xor, target=2, predictors=(0, 1),
        repeats=48, case_cap=64, seed=987,
        max_interaction_order=2,
    )
    assert result["observed_priority_group"] == [0, 1]
    assert result["max_interaction_order"] == 2
    assert [x["axes"] for x in result["groups"]] == [[0], [1], [0, 1]]
    assert all(x["unique_top_group_fraction"] is not None
               for x in result["groups"])
    assert result["group_priority_rule"] == "IN_SAMPLE_INFORMATION_BITS_PER_GROUP_AXIS"
    assert result["limitation"].find("POST_SELECTION_BIAS") >= 0
    # Legacy single-predictor stability remains present, but is not used
    # as a surrogate for the recruited two-axis group.
    assert [x["axis"] for x in result["predictors"]] == [0, 1]


def test_budget_refuses_interaction_bootstrap_explosion_without_fake_stability():
    cells = [(("0", "0", "0", "0", "0", "0"), 1)] * 4096
    result = _bootstrap_stability(
        cells, target=5, predictors=(0, 1, 2, 3, 4),
        repeats=200, case_cap=4096, seed=4,
        max_interaction_order=3,
    )
    assert result["state"] == "HELD_GROUP_BOOTSTRAP_WORK_CAP"
    assert result["repetitions_completed"] == 0


def test_modal_tie_is_explicitly_ambiguous_not_discarded():
    cells = [(("same", "yes"), 2), (("same", "no"), 2)]
    findings = _source_minority(cells, target=1, axis=0)
    assert len(findings) == 1
    assert findings[0]["qualification"] == "TIED_MODAL_TARGETS__NO_UNIQUE_NONMODAL_LABEL"
    assert findings[0]["raw_group_n"] == 4
    assert "raw_contradictory_n" not in findings[0]


def test_below_minimum_branch_never_claims_comparison_or_discloses_target_split():
    _, _, _, query, execution = _real(tag="DHIKR-MULCH-BELOW-MINIMUM")
    result = compare_dhikr_from_i03(
        query=query, execution=execution,
        request=DHIKRComparisonRequest(
            target_axis=2, predictor_axes=(1,), fixed_context=((0, "0"),),
            min_branch_n=3, max_nodes=4,
        ),
    ).material()
    root = result["nodes"][0]
    assert root["raw_same_case_n"] == 2
    assert root["terminal_reason"] == "BELOW_MINIMUM_OBSERVED_CONTEXT_N"
    assert root["sample_association_scores"] == []
    assert root["priority_group"] == []
    assert root["raw_target_counts"] == []
    assert root["target_count_disposition"] == (
        "HELD_BELOW_MIN_BRANCH_N__NO_CONTEXT_TARGET_DISCLOSURE"
    )
