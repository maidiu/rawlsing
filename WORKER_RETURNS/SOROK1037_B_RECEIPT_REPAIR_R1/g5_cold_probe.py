"""SOROK #1023 independent G5 cold-process / no-duplicate proof.

Parent builds one bounded real-material state (two purchases across the B02
period boundary and one household rent), closes it, then a fresh child process
reopens the same sealed state and replays/duplicates the operations. Product
code is READONLY.
"""
from __future__ import annotations

import copy
import json
import shutil
import subprocess
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

PARENT_ID = "TEST_ONLY_G5_COLD_PARENT"
PARENT_ALIAS = "P"


def counts(session):
    store = session.product.store
    rows = store.episodes(session.branch_id)
    result = {"episodes": len(rows)}
    for kind in ("P2_PARENT_PURCHASE", "P2_HOUSEHOLD_RENT"):
        result[kind] = sum(1 for row in rows if row.get("kind") == kind)
    return result


def cold_main(state_path: str) -> int:
    import historical_period as hp
    import material_operations as mo
    import rolling_reproduction as rr
    import run_p6
    from developmental_recursion.contracts import RecursionRefusal
    from developmental_recursion.parent_activity import read_parent_material

    out = {"schema": "SOROK1023_G5_COLD_CHILD@1"}
    owner = run_p6.open_owner(Path(state_path) / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        head_before = dict(owner.store.head())
        purchase1 = mo.read_purchase(
            session, PARENT_ID, "g5:cold:purchase:1", as_actor=PARENT_ID)
        purchase2 = mo.read_purchase(
            session, PARENT_ID, "g5:cold:purchase:2", as_actor=PARENT_ID)
        rent = rr.read_household_obligation(session, "g5:cold:rent:1")
        material = read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)
        owned = mo.read_owned_objects(session)
        market = mo.read_market_inventory(session)
        out.update({
            "purchase1": {
                "status": purchase1["status"],
                "historical": purchase1["historical"],
                "receipt_status": purchase1["receipt"]["status"],
                "period_id": purchase1["receipt"]["period"]["period_id"],
                "parent_cash_after": purchase1["receipt"]["parent_cash_after"],
                "purchase_source": purchase1["receipt"]["purchase_source"],
                "owned_source_after": purchase1["receipt"]["owned_source_after"],
            },
            "purchase2": {
                "status": purchase2["status"],
                "historical": purchase2["historical"],
                "receipt_status": purchase2["receipt"]["status"],
                "period_id": purchase2["receipt"]["period"]["period_id"],
                "parent_cash_after": purchase2["receipt"]["parent_cash_after"],
                "purchase_source": purchase2["receipt"]["purchase_source"],
                "owned_source_after": purchase2["receipt"]["owned_source_after"],
            },
            "rent": {
                "status": rent["status"],
                "historical": rent["historical"],
                "receipt_status": rent["receipt"]["status"],
                "household_cash_before": rent["receipt"]["household_cash_before"],
                "household_cash_after": rent["receipt"]["household_cash_after"],
                "monthly_rent": rent["receipt"]["monthly_rent"],
            },
            "parent_cash": material["material"]["cash_units"],
            "parent_free_hours": material["material"]["free_hours"],
            "household_cash": rent["household_cash"],
            "owned_totals": owned["totals"],
            "owned_source": owned["source"],
            "market_source": market["source"],
            "market_quantity": market["items"][0]["quantity"],
            "counts": counts(session),
            "head": head_before,
        })
        # Replay and duplicate attacks in the fresh process.
        holder = session.world().actor_state["A"]["actor_id"]
        try:
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="g5:cold:purchase:1",
                owner_actor_id=holder)
            replay1 = "UNEXPECTED_REPLAY"
        except RecursionRefusal as exc:
            replay1 = "REFUSED:" + str(exc)
        replay2 = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="g5:cold:purchase:2",
            owner_actor_id=holder)['status']
        rent_replay = rr.apply_household_rent(
            session, operation_id="g5:cold:rent:1",
            period_id="period:2026-h1")
        try:
            rr.apply_household_rent(
                session, operation_id="g5:cold:rent:2",
                period_id="period:2026-h1")
            duplicate_rent = {"refused": False}
        except RecursionRefusal as exc:
            duplicate_rent = {"refused": True, "code": str(exc)}
        out.update({
            "replay1": replay1,
            "replay2": replay2,
            "rent_replay": rent_replay["status"],
            "duplicate_rent": duplicate_rent,
            "counts_after_replay": counts(session),
            "parent_cash_after_replay": read_parent_material(
                session, PARENT_ID, as_actor=PARENT_ID
            )["material"]["cash_units"],
            "household_cash_after_replay": rr.read_household_obligation(
                session, "g5:cold:rent:1")["household_cash"],
            "market_quantity_after_replay": mo.read_market_inventory(
                session)["items"][0]["quantity"],
            "owned_rows_after_replay": len(
                mo.read_owned_objects(session)["objects"]),
            "head_after": dict(owner.store.head()),
        })
        out["ok"] = (
            out["purchase1"]["receipt_status"] == "ADMITTED"
            and out["purchase2"]["receipt_status"] == "ADMITTED"
            and out["rent"]["receipt_status"] == "ADMITTED"
            and out["parent_cash"] == 20
            and out["parent_free_hours"] == 6
            and out["household_cash"] == 43
            and out["market_quantity"] == 0
            and out["owned_totals"][0]["quantity"] == 2
            and out["counts"]["P2_PARENT_PURCHASE"] == 2
            and out["counts"]["P2_HOUSEHOLD_RENT"] == 1
            and out["replay1"] == "REFUSED:PURCHASE_REPLAY_STALE"
            and out["replay2"] == "REPLAY"
            and out["rent_replay"] == "REPLAY"
            and out["duplicate_rent"].get("refused") is True
            and out["parent_cash_after_replay"] == 20
            and out["household_cash_after_replay"] == 43
            and out["market_quantity_after_replay"] == 0
            and out["owned_rows_after_replay"] == 2
            and out["head_after"] == out["head"]
            and out["counts_after_replay"] == out["counts"]
        )
    finally:
        owner.close()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out.get("ok") else 1


