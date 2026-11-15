"""Dated continuing relations and variable-depth relation context over C12/P2.

C05 adds only the missing carrier between the accepted C01 supporting actors and
an ordinary later consumer. A caller supplies one illustrative dated relation
change (enter/leave/change) and an operation ID; this module never selects an
act, invents a motive, generates speech, or decides psychological meaning. The
change is an append-only C12 episode in the existing branch, with a companion
C12 custody head so a severed relation history is detectable at the consumer.

A relation is a dated fact over two live root/supporting actor IDs. Exposure is
explicit: only actors named on an entry can see that entry through these
readers. Physical co-presence is not consulted and is not knowledge. A later
real P2 world event is read through the existing C01 ``read_actor_access``; the
consumer then combines that actor-relative event access with only the dated
relation entries the actor was exposed to. An unexposed or partially exposed
scope is a qualified HOLD, never a negative proof that no relation exists.

This is sourcefree engineering at ``SOURCEFREE_S2_ONLY``, not native ADP-015/C4
relation authority, household membership, genealogy, psychology or autonomy.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from .contracts import RecursionRefusal, canonical, detached, digest
from .supporting_actor import _StoreWrite, resolve_participants

RELATION_CHANGE_KIND = "P2_CONTINUING_RELATION_CHANGE"
RELATION_HEAD_KIND = "P2_CONTINUING_RELATION_HEAD"
RELATION_CHANGE_SCHEMA = "SOROK_P2_CONTINUING_RELATION_CHANGE@1"
RELATION_HEAD_SCHEMA = "SOROK_P2_CONTINUING_RELATION_HEAD@1"
RELATION_READ_SCHEMA = "SOROK_P2_CONTINUING_RELATION_READ@1"
RELATION_CONTEXT_SCHEMA = "SOROK_P2_ACTOR_RELATIVE_CONTEXT@1"
RELATION_GRADE = "SOURCEFREE_S2_ONLY"
RELATION_STATE_CHANGES = frozenset({"ENTER", "LEAVE", "CHANGE"})
RELATION_CHANGES = RELATION_STATE_CHANGES | {"PROMOTE"}
RELATION_BASE_DEPTH = 1
RELATION_PROMOTED_DEPTH = 2
RELATION_PRIVATE = "NOT_READ"
RELATION_STATUS_QUALIFIED = "QUALIFIED"
RELATION_STATUS_NOT_EXPOSED = "HOLD_NOT_EXPOSED"
RELATION_STATUS_CUSTODY = "HOLD_CUSTODY_SEVERED"
RELATION_STATUS_UNKNOWN = "HOLD_UNKNOWN_SCOPE"


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scalar(value: Any) -> bool:
    return type(value) in (bool, int, str)


def _clock(value: Any, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RecursionRefusal(code)
    return value


def _private_state(value: Any) -> dict:
    if value is None:
        return {}
    if not isinstance(value, Mapping) or any(
            not _text(key) or not _scalar(item) for key, item in value.items()):
        raise RecursionRefusal("RELATION_PRIVATE_STATE_SCHEMA")
    return detached(value)


def _private_strings(private_state: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(value for value in private_state.values()
                 if isinstance(value, str) and value.strip())


def _refuse_private_leak(document: Mapping[str, Any],
                         private_state: Mapping[str, Any]) -> None:
    text = canonical(document)
    if any(value in text for value in _private_strings(private_state)):
        raise RecursionRefusal("RELATION_PRIVATE_STATE_LEAK")


def _relation_key(actor_ids: Iterable[str], relation: str) -> str:
    return digest({"actor_ids": list(actor_ids), "relation": relation})


def _resolve_live_actor(session, actor_ref: str, *,
                        code: str = "RELATION_ACTOR_UNKNOWN") -> dict:
    if not _text(actor_ref):
        raise RecursionRefusal(code)
    try:
        resolution = resolve_participants(session, (actor_ref,))
    except RecursionRefusal as exc:
        raise RecursionRefusal(code) from exc
    row = resolution["participants"][0]
    if row.get("actor_id") != actor_ref:
        raise RecursionRefusal(code)
    return {
        "actor_id": actor_ref,
        "alias": row["alias"],
        "kind": row["kind"],
        "role": row.get("role"),
    }


def _actor_pair(session, actor_id: str, other_actor_id: str) -> tuple[dict, dict]:
    first = _resolve_live_actor(session, actor_id)
    second = _resolve_live_actor(session, other_actor_id)
    if first["actor_id"] == second["actor_id"]:
        raise RecursionRefusal("RELATION_SELF_REFERENCE")
    pair = sorted((first, second), key=lambda row: row["actor_id"])
    return pair[0], pair[1]


def _exposure(session, pair: tuple[dict, dict],
              exposed_actor_ids: Any) -> tuple[list[str], list[str]]:
    party_ids = [pair[0]["actor_id"], pair[1]["actor_id"]]
    if exposed_actor_ids is None:
        values = tuple(party_ids)
    elif isinstance(exposed_actor_ids, (list, tuple)):
        values = tuple(exposed_actor_ids)
    else:
        raise RecursionRefusal("RELATION_EXPOSURE_SCHEMA")
    if (not values or any(not _text(value) for value in values)
            or len(set(values)) != len(values)):
        raise RecursionRefusal("RELATION_EXPOSURE_SCHEMA")
    resolved = {}
    for actor_ref in values:
        row = _resolve_live_actor(
            session, actor_ref, code="RELATION_EXPOSURE_ACTOR_UNKNOWN")
        resolved[row["actor_id"]] = row
    if not set(party_ids).issubset(resolved):
        raise RecursionRefusal("RELATION_EXPOSURE_MISSING_PARTY")
    ids = sorted(resolved)
    aliases = [resolved[actor_id]["alias"] for actor_id in ids]
    return ids, aliases


def relation_change_source(body: Mapping[str, Any]) -> str:
    """Content-address the public dated relation body, excluding its seal."""
    return digest({key: value for key, value in body.items()
                   if key not in {"source", "private_state"}})


def relation_head_source(body: Mapping[str, Any]) -> str:
    return digest({key: value for key, value in body.items()
                   if key != "source"})


def _public_body(body: Mapping[str, Any]) -> dict:
    return {key: detached(value) for key, value in body.items()
            if key not in {"private_state", "source"}}


def _history_entry(episode: Mapping[str, Any]) -> dict:
    body = episode.get("body") or {}
    return {
        "episode_id": episode["episode_id"],
        "episode_hash": episode["hash"],
        "clock": body["clock"],
        "change": body["change"],
        "value": body.get("value"),
        "operation_id": body["operation_id"],
    }


def _state_machine(changes: Iterable[Mapping[str, Any]]) -> dict:
    status, value = "ABSENT", None
    depth = RELATION_BASE_DEPTH
    for episode in changes:
        body = episode.get("body") or {}
        change = body.get("change")
        if change not in RELATION_CHANGES:
            raise RecursionRefusal("RELATION_CHANGE_INVALID")
        if change == "ENTER":
            if status not in {"ABSENT", "LEFT"}:
                raise RecursionRefusal("RELATION_ENTRY_INVALID")
            status, value = "ACTIVE", body.get("value")
        elif change == "CHANGE":
            if status not in {"ACTIVE", "CHANGED"}:
                raise RecursionRefusal("RELATION_CHANGE_INVALID")
            status, value = "CHANGED", body.get("value")
        elif change == "LEAVE":
            if status not in {"ACTIVE", "CHANGED"}:
                raise RecursionRefusal("RELATION_EXIT_INVALID")
            status, value = "LEFT", None
        else:
            if status == "ABSENT":
                raise RecursionRefusal("RELATION_PROMOTION_INVALID")
            promoted = body.get("promoted_depth")
            if (isinstance(promoted, bool) or not isinstance(promoted, int)
                    or promoted != RELATION_PROMOTED_DEPTH
                    or promoted <= depth):
                raise RecursionRefusal("RELATION_PROMOTION_INVALID")
            depth = promoted
    return {"status": status, "value": value, "depth": depth}


def _verify_change_body(session, episode: Mapping[str, Any], *,
                        expected_key: str) -> dict:
    body = episode.get("body") or {}
    root = session.read_root()["root_hash"]
    if (episode.get("kind") != RELATION_CHANGE_KIND
            or body.get("schema") != RELATION_CHANGE_SCHEMA
            or body.get("grade") != RELATION_GRADE
            or body.get("root") != root
            or body.get("branch") != session.branch_id
            or body.get("relation_key") != expected_key
            or body.get("change") not in RELATION_CHANGES
            or not _text(body.get("relation"))
            or not _text(body.get("operation_id"))
            or not isinstance(body.get("sequence"), int)
            or isinstance(body.get("sequence"), bool)
            or not isinstance(body.get("clock"), int)
            or isinstance(body.get("clock"), bool)
            or body.get("clock") != episode.get("clock")
            or not (body.get("previous_episode_id") is None
                    or _text(body.get("previous_episode_id")))
            or body.get("source") != relation_change_source(body)):
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    actor_ids = body.get("actor_ids")
    aliases = body.get("aliases")
    if (not isinstance(actor_ids, list) or len(actor_ids) != 2
            or not isinstance(aliases, list) or len(aliases) != 2
            or actor_ids != sorted(actor_ids)
            or any(not _text(value) for value in actor_ids + aliases)):
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    if _relation_key(actor_ids, body["relation"]) != expected_key:
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    for actor_id, alias in zip(actor_ids, aliases):
        row = _resolve_live_actor(
            session, actor_id, code="RELATION_CUSTODY_SEVERED")
        if row["alias"] != alias:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    exposed_ids = body.get("exposed_actor_ids")
    exposed_aliases = body.get("exposed_aliases")
    if (not isinstance(exposed_ids, list) or not exposed_ids
            or exposed_ids != sorted(set(exposed_ids))
            or not isinstance(exposed_aliases, list)
            or len(exposed_ids) != len(exposed_aliases)
            or not set(actor_ids).issubset(exposed_ids)):
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    for actor_id, alias in zip(exposed_ids, exposed_aliases):
        row = _resolve_live_actor(
            session, actor_id, code="RELATION_CUSTODY_SEVERED")
        if row["alias"] != alias:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    private_hash = body.get("private_state_hash")
    if not _text(private_hash) or len(private_hash) != 64:
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    try:
        int(private_hash, 16)
    except ValueError as exc:
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED") from exc
    private = _private_state(body.get("private_state"))
    if digest(private) != private_hash:
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    _refuse_private_leak(_public_body(body), private)
    if body["change"] == "PROMOTE":
        history_hash = body.get("history_hash")
        if (isinstance(body.get("promoted_depth"), bool)
                or not isinstance(body.get("promoted_depth"), int)
                or not _text(history_hash) or len(history_hash) != 64):
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        try:
            int(history_hash, 16)
        except ValueError as exc:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED") from exc
        if body.get("value") is not None:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    else:
        if body.get("promoted_depth") is not None:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        if body["change"] == "LEAVE" and body.get("value") is not None:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        value = body.get("value")
        if value is not None and not _scalar(value):
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    return body


def _verify_scope(session, key: str, changes: list[Mapping[str, Any]],
                  heads: list[Mapping[str, Any]]) -> dict:
    result = {
        "key": key,
        "status": "SEVERED",
        "reason": "RELATION_CUSTODY_SEVERED",
        "changes": changes,
        "heads": heads,
        "actor_ids": [],
        "aliases": [],
        "relation": "",
    }
    try:
        changes = sorted(changes, key=lambda row: (row.get("seq", -1),))
        heads = sorted(heads, key=lambda row: (row.get("seq", -1),))
        bodies = []
        for index, episode in enumerate(changes, start=1):
            body = _verify_change_body(session, episode, expected_key=key)
            if (body.get("sequence") != index
                    or body.get("previous_episode_id")
                    != (changes[index - 2]["episode_id"] if index > 1 else None)):
                raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
            bodies.append((episode, body))
        if not bodies:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        first_body = bodies[0][1]
        if first_body.get("actor_ids") != sorted(first_body["actor_ids"]):
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        if any(body.get("actor_ids") != first_body["actor_ids"]
               or body.get("relation") != first_body["relation"]
               for _episode, body in bodies):
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        _state_machine([episode for episode, _body in bodies])
        seen_heads = {}
        for index, episode in enumerate(heads, start=1):
            body = episode.get("body") or {}
            if (episode.get("kind") != RELATION_HEAD_KIND
                    or body.get("schema") != RELATION_HEAD_SCHEMA
                    or body.get("grade") != RELATION_GRADE
                    or body.get("root") != session.read_root()["root_hash"]
                    or body.get("branch") != session.branch_id
                    or body.get("relation_key") != key
                    or body.get("relation") != first_body.get("relation")
                    or body.get("sequence") != index
                    or body.get("previous_head_episode_id")
                    != (heads[index - 2]["episode_id"] if index > 1 else None)
                    or body.get("previous_head_hash")
                    != (heads[index - 2]["hash"] if index > 1 else None)
                    or body.get("source") != relation_head_source(body)):
                raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
            primary = changes[index - 1] if index <= len(changes) else None
            primary_body = bodies[index - 1][1] if index <= len(bodies) else {}
            if (primary is None
                    or body.get("primary_episode_id") != primary["episode_id"]
                    or body.get("primary_episode_hash") != primary["hash"]
                    or body.get("clock") != primary_body.get("clock")
                    or body.get("operation_id")
                    != primary_body.get("operation_id")
                    or body.get("actor_ids") != primary_body.get("actor_ids")
                    or body.get("aliases") != primary_body.get("aliases")
                    or body.get("exposed_actor_ids")
                    != primary_body.get("exposed_actor_ids")
                    or body.get("exposed_aliases")
                    != primary_body.get("exposed_aliases")):
                raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
            seen_heads[primary["episode_id"]] = body
        if len(heads) != len(changes) or set(seen_heads) != {
                episode["episode_id"] for episode, _body in bodies}:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        for index, (episode, body) in enumerate(bodies):
            if body["change"] != "PROMOTE":
                continue
            prior = [episode for episode, prior_body in bodies[:index]
                     if prior_body["change"] != "PROMOTE"]
            expected = digest([_history_entry(episode)
                               for episode in prior])
            if body.get("history_hash") != expected:
                raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        first = bodies[0][1]
        result.update(
            status="VERIFIED",
            reason="",
            actor_ids=list(first["actor_ids"]),
            aliases=list(first["aliases"]),
            relation=first["relation"],
        )
        return result
    except RecursionRefusal as exc:
        result["reason"] = str(exc) or "RELATION_CUSTODY_SEVERED"
        if changes:
            for episode in changes:
                body = episode.get("body") or {}
                if (isinstance(body.get("actor_ids"), list)
                        and len(body["actor_ids"]) == 2):
                    result["actor_ids"] = list(body["actor_ids"])
                    result["aliases"] = list(body.get("aliases") or [])
                    result["relation"] = body.get("relation") or ""
                    break
        if heads:
            for episode in heads:
                body = episode.get("body") or {}
                if (isinstance(body.get("actor_ids"), list)
                        and len(body["actor_ids"]) == 2):
                    result["actor_ids"] = list(body["actor_ids"])
                    result["aliases"] = list(body.get("aliases") or [])
                    result["relation"] = result["relation"] or body.get(
                        "relation", "")
                    break
        return result


def _scope_groups(session) -> tuple[dict, dict]:
    changes, heads = {}, {}
    for episode in session.product.store.episodes(session.branch_id):
        body = episode.get("body") or {}
        key = body.get("relation_key")
        if not _text(key):
            continue
        if episode.get("kind") == RELATION_CHANGE_KIND:
            changes.setdefault(key, []).append(episode)
        elif episode.get("kind") == RELATION_HEAD_KIND:
            heads.setdefault(key, []).append(episode)
    return changes, heads


def _all_scopes(session) -> dict[str, dict]:
    changes, heads = _scope_groups(session)
    keys = sorted(set(changes) | set(heads))
    return {
        key: _verify_scope(session, key, changes.get(key, []),
                           heads.get(key, []))
        for key in keys
    }


def _viewer_potentially_exposed(scope: Mapping[str, Any], actor_id: str,
                                 *, as_of_clock: int) -> bool:
    for group in (scope.get("changes") or (), scope.get("heads") or ()):
        for episode in group:
            body = episode.get("body") or {}
            clock = body.get("clock")
            if (isinstance(clock, bool) or not isinstance(clock, int)
                    or clock > as_of_clock):
                continue
            if (actor_id in (body.get("actor_ids") or ())
                    or actor_id in (body.get("exposed_actor_ids") or ())):
                return True
    return False


def _entry_document(episode: Mapping[str, Any]) -> dict:
    body = episode.get("body") or {}
    return {
        "episode_id": episode["episode_id"],
        "episode_hash": episode["hash"],
        "clock": body["clock"],
        "change": body["change"],
        "value": body.get("value"),
        "operation_id": body["operation_id"],
        "private_state": RELATION_PRIVATE,
    }


def _promotion_document(episode: Mapping[str, Any]) -> dict:
    body = episode.get("body") or {}
    return {
        "episode_id": episode["episode_id"],
        "episode_hash": episode["hash"],
        "clock": body["clock"],
        "depth": body["promoted_depth"],
        "history_hash": body["history_hash"],
        "operation_id": body["operation_id"],
    }


def _representation(scope: Mapping[str, Any], actor_id: str, *,
                    as_of_clock: int) -> dict | None:
    if scope.get("status") != "VERIFIED":
        return None
    changes = [
        episode for episode in scope.get("changes") or ()
        if (episode.get("body") or {}).get("clock") <= as_of_clock
    ]
    state_changes = [
        episode for episode in changes
        if (episode.get("body") or {}).get("change") in RELATION_STATE_CHANGES
    ]
    visible = [
        episode for episode in state_changes
        if actor_id in ((episode.get("body") or {}).get(
            "exposed_actor_ids") or ())
    ]
    if not visible:
        return None
    visible_ids = {episode["episode_id"] for episode in visible}
    complete = all(episode["episode_id"] in visible_ids
                   for episode in state_changes)
    machine = _state_machine(state_changes)
    if complete:
        status, value = machine["status"], machine["value"]
    else:
        last = visible[-1].get("body") or {}
        status = {
            "ENTER": "ACTIVE",
            "CHANGE": "CHANGED",
            "LEAVE": "LEFT",
        }[last["change"]]
        value = last.get("value")
    depth = max(
        [RELATION_BASE_DEPTH] + [
            (episode.get("body") or {})["promoted_depth"]
            for episode in changes
            if (episode.get("body") or {}).get("change") == "PROMOTE"
            and actor_id in ((episode.get("body") or {}).get(
                "exposed_actor_ids") or ())
        ]
    )
    visible_promotions = [
        _promotion_document(episode) for episode in changes
        if (episode.get("body") or {}).get("change") == "PROMOTE"
        and actor_id in ((episode.get("body") or {}).get(
            "exposed_actor_ids") or ())
    ]
    actor_ids = list(scope["actor_ids"])
    aliases = list(scope["aliases"])
    other_index = 1 if actor_ids[0] == actor_id else 0
    counterpart = {
        "actor_id": actor_ids[other_index],
        "alias": aliases[other_index],
    } if actor_id in actor_ids else None
    return {
        "relation": scope["relation"],
        "relation_key": scope["key"],
        "parties": [
            {"actor_id": actor_id_value, "alias": alias}
            for actor_id_value, alias in zip(actor_ids, aliases)
        ],
        "counterpart": counterpart,
        "viewer_is_party": actor_id in actor_ids,
        "status": status,
        "value": value,
        "history_complete": complete,
        "prior_exposure": (
            RELATION_STATUS_QUALIFIED if complete
            else RELATION_STATUS_NOT_EXPOSED
        ),
        "representation_depth": depth,
        "entries": [_entry_document(episode) for episode in visible],
        "promotions": visible_promotions,
        "visible_history_hash": digest(
            [_history_entry(episode) for episode in visible]),
        "private_state": RELATION_PRIVATE,
    }


def _history_envelope(session, actor_id: str, *,
                      other_actor_id: str | None = None,
                      relation: str | None = None,
                      as_of_clock: int) -> dict:
    scopes = _all_scopes(session)
    query_specified = other_actor_id is not None or relation is not None
    selected = scopes
    if query_specified:
        if not _text(other_actor_id) or not _text(relation):
            raise RecursionRefusal("RELATION_QUERY_SCHEMA")
        pair = _actor_pair(session, actor_id, other_actor_id)
        key = _relation_key(
            [pair[0]["actor_id"], pair[1]["actor_id"]], relation)
        selected = {key: scopes[key]} if key in scopes else {}
    relations, withheld, custody_severed = [], 0, False
    for key in sorted(selected):
        scope = selected[key]
        if scope.get("status") != "VERIFIED":
            if _viewer_potentially_exposed(
                    scope, actor_id, as_of_clock=as_of_clock):
                custody_severed = True
            else:
                withheld += 1
            continue
        representation = _representation(scope, actor_id,
                                         as_of_clock=as_of_clock)
        if representation is None:
            withheld += 1
        else:
            relations.append(representation)
    if query_specified and not selected:
        status = RELATION_STATUS_UNKNOWN
    elif custody_severed:
        status = RELATION_STATUS_CUSTODY
    elif relations:
        status = RELATION_STATUS_QUALIFIED
    else:
        status = RELATION_STATUS_NOT_EXPOSED
    return {
        "schema": RELATION_READ_SCHEMA,
        "grade": RELATION_GRADE,
        "viewer": _resolve_live_actor(
            session, actor_id, code="RELATION_ACTOR_UNKNOWN"),
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "as_of_clock": as_of_clock,
        "status": status,
        "custody": "SEVERED" if custody_severed else "VERIFIED",
        "relations": relations,
        "withheld_relation_count": withheld,
        "private_state": RELATION_PRIVATE,
        "native": False,
        "read_boundary": {
            "physical_copresence": "NOT_CONSULTED",
            "unexposed_scope": "QUALIFIED_HOLD",
            "private_state": "NEVER_RETURNED",
        },
    }


def read_relation_history(session, actor_id: str, *,
                          other_actor_id: str | None = None,
                          relation: str | None = None,
                          as_of_clock: int | None = None) -> dict:
    """Read dated relation history visible to exactly this actor.

    A missing or unexposed scope is a qualified HOLD, never a claim that no
    relation exists. A severed C12 relation chain returns a custody HOLD for a
    viewer who could have been exposed; an unexposed viewer is not told that an
    unseen relation exists.
    """
    if not _text(actor_id):
        raise RecursionRefusal("RELATION_ACTOR_UNKNOWN")
    world_clock = session.world().clock
    if as_of_clock is None:
        as_of = world_clock
    else:
        as_of = _clock(as_of_clock, "RELATION_AS_OF_SCHEMA")
        if as_of > world_clock:
            raise RecursionRefusal("RELATION_AS_OF_FUTURE")
    return _history_envelope(
        session, actor_id, other_actor_id=other_actor_id,
        relation=relation, as_of_clock=as_of,
    )


def _verify_world_event_seal(event: Mapping[str, Any]) -> None:
    """Verify the existing BP4 event hash and event-ID content address."""
    from bp4.world import EVENT_SCHEMA, WORLD_GRADE
    try:
        document = detached(event)
        if (not isinstance(document, dict)
                or document.get("schema") != EVENT_SCHEMA
                or document.get("grade") != WORLD_GRADE
                or document.get("native") is not False):
            raise RecursionRefusal("RELATION_EVENT_SEVERED")
        recorded_hash = document.pop("hash", None)
        if not _text(recorded_hash) or recorded_hash != digest(document):
            raise RecursionRefusal("RELATION_EVENT_SEVERED")
        recorded_id = document.pop("event_id", None)
        if (not _text(recorded_id)
                or recorded_id != "TEST_ONLY_BP4_WORLD_EVT_" + digest(document)):
            raise RecursionRefusal("RELATION_EVENT_SEVERED")
    except (TypeError, ValueError) as exc:
        raise RecursionRefusal("RELATION_EVENT_SEVERED") from exc


def _access_or_hold(session, actor_id: str, event_id: str) -> dict:
    from .supporting_actor import read_actor_access
    try:
        access = read_actor_access(session, actor_id, event_id)
    except RecursionRefusal as exc:
        return {
            "status": RELATION_STATUS_CUSTODY,
            "reason": str(exc) or "ACTOR_ACCESS_SEVERED",
            "event": None,
            "receipt": None,
        }
    return {
        "status": access.get("status"),
        "event": access.get("event"),
        "receipt": access.get("receipt"),
    }


def _context_effect(session, event_id: str,
                    history: Mapping[str, Any]) -> dict:
    if history.get("status") == RELATION_STATUS_CUSTODY:
        return {
            "relation_aware": False,
            "reason": RELATION_STATUS_CUSTODY,
            "basis": ["QUALIFIED_CUSTODY_HOLD"],
        }
    relations = history.get("relations") or []
    if not relations:
        return {
            "relation_aware": False,
            "reason": history.get("status"),
            "basis": ["QUALIFIED_HOLD"],
        }
    relation = relations[0]
    both = None
    if relation.get("viewer_is_party"):
        accesses = [
            _access_or_hold(session, party["actor_id"], event_id)["status"]
            for party in relation["parties"]
        ]
        both = all(status == "PERCEIVED" for status in accesses)
    return {
        "relation_aware": True,
        "reason": "QUALIFIED_RELATION_CONTEXT",
        "basis": [
            "DATED_RELATION_HISTORY",
            "C12_EVENT_PERCEPTION",
        ],
        "relation_status": relation.get("status"),
        "relation_value": relation.get("value"),
        "history_complete": relation.get("history_complete"),
        "representation_depth": relation.get("representation_depth"),
        "both_parties_event_access": both,
    }


def read_actor_relative_context(session, actor_id: str,
                                event_id: str) -> dict:
    """Terminal C05 consumer: one actor's later event plus relation context.

    The event is an actual existing-owner world event. Event access is the C01
    actor-relative C12 receipt path. Relation context is only the dated history
    this actor was exposed to. Physical co-presence is not relation knowledge.
    """
    if not _text(actor_id) or not _text(event_id):
        raise RecursionRefusal("RELATION_CONTEXT_SCHEMA")
    viewer = _resolve_live_actor(session, actor_id)
    event = session.event(event_id)
    if (not isinstance(event, Mapping) or not _text(event.get("hash"))
            or event.get("event_id") != event_id):
        raise RecursionRefusal("RELATION_EVENT_MISSING")
    _verify_world_event_seal(event)
    event_clock = _clock(event.get("clock"), "RELATION_EVENT_CLOCK_INVALID")
    access = _access_or_hold(session, actor_id, event_id)
    history = read_relation_history(
        session, actor_id, as_of_clock=event_clock)
    relation_scope = {
        "status": history["status"],
        "custody": history["custody"],
        "representation_depth": max(
            [relation.get("representation_depth", RELATION_BASE_DEPTH)
             for relation in history["relations"]]
            or [RELATION_BASE_DEPTH]
        ) if history["relations"] else 0,
        "relations": history["relations"],
        "withheld_relation_count": history["withheld_relation_count"],
    }
    return {
        "schema": RELATION_CONTEXT_SCHEMA,
        "grade": RELATION_GRADE,
        "viewer": viewer,
        "event_id": event_id,
        "event_clock": event_clock,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "event_access": access,
        "relation_scope": relation_scope,
        "context_effect": _context_effect(
            session, event_id, history),
        "private_state": RELATION_PRIVATE,
        "native": False,
        "read_boundary": {
            "event": "C01_ACTOR_RELATIVE_RECEIPT",
            "relation": "DATED_EXPOSURE_ONLY",
            "physical_copresence": "NOT_CONSULTED",
            "private_state": "NEVER_RETURNED",
        },
    }


def _request_body(session, *, actor_id: str, other_actor_id: str,
                  relation: str, change: str, clock: int, operation_id: str,
                  exposed_actor_ids: Any, value: Any,
                  private_state: Any) -> tuple[dict, dict]:
    if (not _text(relation) or change not in RELATION_CHANGES
            or not _text(operation_id)):
        raise RecursionRefusal("RELATION_CHANGE_SCHEMA")
    if change == "PROMOTE":
        raise RecursionRefusal("RELATION_PROMOTION_PATH_REQUIRED")
    if change == "LEAVE" and value is not None:
        raise RecursionRefusal("RELATION_EXIT_VALUE_INVALID")
    if value is not None and not _scalar(value):
        raise RecursionRefusal("RELATION_VALUE_SCHEMA")
    pair = _actor_pair(session, actor_id, other_actor_id)
    exposure_ids, exposure_aliases = _exposure(
        session, pair, exposed_actor_ids)
    private = _private_state(private_state)
    actor_ids = [pair[0]["actor_id"], pair[1]["actor_id"]]
    body = {
        "schema": RELATION_CHANGE_SCHEMA,
        "grade": RELATION_GRADE,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "relation_key": _relation_key(actor_ids, relation),
        "actor_ids": actor_ids,
        "aliases": [pair[0]["alias"], pair[1]["alias"]],
        "relation": relation,
        "change": change,
        "value": detached(value),
        "clock": clock,
        "operation_id": operation_id,
        "exposed_actor_ids": exposure_ids,
        "exposed_aliases": exposure_aliases,
        "private_state_hash": digest(private),
    }
    _refuse_private_leak(_public_body(body), private)
    return body, private


def _stored_request_matches(body: Mapping[str, Any],
                            request: Mapping[str, Any]) -> bool:
    keys = (
        "schema", "grade", "root", "branch", "relation_key", "actor_ids",
        "aliases", "relation", "change", "value", "clock", "operation_id",
        "exposed_actor_ids", "exposed_aliases", "private_state_hash",
        "promoted_depth", "history_hash",
    )
    return all(body.get(key) == request.get(key) for key in keys)


def _stored_promotion_matches(body: Mapping[str, Any],
                              request: Mapping[str, Any]) -> bool:
    keys = (
        "schema", "grade", "root", "branch", "relation_key", "actor_ids",
        "aliases", "relation", "change", "value", "clock", "operation_id",
        "promoted_depth",
    )
    return all(body.get(key) == request.get(key) for key in keys)


def _operation_episodes(session, operation_id: str) -> list[dict]:
    return [
        episode for episode in session.product.store.episodes(session.branch_id)
        if episode.get("kind") == RELATION_CHANGE_KIND
        and (episode.get("body") or {}).get("operation_id") == operation_id
    ]


def _head_for(session, primary_id: str) -> dict | None:
    rows = [
        episode for episode in session.product.store.episodes(session.branch_id)
        if episode.get("kind") == RELATION_HEAD_KIND
        and (episode.get("body") or {}).get("primary_episode_id") == primary_id
    ]
    if len(rows) > 1:
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    return rows[0] if rows else None


def _scope_for_key(session, key: str) -> dict | None:
    changes, heads = _scope_groups(session)
    if key not in changes and key not in heads:
        return None
    return _verify_scope(session, key, changes.get(key, []),
                         heads.get(key, []))


def _append_change(session, *, body: Mapping[str, Any], private: Mapping[str, Any],
                   key: str) -> dict:
    store = session.product.store
    body = detached(body)
    actor_id = body["aliases"][0]
    with _StoreWrite(store):
        changes, heads = _scope_groups(session)
        existing = sorted(
            changes.get(key, []), key=lambda row: row.get("seq", -1))
        previous = existing[-1] if existing else None
        previous_head = None
        if heads.get(key):
            previous_head = sorted(
                heads[key], key=lambda row: row.get("seq", -1))[-1]
        body["sequence"] = len(existing) + 1
        body["previous_episode_id"] = (
            previous["episode_id"] if previous is not None else None)
        body["private_state"] = detached(private)
        body["source"] = relation_change_source(body)
        primary = store.append_episode(
            session.branch_id, actor_id=actor_id,
            kind=RELATION_CHANGE_KIND, clock=body["clock"], body=body)
        head_body = {
            "schema": RELATION_HEAD_SCHEMA,
            "grade": RELATION_GRADE,
            "root": body["root"],
            "branch": body["branch"],
            "relation_key": key,
            "actor_ids": list(body["actor_ids"]),
            "aliases": list(body["aliases"]),
            "relation": body["relation"],
            "sequence": body["sequence"],
            "clock": body["clock"],
            "operation_id": body["operation_id"],
            "primary_episode_id": primary["episode_id"],
            "primary_episode_hash": primary["hash"],
            "previous_head_episode_id": (
                previous_head["episode_id"] if previous_head else None),
            "previous_head_hash": (
                previous_head["hash"] if previous_head else None),
            "exposed_actor_ids": list(body["exposed_actor_ids"]),
            "exposed_aliases": list(body["exposed_aliases"]),
        }
        head_body["source"] = relation_head_source(head_body)
        head = store.append_episode(
            session.branch_id, actor_id=actor_id,
            kind=RELATION_HEAD_KIND, clock=body["clock"], body=head_body)
    return {"primary": primary, "head": head}


def _record_result(session, *, key: str, primary: Mapping[str, Any],
                   head: Mapping[str, Any], status: str) -> dict:
    scope = _scope_for_key(session, key)
    if scope is None or scope.get("status") != "VERIFIED":
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    body = primary.get("body") or {}
    machine = _state_machine(scope["changes"])
    return {
        "schema": RELATION_READ_SCHEMA,
        "grade": RELATION_GRADE,
        "status": status,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": body["clock"],
        "relation": scope["relation"],
        "relation_key": key,
        "change": body["change"],
        "operation_id": body["operation_id"],
        "primary_episode_id": primary["episode_id"],
        "primary_episode_hash": primary["hash"],
        "head_episode_id": head["episode_id"],
        "head_episode_hash": head["hash"],
        "current_status": machine["status"],
        "current_value": machine["value"],
        "representation_depth": machine["depth"],
        "private_state": RELATION_PRIVATE,
        "native": False,
    }


def record_relation_change(session, *, actor_id: str, other_actor_id: str,
                           relation: str, change: str, clock: int,
                           operation_id: str,
                           exposed_actor_ids: Any = None,
                           value: Any = None,
                           private_state: Any = None) -> dict:
    """Append one caller-supplied dated relation change.

    This is not an autonomous actor choice. ``clock`` is the actual current P2
    world clock on first write; a future or backdated receipt is refused. The
    retry of an exact operation is idempotent. A changed operation reuse, a
    stranger identity, a missing party exposure, a private-value leak, or a
    severed prior relation chain is refused without a write.
    """
    clock = _clock(clock, "RELATION_CLOCK_SCHEMA")
    body, private = _request_body(
        session, actor_id=actor_id, other_actor_id=other_actor_id,
        relation=relation, change=change, clock=clock,
        operation_id=operation_id, exposed_actor_ids=exposed_actor_ids,
        value=value, private_state=private_state,
    )
    key = body["relation_key"]
    existing = _operation_episodes(session, operation_id)
    if existing:
        if len(existing) > 1:
            raise RecursionRefusal("RELATION_OPERATION_DUPLICATE")
        primary = existing[0]
        stored = primary.get("body") or {}
        if stored.get("relation_key") != key:
            raise RecursionRefusal("RELATION_OPERATION_REUSE_MISMATCH")
        scope = _scope_for_key(session, key)
        if scope is None or scope.get("status") != "VERIFIED":
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        _verify_change_body(session, primary, expected_key=key)
        if not _stored_request_matches(stored, body):
            raise RecursionRefusal("RELATION_OPERATION_REUSE_MISMATCH")
        head = _head_for(session, primary["episode_id"])
        if head is None:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        return _record_result(
            session, key=key, primary=primary, head=head, status="UNCHANGED")
    world_clock = session.world().clock
    if clock > world_clock:
        raise RecursionRefusal("RELATION_CLOCK_FUTURE")
    if clock < world_clock:
        raise RecursionRefusal("RELATION_CLOCK_BACKDATED")
    scope = _scope_for_key(session, key)
    if scope is not None and scope.get("status") != "VERIFIED":
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    prospective = [] if scope is None else [
        episode for episode in scope["changes"]
        if (episode.get("body") or {}).get("clock") <= clock
    ]
    prospective.append({
        "episode_id": "PENDING",
        "hash": "PENDING",
        "body": {**body, "sequence": len(prospective) + 1},
    })
    _state_machine(prospective)
    appended = _append_change(session, body=body, private=private, key=key)
    return _record_result(
        session, key=key, primary=appended["primary"],
        head=appended["head"], status="RECORDED")


def promote_relation(session, *, actor_id: str, other_actor_id: str,
                     relation: str, depth: int, clock: int,
                     operation_id: str) -> dict:
    """Deepen the future relation representation; never alter a dated entry."""
    clock = _clock(clock, "RELATION_CLOCK_SCHEMA")
    if (isinstance(depth, bool) or not isinstance(depth, int)
            or depth != RELATION_PROMOTED_DEPTH):
        raise RecursionRefusal("RELATION_PROMOTION_DEPTH")
    if not _text(relation) or not _text(operation_id):
        raise RecursionRefusal("RELATION_PROMOTION_SCHEMA")
    pair = _actor_pair(session, actor_id, other_actor_id)
    actor_ids = [pair[0]["actor_id"], pair[1]["actor_id"]]
    key = _relation_key(actor_ids, relation)
    existing = _operation_episodes(session, operation_id)
    request = {
        "schema": RELATION_CHANGE_SCHEMA,
        "grade": RELATION_GRADE,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "relation_key": key,
        "actor_ids": actor_ids,
        "aliases": [pair[0]["alias"], pair[1]["alias"]],
        "relation": relation,
        "change": "PROMOTE",
        "value": None,
        "clock": clock,
        "operation_id": operation_id,
        "promoted_depth": depth,
    }
    if existing:
        if len(existing) > 1:
            raise RecursionRefusal("RELATION_OPERATION_DUPLICATE")
        primary = existing[0]
        stored = primary.get("body") or {}
        scope = _scope_for_key(session, key)
        if scope is None or scope.get("status") != "VERIFIED":
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        _verify_change_body(session, primary, expected_key=key)
        if stored.get("change") != "PROMOTE":
            raise RecursionRefusal("RELATION_OPERATION_REUSE_MISMATCH")
        if not _stored_promotion_matches(stored, request):
            raise RecursionRefusal("RELATION_OPERATION_REUSE_MISMATCH")
        head = _head_for(session, primary["episode_id"])
        if head is None:
            raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
        return _record_result(
            session, key=key, primary=primary, head=head, status="UNCHANGED")
    world_clock = session.world().clock
    if clock > world_clock:
        raise RecursionRefusal("RELATION_CLOCK_FUTURE")
    if clock < world_clock:
        raise RecursionRefusal("RELATION_CLOCK_BACKDATED")
    scope = _scope_for_key(session, key)
    if scope is None:
        raise RecursionRefusal("RELATION_PROMOTION_EMPTY")
    if scope.get("status") != "VERIFIED":
        raise RecursionRefusal("RELATION_CUSTODY_SEVERED")
    state_changes = [
        episode for episode in scope["changes"]
        if (episode.get("body") or {}).get("change") in RELATION_STATE_CHANGES
    ]
    machine = _state_machine(scope["changes"])
    if machine["status"] == "ABSENT":
        raise RecursionRefusal("RELATION_PROMOTION_EMPTY")
    if depth <= machine["depth"]:
        raise RecursionRefusal("RELATION_PROMOTION_NOT_DEEPER")
    exposure_ids = sorted({
        actor_id_value
        for episode in scope["changes"]
        for actor_id_value in ((episode.get("body") or {}).get(
            "exposed_actor_ids") or ())
    } | set(actor_ids))
    exposure_aliases = []
    for actor_id_value in exposure_ids:
        row = _resolve_live_actor(
            session, actor_id_value, code="RELATION_CUSTODY_SEVERED")
        exposure_aliases.append(row["alias"])
    body = {
        **request,
        "exposed_actor_ids": exposure_ids,
        "exposed_aliases": exposure_aliases,
        "private_state_hash": digest({}),
        "history_hash": digest(
            [_history_entry(episode) for episode in state_changes]),
    }
    _refuse_private_leak(_public_body(body), {})
    appended = _append_change(session, body=body, private={}, key=key)
    return _record_result(
        session, key=key, primary=appended["primary"],
        head=appended["head"], status="RECORDED")


__all__ = [
    "RELATION_CHANGE_KIND",
    "RELATION_HEAD_KIND",
    "RELATION_CHANGE_SCHEMA",
    "RELATION_HEAD_SCHEMA",
    "RELATION_READ_SCHEMA",
    "RELATION_CONTEXT_SCHEMA",
    "RELATION_GRADE",
    "RELATION_STATE_CHANGES",
    "read_relation_history",
    "read_actor_relative_context",
    "record_relation_change",
    "promote_relation",
    "relation_change_source",
    "relation_head_source",
]
