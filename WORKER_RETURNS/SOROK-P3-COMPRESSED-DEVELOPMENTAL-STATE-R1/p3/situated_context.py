"""D02 read-only situated-field projection over actual world and actor access.

This module reads the existing S47/P2 world material fact, the existing P6
household reader, and C01 actor-access/perception readers. It writes no world,
actor, psychological, or scheduler state and adds no new rule. The result is a
bounded decision-input document for a later P3 proposal/provider call.

Historical calendar/as-of qualification is B02 and is NOT BUILT. The selector
therefore exposes only the current logical clock and an explicit date hold.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RecursionRefusal,
    detached,
    digest,
)

GRADE = "SOURCEFREE_S2_ONLY"
SCHEMA = "SOROK_D02_SITUATED_CONTEXT@1"
HOUSEHOLD_SLOT = "p6_household"
DATE_SCOPE = {
    "calendar": "HELD_B02_NOT_BUILT",
    "historical_period": "NOT_QUALIFIED",
    "logical_clock_only": True,
}
OPTION_SEMANTICS = "SOURCEFREE_ADMISSIBLE_INPUT_LABELS_NOT_ACTOR_CHOICE"


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code)
    return detached(value)


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    return value


def _house_module():
    try:
        import house  # type: ignore
    except ImportError:
        root = Path(__file__).resolve().parents[2] / "SOROK-P6-ONE-LIVING-HOUSE-R1"
        if not (root / "house.py").is_file():
            _refuse("D02_P6_HOUSE_READER_UNAVAILABLE")
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        import house  # type: ignore
    return house


def _supporting_module():
    try:
        from developmental_recursion import supporting_actor  # type: ignore
    except ImportError as exc:
        raise RecursionRefusal(
            "D02_SUPPORTING_ACTOR_READER_UNAVAILABLE") from exc
    return supporting_actor


def _identity(value: Any) -> dict:
    document = value.document() if hasattr(value, "document") else value
    document = _mapping(document, "D02_IDENTITY_SCHEMA")
    for key in ("root", "actor", "branch"):
        _text(document.get(key), "D02_IDENTITY_" + key.upper())
    clock = document.get("clock")
    if isinstance(clock, bool) or not isinstance(clock, int):
        _refuse("D02_IDENTITY_CLOCK")
    _text(document.get("state_hash"), "D02_IDENTITY_STATE_HASH")
    return document


def _check_expected(snapshot: Mapping[str, Any], expected: Any) -> None:
    if expected is None:
        return
    document = _identity(expected)
    for key in ("root", "actor", "branch"):
        if document.get(key) != snapshot.get(key):
            _refuse("D02_FOREIGN_STATE:" + key)
    if document.get("clock") != snapshot.get("clock"):
        _refuse("D02_STALE_CLOCK")
    if document.get("state_hash") != snapshot.get("state_hash"):
        _refuse("D02_STALE_STATE")


def _events(session: Any) -> list[dict]:
    rows = session.read_events()
    if not isinstance(rows, list):
        _refuse("D02_WORLD_EVENT_READ")
    return rows


def _event_ref(row: Mapping[str, Any]) -> str | None:
    for key in ("action_event_id", "e1_event_id", "event_id"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def _latest_perceived(session: Any, actor_id: str,
                      event_id: str | None) -> tuple[str, dict] | tuple[None, None]:
    supporting = _supporting_module()
    if event_id is not None:
        access = supporting.read_actor_access(session, actor_id, event_id)
        if access.get("status") == "PERCEIVED":
            return event_id, access
        return None, None
    candidates = []
    for row in _events(session):
        ref = _event_ref(row)
        if ref is None:
            continue
        try:
            access = supporting.read_actor_access(session, actor_id, ref)
        except RecursionRefusal:
            continue
        if access.get("status") == "PERCEIVED":
            candidates.append((int(access.get("world_clock") or 0), ref, access))
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: (item[0], item[1]))
    _, ref, access = candidates[-1]
    return ref, access


def _focal_position(session: Any, actor_id: str) -> str | None:
    world = session.world()
    for alias, row in world.actor_state.items():
        if isinstance(row, Mapping) and row.get("actor_id") == actor_id:
            position = world.positions.get(alias)
            return position if isinstance(position, str) else None
    return None


def _material(session: Any, actor_id: str) -> dict:
    house = _house_module()
    try:
        document = house.read_household(session)
    except RecursionRefusal as exc:
        if str(exc).startswith("P6_HOUSEHOLD_ABSENT"):
            return {
                "status": "HELD",
                "reason": "P6_HOUSEHOLD_ABSENT",
                "source": None,
                "material_hash": None,
                "actor_accessible": {"status": "HELD",
                                     "reason": "P6_HOUSEHOLD_ABSENT"},
            }
        raise
    place = _mapping(document.get("place"), "D02_HOUSEHOLD_PLACE")
    position = _focal_position(session, actor_id)
    rooms = place.get("rooms") if isinstance(place.get("rooms"), list) else []
    if position is None:
        access = {"status": "UNKNOWN", "position": None}
    elif position in rooms:
        access = {"status": "PRESENT", "position": position}
    else:
        access = {"status": "ELSEWHERE", "position": position}
    return {
        "status": "AVAILABLE",
        "owner": "S47_P2_OBJECTIVE_WORLD",
        "slot": HOUSEHOLD_SLOT,
        "source": _text(document.get("source"), "D02_HOUSEHOLD_SOURCE"),
        "material_hash": _text(document.get("material_hash"),
                               "D02_HOUSEHOLD_MATERIAL_HASH"),
        "world_state_hash": _text(document.get("world_state_hash"),
                                  "D02_HOUSEHOLD_WORLD_HASH"),
        "epoch": document.get("epoch"),
        "clock": document.get("clock"),
        "place": place,
        "owner_actor": _mapping(document.get("owner"), "D02_HOUSEHOLD_OWNER"),
        "resources": detached(document.get("resources")),
        "actor_accessible": access,
    }


def _relations(session: Any, actor_id: str, event_ref: str | None,
               event_access: Mapping[str, Any] | None,
               focal_position: str | None) -> list[dict]:
    if event_ref is None or event_access is None:
        return []
    supporting = _supporting_module()
    result = []
    for public in supporting.registered_supporting_actors(session):
        if public.get("actor_id") == actor_id:
            continue
        access = supporting.read_actor_access(
            session, public["actor_id"], event_ref)
        if access.get("status") != "PERCEIVED":
            continue
        result.append({
            "actor_id": public.get("actor_id"),
            "alias": public.get("alias"),
            "role": public.get("role"),
            "participant_kind": public.get("participant_kind"),
            "root": public.get("root"),
            "branch": public.get("branch"),
            "epoch": public.get("epoch"),
            "source": public.get("source"),
            "position": public.get("position"),
            "co_present": (
                isinstance(focal_position, str)
                and public.get("position") == focal_position
            ),
            "access_event_id": access.get("event_id"),
            "access_hash": digest(access),
            "access_status": "ELIGIBLE_SHARED_PERCEPTION",
            "access_scope": "PUBLIC_SHARED_PERCEPTION",
        })
    result.sort(key=lambda row: (str(row.get("actor_id")), str(row.get("source"))))
    return result


def _options(material: Mapping[str, Any], relations: list[dict],
             observation: Mapping[str, Any]) -> list[str]:
    options = []
    if (material.get("status") == "AVAILABLE"
            and material.get("actor_accessible", {}).get("status") == "PRESENT"):
        options.append("ATTEND_HOUSEHOLD_MATERIAL")
        for binding in material.get("resources", []):
            if (binding.get("kind") == "WORLD_RESOURCE"
                    and binding.get("slot") == "workshop"
                    and binding.get("fields", {}).get("tool_available") is True):
                options.append("USE_HOUSEHOLD_TOOL")
                break
    if observation.get("status") == "AVAILABLE":
        options.append("ATTEND_PERCEIVED_SITUATION")
    if any(row.get("co_present") is True for row in relations):
        options.append("ADDRESS_ELIGIBLE_OTHER")
    return sorted(set(options))


def build_situated_context(owner: Any, *, expected: Any = None,
                           event_id: str | None = None) -> dict:
    """Build a read-only situated decision input from actual owners.

    No provider stub is consulted. The returned document is an input contract;
    it is not an actor decision, memory, native rule, or performed action.
    """
    if not hasattr(owner, "snapshot") or not hasattr(owner, "base_owner"):
        _refuse("D02_P3_OWNER_UNAVAILABLE")
    snapshot = _identity(owner.snapshot())
    _check_expected(snapshot, expected)
    base = owner.base_owner
    session = getattr(getattr(base, "fanin", None), "session", None)
    if session is None:
        _refuse("D02_ACTUAL_SESSION_UNAVAILABLE")
    material = _material(session, snapshot["actor"])
    event_ref, event_access = _latest_perceived(
        session, snapshot["actor"], event_id)
    if event_ref is None:
        observation = {
            "status": "HELD",
            "reason": "ACTOR_DID_NOT_PERCEIVE",
            "event_id": event_id,
            "event": None,
            "access_hash": None,
        }
    else:
        observation = {
            "status": "AVAILABLE",
            "event_id": event_ref,
            "event": detached(event_access.get("event")),
            "receipt": detached(event_access.get("receipt")),
            "access_hash": digest(event_access),
        }
    focal_position = _focal_position(session, snapshot["actor"])
    relations = _relations(
        session, snapshot["actor"], event_ref, event_access, focal_position)
    options = _options(material, relations, observation)
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "identity": snapshot,
        "material": material,
        "observation": observation,
        "relations": relations,
        "admissible_options": options,
        "option_semantics": OPTION_SEMANTICS,
        "date_scope": detached(DATE_SCOPE),
        "read_boundary": {
            "world_material": "OBJECTIVE_WORLD_READ",
            "actor_access": "QUALIFIED_PERCEPTION_READ",
            "parent_private_state": "NOT_READ",
            "psyche_store": "NOT_READ",
            "portal_user_view": "NOT_READ",
            "narrative_prose": "NOT_READ",
        },
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D02_SELECTOR",
        "decision": "NOT_EVALUATED",
    }
    readset = {
        "identity": {
            "root": snapshot["root"], "actor": snapshot["actor"],
            "branch": snapshot["branch"], "clock": snapshot["clock"],
            "state_hash": snapshot["state_hash"],
        },
        "material": {
            "source": material.get("source"),
            "material_hash": material.get("material_hash"),
            "world_state_hash": material.get("world_state_hash"),
            "actor_accessible": material.get("actor_accessible"),
        },
        "observation": {
            "event_id": observation.get("event_id"),
            "access_hash": observation.get("access_hash"),
        },
        "relations": [
            {"actor_id": row.get("actor_id"), "source": row.get("source"),
             "access_hash": row.get("access_hash")}
            for row in relations
        ],
        "options": list(options),
        "date_scope": detached(DATE_SCOPE),
    }
    body["readset"] = readset
    body["hash"] = digest(body)
    return detached(body)


__all__ = ["build_situated_context", "SCHEMA", "GRADE"]
