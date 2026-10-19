"""Source-free N8E/EE12 admissibility and arithmetic exercise.

This module is a specification court, not an N8E producer, not an EE12 issuer
and not a Ghana measurement.  It accepts only explicitly HYPOTHETICAL receipts,
checks the N03 frozen conditions, and computes a weighted two-wave delta only
when every condition is typed positive.  The Ghana N03 state is returned as a
frozen null record and is never computed here.
"""
from __future__ import annotations

import math

Z = 1.96
STATES = (
    "MISSING_SOURCE",
    "REFUSED_NON_HYPOTHETICAL_OR_GHANA_CLAIM",
    "STALE_SOURCE_INVALIDATED",
    "CATEGORY_TOPOLOGY_MISMATCH",
    "SPECIAL_CODE_LAUNDERING",
    "ZERO_SUPPORT",
    "HOLD_EE12_ISSUER",
    "SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND",
    "HOLD_SCIENCE",
    "UNQUANTIFIED_DESIGN_UNCERTAINTY",
    "REFUSED_IID_OR_HEADLINE_VARIANCE",
    "HOLD_COVARIANCE",
    "INCONCLUSIVE_WITH_INTERVAL",
    "NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION",
    "HYPOTHETICAL_MEASURED_INCREASE",
    "HYPOTHETICAL_MEASURED_DECREASE",
    "HYPOTHETICAL_MEASURED_EXACT_ZERO_POINT",
)
WAVE_FIELDS = (
    "source_release_ref", "field_ref", "source_version", "current_release_version",
    "target_population", "native_categories", "substantive_valid_codes",
    "positive_numerator_codes", "special_codes", "special_counts",
    "weights_sum", "category_weights", "raw_counts", "design", "release_asof",
)
DESIGN_FIELDS = (
    "weight_ref", "psu_ref", "strata_ref", "variance_ref",
    "variance", "variance_method", "independent_cross_sections",
)
SPECIAL_KEYS = ("dk", "refused", "missing")
TARGET_USE = "EMPIRICAL_ATTITUDE_TEMPORAL_CONTEXT_ONLY"


def _result(state, **extra):
    out = dict(
        schema="TEST_ONLY_N8E_ADMISSIBILITY_EXERCISE@1",
        test_only=True,
        n8e_product=False,
        ee12_issued=False,
        ghana_claim=False,
        authority_issued=False,
        state=state,
        classification=None,
        p_a=None, p_b=None, delta=None,
        delta_variance=None, delta_se=None, interval=None,
        unweighted_raw_share_a=None, unweighted_raw_share_b=None,
        checks=dict(extra.pop("checks", {})),
    )
    out.update(extra)
    return out


def _missing(obj, fields):
    return [field for field in fields if field not in obj]


def _weights(wave):
    return {str(key): float(value) for key, value in wave["category_weights"].items()}


def _weighted_share(wave):
    weights = _weights(wave)
    total = float(wave["weights_sum"])
    return sum(weights[str(code)] for code in wave["positive_numerator_codes"]) / total


def _raw_share(wave):
    counts = {str(key): float(value) for key, value in wave["raw_counts"].items()}
    total = sum(counts.values())
    return sum(counts[str(code)] for code in wave["positive_numerator_codes"]) / total


