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


def test_house_say_uses_live_recruitment_and_replays_without_retransduction(tmp_path):
    calls = []

    def transduce(*, event_id, event_hash, text):
        calls.append(event_id)
        return {"event_id": event_id, "event_hash": event_hash, "hypotheses": [
            {"move": "REQUEST" if len(calls) == 1 else "ASSERTION",
             "referent": "CURRENT_EDGE" if len(calls) == 1 else None,
             "span": [0, len(text)], "uncertain": False}
        ]}

    experience(tmp_path, Namespace(command="new"))
    first = Namespace(command="say", request_id="first", request_edge=False,
                      text="Could we go over the edge together?")
    second = Namespace(command="say", request_id="second", request_edge=False,
                       text="I'll let you get on with it.")
    answer = experience(tmp_path, first, transduce=transduce)
    assert any("Come look at this edge with me." in row["text"] for row in answer["narration"])
    experience(tmp_path, second, transduce=transduce)
    ledger_path = tmp_path / "p4_receipts.json"
    before_retry = ledger_path.read_bytes()
    experience(tmp_path, second, transduce=transduce)
    assert len(calls) == 2
    assert ledger_path.read_bytes() == before_retry
    turns = json.loads(before_retry)["turns"]
    assert len(turns) == 2
    assert turns[0]["receipt"]["uptake"]["mode"] == "joint_check"
    assert turns[1]["receipt"]["uptake"]["status"] == "SEMANTIC_VALID_EMPTY"
    assert turns[1]["receipt"]["expression"] is None
