from __future__ import annotations

import copy
import dataclasses
import hashlib
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
POLICY_FILES = ("CONTRACT.md", "policy.json", "synthetic_universes.json",
                "decision_cases.json", "freeze.json")


def git_bytes(path):
    return subprocess.check_output(
        ["git", "-c", "gc.auto=0", "show", f"{DEFAULT_COMMIT}:{path}"],
        cwd=str(ROOT), text=False)


def blob(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def independent_policy(variant="CANONICAL_V1"):
    raw = {name: git_bytes(f"{DEFAULT_ROOT}/{name}") for name in POLICY_FILES}
    blobs = {name: blob(data) for name, data in raw.items()}
    freeze = json.loads(raw["freeze.json"])
    expected = {row["path"].rsplit("/", 1)[-1]: row["git_blob_sha1"]
                for row in freeze["successor_content_blobs"]}
    assert all(blobs[name] == expected[name] for name in expected)
    synthetic = json.loads(raw["synthetic_universes.json"])
    if variant == "CANONICAL_V1":
        ops = synthetic["expected_operations"]
    else:
        ops = next(row for row in synthetic["independent_materialized_variants"]
                   if row["variant_id"] == variant)["expected_operations"]
    return blobs, synthetic, copy.deepcopy(ops)


def merge(base, overlay):
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def materialize(case, ops):
    claim = merge(json.loads(CASES_PATH.read_text())["baseline_input"],
                  case.get("input_overlay", {}))
    submitted = claim.setdefault("submitted", {})
    by_id = {row["operation_id"]: row for row in ops}
    if "operation_ids_override" in submitted:
        chosen = [copy.deepcopy(by_id.get(operation_id,
                                          {"operation_id": operation_id}))
                  for operation_id in submitted["operation_ids_override"]]
    else:
        chosen = copy.deepcopy(ops)
    for edit in submitted.get("operation_id_edits", []) or []:
        if edit.get("remove"):
            chosen = [row for row in chosen if row.get("operation_id") != edit["remove"]]
        if edit.get("add"):
            chosen.append({"operation_id": edit["add"]})
    for edit in submitted.get("operation_disposition_edits", []) or []:
        for row in chosen:
            if row.get("operation_id") == edit.get("operation_id"):
                row["eligible_disposition"] = edit.get("to")
                row.setdefault("axis_bindings", {})["eligibility"] = edit.get("to")
                if "native_evidence" in edit:
                    row["native_evidence"] = edit["native_evidence"]
    for edit in submitted.get("operation_status_edits", []) or []:
        for row in chosen:
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
    submitted["operation_objects"] = chosen
    return claim


def baseline_claim():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    return {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": [copy.deepcopy(dict(r))
                                            for r in handle.expected_operations]},
    }


def test_independent_pin_reproduces_all_36_cases():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    blobs, synthetic, canonical_ops = independent_policy()
    assert dict(handle.blobs) == blobs
    assert [dict(r) for r in handle.expected_operations] == canonical_ops
    cases = json.loads(CASES_PATH.read_text())["cases"]
    assert len(cases) == 36
    for case in cases:
        variant = (case.get("input_overlay", {})
                   .get("external_policy_resolution", {})
                   .get("variant_id", "CANONICAL_V1")) or "CANONICAL_V1"
        _, _, ops = independent_policy(variant)
        use_handle = handle if variant == "CANONICAL_V1" else load_pinned_policy(
            DEFAULT_COMMIT, DEFAULT_ROOT, variant)
        decision = evaluate_r56_sourcefree_claim(materialize(case, ops),
                                                 externally_pinned_policy=use_handle)
        expected = case["expected"]
        assert decision["decision"] == expected["decision"], case["case_id"]
        assert decision["grade_ceiling"] == expected["grade_ceiling"], case["case_id"]
        assert decision["reason_rule_ids"] == expected["reason_rule_ids"], case["case_id"]
        if "expected_count" in expected:
            assert len(decision["considered_expected_ids"]) == expected["expected_count"]
        if "expected_missing_count" in expected:
            assert len(decision["submitted_id_diff"]["missing"]) == expected["expected_missing_count"]
        if "expected_extra_count" in expected:
            assert len(decision["submitted_id_diff"]["extra"]) == expected["expected_extra_count"]
        if "expected_missing_ids" in expected:
            assert decision["submitted_id_diff"]["missing"] == expected["expected_missing_ids"]
        if "exact_diff" in expected:
            assert decision["submitted_id_diff"]["missing"] == expected["exact_diff"]["missing"]
            assert decision["submitted_id_diff"]["extra"] == expected["exact_diff"]["extra"]
        if "considered_expected_ids" in expected:
            assert decision["considered_expected_ids"] == sorted(expected["considered_expected_ids"])
        if "materialized_variant_ref" in expected:
            assert decision.get("materialized_variant_ref") == expected["materialized_variant_ref"]


