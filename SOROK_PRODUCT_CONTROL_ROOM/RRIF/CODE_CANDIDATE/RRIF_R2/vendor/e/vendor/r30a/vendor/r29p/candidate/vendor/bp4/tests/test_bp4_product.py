"""Executable A0-A3, offscreen life, cold reentry and fork-divergence court."""
from __future__ import annotations

import json

from bp4.product import BP4Product


def test_a0_a1_a2_a3_full_positive(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        a0 = p.observe()
        assert a0["status"] == "OK"
        assert a0["clock"] == 10
        assert a0["self"]["position"] == "workshop"
        assert a0["c9"]["target_id"] == p.seed.c9_target_id
        assert a0["c9"]["e2_admitted"] is True
        assert any(c["kind"] == "ARRIVAL" for c in a0["claims"])

        said = p.say("I am here about the bench.")
        assert said["admitted"] is True
        assert "B" in said["observable_by"]

        inspected = p.inspect()
        assert inspected["status"] == "NO_CHANGE"
        assert inspected["changed"] is False

        waited = p.wait(30)
        assert waited["clock"] == 40
        assert waited["offscreen_events"]

        other = p.other()
        assert other["public"]["position"] == "market"
        assert other["public"]["completed_units"] == 4
        assert "cash" in other["private_fields_hidden"]

        moved = p.travel("market")
        assert moved["status"] == "OK"
        attended = p.attend()
        assert attended["status"] == "NO_CHANGE"
        assert attended["new_knowledge"]

        reentry = p.observe()
        assert reentry["status"] == "OK"
        assert reentry["clock"] == 40
        kinds = [c["kind"] for c in reentry["claims"]]
        assert "OFFSCREEN_REPAIR" in kinds
        assert all(c["m6_receiver_state"].startswith("READY") for c in reentry["claims"])
        assert reentry["native_claims"] == {
            "actor": False, "rule": False, "c8_trust": False,
            "world": False, "c12": False, "c11": False,
        }
        assert reentry["grade"].startswith("TEST_ONLY_SOURCEFREE")
    finally:
        p.close()


def test_actor_limited_perception_offscreen_is_hidden_until_attended(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        before = p.observe()
        assert not any(c["kind"].startswith("OFFSCREEN") for c in before["claims"])
        p.wait(30)
        hidden = p.observe()
        assert not any(c["kind"].startswith("OFFSCREEN") for c in hidden["claims"])
        assert hidden["clock"] == 40
        p.travel("market")
        p.attend()
        visible = p.observe()
        offscreen = [c for c in visible["claims"] if c["kind"] == "OFFSCREEN_REPAIR"]
        assert len(offscreen) == 1
        assert offscreen[0]["m6_permission"] == "PERMIT_FIRST_PERSON_KNOWLEDGE"
    finally:
        p.close()


def test_no_change_and_deny_paths(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        assert p.inspect()["status"] == "NO_CHANGE"
        assert p.repair()["admitted"] is True
        assert p.repair()["admitted"] is True
        denied = p.repair()
        assert denied["status"] == "DENY"
        assert denied["code"] == "MATERIAL_EXHAUSTED"
        assert p.attend()["status"] == "NO_CHANGE"
        bad = p.travel("nowhere")
        assert bad["status"] == "DENY"
        assert p.travel("market")["status"] == "OK"
        assert p.repair()["code"] == "WRONG_LOCATION"
        assert p.address_other("Are you there?")["code"] == "OTHER_ACTOR_NOT_PRESENT"
    finally:
        p.close()


def test_cold_reentry_preserves_branch_clock_and_history(tmp_path):
    root = tmp_path / "state"
    p = BP4Product(root)
    p.say("hello before cold exit")
    p.wait(30)
    p.travel("market")
    p.attend()
    before = p.observe()
    p.close()
    q = BP4Product(root)
    try:
        after = q.reenter()
        assert after["status"] == "OK"
        assert after["branch_id"] == before["branch_id"]
        assert after["clock"] == before["clock"]
        assert [c["event_id"] for c in after["claims"]] == [c["event_id"] for c in before["claims"]]
        assert after["c9"]["state_hash"] == before["c9"]["state_hash"]
        assert after["c8"]["writer_version"] == before["c8"]["writer_version"]
    finally:
        q.close()


def test_fork_shared_root_and_branch_divergence(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        p.say("branch point")
        fork = p.fork("branch_leave")
        assert fork["shared_root"]["equal"] is True
        p.use("branch_leave")
        assert p.leave_tool()["admitted"] is True
        p.wait(30)
        leave_other = p.other()
        leave_clock = p.observe()["clock"]

        p.use("root")
        assert p.take_tool()["admitted"] is True
        p.wait(30)
        take_other = p.other()
        take_clock = p.observe()["clock"]

        assert leave_clock == take_clock == 40
        assert leave_other["public"]["completed_units"] == 4
        assert take_other["public"]["completed_units"] == 3
        assert leave_other["public"]["public_work_events"] != take_other["public"]["public_work_events"]
        shared = p.store.shared_root_equal("branch_leave", "root")
        assert shared["equal"] is True
        # The post-fork tool action is branch-local.
        leave_events = {e["event_id"] for e in p.store.world_events("branch_leave")}
        take_events = {e["event_id"] for e in p.store.world_events("root")}
        assert leave_events != take_events
    finally:
        p.close()
