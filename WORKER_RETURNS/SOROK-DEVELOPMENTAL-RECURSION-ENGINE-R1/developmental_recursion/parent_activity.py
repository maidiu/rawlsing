"""Bounded independent parent material antecedent and current-clock activity.

The parent is the stable supporting actor registered by C01. Its ordinary
material state lives in the existing P2 world actor state; its activity and
antecedent changes are C12 episodes and, for performed activity, real world
events authored by that parent. No second scheduler, parent world, time ledger
or psychological model is created. Dated historical periods remain HELD because
B02 calendar qualification is not built.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
from pathlib import Path
from typing import Any, Iterable, Mapping

from .contracts import RecursionRefusal, canonical, detached, digest
from .supporting_actor import _StoreWrite, read_supporting_actor

PARENT_MATERIAL_SCHEMA = "SOROK_P2_PARENT_MATERIAL@1"
PARENT_MATERIAL_READ_SCHEMA = "SOROK_P2_PARENT_MATERIAL_READ@1"
PARENT_FEASIBLE_SCHEMA = "SOROK_P2_PARENT_FEASIBLE_ACTIONS@1"
PARENT_ACTIVITY_RECEIPT_SCHEMA = "SOROK_P2_PARENT_ACTIVITY_RECEIPT@1"
PARENT_CIRCUMSTANCE_RECEIPT_SCHEMA = "SOROK_P2_PARENT_CIRCUMSTANCE_RECEIPT@1"
PARENT_HISTORY_SCHEMA = "SOROK_P2_PARENT_HISTORY@1"
PARENT_MATERIAL_KIND = "P2_PARENT_MATERIAL_ANTECEDENT"
PARENT_ACTIVITY_KIND = "P2_PARENT_ACTIVITY"
PARENT_CIRCUMSTANCE_KIND = "P2_PARENT_CIRCUMSTANCE"
PARENT_ACTIVITY_EVENT_KIND = "MATERIAL_ACTIVITY"
PARENT_GRADE = "SOURCEFREE_S2_ONLY"
PARENT_B02_HOLD = "HELD_B02_CALENDAR_ABSENT"
PARENT_MATERIAL_BOUNDARY = {
    "owner": "PARENT_ACTOR_LOCAL_P2_STATE",
    "household_cash": "NOT_READ",
    "household_stock_shared": False,
    "household_spend_permission": "C03_B04_HELD",
    "double_counting": "NO_HOUSEHOLD_EFFECT_APPLIED",
}
PARENT_HISTORICAL_INGRESS = {
    "status": PARENT_B02_HOLD,
    "required": [
        "B02_PERIOD_BOUNDARY",
        "B02_AS_OF_CLOCK_MAPPING",
        "SOURCE_PERIOD_REF",
        "MATERIAL_SOURCE_BINDING",
    ],
    "dates_claimed": False,
}


def _material_boundary(currency_unit: str | None = None) -> dict:
    boundary = dict(PARENT_MATERIAL_BOUNDARY)
    if _text(currency_unit):
        boundary["parent_currency_unit"] = currency_unit
    boundary["household_currency_unit"] = "NOT_READ"
    boundary["currency_conversion"] = "NOT_APPLIED"
    return boundary


EMPLOYMENT_STATES = frozenset({"employed", "unemployed", "UNKNOWN"})
ACTIVITIES = frozenset({"PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"})
MATERIAL_CONTENT_FIELDS = frozenset({
    "schema", "grade", "actor_id", "source_ref", "employment_status",
    "wage_units_per_hour", "debt_units", "care_hours_due", "cash_units",
    "free_hours", "currency_unit",
})
MATERIAL_BINDING_FIELDS = frozenset({"root", "branch", "epoch", "source"})
MATERIAL_STORED_FIELDS = MATERIAL_CONTENT_FIELDS | MATERIAL_BINDING_FIELDS
CHANGE_FIELDS = frozenset({
    "employment_status", "wage_units_per_hour", "debt_units",
    "care_hours_due", "free_hours",
})
WORK_HOURS = 2
CARE_HOURS = 2
DEBT_PAYMENT = 4


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonneg_int(value: Any) -> bool:
    return type(value) is int and value >= 0


def _material_source(document: Mapping[str, Any]) -> str:
    return digest({key: value for key, value in document.items()
                   if key not in MATERIAL_BINDING_FIELDS})


def _material_content(fixture: Mapping[str, Any]) -> dict:
    if not isinstance(fixture, Mapping) or set(fixture) != MATERIAL_CONTENT_FIELDS:
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    content = detached(fixture)
    if (content.get("schema") != PARENT_MATERIAL_SCHEMA
            or content.get("grade") != PARENT_GRADE
            or not _text(content.get("actor_id"))
            or not _text(content.get("source_ref"))
            or content.get("employment_status") not in EMPLOYMENT_STATES
            or not all(_nonneg_int(content.get(key)) for key in (
                "wage_units_per_hour", "debt_units", "care_hours_due",
                "cash_units", "free_hours"))):
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    return content


def parent_material_fixture(*, actor_id: str, source_ref: str,
                            employment_status: str, wage_units_per_hour: int,
                            debt_units: int, care_hours_due: int,
                            cash_units: int, free_hours: int,
                            currency_unit: str = "parent_sourcefree_currency_unit") -> dict:
    return _material_content({
        "schema": PARENT_MATERIAL_SCHEMA,
        "grade": PARENT_GRADE,
        "actor_id": actor_id,
        "source_ref": source_ref,
        "employment_status": employment_status,
        "wage_units_per_hour": wage_units_per_hour,
        "debt_units": debt_units,
        "care_hours_due": care_hours_due,
        "cash_units": cash_units,
        "free_hours": free_hours,
        "currency_unit": currency_unit,
    })


def _parent_registration(session, parent_id: str) -> dict:
    if not _text(parent_id):
        raise RecursionRefusal("PARENT_ACTOR_SCHEMA")
    return read_supporting_actor(session, parent_id)


@contextmanager
def _parent_write_lock(session):
    """Serialize one parent's read-modify-write activity unit.

    parent_activity has its own read/evaluate/write sequence; without a lock,
    two callers could both read the same material source and each admit an
    activity, losing one cash/time effect or duplicating an event. The lock is
    per state root, not a new scheduler or owner.
    """
    root = Path(session.state_root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / "parent_activity.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _parent_material_history(session, alias: str, parent_id: str) -> list[tuple[dict, str]]:
    """Return ordered parent material/activity/circumstance episodes and sources."""
    rows = []
    for episode in session.product.store.episodes(session.branch_id):
        if episode.get("actor_id") != alias:
            continue
        kind = episode.get("kind")
        if kind not in {PARENT_MATERIAL_KIND, PARENT_ACTIVITY_KIND,
                        PARENT_CIRCUMSTANCE_KIND}:
            continue
        body = episode.get("body") or {}
        if body.get("actor_id") != parent_id:
            raise RecursionRefusal("PARENT_MATERIAL_HISTORY_MISMATCH")
        source = (body.get("material_source") if kind == PARENT_MATERIAL_KIND
                  else body.get("material_after_source"))
        if not _text(source):
            raise RecursionRefusal("PARENT_MATERIAL_HISTORY_MISSING")
        rows.append((episode, source))
    if not rows:
        raise RecursionRefusal("PARENT_MATERIAL_HISTORY_MISSING")
    return rows


def _validate_material(session, *, parent_id: str, alias: str,
                       document: Any) -> dict:
    if (not isinstance(document, Mapping)
            or set(document) != MATERIAL_STORED_FIELDS):
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    stored = detached(document)
    world = session.world()
    root = session.read_root()
    if (stored.get("schema") != PARENT_MATERIAL_SCHEMA
            or stored.get("grade") != PARENT_GRADE
            or stored.get("actor_id") != parent_id
            or stored.get("root") != root["root_hash"]
            or stored.get("branch") != session.branch_id):
        raise RecursionRefusal("PARENT_MATERIAL_SOURCE_OR_ROOT_MISMATCH")
    epoch = stored.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("PARENT_MATERIAL_SOURCE_OR_ROOT_MISMATCH")
    if stored.get("source") != _material_source(stored):
        raise RecursionRefusal("PARENT_MATERIAL_SOURCE_OR_ROOT_MISMATCH")
    if stored.get("employment_status") not in EMPLOYMENT_STATES:
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    if not _text(stored.get("currency_unit")):
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    if not all(_nonneg_int(stored.get(key)) for key in (
            "wage_units_per_hour", "debt_units", "care_hours_due",
            "cash_units", "free_hours")):
        raise RecursionRefusal("PARENT_MATERIAL_SCHEMA")
    row = world.actor_state.get(alias)
    if not isinstance(row, Mapping) or row.get("actor_id") != parent_id:
        raise RecursionRefusal("PARENT_MATERIAL_ACTOR_MISMATCH")
    return stored


def _read_material(session, *, parent_id: str, as_actor: str | None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    registration = _parent_registration(session, parent_id)
    alias = registration["alias"]
    row = session.world().actor_state.get(alias)
    document = row.get("material") if isinstance(row, Mapping) else None
    if document is None:
        raise RecursionRefusal("PARENT_MATERIAL_ABSENT")
    stored = _validate_material(
        session, parent_id=parent_id, alias=alias, document=document)
    history = _parent_material_history(session, alias, parent_id)
    if history[-1][1] != stored["source"]:
        raise RecursionRefusal("PARENT_MATERIAL_HISTORY_MISMATCH")
    return {
        "schema": PARENT_MATERIAL_READ_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "role": registration["role"],
        "root": stored["root"],
        "branch": stored["branch"],
        "clock": session.world().clock,
        "epoch": stored["epoch"],
        "source": stored["source"],
        "source_ref": stored["source_ref"],
        "material": {key: stored[key] for key in (
            "employment_status", "wage_units_per_hour", "debt_units",
            "care_hours_due", "cash_units", "free_hours", "currency_unit")},
        "period_qualification": PARENT_B02_HOLD,
        "historical_dates": "NOT_AVAILABLE",
        "historical_ingress": dict(PARENT_HISTORICAL_INGRESS),
        "material_boundary": _material_boundary(stored["currency_unit"]),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "NOT_READ",
    }


def read_parent_material(session, parent_id: str, *, as_actor: str | None) -> dict:
    return _read_material(session, parent_id=parent_id, as_actor=as_actor)


def _activity_parameters(activity: str, material: Mapping[str, Any], *,
                         hours: Any = None, payment: Any = None) -> dict:
    if activity == "PAID_WORK":
        value = WORK_HOURS if hours is None else hours
        if type(value) is not int or not 1 <= value <= 24:
            raise RecursionRefusal("PARENT_ACTIVITY_PARAMETERS")
        return {"hours": value}
    if activity == "CARE_DEPENDENT":
        value = min(CARE_HOURS, material["care_hours_due"]) if hours is None else hours
        if type(value) is not int or not 0 <= value <= 24:
            raise RecursionRefusal("PARENT_ACTIVITY_PARAMETERS")
        return {"hours": value}
    if activity == "PAY_DEBT":
        value = min(DEBT_PAYMENT, material["debt_units"]) if payment is None else payment
        if type(value) is not int or not 0 <= value <= 1_000_000:
            raise RecursionRefusal("PARENT_ACTIVITY_PARAMETERS")
        return {"payment": value}
    raise RecursionRefusal("PARENT_ACTIVITY_UNKNOWN")


def _evaluate_activity(material: Mapping[str, Any], activity: str,
                       parameters: Mapping[str, Any]) -> dict:
    reasons = []
    after = {key: material[key] for key in (
        "employment_status", "wage_units_per_hour", "debt_units",
        "care_hours_due", "cash_units", "free_hours", "currency_unit")}
    if activity == "PAID_WORK":
        hours = parameters["hours"]
        if material["employment_status"] == "UNKNOWN":
            reasons.append("UNKNOWN_EMPLOYMENT")
        elif material["employment_status"] != "employed":
            reasons.append("EMPLOYMENT_NOT_AVAILABLE")
        if material["wage_units_per_hour"] <= 0:
            reasons.append("NO_WAGE")
        if material["free_hours"] < hours:
            reasons.append("NO_FREE_HOURS")
        if not reasons:
            after["cash_units"] += material["wage_units_per_hour"] * hours
            after["free_hours"] -= hours
    elif activity == "CARE_DEPENDENT":
        hours = parameters["hours"]
        if material["care_hours_due"] < 1:
            reasons.append("NO_CARE_OBLIGATION")
        elif hours > material["care_hours_due"]:
            reasons.append("CARE_EXCEEDS_DUE")
        elif hours < 1:
            reasons.append("NO_CARE_HOURS")
        if material["free_hours"] < hours:
            reasons.append("NO_FREE_HOURS")
        if not reasons:
            after["care_hours_due"] -= hours
            after["free_hours"] -= hours
    elif activity == "PAY_DEBT":
        payment = parameters["payment"]
        if material["debt_units"] < 1:
            reasons.append("NO_DEBT")
        elif payment > material["debt_units"]:
            reasons.append("PAYMENT_EXCEEDS_DEBT")
        elif payment < 1:
            reasons.append("NO_PAYMENT")
        if material["cash_units"] < payment:
            reasons.append("INSUFFICIENT_CASH")
        if not reasons:
            after["debt_units"] -= payment
            after["cash_units"] -= payment
    else:
        reasons.append("PARENT_ACTIVITY_UNKNOWN")
    return {
        "activity": activity,
        "parameters": detached(parameters),
        "status": "REFUSED" if reasons else "ADMISSIBLE",
        "reasons": reasons,
        "after_material": after,
    }


def _options(material: Mapping[str, Any]) -> list[dict]:
    result = []
    unchanged = {key: material[key] for key in (
        "employment_status", "wage_units_per_hour", "debt_units",
        "care_hours_due", "cash_units", "free_hours", "currency_unit")}
    for activity in ("PAID_WORK", "CARE_DEPENDENT", "PAY_DEBT"):
        if activity == "CARE_DEPENDENT" and material["care_hours_due"] < 1:
            result.append({
                "activity": activity,
                "parameters": {"hours": 0},
                "status": "REFUSED",
                "reasons": ["NO_CARE_OBLIGATION"],
                "after_material": unchanged,
            })
            continue
        if activity == "PAY_DEBT" and material["debt_units"] < 1:
            result.append({
                "activity": activity,
                "parameters": {"payment": 0},
                "status": "REFUSED",
                "reasons": ["NO_DEBT"],
                "after_material": unchanged,
            })
            continue
        parameters = _activity_parameters(activity, material)
        result.append(_evaluate_activity(material, activity, parameters))
    return result


def parent_feasible_actions(session, parent_id: str, *,
                            as_actor: str | None) -> dict:
    material = _read_material(session, parent_id=parent_id, as_actor=as_actor)
    options = _options(material["material"])
    return {
        "schema": PARENT_FEASIBLE_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": material["alias"],
        "root": material["root"],
        "branch": material["branch"],
        "clock": material["clock"],
        "source": material["source"],
        "material": material["material"],
        "options": options,
        "option_count": len(options),
        "admissible": [row["activity"] for row in options
                       if row["status"] == "ADMISSIBLE"],
        "period_qualification": PARENT_B02_HOLD,
        "historical_dates": "NOT_AVAILABLE",
        "historical_ingress": dict(PARENT_HISTORICAL_INGRESS),
        "material_boundary": _material_boundary(
            material["material"].get("currency_unit")),
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
        "private_state": "NOT_READ",
        "material_reader": "parent_activity.parent_feasible_actions",
    }


def _material_document(session, parent_id: str, content: Mapping[str, Any]) -> dict:
    world = session.world()
    root = session.read_root()
    document = {**detached(content), "root": root["root_hash"],
                "branch": session.branch_id, "epoch": world.clock}
    document["source"] = _material_source(document)
    return document


def _establish_parent_material(session, parent_id: str, *, fixture: Mapping[str, Any]) -> dict:
    registration = _parent_registration(session, parent_id)
    alias = registration["alias"]
    content = _material_content(fixture)
    if content["actor_id"] != parent_id:
        raise RecursionRefusal("PARENT_MATERIAL_ACTOR_MISMATCH")
    world = session.world()
    root = session.read_root()
    row = world.actor_state.get(alias)
    existing = row.get("material") if isinstance(row, Mapping) else None
    document = _material_document(session, parent_id, content)
    if existing is not None:
        stored = _validate_material(
            session, parent_id=parent_id, alias=alias, document=existing)
        if stored == document:
            result = _read_material(session, parent_id=parent_id, as_actor=parent_id)
            result["status"] = "UNCHANGED"
            return result
        raise RecursionRefusal("PARENT_MATERIAL_ALREADY_ESTABLISHED")
    store = session.product.store
    all_episodes = store.episodes(session.branch_id)
    episodes = [
        episode for episode in all_episodes
        if episode.get("actor_id") == alias
        and episode.get("kind") == PARENT_MATERIAL_KIND
        and (episode.get("body") or {}).get("source") == document["source"]
        and (episode.get("body") or {}).get("source_ref")
        == document["source_ref"]
    ]
    if len(episodes) > 1:
        raise RecursionRefusal("PARENT_MATERIAL_DUPLICATE_ANTECEDENT")
    if episodes:
        chosen_id = episodes[0]["episode_id"]
        chosen_index = next(
            index for index, episode in enumerate(all_episodes)
            if episode.get("episode_id") == chosen_id)
        later = [
            episode for episode in all_episodes[chosen_index + 1:]
            if episode.get("actor_id") == alias
            and episode.get("kind") in {
                PARENT_MATERIAL_KIND, PARENT_ACTIVITY_KIND,
                PARENT_CIRCUMSTANCE_KIND}
        ]
        if later:
            raise RecursionRefusal("PARENT_MATERIAL_RECOVERY_STALE")
    with _StoreWrite(store):
        if episodes:
            body = episodes[0].get("body") or {}
            material = _material_content(body.get("material"))
            stored = {
                **material,
                "root": body.get("root"),
                "branch": body.get("branch"),
                "epoch": body.get("epoch"),
                "source": body.get("source"),
            }
            if (stored["root"] != root["root_hash"]
                    or stored["branch"] != session.branch_id
                    or stored["source"] != document["source"]):
                raise RecursionRefusal("PARENT_MATERIAL_RECOVERY_MISMATCH")
            _validate_material(
                session, parent_id=parent_id, alias=alias, document=stored)
            world.actor_state[alias]["material"] = stored
            session.product._checkpoint(session.branch_id, world.clock, world)
            status = "RECOVERED"
        else:
            store.append_episode(
                session.branch_id, actor_id=alias, kind=PARENT_MATERIAL_KIND,
                clock=world.clock,
                body={
                    "schema": PARENT_MATERIAL_SCHEMA,
                    "grade": PARENT_GRADE,
                    "root": document["root"],
                    "branch": document["branch"],
                    "epoch": document["epoch"],
                    "actor_id": parent_id,
                    "alias": alias,
                    "source": document["source"],
                    "source_ref": document["source_ref"],
                    "material_source": document["source"],
                    "material": content,
                },
            )
            world.actor_state[alias]["material"] = document
            session.product._checkpoint(session.branch_id, world.clock, world)
            status = "REGISTERED"
    result = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    result["status"] = status
    return result


def establish_parent_material(session, parent_id: str, *,
                              fixture: Mapping[str, Any]) -> dict:
    with _parent_write_lock(session):
        return _establish_parent_material(session, parent_id, fixture=fixture)


def _operation_episodes(session, alias: str, operation_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias
        and row.get("kind") in {PARENT_ACTIVITY_KIND, PARENT_CIRCUMSTANCE_KIND}
        and (row.get("body") or {}).get("operation_id") == operation_id
    ]


def _apply_changes(content: Mapping[str, Any], changes: Mapping[str, Any]) -> dict:
    result = {key: content[key] for key in (
        "schema", "grade", "actor_id", "source_ref", "employment_status",
        "wage_units_per_hour", "debt_units", "care_hours_due", "cash_units",
        "free_hours", "currency_unit")}
    for key, value in changes.items():
        if key == "cash_units":
            raise RecursionRefusal("PARENT_CASH_REQUIRES_ACTIVITY")
        if key not in CHANGE_FIELDS:
            raise RecursionRefusal("PARENT_CIRCUMSTANCE_SCHEMA")
        if key == "employment_status":
            if value not in EMPLOYMENT_STATES:
                raise RecursionRefusal("PARENT_CIRCUMSTANCE_SCHEMA")
        elif not _nonneg_int(value):
            raise RecursionRefusal("PARENT_CIRCUMSTANCE_SCHEMA")
        result[key] = value
    return result


def _commit_parent_circumstances(session, parent_id: str, *, operation_id: str,
                                 changes: Mapping[str, Any], source_ref: str,
                                 expected_clock: int | None = None) -> dict:
    if not _text(operation_id) or not _text(source_ref):
        raise RecursionRefusal("PARENT_CIRCUMSTANCE_SCHEMA")
    if not isinstance(changes, Mapping) or not changes:
        raise RecursionRefusal("PARENT_CIRCUMSTANCE_SCHEMA")
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    alias = material["alias"]
    if expected_clock is not None and expected_clock != material["clock"]:
        raise RecursionRefusal("PARENT_CIRCUMSTANCE_CLOCK_MISMATCH")
    episodes = _operation_episodes(session, alias, operation_id)
    if len(episodes) > 1:
        raise RecursionRefusal("PARENT_OPERATION_DUPLICATE")
    if episodes:
        body = episodes[0].get("body") or {}
        if (body.get("actor_id") != parent_id
                or body.get("changes") != detached(changes)
                or body.get("source_ref") != source_ref):
            raise RecursionRefusal("PARENT_OPERATION_REUSE_MISMATCH")
        if material["source"] != body.get("material_after_source"):
            raise RecursionRefusal("PARENT_CIRCUMSTANCE_REPLAY_STALE")
        receipt = dict(body.get("receipt") or {})
        receipt["status"] = "REPLAY"
        return receipt
    content = _material_content({
        **{key: material["material"][key] for key in (
            "employment_status", "wage_units_per_hour", "debt_units",
            "care_hours_due", "cash_units", "free_hours", "currency_unit")},
        "schema": PARENT_MATERIAL_SCHEMA,
        "grade": PARENT_GRADE,
        "actor_id": parent_id,
        "source_ref": source_ref,
    })
    after_content = _apply_changes(content, changes)
    document = _material_document(session, parent_id, after_content)
    if document["source"] == material["source"]:
        return {
            "schema": PARENT_CIRCUMSTANCE_RECEIPT_SCHEMA,
            "grade": PARENT_GRADE,
            "status": "UNCHANGED",
            "operation_id": operation_id,
            "actor_id": parent_id,
            "alias": alias,
            "source_ref": source_ref,
            "changes": detached(changes),
            "before_material_source": material["source"],
            "after_material_source": document["source"],
            "clock": material["clock"],
            "event_effect": "NONE",
            "operation_kind": "ANTECEDENT_MATERIAL_CHANGE",
            "period_qualification": PARENT_B02_HOLD,
        }
    receipt = {
        "schema": PARENT_CIRCUMSTANCE_RECEIPT_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "CHANGED",
        "operation_id": operation_id,
        "actor_id": parent_id,
        "alias": alias,
        "source_ref": source_ref,
        "changes": detached(changes),
        "before_material_source": material["source"],
        "after_material_source": document["source"],
        "clock": material["clock"],
        "event_effect": "NONE",
        "operation_kind": "ANTECEDENT_MATERIAL_CHANGE",
        "period_qualification": PARENT_B02_HOLD,
    }
    store = session.product.store
    world = session.world()
    with _StoreWrite(store):
        store.append_episode(
            session.branch_id, actor_id=alias, kind=PARENT_CIRCUMSTANCE_KIND,
            clock=world.clock,
            body={
                "schema": PARENT_CIRCUMSTANCE_RECEIPT_SCHEMA,
                "grade": PARENT_GRADE,
                "root": document["root"],
                "branch": document["branch"],
                "epoch": document["epoch"],
                "actor_id": parent_id,
                "alias": alias,
                "operation_id": operation_id,
                "source_ref": source_ref,
                "changes": detached(changes),
                "material_before_source": material["source"],
                "material_after_source": document["source"],
                "receipt": receipt,
            },
        )
        world.actor_state[alias]["material"] = document
        session.product._checkpoint(session.branch_id, world.clock, world)
    return receipt


def commit_parent_circumstances(session, parent_id: str, *, operation_id: str,
                                changes: Mapping[str, Any], source_ref: str,
                                expected_clock: int | None = None) -> dict:
    with _parent_write_lock(session):
        return _commit_parent_circumstances(
            session, parent_id, operation_id=operation_id, changes=changes,
            source_ref=source_ref, expected_clock=expected_clock)



def _record_parent_activity(session, parent_id: str, *, operation_id: str,
                            activity: str, hours: int | None = None,
                            payment: int | None = None,
                            expected_clock: int | None = None) -> dict:
    if not _text(operation_id) or activity not in ACTIVITIES:
        raise RecursionRefusal("PARENT_ACTIVITY_SCHEMA")
    material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    alias = material["alias"]
    if expected_clock is not None and expected_clock != material["clock"]:
        raise RecursionRefusal("PARENT_ACTIVITY_CLOCK_MISMATCH")
    parameters = _activity_parameters(
        activity, material["material"], hours=hours, payment=payment)
    episodes = _operation_episodes(session, alias, operation_id)
    if len(episodes) > 1:
        raise RecursionRefusal("PARENT_OPERATION_DUPLICATE")
    if episodes:
        body = episodes[0].get("body") or {}
        if (body.get("actor_id") != parent_id
                or body.get("activity") != activity
                or body.get("parameters") != parameters):
            raise RecursionRefusal("PARENT_OPERATION_REUSE_MISMATCH")
        if material["source"] != body.get("material_after_source"):
            raise RecursionRefusal("PARENT_ACTIVITY_REPLAY_STALE")
        receipt = dict(body.get("receipt") or {})
        receipt["status"] = "REPLAY"
        return receipt
    evaluation = _evaluate_activity(
        material["material"], activity, parameters)
    if evaluation["status"] != "ADMISSIBLE":
        raise RecursionRefusal(
            "PARENT_ACTIVITY_NOT_FEASIBLE:" + ",".join(evaluation["reasons"]))
    content = _material_content({
        **evaluation["after_material"],
        "schema": PARENT_MATERIAL_SCHEMA,
        "grade": PARENT_GRADE,
        "actor_id": parent_id,
        "source_ref": material["source_ref"],
    })
    after_document = _material_document(session, parent_id, content)
    world = session.world()
    clock = world.clock
    location = world.positions.get(alias)
    if not _text(location):
        raise RecursionRefusal("PARENT_ACTIVITY_POSITION_MISSING")
    activity_source = digest({
        "schema": PARENT_ACTIVITY_RECEIPT_SCHEMA,
        "operation_id": operation_id,
        "actor_id": parent_id,
        "activity": activity,
        "parameters": parameters,
        "clock": clock,
        "material_before_source": material["source"],
        "material_after_source": after_document["source"],
    })
    summaries = {
        "PAID_WORK": "The parent works a paid shift.",
        "CARE_DEPENDENT": "The parent provides care at home.",
        "PAY_DEBT": "The parent pays down a debt.",
    }
    from bp4.world import make_event, owner_receipt
    receipt = owner_receipt(
        act=PARENT_ACTIVITY_EVENT_KIND, actor_id=alias, clock=clock,
        location=location)
    event = make_event(
        clock=clock, kind=PARENT_ACTIVITY_EVENT_KIND, actor_id=alias,
        location=location, summary=summaries[activity],
        body={
            "activity": activity,
            "parameters": parameters,
            "currency_unit": material["material"]["currency_unit"],
            "parent_actor_id": parent_id,
            "parent_alias": alias,
            "material_before_source": material["source"],
            "material_after_source": after_document["source"],
            "activity_source": activity_source,
            "period_qualification": PARENT_B02_HOLD,
            "visibility": "PARENT_ORDINARY_ACTIVITY",
            "household_effect": "NONE_PARENT_LOCAL_ONLY",
            "child_request": "NOT_EVALUATED",
        },
        receipt=receipt, sequence=len(world.events),
    )
    world.add_event(event)
    activity_receipt = {
        "schema": PARENT_ACTIVITY_RECEIPT_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "ADMITTED",
        "operation_id": operation_id,
        "actor_id": parent_id,
        "alias": alias,
        "activity": activity,
        "parameters": parameters,
        "currency_unit": material["material"]["currency_unit"],
        "clock": clock,
        "event_id": event["event_id"],
        "event_hash": event["hash"],
        "event_kind": event["kind"],
        "event_authored_by": alias,
        "perception_channel": "own_action",
        "activity_source": activity_source,
        "before_material_source": material["source"],
        "after_material_source": after_document["source"],
        "period_qualification": PARENT_B02_HOLD,
        "historical_ingress": dict(PARENT_HISTORICAL_INGRESS),
        "material_boundary": dict(PARENT_MATERIAL_BOUNDARY),
        "household_effect": "NONE_PARENT_LOCAL_ONLY",
        "child_request": "NOT_EVALUATED",
        "nadia_state": "NOT_READ",
    }
    store = session.product.store
    with _StoreWrite(store):
        store.append_world_event(session.branch_id, event)
        store.record_perception(
            session.branch_id, actor_id=alias, event_id=event["event_id"],
            clock=clock, channel="own_action")
        store.append_episode(
            session.branch_id, actor_id=alias, kind=PARENT_ACTIVITY_KIND,
            clock=clock,
            body={
                "schema": PARENT_ACTIVITY_RECEIPT_SCHEMA,
                "grade": PARENT_GRADE,
                "root": session.read_root()["root_hash"],
                "branch": session.branch_id,
                "epoch": after_document["epoch"],
                "actor_id": parent_id,
                "alias": alias,
                "operation_id": operation_id,
                "activity": activity,
                "parameters": parameters,
                "source_ref": material["source_ref"],
                "material_before_source": material["source"],
                "material_after_source": after_document["source"],
                "event_id": event["event_id"],
                "event_hash": event["hash"],
                "receipt": activity_receipt,
            },
        )
        world.actor_state[alias]["material"] = after_document
        session.product._checkpoint(session.branch_id, world.clock, world)
    return activity_receipt


def record_parent_activity(session, parent_id: str, *, operation_id: str,
                           activity: str, hours: int | None = None,
                           payment: int | None = None,
                           expected_clock: int | None = None) -> dict:
    with _parent_write_lock(session):
        return _record_parent_activity(
            session, parent_id, operation_id=operation_id, activity=activity,
            hours=hours, payment=payment, expected_clock=expected_clock)



def _validate_activity_event(session, *, body: Mapping[str, Any],
                             parent_id: str, alias: str) -> dict:
    event = session.event(body.get("event_id") or "")
    if not event or event.get("hash") != body.get("event_hash"):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_SEVERED")
    event_body = event.get("body") or {}
    receipt = body.get("receipt")
    if not isinstance(receipt, Mapping):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_MISMATCH")
    if (event.get("actor_id") != alias
            or event.get("kind") != PARENT_ACTIVITY_EVENT_KIND
            or body.get("actor_id") != parent_id
            or body.get("alias") != alias
            or body.get("activity") != event_body.get("activity")
            or body.get("parameters") != event_body.get("parameters")
            or event_body.get("currency_unit") != receipt.get("currency_unit")
            or body.get("material_before_source")
            != event_body.get("material_before_source")
            or body.get("material_after_source")
            != event_body.get("material_after_source")
            or body.get("event_id") != event.get("event_id")
            or body.get("event_hash") != event.get("hash")):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_MISMATCH")
    if (event_body.get("parent_actor_id") != parent_id
            or event_body.get("parent_alias") != alias
            or not _text(event_body.get("currency_unit"))
            or event_body.get("household_effect") != "NONE_PARENT_LOCAL_ONLY"
            or event_body.get("period_qualification") != PARENT_B02_HOLD
            or event_body.get("visibility") != "PARENT_ORDINARY_ACTIVITY"):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_MISMATCH")
    if (receipt.get("event_id") != event.get("event_id")
            or receipt.get("event_hash") != event.get("hash")
            or receipt.get("event_kind") != PARENT_ACTIVITY_EVENT_KIND
            or receipt.get("event_authored_by") != alias
            or receipt.get("activity") != event_body.get("activity")
            or receipt.get("parameters") != event_body.get("parameters")
            or receipt.get("activity_source")
            != event_body.get("activity_source")
            or receipt.get("before_material_source")
            != event_body.get("material_before_source")
            or receipt.get("after_material_source")
            != event_body.get("material_after_source")
            or receipt.get("period_qualification") != PARENT_B02_HOLD
            or receipt.get("household_effect") != "NONE_PARENT_LOCAL_ONLY"
            or receipt.get("clock") != event.get("clock")):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_MISMATCH")
    from bp4.world import validate_owner_receipt
    try:
        validate_owner_receipt(
            event.get("owner_receipt"), actor_id=alias,
            act=PARENT_ACTIVITY_EVENT_KIND, clock=event.get("clock"))
    except Exception as exc:
        raise RecursionRefusal(
            "PARENT_ACTIVITY_OWNER_RECEIPT_INVALID") from exc
    own_action = [
        row for row in session.product.store.perceptions(
            session.branch_id, actor_id=alias)
        if row.get("event_id") == event.get("event_id")
    ]
    if not any(row.get("channel") == "own_action"
               and row.get("clock") == event.get("clock")
               for row in own_action):
        raise RecursionRefusal("PARENT_ACTIVITY_PERCEPTION_SEVERED")
    return event



def read_parent_activity(session, parent_id: str, operation_id: str, *,
                         as_actor: str | None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    registration = _parent_registration(session, parent_id)
    alias = registration["alias"]
    episodes = [
        episode for episode in session.product.store.episodes(session.branch_id)
        if episode.get("actor_id") == alias
        and episode.get("kind") == PARENT_ACTIVITY_KIND
        and (episode.get("body") or {}).get("operation_id") == operation_id
    ]
    if len(episodes) != 1:
        raise RecursionRefusal("PARENT_ACTIVITY_NOT_FOUND")
    body = episodes[0].get("body") or {}
    event = _validate_activity_event(
        session, body=body, parent_id=parent_id, alias=alias)
    if episodes[0].get("clock") != event.get("clock"):
        raise RecursionRefusal("PARENT_ACTIVITY_EVENT_MISMATCH")
    from s45_projection.projection import project_event
    projected = project_event(event)
    projected.pop("perceived_by_user", None)
    return {
        "schema": PARENT_ACTIVITY_RECEIPT_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "operation_id": operation_id,
        "clock": episodes[0]["clock"],
        "event": projected,
        "event_kind": event.get("kind"),
        "event_authored_by": event.get("actor_id"),
        "receipt": detached(body.get("receipt") or {}),
        "currency_unit": (body.get("receipt") or {}).get("currency_unit"),
        "period_qualification": PARENT_B02_HOLD,
        "historical_ingress": dict(PARENT_HISTORICAL_INGRESS),
        "material_boundary": _material_boundary(
            (body.get("receipt") or {}).get("currency_unit")),
        "household_effect": "NONE_PARENT_LOCAL_ONLY",
        "private_state": "NOT_READ",
    }


def read_parent_history(session, parent_id: str, *,
                        as_actor: str | None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    registration = _parent_registration(session, parent_id)
    alias = registration["alias"]
    rows = []
    for episode in session.product.store.episodes(session.branch_id):
        if episode.get("actor_id") != alias:
            continue
        if episode.get("kind") not in {
                PARENT_MATERIAL_KIND, PARENT_ACTIVITY_KIND,
                PARENT_CIRCUMSTANCE_KIND}:
            continue
        body = episode.get("body") or {}
        rows.append({
            "kind": episode["kind"],
            "operation_id": body.get("operation_id"),
            "clock": episode["clock"],
            "source_ref": body.get("source_ref"),
            "material_before_source": body.get("material_before_source",
                                              body.get("material_source")),
            "material_after_source": body.get("material_after_source",
                                             body.get("material_source")),
            "event_id": body.get("event_id"),
            "event_hash": body.get("event_hash"),
        })
    world = session.world()
    row = world.actor_state.get(alias)
    document = row.get("material") if isinstance(row, Mapping) else None
    current_source = (
        document.get("source") if isinstance(document, Mapping) else None)
    latest_source = rows[-1]["material_after_source"] if rows else None
    return {
        "schema": PARENT_HISTORY_SCHEMA,
        "grade": PARENT_GRADE,
        "status": "READ",
        "actor_id": parent_id,
        "alias": alias,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": world.clock,
        "history": rows,
        "material_source": current_source,
        "latest_history_source": latest_source,
        "material_consistent": current_source == latest_source,
        "period_qualification": PARENT_B02_HOLD,
        "historical_dates": "NOT_AVAILABLE",
        "historical_ingress": dict(PARENT_HISTORICAL_INGRESS),
        "material_boundary": _material_boundary(
            document.get("currency_unit") if isinstance(document, Mapping) else None),
        "private_state": "NOT_READ",
    }
