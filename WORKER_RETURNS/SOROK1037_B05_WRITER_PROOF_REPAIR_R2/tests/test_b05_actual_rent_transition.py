"""Focused #1037 R2 tests: ADMITTED rent needs the actual writer transition."""
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


def open_state(tmp_path, name="state"):
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


def make_receipt(session, *, operation_id, period_id, rent, cash_before,
                 cash_after):
    household = house.read_household(session)
    dwelling = house.read_dwelling(session)
    progress = hp.period_progress(session, period_id)
    return {
        "schema": rr.RENT_RECEIPT_SCHEMA,
        "grade": rr.GRADE,
        "status": "ADMITTED",
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
        "household_material_hash_before": household_material_hash(
            session, cash=cash_before),
        "household_material_hash_after": household_material_hash(
            session, cash=cash_after),
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


def test_sole_caller_rehashed_admitted_receipt_without_transition_refuses(
        tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        assert hp.period_progress(session, "period:2026-h1")["status"] == "COMPLETE"
        assert not [row for row in session.product.store.episodes(session.branch_id)
                    if row.get("kind") == rr.RENT_KIND]
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        operation_id = "r2:sole-rehashed"
        receipt = make_receipt(
            session, operation_id=operation_id, period_id="period:2026-h1",
            rent=rent, cash_before=cash + rent, cash_after=cash)
        append_rent(session, operation_id, receipt)
        assert household_cash(session) == cash
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_UNPROVEN"):
            rr.read_household_obligation(session, operation_id)
        assert household_cash(session) == cash
    finally:
        owner.close()


def test_actual_transition_severed_then_restored(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        rr.apply_household_rent(
            session, operation_id="r2:real", period_id="period:2026-h1")
        baseline = rr.read_household_obligation(session, "r2:real")
        clock = baseline["receipt"]["clock"]
        store = session.product.store
        original = store.checkpoints
        store.checkpoints = lambda branch: [
            row for row in original(branch) if row.get("clock") != clock]
        try:
            with pytest.raises(
                    RecursionRefusal, match="B05_RENT_OPERATION_UNPROVEN"):
                rr.read_household_obligation(session, "r2:real")
        finally:
            del store.checkpoints
        assert rr.read_household_obligation(session, "r2:real") == baseline
    finally:
        owner.close()


def test_sibling_cannot_copy_an_actual_transition_for_another_period(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2027-01-01")
        assert hp.period_progress(session, "period:2026-h2")["status"] == "COMPLETE"
        rr.apply_household_rent(
            session, operation_id="r2:h1", period_id="period:2026-h1")
        genuine = copy.deepcopy(
            rr.read_household_obligation(session, "r2:h1")["receipt"])
        forged = copy.deepcopy(genuine)
        forged["operation_id"] = "r2:h2-copy"
        forged["period_id"] = "period:2026-h2"
        append_rent(session, "r2:h2-copy", forged)
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_UNPROVEN"):
            rr.read_household_obligation(session, "r2:h2-copy")
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_UNPROVEN"):
            rr.read_household_obligation(session, "r2:h1")
    finally:
        owner.close()


def test_zero_and_held_rents_still_read_without_a_debit_transition(tmp_path):
    zero_owner = open_state(tmp_path, "zero")
    try:
        session = zero_owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        facts = copy.deepcopy(house.dwelling_fixture(session))
        facts["costs"]["monthly_rent"] = 0
        facts["costs"]["rent_due_now"] = 0
        house.commit_dwelling(session, facts=facts)
        hp.materialize_to(session, "2026-07-01")
        cash = household_cash(session)
        receipt = rr.apply_household_rent(
            session, operation_id="r2:zero", period_id="period:2026-h1")
        assert receipt["status"] == "UNCHANGED"
        read = rr.read_household_obligation(session, "r2:zero")
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
            session, operation_id="r2:held", period_id="period:2026-h1")
        assert receipt["status"] == "REFUSED"
        read = rr.read_household_obligation(session, "r2:held")
        assert read["status"] == "READ"
        assert read["receipt"]["status"] == "REFUSED"
        assert read["household_cash"] == 5
    finally:
        held_owner.close()


def test_historical_and_replay_reads_still_work(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        h1 = rr.apply_household_rent(
            session, operation_id="r2:h1", period_id="period:2026-h1")
        hp.materialize_to(session, "2027-01-01")
        h2 = rr.apply_household_rent(
            session, operation_id="r2:h2", period_id="period:2026-h2")
        read_h1 = rr.read_household_obligation(session, "r2:h1")
        read_h2 = rr.read_household_obligation(session, "r2:h2")
        assert read_h1["historical"] is True
        assert read_h2["historical"] is False
        replay = rr.apply_household_rent(
            session, operation_id="r2:h1", period_id="period:2026-h1")
        assert replay["status"] == "REPLAY"
        assert household_cash(session) == h2["household_cash_after"]
        with pytest.raises(RecursionRefusal, match="B05_RENT_ALREADY_RECORDED"):
            rr.apply_household_rent(
                session, operation_id="r2:h1-late", period_id="period:2026-h1")
    finally:
        owner.close()
