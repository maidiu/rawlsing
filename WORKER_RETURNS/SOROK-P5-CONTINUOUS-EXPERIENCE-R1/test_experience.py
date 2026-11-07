from argparse import Namespace
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from run_p5 import RecursionRefusal, experience, open_owner


def test_ordinary_encounter_returns_before_work_and_reopens(tmp_path):
    def act(command, **kwargs):
        args = {"request_id": None, "then_wait": False, **kwargs}
        return experience(tmp_path, Namespace(command=command, **args))

    def ledger():
        return json.loads((tmp_path / "p4_receipts.json").read_text())

    opening = act("new", history="recognized_plan")
    first = act("say", text="Could we look at this edge?", request_edge=True)
    assert first["clock"] == opening["clock"]
    invite = first["invitation"]
    assert invite and first["narration"][-1]["event_id"] == invite
    assert ledger()["turns"][-1]["receipt"]["interval"] is None
    pending = ledger()
    with pytest.raises(RecursionRefusal, match="P5_INVITATION_REQUIRES_EXPLICIT_RESPONSE"):
        act("attend")
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
    assert work["state_before"]["material_remaining"] == 1
    assert work["state_after"]["material_remaining"] == 0
    assert turn["receipt"]["performed"]["clock"] == segment["start"] == first["clock"]

    owner = open_owner(tmp_path / "actual-p2")
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
    gaze = tmp_path / "p5_gaze.json"
    gaze.unlink()
    act("orient", event_id=inspection)
    work_view = act("orient", event_id=repair)
    assert [row["event_id"] for row in work_view["narration"]] == [inspection, repair]
    assert work_view["choices"] == speech_view["choices"]
    assert ledger() == before

    cold = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("run_p5.py")),
         "--state", str(tmp_path), "view"], check=True, capture_output=True, text=True,
        env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=60,
    )
    assert json.loads(cold.stdout) == work_view

    attended = act("attend")
    assert attended["clock"] == inspected["clock"] + 1
    interval = ledger()["turns"][-1]["receipt"]["interval"]
    assert interval["segments"][0]["world"]["actual_action_event_id"] == ""
    assert attended["narration"] == []
