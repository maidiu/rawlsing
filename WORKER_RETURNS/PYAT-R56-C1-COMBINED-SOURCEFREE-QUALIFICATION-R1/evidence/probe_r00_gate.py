"""C1 R00 policy/claim-ceiling receipt on the combined tree.

Invokes the actual accepted gate on independently pinned policy objects. Does not
construct a verified-evidence handle and does not claim authenticated native
association. R08/R09 remain NOT_IMPLEMENTED/NOT_REACHED.
"""
import copy
import dataclasses
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (
    DEFAULT_COMMIT,
    DEFAULT_ROOT,
    evaluate_r56_sourcefree_claim,
    load_pinned_policy,
)


def claim(handle):
    return {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": [copy.deepcopy(dict(row))
                                            for row in handle.expected_operations]},
    }


def summarize(decision):
    return {
        "decision": decision["decision"],
        "grade_ceiling": decision["grade_ceiling"],
        "reason_rule_ids": decision["reason_rule_ids"],
        "missing": decision.get("submitted_id_diff", {}).get("missing"),
        "extra": decision.get("submitted_id_diff", {}).get("extra"),
    }


def main():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    base = claim(handle)
    out = {
        "policy_commit": DEFAULT_COMMIT,
        "policy_root": DEFAULT_ROOT,
        "variant_id": handle.variant_id,
        "verified": handle.verified,
        "policy_blobs": dict(handle.blobs),
        "positive_policy_only": summarize(
            evaluate_r56_sourcefree_claim(copy.deepcopy(base),
                                          externally_pinned_policy=handle)),
    }

    missing = copy.deepcopy(base)
    missing["submitted"]["operation_objects"] = missing["submitted"]["operation_objects"][:-1]
    out["missing_frontier"] = summarize(
        evaluate_r56_sourcefree_claim(missing, externally_pinned_policy=handle))

    altered = copy.deepcopy(base)
    altered["submitted"]["operation_objects"][0]["operation_id"] = "OP.TEST.SUBSTITUTED"
    out["altered_frontier"] = summarize(
        evaluate_r56_sourcefree_claim(altered, externally_pinned_policy=handle))

    native = copy.deepcopy(base)
    native["request"]["claim_kind"] = "EXECUTED_NATIVE"
    out["executed_native_without_r09"] = summarize(
        evaluate_r56_sourcefree_claim(native, externally_pinned_policy=handle))

    generic = copy.deepcopy(base)
    generic["request"]["claim_grade"] = "GENERIC_SOURCEFREE"
    out["generic_sourcefree"] = summarize(
        evaluate_r56_sourcefree_claim(generic, externally_pinned_policy=handle))

    marker = copy.deepcopy(base)
    marker["submitted"]["K_mutation"] = {"field": "value", "from": "a", "to": "b"}
    out["k_mutation_marker"] = summarize(
        evaluate_r56_sourcefree_claim(marker, externally_pinned_policy=handle))
    out["k_mutation_note"] = (
        "Policy conflict marker refusal; NOT native producer-consumer association "
        "verification. R08/R09 authenticated binding is NOT_IMPLEMENTED/NOT_REACHED.")

    supported = copy.deepcopy(base)
    op_id = supported["submitted"]["operation_objects"][0]["operation_id"]
    supported["submitted"]["operation_status_edits"] = [{
        "operation_id": op_id, "execution": "COMPLETED",
        "result": "SUPPORTED", "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    out["supported_state_without_native_evidence"] = summarize(
        evaluate_r56_sourcefree_claim(supported, externally_pinned_policy=handle))

    substituted_ops = [copy.deepcopy(dict(row)) for row in handle.expected_operations]
    substituted_ops[0]["operation_id"] = "OP.TEST.POLICY_SUBSTITUTION"
    substituted = dataclasses.replace(
        handle, expected_operations=tuple(substituted_ops),
        expected_ids=tuple(row["operation_id"] for row in substituted_ops))
    out["policy_substitution"] = summarize(
        evaluate_r56_sourcefree_claim(copy.deepcopy(base),
                                      externally_pinned_policy=substituted))
    restored = dataclasses.replace(handle)
    out["policy_restore"] = summarize(
        evaluate_r56_sourcefree_claim(copy.deepcopy(base),
                                      externally_pinned_policy=restored))
    out["verified_evidence_handle_used"] = False
    out["native_positive_gate_verdict_issued"] = False
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