def evaluate_hypothetical(receipt):
    if not isinstance(receipt, dict):
        return _result("MISSING_SOURCE", missing=["receipt"])
    missing_top = _missing(receipt, ("claim_id", "test_only", "ghana",
                                     "target_use", "wave_a", "wave_b",
                                     "ee12", "science"))
    if missing_top:
        return _result("MISSING_SOURCE", missing=missing_top)
    claim_id = receipt["claim_id"]
    if (receipt["test_only"] is not True or receipt["ghana"] is not False or
            not str(claim_id).startswith("HYPOTHETICAL_")):
        return _result("REFUSED_NON_HYPOTHETICAL_OR_GHANA_CLAIM",
                       claim_id=claim_id)
    for label in ("wave_a", "wave_b"):
        missing = _missing(receipt[label], WAVE_FIELDS)
        if missing:
            return _result("MISSING_SOURCE", missing=[label + "." + field
                                                      for field in missing])
        missing_design = _missing(receipt[label]["design"], DESIGN_FIELDS)
        if missing_design:
            return _result("MISSING_SOURCE",
                           missing=[label + ".design." + field
                                    for field in missing_design])
    for label in ("wave_a", "wave_b"):
        wave = receipt[label]
        if wave["source_version"] != wave["current_release_version"]:
            return _result("STALE_SOURCE_INVALIDATED", claim_id=claim_id,
                           wave=label,
                           source_version=wave["source_version"],
                           current_release_version=wave["current_release_version"])
    for label in ("wave_a", "wave_b"):
        wave = receipt[label]
        categories = list(wave["native_categories"])
        substantive = list(wave["substantive_valid_codes"])
        numerator = list(wave["positive_numerator_codes"])
        keys = sorted(str(key) for key in wave["category_weights"])
        if (categories != [0, 1, 2, 3, 4] or substantive != [0, 1, 2, 3, 4] or
                numerator != [3, 4] or keys != ["0", "1", "2", "3", "4"]):
            return _result("CATEGORY_TOPOLOGY_MISMATCH", claim_id=claim_id,
                           wave=label, categories=categories,
                           substantive=substantive, numerator=numerator,
                           category_keys=keys)
    for label in ("wave_a", "wave_b"):
        wave = receipt[label]
        special = wave["special_codes"]
        counts = wave["special_counts"]
        if set(special) != set(SPECIAL_KEYS) or set(counts) != set(SPECIAL_KEYS):
            return _result("SPECIAL_CODE_LAUNDERING", claim_id=claim_id,
                           wave=label, special_codes=special,
                           special_counts=counts)
        special_values = {int(special[key]) for key in SPECIAL_KEYS}
        if any(int(key) in special_values for key in wave["category_weights"]) or \
                special_values & {int(code) for code in wave["substantive_valid_codes"]}:
            return _result("SPECIAL_CODE_LAUNDERING", claim_id=claim_id,
                           wave=label, special_values=sorted(special_values))
        if any(not isinstance(count, int) or count < 0 for count in counts.values()):
            return _result("SPECIAL_CODE_LAUNDERING", claim_id=claim_id,
                           wave=label, reason="TYPED_SPECIAL_COUNTS_NOT_NONNEGATIVE_INTEGERS")
        if int(wave["weights_sum"]) <= 0:
            return _result("ZERO_SUPPORT", claim_id=claim_id, wave=label,
                           reason="DENOMINATOR_WEIGHT_SUM_ZERO")
    ee12 = receipt["ee12"]
    if ee12 is None:
        return _result("HOLD_EE12_ISSUER", claim_id=claim_id,
                       reason="NO_POSITIVE_EXACT_EE12_C7_RELATION_AND_SNAPSHOT")
    if ee12.get("negative_necessary_condition_conflict") is True:
        if not ee12.get("negative_issuer") or not ee12.get("conflict_ref"):
            return _result("HOLD_EE12_ISSUER", claim_id=claim_id,
                           reason="NEGATIVE_CONFLICT_NOT_ISSUED_WITH_EXACT_PROOF")
        return _result("SOURCE_PROVEN_NONCOMPARABLE_FOR_EXACT_ESTIMAND",
                       claim_id=claim_id,
                       negative_issuer=ee12.get("negative_issuer"),
                       conflict_ref=ee12.get("conflict_ref"))
    if (ee12.get("positive") is not True or
            ee12.get("target_use") != TARGET_USE or
            not ee12.get("issuer") or not ee12.get("relation_ref") or
            not ee12.get("snapshot_ref")):
        return _result("HOLD_EE12_ISSUER", claim_id=claim_id,
                       reason="EE12_POSITIVE_TARGET_USE_OR_EXACT_REFS_MISSING")
    science = receipt["science"]
    if science is None:
        return _result("HOLD_SCIENCE", claim_id=claim_id,
                       reason="NO_INDEPENDENT_ESTIMAND_WEIGHT_DESIGN_VARIANCE_DECISION")
    if (science.get("estimand") != "WEIGHTED_SHARE_3_4_AMONG_0_4" or
            "independence" not in science or
            "variance_method" not in science or "no_change_rule" not in science):
        return _result("HOLD_SCIENCE", claim_id=claim_id,
                       reason="ESTIMAND_INDEPENDENCE_VARIANCE_OR_RULE_NOT_FROZEN")
    for label in ("wave_a", "wave_b"):
        design = receipt[label]["design"]
        if design.get("variance") is None:
            return _result("UNQUANTIFIED_DESIGN_UNCERTAINTY", claim_id=claim_id,
                           wave=label,
                           reason="NO_DESIGN_BASED_VARIANCE_AUTHORITY")
        if str(design.get("variance_method", "")).upper() in (
                "IID_BINOMIAL", "HEADLINE_N", "SRS_BINOMIAL"):
            return _result("REFUSED_IID_OR_HEADLINE_VARIANCE", claim_id=claim_id,
                           wave=label, variance_method=design.get("variance_method"))
        if float(design["variance"]) < 0:
            return _result("UNQUANTIFIED_DESIGN_UNCERTAINTY", claim_id=claim_id,
                           wave=label, reason="NEGATIVE_VARIANCE")
    if science["independence"] is False and science.get("covariance") is None:
        return _result("HOLD_COVARIANCE", claim_id=claim_id,
                       reason="DEPENDENT_WAVES_REQUIRE_AUTHORIZED_COVARIANCE")
    w_a, w_b = receipt["wave_a"], receipt["wave_b"]
    p_a = _weighted_share(w_a)
    p_b = _weighted_share(w_b)
    delta = p_b - p_a
    variance = float(w_a["design"]["variance"]) + float(w_b["design"]["variance"])
    if science["independence"] is False:
        variance += 2.0 * float(science["covariance"])
    if variance < 0:
        return _result("UNQUANTIFIED_DESIGN_UNCERTAINTY", claim_id=claim_id,
                       reason="NEGATIVE_DELTA_VARIANCE")
    se = math.sqrt(variance)
    interval = [delta - Z * se, delta + Z * se]
    checks = dict(
        category_zero_substantive=True,
        special_codes_typed_separately=dict(
            wave_a=w_a["special_counts"], wave_b=w_b["special_counts"]),
        weighted_ratio_not_raw_counts=True,
        independence=science["independence"],
        covariance=science.get("covariance"),
        variance_method=science["variance_method"],
        z=Z,
        no_change_rule=science.get("no_change_rule"),
    )
    rule = science.get("no_change_rule")
    if rule is not None:
        margin = float(rule["margin"])
        if (abs(delta) <= margin and interval[0] >= -margin and
                interval[1] <= margin):
            return _result(
                "NO_MEASURABLE_CHANGE_AT_DECLARED_PRECISION", claim_id=claim_id,
                p_a=p_a, p_b=p_b, delta=delta, delta_variance=variance,
                delta_se=se, interval=interval,
                unweighted_raw_share_a=_raw_share(w_a),
                unweighted_raw_share_b=_raw_share(w_b),
                checks=checks, declared_margin=margin, decision=rule.get("decision"))
    if interval[0] <= 0.0 <= interval[1]:
        return _result(
            "INCONCLUSIVE_WITH_INTERVAL", claim_id=claim_id,
            p_a=p_a, p_b=p_b, delta=delta, delta_variance=variance,
            delta_se=se, interval=interval,
            unweighted_raw_share_a=_raw_share(w_a),
            unweighted_raw_share_b=_raw_share(w_b), checks=checks)
    classification = ("HYPOTHETICAL_MEASURED_INCREASE" if delta > 0 else
                      "HYPOTHETICAL_MEASURED_DECREASE" if delta < 0 else
                      "HYPOTHETICAL_MEASURED_EXACT_ZERO_POINT")
    return _result(
        classification, claim_id=claim_id,
        classification=classification,
        p_a=p_a, p_b=p_b, delta=delta, delta_variance=variance,
        delta_se=se, interval=interval,
        unweighted_raw_share_a=_raw_share(w_a),
        unweighted_raw_share_b=_raw_share(w_b), checks=checks)


