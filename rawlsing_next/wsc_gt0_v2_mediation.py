"""Integrated WSC002F V3 -> V2 blocked-expression mediation.

WSC002R-C binds the GT0 negative path to the accepted current M6 and bounded
rendering authority surfaces.  It deliberately does not construct an
ActorSafeClaimEntry, positive actor-safe envelope, ExpressionProjection,
admitted render plan, renderer binding, wording variant, model call, or causal
return merely to prove that the current path is blocked.
"""
from __future__ import annotations

from dataclasses import dataclass

from rawlsing_next import m6_actor_safe_expression as m6
from rawlsing_next import render_bounded_expression as bounded_render
from rawlsing_next.wsc_gt0_protocol import (
    GT0ConservationEnvelope,
    GT0ExactRef,
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
    m6_contract_id: str | None = None
    m6_negative_status: str | None = None
    render_contract_id: str | None = None
    render_plan_authority_status: str | None = None
    model_invocation_count: int = 0


def _bind_authoritative_negative_surfaces(source: GT0ConservationEnvelope) -> tuple[
    tuple[GT0ExactRef, ...],
    str,
    str,
    str,
]:
    """Prove the baseline blocker from current M6/render law, not GT0-local text."""
    if bounded_render.BOUND_M6_CONTRACT_ID != m6.M6_CONTRACT_ID:
        raise AssertionError(
            "bounded renderer is not bound to the current M6 contract identity"
        )

    source_rejection = None
    try:
        m6.assert_behavioral_source_rejected(
            source,
            representation="GT0_CONSERVATION_ENVELOPE",
        )
    except m6.M6ForbiddenBehavioralSource as exc:
        source_rejection = type(exc).__name__
    if source_rejection != "M6ForbiddenBehavioralSource":
        raise AssertionError(
            "current M6 generic behavioral-source firewall did not reject GT0 upstream material"
        )

    m6_status = m6.situated_expression_behavior_status()
    if m6_status != m6.BLOCKED_NAMED_AUTHORITY_REQUIRED:
        raise AssertionError(
            "current M6 situated-expression ceiling diverged from BLOCKED_NAMED_AUTHORITY_REQUIRED"
        )

    owner_block = None
    try:
        m6.require_situated_expression_owner()
    except m6.M6NamedAuthorityRequired as exc:
        owner_block = type(exc).__name__
    if owner_block != "M6NamedAuthorityRequired":
        raise AssertionError(
            "current M6 situated-expression owner requirement did not fail closed"
        )

    render_status = bounded_render.current_positive_plan_authority_status()
    if render_status != m6.BLOCKED_NAMED_AUTHORITY_REQUIRED:
        raise AssertionError(
            "current bounded-render positive-plan authority ceiling diverged from "
            "BLOCKED_NAMED_AUTHORITY_REQUIRED"
        )

    bindings = (
        GT0ExactRef("M6_CONTRACT_ID", m6.M6_CONTRACT_ID),
        GT0ExactRef("M6_NEGATIVE_BEHAVIOR_STATUS", m6_status),
        GT0ExactRef("M6_NEGATIVE_SOURCE_FIREWALL", source_rejection),
        GT0ExactRef("M6_SITUATED_OWNER_BLOCKER", owner_block),
        GT0ExactRef("RENDER_CONTRACT_ID", bounded_render.IG_RENDER_CONTRACT_ID),
        GT0ExactRef("RENDER_BOUND_M6_CONTRACT_ID", bounded_render.BOUND_M6_CONTRACT_ID),
        GT0ExactRef("RENDER_POSITIVE_PLAN_AUTHORITY_STATUS", render_status),
    )
    return bindings, m6_status, render_status, source_rejection


def run_gt0_v3_v2(v3_result: GT0V3ZeroEffectResult) -> GT0V2BlockedResult:
    if not isinstance(v3_result, GT0V3ZeroEffectResult):
        raise TypeError("v3_result must be GT0V3ZeroEffectResult")
    source_receipt = v3_result.receipt
    source = source_receipt.output_envelope

    binding_refs: tuple[GT0ExactRef, ...] = ()
    m6_status: str | None = None
    render_status: str | None = None
    m6_contract_id: str | None = None
    render_contract_id: str | None = None

    if source_receipt.status is GT0StageStatus.INTEGRITY_FAILURE:
        status = GT0StageStatus.INTEGRITY_FAILURE
        detail = "UPSTREAM_INTEGRITY_FAILURE__NO_RENDER"
    elif source_receipt.status is GT0StageStatus.DENIED:
        status = GT0StageStatus.DENIED
        detail = "UPSTREAM_DENIAL_PRESERVED__NO_RENDER"
    else:
        (
            binding_refs,
            m6_status,
            render_status,
            source_rejection,
        ) = _bind_authoritative_negative_surfaces(source)
        m6_contract_id = m6.M6_CONTRACT_ID
        render_contract_id = bounded_render.IG_RENDER_CONTRACT_ID
        status = GT0StageStatus.BLOCKED_NAMED_AUTHORITY_REQUIRED
        detail = (
            "AUTHORITATIVE_M6_RENDER_NEGATIVE_BINDING__"
            f"M6_CONTRACT={m6_contract_id}__"
            f"M6_SOURCE_FIREWALL={source_rejection}__"
            f"M6_SITUATED_STATUS={m6_status}__"
            "M6_OWNER_BLOCKER=M6NamedAuthorityRequired__"
            f"RENDER_CONTRACT={render_contract_id}__"
            f"RENDER_BOUND_M6={bounded_render.BOUND_M6_CONTRACT_ID}__"
            f"RENDER_PLAN_STATUS={render_status}__"
            "NO_ACTOR_SAFE_CLAIM_ENTRY__NO_FIRST_PERSON_PERMISSION__"
            "NO_ADMITTED_SEMANTIC_RENDER_PLAN__NO_RENDERER_BINDING__"
            "NO_WORDING_VARIANT__MODEL_CALLS=0__NO_RENDERED_ARTIFACT__"
            "NO_CAUSAL_RETURN"
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
        provenance_refs=(*source.provenance_refs, *binding_refs),
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
        m6_contract_id=m6_contract_id,
        m6_negative_status=m6_status,
        render_contract_id=render_contract_id,
        render_plan_authority_status=render_status,
        model_invocation_count=0,
    )


__all__ = ["GT0V2BlockedResult", "run_gt0_v3_v2"]
