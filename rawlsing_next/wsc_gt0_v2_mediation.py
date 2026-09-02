#!/usr/bin/env python3
"""GT0 V3 -> V2 blocked-expression mediation glue.

This module is intentionally non-authoritative. It composes the already-current
M6 actor-safe ingress and bounded renderer for Golden Thread 0 without widening
either surface.

The GT0 baseline provides no positive V2 semantic-plan authority and no governed
render-execution binding. Therefore this module can only produce a typed
nonrenderable/blocked/valid-empty outcome and MUST NOT call a model, produce
semantic output, or mutate V3 state.

The shared WSC002 protocol module is implemented independently by WSC002A. This
lane resolves it lazily so the worker branch remains sibling-blind; central
integration can bind the concrete GT0StageReceipt constructor mechanically.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib
import inspect
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.m6_actor_safe_expression import (
    ActorAccessibleRenderEnvelope,
    ActorSafeRef,
    ReceiverSnapshot,
    ReplayClosure,
    ScopeCeiling,
    canonical_json,
)
from rawlsing_next.render_bounded_expression import (
    BLOCKED_NAMED_AUTHORITY_REQUIRED,
    IG_RENDER_CONTRACT_ID,
    RenderState,
    realize_bounded_expression,
)

GT0_V3_V2_STAGE_ID = "GT0_V3_TO_V2_BLOCKED_EXPRESSION"
GT0_V3_V2_STAGE_VERSION = "1.0.0"
INFORMATION_LOSS = "NONE__REFERENCE_PRESERVING__NO_POSITIVE_SEMANTIC_OUTPUT"
PERMISSION_CEILING = "NARROW_ONLY__NO_CLAIM_OR_RENDER_AUTHORITY_WIDENING"

_REQUIRED_V3_FINGERPRINT_KEYS = (
    "actor_state_hash",
    "causal_ledger_hash",
    "causal_cursor",
    "rng_state_hash",
    "scheduler_state_hash",
)


class GT0V3V2IntegrityError(ValueError):
    """The GT0 mediation wrapper could not preserve an exact invariant."""


class GT0ProtocolCompatibilityError(RuntimeError):
    """The independently implemented WSC002 protocol surface needs integration."""


@dataclass(frozen=True)
class GT0V3V2MediationResult:
    """Nonsemantic integration result plus exact protocol/cross-spine references."""

    conservation_envelope: Any
    upstream_stage_receipt: Any
    stage_receipt: Any
    protocol_status_name: str
    receiver_state: str | None
    render_state: str
    block_reason: str | None
    model_called: bool
    semantic_output: bool
    rendered_artifact: Any | None
    exact_upstream_refs: tuple[str, ...]
    v3_runtime_fingerprint_before: tuple[tuple[str, str], ...]
    v3_runtime_fingerprint_after: tuple[tuple[str, str], ...]
    audit_hash: str

    @property
    def v3_unchanged(self) -> bool:
        return self.v3_runtime_fingerprint_before == self.v3_runtime_fingerprint_after


def _exact_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GT0V3V2IntegrityError(f"{name} must be a non-empty exact string")
    out = value.strip()
    if out.lower() in {"latest", "default", "*"}:
        raise GT0V3V2IntegrityError(f"{name} may not use mutable/latest/default selection")
    return out


def _freeze_upstream_refs(values: Sequence[str]) -> tuple[str, ...]:
    refs = tuple(sorted({_exact_text(value, "exact_upstream_ref") for value in values}))
    if not refs:
        raise GT0V3V2IntegrityError("at least one exact upstream ref is required")
    return refs


def _freeze_v3_fingerprint(value: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, Mapping):
        raise GT0V3V2IntegrityError("v3_runtime_fingerprint must be a mapping")
    missing = [key for key in _REQUIRED_V3_FINGERPRINT_KEYS if key not in value]
    if missing:
        raise GT0V3V2IntegrityError(
            "v3_runtime_fingerprint missing required keys: " + ",".join(missing)
        )
    frozen = []
    for key in _REQUIRED_V3_FINGERPRINT_KEYS:
        raw = value[key]
        if raw is None:
            raise GT0V3V2IntegrityError(f"v3_runtime_fingerprint[{key}] may not be null")
        text = str(raw).strip()
        if not text:
            raise GT0V3V2IntegrityError(f"v3_runtime_fingerprint[{key}] may not be empty")
        if text.lower() in {"latest", "default", "*"}:
            raise GT0V3V2IntegrityError(
                f"v3_runtime_fingerprint[{key}] may not use mutable selection"
            )
        frozen.append((key, text))
    return tuple(frozen)


def _protocol_status_from_render_state(state: RenderState) -> str:
    if state is RenderState.BLOCKED_NAMED_AUTHORITY_REQUIRED:
        return "BLOCKED_NAMED_AUTHORITY_REQUIRED"
    if state is RenderState.VALID_EMPTY_NO_MODEL_CALL:
        return "VALID_EMPTY"
    if state is RenderState.BLOCKED_M6_DENY:
        return "DENIED"
    if state in {RenderState.BLOCKED_M6_DEFER, RenderState.BLOCKED_M6_ABSENT}:
        return "UNRESOLVED"
    if state in {RenderState.BLOCKED_M6_HANDOFF_INTEGRITY, RenderState.BLOCKED_M6_STALE}:
        return "INTEGRITY_FAILURE"
    if state is RenderState.ACCEPTED_BOUNDED_RENDER:
        raise GT0V3V2IntegrityError(
            "WSC002F baseline may not produce a positive bounded render"
        )
    raise GT0V3V2IntegrityError(f"unmapped render state: {state!r}")


def _resolve_protocol_status(protocol: Any, status_name: str) -> Any:
    enum_type = getattr(protocol, "GT0StageStatus", None)
    if enum_type is None:
        enum_type = getattr(protocol, "StageStatus", None)
    if enum_type is None:
        return status_name
    try:
        return enum_type(status_name)
    except Exception:
        try:
            return getattr(enum_type, status_name)
        except Exception as exc:
            raise GT0ProtocolCompatibilityError(
                f"shared protocol does not expose status {status_name}"
            ) from exc


def _call_compatible(factory: Callable[..., Any], material: Mapping[str, Any]) -> Any:
    """Call an independently defined protocol factory without guessing extra fields."""
    try:
        sig = inspect.signature(factory)
    except (TypeError, ValueError):
        return factory(**material)

    params = sig.parameters
    if len(params) == 1:
        only = next(iter(params.values()))
        if only.kind in {
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        } and only.name in {"material", "payload", "data"}:
            return factory(material)

    accepts_var_kwargs = any(
        param.kind is inspect.Parameter.VAR_KEYWORD for param in params.values()
    )
    kwargs = dict(material) if accepts_var_kwargs else {
        name: material[name] for name in params if name in material
    }
    required_missing = [
        name
        for name, param in params.items()
        if param.kind
        not in {inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD}
        and param.default is inspect._empty
        and name not in kwargs
    ]
    if required_missing:
        raise GT0ProtocolCompatibilityError(
            "shared GT0StageReceipt constructor has unresolved required fields: "
            + ",".join(required_missing)
        )
    return factory(**kwargs)


def _default_stage_receipt_factory(material: Mapping[str, Any]) -> Any:
    try:
        protocol = importlib.import_module("rawlsing_next.wsc_gt0_protocol")
    except ModuleNotFoundError as exc:
        raise GT0ProtocolCompatibilityError(
            "rawlsing_next.wsc_gt0_protocol is supplied by independent WSC002A "
            "and is intentionally absent on this sibling-blind worker branch"
        ) from exc

    status_name = str(material["status"])
    bound = dict(material)
    bound["status"] = _resolve_protocol_status(protocol, status_name)
    bound["stage_status"] = bound["status"]
    bound["typed_status"] = bound["status"]

    for factory_name in ("make_gt0_stage_receipt", "make_stage_receipt"):
        factory = getattr(protocol, factory_name, None)
        if callable(factory):
            return _call_compatible(factory, bound)

    receipt_type = getattr(protocol, "GT0StageReceipt", None)
    if receipt_type is None:
        raise GT0ProtocolCompatibilityError(
            "shared protocol exposes neither GT0StageReceipt nor a stage-receipt factory"
        )
    return _call_compatible(receipt_type, bound)


def _stage_receipt_material(
    *,
    status_name: str,
    upstream_refs: tuple[str, ...],
    actor_safe_envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
    requested_claim_ref: ActorSafeRef,
    render_state: RenderState,
    block_reason: str | None,
    audit_hash: str,
) -> dict[str, Any]:
    provenance_refs = (
        f"M6_ENVELOPE:{actor_safe_envelope.envelope_id}:{actor_safe_envelope.envelope_hash}",
        f"M6_REPLAY:{replay_closure.closure_id}:{replay_closure.closure_hash}",
        f"M6_REQUESTED_CLAIM:{requested_claim_ref.key}",
        f"RENDER_CONTRACT:{IG_RENDER_CONTRACT_ID}",
    )
    return {
        "stage_id": GT0_V3_V2_STAGE_ID,
        "stage_name": GT0_V3_V2_STAGE_ID,
        "stage_version": GT0_V3_V2_STAGE_VERSION,
        "status": status_name,
        "semantic_owner": "UPSTREAM_V3_ACTOR_SAFE_OWNER__NO_TRANSFER",
        "producer_owner": "UPSTREAM_V3_ACTOR_SAFE_OWNER__NO_TRANSFER",
        "consumer": "V2_BOUNDED_EXPRESSION",
        "consumer_permission": PERMISSION_CEILING,
        "permission": PERMISSION_CEILING,
        "typed_state": render_state.value,
        "upstream_refs": upstream_refs,
        "exact_upstream_refs": upstream_refs,
        "provenance_refs": provenance_refs,
        "dependency_refs": provenance_refs,
        "replay_refs": (f"M6_REPLAY:{replay_closure.closure_id}:{replay_closure.closure_hash}",),
        "information_loss": INFORMATION_LOSS,
        "information_loss_declaration": INFORMATION_LOSS,
        "target_use": "GT0_V3_TO_V2_MEDIATION_ONLY",
        "block_reason": block_reason,
        "content_hash": audit_hash,
        "receipt_hash": audit_hash,
        "actor_id": receiver.actor_id,
        "as_of_causal_time": receiver.causal_time,
    }


def run_gt0_v3_v2(
    conservation_envelope: Any,
    upstream_stage_receipt: Any,
    *,
    actor_safe_envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
    requested_claim_ref: ActorSafeRef,
    source_scope_ceiling: ScopeCeiling,
    requested_first_person_permission: str,
    v3_runtime_fingerprint: Mapping[str, Any],
    exact_upstream_refs: Sequence[str],
    requested_component_refs: Sequence[ActorSafeRef] = (),
    requested_actor_perceived_view_refs: Sequence[ActorSafeRef] = (),
    requested_temporal_scope_refs: Sequence[str] = (),
    requested_subject_scope_refs: Sequence[str] = (),
    requested_referent_scope_refs: Sequence[str] = (),
    stage_receipt_factory: Callable[[Mapping[str, Any]], Any] | None = None,
) -> GT0V3V2MediationResult:
    """Run the GT0 V3->V2 baseline without creating positive expression authority.

    The caller must provide an already-governed M6 actor-safe envelope/replay
    closure and exact V3 receiver snapshot. This function never constructs an
    ActorSafeClaimEntry from upstream GT0 evidence. It deliberately withholds
    admitted V2 semantic plan, plan authority, render execution binding, and
    model callback.
    """

    if conservation_envelope is None or upstream_stage_receipt is None:
        raise GT0V3V2IntegrityError(
            "explicit conservation envelope and upstream stage receipt are required"
        )
    if not isinstance(actor_safe_envelope, ActorAccessibleRenderEnvelope):
        raise GT0V3V2IntegrityError("actor_safe_envelope must be exact M6 runtime type")
    if not isinstance(replay_closure, ReplayClosure):
        raise GT0V3V2IntegrityError("replay_closure must be exact M6 runtime type")
    if not isinstance(receiver, ReceiverSnapshot):
        raise GT0V3V2IntegrityError("receiver must be exact M6 runtime type")
    if not isinstance(requested_claim_ref, ActorSafeRef):
        raise GT0V3V2IntegrityError("requested_claim_ref must be exact M6 ActorSafeRef")
    if not isinstance(source_scope_ceiling, ScopeCeiling):
        raise GT0V3V2IntegrityError("source_scope_ceiling must be exact M6 ScopeCeiling")

    upstream_refs = _freeze_upstream_refs(exact_upstream_refs)
    fingerprint_before = _freeze_v3_fingerprint(v3_runtime_fingerprint)

    outcome = realize_bounded_expression(
        envelope=actor_safe_envelope,
        replay_closure=replay_closure,
        receiver=receiver,
        requested_claim_ref=requested_claim_ref,
        source_scope_ceiling=source_scope_ceiling,
        requested_first_person_permission=_exact_text(
            requested_first_person_permission, "requested_first_person_permission"
        ),
        requested_component_refs=requested_component_refs,
        requested_actor_perceived_view_refs=requested_actor_perceived_view_refs,
        requested_temporal_scope_refs=requested_temporal_scope_refs,
        requested_subject_scope_refs=requested_subject_scope_refs,
        requested_referent_scope_refs=requested_referent_scope_refs,
        admitted_plan=None,
        accepted_plan_authority=None,
        execution=None,
        renderer=None,
    )

    if outcome.model_called or outcome.semantic_output or outcome.artifact is not None:
        raise GT0V3V2IntegrityError(
            "WSC002F baseline must not call a model or produce semantic/rendered output"
        )

    status_name = _protocol_status_from_render_state(outcome.state)
    fingerprint_after = _freeze_v3_fingerprint(v3_runtime_fingerprint)
    if fingerprint_before != fingerprint_after:
        raise GT0V3V2IntegrityError("V3 runtime fingerprint changed during V2 mediation")

    audit_material = {
        "stage_id": GT0_V3_V2_STAGE_ID,
        "stage_version": GT0_V3_V2_STAGE_VERSION,
        "upstream_refs": upstream_refs,
        "m6_envelope_id": actor_safe_envelope.envelope_id,
        "m6_envelope_hash": actor_safe_envelope.envelope_hash,
        "m6_replay_closure_id": replay_closure.closure_id,
        "m6_replay_closure_hash": replay_closure.closure_hash,
        "receiver_actor_id": receiver.actor_id,
        "receiver_causal_time": receiver.causal_time,
        "requested_claim_ref": requested_claim_ref.as_dict(),
        "requested_first_person_permission": requested_first_person_permission,
        "render_contract_id": IG_RENDER_CONTRACT_ID,
        "render_state": outcome.state.value,
        "receiver_state": outcome.receiver_state.value if outcome.receiver_state else None,
        "block_reason": outcome.block_reason,
        "model_called": outcome.model_called,
        "semantic_output": outcome.semantic_output,
        "artifact": None,
        "v3_runtime_fingerprint_before": fingerprint_before,
        "v3_runtime_fingerprint_after": fingerprint_after,
        "information_loss": INFORMATION_LOSS,
        "permission_ceiling": PERMISSION_CEILING,
    }
    audit_hash = hashlib.sha256(
        canonical_json(audit_material).encode("utf-8")
    ).hexdigest()

    material = _stage_receipt_material(
        status_name=status_name,
        upstream_refs=upstream_refs,
        actor_safe_envelope=actor_safe_envelope,
        replay_closure=replay_closure,
        receiver=receiver,
        requested_claim_ref=requested_claim_ref,
        render_state=outcome.state,
        block_reason=outcome.block_reason,
        audit_hash=audit_hash,
    )
    factory = stage_receipt_factory or _default_stage_receipt_factory
    stage_receipt = factory(material)

    return GT0V3V2MediationResult(
        conservation_envelope=conservation_envelope,
        upstream_stage_receipt=upstream_stage_receipt,
        stage_receipt=stage_receipt,
        protocol_status_name=status_name,
        receiver_state=outcome.receiver_state.value if outcome.receiver_state else None,
        render_state=outcome.state.value,
        block_reason=outcome.block_reason,
        model_called=outcome.model_called,
        semantic_output=outcome.semantic_output,
        rendered_artifact=outcome.artifact,
        exact_upstream_refs=upstream_refs,
        v3_runtime_fingerprint_before=fingerprint_before,
        v3_runtime_fingerprint_after=fingerprint_after,
        audit_hash=audit_hash,
    )
