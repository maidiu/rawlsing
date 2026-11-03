"""Five historical-function jurisprudence tests for PDEV01 F6 comparison, TEST_ONLY."""
from __future__ import annotations
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]
F = json.loads((R / "evidence/replay_f6.json").read_text())
C = json.loads((R / "evidence/f6p-receiver-comparison.json").read_text())


def test_01_history_pinned_to_actual_f6m_f6p_reviews():
    p = F["source_pins"]
    assert p["f6m_repair_review"] == "9b885d80be83c25295b3b43a5ece705c4e5c2fbb"
    assert p["f6p_author"] == "7d7ed1cb01bfd32383ee487996d2595c666a07b2"
    assert p["f6p_review"] == "2e00c8c9e9f2d5f78e40ebfedc2f4468dd97edec"
    assert p["f6c"] == "c1ebe091fa2bd12b254e5599cf37975fe438d462"
    assert F["author_tests"]["implementation_7d7"]["seed0"] == "26 passed"
    assert F["author_tests"]["implementation_7d7"]["seed1"] == "26 passed"
    assert F["author_tests"]["publication_912"]["seed0"] == "32 passed"
    assert F["author_tests"]["publication_912"]["seed1"] == "32 passed"
    assert F["independent_reviewer_tests"]["seed0"] == "8 passed"
    assert F["independent_reviewer_tests"]["seed1"] == "8 passed"
    for name in ("f6p-author-tests-seed0.log", "f6p-author-tests-seed1.log",
                 "f6p-authored-912-tests-seed0.log", "f6p-authored-912-tests-seed1.log",
                 "f6p-reviewer-tests-seed0.log", "f6p-reviewer-tests-seed1.log"):
        assert (R / "logs" / name).is_file()


def test_02_current_requirement_is_composer_gap_not_a_new_build():
    g31 = F["gap031"]
    assert g31["requirement"].startswith("ROADMAP:S07.2")
    assert g31["current_successor"].startswith("pre553_source_relations.py::guard_estimand_composition")
    assert g31["disposition"] == "TRUE_CURRENT_GAP"
    assert g31["next_work"] == "OWNER_DECIDE"
    assert g31["no_build"] is True
    assert F["s_f6"]["current_status"] == "MISSING_PRODUCER_OR_READER"
    assert F["s_f6"]["disposition"] == "NO_JUSTIFIED_CONSUMER"
    assert F["s_f6"]["no_build"] is True


def test_03_first_consumer_actual_f6p_and_wp2_typed_mismatch():
    first = F["first_consumer"]
    assert first["symbol"].endswith("consume_f6m_evidence")
    assert first["line"] == 189
    assert first["partial_bounds_reach"] is True
    assert first["uncovered_mass"] == {
        "W1_full_coverage_disjoint": "0",
        "W2_mixed_eligibility_trap": "1/4",
        "W3_minority_whole_stratum_absent": "1/5",
        "W7_source_excluded_all_strata": "1/2",
    }
    assert C["conclusion"]["partial_bounds_reach_f6p_consumer"] is True
    assert C["conclusion"]["partial_bounds_reach_current_wp2_receiver"] is False
    assert F["current_receiver"]["first_typed_mismatch"]["code"] == (
        "F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR")
    assert F["current_receiver"]["first_typed_mismatch"]["first_missing_field"] == "native_bundle"
    assert F["current_receiver"]["f6m_native_sidecar_expected_fields"] == [
        "native_bundle", "native_conditional_consumer"]
    assert F["current_receiver"]["first_typed_mismatch"]["read_effect"] == (
        "NO_NONPARENT_OPTIONS_READ; NO_F6M_E04_JOIN")
    assert F["current_receiver"]["f6m_to_e04_join"] is False
    assert F["current_receiver"]["n9_first_import"] is False


def test_04_authority_distinct_populations_no_pooling_point_refusal_and_uncertainty():
    first = F["first_consumer"]
    assert first["no_pooling"] is True
    assert first["distinct_populations"] is True
    assert first["point_refused_when_uncovered"] is True
    assert first["no_common_respondent_inference"] is True
    for world in ("W2_mixed_eligibility_trap", "W7_source_excluded_all_strata",
                  "W3_minority_whole_stratum_absent"):
        row = C["results"][world]
        assert row["evidence_state"] == "PARTIAL_IDENTIFICATION"
        assert row["supported_point"] is None
        assert row["uncovered_target_mass"] != "0"
        assert row["no_route_probability"] is True
        assert row["no_selection_weight"] is True
        assert row["real_use_authorized"] is False
    assert C["refusals"]["REAL_USE"]["evidence_state"] == "PROHIBITED_MODEL_USE"
    assert C["refusals"]["TRANSPORT_PERMISSION"]["evidence_state"] == "PROHIBITED_MODEL_USE"
    assert C["refusals"]["ADMISSION"]["evidence_state"] == "PROHIBITED_MODEL_USE"
    assert C["conclusion"]["population_claim"] is False


def test_05_comparative_disposition_preserve_test_oracle_no_production_repair():
    g32 = F["gap032"]
    assert g32["disposition"] == "HISTORICAL_REJECTED_PRESERVE"
    assert g32["variants"]["S03FO_A"]["disposition"] == "HISTORICAL_REJECTED_PRESERVE"
    assert g32["variants"]["A0"]["disposition"] == "HISTORICAL_REJECTED_PRESERVE"
    assert g32["variants"]["F6M_B"]["state"] == "PARTIAL_IDENTIFICATION_ONLY_WHEN_UNCOVERED"
    assert g32["variants"]["F6P"]["review"] == "ACCEPT_SOURCEFREE_TEST_ONLY"
    assert g32["non_loss_reuse_candidate"].startswith("F6M/F6P only")
    assert g32["next_work"] == "NO_ACTION"
    assert F["gap031"]["next_work"] == "OWNER_DECIDE"
    assert F["s_f6"]["next_work"] == "NO_ACTION"
    assert "No original source" in F["limits"][0]
