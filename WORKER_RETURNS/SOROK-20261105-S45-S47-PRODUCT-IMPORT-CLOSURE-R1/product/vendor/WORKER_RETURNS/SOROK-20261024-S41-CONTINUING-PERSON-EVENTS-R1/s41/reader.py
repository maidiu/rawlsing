"""Event-keyed continuation reader for two admitted S41 events."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .bootstrap import install

install()

from c8_readonly_consumer import C8ReadOnlyConsumer  # noqa: E402
from candidate import valid  # noqa: E402
from .bindings import BINDING_SCHEMA, binding_episodes  # noqa: E402
from .history import (  # noqa: E402
    S41HistoryRefusal,
    validate_generation_readset,
    validate_history_source,
)


class S41ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _load(row, code: str, record_hash: str) -> dict:
    if row is None:
        raise S41ReadRefusal(code + "_ROW_MISSING")
    value = json.loads(row[0])
    if not isinstance(value, dict):
        raise S41ReadRefusal(code + "_NOT_OBJECT")
    if "hash" in value:
        if value.get("hash") != record_hash:
            raise S41ReadRefusal(code + "_ROW_KEY_MISMATCH")
    else:
        value["hash"] = record_hash
    if not valid(value):
        raise S41ReadRefusal(code + "_UNSEALED")
    return value


def _read_c9(c9: dict) -> tuple[dict, dict, int]:
    path = Path(c9.get("c9_db_path", ""))
    response_ref = c9.get("response_ref", "")
    receipt_ref = c9.get("receipt_ref", "")
    if not path.is_file() or not response_ref or not receipt_ref:
        raise S41ReadRefusal("S41_C9_BINDING_INCOMPLETE")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        response = _load(
            conn.execute("SELECT body FROM response WHERE hash=?", (response_ref,)).fetchone(),
            "S41_C9_RESPONSE", response_ref,
        )
        receipt = _load(
            conn.execute("SELECT body FROM receipt WHERE hash=?", (receipt_ref,)).fetchone(),
            "S41_C9_RECEIPT", receipt_ref,
        )
        target_rows = conn.execute("SELECT count(*) FROM target_state").fetchone()[0]
    finally:
        conn.close()
    return response, receipt, int(target_rows)


def _read_c8(c8: dict, source: dict, binding: dict) -> dict:
    journal_path = c8.get("journal_path", "")
    occurrence_id = c8.get("occurrence_id", "")
    try:
        view = C8ReadOnlyConsumer(journal_path).load()
    except Exception as exc:
        raise S41ReadRefusal("S41_C8_UNREADABLE", str(exc)) from exc
    event = view.get(occurrence_id)
    if not event:
        raise S41ReadRefusal("S41_C8_OCCURRENCE_ABSENT")
    if event.get("content_hash") != c8.get("c8_content_hash"):
        raise S41ReadRefusal("S41_C8_CONTENT_HASH_MISMATCH")
    payload = event.get("payload") or {}
    if payload.get("gm01_pre_c9_source") != dict(source):
        raise S41ReadRefusal("S41_C8_SOURCE_MISMATCH")
    if payload.get("clock") != binding.get("event_time"):
        raise S41ReadRefusal("S41_C8_CLOCK_MISMATCH")
    actor = payload.get("actor") or {}
    other = payload.get("other_actor") or {}
    source_map = binding.get("source_actor_map") or {}
    if actor.get("actor_id") != binding.get("actor_id"):
        raise S41ReadRefusal("S41_C8_ACTOR_MISMATCH")
    if actor.get("actor_id") != source_map.get("TEST_ONLY_R31J_A"):
        raise S41ReadRefusal("S41_C8_ACTOR_SOURCE_MAP_MISMATCH")
    if other.get("actor_id") != source_map.get("TEST_ONLY_R31J_B"):
        raise S41ReadRefusal("S41_C8_OTHER_ACTOR_MISMATCH")
    expected_id = "TEST_ONLY_BP2_E1_" + occurrence_id
    if binding.get("e1_event_id") != expected_id:
        raise S41ReadRefusal("S41_E1_ID_DERIVATION_MISMATCH")
    if payload.get("s41_continuation", {}).get("prior_e1_event_hash") not in (
        None, binding.get("history_refs", [{}])[0].get("e1_event_hash") if binding.get("history_refs") else None
    ):
        raise S41ReadRefusal("S41_C8_PRIOR_E1_MISMATCH")
    return event


def _read_language(session, binding: dict, event: dict) -> dict:
    language = binding.get("language")
    if not isinstance(language, dict) or not valid(dict(language)):
        raise S41ReadRefusal("S41_LANGUAGE_BINDING_MISSING")
    language = dict(language)
    if language.get("schema") != "S40_GENERATED_LANGUAGE_BINDING@1":
        raise S41ReadRefusal("S41_LANGUAGE_SCHEMA_MISMATCH")
    if language.get("equivalence_status") != "ACCEPTED":
        raise S41ReadRefusal("S41_LANGUAGE_EQUIVALENCE_NOT_ACCEPTED")
    if language.get("target_proposals") != []:
        raise S41ReadRefusal("S41_LANGUAGE_TARGET_PRESENT")
    if language.get("private_generation_sources_in_plan") is not False:
        raise S41ReadRefusal("S41_PRIVATE_SOURCES_IN_PLAN")
    if event.get("kind") != "SPEECH" or event.get("actor_id") != "A":
        raise S41ReadRefusal("S41_SPEECH_EVENT_INVALID")
    if event.get("hash") != binding.get("action", {}).get("event_hash"):
        raise S41ReadRefusal("S41_SPEECH_EVENT_HASH_MISMATCH")
    body = event.get("body") or {}
    if body.get("text") != language.get("native_text"):
        raise S41ReadRefusal("S41_NATIVE_TEXT_MISMATCH")
    lme = body.get("lme") or {}
    for key in ("plan_hash", "native_artifact_hash", "translation_artifact_hash",
                "equivalence_receipt_hash"):
        if lme.get(key) != language.get(key):
            raise S41ReadRefusal("S41_LME_" + key.upper() + "_MISMATCH")
    view = session.language_view(binding["action"]["event_id"], locale="en")
    if view.get("status") != "OK" or view.get("display_mode") != "LABELED_ENGLISH":
        raise S41ReadRefusal("S41_LABELED_ENGLISH_VIEW_UNAVAILABLE")
    if view.get("translation_text") != language.get("translation_text"):
        raise S41ReadRefusal("S41_TRANSLATION_TEXT_MISMATCH")
    if (view.get("equivalence") or {}).get("receipt_hash") != language.get(
        "equivalence_receipt_hash"
    ):
        raise S41ReadRefusal("S41_VIEW_EQUIVALENCE_MISMATCH")
    if view.get("plan_hash") != language.get("plan_hash"):
        raise S41ReadRefusal("S41_VIEW_PLAN_MISMATCH")
    if binding.get("e1_event_id") != language.get("e1_event_id"):
        raise S41ReadRefusal("S41_LANGUAGE_E1_ID_MISMATCH")
    if binding.get("e1_event_hash") != language.get("e1_event_hash"):
        raise S41ReadRefusal("S41_LANGUAGE_E1_HASH_MISMATCH")
    return {
        "status": "ACCEPTED",
        "native_text": language.get("native_text"),
        "translation_text": language.get("translation_text"),
        "plan_hash": language.get("plan_hash"),
        "native_artifact_hash": language.get("native_artifact_hash"),
        "translation_artifact_hash": language.get("translation_artifact_hash"),
        "equivalence_receipt_hash": language.get("equivalence_receipt_hash"),
        "source_event_id": language.get("source_event_id"),
        "source_event_hash": language.get("source_event_hash"),
        "access_receipt_id": language.get("access_receipt_id"),
    }


def _validate_history(session, binding: dict, bindings: list[dict]) -> list[dict]:
    refs = list(binding.get("history_refs") or [])
    if binding.get("event_ordinal") == 1:
        if refs or binding.get("history_source") is not None:
            raise S41ReadRefusal("S41_FIRST_EVENT_HISTORY_NOT_EMPTY")
        return []
    if len(refs) != 1:
        raise S41ReadRefusal("S41_HISTORY_REF_COUNT")
    prior_ref = refs[0]
    prior = next(
        (row for row in bindings if row.get("e1_event_id") == prior_ref.get("e1_event_id")),
        None,
    )
    if prior is None or prior.get("e1_event_hash") != prior_ref.get("e1_event_hash"):
        raise S41ReadRefusal("S41_HISTORY_PRIOR_EVENT_MISSING")
    if prior.get("event_ordinal") >= binding.get("event_ordinal"):
        raise S41ReadRefusal("S41_HISTORY_ORDER_INVALID")
    if prior.get("event_time", 0) >= binding.get("event_time", 0):
        raise S41ReadRefusal("S41_HISTORY_CLOCK_INVALID")
    history = binding.get("history_source")
    if not isinstance(history, dict) or not valid(dict(history)):
        raise S41ReadRefusal("S41_HISTORY_SOURCE_MISSING")
    try:
        validate_history_source(
            session, history, prior,
            branch_id=binding["branch_id"], as_of=binding["as_of"],
        )
    except S41HistoryRefusal as exc:
        raise S41ReadRefusal("S41_HISTORY_BINDING_INVALID", exc.code) from exc
    prior_source = prior.get("source") or {}
    expected = {
        "SHARE_TOOL": "PRIOR_B_SHARE",
        "REFUSE_TOOL": "PRIOR_B_REFUSAL",
    }.get(prior_source.get("b_operation"))
    if expected is None or history.get("predicate") != expected:
        raise S41ReadRefusal("S41_HISTORY_PREDICATE_MISMATCH")
    return refs


def read_event(session, event_ref: str) -> dict:
    bindings = binding_episodes(session)
    binding = next(
        (
            row for row in bindings
            if row.get("e1_event_id") == event_ref
            or row.get("e1_event_hash") == event_ref
        ),
        None,
    )
    if binding is None:
        raise S41ReadRefusal("S41_EVENT_NOT_FOUND")
    if not valid(dict(binding)):
        raise S41ReadRefusal("S41_EVENT_BINDING_UNSEALED")
    if binding.get("schema") != BINDING_SCHEMA:
        raise S41ReadRefusal("S41_EVENT_BINDING_SCHEMA_MISMATCH")
    _validate_history(session, binding, bindings)
    c8_event = _read_c8(binding["c8"], binding["source"], binding)
    generation = binding.get("generation")
    if not isinstance(generation, dict) or not valid(dict(generation)):
        raise S41ReadRefusal("S41_GENERATION_UNSEALED")
    if generation.get("hash") != binding.get("generation_hash"):
        raise S41ReadRefusal("S41_GENERATION_HASH_MISMATCH")
    if binding.get("event_ordinal") != 1:
        if not binding.get("generation_sources"):
            raise S41ReadRefusal(
                "S41_GENERATION_READSET_INVALID",
                "S41_GENERATION_INPUT_SOURCES_MISSING",
            )
        try:
            validate_generation_readset(
                generation,
                binding.get("history_source") or {},
                binding.get("generation_sources"),
            )
        except S41HistoryRefusal as exc:
            raise S41ReadRefusal(
                "S41_GENERATION_READSET_INVALID", exc.code
            ) from exc
    status = binding.get("status")
    if status in {"OPEN", "REFUSED"}:
        if status == "OPEN" and generation.get("selection_status") == "UNIQUE_SELECTED":
            raise S41ReadRefusal("S41_OPEN_WITH_SELECTION")
        if binding.get("attempt") is not None or binding.get("s36") is not None:
            raise S41ReadRefusal("S41_OPEN_HAS_ATTEMPT")
        if binding.get("action") is not None:
            raise S41ReadRefusal("S41_OPEN_HAS_ACTION")
        return {
            "schema": "SOROK_S41_EVENT_READ@1",
            "status": status,
            "event_ordinal": binding.get("event_ordinal"),
            "e1_event_id": binding.get("e1_event_id"),
            "e1_event_hash": binding.get("e1_event_hash"),
            "c8_occurrence_id": binding["c8"].get("occurrence_id"),
            "c8_state_digest": binding["c8"].get("c8_state_digest"),
            "event_time": binding.get("event_time"),
            "actor_id": binding.get("actor_id"),
            "source_operation": binding.get("source", {}).get("b_operation"),
            "generation_status": generation.get("selection_status"),
            "unresolved_reason": generation.get("unresolved_reason"),
            "actor_action_appended": False,
            "history_refs": binding.get("history_refs") or [],
            "history_predicate": (binding.get("history_source") or {}).get("predicate"),
            "generation_source_refs": list(generation.get("source_refs") or []),
            "world_tools_remaining": ((binding.get("world_after") or {}).get("actor_state", {}).get("A", {}) or {}).get("tools_remaining"),
            "world_clock_before": (binding.get("world_before") or {}).get("clock"),
            "world_clock_after": (binding.get("world_after") or {}).get("clock"),
            "target_proposals": [],
            "provenance": binding.get("provenance"),
        }

    attempt = binding.get("attempt")
    if not isinstance(attempt, dict) or not valid(dict(attempt)):
        raise S41ReadRefusal("S41_ATTEMPT_UNSEALED")
    if attempt.get("hash") != binding.get("attempt_hash"):
        raise S41ReadRefusal("S41_ATTEMPT_HASH_MISMATCH")
    if attempt.get("generation_receipt_hash") != generation.get("hash"):
        raise S41ReadRefusal("S41_ATTEMPT_GENERATION_LINK_MISMATCH")
    if attempt.get("option_id") != generation.get("selected_option"):
        raise S41ReadRefusal("S41_ATTEMPT_OPTION_MISMATCH")
    if attempt.get("actor_id") != binding.get("actor_id"):
        raise S41ReadRefusal("S41_ATTEMPT_ACTOR_MISMATCH")
    if binding.get("c9") is None:
        raise S41ReadRefusal("S41_C9_BINDING_MISSING")
    response, receipt, target_rows = _read_c9(binding["c9"])
    if response.get("event_ref") != binding.get("e1_event_hash"):
        raise S41ReadRefusal("S41_C9_RESPONSE_EVENT_MISMATCH")
    if receipt.get("response_ref") != binding["c9"].get("response_ref"):
        raise S41ReadRefusal("S41_C9_RECEIPT_RESPONSE_MISMATCH")
    if receipt.get("event_ref") != binding.get("e1_event_hash"):
        raise S41ReadRefusal("S41_C9_RECEIPT_EVENT_MISMATCH")
    if receipt.get("target_branch") != "NO_CHANGE" or receipt.get("target_reason") != "NO_PROPOSAL":
        raise S41ReadRefusal("S41_C9_TARGET_NOT_NO_CHANGE")
    if target_rows != 0 or response.get("target_proposal_ref", "") != "":
        raise S41ReadRefusal("S41_C9_TARGET_PRESENT")
    s35 = response.get("s35_receipt")
    if not isinstance(s35, dict) or not valid(dict(s35)):
        raise S41ReadRefusal("S41_S35_RECEIPT_UNSEALED")
    if s35.get("event_ref") != binding.get("e1_event_hash"):
        raise S41ReadRefusal("S41_S35_EVENT_MISMATCH")
    if s35.get("target_proposals") != []:
        raise S41ReadRefusal("S41_S35_TARGET_PRESENT")
    if s35.get("outcome") in {
        "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION", "OBSERVED_CURRENT_REFUSAL"
    }:
        expected_status = "RESPONSE_COMMITTED"
    else:
        expected_status = "RESPONSE_EFFECTS_VALID_EMPTY"
    if response.get("status") != expected_status:
        raise S41ReadRefusal("S41_C9_STATUS_OUTCOME_MISMATCH")
    if receipt.get("record_hash", "") or receipt.get("target_id", ""):
        raise S41ReadRefusal("S41_C9_TARGET_IDENTITY_PRESENT")

    action = binding.get("action") or {}
    performed = bool(attempt.get("performed"))
    language = None
    if performed:
        event = session.event(action.get("event_id", ""))
        if not event or event.get("hash") != action.get("event_hash"):
            raise S41ReadRefusal("S41_ACTION_EVENT_MISMATCH")
        if attempt.get("s36_response_kind") != (s35.get("response_kind") or ""):
            raise S41ReadRefusal("S41_ACTION_RESPONSE_KIND_MISMATCH")
        if action.get("event_kind") == "SPEECH":
            language = _read_language(session, binding, event)
        elif action.get("event_kind") == "INSPECT":
            if binding.get("language") is not None:
                raise S41ReadRefusal("S41_NONVERBAL_HAS_LANGUAGE")
            language = {"status": "NONVERBAL"}
        else:
            raise S41ReadRefusal("S41_ACTION_EVENT_KIND_INVALID")
    else:
        if binding.get("language") is not None or action.get("event_id"):
            raise S41ReadRefusal("S41_DENIED_HAS_ACTION_OR_LANGUAGE")
        if s35.get("outcome") != "RECEIVABLE_NO_OBSERVED_UPTAKE":
            raise S41ReadRefusal("S41_DENIED_NOT_VALID_EMPTY")
    return {
        "schema": "SOROK_S41_EVENT_READ@1",
        "status": "OK",
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
        "history_predicate": (binding.get("history_source") or {}).get("predicate"),
        "generation_source_refs": list(generation.get("source_refs") or []),
        "world_before": binding.get("world_before"),
        "world_after": binding.get("world_after"),
        "world_tools_remaining": ((binding.get("world_after") or {}).get("actor_state", {}).get("A", {}) or {}).get("tools_remaining"),
        "world_clock_before": (binding.get("world_before") or {}).get("clock"),
        "world_clock_after": (binding.get("world_after") or {}).get("clock"),
        "actor_action_appended": performed,
        "target_proposals": [],
        "provenance": binding.get("provenance"),
    }


def read_all_events(session) -> list[dict]:
    return [read_event(session, row["e1_event_id"]) for row in binding_episodes(session)]


def read_latest_event(session) -> dict:
    events = read_all_events(session)
    if not events:
        raise S41ReadRefusal("S41_NO_EVENTS")
    return events[-1]


__all__ = [
    "S41ReadRefusal",
    "read_all_events",
    "read_event",
    "read_latest_event",
]
