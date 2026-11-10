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
    import shutil

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
        assert [row["eligibility"] for row in evidence] == ["ELIGIBLE", "UNAVAILABLE"]
        assert all(row["event_hash"] == event["hash"] and row["clock"] == event["clock"]
                   for row in evidence)
        assert [row["uptake"] for row in evidence] == [
            "HOLD_ACTOR_REGISTRATION_OWNER_MISSING", "NOT_ELIGIBLE_FOR_REGISTRATION",
        ]
        assert "encounter_evidence" not in json.dumps(result)
        assert experience(state, args)["clock"] == result["clock"]
        assert ledger_path.read_bytes() == raw

        owner = open_owner(state / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            assert session.event(event["event_id"]) == event
            assert owner.store.head() == psyche_before
            parent = next(row for row in session.episodes(session.meta["user_actor"])
                          if row["kind"] == "P6_HOUSE_CONDUCT"
                          and row["body"]["event_id"] == event["event_id"])
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
