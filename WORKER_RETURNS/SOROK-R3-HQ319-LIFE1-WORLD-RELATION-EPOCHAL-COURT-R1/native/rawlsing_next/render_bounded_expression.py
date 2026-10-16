#!/usr/bin/env python3
"""Bounded rendering over the accepted M6 actor-safe expression runtime.

This module owns no actor truth, situated phenomenology, disclosure planning,
salience, inhibition, affective foregrounding, interlocutor openness,
psychological register/voice selection, relationship interpretation, or
response-move selection.  It realizes wording only after an independently
admitted semantic plan is bound to one exact M6 ExpressionProjection.

The current implementation intentionally contains no accepted positive
semantic-plan authority.  Integrators must supply an exact accepted authority
binding; absent that binding, render realization fails closed with
BLOCKED_NAMED_AUTHORITY_REQUIRED.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import unicodedata
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.m6_actor_safe_expression import (
    BLOCKED_NAMED_AUTHORITY_REQUIRED,
    M6_CONTRACT_ID,
    ActorAccessibleRenderEnvelope,
    ActorSafeRef,
    ExpressionProjection,
    OpaqueAuditRef,
    ReceiverSnapshot,
    ReceiverState,
    ReplayClosure,
    ScopeCeiling,
    assert_behavioral_source_rejected,
    canonical_json,
    evaluate_actor_safe_ingress,
    project_actor_safe_entry,
)


IG_RENDER_CONTRACT_ID = "IG_RENDER_BOUNDED_REALIZATION@1.0.0"
BOUND_M6_RUNTIME_HEAD = "c7dfd69131d0909cd0e4a7bec223ba64ec5d6167"
BOUND_M6_RUNTIME_FILE = "rawlsing_next/m6_actor_safe_expression.py"
BOUND_M6_RUNTIME_BLOB = "74d9701cdc7dabccf61eb5089498db290c1efd9c"
BOUND_M6_SEMANTIC_HEAD = "a93335e577f018241d3d027bb8827a79907b9f28"
BOUND_SCRV2APP_HEAD = "24f8811bb7d2eaa18cfac1cb907c48bba8d08f23"
BOUND_RENDER_PREFLIGHT_HEAD = "385651927ff74c0edf3bce55a5174dfc8e59951e"
BOUND_M6_CONTRACT_ID = "M6_V3_TO_V2_ACTOR_SAFE_EXPRESSION_SEAM@1.0.0"

if M6_CONTRACT_ID != BOUND_M6_CONTRACT_ID:
    raise RuntimeError("IG-RENDER imported an M6 runtime with the wrong contract identity")


BLOCKED_SPDM_CLASSES = frozenset({
    "SITUATED_PHENOMENOLOGY",
    "DISCLOSURE_WILLINGNESS",
    "DISCLOSURE_PLANNING",
    "SALIENCE_OR_FOREGROUND_SELECTION",
    "INHIBITION_OR_SUPPRESSION_PSYCHOLOGY",
    "AFFECTIVE_FOREGROUNDING",
    "INTERLOCUTOR_SPECIFIC_OPENNESS",
    "PSYCHOLOGICAL_REGISTER_OR_VOICE_SELECTION",
})


class RenderIntegrityError(ValueError):
    """Exact binding, replay, or immutable-plan identity failed."""


class RenderSemanticConformanceError(ValueError):
    """Candidate wording or declared semantic bindings exceeded the plan."""


class RenderState(str, Enum):
    BLOCKED_M6_HANDOFF_INTEGRITY = "BLOCKED_M6_HANDOFF_INTEGRITY"
    BLOCKED_M6_STALE = "BLOCKED_M6_STALE"
    BLOCKED_M6_DEFER = "BLOCKED_M6_DEFER"
    BLOCKED_M6_DENY = "BLOCKED_M6_DENY"
    BLOCKED_M6_ABSENT = "BLOCKED_M6_ABSENT"
    VALID_EMPTY_NO_MODEL_CALL = "VALID_EMPTY_NO_MODEL_CALL"
    BLOCKED_NAMED_AUTHORITY_REQUIRED = BLOCKED_NAMED_AUTHORITY_REQUIRED
    ACCEPTED_BOUNDED_RENDER = "ACCEPTED_BOUNDED_RENDER"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RenderIntegrityError(f"{name} must be a non-empty string")
    result = unicodedata.normalize("NFC", value.strip())
    if result.lower() in {"latest", "default", "*"}:
        raise RenderIntegrityError(f"{name} may not use mutable/latest/default selection")
    return result


def _hash_text(value: Any, name: str) -> str:
    result = _text(value, name)
    if len(result) < 8:
        raise RenderIntegrityError(f"{name} is not an exact immutable hash/binding")
    return result


def _sha(material: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def _ref_dict(ref: ActorSafeRef) -> dict[str, str]:
    return ref.as_dict()


def _ref_keys(refs: Sequence[ActorSafeRef]) -> tuple[str, ...]:
    return tuple(sorted(ref.key for ref in refs))


@dataclass(frozen=True, order=True)
class ExactAuthorityBinding:
    authority_id: str
    authority_version: str
    authority_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "authority_id", _text(self.authority_id, "authority_id"))
        object.__setattr__(self, "authority_version", _text(self.authority_version, "authority_version"))
        object.__setattr__(self, "authority_hash", _hash_text(self.authority_hash, "authority_hash"))

    def as_dict(self) -> dict[str, str]:
        return {
            "authority_id": self.authority_id,
            "authority_version": self.authority_version,
            "authority_hash": self.authority_hash,
        }


@dataclass(frozen=True)
class AuthorizedWordingVariant:
    variant_id: str
    text: str
    projection_fingerprint: str
    variant_hash: str

    def as_core(self) -> dict[str, str]:
        return {
            "variant_id": self.variant_id,
            "text": self.text,
            "projection_fingerprint": self.projection_fingerprint,
        }


def _make_variant(
    projection: ExpressionProjection,
    variant_id: str,
    text: str,
) -> AuthorizedWordingVariant:
    clean_id = _text(variant_id, "variant_id")
    clean_text = _text(text, "wording_variant.text")
    variant = AuthorizedWordingVariant(
        clean_id,
        clean_text,
        projection.semantic_fingerprint,
        "",
    )
    return replace(variant, variant_hash=_sha(variant.as_core()))


@dataclass(frozen=True)
class AdmittedRenderPlan:
    plan_id: str
    plan_hash: str
    plan_authority: ExactAuthorityBinding
    admission_receipt_ref: ActorSafeRef
    projection_fingerprint: str
    claim_ref: ActorSafeRef
    component_refs: tuple[ActorSafeRef, ...]
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    temporal_scope_refs: tuple[str, ...]
    subject_scope_refs: tuple[str, ...]
    referent_scope_refs: tuple[str, ...]
    first_person_permission: str
    source_entry_hash: str
    wording_variants: tuple[AuthorizedWordingVariant, ...]

    def as_core(self) -> dict[str, Any]:
        return {
            "plan_authority": self.plan_authority.as_dict(),
            "admission_receipt_ref": self.admission_receipt_ref.as_dict(),
            "projection_fingerprint": self.projection_fingerprint,
            "claim_ref": self.claim_ref.as_dict(),
            "component_refs": [_ref_dict(item) for item in self.component_refs],
            "actor_perceived_view_refs": [_ref_dict(item) for item in self.actor_perceived_view_refs],
            "temporal_scope_refs": list(self.temporal_scope_refs),
            "subject_scope_refs": list(self.subject_scope_refs),
            "referent_scope_refs": list(self.referent_scope_refs),
            "first_person_permission": self.first_person_permission,
            "source_entry_hash": self.source_entry_hash,
            "wording_variants": [variant.as_core() | {"variant_hash": variant.variant_hash} for variant in self.wording_variants],
        }


def make_admitted_render_plan(
    projection: ExpressionProjection,
    *,
    plan_authority: ExactAuthorityBinding,
    admission_receipt_ref: ActorSafeRef,
    wording_variants: Mapping[str, str],
) -> AdmittedRenderPlan:
    """Bind, but never invent, an externally admitted semantic wording plan.

    ``wording_variants`` are treated as already authorized by ``plan_authority``.
    This module does not claim that any such authority is currently accepted.
    """
    if not isinstance(projection, ExpressionProjection):
        raise RenderIntegrityError("plan requires an exact M6 ExpressionProjection")
    if not isinstance(plan_authority, ExactAuthorityBinding):
        raise RenderIntegrityError("plan requires an exact authority binding")
    if not isinstance(admission_receipt_ref, ActorSafeRef):
        raise RenderIntegrityError("plan requires an exact admission receipt ref")
    if not wording_variants:
        raise RenderIntegrityError("an admitted plan requires at least one preauthorized wording variant")
    variants = tuple(
        sorted(
            (_make_variant(projection, key, value) for key, value in wording_variants.items()),
            key=lambda item: item.variant_id,
        )
    )
    if len({item.variant_id for item in variants}) != len(variants):
        raise RenderIntegrityError("wording variant IDs must be unique")
    plan = AdmittedRenderPlan(
        "",
        "",
        plan_authority,
        admission_receipt_ref,
        projection.semantic_fingerprint,
        projection.claim_ref,
        projection.component_refs,
        projection.actor_perceived_view_refs,
        projection.temporal_scope_refs,
        projection.subject_scope_refs,
        projection.referent_scope_refs,
        projection.first_person_permission,
        projection.source_entry_hash,
        variants,
    )
    plan_hash = _sha(plan.as_core())
    return replace(plan, plan_id=f"IGRP:{plan_hash}", plan_hash=plan_hash)


@dataclass(frozen=True)
class RenderExecutionBinding:
    render_policy: ExactAuthorityBinding
    renderer: ExactAuthorityBinding
    variability_receipt_ref: ActorSafeRef

    def __post_init__(self) -> None:
        if not isinstance(self.render_policy, ExactAuthorityBinding):
            raise RenderIntegrityError("render_policy must be an exact authority binding")
        if not isinstance(self.renderer, ExactAuthorityBinding):
            raise RenderIntegrityError("renderer must be an exact authority binding")
        if not isinstance(self.variability_receipt_ref, ActorSafeRef):
            raise RenderIntegrityError("variability_receipt_ref must be exact")

    @property
    def binding_hash(self) -> str:
        return _sha({
            "render_policy": self.render_policy.as_dict(),
            "renderer": self.renderer.as_dict(),
            "variability_receipt_ref": self.variability_receipt_ref.as_dict(),
        })


@dataclass(frozen=True)
class RenderModelInput:
    plan_id: str
    plan_hash: str
    projection_fingerprint: str
    allowed_variants: tuple[AuthorizedWordingVariant, ...]
    execution_binding_hash: str


@dataclass(frozen=True)
class RendererCandidate:
    variant_id: str
    text: str
    projection_fingerprint: str
    claim_ref: ActorSafeRef
    component_refs: tuple[ActorSafeRef, ...]
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    temporal_scope_refs: tuple[str, ...]
    subject_scope_refs: tuple[str, ...]
    referent_scope_refs: tuple[str, ...]
    first_person_permission: str


@dataclass(frozen=True)
class RenderedExpressionArtifact:
    artifact_id: str
    artifact_hash: str
    text: str
    variant_id: str
    variant_hash: str
    plan_id: str
    plan_hash: str
    projection_fingerprint: str
    execution_binding_hash: str
    semantic_authority: bool = False
    causal_occurrence: bool = False


@dataclass(frozen=True)
class RenderOutcome:
    state: RenderState
    receiver_state: ReceiverState | None
    model_called: bool
    semantic_output: bool
    projection_fingerprint: str | None
    artifact: RenderedExpressionArtifact | None
    block_reason: str | None
    audit_fingerprint: str


def _audit_fingerprint(opaque_audit_refs: Sequence[OpaqueAuditRef]) -> str:
    material = []
    for item in opaque_audit_refs:
        if not isinstance(item, OpaqueAuditRef):
            raise RenderIntegrityError("opaque audit inputs must be exact M6 OpaqueAuditRef values")
        material.append(item.as_dict())
    return _sha({"opaque_audit_refs": sorted(material, key=lambda item: (item["audit_role"], item["opaque_ref_id"], item["opaque_ref_hash"]))})


def _zero_outcome(
    state: RenderState,
    receiver_state: ReceiverState | None,
    *,
    reason: str,
    audit_fingerprint: str,
    projection_fingerprint: str | None = None,
) -> RenderOutcome:
    return RenderOutcome(
        state,
        receiver_state,
        False,
        False,
        projection_fingerprint,
        None,
        reason,
        audit_fingerprint,
    )


def _map_nonpositive_receiver(receiver_state: ReceiverState) -> RenderState:
    if receiver_state is ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE:
        return RenderState.BLOCKED_M6_HANDOFF_INTEGRITY
    if receiver_state is ReceiverState.BLOCKED_STALE_ACTOR_SAFE_HANDOFF:
        return RenderState.BLOCKED_M6_STALE
    if receiver_state is ReceiverState.DEFERRED_MISSING_AUTHORITY:
        return RenderState.BLOCKED_M6_DEFER
    if receiver_state is ReceiverState.DENIED_EXPLICIT_FIRST_PERSON_CLAIM:
        return RenderState.BLOCKED_M6_DENY
    if receiver_state is ReceiverState.VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS:
        return RenderState.VALID_EMPTY_NO_MODEL_CALL
    return RenderState.BLOCKED_M6_ABSENT


def _validate_plan(
    plan: AdmittedRenderPlan,
    projection: ExpressionProjection,
    accepted_plan_authority: ExactAuthorityBinding,
) -> None:
    if not isinstance(plan, AdmittedRenderPlan):
        raise RenderIntegrityError("rendering requires an exact admitted render plan")
    if not isinstance(accepted_plan_authority, ExactAuthorityBinding):
        raise RenderIntegrityError("accepted plan authority binding is required")
    if plan.plan_authority != accepted_plan_authority:
        raise RenderIntegrityError("plan authority does not match the exact accepted authority binding")
    if plan.plan_hash != _sha(plan.as_core()) or plan.plan_id != f"IGRP:{plan.plan_hash}":
        raise RenderIntegrityError("admitted render plan identity/hash mismatch")
    if plan.projection_fingerprint != projection.semantic_fingerprint:
        raise RenderSemanticConformanceError("plan is not bound to the exact M6 projection")
    exact_pairs = (
        (plan.claim_ref, projection.claim_ref, "claim"),
        (plan.component_refs, projection.component_refs, "component"),
        (plan.actor_perceived_view_refs, projection.actor_perceived_view_refs, "relationship-view"),
        (plan.temporal_scope_refs, projection.temporal_scope_refs, "temporal"),
        (plan.subject_scope_refs, projection.subject_scope_refs, "subject"),
        (plan.referent_scope_refs, projection.referent_scope_refs, "referent"),
        (plan.first_person_permission, projection.first_person_permission, "permission"),
        (plan.source_entry_hash, projection.source_entry_hash, "source-entry"),
    )
    for planned, projected, label in exact_pairs:
        if planned != projected:
            raise RenderSemanticConformanceError(f"plan {label} binding differs from M6 projection")
    for variant in plan.wording_variants:
        if variant.projection_fingerprint != projection.semantic_fingerprint:
            raise RenderSemanticConformanceError("wording variant is bound to a different projection")
        if variant.variant_hash != _sha(variant.as_core()):
            raise RenderIntegrityError("wording variant hash mismatch")


def _candidate_from_variant(plan: AdmittedRenderPlan, variant: AuthorizedWordingVariant) -> RendererCandidate:
    return RendererCandidate(
        variant.variant_id,
        variant.text,
        plan.projection_fingerprint,
        plan.claim_ref,
        plan.component_refs,
        plan.actor_perceived_view_refs,
        plan.temporal_scope_refs,
        plan.subject_scope_refs,
        plan.referent_scope_refs,
        plan.first_person_permission,
    )


def validate_renderer_candidate(
    candidate: RendererCandidate,
    plan: AdmittedRenderPlan,
    projection: ExpressionProjection,
) -> AuthorizedWordingVariant:
    """Post-render semantic conformance without granting the model authority.

    Candidate text must exactly equal one preauthorized wording variant.  The
    renderer/model cannot introduce a novel sentence and then self-declare it
    semantically equivalent.
    """
    if not isinstance(candidate, RendererCandidate):
        raise RenderSemanticConformanceError("renderer returned an untyped candidate")
    variants = {item.variant_id: item for item in plan.wording_variants}
    if candidate.variant_id not in variants:
        raise RenderSemanticConformanceError("renderer selected an unlisted wording variant")
    variant = variants[candidate.variant_id]
    if candidate.text != variant.text:
        raise RenderSemanticConformanceError("model candidate text is not an exact authorized wording variant")
    if candidate.projection_fingerprint != projection.semantic_fingerprint:
        raise RenderSemanticConformanceError("candidate projection fingerprint changed")
    exact_pairs = (
        (candidate.claim_ref, projection.claim_ref, "claim"),
        (candidate.component_refs, projection.component_refs, "component"),
        (candidate.actor_perceived_view_refs, projection.actor_perceived_view_refs, "relationship-view"),
        (candidate.temporal_scope_refs, projection.temporal_scope_refs, "temporal"),
        (candidate.subject_scope_refs, projection.subject_scope_refs, "subject"),
        (candidate.referent_scope_refs, projection.referent_scope_refs, "referent"),
        (candidate.first_person_permission, projection.first_person_permission, "permission"),
    )
    for proposed, allowed, label in exact_pairs:
        if proposed != allowed:
            raise RenderSemanticConformanceError(f"candidate {label} scope was widened or substituted")
    return variant


def _artifact(
    candidate: RendererCandidate,
    variant: AuthorizedWordingVariant,
    plan: AdmittedRenderPlan,
    projection: ExpressionProjection,
    execution: RenderExecutionBinding,
) -> RenderedExpressionArtifact:
    material = {
        "contract_id": IG_RENDER_CONTRACT_ID,
        "m6_contract_id": BOUND_M6_CONTRACT_ID,
        "plan_id": plan.plan_id,
        "plan_hash": plan.plan_hash,
        "projection_fingerprint": projection.semantic_fingerprint,
        "variant_id": variant.variant_id,
        "variant_hash": variant.variant_hash,
        "text": candidate.text,
        "execution_binding_hash": execution.binding_hash,
        "semantic_authority": False,
        "causal_occurrence": False,
    }
    artifact_hash = _sha(material)
    return RenderedExpressionArtifact(
        f"IGRENDER:{artifact_hash}",
        artifact_hash,
        candidate.text,
        variant.variant_id,
        variant.variant_hash,
        plan.plan_id,
        plan.plan_hash,
        projection.semantic_fingerprint,
        execution.binding_hash,
    )


def current_positive_plan_authority_status() -> str:
    """The dispatch assignment supplies no accepted positive SPDM/plan owner."""
    return BLOCKED_NAMED_AUTHORITY_REQUIRED


def realize_bounded_expression(
    *,
    envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
    requested_claim_ref: ActorSafeRef,
    source_scope_ceiling: ScopeCeiling,
    requested_first_person_permission: str,
    requested_component_refs: Sequence[ActorSafeRef] = (),
    requested_actor_perceived_view_refs: Sequence[ActorSafeRef] = (),
    requested_temporal_scope_refs: Sequence[str] = (),
    requested_subject_scope_refs: Sequence[str] = (),
    requested_referent_scope_refs: Sequence[str] = (),
    session_or_transcript_claim_refs: Sequence[ActorSafeRef] = (),
    requested_spdm_classes: Sequence[str] = (),
    admitted_plan: AdmittedRenderPlan | None = None,
    accepted_plan_authority: ExactAuthorityBinding | None = None,
    execution: RenderExecutionBinding | None = None,
    renderer: Callable[[RenderModelInput], RendererCandidate] | None = None,
    selected_variant_id: str | None = None,
    forbidden_behavioral_sources: Sequence[tuple[Any, str, str]] = (),
    opaque_audit_refs: Sequence[OpaqueAuditRef] = (),
) -> RenderOutcome:
    """Realize one bounded expression attempt.

    ``forbidden_behavioral_sources`` tuples are ``(value, declared_class,
    representation)`` and exist only so callers can prove rejection before any
    renderer/model boundary.  They never reach the model.
    """
    audit_fp = _audit_fingerprint(opaque_audit_refs)

    for value, declared_class, representation in forbidden_behavioral_sources:
        assert_behavioral_source_rejected(
            value,
            declared_source_class=declared_class,
            representation=representation,
        )

    decision = evaluate_actor_safe_ingress(
        envelope,
        replay_closure,
        receiver,
        requested_claim_ref,
        session_or_transcript_claim_refs=session_or_transcript_claim_refs,
    )
    if not decision.positive_semantics:
        state = _map_nonpositive_receiver(decision.receiver_state)
        return _zero_outcome(
            state,
            decision.receiver_state,
            reason=decision.receiver_state.value,
            audit_fingerprint=audit_fp,
        )

    projection = project_actor_safe_entry(
        decision,
        source_scope_ceiling=source_scope_ceiling,
        requested_claim_ref=requested_claim_ref,
        requested_first_person_permission=requested_first_person_permission,
        requested_component_refs=requested_component_refs,
        requested_actor_perceived_view_refs=requested_actor_perceived_view_refs,
        requested_temporal_scope_refs=requested_temporal_scope_refs,
        requested_subject_scope_refs=requested_subject_scope_refs,
        requested_referent_scope_refs=requested_referent_scope_refs,
    )

    requested_blocked = tuple(sorted({_text(item, "requested_spdm_class") for item in requested_spdm_classes} & BLOCKED_SPDM_CLASSES))
    if requested_blocked:
        return _zero_outcome(
            RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED,
            decision.receiver_state,
            reason=f"{BLOCKED_NAMED_AUTHORITY_REQUIRED}: {','.join(requested_blocked)}",
            audit_fingerprint=audit_fp,
            projection_fingerprint=projection.semantic_fingerprint,
        )

    if admitted_plan is None or accepted_plan_authority is None:
        return _zero_outcome(
            RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED,
            decision.receiver_state,
            reason=f"{BLOCKED_NAMED_AUTHORITY_REQUIRED}: FINAL_ADMITTED_V2_SEMANTIC_PLAN",
            audit_fingerprint=audit_fp,
            projection_fingerprint=projection.semantic_fingerprint,
        )
    if execution is None:
        return _zero_outcome(
            RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED,
            decision.receiver_state,
            reason=f"{BLOCKED_NAMED_AUTHORITY_REQUIRED}: GOVERNED_RENDER_EXECUTION_BINDING",
            audit_fingerprint=audit_fp,
            projection_fingerprint=projection.semantic_fingerprint,
        )

    _validate_plan(admitted_plan, projection, accepted_plan_authority)
    model_input = RenderModelInput(
        admitted_plan.plan_id,
        admitted_plan.plan_hash,
        projection.semantic_fingerprint,
        admitted_plan.wording_variants,
        execution.binding_hash,
    )

    model_called = renderer is not None
    if renderer is not None:
        candidate = renderer(model_input)
    else:
        if selected_variant_id is None:
            return _zero_outcome(
                RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED,
                decision.receiver_state,
                reason=f"{BLOCKED_NAMED_AUTHORITY_REQUIRED}: WORDING_VARIABILITY_INPUT",
                audit_fingerprint=audit_fp,
                projection_fingerprint=projection.semantic_fingerprint,
            )
        variants = {item.variant_id: item for item in admitted_plan.wording_variants}
        variant_id = _text(selected_variant_id, "selected_variant_id")
        if variant_id not in variants:
            raise RenderSemanticConformanceError("selected wording variant is not admitted by the semantic plan")
        candidate = _candidate_from_variant(admitted_plan, variants[variant_id])

    variant = validate_renderer_candidate(candidate, admitted_plan, projection)
    artifact = _artifact(candidate, variant, admitted_plan, projection, execution)
    return RenderOutcome(
        RenderState.ACCEPTED_BOUNDED_RENDER,
        decision.receiver_state,
        model_called,
        True,
        projection.semantic_fingerprint,
        artifact,
        None,
        audit_fp,
    )
