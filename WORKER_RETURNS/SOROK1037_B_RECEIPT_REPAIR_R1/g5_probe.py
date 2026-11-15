"""SOROK #1023 independent G5 hostile first-reader witness.

Reviewer-owned script. Product code is READONLY; all generated state stays
under this reviewer directory and is removed before publication.
"""
from __future__ import annotations

import copy
import json
import shutil
import sys
import tempfile
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
from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material,
    parent_material_fixture,
    read_parent_history,
    read_parent_material,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_G5_REVIEW_PARENT"
PARENT_ALIAS = "P"
CURRENCY = mo.CURRENCY
REPORT = {"schema": "SOROK1023_G5_HOSTILE_REPORT@1", "checks": [], "defects": []}
STARTED = time.perf_counter()


def check(name, condition, detail=None):
    row = {"check": name, "pass": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    REPORT["checks"].append(row)
    print(("PASS " if condition else "FAIL ") + name
          + ("" if detail is None else " :: " + json.dumps(detail, sort_keys=True)))
    if not condition:
        raise AssertionError(name)


def note_check(name, condition, detail=None):
    """Record a defect witness without aborting the remaining attacks."""
    row = {"check": name, "pass": bool(condition)}
    if detail is not None:
        row["detail"] = detail
    REPORT["checks"].append(row)
    print(("PASS " if condition else "FAIL ") + name
          + ("" if detail is None else " :: " + json.dumps(detail, sort_keys=True)))


def refusal(check_name, code, fn):
    try:
        fn()
    except RecursionRefusal as exc:
        check(check_name, code in str(exc), {"raised": str(exc)})
        return
    except Exception as exc:  # noqa: BLE001 - hostile witness records actual type
        check(check_name, False, {"unexpected": type(exc).__name__ + ":" + str(exc)})
        return
    check(check_name, False, {"raised": None})


def open_state(state):
    state.mkdir(parents=True, exist_ok=True)
    run_p6.experience(state, Namespace(command="new", request_id=None))
    return run_p6.open_owner(state / "actual-p2")


def setup_parent(session, *, cash=100, free_hours=8, currency=CURRENCY):
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": "g5-review-private-not-for-child"},
    )
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(
            actor_id=PARENT_ID, source_ref="sourcefree:parent:g5-review",
            employment_status="employed", wage_units_per_hour=5,
            debt_units=4, care_hours_due=2, cash_units=cash,
            free_hours=free_hours, currency_unit=currency,
        ),
    )


def set_household_cash(session, cash):
    world = session.world()
    world.actor_state["A"]["cash"] = cash
    session.product._checkpoint(session.branch_id, world.clock, world)


def household_cash(session):
    return house.read_household(session)["resources"][1]["fields"]["cash"]


