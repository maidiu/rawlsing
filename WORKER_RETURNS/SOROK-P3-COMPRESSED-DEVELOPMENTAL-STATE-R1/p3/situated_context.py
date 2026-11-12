"""D02 read-only situated-field projection over actual world and actor access.

This module reads the existing S47/P2 world material fact, the existing P6
household reader, and C01 actor-access/perception readers. It writes no world,
actor, psychological, or scheduler state and adds no new rule. The result is a
bounded decision-input document for a later P3 proposal/provider call.

Current-clock only: the B02 historical_period reader is present in the
composition, but the selector uses only the current logical-clock period when
an actual B02 plan is established. A historical as-of query is not treated as
current physical state. If no plan is established or the current clock is
outside the plan, the selector returns an exact period hold; it never invents a
period, date or calendar mapping.

Temporal selection uses the actual event time/ordinal, never the current world
clock returned by the actor-access reader. Event access hashes are normalized
so a later world clock cannot change the identity of a previously perceived
event. Event-time shared perception and current objective co-presence are
separate fields; current position alone never creates an observed relation.

Acquired state is read-only: the selector queries the actual PsycheStore for the
explicit later plan scope and runs the existing projections.activate machinery.
It does not write a target, memory, immediate response, performed action or
native rule. A stored record is eligible only when the existing activation
reader says so; contradictions are surfaced, not silently resolved.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RecursionRefusal,
    detached,
    digest,
)

from . import p3_owner, projections, test_rules

GRADE = "SOURCEFREE_S2_ONLY"
P3_GRADE = test_rules.GRADE
SCHEMA = "SOROK_D02_SITUATED_CONTEXT@1"
SOURCE_SCHEMA = "SOROK_D02_SOURCE_CLOSURE@1"
HOUSEHOLD_SLOT = "p6_household"
DATE_SCOPE = {
    "calendar": "HELD_B02_NO_CURRENT_PERIOD",
    "historical_period": "NOT_QUALIFIED",
    "logical_clock_only": True,
}
SELECTION_BASIS = "EVENT_TIME_THEN_ORDINAL_NOT_READ_TIME"
OPTION_SEMANTICS = (
    "SOURCEFREE_ADMISSIBLE_INPUT_LABELS_NOT_ACTOR_CHOICE_OR_PERFORMED_ACTION"
)
B02_INGRESS = {
    "schema": "SOROK_D02_B02_INGRESS_CONTRACT@1",
    "status": "PREREQUISITE_HELD_NO_CURRENT_PERIOD",
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



def _b02_path() -> Path:
    return _WORKER_RETURNS / "SOROK-DUEL-B02-R1" / "historical_period.py"


def _b02_module():
    path = _b02_path()
    if not path.is_file():
        return None
    name = "_d02_historical_period"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        _refuse("D02_B02_IMPORT_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(name, None)
        raise RecursionRefusal("D02_B02_IMPORT_FAILED") from exc
    return module


def _period_source(module: Any = None) -> dict:
    path = _b02_path()
    if not path.is_file():
        return {"status": "UNAVAILABLE", "path": None, "sha256": None}
    return {
        "status": "SELECTED_SOURCE",
        "path": _source_label(path),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "symbols": ["read_material_period", "p3_interval_span",
                    "read_period_plan"],
    }


def _period_ingress(session: Any, snapshot: Mapping[str, Any]) -> dict:
    module = _b02_module()
    source = _period_source(module)
    if module is None:
        return {
            "status": "HELD",
            "reason": "D02_B02_READER_UNAVAILABLE",
            "source": source,
            "date_scope": {
                "calendar": "B02_READER_UNAVAILABLE",
                "historical_period": "NOT_QUALIFIED",
                "logical_clock_only": True,
            },
        }
    try:
        plan = module.read_period_plan(session)
    except RecursionRefusal as exc:
        if str(exc).startswith(("P6_EMPLOYMENT_ABSENT", "P6_PERIOD_ABSENT")):
            return {
                "status": "HELD",
                "reason": str(exc),
                "source": source,
                "date_scope": {
                    "calendar": "B02_READER_PRESENT_NO_CURRENT_PERIOD",
                    "historical_period": "NOT_QUALIFIED",
                    "logical_clock_only": True,
                    "reason": str(exc),
                },
            }
        raise
    holder = session.world().actor_state.get("A")
    if (not isinstance(holder, Mapping)
            or holder.get("actor_id") != snapshot.get("actor")):
        return {
            "status": "HELD",
            "reason": "B02_EMPLOYMENT_HOLDER_NOT_FOCAL",
            "source": source,
            "date_scope": {
                "calendar": "B02_HOLDER_NOT_FOCAL",
                "historical_period": "NOT_QUALIFIED",
                "logical_clock_only": True,
            },
        }
    ticks = plan.get("ticks_per_day")
    anchor_clock = plan.get("anchor_clock")
    anchor_date = plan.get("anchor_date")
    if (type(ticks) is not int or ticks < 1
            or type(anchor_clock) is not int
            or not isinstance(anchor_date, str)):
        _refuse("D02_B02_PLAN_BASIS")
    delta = int(snapshot["clock"]) - anchor_clock
    if delta < 0:
        return {
            "status": "HELD",
            "reason": "B02_CURRENT_BEFORE_ANCHOR",
            "source": source,
            "date_scope": {
                "calendar": "B02_CURRENT_BEFORE_ANCHOR",
                "historical_period": "NOT_QUALIFIED",
                "logical_clock_only": True,
            },
        }
    if delta % ticks:
        return {
            "status": "HELD",
            "reason": "B02_CURRENT_CLOCK_NOT_DAY_ALIGNED",
            "source": source,
            "date_scope": {
                "calendar": "B02_CURRENT_CLOCK_NOT_DAY_ALIGNED",
                "historical_period": "NOT_QUALIFIED",
                "logical_clock_only": True,
            },
        }
    try:
        as_of = date.fromisoformat(anchor_date) + timedelta(days=delta // ticks)
    except ValueError as exc:
        raise RecursionRefusal("D02_B02_ANCHOR_DATE") from exc
    try:
        read = module.read_material_period(session, as_of.isoformat())
    except RecursionRefusal as exc:
        if str(exc).startswith("P6_PERIOD_OUTSIDE_PLAN"):
            return {
                "status": "HELD",
                "reason": "B02_CURRENT_OUTSIDE_PLAN",
                "source": source,
                "date_scope": {
                    "calendar": "B02_CURRENT_OUTSIDE_PLAN",
                    "historical_period": "NOT_QUALIFIED",
                    "logical_clock_only": True,
                },
            }
        raise
    if read.get("logical_tick") != snapshot["clock"]:
        _refuse("D02_B02_LOGICAL_TICK_MISMATCH")
    period = _mapping(read.get("period"), "D02_B02_PERIOD")
    span = module.p3_interval_span(session, period["period_id"])
    employment = read.get("employment")
    employment_doc = None
    if employment is not None:
        employment_doc = _mapping(employment, "D02_B02_EMPLOYMENT")
    return {
        "status": "QUALIFIED_CURRENT_PERIOD",
        "as_of_date": read.get("as_of_date"),
        "logical_tick": read.get("logical_tick"),
        "calendar_basis": read.get("calendar_basis"),
        "clock_basis": read.get("clock_basis"),
        "ticks_per_day": read.get("ticks_per_day"),
        "period": period,
        "employment": employment_doc,
        "employment_status": read.get("employment_status"),
        "employment_scope": (
            "FOCAL_HOUSEHOLD_OBJECTIVE_MATERIAL_NOT_ACTOR_KNOWLEDGE_OR_PARENT"),
        "holder_actor_slot": "A",
        "holder_actor_id": holder.get("actor_id"),
        "interval": read.get("interval"),
        "interval_status": read.get("interval_status"),
        "interval_span": {
            "mode": span.get("mode"),
            "span": span.get("span"),
            "basis": "B02_TYPED_SEAM_READ_ONLY_NOT_APPLIED",
        },
        "plan_source": read.get("plan_source"),
        "employment_source": read.get("employment_source"),
        "provenance": read.get("provenance"),
        "source": source,
        "date_scope": {
            "calendar": "B02_CURRENT_LOGICAL_PERIOD",
            "as_of": read.get("as_of_date"),
            "historical_period": (
                "CURRENT_STATE_ONLY_NOT_HISTORICAL_QUERY"),
            "logical_clock_only": False,
        },
        "read_boundary": {
            "b02_psyche_store": "NOT_READ",
            "b02_psychology_state": "NOT_WRITTEN",
            "historical_query": "CURRENT_STATE_ONLY",
            "knowledge_claim": "NOT_CLAIMED",
        },
    }


def _plan_scope(plan: Any, owner: Any, snapshot: Mapping[str, Any]) -> dict:
    value = _mapping(plan, "D02_ACQUIRED_PLAN")
    for key in ("actor_observed", "material_eligible", "eligible",
                "eligible_modes", "record_hashes"):
        if key in value:
            _refuse("D02_PLAN_OVERRIDE_FORBIDDEN:" + key)
    for key in ("root", "actor", "branch"):
        if value.get(key) != snapshot.get(key):
            _refuse("D02_ACQUIRED_PLAN_IDENTITY:" + key)
    for key in ("source_hash", "registry_hash", "grade", "project",
                "counterpart"):
        _text(value.get(key), "D02_ACQUIRED_PLAN_" + key.upper())
    if value.get("source_hash") != owner.source_hash:
        _refuse("D02_ACQUIRED_PLAN_SOURCE")
    if value.get("registry_hash") != owner.registry.get("hash"):
        _refuse("D02_ACQUIRED_PLAN_REGISTRY")
    if value.get("grade") != P3_GRADE:
        _refuse("D02_ACQUIRED_PLAN_GRADE")
    if value.get("hash"):
        _hash(value.get("hash"), "D02_ACQUIRED_PLAN_HASH")
        if digest({key: item for key, item in value.items()
                   if key != "hash"}) != value["hash"]:
            _refuse("D02_ACQUIRED_PLAN_HASH_MISMATCH")
    if "permitted_rules" in value and value["permitted_rules"] != (
            test_rules.rule_descriptors()):
        _refuse("D02_ACQUIRED_PLAN_RULES")
    selectors = {}
    for key in ("activation_roles", "relation_refs", "obligation_refs"):
        items = value.get(key, [])
        if not isinstance(items, list) or any(
                not isinstance(item, str) or not item for item in items):
            _refuse("D02_ACQUIRED_PLAN_SELECTORS:" + key)
        selectors[key] = list(items)
    role = value.get("interlocutor_role")
    if role is not None:
        _text(role, "D02_ACQUIRED_PLAN_ROLE")
    relation = value.get("relation_ref")
    if relation is not None:
        _text(relation, "D02_ACQUIRED_PLAN_RELATION")
    elif len(selectors["relation_refs"]) == 1:
        relation = selectors["relation_refs"][0]
    return {
        "project": value["project"],
        "counterpart": value["counterpart"],
        "interlocutor_role": role,
        "relation_ref": relation,
        "obligation_refs": selectors["obligation_refs"],
        "activation_roles": selectors["activation_roles"],
        "relation_refs": selectors["relation_refs"],
        "plan_hash": value.get("hash"),
    }


def _activation_context(snapshot: Mapping[str, Any], owner: Any,
                        scope: Mapping[str, Any], material: Mapping[str, Any],
                        observation: Mapping[str, Any]) -> dict:
    material_eligible = None
    if material.get("status") == "AVAILABLE":
        material_eligible = (
            material.get("actor_accessible", {}).get("status") == "PRESENT")
    body = {
        "root": snapshot["root"], "actor": snapshot["actor"],
        "branch": snapshot["branch"], "clock": snapshot["clock"],
        "project": scope["project"], "counterpart": scope["counterpart"],
        "interlocutor_role": scope.get("interlocutor_role"),
        "relation_ref": scope.get("relation_ref"),
        "obligation_refs": list(scope.get("obligation_refs") or []),
        "actor_observed": observation.get("status") == "AVAILABLE",
        "material_eligible": material_eligible,
        "source_refs": [owner.source_hash],
        "grade": P3_GRADE,
    }
    body["hash"] = digest(body)
    return body


def _acquired_state(owner: Any, snapshot: Mapping[str, Any], plan: Any,
                    material: Mapping[str, Any],
                    observation: Mapping[str, Any]) -> dict:
    if plan is None:
        return {
            "status": "NO_PLAN_SCOPE",
            "scope": None,
            "eligible_modes": [],
            "eligible_record_hashes": [],
            "withheld": [],
            "contradictions": [],
            "stored_count": 0,
            "activation_context": None,
            "source_hash": owner.source_hash,
            "registry_hash": owner.registry.get("hash"),
            "native_rule": "MISSING_RULE",
            "memory_formation": "MISSING_RULE",
            "first_person_claims": [],
            "decision": "NOT_EVALUATED",
            "semantics": (
                "SOURCEFREE_ACTIVATION_READ_ONLY_NOT_MEMORY_NATIVE_STATE_OR_ACTION"),
            "readset": {
                "status": "NO_PLAN_SCOPE",
                "eligible_record_hashes": [],
                "withheld_record_hashes": [],
                "contradictions": [],
                "source_hash": owner.source_hash,
                "registry_hash": owner.registry.get("hash"),
            },
        }
    scope = _plan_scope(plan, owner, snapshot)
    context = _activation_context(snapshot, owner, scope, material, observation)
    head_before = owner.store.head()
    records = owner.store.query(
        project=scope["project"], counterpart=scope["counterpart"],
        as_of=snapshot["clock"],
    )
    activation = projections.activate(
        records, identity=snapshot, context=context, registry=owner.registry,
    )
    head_after = owner.store.head()
    if head_before != head_after:
        _refuse("D02_ACQUIRED_STATE_MUTATED")
    entries = activation.get("entries") if isinstance(
        activation.get("entries"), list) else []
    eligible = [entry for entry in entries
                if entry.get("activation") == "ELIGIBLE"]
    withheld = [entry for entry in entries
                if entry.get("activation") != "ELIGIBLE"]
    contradictions = detached(activation.get("contradictions") or [])
    eligible_ids = {row.get("record_id") for row in eligible}
    active_contradictions = [
        pair for pair in contradictions
        if isinstance(pair, (list, tuple)) and len(pair) == 2
        and set(pair) <= eligible_ids
    ]
    if active_contradictions:
        status = "CONTRADICTION"
    elif not entries:
        status = "NO_RECORDS"
    elif eligible:
        status = "ELIGIBLE"
    else:
        status = "HELD_NO_ELIGIBLE_RECORD"
    bounded = lambda rows: [
        {
            "record_hash": row.get("record_hash"),
            "kind": row.get("kind"),
            "mode": row.get("mode"),
            "activation": row.get("activation"),
            "material_eligible": row.get("material_eligible"),
        }
        for row in rows
    ]
    eligible_hashes = [row.get("record_hash") for row in eligible]
    withheld_hashes = [row.get("record_hash") for row in withheld]
    readset = {
        "status": status,
        "query": {
            "project": scope["project"], "counterpart": scope["counterpart"],
            "as_of": snapshot["clock"],
        },
        "activation_context_hash": context["hash"],
        "eligible_record_hashes": eligible_hashes,
        "withheld_record_hashes": withheld_hashes,
        "contradictions": active_contradictions,
        "latent_contradictions": contradictions,
        "stored_count": len(records),
        "source_hash": owner.source_hash,
        "registry_hash": owner.registry.get("hash"),
        "store_head": _store_head_view(head_before),
    }
    return {
        "status": status,
        "scope": {
            "project": scope["project"], "counterpart": scope["counterpart"],
            "interlocutor_role": scope.get("interlocutor_role"),
            "relation_ref": scope.get("relation_ref"),
            "obligation_refs": list(scope.get("obligation_refs") or []),
        },
        "eligible_modes": sorted({row.get("mode") for row in eligible}),
        "eligible": bounded(eligible),
        "eligible_record_hashes": eligible_hashes,
        "withheld": bounded(withheld),
        "withheld_record_hashes": withheld_hashes,
        "contradictions": active_contradictions,
        "latent_contradictions": contradictions,
        "stored_count": len(records),
        "activation_context": {
            "clock": context["clock"],
            "actor_observed": context["actor_observed"],
            "material_eligible": context["material_eligible"],
            "actor_observed_basis": (
                "SELECTED_ACTUAL_PERCEPTION_NOT_LATER_EVENT"),
            "material_eligible_basis": (
                "OBJECTIVE_HOUSEHOLD_ACTOR_PRESENT_NOT_NATIVE_FEASIBILITY"),
            "hash": context["hash"],
        },
        "source_hash": owner.source_hash,
        "registry_hash": owner.registry.get("hash"),
        "native_rule": "MISSING_RULE",
        "memory_formation": "MISSING_RULE",
        "first_person_claims": [],
        "decision": "NOT_EVALUATED",
        "knowledge": (
            "ELIGIBLE_HYPOTHESIS_READ_NOT_GENERAL_MASTERY_OR_NATIVE_STATE"),
        "semantics": (
            "SOURCEFREE_ACTIVATION_READ_ONLY_NOT_MEMORY_NATIVE_STATE_OR_ACTION"),
        "readset": readset,
    }


def _store_head_view(head: Mapping[str, Any]) -> dict:
    value = _mapping(head, "D02_STORE_HEAD")
    return {"hash": value.get("hash"), "count": value.get("count")}


def build_situated_context(owner: Any, *, expected: Any = None,
                           event_id: str | None = None,
                           expected_source_closure: Any = None,
                           plan: Any = None) -> dict:
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
    period = _period_ingress(session, snapshot)
    acquired = _acquired_state(owner, snapshot, plan, material, observation)
    ingress = detached(B02_INGRESS)
    ingress["status"] = (
        "QUALIFIED_CURRENT_PERIOD"
        if period.get("status") == "QUALIFIED_CURRENT_PERIOD"
        else "PREREQUISITE_HELD_NO_CURRENT_PERIOD")
    ingress["reason"] = period.get("reason")
    ingress["period_source"] = period.get("source")
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "identity": snapshot,
        "material": material,
        "observation": observation,
        "relations": relations,
        "admissible_options": options,
        "option_semantics": OPTION_SEMANTICS,
        "period": period,
        "period_source": period.get("source"),
        "acquired_state": acquired,
        "date_scope": detached(period["date_scope"]),
        "b02_ingress": ingress,
        "source_closure": closure,
        "read_boundary": {
            "world_material": "OBJECTIVE_WORLD_READ",
            "material_access": "OBJECTIVE_FOCAL_POSITION_ONLY_NOT_PERCEPTION",
            "actor_access": "QUALIFIED_PERCEPTION_READ",
            "relation_current_position": "OBJECTIVE_POSITION_ONLY",
            "parent_private_state": "NOT_READ",
            "psyche_store": (
                "P3_HEAD_ONLY_NOT_RECORDS"
                if acquired.get("status") == "NO_PLAN_SCOPE"
                else "P3_ACQUIRED_RECORDS_ACTIVATION_READ"),
            "acquired_state": (
                "SOURCEFREE_ACTIVATION_READ_NOT_NATIVE_MEMORY_OR_ACTION"),
            "period": (
                "B02_CURRENT_PERIOD_READ"
                if period.get("status") == "QUALIFIED_CURRENT_PERIOD"
                else "B02_CURRENT_PERIOD_HELD"),
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
            "status": ingress["status"],
            "hash": digest(ingress),
        },
        "period": {
            "status": period.get("status"),
            "reason": period.get("reason"),
            "as_of_date": period.get("as_of_date"),
            "logical_tick": period.get("logical_tick"),
            "period_id": (
                period.get("period", {}).get("period_id")
                if isinstance(period.get("period"), Mapping) else None),
            "plan_source": period.get("plan_source"),
            "employment_source": period.get("employment_source"),
            "source": period.get("source"),
            "interval_status": period.get("interval_status"),
            "interval_span": period.get("interval_span"),
        },
        "acquired_state": acquired.get("readset"),
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
        "date_scope": detached(period["date_scope"]),
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
