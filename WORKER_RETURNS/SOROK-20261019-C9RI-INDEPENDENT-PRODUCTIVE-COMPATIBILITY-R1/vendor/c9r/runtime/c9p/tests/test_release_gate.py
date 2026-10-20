"""T2 owner-release gate: C9_NATIVE_POSITIVE_HELD preservation tests."""
from __future__ import annotations

from candidate.release_gate import (
    HoldCode,
    ReleaseOutcome,
    evaluate_release_gate,
)


def test_default_gate_is_held_with_all_finite_holds() -> None:
    result = evaluate_release_gate()
    assert result.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    assert result.held is True
    codes = {hold.hold_code for hold in result.holds}
    assert HoldCode.CAN008_RULE_ISSUER_UNVERIFIED in codes
    assert HoldCode.CAN011_TARGET_UNISSUED in codes
    assert HoldCode.ADP019_ACTOR_EVENT_WITNESS_MISSING in codes
    assert HoldCode.POSITIVE_TRANSITION_REGISTRY_EMPTY in codes
    assert HoldCode.PERFORMED_ACTION_OWNER_UNPROVED in codes


def test_fixture_supplied_authority_never_clears_gate() -> None:
    result = evaluate_release_gate(
        fixture_supplied_authority={"CURRENT_ACCEPTED": True, "digest": "abc"}
    )
    assert result.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    assert result.rule_a_issuer_verified is False


def test_partial_issuer_evidence_still_held() -> None:
    result = evaluate_release_gate(rule_a_issuer_verified=True)
    assert result.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    codes = {hold.hold_code for hold in result.holds}
    assert HoldCode.CAN008_RULE_ISSUER_UNVERIFIED not in codes
    assert HoldCode.CAN011_TARGET_UNISSUED in codes


def test_empty_positive_registry_alone_holds() -> None:
    result = evaluate_release_gate(
        rule_a_issuer_verified=True,
        rule_t_issuer_verified=True,
        adp019_witness_present=True,
        adp010_witness_present=True,
        performed_action_owner_proved=True,
        later_action_consumer_bound=True,
    )
    assert result.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_HELD
    assert [hold.hold_code for hold in result.holds] == [
        HoldCode.POSITIVE_TRANSITION_REGISTRY_EMPTY
    ]


def test_all_surfaces_cleared_authorizes() -> None:
    result = evaluate_release_gate(
        rule_a_issuer_verified=True,
        rule_t_issuer_verified=True,
        adp019_witness_present=True,
        adp010_witness_present=True,
        positive_registry_entries=1,
        performed_action_owner_proved=True,
        later_action_consumer_bound=True,
    )
    assert result.outcome is ReleaseOutcome.C9_NATIVE_POSITIVE_AUTHORIZED
    assert result.holds == ()


def test_gate_receipt_is_deterministic() -> None:
    first = evaluate_release_gate()
    second = evaluate_release_gate()
    assert first.gate_receipt_hash == second.gate_receipt_hash


def test_checked_surfaces_cover_all_commissioned_rows() -> None:
    result = evaluate_release_gate()
    assert set(result.checked_surfaces) == {
        "CAN008_RULE_A_ISSUER",
        "CAN011_RULE_T_TARGET_GRANT",
        "ADP019_EVENT_WITNESS",
        "ADP010_ENCOUNTER_WITNESS",
        "PSEPF_POSITIVE_TRANSITION_REGISTRY",
        "PERFORMED_ACTION_OWNER",
        "LATER_ACTION_CONSUMER",
    }
