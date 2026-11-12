"""Parent performed utterance, hidden reason, and Nadia-qualified uptake.

The parent is the C01 stable supporting actor. The performed speech is an actual
P2 SPEECH event; the hidden reason stays in a separate C12 utterance episode.
Nadia receives only her own C12 speech perception and the public projection.
No LLM, no co-presence-only perception, and no new owner/scheduler/ledger.
"""
from __future__ import annotations

from typing import Any, Mapping

from .contracts import RecursionRefusal, detached, digest
from .parent_activity import _parent_write_lock, _StoreWrite
from .parent_decision import (
    DECISION_GRADE, PARENT_DECISION_KIND, read_parent_decision,
)
from .supporting_actor import read_supporting_actor

PARENT_UTTERANCE_SCHEMA = "SOROK_PARENT_UTTERANCE@1"
PARENT_UTTERANCE_RECEIPT_SCHEMA = "SOROK_PARENT_UTTERANCE_RECEIPT@1"
PARENT_UTTERANCE_KIND = "P2_PARENT_UTTERANCE"
CHILD_UPTAKE_SCHEMA = "SOROK_CHILD_SPEECH_UPTAKE@1"
UTTERANCE_GRADE = "SOURCEFREE_S2_ONLY"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scalar(value: Any) -> bool:
    return type(value) in (bool, int, str)


def _hidden_reason(value: Any) -> dict:
    if value is None:
        return {}
    if not isinstance(value, Mapping) or any(
            not _text(key) or not _scalar(item) for key, item in value.items()):
        raise RecursionRefusal("PARENT_UTTERANCE_HIDDEN_REASON_SCHEMA")
    return detached(value)


def _utterance_episodes(session, alias: str, operation_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias
        and row.get("kind") == PARENT_UTTERANCE_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    ]


def _child_alias(session, child_id: str) -> str | None:
    root_ids = tuple(session.read_root()["actor_ids"])
    if child_id not in root_ids:
        raise RecursionRefusal("PARENT_UTTERANCE_CHILD_NOT_FOCAL")
    for alias, row in session.world().actor_state.items():
        if isinstance(row, Mapping) and row.get("actor_id") == child_id:
            return alias
    return None


def _decision_body(session, parent_id: str, alias: str,
                   decision_id: str) -> dict:
    episodes = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias
        and row.get("kind") == PARENT_DECISION_KIND
        and (row.get("body") or {}).get("decision_id") == decision_id
    ]
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_UTTERANCE_DECISION_NOT_FOUND")
    body = episodes[0].get("body") or {}
    if body.get("actor_id") != parent_id or body.get("alias") != alias:
        raise RecursionRefusal("PARENT_UTTERANCE_DECISION_SEVERED")
    return body


def perform_parent_utterance(session, parent_id: str, *, decision_id: str,
                             text: str, hidden_reason: Any,
                             operation_id: str) -> dict:
    if not _text(text) or not _text(decision_id) or not _text(operation_id):
        raise RecursionRefusal("PARENT_UTTERANCE_SCHEMA")
    hidden = _hidden_reason(hidden_reason)
    hidden_hash = digest(hidden)
    registration = read_supporting_actor(session, parent_id)
    alias = registration["alias"]
    with _parent_write_lock(session):
        # The decision is the prior parent choice; the utterance cannot create
        # a decision or speak for a parent with no admitted decision.
        decision = read_parent_decision(
            session, parent_id, decision_id, as_actor=parent_id)
        existing = _utterance_episodes(session, alias, operation_id)
        if len(existing) > 1:
            raise RecursionRefusal("PARENT_UTTERANCE_DUPLICATE")
        if existing:
            body = existing[0].get("body") or {}
            if (body.get("actor_id") != parent_id
                    or body.get("decision_id") != decision_id
                    or body.get("text") != text
                    or body.get("hidden_reason_hash") != hidden_hash):
                raise RecursionRefusal("PARENT_UTTERANCE_REUSE_MISMATCH")
            receipt = dict(body.get("receipt") or {})
            receipt["status"] = "REPLAY"
            return receipt
        period_context = detached(
            ((decision.get("proposal") or {}).get("evaluation") or {}).get(
                "period_context") or {})
        world = session.world()
        location = world.positions.get(alias)
        if not _text(location):
            raise RecursionRefusal("PARENT_UTTERANCE_POSITION_MISSING")
        child_id = session.read_root()["actor_ids"][0]
        child_alias = _child_alias(session, child_id)
        utterance_source = digest({
            "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
            "operation_id": operation_id,
            "decision_id": decision_id,
            "actor_id": parent_id,
            "text": text,
            "clock": world.clock,
        })
        from bp4.world import make_event
        event = make_event(
            clock=world.clock, kind="SPEECH", actor_id=alias,
            location=location, summary=f"{alias} says: {text}",
            body={"text": text, "observable": True,
                  "utterance_source": utterance_source,
                  "decision_id": decision_id},
            sequence=len(world.events),
        )
        world.add_event(event)
        child_perception = (
            child_alias is not None and child_alias != alias
            and world.positions.get(child_alias) == location)
        receipt = {
            "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
            "grade": UTTERANCE_GRADE,
            "status": "ADMITTED",
            "operation_id": operation_id,
            "decision_id": decision_id,
            "actor_id": parent_id,
            "alias": alias,
            "root": session.read_root()["root_hash"],
            "branch": session.branch_id,
            "clock": world.clock,
            "event_id": event["event_id"],
            "event_hash": event["hash"],
            "event_kind": event["kind"],
            "event_authored_by": alias,
            "text": text,
            "hidden_reason": "NOT_READ",
            "hidden_reason_hash": hidden_hash,
            "child_actor_id": child_id,
            "child_alias": child_alias,
            "child_perception_channel": (
                "speech" if child_perception else "NOT_PERCEIVED"),
            "decision_action": (decision.get("decision") or {}).get("action"),
            "period_context": period_context,
            "private_state": "SELF_ONLY_HIDDEN_REASON",
            "public_utterance": True,
        }
        store = session.product.store
        with _StoreWrite(store):
            store.append_world_event(session.branch_id, event)
            store.record_perception(
                session.branch_id, actor_id=alias, event_id=event["event_id"],
                clock=world.clock, channel="own_speech")
            if child_perception:
                store.record_perception(
                    session.branch_id, actor_id=child_alias,
                    event_id=event["event_id"], clock=world.clock,
                    channel="speech")
            store.append_episode(
                session.branch_id, actor_id=alias,
                kind=PARENT_UTTERANCE_KIND, clock=world.clock,
                body={
                    "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
                    "grade": UTTERANCE_GRADE,
                    "root": session.read_root()["root_hash"],
                    "branch": session.branch_id,
                    "actor_id": parent_id,
                    "alias": alias,
                    "operation_id": operation_id,
                    "decision_id": decision_id,
                    "text": text,
                    "hidden_reason": hidden,
                    "hidden_reason_hash": hidden_hash,
                    "event_id": event["event_id"],
                    "event_hash": event["hash"],
                    "child_actor_id": child_id,
                    "child_alias": child_alias,
                    "child_perception_channel": receipt["child_perception_channel"],
                    "decision_action": receipt["decision_action"],
                    "period_context": period_context,
                    "receipt": receipt,
                },
            )
            session.product._checkpoint(session.branch_id, world.clock, world)
        return receipt


