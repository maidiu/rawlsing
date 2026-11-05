"""Unified S41/S42 event-keyed reader for the ongoing consumer."""
from __future__ import annotations

from typing import Any

from .bootstrap import install

install()

import s41.reader as s41_reader  # noqa: E402
from s41.bindings import binding_episodes as s41_binding_episodes  # noqa: E402
from s41.history import (  # noqa: E402
    S41HistoryRefusal,
    validate_generation_readset,
    validate_history_source,
)

from .bindings import BINDING_SCHEMA, binding_episodes  # noqa: E402


class S42ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _all_bindings(session) -> list[dict]:
    rows = list(s41_binding_episodes(session)) + list(binding_episodes(session))
    rows.sort(key=lambda item: (item.get("event_ordinal", 0), item.get("event_time", 0)))
    return rows


def _find_binding(bindings: list[dict], event_ref: str) -> dict | None:
    return next(
        (
            row for row in bindings
            if row.get("e1_event_id") == event_ref
            or row.get("e1_event_hash") == event_ref
        ),
        None,
    )


_PREDECESSOR_KEYS = (
    "event_ordinal", "e1_event_id", "e1_event_hash",
    "c8_occurrence_id", "c8_content_hash", "event_time",
    "actor_id", "branch_id",
)


def _validate_predecessor(session, binding: dict, bindings: list[dict],
                          c8_event: dict) -> None:
    if int(binding.get("event_ordinal", 0)) <= 1:
        raise S42ReadRefusal("S42_PREDECESSOR_ORDINAL_INVALID")
    index = next(
        (
            i for i, row in enumerate(bindings)
            if row.get("e1_event_id") == binding.get("e1_event_id")
            and row.get("event_ordinal") == binding.get("event_ordinal")
        ),
        None,
    )
    if index is None or index == 0:
        raise S42ReadRefusal("S42_PREDECESSOR_BINDING_MISSING")
    actual = bindings[index - 1]
    predecessor = binding.get("predecessor")
    if not isinstance(predecessor, dict):
        raise S42ReadRefusal("S42_PREDECESSOR_BINDING_MISSING")
    actual_values = {
        "event_ordinal": actual.get("event_ordinal"),
        "e1_event_id": actual.get("e1_event_id"),
        "e1_event_hash": actual.get("e1_event_hash"),
        "c8_occurrence_id": actual["c8"].get("occurrence_id"),
        "c8_content_hash": actual["c8"].get("c8_content_hash", ""),
        "event_time": actual.get("event_time"),
        "actor_id": actual.get("actor_id"),
        "branch_id": actual.get("branch_id"),
    }
    for key in _PREDECESSOR_KEYS:
        if predecessor.get(key) != actual_values[key]:
            raise S42ReadRefusal("S42_PREDECESSOR_BINDING_MISMATCH", key)
    if int(actual.get("event_ordinal", 0)) != int(binding.get("event_ordinal", 0)) - 1:
        raise S42ReadRefusal("S42_PREDECESSOR_ORDER_INVALID")
    if int(actual.get("event_time", 0)) >= int(binding.get("event_time", 0)):
        raise S42ReadRefusal("S42_PREDECESSOR_TIME_INVALID")
    continuation = (c8_event.get("payload") or {}).get("s42_continuation")
    if not isinstance(continuation, dict):
        raise S42ReadRefusal("S42_C8_PREDECESSOR_FIELDS_MISSING")
    expected = {
        "event_ordinal": binding.get("event_ordinal"),
        "predecessor_e1_ref": actual.get("e1_event_id"),
        "predecessor_e1_event_hash": actual.get("e1_event_hash"),
        "predecessor_c8_occurrence_id": actual["c8"].get("occurrence_id"),
        "predecessor_c8_content_hash": actual["c8"].get("c8_content_hash", ""),
        "predecessor_event_time": actual.get("event_time"),
        "predecessor_actor_id": actual.get("actor_id"),
        "predecessor_branch_id": actual.get("branch_id"),
    }
    for key, value in expected.items():
        if continuation.get(key) != value:
            raise S42ReadRefusal("S42_C8_PREDECESSOR_MISMATCH", key)


