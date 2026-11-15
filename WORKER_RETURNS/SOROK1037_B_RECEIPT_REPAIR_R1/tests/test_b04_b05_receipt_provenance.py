"""SOROK #1037 B04/B05 public-reader provenance repair tests."""
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
import material_operations as mo  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal, digest,
)
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material, parent_material_fixture, read_parent_material,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_1037_PARENT"
PARENT_ALIAS = "P"


def open_state(tmp_path):
    state = tmp_path / "state"
    state.mkdir(parents=True, exist_ok=True)
    run_p6.experience(state, Namespace(command="new", request_id=None))
    return run_p6.open_owner(state / "actual-p2")


def setup_parent(session, *, cash=100, free_hours=8):
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": "1037-private-not-for-child"},
    )
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(
            actor_id=PARENT_ID, source_ref="sourcefree:parent:1037",
            employment_status="employed", wage_units_per_hour=5,
            debt_units=4, care_hours_due=2, cash_units=cash,
            free_hours=free_hours, currency_unit=mo.CURRENCY,
        ),
    )


def parent_cash(session):
    return read_parent_material(
        session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"]


def stored_parent_cash(session):
    return session.world().actor_state[PARENT_ALIAS]["material"]["cash_units"]


def household_cash(session):
    return house.read_household(session)["resources"][1]["fields"]["cash"]


def purchase_episode(session, operation_id):
    return next(
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == mo.PURCHASE_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    )


def rent_episode(session, operation_id):
    return next(
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == rr.RENT_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    )


def forge_purchase(session, operation_id, mutate):
    body = copy.deepcopy(purchase_episode(session, "b04:real")["body"])
    body["operation_id"] = operation_id
    body["receipt"]["operation_id"] = operation_id
    mutate(body)
    session.product.store.append_episode(
        session.branch_id, actor_id=PARENT_ALIAS, kind=mo.PURCHASE_KIND,
        clock=session.clock(), body=body)
    return body


def forge_rent(session, operation_id, mutate, *, actor_id="A"):
    body = copy.deepcopy(rent_episode(session, "b05:real")["body"])
    body["operation_id"] = operation_id
    body["receipt"]["operation_id"] = operation_id
    mutate(body)
    session.product.store.append_episode(
        session.branch_id, actor_id=actor_id, kind=rr.RENT_KIND,
        clock=session.clock(), body=body)
    return body


def test_b04_read_purchase_binds_receipt_provenance(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        real = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:real",
            owner_actor_id=holder)
        assert real["status"] == "ADMITTED"
        baseline = mo.read_purchase(
            session, PARENT_ID, "b04:real", as_actor=PARENT_ID)
        assert baseline["status"] == "READ"
        assert baseline["historical"] is False
        assert baseline["parent_material_status"] == "READ"
        assert baseline["owned_totals"][0]["quantity"] == 1

        cases = {
            "b04:forged-root": lambda b: b["receipt"].update(
                {"root": "f" * 64}),
            "b04:forged-branch": lambda b: b["receipt"].update(
                {"branch": "foreign-branch"}),
            "b04:forged-body-root": lambda b: b.update({"root": "0" * 64}),
            "b04:forged-body-branch": lambda b: b.update(
                {"branch": "foreign-branch"}),
            "b04:forged-body-actor": lambda b: b.update(
                {"actor_id": "foreign-parent"}),
            "b04:forged-parent": lambda b: b["receipt"].update(
                {"parent_id": "foreign-parent"}),
            "b04:forged-alias": lambda b: b["receipt"].update(
                {"parent_alias": "Q"}),
            "b04:forged-operation": lambda b: b["receipt"].update(
                {"operation_id": "other-operation"}),
            "b04:forged-status": lambda b: b.update({"status": "REFUSED"}),
            "b04:forged-clock": lambda b: b["receipt"].update(
                {"clock": session.clock() + 1}),
        }
        for operation_id, mutate in cases.items():
            forge_purchase(session, operation_id, mutate)
            with pytest.raises(
                    RecursionRefusal,
                    match="PURCHASE_READ_PROVENANCE_MISMATCH"):
                mo.read_purchase(
                    session, PARENT_ID, operation_id, as_actor=PARENT_ID)
        assert stored_parent_cash(session) == 60
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 1
        assert len(mo.read_owned_objects(session)["objects"]) == 1
        with pytest.raises(RecursionRefusal, match="PARENT_SELF_READ_REQUIRED"):
            mo.read_purchase(
                session, PARENT_ID, "b04:real", as_actor="other-parent")
        with pytest.raises(RecursionRefusal, match="PURCHASE_READ_PARENT_MISMATCH"):
            mo.read_purchase(session, PARENT_ID, "b04:real", as_actor=PARENT_ID)
    finally:
        owner.close()


def test_b04_coherent_rehashed_forgery_is_not_accepted(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        assert mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:real",
            owner_actor_id=holder)["status"] == "ADMITTED"
        body = copy.deepcopy(purchase_episode(session, "b04:real")["body"])
        receipt = body["receipt"]
        forged_op = "b04:rehashed"
        body["operation_id"] = forged_op
        receipt["operation_id"] = forged_op
        receipt["owned_source_before"] = receipt["owned_source_after"]
        receipt["purchase_source"] = digest({
            "schema": mo.PURCHASE_RECEIPT_SCHEMA,
            "operation_id": forged_op,
            "parent_id": PARENT_ID,
            "owner_actor_id": receipt["owner_actor_id"],
            "object_id": receipt["object_id"],
            "unit_price": receipt["unit_price"],
            "market_source": receipt["market_source_before"],
            "parent_before": receipt["parent_material_source_before"],
            "parent_after": receipt["parent_material_source_after"],
        })
        world = session.world()
        forged_owned = copy.deepcopy(world.resources[mo.OWNED_SLOT])
        forged_owned["objects"].append({
            "acquisition_id": forged_op,
            "object_id": receipt["object_id"],
            "kind": receipt["kind"],
            "owner_actor_id": receipt["owner_actor_id"],
            "quantity": 1,
            "market_source": receipt["market_source_before"],
            "purchase_source": receipt["purchase_source"],
            "currency_unit": receipt["currency_unit"],
            "unit_price": receipt["unit_price"],
        })
        forged_owned["source"] = mo.material_fact_source(forged_owned)
        world.resources[mo.OWNED_SLOT] = forged_owned
        session.product._checkpoint(session.branch_id, world.clock, world)
        session.product.store.append_episode(
            session.branch_id, actor_id=PARENT_ALIAS, kind=mo.PURCHASE_KIND,
            clock=session.clock(), body=body)
        with pytest.raises(RecursionRefusal, match="PURCHASE_READ_PARENT_MISMATCH"):
            mo.read_purchase(
                session, PARENT_ID, forged_op, as_actor=PARENT_ID)
        assert stored_parent_cash(session) == 60
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 1
        assert len(mo.read_owned_objects(session)["objects"]) == 2
    finally:
        owner.close()


def setup_rent(session):
    hp.establish_period_plan(session)
    hp.materialize_to(session, "2026-02-01")
    setup_parent(session)
    mo.establish_market_inventory(session)
    hp.materialize_to(session, "2026-07-01")
    rent = rr.apply_household_rent(
        session, operation_id="b05:real", period_id="period:2026-h1")
    assert rent["status"] == "ADMITTED"


def test_b05_read_obligation_binds_receipt_identity_and_period(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        setup_rent(session)
        baseline = rr.read_household_obligation(session, "b05:real")
        assert baseline["status"] == "READ"
        assert baseline["historical"] is False
        assert baseline["receipt"]["status"] == "ADMITTED"
        cash = household_cash(session)
        assert cash == baseline["household_cash"]

        cases = {
            "b05:forged-root": lambda b: b["receipt"].update(
                {"root": "e" * 64}),
            "b05:forged-branch": lambda b: b["receipt"].update(
                {"branch": "foreign-branch"}),
            "b05:forged-body-root": lambda b: b.update({"root": "0" * 64}),
            "b05:forged-operation": lambda b: b["receipt"].update(
                {"operation_id": "other-operation"}),
            "b05:forged-clock": lambda b: b["receipt"].update(
                {"clock": session.clock() + 1}),
            "b05:forged-household": lambda b: b["receipt"].update(
                {"household_document_source": "0" * 64}),
            "b05:forged-rent": lambda b: b["receipt"].update(
                {"monthly_rent": 99, "household_cash_before": cash + 99,
                 "household_cash_after": cash}),
        }
        for operation_id, mutate in cases.items():
            forge_rent(session, operation_id, mutate)
            with pytest.raises(RecursionRefusal) as raised:
                rr.read_household_obligation(session, operation_id)
            assert str(raised.value) in {
                "B05_RENT_PROVENANCE_MISMATCH",
                "B05_RENT_SOURCE_STALE",
            }
        forge_rent(session, "b05:forged-actor", lambda b: None, actor_id="B")
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_PROVENANCE_MISMATCH"):
            rr.read_household_obligation(session, "b05:forged-actor")
        assert household_cash(session) == cash

        def coherent(body):
            body["receipt"]["household_cash_before"] = cash + 12
            body["receipt"]["household_cash_after"] = cash
            body["receipt"]["monthly_rent"] = 12

        forge_rent(session, "b05:rehashed", coherent)
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_NOT_UNIQUE"):
            rr.read_household_obligation(session, "b05:rehashed")
        with pytest.raises(
                RecursionRefusal, match="B05_RENT_OPERATION_NOT_UNIQUE"):
            rr.read_household_obligation(session, "b05:real")
        assert household_cash(session) == cash
    finally:
        owner.close()


def test_b05_forged_period_is_bound(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        setup_rent(session)
        cases = {
            "b05:forged-future-period": lambda b: b["receipt"].update(
                {"period_id": "period:2026-h2"}),
            "b05:forged-unknown-period": lambda b: b["receipt"].update(
                {"period_id": "period:missing"}),
            "b05:forged-period-status": lambda b: b["receipt"].update(
                {"period_status": "BEFORE"}),
        }
        for operation_id, mutate in cases.items():
            forge_rent(session, operation_id, mutate)
            with pytest.raises(RecursionRefusal, match="B05_RENT_PERIOD_MISMATCH"):
                rr.read_household_obligation(session, operation_id)
    finally:
        owner.close()


def test_b05_changed_and_restored_household_source(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        setup_rent(session)
        baseline = rr.read_household_obligation(session, "b05:real")
        stored = copy.deepcopy(
            session.world().resources[house.HOUSEHOLD_SLOT])
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT]["root"] = "0" * 64
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH"):
            rr.read_household_obligation(session, "b05:real")
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT] = copy.deepcopy(stored)
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert rr.read_household_obligation(session, "b05:real") == baseline
    finally:
        owner.close()


def test_normal_two_purchases_one_rent_first_readers(tmp_path):
    owner = open_state(tmp_path)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        first = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:p1",
            owner_actor_id=holder)
        assert first["status"] == "ADMITTED"
        assert first["period"]["period_id"] == "period:2026-h1"
        hp.materialize_to(session, "2026-07-01")
        second = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:p2",
            owner_actor_id=holder)
        assert second["status"] == "ADMITTED"
        assert second["period"]["period_id"] == "period:2026-h2"
        rent = rr.apply_household_rent(
            session, operation_id="b05:r1", period_id="period:2026-h1")
        assert rent["status"] == "ADMITTED"
        p1 = mo.read_purchase(session, PARENT_ID, "b04:p1", as_actor=PARENT_ID)
        p2 = mo.read_purchase(session, PARENT_ID, "b04:p2", as_actor=PARENT_ID)
        r1 = rr.read_household_obligation(session, "b05:r1")
        assert p1["status"] == "READ"
        assert p1["historical"] is True
        assert p2["status"] == "READ"
        assert p2["historical"] is False
        assert p1["parent_material_status"] == "READ"
        assert p2["parent_material_status"] == "READ"
        assert r1["status"] == "READ"
        assert r1["historical"] is False
        assert r1["receipt"]["status"] == "ADMITTED"
        assert parent_cash(session) == 20
        assert household_cash(session) == 43
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 0
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2
    finally:
        owner.close()
