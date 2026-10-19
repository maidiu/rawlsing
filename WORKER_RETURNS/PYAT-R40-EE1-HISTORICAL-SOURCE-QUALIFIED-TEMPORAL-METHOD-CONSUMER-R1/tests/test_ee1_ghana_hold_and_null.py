"""C5 Ghana EE12/N8E hold: frozen null record, refusal of Ghana claims, and a
strictly hypothetical exercise that never becomes a Ghana trend."""
from __future__ import annotations

import math

from ee1_historical_consumer import build_comparison_product
from ee1_world import N8E


def _frozen_hypothetical_receipt():
    def wave(weights, raw, variance, release_asof, version):
        return dict(
            source_release_ref=f"TESTONLY_{version}",
            field_ref=f"TESTONLY_{version}_FIELD",
            source_version=version,
            current_release_version=version,
            target_population="TESTONLY_ADULTS",
            native_categories=[0, 1, 2, 3, 4],
            substantive_valid_codes=[0, 1, 2, 3, 4],
            positive_numerator_codes=[3, 4],
            special_codes={"dk": 9, "refused": 998, "missing": -1},
            special_counts={"dk": 3, "refused": 1, "missing": 0},
            weights_sum=sum(weights.values()),
            category_weights=weights,
            raw_counts=raw,
            design=dict(weight_ref=f"W_{version}", psu_ref=f"P_{version}",
                        strata_ref=f"S_{version}", variance_ref=f"V_{version}",
                        variance=variance, variance_method="DESIGN_BASED_TAYLOR",
                        independent_cross_sections=True),
            release_asof=release_asof)
    return dict(
        claim_id="HYPOTHETICAL_EE1_TWO_PERIOD_METHOD_EXERCISE",
        test_only=True,
        ghana=False,
        target_use=N8E.TARGET_USE,
        wave_a=wave({"0": 20, "1": 20, "2": 10, "3": 30, "4": 20},
                    {"0": 40, "1": 20, "2": 15, "3": 15, "4": 10},
                    0.00305, "2021-06-01", "A2020"),
        wave_b=wave({"0": 10, "1": 10, "2": 10, "3": 30, "4": 40},
                    {"0": 5, "1": 10, "2": 15, "3": 25, "4": 45},
                    0.00305, "2023-06-01", "B2022"),
        ee12=dict(positive=True, target_use=N8E.TARGET_USE,
                  issuer="TESTONLY_ISSUER", relation_ref="TESTONLY_REL",
                  snapshot_ref="TESTONLY_SNAP"),
        science=dict(estimand="WEIGHTED_SHARE_3_4_AMONG_0_4",
                     independence=True,
                     variance_method="DESIGN_BASED_TAYLOR",
                     no_change_rule=None))


def test_ghana_frozen_null_record():
    record = N8E.ghana_n03_state()
    assert record["actual_result_state"] == "HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE"
    for field in ("delta_proportion", "design_variance", "design_standard_error",
                  "confidence_or_compatibility_interval",
                  "inferential_classification"):
        assert record[field] is None
    assert record["positive_EE12_relation_and_snapshot"] is None
    assert record["actual_N9_consumer_receipt"] is None
    checks = N8E.ghana_null_checks()
    assert checks["all_null"] is True


def test_ghana_claim_is_refused_before_any_number():
    result = N8E.evaluate_hypothetical({
        "claim_id": "HYPOTHETICAL_ATTEMPT", "test_only": True, "ghana": True,
        "target_use": N8E.TARGET_USE, "wave_a": None, "wave_b": None,
        "ee12": None, "science": None})
    assert result["state"] == "REFUSED_NON_HYPOTHETICAL_OR_GHANA_CLAIM"
    assert result["delta"] is None


def test_hypothetical_method_exercise_is_labeled_and_bounded():
    result = N8E.evaluate_hypothetical(_frozen_hypothetical_receipt())
    assert result["state"] == "HYPOTHETICAL_MEASURED_INCREASE"
    assert result["n8e_product"] is False
    assert result["ee12_issued"] is False
    assert result["ghana_claim"] is False
    assert result["authority_issued"] is False
    assert abs(result["p_a"] - 0.5) < 1e-12
    assert abs(result["p_b"] - 0.7) < 1e-12
    assert abs(result["delta"] - 0.2) < 1e-12
    assert abs(result["delta_variance"] - 0.0061) < 1e-6
    assert abs(result["delta_se"] - math.sqrt(0.0061)) < 1e-9
    lower, upper = result["interval"]
    assert abs(lower - 0.046921) < 1e-4
    assert abs(upper - 0.353079) < 1e-4
    assert result["unweighted_raw_share_a"] != result["p_a"]


def test_ee1_product_contains_no_ghana_number_and_full_hold():
    product, _ = build_comparison_product({"state": "COMPARABLE_PROBE_ONLY"})
    hold = product["ghana_hold"]
    assert hold["delta_proportion"] is None
    assert hold["design_variance"] is None
    assert hold["confidence_or_compatibility_interval"] is None
    assert product["ghana_null_all"] is True
    assert product["authority"]["ghana_claim"] is False
    assert product["authority"]["ee12_issued"] is False
    assert product["authority"]["n8e_product"] is False


def test_design_and_authority_change_refusal_channels():
    iid = _frozen_hypothetical_receipt()
    iid["wave_b"]["design"]["variance_method"] = "IID_BINOMIAL"
    refused = N8E.evaluate_hypothetical(iid)
    assert refused["state"] == "REFUSED_IID_OR_HEADLINE_VARIANCE"
    assert refused["delta"] is None

    no_issuer = _frozen_hypothetical_receipt()
    no_issuer["ee12"] = None
    held = N8E.evaluate_hypothetical(no_issuer)
    assert held["state"] == "HOLD_EE12_ISSUER"
    assert held["delta"] is None

    stale = _frozen_hypothetical_receipt()
    stale["wave_a"]["current_release_version"] = "A2020_R2"
    invalidated = N8E.evaluate_hypothetical(stale)
    assert invalidated["state"] == "STALE_SOURCE_INVALIDATED"
    assert invalidated["delta"] is None
