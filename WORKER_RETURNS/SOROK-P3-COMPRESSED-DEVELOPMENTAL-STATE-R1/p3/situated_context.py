"""D02 read-only situated-field projection over actual world and actor access.

This module reads the existing S47/P2 world material fact, the existing P6
household reader, and C01 actor-access/perception readers. It writes no world,
actor, psychological, or scheduler state and adds no new rule. The result is a
bounded decision-input document for a later P3 proposal/provider call.

Current-clock only: historical calendar/as-of qualification is B02 and is NOT
BUILT. The selector exposes only the current logical clock and an explicit
B02 ingress hold. It does not invent a period, date or calendar mapping.

Temporal selection uses the actual event time/ordinal, never the current world
clock returned by the actor-access reader. Event access hashes are normalized
so a later world clock cannot change the identity of a previously perceived
event. Event-time shared perception and current objective co-presence are
separate fields; current position alone never creates an observed relation.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RecursionRefusal,
    detached,
    digest,
)

from . import p3_owner

GRADE = "SOURCEFREE_S2_ONLY"
SCHEMA = "SOROK_D02_SITUATED_CONTEXT@1"
SOURCE_SCHEMA = "SOROK_D02_SOURCE_CLOSURE@1"
HOUSEHOLD_SLOT = "p6_household"
DATE_SCOPE = {
    "calendar": "HELD_B02_NOT_BUILT",
    "historical_period": "NOT_QUALIFIED",
    "logical_clock_only": True,
}
SELECTION_BASIS = "EVENT_TIME_THEN_ORDINAL_NOT_READ_TIME"
OPTION_SEMANTICS = (
    "SOURCEFREE_ADMISSIBLE_INPUT_LABELS_NOT_ACTOR_CHOICE_OR_PERFORMED_ACTION"
)
B02_INGRESS = {
    "schema": "SOROK_D02_B02_INGRESS_CONTRACT@1",
    "status": "PREREQUISITE_HELD_NOT_QUALIFIED",
    "owner": "P3 DevelopmentOwner/S46 logical clock + existing P2 objective world",
    "clock_basis": "S46_LOGICAL_TICKS_NOT_CALENDAR_YEARS",
    "required_inputs": [
        "exact root/actor/branch identity",
        "as_of logical clock and period id",
        "period effective_from/effective_to in S46/P2 units",
        "period split event id/effective clock and reason",
        "source/evidence refs and world state hash",
        "material as-of household source/world hash",
        "actor participation/access as-of epoch",
    ],
    "prohibited": [
        "workshop ticks relabeled as calendar years",
        "mock or curated calendar period",
        "period invented by this selector",
        "parent private reason or portal gaze in the readset",
    ],
    "consumer": "p3.situated_context.build_situated_context",
    "first_reader": "RecursionCycle provider context / later P3 proposal input",
    "reconcile_at": "B02 exact qualified cut",
    "contract_doc": "WORKER_RETURNS/SOROK-DUEL-D02-R1/D02_B02_INGRESS_CONTRACT.md",
}
_WORKER_RETURNS = Path(__file__).resolve().parents[2]


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


def _hash(value: Any, code: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        _refuse(code)
    try:
        int(value, 16)
    except ValueError:
        _refuse(code)
    return value.lower()


def _house_module():
    try:
        import house  # type: ignore
    except ImportError:
        root = _WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
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


def _projection_module():
    try:
        from s45_projection import projection  # type: ignore
    except ImportError as exc:
        raise RecursionRefusal("D02_PROJECTION_READER_UNAVAILABLE") from exc
    return projection


def _module_source(module: Any, expected: Path, code: str) -> Path:
    value = getattr(module, "__file__", None)
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    path = Path(value).resolve()
    if path != expected.resolve():
        _refuse(code)
    return path


def _source_label(path: Path) -> str:
    path = Path(path).resolve()
    try:
        return str(path.relative_to(_WORKER_RETURNS))
    except ValueError:
        return str(path)


def _selected_source_files() -> list[tuple[str, Path]]:
    """The exact D02 reader closure plus the existing P3 owner code pins.

    This is deliberately narrower than the repository: the selector's own
    module, the C01 actor-access reader, the P6 household reader, and the P3
    owner/projection/rule/store/engine-contract files that establish the
    identity and head it consumes. It does not add these files to the global
    P3Owner config pin or to every unrelated P3 mode.
    """
    rows: list[tuple[str, Path]] = []
    for row in p3_owner._code_pins().get("files", []):
        path = Path(row["path"]).resolve()
        rows.append((_source_label(path), path))
    supporting = _supporting_module()
    expected_supporting = (
        _WORKER_RETURNS
        / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
        / "developmental_recursion" / "supporting_actor.py"
    )
    supporting_path = _module_source(
        supporting, expected_supporting, "D02_SUPPORTING_SOURCE_IDENTITY")
    house = _house_module()
    expected_house = (
        _WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1" / "house.py")
    house_path = _module_source(
        house, expected_house, "D02_HOUSE_SOURCE_IDENTITY")
    projection = _projection_module()
    expected_projection = (
        _WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
        / "s45_projection" / "projection.py")
    projection_path = _module_source(
        projection, expected_projection, "D02_PROJECTION_SOURCE_IDENTITY")
    situated_path = Path(__file__).resolve()
    p3_init = Path(__file__).with_name("__init__.py").resolve()
    rows.extend([
        (_source_label(situated_path), situated_path),
        (_source_label(p3_init), p3_init),
        (_source_label(supporting_path), supporting_path),
        (_source_label(house_path), house_path),
        (_source_label(projection_path), projection_path),
    ])
    unique: dict[str, Path] = {}
    for label, path in rows:
        unique[label] = path
    return sorted(unique.items(), key=lambda row: row[0])


def _source_closure(files: Any = None) -> dict:
    rows = _selected_source_files() if files is None else list(files)
    result = []
    for label, path in rows:
        label = _text(str(label), "D02_SOURCE_LABEL")
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            _refuse("D02_SOURCE_MISSING:" + label)
        result.append({
            "path": label,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    result.sort(key=lambda row: row["path"])
    if len({row["path"] for row in result}) != len(result):
        _refuse("D02_SOURCE_DUPLICATE")
    return {"schema": SOURCE_SCHEMA, "files": result,
            "hash": digest(result)}


def source_closure() -> dict:
    """Return the exact selected source closure; read-only and no authority."""
    return _source_closure()


def _closure_hash(value: Any, code: str) -> str:
    if isinstance(value, str):
        return _hash(value, code)
    document = _mapping(value, code)
    return _hash(document.get("hash"), code + ":HASH")


def _identity(value: Any) -> dict:
    document = value.document() if hasattr(value, "document") else value
    document = _mapping(document, "D02_IDENTITY_SCHEMA")
    for key in ("root", "actor", "branch"):
        _text(document.get(key), "D02_IDENTITY_" + key.upper())
    clock = document.get("clock")
    if isinstance(clock, bool) or not isinstance(clock, int):
        _refuse("D02_IDENTITY_CLOCK")
    _hash(document.get("state_hash"), "D02_IDENTITY_STATE_HASH")
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


def _check_session_alignment(base_owner: Any, session: Any,
                             snapshot: Mapping[str, Any]) -> None:
    current = base_owner.snapshot()
    for key in ("root", "actor", "branch", "clock"):
        if getattr(current, key) != snapshot.get(key):
            _refuse("D02_STALE_BASE_SESSION:" + key)
    root = session.read_root()
    if root.get("root_hash") != snapshot["root"]:
        _refuse("D02_STALE_SESSION_ROOT")
    if session.branch_id != snapshot["branch"]:
        _refuse("D02_STALE_SESSION_BRANCH")
    if session.clock() != snapshot["clock"]:
        _refuse("D02_STALE_SESSION_CLOCK")


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


def _event_temporal(row: Mapping[str, Any], access: Mapping[str, Any]) -> tuple[int, int]:
    event_time = row.get("event_time")
    if isinstance(event_time, bool) or not isinstance(event_time, int):
        event = access.get("event") if isinstance(access.get("event"), Mapping) else {}
        event_time = event.get("clock")
    if isinstance(event_time, bool) or not isinstance(event_time, int):
        receipt = access.get("receipt") if isinstance(access.get("receipt"), Mapping) else {}
        event_time = receipt.get("clock")
    if isinstance(event_time, bool) or not isinstance(event_time, int):
        _refuse("D02_EVENT_TIME_UNAVAILABLE")
    event = access.get("event") if isinstance(access.get("event"), Mapping) else {}
    access_clock = event.get("clock")
    if (isinstance(access_clock, int) and not isinstance(access_clock, bool)
            and access_clock != event_time):
        _refuse("D02_EVENT_CLOCK_MISMATCH")
    ordinal = row.get("event_ordinal")
    if isinstance(ordinal, bool) or not isinstance(ordinal, int):
        ordinal = -1
    return event_time, ordinal


def _latest_perceived(
    session: Any, actor_id: str, event_id: str | None,
) -> tuple[str | None, dict | None, int | None, int | None]:
    supporting = _supporting_module()
    rows = _events(session)
    if event_id is not None:
        access = supporting.read_actor_access(session, actor_id, event_id)
        if access.get("status") != "PERCEIVED":
            return None, None, None, None
        match = next((
            row for row in rows
            if event_id in (row.get("action_event_id"), row.get("e1_event_id"),
                            row.get("event_id"))
        ), None)
        event_time, ordinal = _event_temporal(match or {}, access)
        return event_id, access, event_time, ordinal
    candidates = []
    for row in rows:
        ref = _event_ref(row)
        if ref is None:
            continue
        access = supporting.read_actor_access(session, actor_id, ref)
        if access.get("status") != "PERCEIVED":
            continue
        event_time, ordinal = _event_temporal(row, access)
        candidates.append((event_time, ordinal, ref, access))
    if not candidates:
        return None, None, None, None
    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
    event_time, ordinal, ref, access = candidates[-1]
    return ref, access, event_time, ordinal


def _access_identity(access: Mapping[str, Any], code: str) -> dict:
    document = _mapping(access, code)
    if document.get("status") != "PERCEIVED":
        _refuse(code + ":STATUS")
    return {
        key: item for key, item in document.items() if key != "world_clock"
    }


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
                "access_basis": "OBJECTIVE_FOCAL_POSITION_NOT_PERCEPTION",
                "knowledge_claim": "NOT_CLAIMED",
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
        "access_basis": "OBJECTIVE_FOCAL_POSITION_NOT_PERCEPTION",
        "knowledge_claim": "NOT_CLAIMED",
        "current_position": position,
        "rooms": detached(rooms),
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
        access_identity = _access_identity(access, "D02_RELATION_ACCESS")
        current_position = public.get("position")
        current_co_present = (
            isinstance(focal_position, str)
            and current_position == focal_position
        )
        receipt = access.get("receipt") if isinstance(
            access.get("receipt"), Mapping) else {}
        event_co_present = receipt.get("channel") == "co_present"
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
            "current_position": current_position,
            "co_present": current_co_present,
            "current_co_present": current_co_present,
            "event_co_present": event_co_present,
            "access_event_id": access.get("event_id"),
            "access_hash": digest(access_identity),
            "access_status": "ELIGIBLE_SHARED_PERCEPTION",
            "access_scope": "PUBLIC_SHARED_PERCEPTION",
            "event_access_scope": "SELECTED_EVENT_SHARED_PERCEPTION",
            "current_scope": "OBJECTIVE_POSITION_ONLY",
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
    if any(
        row.get("event_co_present") is True
        and row.get("current_co_present") is True
        for row in relations
    ):
        options.append("ADDRESS_ELIGIBLE_OTHER")
    return sorted(set(options))


def build_situated_context(owner: Any, *, expected: Any = None,
                           event_id: str | None = None,
                           expected_source_closure: Any = None) -> dict:
    """Build a read-only situated decision input from actual owners.

    No provider stub is consulted. The returned document is an input contract;
    it is not an actor decision, memory, native rule, or performed action.
    """
    if not hasattr(owner, "snapshot") or not hasattr(owner, "base_owner"):
        _refuse("D02_P3_OWNER_UNAVAILABLE")
    snapshot = _identity(owner.snapshot())
    _check_expected(snapshot, expected)
    store = getattr(owner, "store", None)
    if store is not None and hasattr(store, "pending") and store.pending():
        _refuse("D02_PENDING_OPERATION")
    base = owner.base_owner
    session = getattr(getattr(base, "fanin", None), "session", None)
    if session is None:
        _refuse("D02_ACTUAL_SESSION_UNAVAILABLE")
    _check_session_alignment(base, session, snapshot)
    closure = source_closure()
    if expected_source_closure is not None:
        expected_hash = _closure_hash(
            expected_source_closure, "D02_EXPECTED_SOURCE_CLOSURE")
        if expected_hash != closure["hash"]:
            _refuse("D02_SOURCE_CLOSURE_CHANGED")
    material = _material(session, snapshot["actor"])
    event_ref, event_access, event_time, event_ordinal = _latest_perceived(
        session, snapshot["actor"], event_id)
    if event_ref is None:
        observation = {
            "status": "HELD",
            "reason": "ACTOR_DID_NOT_PERCEIVE",
            "event_id": event_id,
            "event": None,
            "selected_event_clock": None,
            "selected_event_ordinal": None,
            "selection_basis": SELECTION_BASIS,
            "read_world_clock": snapshot["clock"],
            "access_hash": None,
        }
    else:
        access_identity = _access_identity(
            event_access, "D02_OBSERVATION_ACCESS")
        observation = {
            "status": "AVAILABLE",
            "event_id": event_ref,
            "event": detached(event_access.get("event")),
            "receipt": detached(event_access.get("receipt")),
            "selected_event_clock": event_time,
            "selected_event_ordinal": event_ordinal,
            "selection_basis": SELECTION_BASIS,
            "read_world_clock": event_access.get("world_clock"),
            "access_hash": digest(access_identity),
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
        "b02_ingress": detached(B02_INGRESS),
        "source_closure": closure,
        "read_boundary": {
            "world_material": "OBJECTIVE_WORLD_READ",
            "material_access": "OBJECTIVE_FOCAL_POSITION_ONLY_NOT_PERCEPTION",
            "actor_access": "QUALIFIED_PERCEPTION_READ",
            "relation_current_position": "OBJECTIVE_POSITION_ONLY",
            "parent_private_state": "NOT_READ",
            "psyche_store": "P3_HEAD_ONLY_NOT_RECORDS",
            "portal_user_view": "NOT_READ",
            "narrative_prose": "NOT_READ",
            "source_identity": "D02_SELECTED_CLOSURE",
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
        "source_closure": {
            "hash": closure["hash"],
            "files": [row["path"] for row in closure["files"]],
        },
        "b02_ingress": {
            "status": B02_INGRESS["status"],
            "hash": digest(B02_INGRESS),
        },
        "material": {
            "source": material.get("source"),
            "material_hash": material.get("material_hash"),
            "world_state_hash": material.get("world_state_hash"),
            "actor_accessible": material.get("actor_accessible"),
            "access_basis": material.get("access_basis"),
            "knowledge_claim": material.get("knowledge_claim"),
        },
        "observation": {
            "event_id": observation.get("event_id"),
            "selected_event_clock": observation.get("selected_event_clock"),
            "selected_event_ordinal": observation.get("selected_event_ordinal"),
            "access_hash": observation.get("access_hash"),
        },
        "relations": [
            {"actor_id": row.get("actor_id"), "source": row.get("source"),
             "event_co_present": row.get("event_co_present"),
             "current_co_present": row.get("current_co_present"),
             "access_hash": row.get("access_hash")}
            for row in relations
        ],
        "options": list(options),
        "date_scope": detached(DATE_SCOPE),
    }
    body["readset"] = readset
    body["hash"] = digest(body)
    return detached(body)


__all__ = [
    "build_situated_context",
    "source_closure",
    "SCHEMA",
    "GRADE",
    "B02_INGRESS",
]