def validate_predecessor_chain(session, bindings: list[dict]) -> None:
    for binding in bindings:
        if binding.get("schema") != BINDING_SCHEMA:
            continue
        c8_event = s41_reader._read_c8(binding["c8"], binding["source"], binding)
        _validate_predecessor(session, binding, bindings, c8_event)


def _validate_histories(
    session, binding: dict, bindings: list[dict]
) -> list[dict]:
    refs = list(binding.get("history_refs") or [])
    sources = list(binding.get("history_sources") or [])
    if len(refs) != len(sources):
        raise S42ReadRefusal("S42_HISTORY_SOURCE_COUNT_MISMATCH")
    if len({row.get("e1_event_id") for row in refs}) != len(refs):
        raise S42ReadRefusal("S42_HISTORY_REF_DUPLICATE")
    last_ordinal = -1
    last_time = -1
    resolved = []
    for ref, source in zip(refs, sources):
        prior = _find_binding(bindings, ref.get("e1_event_id", ""))
        if prior is None or prior.get("e1_event_hash") != ref.get("e1_event_hash"):
            raise S42ReadRefusal("S42_HISTORY_PRIOR_MISSING")
        if prior.get("event_ordinal") >= binding.get("event_ordinal"):
            raise S42ReadRefusal("S42_HISTORY_ORDER_INVALID")
        if prior.get("event_time", 0) >= binding.get("event_time", 0):
            raise S42ReadRefusal("S42_HISTORY_CLOCK_INVALID")
        if prior.get("event_ordinal") <= last_ordinal or prior.get("event_time") <= last_time:
            raise S42ReadRefusal("S42_HISTORY_INPUT_OUT_OF_ORDER")
        last_ordinal = prior["event_ordinal"]
        last_time = prior["event_time"]
        if prior.get("branch_id") != binding.get("branch_id"):
            raise S42ReadRefusal("S42_HISTORY_BRANCH_MISMATCH")
        if prior.get("actor_id") != binding.get("actor_id"):
            raise S42ReadRefusal("S42_HISTORY_ACTOR_MISMATCH")
        if not isinstance(source, dict):
            raise S42ReadRefusal("S42_HISTORY_SOURCE_MISSING")
        try:
            validate_history_source(
                session, source, prior,
                branch_id=binding["branch_id"], as_of=binding["as_of"],
            )
        except S41HistoryRefusal as exc:
            raise S42ReadRefusal("S42_HISTORY_BINDING_INVALID", exc.code) from exc
        resolved.append((ref, source, prior))
    generation = binding.get("generation") or {}
    generation_sources = binding.get("generation_sources")
    if not generation_sources:
        raise S42ReadRefusal(
            "S42_GENERATION_READSET_INVALID", "S42_GENERATION_INPUT_SOURCES_MISSING"
        )
    declared = {source.get("source_ref") for _, source, _ in resolved}
    historical = [
        row for row in generation_sources
        if row.get("source_class") == "HISTORICAL_EPISODE"
    ]
    if {row.get("source_ref") for row in historical} != declared:
        raise S42ReadRefusal("S42_GENERATION_HISTORY_SET_MISMATCH")
    for _, source, _ in resolved:
        try:
            validate_generation_readset(generation, source, generation_sources)
        except S41HistoryRefusal as exc:
            raise S42ReadRefusal(
                "S42_GENERATION_READSET_INVALID", exc.code
            ) from exc
    return refs


