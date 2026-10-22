"""Independent R00V-R2 requalification, successor to review 140c41d6."""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (
    DEFAULT_COMMIT, DEFAULT_ROOT, canonical_typed_identity,
    evaluate_r56_sourcefree_claim, load_pinned_policy,
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
            for key in ("denominator", "numerator", "proof_source",
                        "native_state", "substantive_cells"):
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


def decide(claim):
    return evaluate_r56_sourcefree_claim(
        claim, externally_pinned_policy=load_pinned_policy(
            DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1"))


def test_all_36_frozen_cases_independent_pin():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    blobs, _, canonical_ops = independent_policy()
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


def test_valid_subsets_order_and_typed_identity():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    ops = [copy.deepcopy(dict(r)) for r in handle.expected_operations]
    for count in (1, 5, 17):
        claim = baseline_claim()
        claim["submitted"] = {"claims_scope_is_full_universe": False,
                              "operation_objects": ops[:count]}
        assert decide(claim)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    claim = baseline_claim()
    claim["submitted"]["operation_objects"] = list(reversed(ops))
    assert decide(claim)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    assert canonical_typed_identity(True) != canonical_typed_identity(1)
    assert canonical_typed_identity(None) != canonical_typed_identity({})
    assert canonical_typed_identity([1, 2]) != canonical_typed_identity([2, 1])


def test_d1_executed_native_without_evidence_holds():
    claim = baseline_claim()
    claim["request"]["claim_kind"] = "EXECUTED_NATIVE"
    assert decide(claim)["decision"] == "HOLD_TRUSTED_NATIVE"


def test_d2_supported_status_without_native_evidence_holds():
    claim = baseline_claim()
    op = claim["submitted"]["operation_objects"][0]
    claim["submitted"]["operation_status_edits"] = [{
        "operation_id": op["operation_id"], "execution": "COMPLETED",
        "result": "SUPPORTED", "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    assert decide(claim)["decision"] == "HOLD_TRUSTED_NATIVE"


def test_d3_prohibited_completion_refuses():
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
    assert decide(claim)["decision"] == "REFUSE_STATUS"


def test_d4_semantic_mutation_not_masked_by_status_edit():
    claim = baseline_claim()
    op = claim["submitted"]["operation_objects"][0]
    op["direction_ref"] = "TEST:CHANGED"
    claim["submitted"]["operation_status_edits"] = [{
        "operation_id": op["operation_id"], "execution": "NOT_STARTED",
        "result": "UNKNOWN"}]
    assert decide(claim)["decision"] == "REFUSE_FRONTIER"


def test_d5_unknown_grade_and_kind_refuse():
    claim = baseline_claim()
    claim["request"]["claim_grade"] = "MADE_UP"
    assert decide(claim)["decision"] == "REFUSE_AUTHORITY"
    claim = baseline_claim()
    claim["request"]["claim_kind"] = "MADE_UP"
    assert decide(claim)["decision"] == "REFUSE_AUTHORITY"


def test_d6_duplicate_occurrence_objects_refuse():
    claim = baseline_claim()
    claim["submitted"]["occurrence_objects"] = [
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET",
         "administration": "ADMINISTERED"},
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET",
         "administration": "ADMINISTERED"}]
    assert decide(claim)["decision"] == "REFUSE_FRONTIER"


def test_d7_handle_contract_mismatch_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    bad = dataclasses.replace(handle, policy=dict(handle.policy,
                                                  contract_id="OTHER"))
    assert evaluate_r56_sourcefree_claim(baseline_claim(),
                                         externally_pinned_policy=bad)["decision"] == "REFUSE_PIN"


def test_d8_eligible_to_held_disposition_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = next(r for r in handle.expected_operations
              if r.get("axis_bindings", {}).get("eligibility") == "ELIGIBLE")
    claim["submitted"]["operation_disposition_edits"] = [{
        "operation_id": op["operation_id"], "to": "HELD"}]
    assert decide(claim)["decision"] == "REFUSE_STATUS"


def test_invalid_status_values_and_unknown_edit_ids_refuse():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    op = handle.expected_operations[0]
    for edit in (
        {"operation_id": op["operation_id"], "execution": "COMPLETED",
         "result": "MADEUP", "proof_source": "TEST_ONLY_HAND_DERIVED"},
        {"operation_id": op["operation_id"], "execution": "DONE",
         "result": "UNKNOWN"},
        {"operation_id": "OP.TEST.UNKNOWN", "execution": "COMPLETED",
         "result": "VALID_NULL"},
    ):
        claim = baseline_claim()
        claim["request"]["claim_kind"] = "POLICY_STATUS_CHECK_ONLY"
        claim["submitted"]["operation_status_edits"] = [edit]
        assert decide(claim)["decision"] == "REFUSE_STATUS"


def test_simultaneous_faults_cannot_hide_refusal():
    claim = baseline_claim()
    claim["submitted"]["operation_objects"][0]["measure_ref"] = "TEST:CHANGED"
    claim["request"]["claim_kind"] = "EXECUTED_NATIVE"
    claim["submitted"]["native"] = True
    assert decide(claim)["decision"] != "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_dependency_fault_and_fresh_cold_restore():
    helper = ROOT / "tests/universal_execution_oracle/r00v_r2_dependency_probe.py"
    env = {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(ROOT)}
    results = []
    for mode in ("baseline", "fault", "restore"):
        completed = subprocess.run([sys.executable, str(helper), mode],
                                   cwd=str(ROOT), env=env, text=True,
                                   capture_output=True, check=True)
        results.append(json.loads(completed.stdout.strip().splitlines()[-1]))
    assert results[0]["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    assert results[1]["decision"] == "REFUSE_FRONTIER"
    assert results[2]["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"


def test_valid_occurrence_transport_is_not_refused():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    occurrences = []
    for universe in handle.synthetic["test_universes"]:
        occurrences.extend(copy.deepcopy(universe["occurrences"]))
    claim = baseline_claim()
    claim["submitted"]["occurrence_objects"] = occurrences
    assert decide(claim)["decision"] == "ALLOW_LOCAL_POLICY_CONSISTENT"
    claim = baseline_claim()
    claim["submitted"]["occurrence_objects"] = occurrences[:-1] + [
        dict(occurrences[-1], item="SEMANTIC_MISMATCH")]
    assert decide(claim)["decision"] == "REFUSE_FRONTIER"
    claim = baseline_claim()
    claim["submitted"]["occurrence_objects"] = "NOT_A_LIST"
    assert decide(claim)["decision"] == "REFUSE_FRONTIER"


def test_unknown_submitted_kind_and_native_claim_refuse():
    claim = baseline_claim()
    claim["submitted"]["claim_kind"] = "MADE_UP"
    assert decide(claim)["decision"] == "REFUSE_AUTHORITY"
    claim = baseline_claim()
    claim["submitted"]["native_event_claim"] = "MADE_UP"
    assert decide(claim)["decision"] == "REFUSE_FORGED_EVIDENCE"


def test_semantic_mutation_not_masked_by_disposition_edit():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = baseline_claim()
    op = claim["submitted"]["operation_objects"][0]
    op["condition_tuple"] = [{"domain_version": "TEST:CHANGED",
                              "occurrence_ref": "a:q-azur:main",
                              "value": {"t": "integer", "v": "9"}}]
    claim["submitted"]["operation_disposition_edits"] = [{
        "operation_id": op["operation_id"], "to": "ELIGIBLE"}]
    assert decide(claim)["decision"] == "REFUSE_FRONTIER"


def test_handle_version_mismatch_refuses():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    bad = dataclasses.replace(handle, policy=dict(handle.policy,
                                                  spec_version="9.9.9"))
    assert evaluate_r56_sourcefree_claim(baseline_claim(),
                                         externally_pinned_policy=bad)["decision"] == "REFUSE_PIN"