def read_parent_utterance(session, parent_id: str, operation_id: str, *,
                          as_actor: str | None = None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    registration = read_supporting_actor(session, parent_id)
    alias = registration["alias"]
    episodes = _utterance_episodes(session, alias, operation_id)
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_UTTERANCE_NOT_FOUND")
    body = episodes[0].get("body") or {}
    if body.get("actor_id") != parent_id or body.get("alias") != alias:
        raise RecursionRefusal("PARENT_UTTERANCE_SEVERED")
    event = session.event(body.get("event_id") or "")
    if not event or event.get("hash") != body.get("event_hash"):
        raise RecursionRefusal("PARENT_UTTERANCE_EVENT_SEVERED")
    from s45_projection.projection import project_event
    projected = project_event(event)
    projected.pop("perceived_by_user", None)
    receipt = dict(body.get("receipt") or {})
    return {
        "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
        "grade": UTTERANCE_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "operation_id": operation_id,
        "decision_id": body.get("decision_id"),
        "clock": episodes[0]["clock"],
        "event": projected,
        "hidden_reason": detached(body.get("hidden_reason") or {}),
        "hidden_reason_hash": body.get("hidden_reason_hash"),
        "period_context": detached(body.get("period_context") or {}),
        "receipt": receipt,
        "private_state": "SELF_ONLY_HIDDEN_REASON",
    }


def read_child_uptake(session, child_id: str, event_id: str) -> dict:
    if not _text(child_id) or not _text(event_id):
        raise RecursionRefusal("CHILD_UPTAKE_SCHEMA")
    child_alias = _child_alias(session, child_id)
    if child_alias is None:
        raise RecursionRefusal("CHILD_UPTAKE_ALIAS_UNAVAILABLE")
    utterances = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == PARENT_UTTERANCE_KIND
        and (row.get("body") or {}).get("event_id") == event_id
    ]
    if len(utterances) != 1:
        raise RecursionRefusal("CHILD_UPTAKE_UTTERANCE_NOT_FOUND")
    utterance = utterances[0].get("body") or {}
    if (utterance.get("child_actor_id") != child_id
            or utterance.get("event_hash") is None):
        raise RecursionRefusal("CHILD_UPTAKE_UTTERANCE_MISMATCH")
    event = session.event(event_id)
    if not event:
        raise RecursionRefusal("CHILD_UPTAKE_EVENT_SEVERED")
    if (event.get("kind") != "SPEECH"
            or event.get("hash") != utterance.get("event_hash")
            or event.get("actor_id") != utterance.get("alias")):
        raise RecursionRefusal("CHILD_UPTAKE_NOT_SPEECH")
    receipt = next((
        row for row in session.product.store.perceptions(
            session.branch_id, actor_id=child_alias)
        if row.get("event_id") == event_id
    ), None)
    base = {
        "schema": CHILD_UPTAKE_SCHEMA,
        "grade": UTTERANCE_GRADE,
        "child_actor_id": child_id,
        "child_alias": child_alias,
        "event_id": event_id,
        "hidden_reason": "NOT_READ",
        "private_state": "NOT_READ",
    }
    if receipt is None:
        return {**base, "status": "NOT_PERCEIVED", "event": None}
    if (receipt.get("channel") != "speech"
            or receipt.get("clock") != event.get("clock")):
        raise RecursionRefusal("CHILD_UPTAKE_RECEIPT_MISMATCH")
    from s45_projection.projection import project_event
    project = project_event(event)
    project.pop("perceived_by_user", None)
    return {
        **base,
        "status": "PERCEIVED",
        "event": project,
        "receipt": {
            "clock": receipt.get("clock"),
            "channel": receipt.get("channel"),
        },
    }