def _read_s42_event(session, binding: dict, bindings: list[dict]) -> dict:
    if not s41_reader.valid(dict(binding)):
        raise S42ReadRefusal("S42_EVENT_BINDING_UNSEALED")
    if binding.get("schema") != BINDING_SCHEMA:
        raise S42ReadRefusal("S42_EVENT_BINDING_SCHEMA_MISMATCH")
    _validate_histories(session, binding, bindings)
    c8_event = s41_reader._read_c8(binding["c8"], binding["source"], binding)
    _validate_predecessor(session, binding, bindings, c8_event)
    generation = binding.get("generation")
    if not isinstance(generation, dict) or not s41_reader.valid(dict(generation)):
        raise S42ReadRefusal("S42_GENERATION_UNSEALED")
    if generation.get("hash") != binding.get("generation_hash"):
        raise S42ReadRefusal("S42_GENERATION_HASH_MISMATCH")
    status = binding.get("status")
    if status in {"OPEN", "REFUSED"}:
        if status == "OPEN" and generation.get("selection_status") == "UNIQUE_SELECTED":
            raise S42ReadRefusal("S42_OPEN_WITH_SELECTION")
        if binding.get("attempt") is not None or binding.get("s36") is not None:
            raise S42ReadRefusal("S42_OPEN_HAS_ATTEMPT")
        if binding.get("action") is not None:
            raise S42ReadRefusal("S42_OPEN_HAS_ACTION")
        return _base_read(binding, generation, status)
    attempt = binding.get("attempt")
    if not isinstance(attempt, dict) or not s41_reader.valid(dict(attempt)):
        raise S42ReadRefusal("S42_ATTEMPT_UNSEALED")
    if attempt.get("hash") != binding.get("attempt_hash"):
        raise S42ReadRefusal("S42_ATTEMPT_HASH_MISMATCH")
    if attempt.get("generation_receipt_hash") != generation.get("hash"):
        raise S42ReadRefusal("S42_ATTEMPT_GENERATION_LINK_MISMATCH")
    if attempt.get("option_id") != generation.get("selected_option"):
        raise S42ReadRefusal("S42_ATTEMPT_OPTION_MISMATCH")
    if attempt.get("actor_id") != binding.get("actor_id"):
        raise S42ReadRefusal("S42_ATTEMPT_ACTOR_MISMATCH")
    if binding.get("c9") is None:
        raise S42ReadRefusal("S42_C9_BINDING_MISSING")
    response, receipt, target_rows = s41_reader._read_c9(binding["c9"])
    if response.get("event_ref") != binding.get("e1_event_hash"):
        raise S42ReadRefusal("S42_C9_RESPONSE_EVENT_MISMATCH")
    if receipt.get("response_ref") != binding["c9"].get("response_ref"):
        raise S42ReadRefusal("S42_C9_RECEIPT_RESPONSE_MISMATCH")
    if receipt.get("event_ref") != binding.get("e1_event_hash"):
        raise S42ReadRefusal("S42_C9_RECEIPT_EVENT_MISMATCH")
    if receipt.get("target_branch") != "NO_CHANGE" or receipt.get("target_reason") != "NO_PROPOSAL":
        raise S42ReadRefusal("S42_C9_TARGET_NOT_NO_CHANGE")
    if target_rows != 0 or response.get("target_proposal_ref", "") != "":
        raise S42ReadRefusal("S42_C9_TARGET_PRESENT")
    s35 = response.get("s35_receipt")
    if not isinstance(s35, dict) or not s41_reader.valid(dict(s35)):
        raise S42ReadRefusal("S42_S35_RECEIPT_UNSEALED")
    if s35.get("event_ref") != binding.get("e1_event_hash"):
        raise S42ReadRefusal("S42_S35_EVENT_MISMATCH")
    if s35.get("target_proposals") != []:
        raise S42ReadRefusal("S42_S35_TARGET_PRESENT")
    expected_status = (
        "RESPONSE_COMMITTED"
        if s35.get("outcome") in {
            "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION", "OBSERVED_CURRENT_REFUSAL"
        }
        else "RESPONSE_EFFECTS_VALID_EMPTY"
    )
    if response.get("status") != expected_status:
        raise S42ReadRefusal("S42_C9_STATUS_OUTCOME_MISMATCH")
    if receipt.get("record_hash", "") or receipt.get("target_id", ""):
        raise S42ReadRefusal("S42_C9_TARGET_IDENTITY_PRESENT")
    action = binding.get("action") or {}
    performed = bool(attempt.get("performed"))
    language = None
    if performed:
        event = session.event(action.get("event_id", ""))
        if not event or event.get("hash") != action.get("event_hash"):
            raise S42ReadRefusal("S42_ACTION_EVENT_MISMATCH")
        if attempt.get("s36_response_kind") != (s35.get("response_kind") or ""):
            raise S42ReadRefusal("S42_ACTION_RESPONSE_KIND_MISMATCH")
        if action.get("event_kind") == "SPEECH":
            language = s41_reader._read_language(session, binding, event)
        elif action.get("event_kind") == "INSPECT":
            if binding.get("language") is not None:
                raise S42ReadRefusal("S42_NONVERBAL_HAS_LANGUAGE")
            language = {"status": "NONVERBAL"}
        else:
            raise S42ReadRefusal("S42_ACTION_EVENT_KIND_INVALID")
    else:
        if binding.get("language") is not None or action.get("event_id"):
            raise S42ReadRefusal("S42_DENIED_HAS_ACTION_OR_LANGUAGE")
        if s35.get("outcome") != "RECEIVABLE_NO_OBSERVED_UPTAKE":
            raise S42ReadRefusal("S42_DENIED_NOT_VALID_EMPTY")
    result = _base_read(binding, generation, "OK")
    result.update({
        "attempt_hash": attempt.get("hash"),
        "attempt_status": attempt.get("attempt_status"),
        "performed": performed,
        "action_event_id": action.get("event_id", ""),
        "action_event_hash": action.get("event_hash", ""),
        "action_event_kind": action.get("event_kind", ""),
        "language": language,
        "c9": {
            "response_ref": binding["c9"].get("response_ref"),
            "receipt_ref": binding["c9"].get("receipt_ref"),
            "outcome": s35.get("outcome"),
            "response_kind": s35.get("response_kind"),
            "target_branch": receipt.get("target_branch"),
            "target_reason": receipt.get("target_reason"),
            "target_proposals": s35.get("target_proposals"),
            "target_state_rows": target_rows,
            "target_id": receipt.get("target_id", ""),
        },
        "history_refs": binding.get("history_refs") or [],
        "history_predicates": [
            row.get("predicate") for row in binding.get("history_sources") or []
        ],
        "world_before": binding.get("world_before"),
        "world_after": binding.get("world_after"),
        "world_tools_remaining": (
            (binding.get("world_after") or {}).get("actor_state", {}).get("A", {}) or {}
        ).get("tools_remaining"),
        "world_clock_before": (binding.get("world_before") or {}).get("clock"),
        "world_clock_after": (binding.get("world_after") or {}).get("clock"),
        "actor_action_appended": performed,
        "target_proposals": [],
    })
    return result


