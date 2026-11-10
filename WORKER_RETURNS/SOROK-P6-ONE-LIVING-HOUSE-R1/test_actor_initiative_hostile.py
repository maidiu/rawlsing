"""Hostile #880 repair court: real event, writer and actor continuity boundaries."""
from argparse import Namespace
import json

import pytest

from run_p6 import experience, open_owner, read_house, RecursionRefusal
from actor_initiative import issue_visit_admission, visit_adjacent_room


def _run(state, command, interpret, **args):
    return experience(state, Namespace(command=command, **args), interpret=interpret)


def _decision(action="continue"):
    return {"attention": "uncertain", "interpretation": "Stay or cross the doorway.",
            "action": action, "cue_event_id": None, "channel": None}


def _visible_scene(monkeypatch, *, origin="VISIBLE", destination="VISIBLE"):
    import run_p6
    original = run_p6.establish_demo_conditions

    def install(session):
        original(session)
        world, house = read_house(session)
        house["situated_conditions"]["actor_move_visibility"] = {
            "origin": origin, "destination": destination,
        }
        session.product._checkpoint(session.branch_id, world.clock, world)
    monkeypatch.setattr(run_p6, "establish_demo_conditions", install)


@pytest.mark.parametrize("player_room,origin,destination,expected_lane", [
    ("workshop", "VISIBLE", "VISIBLE", "origin"),
    ("living room", "VISIBLE", "VISIBLE", "destination"),
    ("workshop", "OCCLUDED", "VISIBLE", None),
    ("living room", "VISIBLE", "OCCLUDED", None),
    ("workshop", "UNKNOWN", "VISIBLE", None),
    ("living room", "VISIBLE", "UNKNOWN", None),
])
def test_departure_arrival_visibility_separate_and_no_omniscience(
        tmp_path, monkeypatch, player_room, origin, destination, expected_lane):
    _visible_scene(monkeypatch, origin=origin, destination=destination)
    state = tmp_path / "world"
    packets = []

    def choose(packet):
        packets.append(packet)
        assert "visit_adjacent_room" in packet["available_actions"]
        assert packet["action_affordances"] == [{
            "action": "visit_adjacent_room", "origin": "workshop",
            "destination": "living room", "basis": "SOURCEFREE_CHECKPOINTED_ADJACENCY",
        }]
        return _decision("visit_adjacent_room" if packet["elapsed"] == 2 else "continue")

    _run(state, "new", choose, situated_house=True)
    if player_room == "living room":
        # The leading GO has elapsed 1, so it must not select movement.
        _run(state, "go", choose, target="living room", request_id="player-arrives")
    public = _run(state, "wait", choose, duration=2, request_id="actor-moves")
    receipt = json.loads((state / "p4_receipts.json").read_text())["turns"][-1]["receipt"]
    movement = receipt["situated"]["movement"]
    event_id = movement["event_id"]
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, _ = read_house(session)
        assert world.positions["A"] == "living room"
        assert session.event(event_id)["kind"] == "MOVE"
        assert movement["user_observation"] == (expected_lane or "HELD_UNQUALIFIED")
        assert (event_id in session.user_perceived_ids()) is (expected_lane is not None)
    finally:
        owner.close()
    rendered = [row["text"] for row in public["narration"]]
    assert any("worker walks into the adjoining room" in x for x in rendered) is (
        expected_lane is not None
    )
    saved = (state / "p4_receipts.json").read_bytes()
    replay = _run(state, "wait", choose, duration=2, request_id="actor-moves")
    assert replay["clock"] == public["clock"]
    assert (state / "p4_receipts.json").read_bytes() == saved


@pytest.mark.parametrize("fault", ["missing_ticket", "stale_clock", "changed_source",
                                   "removed_actor_context", "invalid_decision"])
def test_direct_world_writer_requires_selected_fresh_checkpoint_authority(tmp_path, fault):
    state = tmp_path / "world"
    packets = []

    def continue_only(packet):
        packets.append(packet)
        return _decision("continue")

    _run(state, "new", continue_only, situated_house=True)
    _run(state, "wait", continue_only, duration=2, request_id="capture")
    packet = packets[-1]
    decision = _decision("visit_adjacent_room")
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        world, house = read_house(session)
        actor = world.actor_state["A"]["actor_id"]
        events_before = [e["event_id"] for e in session.events()]
        episodes_before = len(session.episodes("A"))
        positions_before = dict(world.positions)
        if fault == "missing_ticket":
            ticket = None
        else:
            ticket = issue_visit_admission(session, packet, decision)
        if fault == "stale_clock":
            world.advance(world.clock + 1)
            session.product._checkpoint(session.branch_id, world.clock, world)
        elif fault == "changed_source":
            house["situated_conditions"]["actor_move_visibility"]["origin"] = "OCCLUDED"
            session.product._checkpoint(session.branch_id, world.clock, world)
        elif fault == "removed_actor_context":
            house.pop("situated_actor_context")
            session.product._checkpoint(session.branch_id, world.clock, world)
        elif fault == "invalid_decision":
            decision = _decision("continue")
        with pytest.raises(RecursionRefusal, match="P6_INITIATIVE_(SELECTION_NOT_ADMITTED|CHECKPOINT_AUTHORITY_MISSING|ADMISSION_STALE_OR_INVALID)"):
            visit_adjacent_room(session, actor, packet=packet,
                                decision=decision, admission=ticket)
        assert [e["event_id"] for e in session.events()] == events_before
        assert len(session.episodes("A")) == episodes_before
        after, _ = read_house(session)
        assert after.positions == positions_before
    finally:
        owner.close()


