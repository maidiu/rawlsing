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
CHILD_EXPERIENCE_SCHEMA = "SOROK_CHILD_SPEECH_EXPERIENCE@1"
CHILD_RESPONSE_INPUT_SCHEMA = "SOROK_CHILD_SPEECH_RESPONSE_INPUT@1"
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



def _verify_world_event_seal(event: Mapping[str, Any], *, refusal: str) -> None:
    """Verify BP4's event hash AND event-ID content address before consumption.

    BP4's existing make_event derives the ID from the complete base, then
    hashes that ID plus the base. Merely matching the stored episode hash
    would accept altered public summary, location, observable flag or sequence
    with a copied stale hash. This is read-only sourcefree custody, not a new
    world writer, scientific rule or actor authorization.
    """
    from bp4.world import EVENT_SCHEMA, WORLD_GRADE
    try:
        document = detached(event)
        if (not isinstance(document, dict)
                or document.get("schema") != EVENT_SCHEMA
                or document.get("grade") != WORLD_GRADE
                or document.get("native") is not False):
            raise RecursionRefusal(refusal)
        recorded_hash = document.pop("hash", None)
        if not _text(recorded_hash) or recorded_hash != digest(document):
            raise RecursionRefusal(refusal)
        recorded_id = document.pop("event_id", None)
        if (not _text(recorded_id)
                or recorded_id != "TEST_ONLY_BP4_WORLD_EVT_" + digest(document)):
            raise RecursionRefusal(refusal)
    except (TypeError, ValueError) as exc:
        raise RecursionRefusal(refusal) from exc


