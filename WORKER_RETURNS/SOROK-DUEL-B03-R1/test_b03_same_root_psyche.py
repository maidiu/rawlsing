"""B03 same-root PsycheStore negative: world material readers never consume it.

This closes the strongest remaining B03 evidence gap in A's handoff: the
MEDIATOR is injected into the actual P6 root's p3_psyche.sqlite3, not a
separate test store.  The world dwelling/feasibility readers must remain
unchanged and must refuse when the world dwelling is severed, while the
PsycheStore decision remains available.
"""
from __future__ import annotations

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P3 = RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for _path in (P6, ENGINE, P3):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
import run_p6  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal, digest  # noqa: E402


def run_cmd(state, command, **args):
    return run_p6.experience(state, Namespace(command=command, request_id=None, **args))


def write_actual_root_mediator(owner, session):
    """Write one valid MEDIATOR through the actual root's PsycheStore protocol."""
    store = owner.store
    binding = store.binding
    clock = session.clock()
    expected = owner.snapshot().document()
    base_before = owner.base_owner.snapshot().document()
    rule = {
        "rule_id": "rule.b03.same-root.home",
        "rule_version": "1",
        "rule_hash": "rule:b03:same-root:home:1",
    }
    plan = {
        **binding,
        "source_hash": store.source_hash,
        "authority": "TEST_ONLY",
        "grade": "TEST_ONLY",
        "permitted_rules": [rule],
    }
    operation = "b03:same-root:psyche-mediator"
    event_id = "event:b03:same-root:kitchen"
    event_hash = "eventhash:b03:same-root:kitchen"
    store.reserve(
        operation,
        proposal_hash="proposal:b03:same-root",
        expected=expected,
        plan_hash=digest(plan),
        base_before=base_before,
        psyche_before=store.head(),
        plan=plan,
    )
    base_result = {
        **binding,
        "event_id": event_id,
        "event_hash": event_hash,
        "clock": clock,
        "before": base_before,
        "after": expected,
        "objective": {"event": {"e1_event_id": event_id,
                                "e1_event_hash": event_hash}},
        "receipt_ref": "P2_EVENT:" + event_hash,
    }
    store.save_world(operation, base_result)
    record = {
        **binding,
        "project": "b03:same-root",
        "counterpart": "mother",
        "record_id": "record:b03:same-root:kitchen",
        "kind": "MEDIATOR",
        "payload": {"room": "kitchen", "qualified_speech": "mother-invitation"},
        "rule_id": rule["rule_id"],
        "rule_version": rule["rule_version"],
        "rule_hash": rule["rule_hash"],
        "registry_hash": store.registry_hash,
        "source_hash": store.source_hash,
        "effective_from": clock,
        "causal_parents": [event_hash],
        "grade": "TEST_ONLY",
    }
    store.commit_effects(
        operation,
        records=[record],
        response={"status": "COMPUTED_TEST_ONLY_HOME_READ"},
        event_binding={**binding, "event_id": event_id,
                       "event_hash": event_hash, "clock": clock},
    )
    rows = store.query(project="b03:same-root", counterpart="mother", as_of=clock)
    assert len(rows) == 1
    return rows[0]["hash"], store.path


def test_same_root_psyche_mediator_not_world_dwelling_fact(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        baseline_dwelling = house.read_dwelling(session)
        baseline_household = house.read_household(session)
        baseline_feasibility = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        baseline_mother = house.mother_material_input(
            session, house.DRUM_KIT_REQUESTS["junior"])

        record_hash, store_path = write_actual_root_mediator(owner, session)
        assert str(state / "actual-p2" / "p3_psyche.sqlite3") == store_path
        assert owner.store.query(project="b03:same-root", counterpart="mother",
                                 as_of=session.clock())[0]["payload"]["room"] == "kitchen"

        after_dwelling = house.read_dwelling(session)
        after_household = house.read_household(session)
        after_feasibility = house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"])
        after_mother = house.mother_material_input(
            session, house.DRUM_KIT_REQUESTS["junior"])
        assert after_dwelling == baseline_dwelling
        assert after_household == baseline_household
        assert after_feasibility == baseline_feasibility
        assert after_mother == baseline_mother
        assert "kitchen" not in json.dumps(after_dwelling).lower()
        assert "kitchen" not in json.dumps(after_feasibility).lower()
        assert record_hash not in json.dumps(after_mother)
        assert after_feasibility["read_boundary"]["psyche_store"] == "NOT_READ"
        assert after_mother["read_boundary"]["psyche_store"] == "NOT_READ"

        world = session.world()
        world.resources.pop(house.DWELLING_SLOT)
        session.product._checkpoint(session.branch_id, world.clock, world)
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            house.read_dwelling(session)
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            house.material_feasibility(session, house.DRUM_KIT_REQUESTS["junior"])
        with pytest.raises(RecursionRefusal, match="P6_DWELLING_ABSENT"):
            house.mother_material_input(session, house.DRUM_KIT_REQUESTS["junior"])
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ABSENT"):
            owner.base_owner.material_fact(house.DWELLING_SLOT)
        assert owner.store.query(project="b03:same-root", counterpart="mother",
                                 as_of=session.clock())[0]["hash"] == record_hash

        restored = house.establish_dwelling(session)
        assert restored == baseline_dwelling
        assert house.read_household(session) == baseline_household
        assert house.material_feasibility(
            session, house.DRUM_KIT_REQUESTS["junior"]) == baseline_feasibility
        assert house.mother_material_input(
            session, house.DRUM_KIT_REQUESTS["junior"]) == baseline_mother
    finally:
        owner.close()