def ghana_n03_state():
    """The frozen N03 null record.  No number is computed or inferred."""
    record = dict(
        schema="N8E_GHA_DEMOCRACY_SATISFACTION_DELTA@1",
        proof_grade="FROZEN_EXPECTATION_ONLY",
        claim_id="N8E_GHA_R5Q43_R9Q31_DSAT_R1",
        graph_edge="TEMP_SRC02_SRC03",
        country="Ghana",
        target_population="adult citizens age >=18 in each independent field period",
        source_refs=[
            dict(SRC="SRC02", wave="R5", item="GHA:Q43",
                 root_sha256="c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
                 field_dates="2012-05-08/2012-05-27", release_version=None,
                 per_wave_fact_ref=None),
            dict(SRC="SRC03", wave="R9", item="GHA:Q31",
                 root_sha256="3afcecd08d2f4b531a926d455a943084d9f71c1276b4f3a58e77a9162e6879d8",
                 field_dates="2022-04-04/2022-04-20", release_version=None,
                 per_wave_fact_ref=None),
        ],
        native_substantive_labels={
            "0": "Ghana is not a democracy",
            "1": "not at all satisfied",
            "2": "not very satisfied",
            "3": "fairly satisfied",
            "4": "very satisfied"},
        substantive_valid_codes=[0, 1, 2, 3, 4],
        positive_numerator_codes=[3, 4],
        typed_special_codes={"R5": {"dk": 9, "refused": 998, "missing": -1},
                             "R9": {"dk": 9, "refused": 8, "missing": -1}},
        denominator="eligible national citizens, asked and valid one of 0..4",
        estimand="weighted p2022(3,4)-p2012(3,4)",
        wave_sample_and_weight_design_receipts=[None, None],
        wave_five_category_weighted_distributions=[None, None],
        wave_asked_valid_and_typed_nonresponse_receipts=[None, None],
        weight_PSU_stratum_variance_authority=None,
        independent_scientific_decision=None,
        positive_EE12_relation_and_snapshot=None,
        source_run_authority_and_product_receipts=[None, None],
        N8E_implementation_commit_blob=None,
        delta_proportion=None,
        design_variance=None,
        design_standard_error=None,
        confidence_or_compatibility_interval=None,
        inferential_classification=None,
        actual_result_state="HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE",
        N9_product_family_and_target_use_permission=None,
        actual_N9_consumer_receipt=None,
        asof_replay_invalidation_receipt=None,
        N8S_structural_rule_and_fact_refs=None,
        forbidden_claims=[
            "Ghana numeric change or measured no-change",
            "measured zero from missing evidence",
            "N8E product or N9 installed historical context",
            "original weight/design comparability",
            "N8S structural interpretation",
        ],
    )
    return record