def _verify_utterance_custody(session, body: Mapping[str, Any],
                              episode_clock: int, *, parent_id: str,
                              alias: str) -> dict:
    """Re-derive C04 event and perception custody before replay/self-read.

    A stored episode alone must never authorize replay of a severed event.
    Historical child presence is the admission-time receipt, not her current
    position. This is custody checking, not native actor/language authority.
    """
    root = session.read_root()["root_hash"]
    event_id = body.get("event_id")
    event_hash = body.get("event_hash")
    receipt = body.get("receipt") or {}
    if (body.get("root") != root or body.get("branch") != session.branch_id
            or body.get("actor_id") != parent_id
            or body.get("alias") != alias
            or not _text(body.get("operation_id"))
            or not _text(body.get("decision_id"))
            or not _text(body.get("text"))
            or not _text(event_id) or not _text(event_hash)):
        raise RecursionRefusal("PARENT_UTTERANCE_CUSTODY_SEVERED")
    event = session.event(event_id)
    if (not isinstance(event, Mapping)
            or event.get("event_id") != event_id
            or event.get("hash") != event_hash
            or event.get("kind") != "SPEECH"
            or event.get("actor_id") != alias
            or event.get("clock") != episode_clock
            or (event.get("body") or {}).get("text") != body["text"]
            or (event.get("body") or {}).get("decision_id")
                != body["decision_id"]):
        raise RecursionRefusal("PARENT_UTTERANCE_EVENT_SEVERED")
    expected_source = digest({
        "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
        "operation_id": body["operation_id"],
        "decision_id": body["decision_id"],
        "actor_id": parent_id,
        "text": body["text"],
        "clock": episode_clock,
    })
    if (event.get("body") or {}).get("utterance_source") != expected_source:
        raise RecursionRefusal("PARENT_UTTERANCE_SOURCE_SEVERED")
    if (receipt.get("event_id") != event_id
            or receipt.get("event_hash") != event_hash
            or receipt.get("event_kind") != event.get("kind")
            or receipt.get("event_authored_by") != alias
            or receipt.get("actor_id") != parent_id
            or receipt.get("root") != root
            or receipt.get("branch") != session.branch_id
            or receipt.get("clock") != episode_clock
            or receipt.get("decision_id") != body["decision_id"]
            or receipt.get("text") != body["text"]
            or receipt.get("hidden_reason") != "NOT_READ"
            or receipt.get("decision_action") != body.get("decision_action")
            or receipt.get("public_utterance") is not True
            or receipt.get("hidden_reason_hash")
                != body.get("hidden_reason_hash")):
        raise RecursionRefusal("PARENT_UTTERANCE_RECEIPT_SEVERED")
    own = [
        p for p in session.product.store.perceptions(session.branch_id, alias)
        if p.get("event_id") == event_id and p.get("clock") == episode_clock
        and p.get("channel") == "own_speech"
    ]
    if len(own) != 1:
        raise RecursionRefusal("PARENT_UTTERANCE_OWN_SPEECH_SEVERED")
    child_id = body.get("child_actor_id")
    if not _text(child_id):
        raise RecursionRefusal("PARENT_UTTERANCE_CHILD_ID_SEVERED")
    child_alias = _child_alias(session, child_id)
    if child_alias != body.get("child_alias"):
        raise RecursionRefusal("PARENT_UTTERANCE_CHILD_ALIAS_SEVERED")
    seen = [] if child_alias is None else [
        p for p in session.product.store.perceptions(session.branch_id, child_alias)
        if p.get("event_id") == event_id and p.get("clock") == episode_clock
        and p.get("channel") == "speech"
    ]
    channel = body.get("child_perception_channel")
    if (channel == "speech" and len(seen) != 1
            or channel == "NOT_PERCEIVED" and len(seen) != 0
            or channel not in {"speech", "NOT_PERCEIVED"}
            or receipt.get("child_perception_channel") != channel):
        raise RecursionRefusal("PARENT_UTTERANCE_CHILD_RECEIPT_SEVERED")
    _verify_world_event_seal(
        event, refusal="PARENT_UTTERANCE_WORLD_EVENT_UNSEALED")
    return dict(event)



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
            _verify_utterance_custody(
                session, body, existing[0]["clock"],
                parent_id=parent_id, alias=alias)
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
            "text_source": "CALLER_SUPPLIED_NOT_GENERATED",
            "hidden_reason_source": "CALLER_SUPPLIED_NOT_GENERATED",
            "language_generation_owner": "NOT_IMPLEMENTED",
            "physical_admission": "SPEECH_EVENT_COMMITTED",
            "custody": "C12_SPEECH_RECEIPT_NOT_MEMORY",
            "durable_acquisition": "MISSING_RULE",
            "native_science": False,
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
    event = _verify_utterance_custody(
        session, body, episodes[0]["clock"],
        parent_id=parent_id, alias=alias)
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


def _utterance_by_event_or_operation(session, *, event_id=None,
                                       operation_id=None) -> dict:
    # Two selectors identify the SAME occurrence, not competing alternatives.
    # Previously OR would silently ignore a wrong/nonexistent selector and
    # return the event identified by the other one.
    if ((event_id is not None and not _text(event_id))
            or (operation_id is not None and not _text(operation_id))
            or (event_id is None and operation_id is None)):
        raise RecursionRefusal("CHILD_EXPERIENCE_SELECTOR_SCHEMA")
    rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == PARENT_UTTERANCE_KIND
        and (event_id is None
             or (row.get("body") or {}).get("event_id") == event_id)
        and (operation_id is None
             or (row.get("body") or {}).get("operation_id") == operation_id)
    ]
    if len(rows) != 1:
        raise RecursionRefusal("CHILD_EXPERIENCE_UTTERANCE_NOT_FOUND")
    return rows[0]


