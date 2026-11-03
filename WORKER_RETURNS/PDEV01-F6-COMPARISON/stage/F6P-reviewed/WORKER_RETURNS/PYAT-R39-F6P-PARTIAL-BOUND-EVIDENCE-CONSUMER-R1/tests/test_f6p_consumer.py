"""F6P positive and hostile consumer court over the ACTUAL F6M product.

The expected values are from the frozen R35 F6C exact-rational oracle and the
F6M method contract, not from this consumer's output.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f6p_fixtures import build, f6m_blob, rehash, request  # noqa: E402

import f6p_partial_bound_evidence_consumer as C  # noqa: E402


def test_actual_f6m_source_is_exact_pinned_blob():
    assert f6m_blob() == "2df811d76db258d98d89ffb43c830cb221ff9a7d"


def test_w1_supported_synthesis_full_coverage():
    bundle = build("B", "W1_full_coverage_disjoint")
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    assert r["evidence_state"] == C.SUPPORTED
    assert r["uncovered_target_mass"] == "0"
    assert r["supported_point"] == {"formal": "5/8", "informal": "3/8"}
    assert r["conditional"]["state"] == "SUPPORTED_MODEL"
    assert r["input_bundle"]["decision"] == "SYNTHETIC_CANDIDATE"
    assert r["input_bundle"]["target_joint_status"] == "COMPLETE_EXPERIMENTAL_TARGET_JOINT"
    assert r["exclusions"] == []


def test_w2_partial_preserves_uncovered_mass():
    bundle = build("B", "W2_mixed_eligibility_trap")
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert r["evidence_state"] == C.PARTIAL
    assert r["uncovered_target_mass"] == "1/4"
    assert r["covered_subprobability"] == {
        "secure|formal": "1/4", "secure|informal": "1/8",
        "insecure|formal": "3/16", "insecure|informal": "3/16"}
    assert r["supported_point"] is None
    assert r["conditional"]["state"] == "UNAVAILABLE"
    assert r["conditional"]["reason"] == "NO_COMPLETE_TARGET_JOINT"
    assert r["input_bundle"]["target_joint_status"] == "NO_COMPLETE_TARGET_JOINT"
    assert any(e["source_id"] == "S_A" and e["stratum"] == "minority"
               and e["reason"] == "AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT"
               for e in r["exclusions"])


def test_w7_partial_preserves_half_uncovered_mass():
    bundle = build("B", "W7_source_excluded_all_strata")
    r = C.consume_f6m_evidence(bundle, request("W7_source_excluded_all_strata"))
    assert r["evidence_state"] == C.PARTIAL
    assert r["uncovered_target_mass"] == "1/2"
    assert r["covered_subprobability"] == {
        "secure|formal": "3/20", "secure|informal": "1/10",
        "insecure|formal": "1/8", "insecure|informal": "1/8"}
    assert r["supported_point"] is None
    assert {e["stratum"] for e in r["exclusions"] if e["source_id"] == "S_A"} == \
        {"majority", "minority"}
    assert all(e["reason"] == "AGGREGATE_SUPPORT_OR_MASS_INSUFFICIENT"
               for e in r["exclusions"])


def test_w3_partial_names_source_stratum_exclusions():
    bundle = build("B", "W3_minority_whole_stratum_absent")
    r = C.consume_f6m_evidence(bundle, request("W3_minority_whole_stratum_absent"))
    assert r["evidence_state"] == C.PARTIAL
    assert r["uncovered_target_mass"] == "1/5"
    assert r["supported_point"] is None
    assert {e["source_id"] for e in r["exclusions"]} == {"S_A", "S_B"}
    assert {e["reason"] for e in r["exclusions"]} == {"NO_SOURCE_STRATUM"}


def test_w4_self_conditioning_refused():
    bundle = build("B", "W4_outcome_leakage")
    r = C.consume_f6m_evidence(bundle, request("W4_outcome_leakage"))
    assert r["evidence_state"] == C.SELF_CONDITIONING
    assert r["conditional"]["state"] == "DESCRIPTIVE_SELF_CONDITIONING"
    assert r["conditional"]["self_conditioning_status"] == "OUTCOME_LEAKAGE_TAUTOLOGY"
    assert r["supported_point"] is None


def test_w6_duplicate_sample_incompatible_respondents():
    bundle = build("B", "W6_overlap_duplicate_sample")
    r = C.consume_f6m_evidence(bundle, request("W6_overlap_duplicate_sample"))
    assert r["evidence_state"] == C.INCOMPATIBLE_RESPONDENT
    assert r["input_bundle"]["decision"] == "SOURCE_INDEXED_BACKOFF"
    assert r["input_bundle"]["target_joint_status"] is None
    assert r["supported_point"] is None
    assert any(o.get("reason") == "DUPLICATE_SAMPLE" for o in r["overlap"])


def test_w8_category_outside_support():
    bundle = build("B", "W8_condition_outside_mapped_support")
    r = C.consume_f6m_evidence(bundle, request("W8_condition_outside_mapped_support"))
    assert r["evidence_state"] == C.CATEGORY_OUTSIDE
    assert r["conditional"]["reason"] == "CATEGORY_OUTSIDE_MAPPED_SUPPORT"
    assert r["supported_point"] is None


def test_A_w2_false_full_coverage_rejected():
    bundle = build("A", "W2_mixed_eligibility_trap")
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert r["uncovered_target_mass"] == "0"
    assert r["evidence_state"] == C.FALSE_FULL
    assert r["supported_point"] is None


def test_A_w7_false_full_coverage_rejected():
    bundle = build("A", "W7_source_excluded_all_strata")
    r = C.consume_f6m_evidence(bundle, request("W7_source_excluded_all_strata"))
    assert r["uncovered_target_mass"] == "0"
    assert r["evidence_state"] == C.FALSE_FULL
    assert r["supported_point"] is None


def test_A_w3_mislabelled_decision_rejected():
    bundle = build("A", "W3_minority_whole_stratum_absent")
    r = C.consume_f6m_evidence(bundle, request("W3_minority_whole_stratum_absent"))
    assert r["evidence_state"] == C.INCONSISTENT
    assert r["supported_point"] is None


def test_real_use_prohibited():
    bundle = build("B", "W1_full_coverage_disjoint")
    req = request("W1_full_coverage_disjoint")
    req["use"] = "REAL_USE"
    r = C.consume_f6m_evidence(bundle, req)
    assert r["evidence_state"] == C.PROHIBITED
    assert r["supported_point"] is None
    assert r["real_use_authorized"] is False


def test_forged_owner_admission_prohibited():
    bundle = build("B", "W1_full_coverage_disjoint")
    req = request("W1_full_coverage_disjoint")
    req["admission"] = "OWNER_APPROVED"
    r = C.consume_f6m_evidence(bundle, req)
    assert r["evidence_state"] == C.PROHIBITED
    assert any("SELF_DECLARED" in reason for reason in r["evidence_reasons"])
    assert r["supported_point"] is None


def test_revoked_source_refused():
    bundle = build("B", "W2_mixed_eligibility_trap")
    req = request("W2_mixed_eligibility_trap")
    req["revoked_source_ids"] = ["S_A"]
    r = C.consume_f6m_evidence(bundle, req)
    assert r["evidence_state"] == C.REVOKED
    assert r["supported_point"] is None


def test_unknown_design_weight_not_defaulted():
    bundle = build("B", "W2_mixed_eligibility_trap")
    req = request("W2_mixed_eligibility_trap")
    req["requested_use"] = "POPULATION_ESTIMATE"
    r = C.consume_f6m_evidence(bundle, req)
    assert r["evidence_state"] == C.WEIGHT_UNKNOWN
    assert r["sampling"]["sampling_status"] == "UNKNOWN_DESIGN"
    assert r["sampling"]["weight_defaulted_to_one"] is False
    assert r["supported_point"] is None


def test_bundle_replay_mismatch_refused():
    bundle = build("B", "W2_mixed_eligibility_trap")
    bundle["candidate"]["uncovered_target_mass"] = "0"
    with pytest.raises(C.ConsumerRefusal, match="BUNDLE_REPLAY_MISMATCH"):
        C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))


def test_inconsistent_product_refused():
    bundle = build("B", "W2_mixed_eligibility_trap")
    bundle["candidate"]["covered_subprobability"][0]["probability"] = "1/2"
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert r["evidence_state"] == C.INCONSISTENT
    assert r["supported_point"] is None


def test_severed_f6m_product_changes_consumer():
    bundle = build("B", "W2_mixed_eligibility_trap")
    bundle["candidate"] = None
    bundle["decision"] = "SOURCE_INDEXED_BACKOFF"
    bundle["target_joint_status"] = "NO_COMPLETE_TARGET_JOINT"
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert r["evidence_state"] != C.PARTIAL
    assert r["supported_point"] is None


def test_no_route_probability_or_selection_weight():
    bundle = build("B", "W1_full_coverage_disjoint")
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    text = json.dumps(r, sort_keys=True)
    assert '"route_probability":' not in text
    assert '"selection_weight":' not in text
    assert r["no_route_probability"] is True
    assert r["no_selection_weight"] is True
    assert r["real_use_authorized"] is False


def test_incomplete_native_domain_producer_refusal():
    with pytest.raises(Exception) as exc:
        build("B", "W5_positivity_incomplete_native_domain")
    assert "incomplete native joint domain" in str(exc.value)
    with pytest.raises(C.ConsumerRefusal):
        C.consume_f6m_evidence(None, {})


def test_values_read_and_source_module_provenance():
    bundle = build("B", "W2_mixed_eligibility_trap")
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert r["source_product"]["module_git_blob"] == \
        "2df811d76db258d98d89ffb43c830cb221ff9a7d"
    assert r["source_product"]["module_sha256"] == \
        "2930b5cd15c899146e9552b2e6b0efa3fc5835e57e58a6c16d756093e21d3871"
    assert r["input_bundle"]["content_hash"] == bundle["content_hash"]
    for field in ("candidate.uncovered_target_mass",
                  "candidate.covered_subprobability",
                  "candidate.support", "candidate.uncertainty",
                  "conditional"):
        assert field in r["values_read"]
    assert all(F(cell["lower"]) <= F(cell["upper"]) for cell in r["bounds"])


def test_wrong_clock_or_source_version_refused():
    bundle = build("B", "W1_full_coverage_disjoint")
    bundle["refusals"] = {"S_A": ["TIME_NOT_APPLICABLE"]}
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    assert r["evidence_state"] == C.WRONG_VERSION
    assert r["supported_point"] is None


def test_incorrect_scope_refused():
    bundle = build("B", "W1_full_coverage_disjoint")
    bundle["refusals"] = {"S_A": ["TARGET_SCOPE_MISMATCH"]}
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    assert r["evidence_state"] == C.INCOMPATIBLE_POPULATION
    assert r["supported_point"] is None


def test_unsupported_transport_refused():
    bundle = build("B", "W1_full_coverage_disjoint")
    bundle["refusals"] = {"S_A": ["TRANSPORT_PERMISSION_NOT_ADMITTED"]}
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    assert r["evidence_state"] == C.UNVERIFIED_TRANSPORT
    assert r["supported_point"] is None


def test_incomplete_native_domain_refused():
    bundle = build("B", "W1_full_coverage_disjoint")
    bundle["refusals"] = {"S_A": ["JOINT_DOMAIN_EXCEEDS_BUDGET"]}
    bundle = rehash(bundle)
    r = C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))
    assert r["evidence_state"] == C.INCOMPLETE_DOMAIN
    assert r["supported_point"] is None


def test_forged_real_use_flag_refused():
    bundle = build("B", "W1_full_coverage_disjoint")
    bundle["real_use_authorized"] = True
    bundle = rehash(bundle)
    with pytest.raises(C.ConsumerRefusal, match="FORGED_MODEL_USE_ADMISSION"):
        C.consume_f6m_evidence(bundle, request("W1_full_coverage_disjoint"))


def test_minority_cells_are_not_pruned_from_partial_bounds():
    bundle = build("B", "W2_mixed_eligibility_trap")
    r = C.consume_f6m_evidence(bundle, request("W2_mixed_eligibility_trap"))
    assert set(r["covered_subprobability"]) == {
        "secure|formal", "secure|informal", "insecure|formal", "insecure|informal"}
    assert r["supported_point"] is None
    assert r["bounds"]
