#!/usr/bin/env python3
"""
Bounded R2-03 oracle-control proof.

Purpose:
Show mechanically that:
1) a destructive respondent-linkage mutation can preserve per-question marginals;
2) both base and mutant can be internally self-consistent and have valid self-digests;
3) an identity-aware independent primitive comparator and joint evaluator still detect loss;
4) typed negative-state flattening and zero-incidence metadata deletion are likewise detectable.

This is a tiny proof-of-principle control, not the future production oracle.
It imports no Rawlsing/candidate code.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any


def canon(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha(obj: Any) -> str:
    return hashlib.sha256(canon(obj)).hexdigest()


BASE_EVENTS = [
    {"source": "S", "row": 0, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "A"},
    {"source": "S", "row": 0, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "X"},
    {"source": "S", "row": 1, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "A"},
    {"source": "S", "row": 1, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "X"},
    {"source": "S", "row": 2, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "B"},
    {"source": "S", "row": 2, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "Y"},
    {"source": "S", "row": 3, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "B"},
    {"source": "S", "row": 3, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "Y"},
]

# Destructive mutation: Q2 is reassigned across respondent rows.
# Q1 marginal remains A=2/B=2; Q2 remains X=2/Y=2.
# But row-level joint A&X changes from 2 to 1.
MUTANT_EVENTS = [
    {"source": "S", "row": 0, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "A"},
    {"source": "S", "row": 0, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "X"},
    {"source": "S", "row": 1, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "A"},
    {"source": "S", "row": 1, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "Y"},
    {"source": "S", "row": 2, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "B"},
    {"source": "S", "row": 2, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "X"},
    {"source": "S", "row": 3, "question": "Q1", "occ": 0, "state": "SUBSTANTIVE", "value": "B"},
    {"source": "S", "row": 3, "question": "Q2", "occ": 0, "state": "SUBSTANTIVE", "value": "Y"},
]


def self_seal(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Candidate-style internally valid self-manifest."""
    payload_digest = sha(events)
    return {
        "declared_event_count": len(events),
        "payload_sha256": payload_digest,
        "manifest_sha256": sha({
            "declared_event_count": len(events),
            "payload_sha256": payload_digest,
        }),
    }


def validate_self_seal(events: list[dict[str, Any]], seal: dict[str, Any]) -> bool:
    expected = self_seal(events)
    return expected == seal


def marginal_projection(events: list[dict[str, Any]]) -> list[tuple[str, str, int]]:
    counts = Counter((e["question"], e["value"]) for e in events)
    return sorted((q, v, n) for (q, v), n in counts.items())


def primitive_projection(events: list[dict[str, Any]]) -> list[tuple[Any, ...]]:
    return sorted(
        (
            e["source"],
            e["row"],
            e["question"],
            e["occ"],
            e["state"],
            e["value"],
        )
        for e in events
    )


def respondent_map(events: list[dict[str, Any]]) -> dict[int, dict[str, str]]:
    rows: dict[int, dict[str, str]] = {}
    for e in events:
        rows.setdefault(e["row"], {})[e["question"]] = e["value"]
    return rows


def joint_count(events: list[dict[str, Any]], q1: str, v1: str, q2: str, v2: str) -> int:
    rows = respondent_map(events)
    return sum(1 for answers in rows.values() if answers.get(q1) == v1 and answers.get(q2) == v2)


def negative_state_control() -> dict[str, Any]:
    base = [
        {"query": "Q", "case": "no_risk_authority", "state": "UNAVAILABLE_RISK_SET"},
        {"query": "Q", "case": "valid_empty", "state": "VALID_EMPTY"},
    ]
    mutant = [
        {"query": "Q", "case": "no_risk_authority", "state": "NO_DATA"},
        {"query": "Q", "case": "valid_empty", "state": "NO_DATA"},
    ]
    return {
        "base_digest": sha(base),
        "mutant_digest": sha(mutant),
        "detected": sha(base) != sha(mutant),
    }


def zero_incidence_metadata_control() -> dict[str, Any]:
    base = {
        "question": "Q_UNUSED_DECL",
        "missing_declarations": [{"kind": "USER_MISSING_VALUE", "value": -1}],
        "observed_matching_incidence": 0,
    }
    mutant = {
        "question": "Q_UNUSED_DECL",
        "missing_declarations": [],
        "observed_matching_incidence": 0,
    }
    return {
        "same_incidence": base["observed_matching_incidence"] == mutant["observed_matching_incidence"],
        "base_digest": sha(base),
        "mutant_digest": sha(mutant),
        "detected": sha(base) != sha(mutant),
    }


def main() -> int:
    base_seal = self_seal(BASE_EVENTS)
    mutant_seal = self_seal(MUTANT_EVENTS)

    base_marginals = marginal_projection(BASE_EVENTS)
    mutant_marginals = marginal_projection(MUTANT_EVENTS)

    base_primitive = primitive_projection(BASE_EVENTS)
    mutant_primitive = primitive_projection(MUTANT_EVENTS)

    base_joint = joint_count(BASE_EVENTS, "Q1", "A", "Q2", "X")
    mutant_joint = joint_count(MUTANT_EVENTS, "Q1", "A", "Q2", "X")

    negative = negative_state_control()
    zero_incidence = zero_incidence_metadata_control()

    assertions = {
        "base_self_seal_valid": validate_self_seal(BASE_EVENTS, base_seal),
        "mutant_self_seal_valid": validate_self_seal(MUTANT_EVENTS, mutant_seal),
        "candidate_self_digests_are_distinct_but_each_internally_valid": (
            base_seal["payload_sha256"] != mutant_seal["payload_sha256"]
        ),
        "marginals_equal": base_marginals == mutant_marginals,
        "marginal_digest_equal": sha(base_marginals) == sha(mutant_marginals),
        "primitive_identity_detects_mutation": base_primitive != mutant_primitive,
        "primitive_digest_detects_mutation": sha(base_primitive) != sha(mutant_primitive),
        "joint_truth_detects_mutation": base_joint != mutant_joint,
        "expected_base_joint_A_X_is_2": base_joint == 2,
        "expected_mutant_joint_A_X_is_1": mutant_joint == 1,
        "negative_state_flattening_detected": negative["detected"],
        "zero_incidence_metadata_loss_detected": zero_incidence["detected"],
        "zero_incidence_remains_zero_in_both": zero_incidence["same_incidence"],
    }

    pass_all = all(assertions.values())

    receipt = {
        "schema": "R2_03_ORACLE_CONTROL_PROOF@1",
        "purpose": "Demonstrate aggregate parity and self-consistency do not prove identity-preserving semantic equivalence.",
        "imports_rawlsing_or_candidate_code": False,
        "base": {
            "self_seal": base_seal,
            "marginals": base_marginals,
            "marginal_digest": sha(base_marginals),
            "primitive_digest": sha(base_primitive),
            "joint_Q1_A_Q2_X": base_joint,
        },
        "mutant": {
            "self_seal": mutant_seal,
            "marginals": mutant_marginals,
            "marginal_digest": sha(mutant_marginals),
            "primitive_digest": sha(mutant_primitive),
            "joint_Q1_A_Q2_X": mutant_joint,
        },
        "negative_state_control": negative,
        "zero_incidence_metadata_control": zero_incidence,
        "assertions": assertions,
        "result": "PASS" if pass_all else "FAIL",
    }

    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if pass_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
