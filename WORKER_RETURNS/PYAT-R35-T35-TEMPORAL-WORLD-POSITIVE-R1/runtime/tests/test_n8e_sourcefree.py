"""Frozen N03/EE12 admissibility tests over hypothetical receipts only."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

import n8e_sourcefree_comparator as C
import v553_candidate_eval


def ref(tag):
    return {"kind": "HYPOTHETICAL_REF",
            "object_id": "urn:test:hypothetical:" + tag,
            "content_hash": hashlib.sha256(tag.encode()).hexdigest()}


def wave(label, weights, variance, raw, source_version="v1",
         current_release_version="v1"):
    return dict(
        source_release_ref=ref(label + "_release"),
        field_ref=ref(label + "_field"),
        source_version=source_version,
        current_release_version=current_release_version,
        target_population="HYPOTHETICAL_ADULT_CITIZENS_18_PLUS",
        native_categories=[0, 1, 2, 3, 4],
        substantive_valid_codes=[0, 1, 2, 3, 4],
        positive_numerator_codes=[3, 4],
        special_codes={"dk": 9, "refused": 998, "missing": -1},
        special_counts={"dk": 3, "refused": 2, "missing": 1},
        weights_sum=float(sum(weights.values())),
        category_weights={str(key): float(value) for key, value in weights.items()},
        raw_counts={str(key): int(value) for key, value in raw.items()},
        design=dict(
            weight_ref=ref(label + "_weight"),
            psu_ref=ref(label + "_psu"),
            strata_ref=ref(label + "_strata"),
            variance_ref=ref(label + "_variance"),
            variance=variance,
            variance_method="DESIGN_BASED_REPLICATE",
            independent_cross_sections=True,
        ),
        release_asof="2026-01-01",
    )


def base_receipt():
    a = wave("a", {0: 10, 1: 20, 2: 20, 3: 30, 4: 20}, 0.0025,
             {0: 10, 1: 20, 2: 20, 3: 30, 4: 20})
    b = wave("b", {0: 20, 1: 20, 2: 20, 3: 60, 4: 80}, 0.0036,
             {0: 90, 1: 10, 2: 10, 3: 45, 4: 45})
    return dict(
        claim_id="HYPOTHETICAL_N8E_TWO_WAVE_DSAT_ARITHMETIC_CHECK",
        test_only=True,
        ghana=False,
        target_use=C.TARGET_USE,
        wave_a=a,
        wave_b=b,
        ee12=dict(issuer="HYPOTHETICAL_EE12_ISSUER",
                  relation_ref=ref("ee12_relation"),
                  snapshot_ref=ref("ee12_snapshot"),
                  target_use=C.TARGET_USE,
                  positive=True,
                  negative_necessary_condition_conflict=False),
        science=dict(estimand="WEIGHTED_SHARE_3_4_AMONG_0_4",
                     independence=True, covariance=None,
                     variance_method="DESIGN_BASED_REPLICATE",
                     no_change_rule=None),
    )


def test_hypothetical_full_admissibility_computes_weighted_delta():
    out = C.evaluate_hypothetical(base_receipt())
    assert out["state"] == "HYPOTHETICAL_MEASURED_INCREASE"
    assert out["classification"] == "HYPOTHETICAL_MEASURED_INCREASE"
    assert out["p_a"] == pytest.approx(0.5)
    assert out["p_b"] == pytest.approx(0.7)
    assert out["delta"] == pytest.approx(0.2)
    assert out["delta_variance"] == pytest.approx(0.0061)
    assert out["delta_se"] == pytest.approx(0.07810249675906655)
    assert out["interval"] == pytest.approx([0.04691910635222957, 0.35308089364777046])
    assert out["n8e_product"] is False
    assert out["ee12_issued"] is False
    assert out["ghana_claim"] is False


def test_weighted_estimate_differs_from_unweighted_raw_share():
    receipt = base_receipt()
    out = C.evaluate_hypothetical(receipt)
    assert out["unweighted_raw_share_b"] == pytest.approx(0.45)
    assert out["p_b"] == pytest.approx(0.7)
    assert out["p_b"] != out["unweighted_raw_share_b"]


def test_missing_ee12_holds():
    receipt = base_receipt()
    receipt["ee12"] = None
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "HOLD_EE12_ISSUER"
    assert out["delta"] is None


def test_missing_science_holds():
    receipt = base_receipt()
    receipt["science"] = None
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "HOLD_SCIENCE"
    assert out["delta"] is None


def test_missing_design_variance_unquantified():
    receipt = base_receipt()
    receipt["wave_b"]["design"]["variance"] = None
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "UNQUANTIFIED_DESIGN_UNCERTAINTY"
    assert out["delta"] is None


def test_dependent_waves_without_covariance_hold():
    receipt = base_receipt()
    receipt["science"]["independence"] = False
    receipt["science"]["covariance"] = None
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "HOLD_COVARIANCE"
    assert out["delta"] is None


def test_zero_denominator_is_zero_support_not_zero_delta():
    receipt = base_receipt()
    receipt["wave_b"]["weights_sum"] = 0.0
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "ZERO_SUPPORT"
    assert out["delta"] is None


def test_interval_including_zero_is_inconclusive_not_no_change():
    receipt = base_receipt()
    receipt["wave_b"] = wave("b", {0: 10, 1: 10, 2: 25, 3: 25, 4: 30},
                             0.0025, {0: 10, 1: 10, 2: 25, 3: 25, 4: 30})
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "INCONCLUSIVE_WITH_INTERVAL"
    assert out["classification"] is None
    assert out["delta"] == pytest.approx(0.05)
    assert out["interval"][0] < 0 < out["interval"][1]


def test_predeclared_no_change_rule_only_with_rule():
    receipt = base_receipt()
    receipt["wave_a"] = wave("a", {0: 10, 1: 20, 2: 20, 3: 30, 4: 20},
                             0.0004, {0: 10, 1: 20, 2: 20, 3: 30, 4: 20})
    receipt["wave_b"] = wave("b", {0: 10, 1: 10, 2: 28, 3: 22, 4: 30},
                             0.0004, {0: 10, 1: 10, 2: 28, 3: 22, 4: 30})
    receipt["science"]["no_change_rule"] = dict(
        margin=0.10, decision="TWO_SIDED_EQUIVALENCE_AT_DECLARED_MARGIN")
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION"
    assert out["delta"] == pytest.approx(0.02)
    assert out["declared_margin"] == pytest.approx(0.10)


def test_positive_necessary_condition_conflict_is_noncomparable():
    receipt = base_receipt()
    receipt["ee12"]["negative_necessary_condition_conflict"] = True
    receipt["ee12"]["negative_issuer"] = "HYPOTHETICAL_NEGATIVE_ISSUER"
    receipt["ee12"]["conflict_ref"] = ref("conflict")
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND"
    assert out["delta"] is None


def test_missing_category_zero_refused():
    receipt = base_receipt()
    receipt["wave_a"]["native_categories"] = [1, 2, 3, 4]
    receipt["wave_a"]["substantive_valid_codes"] = [1, 2, 3, 4]
    receipt["wave_a"]["category_weights"].pop("0")
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "CATEGORY_TOPOLOGY_MISMATCH"


def test_special_code_laundering_refused():
    receipt = base_receipt()
    receipt["wave_a"]["special_codes"] = {"dk": 9, "missing": -1}
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "SPECIAL_CODE_LAUNDERING"


def test_iid_binomial_variance_refused():
    receipt = base_receipt()
    receipt["wave_a"]["design"]["variance_method"] = "IID_BINOMIAL"
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "REFUSED_IID_OR_HEADLINE_VARIANCE"


def test_source_version_change_invalidates():
    receipt = base_receipt()
    receipt["wave_a"]["current_release_version"] = "v2"
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "STALE_SOURCE_INVALIDATED"


def test_missing_receipt_fields():
    receipt = base_receipt()
    receipt["wave_a"]["design"].pop("psu_ref")
    out = C.evaluate_hypothetical(receipt)
    assert out["state"] == "MISSING_SOURCE"
    assert "wave_a.design.psu_ref" in out["missing"]


def test_hypothetical_outputs_are_not_n8e_products_or_ghana_claims():
    out = C.evaluate_hypothetical(base_receipt())
    assert out["schema"] == "TEST_ONLY_N8E_ADMISSIBILITY_EXERCISE@1"
    assert out["n8e_product"] is False
    assert out["ee12_issued"] is False
    assert out["ghana_claim"] is False
    assert out["authority_issued"] is False
    assert out["claim_id"].startswith("HYPOTHETICAL_")


def test_ghana_n03_state_is_hold_with_all_numeric_fields_null():
    checked = C.ghana_null_checks()
    record = checked["record"]
    assert record["actual_result_state"] == "HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE"
    assert record["delta_proportion"] is None
    assert record["design_variance"] is None
    assert record["design_standard_error"] is None
    assert record["confidence_or_compatibility_interval"] is None
    assert record["inferential_classification"] is None
    assert record["wave_sample_and_weight_design_receipts"] == [None, None]
    assert record["wave_five_category_weighted_distributions"] == [None, None]
    assert record["positive_EE12_relation_and_snapshot"] is None
    assert record["actual_N9_consumer_receipt"] is None
    assert record["N8S_structural_rule_and_fact_refs"] is None
    assert record["substantive_valid_codes"] == [0, 1, 2, 3, 4]
    assert record["native_substantive_labels"]["0"] == "Ghana is not a democracy"
    assert record["typed_special_codes"]["R5"]["refused"] == 998
    assert record["typed_special_codes"]["R9"]["refused"] == 8
    assert all(checked["checks"].values())


def test_ghana_receipt_cannot_be_evaluated_as_a_numeric_claim():
    out = C.evaluate_hypothetical(C.ghana_n03_state())
    assert out["state"] == "MISSING_SOURCE"
    assert out["delta"] is None


def test_v553_candidate_is_structural_only_and_strictly_refuses_empty_inputs():
    out = v553_candidate_eval.evaluate()
    assert out["empty_readiness_error_count"] == 45
    assert out["empty_readiness_first_error"] == (
        "V553 thin temporal pressure layer missing packet path")
    assert out["empty_readiness_last_error"] == (
        "V553 thin temporal pressure layer missing harmonization_score")
    assert out["empty_readiness_has_structural_missing_paths"] is True
    report = out["empty_harmonization_report"]
    assert report["overall_status"] == (
        "STATUS: V553_WAVE_HARMONIZATION_SCAFFOLD_ONLY_SINGLE_WAVE")
    assert report["comparability_status"] == "comparability_limited"
    assert report["comparison_authority_status"] == "insufficient_multi_wave_authority"
    assert report["multiple_waves_present"] is False
    assert report["wave_count"] == 0
    assert out["candidate_verdict"] == (
        "V553_STRUCTURAL_TEMPORAL_HARMONIZATION_CANDIDATE__NOT_N8E_SURVEY_COMPARATOR")
    assert out["reuse_decision"] == (
        "REUSE_AS_STRUCTURAL_TEMPORAL_CANDIDATE_ONLY__NO_GHANA_OR_N8E_USE")
    assert out["consumes_respondent_survey_rows"] is False
    assert out["produces_survey_delta"] is False
    assert out["n8e_authority_created"] is False


def test_n9_target_use_is_context_only_and_installation_hold():
    out = C.evaluate_hypothetical(base_receipt())
    assert C.TARGET_USE == "EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY"
    assert out["checks"]["variance_method"] == "DESIGN_BASED_REPLICATE"
    record = C.ghana_n03_state()
    assert record["N9_product_family_and_target_use_permission"] is None
    assert record["actual_N9_consumer_receipt"] is None