def parent_main() -> int:
    import historical_period as hp
    import house
    import material_operations as mo
    import rolling_reproduction as rr
    import run_p6
    from developmental_recursion.contracts import RecursionRefusal
    from developmental_recursion.parent_activity import (
        establish_parent_material, parent_material_fixture,
    )
    from developmental_recursion.supporting_actor import register_supporting_actor

    local = HERE / ".local-data" / "cold"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    state = local / "state"
    started = time.perf_counter()
    report = {"schema": "SOROK1023_G5_COLD_PARENT@1"}
    try:
        run_p6.experience(state, Namespace(command="new", request_id=None))
        owner = run_p6.open_owner(state / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            hp.establish_period_plan(session)
            register_supporting_actor(
                session, alias=PARENT_ALIAS, actor_id=PARENT_ID,
                role="parent", private_state={"motive": "g5-cold-private"},
            )
            establish_parent_material(
                session, PARENT_ID,
                fixture=parent_material_fixture(
                    actor_id=PARENT_ID, source_ref="sourcefree:parent:g5-cold",
                    employment_status="employed", wage_units_per_hour=5,
                    debt_units=4, care_hours_due=2, cash_units=100,
                    free_hours=8, currency_unit=mo.CURRENCY),
            )
            mo.establish_market_inventory(session)
            holder = session.world().actor_state["A"]["actor_id"]
            head = dict(owner.store.head())
            hp.materialize_to(session, "2026-02-01")
            purchase1 = mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="g5:cold:purchase:1",
                owner_actor_id=holder)
            before_failure = {
                "parent_cash": mo.read_purchase(
                    session, PARENT_ID, "g5:cold:purchase:1",
                    as_actor=PARENT_ID)["receipt"]["parent_cash_after"],
                "market": mo.read_market_inventory(session)["source"],
                "owned": mo.read_owned_objects(session)["source"],
            }
            try:
                mo.purchase_drum_kit(
                    session, PARENT_ID, operation_id="g5:cold:failed",
                    owner_actor_id=holder,
                    request={**house.DRUM_KIT_REQUESTS["junior"],
                             "currency_unit": "wrong_currency"})
                failure = "UNEXPECTED_ACCEPT"
            except RecursionRefusal as exc:
                failure = "REFUSED:" + str(exc)
            after_failure = {
                "parent_cash": mo.read_purchase(
                    session, PARENT_ID, "g5:cold:purchase:1",
                    as_actor=PARENT_ID)["receipt"]["parent_cash_after"],
                "market": mo.read_market_inventory(session)["source"],
                "owned": mo.read_owned_objects(session)["source"],
            }
            hp.materialize_to(session, "2026-07-01")
            purchase2 = mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="g5:cold:purchase:2",
                owner_actor_id=holder)
            rent = rr.apply_household_rent(
                session, operation_id="g5:cold:rent:1",
                period_id="period:2026-h1")
            report.update({
                "warm": {
                    "purchase1_period": purchase1["period"]["period_id"],
                    "purchase2_period": purchase2["period"]["period_id"],
                    "purchase1_cash": purchase1["parent_cash_after"],
                    "purchase2_cash": purchase2["parent_cash_after"],
                    "rent_status": rent["status"],
                    "rent_cash": rent["household_cash_after"],
                    "owned_source": mo.read_owned_objects(session)["source"],
                    "market_source": mo.read_market_inventory(session)["source"],
                    "counts": counts(session),
                    "head": head,
                    "failure": failure,
                    "failure_unchanged": before_failure == after_failure,
                }
            })
            if (purchase1["period"]["period_id"] != "period:2026-h1"
                    or purchase2["period"]["period_id"] != "period:2026-h2"
                    or purchase1["parent_cash_after"] != 60
                    or purchase2["parent_cash_after"] != 20
                    or rent["status"] != "ADMITTED"
                    or rent["household_cash_after"] != 43
                    or failure != "REFUSED:PURCHASE_CURRENCY_MISMATCH"
                    or before_failure != after_failure):
                report["warm_ok"] = False
                print(json.dumps(report, indent=2, sort_keys=True))
                return 1
            report["warm_ok"] = True
        finally:
            owner.close()
        child = subprocess.run(
            [sys.executable, str(Path(__file__)), "--cold", str(state)],
            capture_output=True, text=True, check=False,
        )
        report["child_exit"] = child.returncode
        report["child_stderr"] = child.stderr[-2000:]
        report["child"] = json.loads(child.stdout) if child.stdout.strip() else None
        report["ok"] = (
            child.returncode == 0
            and report["child"] is not None
            and report["child"].get("ok") is True
            and report["child"]["purchase1"]["period_id"] == "period:2026-h1"
            and report["child"]["purchase2"]["period_id"] == "period:2026-h2"
            and report["child"]["counts"]["P2_PARENT_PURCHASE"] == 2
            and report["child"]["counts"]["P2_HOUSEHOLD_RENT"] == 1
            and report["child"]["head_after"] == report["child"]["head"]
        )
    finally:
        report["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        (HERE / ".local-data" / "cold_report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--cold":
        raise SystemExit(cold_main(sys.argv[2]))
    raise SystemExit(parent_main())
