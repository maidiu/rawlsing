"""Stable supporting-actor identity over the existing S47/P2 world and C12 store.

The focal root actor remains the generated root's first actor. A supporting
actor is registered in the existing branch actor set and world actor state, is
checked against that live registration at every participant admission, and is
read only through actor-specific C12 perception receipts. This is sourcefree
engineering, not native C4/ADP-015 issuance.
"""
from __future__ import annotations

import itertools
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


_SAVEPOINT_SEQ = itertools.count()


class _StoreWrite:
    """One durable C12 write unit: all rows commit or none do.

    The C12 store is opened with sqlite autocommit. Registration and
    participation each span several rows (branch metadata, episode, checkpoint,
    perception); without an explicit transaction a process death between rows
    leaves a branch alias with no world actor row. BEGIN IMMEDIATE also
    serializes competing registrations. If a caller already opened a
    transaction, a savepoint preserves its outer unit.
    """

    def __init__(self, store) -> None:
        self.store = store
        self.savepoint = None

    def __enter__(self) -> "_StoreWrite":
        if self.store.db.in_transaction:
            self.savepoint = "c01_write_%d" % next(_SAVEPOINT_SEQ)
            self.store.db.execute("SAVEPOINT " + self.savepoint)
        else:
            self.store.db.execute("BEGIN IMMEDIATE")
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if self.savepoint is not None:
            if exc_type is None:
                self.store.db.execute("RELEASE SAVEPOINT " + self.savepoint)
            else:
                self.store.db.execute("ROLLBACK TO SAVEPOINT " + self.savepoint)
                self.store.db.execute("RELEASE SAVEPOINT " + self.savepoint)
            return False
        self.store.db.execute("COMMIT" if exc_type is None else "ROLLBACK")
        return False


def _registration_episodes(session, alias: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == SUPPORTING_REGISTRATION_KIND
        and (row.get("body") or {}).get("alias") == alias
    ]


def _row_from_registration(episode: Mapping[str, Any]) -> dict:
    body = episode.get("body") or {}
    return {
        "actor_id": body["actor_id"],
        "role": body["role"],
        "participant_kind": PARTICIPANT_KIND,
        "private_state_hash": body["private_state_hash"],
        "private_episode_id": episode["episode_id"],
        "registration": {
            key: body[key] for key in (
                "schema", "grade", "root", "branch", "epoch", "actor_id",
                "alias", "role", "source",
            )
        },
    }


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


def _validate_recovery_episode(session, episode: Mapping[str, Any], *,
                               alias: str, actor_id: str, role: str,
                               private: Mapping[str, Any], private_hash: str,
                               source: str, root_hash: str, world_clock: int) -> dict:
    body = episode.get("body") or {}
    if (body.get("schema") != SUPPORTING_ACTOR_SCHEMA
            or body.get("grade") != SUPPORTING_GRADE
            or body.get("root") != root_hash
            or body.get("branch") != session.branch_id
            or body.get("actor_id") != actor_id
            or body.get("alias") != alias
            or body.get("role") != role
            or body.get("private_state_hash") != private_hash
            or body.get("source") != source
            or _private_state(body.get("private_state")) != private):
        raise RecursionRefusal("SUPPORTING_ACTOR_REGISTRATION_MISMATCH")
    epoch = body.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world_clock):
        raise RecursionRefusal("SUPPORTING_ACTOR_EPOCH_INVALID")
    return body


