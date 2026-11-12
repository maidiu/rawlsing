"""Stable supporting-actor identity over the existing S47/P2 world and C12 store.

The focal root actor remains the generated root's first actor. A supporting
actor is registered in the existing branch actor set and world actor state, is
checked against that live registration at every participant admission, and is
read only through actor-specific C12 perception receipts. This is sourcefree
engineering, not native C4/ADP-015 issuance.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from .contracts import RecursionRefusal, canonical, detached, digest

SUPPORTING_ACTOR_SCHEMA = "SOROK_P2_SUPPORTING_ACTOR@1"
SUPPORTING_ACTOR_READ_SCHEMA = "SOROK_P2_SUPPORTING_ACTOR_READ@1"
SUPPORTING_REGISTRATION_KIND = "P2_SUPPORTING_ACTOR"
SUPPORTING_PARTICIPATION_KIND = "P2_SUPPORTING_PARTICIPATION"
SUPPORTING_PARTICIPATION_SCHEMA = "SOROK_P2_SUPPORTING_PARTICIPATION@1"
ACTOR_ACCESS_SCHEMA = "SOROK_P2_ACTOR_ACCESS@1"
SUPPORTING_GRADE = "SOURCEFREE_S2_ONLY"
SUPPORTING_ROLES = frozenset({"parent"})
PARTICIPANT_KIND = "SUPPORTING_ACTOR"
REGISTRATION_FIELDS = frozenset({
    "schema", "grade", "root", "branch", "epoch", "actor_id", "alias",
    "role", "source",
})


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _scalar(value: Any) -> bool:
    return type(value) in (bool, int, str)


def _private_state(value: Any) -> dict:
    if value is None:
        return {}
    if not isinstance(value, Mapping) or any(
            not _text(key) or not _scalar(item) for key, item in value.items()):
        raise RecursionRefusal("SUPPORTING_ACTOR_PRIVATE_STATE_SCHEMA")
    return detached(value)


def registration_source(*, actor_id: str, alias: str, role: str,
                        private_state_hash: str) -> str:
    return digest({
        "schema": SUPPORTING_ACTOR_SCHEMA,
        "grade": SUPPORTING_GRADE,
        "actor_id": actor_id,
        "alias": alias,
        "role": role,
        "private_state_hash": private_state_hash,
    })


def _root_and_alias_maps(session):
    root = session.read_root()
    root_ids = tuple(root["actor_ids"])
    world = session.world()
    by_id, by_alias = {}, {}
    for alias, row in world.actor_state.items():
        if isinstance(row, dict) and _text(row.get("actor_id")):
            by_alias[alias] = row["actor_id"]
            by_id.setdefault(row["actor_id"], alias)
    return root_ids, by_id, by_alias


def _branch_actor_ids(session) -> tuple[str, ...]:
    return tuple(session.product.store.branch(session.branch_id)["actor_ids"])


def _private_state_for(session, alias: str, row: Mapping[str, Any]) -> dict:
    registration = row.get("registration") or {}
    private_hash = row.get("private_state_hash")
    episode_id = row.get("private_episode_id")
    if not _text(private_hash) or not _text(episode_id):
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    episode = next((
        item for item in session.product.store.episodes(session.branch_id)
        if item.get("episode_id") == episode_id
    ), None)
    if (episode is None or episode.get("actor_id") != alias
            or episode.get("kind") != SUPPORTING_REGISTRATION_KIND):
        raise RecursionRefusal("SUPPORTING_ACTOR_PRIVATE_STATE_SEVERED")
    body = episode.get("body") or {}
    if (body.get("schema") != SUPPORTING_ACTOR_SCHEMA
            or body.get("actor_id") != row.get("actor_id")
            or body.get("alias") != alias
            or body.get("role") != row.get("role")
            or body.get("root") != registration.get("root")
            or body.get("branch") != registration.get("branch")
            or body.get("epoch") != registration.get("epoch")
            or body.get("source") != registration.get("source")
            or body.get("private_state_hash") != private_hash):
        raise RecursionRefusal("SUPPORTING_ACTOR_PRIVATE_STATE_SEVERED")
    private = _private_state(body.get("private_state"))
    if digest(private) != private_hash:
        raise RecursionRefusal("SUPPORTING_ACTOR_PRIVATE_STATE_SEVERED")
    return private


def _validate_registration(session, alias: str, row: Mapping[str, Any],
                           *, root_ids: tuple[str, ...]) -> dict:
    if (not isinstance(row, Mapping)
            or row.get("participant_kind") != PARTICIPANT_KIND
            or not _text(row.get("actor_id")) or not _text(row.get("role"))
            or row.get("role") not in SUPPORTING_ROLES):
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    registration = row.get("registration")
    if not isinstance(registration, Mapping) or set(registration) != REGISTRATION_FIELDS:
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    if (registration.get("schema") != SUPPORTING_ACTOR_SCHEMA
            or registration.get("grade") != SUPPORTING_GRADE):
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    world = session.world()
    root = session.read_root()
    if (registration.get("root") != root["root_hash"]
            or registration.get("branch") != session.branch_id):
        raise RecursionRefusal("SUPPORTING_ACTOR_ROOT_OR_BRANCH_MISMATCH")
    epoch = registration.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("SUPPORTING_ACTOR_EPOCH_INVALID")
    if (registration.get("actor_id") != row.get("actor_id")
            or registration.get("alias") != alias
            or registration.get("role") != row.get("role")):
        raise RecursionRefusal("SUPPORTING_ACTOR_IDENTITY_MISMATCH")
    if row.get("actor_id") in root_ids:
        raise RecursionRefusal("SUPPORTING_ACTOR_FOCAL_IDENTITY_RESERVED")
    private = _private_state_for(session, alias, row)
    source = registration_source(
        actor_id=row["actor_id"], alias=alias, role=row["role"],
        private_state_hash=digest(private),
    )
    if registration.get("source") != source:
        raise RecursionRefusal("SUPPORTING_ACTOR_SOURCE_MISMATCH")
    if alias not in _branch_actor_ids(session):
        raise RecursionRefusal("SUPPORTING_ACTOR_NOT_IN_BRANCH")
    if world.actor_state.get(alias) is not row:
        current = world.actor_state.get(alias)
        if current != row:
            raise RecursionRefusal("SUPPORTING_ACTOR_STALE_ROW")
    return detached(row)


def _find(session, *, actor_id: str | None = None,
          alias: str | None = None) -> tuple[str, dict] | tuple[None, None]:
    world = session.world()
    matches = []
    for candidate in _branch_actor_ids(session):
        row = world.actor_state.get(candidate)
        if (isinstance(row, dict)
                and row.get("participant_kind") == PARTICIPANT_KIND
                and (actor_id is None or row.get("actor_id") == actor_id)
                and (alias is None or candidate == alias)):
            matches.append((candidate, row))
    if len(matches) > 1:
        raise RecursionRefusal("SUPPORTING_ACTOR_DUPLICATE_REGISTRATION")
    return matches[0] if matches else (None, None)


def register_supporting_actor(session, *, alias: str, actor_id: str, role: str,
                              private_state: Mapping[str, Any] | None = None) -> dict:
    """Register one stable supporting actor through the actual C12/P2 writer."""
    world = session.world()
    root = session.read_root()
    if not _text(alias) or not _text(actor_id) or role not in SUPPORTING_ROLES:
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    private = _private_state(private_state)
    root_ids, by_id, by_alias = _root_and_alias_maps(session)
    if actor_id in root_ids:
        raise RecursionRefusal("SUPPORTING_ACTOR_FOCAL_IDENTITY_RESERVED")
    root_aliases = {by_id[actor] for actor in root_ids if actor in by_id}
    user_alias = session.meta.get("user_actor")
    if alias in root_aliases or alias == user_alias:
        raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_RESERVED")
    if alias in by_alias and by_alias[alias] != actor_id:
        raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_COLLISION")
    existing_alias = by_id.get(actor_id)
    if existing_alias is not None and existing_alias != alias:
        raise RecursionRefusal("SUPPORTING_ACTOR_ID_COLLISION")
    found_alias, found = _find(session, actor_id=actor_id)
    if found_alias is not None and found_alias != alias:
        raise RecursionRefusal("SUPPORTING_ACTOR_ID_COLLISION")
    private_hash = digest(private)
    source = registration_source(
        actor_id=actor_id, alias=alias, role=role,
        private_state_hash=private_hash,
    )
    if found is not None:
        _validate_registration(session, found_alias, found, root_ids=root_ids)
        if (found.get("role") == role
                and _private_state_for(session, found_alias, found) == private
                and found["registration"].get("source") == source):
            return {
                "schema": SUPPORTING_ACTOR_READ_SCHEMA,
                "grade": SUPPORTING_GRADE,
                "status": "UNCHANGED",
                **_public_read(session, found_alias, found),
            }
        raise RecursionRefusal("SUPPORTING_ACTOR_REGISTRATION_MISMATCH")
    if alias in world.actor_state or alias in _branch_actor_ids(session):
        raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_RESERVED")
    focal_alias = by_id.get(root_ids[0])
    position = world.positions.get(focal_alias) if focal_alias else None
    if not _text(position):
        raise RecursionRefusal("SUPPORTING_ACTOR_FOCAL_POSITION_MISSING")
    store = session.product.store
    old_actors = list(_branch_actor_ids(session))
    changed = alias not in old_actors
    try:
        if changed:
            actors = sorted(set(old_actors) | {alias})
            store.db.execute(
                "UPDATE branch SET actor_ids=? WHERE branch_id=?",
                (canonical(actors), session.branch_id),
            )
            store.db.commit()
        body = {
            "schema": SUPPORTING_ACTOR_SCHEMA,
            "grade": SUPPORTING_GRADE,
            "root": root["root_hash"],
            "branch": session.branch_id,
            "epoch": world.clock,
            "actor_id": actor_id,
            "alias": alias,
            "role": role,
            "source": source,
            "private_state_hash": private_hash,
            "private_state": private,
        }
        existing_episode = next((
            row for row in store.episodes(session.branch_id)
            if row.get("kind") == SUPPORTING_REGISTRATION_KIND
            and row.get("body") == body
        ), None)
        episode = existing_episode or store.append_episode(
            session.branch_id, actor_id=alias,
            kind=SUPPORTING_REGISTRATION_KIND, clock=world.clock, body=body,
        )
        row = {
            "actor_id": actor_id,
            "role": role,
            "participant_kind": PARTICIPANT_KIND,
            "private_state_hash": private_hash,
            "private_episode_id": episode["episode_id"],
            "registration": {
                "schema": SUPPORTING_ACTOR_SCHEMA,
                "grade": SUPPORTING_GRADE,
                "root": root["root_hash"],
                "branch": session.branch_id,
                "epoch": world.clock,
                "actor_id": actor_id,
                "alias": alias,
                "role": role,
                "source": source,
            },
        }
        world.actor_state[alias] = row
        world.positions[alias] = position
        session.product._checkpoint(session.branch_id, world.clock, world)
    except BaseException:
        if changed:
            store.db.execute(
                "UPDATE branch SET actor_ids=? WHERE branch_id=?",
                (canonical(old_actors), session.branch_id),
            )
            store.db.commit()
            world.actor_state.pop(alias, None)
            world.positions.pop(alias, None)
        raise
    return {
        "schema": SUPPORTING_ACTOR_READ_SCHEMA,
        "grade": SUPPORTING_GRADE,
        "status": "REGISTERED",
        **_public_read(session, alias, row),
    }


def _public_read(session, alias: str, row: Mapping[str, Any]) -> dict:
    world = session.world()
    registration = dict(row["registration"])
    return {
        "actor_id": row["actor_id"],
        "alias": alias,
        "role": row["role"],
        "participant_kind": PARTICIPANT_KIND,
        "root": registration["root"],
        "branch": registration["branch"],
        "epoch": registration["epoch"],
        "source": registration["source"],
        "private_state_hash": row["private_state_hash"],
        "position": world.positions.get(alias),
        "world_state_hash": digest(world.snapshot()),
        "private_state": "NOT_READ",
        "read_boundary": {
            "private_state": "SELF_ONLY",
            "focal_root": "UNCHANGED",
        },
    }


def read_supporting_actor(session, actor_id: str, *, as_actor: str | None = None) -> dict:
    """Read one registered supporting actor; private state is self-readable only."""
    alias, row = _find(session, actor_id=actor_id)
    if alias is None:
        raise RecursionRefusal("SUPPORTING_ACTOR_NOT_REGISTERED")
    root_ids, _, _ = _root_and_alias_maps(session)
    checked = _validate_registration(session, alias, row, root_ids=root_ids)
    result = {
        "schema": SUPPORTING_ACTOR_READ_SCHEMA,
        "grade": SUPPORTING_GRADE,
        "status": "REGISTERED",
        **_public_read(session, alias, checked),
    }
    if as_actor is not None and as_actor == actor_id:
        result["private_state"] = _private_state_for(session, alias, checked)
        result["read_boundary"] = {
            "private_state": "SELF_READ",
            "focal_root": "UNCHANGED",
        }
    return result


def registered_supporting_actors(session) -> list[dict]:
    world = session.world()
    root_ids, _, _ = _root_and_alias_maps(session)
    result = []
    for alias in _branch_actor_ids(session):
        row = world.actor_state.get(alias)
        if isinstance(row, dict) and row.get("participant_kind") == PARTICIPANT_KIND:
            _validate_registration(session, alias, row, root_ids=root_ids)
            result.append({
                "schema": SUPPORTING_ACTOR_READ_SCHEMA,
                "grade": SUPPORTING_GRADE,
                "status": "REGISTERED",
                **_public_read(session, alias, row),
            })
    return result


def resolve_participants(session, participants: Iterable[str]) -> dict:
    """Resolve each stable ID against the live root and supporting registration."""
    if not isinstance(participants, (list, tuple)):
        raise RecursionRefusal("P2_PARTICIPANT_SCHEMA")
    values = tuple(participants)
    if (not values or any(not _text(value) for value in values)
            or len(set(values)) != len(values)):
        raise RecursionRefusal("P2_PARTICIPANT_SCHEMA")
    root_ids, by_id, _ = _root_and_alias_maps(session)
    resolved = []
    for participant in values:
        if participant in root_ids:
            alias = by_id.get(participant)
            if alias is None:
                raise RecursionRefusal("P2_PARTICIPANT_ALIAS_UNAVAILABLE")
            resolved.append({
                "actor_id": participant,
                "alias": alias,
                "kind": "ROOT_ACTOR",
                "role": None,
            })
            continue
        doc = read_supporting_actor(session, participant)
        resolved.append({
            "actor_id": doc["actor_id"],
            "alias": doc["alias"],
            "kind": PARTICIPANT_KIND,
            "role": doc["role"],
        })
    focal_alias = by_id.get(root_ids[0])
    if focal_alias is None:
        raise RecursionRefusal("P2_PARTICIPANT_ALIAS_UNAVAILABLE")
    return {
        "root_actor_ids": root_ids,
        "focal_actor_id": root_ids[0],
        "focal_alias": focal_alias,
        "participants": resolved,
    }


def _private_strings(private_state: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(value for value in private_state.values()
                 if isinstance(value, str) and value.strip())


def _refuse_private_leak(event: Mapping[str, Any], private_state: Mapping[str, Any]) -> None:
    text = canonical(event)
    if any(value in text for value in _private_strings(private_state)):
        raise RecursionRefusal("SUPPORTING_PRIVATE_STATE_LEAK")


def _participation_episode(session, *, actor_id: str, event_id: str) -> dict | None:
    return next((
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == SUPPORTING_PARTICIPATION_KIND
        and (row.get("body") or {}).get("actor_id") == actor_id
        and (row.get("body") or {}).get("event_id") == event_id
    ), None)


def record_supporting_participation(session, *, event: Mapping[str, Any],
                                    participants: Iterable[str]) -> list[dict]:
    """Record actual C12 perception and a public participation receipt."""
    if not isinstance(event, Mapping):
        raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_MISSING")
    event_id = event.get("event_id")
    clock = event.get("clock")
    location = event.get("location")
    if (not _text(event_id) or not _text(event.get("hash"))
            or isinstance(clock, bool)
            or not isinstance(clock, int) or not _text(location)):
        raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_INVALID")
    world = session.world()
    root_ids, _, _ = _root_and_alias_maps(session)
    store = session.product.store
    result = []
    for participant in participants:
        if participant in root_ids:
            continue
        alias, row = _find(session, actor_id=participant)
        if alias is None:
            raise RecursionRefusal("P2_PARTICIPANT_NOT_REGISTERED")
        checked = _validate_registration(session, alias, row, root_ids=root_ids)
        if world.positions.get(alias) != location:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPANT_NOT_COPRESENT")
        private = _private_state_for(session, alias, checked)
        _refuse_private_leak(event, private)
        receipt = store.record_perception(
            session.branch_id, actor_id=alias, event_id=event_id,
            clock=clock, channel="co_present",
        )
        episode = _participation_episode(session, actor_id=participant,
                                         event_id=event_id)
        if episode is None:
            episode = store.append_episode(
                session.branch_id, actor_id=alias,
                kind=SUPPORTING_PARTICIPATION_KIND, clock=clock,
                body={
                    "schema": SUPPORTING_PARTICIPATION_SCHEMA,
                    "grade": SUPPORTING_GRADE,
                    "root": session.read_root()["root_hash"],
                    "branch": session.branch_id,
                    "epoch": checked["registration"]["epoch"],
                    "source": checked["registration"]["source"],
                    "actor_id": participant,
                    "alias": alias,
                    "role": checked["role"],
                    "event_id": event_id,
                    "event_hash": event.get("hash"),
                    "event_kind": event.get("kind"),
                    "location": location,
                    "clock": clock,
                    "access_channel": "co_present",
                    "private_state": "NOT_READ",
                },
            )
        result.append({
            "schema": SUPPORTING_PARTICIPATION_SCHEMA,
            "grade": SUPPORTING_GRADE,
            "actor_id": participant,
            "alias": alias,
            "role": checked["role"],
            "event_id": event_id,
            "event_hash": event.get("hash"),
            "event_kind": event.get("kind"),
            "clock": clock,
            "access_channel": "co_present",
            "perception_duplicate": bool(receipt.get("duplicate")),
            "participation_episode_id": episode["episode_id"],
            "private_state": "NOT_READ",
        })
    return result


def verify_supporting_participation(session, *, event_id: str,
                                    participants: Iterable[Mapping[str, Any]]) -> None:
    """Fail closed when a recorded C12 perception or receipt was severed."""
    root_ids, _, _ = _root_and_alias_maps(session)
    receipts = {
        (row["actor_id"], row["event_id"])
        for row in session.product.store.perceptions(session.branch_id)
    }
    event = session.event(event_id)
    for participant in participants:
        actor_id = participant.get("actor_id")
        alias = participant.get("alias")
        if not _text(actor_id) or not _text(alias) or not event:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        current_alias, row = _find(session, actor_id=actor_id)
        if current_alias != alias or row is None:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        _validate_registration(session, alias, row, root_ids=root_ids)
        if (alias, event_id) not in receipts:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        if (participant.get("event_hash") != event.get("hash")
                or participant.get("clock") != event.get("clock")):
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        episode = _participation_episode(session, actor_id=actor_id,
                                         event_id=event_id)
        if episode is None:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        body = episode.get("body") or {}
        if (body.get("alias") != alias
                or body.get("event_hash") != event.get("hash")
                or body.get("role") != row.get("role")
                or body.get("source") != row["registration"].get("source")):
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")


def read_actor_access(session, actor_ref: str, event_id: str) -> dict:
    """Return only the event content this actor actually perceived."""
    if not _text(actor_ref) or not _text(event_id):
        raise RecursionRefusal("ACTOR_ACCESS_SCHEMA")
    root_ids, by_id, by_alias = _root_and_alias_maps(session)
    if actor_ref in root_ids:
        actor_id = actor_ref
    elif actor_ref in by_alias:
        actor_id = by_alias[actor_ref]
    else:
        found_alias, row = _find(session, actor_id=actor_ref)
        if row is not None:
            actor_id = row["actor_id"]
        elif actor_ref in _branch_actor_ids(session):
            row = session.world().actor_state.get(actor_ref)
            if not isinstance(row, dict) or not _text(row.get("actor_id")):
                raise RecursionRefusal("ACTOR_ACCESS_ACTOR_UNAVAILABLE")
            actor_id = row["actor_id"]
        else:
            raise RecursionRefusal("ACTOR_ACCESS_UNKNOWN_ACTOR")
    alias = by_id.get(actor_id)
    if alias is None:
        found_alias, row = _find(session, actor_id=actor_id)
        alias = found_alias
    if alias is None:
        raise RecursionRefusal("ACTOR_ACCESS_ACTOR_UNAVAILABLE")
    receipt = next((
        row for row in session.product.store.perceptions(
            session.branch_id, actor_id=alias)
        if row["event_id"] == event_id
    ), None)
    base = {
        "schema": ACTOR_ACCESS_SCHEMA,
        "grade": SUPPORTING_GRADE,
        "viewer": {"actor_id": actor_id, "alias": alias},
        "event_id": event_id,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "private_state": "NOT_READ",
    }
    if receipt is None:
        return {**base, "status": "NOT_PERCEIVED", "event": None}
    event = session.event(event_id)
    if not event:
        raise RecursionRefusal("ACTOR_ACCESS_EVENT_UNAVAILABLE")
    from s45_projection.projection import project_event
    projected = project_event(event)
    projected.pop("perceived_by_user", None)
    return {
        **base,
        "status": "PERCEIVED",
        "world_clock": session.world().clock,
        "event": projected,
        "receipt": {
            "clock": receipt["clock"],
            "channel": receipt["channel"],
        },
    }
