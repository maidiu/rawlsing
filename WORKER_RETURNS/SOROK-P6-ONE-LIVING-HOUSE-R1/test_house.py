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
    import shutil

    state = tmp_path / "world"
    branch_point = tmp_path / "branch-point"
    packets = []
    words = "Are you still there?"

    def interpret(packet):
        packets.append(packet)
        context = packet["actor_context"]
        if context is None:
            return {"attention": "noticed", "interpretation": "I saw a person.",
                    "action": "speak", "cue_event_id": "foreign", "channel": "VISUAL"}
        action = "speak" if context["priority"] == "check whether my collaborator is ready" else "continue"
        return {"attention": "uncertain", "interpretation": "Time to reassess the work.",
                "action": action, "cue_event_id": None, "channel": None}

    def realize(packet, decision):
        assert decision["action"] == "speak" and "interpretation" not in decision
        return words

    def run(command, context=None, **args):
        return experience(state, Namespace(command=command, **args), interpret=interpret,
                          realize=realize, actor_context=context)

    start = run("new")["clock"]
    run("go", target="living room", request_id="away")
    owner = open_owner(state / "actual-p2")
    try:
        actor = owner.base_owner.fanin.session.world().actor_state["A"]["actor_id"]
        psyche = owner.store.head()
    finally:
        owner.close()

    base = {"grade": "SOURCEFREE_FIXTURE", "actor_id": actor,
            "analyst_only": "private analyst note", "user_intention": "private player intention"}
    finish = {**base, "priority": "finish the piece", "relationship": "visitor"}
    collaborate = {**base, "priority": "check whether my collaborator is ready",
                   "relationship": "working together"}
    first = run("wait", finish, duration=4, request_id="wait-1")
    assert first["clock"] == start + 5
    shutil.copytree(state, branch_point)

    ledger = state / "p4_receipts.json"
    alternative = run("wait", finish, duration=7, request_id="wait-2")
    alternative_turn = json.loads(ledger.read_text())["turns"][-1]
    assert alternative_turn["receipt"]["situated"]["decision"]["action"] == "continue"
    assert "speech" not in alternative_turn["receipt"]["situated"]

    shutil.rmtree(state)
    shutil.copytree(branch_point, state)
    second = run("wait", collaborate, duration=7, request_id="wait-2")
    assert second["clock"] == alternative["clock"] == start + 12
    assert [packet["elapsed"] for packet in packets] == [4, 7, 7]
    assert all(packet["room"] == "workshop" and not packet["cues"] for packet in packets)
    assert {key: value for key, value in packets[1].items() if key != "actor_context"} == {
        key: value for key, value in packets[2].items() if key != "actor_context"
    }
    assert packets[1]["actor_context"]["relationship"] == "visitor"
    assert packets[2]["actor_context"]["relationship"] == "working together"
    assert all("private" not in json.dumps(packet) for packet in packets)
    assert "situated" not in json.dumps(second)

    saved = ledger.read_bytes()
    turns = json.loads(saved)["turns"]
    speech = turns[-1]["receipt"]["situated"]["speech"]
    assert speech["admitted"]
    assert run("wait", collaborate, duration=7, request_id="wait-2")["clock"] == second["clock"]
    assert len(packets) == 3 and ledger.read_bytes() == saved

    run("wait", {**collaborate, "actor_id": "foreign"}, duration=1, request_id="foreign")
    assert packets[-1]["actor_context"] is None
    assert packets[-1]["recent_speech"][-1]["text"] == words
    assert packets[-1]["recent_speech"][-1]["event_id"] == speech["event_id"]
    assert "Time to reassess" not in json.dumps(packets[-1])
    refusal = json.loads(ledger.read_text())["turns"][-1]["receipt"]["situated"]
    assert refusal["status"] == "INVALID_INTERPRETATION" and "speech" not in refusal

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        event = session.event(speech["event_id"])
        assert event["kind"] == "SPEECH" and event["actor_id"] == "A"
        assert event["body"]["text"] == words
        assert speech["event_id"] not in session.user_perceived_ids()
        assert owner.store.head() == psyche
        assert [row["event_id"] for row in session.events() if row["kind"] == "SPEECH"
                and row["clock"] >= start] == [speech["event_id"]]
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
                "action": "continue", "cue_event_id": cues[-1]["event_id"],
                "channel": cues[-1]["channels"][0]}

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