def parent_cash(session):
    return read_parent_material(
        session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"]


def main():
    local = HERE / ".local-data" / "hostile"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    try:
        run_hostile(local)
    finally:
        REPORT["elapsed_seconds"] = round(time.perf_counter() - STARTED, 3)
        REPORT["verdict"] = ("REVISE_EXACT_DEFECT"
                             if REPORT["defects"] else "ACCEPT_SCOPED")
        (HERE / ".local-data" / "hostile_report.json").write_text(
            json.dumps(REPORT, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print("HOSTILE_DEFECTS", json.dumps(REPORT["defects"], sort_keys=True))
    return 1 if REPORT["defects"] else 0


def run_hostile(local):
    state = local / "state"
    owner = open_state(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        setup_parent(session)
        mo.establish_market_inventory(session)
        holder = session.world().actor_state["A"]["actor_id"]

        # G1/G2 normal path: actual first readers over real state.
        base_household = house.read_household(session)
        base_dwelling = house.read_dwelling(session)
        base_dwelling_doc = copy.deepcopy(
            session.world().resources[house.DWELLING_SLOT])
        base_feas = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("baseline feasibility admissible",
              base_feas["status"] == "ADMISSIBLE", base_feas["status"])
        base_market = mo.read_market_inventory(session)
        base_owned = mo.read_owned_objects(session)
        base_parent = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        check("baseline market stock", base_market["items"][0]["quantity"] == 2)
        check("baseline ownership absent", base_owned["status"] == "ABSENT")
        check("baseline parent cash", base_parent["material"]["cash_units"] == 100)

        # Hostile 1: currency mismatch at the purchase reader and at the
        # parent decision reader; no debit/stock/ownership may change.
        refusal(
            "wrong request currency refused at purchase reader",
            "PURCHASE_CURRENCY_MISMATCH",
            lambda: mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="g5:wrong-currency",
                owner_actor_id=holder,
                request={**house.DRUM_KIT_REQUESTS["junior"],
                         "currency_unit": "other_sourcefree_unit"}),
        )
        check("wrong currency left parent cash", parent_cash(session) == 100)
        check("wrong currency left stock",
              mo.read_market_inventory(session)["items"][0]["quantity"] == 2)
        check("wrong currency left ownership absent",
              mo.read_owned_objects(session)["status"] == "ABSENT")
        unknown_currency = house.material_feasibility(
            session, {**house.DRUM_KIT_REQUESTS["junior"],
                      "currency_unit": "other_sourcefree_unit"})
        check("unknown currency held by material reader",
              unknown_currency["status"] == "UNKNOWN"
              and "UNKNOWN_CURRENCY" in unknown_currency["unknowns"],
              unknown_currency["unknowns"])
        refusal(
            "wrong purchase owner refused",
            "PURCHASE_OWNER_UNKNOWN",
            lambda: mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="g5:wrong-owner",
                owner_actor_id="foreign-owner"),
        )
        refusal(
            "unknown parent refused",
            "PURCHASE_PARENT_UNAVAILABLE",
            lambda: mo.purchase_drum_kit(
                session, "missing-parent", operation_id="g5:missing-parent",
                owner_actor_id=holder),
        )
        check("wrong owner/parent left parent cash", parent_cash(session) == 100)
        check("wrong owner/parent left stock",
              mo.read_market_inventory(session)["items"][0]["quantity"] == 2)

        # Market root/branch tamper is refused and exact source restored.
        market_doc = copy.deepcopy(
            session.world().resources[mo.MARKET_SLOT])
        world = session.world()
        world.resources[mo.MARKET_SLOT]["branch"] = "foreign-branch"
        session.product._checkpoint(session.branch_id, world.clock, world)
        refusal("wrong market branch refused",
                "P6_MARKET_SOURCE_OR_ROOT_MISMATCH",
                lambda: mo.read_market_inventory(session))
        world = session.world()
        world.resources[mo.MARKET_SLOT] = market_doc
        session.product._checkpoint(session.branch_id, world.clock, world)
        check("market source restored exactly",
              mo.read_market_inventory(session)["source"] == base_market["source"])

        # Hostile 2: wallet separation. Parent adequate / household low:
        # material affordance is refused but the parent's own funds still buy.
        set_household_cash(session, 5)
        low_household = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("household-low feasibility refused",
              low_household["status"] == "REFUSED"
              and low_household["reasons"] == ["REFUSED_AFFORDABILITY"],
              low_household["reasons"])
        parent_low_probe = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        check("parent funds unaffected by household low",
              parent_low_probe["material"]["cash_units"] == 100)
        purchased_low_household = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="g5:parent-buys-low-household",
            owner_actor_id=holder)
        check("parent purchase admitted on parent funds",
              purchased_low_household["status"] == "ADMITTED")
        check("one purchase debits exactly 40 parent cash",
              parent_cash(session) == 60)
        check("one purchase decrements exactly one stock",
              mo.read_market_inventory(session)["items"][0]["quantity"] == 1)
        check("one purchase writes exactly one ownership row",
              mo.read_owned_objects(session)["totals"] == [{
                  "owner_actor_id": holder,
                  "object_id": "object:junior-drum-kit",
                  "kind": "junior_drum_kit", "quantity": 1}])
        check("household cash untouched by parent purchase",
              household_cash(session) == 5)
        replay = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="g5:parent-buys-low-household",
            owner_actor_id=holder)
        check("purchase replay is not a second debit", replay["status"] == "REPLAY")
        check("purchase replay left parent cash", parent_cash(session) == 60)
        check("purchase replay left stock",
              mo.read_market_inventory(session)["items"][0]["quantity"] == 1)
        check("purchase replay left one ownership row",
              len(mo.read_owned_objects(session)["objects"]) == 1)

        # Other direction: household adequate / parent low => parent decision
        # must refuse without touching household cash.
        set_household_cash(session, 55)
        fresh_parent = "TEST_ONLY_G5_REVIEW_PARENT_LOW"
        register_supporting_actor(
            session, alias="Q", actor_id=fresh_parent, role="parent",
            private_state={"motive": "g5-review-private-low"},
        )
        establish_parent_material(
            session, fresh_parent,
            fixture=parent_material_fixture(
                actor_id=fresh_parent, source_ref="sourcefree:parent:g5-low",
                employment_status="employed", wage_units_per_hour=5,
                debt_units=4, care_hours_due=2, cash_units=30,
                free_hours=8, currency_unit=CURRENCY),
        )
        parent_low = mo.purchase_drum_kit(
            session, fresh_parent, operation_id="g5:parent-low",
            owner_actor_id=holder)
        check("parent-low purchase refused",
              parent_low["status"] == "REFUSED"
              and parent_low["reasons"] == ["PURCHASE_INSUFFICIENT_FUNDS"],
              parent_low["reasons"])
        check("parent-low left household cash", household_cash(session) == 55)
        check("parent-low left stock",
              mo.read_market_inventory(session)["items"][0]["quantity"] == 1)
        check("parent-low left one ownership row",
              len(mo.read_owned_objects(session)["objects"]) == 1)

        # Hostile 3: unknown acoustics and prohibited tenancy are HELD/REFUSED,
        # never ADMISSIBLE; restore the original dwelling and exact identity.
        unknown = copy.deepcopy(house.dwelling_fixture(session))
        unknown["acoustics"]["max_indoor_loudness_db"] = "UNKNOWN"
        house.commit_dwelling(session, facts=unknown)
        unknown_feas = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("unknown acoustics held",
              unknown_feas["status"] == "UNKNOWN"
              and "UNKNOWN_ACOUSTICS" in unknown_feas["unknowns"],
              unknown_feas["unknowns"])
        prohibited = copy.deepcopy(house.dwelling_fixture(session))
        prohibited["home"]["tenancy"]["instrument_policy"] = "prohibited"
        house.commit_dwelling(session, facts=prohibited)
        prohibited_feas = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("prohibited tenancy refused",
              prohibited_feas["status"] == "REFUSED"
              and "REFUSED_TENANCY" in prohibited_feas["reasons"],
              prohibited_feas["reasons"])
        house.commit_dwelling(
            session, facts=house.dwelling_fixture(session))
        restored_dwelling = house.read_dwelling(session)
        check("dwelling source restored exactly",
              restored_dwelling["source"] == base_dwelling["source"])
        check("dwelling content restored exactly",
              all(restored_dwelling[key] == base_dwelling[key]
                  for key in ("home", "space", "acoustics", "costs")),
              {"note": "a re-commit is a new dated fact; exact hash restore "
                       "uses the original document below"})
        restored_feas = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("baseline feasibility outcome restored exactly",
              (restored_feas["status"], restored_feas["reasons"],
               restored_feas["unknowns"], restored_feas["conditions"],
               restored_feas["dwelling"]["source"])
              == (base_feas["status"], base_feas["reasons"],
                  base_feas["unknowns"], base_feas["conditions"],
                  base_feas["dwelling"]["source"]))
        # Exact epoch/hash identity is restored by putting the original stored
        # document back unchanged; a legitimate re-commit is a new dated fact.
        world = session.world()
        world.resources[house.DWELLING_SLOT] = copy.deepcopy(base_dwelling_doc)
        session.product._checkpoint(session.branch_id, world.clock, world)
        check("original dwelling document hash restored exactly",
              house.read_dwelling(session)["material_hash"]
              == base_dwelling["material_hash"])

        # Hostile 4: root/source/actor binding in the actual household reader.
        stored_household = copy.deepcopy(
            session.world().resources[house.HOUSEHOLD_SLOT])
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT]["root"] = "0" * 64
        session.product._checkpoint(session.branch_id, world.clock, world)
        refusal(
            "wrong household root refused",
            "P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH",
            lambda: house.read_household(session))
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT] = stored_household
        session.product._checkpoint(session.branch_id, world.clock, world)
        forged_actor = copy.deepcopy(stored_household)
        forged_actor["owner"]["actor_id"] = "foreign-actor"
        forged_actor["source"] = __import__(
            "developmental_recursion.p2_owner", fromlist=["material_fact_source"]
        ).material_fact_source(forged_actor)
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT] = forged_actor
        session.product._checkpoint(session.branch_id, world.clock, world)
        refusal(
            "wrong household actor refused",
            "P6_HOUSEHOLD_OWNER_MISMATCH",
            lambda: house.read_household(session))
        world = session.world()
        world.resources[house.HOUSEHOLD_SLOT] = stored_household
        session.product._checkpoint(session.branch_id, world.clock, world)
        check("household restored exactly",
              house.read_household(session)["source"] == base_household["source"])

        # Hostile 5: changed legitimate objective input (space) changes typed
        # feasibility; exact restore returns the exact same identity document.
        tight = copy.deepcopy(house.dwelling_fixture(session))
        tight["space"]["floor_area_m2"] = 1.0
        house.commit_dwelling(session, facts=tight)
        tight_feas = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("changed space changes feasibility",
              tight_feas["status"] == "REFUSED"
              and "REFUSED_SPACE" in tight_feas["reasons"],
              tight_feas["reasons"])
        world = session.world()
        world.resources[house.DWELLING_SLOT] = copy.deepcopy(base_dwelling_doc)
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        check("changed legitimate input exact restore", restored == base_feas,
              {"changed_source": tight_feas["dwelling"]["source"][:12],
               "restored_source": restored["dwelling"]["source"][:12]})

        # Hostile 6: period boundaries, midperiod split and as-of currentness.
        boundary_before = hp.read_material_period(session, "2026-06-30")
        boundary_at = hp.read_material_period(session, "2026-07-01")
        check("period boundary before is h1",
              boundary_before["period"]["period_id"] == "period:2026-h1")
        check("period boundary at is h2",
              boundary_at["period"]["period_id"] == "period:2026-h2")
        s14 = hp.read_material_period(session, "2026-03-14")
        s15 = hp.read_material_period(session, "2026-03-15")
        check("midperiod split old term",
              s14["employment"]["term_id"] == "employment:workshop-cooperative")
        check("midperiod split new term",
              s15["employment"]["term_id"] == "employment:civic-works")
        refusal("outside plan as-of refused", "P6_PERIOD_OUTSIDE_PLAN",
                lambda: hp.read_material_period(session, "2027-01-01"))
        to_boundary = hp.materialize_to(session, "2026-07-01")
        check("materialize to exact boundary",
              to_boundary["status"] == "MATERIALIZED")
        check("h1 complete at boundary",
              hp.period_progress(session, "period:2026-h1")["status"] == "COMPLETE")
        check("h2 before at boundary",
              hp.period_progress(session, "period:2026-h2")["status"] == "BEFORE")
        replay_period = hp.materialize_to(session, "2026-07-01")
        check("period replay does not duplicate state",
              replay_period["status"] == "ALREADY_CURRENT"
              and replay_period["produced_states"] == 0,
              {"status": replay_period["status"],
               "produced": replay_period["produced_states"]})
        rental = rr.apply_household_rent(
            session, operation_id="g5:rent:1", period_id="period:2026-h1")
        check("rent admitted once", rental["status"] == "ADMITTED")
        check("rent debits exactly one month", rental["household_cash_after"]
              == rental["household_cash_before"] - 12)
        after_rent_cash = household_cash(session)
        duplicate_rent = rr.apply_household_rent(
            session, operation_id="g5:rent:1", period_id="period:2026-h1")
        check("rent replay not a second debit",
              duplicate_rent["status"] == "REPLAY")
        check("rent replay cash unchanged", household_cash(session) == after_rent_cash)
        refusal("same period second rent operation refused",
                "B05_RENT_ALREADY_RECORDED",
                lambda: rr.apply_household_rent(
                    session, operation_id="g5:rent:2",
                    period_id="period:2026-h1"))
        check("second rent attempt cash unchanged",
              household_cash(session) == after_rent_cash)

        # Hostile 7: forged/partial purchase evidence. Remove the ownership row
        # while keeping the admitted P2_PARENT_PURCHASE receipt.
        world = session.world()
        owned_doc = copy.deepcopy(world.resources[mo.OWNED_SLOT])
        owned_doc["objects"] = []
        owned_doc["source"] = mo.material_fact_source(owned_doc)
        world.resources[mo.OWNED_SLOT] = owned_doc
        session.product._checkpoint(session.branch_id, world.clock, world)
        refusal("partial purchase evidence refused",
                "PURCHASE_READ_STALE",
                lambda: mo.read_purchase(
                    session, PARENT_ID, "g5:parent-buys-low-household",
                    as_actor=PARENT_ID))
        # Restore real ownership document exactly from the replay receipt.
        real_receipt = [row for row in session.product.store.episodes(
            session.branch_id)
            if row.get("kind") == mo.PURCHASE_KIND
            and (row.get("body") or {}).get("operation_id")
            == "g5:parent-buys-low-household"][0]["body"]["receipt"]
        world = session.world()
        world.resources[mo.OWNED_SLOT] = {
            "schema": mo.OWNED_SCHEMA, "grade": mo.FIXTURE_GRADE,
            "objects": [{
                "acquisition_id": "g5:parent-buys-low-household",
                "object_id": real_receipt["object_id"],
                "kind": real_receipt["kind"],
                "owner_actor_id": real_receipt["owner_actor_id"],
                "quantity": 1,
                "market_source": real_receipt["market_source_before"],
                "purchase_source": real_receipt["purchase_source"],
                "currency_unit": real_receipt["currency_unit"],
                "unit_price": real_receipt["unit_price"],
            }],
            "root": session.read_root()["root_hash"],
            "branch": session.branch_id, "epoch": session.clock(),
        }
        world.resources[mo.OWNED_SLOT]["source"] = mo.material_fact_source(
            world.resources[mo.OWNED_SLOT])
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored_read = mo.read_purchase(
            session, PARENT_ID, "g5:parent-buys-low-household",
            as_actor=PARENT_ID)
        check("restored ownership reads", restored_read["status"] == "READ")
        check("restored ownership quantity",
              restored_read["owned_totals"][0]["quantity"] == 1)

        final_parent_cash = parent_cash(session)
        final_household_cash = household_cash(session)

        # Hostile 8 (novel): a forged ADMITTED P2_PARENT_PURCHASE episode with a
        # foreign root/branch, appended through the actual C12 store API with a
        # coherent ownership row. If read_purchase accepts it, that is a real
        # first-reader source/operation binding defect, not a fixture error.
        alias = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["alias"]
        original = next(row for row in session.product.store.episodes(
            session.branch_id)
            if row.get("kind") == mo.PURCHASE_KIND
            and (row.get("body") or {}).get("operation_id")
            == "g5:parent-buys-low-household")
        forged_body = copy.deepcopy(original["body"])
        forged_receipt = forged_body["receipt"]
        forged_op = "g5:forged-foreign-root"
        forged_body["operation_id"] = forged_op
        forged_receipt["operation_id"] = forged_op
        forged_receipt["root"] = "f" * 64
        forged_receipt["branch"] = "foreign-branch"
        forged_purchase_source = digest({
            "schema": mo.PURCHASE_RECEIPT_SCHEMA,
            "operation_id": forged_op,
            "parent_id": PARENT_ID,
            "owner_actor_id": forged_receipt["owner_actor_id"],
            "object_id": forged_receipt["object_id"],
            "unit_price": forged_receipt["unit_price"],
            "market_source": forged_receipt["market_source_before"],
            "parent_before": forged_receipt["parent_material_source_before"],
            "parent_after": forged_receipt["parent_material_source_after"],
        })
        forged_receipt["purchase_source"] = forged_purchase_source
        forged_receipt["owned_source_before"] = forged_receipt["owned_source_after"]
        world = session.world()
        forged_owned = copy.deepcopy(world.resources[mo.OWNED_SLOT])
        forged_owned["objects"].append({
            "acquisition_id": forged_op,
            "object_id": forged_receipt["object_id"],
            "kind": forged_receipt["kind"],
            "owner_actor_id": forged_receipt["owner_actor_id"],
            "quantity": 1,
            "market_source": forged_receipt["market_source_before"],
            "purchase_source": forged_purchase_source,
            "currency_unit": forged_receipt["currency_unit"],
            "unit_price": forged_receipt["unit_price"],
        })
        forged_owned["source"] = mo.material_fact_source(forged_owned)
        world.resources[mo.OWNED_SLOT] = forged_owned
        session.product._checkpoint(session.branch_id, world.clock, world)
        session.product.store.append_episode(
            session.branch_id, actor_id=alias, kind=mo.PURCHASE_KIND,
            clock=session.clock(), body=forged_body)
        try:
            forged_read = mo.read_purchase(
                session, PARENT_ID, forged_op, as_actor=PARENT_ID)
            accepted = forged_read["status"] == "READ"
        except RecursionRefusal as exc:
            accepted = False
            forged_read = {"status": "REFUSED", "error": str(exc)}
        REPORT["defects"].append({
            "id": "G5-B04-RECEIPT-FOREIGN-ROOT",
            "actual": ("read_purchase accepted forged ADMITTED receipt "
                       "with root=" + forged_receipt["root"][:12]
                       + " and branch=" + forged_receipt["branch"])
                      if accepted else "typed refusal " + str(forged_read),
            "expected": "typed refusal binding receipt root/branch/parent to "
                        "the current session and actual B04 operation",
            "first_reader": "material_operations.read_purchase",
            "source_cause": "read_purchase validates acquisition fields but "
                            "never compares the nested receipt root/branch/"
                            "parent_id to the current session, while C02 "
                            "_purchase_history_source does check them",
            "suggested_owner_fix": "B04 owner adds receipt root/branch/"
                                   "parent_id equality before returning READ",
            "accepted": accepted,
        })
        note_check("forged foreign-root receipt refused", not accepted,
                   {"accepted": accepted, "status": forged_read["status"]})
        refusal(
            "C02 history rejects the same forged receipt",
            "PARENT_MATERIAL_HISTORY_MISMATCH",
            lambda: read_parent_history(
                session, PARENT_ID, as_actor=PARENT_ID),
        )

        # Hostile 9 (novel): forged ADMITTED rent evidence, appended through the
        # actual C12 store API. Cash is unchanged; only the receipt provenance
        # is foreign. The B05 obligation reader should bind it or refuse.
        rent_original = next(
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == rr.RENT_KIND
            and (row.get("body") or {}).get("operation_id") == "g5:rent:1")
        rent_body = copy.deepcopy(rent_original["body"])
        rent_receipt = rent_body["receipt"]
        rent_op = "g5:forged-rent-foreign-root"
        current_cash = household_cash(session)
        rent_body["operation_id"] = rent_op
        rent_receipt["operation_id"] = rent_op
        rent_receipt["root"] = "e" * 64
        rent_receipt["branch"] = "foreign-branch"
        rent_receipt["household_cash_before"] = current_cash + 12
        rent_receipt["household_cash_after"] = current_cash
        rent_receipt["monthly_rent"] = 12
        session.product.store.append_episode(
            session.branch_id, actor_id="A", kind=rr.RENT_KIND,
            clock=session.clock(), body=rent_body)
        try:
            forged_rent = rr.read_household_obligation(session, rent_op)
            rent_accepted = forged_rent["status"] == "READ"
        except RecursionRefusal as exc:
            rent_accepted = False
            forged_rent = {"status": "REFUSED", "error": str(exc)}
        REPORT["defects"].append({
            "id": "G5-B05-RENT-RECEIPT-FOREIGN-ROOT",
            "actual": ("read_household_obligation accepted forged ADMITTED "
                       "rent receipt with root=" + rent_receipt["root"][:12]
                       + " and branch=" + rent_receipt["branch"])
                      if rent_accepted else "typed refusal " + str(forged_rent),
            "expected": "typed refusal binding receipt root/branch and exact "
                        "rent operation/debit to the current session",
            "first_reader": "rolling_reproduction.read_household_obligation",
            "source_cause": "the B05 reader checks sources and arithmetic but "
                            "not receipt root/branch, and does not require the "
                            "receipt to correspond to a single actual rent "
                            "operation for the period",
            "suggested_owner_fix": "B05 owner adds receipt root/branch and "
                                   "period-operation binding before READ",
            "accepted": rent_accepted,
        })
        note_check("forged foreign-root rent refused", not rent_accepted,
                   {"accepted": rent_accepted, "status": forged_rent["status"]})
        check("forged rent did not change household cash",
              household_cash(session) == current_cash)

        REPORT["final"] = {
            "root": session.read_root()["root_hash"],
            "branch": session.branch_id,
            "clock": session.clock(),
            "parent_cash": final_parent_cash,
            "household_cash": final_household_cash,
            "market_source": mo.read_market_inventory(session)["source"],
            "owned_source": mo.read_owned_objects(session)["source"],
            "episode_count": len(session.product.store.episodes(session.branch_id)),
        }
        local.joinpath("final.json").write_text(
            json.dumps(REPORT["final"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8")
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
