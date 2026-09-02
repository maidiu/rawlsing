"""Integrated WSC002E PRE-V3 -> V3 zero-effect runtime."""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0StageReceipt,
    GT0StageStatus,
    gt0_content_hash,
)

@dataclass(frozen=True, slots=True)
class GT0V3Checkpoint:
    actor_state_hash: str
    causal_ledger_hash: str
    rng_state_hash: str
    scheduler_state_hash: str

    @property
    def fingerprint(self) -> str:
        return gt0_content_hash({
            "actor_state_hash": self.actor_state_hash,
            "causal_ledger_hash": self.causal_ledger_hash,
            "rng_state_hash": self.rng_state_hash,
            "scheduler_state_hash": self.scheduler_state_hash,
        })

@dataclass(frozen=True, slots=True)
class GT0V3ZeroEffectResult:
    receipt: GT0StageReceipt
    before: GT0V3Checkpoint
    after: GT0V3Checkpoint

def _default_checkpoint() -> GT0V3Checkpoint:
    return GT0V3Checkpoint(
        actor_state_hash=gt0_content_hash({"gt0": "actor_state", "state": "EMPTY_BASELINE"}),
        causal_ledger_hash=gt0_content_hash({"gt0": "causal_ledger", "events": []}),
        rng_state_hash=gt0_content_hash({"gt0": "rng", "state": "UNCHANGED_BASELINE"}),
        scheduler_state_hash=gt0_content_hash({"gt0": "scheduler", "state": "UNCHANGED_BASELINE"}),
    )

def run_gt0_prev3_v3(
    prev3_receipt: GT0StageReceipt,
    *,
    checkpoint: GT0V3Checkpoint | None = None,
) -> GT0V3ZeroEffectResult:
    if not isinstance(prev3_receipt, GT0StageReceipt):
        raise TypeError("prev3_receipt must be GT0StageReceipt")
    before = _default_checkpoint() if checkpoint is None else checkpoint

    if prev3_receipt.status is GT0StageStatus.INTEGRITY_FAILURE:
        status = GT0StageStatus.INTEGRITY_FAILURE
        detail = "UPSTREAM_INTEGRITY_FAILURE__ZERO_V3_EFFECT"
    elif prev3_receipt.status is GT0StageStatus.DENIED:
        status = GT0StageStatus.DENIED
        detail = "UPSTREAM_DENIAL_PRESERVED__ZERO_V3_EFFECT"
    else:
        status = GT0StageStatus.BLOCKED_COMPARATOR_ANCESTRY
        detail = (
            "NO_EXACT_POSITIONED_SUBJECT_POSSIBILITY__"
            "NO_COMPARATOR_PREDICATE_ANCESTRY__"
            "NO_POSITIVE_TRANSITION_AUTHORITY__ZERO_V3_EFFECT"
        )

    source = prev3_receipt.output_envelope
    env = GT0ConservationEnvelope(
        semantic_owner_ref=source.semantic_owner_ref,
        object_refs=source.object_refs,
        authority_refs=source.authority_refs,
        current_selection_refs=source.current_selection_refs,
        scope_refs=source.scope_refs,
        relation_query_refs=source.relation_query_refs,
        permission_ceiling=source.permission_ceiling,
        status=status,
        dependency_refs=source.dependency_refs,
        provenance_refs=source.provenance_refs,
        replay_refs=source.replay_refs,
        information_loss=source.information_loss,
    )
    after = before
    receipt = GT0StageReceipt(
        stage_id="GT0_PREV3_TO_V3",
        status=status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=env,
        upstream_refs=prev3_receipt.upstream_refs,
        authority_refs=prev3_receipt.authority_refs,
        replay_refs=prev3_receipt.replay_refs,
        detail_code=(
            f"{detail}__STATE={before.actor_state_hash}__LEDGER={before.causal_ledger_hash}__"
            f"RNG={before.rng_state_hash}__SCHEDULER={before.scheduler_state_hash}"
        ),
    )
    if before != after:
        raise AssertionError("GT0 zero-effect runtime mutated V3 checkpoint")
    return GT0V3ZeroEffectResult(receipt=receipt, before=before, after=after)

__all__ = [
    "GT0V3Checkpoint",
    "GT0V3ZeroEffectResult",
    "run_gt0_prev3_v3",
]
