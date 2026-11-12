"""B04 composition: typed purchase receipt, honest C02 join refusal, crash rollback."""
from __future__ import annotations

from argparse import Namespace
import copy
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
B04 = Path(__file__).resolve().parent
B02 = RETURNS / "SOROK-DUEL-B02-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (B04, B02, P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import historical_period as hp  # noqa: E402
import material_operations as mo  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material, parent_feasible_actions, parent_material_fixture,
    read_parent_history, read_parent_material, record_parent_activity,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_B04_COMPOSE_PARENT"
PARENT_ALIAS = "P"


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def setup(tmp_path, *, cash=120, free_hours=8):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    session = owner.base_owner.fanin.session
    hp.establish_period_plan(session)
    hp.materialize_to(session, "2026-02-01")
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": "b04-composition-private"},
    )
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(
            actor_id=PARENT_ID, source_ref="sourcefree:parent:b04-composition",
            employment_status="employed", wage_units_per_hour=5,
            debt_units=4, care_hours_due=2, cash_units=cash,
            free_hours=free_hours, currency_unit=mo.CURRENCY,
        ),
    )
    mo.establish_market_inventory(session)
    return state, owner, session


def holder_id(session):
    return session.world().actor_state["A"]["actor_id"]


def test_purchase_is_typed_and_c02_history_refuses_until_hook(tmp_path):
    state, owner, session = setup(tmp_path)
    try:
        holder = holder_id(session)
        purchase = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:compose:1",
            owner_actor_id=holder)
        assert purchase["status"] == "ADMITTED"
        with pytest.raises(RecursionRefusal, match="PARENT_MATERIAL_HISTORY_MISMATCH"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        with pytest.raises(RecursionRefusal, match="PARENT_MATERIAL_HISTORY_MISMATCH"):
            parent_feasible_actions(session, PARENT_ID, as_actor=PARENT_ID)
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        assert history["material_consistent"] is False
        assert all(row.get("operation_id") != "b04:compose:1"
                   for row in history["history"])
        assert all(row.get("operation_kind") != "PURCHASE_MATERIAL_STATE"
                   for row in history["history"])
        read = mo.read_purchase(
            session, PARENT_ID, "b04:compose:1", as_actor=PARENT_ID)
        assert read["status"] == "READ"
        assert read["parent_material_status"] == (
            "REFUSED:PARENT_MATERIAL_HISTORY_MISMATCH")
        assert read["purchase_history_hook"] == "C02_PARENT_HISTORY_KIND_PENDING"
        assert read["receipt"]["status"] == "ADMITTED"
        assert read["owned_totals"][0]["quantity"] == 1
    finally:
        owner.close()


def test_c02_parent_activity_refuses_after_purchase_without_double_debit(tmp_path):
    state, owner, session = setup(tmp_path)
    try:
        holder = holder_id(session)
        purchase = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:compose:typed",
            owner_actor_id=holder)
        assert purchase["status"] == "ADMITTED"
        before_market = mo.read_market_inventory(session)
        before_owned = mo.read_owned_objects(session)
        with pytest.raises(RecursionRefusal, match="PARENT_MATERIAL_HISTORY_MISMATCH"):
            record_parent_activity(
                session, PARENT_ID, operation_id="b04:compose:work",
                activity="PAID_WORK", hours=2)
        assert mo.read_market_inventory(session) == before_market
        assert mo.read_owned_objects(session) == before_owned
        read = mo.read_purchase(
            session, PARENT_ID, "b04:compose:typed", as_actor=PARENT_ID)
        assert read["status"] == "READ"
        assert read["receipt"]["status"] == "ADMITTED"
        assert read["parent_material_status"] == (
            "REFUSED:PARENT_MATERIAL_HISTORY_MISMATCH")
    finally:
        owner.close()


def test_purchase_crash_rolls_back_parent_stock_ownership_and_history(tmp_path):
    state, owner, session = setup(tmp_path)
    holder = holder_id(session)
    baseline_parent = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
    baseline_market = mo.read_market_inventory(session)
    assert mo.read_owned_objects(session)["status"] == "ABSENT"

    def crash(*args, **kwargs):
        raise RuntimeError("injected checkpoint failure")

    session.product._checkpoint = crash
    with pytest.raises(RuntimeError, match="injected checkpoint failure"):
        mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:compose:crash",
            owner_actor_id=holder)
    owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        assert mo.read_market_inventory(session)["source"] == baseline_market["source"]
        assert mo.read_owned_objects(session)["status"] == "ABSENT"
        parent = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        assert parent["material"] == baseline_parent["material"]
        history = read_parent_history(session, PARENT_ID, as_actor=PARENT_ID)
        assert history["material_consistent"] is True
        with pytest.raises(RecursionRefusal, match="PURCHASE_NOT_FOUND"):
            mo.read_purchase(
                session, PARENT_ID, "b04:compose:crash", as_actor=PARENT_ID)
    finally:
        owner.close()
