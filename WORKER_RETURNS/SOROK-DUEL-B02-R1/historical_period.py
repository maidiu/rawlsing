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


def materialize_periods(session) -> dict:
    """Advance the existing S46 clock in the plan's dated segments once.

    Existing interval states with the exact domain hash are reused.  A retry
    therefore returns the same period state IDs and appends no duplicate
    period.  A missing interval whose start is already in the past is refused;
    no clock is rewound.
    """
    plan = read_period_plan(session)
    employment = read_employment(session)
    if plan["provenance"]["inherited"] or employment["provenance"]["inherited"]:
        raise RecursionRefusal("P6_PERIOD_FORK_MATERIALIZATION_NOT_SUPPORTED")
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    domains = _period_domains(session, plan, employment)
    index = _state_index(session)
    produced, rows = 0, []
    for item in domains:
        period, domain = item["period"], item["domain"]
        matches = index.get(domain["domain_hash"], [])
        if len(matches) > 1:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
        if matches:
            state = matches[0]
        else:
            if session.clock() > domain["start"]:
                raise RecursionRefusal("P6_PERIOD_LOGICAL_CLOCK_IN_PAST")
            state = session.produce_interval(domain)
            if state.get("domain_hash") != domain["domain_hash"]:
                raise RecursionRefusal("P6_PERIOD_STATE_DOMAIN_MISMATCH")
            index[domain["domain_hash"]] = [state]
            produced += 1
        if state.get("start") != period["start_clock"] or state.get("end") != period["end_clock"]:
            raise RecursionRefusal("P6_PERIOD_STATE_CLOCK_MISMATCH")
        rows.append({
            "period_id": period["period_id"],
            "start_date": period["start_date"],
            "end_date": period["end_date"],
            "start_clock": period["start_clock"],
            "end_clock": period["end_clock"],
            "domain_hash": domain["domain_hash"],
            **_interval_summary(state),
        })
    return {
        "schema": MATERIALIZATION_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "status": "MATERIALIZED" if produced else "REPLAYED",
        "produced_states": produced,
        "root_hash": plan["root"],
        "branch_id": session.branch_id,
        "clock": session.clock(),
        "plan_source": plan["source"],
        "employment_source": employment["source"],
        "periods": rows,
        "provenance": detached(plan["provenance"]),
        "read_boundary": detached(READ_BOUNDARY),
    }


def read_material_period(session, as_of_date: str) -> dict:
    """Read the dated material period and employment as-of a calendar date."""
    plan = read_period_plan(session)
    employment = read_employment(session)
    if plan["employment_source"] != employment["source"]:
        raise RecursionRefusal("P6_PERIOD_EMPLOYMENT_SOURCE_MISMATCH")
    as_of = _date(as_of_date, "P6_PERIOD_AS_OF_DATE")
    period = _period_for_date(plan, as_of)
    logical_tick = _logical_tick(plan, as_of)
    if not period["start_clock"] <= logical_tick < period["end_clock"]:
        raise RecursionRefusal("P6_PERIOD_CLOCK_MISMATCH")
    term = _employment_as_of(employment["terms"], as_of)
    interval, interval_status = None, "NOT_MATERIALIZED"
    provenance = detached(plan["provenance"])
    if provenance["inherited"]:
        interval_status = "NOT_AVAILABLE_ON_FORK"
    else:
        domains = _period_domains(session, plan, employment)
        domain = next(row["domain"] for row in domains
                      if row["period"]["period_id"] == period["period_id"])
        index = _state_index(session)
        matches = index.get(domain["domain_hash"], [])
        if len(matches) > 1:
            raise RecursionRefusal("P6_PERIOD_DUPLICATE_STATE")
        if matches:
            interval = _interval_summary(matches[0])
            interval_status = "MATERIALIZED"
    return {
        "schema": MATERIAL_PERIOD_READ_SCHEMA,
        "grade": "SOURCEFREE_S2_ONLY",
        "as_of_date": as_of_date,
        "logical_tick": logical_tick,
        "calendar_basis": plan["calendar_basis"],
        "clock_basis": plan["clock_basis"],
        "ticks_per_day": plan["ticks_per_day"],
        "period": detached(period),
        "employment": term,
        "employment_status": ("EFFECTIVE" if term is not None
                              else "UNKNOWN_NO_EFFECTIVE_TERM"),
        "employment_source": employment["source"],
        "plan_source": plan["source"],
        "interval": interval,
        "interval_status": interval_status,
        "root_hash": plan["root"],
        "branch_id": session.branch_id,
        "clock": session.clock(),
        "provenance": provenance,
        "read_boundary": detached(READ_BOUNDARY),
    }


def p3_interval_span(session, period_id: str) -> dict:
    """Return only the existing P3 EventProposal.interval shape for a period."""
    plan = read_period_plan(session)
    for period in plan["periods"]:
        if period["period_id"] == period_id:
            return {
                "mode": "SCHEDULED_ONLY",
                "span": period["end_clock"] - period["start_clock"],
            }
    raise RecursionRefusal("P6_PERIOD_UNKNOWN")


def period_plan_fixture(session) -> dict:
    """Return a caller-editable plan content fixture (not yet committed)."""
    employment = _employment_content()
    document = _document_from_content(session, EMPLOYMENT_SCHEMA, employment)
    return _plan_content(session, document["source"])


__all__ = [
    "EMPLOYMENT_SLOT", "PERIOD_SLOT", "EMPLOYMENT_SCHEMA", "EMPLOYMENT_READ_SCHEMA",
    "PERIOD_SCHEMA", "PERIOD_READ_SCHEMA", "MATERIAL_PERIOD_READ_SCHEMA",
    "MATERIALIZATION_SCHEMA", "GRADE", "CALENDAR_BASIS", "CLOCK_BASIS",
    "TICKS_PER_DAY", "MAX_PERIODS", "MAX_DAYS",
    "default_employment_terms", "default_periods", "period_plan_fixture",
    "establish_period_plan", "read_employment", "read_period_plan",
    "materialize_periods", "read_material_period", "p3_interval_span",
]
