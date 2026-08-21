"""Independent bounded oracle controls for PRE553 R5 acceptance.

IMPORTANT: this module intentionally imports no R5 carrier/codec/seam/C11 code.
Expected truth is computed from independently declared source/C11 microfixtures.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Iterable, Mapping, Sequence


ORACLE_VERSION = "PRE553_R5_INDEPENDENT_BOUNDED_ORACLE@1.0.0"


def _canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def independent_hash(value: Any) -> str:
    return hashlib.sha256(_canon(value).encode("ascii")).hexdigest()


def hostile_microfixture() -> tuple[dict[str, Any], ...]:
    """Independent source/C11 truth with identity, topology, and negative-state sensitivity."""
    base = [
        {"event_id": "e1", "respondent": "r1", "question": "q1", "occurrence": 1,
         "raw": "YES", "state": "SUBSTANTIVE", "rank": None, "eligible": True},
        {"event_id": "e2", "respondent": "r1", "question": "q2", "occurrence": 1,
         "raw": -0.0, "state": "SUBSTANTIVE", "rank": 1, "eligible": True},
        {"event_id": "e3", "respondent": "r1", "question": "q2", "occurrence": 2,
         "raw": 2, "state": "SUBSTANTIVE", "rank": 2, "eligible": True},
        {"event_id": "e4", "respondent": "r2", "question": "q1", "occurrence": 1,
         "raw": "", "state": "REFUSAL", "rank": None, "eligible": True},
        {"event_id": "e5", "respondent": "r2", "question": "q2", "occurrence": 1,
         "raw": "A\u0000B", "state": "NOT_ASKED", "rank": None, "eligible": False},
        {"event_id": "e6", "respondent": "r3", "question": "q1", "occurrence": 1,
         "raw": "YES", "state": "DK", "rank": None, "eligible": True},
        {"event_id": "e7", "respondent": "r3", "question": "q2", "occurrence": 1,
         "raw": "é", "state": "SUBSTANTIVE", "rank": None, "eligible": True},
        {"event_id": "e8", "respondent": "r4", "question": "q1", "occurrence": 1,
         "raw": "NO", "state": "INAPPLICABLE", "rank": None, "eligible": False},
    ]
    for item in base:
        projection = {k: item[k] for k in ("event_id", "respondent", "question", "occurrence", "raw", "state", "rank", "eligible")}
        # JSON does not distinguish -0.0 textually under all encoders, so the independent
        # fixture carries a specific signed-zero observation for oracle equality.
        if isinstance(item["raw"], float) and item["raw"] == 0.0:
            projection["raw_float_bits"] = "8000000000000000"
        item["content_hash"] = independent_hash(projection)
    return tuple(base)


def canonical_observation(event: Mapping[str, Any]) -> Mapping[str, Any]:
    projection = {k: event.get(k) for k in ("event_id", "respondent", "question", "occurrence", "raw", "state", "rank", "eligible")}
    if isinstance(event.get("raw"), float) and event.get("raw") == 0.0:
        import struct
        projection["raw_float_bits"] = struct.pack(">d", event["raw"]).hex()
    return projection


def observation_multiset(events: Iterable[Mapping[str, Any]]) -> tuple[str, ...]:
    return tuple(sorted(_canon(canonical_observation(event)) for event in events))


def exact_equal(expected: Iterable[Mapping[str, Any]], observed: Iterable[Mapping[str, Any]]) -> bool:
    return observation_multiset(expected) == observation_multiset(observed)


def independent_query(events: Sequence[Mapping[str, Any]], *, question: str,
                      state: str | None = None, require_eligible: bool = True) -> Mapping[str, Any]:
    governed = {e["respondent"] for e in events if (e["eligible"] or not require_eligible)}
    selected = [e for e in events if e["question"] == question and e["respondent"] in governed
                and (state is None or e["state"] == state)]
    return {
        "governed_respondents": tuple(sorted(governed)),
        "matching_event_ids": tuple(sorted(e["event_id"] for e in selected)),
        "matching_respondents": tuple(sorted({e["respondent"] for e in selected})),
        "event_count": len(selected),
    }


def mutate_aggregate_preserving_respondent_permutation(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = deepcopy(list(events)); mapping = {"r1": "r2", "r2": "r1", "r3": "r4", "r4": "r3"}
    for event in result:
        event["respondent"] = mapping[event["respondent"]]
    return result


def mutate_compensating_drop_duplicate(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = deepcopy(list(events))
    result.pop(0)
    dup = deepcopy(result[0]); dup["event_id"] = "e2b"; result.append(dup)
    return result


def mutate_one_field_omission(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = deepcopy(list(events)); result[0].pop("eligible", None); return result


def mutate_negative_state_flatten(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = deepcopy(list(events))
    for event in result:
        if event["state"] in {"REFUSAL", "NOT_ASKED", "DK", "INAPPLICABLE"}:
            event["state"] = "MISSING"
    return result


def mutate_self_consistent_destructive_rehash(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    result = deepcopy(list(events)); result[0]["raw"] = "NO"
    for event in result:
        event["content_hash"] = independent_hash(canonical_observation(event))
    return result


def benign_physical_relayout(events: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return list(reversed(deepcopy(list(events))))


def control_results() -> Mapping[str, bool]:
    expected = hostile_microfixture()
    destructive = {
        "aggregate_preserving_respondent_permutation": mutate_aggregate_preserving_respondent_permutation(expected),
        "compensating_event_drop_duplicate": mutate_compensating_drop_duplicate(expected),
        "one_field_omission": mutate_one_field_omission(expected),
        "negative_state_flattening": mutate_negative_state_flatten(expected),
        "self_consistent_destructive_rehash": mutate_self_consistent_destructive_rehash(expected),
    }
    result = {name: not exact_equal(expected, mutant) for name, mutant in destructive.items()}
    result["benign_physical_relayout"] = exact_equal(expected, benign_physical_relayout(expected))
    return result


__all__ = [
    "ORACLE_VERSION", "hostile_microfixture", "canonical_observation", "observation_multiset",
    "exact_equal", "independent_query", "mutate_aggregate_preserving_respondent_permutation",
    "mutate_compensating_drop_duplicate", "mutate_one_field_omission", "mutate_negative_state_flatten",
    "mutate_self_consistent_destructive_rehash", "benign_physical_relayout", "control_results",
]
