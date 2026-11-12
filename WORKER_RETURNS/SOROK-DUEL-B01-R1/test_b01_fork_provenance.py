"""A relay attack on B's C12 fork household provenance and shared prefix."""
from __future__ import annotations

from argparse import Namespace
import copy
import json
from pathlib import Path
import sys

import pytest

RETURNS = Path(__file__).resolve().parents[1]
P6 = RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
ENGINE = RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for _path in (P6, ENGINE):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import branch_is_ancestor  # noqa: E402
import run_p6  # noqa: E402
from house import (  # noqa: E402
    HOUSEHOLD_SLOT,
    parent_choice_input,
    read_household,
)


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


def test_fork_provenance_is_explicit_and_not_full_composite(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        parent_household = read_household(session)
        session.fork_alt("child")
        session.fork_alt("grandchild")
        child_household = read_household(session)
        child_input = parent_choice_input(session)
        p2 = owner.base_owner.material_fact(HOUSEHOLD_SLOT)
        before = counts(session)

        provenance = {
            "stored_branch": parent_branch,
            "current_branch": "grandchild",
            "inherited": True,
            "scope": "P6_MATERIAL_FACT_ONLY",
            "fork_state": "C12_FORK_WITHOUT_S46_INTERVAL_STATE",
        }
        assert child_household["provenance"] == provenance
        assert child_input["provenance"] == provenance
        assert child_input["source"]["stored_branch"] == parent_branch
        assert child_input["source"]["inherited"] is True
        assert child_input["source"]["fork_state"] == provenance["fork_state"]
        assert child_household["source"] == parent_household["source"]
        assert child_household["branch"] == "grandchild"
        assert len(child_household["material_hash"]) == 64
        assert p2["branch"] == "grandchild"
        assert p2["document"]["branch"] == parent_branch
        assert p2["state_scope"] == "C12_FORK_WITHOUT_S46_INTERVAL_STATE"
        assert len(p2["state_hash"]) == 64
        assert counts(session) == before
    finally:
        owner.close()


def test_fact_after_fork_clock_is_refused_and_restored(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        session.fork_alt("child")
        fork_clock = session.product.store.branch("child")["fork_clock"]
        baseline = read_household(session)
        assert branch_is_ancestor(session, parent_branch, baseline["epoch"])

        world = session.world()
        world.advance(fork_clock + 5)
        session.product._checkpoint(session.branch_id, world.clock, world)
        world = session.world()
        original_epoch = world.resources[HOUSEHOLD_SLOT]["epoch"]
        world.resources[HOUSEHOLD_SLOT]["epoch"] = fork_clock + 1
        session.product._checkpoint(session.branch_id, world.clock, world)

        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH"):
            read_household(session)
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH"):
            owner.base_owner.material_fact(HOUSEHOLD_SLOT)

        world = session.world()
        world.resources[HOUSEHOLD_SLOT]["epoch"] = original_epoch
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert read_household(session)["source"] == baseline["source"]
    finally:
        owner.close()


def test_actual_copied_prefix_not_mutable_root_counts(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        session.fork_alt("child")
        epoch = read_household(session)["epoch"]
        store = session.product.store
        original_counts = copy.deepcopy(store.branch("child")["root_counts"])
        original_row = store.db.execute(
            "SELECT hash FROM world_event WHERE branch_id='child' ORDER BY seq LIMIT 1"
        ).fetchone()

        store.db.execute(
            "UPDATE branch SET root_counts=? WHERE branch_id=?",
            (json.dumps({}), "child"),
        )
        store.db.commit()
        assert branch_is_ancestor(session, parent_branch, epoch)
        assert read_household(session)["source"]

        store.db.execute("DROP TRIGGER IF EXISTS world_event_no_update")
        store.db.execute(
            "UPDATE world_event SET hash=? WHERE branch_id='child' AND seq=0",
            ("0" * 64,),
        )
        store.db.commit()
        assert not branch_is_ancestor(session, parent_branch, epoch)
        with pytest.raises(RecursionRefusal, match="P6_HOUSEHOLD_SOURCE_OR_ROOT_MISMATCH"):
            read_household(session)
        with pytest.raises(RecursionRefusal, match="P2_MATERIAL_FACT_ROOT_OR_BRANCH_MISMATCH"):
            owner.base_owner.material_fact(HOUSEHOLD_SLOT)

        store.db.execute(
            "UPDATE world_event SET hash=? WHERE branch_id='child' AND seq=0",
            (original_row[0],),
        )
        store.db.execute(
            "UPDATE branch SET root_counts=? WHERE branch_id=?",
            (json.dumps(original_counts), "child"),
        )
        store.db.commit()
        assert branch_is_ancestor(session, parent_branch, epoch)
        assert read_household(session)["source"]
    finally:
        owner.close()


def test_child_p6_action_is_stored_on_child_with_parent_house_provenance(tmp_path):
    state = tmp_path / "state"
    run_cmd(state, "new")
    owner = open_owner(state)
    try:
        session = owner.base_owner.fanin.session
        parent_branch = session.branch_id
        session.fork_alt("child")
        child_branch = session.branch_id
        receipt, moved = house.perform(session, {"operation": "GO", "target": "living room"})
        assert moved["admission"] == "ADMITTED" and moved["performed"] is True
        event = receipt["performed"]
        assert session.branch_id == child_branch
        assert event["body"]["branch"] == parent_branch
        assert any(row["event_id"] == event["event_id"]
                   for row in session.product.store.world_events(child_branch))
        assert not any(row["event_id"] == event["event_id"]
                       for row in session.product.store.world_events(parent_branch))
    finally:
        owner.close()
