"""Independent nonauthor G5 probes for the #982 composite source cut.

These probes are reviewer-authored only. They do not patch product source and
do not replace the original hostile, D1, receiver, P4 or P6 assets.
"""
from argparse import Namespace
from copy import deepcopy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"
if str(P6) not in sys.path:
    sys.path.insert(0, str(P6))

import run_p6
from house import read_house
from situated import current_p3_actor_access


def _run(state, command, request_id, *, duration=None, interpret=None, bridge=False):
    return run_p6.experience(
        state,
        Namespace(command=command, request_id=request_id, duration=duration,
                  situated_house=True),
        interpret=interpret,
        sourcefree_p3_bridge=bridge,
    )


def _turn(state):
    return json.loads((state / "p4_receipts.json").read_text())["turns"][-1]


def _owner(state):
    return run_p6.open_owner(state / "actual-p2")


def _access(session, interval, world, house, packet, receipt):
    return current_p3_actor_access(
        session, interval, world, house, packet, source_receipt=receipt,
    )


def test_first_consumer_checks_owner_interval_before_outer_turn_commit(tmp_path):
    state = tmp_path / "first-consumer"
    _run(state, "new", None)
    captured = []

    def interpret(packet):
        captured.append(deepcopy(packet))
        ledger = json.loads((state / "p4_receipts.json").read_text())
        # The P6 access decision is made inside run_p4.act's conduct callback,
        # after PACE persisted the S46 state and before the outer turn append.
        assert ledger["pending"] is not None
        assert len(ledger["turns"]) == 0
        p3 = packet["sourcefree_p3"]
        assert p3["actor_access_evidence"]
        assert {row["basis"] for row in p3["actor_access_evidence"]} == {
            "P6_OUTWARD_CURRENT_OPERATION_DERIVED"
        }
        assert p3["stimulus_to_mediator_relevance"] == "UNISSUED_NATIVE_RULE"
        assert p3["world_readset"] and p3["readset"]
        assert set(p3["world_readset"]).isdisjoint(p3["readset"])
        return {"attention": "noticed", "interpretation": "first consumer only",
                "action": "continue", "cue_event_id": None, "channel": None}

    public = _run(state, "approach", "first", interpret=interpret, bridge=True)
    assert len(captured) == 1
    packet = captured[0]
    assert packet["sourcefree_p3"]["grade"] == "SOURCEFREE_TEST_ONLY"
    assert "sourcefree_p3_receipt" not in json.dumps(public)

    ledger = json.loads((state / "p4_receipts.json").read_text())
    assert len(ledger["turns"]) == 1
    turn = ledger["turns"][-1]
    receipt = turn["receipt"]
    private = receipt["situated"]["sourcefree_p3_receipt"]
    assert private["actor_access_evidence"] == packet["sourcefree_p3"]["actor_access_evidence"]
    assert private["p3_record_readset"] == packet["sourcefree_p3"]["readset"]
    assert private["current_world_readset"] == packet["sourcefree_p3"]["world_readset"]
    assert private["stimulus_to_mediator_relevance"] == "UNISSUED_NATIVE_RULE"

    interval = receipt["interval"]
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        states = session.read_interval_states()
        state_row = states[-1]
        assert state_row["currentness"] == "CURRENT"
        assert state_row["episode_id"] == interval["episode_id"]
        assert state_row["state_id"] == interval["state_id"]
        assert state_row["receipt_hash"] == interval["receipt_hash"]
        assert state_row["domain_issuance_id"] == interval["domain_issuance_id"]
        assert state_row["end"] == session.clock()
        assert state_row["root_hash"] == session.read_root()["root_hash"]
        assert state_row["branch_id"] == session.branch_id
        assert state_row["actor_id"] == session.world().actor_state["A"]["actor_id"]
        episodes = session.product.store.episodes(session.branch_id)
        index = next(i for i, row in enumerate(episodes)
                     if row.get("kind") == "S46_INTERVAL_STATE"
                     and row.get("episode_id") == state_row["episode_id"])
        previous = next((i for i in range(index - 1, -1, -1)
                         if episodes[i].get("kind") == "S46_INTERVAL_STATE"), -1)
        window_ids = {row.get("episode_id") for row in episodes[previous + 1:index]}
        conducts = [row for row in session.episodes(session.meta["user_actor"])
                    if row.get("kind") == "P6_HOUSE_CONDUCT"
                    and row.get("episode_id") in window_ids]
        assert len(conducts) == 1
        assert conducts[0]["body"] == {
            "event_id": receipt["performed"]["event_id"],
            "operation": receipt["performed"]["kind"],
        }
        world, house = read_house(session)
        current_packet = {"cues": [receipt["outward_cue"]],
                          "recent_self_actions": [], "recent_speech": []}
        assert _access(session, interval, world, house, current_packet, receipt) is True
    finally:
        owner.close()

    # Cold reopen conserves the exact current operation receipt.
    for _ in range(2):
        owner = _owner(state)
        try:
            session = owner.base_owner.fanin.session
            world, house = read_house(session)
            current_packet = {"cues": [receipt["outward_cue"]],
                              "recent_self_actions": [], "recent_speech": []}
            assert _access(session, interval, world, house, current_packet, receipt) is True
        finally:
            owner.close()

    _run(state, "wait", "later", duration=4)
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        current_packet = {"cues": [receipt["outward_cue"]],
                          "recent_self_actions": [], "recent_speech": []}
        assert _access(session, interval, world, house, current_packet, receipt) is False
        assert _access(session, {"start": interval["start"] - 1,
                                 "end": world.clock}, world, house,
                       current_packet, receipt) is False
    finally:
        owner.close()


def test_tampered_performed_or_sensory_cue_on_current_interval_refuses(tmp_path):
    state = tmp_path / "tampered"
    _run(state, "new", None)
    _run(state, "approach", "current")
    receipt = _turn(state)["receipt"]
    assert receipt["outward_cue"]
    owner = _owner(state)
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        packet = {"cues": [receipt["outward_cue"]],
                  "recent_self_actions": [], "recent_speech": []}
        assert _access(session, receipt["interval"], world, house, packet, receipt) is True

        # Authentic current interval identity but tampered performed event body.
        forged_performed = deepcopy(receipt)
        forged_performed["performed"]["body"] = {
            **forged_performed["performed"]["body"], "tampered": True,
        }
        assert _access(session, forged_performed["interval"], world, house,
                       packet, forged_performed) is False

        # Authentic current interval identity and event id, but forged cue detail.
        forged_cue = deepcopy(receipt)
        forged_cue["outward_cue"]["detail"] = {
            **forged_cue["outward_cue"]["detail"], "near": not forged_cue[
                "outward_cue"]["detail"].get("near"),
        }
        forged_packet = {"cues": [forged_cue["outward_cue"]],
                         "recent_self_actions": [], "recent_speech": []}
        assert _access(session, forged_cue["interval"], world, house,
                       forged_packet, forged_cue) is False
    finally:
        owner.close()
