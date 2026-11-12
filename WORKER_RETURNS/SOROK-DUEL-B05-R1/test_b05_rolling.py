"""B05 sourcefree proof: recurring rent + parent work + B04 purchase across periods."""
from __future__ import annotations

from argparse import Namespace
import copy
import json
from pathlib import Path
import subprocess
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
import material_operations as mo  # noqa: E402
import rolling_reproduction as rr  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material,
    parent_feasible_actions,
    parent_material_fixture,
    read_parent_material,
    record_parent_activity,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_B05_PARENT"
PARENT_ALIAS = "P"


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def register_and_establish(session):
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": "b05-private"},
    )
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(
            actor_id=PARENT_ID, source_ref="sourcefree:parent:b05",
            employment_status="employed", wage_units_per_hour=5,
            debt_units=4, care_hours_due=2, cash_units=60, free_hours=8,
        ),
    )


def holder_id(session):
    return session.world().actor_state["A"]["actor_id"]


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def test_recurring_rent_parent_work_and_purchase_change_later_inputs(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        register_and_establish(session)
        mo.establish_market_inventory(session)
        holder = holder_id(session)
        p3_head = owner.store.head()
        baseline_household = house.read_household(session)
        baseline_dwelling = house.read_dwelling(session)
        baseline_junior = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        assert baseline_household["resources"][1]["fields"]["cash"] == 55
        assert baseline_junior["status"] == "ADMISSIBLE"

        period1 = hp.materialize_to(session, "2026-07-01")
        assert period1["status"] == "MATERIALIZED"
        assert hp.period_progress(session, "period:2026-h1")["status"] == "COMPLETE"
        rent1 = rr.apply_household_rent(
            session, operation_id="b05:rent:1", period_id="period:2026-h1")
        assert rent1["status"] == "ADMITTED"
        assert rent1["household_cash_before"] == 55
        assert rent1["household_cash_after"] == 43
        assert rent1["period_status"] == "COMPLETE"
        assert rent1["scheduled_participation"] == "NOT_PERFORMED"
        assert rent1["event_effect"] == "NONE"
        assert rent1["public_event"] == "NOT_EMITTED"
        assert rent1["household_document_source"] == baseline_household["source"]
        assert rent1["dwelling_source"] == baseline_dwelling["source"]
        assert house.read_dwelling(session)["source"] == baseline_dwelling["source"]
        after_rent1 = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        assert after_rent1["status"] == "REFUSED"
        assert after_rent1["reasons"] == ["REFUSED_AFFORDABILITY"]
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 60

        work1 = record_parent_activity(
            session, PARENT_ID, operation_id="b05:work:1",
            activity="PAID_WORK", hours=2)
        assert work1["status"] == "ADMITTED"
        parent1 = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        assert parent1["material"]["cash_units"] == 70
        assert parent1["material"]["free_hours"] == 6
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 43
        purchase1 = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b05:buy:1",
            owner_actor_id=holder)
        assert purchase1["status"] == "ADMITTED"
        assert purchase1["parent_cash_before"] == 70
        assert purchase1["parent_cash_after"] == 30
        assert purchase1["parent_free_hours_after"] == 5
        assert purchase1["period"]["period_id"] == "period:2026-h2"
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 43
        assert house.read_dwelling(session)["source"] == baseline_dwelling["source"]
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 1
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 1
        with pytest.raises(RecursionRefusal, match="PARENT_MATERIAL_HISTORY_MISMATCH"):
            read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        with pytest.raises(RecursionRefusal, match="PARENT_MATERIAL_HISTORY_MISMATCH"):
            parent_feasible_actions(session, PARENT_ID, as_actor=PARENT_ID)
        purchase_read = mo.read_purchase(
            session, PARENT_ID, "b05:buy:1", as_actor=PARENT_ID)
        assert purchase_read["status"] == "READ"
        assert purchase_read["parent_material_status"] == (
            "REFUSED:PARENT_MATERIAL_HISTORY_MISMATCH")
        assert purchase_read["purchase_history_hook"] == (
            "C02_PARENT_HISTORY_KIND_PENDING")
        assert purchase_read["owned_totals"][0]["quantity"] == 1
        with pytest.raises(RecursionRefusal, match="PURCHASE_PARENT_UNAVAILABLE"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b05:buy:2",
                owner_actor_id=holder)
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 1
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 1

        period2 = hp.materialize_to(session, "2027-01-01")
        assert period2["status"] == "MATERIALIZED"
        assert hp.period_progress(session, "period:2026-h2")["status"] == "COMPLETE"
        rent2 = rr.apply_household_rent(
            session, operation_id="b05:rent:2", period_id="period:2026-h2")
        assert rent2["status"] == "ADMITTED"
        assert rent2["household_cash_before"] == 43
        assert rent2["household_cash_after"] == 31
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 31
        after_rent2 = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        assert after_rent2["status"] == "REFUSED"
        assert after_rent2["reasons"] == ["REFUSED_AFFORDABILITY"]
        assert owner.store.head() == p3_head

        april = hp.read_material_period(session, "2026-04-01")
        august = hp.read_material_period(session, "2026-08-01")
        assert april["as_of_relation"] == "PAST"
        assert april["employment"]["term_id"] == "employment:civic-works"
        assert april["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
        assert august["as_of_relation"] == "PAST"
        assert august["employment"]["term_id"] == "employment:civic-works"
        assert august["interval_status_detail"] == "MATERIALIZED_RETROSPECTIVELY"
        assert owner.store.head() == p3_head

        rent1_read = rr.read_household_obligation(session, "b05:rent:1")
        rent2_read = rr.read_household_obligation(session, "b05:rent:2")
        assert rent1_read["status"] == "READ"
        assert rent1_read["receipt"]["status"] == "ADMITTED"
        assert rent2_read["receipt"]["status"] == "ADMITTED"
        assert rent1_read["household_cash"] == 31
        with pytest.raises(RecursionRefusal, match="B05_RENT_ALREADY_RECORDED"):
            rr.apply_household_rent(
                session, operation_id="b05:rent:1-duplicate",
                period_id="period:2026-h1")
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 31
        replay = rr.apply_household_rent(
            session, operation_id="b05:rent:1", period_id="period:2026-h1")
        assert replay["status"] == "REPLAY"
        assert house.read_household(session)["resources"][1]["fields"]["cash"] == 31

        stored_dwelling = copy.deepcopy(session.world().resources[house.DWELLING_SLOT])
        world = session.world()
        world.resources.pop(house.DWELLING_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            rr.read_household_obligation(session, "b05:rent:1")
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            house.material_feasibility(session, house.DRUM_KIT_REQUESTS["junior"])
        world = session.world()
        world.resources[house.DWELLING_SLOT] = stored_dwelling
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert rr.read_household_obligation(session, "b05:rent:1") == rent1_read
        assert house.read_dwelling(session)["source"] == baseline_dwelling["source"]

        baseline_cold = {
            "rent1": rent1_read,
            "rent2": rent2_read,
            "purchase": mo.read_purchase(
                session, PARENT_ID, "b05:buy:1", as_actor=PARENT_ID),
            "owned": mo.read_owned_objects(session),
            "market": mo.read_market_inventory(session),
            "household": house.read_household(session),
            "dwelling": house.read_dwelling(session),
            "feasibility": house.material_feasibility(
                session, house.DRUM_KIT_REQUESTS["junior"]),
            "period1": hp.period_progress(session, "period:2026-h1"),
            "period2": hp.period_progress(session, "period:2026-h2"),
            "p3_head": p3_head,
            "counts": counts(session),
        }
    finally:
        owner.close()

    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "sys.path.insert(0, sys.argv[2])\n"
        "sys.path.insert(0, sys.argv[3])\n"
        "sys.path.insert(0, sys.argv[4])\n"
        "sys.path.insert(0, sys.argv[5])\n"
        "sys.path.insert(0, sys.argv[6])\n"
        "import run_p6\n"
        "import house\n"
        "import material_operations as mo\n"
        "import rolling_reproduction as rr\n"
        "import historical_period as hp\n"
        "state = Path(sys.argv[7])\n"
        "parent = sys.argv[8]\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    print(json.dumps({\n"
        "        'rent1': rr.read_household_obligation(session, 'b05:rent:1'),\n"
        "        'rent2': rr.read_household_obligation(session, 'b05:rent:2'),\n"
        "        'purchase': mo.read_purchase(session, parent, 'b05:buy:1', as_actor=parent),\n"
        "        'owned': mo.read_owned_objects(session),\n"
        "        'market': mo.read_market_inventory(session),\n"
        "        'household': house.read_household(session),\n"
        "        'dwelling': house.read_dwelling(session),\n"
        "        'feasibility': house.material_feasibility(\n"
        "            session, house.DRUM_KIT_REQUESTS['junior']),\n"
        "        'period1': hp.period_progress(session, 'period:2026-h1'),\n"
        "        'period2': hp.period_progress(session, 'period:2026-h2'),\n"
        "        'p3_head': owner.store.head(),\n"
        "        'counts': {\n"
        "            'episodes': len(session.product.store.episodes(session.branch_id)),\n"
        "            'checkpoints': len(session.product.store.checkpoints(session.branch_id)),\n"
        "            'world_events': len(session.product.store.world_events(session.branch_id)),\n"
        "            'perceptions': len(session.product.store.perceptions(session.branch_id)),\n"
        "        },\n"
        "    }, sort_keys=True))\n"
        "finally:\n"
        "    owner.close()\n"
    )
    cold = subprocess.run(
        [sys.executable, "-B", "-c", script, str(B05), str(B04), str(B02),
         str(P6), str(ENGINE), str(P3), str(state), PARENT_ID],
        capture_output=True, text=True, timeout=180,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    for key in ("rent1", "rent2", "purchase", "owned", "market", "household",
                "dwelling", "feasibility", "period1", "period2", "p3_head",
                "counts"):
        assert reopened[key] == baseline_cold[key], key
