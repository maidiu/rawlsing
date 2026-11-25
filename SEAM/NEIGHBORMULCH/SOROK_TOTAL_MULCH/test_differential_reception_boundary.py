"""NEIGHBOR first-consumer boundary against the existing received P6 producer.

ONE canonical world movement produces two independent, actor-specific sensory
eligibility receipts. That does NOT establish two psychological receptions:
P6 currently holds A registration, B is ineligible for this sourcefree
sightline, and no qualified developmental/expressive afterlife is produced.

This is an executable NEGATIVE COURT / currentness baseline, not a synthetic
replacement for CAN-008, MIII or the SORACLE Constitutive Organism.
"""
from argparse import Namespace
from copy import deepcopy
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
P6 = ROOT / "WORKER_RETURNS" / "SOROK-P6-ONE-LIVING-HOUSE-R1"
sys.path.insert(0, str(P6))

import run_p6
from encounter import VISUAL_FIXTURE, VISUAL_SOURCE
from situated import actor_context_for


def test_one_world_event_two_access_receipts_but_no_two_person_uptake(tmp_path, monkeypatch):
    state = tmp_path / "continuity"
    original = run_p6.establish
    interpreted = []

    def establish_bound_fixture(session):
        original(session)
        world, house = run_p6.read_house(session)
        world.positions["B"] = "workshop"
        house["movement_visual_fixture"] = {
            "source": VISUAL_SOURCE, "facts": deepcopy(VISUAL_FIXTURE),
        }
        session.product._checkpoint(session.branch_id, world.clock, world)

    def interpret(packet):
        interpreted.append(deepcopy(packet))
        assert len(packet["cues"]) == 1
        cue = packet["cues"][0]
        assert cue["modality"] == "VISUAL"
        return {
            "attention": "noticed",
            "interpretation": "A real movement was seen, but no durable psyche is proven.",
            "action": "continue",
            "cue_event_id": cue["event_id"],
            "channel": cue["modality"],
        }

    monkeypatch.setattr(run_p6, "establish", establish_bound_fixture)
    run_p6.experience(state, Namespace(command="new"))
    run_p6.experience(
        state, Namespace(command="go", target="living room",
                         request_id="visitor-left"), interpret=interpret
    )
    run_p6.experience(
        state, Namespace(command="go", target="workshop",
                         request_id="visitor-returned"), interpret=interpret
    )

    ledger = json.loads((state / "p4_receipts.json").read_text())
    receipt = ledger["turns"][-1]["receipt"]
    event = receipt["performed"]
    rows = {row["recipient"]: row for row in receipt["encounter_evidence"]}
    assert event["kind"] == "MOVE"
    assert set(rows) == {"A", "B"}
    assert {r["event_id"] for r in rows.values()} == {event["event_id"]}
    assert {r["event_hash"] for r in rows.values()} == {event["hash"]}
    assert {r["clock"] for r in rows.values()} == {event["clock"]}
    assert rows["A"]["eligibility"] == "ELIGIBLE"
    assert rows["A"]["uptake"] == "HOLD_ACTOR_REGISTRATION_OWNER_MISSING"
    assert rows["B"]["eligibility"] == "UNAVAILABLE"
    assert rows["B"]["uptake"] == "NOT_ELIGIBLE_FOR_REGISTRATION"

    # An injected *A-only* inference is not canonical, historically
    # conditioned psychological processing of the two people.
    assert len(interpreted) == 1
    assert interpreted[0]["cues"][0]["event_id"] == event["event_id"]
    assert receipt["situated"]["status"] == "INTERPRETED"
    assert receipt["situated"]["decision"]["action"] == "continue"
    assert "adp010_admission" not in receipt

    owner = run_p6.open_owner(state / "actual-p2")
    try:
        session = owner.base_owner.fanin.session
        assert session.event(event["event_id"]) == event
        for actor in ("A", "B"):
            assert not any(
                row["event_id"] == event["event_id"]
                for row in session.product.store.perceptions(session.branch_id, actor)
            )
    finally:
        owner.close()

    # Same actor-local fixture must not be impersonated as B's life.
    local = {
        "grade": "SOURCEFREE_FIXTURE", "actor_id": interpreted[0]["actor"],
        "priority": "Finish the current workshop work.",
    }
    assert actor_context_for("unrelated-actor", local) is None
