"""Sourcefree recognition surface proof over the actual P6 house/run path."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

HERE = Path(__file__).resolve()
P6 = HERE.parents[1] / "SOROK-P6-ONE-LIVING-HOUSE-R1"
P5 = HERE.parents[1] / "SOROK-P5-CONTINUOUS-EXPERIENCE-R1"
sys.path.insert(0, str(P6))
sys.path.insert(0, str(P5))

from run_p6 import experience  # noqa: E402
import house  # noqa: E402
from developmental_recursion.contracts import digest  # noqa: E402


def run(state: Path, command: str, **kwargs):
    return experience(state, Namespace(command=command, request_id=None, **kwargs))


def cold_view(state: Path):
    proc = subprocess.run(
        [sys.executable, "-B", str(P6 / "run_p6.py"), "--state", str(state), "view"],
        cwd=str(P6), capture_output=True, text=True, timeout=120,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_plain_category_before_evidence_and_specialist_identity_after_look(tmp_path):
    state = tmp_path / "state"
    opening = run(state, "new")
    assert opening["recognized_identity"] is None
    assert "bench" in opening["available"]  # plain category, allowed
    assert "specialist" not in str(opening["detail"]).lower()

    moved = run(state, "go", target="living room")
    before = run(state, "view")
    assert moved["admission"] == "ADMITTED"
    assert before["recognized_identity"] is None
    assert before["recognition"] == {}
    assert "sandals" in before["available"]  # plain category, allowed

    looked = run(state, "look", target="sandals")
    assert looked["admission"] == "ADMITTED"
    assert looked["recognized_identity"] == "the repaired blue-thread sandals"
    assert looked["recognition"]["sandals"]["marking"] == "blue-thread-left-strap"

    reopened = cold_view(state)
    assert reopened["recognized_identity"] == "the repaired blue-thread sandals"
    assert reopened["recognition"]["sandals"]["identity"] == "the repaired blue-thread sandals"


def test_unavailable_and_history_only_cannot_earn_recognition(tmp_path):
    assert house.recognize("sandals", "Nadia privately knows these sandals") is None
    assert house.recognize("sandals", "Blue thread crosses the left strap.") is not None
    state = tmp_path / "state"
    run(state, "new")
    refused = run(state, "look", target="sandals")
    assert refused["admission"] == "UNAVAILABLE"
    assert refused["recognized_identity"] is None
    assert refused["recognition"] == {}

    history_state = tmp_path / "history"
    run(history_state, "new")
    (history_state / "p6_gaze.json").write_text(json.dumps({
        "history": [{"target": "sandals", "turn": 1, "shown": True,
                     "available": ["sandals"]}],
        "exposure": {"room": "living room", "detail": "sandals"},
    }), encoding="utf8")
    history_view = run(history_state, "view")
    assert history_view["recognized_identity"] is None
    assert history_view["recognition"] == {}



def test_cold_view_rederives_genuine_and_ignores_fabricated_cache(tmp_path):
    state = tmp_path / "state"
    run(state, "new")
    run(state, "go", target="living room")
    run(state, "look", target="sandals")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    actual_event = ledger["turns"][-1]["receipt"]["performed"]["event_id"]
    gaze = json.loads((state / "p6_gaze.json").read_text())
    gaze["recognized"] = {
        "sandals": {
            "object_id": "sandals", "identity": "FABRICATED IDENTITY",
            "marking": "fake-marking", "evidence": "fake evidence",
            "event_id": "fake-event", "turn": 99,
        },
        "photo": {
            "object_id": "photo", "identity": "FABRICATED PHOTO IDENTITY",
            "marking": "fake-photo-marking", "evidence": "fake photo evidence",
            "event_id": "fake-photo-event", "turn": 99,
        },
    }
    (state / "p6_gaze.json").write_text(json.dumps(gaze), encoding="utf8")
    reopened = cold_view(state)
    assert reopened["recognized_identity"] == "the repaired blue-thread sandals"
    assert reopened["recognition"]["sandals"]["event_id"] == actual_event
    assert reopened["recognition"]["sandals"]["marking"] == "blue-thread-left-strap"
    assert "FABRICATED" not in json.dumps(reopened["recognition"])
    assert "photo" not in reopened["recognition"]

    fake_state = tmp_path / "fake"
    run(fake_state, "new")
    (fake_state / "p6_gaze.json").write_text(json.dumps({
        "history": [], "exposure": {},
        "recognized": {"sandals": {
            "object_id": "sandals", "identity": "FABRICATED IDENTITY",
            "marking": "fake-marking", "evidence": "fake evidence",
            "event_id": "fake-event", "turn": 99,
        }},
    }), encoding="utf8")
    fake_view = cold_view(fake_state)
    assert fake_view["recognized_identity"] is None
    assert fake_view["recognition"] == {}

    photo_state = tmp_path / "photo"
    run(photo_state, "new")
    run(photo_state, "go", target="living room")
    photo = run(photo_state, "look", target="photo")
    assert photo["admission"] == "ADMITTED"
    photo_view = cold_view(photo_state)
    assert photo_view["recognized_identity"] is None
    assert "sandals" not in photo_view["recognition"]


def test_ledger_summary_and_event_are_resolved_from_owner_events(tmp_path):
    state = tmp_path / "ledger"
    run(state, "new")
    run(state, "go", target="living room")
    run(state, "look", target="sandals")
    ledger = json.loads((state / "p4_receipts.json").read_text())
    actual_event = ledger["turns"][-1]["receipt"]["performed"]["event_id"]

    rewritten = copy.deepcopy(ledger)
    rewritten["turns"][-1]["receipt"]["performed"]["summary"] = "FABRICATED SUMMARY"
    rewritten["turns"][-1]["public"]["observation"]["summary"] = "FABRICATED SUMMARY"
    (state / "p4_receipts.json").write_text(json.dumps(rewritten), encoding="utf8")
    view = cold_view(state)
    assert view["recognized_identity"] == "the repaired blue-thread sandals"
    assert view["recognition"]["sandals"]["event_id"] == actual_event
    assert view["recognition"]["sandals"]["turn"] == 2
    assert "FABRICATED" not in json.dumps(view["recognition"])

    forged = copy.deepcopy(rewritten)
    forged["turns"][-1]["receipt"]["performed"]["event_id"] = "FAKE-LEDGER-EVENT"
    forged["turns"][-1]["public"]["observation"]["event_id"] = "FAKE-LEDGER-EVENT"
    (state / "p4_receipts.json").write_text(json.dumps(forged), encoding="utf8")
    fake_view = cold_view(state)
    assert fake_view["recognized_identity"] is None
    assert fake_view["recognition"] == {}

    photo = run(state, "look", target="photo")
    assert photo["admission"] == "ADMITTED"
    photo_ledger = json.loads((state / "p4_receipts.json").read_text())
    photo_event = photo_ledger["turns"][-1]["receipt"]["performed"]["event_id"]
    mixed = copy.deepcopy(photo_ledger)
    mixed["turns"][-2]["receipt"]["performed"]["event_id"] = photo_event
    mixed["turns"][-2]["public"]["observation"]["event_id"] = photo_event
    (state / "p4_receipts.json").write_text(json.dumps(mixed), encoding="utf8")
    mismatched = cold_view(state)
    assert "sandals" not in mismatched["recognition"]

def test_changed_specialist_input_changes_identity_and_preserves_gross_facts(tmp_path):
    normal_state = tmp_path / "normal"
    changed_state = tmp_path / "changed"
    normal_open = run(normal_state, "new")
    run(normal_state, "go", target="living room")
    normal = run(normal_state, "look", target="sandals")

    original_objects = house.OBJECTS
    original_source = house.SOURCE
    changed_objects = {key: dict(value) for key, value in original_objects.items()}
    changed_objects["sandals"]["specialist_identity"] = "the alternate blue-thread sandals"
    try:
        house.OBJECTS = changed_objects
        house.SOURCE = digest({"rooms": house.ROOMS, "objects": house.OBJECTS,
                               "history": house.HISTORY})
        changed_open = run(changed_state, "new")
        run(changed_state, "go", target="living room")
        changed = run(changed_state, "look", target="sandals")
    finally:
        house.OBJECTS = original_objects
        house.SOURCE = original_source

    assert changed["recognized_identity"] == "the alternate blue-thread sandals"
    assert changed["recognized_identity"] != normal["recognized_identity"]
    assert changed_open["clock"] == normal_open["clock"]
    assert changed_open["room"] == normal_open["room"]
    assert len(changed_open["available"]) == len(normal_open["available"])