def register_supporting_actor(session, *, alias: str, actor_id: str, role: str,
                              private_state: Mapping[str, Any] | None = None) -> dict:
    """Register one stable supporting actor through the actual C12/P2 writer.

    Branch metadata, the private-state episode and the world checkpoint commit
    as one C12 transaction. A crash therefore leaves either the exact prior
    state or the complete registration, never a branch alias with no live actor
    row. A partial state written by the earlier non-atomic cut is recovered when
    its registration episode still proves the requested identity; an orphan
    branch alias with no episode and no world row is reclaimed.
    """
    if not _text(alias) or not _text(actor_id) or role not in SUPPORTING_ROLES:
        raise RecursionRefusal("SUPPORTING_ACTOR_SCHEMA")
    private = _private_state(private_state)
    private_hash = digest(private)
    source = registration_source(
        actor_id=actor_id, alias=alias, role=role,
        private_state_hash=private_hash,
    )
    store = session.product.store
    result = None
    status = "REGISTERED"
    with _StoreWrite(store):
        world = session.world()
        root = session.read_root()
        root_ids, by_id, by_alias = _root_and_alias_maps(session)
        branch_ids = _branch_actor_ids(session)
        root_aliases = {by_id[actor] for actor in root_ids if actor in by_id}
        user_alias = session.meta.get("user_actor")
        if actor_id in root_ids:
            raise RecursionRefusal("SUPPORTING_ACTOR_FOCAL_IDENTITY_RESERVED")
        # Alias and stable-ID namespaces must not overlap either root, user or
        # supporting registrations. Otherwise read_actor_access can resolve the
        # same string as two different actors.
        if (alias in root_ids or alias in root_aliases or alias in by_id
                or alias == user_alias):
            raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_RESERVED")
        if (actor_id in by_alias or actor_id in root_aliases
                or actor_id == user_alias):
            raise RecursionRefusal("SUPPORTING_ACTOR_ID_COLLISION")
        if alias in by_alias and by_alias[alias] != actor_id:
            raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_COLLISION")
        existing_alias = by_id.get(actor_id)
        if existing_alias is not None and existing_alias != alias:
            raise RecursionRefusal("SUPPORTING_ACTOR_ID_COLLISION")
        found_alias, found = _find(session, actor_id=actor_id)
        if found_alias is not None and found_alias != alias:
            raise RecursionRefusal("SUPPORTING_ACTOR_ID_COLLISION")
        if found is not None:
            _validate_registration(session, found_alias, found, root_ids=root_ids)
            episodes = _registration_episodes(session, found_alias)
            if (len(episodes) != 1
                    or episodes[0].get("episode_id")
                    != found.get("private_episode_id")):
                raise RecursionRefusal(
                    "SUPPORTING_ACTOR_DUPLICATE_REGISTRATION")
            if (found.get("role") == role
                    and _private_state_for(session, found_alias, found) == private
                    and found["registration"].get("source") == source):
                result = {
                    "schema": SUPPORTING_ACTOR_READ_SCHEMA,
                    "grade": SUPPORTING_GRADE,
                    "status": "UNCHANGED",
                    **_public_read(session, found_alias, found),
                }
            else:
                raise RecursionRefusal("SUPPORTING_ACTOR_REGISTRATION_MISMATCH")
        else:
            if alias in world.actor_state:
                existing = world.actor_state[alias]
                same_identity = (
                    isinstance(existing, Mapping)
                    and existing.get("participant_kind") == PARTICIPANT_KIND
                    and existing.get("actor_id") == actor_id
                    and existing.get("role") == role
                )
                if not same_identity:
                    raise RecursionRefusal("SUPPORTING_ACTOR_ALIAS_RESERVED")
                if existing.get("private_state_hash") != private_hash:
                    raise RecursionRefusal(
                        "SUPPORTING_ACTOR_REGISTRATION_MISMATCH")
            focal_alias = by_id.get(root_ids[0])
            position = world.positions.get(focal_alias) if focal_alias else None
            if not _text(position):
                raise RecursionRefusal("SUPPORTING_ACTOR_FOCAL_POSITION_MISSING")
            episodes = _registration_episodes(session, alias)
            if len(episodes) > 1:
                raise RecursionRefusal("SUPPORTING_ACTOR_DUPLICATE_REGISTRATION")
            if episodes:
                episode = episodes[0]
                _validate_recovery_episode(
                    session, episode, alias=alias, actor_id=actor_id,
                    role=role, private=private, private_hash=private_hash,
                    source=source, root_hash=root["root_hash"],
                    world_clock=world.clock,
                )
                row = _row_from_registration(episode)
                if alias not in branch_ids:
                    actors = sorted(set(branch_ids) | {alias})
                    store.db.execute(
                        "UPDATE branch SET actor_ids=? WHERE branch_id=?",
                        (canonical(actors), session.branch_id),
                    )
                world.actor_state[alias] = row
                world.positions[alias] = position
                session.product._checkpoint(
                    session.branch_id, world.clock, world)
                _validate_registration(session, alias, row, root_ids=root_ids)
                result = {
                    "schema": SUPPORTING_ACTOR_READ_SCHEMA,
                    "grade": SUPPORTING_GRADE,
                    "status": "RECOVERED",
                    **_public_read(session, alias, row),
                }
            else:
                # An alias present only in branch metadata has no actor state
                # and no registration episode: it is the exact partial left by
                # the earlier non-atomic writer. Reclaiming the label cannot
                # erase a live actor; the transaction then writes the full row.
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
                if alias not in branch_ids:
                    actors = sorted(set(branch_ids) | {alias})
                    store.db.execute(
                        "UPDATE branch SET actor_ids=? WHERE branch_id=?",
                        (canonical(actors), session.branch_id),
                    )
                    status = "REGISTERED"
                else:
                    status = "RECOVERED"
                episode = store.append_episode(
                    session.branch_id, actor_id=alias,
                    kind=SUPPORTING_REGISTRATION_KIND, clock=world.clock,
                    body=body,
                )
                row = _row_from_registration(episode)
                world.actor_state[alias] = row
                world.positions[alias] = position
                session.product._checkpoint(
                    session.branch_id, world.clock, world)
                _validate_registration(session, alias, row, root_ids=root_ids)
                result = {
                    "schema": SUPPORTING_ACTOR_READ_SCHEMA,
                    "grade": SUPPORTING_GRADE,
                    "status": status,
                    **_public_read(session, alias, row),
                }
    if result is None:
        raise RecursionRefusal("SUPPORTING_ACTOR_REGISTRATION_FAILED")
    return result


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