def read_child_experience(session, child_id: str, *, event_id: str | None = None,
                          operation_id: str | None = None) -> dict:
    """Compile Nadia's qualified current speech experience and response input.

    This consumes the actual committed speech event and the child's own C12
    speech perception. It is not a memory/durable-acquisition claim and never
    reads the parent hidden reason. The experimental access condition is
    bounded same-room registration by the existing speech writer; the C12
    speech receipt remains the access owner.
    """
    if not _text(child_id) or (event_id is None and operation_id is None):
        raise RecursionRefusal("CHILD_EXPERIENCE_SCHEMA")
    episode = _utterance_by_event_or_operation(
        session, event_id=event_id, operation_id=operation_id)
    body = episode.get("body") or {}
    event_id = body.get("event_id")
    if not _text(event_id):
        raise RecursionRefusal("CHILD_EXPERIENCE_UTTERANCE_MISMATCH")
    child_alias = _child_alias(session, child_id)
    if child_alias is None:
        raise RecursionRefusal("CHILD_EXPERIENCE_ALIAS_UNAVAILABLE")
    root = session.read_root()["root_hash"]
    if (body.get("root") != root or body.get("branch") != session.branch_id
            or body.get("child_actor_id") != child_id
            or body.get("child_alias") != child_alias
            or not _text(body.get("actor_id"))
            or not _text(body.get("alias"))
            or not _text(body.get("text"))):
        raise RecursionRefusal("CHILD_EXPERIENCE_UTTERANCE_MISMATCH")
    parent_id, parent_alias = body["actor_id"], body["alias"]
    event = session.event(event_id)
    if not event:
        raise RecursionRefusal("CHILD_UPTAKE_EVENT_SEVERED")
    if (event.get("kind") != "SPEECH"
            or event.get("hash") != body.get("event_hash")
            or event.get("actor_id") != parent_alias
            or event.get("clock") != episode.get("clock")
            or (event.get("body") or {}).get("text") != body.get("text")):
        raise RecursionRefusal("CHILD_EXPERIENCE_EVENT_MISMATCH")
    expected_source = digest({
        "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
        "operation_id": body.get("operation_id"),
        "decision_id": body.get("decision_id"),
        "actor_id": parent_id,
        "text": body.get("text"),
        "clock": event.get("clock"),
    })
    if (event.get("body") or {}).get("utterance_source") != expected_source:
        raise RecursionRefusal("CHILD_EXPERIENCE_SOURCE_MISMATCH")
    _verify_world_event_seal(
        event, refusal="CHILD_EXPERIENCE_WORLD_EVENT_UNSEALED")
    own_speech = next((
        row for row in session.product.store.perceptions(session.branch_id, parent_alias)
        if row.get("event_id") == event_id
        and row.get("channel") == "own_speech"
        and row.get("clock") == event.get("clock")
    ), None)
    if own_speech is None:
        raise RecursionRefusal("CHILD_EXPERIENCE_PARENT_RECEIPT_MISSING")
    uptake = read_child_uptake(session, child_id, event_id)
    base = {
        "schema": CHILD_EXPERIENCE_SCHEMA,
        "grade": UTTERANCE_GRADE,
        "child_actor_id": child_id,
        "child_alias": child_alias,
        "speaker_actor_id": parent_id,
        "speaker_alias": parent_alias,
        "event_id": event_id,
        "event_hash": event.get("hash"),
        "occurrence_clock": event.get("clock"),
        "read_clock": session.clock(),
        "hidden_reason": "NOT_READ",
        "private_state": "NOT_READ",
        "custody": "C12_SPEECH_RECEIPT_NOT_MEMORY",
        "durable_acquisition": "MISSING_RULE",
        "native_science": False,
        "access_condition": "SAME_ROOM_AT_ADMISSION",
        "access_owner": "C12_SPEECH_PERCEPTION_RECEIPT",
        "user_view": "NOT_EXPOSED",
        "text_source": "CALLER_SUPPLIED_NOT_GENERATED",
        "language_generation_owner": "NOT_IMPLEMENTED",
    }
    expected_channel = body.get("child_perception_channel")
    if uptake.get("status") != "PERCEIVED":
        if expected_channel == "speech":
            raise RecursionRefusal("CHILD_EXPERIENCE_PERCEPTION_SEVERED")
        return {**base, "status": "NOT_PERCEIVED", "event": None,
                "response_input": None}
    if expected_channel != "speech":
        raise RecursionRefusal("CHILD_EXPERIENCE_PERCEPTION_MISMATCH")
    if uptake["receipt"]["clock"] != event.get("clock"):
        raise RecursionRefusal("CHILD_EXPERIENCE_PERCEPTION_CLOCK_MISMATCH")
    decision_rows = [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == PARENT_DECISION_KIND
        and (row.get("body") or {}).get("decision_id") == body.get("decision_id")
        and (row.get("body") or {}).get("actor_id") == parent_id
        and (row.get("body") or {}).get("alias") == parent_alias
        and (row.get("body") or {}).get("root") == root
        and (row.get("body") or {}).get("branch") == session.branch_id
    ]
    if len(decision_rows) != 1:
        raise RecursionRefusal("CHILD_EXPERIENCE_DECISION_SEVERED")
    decision = (decision_rows[0].get("body") or {}).get("decision") or {}
    if decision.get("action") != body.get("decision_action"):
        raise RecursionRefusal("CHILD_EXPERIENCE_DECISION_MISMATCH")
    public_event = dict(uptake["event"])
    response_input = {
        "schema": CHILD_RESPONSE_INPUT_SCHEMA,
        "grade": UTTERANCE_GRADE,
        "event_id": event_id,
        "event_hash": event.get("hash"),
        "speaker_actor_id": parent_id,
        "speaker_alias": parent_alias,
        "child_actor_id": child_id,
        "child_alias": child_alias,
        "public_text": body.get("text"),
        "occurrence_clock": event.get("clock"),
        "read_clock": session.clock(),
        "perception_clock": uptake["receipt"]["clock"],
        "perception_channel": uptake["receipt"]["channel"],
        "access_condition": "SAME_ROOM_AT_ADMISSION",
        "access_owner": "C12_SPEECH_PERCEPTION_RECEIPT",
        "hidden_reason": "NOT_READ",
        "decision_state": "NOT_READ",
        "custody": "C12_SPEECH_RECEIPT_NOT_MEMORY",
        "durable_acquisition": "MISSING_RULE",
        "native_science": False,
        "text_source": "CALLER_SUPPLIED_NOT_GENERATED",
        "language_generation_owner": "NOT_IMPLEMENTED",
    }
    return {
        **base,
        "status": "PERCEIVED",
        "event": public_event,
        "receipt": dict(uptake["receipt"]),
        "response_input": response_input,
    }


