"""SOROK #1037 R2 focused reviewer probe (same nonauthor session).

Independent checks for the R2 claim that an ADMITTED rent receipt must match
the actual C12 owner transition, plus the zero/held/historical/retry edges and
the most discriminating question: a legitimate public non-rent checkpoint pair
of the same cash state at the same clock.

Product is READONLY.  State stays under this reviewer root and is removed.
Own oracle exit: 0 = no false ADMITTED proof found; 2 = false ADMITTED proof
reproduced; 1 = harness/unexpected.
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

REPORT = {"schema": "SOROK1037_R2_FOCUSED_REVIEW_PROBE@1",
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


def checkpoint_household(session, checkpoint):
    state = checkpoint.get("state")
    snapshot = state.get("world") if isinstance(state, dict) else None
    if not isinstance(snapshot, dict):
        return None
    try:
        root_row = session.read_root()
        world = type(session.world()).restore(dict(snapshot))
        document = world.resources.get(house.HOUSEHOLD_SLOT)
        return house._read_household_document(
            document, world, root_row["root_hash"], session.branch_id,
            tuple(root_row.get("actor_ids") or ()))
    except Exception:
        return None


def checkpoint_cash(household):
    for binding in household["resources"]:
        if binding.get("kind") == "ACTOR_STATE" and binding.get("actor_slot") == "A":
            return binding["fields"]["cash"]
    return None


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


def set_rent(session, rent):
    facts = copy.deepcopy(house.dwelling_fixture(session))
    facts["costs"]["monthly_rent"] = rent
    facts["costs"]["rent_due_now"] = rent
    house.commit_dwelling(session, facts=facts)


def scenario_zero_false_admitted(local):
    """Two public no-cash actions give an adjacent same-clock checkpoint pair;
    a sole appended ADMITTED zero-rent receipt must not be proven by it."""
    state = local / "zero-false-admitted"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        set_rent(session, 0)
        hp.materialize_to(session, "2026-07-01")
        clock = session.clock()
        first = session.product.say("g5-r2-zero-probe-1", actor="A")
        second = session.product.say("g5-r2-zero-probe-2", actor="A")
        check("zero probe: public no-cash actions succeed and do not advance clock",
              first.get("status") == "OK" and second.get("status") == "OK"
              and session.clock() == clock,
              {"clock": clock, "first": first.get("status"),
               "second": second.get("status"), "current": session.clock()})
        cash = household_cash(session)
        h = household_material_hash(session, cash=cash)
        op = "g5review:r2:zero-false-admitted"
        receipt = make_receipt(
            session, operation_id=op, period_id="period:2026-h1",
            status="ADMITTED", rent=0, cash_before=cash, cash_after=cash,
            before_hash=h, after_hash=h)
        append_rent(session, op, receipt)
        check("zero probe: append changed no household cash",
              household_cash(session) == cash,
              {"cash_before": cash, "cash_after": household_cash(session)})
        try:
            read = rr.read_household_obligation(session, op)
            accepted = read["status"] == "READ"
            detail = {"status": read["status"],
                      "historical": read.get("historical"),
                      "receipt_status": read.get("receipt", {}).get("status"),
                      "household_cash": read.get("household_cash")}
        except RecursionRefusal as exc:
            accepted = False
            detail = {"refused": str(exc)}
        checkpoints = session.product.store.checkpoints(session.branch_id)
        at_clock = []
        for index, checkpoint in enumerate(checkpoints):
            if checkpoint.get("clock") != clock:
                continue
            household = checkpoint_household(session, checkpoint)
            if household is None:
                continue
            at_clock.append({
                "index": index,
                "checkpoint_clock": checkpoint.get("clock"),
                "world_clock": household.get("clock"),
                "cash": checkpoint_cash(household),
                "material_hash": household.get("material_hash"),
                "source": household.get("source"),
            })
        REPORT["residual"]["zero_false_admitted"] = {
            "accepted": accepted, "detail": detail,
            "source_bound": {
                "root": session.read_root()["root_hash"],
                "branch": session.branch_id,
                "clock": clock,
                "operation_id": op,
                "period_id": "period:2026-h1",
                "actual_writer_zero_status": "UNCHANGED",
                "public_actions": [
                    {"api": "session.product.say", "text": "g5-r2-zero-probe-1",
                     "status": first.get("status")},
                    {"api": "session.product.say", "text": "g5-r2-zero-probe-2",
                     "status": second.get("status")},
                ],
                "checkpoints_at_receipt_clock": at_clock,
                "forged_receipt": {
                    "status": "ADMITTED",
                    "monthly_rent": 0,
                    "household_cash_before": cash,
                    "household_cash_after": cash,
                    "household_material_hash_before": h,
                    "household_material_hash_after": h,
                },
                "cash_before_append": cash,
                "cash_after_append": household_cash(session),
            },
        }
        check("zero probe: forged ADMITTED zero-rent receipt is not accepted as "
              "actual operation proof", not accepted, detail)
        return accepted
    finally:
        owner.close()


def scenario_positive_control(local):
    """A positive forged rent cannot use the same unchanged-cash pair."""
    state = local / "positive-control"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        session.product.say("g5-r2-positive-probe-1", actor="A")
        session.product.say("g5-r2-positive-probe-2", actor="A")
        cash = household_cash(session)
        rent = house.read_dwelling(session)["costs"]["monthly_rent"]
        h_before = household_material_hash(session, cash=cash + rent)
        h_after = household_material_hash(session, cash=cash)
        op = "g5review:r2:positive-false"
        receipt = make_receipt(
            session, operation_id=op, period_id="period:2026-h1",
            status="ADMITTED", rent=rent, cash_before=cash + rent,
            cash_after=cash, before_hash=h_before, after_hash=h_after)
        append_rent(session, op, receipt)
        expect_refusal(
            "positive probe: unchanged-cash public checkpoints do not prove a "
            "forged debit", "B05_RENT_OPERATION_UNPROVEN",
            lambda: rr.read_household_obligation(session, op))
    finally:
        owner.close()


def scenario_zero_genuine(local):
    state = local / "zero-genuine"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        set_rent(session, 0)
        hp.materialize_to(session, "2026-07-01")
        cash = household_cash(session)
        receipt = rr.apply_household_rent(
            session, operation_id="g5review:r2:zero-genuine",
            period_id="period:2026-h1")
        check("zero genuine: existing writer produces UNCHANGED",
              receipt["status"] == "UNCHANGED", {"status": receipt["status"]})
        read = rr.read_household_obligation(
            session, "g5review:r2:zero-genuine")
        check("zero genuine: UNCHANGED reads without a debit checkpoint",
              read["status"] == "READ"
              and read["receipt"]["status"] == "UNCHANGED"
              and read["household_cash"] == cash,
              {"status": read["status"],
               "receipt_status": read["receipt"]["status"],
               "cash": read["household_cash"]})
    finally:
        owner.close()


def scenario_held(local):
    state = local / "held"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        world = session.world()
        world.actor_state["A"]["cash"] = 5
        session.product._checkpoint(session.branch_id, world.clock, world)
        receipt = rr.apply_household_rent(
            session, operation_id="g5review:r2:held",
            period_id="period:2026-h1")
        check("held: existing writer produces REFUSED",
              receipt["status"] == "REFUSED", {"status": receipt["status"]})
        read = rr.read_household_obligation(session, "g5review:r2:held")
        check("held: REFUSED reads without a debit checkpoint",
              read["status"] == "READ"
              and read["receipt"]["status"] == "REFUSED"
              and read["household_cash"] == 5,
              {"status": read["status"],
               "receipt_status": read["receipt"]["status"],
               "cash": read["household_cash"]})
    finally:
        owner.close()


def scenario_sever_restore(local):
    state = local / "sever"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        rr.apply_household_rent(
            session, operation_id="g5review:r2:real",
            period_id="period:2026-h1")
        baseline = rr.read_household_obligation(
            session, "g5review:r2:real")
        clock = baseline["receipt"]["clock"]
        store = session.product.store
        original = store.checkpoints
        try:
            store.checkpoints = lambda branch: [
                row for row in original(branch) if row.get("clock") != clock]
            expect_refusal(
                "sever: hiding actual-clock checkpoints refuses the genuine rent",
                "B05_RENT_OPERATION_UNPROVEN",
                lambda: rr.read_household_obligation(
                    session, "g5review:r2:real"))
        finally:
            del store.checkpoints
        restored = rr.read_household_obligation(
            session, "g5review:r2:real")
        check("sever: exact checkpoint restore returns exact baseline read",
              restored == baseline)
    finally:
        owner.close()


def scenario_sibling(local):
    state = local / "sibling"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2027-01-01")
        rr.apply_household_rent(
            session, operation_id="g5review:r2:h1",
            period_id="period:2026-h1")
        genuine = copy.deepcopy(rr.read_household_obligation(
            session, "g5review:r2:h1")["receipt"])
        forged = copy.deepcopy(genuine)
        forged["operation_id"] = "g5review:r2:h2-copy"
        forged["period_id"] = "period:2026-h2"
        append_rent(session, "g5review:r2:h2-copy", forged)
        expect_refusal(
            "sibling: forged h2 copy of the h1 transition is refused",
            "B05_RENT_OPERATION_UNPROVEN",
            lambda: rr.read_household_obligation(
                session, "g5review:r2:h2-copy"))
        expect_refusal(
            "sibling: genuine h1 is fail-closed while the copy exists",
            "B05_RENT_OPERATION_UNPROVEN",
            lambda: rr.read_household_obligation(
                session, "g5review:r2:h1"))
    finally:
        owner.close()


def scenario_historical_retry(local):
    state = local / "historical"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-07-01")
        h1 = rr.apply_household_rent(
            session, operation_id="g5review:r2:hist-h1",
            period_id="period:2026-h1")
        hp.materialize_to(session, "2027-01-01")
        h2 = rr.apply_household_rent(
            session, operation_id="g5review:r2:hist-h2",
            period_id="period:2026-h2")
        read_h1 = rr.read_household_obligation(
            session, "g5review:r2:hist-h1")
        read_h2 = rr.read_household_obligation(
            session, "g5review:r2:hist-h2")
        check("historical: genuine h1 remains historical=true after h2",
              read_h1["status"] == "READ" and read_h1["historical"] is True,
              {"historical": read_h1["historical"]})
        check("historical: current h2 remains historical=false",
              read_h2["status"] == "READ" and read_h2["historical"] is False,
              {"historical": read_h2["historical"]})
        check("historical: exactly two debits",
              read_h2["household_cash"] == h1["household_cash_after"] - 12)
        replay = rr.apply_household_rent(
            session, operation_id="g5review:r2:hist-h1",
            period_id="period:2026-h1")
        check("retry: replay is REPLAY without a second debit",
              replay["status"] == "REPLAY"
              and household_cash(session) == h2["household_cash_after"])
        expect_refusal(
            "retry: late same-period operation remains already recorded",
            "B05_RENT_ALREADY_RECORDED",
            lambda: rr.apply_household_rent(
                session, operation_id="g5review:r2:hist-h1-late",
                period_id="period:2026-h1"))
    finally:
        owner.close()


def main():
    local = HERE / ".local-data" / "focused"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    zero_false = False
    try:
        zero_false = scenario_zero_false_admitted(local)
        scenario_positive_control(local)
        scenario_zero_genuine(local)
        scenario_held(local)
        scenario_sever_restore(local)
        scenario_sibling(local)
        scenario_historical_retry(local)
    finally:
        REPORT["residual"]["reproduced"] = bool(zero_false)
        REPORT["verdict"] = ("REVISE_EXACT_DEFECT" if zero_false
                             else "NO_RESIDUAL_FALSE_ACCEPT")
        REPORT["finished"] = time.time()
        REPORT["elapsed_seconds"] = round(
            REPORT["finished"] - REPORT["started"], 3)
        REPORT["failed_checks"] = [
            row for row in REPORT["checks"] if not row["pass"]]
        (HERE / "evidence" / "g5_r2_focused_probe_report.json").write_text(
            json.dumps(REPORT, indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print("R2_RESIDUAL", json.dumps(REPORT["residual"], sort_keys=True))
    print("R2_FAILED_CHECKS", json.dumps(
        REPORT["failed_checks"], sort_keys=True))
    if REPORT["failed_checks"] and not zero_false:
        return 1
    return 2 if zero_false else 0


if __name__ == "__main__":
    raise SystemExit(main())
