#!/usr/bin/env python3
"""R00E-R2 replay and defect regression matrix."""
from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())
RETURN = HERE.parents[1]
EVID = RETURN / "evidence"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/universal_execution_oracle"))

import test_r00e_r2_reviewer_regressions as T  # noqa: E402
from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (  # noqa: E402
    DEFAULT_COMMIT, DEFAULT_ROOT, evaluate_r56_sourcefree_claim,
    load_pinned_policy, operation_identity_digest,
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def case_check(case, decision):
    expected = case["expected"]
    issues = []
    for key in ("decision", "grade_ceiling", "reason_rule_ids"):
        if decision.get(key) != expected.get(key):
            issues.append({"field": key, "expected": expected.get(key),
                           "actual": decision.get(key)})
    if "expected_count" in expected and len(decision["considered_expected_ids"]) != expected["expected_count"]:
        issues.append({"field": "expected_count"})
    if "expected_missing_count" in expected and len(decision["submitted_id_diff"]["missing"]) != expected["expected_missing_count"]:
        issues.append({"field": "expected_missing_count"})
    if "expected_extra_count" in expected and len(decision["submitted_id_diff"]["extra"]) != expected["expected_extra_count"]:
        issues.append({"field": "expected_extra_count"})
    if "expected_missing_ids" in expected and decision["submitted_id_diff"]["missing"] != expected["expected_missing_ids"]:
        issues.append({"field": "expected_missing_ids"})
    if "exact_diff" in expected:
        for key in ("missing", "extra"):
            if decision["submitted_id_diff"][key] != expected["exact_diff"][key]:
                issues.append({"field": f"exact_diff.{key}"})
    if "considered_expected_ids" in expected and decision["considered_expected_ids"] != sorted(expected["considered_expected_ids"]):
        issues.append({"field": "considered_expected_ids"})
    if "materialized_variant_ref" in expected and decision.get("materialized_variant_ref") != expected["materialized_variant_ref"]:
        issues.append({"field": "materialized_variant_ref"})
    return issues


def main():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    blobs, synthetic, canonical_ops = T.independent_policy()
    cases = json.loads(T.CASES_PATH.read_text())["cases"]
    results = []
    for case in cases:
        variant = (case.get("input_overlay", {})
                   .get("external_policy_resolution", {})
                   .get("variant_id", "CANONICAL_V1")) or "CANONICAL_V1"
        _, _, ops = T.independent_policy(variant)
        use_handle = handle if variant == "CANONICAL_V1" else load_pinned_policy(
            DEFAULT_COMMIT, DEFAULT_ROOT, variant)
        decision = evaluate_r56_sourcefree_claim(T.materialize(case, ops),
                                                 externally_pinned_policy=use_handle)
        issues = case_check(case, decision)
        results.append({"case_id": case["case_id"], "variant_id": variant,
                        "decision": decision["decision"],
                        "ceiling": decision["grade_ceiling"],
                        "reasons": decision["reason_rule_ids"],
                        "missing": decision["submitted_id_diff"]["missing"],
                        "extra": decision["submitted_id_diff"]["extra"],
                        "pass": not issues, "issues": issues})
    replay = {"schema": "R56_R00E_R2_REPLAY@1",
              "candidate_parent": "efd12b1d46f1ccf90de14b292f600078f11ec7e0",
              "policy_commit": DEFAULT_COMMIT, "policy_root": DEFAULT_ROOT,
              "policy_blobs_independently_recomputed": blobs,
              "expected_count": len(canonical_ops), "case_count": len(results),
              "passed": sum(1 for row in results if row["pass"]),
              "all_pass": all(row["pass"] for row in results),
              "results": results}
    (EVID / "replay.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf8")

    baseline = T.baseline_claim()
    probes = []

    def probe(name, claim, secure):
        decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
        probes.append({"name": name, "actual": decision["decision"],
                       "reasons": decision["reason_rule_ids"],
                       "expected_secure": sorted(secure),
                       "pass": decision["decision"] in secure})

    c = copy.deepcopy(baseline); c["request"]["claim_kind"] = "EXECUTED_NATIVE"
    probe("executed_native_without_evidence", c,
          {"HOLD_TRUSTED_NATIVE", "REFUSE_FORGED_EVIDENCE", "REFUSE_AUTHORITY"})
    c = copy.deepcopy(baseline); op = c["submitted"]["operation_objects"][0]
    c["submitted"]["operation_status_edits"] = [{"operation_id": op["operation_id"],
        "execution": "COMPLETED", "result": "SUPPORTED",
        "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    probe("supported_status_without_native_evidence", c,
          {"HOLD_TRUSTED_NATIVE", "REFUSE_STATUS", "REFUSE_FORGED_EVIDENCE"})
    c = copy.deepcopy(baseline)
    prohibited = next(r for r in canonical_ops
                      if r.get("axis_bindings", {}).get("eligibility") == "PROHIBITED")
    c["submitted"]["operation_status_edits"] = [{"operation_id": prohibited["operation_id"],
        "eligibility": "ELIGIBLE", "execution": "COMPLETED",
        "result": "OBSERVED_ZERO", "denominator": {"t": "integer", "v": "8"},
        "numerator": {"t": "integer", "v": "0"},
        "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    probe("prohibited_completed_observed_zero", c, {"REFUSE_STATUS"})
    c = copy.deepcopy(baseline); c["submitted"]["operation_objects"][0]["direction_ref"] = "TEST:CHANGED"
    c["submitted"]["operation_status_edits"] = [{"operation_id": c["submitted"]["operation_objects"][0]["operation_id"],
        "execution": "NOT_STARTED", "result": "UNKNOWN"}]
    probe("semantic_mutation_masked_by_status_edit", c, {"REFUSE_FRONTIER"})
    c = copy.deepcopy(baseline); c["request"]["claim_grade"] = "MADE_UP"
    probe("unknown_claim_grade", c, {"REFUSE_AUTHORITY", "REFUSE_STATUS", "REFUSE_PIN"})
    c = copy.deepcopy(baseline); c["submitted"]["occurrence_objects"] = [
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET", "administration": "ADMINISTERED"},
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET", "administration": "ADMINISTERED"}]
    probe("duplicate_occurrence_objects", c, {"REFUSE_FRONTIER"})
    bad = dataclasses.replace(handle, policy=dict(handle.policy, contract_id="OTHER"))
    decision = evaluate_r56_sourcefree_claim(baseline, externally_pinned_policy=bad)
    probes.append({"name": "policy_contract_mismatch", "actual": decision["decision"],
                   "reasons": decision["reason_rule_ids"],
                   "expected_secure": ["REFUSE_IDENTITY", "REFUSE_PIN"],
                   "pass": decision["decision"] in {"REFUSE_IDENTITY", "REFUSE_PIN"}})
    c = copy.deepcopy(baseline)
    eligible = next(r for r in canonical_ops
                    if r.get("axis_bindings", {}).get("eligibility") == "ELIGIBLE")
    c["submitted"]["operation_disposition_edits"] = [{"operation_id": eligible["operation_id"],
                                                       "to": "HELD"}]
    probe("eligible_to_held_disposition", c, {"REFUSE_STATUS"})
    matrix = {"schema": "R56_R00E_R2_DEFECT_MATRIX@1",
              "source_reviewer_commit": "140c41d6a10a595ff5d80de4eb855bcd65e7a8f6",
              "probes": probes,
              "defect_count": len(probes),
              "passed": sum(1 for row in probes if row["pass"]),
              "all_repaired": all(row["pass"] for row in probes)}
    (EVID / "defect_matrix.json").write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf8")
    pin = {"schema": "R56_R00E_R2_POLICY_PIN@1",
           "commit": DEFAULT_COMMIT, "root": DEFAULT_ROOT,
           "blobs": blobs, "expected_count": len(canonical_ops),
           "expected_ids": sorted(row["operation_id"] for row in canonical_ops),
           "expected_identity_digests": {row["operation_id"]: operation_identity_digest(row)
                                         for row in canonical_ops}}
    (EVID / "policy_pin.json").write_text(json.dumps(pin, indent=2, sort_keys=True) + "\n", encoding="utf8")
    gate_path = ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"
    source = gate_path.read_text()
    imports = {"schema": "R56_R00E_R2_IMPORTS@1",
               "public_function": "CROSS_HQ_CONTROL_ROOM.universal_promotion_gate.evaluate_r56_sourcefree_claim",
               "module_path": str(gate_path.relative_to(ROOT)),
               "module_sha256": sha(gate_path),
               "stdlib_imports": ["copy", "hashlib", "json", "subprocess",
                                  "dataclasses", "pathlib", "typing"],
               "policy_commit": DEFAULT_COMMIT,
               "policy_blobs_verified": all(blobs[name] == handle.blobs[name] for name in blobs),
               "case_id_switch_present": any(f"C{i:02d}" in source for i in range(36)),
               "literal_q301_blacklist_present": "q301_2" in source or "q301_7" in source,
               "fixed_18_decision_branch_present": "len(expected_ids) == 18" in source,
               "fixture_name_branch_present": "CLONE_A" in source or "OP.TEST" in source}
    (EVID / "imports.json").write_text(json.dumps(imports, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({"cases": len(results), "passed": replay["passed"],
                      "all_pass": replay["all_pass"],
                      "defects_repaired": matrix["passed"],
                      "all_repaired": matrix["all_repaired"],
                      "gate_sha256": imports["module_sha256"]}, indent=1))
    raise SystemExit(0 if replay["all_pass"] and matrix["all_repaired"] else 1)


if __name__ == "__main__":
    main()
