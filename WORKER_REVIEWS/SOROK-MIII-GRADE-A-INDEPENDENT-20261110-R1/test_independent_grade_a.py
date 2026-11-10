"""Independent Grade-A adversarial check; candidate code untouched.

This establishes actor-specific sensory eligibility and non-registration only.
ADP-010 exposure/actor noticing are not inferred.
"""
from argparse import Namespace
from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
RETURNS = ROOT / "WORKER_RETURNS"
for relative in (
    "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1",
    "SOROK-S45-S47-PROJECTION-20261105-R1",
    "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1",
    "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests",
    "SOROK-P4-FIRST-FULL-MPC-R1",
    "SOROK-P5-CONTINUOUS-EXPERIENCE-R1",
    "SOROK-P6-ONE-LIVING-HOUSE-R1",
):
    sys.path.insert(0, str(RETURNS / relative))

import house
import run_p6
from encounter import VISUAL_FIXTURE, VISUAL_SOURCE, movement_evidence
from developmental_recursion.contracts import RecursionRefusal


def test_independent_actor_specific_visual_eligibility_and_no_registration(tmp_path, monkeypatch):
    """A genuine P6 MOVE may qualify a visual cue but cannot grant awareness."""
    establish = run_p6.establish

    def established_source(session):
        establish(session)
        world, resource = run_p6.read_house(session)
        world.positions["B"] = "workshop"
        resource["movement_visual_fixture"] = {
            "source": VISUAL_SOURCE, "facts": deepcopy(VISUAL_FIXTURE)
        }
        session.product._checkpoint(session.branch_id, world.clock, world)

    monkeypatch.setattr(run_p6, "establish", established_source)
    run_p6.experience(tmp_path, Namespace(command="new"))
    run_p6.experience(tmp_path, Namespace(command="go", target="living room", request_id="away"))

    owner = run_p6.open_owner(tmp_path / "actual-p2")
    try:
        head_before = owner.store.head()
    finally:
        owner.close()

    original_reader = house.movement_evidence

    def adversarial_reader(session, event, world, resource):
        # This is the real first reader, before ordinary S46 pacing.
        witness = original_reader(session, event, world, resource)
        assert [item["eligibility"] for item in witness] == ["ELIGIBLE", "UNAVAILABLE"]
        assert all(item["event_id"] == event["event_id"] and
                   item["event_hash"] == event["hash"] for item in witness)
        forged = {**event, "event_id": "forged-actor-event"}
        with pytest.raises(RecursionRefusal, match="P6_ENCOUNTER_MOVEMENT_SOURCE_MISMATCH"):
            original_reader(session, forged, world, resource)
        tampered = deepcopy(resource)
        tampered["movement_visual_fixture"]["facts"]["recipients"]["A"]["facing"] = "away"
        denied = original_reader(session, event, world, tampered)
        assert all(item["eligibility"] == "UNKNOWN" for item in denied)
        omitted = {k: v for k, v in resource.items() if k != "movement_visual_fixture"}
        absent = original_reader(session, event, world, omitted)
        assert all(item["eligibility"] == "UNKNOWN" and
                   item["modality"] is None for item in absent)
        return witness

    monkeypatch.setattr(house, "movement_evidence", adversarial_reader)
    public = run_p6.experience(tmp_path, Namespace(command="go", target="workshop",
                                                    request_id="return"))
    assert public["admission"] == "ADMITTED"
    assert "encounter_evidence" not in json.dumps(public)
    [turn] = [x for x in json.loads((tmp_path / "p4_receipts.json").read_text())["turns"]
              if x["request_id"] == "return"]
    ev = turn["receipt"]["performed"]
    packet = turn["receipt"]["encounter_evidence"]
    assert [x["eligibility"] for x in packet] == ["ELIGIBLE", "UNAVAILABLE"]
    assert packet[0]["uptake"] == "HOLD_ACTOR_REGISTRATION_OWNER_MISSING"
    owner = run_p6.open_owner(tmp_path / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.event(ev["event_id"]) == ev
        assert owner.store.head() == head_before
        for actor in ("A", "B"):
            assert not any(p["event_id"] == ev["event_id"] for p in
                           session.product.store.perceptions(session.branch_id, actor))
        # A persisted receipt is not a native actor registration.
        assert packet[0]["recipient"] == "A"
        assert packet[1]["recipient"] == "B"
    finally:
        owner.close()
