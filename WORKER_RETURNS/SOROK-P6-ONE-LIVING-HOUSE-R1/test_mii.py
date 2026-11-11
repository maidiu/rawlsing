"""Mechanism II sourcefree presentation, exposure and control tests."""

from argparse import Namespace
import json
from pathlib import Path

import pytest

import mii
import run_p6
from run_p6 import experience, open_owner, read_house
from developmental_recursion.contracts import RecursionRefusal


def _run(state, command, **kwargs):
    kwargs.setdefault("request_id", None)
    return experience(state, Namespace(command=command, **kwargs))


def _profile(state):
    return json.loads((state / "p6_gaze.json").read_text())


def test_neutral_exposure_earned_recognition_and_cold_replay(tmp_path):
    state = tmp_path / "world"
    opening = _run(state, "new")
    profile = _profile(state)
    assert profile["schema"] == mii.SCHEMA
    assert profile["mode"] == "NEUTRAL"
    assert profile["learning_enabled"] is False
    assert profile["scope"]["user"] == "U"
    assert profile["exposures"][-1]["available"] == ["bench", "mug"]
    assert profile["exposures"][-1]["selection_basis"] == "NEUTRAL_AMBIENT"
    assert profile["exposures"][-1]["entry_hash"]
    assert opening["mii_surface"]["schema"] == mii.SURFACE_SCHEMA
    assert opening["mii_surface"]["mandatory"]
    assert all(row["event_id"] for row in opening["mii_surface"]["mandatory"])
    assert opening["mii_surface"]["budget"]["optional"] == 1

    _run(state, "go", target="living room")
    looked = _run(state, "look", target="sandals")
    assert looked["admission"] == "ADMITTED"
    assert looked["recognized_identity"] == "the repaired blue-thread sandals"
    assert looked["recognition_source"] == "COMMITTED_INSPECTION"
    profile = _profile(state)
    assert profile["recognized"]["sandals"]["event_id"]
    assert profile["recognition"]["seen"]["sandals"]["source"] == "COMMITTED_INSPECTION"
    assert profile["exposures"][-1]["prior_exposure"]["detail"] in {"coaster", "photo", "sandals"}

    owner = open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        scope = mii.scope(session)
    finally:
        owner.close()
    reopened = mii.load_profile(state / "p6_gaze.json", type("S", (), {
        "read_root": lambda self: {"root_hash": scope["root"]},
        "branch_id": scope["branch"],
        "meta": {"user_actor": scope["user"]},
    })())
    assert reopened["recognized"] == {}
    assert reopened["exposures"][-1]["entry_hash"] == profile["exposures"][-1]["entry_hash"]
    replay = _run(state, "view")
    assert replay["recognition"]["sandals"]["event_id"] == profile["recognized"]["sandals"]["event_id"]


def test_occluded_viewer_source_hides_detail_but_not_world_existence(tmp_path, monkeypatch):
    original = run_p6.establish

    def occluded(session):
        original(session)
        world, house = read_house(session)
        house["presentation_conditions"]["sightline"] = "occluded"
        session.product._checkpoint(session.branch_id, world.clock, world)

    with monkeypatch.context() as patch:
        patch.setattr(run_p6, "establish", occluded)
        state = tmp_path / "occluded"
        opening = _run(state, "new")
        assert opening["available"] == ["bench", "mug"]
        assert opening["detail"] is None
        assert opening["mii_surface"]["optional"] is None
        assert opening["mii_surface"]["omitted_available"] == []

        _run(state, "go", target="living room")
        view = _run(state, "view")
        assert view["available"] == ["coaster", "photo", "sandals"]
        assert view["detail"] is None
        refused = _run(state, "look", target="sandals")
        assert refused["admission"] == "UNAVAILABLE"
        assert refused["detail"] is None

    normal = tmp_path / "normal"
    _run(normal, "new")
    _run(normal, "go", target="living room")
    restored = _run(normal, "look", target="sandals")
    assert restored["admission"] == "ADMITTED"
    assert restored["recognized_identity"] == "the repaired blue-thread sandals"


