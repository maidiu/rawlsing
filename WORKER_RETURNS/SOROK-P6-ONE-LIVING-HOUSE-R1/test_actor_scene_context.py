"""Exact self-action context at P6 sourcefree scene scope."""
from argparse import Namespace
import json

from actor_scene_context import recent_self_actions
from run_p6 import experience, open_owner, read_house


def test_actor_knows_own_committed_movement_in_next_turn_without_durable_memory(tmp_path):
    packets = []

    def interpret(packet):
        packets.append(packet)
        action = "visit_adjacent_room" if len(packets) == 1 else "continue"
        return {
            "attention": "uncertain", "interpretation": "Act in the present scene.",
            "action": action, "cue_event_id": None, "channel": None,
        }

    def act(command, **kwargs):
        return experience(tmp_path, Namespace(command=command, **kwargs), interpret=interpret)

    act("new", situated_house=True)
    act("go", target="living room", request_id="go-away")
    owner = open_owner(tmp_path / "actual-p2")
    try:
        psyche = owner.store.head()
    finally:
        owner.close()
    act("wait", duration=2, request_id="first-quiet")
    ledger_file = tmp_path / "p4_receipts.json"
    ledger = json.loads(ledger_file.read_text())
    movement = ledger["turns"][-1]["receipt"]["situated"]["movement"]
    assert movement["admitted"] and movement["destination"] == "living room"
    assert packets[0]["recent_self_actions"] == [
        x for x in packets[0]["recent_self_actions"]
        if x["kind"] in ("MOVE", "REPAIR")
    ]
    assert not any(x["event_id"] == movement["event_id"] for x in packets[0]["recent_self_actions"])

    result = act("wait", duration=2, request_id="second-quiet")
    later = packets[1]["recent_self_actions"]
    [own_move] = [x for x in later if x["event_id"] == movement["event_id"]]
    assert own_move["kind"] == "MOVE"
    assert own_move["location"] == "living room"
    assert own_move["event_hash"] == movement["event_hash"]
    assert own_move["source"] == "COMMITTED_SELF_ACTION_WITH_ACTOR_PERCEPTION"
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.event(movement["event_id"])["hash"] == own_move["event_hash"]
        assert any(p["event_id"] == movement["event_id"] for p in
                   session.product.store.perceptions(session.branch_id, "A"))
        assert all(session.event(x["event_id"])["actor_id"] == "A" for x in later)
        assert read_house(session)[0].positions["A"] == "living room"
        assert owner.store.head() == psyche
    finally:
        owner.close()
    written = ledger_file.read_bytes()
    duplicate = act("wait", duration=2, request_id="second-quiet")
    assert duplicate["clock"] == result["clock"]
    assert len(packets) == 2
    assert ledger_file.read_bytes() == written


def test_self_action_projection_rejects_user_or_forged_perception_rows(tmp_path, monkeypatch):
    def interpret(packet):
        return {
            "attention": "uncertain", "interpretation": "",
            "action": "continue", "cue_event_id": None, "channel": None,
        }

    experience(tmp_path, Namespace(command="new", situated_house=True), interpret=interpret)
    experience(tmp_path, Namespace(command="go", target="living room", request_id="go"),
               interpret=interpret)
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        user_event = next(e for e in reversed(session.events())
                          if e["kind"] == "MOVE" and e["actor_id"] == session.meta["user_actor"])
        canonical = recent_self_actions(session)
        store = session.product.store
        real = store.perceptions

        def hostile(branch, actor):
            return list(real(branch, actor)) + [
                {"event_id": user_event["event_id"], "clock": user_event["clock"]},
                {"event_id": "invented-world-event", "clock": user_event["clock"]},
                {"event_id": user_event["event_id"], "clock": user_event["clock"] + 17},
            ]

        monkeypatch.setattr(store, "perceptions", hostile)
        assert recent_self_actions(session) == canonical
        assert all(x["kind"] in ("MOVE", "REPAIR") for x in canonical)
    finally:
        owner.close()
