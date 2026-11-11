"""Reviewer-only adverse probe for MII checkpoint eb2e53d."""

from argparse import Namespace
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
P6 = ROOT / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P5 = ROOT / "WORKER_RETURNS" / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
P4 = ROOT / "WORKER_RETURNS" / "SOROK-P4-FIRST-FULL-MPC-R1"
P3 = ROOT / "WORKER_RETURNS" / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
for path in (P6, P5, P4, P3 / "tests"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import mii
import run_p6
from run_p6 import experience, open_owner, read_house


def _run(state, command, **kwargs):
    kwargs.setdefault("request_id", None)
    return experience(state, Namespace(command=command, **kwargs))


def test_exposure_ledger_omits_unselected_available_candidate(tmp_path):
    state = tmp_path / "world"
    opening = _run(state, "new")
    profile = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))
    entry = profile["exposures"][-1]
    assert opening["available"] == ["bench", "mug"]
    assert opening["mii_surface"]["omitted_available"] == ["mug"]
    assert "mug" not in entry["offered"]
    assert set(entry["offered"]) == {opening["mii_surface"]["optional"]["target"]}


def test_repaired_observer_identity_through_p6(tmp_path, monkeypatch):
    original = run_p6.establish

    def foreign_observer(session):
        original(session)
        world, house = read_house(session)
        house["presentation_conditions"]["observer"] = "B"
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish", foreign_observer)
    opening = _run(tmp_path / "foreign", "new")
    assert opening["mii_surface"]["optional"] is None
    assert opening["detail"] is None


def test_repaired_forged_recognition_is_not_rendered(tmp_path):
    state = tmp_path / "forged"
    _run(state, "new")
    _run(state, "go", target="living room")
    owner = open_owner(state / "actual-p2")
    try:
        profile_scope = mii.scope(owner.base_owner.fanin.session)
    finally:
        owner.close()
    profile = mii.default_profile(profile_scope)
    profile["recognized"]["coaster"] = {
        "object_id": "coaster", "identity": "forged identity",
        "event_id": "invented", "turn": 1,
        "evidence": "never observed", "marking": "invented",
    }
    mii.save_profile(state / "p6_gaze.json", profile)
    view = _run(state, "view")
    assert "forged identity" not in json.dumps(view["recognition"])
    assert view["recognized_identity"] is None


def test_repaired_offered_and_independent_weights(tmp_path):
    state = tmp_path / "adaptive"
    _run(state, "new")
    _run(state, "go", target="living room")
    surface = _run(state, "view")["mii_surface"]
    selected = surface["optional"]["target"]
    omitted = surface["omitted_available"][0]
    _run(state, "mii-enable-learning")
    _run(state, "look", target=selected)
    profile = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))
    assert profile["hypotheses"][selected]["weight"] == 1
    _run(state, "look", target=omitted)
    profile = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))
    assert profile["hypotheses"][omitted]["weight"] == 2
