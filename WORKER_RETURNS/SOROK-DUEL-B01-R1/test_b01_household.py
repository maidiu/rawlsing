"""B01 sourcefree proof: world-owned household facts and parent-choice input."""
from __future__ import annotations

from argparse import Namespace
import copy
import inspect
import json
from pathlib import Path
import subprocess
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
ROOT = RETURNS.parent
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402
from developmental_recursion.p2_owner import write_material_fact  # noqa: E402
from p3.state_store import PsycheStore  # noqa: E402
import run_p6  # noqa: E402
from house import (  # noqa: E402
    HOUSEHOLD_SLOT,
    establish_household,
    parent_choice_input,
    read_household,
)

PROJECT = "b01:household:late"
MOTHER = "actor:mother"
REGISTRY_HASH = "registry:b01:test-only"
STORE_SOURCE_HASH = "source:b01:kitchen-mediator"
RULE = {"rule_id": "rule.b01.home", "rule_version": "1", "rule_hash": "rule:b01:home:1"}
GRADE = "SOURCEFREE_TEST_ONLY"


def run_cmd(state, command, **args):
    return run_p6.experience(
        state, Namespace(command=command, request_id=None, **args)
    )


def open_owner(state):
    return run_p6.open_owner(state / "actual-p2")


def counts(session):
    store = session.product.store
    return {
        "episodes": len(store.episodes(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
    }


def state_doc(binding, clock, tag):
    return {
        **binding,
        "clock": clock,
        "state_hash": digest({"tag": tag, "clock": clock}),
    }


def plan(binding):
    return {
        **binding,
        "source_hash": STORE_SOURCE_HASH,
        "authority": "TEST_ONLY",
        "grade": GRADE,
        "permitted_rules": [dict(RULE)],
    }


def base_result(binding, clock, before):
    return {
        **binding,
        "event_id": "event:b01:kitchen:1",
        "event_hash": "event:b01:kitchen:1",
        "clock": clock,
        "before": before,
        "after": state_doc(binding, clock, "base-after"),
        "objective": {
            "event": {
                "e1_event_id": "event:b01:kitchen:1",
                "e1_event_hash": "event:b01:kitchen:1",
            }
        },
        "receipt_ref": "P2_EVENT:event:b01:kitchen:1",
    }


def mediator_record(binding, clock):
    return {
        **binding,
        "project": PROJECT,
        "counterpart": MOTHER,
        "record_id": "record:b01:kitchen:1",
        "kind": "MEDIATOR",
        "payload": {"room": "kitchen", "qualified_speech": "mother-invitation"},
        "rule_id": RULE["rule_id"],
        "rule_version": RULE["rule_version"],
        "rule_hash": RULE["rule_hash"],
        "registry_hash": REGISTRY_HASH,
        "source_hash": STORE_SOURCE_HASH,
        "effective_from": clock,
        "causal_parents": ["event:b01:kitchen:1"],
        "grade": GRADE,
    }


def event_binding(binding, clock):
    return {
        **binding,
        "event_id": "event:b01:kitchen:1",
        "event_hash": "event:b01:kitchen:1",
        "clock": clock,
    }


def write_kitchen_mediator(path, binding):
    clock = 10
    store = PsycheStore(
        path, binding=binding, registry_hash=REGISTRY_HASH,
        source_hash=STORE_SOURCE_HASH,
    )
    try:
        store.reserve(
            "op:b01:kitchen:1",
            proposal_hash="proposal:b01:kitchen:1",
            expected=state_doc(binding, clock - 1, "expected"),
            plan_hash=digest(plan(binding)),
            base_before=state_doc(binding, clock - 1, "base-before"),
            psyche_before=store.head(),
            plan=plan(binding),
        )
        store.save_world(
            "op:b01:kitchen:1",
            base_result(binding, clock, state_doc(binding, clock - 1, "base-before")),
        )
        receipt = store.commit_effects(
            "op:b01:kitchen:1",
            records=[mediator_record(binding, clock)],
            response={"status": "COMPUTED_TEST_ONLY_HOME_READ"},
            event_binding=event_binding(binding, clock),
        )
        stored = store.query(project=PROJECT, counterpart=MOTHER, as_of=clock)
        assert len(stored) == 1
        record_hash = stored[0]["hash"]
        store.finish(
            "op:b01:kitchen:1",
            {
                "operation_id": "op:b01:kitchen:1",
                "proposal_hash": "proposal:b01:kitchen:1",
                "before": state_doc(binding, clock - 1, "expected"),
                "after": state_doc(binding, clock, "combined"),
                "status": "REALIZED",
                "objective": {"event": {"event_id": "event:b01:kitchen:1"}},
                "accessible": {"event_id": "event:b01:kitchen:1"},
                "consequences": {"effects_receipt_hash": receipt["receipt_hash"]},
                "readset": ["event:b01:kitchen:1"],
                "receipt_ref": "P3_PSYCH:" + receipt["response_hash"],
            },
        )
    finally:
        store.close()
    return record_hash


def later_decision(store_path, binding, *, as_of):
    """Test-local CG-A-style consumer; it is deliberately NOT a world reader."""
    store = PsycheStore(
        store_path, binding=binding, registry_hash=REGISTRY_HASH,
        source_hash=STORE_SOURCE_HASH,
    )
    try:
        rows = store.query(project=PROJECT, counterpart=MOTHER, as_of=as_of)
        if not rows:
            return {"action": "HOLD_NO_QUALIFIED_HOME", "basis": None}
        return {"action": "ENTER_KITCHEN", "basis": rows[0]["hash"]}
    finally:
        store.close()


def test_actual_root_household_is_world_owned_and_read_through_p6(tmp_path):
    state = tmp_path / "state"
    opening = run_cmd(state, "new")
    assert opening["room"] == "workshop"

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        household = read_household(session)
        parent = parent_choice_input(session)
        p2 = owner.base_owner.material_fact(HOUSEHOLD_SLOT)
        root = session.read_root()
        world = session.world()
        holder = world.actor_state["A"]

        assert household["schema"] == "SOROK_HOUSEHOLD_MATERIAL_READ@1"
        assert household["grade"] == "SOURCEFREE_FIXTURE"
        assert household["root"] == root["root_hash"] == parent["root_hash"] == p2["root"]
        assert household["branch"] == session.branch_id == parent["branch_id"] == p2["branch"]
        assert household["epoch"] <= household["clock"] == world.clock
        assert len(household["source"]) == 64
        int(household["source"], 16)
        assert household["source"] == p2["source"] == parent["source"]["hash"]
        assert household["place"] == {
            "dwelling_id": "dwelling:p6-workshop-home",
            "kind": "two_room_dwelling",
            "rooms": ["workshop", "living room"],
            "tenure": "rented",
            "tenancy": {
                "holder_actor_slot": "A",
                "landlord_ref": "SOURCEFREE_FIXTURE_LANDLORD",
            },
        }
        assert household["owner"] == {
            "actor_slot": "A",
            "actor_id": holder["actor_id"],
            "authority": "household_holder",
        }
        assert household["resources"] == [
            {
                "kind": "WORLD_RESOURCE", "slot": "workshop",
                "fields": {
                    "tool_available": world.resources["workshop"]["tool_available"],
                    "material": world.resources["workshop"]["material"],
                },
            },
            {
                "kind": "ACTOR_STATE", "actor_slot": "A",
                "actor_id": holder["actor_id"],
                "fields": {
                    "cash": holder["cash"],
                    "material_remaining": holder["material_remaining"],
                    "free_hours": holder["free_hours"],
                },
            },
        ]
        assert p2["state_hash"] == owner.base_owner.snapshot().state_hash
        assert p2["document"] == world.resources[HOUSEHOLD_SLOT]
        assert parent["first_consumer"] == "NONE_VERIFIED"
        assert parent["parent_decision"] == "NOT_EVALUATED"
        assert parent["parent_action"] is None
        assert parent["read_boundary"] == {
            "psyche_store": "NOT_READ",
            "parent_hidden_reason": "NOT_READ",
            "model_prose": "NOT_READ",
        }
        assert parent["household"] == {
            "place": household["place"],
            "owner": household["owner"],
            "resources": household["resources"],
        }
        assert parent["source"]["ref"] == "P6_HOUSEHOLD:" + household["source"]

        before = counts(session)
        for _ in range(3):
            assert read_household(session) == household
            assert parent_choice_input(session) == parent
            owner.base_owner.material_fact(HOUSEHOLD_SLOT)
        assert counts(session) == before
        assert establish_household(session) == household
        assert counts(session) == before
        world.advance(world.clock + 1)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_ALREADY_ESTABLISHED"):
            establish_household(session)
    finally:
        owner.close()

    source = inspect.getsource(house)
    assert "PsycheStore(" not in source
    assert "p3.state_store" not in source
    assert "p3_psyche" not in source


def test_changed_value_severance_restore_and_cold_reopen(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        baseline = read_household(session)
        baseline_parent = parent_choice_input(session)
        baseline_doc = copy.deepcopy(session.world().resources[HOUSEHOLD_SLOT])
        baseline_cash = session.world().actor_state["A"]["cash"]
        baseline_counts = counts(session)
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        world = session.world()
        world.actor_state["A"]["cash"] = baseline_cash - 7
        session.product._checkpoint(session.branch_id, world.clock, world)
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        changed = read_household(session)
        changed_parent = parent_choice_input(session)
        changed_p2 = owner.base_owner.material_fact(HOUSEHOLD_SLOT)
        assert changed["resources"][1]["fields"]["cash"] == baseline_cash - 7
        assert changed["source"] == baseline["source"]
        assert changed_p2["document"] == baseline_doc == changed_p2["document"]
        assert changed_p2["source"] == baseline["source"]
        assert changed["material_hash"] != baseline["material_hash"]
        assert changed_parent["source"]["material_hash"] == changed["material_hash"]
        assert changed_parent["household"]["resources"] == changed["resources"]
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        world = session.world()
        world.resources.pop(HOUSEHOLD_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_ABSENT"):
            read_household(session)
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_ABSENT"):
            parent_choice_input(session)
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ABSENT"):
            owner.base_owner.material_fact(HOUSEHOLD_SLOT)
    finally:
        owner.close()

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        world = session.world()
        world.actor_state["A"]["cash"] = baseline_cash
        session.product._checkpoint(session.branch_id, world.clock, world)
        restored = establish_household(session)
        assert restored == baseline
        assert parent_choice_input(session) == baseline_parent
        restored_counts = counts(session)
    finally:
        owner.close()

    script = (
        "import json, sys\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, sys.argv[1])\n"
        "import run_p6\n"
        "from house import read_household, parent_choice_input\n"
        "state = Path(sys.argv[2])\n"
        "owner = run_p6.open_owner(state / 'actual-p2')\n"
        "try:\n"
        "    session = owner.base_owner.fanin.session\n"
        "    store = session.product.store\n"
        "    print(json.dumps({\n"
        "        'household': read_household(session),\n"
        "        'parent': parent_choice_input(session),\n"
        "        'counts': {\n"
        "            'episodes': len(store.episodes(session.branch_id)),\n"
        "            'checkpoints': len(store.checkpoints(session.branch_id)),\n"
        "            'world_events': len(store.world_events(session.branch_id)),\n"
        "            'perceptions': len(store.perceptions(session.branch_id)),\n"
        "        },\n"
        "    }, sort_keys=True))\n"
        "finally:\n"
        "    owner.close()\n"
    )
    cold = subprocess.run(
        [sys.executable, "-B", "-c", script, str(P6), str(state)],
        capture_output=True, text=True, timeout=120,
    )
    assert cold.returncode == 0, cold.stdout + cold.stderr
    reopened = json.loads(cold.stdout)
    assert reopened["household"] == baseline
    assert reopened["parent"] == baseline_parent
    assert reopened["counts"] == restored_counts


def test_psyche_store_kitchen_mediator_cannot_stand_for_a_world_fact(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        household = read_household(session)
        binding = {
            "root": household["root"],
            "actor": household["owner"]["actor_id"],
            "branch": household["branch"],
        }
        baseline_counts = counts(session)
    finally:
        owner.close()

    store_path = tmp_path / "p3_psyche_kitchen.sqlite3"
    record_hash = write_kitchen_mediator(store_path, binding)
    assert later_decision(store_path, binding, as_of=12) == {
        "action": "ENTER_KITCHEN", "basis": record_hash,
    }

    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent = parent_choice_input(session)
        assert parent["household"]["place"]["dwelling_id"] == "dwelling:p6-workshop-home"
        assert parent["household"]["place"]["rooms"] == ["workshop", "living room"]
        assert "kitchen" not in json.dumps(parent)
        assert record_hash not in json.dumps(parent)
        assert parent["read_boundary"]["psyche_store"] == "NOT_READ"
        assert counts(session) == baseline_counts

        world = session.world()
        world.resources.pop(HOUSEHOLD_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
    finally:
        owner.close()

    assert later_decision(store_path, binding, as_of=12)["action"] == "ENTER_KITCHEN"
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_ABSENT"):
            read_household(session)
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_ABSENT"):
            parent_choice_input(session)
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ABSENT"):
            owner.base_owner.material_fact(HOUSEHOLD_SLOT)
    finally:
        owner.close()


def test_material_fact_writer_refuses_psyche_records_and_foreign_sources(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        document = copy.deepcopy(session.world().resources[HOUSEHOLD_SLOT])

        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_SLOT_INVALID"):
            write_material_fact(session, slot="p6_house", document=document)
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_SLOT_INVALID"):
            owner.base_owner.material_fact("p6_house")
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_PSYCH_RECORD_REFUSED"):
            write_material_fact(
                session, slot=HOUSEHOLD_SLOT,
                document=mediator_record(
                    {"root": document["root"],
                     "actor": document["owner"]["actor_id"],
                     "branch": document["branch"]},
                    10,
                ),
            )
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_SOURCE_MISMATCH"):
            write_material_fact(
                session, slot=HOUSEHOLD_SLOT,
                document={**document, "source": "0" * 64},
            )
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH"):
            write_material_fact(
                session, slot=HOUSEHOLD_SLOT,
                document={**document, "root": "foreign-root"},
            )
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_EPOCH_INVALID"):
            write_material_fact(
                session, slot=HOUSEHOLD_SLOT,
                document={**document, "epoch": session.world().clock + 1},
            )
    finally:
        owner.close()
