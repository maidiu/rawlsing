"""REMONT RMT-Q016: mathematically falsify naive low-n and raw-MI explosion.

Sourcefree deterministic test fixtures. Author does not execute tests/repairs.
Confirm exact-source support vs statistical routing are noninterchangeable.
"""
from decimal import Decimal

import pytest

from rawlsing_next.pre553_s04_adaptive_support import (
    AdaptiveSupportPolicy, classify_observed_branch, order_child_probes,
    thresholds,
)
from rawlsing_next.pre553_s04_exploration_admission import (
    SearchEvidence, route_exploratory_split, source_observed_group_states,
)


def test_500_respondent_country_not_pooled_with_5000_multicountry_wave():
    p = AdaptiveSupportPolicy()
    assert (thresholds(500, p)["explore_min_n"],
            thresholds(500, p)["review_candidate_min_n"]) == (3, 5)
    assert (thresholds(5000, p)["explore_min_n"],
            thresholds(5000, p)["review_candidate_min_n"]) == (15, 25)
    assert (thresholds(100000, p)["explore_min_n"],
            thresholds(100000, p)["review_candidate_min_n"]) == (15, 30)


def test_15_of_60_keeps_exploration_but_does_not_claim_population_inference():
    r = classify_observed_branch(
        country_question_n=5000, parent_n=60, observed_n=15,
        parent_target_counts={"no": 45, "yes": 15},
        child_target_counts={"no": 0, "yes": 15},
        policy=AdaptiveSupportPolicy(),
    )
    assert r["routine_exploration_eligible"]
    assert not r["initial_review_support_candidate"]
    assert r["observed_raw_n"] == 15
    assert r["scientific_grade"].endswith("NOT_INFERENTIALLY_QUALIFIED")


def test_35_of_60_is_review_support_candidate_but_not_science_issued():
    r = classify_observed_branch(
        country_question_n=5000, parent_n=60, observed_n=35,
        parent_target_counts={"no": 45, "yes": 15},
        child_target_counts={"no": 20, "yes": 15},
        policy=AdaptiveSupportPolicy(),
    )
    assert r["routine_exploration_eligible"]
    assert r["initial_review_support_candidate"]
    assert r["scientific_grade"] == "SOURCE_SAMPLE_REVIEWABLE_NOT_POPULATION_INFERENCE"


def test_spurious_four_person_minor_contrast_is_retained_but_not_autorecursed():
    p = AdaptiveSupportPolicy()
    r = classify_observed_branch(
        country_question_n=5000, parent_n=40, observed_n=4,
        parent_target_counts={"no": 20, "yes": 20},
        child_target_counts={"no": 4, "yes": 0},
        policy=p,
    )
    assert r["protected_minor_exploration_candidate"]
    assert r["target_total_variation_vs_parent"] == Decimal("0.5")
    assert p.max_protected_children_per_split == 0
    scheduled, conserved = order_child_probes(
        [("raw_sample_rare", r)], policy=p,
    )
    assert scheduled == []
    assert len(conserved) == 1
    assert conserved[0]["source_value"] == "raw_sample_rare"
    assert conserved[0]["reason"] == "PROTECTED_MINOR_PROBE_QUOTA_NOT_NEGATIVE"
    assert conserved[0]["support"]["source_observed_positive"]


def test_positive_Mi_under_independence_is_not_automatic_recursion():
    # Under independence, leading finite-sample MI bias at N=500 for 4x2
    # categories is about 0.00433 bits: positive != discovery.
    r = route_exploratory_split(SearchEvidence(
        common_case_n=500, target_observed_states=2,
        joint_predictor_observed_states=4,
        information_bits=0.00433,
        candidate_family_size=20, previous_search_nodes=0,
    ))
    assert r["raw_information_bits_per_respondent"] > 0
    assert r["net_search_codelength_bits"] < 0
    assert not r["admit_automatic_recursion"]
    assert r["source_observed_alternatives_preserved"]


def test_genuine_symmetric_xor_joint_can_exceed_penalty_without_single_gain():
    r = route_exploratory_split(SearchEvidence(
        common_case_n=16, target_observed_states=2,
        joint_predictor_observed_states=4,
        information_bits=1.0,
        candidate_family_size=3, previous_search_nodes=0,
    ))
    assert r["admit_automatic_recursion"]
    assert r["net_search_codelength_bits"] > 0
    assert r["grade"] == "PROVISIONAL_SOURCE_SAMPLE_ROUTING_NOT_INFERENTIAL_APPROVAL"


def test_effect_size_and_multiple_comparisons_both_change_codelength():
    weak = SearchEvidence(
        common_case_n=35, target_observed_states=2,
        joint_predictor_observed_states=4,
        information_bits=0.10, candidate_family_size=20,
        previous_search_nodes=0,
    )
    strong = SearchEvidence(
        common_case_n=35, target_observed_states=2,
        joint_predictor_observed_states=4,
        information_bits=0.9, candidate_family_size=20,
        previous_search_nodes=0,
    )
    assert not route_exploratory_split(weak)["admit_automatic_recursion"]
    assert route_exploratory_split(strong)["admit_automatic_recursion"]
    large_search = SearchEvidence(
        common_case_n=35, target_observed_states=2,
        joint_predictor_observed_states=4,
        information_bits=0.9, candidate_family_size=1000,
        previous_search_nodes=0,
    )
    assert (route_exploratory_split(large_search)["net_search_codelength_bits"]
            < route_exploratory_split(strong)["net_search_codelength_bits"])


def test_two_person_perfect_contrast_is_not_automatic_branch():
    r = route_exploratory_split(SearchEvidence(
        common_case_n=2, target_observed_states=2,
        joint_predictor_observed_states=2,
        information_bits=1.0, candidate_family_size=1,
        previous_search_nodes=0,
    ))
    assert r["too_sparse_for_automatic_recursion"]
    assert not r["admit_automatic_recursion"]


def test_source_same_case_support_and_joint_states_not_invented():
    cells = [
        (("yes", "A", "left"), 7),
        (("no", "A", "right"), 2),
        (("yes", "B", "right"), 1),
    ]
    assert source_observed_group_states(
        positive_cells=cells, target_axis=0, predictor_axes=(1,),
    ) == (10, 2, 2)
    assert source_observed_group_states(
        positive_cells=cells, target_axis=0, predictor_axes=(1, 2),
    ) == (10, 2, 3)
