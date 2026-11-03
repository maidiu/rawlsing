import json

import pytest

from persona import sources
from persona.input import build_persona_input, evaluate_persona_response


@pytest.fixture(scope="module")
def performed_bundle(tmp_path_factory):
    root = tmp_path_factory.mktemp("persona-join-e-performed")
    return sources.run_probe(
        state_root=root,
        disposition="PERFORMED",
        perform="omit",
        mode="start",
        do_help=True,
    )


@pytest.fixture(scope="module")
def refused_bundle(tmp_path_factory):
    root = tmp_path_factory.mktemp("persona-join-e-refused")
    return sources.run_probe(
        state_root=root,
        disposition="REFUSED",
        mode="start",
        do_help=True,
    )


def test_intact_persisted_perception_and_history_hold(performed_bundle):
    result = evaluate_persona_response(performed_bundle)
    assert result["status"] == "HELD"
    assert result["outcome"] == "A_OWNED_ACTION_HOLD"
    assert result["response_status"] == "RESPONSE_EFFECTS_VALID_EMPTY"
    assert result["perception_gate"] == "OK"
    assert result["target_branch"] == "NO_CHANGE"
    assert result["target_reason"] == "NO_PROPOSAL"
    assert result["target_proposals"] == 0
    assert result["missing_inputs"] == [
        "A_ACTION_RESPONSE_PRODUCER_MISSING",
        "PERSONA_HISTORY_RESPONSE_RULE_MISSING",
        "ISSUED_A_RESPONSE_RULE_MISSING",
    ]
    assert result["history_used_for_choice"] is False
    assert result["s39_synthetic_premises_used"] is False
    assert result["store_mutated"] is False
    persona_input = result["persona_input"]
    assert persona_input["occurrence_ok"] is True
    assert persona_input["objective_event_present"] is True
    assert persona_input["perception"]["actor_id"] == "A"
    assert persona_input["perception"]["channel"] == "co_present"
    assert persona_input["history"]["history_hash"]
    assert persona_input["history"]["event_count"] > 0
    assert persona_input["history"]["performed_action_refs"]
    assert persona_input["checks"] == {
        "event_order_present": True,
        "history_before_e1": True,
        "history_domain_distinguished": True,
        "history_enabled": True,
        "history_hash_present": True,
        "history_order_comparable": False,
        "history_present": True,
        "history_source_matches_actor": True,
        "objective_event_present": True,
        "occurrence_ok": True,
        "perception_actor_a": True,
        "perception_clock_matches_event": True,
        "perception_enabled": True,
        "perception_event_matches": True,
        "perception_present": True,
    }


def test_refused_persisted_perception_uses_same_boundary(refused_bundle):
    result = evaluate_persona_response(refused_bundle)
    assert result["outcome"] == "A_OWNED_ACTION_HOLD"
    persona_input = result["persona_input"]
    assert persona_input["perception"]["actor_id"] == "A"
    assert persona_input["history"]["history_hash"]
    assert persona_input["event"]["kind"] == "SPEECH"
    assert "REFUSE" in persona_input["event"]["body_public"]["strategy"]
    assert result["store_mutated"] is False


def test_objective_availability_does_not_imply_perception(performed_bundle):
    intact = build_persona_input(performed_bundle)
    event_id = intact["selected_event_id"]
    severed = evaluate_persona_response(
        performed_bundle, event_id=event_id, include_perception=False
    )
    assert severed["status"] == "HELD"
    assert severed["outcome"] == "A_LOCAL_PERCEPTION_INPUT_MISSING"
    assert severed["persona_input"]["objective_event_present"] is True
    assert severed["persona_input"]["perception"] is None
    assert severed["persona_input"]["event"] == {
        "event_id": event_id,
        "objective_present": True,
    }
    encoded = json.dumps(severed["persona_input"])
    assert "Put your hand" not in encoded
    assert "clears a space" not in encoded
    assert "SHARE_TOOL" not in encoded
    restored = evaluate_persona_response(
        performed_bundle, event_id=event_id, include_perception=True
    )
    assert restored["outcome"] == "A_OWNED_ACTION_HOLD"


def test_history_severance_and_restoration(performed_bundle):
    severed = evaluate_persona_response(performed_bundle, include_history=False)
    assert severed["status"] == "HELD"
    assert severed["outcome"] == "ACTOR_HISTORY_INPUT_MISSING"
    assert severed["persona_input"]["perception"]["actor_id"] == "A"
    assert severed["persona_input"]["history"] is None
    assert severed["target_branch"] == "NO_CHANGE"
    restored = evaluate_persona_response(performed_bundle, include_history=True)
    assert restored["outcome"] == "A_OWNED_ACTION_HOLD"


def test_missing_objective_event_holds(performed_bundle):
    result = evaluate_persona_response(
        performed_bundle, event_id="TEST_ONLY_NOT_A_PERSISTED_EVENT"
    )
    assert result["status"] == "HELD"
    assert result["outcome"] == "PERSISTED_EVENT_MISSING"
    assert result["target_branch"] == "NO_CHANGE"
    assert result["store_mutated"] is False


def test_s39_synthetic_producer_is_audited_and_not_used(performed_bundle):
    audit = __import__("persona.s39_audit", fromlist=["audit"]).audit()
    assert audit["commit"] == "6604f2d9"
    assert audit["uses_synthetic_source_records"] is True
    assert audit["uses_test_only_response_witness"] is True
    assert audit["operation_only_availability"] is True
    assert audit["used_by_persona_input"] is False
    result = evaluate_persona_response(performed_bundle)
    assert result["s39_audit"] == audit
    assert result["s39_synthetic_premises_used"] is False
