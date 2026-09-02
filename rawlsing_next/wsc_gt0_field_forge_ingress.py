"""Integrated WSC002C PRE-FF -> FIELD FORGE GT0 ingress."""
from __future__ import annotations

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0StageReceipt,
    GT0StageStatus,
)
from rawlsing_next.wsc_gt0_source_preff import GT0SourcePreFFResult

INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"

def run_gt0_field_forge_ingress(preff: GT0SourcePreFFResult) -> GT0StageReceipt:
    if not isinstance(preff, GT0SourcePreFFResult):
        raise TypeError("preff must be GT0SourcePreFFResult")
    source = preff.receipt.output_envelope
    if source.information_loss != INFORMATION_LOSS:
        raise ValueError("GT0 FIELD FORGE baseline must remain reference-preserving")
    env = GT0ConservationEnvelope(
        semantic_owner_ref=source.semantic_owner_ref,
        object_refs=source.object_refs,
        authority_refs=source.authority_refs,
        current_selection_refs=source.current_selection_refs,
        scope_refs=source.scope_refs,
        relation_query_refs=source.relation_query_refs,
        permission_ceiling=source.permission_ceiling,
        status=source.status,
        dependency_refs=source.dependency_refs,
        provenance_refs=source.provenance_refs,
        replay_refs=source.replay_refs,
        information_loss=source.information_loss,
    )
    return GT0StageReceipt(
        stage_id="GT0_FIELD_FORGE_INGRESS",
        status=source.status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=env,
        upstream_refs=preff.receipt.upstream_refs,
        authority_refs=preff.receipt.authority_refs,
        replay_refs=preff.receipt.replay_refs,
        detail_code=(
            "ACTOR_INDEPENDENT_REFERENCE_ONLY__NO_SEMANTIC_REOWNERSHIP__"
            "NO_FIELD_CAPITAL_HEGEMONY_HOMOLOGY_PRESSURE_MECHANISM__"
            "NO_NEW_FIELD_FORGE_RELATION_MINTED"
        ),
    )

__all__ = ["INFORMATION_LOSS", "run_gt0_field_forge_ingress"]
