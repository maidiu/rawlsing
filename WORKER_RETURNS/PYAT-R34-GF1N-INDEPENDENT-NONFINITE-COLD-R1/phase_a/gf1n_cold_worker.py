"""GF1N cold-process witness: one native hostile shape per fresh OS process.

Usage: python3 -B gf1n_cold_worker.py <case>
Prints one strict-JSON line.  Two runs with different PYTHONHASHSEED must be
bit-identical in their non-PID content for accepted and refused cases.
"""
from __future__ import annotations

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gf1n_probe as P  # noqa: E402

INF = float("inf")
NINF = float("-inf")
NAN = float("nan")

CASES = {
    "native_positive": dict(role="none"),
    "finite_heterogeneous_condition": dict(role="condition", domain=(0, "0")),
    "finite_heterogeneous_target": dict(role="target", domain=(0.5, "0.5")),
    "nonfinite_plus_infinity_condition": dict(role="condition", domain=(INF, 1.0)),
    "nonfinite_minus_infinity_target": dict(role="target", domain=(NINF, 1.0)),
    "nonfinite_nan_condition": dict(role="condition", domain=(NAN, 1.0)),
    "signed_zero_target": dict(role="target", domain=(-0.0, 0.0)),
    "collision_int_string_condition": dict(role="condition", domain=(0, "0")),
    "support_exceeds_risk": dict(role="condition", domain=("0", "1"),
                                 counts={"00": 1, "11": 1}, eligible=1),
    "typed_missing_target": dict(role="none", typed_state="MISSING_TARGET_STATE", eligible=0),
    "observed_zero": dict(role="condition", domain=("0", "1"), counts={}, eligible=2,
                          zero_state="OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"),
}


def main() -> int:
    name = sys.argv[1]
    if name not in CASES:
        print(json.dumps({"error": "UNKNOWN_CASE", "case": name}))
        return 2
    got = P.assess(**CASES[name])
    payload = {
        "case": name,
        "outcome": got["outcome"],
        "error": got.get("error"),
        "strict_ok": got.get("strict_ok"),
        "strict_error": got.get("strict_error"),
        "contract_ok": got.get("contract_ok"),
        "deterministic": got.get("deterministic"),
        "result": got.get("result"),
        "strict": got.get("strict"),
        "relation_hash": got.get("relation_hash"),
        "relation_object_id": got.get("relation_object_id"),
        "python": sys.version.split()[0],
        "pid": os.getpid(),
    }
    try:
        line = json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except Exception as exc:  # noqa: BLE001 - non-strict result is itself the RED witness
        payload["NON_STRICT_RESULT"] = type(exc).__name__ + ":" + str(exc)
        line = json.dumps(payload, sort_keys=True, ensure_ascii=False, allow_nan=True)
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
