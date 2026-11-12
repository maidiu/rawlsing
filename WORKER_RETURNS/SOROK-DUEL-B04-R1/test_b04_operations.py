"""B04 sourcefree proof: parent-funded stock purchase, refusal and later reader."""
from __future__ import annotations

from argparse import Namespace
import copy
import json
from pathlib import Path
import subprocess
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
import house  # noqa: E402
import material_operations as mo  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    commit_parent_circumstances,
    establish_parent_material,
    parent_feasible_actions,
    parent_material_fixture,
    read_parent_material,
)
from developmental_recursion.supporting_actor import register_supporting_actor  # noqa: E402

PARENT_ID = "TEST_ONLY_B04_PARENT"
PARENT_ALIAS = "P"
SECRET = "b04-private-motive-do-not-expose"


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def register_and_establish(session, *, cash=120, free_hours=8):
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": SECRET},
    )
    fixture = parent_material_fixture(
        actor_id=PARENT_ID, source_ref="sourcefree:parent:b04",
        employment_status="employed", wage_units_per_hour=5,
        debt_units=4, care_hours_due=2, cash_units=cash,
        free_hours=free_hours,
    )
    return establish_parent_material(session, PARENT_ID, fixture=fixture)


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


def test_purchase_stock_ownership_parent_feasibility_and_refusals(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        register_and_establish(session)
        mo.establish_market_inventory(session)
        holder = holder_id(session)
        household_before = house.read_household(session)
        dwelling_before = house.read_dwelling(session)
        parent_before = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        market_before = mo.read_market_inventory(session)
        assert mo.read_owned_objects(session)["status"] == "ABSENT"
        baseline_feasibility = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])

        first = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:purchase:1",
            owner_actor_id=holder)
        assert first["status"] == "ADMITTED"
        assert first["buyer"] == "REGISTERED_PARENT"
        assert first["parent_cash_before"] == 120
        assert first["parent_cash_after"] == 80
        assert first["parent_free_hours_before"] == 8
        assert first["parent_free_hours_after"] == 7
        assert first["object_id"] == "object:junior-drum-kit"
        assert first["quantity"] == 1
        assert first["unit_price"] == 40
        assert first["event_effect"] == "NONE"
        assert first["public_event"] == "NOT_EMITTED_HELD_PAIR3_VOCABULARY"
        assert first["possession"] == "OBJECT_STOCK_AND_OWNERSHIP_WRITTEN"
        assert first["period"]["status"] == "B02_MATERIAL_PERIOD_READ"
        assert first["period"]["period_id"] == "period:2026-h1"
        assert first["period"]["as_of_date"] == "2026-02-01"
        assert first["household_source"] == household_before["source"]
        assert first["dwelling_source"] == dwelling_before["source"]
        assert first["b03_feasibility"]["status"] == "ADMISSIBLE"
        market_after = mo.read_market_inventory(session)
        owned_after = mo.read_owned_objects(session)
        assert market_after["items"][0]["quantity"] == 1
        assert owned_after["status"] == "READ"
        assert owned_after["totals"] == [{
            "owner_actor_id": holder, "object_id": "object:junior-drum-kit",
            "kind": "junior_drum_kit", "quantity": 1,
        }]
        assert house.read_household(session)["source"] == household_before["source"]
        assert house.read_household(session)["material_hash"] == household_before["material_hash"]
        assert house.read_dwelling(session)["source"] == dwelling_before["source"]
        assert house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"]) == baseline_feasibility
        options_after = {row["activity"]: row for row in parent_feasible_actions(
            session, PARENT_ID, as_actor=PARENT_ID)["options"]}
        assert options_after["PAID_WORK"]["status"] == "ADMISSIBLE"
        assert options_after["PAY_DEBT"]["status"] == "ADMISSIBLE"
        read = mo.read_purchase(
            session, PARENT_ID, "b04:purchase:1", as_actor=PARENT_ID)
        assert read["status"] == "READ"
        assert read["historical"] is False
        assert read["receipt"]["status"] == "ADMITTED"
        assert read["owned_totals"] == owned_after["totals"]
        assert SECRET not in json.dumps(first)
        assert SECRET not in json.dumps(read)

        before_replay = counts(session)
        replay = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:purchase:1",
            owner_actor_id=holder)
        assert replay["status"] == "REPLAY"
        assert counts(session) == before_replay
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 80

        with pytest.raises(RecursionRefusal, match="PURCHASE_PRICE_MISMATCH"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:bad-price",
                owner_actor_id=holder,
                request={**house.DRUM_KIT_REQUESTS["junior"],
                         "purchase_price": 41})

        commit_parent_circumstances(
            session, PARENT_ID, operation_id="b04:no-time",
            changes={"free_hours": 0}, source_ref="sourcefree:parent:no-time")
        no_time = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:no-time-purchase",
            owner_actor_id=holder)
        assert no_time["status"] == "REFUSED"
        assert no_time["reasons"] == ["PURCHASE_TIME_UNAVAILABLE"]
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 80
        commit_parent_circumstances(
            session, PARENT_ID, operation_id="b04:time-restored",
            changes={"free_hours": 7}, source_ref="sourcefree:parent:time-restored")

        second = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:purchase:2",
            owner_actor_id=holder)
        assert second["status"] == "ADMITTED"
        assert second["parent_cash_after"] == 40
        assert second["parent_free_hours_after"] == 6
        assert mo.read_market_inventory(session)["items"][0]["quantity"] == 0
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2
        later_read = mo.read_purchase(
            session, PARENT_ID, "b04:purchase:1", as_actor=PARENT_ID)
        assert later_read["status"] == "READ"
        assert later_read["historical"] is True
        assert later_read["owned_totals"][0]["quantity"] == 2
        assert later_read["receipt"]["status"] == "ADMITTED"

        before_refusal = counts(session)
        stock_refusal = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:purchase:3",
            owner_actor_id=holder)
        assert stock_refusal["status"] == "REFUSED"
        assert stock_refusal["reasons"] == ["PURCHASE_STOCK_UNAVAILABLE"]
        assert stock_refusal["parent_material_source_before"] == (
            stock_refusal["parent_material_source_after"])
        assert stock_refusal["market_source_before"] == stock_refusal["market_source_after"]
        assert stock_refusal["owned_source_before"] == stock_refusal["owned_source_after"]
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 40
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2
        refuse_read = mo.read_purchase(
            session, PARENT_ID, "b04:purchase:3", as_actor=PARENT_ID)
        assert refuse_read["receipt"]["status"] == "REFUSED"
        assert refuse_read["receipt"]["reasons"] == ["PURCHASE_STOCK_UNAVAILABLE"]

        with pytest.raises(RecursionRefusal, match="PURCHASE_OWNER_UNKNOWN"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:bad-owner",
                owner_actor_id="foreign-owner")
        with pytest.raises(RecursionRefusal, match="PURCHASE_CURRENCY_MISMATCH"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:bad-currency",
                owner_actor_id=holder,
                request={**house.DRUM_KIT_REQUESTS["junior"],
                         "currency_unit": "other"})
        with pytest.raises(RecursionRefusal, match="PURCHASE_PARENT_UNAVAILABLE"):
            mo.purchase_drum_kit(
                session, "missing-parent", operation_id="b04:bad-parent",
                owner_actor_id=holder)
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 40
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2

        acoustic = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:acoustic",
            owner_actor_id=holder, request=house.DRUM_KIT_REQUESTS["acoustic"])
        assert acoustic["status"] == "REFUSED"
        assert acoustic["reasons"] == ["REFUSED_NOISE"]
        assert read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["material"]["cash_units"] == 40
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2

        grand = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:missing-object",
            owner_actor_id=holder,
            request={**house.DRUM_KIT_REQUESTS["junior"], "kind": "grand_piano"})
        assert grand["status"] == "REFUSED"
        assert grand["reasons"] == ["PURCHASE_STOCK_UNAVAILABLE"]
        assert mo.read_owned_objects(session)["totals"][0]["quantity"] == 2
        assert "grand_piano" not in json.dumps(mo.read_owned_objects(session))

    finally:
        owner.close()


