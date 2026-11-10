from argparse import Namespace
import json

import pytest

from run_p6 import RecursionRefusal, experience, open_owner, read_house


def test_house_reopens_with_two_separate_closure_triggers(tmp_path):
    def run(command, **args):
        return experience(tmp_path, Namespace(command=command, request_id=None, **args))

    def canonical_house():
        owner = open_owner(tmp_path / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            _, house = read_house(session)
            return house, session.episodes("A"), session.user_perceived_ids()
        finally:
            owner.close()

    opening = run("new")
    house, _, _ = canonical_house()
    assert house["objects"]["sandals"]["room"] == "living room"
    assert set(house["history"]) == {"strap-repair"}
    assert "sandals" not in opening["available"]
    assert run("look", target="sandals")["admission"] == "UNAVAILABLE"
    assert run("view")["clock"] == opening["clock"]

    adjacent = run("go", target="living room")
    assert adjacent["clock"] == opening["clock"] + 1
    moved = json.loads((tmp_path / "p4_receipts.json").read_text())["turns"][-1]["receipt"]
    assert all(row["modality"] is None and row["eligibility"] == "UNKNOWN"
               and row["uptake"] == "HOLD_SENSORY_SOURCE_UNQUALIFIED"
               for row in moved["encounter_evidence"])
    house, episodes, perceived = canonical_house()
    assert set(house["history"]) == {"strap-repair", "bench-installation"}
    closure = next(row for row in episodes if row["kind"] == "P6_OBJECT_CLOSURE")
    assert closure["body"]["source_event_id"] not in perceived
    assert "bench-installation" not in json.dumps(adjacent)

    looked = run("look", target="sandals")
    assert looked["clock"] == adjacent["clock"] + 3
    assert any("Blue thread" in row["text"] for row in looked["narration"])
    assert "photo-exposure" not in json.dumps(looked)
    house, _, _ = canonical_house()
    assert house["history"]["photo-exposure"]["clock"] > house["history"]["strap-repair"]["clock"]
    assert looked["detail"] != adjacent["detail"]

    photo = run("look", target="photo")
    assert any("In the photograph" in row["text"] for row in photo["narration"])
    assert run("go", target="workshop")["room"] == "workshop"
    assert canonical_house()[0] == house
    with pytest.raises(RecursionRefusal, match="P6_HOUSE_SOURCE_OR_ROOT_MISMATCH"):
        from unittest.mock import patch
        with patch("house.SOURCE", "severed"):
            run("view")


def test_committed_go_qualifies_actor_specific_fixture_without_registering(tmp_path, monkeypatch):
    from copy import deepcopy
    from pathlib import Path
    import shutil
    import subprocess
    import sys

    import house
    import run_p6
    from encounter import VISUAL_FIXTURE, VISUAL_SOURCE

    state = tmp_path / "world"
    saved = tmp_path / "opening"
    establish = run_p6.establish

    with_visual_source = True

    def establish_fixture(session):
        establish(session)
        world, resource = read_house(session)
        world.positions["B"] = "workshop"
        if with_visual_source:
            resource["movement_visual_fixture"] = {
                "source": VISUAL_SOURCE, "facts": deepcopy(VISUAL_FIXTURE),
            }
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish", establish_fixture)
    experience(state, Namespace(command="new"))
    experience(state, Namespace(command="go", target="living room", request_id="out"))
    shutil.copytree(state, saved)

    opening_owner = open_owner(state / "actual-p2")
    try:
        psyche_before = opening_owner.store.head()
    finally:
        opening_owner.close()

    real_reader = house.movement_evidence

    def check_source_faults(session, event, world, resource):
        if event["location"] == "workshop":
            forged = {**event, "event_id": "uncommitted-move"}
            with pytest.raises(RecursionRefusal, match="P6_ENCOUNTER_MOVEMENT_SOURCE_MISMATCH"):
                real_reader(session, forged, world, resource)
            for change in ({"hash": "0" * 64}, {"actor_id": "A"}, {"clock": event["clock"] - 1}):
                with pytest.raises(RecursionRefusal, match="P6_ENCOUNTER_MOVEMENT_SOURCE_MISMATCH"):
                    real_reader(session, {**event, **change}, world, resource)
            for key in ("root", "branch"):
                with pytest.raises(RecursionRefusal, match="P6_ENCOUNTER_MOVEMENT_SOURCE_MISMATCH"):
                    real_reader(session, event, world, {**resource, key: "foreign"})
            with monkeypatch.context() as fault:
                fault.setattr(session, "episodes", lambda _actor: [])
                with pytest.raises(RecursionRefusal, match="P6_ENCOUNTER_MOVEMENT_PARENT_MISSING"):
                    real_reader(session, event, world, resource)
            no_fixture = {k: v for k, v in resource.items() if k != "movement_visual_fixture"}
            assert all(row["eligibility"] == "UNKNOWN"
                       for row in real_reader(session, event, world, no_fixture))
        return real_reader(session, event, world, resource)

    monkeypatch.setattr(house, "movement_evidence", check_source_faults)
    variants = []
    for focus in ("bench", "mug"):
        shutil.rmtree(state)
        shutil.copytree(saved, state)
        (state / "p6_gaze.json").write_text(json.dumps({
            "history": [{"target": focus, "turn": 0, "shown": False}],
            "exposure": {"room": "workshop", "detail": focus},
        }))
        args = Namespace(command="go", target="workshop", request_id="in")
        result = experience(state, args)
        ledger_path = state / "p4_receipts.json"
        raw = ledger_path.read_bytes()
        turn = json.loads(raw)["turns"][-1]
        event = turn["receipt"]["performed"]
        evidence = turn["receipt"]["encounter_evidence"]
        assert "adp010_admission" not in turn["receipt"]
        assert [row["eligibility"] for row in evidence] == ["ELIGIBLE", "UNAVAILABLE"]
        assert all(row["event_hash"] == event["hash"] and row["clock"] == event["clock"]
                   for row in evidence)
        assert [row["uptake"] for row in evidence] == [
            "HOLD_ACTOR_REGISTRATION_OWNER_MISSING", "NOT_ELIGIBLE_FOR_REGISTRATION",
        ]
        assert "encounter_evidence" not in json.dumps(result)
        if focus == "bench":
            replay = subprocess.run(
                [sys.executable, "-B", str(Path(__file__).with_name("run_p6.py")),
                 "--state", str(state), "go", "workshop", "--request-id", "in"],
                capture_output=True, text=True, timeout=90,
            )
            assert replay.returncode == 0, replay.stdout + replay.stderr
            assert json.loads(replay.stdout)["clock"] == result["clock"]
        assert ledger_path.read_bytes() == raw

        owner = open_owner(state / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            assert session.event(event["event_id"]) == event
            assert owner.store.head() == psyche_before
            assert sum(row["kind"] == "MOVE" and row["actor_id"] == event["actor_id"]
                       for row in session.events()) == 2
            [parent] = [row for row in session.episodes(session.meta["user_actor"])
                        if row["kind"] == "P6_HOUSE_CONDUCT"
                        and row["body"]["event_id"] == event["event_id"]]
            assert {row["conduct_parent"] for row in evidence} == {parent["episode_id"]}
            for actor in ("A", "B"):
                assert not any(row["event_id"] == event["event_id"]
                               for row in session.product.store.perceptions(session.branch_id, actor))
            assert not any(row["kind"] == "SPEECH" and row["clock"] == event["clock"]
                           and row["actor_id"] == "A" for row in session.events())
        finally:
            owner.close()
        variants.append((result["detail"], event, evidence))
    assert variants[0][0] != variants[1][0]
    assert variants[0][1:] == variants[1][1:]

    # An independently established matching scene omits the fixture source.
    # The same ordinary return GO still commits, but nobody gains access.
    with_visual_source = False
    unknown = tmp_path / "without-visual-source"
    experience(unknown, Namespace(command="new"))
    experience(unknown, Namespace(command="go", target="living room", request_id="out"))
    experience(unknown, Namespace(command="go", target="workshop", request_id="in"))
    unknown_turn = json.loads((unknown / "p4_receipts.json").read_text())["turns"][-1]
    unknown_move = unknown_turn["receipt"]["performed"]
    assert unknown_move["kind"] == "MOVE"
    assert unknown_move["clock"] == variants[0][1]["clock"]
    assert unknown_move["body"] == variants[0][1]["body"]
    for row in unknown_turn["receipt"]["encounter_evidence"]:
        assert row["modality"] is row["modality_source"] is None
        assert row["eligibility"] == "UNKNOWN"
        assert row["uptake"] == "HOLD_SENSORY_SOURCE_UNQUALIFIED"


def test_silent_interval_reconsiders_and_commits_only_admitted_speech(tmp_path):
    packets = []
    words = "I'll finish this piece first."

    def interpret(packet):
        packets.append(packet)
        action = "continue" if len(packets) == 1 else "speak"
        return {"attention": "uncertain", "interpretation": "Time to reassess the work.",
                "action": action}

    def realize(packet, decision):
        assert decision["action"] == "speak"
        return words

    def run(command, **args):
        return experience(tmp_path, Namespace(command=command, **args), interpret=interpret,
                          realize=realize, actor_context={"grade": "SOURCEFREE_FIXTURE",
                                                          "priority": "finish the piece"})

    start = run("new")["clock"]
    run("go", target="living room", request_id="away")
    first = run("wait", duration=4, request_id="wait-1")
    second = run("wait", duration=7, request_id="wait-2")
    assert first["clock"] == start + 5 and second["clock"] == start + 12
    assert [packet["elapsed"] for packet in packets] == [4, 7]
    assert all(packet["room"] == "workshop" and not packet["cues"] for packet in packets)
    assert all(packet["actor_context"]["priority"] == "finish the piece" for packet in packets)
    assert "situated" not in json.dumps(second)
    ledger = tmp_path / "p4_receipts.json"
    saved = ledger.read_bytes()
    turns = json.loads(saved)["turns"]
    assert turns[-2]["receipt"]["situated"]["decision"]["action"] == "continue"
    speech = turns[-1]["receipt"]["situated"]["speech"]
    assert speech["admitted"]
    assert run("wait", duration=7, request_id="wait-2")["clock"] == second["clock"]
    assert len(packets) == 2 and ledger.read_bytes() == saved

    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        event = session.event(speech["event_id"])
        assert event["kind"] == "SPEECH" and event["actor_id"] == "A"
        assert event["body"]["text"] == words
        assert speech["event_id"] not in session.user_perceived_ids()
    finally:
        owner.close()


@pytest.mark.parametrize("sound_path", ["audible", "obstructed"])
def test_outward_conduct_supplies_only_qualified_cues(tmp_path, monkeypatch, sound_path):
    import run_p6

    establish = run_p6.establish

    def establish_conditions(session):
        establish(session)
        world, house = read_house(session)
        house["situated_conditions"] = {
            "grade": "SOURCEFREE_FIXTURE", "hearing": "available", "sound_path": sound_path,
            "bench_view": "facing_away" if sound_path == "audible" else "facing_player",
            "footsteps": "audible",
        }
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish", establish_conditions)
    cues = []

    def interpret(packet):
        cues.append(packet["cues"][0])
        return {"attention": "noticed", "interpretation": "A possible cue.",
                "action": "continue"}

    def run(command, **args):
        return experience(tmp_path, Namespace(command=command, **args), interpret=interpret)

    run("new")
    (tmp_path / "p6_gaze.json").write_text(json.dumps({
        "history": [], "exposure": {"room": "workshop", "detail": "A"},
    }))
    run("view")
    assert not cues
    run("approach", request_id="approach")
    assert cues[0]["kind"] == "APPROACH"
    assert "AUDITORY" in cues[0]["channels"]
    run("orient", request_id="outward-orientation")
    if sound_path == "audible":
        assert len(cues) == 1 and "VISUAL" not in cues[0]["channels"]
        assert "oriented_toward_actor" not in cues[0]["detail"]
    else:
        assert cues[1]["kind"] == "ORIENT" and cues[1]["channels"] == ["VISUAL"]
        assert cues[1]["detail"] == {"near": True, "oriented_toward_actor": True}
    run("go", target="living room", request_id="away")
    run("play", request_id="music")
    run("stop-playing", request_id="stop")
    receipts = [turn["receipt"] for turn in json.loads(
        (tmp_path / "p4_receipts.json").read_text())["turns"]]
    assert receipts[1]["performed"]["body"]["oriented_toward"] is True
    assert [row["performed"]["kind"] for row in receipts[-2:]] == [
        "PLAY_INSTRUMENT", "STOP_INSTRUMENT",
    ]
    if sound_path == "audible":
        assert [cue["channels"] for cue in cues[1:]] == [["AUDITORY"], ["AUDITORY"]]
        assert [cue["detail"]["sounding"] for cue in cues[1:]] == [True, False]
        assert all(row["situated"]["decision"]["action"] == "continue" for row in receipts[-2:])
        assert all(row["situated"]["decision"]["attention"] == "noticed" for row in receipts[-2:])
    else:
        assert len(cues) == 2 and all("situated" not in row for row in receipts[-2:])
