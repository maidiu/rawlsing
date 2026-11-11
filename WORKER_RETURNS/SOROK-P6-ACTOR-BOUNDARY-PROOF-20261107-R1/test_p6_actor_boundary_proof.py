"""Sourcefree P6 SAY input/output and private-gaze isolation proof."""
from __future__ import annotations

import json
import shutil
from argparse import Namespace
from pathlib import Path
import sys

P6 = Path(__file__).resolve().parents[1] / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

import run_p6
from run_p6 import experience

TEXT = "Could we look at the edge?"
PROFILE = {
    "history": [{
        "target": "mug", "turn": 0, "shown": False,
        "available": ["bench", "mug"],
    }],
    "exposure": {"room": "workshop", "detail": "mug"},
}


def _call(state, **kwargs):
    return experience(state, Namespace(command="say", request_id=None, **kwargs))


def _turn(state):
    ledger = json.loads((state / "p4_receipts.json").read_text())
    assert ledger["turns"]
    return ledger["turns"][-1]


def _material(turn):
    receipt = turn["receipt"]
    return {
        "speech": receipt["speech"],
        "uptake": receipt["uptake"],
        "expression": receipt["expression"],
        "interval": receipt["interval"],
    }


def _prepare(tmp_path):
    state = tmp_path / "state"
    run_p6.experience(state, Namespace(command="new", request_id=None))
    base = tmp_path / "base"
    shutil.copytree(state, base)
    return state, base


def _variant(tmp_path, base, name, *, edge, profile=None):
    state = tmp_path / "state"
    if state.exists():
        state.rename(tmp_path / f"old-{name}")
    shutil.copytree(base, state)
    if profile is not None:
        (state / "p6_gaze.json").write_text(json.dumps(profile), encoding="utf-8")
    result = _call(state, text=TEXT, request_edge=edge)
    turn = _turn(state)
    state.rename(tmp_path / name)
    return result, turn


def test_p6_actor_input_output_and_private_gaze_isolation(tmp_path):
    _, base = _prepare(tmp_path)
    plain_result, plain_turn = _variant(tmp_path, base, "plain", edge=False)
    edge_result, edge_turn = _variant(tmp_path, base, "edge", edge=True)
    profile_result, profile_turn = _variant(
        tmp_path, base, "profile", edge=False, profile=PROFILE)

    plain = _material(plain_turn)
    edge = _material(edge_turn)
    prof = _material(profile_turn)

    assert plain["speech"]["attempt"]["text"] == TEXT
    assert plain["speech"]["attempt"]["request_edge"] is False
    assert plain["speech"]["performed"]["body"]["text"] == TEXT
    assert plain["speech"]["performed"]["body"]["request_edge"] is False
    assert plain["uptake"]["status"] == "PERCEIVED_NO_INSPECTION_REQUEST"
    assert plain["expression"] is None
    assert plain["interval"]["segments"][0]["world"]["actual_action_event_id"]
    assert plain["interval"]["segments"][0]["world"]["state_after"]["material_remaining"] < \
        plain["interval"]["segments"][0]["world"]["state_before"]["material_remaining"]
    assert plain_result["clock"] > edge_result["clock"]

    assert edge["speech"]["attempt"]["request_edge"] is True
    assert edge["speech"]["performed"]["body"]["request_edge"] is True
    assert edge["uptake"]["status"] == "UPTAKE"
    assert edge["expression"] is not None
    assert edge["expression"]["kind"] == "SPEECH"
    assert edge["interval"] is None
    assert edge_result["invitation"] == edge["expression"]["event_id"]
    assert plain_result["invitation"] is None
    assert edge["uptake"]["readset"] != plain["uptake"]["readset"]

    assert profile_result["detail"] != plain_result["detail"]
    assert prof == plain
    assert profile_result["narration"] == plain_result["narration"]
    assert profile_result["clock"] == plain_result["clock"]
    assert profile_result["room"] == plain_result["room"]
    assert profile_result["admission"] == plain_result["admission"]
    assert profile_result["invitation"] == plain_result["invitation"]
    assert (profile_turn["before"], profile_turn["after"]) == (
        plain_turn["before"], plain_turn["after"])
