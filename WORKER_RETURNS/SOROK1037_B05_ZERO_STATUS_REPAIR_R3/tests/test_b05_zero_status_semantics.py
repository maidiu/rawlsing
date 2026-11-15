"""Focused #1037 R3 tests: ADMITTED rent requires a strict actual debit."""
from __future__ import annotations

import copy
from argparse import Namespace
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[2]
B02 = RETURNS / "SOROK-DUEL-B02-R1"
B04 = RETURNS / "SOROK-DUEL-B04-R1"
B05 = RETURNS / "SOROK-DUEL-B05-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
P4 = RETURNS / "SOROK-P4-FIRST-FULL-MPC-R1"
P5 = RETURNS / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
PROJECTION = RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
for _path in (B02, B04, B05, P3, P3 / "tests", P4, P5, P6, ENGINE, PROJECTION):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import house  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal, detached, digest,
)


def open_state(tmp_path, name):
    state = tmp_path / name
    state.mkdir(parents=True, exist_ok=True)
    run_p6.experience(state, Namespace(command="new", request_id=None))
    return run_p6.open_owner(state / "actual-p2")


def household_cash(session):
    household = house.read_household(session)
    for binding in household["resources"]:
        if (binding.get("kind") == "ACTOR_STATE"
                and binding.get("actor_slot") == "A"):
            return binding["fields"]["cash"]
    raise AssertionError("household A cash binding missing")


def household_material_hash(session, *, cash):
    household = house.read_household(session)
    resources = copy.deepcopy(household["resources"])
    for binding in resources:
        if (binding.get("kind") == "ACTOR_STATE"
                and binding.get("actor_slot") == "A"):
            binding["fields"]["cash"] = cash
    return digest({
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": session.world().clock,
        "epoch": household["epoch"],
        "source": household["source"],
        "place": detached(household["place"]),
        "owner": detached(household["owner"]),
        "resources": resources,
    })


def set_rent(session, rent):
    facts = copy.deepcopy(house.dwelling_fixture(session))
    facts["costs"]["monthly_rent"] = rent
    facts["costs"]["rent_due_now"] = rent
    house.commit_dwelling(session, facts=facts)


def make_receipt(session, *, operation_id, period_id, status, rent,
                 cash_before, cash_after, before_hash, after_hash):
    household = house.read_household(session)
    dwelling = house.read_dwelling(session)
    progress = hp.period_progress(session, period_id)
    return {
        "schema": rr.RENT_RECEIPT_SCHEMA,
        "grade": rr.GRADE,
        "status": status,
        "operation_id": operation_id,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": session.clock(),
        "period_id": period_id,
        "period_status": progress["status"],
        "period_b02_coverage": detached(progress.get("b02_coverage") or []),
        "period_state_coverage": detached(progress.get("state_coverage") or []),
        "period_uncovered": detached(progress.get("uncovered") or []),
        "period_elapsed_ticks": progress.get("elapsed_ticks"),
        "period_remaining_ticks": progress.get("remaining_ticks"),
        "monthly_rent": rent,
        "household_cash_before": cash_before,
        "household_cash_after": cash_after,
        "household_document_source": household["source"],
        "household_material_hash_before": before_hash,
        "household_material_hash_after": after_hash,
        "dwelling_source": dwelling["source"],
        "dwelling_material_hash": dwelling["material_hash"],
        "reasons": [],
        "scheduled_participation": "NOT_PERFORMED",
        "event_effect": "NONE",
        "public_event": "NOT_EMITTED",
        "psychology_state": "NOT_WRITTEN",
        "actual_reader": "rolling_reproduction.read_household_obligation",
        "read_boundary": detached(rr.READ_BOUNDARY),
    }


def append_rent(session, operation_id, receipt):
    body = {
        "schema": rr.RENT_RECEIPT_SCHEMA,
        "grade": rr.GRADE,
        "root": receipt["root"],
        "branch": receipt["branch"],
        "operation_id": operation_id,
        "status": receipt["status"],
        "receipt": receipt,
    }
    return session.product.store.append_episode(
        session.branch_id, actor_id="A", kind=rr.RENT_KIND,
        clock=session.clock(), body=body)


