"""Independent B producer over the same S48/S47 person and normal S42 path."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import RETURN, install

install()

from candidate import digest, seal  # noqa: E402
from s48.session import S48Session  # noqa: E402
from s39.model import S39GenerationRefusal  # noqa: E402

from .actor import (
    MISSING_B_CONTEXT,
    SOURCE_OWNER_HOLD,
    controlled_b_sources,
    generate_b,
    perform_b_attempt,
    record_b_observation,
    root_b_sources,
    validate_b_generation,
)
from .errors import S49Refusal

S49_SCHEMA = "SOROK_S49_INDEPENDENT_ACTOR_PRODUCER@1"
B_TURN_KIND = "S49_B_ACTOR_TURN"
B_RESULT_KIND = "S49_B_ACTOR_RESULT"
CONTROLLED_SOURCE_GRADE = "TEST_ONLY_S49_CONTROLLED_B_MODEL_PREMISE"
ACTUAL_SOURCE_GRADE = "UNAVAILABLE_CURRENT_B_ACTOR_OWNED_CONTEXT"


def _source_from_b_event(session, *, generation_body: Mapping[str, Any],
                         attempt: Mapping[str, Any]) -> tuple[dict, dict, dict]:
    event = session.event(attempt.get("event_id", ""))
    if not event:
        raise S49Refusal("S49_B_PERFORMED_EVENT_MISSING")
    if event.get("actor_id") != "B" or event.get("kind") != "REFUSAL":
        raise S49Refusal("S49_B_SOURCE_OPERATION_MISMATCH")
    first = session.read_events()[0]
    world = session.world()
    actor_b = (world.actor_state.get("B") or {}).get("actor_id")
    actor_a = (world.actor_state.get("A") or {}).get("actor_id")
    try:
        validate_b_generation(session, generation_body)
    except S49Refusal:
        raise
    if attempt.get("generation_hash") != generation_body.get("hash"):
        raise S49Refusal("S49_ATTEMPT_GENERATION_LINK_MISMATCH")
    generation = generation_body.get("generation") or {}
    request = generation.get("attempt_request") or {}
    source_chain_hash = digest({
        "generation": generation_body.get("hash"),
        "attempt": attempt.get("hash"),
        "event": attempt.get("event_id"),
        "event_hash": attempt.get("event_hash"),
    })
    source = {
        "schema": "BP2_FIRSTCLASS_B_MATERIAL_SOURCE@1",
        "b_actor": actor_b,
        "b_owner": actor_b,
        "b_event_ref": event["event_id"],
        "b_event_hash": event["hash"],
        "b_performed": True,
        "b_operation": "REFUSE_TOOL",
        "b_quantity": 0,
        "b_to_actor": actor_a,
        "b_clock": event["clock"],
        "a_e1_ref": first["e1_event_id"],
        "a_e1_hash": first["e1_event_hash"],
        "a_e1_clock": first["event_time"],
        "source_grade": "TEST_ONLY_SOURCEFREE",
        "native": False,
        "psychology_claim": False,
        "s49_generation_hash": generation_body.get("hash", ""),
        "s49_attempt_hash": attempt.get("hash", ""),
        "s49_rule_content_hash": (generation.get("rule") or {}).get(
            "content_hash", ""
        ),
        "s49_access_witness_hash": generation_body.get(
            "access_witness_hash", ""
        ),
        "s49_source_chain_hash": source_chain_hash,
    }
    case = {
        "schema": "S49_CURRENT_B_SOURCE_CASE@1",
        "case_id": "S49_CONTROLLED_B_REFUSAL",
        "actor": {"actor_id": actor_a},
        "other": {"actor_id": actor_b},
        "as_of": world.clock,
        "s49_generation_hash": generation_body.get("hash", ""),
        "s49_attempt_hash": attempt.get("hash", ""),
        "s49_source_chain_hash": source_chain_hash,
        "records": [
            {
                "kind": "OTHER_PERFORMED",
                "subject": actor_b,
                "owner": actor_b,
                "ref": event["event_id"],
                "content_hash": event["hash"],
                "performed": True,
                "at": event["clock"],
                "payload": {
                    "operation": "REFUSE_TOOL",
                    "to_actor": actor_a,
                    "quantity": 0,
                },
            },
            {
                "kind": "E1_EVENT",
                "subject": actor_a,
                "owner": "TEST_ONLY_OWNER_e1",
                "ref": first["e1_event_id"],
                "content_hash": first["e1_event_hash"],
                "at": first["event_time"],
                "payload": {},
            },
        ],
    }
    return case, source, event


class S49Session(S48Session):
    """S48 person plus the independent B actor producer/consumer seam."""

    def b_turns(self) -> list[dict]:
        rows = [
            row for row in self.product.store.episodes(self.branch_id)
            if row.get("kind") in {B_TURN_KIND, B_RESULT_KIND}
        ]
        return [
            {
                "episode_id": row.get("episode_id"),
                "clock": row.get("clock"),
                "kind": row.get("kind"),
                "body": dict(row.get("body") or {}),
            }
            for row in rows
        ]

    def _append(self, kind: str, body: Mapping[str, Any]) -> dict:
        episode = self.product._append_episode(
            self.branch_id, "B", kind, self.clock(), dict(body)
        )
        self.product._checkpoint(self.branch_id, self.clock(), self.world())
        return episode

    def produce_b_turn(self, *, controlled: bool = False) -> dict:
        source_records = controlled_b_sources(self) if controlled else root_b_sources(self)
        generation = generate_b(self, source_records=source_records)
        generation_episode = self._append(
            B_TURN_KIND,
            {
                "schema": S49_SCHEMA,
                "stage": "GENERATION",
                "controlled": bool(controlled),
                "generation": generation,
                "source_grade": (
                    CONTROLLED_SOURCE_GRADE if controlled else ACTUAL_SOURCE_GRADE
                ),
                "missing_context": MISSING_B_CONTEXT if not source_records else "",
            },
        )
        selection = generation["generation"]
        if selection.get("selection_status") != "UNIQUE_SELECTED":
            body = {
                "schema": S49_SCHEMA,
                "stage": "B_CONTEXT_HOLD",
                "controlled": bool(controlled),
                "status": "SOURCE_OWNER_HOLD",
                "reason": MISSING_B_CONTEXT if not source_records else "B_GENERATION_OPEN",
                "generation_ref": generation["hash"],
                "generation_episode_ref": generation_episode["episode_id"],
                "event_ref": "",
                "target_proposals": [],
                "native": False,
                "psychology_claim": False,
            }
            self._append(B_RESULT_KIND, body)
            return body
        attempt = perform_b_attempt(self, generation)
        attempt["generation_hash"] = generation["hash"]
        self._append(B_RESULT_KIND, {
            "schema": S49_SCHEMA,
            "stage": "B_PERFORMER",
            "controlled": bool(controlled),
            "generation_episode_ref": generation_episode["episode_id"],
            "attempt": attempt,
            "source_grade": CONTROLLED_SOURCE_GRADE if controlled else ACTUAL_SOURCE_GRADE,
        })
        if not attempt.get("performed"):
            return {
                "schema": S49_SCHEMA,
                "stage": "B_PERFORMER",
                "controlled": bool(controlled),
                "status": attempt.get("status"),
                "generation_ref": generation["hash"],
                "attempt": attempt,
                "event_ref": "",
                "target_proposals": [],
                "native": False,
                "psychology_claim": False,
            }
        selected = selection.get("selected_option")
        if selected != "EXPLICIT_REFUSAL" or attempt.get("option_id") != "EXPLICIT_REFUSAL":
            body = {
                "schema": S49_SCHEMA,
                "stage": "SOURCE_ADAPTER_HOLD",
                "controlled": bool(controlled),
                "status": "SOURCE_OWNER_HOLD",
                "reason": "NO_HONEST_S42_SOURCE_ADAPTER_FOR_" + str(selected),
                "generation_ref": generation["hash"],
                "attempt": attempt,
                "event_ref": "",
                "target_proposals": [],
                "native": False,
                "psychology_claim": False,
            }
            self._append(B_RESULT_KIND, body)
            return body
        case, source, b_event = _source_from_b_event(
            self, generation_body=generation, attempt=attempt
        )
        try:
            admitted = self.admit_event(
                case=case,
                source=source,
                history_event_refs=(self.read_events()[-1]["e1_event_id"],),
                event_time=self.clock() + 1,
            )
        except Exception as exc:
            body = {
                "schema": S49_SCHEMA,
                "stage": "NORMAL_CONSUMER_HOLD",
                "controlled": bool(controlled),
                "status": "SOURCE_OWNER_HOLD",
                "reason": getattr(exc, "code", type(exc).__name__),
                "generation_ref": generation["hash"],
                "attempt": attempt,
                "event_ref": "",
                "target_proposals": [],
                "native": False,
                "psychology_claim": False,
            }
            self._append(B_RESULT_KIND, body)
            return body
        event = admitted.get("event") or {}
        result = {
            "schema": S49_SCHEMA,
            "stage": "NORMAL_CONSUMER",
            "controlled": bool(controlled),
            "status": admitted.get("status"),
            "generation_ref": generation["hash"],
            "generation_episode_ref": generation_episode["episode_id"],
            "attempt": attempt,
            "b_source_event_ref": b_event["event_id"],
            "b_source_event_hash": b_event["hash"],
            "b_source_operation": "REFUSE_TOOL",
            "event_ref": event.get("e1_event_id", ""),
            "event_hash": event.get("e1_event_hash", ""),
            "event_ordinal": event.get("event_ordinal"),
            "target_proposals": list(event.get("target_proposals") or []),
            "native": False,
            "psychology_claim": False,
        }
        self._append(B_RESULT_KIND, result)
        return {**result, "event": event}

    def verify(self) -> dict:
        result = super().verify()
        try:
            result["s49_b_turns"] = {
                "status": "OK",
                "count": len(self.b_turns()),
            }
            ok = True
        except Exception as exc:
            result["s49_b_turns"] = {
                "status": "REFUSED", "code": getattr(exc, "code", type(exc).__name__),
            }
            ok = False
        result["ok"] = bool(result.get("ok")) and ok
        return result


__all__ = [
    "ACTUAL_SOURCE_GRADE", "B_RESULT_KIND", "B_TURN_KIND",
    "CONTROLLED_SOURCE_GRADE", "S49_SCHEMA", "S49Session",
]