def test_purchase_cold_restore_and_source_severance(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        hp.establish_period_plan(session)
        hp.materialize_to(session, "2026-02-01")
        register_and_establish(session, cash=60, free_hours=8)
        mo.establish_market_inventory(session)
        holder = holder_id(session)
        household = house.read_household(session)
        dwelling = house.read_dwelling(session)
        purchase = mo.purchase_drum_kit(
            session, PARENT_ID, operation_id="b04:cold:1",
            owner_actor_id=holder)
        assert purchase["status"] == "ADMITTED"
        baseline_owned = mo.read_owned_objects(session)
        baseline_market = mo.read_market_inventory(session)
        baseline_parent = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)
        baseline_household = house.read_household(session)
        baseline_dwelling = house.read_dwelling(session)
        baseline_read = mo.read_purchase(
            session, PARENT_ID, "b04:cold:1", as_actor=PARENT_ID)
        baseline_counts = counts(session)
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
        "import run_p6\n"
        "import house\n"
        "import material_operations as mo\n"
        "from developmental_recursion.parent_activity import read_parent_material\n"
        "state = Path(sys.argv[6])\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    print(json.dumps({\n"
        "        'purchase': mo.read_purchase(session, sys.argv[7], sys.argv[8], as_actor=sys.argv[7]),\n"
        "        'owned': mo.read_owned_objects(session),\n"
        "        'market': mo.read_market_inventory(session),\n"
        "        'parent': read_parent_material(session, sys.argv[7], as_actor=sys.argv[7]),\n"
        "        'household': house.read_household(session),\n"
        "        'dwelling': house.read_dwelling(session),\n"
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
        [sys.executable, "-B", "-c", script, str(B04), str(B02), str(P6),
         str(ENGINE), str(P3), str(state), PARENT_ID, "b04:cold:1"],
        capture_output=True, text=True, timeout=180,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    assert reopened["purchase"] == baseline_read
    assert reopened["owned"] == baseline_owned
    assert reopened["market"] == baseline_market
    assert reopened["parent"] == baseline_parent
    assert reopened["household"] == baseline_household
    assert reopened["dwelling"] == baseline_dwelling
    assert reopened["counts"] == baseline_counts

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        world = session.world()
        market_doc = copy.deepcopy(world.resources[mo.MARKET_SLOT])
        world.resources.pop(mo.MARKET_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_MARKET_ABSENT"):
            mo.read_market_inventory(session)
        with pytest.raises(RecursionRefusal, match="P6_MARKET_ABSENT"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:severed-market",
                owner_actor_id=holder_id(session))
        world = session.world()
        world.resources[mo.MARKET_SLOT] = market_doc
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert mo.read_market_inventory(session)["source"] == baseline_market["source"]
        assert mo.read_owned_objects(session) == baseline_owned

        market_doc = copy.deepcopy(session.world().resources[mo.MARKET_SLOT])
        world = session.world()
        world.resources[mo.MARKET_SLOT]["branch"] = "foreign-branch"
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_MARKET_SOURCE_OR_ROOT_MISMATCH"):
            mo.read_market_inventory(session)
        with pytest.raises(RecursionRefusal, match="P6_MARKET_SOURCE_OR_ROOT_MISMATCH"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:bad-market-branch",
                owner_actor_id=holder_id(session))
        world = session.world()
        world.resources[mo.MARKET_SLOT] = market_doc
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert mo.read_market_inventory(session)["source"] == baseline_market["source"]

        alias = read_parent_material(session, PARENT_ID, as_actor=PARENT_ID)["alias"]
        parent_doc = copy.deepcopy(session.world().actor_state[alias]["material"])
        world = session.world()
        world.actor_state[alias]["material"]["branch"] = "foreign-branch"
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="PURCHASE_PARENT_UNAVAILABLE"):
            mo.purchase_drum_kit(
                session, PARENT_ID, operation_id="b04:bad-parent-branch",
                owner_actor_id=holder_id(session))
        world = session.world()
        world.actor_state[alias]["material"] = parent_doc
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_parent_material(
            session, PARENT_ID, as_actor=PARENT_ID)["source"] == baseline_parent["source"]
    finally:
        owner.close()
