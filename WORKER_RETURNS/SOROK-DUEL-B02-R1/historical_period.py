"""Bounded historical calendar to existing S46 logical-clock period adapter.

This module does not own time.  It writes two source-qualified P2 material facts
(employment terms and a period plan) and, when asked, asks the existing S46
session producer to advance the existing logical clock in dated segments.  It
does not write P3 psychology, a second scheduler, a second event journal, or a
calendar-day event stream.

Calendar dates and logical ticks are deliberately distinct:

* source calendar: Gregorian proleptic UTC date, inclusive start/exclusive end;
* logical clock: S46 TEST_ONLY logical ticks, one declared day per tick;
* the plan stores the anchor date, anchor clock and both representations.
"""
from __future__ import annotations

from datetime import date
import math
from typing import Any, Mapping

from developmental_recursion.contracts import RecursionRefusal, detached, digest
from developmental_recursion.p2_owner import (
    branch_is_ancestor,
    material_fact_source,
    write_material_fact,
)

EMPLOYMENT_SLOT = "p6_employment"
PERIOD_SLOT = "p6_historical_period"
EMPLOYMENT_SCHEMA = "SOROK_EMPLOYMENT_TERMS@1"
EMPLOYMENT_READ_SCHEMA = "SOROK_EMPLOYMENT_TERMS_READ@1"
PERIOD_SCHEMA = "SOROK_HISTORICAL_PERIOD_PLAN@1"
PERIOD_READ_SCHEMA = "SOROK_HISTORICAL_PERIOD_PLAN_READ@1"
MATERIAL_PERIOD_READ_SCHEMA = "SOROK_MATERIAL_PERIOD_READ@1"
MATERIALIZATION_SCHEMA = "SOROK_PERIOD_MATERIALIZATION@1"
MATERIALIZATION_RECEIPT_KIND = "P2_B02_PERIOD_MATERIALIZATION"
MATERIALIZATION_RECEIPT_SCHEMA = "SOROK_PERIOD_MATERIALIZATION_RECEIPT@1"
GRADE = "SOURCEFREE_FIXTURE"
CALENDAR_BASIS = "GREGORIAN_PROLEPTIC_UTC_DATE"
CLOCK_BASIS = "S46_TEST_ONLY_LOGICAL_TICK_DAY_V1"
TICKS_PER_DAY = 1
MAX_PERIODS = 8
MAX_DAYS = 3660
EMPLOYMENT_FIELDS = frozenset({"schema", "grade", "holder_actor_slot", "terms"})
EMPLOYMENT_STORED_FIELDS = frozenset({
    *EMPLOYMENT_FIELDS, "root", "branch", "epoch", "source",
})
TERM_FIELDS = frozenset({
    "term_id", "term_version", "employer_ref", "role_ref", "workplace_ref",
    "effective_from", "daily_wage_units", "currency_unit",
})
PLAN_FIELDS = frozenset({
    "schema", "grade", "calendar_basis", "clock_basis", "anchor_date",
    "anchor_clock", "ticks_per_day", "employment_source", "periods",
})
PLAN_STORED_FIELDS = frozenset({*PLAN_FIELDS, "root", "branch", "epoch", "source"})
PERIOD_FIELDS = frozenset({
    "period_id", "start_date", "end_date", "start_clock", "end_clock",
})
READ_BOUNDARY = {
    "psyche_store": "NOT_READ",
    "psychology_state": "NOT_WRITTEN",
    "class_to_trait": "NOT_APPLIED",
    "model_prose": "NOT_READ",
}

DEFAULT_TERMS = (
    {
        "term_id": "employment:workshop-cooperative",
        "term_version": 1,
        "employer_ref": "employer:workshop-cooperative",
        "role_ref": "role:repair-assistant",
        "workplace_ref": "workplace:p6-workshop",
        "effective_from": "2026-01-01",
        "daily_wage_units": 3,
        "currency_unit": "sourcefree_currency_unit",
    },
    {
        "term_id": "employment:civic-works",
        "term_version": 1,
        "employer_ref": "employer:civic-works",
        "role_ref": "role:maintenance-worker",
        "workplace_ref": "workplace:civic-yard",
        "effective_from": "2026-03-15",
        "daily_wage_units": 4,
        "currency_unit": "sourcefree_currency_unit",
    },
)
DEFAULT_PERIODS = (
    {
        "period_id": "period:2026-h1",
        "start_date": "2026-01-01",
        "end_date": "2026-07-01",
    },
    {
        "period_id": "period:2026-h2",
        "start_date": "2026-07-01",
        "end_date": "2027-01-01",
    },
)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _date(value: Any, code: str) -> date:
    if not isinstance(value, str):
        raise RecursionRefusal(code)
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise RecursionRefusal(code) from exc