def test_viewer_observer_identity_is_enforced(tmp_path, monkeypatch):
    original = run_p6.establish

    def foreign_observer(session):
        original(session)
        world, house = read_house(session)
        house["presentation_conditions"]["observer"] = "B"
        session.product._checkpoint(session.branch_id, world.clock, world)

    with monkeypatch.context() as patch:
        patch.setattr(run_p6, "establish", foreign_observer)
        state = tmp_path / "foreign-observer"
        opening = _run(state, "new")
    assert opening["available"] == ["bench", "mug"]
    assert opening["detail"] is None
    assert opening["mii_surface"]["optional"] is None
    assert opening["mii_surface"]["omitted_available"] == []


def test_forged_profile_recognition_is_not_trusted(tmp_path):
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
    assert "forged canonical identity" not in json.dumps(view["recognition"])
    assert view["recognized_identity"] is None
    assert view["recognition_source"] is None


def test_offered_and_independent_targeting_get_different_weight(tmp_path):
    state = tmp_path / "adaptive"
    _run(state, "new")
    _run(state, "go", target="living room")
    surface = _run(state, "view")["mii_surface"]
    selected = surface["optional"]["target"]
    omitted = surface["omitted_available"][0]
    _run(state, "mii-enable-learning")
    _run(state, "look", target=selected)
    profile = _profile(state)
    assert profile["hypotheses"][selected]["weight"] == 1
    assert profile["hypotheses"][selected]["uncertainty"] == "HIGH"
    _run(state, "look", target=omitted)
    profile = _profile(state)
    assert profile["hypotheses"][omitted]["weight"] == 2
    assert profile["hypotheses"][omitted]["uncertainty"] == "HIGH"


def test_duplicate_exposure_and_unknown_control_target_are_bounded(tmp_path):
    state = tmp_path / "world"
    _run(state, "new")
    _run(state, "go", target="living room")
    first = _run(state, "look", target="coaster", request_id="duplicate-look")
    profile = _profile(state)
    count = len(profile["exposures"])
    ledger = (state / "p4_receipts.json").read_bytes()
    second = _run(state, "look", target="coaster", request_id="duplicate-look")
    assert second["clock"] == first["clock"]
    assert len(_profile(state)["exposures"]) == count
    assert (state / "p4_receipts.json").read_bytes() == ledger
    with pytest.raises(RecursionRefusal, match="MII_TARGET_UNKNOWN"):
        _run(state, "mii-learn-label", target="not-an-object", label="invented")

    (state / "p6_gaze.json").write_text("{not-json", encoding="utf8")
    recovered = _run(state, "view")
    assert recovered["mii"]["reset_reason"] == "CORRUPT_PROFILE"
    assert recovered["available"]

    tampered = _profile(state)
    tampered["exposures"][-1]["selected"] = "forged"
    mii.save_profile(state / "p6_gaze.json", tampered)
    reset = _run(state, "view")
    assert reset["mii"]["reset_reason"] == "EXPOSURE_TAMPER"
    assert reset["mii"]["exposure_count"] == 1


def test_adaptive_hypotheses_compete_without_overriding_explicit_task(tmp_path):
    state = tmp_path / "world"
    _run(state, "new")
    _run(state, "go", target="living room")
    _run(state, "mii-enable-learning")
    _run(state, "look", target="sandals")
    _run(state, "look", target="photo")
    profile = _profile(state)
    assert profile["hypotheses"]["sandals"]["weight"] >= 1
    assert profile["hypotheses"]["photo"]["weight"] >= 1
    selected = _run(state, "look", target="coaster")
    assert selected["detail"] == "A round cork coaster lies on the shelf."

    profile["hypotheses"]["sandals"]["weight"] = 5
    profile["hypotheses"]["photo"]["weight"] = 3
    choice, basis = mii.select_detail(
        {"coaster": "", "photo": "", "sandals": ""}, profile,
        offered={"coaster": "", "photo": "", "sandals": ""},
    )
    assert choice == "sandals"
    assert basis == "ADAPTIVE_HYPOTHESIS"
    assert profile["hypotheses"]["photo"]["weight"] == 3


