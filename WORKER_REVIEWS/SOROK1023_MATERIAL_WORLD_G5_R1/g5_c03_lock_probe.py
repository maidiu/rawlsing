"""SOROK #1023 independent G5 read-only C03/B04 lock-order integration.

No product edit. The actual parent-decision caller is executed once with thin
instrumentation around the real lock context managers to record acquisition
order. The underlying locks are still the accepted B04/C03 locks.
"""
from __future__ import annotations

import json
import shutil
import sys
import time
from argparse import Namespace
from contextlib import contextmanager
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

PARENT_ID = "TEST_ONLY_G5_LOCK_PARENT"


def main() -> int:
    import historical_period as hp
    import material_operations as mo
    import run_p6
    from developmental_recursion import parent_decision as pd
    from developmental_recursion.parent_activity import (
        establish_parent_material, parent_material_fixture,
    )
    from developmental_recursion.supporting_actor import register_supporting_actor

    local = HERE / ".local-data" / "lock"
    if local.exists():
        shutil.rmtree(local)
    local.mkdir(parents=True)
    started = time.perf_counter()
    order = []
    report = {"schema": "SOROK1023_G5_C03_LOCK_REPORT@1"}
    original_purchase = mo._purchase_lock
    original_parent = pd._parent_write_lock

    @contextmanager
    def record_purchase(session):
        order.append("purchase_lock")
        with original_purchase(session):
            yield

    @contextmanager
    def record_parent(session):
        order.append("parent_lock")
        with original_parent(session):
            yield

    try:
        state = local / "state"
        run_p6.experience(state, Namespace(command="new", request_id=None))
        owner = run_p6.open_owner(state / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            hp.establish_period_plan(session)
            hp.materialize_to(session, "2026-02-01")
            register_supporting_actor(
                session, alias="P", actor_id=PARENT_ID, role="parent",
                private_state={"motive": "g5-lock-private"},
            )
            establish_parent_material(
                session, PARENT_ID,
                fixture=parent_material_fixture(
                    actor_id=PARENT_ID, source_ref="sourcefree:parent:g5-lock",
                    employment_status="employed", wage_units_per_hour=5,
                    debt_units=4, care_hours_due=2, cash_units=100,
                    free_hours=8, currency_unit=mo.CURRENCY),
            )
            mo.establish_market_inventory(session)
            holder = session.world().actor_state["A"]["actor_id"]
            request = pd.parent_request_fixture(
                kind="junior", owner_actor_id=PARENT_ID)
            admission = pd.admit_parent_decision(
                session, PARENT_ID, operation_id="g5:lock:decision",
                request=request, as_actor=PARENT_ID)
            mo._purchase_lock = record_purchase
            pd._parent_write_lock = record_parent
            action = pd.perform_parent_decision(
                session, PARENT_ID, decision_id="g5:lock:decision",
                as_actor=PARENT_ID)
            report.update({
                "lock_order": list(order),
                "decision_action": admission["decision"]["action"],
                "decision_status": admission["decision"]["status"],
                "action_status": action["status"],
                "performed": action["performed"],
                "physical_admission": action["physical_admission"],
                "purchase_status": (action.get("purchase") or {}).get("status"),
                "parent_cash_after": (action.get("purchase") or {}).get(
                    "parent_cash_after"),
                "purchase_period": ((action.get("purchase") or {}).get(
                    "period") or {}).get("period_id"),
                "market_quantity": mo.read_market_inventory(
                    session)["items"][0]["quantity"],
                "owned_totals": mo.read_owned_objects(session)["totals"],
                "holder": holder,
            })
            report["ok"] = (
                order == ["purchase_lock", "parent_lock"]
                and report["decision_action"] == "PURCHASE"
                and report["action_status"] == "PERFORMED"
                and report["performed"] is True
                and report["purchase_status"] == "ADMITTED"
                and report["parent_cash_after"] == 60
                and report["purchase_period"] == "period:2026-h1"
                and report["market_quantity"] == 1
                and report["owned_totals"][0]["quantity"] == 1
            )
        finally:
            owner.close()
    finally:
        mo._purchase_lock = original_purchase
        pd._parent_write_lock = original_parent
        report["elapsed_seconds"] = round(time.perf_counter() - started, 3)
        (HERE / ".local-data" / "lock_report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        shutil.rmtree(local, ignore_errors=True)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