def _base_read(binding: dict, generation: dict, status: str) -> dict:
    return {
        "schema": "SOROK_S42_EVENT_READ@1",
        "status": status,
        "event_ordinal": binding.get("event_ordinal"),
        "e1_event_id": binding.get("e1_event_id"),
        "e1_event_hash": binding.get("e1_event_hash"),
        "c8_occurrence_id": binding["c8"].get("occurrence_id"),
        "c8_state_digest": binding["c8"].get("c8_state_digest"),
        "c8_content_hash": binding["c8"].get("c8_content_hash"),
        "event_time": binding.get("event_time"),
        "as_of": binding.get("as_of"),
        "actor_id": binding.get("actor_id"),
        "branch_id": binding.get("branch_id"),
        "source_operation": binding.get("source", {}).get("b_operation"),
        "source_event_hash": binding.get("source", {}).get("b_event_hash"),
        "generation_status": generation.get("selection_status"),
        "selected_option": generation.get("selected_option"),
        "generation_hash": generation.get("hash"),
        "generation_source_refs": list(generation.get("source_refs") or []),
        "history_refs": binding.get("history_refs") or [],
        "target_proposals": [],
        "provenance": binding.get("provenance"),
    }


def read_event(session, event_ref: str) -> dict:
    bindings = _all_bindings(session)
    binding = _find_binding(bindings, event_ref)
    if binding is None:
        raise S42ReadRefusal("S42_EVENT_NOT_FOUND")
    if binding.get("schema") == BINDING_SCHEMA:
        return _read_s42_event(session, binding, bindings)
    return s41_reader.read_event(session, event_ref)


def read_all_events(session) -> list[dict]:
    bindings = _all_bindings(session)
    return [
        read_event(session, row["e1_event_id"])
        for row in bindings
    ]


def read_latest_event(session) -> dict:
    events = read_all_events(session)
    if not events:
        raise S42ReadRefusal("S42_NO_EVENTS")
    return events[-1]


__all__ = [
    "S42ReadRefusal",
    "read_all_events",
    "read_event",
    "read_latest_event",
    "validate_predecessor_chain",
]
