"""SOROK #1037 R3 independent reviewer negative/positive witness.

Own construction, not the author's test copy.  Uses existing public product
actions and public append_episode, then the actual public reader
read_household_obligation.  Checks malformed ADMITTED status/debit shapes and
a same-period replay boundary, while distinguishing genuine zero UNCHANGED,
held REFUSED and positive ADMITTED.

Product is READONLY.  State is under this reviewer root and removed.
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
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import (  # noqa: E402
    RecursionRefusal, detached, digest,
)

REPORT = {"schema": "SOROK1037_R3_INDEPENDENT_REVIEW_PROBE@1",
          "checks": [], "cases": {}, "started": time.time()}


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
    except Exception as exc:  # noqa: BLE001
        return check(name, False, {"unexpected": type(exc).__name__ + ":" + str(exc)})
    return check(name, False, {"raised": None})


def open_state(path):
    path.mkdir(parents=True, exist_ok=True)
    run_p6.experience(path, Namespace(command="new", request_id=None))
    return run_p6.open_owner(path / "actual-p2")


def household_cash(session):
    household = house.read_household(session)
    for binding in household["resources"]:
        if binding.get("kind") == "ACTOR_STATE" and binding.get("actor_slot") == "A":
            return binding["fields"]["cash"]
    raise AssertionError("household A cash binding missing")


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


def malformed_admitted(local):
    """ADMITTED must be a strict positive debit, not merely a matching pair."""
    state = local / "malformed-admitted"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        clock = session.clock()
        session.product.say("r3-review-malformed-1", actor="A")
        session.product.say("r3-review-malformed-2", actor="A")
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        h_now = household_material_hash(session, cash=cash)
        h_before = household_material_hash(session, cash=cash)
        op_no_decrease = "g5review:r3:admitted-no-decrease"
        receipt = make_receipt(
            session, operation_id=op_no_decrease, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash, cash_after=cash,
            before_hash=h_now, after_hash=h_now)
        append_rent(session, op_no_decrease, receipt)
        expect_refusal(
            "own negative: ADMITTED positive rent with no cash decrease is "
            "rejected by the actual reader", "B05_RENT_RECEIPT_INVALID",
            lambda: rr.read_household_obligation(session, op_no_decrease))
        REPORT["cases"]["admitted_no_decrease"] = {
            "operation": op_no_decrease, "rent": rent,
            "cash_before": cash, "cash_after": cash,
            "clock": clock, "expected": "B05_RENT_RECEIPT_INVALID",
        }

        op_wrong_debit = "g5review:r3:admitted-wrong-debit"
        wrong_after = cash - 5
        receipt = make_receipt(
            session, operation_id=op_wrong_debit, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash, cash_after=wrong_after,
            before_hash=h_now,
            after_hash=household_material_hash(session, cash=wrong_after))
        append_rent(session, op_wrong_debit, receipt)
        expect_refusal(
            "own negative: ADMITTED rent does not equal the cash decrease is "
            "rejected by the actual reader", "B05_RENT_RECEIPT_INVALID",
            lambda: rr.read_household_obligation(session, op_wrong_debit))
        REPORT["cases"]["admitted_wrong_debit"] = {
            "operation": op_wrong_debit, "rent": rent,
            "cash_before": cash, "cash_after": wrong_after,
            "clock": clock, "expected": "B05_RENT_RECEIPT_INVALID",
        }

        check("own negative: malformed ADMITTED forgeries moved no cash",
              household_cash(session) == cash,
              {"cash": household_cash(session)})
    finally:
        owner.close()


def malformed_no_transition(local):
    """A fresh state isolates the checkpoint-proof negative from same-period
    uniqueness; no actual debit transition exists for the forged receipt."""
    state = local / "malformed-no-transition"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        clock = session.clock()
        session.product.say("r3-review-no-transition-1", actor="A")
        session.product.say("r3-review-no-transition-2", actor="A")
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        h_before = household_material_hash(session, cash=cash + rent)
        h_after = household_material_hash(session, cash=cash)
        op = "g5review:r3:admitted-no-transition"
        receipt = make_receipt(
            session, operation_id=op, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash + rent,
            cash_after=cash, before_hash=h_before, after_hash=h_after)
        append_rent(session, op, receipt)
        expect_refusal(
            "own negative: well-formed ADMITTED debit with no actual checkpoint "
            "transition remains unproven", "B05_RENT_OPERATION_UNPROVEN",
            lambda: rr.read_household_obligation(session, op))
        check("own negative: no-transition forgery moved no cash",
              household_cash(session) == cash,
              {"cash": household_cash(session)})
        REPORT["cases"]["admitted_no_transition"] = {
            "operation": op, "rent": rent, "cash_before": cash + rent,
            "cash_after": cash, "clock": clock,
            "expected": "B05_RENT_OPERATION_UNPROVEN"}
    finally:
        owner.close()


def genuine_statuses(local):
    """Genuine zero UNCHANGED, held REFUSED and positive ADMITTED still read."""
    zero = open_state(local / "genuine-zero")
    try:
        session = zero.base_owner.fanin.session
        hp.establish_period_plan(session)
        set_rent(session, 0)
        hp.materialize_to(session, "2026-07-01")
        cash = household_cash(session)
        receipt = rr.apply_household_rent(
            session, operation_id="g5review:r3:genuine-zero",
            period_id="period:2026-h1")
        read = rr.read_household_obligation(
            session, "g5review:r3:genuine-zero")
        check("genuine zero: writer UNCHANGED and reader READ without debit",
              receipt["status"] == "UNCHANGED"
              and read["status"] == "READ"
              and read["receipt"]["status"] == "UNCHANGED"
              and read["household_cash"] == cash,
              {"writer": receipt["status"], "reader": read["status"],
               "receipt": read["receipt"]["status"],
               "cash": read["household_cash"]})
        REPORT["cases"]["genuine_zero"] = {
            "writer": receipt["status"], "reader": read["status"],
            "cash": read["household_cash"]}
    finally:
        zero.close()

    held = open_state(local / "genuine-held")
    try:
        session = held.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        world = session.world()
        world.actor_state["A"]["cash"] = 5
        session.product._checkpoint(session.branch_id, world.clock, world)
        receipt = rr.apply_household_rent(
            session, operation_id="g5review:r3:genuine-held",
            period_id="period:2026-h1")
        read = rr.read_household_obligation(
            session, "g5review:r3:genuine-held")
        check("genuine held: writer REFUSED and reader READ without debit",
              receipt["status"] == "REFUSED"
              and read["status"] == "READ"
              and read["receipt"]["status"] == "REFUSED"
              and read["household_cash"] == 5,
              {"writer": receipt["status"], "reader": read["status"],
               "receipt": read["receipt"]["status"],
               "cash": read["household_cash"]})
        REPORT["cases"]["genuine_held"] = {
            "writer": receipt["status"], "reader": read["status"],
            "cash": read["household_cash"]}
    finally:
        held.close()

    positive = open_state(local / "genuine-positive")
    try:
        session = positive.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        h1 = rr.apply_household_rent(
            session, operation_id="g5review:r3:genuine-h1",
            period_id="period:2026-h1")
        read_h1 = rr.read_household_obligation(
            session, "g5review:r3:genuine-h1")
        hp.materialize_to(session, "2027-01-01")
        h2 = rr.apply_household_rent(
            session, operation_id="g5review:r3:genuine-h2",
            period_id="period:2026-h2")
        read_h1_after = rr.read_household_obligation(
            session, "g5review:r3:genuine-h1")
        read_h2 = rr.read_household_obligation(
            session, "g5review:r3:genuine-h2")
        check("genuine positive: ADMITTED debits exactly and reads",
              h1["status"] == "ADMITTED" and h2["status"] == "ADMITTED"
              and read_h2["household_cash"] == h1["household_cash_after"] - 12,
              {"h1": h1["status"], "h2": h2["status"],
               "cash": read_h2["household_cash"]})
        check("genuine positive historical chain: h1 true, h2 false",
              read_h1_after["status"] == "READ"
              and read_h1_after["historical"] is True
              and read_h2["status"] == "READ"
              and read_h2["historical"] is False,
              {"h1_historical": read_h1_after["historical"],
               "h2_historical": read_h2["historical"]})
        REPORT["cases"]["genuine_positive"] = {
            "h1": h1["status"], "h2": h2["status"],
            "h1_historical_after_h2": read_h1_after["historical"],
            "h2_historical": read_h2["historical"],
            "cash": read_h2["household_cash"]}
    finally:
        positive.close()


def replay_boundary(local):
    """A second same-period ADMITTED receipt cannot copy the genuine debit."""
    state = local / "replay-boundary"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        real = rr.apply_household_rent(
            session, operation_id="g5review:r3:replay-real",
            period_id="period:2026-h1")
        cash = household_cash(session)
        copied = copy.deepcopy(real)
        copied["operation_id"] = "g5review:r3:replay-copy"
        append_rent(session, "g5review:r3:replay-copy", copied)
        expect_refusal(
            "own replay boundary: same-period copied ADMITTED receipt is "
            "refused by actual reader", "B05_RENT_OPERATION_NOT_UNIQUE",
            lambda: rr.read_household_obligation(
                session, "g5review:r3:replay-copy"))
        expect_refusal(
            "own replay boundary: genuine receipt is fail-closed while the "
            "copy exists", "B05_RENT_OPERATION_NOT_UNIQUE",
            lambda: rr.read_household_obligation(
                session, "g5review:r3:replay-real"))
        check("own replay boundary: no second debit", household_cash(session) == cash,
              {"cash": household_cash(session)})
        REPORT["cases"]["replay_boundary"] = {
            "real": real["operation_id"], "copy": copied["operation_id"],
            "cash_before": cash, "cash_after": household_cash(session),
            "expected": "B05_RENT_OPERATION_NOT_UNIQUE"}
    finally:
        owner.close()


def main():
    local = HERE / ".local-data" / "r3-independent"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    try:
        malformed_admitted(local)
        malformed_no_transition(local)
        genuine_statuses(local)
        replay_boundary(local)
    finally:
        REPORT["finished"] = time.time()
        REPORT["elapsed_seconds"] = round(
            REPORT["finished"] - REPORT["started"], 3)
        REPORT["failed_checks"] = [
            row for row in REPORT["checks"] if not row["pass"]]
        (HERE / "evidence" / "g5_r3_independent_probe_report.json").write_text(
            json.dumps(REPORT, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print("R3_NEGATIVE_FAILED_CHECKS", json.dumps(
        REPORT["failed_checks"], sort_keys=True))
    return 1 if REPORT["failed_checks"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
