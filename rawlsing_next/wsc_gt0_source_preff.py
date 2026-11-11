"""Integrated WSC002B GT0 source/PRE-FF binding."""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
    GT0StageReceipt,
    GT0StageStatus,
)

F0_SOURCE_STRUCTURE_ID = "cssu.r1.afrobarometer.r1.005b474d6eb4253cb166"
F0_ADMITTED_UPSTREAM_GIT_SHA = "ba23b0fc1d22bb35abb8a6e8f9ab6100df8f7564"
F0_SOURCE_STRUCTURE_TYPE = "MATRIX_GRID"
F0_SOURCE_NATIVE_LABEL = "Current-versus-past freedoms and equality"
F0_MEMBERS = ("pfesol", "pfrsay", "pfrass", "pfrvot", "pfreql", "pfpsaf")
F0_ROW_IDENTITY_SHA256 = "ef21f9f95c26e7ddd833401618e70cddcebdb7250ba7605de97a3387665843c6"
F0_SOURCE_DOCUMENT_SHA256 = "f603d9f5f95a3898dc42661b3cf8da749f874594b8770fe5fd5fb44f696eb537"
F0_PERMISSION = ("REFERENCE_ONLY__NO_RESPONDENT_VALUES__NO_EXECUTABLE_J",)
F0_INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING"

@dataclass(frozen=True, slots=True)
class GT0SourcePreFFResult:
    receipt: GT0StageReceipt
    f0_ref: GT0ExactRef

def _refs():
    f0 = GT0ExactRef("CURRENT_SOURCE_STRUCTURE", F0_SOURCE_STRUCTURE_ID, F0_ROW_IDENTITY_SHA256)
    owner = GT0ExactRef("SEMANTIC_OWNER", "J01A_CURRENT_JOINT_SOURCE_CANDIDACY")
    authority = GT0ExactRef("J01A_UPSTREAM_GIT_REF", F0_ADMITTED_UPSTREAM_GIT_SHA, F0_ADMITTED_UPSTREAM_GIT_SHA)
    scope = GT0ExactRef("SOURCE_SCOPE", "Afrobarometer:R1")
    relation = GT0ExactRef(
        "SOURCE_NATIVE_RELATION",
        f"{F0_SOURCE_STRUCTURE_TYPE}:{F0_SOURCE_NATIVE_LABEL}",
        F0_ROW_IDENTITY_SHA256,
    )
    source_doc = GT0ExactRef("SOURCE_DOCUMENT_SHA256", F0_SOURCE_DOCUMENT_SHA256, F0_SOURCE_DOCUMENT_SHA256)
    replay = GT0ExactRef("GT0_F0_REPLAY_ROOT", F0_ROW_IDENTITY_SHA256, F0_ROW_IDENTITY_SHA256)
    return f0, owner, authority, scope, relation, source_doc, replay

def bind_gt0_f0() -> GT0SourcePreFFResult:
    f0, owner, authority, scope, relation, source_doc, replay = _refs()
    env = GT0ConservationEnvelope(
        semantic_owner_ref=owner,
        object_refs=(f0,),
        authority_refs=(authority,),
        current_selection_refs=(f0,),
        scope_refs=(scope,),
        relation_query_refs=(relation,),
        permission_ceiling=F0_PERMISSION,
        status=GT0StageStatus.PASS,
        dependency_refs=(source_doc, authority),
        provenance_refs=(source_doc, authority, f0),
        replay_refs=(replay, source_doc, authority),
        information_loss=F0_INFORMATION_LOSS,
    )
    receipt = GT0StageReceipt(
        stage_id="GT0_F0_BIND",
        status=GT0StageStatus.PASS,
        input_envelope_hashes=(),
        output_envelope=env,
        upstream_refs=(f0, authority),
        authority_refs=(authority,),
        replay_refs=(replay,),
        detail_code=(
            "F0_BOUND_VERIFIED__SOURCE_STRUCTURE_GRAIN__"
            "CURRENT_J_CANDIDATE_NE_EXECUTABLE_J__NO_RESPONDENT_VALUES"
        ),
    )
    return GT0SourcePreFFResult(receipt=receipt, f0_ref=f0)

def run_gt0_preff(bound: GT0SourcePreFFResult | None = None) -> GT0SourcePreFFResult:
    bound = bind_gt0_f0() if bound is None else bound
    if not isinstance(bound, GT0SourcePreFFResult):
        raise TypeError("bound must be GT0SourcePreFFResult")
    source = bound.receipt.output_envelope
    receipt = GT0StageReceipt(
        stage_id="GT0_PREFF",
        status=source.status,
        input_envelope_hashes=(source.content_hash,),
        output_envelope=source,
        upstream_refs=bound.receipt.upstream_refs,
        authority_refs=bound.receipt.authority_refs,
        replay_refs=bound.receipt.replay_refs,
        detail_code=(
            "PREFF_REFERENCE_ONLY__PRODUCER_OWNERSHIP_PRESERVED__"
            "CURRENT_J_CANDIDATE_NE_EXECUTABLE_J"
        ),
    )
    return GT0SourcePreFFResult(receipt=receipt, f0_ref=bound.f0_ref)

__all__ = [
    "F0_SOURCE_STRUCTURE_ID",
    "F0_ADMITTED_UPSTREAM_GIT_SHA",
    "F0_SOURCE_STRUCTURE_TYPE",
    "F0_SOURCE_NATIVE_LABEL",
    "F0_MEMBERS",
    "GT0SourcePreFFResult",
    "bind_gt0_f0",
    "run_gt0_preff",
]
