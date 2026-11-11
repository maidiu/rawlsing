"""Read the persisted S39 generation/attempt and bind it to the same C9/C12."""
from __future__ import annotations

from typing import Any

from .bootstrap import install

install()

from candidate import valid  # noqa: E402

from .model import PROVENANCE  # noqa: E402

GENERATION_KIND = "S39_CONSTRUCTIVE_GENERATION"
ATTEMPT_KIND = "S39_GENERATED_ATTEMPT"


class S39ReadRefusal(ValueError):
    def __init__(self, code: str, detail: str = "") -> None:
        super().__init__(code if not detail else f"{code}: {detail}")
        self.code = code


def _one(episodes, kind: str) -> dict:
    rows = [row for row in episodes if row.get("kind") == kind]
    if len(rows) != 1:
        code = (
            "S39_GENERATION_BINDING_COUNT"
            if kind == GENERATION_KIND
            else "S39_ATTEMPT_BINDING_COUNT"
        )
        raise S39ReadRefusal(code, str(len(rows)))
    body = rows[0].get("body") or {}
    return dict(body)


def read_generation(session) -> dict:
    episodes = session.product.store.episodes(session.branch_id)
    generation_body = _one(episodes, GENERATION_KIND)
    attempt_body = _one(episodes, ATTEMPT_KIND)
    generation = generation_body.get("generation")
    attempt = attempt_body.get("attempt")
    if not isinstance(generation, dict) or not valid(dict(generation)):
        raise S39ReadRefusal("S39_GENERATION_UNSEALED")
    if not isinstance(attempt, dict) or not valid(dict(attempt)):
        raise S39ReadRefusal("S39_ATTEMPT_UNSEALED")
    generation = dict(generation)
    attempt = dict(attempt)
    meta = session.meta
    c8 = meta.get("c8") or {}
    s39 = {
        "generation_hash": meta.get("s39_generation_hash"),
        "attempt_hash": meta.get("s39_attempt_hash"),
        "selected_option": meta.get("s39_selected_option"),
        "provenance": meta.get("s39_provenance"),
    }
    if generation.get("hash") != s39["generation_hash"]:
        raise S39ReadRefusal("S39_GENERATION_HASH_MISMATCH")
    if attempt.get("hash") != s39["attempt_hash"]:
        raise S39ReadRefusal("S39_ATTEMPT_HASH_MISMATCH")
    if generation_body.get("generation_hash") != generation.get("hash"):
        raise S39ReadRefusal("S39_GENERATION_EPISODE_HASH_MISMATCH")
    if attempt_body.get("attempt_hash") != attempt.get("hash"):
        raise S39ReadRefusal("S39_ATTEMPT_EPISODE_HASH_MISMATCH")
    if attempt_body.get("generation_hash") != generation.get("hash"):
        raise S39ReadRefusal("S39_ATTEMPT_GENERATION_LINK_MISMATCH")
    if generation.get("provenance") != PROVENANCE:
        raise S39ReadRefusal("S39_GENERATION_PROVENANCE_MISMATCH")
    if generation.get("selected_option") != s39["selected_option"]:
        raise S39ReadRefusal("S39_GENERATION_OPTION_MISMATCH")
    if generation.get("selection_status") != "UNIQUE_SELECTED":
        raise S39ReadRefusal("S39_GENERATION_NOT_UNIQUE")
    if generation.get("input_contains_desired_action") is not False:
        raise S39ReadRefusal("S39_GENERATION_INPUT_CONTAINED_ANSWER")
    if generation.get("target_proposals") != []:
        raise S39ReadRefusal("S39_GENERATION_TARGET_PRESENT")
    if attempt.get("target_proposals") != []:
        raise S39ReadRefusal("S39_ATTEMPT_TARGET_PRESENT")
    if attempt.get("generation_receipt_hash") != generation.get("hash"):
        raise S39ReadRefusal("S39_ATTEMPT_GENERATION_RECEIPT_MISMATCH")
    if attempt.get("attempt_request_hash") != (
        generation.get("attempt_request") or {}
    ).get("hash"):
        raise S39ReadRefusal("S39_ATTEMPT_REQUEST_HASH_MISMATCH")
    if attempt.get("option_id") != generation.get("selected_option"):
        raise S39ReadRefusal("S39_ATTEMPT_OPTION_MISMATCH")
    if attempt.get("actor_id") != generation.get("actor_id"):
        raise S39ReadRefusal("S39_ATTEMPT_ACTOR_MISMATCH")
    if generation.get("branch_id") != session.branch_id:
        raise S39ReadRefusal("S39_GENERATION_BRANCH_MISMATCH")
    if generation.get("event_ref") != c8.get("e1_event_hash"):
        raise S39ReadRefusal("S39_GENERATION_EVENT_MISMATCH")
    if generation.get("c8_state_digest") != c8.get("c8_state_digest"):
        raise S39ReadRefusal("S39_GENERATION_C8_MISMATCH")
    source_map = meta.get("source_actor_map") or {}
    if generation.get("actor_id") != source_map.get("TEST_ONLY_R31J_A"):
        raise S39ReadRefusal("S39_GENERATION_ACTOR_SOURCE_MISMATCH")

    s36 = session.read_s36()
    performed = bool(attempt.get("performed"))
    if performed:
        if attempt.get("attempt_status") != "ADMITTED":
            raise S39ReadRefusal("S39_ATTEMPT_STATUS_MISMATCH")
        event_id = attempt.get("event_id", "")
        event = session.event(event_id) if event_id else None
        if not event:
            raise S39ReadRefusal("S39_ACTION_EVENT_ABSENT")
        if event.get("hash") != attempt.get("event_hash"):
            raise S39ReadRefusal("S39_ACTION_EVENT_HASH_MISMATCH")
        if s36["outcome"] not in {
            "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
            "OBSERVED_CURRENT_REFUSAL",
        }:
            raise S39ReadRefusal("S39_PERFORMED_S36_NOT_OBSERVED")
        if s36["response_kind"] != attempt.get("s36_response_kind"):
            raise S39ReadRefusal("S39_PERFORMED_S36_KIND_MISMATCH")
        if s36["s35_receipt"].get("observed_response_ref") != event_id:
            raise S39ReadRefusal("S39_PERFORMED_S36_RESPONSE_REF_MISMATCH")
    else:
        if attempt.get("attempt_status") != "DENIED":
            raise S39ReadRefusal("S39_DENIED_STATUS_MISMATCH")
        if attempt.get("event_id") or attempt.get("event_hash"):
            raise S39ReadRefusal("S39_DENIED_WITH_EVENT")
        if s36["outcome"] != "RECEIVABLE_NO_OBSERVED_UPTAKE":
            raise S39ReadRefusal("S39_DENIED_S36_NOT_EMPTY")
        if s36["response_kind"]:
            raise S39ReadRefusal("S39_DENIED_S36_RESPONSE_KIND")
    if s36["target_branch"] != "NO_CHANGE" or s36["target_reason"] != "NO_PROPOSAL":
        raise S39ReadRefusal("S39_S36_TARGET_NOT_NO_CHANGE")
    if s36["target_proposals"] != [] or s36["target_state_rows"] != 0:
        raise S39ReadRefusal("S39_S36_TARGET_PRESENT")
    return {
        "schema": "SOROK_S39_GENERATION_READ@1",
        "grade": PROVENANCE,
        "native": False,
        "status": "OK",
        "generation": generation,
        "attempt": attempt,
        "generation_hash": generation["hash"],
        "attempt_hash": attempt["hash"],
        "selected_option": generation["selected_option"],
        "action": attempt.get("action"),
        "attempt_status": attempt.get("attempt_status"),
        "performed": performed,
        "event_id": attempt.get("event_id", ""),
        "event_hash": attempt.get("event_hash", ""),
        "s36": {
            "response_ref": s36["response_ref"],
            "c9_receipt_hash": s36["c9_receipt_hash"],
            "outcome": s36["outcome"],
            "response_kind": s36["response_kind"],
            "target_branch": s36["target_branch"],
            "target_reason": s36["target_reason"],
            "target_proposals": s36["target_proposals"],
            "target_state_rows": s36["target_state_rows"],
        },
        "provenance": PROVENANCE,
    }


__all__ = ["ATTEMPT_KIND", "GENERATION_KIND", "S39ReadRefusal", "read_generation"]
