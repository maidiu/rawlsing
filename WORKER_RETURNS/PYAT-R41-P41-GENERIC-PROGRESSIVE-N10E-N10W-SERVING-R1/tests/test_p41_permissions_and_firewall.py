"""P41 permission matrix, actor firewall and sampling-unit firewall."""
from __future__ import annotations

import json

import pytest

from p41_service import P41Service, P41ServiceError


def test_permission_matrix_and_type_unissued_purpose():
    service = P41Service()
    for name in ("NONPARENT_OPTIONS", "GENERIC_POSITIONED_SUBJECT"):
        receipt = service.progressive(consumer=name)
        assert receipt["consumer"]["permission_state"] == "ADMITTED_TEST_ONLY"
        assert receipt["n10e_steps"]
    unissued = service.progressive(consumer="CONCEPTION_SCENARIO_PROPOSALS")
    assert unissued["state"] == "CONSUMER_PERMISSION_UNISSUED"
    assert unissued["receipt"] is None
    assert "nonauthoritative" in unissued["versioned_consumer_contract"].lower()
    for name in ("SOROK_ACTOR", "HOUSEHOLD_DYAD"):
        with pytest.raises(P41ServiceError):
            service.progressive(consumer=name)


def test_actor_firewall_and_no_route_probability():
    receipt = P41Service().progressive()
    firewall = receipt["firewall"]
    assert firewall["actor_state_present"] is False
    assert firewall["personhood_present"] is False
    assert firewall["encounter_probability_present"] is False
    assert receipt["structural"]["route_probability"] is None
    assert receipt["structural"]["route_probability_reason"] == \
        "NO_JOINT_EMPIRICAL_STRUCTURAL_ROUTE_MODEL"
    assert receipt["structural"]["actor_executions"] == 0
    assert receipt["structural"]["model_calls"] == 0
    scanned = dict(receipt)
    scanned.pop("firewall", None)
    blob = json.dumps(scanned, sort_keys=True).lower()
    for token in ("father", "mother", "partner_choice", "personality",
                  "belief", "encounter_probability"):
        assert token not in blob
    assert "is_father" not in blob
