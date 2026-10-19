"""(h) Performed-action owner admission and typed HOLD tests."""
from __future__ import annotations

from conftest import ACTOR_ID
from candidate.action_admission import (
    AdmissionReason,
    AdmissionStatus,
    PerformedActionAdmission,
    PerformedActionHold,
    admit_performed_action,
    make_performed_action_receipt,
)


def _receipt(**overrides) -> dict:
    defaults = dict(
        actor_id=ACTOR_ID,
        act="inspect_with_tool",
        actuator_ref="TEST_ONLY_ACTUATOR",
        occurrence_ref="TEST_ONLY_OCCURRENCE_E2",
        action_time=30,
        consumed_state_hash="state-hash",
    )
    defaults.update(overrides)
    return make_performed_action_receipt(**defaults)


def test_missing_owner_receipt_returns_typed_hold() -> None:
    result = admit_performed_action(
        owner_receipt=None,
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert isinstance(result, PerformedActionHold)
    assert result.status is AdmissionStatus.HELD
    assert result.reason is AdmissionReason.OWNER_RECEIPT_MISSING
    assert "OWNER_RECEIPT" in result.expected_owner_form


def test_hand_authored_action_is_always_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(),
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
        hand_authored=True,
    )
    assert isinstance(result, PerformedActionHold)
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.HAND_AUTHORED_ACTION


def test_genuine_receipt_is_admitted() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(),
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert isinstance(result, PerformedActionAdmission)
    assert result.status is AdmissionStatus.ADMITTED
    assert result.act == "inspect_with_tool"
    assert result.actuator_ref == "TEST_ONLY_ACTUATOR"
    assert result.consumed_state_hash == "state-hash"


def test_actor_mismatch_is_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(),
        expected_actor_id="OTHER_ACTOR",
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.ACTOR_MISMATCH


def test_act_mismatch_is_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(),
        expected_actor_id=ACTOR_ID,
        expected_act="decline_help",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.ACT_UNBOUND


def test_missing_occurrence_ref_is_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(occurrence_ref=""),
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.OCCURRENCE_REF_MISSING


def test_future_action_time_is_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(action_time=50),
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.TIME_REVERSED


def test_no_consumed_state_is_refused() -> None:
    result = admit_performed_action(
        owner_receipt=_receipt(consumed_state_hash=""),
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.NO_CONSUMED_TARGET_STATE


def test_unsealed_receipt_is_refused() -> None:
    broken = dict(_receipt())
    broken["hash"] = "0" * 64
    result = admit_performed_action(
        owner_receipt=broken,
        expected_actor_id=ACTOR_ID,
        expected_act="inspect_with_tool",
        consumed_state_hash="state-hash",
        as_of=40,
    )
    assert result.status is AdmissionStatus.REFUSED
    assert result.reason is AdmissionReason.RECEIPT_INTEGRITY_FAILURE