def _participation_episodes(session, *, actor_id: str,
                            event_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == SUPPORTING_PARTICIPATION_KIND
        and (row.get("body") or {}).get("actor_id") == actor_id
        and (row.get("body") or {}).get("event_id") == event_id
    ]


def _participation_episode(session, *, actor_id: str, event_id: str) -> dict | None:
    rows = _participation_episodes(
        session, actor_id=actor_id, event_id=event_id)
    if len(rows) > 1:
        raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
    return rows[0] if rows else None


def assert_no_private_leak(session, document: Mapping[str, Any],
                           participants: Iterable[str]) -> None:
    """Refuse a proposal that carries any supporting actor's private value."""
    root_ids, _, _ = _root_and_alias_maps(session)
    for participant in participants:
        if participant in root_ids:
            continue
        alias, row = _find(session, actor_id=participant)
        if alias is None:
            continue
        checked = _validate_registration(session, alias, row, root_ids=root_ids)
        _refuse_private_leak(document, _private_state_for(session, alias, checked))


def _validate_participation_episode(session, episode: Mapping[str, Any], *,
                                    actor_id: str, alias: str, role: str,
                                    source: str, event: Mapping[str, Any]) -> dict:
    body = episode.get("body") or {}
    if (episode.get("actor_id") != alias
            or body.get("schema") != SUPPORTING_PARTICIPATION_SCHEMA
            or body.get("grade") != SUPPORTING_GRADE
            or body.get("root") != session.read_root()["root_hash"]
            or body.get("branch") != session.branch_id
            or body.get("actor_id") != actor_id
            or body.get("alias") != alias
            or body.get("role") != role
            or body.get("source") != source
            or body.get("event_id") != event.get("event_id")
            or body.get("event_hash") != event.get("hash")
            or body.get("event_kind") != event.get("kind")
            or body.get("location") != event.get("location")
            or body.get("clock") != event.get("clock")
            or body.get("access_channel") != "co_present"):
        raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
    return body