def test_quiet_streak_not_conflated_with_scene_age_or_continuing_music(tmp_path):
    packets = []

    def choose(packet):
        packets.append(packet)
        return _decision()

    state = tmp_path / "world"
    _run(state, "new", choose, situated_house=True)
    _run(state, "wait", choose, duration=1, request_id="quiet1")
    _run(state, "wait", choose, duration=1, request_id="quiet2")
    assert [p["interaction_quiet"]["elapsed"] for p in packets] == [1, 2]
    assert packets[-1]["scene_elapsed"] >= 2
    go = _run(state, "go", choose, target="living room", request_id="go")
    assert go["admission"] == "ADMITTED", go
    # Ordinary GO has no actor-qualified sensory cue in this sourcefree
    # fixture, so it need not invoke the model immediately. The next quiet
    # interval must nevertheless see the real committed move as a reset.
    committed_go = json.loads((state / "p4_receipts.json").read_text())["turns"][-1]
    go_event_id = committed_go["receipt"]["performed"]["event_id"]
    _run(state, "wait", choose, duration=1, request_id="after-go")
    # The MOVE was not qualified for Nadia in this case: the world knows
    # it happened, but her quiet-awareness model must not inherit its ID.
    assert packets[-1]["interaction_quiet"]["last_break_event_id"] != go_event_id
    assert packets[-1]["interaction_quiet"]["elapsed"] >= packets[1]["interaction_quiet"]["elapsed"]
    assert packets[-1]["scene_elapsed"] >= packets[-1]["interaction_quiet"]["elapsed"]
    # A fresh compact music scene tests ongoing sound without relying on the
    # finite workshop's ability to remain open after many completed work beats.
    music_state = tmp_path / "music"
    music_packets = []

    def music_choice(packet):
        music_packets.append(packet)
        return _decision()

    _run(music_state, "new", music_choice, situated_house=True)
    assert _run(music_state, "go", music_choice, target="living room",
                request_id="music-go")["admission"] == "ADMITTED"
    assert _run(music_state, "play", music_choice,
                request_id="play")["admission"] == "ADMITTED"
    assert music_packets[-1]["interaction_quiet"]["status"] == "ACTIVE_QUALIFIED_INSTRUMENT"
    assert music_packets[-1]["interaction_quiet"]["elapsed"] == 0
    _run(music_state, "wait", music_choice, duration=1, request_id="music-sounding")
    assert music_packets[-1]["interaction_quiet"]["elapsed"] == 0
    assert _run(music_state, "stop-playing", music_choice,
                request_id="stop")["admission"] == "ADMITTED"
    assert music_packets[-1]["interaction_quiet"]["status"] == "NO_ACTOR_QUALIFIED_INTERPERSONAL_INTERRUPTION"
    assert music_packets[-1]["interaction_quiet"]["elapsed"] <= 1
    assert music_packets[-1]["scene_elapsed"] > music_packets[0]["scene_elapsed"]



def test_unheard_instrument_does_not_become_subjective_active_sound(tmp_path, monkeypatch):
    import run_p6
    state = tmp_path / "world"
    real_install = run_p6.establish_demo_conditions

    def obstructed(session):
        real_install(session)
        world, house = read_house(session)
        house["situated_conditions"]["sound_path"] = "obstructed"
        session.product._checkpoint(session.branch_id, world.clock, world)
    monkeypatch.setattr(run_p6, "establish_demo_conditions", obstructed)
    packets = []

    def choose(packet):
        packets.append(packet)
        return _decision()

    _run(state, "new", choose, situated_house=True)
    assert _run(state, "go", choose, target="living room",
                request_id="go")["admission"] == "ADMITTED"
    assert _run(state, "play", choose, request_id="play")["admission"] == "ADMITTED"
    played = json.loads((state / "p4_receipts.json").read_text())["turns"][-1]
    music_id = played["receipt"]["performed"]["event_id"]
    assert "situated" not in played["receipt"]
    _run(state, "wait", choose, duration=1, request_id="quiet")
    assert packets[-1]["interaction_quiet"]["status"] == "NO_ACTOR_QUALIFIED_INTERPERSONAL_INTERRUPTION"
    assert packets[-1]["interaction_quiet"]["last_break_event_id"] != music_id
    assert packets[-1]["interaction_quiet"]["elapsed"] > 0



