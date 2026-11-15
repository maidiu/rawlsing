"""SOROK #1037 independent G5 reviewer probe (fresh nonauthor session).

Focus: source/root/branch/actor/parent/household/period/operation binding at
the two public first readers, plus the author-disclosed B05 residual: a fully
rehashed SOLE rent receipt for a completed period with no prior actual rent.

Product code is READONLY.  The probe only appends episodes through the public
C12 store API and, where the historical #1023 witness already did so, uses the
same bounded material-fact writes for coherent-ownership cases.  All state is
under this reviewer directory and removed before publication.

Exit convention for this own oracle (disclosed, not the #1027 asset):
  0 = every expected control outcome observed and no residual false accept
  2 = in-scope B05 sole-receipt false accept reproduced (semantic RED)
  1 = harness error / unexpected outcome
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
import time
from argparse import Namespace
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RET = ROOT / "WORKER_RETURNS"
B02 = RET / "SOROK-DUEL-B02-R1"
B04 = RET / "SOROK-DUEL-B04-R1"
B05 = RET / "SOROK-DUEL-B05-R1"
P3 = RET / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
P4 = RET / "SOROK-P4-FIRST-FULL-MPC-R1"
P5 = RET / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P6 = RET / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RET / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
PROJECTION = RET / "SOROK-S45-S47-PROJECTION-20261105-R1"
for _p in (B02, B04, B05, P3, P3 / "tests", P4, P5, P6, ENGINE, PROJECTION):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import historical_period as hp  # noqa: E402
import house  # noqa: E402
import material_operations as mo  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal, detached, digest,
)
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material, parent_material_fixture, read_parent_material,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_1037_G5_REVIEW_PARENT"
PARENT_ALIAS = "P"
REPORT = {"schema": "SOROK1037_B_RECEIPT_G5_REVIEW_PROBE@1",
          "checks": [], "residual": {}, "started": time.time()}


def check(name, ok, detail=None):
    row = {"check": name, "pass": bool(ok)}
    if detail is not None:
        row["detail"] = detail
    REPORT["checks"].append(row)
    print(("PASS " if ok else "FAIL ") + name
          + ("" if detail is None else " :: " + json.dumps(detail, sort_keys=True)))
    return ok


def expect_refusal(name, code, fn):
    try:
        fn()
    except RecursionRefusal as exc:
        return check(name, code in str(exc), {"raised": str(exc)})
    except Exception as exc:  # noqa: BLE001 - record the actual hostile outcome
        return check(name, False, {"unexpected": type(exc).__name__ + ":" + str(exc)})
    return check(name, False, {"raised": None})


def open_state(path):
    path.mkdir(parents=True, exist_ok=True)
    run_p6.experience(path, Namespace(command="new", request_id=None))
    return run_p6.open_owner(path / "actual-p2")


def setup_parent(session, *, cash=100, free_hours=8):
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": "g5-review-private-not-for-child"},
    )
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(
            actor_id=PARENT_ID, source_ref="sourcefree:parent:1037-g5-review",
            employment_status="employed", wage_units_per_hour=5,
            debt_units=4, care_hours_due=2, cash_units=cash,
            free_hours=free_hours, currency_unit=mo.CURRENCY,
        ),
    )


def household_cash(session):
    household = house.read_household(session)
    for binding in household["resources"]:
        if binding.get("kind") == "ACTOR_STATE" and binding.get("actor_slot") == "A":
            return binding["fields"]["cash"]
    raise AssertionError("household A cash binding missing")


def parent_cash(session):
    return read_parent_material(
        session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"]


def rent_episode(session, operation_id):
    return next(
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == rr.RENT_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    )


def purchase_episode(session, operation_id):
    return next(
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == mo.PURCHASE_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    )


def append_rent(session, operation_id, receipt, *, actor_id="A"):
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
        session.branch_id, actor_id=actor_id, kind=rr.RENT_KIND,
        clock=session.clock(), body=body)


def append_purchase(session, operation_id, receipt, *, actor_id=PARENT_ALIAS,
                    body_actor_id=PARENT_ID, alias=PARENT_ALIAS):
    body = {
        "schema": mo.PURCHASE_RECEIPT_SCHEMA,
        "grade": mo.GRADE,
        "root": receipt["root"],
        "branch": receipt["branch"],
        "operation_id": operation_id,
        "actor_id": body_actor_id,
        "alias": alias,
        "status": receipt["status"],
        "receipt": receipt,
    }
    return session.product.store.append_episode(
        session.branch_id, actor_id=actor_id, kind=mo.PURCHASE_KIND,
        clock=session.clock(), body=body)


def rehash_purchase(receipt, operation_id, *, root=None, branch=None,
                    parent_id=PARENT_ID, alias=PARENT_ALIAS):
    receipt = copy.deepcopy(receipt)
    receipt["operation_id"] = operation_id
    receipt["parent_id"] = parent_id
    receipt["parent_alias"] = alias
    if root is not None:
        receipt["root"] = root
    if branch is not None:
        receipt["branch"] = branch
    receipt["purchase_source"] = digest({
        "schema": mo.PURCHASE_RECEIPT_SCHEMA,
        "operation_id": operation_id,
        "parent_id": parent_id,
        "owner_actor_id": receipt.get("owner_actor_id"),
        "object_id": receipt.get("object_id"),
        "unit_price": receipt.get("unit_price"),
        "market_source": receipt.get("market_source_before"),
        "parent_before": receipt.get("parent_material_source_before"),
        "parent_after": receipt.get("parent_material_source_after"),
    })
    return receipt


def write_owned_row(session, receipt):
    world = session.world()
    doc = copy.deepcopy(world.resources[mo.OWNED_SLOT])
    doc["objects"].append({
        "acquisition_id": receipt["operation_id"],
        "object_id": receipt["object_id"],
        "kind": receipt["kind"],
        "owner_actor_id": receipt["owner_actor_id"],
        "quantity": 1,
        "market_source": receipt["market_source_before"],
        "purchase_source": receipt["purchase_source"],
        "currency_unit": receipt["currency_unit"],
        "unit_price": receipt["unit_price"],
    })
    doc["source"] = mo.material_fact_source(doc)
    world.resources[mo.OWNED_SLOT] = doc
    session.product._checkpoint(session.branch_id, world.clock, world)


def household_material_hash(session, *, cash):
    household = house.read_household(session)
    resources = copy.deepcopy(household["resources"])
    for binding in resources:
        if binding.get("kind") == "ACTOR_STATE" and binding.get("actor_slot") == "A":
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


def make_receipt(session, *, operation_id, period_id, status, rent, cash_before,
                 cash_after, household_before_hash, household_after_hash,
                 root=None, branch=None):
    household = house.read_household(session)
    dwelling = house.read_dwelling(session)
    progress = hp.period_progress(session, period_id)
    return {
        "schema": rr.RENT_RECEIPT_SCHEMA,
        "grade": rr.GRADE,
        "status": status,
        "operation_id": operation_id,
        "root": root or session.read_root()["root_hash"],
        "branch": branch or session.branch_id,
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
        "household_material_hash_before": household_before_hash,
        "household_material_hash_after": household_after_hash,
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


def scenario_b05_sole_rehash(local):
    state = local / "b05-sole"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        progress = hp.period_progress(session, "period:2026-h1")
        assert progress["status"] == "COMPLETE"
        assert not [row for row in session.product.store.episodes(session.branch_id)
                    if row.get("kind") == rr.RENT_KIND], "precondition: no rent yet"
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        assert type(rent) is int and rent > 0
        before_hash = household_material_hash(session, cash=cash + rent)
        after_hash = household_material_hash(session, cash=cash)
        op = "g5review:b05:sole-rehashed"
        receipt = make_receipt(
            session, operation_id=op, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash + rent,
            cash_after=cash, household_before_hash=before_hash,
            household_after_hash=after_hash)
        append_rent(session, op, receipt)
        check("sole-rehash: no cash moved by append-only receipt",
              household_cash(session) == cash,
              {"cash_before": cash, "cash_after": household_cash(session)})
        try:
            read = rr.read_household_obligation(session, op)
            accepted = read["status"] == "READ"
            detail = {"status": read["status"], "historical": read["historical"],
                      "household_cash": read["household_cash"],
                      "receipt_status": read["receipt"]["status"]}
        except RecursionRefusal as exc:
            accepted = False
            detail = {"refused": str(exc)}
        REPORT["residual"]["b05_sole_rehashed_receipt"] = {
            "accepted": accepted,
            "detail": detail,
            "source_bound": {
                "root": session.read_root()["root_hash"],
                "branch": session.branch_id,
                "operation_id": op,
                "period_id": "period:2026-h1",
                "prior_actual_rent": False,
            },
        }
        check("sole-rehashed receipt for completed period with no prior actual "
              "rent is refused (expected by #1037 operation binding)", not accepted,
              detail)
        return accepted
    finally:
        owner.close()


def scenario_b05_controls(local):
    state = local / "b05-controls"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        real = rr.apply_household_rent(
            session, operation_id="g5review:b05:real",
            period_id="period:2026-h1")
        check("b05 control: genuine rent admitted", real["status"] == "ADMITTED")
        baseline = rr.read_household_obligation(session, "g5review:b05:real")
        check("b05 control: genuine rent reads", baseline["status"] == "READ")
        cash = household_cash(session)
        original = copy.deepcopy(rent_episode(session, "g5review:b05:real")["body"])

        # Foreign nested root/branch.
        body = copy.deepcopy(original)
        op = "g5review:b05:foreign-root"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["receipt"]["root"] = "e" * 64
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 foreign nested root refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        body = copy.deepcopy(original)
        op = "g5review:b05:foreign-branch"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["receipt"]["branch"] = "foreign-branch"
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 foreign nested branch refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        body = copy.deepcopy(original)
        op = "g5review:b05:body-root"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["root"] = "0" * 64
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 foreign body root refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        # Wrong actor.
        body = copy.deepcopy(original)
        op = "g5review:b05:wrong-actor"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        session.product.store.append_episode(
            session.branch_id, actor_id="B", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 wrong episode actor refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        # Receipt exchange: body operation and nested receipt operation differ.
        body = copy.deepcopy(original)
        op = "g5review:b05:exchange"
        body["operation_id"] = op
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 exchanged nested receipt operation refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        # Forged period.
        body = copy.deepcopy(original)
        op = "g5review:b05:foreign-period"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["receipt"]["period_id"] = "period:2026-h2"
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 foreign/incomplete period refused",
                       "B05_RENT_PERIOD_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        # Forged rent against the same current dwelling source.
        body = copy.deepcopy(original)
        op = "g5review:b05:wrong-rent"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["receipt"]["monthly_rent"] = 99
        body["receipt"]["household_cash_before"] = cash + 99
        body["receipt"]["household_cash_after"] = cash
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 receipt rent not current dwelling rent refused",
                       "B05_RENT_PROVENANCE_MISMATCH",
                       lambda: rr.read_household_obligation(session, op))

        # Same-period second receipt with fully coherent cash arithmetic.
        body = copy.deepcopy(original)
        op = "g5review:b05:second"
        body["operation_id"] = op
        body["receipt"]["operation_id"] = op
        body["receipt"]["household_cash_before"] = cash + 12
        body["receipt"]["household_cash_after"] = cash
        body["receipt"]["monthly_rent"] = 12
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b05 same-period second receipt refused",
                       "B05_RENT_OPERATION_NOT_UNIQUE",
                       lambda: rr.read_household_obligation(session, op))
        expect_refusal("b05 genuine receipt is fail-closed while forged "
                       "same-period sibling exists",
                       "B05_RENT_OPERATION_NOT_UNIQUE",
                       lambda: rr.read_household_obligation(
                           session, "g5review:b05:real"))
        check("b05 control: append-only forgeries never moved cash",
              household_cash(session) == cash)
    finally:
        owner.close()


def scenario_b05_historical(local):
    state = local / "b05-historical"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        h1 = rr.apply_household_rent(
            session, operation_id="g5review:b05:h1",
            period_id="period:2026-h1")
        check("b05 historical: h1 rent admitted", h1["status"] == "ADMITTED")
        hp.materialize_to(session, "2027-01-01")
        h2 = rr.apply_household_rent(
            session, operation_id="g5review:b05:h2",
            period_id="period:2026-h2")
        check("b05 historical: h2 rent admitted", h2["status"] == "ADMITTED")
        read_h1 = rr.read_household_obligation(session, "g5review:b05:h1")
        read_h2 = rr.read_household_obligation(session, "g5review:b05:h2")
        check("b05 historical genuine h1 receipt still reads with historical=true",
              read_h1["status"] == "READ" and read_h1["historical"] is True,
              {"historical": read_h1["historical"], "cash": read_h1["household_cash"]})
        check("b05 current genuine h2 receipt reads with historical=false",
              read_h2["status"] == "READ" and read_h2["historical"] is False,
              {"historical": read_h2["historical"], "cash": read_h2["household_cash"]})
        check("b05 historical: two periods debit exactly twice",
              read_h2["household_cash"] == h1["household_cash_after"] - 12)
    finally:
        owner.close()


def scenario_b05_dwelling_change(local):
    state = local / "b05-dwelling"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        rr.apply_household_rent(
            session, operation_id="g5review:b05:before-change",
            period_id="period:2026-h1")
        baseline = rr.read_household_obligation(
            session, "g5review:b05:before-change")
        stored = copy.deepcopy(session.world().resources[house.DWELLING_SLOT])
        changed = copy.deepcopy(house.dwelling_fixture(session))
        changed["costs"]["monthly_rent"] = baseline["receipt"]["monthly_rent"] + 8
        changed["costs"]["rent_due_now"] = changed["costs"]["monthly_rent"]
        house.commit_dwelling(session, facts=changed)
        expect_refusal("b05 genuine historical receipt after lawful dwelling "
                       "change is not falsely accepted",
                       "B05_RENT_SOURCE_STALE",
                       lambda: rr.read_household_obligation(
                           session, "g5review:b05:before-change"))
        world = session.world()
        world.resources[house.DWELLING_SLOT] = stored
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored = rr.read_household_obligation(
            session, "g5review:b05:before-change")
        check("b05 changed/restored dwelling exact read restore",
              restored == baseline)
    finally:
        owner.close()


def stored_parent_cash(session):
    return session.world().actor_state[PARENT_ALIAS]["material"]["cash_units"]


def scenario_b04_basic(local):
    state = local / "b04-basic"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        real = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="g5review:b04:real",
            owner_actor_id=holder)
        check("b04 control: genuine purchase admitted",
              real["status"] == "ADMITTED")
        baseline = mo.read_purchase(
            session, PARENT_ID, "g5review:b04:real", as_actor=PARENT_ID)
        check("b04 control: genuine purchase reads",
              baseline["status"] == "READ" and baseline["historical"] is False)
        cash_after_real = parent_cash(session)
        market_after_real = mo.read_market_inventory(session)["source"]
        owned_after_real = mo.read_owned_objects(session)["source"]

        # Changed/restored ownership source.
        world = session.world()
        stored_owned = copy.deepcopy(world.resources[mo.OWNED_SLOT])
        empty = copy.deepcopy(stored_owned)
        empty["objects"] = []
        empty["source"] = mo.material_fact_source(empty)
        world.resources[mo.OWNED_SLOT] = empty
        session.product._checkpoint(session.branch_id, world.clock, world)
        expect_refusal("b04 ownership row removed refuses",
                       "PURCHASE_READ_STALE",
                       lambda: mo.read_purchase(
                           session, PARENT_ID, "g5review:b04:real",
                           as_actor=PARENT_ID))
        world = session.world()
        world.resources[mo.OWNED_SLOT] = stored_owned
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored = mo.read_purchase(
            session, PARENT_ID, "g5review:b04:real", as_actor=PARENT_ID)
        check("b04 changed/restored ownership exact read restore",
              restored["status"] == "READ" and restored["owned_source"]
              == owned_after_real)

        real_body = copy.deepcopy(purchase_episode(
            session, "g5review:b04:real")["body"])

        # Receipt exchange: body operation and nested receipt operation differ.
        body = copy.deepcopy(real_body)
        op = "g5review:b04:exchange"
        body["operation_id"] = op
        session.product.store.append_episode(
            session.branch_id, actor_id=PARENT_ALIAS, kind=mo.PURCHASE_KIND,
            clock=session.clock(), body=body)
        expect_refusal("b04 exchanged nested receipt operation refused",
                       "PURCHASE_READ_PROVENANCE_MISMATCH",
                       lambda: mo.read_purchase(
                           session, PARENT_ID, op, as_actor=PARENT_ID))

        # Foreign nested root/branch with a coherent ownership row.
        forged = rehash_purchase(real_body["receipt"],
                                 "g5review:b04:foreign-root",
                                 root="f" * 64, branch="foreign-branch")
        write_owned_row(session, forged)
        append_purchase(session, "g5review:b04:foreign-root", forged)
        expect_refusal("b04 foreign nested root/branch refused",
                       "PURCHASE_READ_PROVENANCE_MISMATCH",
                       lambda: mo.read_purchase(
                           session, PARENT_ID, "g5review:b04:foreign-root",
                           as_actor=PARENT_ID))
        check("b04 foreign root forgery left stored parent cash",
              stored_parent_cash(session) == cash_after_real,
              {"stored_parent_cash": stored_parent_cash(session),
               "expected": cash_after_real})
        check("b04 foreign root forgery left market source",
              mo.read_market_inventory(session)["source"] == market_after_real)
    finally:
        owner.close()


def scenario_b04_c02_chain(local):
    state = local / "b04-c02-chain"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]
        real = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="g5review:b04:real",
            owner_actor_id=holder)
        check("b04 c02 control: genuine purchase admitted",
              real["status"] == "ADMITTED")
        cash_after_real = parent_cash(session)
        market_after_real = mo.read_market_inventory(session)["source"]
        real_receipt = copy.deepcopy(real)

        # Chain-extending forgery: correct session root/branch/actor/alias,
        # coherent source chain and recomputed purchase_source, coherent owned
        # row, but no actual parent cash debit and no C02 owner history write.
        op = "g5review:b04:c02-chain-forgery"
        forged = copy.deepcopy(real_receipt)
        forged["operation_id"] = op
        forged["parent_material_source_before"] = real_receipt[
            "parent_material_source_after"]
        forged["parent_material_source_after"] = digest({
            "review": "forged-parent-material-after",
            "operation_id": op,
        })
        forged["parent_cash_before"] = real_receipt["parent_cash_after"]
        forged["parent_cash_after"] = real_receipt["parent_cash_after"] - forged[
            "unit_price"]
        forged["owned_source_before"] = real_receipt["owned_source_after"]
        forged["purchase_source"] = digest({
            "schema": mo.PURCHASE_RECEIPT_SCHEMA,
            "operation_id": op,
            "parent_id": PARENT_ID,
            "owner_actor_id": forged["owner_actor_id"],
            "object_id": forged["object_id"],
            "unit_price": forged["unit_price"],
            "market_source": forged["market_source_before"],
            "parent_before": forged["parent_material_source_before"],
            "parent_after": forged["parent_material_source_after"],
        })
        write_owned_row(session, forged)
        append_purchase(session, op, forged)
        try:
            read = mo.read_purchase(
                session, PARENT_ID, op, as_actor=PARENT_ID)
            accepted = read["status"] == "READ"
            detail = {"status": read["status"]}
        except RecursionRefusal as exc:
            accepted = False
            detail = {"refused": str(exc)}
        check("b04 chain-extending rehashed forgery is refused by the actual "
              "C02 parent-material owner chain, not accepted on local hashes",
              not accepted, detail)
        check("b04 chain forgery left stored parent cash undebited",
              stored_parent_cash(session) == cash_after_real,
              {"stored_parent_cash": stored_parent_cash(session),
               "expected": cash_after_real})
        check("b04 chain forgery left market source unchanged",
              mo.read_market_inventory(session)["source"] == market_after_real)
        check("b04 forged receipt hash was self-consistent before refusal",
              forged["purchase_source"] == digest({
                  "schema": mo.PURCHASE_RECEIPT_SCHEMA,
                  "operation_id": op,
                  "parent_id": PARENT_ID,
                  "owner_actor_id": forged["owner_actor_id"],
                  "object_id": forged["object_id"],
                  "unit_price": forged["unit_price"],
                  "market_source": forged["market_source_before"],
                  "parent_before": forged["parent_material_source_before"],
                  "parent_after": forged["parent_material_source_after"],
              }))
    finally:
        owner.close()


def main():
    local = HERE / ".local-data" / "review"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    residual = False
    try:
        residual = scenario_b05_sole_rehash(local)
        scenario_b05_controls(local)
        scenario_b05_historical(local)
        scenario_b05_dwelling_change(local)
        scenario_b04_basic(local)
        scenario_b04_c02_chain(local)
    finally:
        REPORT["residual"]["reproduced"] = bool(residual)
        REPORT["verdict"] = ("REVISE_EXACT_DEFECT" if residual
                             else "NO_RESIDUAL_FALSE_ACCEPT")
        REPORT["finished"] = time.time()
        REPORT["elapsed_seconds"] = round(
            REPORT["finished"] - REPORT["started"], 3)
        REPORT["failed_checks"] = [
            row for row in REPORT["checks"] if not row["pass"]]
        (HERE / "evidence" / "g5_review_probe_report.json").write_text(
            json.dumps(REPORT, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print("REVIEW_RESIDUAL", json.dumps(REPORT["residual"], sort_keys=True))
    print("REVIEW_FAILED_CHECKS", json.dumps(
        REPORT["failed_checks"], sort_keys=True))
    if REPORT["failed_checks"] and not residual:
        return 1
    return 2 if residual else 0


if __name__ == "__main__":
    raise SystemExit(main())