def test_cli_situated_transport_and_provider_failure_preserve_turn(tmp_path, monkeypatch, capsys):
    import sys

    import run_p6
    from situated_provider import SituatedProvider

    monkeypatch.setenv("SOROK_SITUATED_MODEL_ENDPOINT", "http://127.0.0.1:1/chat/completions")
    monkeypatch.setenv("SOROK_SITUATED_SEMANTIC_MODEL", "test-semantic")
    monkeypatch.setenv("SOROK_SITUATED_EXPRESSIVE_MODEL", "test-expressive")
    calls = []
    real_request = SituatedProvider._request

    def transport(provider, role, model, payload):
        calls.append((model, payload))
        if len(calls) > 1:
            return real_request(provider, role, model, payload)
        return {"attention": "noticed", "interpretation": "Music may be coming through the doorway.",
                "action": "continue", "cue_event_id": payload["cues"][0]["event_id"],
                "channel": "AUDITORY"}

    monkeypatch.setattr(SituatedProvider, "_request", transport)

    def cli(*args):
        monkeypatch.setattr(sys, "argv", ["run_p6.py", "--state", str(tmp_path), *args])
        assert run_p6.main() == 0
        return json.loads(capsys.readouterr().out)

    cli("new", "--situated-house")
    cli("go", "living room")
    audible = cli("play", "--request-id", "play")
    closed = cli("stop-playing", "--request-id", "stop")
    assert closed["clock"] == audible["clock"] + 1
    assert cli("stop-playing", "--request-id", "stop")["clock"] == closed["clock"]
    assert [model for model, _ in calls] == ["test-semantic", "test-semantic"]
    assert calls[0][1]["actor_context"] == {
        "grade": "SOURCEFREE_FIXTURE",
        "priority": "Finish the current bench work while the material allows it.",
        "relationship": "A visitor in the workshop.",
        "routes": {
            "workshop": {
                "origin": "workshop", "destination": "living room",
                "source": "SOURCEFREE_ACTOR_LOCAL_ADJACENCY",
            },
            "living room": {
                "origin": "living room", "destination": "workshop",
                "source": "SOURCEFREE_ACTOR_LOCAL_ADJACENCY",
            },
        },
    }
    assert calls[0][1]["cues"][0]["detail"] == {"instrument": "mandolin", "sounding": True}
    ledger = json.loads((tmp_path / "p4_receipts.json").read_text())
    assert ledger["pending"] is None
    last_two = [turn["receipt"]["situated"] for turn in ledger["turns"][-2:]]
    assert [row["status"] for row in last_two] == ["INTERPRETED", "MODEL_UNAVAILABLE"]
    assert all(row["provider_mode"] == "CONFIGURED_TRANSPORT" for row in last_two)



def test_perception_claim_requires_exact_cue_and_channel():
    from situated import decision_is_grounded

    cues = [{"event_id": "music", "channels": ["AUDITORY"]}]
    decision = {"attention": "noticed", "interpretation": "Someone may be nearby.",
                "action": "speak", "cue_event_id": "music", "channel": "AUDITORY"}
    assert decision_is_grounded(decision, cues, ("speak",))
    assert not decision_is_grounded({**decision, "channel": "VISUAL"}, cues, ("speak",))
    assert not decision_is_grounded({**decision, "cue_event_id": "other"}, cues, ("speak",))


def test_cli_two_role_http_fixture_commits_visible_speech(tmp_path, monkeypatch, capsys):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import sys
    from threading import Thread

    import run_p6

    requests = []
    spoken = "Could you give me a hand with this?"

    class Fixture(BaseHTTPRequestHandler):
        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            payload = json.loads(request["messages"][-1]["content"])
            requests.append((request["model"], payload))
            if request["model"] == "fixture-semantic":
                response = {"attention": "uncertain", "interpretation": "Private hypothesis",
                            "action": "speak", "cue_event_id": None, "channel": None}
            else:
                response = {"text": spoken}
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"choices": [
                {"message": {"content": json.dumps(response)}},
            ]}).encode())

        def log_message(self, *_args):
            pass

    def cli(*args):
        monkeypatch.setattr(sys, "argv", ["run_p6.py", "--state", str(tmp_path), *args])
        assert run_p6.main() == 0
        return json.loads(capsys.readouterr().out)

    with ThreadingHTTPServer(("127.0.0.1", 0), Fixture) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        monkeypatch.setenv("SOROK_SITUATED_MODEL_ENDPOINT",
                           f"http://127.0.0.1:{server.server_port}/chat/completions")
        monkeypatch.setenv("SOROK_SITUATED_SEMANTIC_MODEL", "fixture-semantic")
        monkeypatch.setenv("SOROK_SITUATED_EXPRESSIVE_MODEL", "fixture-expressive")
        try:
            cli("new", "--situated-house")
            response = cli("wait", "1", "--request-id", "nearby")
            assert spoken in json.dumps(response["narration"])
            cli("wait", "1", "--request-id", "nearby")
        finally:
            server.shutdown()
            thread.join()

    assert [model for model, _ in requests] == ["fixture-semantic", "fixture-expressive"]
    assert "Private hypothesis" not in json.dumps(requests[-1][1])
    assert "Private hypothesis" not in json.dumps(response)
    ledger = json.loads((tmp_path / "p4_receipts.json").read_text())
    [turn] = ledger["turns"]
    speech = turn["receipt"]["situated"]["speech"]
    assert speech["admitted"]
    owner = open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert speech["event_id"] in session.user_perceived_ids()
        assert session.event(speech["event_id"])["body"]["text"] == spoken
    finally:
        owner.close()