def test_gallery_fixture_is_not_hardcoded_to_house_objects(tmp_path):
    state = tmp_path / "gallery"
    opening = _run(state, "new", scene="gallery")
    assert opening["room"] == "gallery"
    assert opening["available"] == ["hinge"]
    _run(state, "go", target="storeroom")
    assert _run(state, "view")["available"] == ["ledger"]
    _run(state, "go", target="gallery")
    looked = _run(state, "look", target="hinge")
    assert looked["admission"] == "ADMITTED"
    assert looked["recognized_identity"] == "the stamped brass hinge"
    assert looked["recognition_source"] == "COMMITTED_INSPECTION"
    profile = _profile(state)
    assert profile["recognized"]["hinge"]["marking"] == "stamped-mark-g-17"
    assert profile["exposures"][-1]["available"] == ["hinge"]


def test_adaptive_controls_are_explicit_and_do_not_touch_world_history(tmp_path):
    state = tmp_path / "world"
    _run(state, "new")
    _run(state, "go", target="living room")
    ledger_file = state / "p4_receipts.json"

    assert _run(state, "mii-status")["mode"] == "NEUTRAL"
    assert _run(state, "mii-enable-learning")["mode"] == "ADAPTIVE"
    _run(state, "look", target="sandals")
    profile = _profile(state)
    assert profile["mode"] == "ADAPTIVE"
    assert profile["learning_enabled"] is True
    assert profile["hypotheses"]["sandals"]["weight"] >= 1

    export = _run(state, "mii-export")
    assert export["profile"]["hypotheses"]["sandals"]["weight"] >= 1
    assert _run(state, "mii-stop-learning")["status"] == "LEARNING_STOPPED"
    _run(state, "look", target="photo")
    profile = _profile(state)
    assert profile["learning_enabled"] is False
    assert "photo" not in profile["hypotheses"]

    before_controls = ledger_file.read_bytes()
    assert _run(state, "mii-learn-label", target="mug", label="old mug")["status"] == "LABEL_LEARNED"
    assert _run(state, "mii-correct-label", target="mug", label="chipped mug")["label"] == "chipped mug"
    assert _run(state, "mii-correct-attention", target="sandals", weight=0)["weight"] == 0
    profile = _profile(state)
    assert profile["hypotheses"]["sandals"]["weight"] == 0
    assert profile["recognition"]["labels"]["mug"]["label"] == "chipped mug"
    assert profile["recognition"]["corrections"]
    assert profile["corrections"]

    reset = _run(state, "mii-reset")
    assert reset["status"] == "RESET"
    profile = _profile(state)
    assert profile["exposures"] == []
    assert profile["recognized"] == {}
    assert profile["mode"] == "NEUTRAL"
    assert ledger_file.read_bytes() == before_controls


def test_taught_label_is_acquired_not_spontaneous_and_scope_mismatch_resets(tmp_path):
    profile = mii.default_profile({"root": "r1", "branch": "b1", "user": "U"})
    profile, result = mii.control(
        profile, "mii-learn-label",
        Namespace(target="sandals", label="my old sandals"), turn=1, clock=1,
    )
    assert result["confidence"] == "ACQUIRED"
    assert "sandals" not in profile["recognized"]
    recognized = mii.recognized_for(profile, "sandals")
    assert recognized["identity"] == "my old sandals"
    assert recognized["recognition_source"] == "USER_TAUGHT_LABEL"

    path = tmp_path / "p6_gaze.json"
    path.write_text(json.dumps({
        "schema": mii.SCHEMA,
        "scope": {"root": "other", "branch": "other", "user": "U"},
        "exposures": [{"exposure_id": "foreign"}],
    }))
    class Session:
        branch_id = "b1"
        meta = {"user_actor": "U"}
        @staticmethod
        def read_root():
            return {"root_hash": "r1"}
    loaded = mii.load_profile(path, Session())
    assert loaded["reset_reason"] == "SCOPE_MISMATCH"
    assert loaded["exposures"] == []
    assert loaded["legacy_unknown"] is False
