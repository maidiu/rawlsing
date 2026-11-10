"""Independent frozen-head probes: MIII Grade B is an owner-call refusal, not an OEE realization.

The sourcefree P6 integration is separately exercised by the unchanged author's
normal GO/cold-replay test.  Here we test the exact owner call contract and
whether caller-supplied cues become authenticated ADP-010 inputs.
"""
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
sys.path.insert(0, str(ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"))
import adp010
from rawlsing_next import gt34_adp010_input_authority_acceptance as acceptance


def cue(*, event_id="move-a", event_hash="a" * 64, recipient="A", eligibility="ELIGIBLE"):
    return {
        "schema": "P6_MOVEMENT_EVIDENCE@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "root": "house-r",
        "branch": "branch-r",
        "clock": 7,
        "event_id": event_id,
        "event_hash": event_hash,
        "conduct_parent": "episode-r",
        "world_source": "world-r",
        "modality_source": "sourcefree-visual",
        "performer": "U",
        "recipient": recipient,
        "origin": "living room",
        "destination": "workshop",
        "recipient_location": "workshop",
        "modality": "VISUAL",
        "eligibility": eligibility,
        "basis": "SOURCEFREE_DOORWAY_SIGHTLINE",
        "uptake": "HOLD_ACTOR_REGISTRATION_OWNER_MISSING",
    }


def test_independent_actual_adp010_call_refuses_before_cue_semantics(monkeypatch):
    """Exact installed owner is called, but authenticated input is absent."""
    actual = adp010.oee.admit_available
    observed = []

    def intercept(**kwargs):
        observed.append(kwargs)
        return actual(**kwargs)

    monkeypatch.setattr(adp010.oee, "admit_available", intercept)
    a = adp010.attempt_movement_admission(cue(event_id="move-a"))
    b = adp010.attempt_movement_admission(cue(event_id="move-b", event_hash="b" * 64))
    assert len(observed) == 2
    assert a["status"] == b["status"] == "OWNER_REFUSED"
    assert a["gate"] == b["gate"] == "AVAILABLE"
    assert a["reason"] == b["reason"] == "subject must be SubjectIngressEvidence"
    assert a["context"] != b["context"]
    for inputs, result in zip(observed, (a, b)):
        assert inputs["subject"] is None
        assert inputs["actor"] is None
        assert inputs["causal_use_acceptance_receipt"] is None
        assert inputs["prior_ledger_anchor_ref"] is None
        assert inputs["effective_from"] is None
        assert inputs["effective_until"] is None
        assert inputs["context_or_world_receipt_refs"][0].content_hash == result["context"]["content_hash"]
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []
    # This passes no input grade that can create AVAILABLE.
    assert a["registry_state"] == b["registry_state"] == "CANDIDATE_NOT_ADOPTED"


@pytest.mark.parametrize("state", ["UNAVAILABLE", "UNKNOWN"])
def test_negative_sensory_lanes_do_not_call_owner(monkeypatch, state):
    def forbidden(**kwargs):
        raise AssertionError("no ADP-010 owner call allowed")
    monkeypatch.setattr(adp010.oee, "admit_available", forbidden)
    result = adp010.attempt_movement_admission(cue(eligibility=state))
    assert result == {"recipient": "A", "status": "NOT_SUBMITTED", "reason": state}


def test_bounded_helper_is_not_independent_source_authenticator():
    """By design, direct caller-provided content alone cannot prove a P6 move."""
    unsupported = cue(event_id="not-an-authenticated-world-event")
    result = adp010.attempt_movement_admission(unsupported)
    assert result["status"] == "OWNER_REFUSED"
    assert result["reason"] == "subject must be SubjectIngressEvidence"
    # Actual source authentication is required upstream in movement_evidence.
    # The ADP-010 executor never validates this context, as it refuses first.


def test_no_positive_adp010_transition_is_silently_accepted(monkeypatch):
    """Current handoff has an explicit nonpositive ceiling, not a release path."""
    monkeypatch.setattr(adp010.oee, "admit_available", lambda **kwargs: object())
    with pytest.raises(RuntimeError, match="admitted a cue without governed subject"):
        adp010.attempt_movement_admission(cue())