def record_supporting_participation(session, *, event: Mapping[str, Any],
                                    participants: Iterable[str]) -> list[dict]:
    """Record actual C12 perception and a public participation receipt.

    The world event is resolved from the branch store, not trusted from the
    caller: a detached or forged event mapping cannot mint a receipt. Every
    participant is validated before the first write, and all perception rows,
    participation episodes and receipts commit as one C12 transaction, so a
    refused second participant cannot leave the first partially recorded.
    """
    if not isinstance(event, Mapping):
        raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_MISSING")
    event_id = event.get("event_id")
    if not _text(event_id):
        raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_INVALID")
    store = session.product.store
    result = []
    with _StoreWrite(store):
        actual = store.world_event(session.branch_id, event_id)
        if actual is None:
            raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_MISSING")
        clock = actual.get("clock")
        location = actual.get("location")
        if (not _text(actual.get("hash"))
                or isinstance(clock, bool) or not isinstance(clock, int)
                or not _text(location) or not _text(actual.get("kind"))):
            raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_INVALID")
        if (event.get("hash") != actual.get("hash")
                or event.get("clock") != clock
                or event.get("kind") != actual.get("kind")
                or event.get("location") != location):
            raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_MISMATCH")
        world = session.world()
        root_ids, _, _ = _root_and_alias_maps(session)
        plan = []
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
            _refuse_private_leak(actual, private)
            plan.append((participant, alias, checked, private))
        if canonical(detached(event)) != canonical(actual):
            raise RecursionRefusal("SUPPORTING_PARTICIPATION_EVENT_MISMATCH")
        for participant, alias, checked, _private in plan:
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
                        "event_hash": actual["hash"],
                        "event_kind": actual["kind"],
                        "location": location,
                        "clock": clock,
                        "access_channel": "co_present",
                        "private_state": "NOT_READ",
                    },
                )
            else:
                _validate_participation_episode(
                    session, episode, actor_id=participant, alias=alias,
                    role=checked["role"], event=actual,
                    source=checked["registration"]["source"],
                )
            result.append({
                "schema": SUPPORTING_PARTICIPATION_SCHEMA,
                "grade": SUPPORTING_GRADE,
                "actor_id": participant,
                "alias": alias,
                "role": checked["role"],
                "event_id": event_id,
                "event_hash": actual["hash"],
                "event_kind": actual["kind"],
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
        (row["actor_id"], row["event_id"]): row
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
        receipt = receipts.get((alias, event_id))
        if receipt is None:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        if (receipt.get("clock") != event.get("clock")
                or receipt.get("channel") != "co_present"):
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        if (participant.get("event_hash") != event.get("hash")
                or participant.get("clock") != event.get("clock")):
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        episode = _participation_episode(session, actor_id=actor_id,
                                         event_id=event_id)
        if episode is None:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        _validate_participation_episode(
            session, episode, actor_id=actor_id, alias=alias,
            role=row.get("role"), event=event,
            source=row["registration"].get("source"),
        )


def read_actor_access(session, actor_ref: str, event_id: str) -> dict:
    """Return only the event content this actor actually perceived.

    Root actors are read through their existing C12 perception receipts. A
    supporting actor additionally needs its live registration and the public
    participation episode for this exact event; a bare or forged perception row
    cannot by itself grant access. A registration whose alias collides with a
    root stable ID is refused rather than silently resolved as the root actor.
    """
    if not _text(actor_ref) or not _text(event_id):
        raise RecursionRefusal("ACTOR_ACCESS_SCHEMA")
    root_ids, by_id, by_alias = _root_and_alias_maps(session)
    if actor_ref in root_ids and actor_ref in by_alias:
        raise RecursionRefusal("ACTOR_ACCESS_IDENTITY_AMBIGUOUS")
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
    supporting_alias, supporting_row = (None, None)
    if actor_id not in root_ids:
        supporting_alias, supporting_row = _find(session, actor_id=actor_id)
        if supporting_alias is not None and supporting_alias != alias:
            raise RecursionRefusal("ACTOR_ACCESS_IDENTITY_AMBIGUOUS")
    if supporting_row is not None:
        checked = _validate_registration(
            session, alias, supporting_row, root_ids=root_ids)
        episode = _participation_episode(
            session, actor_id=actor_id, event_id=event_id)
        if receipt is None and episode is None:
            return {**base, "status": "NOT_PERCEIVED", "event": None}
        if receipt is None or episode is None:
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
        event = session.event(event_id)
        if not event:
            raise RecursionRefusal("ACTOR_ACCESS_EVENT_UNAVAILABLE")
        _validate_participation_episode(
            session, episode, actor_id=actor_id, alias=alias,
            role=checked.get("role"), event=event,
            source=checked["registration"].get("source"),
        )
        if (receipt.get("clock") != event.get("clock")
                or receipt.get("channel") != "co_present"):
            raise RecursionRefusal("P2_SUPPORTING_PARTICIPATION_SEVERED")
    else:
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
