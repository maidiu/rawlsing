"""Tests for descriptive re-query/marginals/conditional contrasts on real FF01 joint."""
import pytest

from rawlsing_next.field_forge_observed_research import (
    ObservedResearchError,
    ask_exact_descriptive_support,
    ask_observed_minor_cell_candidates,
    ask_unissued_comparative_ranking,
)
from rawlsing_next.tests.test_pyat1009_ff01_generic_ingress import _case, _receive


def _real():
    _, _, _, query, result = _case(tag="FF01-REQUERY-XOR")
    return _receive(query, result)


def _cell_map(answer):
    return {
        row["target_state"]: row for row in answer.material()["complete_case_cells"]
    }


def test_genuine_three_way_exact_conditional_and_inverse_are_both_requeryable():
    received = _real()
    left = ask_exact_descriptive_support(
        received=received, target_index=2, conditions={0: "0"},
    )
    right = ask_exact_descriptive_support(
        received=received, target_index=0, conditions={2: "0"},
    )
    assert left.ref != right.ref
    assert left.material()["source_ff01_ref"] == right.material()["source_ff01_ref"]
    assert left.material()["condition_fully_resolved_n"] == 2
    assert _cell_map(left)["0"]["fraction_of_condition_complete_case"] == {"$exact_fraction": [1, 2]}
    assert _cell_map(left)["1"]["fraction_of_condition_complete_case"] == {"$exact_fraction": [1, 2]}
    assert right.material()["condition_fully_resolved_n"] == 2
    assert "POPULATION_CONFIDENCE_UNISSUED" in right.material()["limits"]


def test_double_condition_returns_full_observed_support_not_pairwise_reconstruction():
    received = _real()
    answer = ask_exact_descriptive_support(
        received=received, target_index=2, conditions={0: "0", 1: "0"},
    )
    assert answer.material()["condition_fully_resolved_n"] == 1
    assert _cell_map(answer)["0"]["raw_count"] == 1
    assert _cell_map(answer)["1"]["raw_count"] == 0
    assert _cell_map(answer)["0"]["fraction_of_condition_complete_case"] == {"$exact_fraction": [1, 1]}


def test_unconditioned_marginal_is_exact_no_fake_design_inference():
    observed = _real()
    marg = ask_exact_descriptive_support(
        received=observed, target_index=2, conditions={},
    )
    assert marg.material()["condition_fully_resolved_n"] == 4
    assert _cell_map(marg)["0"]["raw_count"] == 2
    assert _cell_map(marg)["1"]["raw_count"] == 2
    assert "NOT_SURVEY_DESIGN" in marg.material()["denominator_grade"]


def test_outside_domain_and_target_leakage_refuse_not_sample_zero():
    observed = _real()
    with pytest.raises(ObservedResearchError, match="domain"):
        ask_exact_descriptive_support(
            received=observed, target_index=2, conditions={0: "UNADMINISTERED"},
        )
    with pytest.raises(ObservedResearchError, match="target leakage"):
        ask_exact_descriptive_support(
            received=observed, target_index=2, conditions={2: "0"},
        )


def test_two_variable_context_absent_within_full_joint_is_typed_zero():
    observed = _real()
    # For 3-way parity, X=0,Z=0 selects exactly one fully resolved row.
    answer = ask_exact_descriptive_support(
        received=observed, target_index=1, conditions={0: "0", 2: "1"},
    )
    assert answer.material()["state"] == "OBSERVED_COMPLETE_CASE_SUPPORT"
    assert answer.material()["condition_fully_resolved_n"] == 1


def test_small_cell_candidate_is_a_bounded_inspection_not_recursion():
    observed = _real()
    res = ask_observed_minor_cell_candidates(
        received=observed, selected_condition_index=0, max_observed_support=1,
    )
    data = res.material()
    assert len(data["candidate_cells"]) == 4
    assert all(item["raw_support"] == 1 for item in data["candidate_cells"])
    assert "NOT_MINORITY_DISCOVERY" in data["kind"]
    assert "ADAPTIVE_RECURSIVE_MINORITY_DISCOVERY_UNISSUED" in data["limits"]


def test_ranking_request_returns_owner_hold_not_fake_mi_or_cramers_v():
    observed = _real()
    req = ask_unissued_comparative_ranking(
        received=observed, candidate_indices=(0, 1), target_index=2,
    )
    data = req.material()
    assert data["state"] == "SCIENTIFIC_METHOD_OWNER_HOLD"
    assert data["ranked_results"] is None
    assert len(data["candidate_refs"]) == 2
    with pytest.raises(ObservedResearchError, match="duplicate"):
        ask_unissued_comparative_ranking(
            received=observed, candidate_indices=(0, 0), target_index=2,
        )


def test_changing_actual_joint_source_changes_contextual_answer_and_replay_identity():
    _, _, _, q0, r0 = _case(tag="FF01-DYNAMIC", parity=0)
    _, _, _, q1, r1 = _case(tag="FF01-DYNAMIC", parity=1)
    original = ask_exact_descriptive_support(
        received=_receive(q0, r0), target_index=2, conditions={0: "0", 1: "0"},
    )
    changed = ask_exact_descriptive_support(
        received=_receive(q1, r1), target_index=2, conditions={0: "0", 1: "0"},
    )
    assert original.ref != changed.ref
    assert _cell_map(original)["0"]["raw_count"] == 1
    assert _cell_map(changed)["0"]["raw_count"] == 0


def test_descriptive_result_is_immutable_detached_and_identity_verifiable():
    observed = _real()
    answer = ask_exact_descriptive_support(
        received=observed, target_index=1, conditions={0: "1"},
    )
    exported = answer.material()
    exported["complete_case_cells"][0]["raw_count"] = 9000
    assert answer.material()["complete_case_cells"][0]["raw_count"] != 9000
    assert answer.ref == ask_exact_descriptive_support(
        received=observed, target_index=1, conditions={0: "1"},
    ).ref
