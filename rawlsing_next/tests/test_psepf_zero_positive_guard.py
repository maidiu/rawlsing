from __future__ import annotations

import copy
import random

import pytest

from rawlsing_next.v3_psepf_zero_positive_guard import (
    AcceptedPositiveTransitionAuthority,
    DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES,
    GuardOutcome,
    GuardReason,
    GuardedTruthClass,
    _coerce_request,
    _evaluate_request_against_registry,
    evaluate_psepf_zero_positive_guard,
)


def _state() -> dict[str, object]:
    return {
        "actor_state_hash": "actor-before",
        "causal_ledger_hash": "ledger-before",
        "causal_cursor": 41,
        "rng_state_hash": "rng-before",
        "scheduler_state_hash": "scheduler-before",
    }


def _request(source_class: str = "PSEPF") -> dict[str, object]:
    return {
        "actor_id": "actor-1",
        "source_class": source_class,
        "source_ref": "source:1",
        "source_hash": "source-hash-1",
        "source_lineage": [],
        "transition_surface_id": "V3.TEST.TRANSITION",
        "operation_class": "ADD_TEST_STATE",
        "state_fingerprint": _state(),
    }


def _accepted() -> AcceptedPositiveTransitionAuthority:
    return AcceptedPositiveTransitionAuthority(
        authority_id="TEST_ONLY_POSITIVE_AUTHORITY",
        authority_version="1.0.0",
        authority_content_hash="authority-hash",
        acceptance_ref="test-only-acceptance-ref",
        acceptance_hash="acceptance-hash",
        owner_rule_id="TEST_ONLY_OWNER_RULE",
        owner_rule_version="1.0.0",
        owner_rule_content_hash="owner-rule-hash",
        transition_surface_id="V3.TEST.TRANSITION",
        operation_class="ADD_TEST_STATE",
        allowed_source_classes=(GuardedTruthClass.PSEPF,),
    )


def _presentation() -> dict[str, str]:
    return {
        "authority_id": "TEST_ONLY_POSITIVE_AUTHORITY",
        "authority_version": "1.0.0",
        "authority_content_hash": "authority-hash",
        "acceptance_ref": "test-only-acceptance-ref",
        "acceptance_hash": "acceptance-hash",
        "owner_rule_id": "TEST_ONLY_OWNER_RULE",
        "owner_rule_version": "1.0.0",
        "owner_rule_content_hash": "owner-rule-hash",
        "transition_surface_id": "V3.TEST.TRANSITION",
        "operation_class": "ADD_TEST_STATE",
    }


def _assert_zero(decision) -> None:
    assert decision.zero_effect is True
    assert decision.actor_state_effect == "ZERO"
    assert decision.causal_ledger_appends == 0
    assert decision.causal_cursor_delta == 0
    assert decision.rng_mutations == 0
    assert decision.scheduler_mutations == 0
    assert decision.pre_state_fingerprint == decision.post_guard_state_fingerprint


def test_active_registry_is_exactly_zero_positive() -> None:
    assert dict(DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}


@pytest.mark.parametrize(
    "source_class",
    [
        "PSEPF",
        "V3EmpiricalPossibilityInput",
        "ResolvedStructuralContext",
        "StructuralPriorRepository",
        "V553_V558_STRUCTURAL_OBJECT",
        "OBSERVER_TRUTH",
        "ANALYST_TRUTH",
        "ActorComparatorReceipt",
        "ReplayReceipt",
        "OPAQUE_PROVENANCE",
    ],
)
def test_guarded_truth_has_zero_effect_without_positive_authority(source_class: str) -> None:
    request = _request(source_class)
    before = copy.deepcopy(request)
    decision = evaluate_psepf_zero_positive_guard(request)
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is GuardReason.ZERO_POSITIVE_REGISTRY
    _assert_zero(decision)
    assert request == before


def test_true_observer_fact_cannot_become_actor_knowledge() -> None:
    request = _request("OBSERVER_TRUTH")
    request["operation_class"] = "ADD_KNOWLEDGE"
    decision = evaluate_psepf_zero_positive_guard(request)
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    _assert_zero(decision)


def test_authority_claim_without_external_acceptance_is_still_zero_effect() -> None:
    request = _request()
    request["authority"] = _presentation()
    decision = evaluate_psepf_zero_positive_guard(request)
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is GuardReason.UNACCEPTED_AUTHORITY
    _assert_zero(decision)


@pytest.mark.parametrize(
    ("field", "wrong_value"),
    [
        ("authority_version", "9.9.9"),
        ("acceptance_hash", "wrong-acceptance"),
        ("owner_rule_content_hash", "wrong-owner-rule"),
        ("transition_surface_id", "V3.WRONG.SURFACE"),
        ("operation_class", "WRONG_OPERATION"),
    ],
)
def test_wrong_exact_authority_binding_is_zero_effect(field: str, wrong_value: str) -> None:
    accepted = _accepted()
    registry = {accepted.registry_key: accepted}
    request = _request()
    presentation = _presentation()
    presentation[field] = wrong_value
    request["authority"] = presentation
    decision = _evaluate_request_against_registry(
        _coerce_request(request),
        registry,
    )
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason in {
        GuardReason.UNACCEPTED_AUTHORITY,
        GuardReason.AUTHORITY_BINDING_MISMATCH,
    }
    _assert_zero(decision)


def test_generic_wrapper_or_alias_fails_closed() -> None:
    request = _request("GENERIC_WRAPPER")
    request["source_lineage"] = ["PSEPF"]
    decision = evaluate_psepf_zero_positive_guard(request)
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is GuardReason.INVALID_OR_UNTYPED_REQUEST
    _assert_zero(decision)


def test_exact_authority_cannot_smuggle_unbound_structural_lineage() -> None:
    accepted = _accepted()
    registry = {accepted.registry_key: accepted}
    request = _request()
    request["source_lineage"] = ["ResolvedStructuralContext"]
    request["authority"] = _presentation()
    decision = _evaluate_request_against_registry(
        _coerce_request(request),
        registry,
    )
    assert decision.outcome is GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is GuardReason.SOURCE_CLASS_NOT_AUTHORIZED
    _assert_zero(decision)


def test_runtime_caller_cannot_override_zero_positive_registry() -> None:
    accepted = _accepted()
    request = _request()
    request["authority"] = _presentation()
    with pytest.raises(TypeError):
        evaluate_psepf_zero_positive_guard(
            request,
            accepted_authorities={accepted.registry_key: accepted},
        )


def test_exact_separately_accepted_binding_only_delegates_and_guard_remains_zero_effect() -> None:
    accepted = _accepted()
    registry = {accepted.registry_key: accepted}
    request = _request()
    request["authority"] = _presentation()
    random_before = random.getstate()
    request_before = copy.deepcopy(request)

    decision = _evaluate_request_against_registry(
        _coerce_request(request),
        registry,
    )

    assert decision.outcome is GuardOutcome.DELEGATE_TO_ACCEPTED_OWNER
    assert decision.reason is GuardReason.EXACT_ACCEPTED_AUTHORITY
    assert decision.delegated_owner_rule_id == "TEST_ONLY_OWNER_RULE"
    _assert_zero(decision)
    assert request == request_before
    assert random.getstate() == random_before
