from __future__ import annotations

import copy
import dataclasses
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (  # noqa: E402
    DEFAULT_COMMIT,
    DEFAULT_ROOT,
    evaluate_r56_sourcefree_claim,
    load_pinned_policy,
)


def main(mode):
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    claim = {
        "contract_id": "R56-R00P-CLAIM-TRANSITION-GATE@1.1.0",
        "request": {"claim_grade": "LOCAL_OPERATOR", "claim_kind": "POLICY_ONLY"},
        "external_policy_resolution": {"variant_id": "CANONICAL_V1"},
        "submitted": {"operation_objects": [copy.deepcopy(dict(r))
                                            for r in handle.expected_operations]},
    }
    if mode == "fault":
        altered = [copy.deepcopy(dict(r)) for r in handle.expected_operations]
        altered[0]["operation_id"] = "OP.TEST.DEPENDENCY_FAULT"
        handle = dataclasses.replace(
            handle, expected_operations=tuple(altered),
            expected_ids=tuple(r["operation_id"] for r in altered))
    decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
    print(json.dumps({"mode": mode, "decision": decision["decision"],
                      "reasons": decision["reason_rule_ids"]}, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
