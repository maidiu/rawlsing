"""Canonical prior-history binding for the S41 continuation source."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from candidate import valid  # noqa: E402
from s39.sources import CONTEXT_KINDS, validate_source  # noqa: E402

CANONICAL_PREFIX = "TEST_ONLY_S41_HIST_"


class S41HistoryRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def canonical_source_ref(prior: Mapping[str, Any]) -> str:
    return CANONICAL_PREFIX + str(prior.get("e1_event_id", ""))


def validate_history_source(
    session,
    history: Mapping[str, Any],
    prior: Mapping[str, Any],
    *,
    branch_id: str,
    as_of: int,
) -> dict:
    """Bind a history record to the actual earlier admitted C8/E1/source/access."""
    if not isinstance(history, Mapping) or not valid(dict(history)):
        raise S41HistoryRefusal("S41_HISTORY_UNSEALED")
    history = dict(history)
    if history.get("source_ref") != canonical_source_ref(prior):
        raise S41HistoryRefusal("S41_HISTORY_SOURCE_REF_NOT_CANONICAL")
    try:
        validate_source(
            history,
            actor_id=str(prior.get("actor_id", "")),
            branch_id=branch_id,
            as_of=as_of,
        )
    except ValueError as exc:
        raise S41HistoryRefusal("S41_HISTORY_SOURCE_INVALID", str(exc)) from exc
    if history.get("actor_id") != prior.get("actor_id"):
        raise S41HistoryRefusal("S41_HISTORY_ACTOR_MISMATCH")
    if history.get("branch_id") != prior.get("branch_id"):
        raise S41HistoryRefusal("S41_HISTORY_BRANCH_MISMATCH")

    c8 = prior.get("c8") or {}
    source = prior.get("source") or {}
    try:
        view = C8ReadOnlyConsumer(str(c8.get("journal_path", ""))).load()
    except Exception as exc:
        raise S41HistoryRefusal("S41_HISTORY_C8_UNREADABLE", str(exc)) from exc
    c8_event = view.get(c8.get("occurrence_id", ""))
    if not c8_event:
        raise S41HistoryRefusal("S41_HISTORY_C8_ABSENT")
    if c8_event.get("content_hash") != c8.get("c8_content_hash"):
        raise S41HistoryRefusal("S41_HISTORY_C8_CONTENT_HASH_MISMATCH")
    payload = c8_event.get("payload") or {}
    if payload.get("gm01_pre_c9_source") != dict(source):
        raise S41HistoryRefusal("S41_HISTORY_C8_SOURCE_MISMATCH")
    if payload.get("clock") != prior.get("event_time"):
        raise S41HistoryRefusal("S41_HISTORY_C8_CLOCK_MISMATCH")
    prior_actor = (payload.get("actor") or {}).get("actor_id")
    if prior_actor != prior.get("actor_id"):
        raise S41HistoryRefusal("S41_HISTORY_C8_ACTOR_MISMATCH")

    generation = prior.get("generation")
    if not isinstance(generation, dict) or not valid(dict(generation)):
        raise S41HistoryRefusal("S41_HISTORY_PRIOR_GENERATION_UNSEALED")
    if generation.get("hash") != prior.get("generation_hash"):
        raise S41HistoryRefusal("S41_HISTORY_PRIOR_GENERATION_HASH_MISMATCH")
    if generation.get("event_ref") != prior.get("e1_event_hash"):
        raise S41HistoryRefusal("S41_HISTORY_PRIOR_E1_MISMATCH")

    content = history.get("content") or {}
    checks = {
        "prior_e1_event_id": prior.get("e1_event_id"),
        "prior_e1_event_hash": prior.get("e1_event_hash"),
        "mapped_from_e1_event_id": prior.get("e1_event_id"),
        "mapped_from_e1_event_hash": prior.get("e1_event_hash"),
        "prior_c8_occurrence_id": c8.get("occurrence_id"),
        "prior_c8_content_hash": c8_event.get("content_hash"),
        "prior_b_operation": source.get("b_operation"),
        "prior_b_event_hash": source.get("b_event_hash"),
        "prior_actor_id": prior.get("actor_id"),
        "prior_branch_id": prior.get("branch_id"),
        "prior_event_time": prior.get("event_time"),
        "prior_access_witness_hash": generation.get("access_witness_hash"),
        "prior_access_source_ref": generation.get("access_source_ref"),
        "prior_access_source_hash": generation.get("access_source_hash"),
        "prior_source_actor_map": prior.get("source_actor_map"),
    }
    for key, expected in checks.items():
        if content.get(key) != expected:
            raise S41HistoryRefusal("S41_HISTORY_" + key.upper() + "_MISMATCH")
    if content.get("prior_b_event_hash") != payload.get(
        "gm01_pre_c9_source", {}
    ).get("b_event_hash"):
        raise S41HistoryRefusal("S41_HISTORY_C8_B_EVENT_HASH_MISMATCH")
    if content.get("prior_c8_content_hash") != c8_event.get("content_hash"):
        raise S41HistoryRefusal("S41_HISTORY_C8_CONTENT_HASH_LINK_MISMATCH")
    return {
        "history": history,
        "prior_c8_event": c8_event,
        "prior_generation": generation,
        "prior_source": source,
    }


def validate_generation_readset(
    generation: Mapping[str, Any],
    history: Mapping[str, Any],
    source_records: list[Mapping[str, Any]] | None = None,
) -> None:
    """Require the actual consumed generation sources to include canonical history."""
    refs = generation.get("source_refs")
    if not isinstance(refs, list) or not refs:
        raise S41HistoryRefusal("S41_GENERATION_SOURCE_REFS_MISSING")
    if any(not isinstance(ref, str) or not ref for ref in refs):
        raise S41HistoryRefusal("S41_GENERATION_SOURCE_REF_INVALID")
    if len(set(refs)) != len(refs):
        raise S41HistoryRefusal("S41_GENERATION_SOURCE_REF_DUPLICATE")
    canonical = history.get("source_ref")
    if not canonical or canonical not in refs:
        raise S41HistoryRefusal("S41_GENERATION_CANONICAL_HISTORY_ABSENT")
    if source_records is not None:
        if not isinstance(source_records, list):
            raise S41HistoryRefusal("S41_GENERATION_INPUT_SOURCES_INVALID")
        input_refs = [record.get("source_ref") for record in source_records]
        if len(input_refs) != len(set(input_refs)):
            raise S41HistoryRefusal("S41_GENERATION_INPUT_SOURCE_DUPLICATE")
        canonical_rows = [
            record for record in source_records
            if record.get("source_ref") == canonical
        ]
        if len(canonical_rows) != 1:
            raise S41HistoryRefusal("S41_GENERATION_CANONICAL_INPUT_COUNT")
        canonical_record = canonical_rows[0]
        if (
            not isinstance(canonical_record, Mapping)
            or not valid(dict(canonical_record))
            or dict(canonical_record) != dict(history)
        ):
            raise S41HistoryRefusal("S41_GENERATION_CANONICAL_INPUT_REPLACED")
        allowed = {
            record.get("source_ref")
            for record in source_records
            if record.get("source_class") in CONTEXT_KINDS
        }
        if canonical not in allowed:
            raise S41HistoryRefusal("S41_GENERATION_CANONICAL_HISTORY_NOT_INPUT")
        if not set(refs).issubset(allowed):
            raise S41HistoryRefusal("S41_GENERATION_UNRECOGNIZED_SOURCE_REF")
    reasons = generation.get("reasons") or []
    history_reasons = [
        row for row in reasons if row.get("source_ref") == canonical
    ]
    if not history_reasons:
        raise S41HistoryRefusal("S41_GENERATION_HISTORY_REASON_ABSENT")
    if any(
        row.get("source_hash") != history.get("source_hash")
        or row.get("predicate") != history.get("predicate")
        for row in history_reasons
    ):
        raise S41HistoryRefusal("S41_GENERATION_HISTORY_REASON_MISMATCH")


__all__ = [
    "CANONICAL_PREFIX",
    "S41HistoryRefusal",
    "canonical_source_ref",
    "validate_generation_readset",
    "validate_history_source",
]