def test_public_no_cash_checkpoints_cannot_prove_admitted_zero_rent(tmp_path):
    owner = open_state(tmp_path, "zero-forged")
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        set_rent(session, 0)
        hp.materialize_to(session, "2026-07-01")
        clock = session.clock()
        first = session.product.say("r3-zero-1", actor="A")
        second = session.product.say("r3-zero-2", actor="A")
        assert first["status"] == "OK" and second["status"] == "OK"
        assert session.clock() == clock
        cash = household_cash(session)
        material = household_material_hash(session, cash=cash)
        operation_id = "r3:zero-false-admitted"
        receipt = make_receipt(
            session, operation_id=operation_id, period_id="period:2026-h1",
            status="ADMITTED", rent=0, cash_before=cash, cash_after=cash,
            before_hash=material, after_hash=material)
        append_rent(session, operation_id, receipt)
        assert household_cash(session) == cash
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_RECEIPT_INVALID"):
            rr.read_household_obligation(session, operation_id)
        assert household_cash(session) == cash
    finally:
        owner.close()


def test_positive_forgery_without_actual_debit_remains_refused(tmp_path):
    owner = open_state(tmp_path, "positive-forged")
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        session.product.say("r3-positive-1", actor="A")
        session.product.say("r3-positive-2", actor="A")
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        before_hash = household_material_hash(session, cash=cash + rent)
        after_hash = household_material_hash(session, cash=cash)
        operation_id = "r3:positive-false"
        receipt = make_receipt(
            session, operation_id=operation_id, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash + rent,
            cash_after=cash, before_hash=before_hash, after_hash=after_hash)
        append_rent(session, operation_id, receipt)
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_UNPROVEN"):
            rr.read_household_obligation(session, operation_id)
        assert household_cash(session) == cash
    finally:
        owner.close()


def test_genuine_zero_and_refused_remain_readable(tmp_path):
    zero_owner = open_state(tmp_path, "zero-genuine")
    try:
        session = zero_owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        set_rent(session, 0)
        hp.materialize_to(session, "2026-07-01")
        cash = household_cash(session)
        receipt = rr.apply_household_rent(
            session, operation_id="r3:zero", period_id="period:2026-h1")
        assert receipt["status"] == "UNCHANGED"
        read = rr.read_household_obligation(session, "r3:zero")
        assert read["status"] == "READ"
        assert read["receipt"]["status"] == "UNCHANGED"
        assert read["household_cash"] == cash
    finally:
        zero_owner.close()

    held_owner = open_state(tmp_path, "held")
    try:
        session = held_owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        world = session.world()
        world.actor_state["A"]["cash"] = 5
        session.product._checkpoint(session.branch_id, world.clock, world)
        receipt = rr.apply_household_rent(
            session, operation_id="r3:held", period_id="period:2026-h1")
        assert receipt["status"] == "REFUSED"
        read = rr.read_household_obligation(session, "r3:held")
        assert read["status"] == "READ"
        assert read["receipt"]["status"] == "REFUSED"
        assert read["household_cash"] == 5
    finally:
        held_owner.close()


def test_genuine_positive_historical_and_retry(tmp_path):
    owner = open_state(tmp_path, "positive-genuine")
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        h1 = rr.apply_household_rent(
            session, operation_id="r3:h1", period_id="period:2026-h1")
        assert h1["status"] == "ADMITTED"
        hp.materialize_to(session, "2027-01-01")
        h2 = rr.apply_household_rent(
            session, operation_id="r3:h2", period_id="period:2026-h2")
        assert h2["status"] == "ADMITTED"
        read_h1 = rr.read_household_obligation(session, "r3:h1")
        read_h2 = rr.read_household_obligation(session, "r3:h2")
        assert read_h1["historical"] is True
        assert read_h2["historical"] is False
        assert read_h2["household_cash"] == h1["household_cash_after"] - 12
        replay = rr.apply_household_rent(
            session, operation_id="r3:h1", period_id="period:2026-h1")
        assert replay["status"] == "REPLAY"
        assert household_cash(session) == h2["household_cash_after"]
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_ALREADY_RECORDED"):
            rr.apply_household_rent(
                session, operation_id="r3:h1-late",
                period_id="period:2026-h1")
    finally:
        owner.close()
