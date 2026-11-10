"""Sourcefree independent actor initiative over the actual P6 turn/world store."""
from argparse import Namespace
import json

from run_p6 import experience, open_owner, read_house


def _run(state, command, interpret, **kw):
    return experience(state, Namespace(command=command, **kw), interpret=interpret)


def test_silent_multi_turn_cumulative_time_leads_to_world_admitted_actor_visit(tmp_path):
    state = tmp_path / "world"
    packets = []

    def interpret(packet):
        packets.append(packet)
        action = "visit_adjacent_room" if len(packets) == 2 else "continue"
        return {
            "attention": "uncertain",
            "interpretation": "Continue work or check the adjoining room.",
            "action": action,
            "cue_event_id": None,
            "channel": None,
        }

    first = _run(state, "new", interpret, situated_house=True)
    _run(state, "go", interpret, target="living room", request_id="player-away")

    owner = open_owner(state / "actual-p2")
    try:
        psyche_before = owner.store.head()
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        epoch = house["epoch"]
        assert world.positions["A"] == "workshop"
    finally:
        owner.close()

    _run(state, "wait", interpret, duration=2, request_id="quiet-first")
    second = _run(state, "wait", interpret, duration=3, request_id="quiet-next")
    assert any("The worker walks into the adjoining room." in row["text"]
               for row in second["narration"])

    assert len(packets) == 2
    assert [x["elapsed"] for x in packets] == [2, 3]
    assert [x["scene_elapsed"] for x in packets] == [3, 6]
    assert all(x["available_actions"] == ["continue", "visit_adjacent_room"]
               for x in packets)
    assert all(x["room"] == "workshop" for x in packets)
    assert second["clock"] == epoch + 6
    assert first["clock"] == epoch

    ledger = state / "p4_receipts.json"
    prior = ledger.read_bytes()
    [turn] = [t for t in json.loads(prior)["turns"]
              if t["request_id"] == "quiet-next"]
    situated = turn["receipt"]["situated"]
    movement = situated["movement"]
    assert situated["decision"]["action"] == "visit_adjacent_room"
    assert movement["admitted"] and movement["origin"] == "workshop"
    assert movement["destination"] == "living room"
    assert movement["grade"] == "SOURCEFREE_PROVISIONAL_ACTOR_WORLD_ACTION_NOT_NATIVE"

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, _ = read_house(session)
        event = session.event(movement["event_id"])
        assert event["kind"] == "MOVE"
        assert event["actor_id"] == "A"
        assert event["location"] == "living room"
        assert event["hash"] == movement["event_hash"]
        assert event["body"]["origin"] == "workshop"
        assert event["body"]["target"] == "living room"
        assert event["body"]["actor_action"] == "visit_adjacent_room"
        assert world.positions["A"] == "living room"
        assert movement["event_id"] in session.user_perceived_ids()
        assert owner.store.head() == psyche_before
        assert len([e for e in session.events()
                    if e["actor_id"] == "A"
                    and e["kind"] == "MOVE"
                    and e["body"].get("actor_action") == "visit_adjacent_room"]) == 1
    finally:
        owner.close()

    duplicate = _run(state, "wait", interpret, duration=3, request_id="quiet-next")
    assert duplicate["clock"] == second["clock"]
    assert ledger.read_bytes() == prior
    assert len(packets) == 2

    # This is not a terminal vignette: the actor's moved location must
    # remain authoritative when the next independent interval begins.
    following = _run(state, "wait", interpret, duration=1, request_id="after-visit")
    assert following["clock"] == epoch + 7
    assert len(packets) == 3
    assert packets[-1]["room"] == "living room"
    assert packets[-1]["scene_elapsed"] == 7
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert read_house(session)[0].positions["A"] == "living room"
        assert len([e for e in session.events() if e["actor_id"] == "A"
                    and e["body"].get("actor_action") == "visit_adjacent_room"]) == 1
    finally:
        owner.close()


def test_model_cannot_visit_without_source_bound_actor_context(tmp_path):
    state = tmp_path / "world"

    def attempt(packet):
        assert packet["actor_context"] is None
        assert "visit_adjacent_room" not in packet["available_actions"]
        return {"attention": "uncertain", "interpretation": "I want to go.",
                "action": "visit_adjacent_room", "cue_event_id": None, "channel": None}

    _run(state, "new", attempt, situated_house=True)
    result = experience(
        state, Namespace(command="wait", duration=2, request_id="foreign-context"),
        interpret=attempt,
        actor_context={"grade": "SOURCEFREE_FIXTURE", "actor_id": "foreign",
                       "priority": "go somewhere"},
    )
    assert result["admission"] == "ADMITTED"
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, _ = read_house(session)
        assert world.positions["A"] == "workshop"
        assert not any(e["actor_id"] == "A" and
                       e["body"].get("actor_action") == "visit_adjacent_room"
                       for e in session.events())
    finally:
        owner.close()
    ledger = json.loads((state / "p4_receipts.json").read_text())
    assert ledger["turns"][-1]["receipt"]["situated"]["status"] == "INVALID_INTERPRETATION"


def test_matching_actor_but_invented_relationship_cannot_license_movement(tmp_path):
    state = tmp_path / "world"

    def interpret(packet):
        assert packet["actor_context"]["priority"] == "invented outside the world"
        assert "visit_adjacent_room" not in packet["available_actions"]
        return {"attention": "uncertain", "interpretation": "I will go next door.",
                "action": "visit_adjacent_room", "cue_event_id": None, "channel": None}

    _run(state, "new", interpret, situated_house=True)
    owner = open_owner(state / "actual-p2")
    try:
        actor_id = owner.base_owner.fanin.session.world().actor_state["A"]["actor_id"]
    finally:
        owner.close()
    result = experience(
        state, Namespace(command="wait", duration=2, request_id="invented-persona"),
        interpret=interpret,
        actor_context={
            "grade": "SOURCEFREE_FIXTURE", "actor_id": actor_id,
            "priority": "invented outside the world",
            "relationship": "unverified lifelong friend",
        },
    )
    assert result["admission"] == "ADMITTED"
    owner = open_owner(state / "actual-p2")
    try:
        world, _ = read_house(owner.base_owner.fanin.session)
        assert world.positions["A"] == "workshop"
    finally:
        owner.close()
    ledger = json.loads((state / "p4_receipts.json").read_text())
    assert ledger["turns"][-1]["receipt"]["situated"]["status"] == "INVALID_INTERPRETATION"


def test_actor_visit_is_not_omnisciently_public_when_player_elsewhere(tmp_path):
    state = tmp_path / "world"

    def interpret(packet):
        assert "visit_adjacent_room" in packet["available_actions"]
        return {"attention": "uncertain", "interpretation": "Finish in the next room.",
                "action": "visit_adjacent_room", "cue_event_id": None, "channel": None}

    _run(state, "new", interpret, situated_house=True)
    _run(state, "wait", interpret, duration=3, request_id="actor-steps-away")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    event_id = ledger["turns"][-1]["receipt"]["situated"]["movement"]["event_id"]
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, _ = read_house(session)
        assert world.positions["A"] == "living room"
        assert world.positions[session.meta["user_actor"]] == "workshop"
        assert event_id not in session.user_perceived_ids()
        assert session.event(event_id)["kind"] == "MOVE"
    finally:
        owner.close()