def test_workshop_producer_does_not_repair_actor_from_living_room_and_return_restores_eligibility(tmp_path):
    state = tmp_path / "world"
    moves = 0

    def choose(packet):
        nonlocal moves
        if ("visit_adjacent_room" in packet["available_actions"]
                and moves < 2 and packet["elapsed"] >= 2):
            moves += 1
            return _decision("visit_adjacent_room")
        return _decision()

    _run(state, "new", choose, situated_house=True)
    _run(state, "wait", choose, duration=2, request_id="move-out")
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.world().positions["A"] == "living room"
        before = [e["event_id"] for e in session.events() if e["kind"] == "REPAIR"
                  and e["actor_id"] == "A"]
    finally:
        owner.close()
    _run(state, "wait", choose, duration=1, request_id="away-work")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    off = ledger["turns"][-1]["receipt"]["interval"]
    assert off["segments"][-1]["attempt"]["inputs"]["actor_present"] is False
    assert off["mode"] == "BLOCKED"
    assert off["segments"][-1]["attempt"]["attempt"] == "BLOCKED"
    assert off["segments"][-1]["world"]["status"] == "NOT_PERFORMED"
    assert not off["segments"][-1]["coverage"]
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert [e["event_id"] for e in session.events() if e["kind"] == "REPAIR"
                and e["actor_id"] == "A"] == before
    finally:
        owner.close()
    _run(state, "wait", choose, duration=2, request_id="move-back")
    owner = open_owner(state / "actual-p2")
    try:
        assert owner.base_owner.fanin.session.world().positions["A"] == "workshop"
    finally:
        owner.close()
    _run(state, "wait", choose, duration=1, request_id="resumed-work")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    resumed = ledger["turns"][-1]["receipt"]["interval"]["segments"][-1]
    assert resumed["attempt"]["inputs"]["actor_present"] is True


@pytest.mark.parametrize("failure_site", ["after_event_before_user_perception", "after_perception_before_episode", "after_episode_before_checkpoint", "after_complete_writer_before_p4"])
def test_interrupted_write_stays_pending_and_cannot_replay_ambiguous_move(
        tmp_path, monkeypatch, failure_site):
    import actor_initiative
    import situated
    state = tmp_path / "world"

    def choose(packet):
        return _decision("visit_adjacent_room")

    _run(state, "new", choose, situated_house=True)
    if failure_site != "after_complete_writer_before_p4":
        owner = open_owner(state / "actual-p2")
        try:
            product_cls = type(owner.base_owner.fanin.session.product)
        finally:
            owner.close()
        if failure_site == "after_event_before_user_perception":
            original = product_cls._perceive

            def crash_perception(self, branch, actor, event, channel="co_present"):
                if channel.startswith("p6_sourcefree_actor_move_"):
                    raise RuntimeError("injected after event before user perception")
                return original(self, branch, actor, event, channel)
            monkeypatch.setattr(product_cls, "_perceive", crash_perception)
        elif failure_site == "after_perception_before_episode":
            original = product_cls._append_episode

            def crash_episode(self, branch, actor, kind, clock, body):
                if kind == "P6_SITUATED_ACTOR_CONDUCT":
                    raise RuntimeError("injected after perception before episode")
                return original(self, branch, actor, kind, clock, body)
            monkeypatch.setattr(product_cls, "_append_episode", crash_episode)
        else:
            original = product_cls._checkpoint

            def crash_checkpoint(self, branch, clock, world, actors=None):
                last = world.events[-1] if world.events else {}
                if (last.get("kind") == "MOVE" and last.get("actor_id") == "A"
                        and last.get("body", {}).get("actor_action") == "visit_adjacent_room"):
                    raise RuntimeError("injected after episode before checkpoint")
                return original(self, branch, clock, world, actors)
            monkeypatch.setattr(product_cls, "_checkpoint", crash_checkpoint)
    else:
        original = situated.visit_adjacent_room

        def crash_after_writer(*args, **kwargs):
            result = original(*args, **kwargs)
            assert result["admitted"]
            raise RuntimeError("injected after checkpoint before P4 ledger")
        monkeypatch.setattr(situated, "visit_adjacent_room", crash_after_writer)

    with pytest.raises(RuntimeError, match="injected"):
        _run(state, "wait", choose, duration=2, request_id="interrupted")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    assert ledger["pending"]["request_id"] == "interrupted"
    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        moves = [e for e in session.events()
                 if e["kind"] == "MOVE" and e["actor_id"] == "A"
                 and e["body"].get("actor_action") == "visit_adjacent_room"]
        assert len(moves) <= 1
    finally:
        owner.close()
    with pytest.raises(RecursionRefusal, match="P4_PENDING_OPERATION_REQUIRES_RECONCILIATION"):
        _run(state, "wait", choose, duration=2, request_id="interrupted")