def _nonneg_number(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def _positive_int(value: Any) -> bool:
    return type(value) is int and value >= 1


def _hash_text(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def _provenance(stored_branch: str, current_branch: str) -> dict:
    inherited = stored_branch != current_branch
    return {
        "stored_branch": stored_branch,
        "current_branch": current_branch,
        "inherited": inherited,
        "scope": "P6_MATERIAL_PERIOD_ONLY",
        "fork_state": ("C12_FORK_WITHOUT_S46_INTERVAL_STATE"
                       if inherited else "CURRENT_BRANCH"),
    }


def default_employment_terms() -> list[dict]:
    return detached(list(DEFAULT_TERMS))


def default_periods() -> list[dict]:
    return detached(list(DEFAULT_PERIODS))


def _validate_terms(value: Any) -> list[dict]:
    if not isinstance(value, list) or not value:
        raise RecursionRefusal("P6_EMPLOYMENT_TERMS_SCHEMA")
    rows, term_ids, last = [], set(), None
    for item in value:
        if not isinstance(item, Mapping) or set(item) != TERM_FIELDS:
            raise RecursionRefusal("P6_EMPLOYMENT_TERM_SCHEMA")
        term = detached(item)
        for key in ("term_id", "employer_ref", "role_ref", "workplace_ref",
                    "currency_unit"):
            if not _text(term.get(key)):
                raise RecursionRefusal("P6_EMPLOYMENT_TERM_SCHEMA")
        if not _positive_int(term.get("term_version")):
            raise RecursionRefusal("P6_EMPLOYMENT_TERM_SCHEMA")
        if not _nonneg_number(term.get("daily_wage_units")):
            raise RecursionRefusal("P6_EMPLOYMENT_TERM_SCHEMA")
        effective = _date(term.get("effective_from"),
                          "P6_EMPLOYMENT_EFFECTIVE_DATE")
        if term["term_id"] in term_ids:
            raise RecursionRefusal("P6_EMPLOYMENT_TERM_DUPLICATE")
        if last is not None and effective <= last:
            raise RecursionRefusal("P6_EMPLOYMENT_EFFECTIVE_ORDER")
        term_ids.add(term["term_id"])
        last = effective
        rows.append(term)
    return rows


def _employment_content(terms: Any = None) -> dict:
    return {
        "schema": EMPLOYMENT_SCHEMA,
        "grade": GRADE,
        "holder_actor_slot": "A",
        "terms": _validate_terms(default_employment_terms()
                                 if terms is None else terms),
    }


def _read_employment_document(document: Any, world, root: str, branch: str, *,
                              branch_ok=None) -> dict:
    if not isinstance(document, dict) or set(document) != EMPLOYMENT_STORED_FIELDS:
        raise RecursionRefusal("P6_EMPLOYMENT_SCHEMA")
    if (document.get("schema") != EMPLOYMENT_SCHEMA
            or document.get("grade") != GRADE):
        raise RecursionRefusal("P6_EMPLOYMENT_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_EMPLOYMENT_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_EMPLOYMENT_SOURCE_OR_ROOT_MISMATCH")
    source = document.get("source")
    if not _hash_text(source) or material_fact_source(document) != source:
        raise RecursionRefusal("P6_EMPLOYMENT_SOURCE_OR_ROOT_MISMATCH")
    if document.get("holder_actor_slot") != "A":
        raise RecursionRefusal("P6_EMPLOYMENT_HOLDER")
    if not isinstance(world.actor_state.get("A"), dict):
        raise RecursionRefusal("P6_EMPLOYMENT_HOLDER_UNAVAILABLE")
    terms = _validate_terms(document.get("terms"))
    material_hash = digest({
        "root": root, "branch": branch, "clock": world.clock,
        "epoch": epoch, "source": source, "holder_actor_slot": "A",
        "terms": terms,
    })
    return {
        "schema": EMPLOYMENT_READ_SCHEMA,
        "grade": GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": source,
        "material_hash": material_hash,
        "holder_actor_slot": "A",
        "terms": terms,
        "provenance": _provenance(stored_branch, branch),
    }


def _employment_document(session, terms: Any = None) -> dict:
    world = session.world()
    root = session.read_root()["root_hash"]
    content = _employment_content(terms)
    document = {**content, "root": root, "branch": session.branch_id,
                "epoch": world.clock}
    document["source"] = material_fact_source(document)
    _read_employment_document(document, world, root, session.branch_id)
    return document


def read_employment(session) -> dict:
    """Read the source-qualified employment terms as a P2 material fact."""
    world = session.world()
    document = world.resources.get(EMPLOYMENT_SLOT)
    if document is None:
        raise RecursionRefusal("P6_EMPLOYMENT_ABSENT")
    root_row = session.read_root()
    return _read_employment_document(
        document, world, root_row["root_hash"], session.branch_id,
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )


def _normalize_periods(anchor_date: str, anchor_clock: int,
                       ticks_per_day: int, periods: Any) -> list[dict]:
    if not isinstance(periods, list) or not 1 <= len(periods) <= MAX_PERIODS:
        raise RecursionRefusal("P6_PERIOD_SCHEMA")
    anchor = _date(anchor_date, "P6_PERIOD_ANCHOR")
    normalized, ids, previous_end = [], set(), None
    for item in periods:
        if not isinstance(item, Mapping) or set(item) != PERIOD_FIELDS:
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        period = detached(item)
        if not _text(period.get("period_id")) or period["period_id"] in ids:
            raise RecursionRefusal("P6_PERIOD_ID")
        start = _date(period.get("start_date"), "P6_PERIOD_DATE")
        end = _date(period.get("end_date"), "P6_PERIOD_DATE")
        if end <= start or (end - start).days > MAX_DAYS:
            raise RecursionRefusal("P6_PERIOD_DATE_ORDER")
        start_clock = anchor_clock + (start - anchor).days * ticks_per_day
        end_clock = anchor_clock + (end - anchor).days * ticks_per_day
        if (type(period.get("start_clock")) is not int
                or type(period.get("end_clock")) is not int
                or period["start_clock"] != start_clock
                or period["end_clock"] != end_clock):
            raise RecursionRefusal("P6_PERIOD_CLOCK_MISMATCH")
        if previous_end is not None and start_clock != previous_end:
            raise RecursionRefusal("P6_PERIOD_NOT_CONTIGUOUS")
        if period["start_clock"] < 0 or period["end_clock"] <= period["start_clock"]:
            raise RecursionRefusal("P6_PERIOD_CLOCK_MISMATCH")
        ids.add(period["period_id"])
        previous_end = end_clock
        normalized.append(period)
    if normalized[0]["start_date"] != anchor_date:
        raise RecursionRefusal("P6_PERIOD_ANCHOR_MISMATCH")
    if normalized[0]["start_clock"] != anchor_clock:
        raise RecursionRefusal("P6_PERIOD_ANCHOR_MISMATCH")
    return normalized


def _plan_content(session, employment_source: str,
                  periods: Any = None, *, anchor_date: Any = None,
                  anchor_clock: Any = None) -> dict:
    if periods is None:
        raw = default_periods()
        if anchor_date is None:
            anchor_date = raw[0]["start_date"]
        if anchor_clock is None:
            anchor_clock = session.clock()
    else:
        if not isinstance(periods, list) or not periods:
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        raw = detached(periods)
        if anchor_date is None:
            anchor_date = raw[0].get("start_date") if isinstance(raw[0], Mapping) else None
        if anchor_clock is None:
            anchor_clock = raw[0].get("start_clock") if isinstance(raw[0], Mapping) else None
        if anchor_clock is None:
            anchor_clock = session.clock()
    if not _hash_text(employment_source):
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE")
    if not _text(anchor_date) or type(anchor_clock) is not int or anchor_clock < 0:
        raise RecursionRefusal("P6_PERIOD_ANCHOR")
    anchor = _date(anchor_date, "P6_PERIOD_ANCHOR")
    filled = []
    for item in raw:
        if not isinstance(item, Mapping):
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        period = detached(item)
        if set(period) not in (
                PERIOD_FIELDS, frozenset({"period_id", "start_date", "end_date"})):
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        if "start_clock" not in period:
            period["start_clock"] = anchor_clock + (
                _date(period.get("start_date"), "P6_PERIOD_DATE") - anchor
            ).days * TICKS_PER_DAY
            period["end_clock"] = anchor_clock + (
                _date(period.get("end_date"), "P6_PERIOD_DATE") - anchor
            ).days * TICKS_PER_DAY
        filled.append(period)
    raw = filled
    return {
        "schema": PERIOD_SCHEMA,
        "grade": GRADE,
        "calendar_basis": CALENDAR_BASIS,
        "clock_basis": CLOCK_BASIS,
        "anchor_date": anchor_date,
        "anchor_clock": anchor_clock,
        "ticks_per_day": TICKS_PER_DAY,
        "employment_source": employment_source,
        "periods": _normalize_periods(anchor_date, anchor_clock,
                                      TICKS_PER_DAY, raw),
    }


def _read_plan_document(document: Any, world, root: str, branch: str, *,
                        branch_ok=None) -> dict:
    if not isinstance(document, dict) or set(document) != PLAN_STORED_FIELDS:
        raise RecursionRefusal("P6_PERIOD_SCHEMA")
    if document.get("schema") != PERIOD_SCHEMA or document.get("grade") != GRADE:
        raise RecursionRefusal("P6_PERIOD_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_PERIOD_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_PERIOD_SOURCE_OR_ROOT_MISMATCH")
    source = document.get("source")
    if not _hash_text(source) or material_fact_source(document) != source:
        raise RecursionRefusal("P6_PERIOD_SOURCE_OR_ROOT_MISMATCH")
    if (document.get("calendar_basis") != CALENDAR_BASIS
            or document.get("clock_basis") != CLOCK_BASIS
            or document.get("ticks_per_day") != TICKS_PER_DAY):
        raise RecursionRefusal("P6_PERIOD_BASIS")
    anchor_date = document.get("anchor_date")
    anchor_clock = document.get("anchor_clock")
    if not _text(anchor_date) or type(anchor_clock) is not int or anchor_clock < 0:
        raise RecursionRefusal("P6_PERIOD_ANCHOR")
    _date(anchor_date, "P6_PERIOD_ANCHOR")
    employment_source = document.get("employment_source")
    if not _hash_text(employment_source):
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE")
    periods = _normalize_periods(anchor_date, anchor_clock, TICKS_PER_DAY,
                                 document.get("periods"))
    material_hash = digest({
        "root": root, "branch": branch, "clock": world.clock,
        "epoch": epoch, "source": source, "calendar_basis": CALENDAR_BASIS,
        "clock_basis": CLOCK_BASIS, "anchor_date": anchor_date,
        "anchor_clock": anchor_clock, "ticks_per_day": TICKS_PER_DAY,
        "employment_source": employment_source, "periods": periods,
    })
    return {
        "schema": PERIOD_READ_SCHEMA,
        "grade": GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": source,
        "material_hash": material_hash,
        "calendar_basis": CALENDAR_BASIS,
        "clock_basis": CLOCK_BASIS,
        "anchor_date": anchor_date,
        "anchor_clock": anchor_clock,
        "ticks_per_day": TICKS_PER_DAY,
        "employment_source": employment_source,
        "periods": periods,
        "provenance": _provenance(stored_branch, branch),
    }


def read_period_plan(session) -> dict:
    """Read and cross-check the plan against the employment material fact."""
    employment = read_employment(session)
    world = session.world()
    document = world.resources.get(PERIOD_SLOT)
    if document is None:
        raise RecursionRefusal("P6_PERIOD_ABSENT")
    root_row = session.read_root()
    plan = _read_plan_document(
        document, world, root_row["root_hash"], session.branch_id,
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    plan["employment_material_hash"] = employment["material_hash"]
    return plan


def _write_or_check(session, slot: str, document: Mapping) -> None:
    existing = session.world().resources.get(slot)
    if existing is not None and existing != document:
        raise RecursionRefusal("P6_PERIOD_ALREADY_ESTABLISHED")
    if existing is None:
        write_material_fact(session, slot=slot, document=document)


def _document_from_content(session, schema: str, content: Mapping) -> dict:
    world = session.world()
    root = session.read_root()["root_hash"]
    document = {**detached(content), "root": root, "branch": session.branch_id,
                "epoch": world.clock}
    document["source"] = material_fact_source(document)
    return document


def establish_period_plan(session, *, employment: Any = None,
                          plan: Any = None) -> dict:
    """Admit the bounded employment and period-plan material facts.

    The writer is the existing S47/P2 material-fact checkpoint.  Existing equal
    documents are idempotent; different existing documents are refused.  This
    function does not advance the clock or produce any interval.
    """
    if employment is not None:
        if not isinstance(employment, Mapping) or set(employment) not in (
                EMPLOYMENT_FIELDS, EMPLOYMENT_STORED_FIELDS):
            raise RecursionRefusal("P6_EMPLOYMENT_SCHEMA")
    if plan is not None:
        if not isinstance(plan, Mapping) or set(plan) not in (
                PLAN_FIELDS, PLAN_STORED_FIELDS):
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
    if employment is None:
        employment_document = _employment_document(session)
    else:
        employment_content = employment
        if set(employment) == EMPLOYMENT_STORED_FIELDS:
            employment_content = {key: employment[key] for key in EMPLOYMENT_FIELDS}
        if employment_content.get("holder_actor_slot") not in (None, "A"):
            raise RecursionRefusal("P6_EMPLOYMENT_HOLDER")
        if employment_content.get("schema") not in (None, EMPLOYMENT_SCHEMA):
            raise RecursionRefusal("P6_EMPLOYMENT_SCHEMA")
        if employment_content.get("grade") not in (None, GRADE):
            raise RecursionRefusal("P6_EMPLOYMENT_SCHEMA")
        employment_document = _employment_document(
            session, employment_content.get("terms"),
        )
    employment_read = _read_employment_document(
        employment_document, session.world(),
        session.read_root()["root_hash"], session.branch_id,
    )
    if plan is None:
        plan_content = _plan_content(session, employment_read["source"])
    else:
        plan_content = plan
        if set(plan) == PLAN_STORED_FIELDS:
            plan_content = {key: plan[key] for key in PLAN_FIELDS}
        if plan_content.get("schema") not in (None, PERIOD_SCHEMA):
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        if plan_content.get("grade") not in (None, GRADE):
            raise RecursionRefusal("P6_PERIOD_SCHEMA")
        if plan_content.get("calendar_basis") not in (None, CALENDAR_BASIS):
            raise RecursionRefusal("P6_PERIOD_BASIS")
        if plan_content.get("clock_basis") not in (None, CLOCK_BASIS):
            raise RecursionRefusal("P6_PERIOD_BASIS")
        if plan_content.get("ticks_per_day") not in (None, TICKS_PER_DAY):
            raise RecursionRefusal("P6_PERIOD_BASIS")
        supplied_anchor_date = plan_content.get("anchor_date")
        supplied_anchor_clock = plan_content.get("anchor_clock")
        plan_content = _plan_content(
            session, employment_read["source"],
            plan_content.get("periods"),
            anchor_date=supplied_anchor_date,
            anchor_clock=supplied_anchor_clock,
        )
        if (plan_content.get("anchor_date") != supplied_anchor_date
                or plan_content.get("anchor_clock") != supplied_anchor_clock):
            raise RecursionRefusal("P6_PERIOD_ANCHOR_MISMATCH")
        if plan.get("employment_source") not in (None, employment_read["source"]):
            raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    plan_document = _document_from_content(session, PERIOD_SCHEMA, plan_content)
    _read_plan_document(plan_document, session.world(),
                        session.read_root()["root_hash"], session.branch_id)
    _write_or_check(session, EMPLOYMENT_SLOT, employment_document)
    _write_or_check(session, PERIOD_SLOT, plan_document)
    return read_period_plan(session)


def _employment_as_of(terms: list[dict], as_of: date) -> dict | None:
    selected = None
    for term in terms:
        if date.fromisoformat(term["effective_from"]) <= as_of:
            selected = term
        else:
            break
    return detached(selected) if selected is not None else None


def _period_for_date(plan: dict, as_of: date) -> dict:
    for period in plan["periods"]:
        start = date.fromisoformat(period["start_date"])
        end = date.fromisoformat(period["end_date"])
        if start <= as_of < end:
            return period
    raise RecursionRefusal("P6_PERIOD_OUTSIDE_PLAN")


def _logical_tick(plan: dict, day: date) -> int:
    anchor = date.fromisoformat(plan["anchor_date"])
    return plan["anchor_clock"] + (day - anchor).days * plan["ticks_per_day"]


def _change_dates(period: Mapping, terms: list[dict]) -> list[str]:
    start = date.fromisoformat(period["start_date"])
    end = date.fromisoformat(period["end_date"])
    return [
        term["effective_from"] for term in terms
        if start < date.fromisoformat(term["effective_from"]) < end
    ]


def _period_domains(session, plan: dict, employment: dict) -> list[dict]:
    try:
        from s46.model import make_domain
    except Exception as exc:
        raise RecursionRefusal("P6_PERIOD_S46_MODEL_MISSING") from exc
    actor = session.world().actor_state.get("A", {}).get("actor_id")
    if not _text(actor):
        raise RecursionRefusal("P6_PERIOD_ACTOR_UNAVAILABLE")
    result = []
    for period in plan["periods"]:
        changes = _change_dates(period, employment["terms"])
        boundary_dates = [period["start_date"], *changes, period["end_date"]]
        boundary_ticks = [_logical_tick(plan, date.fromisoformat(value))
                          for value in boundary_dates]
        segments = tuple(
            (boundary_ticks[index], boundary_ticks[index + 1])
            for index in range(len(boundary_ticks) - 1)
            if boundary_ticks[index] < boundary_ticks[index + 1]
        )
        if not segments:
            raise RecursionRefusal("P6_PERIOD_EMPTY_SEGMENTS")
        domain = make_domain(
            mode="SCHEDULED_ONLY", start=period["start_clock"],
            end=period["end_clock"], segments=segments,
            actor_id=actor, branch_id=session.branch_id,
        )
        result.append({"period": period, "domain": domain})
    return result


def _state_index(session) -> dict:
    try:
        states = session.read_interval_states()
    except Exception as exc:
        raise RecursionRefusal("P6_PERIOD_S46_STATE_INVALID") from exc
    index = {}
    for state in states:
        index.setdefault(state.get("domain_hash"), []).append(state)
    return index


def _interval_summary(state: dict) -> dict:
    return {
        "state_id": state.get("state_id", ""),
        "status": state.get("status", ""),
        "start": state.get("start"),
        "end": state.get("end"),
        "segments": detached(state.get("segments") or []),
        "currentness": state.get("currentness", ""),
        "domain_hash": state.get("domain_hash", ""),
    }


def _all_states(session) -> list[dict]:
    try:
        return session.read_interval_states()
    except Exception as exc:
        raise RecursionRefusal("P6_PERIOD_S46_STATE_INVALID") from exc


def _state_maps(states: list[dict]) -> tuple[dict, dict]:
    by_id, by_domain = {}, {}
    for state in states:
        state_id = state.get("state_id")
        if not _text(state_id):
            raise RecursionRefusal("P6_PERIOD_STATE_ID")
        if state_id in by_id:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
        by_id[state_id] = state
        by_domain.setdefault(state.get("domain_hash"), []).append(state)
    return by_id, by_domain


def _receipt_rows(session, plan_source: str, period_id: str | None = None) -> list[dict]:
    root = session.read_root()["root_hash"]
    rows = []
    for episode in session.product.store.episodes(session.branch_id):
        if episode.get("kind") != MATERIALIZATION_RECEIPT_KIND:
            continue
        body = dict(episode.get("body") or {})
        if body.get("plan_source") != plan_source:
            continue
        if period_id is not None and body.get("period_id") != period_id:
            continue
        if body.get("root") != root or body.get("branch") != session.branch_id:
            raise RecursionRefusal("P6_PERIOD_RECEIPT_SOURCE_MISMATCH")
        body["_episode_id"] = episode["episode_id"]
        body["_clock"] = episode["clock"]
        rows.append(body)
    return rows


def _date_from_clock(plan: dict, clock: int) -> date:
    anchor = date.fromisoformat(plan["anchor_date"])
    return anchor.fromordinal(anchor.toordinal() + (int(clock) - plan["anchor_clock"]))


def _segments_for_range(plan: dict, employment: dict,
                        start_clock: int, end_clock: int) -> tuple:
    if start_clock >= end_clock:
        raise RecursionRefusal("P6_PERIOD_EMPTY_SEGMENTS")
    start_date = _date_from_clock(plan, start_clock)
    end_date = _date_from_clock(plan, end_clock)
    boundaries = [start_clock]
    for term in employment["terms"]:
        effective = date.fromisoformat(term["effective_from"])
        if start_date < effective < end_date:
            tick = _logical_tick(plan, effective)
            if start_clock < tick < end_clock:
                boundaries.append(tick)
    boundaries.append(end_clock)
    boundaries = sorted(set(boundaries))
    segments = tuple((boundaries[i], boundaries[i + 1])
                     for i in range(len(boundaries) - 1))
    if not segments or any(a >= b for a, b in segments):
        raise RecursionRefusal("P6_PERIOD_EMPTY_SEGMENTS")
    return segments


def _coverage_union(intervals: list[tuple[int, int]]) -> list[list[int]]:
    rows = sorted([tuple(row) for row in intervals])
    if not rows:
        return []
    merged = [list(rows[0])]
    for start, end in rows[1:]:
        if start < merged[-1][1]:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
        if start == merged[-1][1]:
            merged[-1][1] = end
        else:
            merged.append([start, end])
    return merged


def _coverage_ticks(intervals: list[list[int]]) -> int:
    return sum(end - start for start, end in intervals)


def _receipt_document(session, plan: dict, employment: dict, period: dict,
                      target_date: str, target_clock: int, state: dict,
                      status: str) -> dict:
    return {
        "schema": MATERIALIZATION_RECEIPT_SCHEMA,
        "grade": GRADE,
        "status": status,
        "root": plan["root"],
        "branch": session.branch_id,
        "plan_source": plan["source"],
        "employment_source": employment["source"],
        "period_id": period["period_id"],
        "period_start": period["start_clock"],
        "period_end": period["end_clock"],
        "target_date": target_date,
        "target_clock": target_clock,
        "clock_before": state["start"],
        "clock_after": state["end"],
        "state_id": state["state_id"],
        "domain_hash": state["domain_hash"],
        "start": state["start"],
        "end": state["end"],
        "segments": detached(state.get("segments") or []),
        "mode": state.get("domain", {}).get("mode", ""),
        "public_event": "NOT_EMITTED",
        "read_boundary": detached(READ_BOUNDARY),
    }


def _append_receipt(session, document: dict) -> dict:
    rows = _receipt_rows(session, document["plan_source"], document["period_id"])
    for row in rows:
        if (row.get("domain_hash") == document["domain_hash"]
                or row.get("state_id") == document["state_id"]):
            if (row.get("domain_hash") != document["domain_hash"]
                    or row.get("state_id") != document["state_id"]):
                raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
            return {**row, "receipt_status": "REPLAYED"}
    episode = session.product._append_episode(
        session.branch_id, "A", MATERIALIZATION_RECEIPT_KIND,
        session.clock(), detached(document),
    )
    return {**detached(document), "receipt_status": "APPENDED",
            "_episode_id": episode["episode_id"], "_clock": episode["clock"]}


def _period_state_row(session, plan: dict, period: dict, receipts: list[dict]) -> dict:
    by_id, _ = _state_maps(_all_states(session))
    states = []
    for receipt in receipts:
        state = by_id.get(receipt.get("state_id"))
        if state is None:
            raise RecursionRefusal("P6_PERIOD_STATE_SEVERED")
        states.append(state)
    if not states:
        raise RecursionRefusal("P6_PERIOD_NOT_MATERIALIZED")
    states.sort(key=lambda row: (row["start"], row["end"]))
    if len(states) == 1:
        state = states[0]
        return {
            "period_id": period["period_id"],
            "start_date": period["start_date"],
            "end_date": period["end_date"],
            "start_clock": period["start_clock"],
            "end_clock": period["end_clock"],
            "domain_hash": state["domain_hash"],
            **_interval_summary(state),
        }
    segments = [row for state in states for row in state.get("segments") or []]
    segments.sort(key=lambda row: (row.get("start"), row.get("end")))
    coverage = [row for state in states for row in state.get("coverage") or []]
    coverage.sort()
    return {
        "period_id": period["period_id"],
        "start_date": period["start_date"],
        "end_date": period["end_date"],
        "start_clock": period["start_clock"],
        "end_clock": period["end_clock"],
        "domain_hash": states[-1]["domain_hash"],
        "state_id": states[-1]["state_id"],
        "status": "PARTIAL",
        "start": period["start_clock"],
        "end": period["end_clock"],
        "segments": segments,
        "coverage": coverage,
        "currentness": states[-1].get("currentness", ""),
        "state_ids": [state["state_id"] for state in states],
    }


def period_progress(session, period_id: str) -> dict:
    """Return clock/state progress for a dated period without advancing time."""
    plan = read_period_plan(session)
    employment = read_employment(session)
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    period = next((row for row in plan["periods"]
                   if row["period_id"] == period_id), None)
    if period is None:
        raise RecursionRefusal("P6_PERIOD_UNKNOWN")
    receipts = _receipt_rows(session, plan["source"], period_id)
    states = _all_states(session)
    by_id, _ = _state_maps(states)
    b02_states = []
    for receipt in receipts:
        state = by_id.get(receipt.get("state_id"))
        if state is None:
            raise RecursionRefusal("P6_PERIOD_STATE_SEVERED")
        if (state.get("domain_hash") != receipt.get("domain_hash")
                or state.get("start") != receipt.get("start")
                or state.get("end") != receipt.get("end")):
            raise RecursionRefusal("P6_PERIOD_STATE_DOMAIN_MISMATCH")
        if (state.get("domain") or {}).get("mode") != "SCHEDULED_ONLY":
            raise RecursionRefusal("P6_PERIOD_STATE_MODE_MISMATCH")
        if not (period["start_clock"] <= state["start"] < state["end"]
                <= period["end_clock"]):
            raise RecursionRefusal("P6_PERIOD_STATE_OUT_OF_PERIOD")
        b02_states.append(state)
    b02_ids = {state["state_id"] for state in b02_states}
    actor_id = session.world().actor_state.get("A", {}).get("actor_id")
    other_states = [
        state for state in states
        if state.get("state_id") not in b02_ids
        and state.get("actor_id") == actor_id
        and state.get("branch_id") == session.branch_id
        and period["start_clock"] <= state["start"] < state["end"]
        <= period["end_clock"]
    ]
    b02_coverage = _coverage_union(
        [(state["start"], state["end"]) for state in b02_states])
    all_coverage = _coverage_union(
        [(state["start"], state["end"]) for state in b02_states + other_states])
    clock = session.clock()
    current_end = min(max(clock, period["start_clock"]), period["end_clock"])
    elapsed = max(0, current_end - period["start_clock"])
    remaining = max(0, period["end_clock"] - max(clock, period["start_clock"]))
    gaps = []
    cursor = period["start_clock"]
    for start, end in all_coverage:
        if end <= cursor:
            continue
        if start > cursor and cursor < current_end:
            gaps.append([cursor, min(start, current_end)])
        cursor = max(cursor, end)
        if cursor >= current_end:
            break
    if cursor < current_end:
        gaps.append([cursor, current_end])
    status = ("BEFORE" if clock <= period["start_clock"]
              else "COMPLETE" if clock >= period["end_clock"]
              else "PARTIAL")
    remaining_segments = []
    if clock < period["end_clock"]:
        start = max(clock, period["start_clock"])
        if start < period["end_clock"]:
            remaining_segments = [
                [a, b] for a, b in _segments_for_range(
                    plan, employment, start, period["end_clock"])]
    return {
        "schema": MATERIALIZATION_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "status": status,
        "period_id": period["period_id"],
        "start_date": period["start_date"],
        "end_date": period["end_date"],
        "start_clock": period["start_clock"],
        "end_clock": period["end_clock"],
        "clock": clock,
        "current_date": _date_from_clock(plan, clock).isoformat(),
        "elapsed_ticks": elapsed,
        "remaining_ticks": remaining,
        "b02_coverage": b02_coverage,
        "b02_covered_ticks": _coverage_ticks(b02_coverage),
        "state_coverage": all_coverage,
        "state_covered_ticks": _coverage_ticks(all_coverage),
        "uncovered": gaps,
        "uncovered_ticks": sum(end - start for start, end in gaps),
        "b02_state_ids": sorted(b02_ids),
        "other_state_ids": sorted(state["state_id"] for state in other_states),
        "remaining_segments": remaining_segments,
        "next_p3_span": remaining,
        "root_hash": plan["root"],
        "branch_id": session.branch_id,
        "plan_source": plan["source"],
        "employment_source": employment["source"],
        "provenance": detached(plan["provenance"]),
        "read_boundary": detached(READ_BOUNDARY),
    }


def remaining_span(session, period_id: str, *, to_date: Any = None) -> dict:
    """Return the not-yet-elapsed span for a period, subtracting current progress."""
    plan = read_period_plan(session)
    period = next((row for row in plan["periods"]
                   if row["period_id"] == period_id), None)
    if period is None:
        raise RecursionRefusal("P6_PERIOD_UNKNOWN")
    target = period["end_clock"]
    if to_date is not None:
        target = _logical_tick(plan, _date(to_date, "P6_PERIOD_AS_OF_DATE"))
        target = min(target, period["end_clock"])
    current = session.clock()
    if target < current:
        if to_date is None and current >= period["end_clock"]:
            target = current
        else:
            raise RecursionRefusal("P6_PERIOD_CLOCK_IN_PAST")
    start = max(period["start_clock"], current)
    return {
        "period_id": period_id,
        "start_clock": start,
        "end_clock": target,
        "span": max(0, target - start),
        "mode": "SCHEDULED_ONLY",
        "current_clock": current,
    }


def _materialization_result(session, plan: dict, employment: dict,
                            target_date: str, target_clock: int,
                            status: str, produced: int, replayed: int,
                            recovered: int, touched: list[dict]) -> dict:
    periods = []
    for period in plan["periods"]:
        receipts = _receipt_rows(session, plan["source"], period["period_id"])
        if not receipts:
            continue
        periods.append(_period_state_row(session, plan, period, receipts))
    return {
        "schema": MATERIALIZATION_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "status": status,
        "produced_states": produced,
        "replayed_states": replayed,
        "recovered_receipts": recovered,
        "target_date": target_date,
        "target_clock": target_clock,
        "root_hash": plan["root"],
        "branch_id": session.branch_id,
        "clock": session.clock(),
        "plan_source": plan["source"],
        "employment_source": employment["source"],
        "periods": periods,
        "touched": touched,
        "provenance": detached(plan["provenance"]),
        "read_boundary": detached(READ_BOUNDARY),
    }


def _recover_missing_receipts(session, plan: dict, employment: dict,
                              target_date: str, target_clock: int) -> int:
    """Recover a B02 state produced before its receipt in a crashed call."""
    existing = _receipt_rows(session, plan["source"])
    receipt_ids = {row.get("state_id") for row in existing}
    recovered = 0
    for state in _all_states(session):
        if state.get("state_id") in receipt_ids:
            continue
        domain = state.get("domain") or {}
        if domain.get("mode") != "SCHEDULED_ONLY":
            continue
        period = next((row for row in plan["periods"]
                       if row["start_clock"] <= state.get("start")
                       and state.get("end") <= row["end_clock"]), None)
        if period is None:
            continue
        try:
            expected = _segments_for_range(
                plan, employment, state["start"], state["end"])
        except RecursionRefusal:
            continue
        actual = tuple(
            (int(row[0]), int(row[1])) if isinstance(row, (list, tuple))
            else (int(row["start"]), int(row["end"]))
            for row in domain.get("segments") or []
        )
        if actual != expected:
            continue
        _append_receipt(session, _receipt_document(
            session, plan, employment, period, target_date, target_clock,
            state, "RECOVERED",
        ))
        receipt_ids.add(state["state_id"])
        recovered += 1
    return recovered


def materialize_to(session, as_of_date: str) -> dict:
    """Advance the existing S46 clock to a dated target incrementally.

    Only the not-yet-elapsed range from the current clock to the target is
    materialized.  A prior period or segment is never replayed from its start,
    a past target is refused, and the employment change is split only when it
    falls inside the newly advanced range.
    """
    plan = read_period_plan(session)
    employment = read_employment(session)
    if plan["provenance"]["inherited"] or employment["provenance"]["inherited"]:
        raise RecursionRefusal("P6_PERIOD_FORK_MATERIALIZATION_NOT_SUPPORTED")
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    as_of = _date(as_of_date, "P6_PERIOD_AS_OF_DATE")
    target_clock = _logical_tick(plan, as_of)
    if target_clock < plan["periods"][0]["start_clock"] or target_clock > plan["periods"][-1]["end_clock"]:
        raise RecursionRefusal("P6_PERIOD_OUTSIDE_PLAN")
    current = session.clock()
    if target_clock < current:
        raise RecursionRefusal("P6_PERIOD_CLOCK_IN_PAST")
    recovered_initial = _recover_missing_receipts(
        session, plan, employment, as_of_date, target_clock)
    if target_clock == current:
        status = "RECOVERED" if recovered_initial else "ALREADY_CURRENT"
        return _materialization_result(
            session, plan, employment, as_of_date, target_clock,
            status, 0, sum(
                len(_receipt_rows(session, plan["source"], period["period_id"]))
                for period in plan["periods"]), recovered_initial, [],
        )
    produced = replayed = 0
    recovered = recovered_initial
    touched = []
    for period in plan["periods"]:
        start = max(period["start_clock"], session.clock())
        end = min(period["end_clock"], target_clock)
        if end <= start:
            continue
        actor = session.world().actor_state.get("A", {}).get("actor_id")
        if not _text(actor):
            raise RecursionRefusal("P6_PERIOD_ACTOR_UNAVAILABLE")
        from s46.model import make_domain
        segments = _segments_for_range(plan, employment, start, end)
        domain = make_domain(
            mode="SCHEDULED_ONLY", start=start, end=end, segments=segments,
            actor_id=actor, branch_id=session.branch_id,
        )
        receipts = _receipt_rows(session, plan["source"], period["period_id"])
        existing = next((row for row in receipts
                         if row.get("domain_hash") == domain["domain_hash"]), None)
        by_id, by_domain = _state_maps(_all_states(session))
        if existing is not None:
            state = by_id.get(existing.get("state_id"))
            if state is None:
                raise RecursionRefusal("P6_PERIOD_STATE_SEVERED")
            if (state.get("domain_hash") != domain["domain_hash"]
                    or state.get("start") != start or state.get("end") != end):
                raise RecursionRefusal("P6_PERIOD_STATE_DOMAIN_MISMATCH")
            replayed += 1
            receipt_status = "REPLAYED"
        else:
            matches = by_domain.get(domain["domain_hash"], [])
            if len(matches) > 1:
                raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
            if matches:
                state = matches[0]
                if state.get("start") != start or state.get("end") != end:
                    raise RecursionRefusal("P6_PERIOD_STATE_CLOCK_MISMATCH")
                recovered += 1
                receipt_status = "RECOVERED"
            else:
                if session.clock() > start:
                    raise RecursionRefusal("P6_PERIOD_LOGICAL_CLOCK_IN_PAST")
                state = session.produce_interval(domain)
                if (state.get("domain_hash") != domain["domain_hash"]
                        or state.get("start") != start or state.get("end") != end):
                    raise RecursionRefusal("P6_PERIOD_STATE_DOMAIN_MISMATCH")
                produced += 1
                receipt_status = "PRODUCED"
            _append_receipt(session, _receipt_document(
                session, plan, employment, period, as_of_date, target_clock,
                state, receipt_status,
            ))
        if session.clock() != state["end"]:
            raise RecursionRefusal("P6_PERIOD_CLOCK_DID_NOT_ADVANCE")
        touched.append({
            "period_id": period["period_id"],
            "start_clock": start,
            "end_clock": end,
            "domain_hash": domain["domain_hash"],
            "state_id": state["state_id"],
            "receipt_status": receipt_status,
        })
        if session.clock() >= target_clock:
            break
    if session.clock() != target_clock:
        raise RecursionRefusal("P6_PERIOD_MATERIALIZATION_INCOMPLETE")
    status = "MATERIALIZED" if produced else ("RECOVERED" if recovered else "REPLAYED")
    return _materialization_result(
        session, plan, employment, as_of_date, target_clock, status,
        produced, replayed, recovered, touched,
    )


def materialize_periods(session) -> dict:
    """Materialize the whole plan through the incremental dated API.

    This is the legacy full-plan wrapper.  It still advances only from the
    current clock; it never replays an already elapsed period.  Use
    materialize_to for a bounded partial advance.
    """
    plan = read_period_plan(session)
    last_date = plan["periods"][-1]["end_date"]
    result = materialize_to(session, last_date)
    if result["status"] == "ALREADY_CURRENT" and result["periods"]:
        result = {**result, "status": "REPLAYED"}
    return result


def _covering_states(states: list[dict], tick: int, *, actor_id: str,
                     branch_id: str, period: dict) -> list[dict]:
    return [
        state for state in states
        if state.get("actor_id") == actor_id
        and state.get("branch_id") == branch_id
        and state.get("start") <= tick < state.get("end")
        and period["start_clock"] <= state.get("start") < state.get("end")
        <= period["end_clock"]
    ]


def _state_interval_read(state: dict, *, b02_ids: set[str], tick: int) -> dict:
    summary = _interval_summary(state)
    summary["mode"] = (state.get("domain") or {}).get("mode", "")
    summary["admitted_clock"] = state.get("clock", 0)
    summary["b02_materialized"] = state.get("state_id") in b02_ids
    summary["available_at_as_of"] = int(state.get("clock", 0)) <= tick
    summary["retrospective"] = not summary["available_at_as_of"]
    return summary


def read_material_period(session, as_of_date: str) -> dict:
    """Read the dated period, employment and state currentness as-of a date."""
    plan = read_period_plan(session)
    employment = read_employment(session)
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    as_of = _date(as_of_date, "P6_PERIOD_AS_OF_DATE")
    period = _period_for_date(plan, as_of)
    logical_tick = _logical_tick(plan, as_of)
    if not period["start_clock"] <= logical_tick < period["end_clock"]:
        raise RecursionRefusal("P6_PERIOD_CLOCK_MISMATCH")
    current_clock = session.clock()
    current_date = _date_from_clock(plan, current_clock)
    current_term = _employment_as_of(employment["terms"], current_date)
    term = _employment_as_of(employment["terms"], as_of)
    relation = ("PAST" if logical_tick < current_clock
                else "CURRENT" if logical_tick == current_clock else "FUTURE")
    provenance = detached(plan["provenance"])
    actor_id = session.world().actor_state.get("A", {}).get("actor_id")
    states = [] if provenance["inherited"] else _all_states(session)
    receipts = [] if provenance["inherited"] else _receipt_rows(
        session, plan["source"], period["period_id"])
    b02_ids = {row.get("state_id") for row in receipts}
    interval = None
    interval_status = "NOT_MATERIALIZED"
    interval_detail = "NOT_MATERIALIZED"
    state_admitted_clock = None
    state_available_at_as_of = None
    retrospective = None
    current_interval = None
    current_interval_status = "NOT_MATERIALIZED"
    progress = None
    if provenance["inherited"]:
        interval_status = "NOT_AVAILABLE_ON_FORK"
        interval_detail = "NOT_AVAILABLE_ON_FORK"
    else:
        progress = period_progress(session, period["period_id"])
        covering = _covering_states(
            states, logical_tick, actor_id=actor_id,
            branch_id=session.branch_id, period=period)
        if len(covering) > 1:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
        if covering:
            interval = _state_interval_read(
                covering[0], b02_ids=b02_ids, tick=logical_tick)
            interval_status = "MATERIALIZED"
            interval_detail = (
                "ELAPSED_BY_OTHER_OWNER" if not interval["b02_materialized"]
                else "MATERIALIZED_RETROSPECTIVELY" if interval["retrospective"]
                else "MATERIALIZED_AT_AS_OF")
            state_admitted_clock = interval["admitted_clock"]
            state_available_at_as_of = interval["available_at_as_of"]
            retrospective = interval["retrospective"]
        else:
            interval_detail = (
                "FUTURE_NOT_MATERIALIZED" if relation == "FUTURE"
                else "NOT_MATERIALIZED_AT_AS_OF" if relation == "PAST"
                else "CURRENT_NOT_MATERIALIZED")
        current_covering = [
            state for state in states
            if state.get("actor_id") == actor_id
            and state.get("branch_id") == session.branch_id
            and state.get("start") <= current_clock < state.get("end")
        ]
        if len(current_covering) == 1:
            current_interval = _interval_summary(current_covering[0])
            current_interval["mode"] = (
                current_covering[0].get("domain") or {}).get("mode", "")
            current_interval_status = "MATERIALIZED"
        elif len(current_covering) > 1:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
    return {
        "schema": MATERIAL_PERIOD_READ_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "as_of_date": as_of_date,
        "logical_tick": logical_tick,
        "as_of_relation": relation,
        "calendar_basis": plan["calendar_basis"],
        "clock_basis": plan["clock_basis"],
        "ticks_per_day": plan["ticks_per_day"],
        "period": detached(period),
        "employment": term,
        "employment_status": ("EFFECTIVE" if term is not None
                              else "UNKNOWN_NO_EFFECTIVE_TERM"),
        "employment_is_current": relation == "CURRENT",
        "employment_currentness": (
            "CURRENT_AS_OF" if relation == "CURRENT"
            else "PAST_AS_OF" if relation == "PAST"
            else "FUTURE_NOT_CURRENT"),
        "current_date": current_date.isoformat(),
        "current_employment": detached(current_term),
        "current_employment_status": ("EFFECTIVE" if current_term is not None
                                      else "UNKNOWN_NO_EFFECTIVE_TERM"),
        "employment_source": employment["source"],
        "plan_source": plan["source"],
        "interval": interval,
        "interval_status": interval_status,
        "interval_status_detail": interval_detail,
        "state_admitted_clock": state_admitted_clock,
        "state_available_at_as_of": state_available_at_as_of,
        "retrospective": retrospective,
        "current_interval": current_interval,
        "current_interval_status": current_interval_status,
        "period_progress": progress,
        "root_hash": plan["root"],
        "branch_id": session.branch_id,
        "clock": current_clock,
        "provenance": provenance,
        "read_boundary": detached(READ_BOUNDARY),
    }


def p3_interval_span(session, period_id: str, *, to_date: Any = None) -> dict:
    """Return only the existing P3 EventProposal.interval shape, net of progress."""
    span = remaining_span(session, period_id, to_date=to_date)
    return {"mode": "SCHEDULED_ONLY", "span": span["span"]}


def period_plan_fixture(session) -> dict:
    """Return a caller-editable plan content fixture (not yet committed)."""
    employment = _employment_content()
    document = _document_from_content(session, EMPLOYMENT_SCHEMA, employment)
    return _plan_content(session, document["source"])


__all__ = [
    "EMPLOYMENT_SLOT", "PERIOD_SLOT", "EMPLOYMENT_SCHEMA", "EMPLOYMENT_READ_SCHEMA",
    "PERIOD_SCHEMA", "PERIOD_READ_SCHEMA", "MATERIAL_PERIOD_READ_SCHEMA",
    "MATERIALIZATION_SCHEMA", "MATERIALIZATION_RECEIPT_KIND",
    "MATERIALIZATION_RECEIPT_SCHEMA", "GRADE", "CALENDAR_BASIS", "CLOCK_BASIS",
    "TICKS_PER_DAY", "MAX_PERIODS", "MAX_DAYS",
    "default_employment_terms", "default_periods", "period_plan_fixture",
    "establish_period_plan", "read_employment", "read_period_plan",
    "materialize_periods", "materialize_to", "period_progress",
    "remaining_span", "read_material_period", "p3_interval_span",
]