def ghana_null_checks():
    record = ghana_n03_state()
    numeric_fields = ("delta_proportion", "design_variance",
                      "design_standard_error", "confidence_or_compatibility_interval",
                      "inferential_classification")
    checks = {
        "state_is_hold": record["actual_result_state"] ==
        "HELD_UPSTREAM_EVIDENCE_AND_ISSUANCE",
        "all_numeric_result_fields_null": all(record[field] is None
                                              for field in numeric_fields),
        "both_wave_design_receipts_null": record["wave_sample_and_weight_design_receipts"] == [None, None],
        "both_wave_distributions_null": record["wave_five_category_weighted_distributions"] == [None, None],
        "ee12_null": record["positive_EE12_relation_and_snapshot"] is None,
        "n9_consumer_null": record["actual_N9_consumer_receipt"] is None,
        "n8s_not_requested": record["N8S_structural_rule_and_fact_refs"] is None,
        "five_categories_include_zero": record["substantive_valid_codes"] == [0, 1, 2, 3, 4],
        "zero_is_substantive_label": "0" in record["native_substantive_labels"],
        "refusal_codes_typed": (record["typed_special_codes"]["R5"]["refused"] == 998 and
                                record["typed_special_codes"]["R9"]["refused"] == 8),
    }
    return dict(record=record, checks=checks,
                all_null=all(checks[key] for key in checks
                             if key not in ("state_is_hold",)))
