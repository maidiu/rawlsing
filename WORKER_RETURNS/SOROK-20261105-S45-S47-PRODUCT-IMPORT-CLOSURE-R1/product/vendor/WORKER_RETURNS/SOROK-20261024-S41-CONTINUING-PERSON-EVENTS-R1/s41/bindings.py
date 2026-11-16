"""Event-keyed S41 binding episodes over the continuing C12 branch."""
from __future__ import annotations

from typing import Any, Mapping

from .bootstrap import install

install()

from candidate import seal  # noqa: E402

EVENT_KIND = "S41_ADMITTED_EVENT"
BINDING_SCHEMA = "S41_ADMITTED_EVENT_BINDING@1"
GRADE = "TEST_ONLY_SOURCEFREE_CONTINUING_PERSON_NOT_NATIVE"


def _sealed(body: Mapping[str, Any]) -> dict:
    return seal(dict(body))


def make_first_event_binding(session) -> dict:
    generation = session.read_generation()
    attempt = dict(generation["attempt"])
    s36 = dict(session.read_s36())
    action = {
        "event_id": attempt.get("event_id", ""),
        "event_hash": attempt.get("event_hash", ""),
        "event_kind": attempt.get("event_kind", ""),
        "s36_response_kind": attempt.get("s36_response_kind", ""),
        "attempt_status": attempt.get("attempt_status", ""),
        "performed": bool(attempt.get("performed")),
    }
    world = session.world().snapshot()
    body = {
        "schema": BINDING_SCHEMA,
        "grade": GRADE,
        "native": False,
        "provenance": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "event_ordinal": 1,
        "actor_id": session.meta["source_actor_map"]["TEST_ONLY_R31J_A"],
        "branch_id": session.branch_id,
        "event_time": generation["generation"].get("event_time", session.clock()),
        "as_of": generation["generation"].get("as_of", session.clock()),
        "source": dict(session.meta["source"]),
        "source_actor_map": dict(session.meta["source_actor_map"]),
        "c8": dict(session.meta["c8"]),
        "e1_event_id": session.meta["c8"]["e1_event_id"],
        "e1_event_hash": session.meta["c8"]["e1_event_hash"],
        "generation": dict(generation["generation"]),
        "generation_hash": generation["generation_hash"],
        "attempt": attempt,
        "attempt_hash": generation["attempt_hash"],
        "s36": s36,
        "action": action,
        "language": attempt.get("language"),
        "c9": {
            "c9_db_path": session.meta["s36"]["c9_db_path"],
            "response_ref": s36["response_ref"],
            "receipt_ref": s36["c9_receipt_hash"],
            "outcome": s36["outcome"],
            "response_kind": s36["response_kind"],
            "target_branch": s36["target_branch"],
            "target_reason": s36["target_reason"],
            "target_proposals": s36["target_proposals"],
            "target_state_rows": s36["target_state_rows"],
        },
        "history_refs": [],
        "history_source": None,
        "world_before": world,
        "world_after": world,
        "status": "ADMITTED" if attempt.get("performed") else "DENIED",
        "target_proposals": [],
    }
    return _sealed(body)


def make_continuation_binding(
    session,
    *,
    producer,
    generation: Mapping[str, Any],
    attempt: Mapping[str, Any] | None,
    s36: Mapping[str, Any] | None,
    source: Mapping[str, Any],
    first_binding: Mapping[str, Any],
    history_source: Mapping[str, Any] | None,
    world_before: Mapping[str, Any],
    world_after: Mapping[str, Any],
    status: str,
    generation_sources: list[Mapping[str, Any]] | None = None,
) -> dict:
    attempt = dict(attempt or {})
    s36 = dict(s36 or {})
    c8 = dict(producer.c8_binding())
    action = {
        "event_id": attempt.get("event_id", ""),
        "event_hash": attempt.get("event_hash", ""),
        "event_kind": attempt.get("event_kind", ""),
        "s36_response_kind": attempt.get("s36_response_kind", ""),
        "attempt_status": attempt.get("attempt_status", ""),
        "performed": bool(attempt.get("performed")),
    }
    c9 = {
        "c9_db_path": str(producer.c9.path),
        "response_ref": s36.get("response_ref", ""),
        "receipt_ref": s36.get("c9_receipt_hash", ""),
        "outcome": s36.get("outcome", ""),
        "response_kind": s36.get("response_kind", ""),
        "target_branch": s36.get("target_branch", "NO_CHANGE"),
        "target_reason": s36.get("target_reason", "NO_PROPOSAL"),
        "target_proposals": s36.get("target_proposals", []),
        "target_state_rows": s36.get("target_state_rows", 0),
    }
    body = {
        "schema": BINDING_SCHEMA,
        "grade": GRADE,
        "native": False,
        "provenance": "TEST_ONLY_CONSTRUCTIVE_GENERATION_NOT_EXTERNALLY_OBSERVED",
        "event_ordinal": 2,
        "actor_id": producer.occurrence.actor_id,
        "branch_id": session.branch_id,
        "event_time": producer.occurrence.event_time,
        "as_of": producer.as_of,
        "source": dict(source),
        "source_actor_map": producer.source_map(),
        "c8": c8,
        "e1_event_id": c8["e1_event_id"],
        "e1_event_hash": c8["e1_event_hash"],
        "generation": dict(generation),
        "generation_hash": generation["hash"],
        "attempt": attempt or None,
        "attempt_hash": attempt.get("hash", ""),
        "s36": s36 or None,
        "action": action if attempt else None,
        "language": attempt.get("language") if attempt else None,
        "c9": c9 if s36 else None,
        "history_refs": [{
            "event_ordinal": first_binding["event_ordinal"],
            "e1_event_id": first_binding["e1_event_id"],
            "e1_event_hash": first_binding["e1_event_hash"],
            "c8_occurrence_id": first_binding["c8"]["occurrence_id"],
            "c8_content_hash": first_binding["c8"].get("c8_content_hash", ""),
        }],
        "history_source": dict(history_source) if history_source else None,
        "generation_sources": [
            dict(record) for record in (generation_sources or [])
        ],
        "world_before": dict(world_before),
        "world_after": dict(world_after),
        "status": status,
        "target_proposals": [],
    }
    return _sealed(body)


def append_event_binding(session, binding: Mapping[str, Any]) -> dict:
    body = {
        "schema": "SOROK_S41_EVENT_EPISODE@1",
        "grade": GRADE,
        "native": False,
        "event_ordinal": binding["event_ordinal"],
        "e1_event_id": binding["e1_event_id"],
        "e1_event_hash": binding["e1_event_hash"],
        "binding": dict(binding),
    }
    episode = session.product._append_episode(
        session.branch_id, "A", EVENT_KIND, session.clock(), body
    )
    session.product._checkpoint(session.branch_id, session.clock(), session.world())
    return episode


def binding_episodes(session) -> list[dict]:
    rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == EVENT_KIND
    ]
    bindings = []
    for row in rows:
        body = dict(row.get("body") or {})
        binding = body.get("binding")
        if isinstance(binding, dict):
            bindings.append(binding)
    bindings.sort(key=lambda item: (item.get("event_ordinal", 0), item.get("event_time", 0)))
    return bindings


__all__ = [
    "BINDING_SCHEMA",
    "EVENT_KIND",
    "GRADE",
    "append_event_binding",
    "binding_episodes",
    "make_continuation_binding",
    "make_first_event_binding",
]
