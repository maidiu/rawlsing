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


def test_exact_e1_hold_with_real_history(performed_bundle):
    result = evaluate_persona_response(performed_bundle)
    assert result["status"] == "HELD"
    assert result["outcome"] == "A_LOCAL_PERCEPTION_HOLD"
    assert result["response_status"] == "RESPONSE_EFFECTS_VALID_EMPTY"
    assert result["perception_gate"] == "MISSING"
    assert result["action_gate"] == "MISSING"
    assert result["actual_actor_input"] is False
    assert result["qualification"] == "TYPED_HOLD_ACTUAL_A_INPUT_UNAVAILABLE"
    assert result["target_branch"] == "NO_CHANGE"
    assert result["target_reason"] == "NO_PROPOSAL"
    assert result["target_proposals"] == 0
    assert result["history_used_for_choice"] is False
    assert result["s39_synthetic_premises_used"] is False
    assert result["store_mutated"] is False
    persona_input = result["persona_input"]
    assert persona_input["occurrence_ok"] is True
    assert persona_input["occurrence"]["event_id"] == performed_bundle["event_id"]
    assert persona_input["occurrence"]["event_clock"] == 242
    assert persona_input["occurrence"]["branch_clock"] == 10
    assert persona_input["objective_event_present"] is True
    assert persona_input["perception"] is None
    assert persona_input["event"] == {
        "event_id": performed_bundle["event_id"],
        "objective_present": True,
    }
    assert persona_input["history"]["history_hash"]
    assert persona_input["history"]["event_count"] > 0
    assert persona_input["history"]["performed_action_refs"]
    assert persona_input["c12_a_perception_count"] > 0
    assert persona_input["c12_other_event_perception_event_ids"]
    assert persona_input["c12_perceptions_are_not_e1_receipts"] is True
    assert persona_input["checks"]["event_identity_ok"] is True
    assert persona_input["checks"]["perception_event_matches_e1"] is False
    assert persona_input["checks"]["perception_substitution"] is False
    assert persona_input["checks"]["history_before_e1"] is True
    assert "A_LOCAL_OBSERVATION_RECEIPT_OF_E1" in result["missing_inputs"]
    assert (
        "A_ACTION_OR_OMISSION_RECEIPT_BOUND_TO_E1_CLOCK_AND_ORDER"
        in result["missing_inputs"]
    )
    assert result["s35"]["event_ref"] == persona_input["occurrence"]["event_ref"]
    assert result["s35"]["event_id"] == performed_bundle["event_id"]


def test_refused_exact_e1_also_holds(refused_bundle):
    result = evaluate_persona_response(refused_bundle)
    assert result["outcome"] == "A_LOCAL_PERCEPTION_HOLD"
    assert result["actual_actor_input"] is False
    assert result["persona_input"]["perception"] is None
    assert result["persona_input"]["history"]["history_hash"]
    assert result["target_branch"] == "NO_CHANGE"
    assert result["store_mutated"] is False


def test_other_event_perception_cannot_become_e1_receipt(performed_bundle):
    c12_event_id = performed_bundle["world_events"][-1]["event_id"]
    result = evaluate_persona_response(
        performed_bundle, event_id=c12_event_id
    )
    assert result["status"] == "HELD"
    assert result["outcome"] == "PERCEPTION_EVENT_IDENTITY_MISMATCH"
    assert result["target_branch"] == "NO_CHANGE"
    persona_input = result["persona_input"]
    assert persona_input["requested_event_id"] == c12_event_id
    assert persona_input["selected_event_id"] == performed_bundle["event_id"]
    assert persona_input["perception"] is None
    assert persona_input["checks"]["event_identity_ok"] is False
    assert persona_input["checks"]["perception_substitution"] is False
    assert "PERCEPTION_EVENT_IDENTITY_MISMATCH" in result["missing_inputs"]
    encoded = json.dumps(result["persona_input"], sort_keys=True)
    assert "Put your hand" not in encoded
    assert "clears a space" not in encoded
    assert "SHARE_TOOL" not in encoded
    assert "REFUSE_TOOL" not in encoded


def test_history_severance_is_visible_but_not_used(performed_bundle):
    full = build_persona_input(performed_bundle)
    assert full["history"] is not None
    severed = build_persona_input(performed_bundle, include_history=False)
    assert severed["history"] is None
    assert "ACTOR_HISTORY_INPUT_MISSING" in severed["missing_inputs"]
    assert severed["history_used_for_choice"] is False
    result = evaluate_persona_response(performed_bundle, include_history=False)
    assert result["outcome"] == "A_LOCAL_PERCEPTION_HOLD"
    assert result["history_used_for_choice"] is False


def test_missing_event_identity_holds(performed_bundle):
    result = evaluate_persona_response(
        performed_bundle, event_id="TEST_ONLY_NOT_A_PERSISTED_EVENT"
    )
    assert result["status"] == "HELD"
    assert result["outcome"] == "PERCEPTION_EVENT_IDENTITY_MISMATCH"
    assert result["target_branch"] == "NO_CHANGE"
    assert result["store_mutated"] is False


def test_s39_synthetic_producer_is_audited_and_not_used(performed_bundle):
    from persona import s39_audit

    audit = s39_audit.audit()
    assert audit["commit"] == "6604f2d9"
    assert audit["uses_synthetic_source_records"] is True
    assert audit["uses_test_only_response_witness"] is True
    assert audit["operation_only_availability"] is True
    assert audit["used_by_persona_input"] is False
    result = evaluate_persona_response(performed_bundle)
    assert result["s39_synthetic_premises_used"] is False
