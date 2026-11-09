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
    from pathlib import Path
    import subprocess
    import sys

    request = "Could we go over the edge together?"
    departure = "I'll let you get on with it."
    calls = []

    def transduce(*, event_id, event_hash, text):
        calls.append(event_id)
        move, referent = {
            request: ("REQUEST", "CURRENT_EDGE"),
            departure: ("ASSERTION", None),
        }[text]
        return {"event_id": event_id, "event_hash": event_hash, "hypotheses": [
            {"move": move, "referent": referent, "span": [0, len(text)], "uncertain": False}
        ]}

    experience(tmp_path, Namespace(command="new"))
    first = Namespace(command="say", request_id="first", request_edge=False, text=request)
    second = Namespace(command="say", request_id="second", request_edge=False, text=departure)
    answer = experience(tmp_path, first, transduce=transduce)
    assert any("Come look at this edge with me." in row["text"] for row in answer["narration"])
    silence = experience(tmp_path, second, transduce=transduce)
    ledger_path = tmp_path / "p4_receipts.json"
    before_retry = ledger_path.read_bytes()

    def snapshot():
        owner = open_owner(tmp_path / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            return list(session.events()), session.clock(), owner.store.head()
        finally:
            owner.close()

    before = snapshot()
    script = """
from argparse import Namespace
import json
from pathlib import Path
import sys
from run_p6 import experience

def unexpected(**_):
    raise AssertionError("completed request was retransduced")

state, request_id, text = sys.argv[1:]
args = Namespace(command="say", request_id=request_id, request_edge=False, text=text)
print(json.dumps(experience(Path(state), args, transduce=unexpected)))
"""
    for args, original in ((first, answer), (second, silence)):
        result = subprocess.run(
            [sys.executable, "-B", "-c", script, str(tmp_path), args.request_id, args.text],
            cwd=Path(__file__).parent, capture_output=True, text=True, timeout=90,
        )
        assert result.returncode == 0, result.stderr
        replay = json.loads(result.stdout)
        assert replay["admission"] == original["admission"]
        assert replay["clock"] == silence["clock"]
        assert ledger_path.read_bytes() == before_retry

    assert snapshot() == before
    assert len(calls) == 2
    turns = json.loads(before_retry)["turns"]
    assert len(turns) == 2
    assert turns[0]["receipt"]["uptake"]["mode"] == "joint_check"
    assert turns[1]["receipt"]["uptake"]["status"] == "SEMANTIC_VALID_EMPTY"
    assert turns[1]["receipt"]["expression"] is None


def test_live_say_access_and_private_gaze_counterfactual(tmp_path):
    import shutil

    state = tmp_path / "state"
    initial = tmp_path / "initial"
    experience(state, Namespace(command="new"))
    shutil.copytree(state, initial)
    utterance = Namespace(command="say", request_id="access", request_edge=False,
                          text="Could we go over the edge together?")
    inputs = []

    def transduce(*, event_id, event_hash, text):
        inputs.append((event_id, event_hash, text))
        return {"event_id": event_id, "event_hash": event_hash, "hypotheses": [
            {"move": "REQUEST", "referent": "CURRENT_EDGE",
             "span": [0, len(text)], "uncertain": False}
        ]}

    def restore():
        shutil.rmtree(state)
        shutil.copytree(initial, state)

    def receipt():
        return json.loads((state / "p4_receipts.json").read_text())["turns"][-1]["receipt"]

    variants = []
    for target in ("bench", "mug"):
        restore()
        (state / "p6_gaze.json").write_text(json.dumps({
            "history": [{"target": target, "turn": 0, "shown": False,
                         "available": ["bench", "mug"]}],
            "exposure": {"room": "workshop", "detail": target},
        }))
        view = experience(state, utterance, transduce=transduce)
        variants.append((view["detail"], receipt()))

    assert variants[0][0] != variants[1][0]
    assert inputs[0] == inputs[1]
    assert variants[0][1]["speech"] == variants[1][1]["speech"]
    assert variants[0][1]["uptake"] == variants[1][1]["uptake"]
    assert variants[0][1]["expression"] == variants[1][1]["expression"]
    assert variants[0][1]["expression"] is not None

    restore()
    experience(state, Namespace(command="go", target="living room", request_id="leave"))
    experience(state, utterance, transduce=transduce)
    separated = receipt()
    assert separated["speech"]["performed"]["body"]["text"] == utterance.text
    assert separated["speech"]["actor_access"] is None
    assert separated["uptake"]["status"] == "NOT_PERCEIVED"
    assert separated["expression"] is None
    assert len(inputs) == 2


def test_interrupted_live_say_cold_retry_holds_without_duplicate(tmp_path):
    from pathlib import Path
    import subprocess
    import sys

    experience(tmp_path, Namespace(command="new"))
    script = """
from argparse import Namespace
import os
from pathlib import Path
import sys
from run_p6 import RecursionRefusal, experience

def interrupt(**_):
    os._exit(73)

args = Namespace(command="say", request_id="interrupted", request_edge=False,
                 text="Could we check the edge together?")
try:
    experience(Path(sys.argv[1]), args, transduce=interrupt)
except RecursionRefusal as exc:
    print(exc)
    raise SystemExit(2)
"""
    command = [sys.executable, "-B", "-c", script, str(tmp_path)]
    options = {"cwd": Path(__file__).parent, "capture_output": True,
               "text": True, "timeout": 90}
    interrupted = subprocess.run(command, **options)
    assert interrupted.returncode == 73, interrupted.stderr
    ledger_path = tmp_path / "p4_receipts.json"
    pending = ledger_path.read_bytes()

    def committed_state():
        owner = open_owner(tmp_path / "actual-p2")
        try:
            session = owner.base_owner.fanin.session
            return list(session.events()), session.clock(), owner.store.head()
        finally:
            owner.close()

    before = committed_state()
    spoken = [row for row in before[0] if row["kind"] == "SPEECH"
              and row["body"].get("text") == "Could we check the edge together?"]
    assert len(spoken) == 1
    assert json.loads(pending)["pending"]["request_id"] == "interrupted"
    assert json.loads(pending)["turns"] == []

    retry = subprocess.run(command, **options)
    assert retry.returncode == 2, retry.stderr
    assert retry.stdout.strip() == "P4_PENDING_OPERATION_REQUIRES_RECONCILIATION"
    assert ledger_path.read_bytes() == pending
    assert committed_state() == before
