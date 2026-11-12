"""B05: zero and insufficient household rent are held/unchanged without debit."""
from __future__ import annotations

from argparse import Namespace
import copy
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B05 = Path(__file__).resolve().parent
B04 = RETURNS / "SOROK-DUEL-B04-R1"
B02 = RETURNS / "SOROK-DUEL-B02-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B05, B04, B02, P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import house  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def test_insufficient_household_cash_is_held_without_debit(tmp_path):
    state = tmp_path / "held"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        assert hp.period_progress(session, "period:2026-h1")["status"] == "COMPLETE"
        world = session.world()
        original_cash = world.actor_state["A"]["cash"]
        world.actor_state["A"]["cash"] = 5
        session.product._checkpoint(session.branch_id, world.clock, world)
        receipt = rr.apply_household_rent(
            session, operation_id="b05:held", period_id="period:2026-h1")
        assert receipt["status"] == "REFUSED"
        assert receipt["reasons"] == ["B05_INSUFFICIENT_HOUSEHOLD_CASH"]
        assert receipt["household_cash_before"] == 5
        assert receipt["household_cash_after"] == 5
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 5
        read = rr.read_household_obligation(session, "b05:held")
        assert read["receipt"]["status"] == "REFUSED"
        assert read["household_cash"] == 5
        with pytest.raises(RecursionRefusal, match="B05_RENT_ALREADY_RECORDED"):
            rr.apply_household_rent(
                session, operation_id="b05:held-late",
                period_id="period:2026-h1")
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 5
        world = session.world()
        world.actor_state["A"]["cash"] = original_cash
        session.product._checkpoint(session.branch_id, world.clock, world)
    finally:
        owner.close()


def test_zero_rent_is_unchanged_without_debit(tmp_path):
    state = tmp_path / "zero"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        facts = copy.deepcopy(house.dwelling_fixture(session))
        facts["costs"]["monthly_rent"] = 0
        facts["costs"]["rent_due_now"] = 0
        house.commit_dwelling(session, facts=facts)
        hp.materialize_to(session, "2026-07-01")
        before = house.read_household(session)["resources"][1]["fields"]["cash"]
        receipt = rr.apply_household_rent(
            session, operation_id="b05:zero", period_id="period:2026-h1")
        assert receipt["status"] == "UNCHANGED"
        assert receipt["monthly_rent"] == 0
        assert receipt["household_cash_before"] == receipt["household_cash_after"] == before
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == before
        read = rr.read_household_obligation(session, "b05:zero")
        assert read["receipt"]["status"] == "UNCHANGED"
        assert read["household_cash"] == before
    finally:
        owner.close()
