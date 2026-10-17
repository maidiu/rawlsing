from __future__ import annotations

from dataclasses import replace

import pytest

import rawlsing_next.v3_psepf_zero_positive_guard as guard
from rawlsing_next.wsc_gt0_field_forge_ingress import run_gt0_field_forge_ingress
from rawlsing_next.wsc_gt0_prev3_bridge import run_gt0_prev3
from rawlsing_next.wsc_gt0_source_preff import bind_gt0_f0, run_gt0_preff
from rawlsing_next.wsc_gt0_v3_runtime import (
    GT0_GUARD_SOURCE_CLASS,
    GT0V3Checkpoint,
    GT0V3GuardBindingError,
    run_gt0_prev3_v3,
)


def _prev3():
    bound = bind_gt0_f0()
    preff = run_gt0_preff(bound)
    field_forge = run_gt0_field_forge_ingress(preff)
    return run_gt0_prev3(field_forge, f0_ref=bound.f0_ref)


def test_gt0_v3_binds_current_authoritative_guard_and_zero_effect() -> None:
    result = run_gt0_prev3_v3(_prev3())
    decision = result.guard_decision

    assert guard.GUARD_ID == "IG_PSEPF_ZERO_POSITIVE_GUARD"
    assert guard.GUARD_VERSION == "ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE@1"
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES) == {}
    assert decision.guard_id == guard.GUARD_ID
    assert decision.guard_version == guard.GUARD_VERSION
    assert decision.outcome is guard.GuardOutcome.DENY_ZERO_EFFECT
    assert decision.reason is guard.GuardReason.ZERO_POSITIVE_REGISTRY
    assert decision.source_class == GT0_GUARD_SOURCE_CLASS.value == "OPAQUE_PROVENANCE"
    assert decision.delegated_owner_rule_id is None
    assert decision.zero_effect is True
    assert result.before == result.after
    assert "GUARD_ID=IG_PSEPF_ZERO_POSITIVE_GUARD" in result.receipt.detail_code
    assert "GUARD_VERSION=ACTIVE_ZERO_POSITIVE_FIRST_TRANCHE@1" in result.receipt.detail_code
    assert "GUARD_REASON=ZERO_POSITIVE_REGISTRY" in result.receipt.detail_code
    assert any(
        ref.kind == "V3_ZERO_POSITIVE_GUARD_CONTRACT"
        for ref in result.receipt.output_envelope.provenance_refs
    )
    assert any(
        ref.kind == "V3_ZERO_POSITIVE_GUARD_DECISION"
        for ref in result.receipt.output_envelope.replay_refs
    )


def test_gt0_v3_preserves_cursor_state_ledger_rng_and_scheduler() -> None:
    checkpoint = GT0V3Checkpoint(
        actor_state_hash="actor-state-exact",
        causal_ledger_hash="causal-ledger-exact",
        causal_cursor="17",
        rng_state_hash="rng-state-exact",
        scheduler_state_hash="scheduler-state-exact",
    )
    result = run_gt0_prev3_v3(_prev3(), checkpoint=checkpoint)
    fp = result.guard_decision.pre_state_fingerprint

    assert result.before == checkpoint == result.after
    assert fp == result.guard_decision.post_guard_state_fingerprint
    assert fp is not None
    assert fp.actor_state_hash == checkpoint.actor_state_hash
    assert fp.causal_ledger_hash == checkpoint.causal_ledger_hash
    assert fp.causal_cursor == checkpoint.causal_cursor
    assert fp.rng_state_hash == checkpoint.rng_state_hash
    assert fp.scheduler_state_hash == checkpoint.scheduler_state_hash


def test_gt0_v3_calls_authoritative_guard_instead_of_local_shadow(monkeypatch) -> None:
    original = guard.evaluate_psepf_zero_positive_guard
    calls = []

    def spy(payload):
        calls.append(payload)
        return original(payload)

    monkeypatch.setattr(guard, "evaluate_psepf_zero_positive_guard", spy)
    result = run_gt0_prev3_v3(_prev3())

    assert len(calls) == 1
    assert calls[0].source_class is guard.GuardedTruthClass.OPAQUE_PROVENANCE
    assert calls[0].authority is None
    assert result.guard_decision.reason is guard.GuardReason.ZERO_POSITIVE_REGISTRY


def test_gt0_v3_fails_closed_on_authoritative_guard_divergence(monkeypatch) -> None:
    original = guard.evaluate_psepf_zero_positive_guard

    def divergent(payload):
        return replace(original(payload), guard_version="DIVERGED_GUARD_VERSION")

    monkeypatch.setattr(guard, "evaluate_psepf_zero_positive_guard", divergent)
    with pytest.raises(GT0V3GuardBindingError, match="version diverged"):
        run_gt0_prev3_v3(_prev3())