def read_child_uptake(session, child_id: str, event_id: str) -> dict:
    """Read a genuinely admitted parent speech relative to this child.

    Event self-hashing is necessary but not sufficient: the stored speech
    episode and admission-time perception channel must agree with the event
    and actor's actual C12 receipts. Otherwise a missing receipt must not be
    mistaken for an originally unheard utterance, or a forged receipt used
    to invent historical access. This is read-only sourcefree custody.
    """
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
    episode = utterances[0]
    utterance = episode.get("body") or {}
    parent_id = utterance.get("actor_id")
    parent_alias = utterance.get("alias")
    root = session.read_root()["root_hash"]
    channel = utterance.get("child_perception_channel")
    receipt_body = utterance.get("receipt") or {}
    if (utterance.get("root") != root
            or utterance.get("branch") != session.branch_id
            or utterance.get("child_actor_id") != child_id
            or utterance.get("child_alias") != child_alias
            or not _text(parent_id) or not _text(parent_alias)
            or not _text(utterance.get("decision_id"))
            or not _text(utterance.get("operation_id"))
            or not _text(utterance.get("text"))
            or channel not in {"speech", "NOT_PERCEIVED"}
            or not isinstance(receipt_body, Mapping)
            or receipt_body.get("schema") != PARENT_UTTERANCE_RECEIPT_SCHEMA
            or receipt_body.get("status") != "ADMITTED"
            or receipt_body.get("root") != root
            or receipt_body.get("branch") != session.branch_id
            or receipt_body.get("actor_id") != parent_id
            or receipt_body.get("alias") != parent_alias
            or receipt_body.get("child_actor_id") != child_id
            or receipt_body.get("child_alias") != child_alias
            or receipt_body.get("child_perception_channel") != channel
            or receipt_body.get("event_id") != event_id
            or receipt_body.get("event_hash") != utterance.get("event_hash")
            or receipt_body.get("event_kind") != "SPEECH"
            or receipt_body.get("event_authored_by") != parent_alias
            or receipt_body.get("decision_id") != utterance["decision_id"]
            or receipt_body.get("operation_id") != utterance["operation_id"]
            or receipt_body.get("clock") != episode.get("clock")
            or receipt_body.get("text") != utterance["text"]
            or receipt_body.get("hidden_reason") != "NOT_READ"
            or receipt_body.get("hidden_reason_hash")
                != utterance.get("hidden_reason_hash")
            or receipt_body.get("decision_action")
                != utterance.get("decision_action")
            or receipt_body.get("public_utterance") is not True):
        raise RecursionRefusal("CHILD_UPTAKE_UTTERANCE_MISMATCH")
    event = session.event(event_id)
    if not event:
        raise RecursionRefusal("CHILD_UPTAKE_EVENT_SEVERED")
    if (event.get("event_id") != event_id
            or event.get("kind") != "SPEECH"
            or event.get("hash") != utterance.get("event_hash")
            or event.get("actor_id") != parent_alias
            or event.get("clock") != episode.get("clock")
            or (event.get("body") or {}).get("text") != utterance["text"]
            or (event.get("body") or {}).get("decision_id")
                != utterance["decision_id"]):
        raise RecursionRefusal("CHILD_UPTAKE_NOT_SPEECH")
    expected_source = digest({
        "schema": PARENT_UTTERANCE_RECEIPT_SCHEMA,
        "operation_id": utterance["operation_id"],
        "decision_id": utterance["decision_id"],
        "actor_id": parent_id,
        "text": utterance["text"],
        "clock": episode["clock"],
    })
    if (event.get("body") or {}).get("utterance_source") != expected_source:
        raise RecursionRefusal("CHILD_UPTAKE_SOURCE_SEVERED")
    # Preserve B's complete BP4 event seal (content hash plus event-ID hash).
    _verify_world_event_seal(
        event, refusal="CHILD_UPTAKE_WORLD_EVENT_UNSEALED")
    own = [
        row for row in session.product.store.perceptions(
            session.branch_id, actor_id=parent_alias)
        if row.get("event_id") == event_id
        and row.get("clock") == episode["clock"]
        and row.get("channel") == "own_speech"
    ]
    if len(own) != 1:
        raise RecursionRefusal("CHILD_UPTAKE_PARENT_RECEIPT_SEVERED")
    child_receipts = [
        row for row in session.product.store.perceptions(
            session.branch_id, actor_id=child_alias)
        if row.get("event_id") == event_id
    ]
    # The receipt stored AT ADMISSION controls whether she originally heard.
    # Missing a historically present receipt is severance, not NONPERCEPTION.
    if channel == "speech" and len(child_receipts) == 0:
        raise RecursionRefusal("CHILD_UPTAKE_PERCEPTION_SEVERED")
    if channel == "NOT_PERCEIVED" and child_receipts:
        raise RecursionRefusal("CHILD_UPTAKE_FALSE_PERCEPTION")
    if len(child_receipts) > 1:
        raise RecursionRefusal("CHILD_UPTAKE_RECEIPT_DUPLICATE")
    base = {
        "schema": CHILD_UPTAKE_SCHEMA,
        "grade": UTTERANCE_GRADE,
        "child_actor_id": child_id,
        "child_alias": child_alias,
        "event_id": event_id,
        "hidden_reason": "NOT_READ",
        "private_state": "NOT_READ",
    }
    if channel == "NOT_PERCEIVED":
        return {**base, "status": "NOT_PERCEIVED", "event": None}
    receipt = child_receipts[0]
    if (receipt.get("channel") != "speech"
            or receipt.get("clock") != episode["clock"]):
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
