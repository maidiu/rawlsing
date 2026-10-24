"""S36 same-assertion faults, legacy preservation and no-native-grant checks."""
from __future__ import annotations

from candidate import (
    CandidateStore,
    ResponseRuleRegistry,
    ResponseStatus,
    TargetBranch,
    TargetReason,
    TargetRuleRegistry,
)
from candidate.actor_access_response import (
    OBSERVED_IMMEDIATE_OBJECT_ORIENTATION,
    RECEIVABLE_NO_OBSERVED_UPTAKE,
    UNKNOWN_RECEIVABILITY,
)
from s36_harness import LEGACY_HISTORY, legacy_two_history_response, run_s35_case


def test_same_assertion_access_removed_to_empty_restored_positive(tmp_path):
    with CandidateStore(tmp_path / "access_positive.sqlite") as store:
        positive, _ = run_s35_case(store)
        assert positive.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert positive.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
    with CandidateStore(tmp_path / "access_fault.sqlite") as store:
        fault, _ = run_s35_case(store, access=None)
        assert fault.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert fault.response.reason == UNKNOWN_RECEIVABILITY
        assert fault.response.target_proposals == ()
        assert fault.decision.branch is TargetBranch.NO_CHANGE
        assert fault.decision.reason is TargetReason.NO_PROPOSAL
    with CandidateStore(tmp_path / "access_restored.sqlite") as store:
        restored, _ = run_s35_case(store)
        assert restored.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert restored.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert restored.response.receipt_hash == positive.response.receipt_hash


def test_same_assertion_response_removed_to_empty_restored_positive(tmp_path):
    with CandidateStore(tmp_path / "response_positive.sqlite") as store:
        positive, _ = run_s35_case(store)
        assert positive.response.status is ResponseStatus.RESPONSE_COMMITTED
    with CandidateStore(tmp_path / "response_fault.sqlite") as store:
        fault, _ = run_s35_case(store, response=None)
        assert fault.response.status is ResponseStatus.RESPONSE_EFFECTS_VALID_EMPTY
        assert fault.response.reason == RECEIVABLE_NO_OBSERVED_UPTAKE
        assert fault.response.target_proposals == ()
        assert fault.decision.branch is TargetBranch.NO_CHANGE
    with CandidateStore(tmp_path / "response_restored.sqlite") as store:
        restored, _ = run_s35_case(store)
        assert restored.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert restored.response.receipt_hash == positive.response.receipt_hash


def test_legacy_two_history_response_is_preserved():
    response, _ = legacy_two_history_response()
    assert response.status is ResponseStatus.RESPONSE_COMMITTED
    assert len(response.target_proposals) == 1
    assert response.target_proposals[0]["operation"] == "CREATE"
    assert response.declared_history_refs == LEGACY_HISTORY


def test_s35_two_history_refs_never_fall_back_to_legacy(tmp_path):
    with CandidateStore(tmp_path / "s35_two_history.sqlite") as store:
        result, _ = run_s35_case(store, history=LEGACY_HISTORY)
        assert result.response.status is ResponseStatus.RESPONSE_COMMITTED
        assert result.response.reason == OBSERVED_IMMEDIATE_OBJECT_ORIENTATION
        assert result.response.target_proposals == ()
        assert result.response.declared_history_refs == ()
        assert result.decision.branch is TargetBranch.NO_CHANGE
        assert result.decision.reason is TargetReason.NO_PROPOSAL
        assert store.committed_target_ids() == frozenset()


def test_native_rule_registries_remain_empty():
    assert dict(ResponseRuleRegistry.production().rules) == {}
    assert dict(TargetRuleRegistry.production().rules) == {}
