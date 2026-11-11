"""Reviewer-only early-construction adversarial probes for MII snapshot de373b08."""

from argparse import Namespace
import json
from pathlib import Path
import sys

from pytest import MonkeyPatch

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
    return experience(state, Namespace(command=command, request_id=None, **kwargs))


def test_viewer_observer_identity_is_not_enforced(tmp_path: Path, monkeypatch: MonkeyPatch):
    original = run_p6.establish

    def foreign_observer(session):
        original(session)
        world, house = read_house(session)
        house["presentation_conditions"]["observer"] = "B"
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish", foreign_observer)
    state = tmp_path / "foreign-observer"
    opening = _run(state, "new")
    assert opening["mii_surface"]["optional"] is not None
    assert opening["detail"] is not None


def test_unselected_available_look_gets_only_offered_weight(tmp_path: Path):
    state = tmp_path / "adaptive"
    _run(state, "new")
    _run(state, "go", target="living room")
    surface = _run(state, "view")["mii_surface"]
    target = surface["omitted_available"][0]
    assert surface["optional"]["target"] != target
    _run(state, "mii-enable-learning")
    _run(state, "look", target=target)
    profile = json.loads((state / "p6_gaze.json").read_text(encoding="utf8"))
    assert profile["hypotheses"][target]["weight"] == 1
    assert profile["hypotheses"][target]["uncertainty"] == "HIGH"


def test_forged_profile_recognition_is_accepted_as_committed(tmp_path: Path):
    state = tmp_path / "forged-recognition"
    _run(state, "new")
    _run(state, "go", target="living room")
    owner = open_owner(state / "actual-p2")
    try:
        profile_scope = mii.scope(owner.base_owner.fanin.session)
    finally:
        owner.close()
    profile = mii.default_profile(profile_scope)
    profile["recognized"]["coaster"] = {
        "object_id": "coaster",
        "identity": "forged canonical identity",
        "event_id": "invented-inspection-event",
        "turn": 1,
        "evidence": "never observed",
        "marking": "invented-marking",
    }
    mii.save_profile(state / "p6_gaze.json", profile)
    view = _run(state, "view")
    assert view["recognized_identity"] == "forged canonical identity"
    assert view["recognition_source"] == "COMMITTED_INSPECTION"
