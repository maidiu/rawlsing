from argparse import Namespace
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys

import pytest

from run_p5 import RecursionRefusal, experience, open_owner
from p3 import test_rules


def test_ordinary_encounter_returns_before_work_and_reopens(tmp_path, monkeypatch):
    state = tmp_path / "encounter"

    def act(command, **kwargs):
        args = {"request_id": None, "then_wait": False, **kwargs}
        return experience(state, Namespace(command=command, **args))

    def ledger():
        return json.loads((state / "p4_receipts.json").read_text())

    opening = act("new", history="recognized_plan")
    original = ledger()
    with monkeypatch.context() as cut:
        cut.setattr(test_rules, "B1_PATH", tmp_path / "missing-b1")
        with pytest.raises(RecursionRefusal, match="P3_B1_SOURCE_SEVERED"):
            act("say", text="Could we look at this edge?", request_edge=True)
    assert ledger() == original
    first = act("say", text="Could we look at this edge?", request_edge=True)
    assert first["clock"] == opening["clock"]
    invite = first["invitation"]
    assert invite and first["narration"][-1]["event_id"] == invite
    assert ledger()["turns"][-1]["receipt"]["interval"] is None
    pending = ledger()
    with pytest.raises(RecursionRefusal, match="P5_INVITATION_REQUIRES_EXPLICIT_RESPONSE"):
        act("attend")
    assert ledger() == pending
    with pytest.raises(RecursionRefusal, match="P5_OCCURRENCE_UNAVAILABLE"):
        act("orient", event_id="unperceived-occurrence")
    assert ledger() == pending
    refused = act("inspect-edge", invitation="unknown")
    assert not refused["performed"]
    assert refused["clock"] == first["clock"] and refused["invitation"] == invite

    speech_history = [
        row["event_id"] for row in first["narration"]
        if "say" in row["text"]
    ]
    assert len(speech_history) == 2
    for ref in speech_history:
        act("orient", event_id=ref)
    inspected = act("inspect-edge", invitation=invite)
    assert inspected["clock"] == first["clock"] + 3
    assert inspected["invitation"] is None
    before = ledger()
    turn = before["turns"][-1]
    segment = turn["receipt"]["interval"]["segments"][0]
    work = segment["world"]
    repair = work["actual_action_event_id"]
    inspection = turn["receipt"]["performed"]["event_id"]
    assert work["state_before"]["material_remaining"] == 2
    assert work["state_after"]["material_remaining"] == 1
    assert turn["receipt"]["performed"]["clock"] == segment["start"] == first["clock"]

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert {repair, inspection} <= session.user_perceived_ids()
        assert session.event(repair)["hash"] == work["actual_action_event_hash"]
        assert session.event(repair)["clock"] == first["clock"]
        assert owner.snapshot().document() == turn["after"]
    finally:
        owner.close()

    speech_view = act("view")
    assert [row["event_id"] for row in speech_view["narration"]] == speech_history

    # Replay the other practice against exactly the same completed world.
    gaze = state / "p5_gaze.json"
    gaze.unlink()
    act("orient", event_id=inspection)
    work_view = act("orient", event_id=repair)
    assert [row["event_id"] for row in work_view["narration"]] == [inspection, repair]
    assert work_view["choices"] == speech_view["choices"]
    assert ledger() == before

    cold = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("run_p5.py")),
         "--state", str(state), "view"], check=True, capture_output=True, text=True,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=60,
    )
    assert json.loads(cold.stdout) == work_view

    # The conduct contrast starts with one unit of real work remaining.
    baseline = tmp_path / "baseline"
    shutil.copytree(state, baseline)
    attended = act("attend")
    assert attended["clock"] == inspected["clock"] + 1
    interval = ledger()["turns"][-1]["receipt"]["interval"]
    second_work = interval["segments"][0]["world"]
    assert second_work["state_before"]["material_remaining"] == 1
    assert second_work["state_after"]["material_remaining"] == 0
    assert second_work["actual_action_event_id"] != repair
    assert attended["narration"] == [{
        "event_id": second_work["actual_action_event_id"], "text": "Nadia makes a repair.",
    }]

    quiet = act("attend")
    assert quiet["clock"] == attended["clock"] + 1
    assert ledger()["turns"][-1]["receipt"]["interval"]["segments"][0]["world"][
        "actual_action_event_id"] == ""
    assert quiet["narration"] == []


    # Branch from the same cold checkpoint at the same path. P2 binds its
    # store to that path, so copied baselines only run after restoration.
    state.rename(tmp_path / "ordinary-continuation")
    shutil.copytree(baseline, state)
    utterance = "Could we look at the edge once more?"
    work_request = act("say", text=utterance, request_edge=True)
    work_world = ledger()
    assert work_request["invitation"]
    assert work_world["turns"][-1]["receipt"]["interval"] is None

    state.rename(tmp_path / "work-continuation")
    shutil.copytree(baseline, state)
    gaze.unlink()
    for ref in speech_history:
        act("orient", event_id=ref)
    speech_request = act("say", text=utterance, request_edge=True)
    assert speech_request == work_request
    assert ledger() == work_world

    state.rename(tmp_path / "speech-continuation")
    shutil.copytree(baseline, state)
    plain = act("say", text=utterance, request_edge=False)
    plain_turn = ledger()["turns"][-1]
    assert plain["performed"] and plain["invitation"] is None
    assert plain_turn["before"] == work_world["turns"][-1]["before"]
    assert plain_turn["receipt"]["speech"]["attempt"]["text"] == utterance
    assert plain_turn["receipt"]["uptake"]["status"] == "PERCEIVED_NO_INSPECTION_REQUEST"
    assert plain_turn["receipt"]["expression"] is None
    assert plain["clock"] == inspected["clock"] + 1
    plain_work = plain_turn["receipt"]["interval"]["segments"][0]["world"]
    assert plain_work["actual_action_event_id"]
    assert plain_work["state_before"]["material_remaining"] == 1
    assert plain_work["state_after"]["material_remaining"] == 0


def test_deliberate_sustained_inspection_advances_two_work_periods(tmp_path):
    experience(tmp_path, Namespace(command="new", history="recognized_plan"))
    result = experience(tmp_path, Namespace(command="inspect", request_id=None, thorough=True))
    ledger = json.loads((tmp_path / "p4_receipts.json").read_text())
    turn = ledger["turns"][0]
    start = turn["before"]["clock"]
    assert turn["action"]["thorough"] is True
    assert result["clock"] == start + 6
    segments = turn["receipt"]["interval"]["segments"]
    assert [(row["start"], row["end"]) for row in segments] == [
        (start, start + 3), (start + 3, start + 6),
    ]
    assert [row["world"]["state_after"]["material_remaining"] for row in segments] == [1, 0]
    assert [line["event_id"] for line in result["narration"]] == [
        row["world"]["actual_action_event_id"] for row in segments
    ]
