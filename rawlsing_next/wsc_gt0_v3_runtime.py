"""WSC002R-B GT0 PRE-V3 -> V3 authoritative zero-positive guard binding."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import rawlsing_next.v3_psepf_zero_positive_guard as _v3_guard
from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0StageReceipt,
    GT0StageStatus,
    gt0_content_hash,
    validate_exact_upstream_ref,
)

STAGE_ID = "GT0_PREV3_TO_V3"
GT0_GUARD_SOURCE_CLASS = _v3_guard.GuardedTruthClass.OPAQUE_PROVENANCE
GT0_GUARD_ACTOR_SENTINEL = "GT0_NO_ACTOR_BOUND"
GT0_GUARD_TRANSITION_SURFACE = "GT0.PREV3_TO_V3.ZERO_POSITIVE_FIREWALL"
GT0_GUARD_OPERATION_CLASS = "VALIDATE_ZERO_EFFECT_ONLY"


class GT0V3GuardBindingError(RuntimeError):
    """The GT0 V3 adapter diverged from the accepted zero-positive guard."""


@dataclass(frozen=True, slots=True)
class GT0V3Checkpoint:
    actor_state_hash: str
    causal_ledger_hash: str
    rng_state_hash: str
    scheduler_state_hash: str
    causal_cursor: str = "0"

    @property
    def fingerprint(self) -> str:
        return gt0_content_hash({
            "actor_state_hash": self.actor_state_hash,
            "causal_ledger_hash": self.causal_ledger_hash,
            "causal_cursor": self.causal_cursor,
            "rng_state_hash": self.rng_state_hash,
            "scheduler_state_hash": self.scheduler_state_hash,
        })


@dataclass(frozen=True, slots=True)
class GT0V3ZeroEffectResult:
    receipt: GT0StageReceipt
    before: GT0V3Checkpoint
    after: GT0V3Checkpoint
    guard_decision: _v3_guard.GuardDecision


def _default_checkpoint() -> GT0V3Checkpoint:
    return GT0V3Checkpoint(
        actor_state_hash=gt0_content_hash({"gt0": "actor_state", "state": "EMPTY_BASELINE"}),
        causal_ledger_hash=gt0_content_hash({"gt0": "causal_ledger", "events": []}),
        causal_cursor="0",
        rng_state_hash=gt0_content_hash({"gt0": "rng", "state": "UNCHANGED_BASELINE"}),
        scheduler_state_hash=gt0_content_hash({"gt0": "scheduler", "state": "UNCHANGED_BASELINE"}),
    )


def _merged_refs(*groups: Iterable[GT0ExactRef]) -> tuple[GT0ExactRef, ...]:
    by_key: dict[str, GT0ExactRef] = {}
    for group in groups:
        for ref in group:
            exact = validate_exact_upstream_ref(ref)
            by_key[exact.key] = exact
    return tuple(by_key[key] for key in sorted(by_key))


def _guard_contract_ref() -> GT0ExactRef:
    content_hash = gt0_content_hash({
        "guard_id": _v3_guard.GUARD_ID,
        "guard_version": _v3_guard.GUARD_VERSION,
        "source_class": GT0_GUARD_SOURCE_CLASS.value,
        "production_registry_empty": not bool(
            _v3_guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
        ),
    })
    return GT0ExactRef(
        kind="V3_ZERO_POSITIVE_GUARD_CONTRACT",
        value=(
            f"rawlsing_next/v3_psepf_zero_positive_guard.py::"
            f"{_v3_guard.GUARD_ID}::{_v3_guard.GUARD_VERSION}"
        ),
        content_hash=content_hash,
    )


def _guard_decision_ref(decision: _v3_guard.GuardDecision) -> GT0ExactRef:
    content_hash = gt0_content_hash({
        "guard_id": decision.guard_id,
        "guard_version": decision.guard_version,
        "outcome": decision.outcome.value,
        "reason": decision.reason.value,
        "source_class": decision.source_class,
        "transition_surface_id": decision.transition_surface_id,
        "operation_class": decision.operation_class,
        "actor_state_effect": decision.actor_state_effect,
        "causal_ledger_appends": decision.causal_ledger_appends,
        "causal_cursor_delta": decision.causal_cursor_delta,
        "rng_mutations": decision.rng_mutations,
        "scheduler_mutations": decision.scheduler_mutations,
        "zero_effect": decision.zero_effect,
    })
    return GT0ExactRef(
        kind="V3_ZERO_POSITIVE_GUARD_DECISION",
        value=f"urn:rawlsing:wsc002:v3-zero-positive-guard:sha256:{content_hash}",
        content_hash=content_hash,
    )


def _guard_request(
    prev3_receipt: GT0StageReceipt,
    before: GT0V3Checkpoint,
) -> _v3_guard.GuardRequest:
    """Bind only the PRE-V3 receipt's opaque provenance class to the guard.

    ``GT0_NO_ACTOR_BOUND`` is a schema sentinel, not a generated-person identity:
    GT0 has no actor binding to supply and this adapter creates none.
    """
    return _v3_guard.GuardRequest(
        actor_id=GT0_GUARD_ACTOR_SENTINEL,
        source_class=GT0_GUARD_SOURCE_CLASS,
        source_ref=(
            f"urn:rawlsing:wsc002:stage:{prev3_receipt.stage_id}:"
            f"sha256:{prev3_receipt.content_hash}"
        ),
        source_hash=prev3_receipt.content_hash,
        source_lineage=(),
        transition_surface_id=GT0_GUARD_TRANSITION_SURFACE,
        operation_class=GT0_GUARD_OPERATION_CLASS,
        state_fingerprint=_v3_guard.GuardStateFingerprint(
            actor_state_hash=before.actor_state_hash,
            causal_ledger_hash=before.causal_ledger_hash,
            causal_cursor=before.causal_cursor,
            rng_state_hash=before.rng_state_hash,
            scheduler_state_hash=before.scheduler_state_hash,
        ),
        authority=None,
    )


def _evaluate_authoritative_guard(
    prev3_receipt: GT0StageReceipt,
    before: GT0V3Checkpoint,
) -> _v3_guard.GuardDecision:
    if dict(_v3_guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES):
        raise GT0V3GuardBindingError(
            "accepted production V3 positive-transition registry is no longer empty"
        )

    decision = _v3_guard.evaluate_psepf_zero_positive_guard(
        _guard_request(prev3_receipt, before)
    )
    if not isinstance(decision, _v3_guard.GuardDecision):
        raise GT0V3GuardBindingError("authoritative V3 guard returned an invalid decision")
    if decision.guard_id != _v3_guard.GUARD_ID:
        raise GT0V3GuardBindingError("authoritative V3 guard identity diverged")
    if decision.guard_version != _v3_guard.GUARD_VERSION:
        raise GT0V3GuardBindingError("authoritative V3 guard version diverged")
    if decision.outcome is not _v3_guard.GuardOutcome.DENY_ZERO_EFFECT:
        raise GT0V3GuardBindingError("GT0 cannot delegate to a positive V3 transition owner")
    if decision.reason is not _v3_guard.GuardReason.ZERO_POSITIVE_REGISTRY:
        raise GT0V3GuardBindingError("authoritative V3 guard reason diverged from zero registry")
    if decision.source_class != GT0_GUARD_SOURCE_CLASS.value:
        raise GT0V3GuardBindingError("GT0 guard source class was promoted or relabeled")
    if decision.delegated_owner_rule_id is not None:
        raise GT0V3GuardBindingError("GT0 guard unexpectedly delegated to an owner rule")
    if not decision.zero_effect:
        raise GT0V3GuardBindingError("authoritative V3 guard did not prove exact zero effect")

    expected_fingerprint = _guard_request(prev3_receipt, before).state_fingerprint
    if decision.pre_state_fingerprint != expected_fingerprint:
        raise GT0V3GuardBindingError("authoritative V3 guard pre-state fingerprint diverged")
    if decision.post_guard_state_fingerprint != expected_fingerprint:
        raise GT0V3GuardBindingError("authoritative V3 guard mutated the state fingerprint")
    return decision


def run_gt0_prev3_v3(
    prev3_receipt: GT0StageReceipt,
    *,
    checkpoint: GT0V3Checkpoint | None = None,
) -> GT0V3ZeroEffectResult:
    if not isinstance(prev3_receipt, GT0StageReceipt):
        raise TypeError("prev3_receipt must be GT0StageReceipt")
    before = _default_checkpoint() if checkpoint is None else checkpoint
    if not isinstance(before, GT0V3Checkpoint):
        raise TypeError("checkpoint must be GT0V3Checkpoint")

    # This is the authoritative zero-effect proof. The GT0 wrapper does not
    # synthesize comparator/PSEPF/positive authority merely to exercise it.
    guard_decision = _evaluate_authoritative_guard(prev3_receipt, before)

    if prev3_receipt.status is GT0StageStatus.INTEGRITY_FAILURE:
        status = GT0StageStatus.INTEGRITY_FAILURE
        detail = "UPSTREAM_INTEGRITY_FAILURE__ZERO_V3_EFFECT"
    elif prev3_receipt.status is GT0StageStatus.DENIED:
        status = GT0StageStatus.DENIED
        detail = "UPSTREAM_DENIAL_PRESERVED__ZERO_V3_EFFECT"
    else:
        # Comparator ancestry remains the narrower GT0 baseline blocker. Exact
        # zero actor effect is separately demonstrated by the accepted guard.
        status = GT0StageStatus.BLOCKED_COMPARATOR_ANCESTRY
        detail = (
            "NO_EXACT_POSITIONED_SUBJECT_POSSIBILITY__"
            "NO_COMPARATOR_PREDICATE_ANCESTRY__"
            "NO_POSITIVE_TRANSITION_AUTHORITY__ZERO_V3_EFFECT"
        )

    source = prev3_receipt.output_envelope
    guard_contract_ref = _guard_contract_ref()
    guard_decision_ref = _guard_decision_ref(guard_decision)
    env = GT0ConservationEnvelope(
        semantic_owner_ref=source.semantic_owner_ref,
        object_refs=source.object_refs,
        authority_refs=source.authority_refs,
        current_selection_refs=source.current_selection_refs,
        scope_refs=source.scope_refs,
        relation_query_refs=source.relation_query_refs,
        permission_ceiling=source.permission_ceiling,
        status=status,
        dependency_refs=_merged_refs(
            source.dependency_refs,
            (guard_contract_ref, guard_decision_ref),
        ),
        provenance_refs=_merged_refs(
            source.provenance_refs,
            (guard_contract_ref, guard_decision_ref),
        ),
        replay_refs=_merged_refs(
            source.replay_refs,
            (guard_contract_ref, guard_decision_ref),
        ),
        information_loss=source.information_loss,
    )
    after = before
    receipt = GT0StageReceipt(
        stage_id=STAGE_ID,
        status=status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=env,
        upstream_refs=prev3_receipt.upstream_refs,
        authority_refs=prev3_receipt.authority_refs,
        replay_refs=_merged_refs(
            prev3_receipt.replay_refs,
            (guard_contract_ref, guard_decision_ref),
        ),
        detail_code=(
            f"{detail}__"
            f"GUARD_ID={guard_decision.guard_id}__"
            f"GUARD_VERSION={guard_decision.guard_version}__"
            f"GUARD_OUTCOME={guard_decision.outcome.value}__"
            f"GUARD_REASON={guard_decision.reason.value}__"
            f"GUARD_SOURCE_CLASS={guard_decision.source_class}__"
            f"ACTOR_BINDING=NONE__"
            f"STATE={before.actor_state_hash}__"
            f"LEDGER={before.causal_ledger_hash}__"
            f"CURSOR={before.causal_cursor}__"
            f"RNG={before.rng_state_hash}__"
            f"SCHEDULER={before.scheduler_state_hash}"
        ),
    )
    if before != after:
        raise AssertionError("GT0 zero-effect runtime mutated V3 checkpoint")
    return GT0V3ZeroEffectResult(
        receipt=receipt,
        before=before,
        after=after,
        guard_decision=guard_decision,
    )


__all__ = [
    "STAGE_ID",
    "GT0_GUARD_SOURCE_CLASS",
    "GT0_GUARD_ACTOR_SENTINEL",
    "GT0_GUARD_TRANSITION_SURFACE",
    "GT0_GUARD_OPERATION_CLASS",
    "GT0V3GuardBindingError",
    "GT0V3Checkpoint",
    "GT0V3ZeroEffectResult",
    "run_gt0_prev3_v3",
]
