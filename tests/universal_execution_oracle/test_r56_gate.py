from __future__ import annotations

import copy
import dataclasses
import json
import subprocess
from pathlib import Path

import pytest

from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (
    DEFAULT_COMMIT,
    DEFAULT_ROOT,
    evaluate_r56_sourcefree_claim,
    load_pinned_policy,
)

ROOT = Path(__file__).resolve().parents[2]
CASES_PATH = ROOT / DEFAULT_ROOT / "decision_cases.json"


def deep_merge(base, overlay):
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def materialize(case, handle):
    merged = deep_merge(json.loads(CASES_PATH.read_text())["baseline_input"],
                        case.get("input_overlay", {}))
    submitted = merged.setdefault("submitted", {})
    expected = [copy.deepcopy(dict(row)) for row in handle.expected_operations]
    by_id = {row["operation_id"]: row for row in expected}
    if "operation_ids_override" in submitted:
        ops = []
        for operation_id in submitted["operation_ids_override"]:
            ops.append(copy.deepcopy(by_id.get(operation_id,
                                                {"operation_id": operation_id})))
    else:
        ops = expected
    for edit in submitted.get("operation_id_edits", []) or []:
        if edit.get("remove"):
            ops = [row for row in ops if row.get("operation_id") != edit["remove"]]
        if edit.get("add"):
            ops.append({"operation_id": edit["add"]})
    for edit in submitted.get("operation_disposition_edits", []) or []:
        for row in ops:
            if row.get("operation_id") == edit.get("operation_id"):
                row["eligible_disposition"] = edit.get("to")
                row.setdefault("axis_bindings", {})["eligibility"] = edit.get("to")
                if "native_evidence" in edit:
                    row["native_evidence"] = edit["native_evidence"]
    for edit in submitted.get("operation_status_edits", []) or []:
        for row in ops:
            if row.get("operation_id") != edit.get("operation_id"):
                continue
            axis = row.setdefault("axis_bindings", {})
            for key in ("eligibility", "execution", "result"):
                if key in edit:
                    axis[key] = edit[key]
            for key in ("denominator", "numerator", "proof_source", "native_state"):
                if key in edit:
                    row[key] = edit[key]
            if edit.get("assert_complete"):
                row["asserted_complete"] = True
    submitted["operation_objects"] = ops
    return merged


def assert_case(case, decision):
    expected = case["expected"]
    assert decision["decision"] == expected["decision"], case["case_id"]
    assert decision["grade_ceiling"] == expected["grade_ceiling"], case["case_id"]
    assert decision["reason_rule_ids"] == expected["reason_rule_ids"], case["case_id"]
    if "expected_count" in expected:
        assert len(decision["considered_expected_ids"]) == expected["expected_count"]
    for status in ("ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "HELD", "UNKNOWN"):
        key = f"expected_{status}"
        if key in expected:
            assert len(decision["eligibility_partition"][status]) == expected[key]
    if "expected_missing_count" in expected:
        assert len(decision["submitted_id_diff"]["missing"]) == expected["expected_missing_count"]
    if "expected_extra_count" in expected:
        assert len(decision["submitted_id_diff"]["extra"]) == expected["expected_extra_count"]
    if "expected_missing_ids" in expected:
        assert decision["submitted_id_diff"]["missing"] == expected["expected_missing_ids"]
    if "expected_extra_ids" in expected:
        assert decision["submitted_id_diff"]["extra"] == expected["expected_extra_ids"]
    if "exact_diff" in expected:
        for key in ("missing", "extra"):
            assert decision["submitted_id_diff"][key] == expected["exact_diff"][key]
    if "considered_expected_ids" in expected:
        assert decision["considered_expected_ids"] == sorted(expected["considered_expected_ids"])
    if "consumer_evidence" in expected:
        assert decision.get("consumer_evidence") == expected["consumer_evidence"]
    if "materialized_variant_ref" in expected:
        assert decision.get("materialized_variant_ref") == expected["materialized_variant_ref"]
    if "duplicate_destination_label" in expected:
        assert decision.get("duplicate_destination_label") == expected["duplicate_destination_label"]
    if "invalid_rename" in expected:
        assert decision.get("invalid_rename") == expected["invalid_rename"]


def test_all_36_independent_cases():
    cases = json.loads(CASES_PATH.read_text())["cases"]
    assert len(cases) == 36
    for case in cases:
        variant = (case.get("input_overlay", {})
                   .get("external_policy_resolution", {})
                   .get("variant_id", "CANONICAL_V1"))
        if variant is None:
            variant = "CANONICAL_V1"
        handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, variant)
        decision = evaluate_r56_sourcefree_claim(materialize(case, handle),
                                                 externally_pinned_policy=handle)
        assert_case(case, decision)


def test_independent_subset_and_order_not_case_named():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    ops = [copy.deepcopy(dict(row)) for row in handle.expected_operations]
    chosen = [ops[0], ops[7], ops[13]]
    claim = {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY",
                    "consumer": "TEST_ONLY_GATE_POLICY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"claims_scope_is_full_universe": False,
                      "operation_objects": chosen},
    }
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    claim["submitted"]["operation_objects"] = list(reversed(ops))
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_semantic_field_change_refused_and_restore():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    ops = [copy.deepcopy(dict(row)) for row in handle.expected_operations]
    claim = {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": ops},
    }
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    ops[3]["direction_ref"] = "TEST:CHANGED"
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"
    ops[3]["direction_ref"] = handle.expected_operations[3]["direction_ref"]
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_policy_dependency_substitution_and_cold_restore():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": [copy.deepcopy(dict(r)) for r in handle.expected_operations]},
    }
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    altered = list(handle.expected_operations)
    altered[0] = dict(altered[0])
    altered[0]["operation_id"] = "OP.TEST.SUBSTITUTED"
    substitute = dataclasses.replace(handle, expected_operations=tuple(altered),
                                     expected_ids=tuple(r["operation_id"] for r in altered))
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=substitute)["decision"] == "REFUSE_FRONTIER"
    restored = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=restored)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_no_case_id_or_label_blacklist_in_gate_source():
    text = (ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").read_text()
    for case_id in [f"C{i:02d}" for i in range(36)]:
        assert case_id not in text
    assert "q301_2" not in text and "q301_7" not in text
    assert "CANDIDATE_JSON_ONLY" not in text


def test_untrusted_handle_rejected():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = {"contract_id": "x", "request": {}, "submitted": {}}
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy={})
    assert decision["decision"] == "REFUSE_PIN"
    assert decision["reason_rule_ids"] == ["P00_INDEPENDENT_PIN"]