def test_schema_conforming_subset_cardinality_and_order():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    ops = [copy.deepcopy(dict(r)) for r in handle.expected_operations]
    for count in (1, 5, 17):
        claim = baseline_claim()
        claim["submitted"] = {"claims_scope_is_full_universe": False,
                              "operation_objects": ops[:count]}
        assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    claim = baseline_claim()
    claim["submitted"]["operation_objects"] = list(reversed(ops))
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_opposite_controls_count_preserving_substitution_and_collision():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    ops = [copy.deepcopy(dict(r)) for r in handle.expected_operations]
    claim = baseline_claim()
    claim["submitted"]["operation_objects"] = ops[:-1] + [{"operation_id": "OP.TEST.REPLACEMENT"}]
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"
    claim = baseline_claim()
    claim["submitted"]["operation_objects"] = ops + [copy.deepcopy(ops[0])]
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"
    claim = baseline_claim()
    claim["submitted"]["candidate_supplied_rename"] = {"a": "same", "b": "same"}
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "REFUSE_FRONTIER"


def test_policy_dependency_fault_and_cold_restore():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    altered = [copy.deepcopy(dict(r)) for r in handle.expected_operations]
    altered[0]["operation_id"] = "OP.TEST.ALTERED"
    substitute = dataclasses.replace(handle, expected_operations=tuple(altered),
                                     expected_ids=tuple(r["operation_id"] for r in altered))
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=substitute)["decision"] == "REFUSE_FRONTIER"
    cold = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    assert evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=cold)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_typed_identity_distinguishes_bool_int_null_and_order():
    from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import canonical_typed_identity
    assert canonical_typed_identity(True) != canonical_typed_identity(1)
    assert canonical_typed_identity(None) != canonical_typed_identity({})
    assert canonical_typed_identity([1, 2]) != canonical_typed_identity([2, 1])
    assert canonical_typed_identity({"a": None}) != canonical_typed_identity({})


@pytest.mark.xfail(strict=True, reason="R00V defect: EXECUTED_NATIVE claim without evidence returns local ALLOW")
def test_executed_native_without_evidence_is_not_local_allow():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    claim["request"]["claim_kind"] = "EXECUTED_NATIVE"
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] in {"HOLD_TRUSTED_NATIVE", "REFUSE_FORGED_EVIDENCE", "REFUSE_AUTHORITY"}


@pytest.mark.xfail(strict=True, reason="R00V defect: completed SUPPORTED status edit without native evidence gets local ALLOW")
def test_supported_status_edit_without_native_evidence_is_not_local_allow():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = claim["submitted"]["operation_objects"][0]
    claim["submitted"]["operation_status_edits"] = [{
        "operation_id": op["operation_id"], "execution": "COMPLETED",
        "result": "SUPPORTED", "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] != "ALLOW_LOCAL_POLICY_CONSISTENT"


@pytest.mark.xfail(strict=True, reason="R00V defect: PROHIBITED operation can be completed as OBSERVED_ZERO")
def test_prohibited_operation_cannot_be_completed_observed_zero():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = next(r for r in handle.expected_operations
              if r.get("axis_bindings", {}).get("eligibility") == "PROHIBITED")
    claim["submitted"]["operation_status_edits"] = [{
        "operation_id": op["operation_id"], "eligibility": "ELIGIBLE",
        "execution": "COMPLETED", "result": "OBSERVED_ZERO",
        "denominator": {"t": "integer", "v": "8"},
        "numerator": {"t": "integer", "v": "0"},
        "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "REFUSE_STATUS"


@pytest.mark.xfail(strict=True, reason="R00V defect: status edit suppresses exact semantic mismatch")
def test_semantic_mutation_cannot_be_masked_by_status_edit():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = claim["submitted"]["operation_objects"][0]
    op["direction_ref"] = "TEST:CHANGED"
    claim["submitted"]["operation_status_edits"] = [{
        "operation_id": op["operation_id"], "execution": "NOT_STARTED",
        "result": "UNKNOWN"}]
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "REFUSE_FRONTIER"


@pytest.mark.xfail(strict=True, reason="R00V defect: unknown claim_grade is allowed as local")
def test_unknown_claim_grade_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    claim["request"]["claim_grade"] = "MADE_UP"
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] in {"REFUSE_AUTHORITY", "REFUSE_STATUS", "REFUSE_PIN"}


@pytest.mark.xfail(strict=True, reason="R00V defect: submitted occurrence_objects are ignored")
def test_duplicate_occurrence_objects_refuse():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    claim["submitted"]["occurrence_objects"] = [
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET",
         "administration": "ADMINISTERED"},
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET",
         "administration": "ADMINISTERED"},
    ]
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "REFUSE_FRONTIER"


@pytest.mark.xfail(strict=True, reason="R00V defect: handle contract identity is not checked")
def test_policy_contract_mismatch_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    bad = dataclasses.replace(handle, policy=dict(handle.policy,
                                                  contract_id="OTHER"))
    claim = baseline_claim()
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=bad)
    assert decision["decision"] in {"REFUSE_PIN", "REFUSE_IDENTITY"}


@pytest.mark.xfail(strict=True, reason="R00V defect: ELIGIBLE can be disposition-edited to HELD")
def test_eligible_to_held_disposition_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = next(r for r in handle.expected_operations
              if r.get("axis_bindings", {}).get("eligibility") == "ELIGIBLE")
    claim["submitted"]["operation_disposition_edits"] = [{
        "operation_id": op["operation_id"], "to": "HELD"}]
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    assert decision["decision"] == "REFUSE_STATUS"
