"""B05 atomic rent rollback: no cash debit or receipt survives a failed checkpoint."""
from __future__ import annotations

from argparse import Namespace
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B05 = Path(__file__).resolve().parent
B02 = RETURNS / "SOROK-DUEL-B02-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B05, B02, P6, ENGINE, P3):
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


def household_cash(session):
    household = house.read_household(session)
    for binding in household["resources"]:
        if binding.get("kind") == "ACTOR_STATE" and binding.get("actor_slot") == "A":
            return binding["fields"]["cash"]
    raise AssertionError("missing household cash binding")


def test_rent_crash_rolls_back_cash_and_receipt(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        baseline = household_cash(session)
        assert baseline == 55

        def crash(*args, **kwargs):
            raise RuntimeError("injected rent checkpoint failure")

        session.product._checkpoint = crash
        with pytest.raises(RuntimeError, match="injected rent checkpoint failure"):
            rr.apply_household_rent(
                session, operation_id="b05:rent:crash",
                period_id="period:2026-h1")
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        assert household_cash(session) == 55
        with pytest.raises(RecursionRefusal, match="B05_RENT_NOT_FOUND"):
            rr.read_household_obligation(session, "b05:rent:crash")
        admitted = rr.apply_household_rent(
            session, operation_id="b05:rent:after-crash",
            period_id="period:2026-h1")
        assert admitted["status"] == "ADMITTED"
        assert admitted["household_cash_before"] == 55
        assert admitted["household_cash_after"] == 43
        assert household_cash(session) == 43
    finally:
        owner.close()
