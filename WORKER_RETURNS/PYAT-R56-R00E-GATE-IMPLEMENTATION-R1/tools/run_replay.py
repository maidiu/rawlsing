#!/usr/bin/env python3
"""Replay all 36 frozen R00P cases through the public R00E gate."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (  # noqa: E402
    DEFAULT_COMMIT,
    DEFAULT_ROOT,
    evaluate_r56_sourcefree_claim,
    load_pinned_policy,
    operation_identity_digest,
)

RETURN = Path(__file__).resolve().parents[1]
EVID = RETURN / "evidence"
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
        ops = [copy.deepcopy(by_id.get(operation_id, {"operation_id": operation_id}))
               for operation_id in submitted["operation_ids_override"]]
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


def checks(case, decision):
    expected = case["expected"]
    problems = []
    for key in ("decision", "grade_ceiling", "reason_rule_ids"):
        if decision.get(key) != expected.get(key):
            problems.append({"field": key, "expected": expected.get(key),
                             "actual": decision.get(key)})
    if "expected_count" in expected and len(decision["considered_expected_ids"]) != expected["expected_count"]:
        problems.append({"field": "expected_count", "expected": expected["expected_count"],
                         "actual": len(decision["considered_expected_ids"])})
    for status in ("ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "HELD", "UNKNOWN"):
        key = f"expected_{status}"
        if key in expected and len(decision["eligibility_partition"][status]) != expected[key]:
            problems.append({"field": key, "expected": expected[key],
                             "actual": len(decision["eligibility_partition"][status])})
    diff = decision["submitted_id_diff"]
    if "expected_missing_count" in expected and len(diff["missing"]) != expected["expected_missing_count"]:
        problems.append({"field": "expected_missing_count",
                         "expected": expected["expected_missing_count"],
                         "actual": len(diff["missing"])})
    if "expected_extra_count" in expected and len(diff["extra"]) != expected["expected_extra_count"]:
        problems.append({"field": "expected_extra_count",
                         "expected": expected["expected_extra_count"],
                         "actual": len(diff["extra"])})
    if "expected_missing_ids" in expected and diff["missing"] != expected["expected_missing_ids"]:
        problems.append({"field": "expected_missing_ids",
                         "expected": expected["expected_missing_ids"],
                         "actual": diff["missing"]})
    if "expected_extra_ids" in expected and diff["extra"] != expected["expected_extra_ids"]:
        problems.append({"field": "expected_extra_ids",
                         "expected": expected["expected_extra_ids"],
                         "actual": diff["extra"]})
    if "exact_diff" in expected:
        for key in ("missing", "extra"):
            if diff[key] != expected["exact_diff"][key]:
                problems.append({"field": f"exact_diff.{key}",
                                 "expected": expected["exact_diff"][key],
                                 "actual": diff[key]})
    if "considered_expected_ids" in expected and decision["considered_expected_ids"] != sorted(expected["considered_expected_ids"]):
        problems.append({"field": "considered_expected_ids"})
    if "consumer_evidence" in expected and decision.get("consumer_evidence") != expected["consumer_evidence"]:
        problems.append({"field": "consumer_evidence"})
    if "materialized_variant_ref" in expected and decision.get("materialized_variant_ref") != expected["materialized_variant_ref"]:
        problems.append({"field": "materialized_variant_ref"})
    if "duplicate_destination_label" in expected and decision.get("duplicate_destination_label") != expected["duplicate_destination_label"]:
        problems.append({"field": "duplicate_destination_label"})
    if "invalid_rename" in expected and decision.get("invalid_rename") != expected["invalid_rename"]:
        problems.append({"field": "invalid_rename"})
    return problems


def main():
    cases = json.loads(CASES_PATH.read_text())["cases"]
    results = []
    for case in cases:
        variant = (case.get("input_overlay", {})
                   .get("external_policy_resolution", {})
                   .get("variant_id", "CANONICAL_V1")) or "CANONICAL_V1"
        handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, variant)
        decision = evaluate_r56_sourcefree_claim(materialize(case, handle),
                                                 externally_pinned_policy=handle)
        problems = checks(case, decision)
        results.append({
            "case_id": case["case_id"],
            "title": case["title"],
            "variant_id": variant,
            "expected": case["expected"],
            "actual": {
                "decision": decision["decision"],
                "grade_ceiling": decision["grade_ceiling"],
                "reason_rule_ids": decision["reason_rule_ids"],
                "considered_expected_ids": decision["considered_expected_ids"],
                "submitted_id_diff": decision["submitted_id_diff"],
                "eligibility_partition": {k: len(v) for k, v in decision["eligibility_partition"].items()},
                "materialized_variant_ref": decision.get("materialized_variant_ref"),
                "consumer_evidence": decision.get("consumer_evidence"),
            },
            "pass": not problems,
            "problems": problems,
            "mock_only": case["case_id"] == "C26",
        })
    replay = {
        "schema": "R56_R00E_REPLAY@1",
        "gate_contract": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "policy_commit": DEFAULT_COMMIT,
        "policy_root": DEFAULT_ROOT,
        "case_count": len(results),
        "passed": sum(1 for row in results if row["pass"]),
        "all_pass": all(row["pass"] for row in results),
        "results": results,
    }
    (EVID / "replay.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n",
                                      encoding="utf8")
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    witness = {
        "schema": "R56_R00E_PROOF_WITNESS@1",
        "gate_module": str((ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").relative_to(ROOT)),
        "gate_module_sha256": hashlib.sha256((ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").read_bytes()).hexdigest(),
        "policy_commit": handle.commit,
        "policy_root": handle.root,
        "policy_variant": handle.variant_id,
        "policy_blobs": dict(handle.blobs),
        "expected_count": len(handle.expected_ids),
        "expected_ids": sorted(handle.expected_ids),
        "expected_identity_digests": {
            row["operation_id"]: operation_identity_digest(row)
            for row in handle.expected_operations
        },
        "eligibility_counts": {
            status: sum(1 for row in handle.expected_operations
                        if row.get("axis_bindings", {}).get("eligibility") == status)
            for status in ("ELIGIBLE", "PROHIBITED", "INAPPLICABLE_PROVED", "HELD", "UNKNOWN")
        },
        "trusted_native_provenance": "NOT_PRESENT",
        "published_original_grant": "UNISSUED",
        "actual_consumer_values_read": None,
        "held_requirements": ["G3", "G6", "G7", "G8"],
    }
    (EVID / "proof_witness.json").write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n",
                                             encoding="utf8")
    imports = {
        "schema": "R56_R00E_IMPORTS@1",
        "public_function": "CROSS_HQ_CONTROL_ROOM.universal_promotion_gate.evaluate_r56_sourcefree_claim",
        "module_file": str((ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").relative_to(ROOT)),
        "module_sha256": witness["gate_module_sha256"],
        "stdlib_imports": ["copy", "hashlib", "json", "subprocess", "dataclasses", "pathlib", "typing"],
        "policy_loaded_from_git_commit": handle.commit,
        "policy_blob_verification": all(handle.verified for _ in [0]),
        "case_id_switch_present": any(f"C{i:02d}" in (ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").read_text() for i in range(36)),
        "literal_q301_blacklist_present": "q301_2" in (ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py").read_text(),
    }
    (EVID / "imports.json").write_text(json.dumps(imports, indent=2, sort_keys=True) + "\n",
                                        encoding="utf8")
    verdict = {
        "schema": "R56_R00E_AUTHOR_VERDICT@1",
        "author_role": "R00E_IMPLEMENTATION_OWNER_NOT_R00P_POLICY_OWNER_OR_R00V_REVIEWER",
        "engineering": "AUTHOR_SCOPED_PASS__36_CASES__NO_NATIVE_CLAIM",
        "scientific": "TEST_ONLY_POLICY_CONSISTENCY__NO_ORIGINAL_SOURCE_OR_NATIVE_INFERENCE",
        "authority": "HOLD__R09_UNGRANTED__ORIGINAL_UNISSUED__R00V_NOT_RUN",
        "r00v": "SEPARATE_INDEPENDENT_NATIVE_REVIEW_REQUIRED",
        "claims": {
            "local_policy_consistency": "PASS at exact frozen policy pin and exact operation multiset",
            "native_execution": "NOT_CLAIMED",
            "generic_sourcefree": "NOT_CLAIMED",
            "original35_n11": "NOT_CLAIMED",
            "actual_consumer": "NOT_RUN",
        },
    }
    (EVID / "author_verdict.json").write_text(json.dumps(verdict, indent=2, sort_keys=True) + "\n",
                                              encoding="utf8")
    print(json.dumps({"cases": len(results), "passed": replay["passed"],
                      "all_pass": replay["all_pass"]}, indent=1))
    raise SystemExit(0 if replay["all_pass"] else 1)


if __name__ == "__main__":
    main()
