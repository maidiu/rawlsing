"""Runnable unit harness for the W10 world-consumer probe (isolated, no owner writes)."""
from __future__ import annotations

import pytest

from probe.e05_vertical_experiment import (
    SUBJECT_SELECTOR,
    run_full_experiment,
)
from probe.modeled_selected_world import (
    DECLARED_HISTORICAL_YEAR,
    WORLD_GRADE,
    build_modeled_selected_world,
    world_spec_a,
    world_spec_b,
)
from probe.n10e_computed_edge import compute_n10e_product, handwritten_slice_hostile_probe
from probe.n10w_progressive_adapter import (
    GRADE_DYAD,
    ROUTES,
    STAGE_C0,
    STAGE_C1,
    STAGE_C2,
    N10WProgressiveRequest,
    evaluate_progressive_world_conditioning,
)


@pytest.fixture(scope="module")
def experiment():
    return run_full_experiment()


def test_subject_selector_is_uninstantiated_and_test_only():
    assert SUBJECT_SELECTOR["real_subject"] is False
    assert SUBJECT_SELECTOR["subject_kind"] == "UNINSTANTIATED_POSITIONED_SUBJECT_SELECTOR"
    assert SUBJECT_SELECTOR["declared_historical_year"] == DECLARED_HISTORICAL_YEAR
    assert "NOT_GOVERNED_SURVEY" in SUBJECT_SELECTOR["source_universe"]


def test_world_grade_is_test_only_modeled(experiment):
    assert experiment["world_a_identity"]["world_grade"] == WORLD_GRADE
    assert experiment["world_b_identity"]["world_grade"] == WORLD_GRADE
    assert "NOT_N9_OPERATIVE_CURRENT" in WORLD_GRADE


def test_v01_declared_single_eligibility_route_change(experiment):
    oracle = experiment["positive_oracles"]["V01_MODELED_CONTEXT_DIFFERENTIATION"]
    assert oracle["pass"], oracle
    assert oracle["change_count"] == 1
    assert oracle["declared_change"]["route_id"] == "formal_schooling"


def test_v02_two_progressive_steps_with_unique_witnesses(experiment):
    oracle = experiment["positive_oracles"]["V02_STEPWISE_WORLD_CONDITIONING"]
    assert oracle["pass"], oracle
    assert len(set(oracle["conditioner_witness_ids_A"].values())) == 3


def test_v03_identical_context_hash_stable(experiment):
    oracle = experiment["positive_oracles"]["V03_UNALTERED_CONTROL"]
    assert oracle["pass"], oracle
    assert oracle["canonical_bytes_equal"]


def test_v04_minority_alternatives_preserved(experiment):
    oracle = experiment["positive_oracles"]["V04_MINORITY_AND_CONTRADICTION"]
    assert oracle["pass"], oracle
    assert set(oracle["routes_present_in_B"]) == set(ROUTES)


def test_v05_counterfactual_reversal_restores_exact_supports(experiment):
    oracle = experiment["positive_oracles"]["V05_COUNTERFACTUAL_REVERSAL"]
    assert oracle["pass"], oracle
    assert oracle["exact_restoration"]


def test_v06_modeled_labels_and_null_route_probabilities(experiment):
    oracle = experiment["positive_oracles"]["V06_SOURCEFREE_EPISTEMIC_LABELS"]
    assert oracle["pass"], oracle
    assert oracle["route_numeric_probabilities"] == []
    assert oracle["n10e_computed_cells"]


def test_controlled_empirical_law_changes_computed_lane_only(experiment):
    oracle = experiment["positive_oracles"]["CONTROLLED_EMPIRICAL_LAW_VARIATION"]
    assert oracle["pass"], oracle
    assert oracle["n10e_lane_hash_base"] != oracle["n10e_lane_hash_changed_law"]


def test_at34_dyad_refused_individual_retained(experiment):
    oracle = experiment["positive_oracles"]["AT34_SAMPLING_UNIT_FIREWALL"]
    assert oracle["pass"], oracle


def test_hostile_oracles_h01_h10(experiment):
    for oracle_id, record in experiment["hostile_oracles"].items():
        assert record["pass"], (oracle_id, record)


def test_wrong_unit_year_and_revoked_scope_refuse(experiment):
    for record in experiment["typed_refusals"]:
        assert record["pass"], record


def test_replay_and_invalidation(experiment):
    for name, record in experiment["replay_and_invalidation"].items():
        assert record["pass"], (name, record)


def test_no_actor_no_model_and_no_integrated_pass_claim(experiment):
    assert experiment["execution"]["actor"] is False
    assert experiment["execution"]["model_calls"] == 0
    overall = experiment["overall"]
    assert overall["sourcefree_interface_court_pass"] is True
    assert overall["integrated_n9_n10w_pass"] is False


def test_receipts_carry_computed_n10e_lane_and_no_route_probabilities(experiment):
    for key in ("receipt_a", "receipt_b"):
        receipt = experiment[key]
        assert receipt["n10e_lane"]["lane_grade"].startswith("COMPUTED_N10E_SLICE")
        assert receipt["n10e_lane"]["computed_cells"]
        for stage in receipt["stages"]:
            for route, entry in stage["typed_route_support"].items():
                assert entry["probability"] is None
                assert entry["type_belief_voice_state"] == "UNKNOWN_NOT_ASSIGNED"
                assert entry["epistemic_label"] == "MODELED__NOT_OBSERVED__NOT_MEASURED"


def test_handwritten_slice_is_rejected_at_provider_boundary():
    probe = handwritten_slice_hostile_probe()
    assert probe["all_pass"], probe


def test_progressive_stages_are_ordered_and_witnessed(experiment):
    receipt = experiment["receipt_a"]
    stage_ids = [s["stage_id"] for s in receipt["stages"]]
    assert stage_ids == [STAGE_C0, STAGE_C1, STAGE_C2]
    for stage in receipt["stages"]:
        assert stage["conditioner_witness_id"].startswith("W10CW:")
        assert set(stage["typed_route_support"]) == set(ROUTES)
