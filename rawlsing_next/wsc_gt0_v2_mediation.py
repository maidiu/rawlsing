"""Integrated WSC002F V3 -> V2 blocked-expression mediation."""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0StageReceipt,
    GT0StageStatus,
)
from rawlsing_next.wsc_gt0_v3_runtime import GT0V3ZeroEffectResult

@dataclass(frozen=True, slots=True)
class GT0V2BlockedResult:
    receipt: GT0StageReceipt
    actor_claim_created: bool
    rendered_text: str | None
    v3_mutated: bool

def run_gt0_v3_v2(v3_result: GT0V3ZeroEffectResult) -> GT0V2BlockedResult:
    if not isinstance(v3_result, GT0V3ZeroEffectResult):
        raise TypeError("v3_result must be GT0V3ZeroEffectResult")
    source_receipt = v3_result.receipt
    source = source_receipt.output_envelope

    if source_receipt.status is GT0StageStatus.INTEGRITY_FAILURE:
        status = GT0StageStatus.INTEGRITY_FAILURE
        detail = "UPSTREAM_INTEGRITY_FAILURE__NO_RENDER"
    elif source_receipt.status is GT0StageStatus.DENIED:
        status = GT0StageStatus.DENIED
        detail = "UPSTREAM_DENIAL_PRESERVED__NO_RENDER"
    else:
        status = GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED
        detail = (
            "NO_ACTOR_SAFE_CLAIM_DERIVED_FROM_F0__"
            "NO_FIRST_PERSON_PERMISSION__NO_ADMITTED_SEMANTIC_RENDER_PLAN__NO_RENDER"
        )

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
    receipt = GT0StageReceipt(
        stage_id="GT0_V3_TO_V2",
        status=status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=env,
        upstream_refs=source_receipt.upstream_refs,
        authority_refs=source_receipt.authority_refs,
        replay_refs=source_receipt.replay_refs,
        detail_code=detail,
    )
    return GT0V2BlockedResult(
        receipt=receipt,
        actor_claim_created=False,
        rendered_text=None,
        v3_mutated=(v3_result.before != v3_result.after),
    )

__all__ = ["GT0V2BlockedResult", "run_gt0_v3_v2"]
