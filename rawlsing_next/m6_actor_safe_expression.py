#!/usr/bin/env python3
"""Clean-sideline runtime for the frozen M6 actor-safe expression seam.

This module implements only the actor-accessible semantic ceiling and V2 ingress
firewall accepted at M6. It deliberately does not implement situated
phenomenology, disclosure planning, salience, inhibition, affective
foregrounding, interlocutor-specific openness, psychological register
selection, utterance planning, or rendering.

Positive semantic ingress is exactly a current verified ActorSafeClaimEntry
inside a current verified ActorAccessibleRenderEnvelope. Upstream structural
and empirical priors, including accepted M5 runtime evidence, are never positive
expression authority.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import json
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.m5_runtime_rsc_peer_prior import (
    RSCValidationReceipt,
    ResolvedStructuralContext,
    StructuralCurrentnessReceipt,
    StructuralPeerUseReceipt,
)


M6_CONTRACT_ID = "M6_V3_TO_V2_ACTOR_SAFE_EXPRESSION_SEAM@1.0.0"
AARE_TYPE = "ActorAccessibleRenderEnvelope@1.0.0"
ENTRY_TYPE = "ActorSafeClaimEntry@1.0.0"
DECISION_TYPE = "ActorSafeNonrenderableDecisionRef@1.0.0"
OPAQUE_AUDIT_TYPE = "OpaqueAuditRef@1.0.0"
REPLAY_CLOSURE_SCHEMA = "SCRV3_M6_AARE_REPLAY_CLOSURE@1.0.0"
CURRENTNESS_PREDICATE = "SCRV3_M6_AARE_CURRENTNESS_V1"
CANONICAL_PROFILE = "SCRV3_M6_CANONICAL_JSON_V1"

ADP017_VERSION = "1.0.0"
ADP017_HASH = "git-blob-sha1:eece4f3f2f3f9288ab9bbc645dc81e20a99e1280"

BLOCKED_NAMED_AUTHORITY_REQUIRED = "BLOCKED_NAMED_AUTHORITY_REQUIRED"
NO_DIRECT_M5_TO_M6_EDGE = "NO_DIRECT_POSITIVE_M5_TO_M6_SEMANTIC_EDGE"

ENTRY_DOMAIN = bytes.fromhex(
    "5241574c53494e470053435256335f4d36004163746f7253616665436c61696d456e74727900312e302e3000"
)
ENVELOPE_DOMAIN = bytes.fromhex(
    "5241574c53494e470053435256335f4d36004163746f7241636365737369626c6552656e646572456e76656c6f706500312e302e3000"
)
DECISION_DOMAIN = bytes.fromhex(
    "5241574c53494e470053435256335f4d36004163746f72536166654e6f6e72656e64657261626c654465636973696f6e52656600312e302e3000"
)
REPLAY_DOMAIN = bytes.fromhex(
    "5241574c53494e470053435256335f4d3600414152455f5245504c41595f434c4f5355524500312e302e3000"
)

POSITIVE_PERMISSIONS = frozenset({
    "PERMIT_FIRST_PERSON_KNOWLEDGE",
    "PERMIT_FIRST_PERSON_BELIEF",
    "PERMIT_FIRST_PERSON_UNCERTAINTY",
    "PERMIT_FIRST_PERSON_NONKNOWLEDGE",
})
CONTROL_PERMISSIONS = frozenset({"DENY_FIRST_PERSON_CLAIM", "DEFER_MISSING_AUTHORITY"})
ACCESSIBILITY_STATES = frozenset({
    "CLAIM_ACCESSIBLE",
    "CLAIM_PARTIALLY_ACCESSIBLE",
    "CLAIM_INACCESSIBLE",
    "CLAIM_ACCESS_UNKNOWN",
})

FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES = frozenset({
    "PSEPF",
    "ActorComparatorReceipt",
    "SourceDisagreementOrEmpiricalNegativeAsSuch",
    "V3EmpiricalPossibilityInput",
    "ResolvedStructuralContext",
    "StructuralPriorRepository",
    "V557_V558_OBJECT_LOCATOR_INDEX_SELECTION_RECORD",
    "RAW_V553_V554_V555_V556_STRUCTURAL_OBJECT",
    "ReplayReceipt",
    "OPAQUE_UPSTREAM_AUDIT_OR_PROVENANCE",
    "ANALYST_ONLY_TRUTH",
    "RSCValidationReceipt",
    "StructuralCurrentnessReceipt",
    "StructuralPeerUseReceipt",
})


class M6IntegrityError(ValueError):
    """Fail-closed identity/currentness/replay error."""


class M6SemanticWideningError(ValueError):
    """Downstream projection exceeded the actor-safe allowlist."""


class M6ForbiddenBehavioralSource(ValueError):
    """Upstream/audit/M5 material was offered as behavioral authority."""


class M6NamedAuthorityRequired(ValueError):
    """M6 does not own situated phenomenology/expression psychology."""


class CurrentnessState(str, Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


class ReceiverState(str, Enum):
    BLOCKED_HANDOFF_INTEGRITY_FAILURE = "BLOCKED_HANDOFF_INTEGRITY_FAILURE"
    BLOCKED_STALE_ACTOR_SAFE_HANDOFF = "BLOCKED_STALE_ACTOR_SAFE_HANDOFF"
    DEFERRED_MISSING_AUTHORITY = "DEFERRED_MISSING_AUTHORITY"
    DENIED_EXPLICIT_FIRST_PERSON_CLAIM = "DENIED_EXPLICIT_FIRST_PERSON_CLAIM"
    READY_PARTIAL_COMPONENT_SCOPE = "READY_PARTIAL_COMPONENT_SCOPE"
    READY_FULL_CLAIM_SCOPE = "READY_FULL_CLAIM_SCOPE"
    NO_RENDERABLE_ENTRY_FOR_REQUEST = "NO_RENDERABLE_ENTRY_FOR_REQUEST"
    VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS = "VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS"


class ExternalEventDecision(str, Enum):
    ADMIT = "ADMIT"
    REJECT = "REJECT"
    DEFER = "DEFER"
    INVALID = "INVALID"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise M6IntegrityError(f"{name} must be a non-empty string")
    out = unicodedata.normalize("NFC", value.strip())
    if out.lower() in {"latest", "default", "*"}:
        raise M6IntegrityError(f"{name} may not use mutable/latest/default selection")
    return out


def _hash_text(value: Any, name: str) -> str:
    out = _text(value, name)
    if len(out) < 8:
        raise M6IntegrityError(f"{name} is not an exact immutable hash/binding")
    return out


def _normalize_json(value: Any) -> Any:
    if isinstance(value, Enum):
        return _normalize_json(value.value)
    if isinstance(value, ActorSafeRef):
        return _normalize_json(value.as_dict())
    if isinstance(value, OpaqueAuditRef):
        return _normalize_json(value.as_dict())
    if isinstance(value, ActorSafeClaimEntry):
        return _normalize_json(value.as_dict())
    if isinstance(value, ActorSafeNonrenderableDecisionRef):
        return _normalize_json(value.as_dict())
    if isinstance(value, Mapping):
        return {
            unicodedata.normalize("NFC", str(key)): _normalize_json(item)
            for key, item in value.items()
        }
    if isinstance(value, (tuple, list)):
        return [_normalize_json(item) for item in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if value is None or isinstance(value, (bool, int)):
        return value
    if isinstance(value, float):
        raise M6IntegrityError("floating-point seam-native identity material is forbidden")
    raise M6IntegrityError(f"unsupported canonical identity material: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    """Frozen SCRV3→M6 canonical JSON profile."""
    return json.dumps(
        _normalize_json(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def _domain_hash(domain: bytes, material: Mapping[str, Any]) -> str:
    return hashlib.sha256(domain + canonical_json(material).encode("utf-8")).hexdigest()


@dataclass(frozen=True, order=True)
class ActorSafeRef:
    kind: str
    object_id: str
    content_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "kind", _text(self.kind, "ref.kind"))
        object.__setattr__(self, "object_id", _text(self.object_id, "ref.object_id"))
        object.__setattr__(self, "content_hash", _hash_text(self.content_hash, "ref.content_hash"))

    def as_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "object_id": self.object_id, "content_hash": self.content_hash}

    @property
    def key(self) -> str:
        return f"{self.kind}|{self.object_id}|{self.content_hash}"


def _ref(value: ActorSafeRef | Mapping[str, str], name: str) -> ActorSafeRef:
    if isinstance(value, ActorSafeRef):
        return value
    if not isinstance(value, Mapping):
        raise M6IntegrityError(f"{name} must be an exact ref")
    try:
        return ActorSafeRef(str(value["kind"]), str(value["object_id"]), str(value["content_hash"]))
    except KeyError as exc:
        raise M6IntegrityError(f"{name} missing {exc.args[0]}") from exc


def _refs(values: Iterable[ActorSafeRef | Mapping[str, str]], name: str) -> tuple[ActorSafeRef, ...]:
    result = tuple(_ref(value, name) for value in values)
    return tuple(sorted(result, key=lambda item: (item.kind, item.object_id, item.content_hash)))


@dataclass(frozen=True)
class OpaqueAuditRef:
    role: str
    audit_role: str
    opaque_ref_id: str
    opaque_ref_hash: str

    def __post_init__(self) -> None:
        if self.role != "AUDIT_ONLY_REF":
            raise M6IntegrityError("opaque provenance role must be AUDIT_ONLY_REF")
        object.__setattr__(self, "audit_role", _text(self.audit_role, "opaque.audit_role"))
        object.__setattr__(self, "opaque_ref_id", _text(self.opaque_ref_id, "opaque.opaque_ref_id"))
        object.__setattr__(self, "opaque_ref_hash", _hash_text(self.opaque_ref_hash, "opaque.opaque_ref_hash"))

    def as_dict(self) -> dict[str, str]:
        return {
            "role": self.role,
            "audit_role": self.audit_role,
            "opaque_ref_id": self.opaque_ref_id,
            "opaque_ref_hash": self.opaque_ref_hash,
        }


@dataclass(frozen=True)
class ActorSafeClaimEntry:
    claim_ref: ActorSafeRef
    stance_record_ref: ActorSafeRef
    accessibility_state: str
    permitted_component_refs: tuple[ActorSafeRef, ...]
    first_person_permission: str
    memory_refs: tuple[ActorSafeRef, ...]
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    source_transition_refs: tuple[ActorSafeRef, ...]
    entry_hash: str

    def as_core(self) -> dict[str, Any]:
        return {
            "claim_ref": self.claim_ref.as_dict(),
            "stance_record_ref": self.stance_record_ref.as_dict(),
            "accessibility_state": self.accessibility_state,
            "permitted_component_refs": [item.as_dict() for item in self.permitted_component_refs],
            "first_person_permission": self.first_person_permission,
            "memory_refs": [item.as_dict() for item in self.memory_refs],
            "actor_perceived_view_refs": [item.as_dict() for item in self.actor_perceived_view_refs],
            "source_transition_refs": [item.as_dict() for item in self.source_transition_refs],
        }

    def as_dict(self) -> dict[str, Any]:
        return {**self.as_core(), "entry_hash": self.entry_hash}


def make_actor_safe_claim_entry(
    *,
    claim_ref: ActorSafeRef | Mapping[str, str],
    stance_record_ref: ActorSafeRef | Mapping[str, str],
    accessibility_state: str,
    permitted_component_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    first_person_permission: str,
    memory_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    actor_perceived_view_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    source_transition_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
) -> ActorSafeClaimEntry:
    access = _text(accessibility_state, "accessibility_state")
    permission = _text(first_person_permission, "first_person_permission")
    if access not in {"CLAIM_ACCESSIBLE", "CLAIM_PARTIALLY_ACCESSIBLE"}:
        raise M6IntegrityError("positive entry accessibility must be ACCESSIBLE or PARTIALLY_ACCESSIBLE")
    if permission not in POSITIVE_PERMISSIONS:
        raise M6IntegrityError("positive entry must use an exact positive ADP-017 permission class")
    components = _refs(permitted_component_refs, "permitted_component_ref")
    if access == "CLAIM_ACCESSIBLE" and components:
        raise M6IntegrityError("full-access entry must carry no permitted_component_refs")
    if access == "CLAIM_PARTIALLY_ACCESSIBLE" and not components:
        raise M6IntegrityError("partial-access entry requires exact permitted_component_refs")
    entry = ActorSafeClaimEntry(
        _ref(claim_ref, "claim_ref"),
        _ref(stance_record_ref, "stance_record_ref"),
        access,
        components,
        permission,
        _refs(memory_refs, "memory_ref"),
        _refs(actor_perceived_view_refs, "actor_perceived_view_ref"),
        _refs(source_transition_refs, "source_transition_ref"),
        "",
    )
    return replace(entry, entry_hash=_domain_hash(ENTRY_DOMAIN, entry.as_core()))


@dataclass(frozen=True)
class ActorSafeNonrenderableDecisionRef:
    claim_ref: ActorSafeRef
    permission_record_ref: ActorSafeRef
    accessibility_state: str
    first_person_permission: str
    decision_ref_hash: str

    def as_core(self) -> dict[str, Any]:
        return {
            "claim_ref": self.claim_ref.as_dict(),
            "permission_record_ref": self.permission_record_ref.as_dict(),
            "accessibility_state": self.accessibility_state,
            "first_person_permission": self.first_person_permission,
        }

    def as_dict(self) -> dict[str, Any]:
        return {**self.as_core(), "decision_ref_hash": self.decision_ref_hash}


def make_nonrenderable_decision(
    *,
    claim_ref: ActorSafeRef | Mapping[str, str],
    permission_record_ref: ActorSafeRef | Mapping[str, str],
    accessibility_state: str,
    first_person_permission: str,
) -> ActorSafeNonrenderableDecisionRef:
    access = _text(accessibility_state, "accessibility_state")
    permission = _text(first_person_permission, "first_person_permission")
    if access not in ACCESSIBILITY_STATES:
        raise M6IntegrityError("unknown accessibility state")
    lawful = (
        (access == "CLAIM_INACCESSIBLE" and permission == "DENY_FIRST_PERSON_CLAIM")
        or (access == "CLAIM_ACCESS_UNKNOWN" and permission == "DEFER_MISSING_AUTHORITY")
        or permission == "DENY_FIRST_PERSON_CLAIM"
    )
    if not lawful:
        raise M6IntegrityError("deny/defer control state is not a frozen ADP-017 mapping")
    decision = ActorSafeNonrenderableDecisionRef(
        _ref(claim_ref, "claim_ref"),
        _ref(permission_record_ref, "permission_record_ref"),
        access,
        permission,
        "",
    )
    return replace(decision, decision_ref_hash=_domain_hash(DECISION_DOMAIN, decision.as_core()))


@dataclass(frozen=True)
class ReplayClosure:
    closure_id: str
    closure_hash: str
    actor_id: str
    as_of_causal_time: int
    source_generated_person_record_hash: str
    source_actor_state_hash: str
    source_memory_state_hash: str
    source_epistemic_state_hash: str
    adp017_authority_version: str
    adp017_authority_hash: str
    canonicalization_profile_id: str
    causal_event_or_generated_fact_state_refs: tuple[ActorSafeRef, ...]
    adp016_memory_object_and_transition_refs: tuple[ActorSafeRef, ...]
    canonical_claim_refs: tuple[ActorSafeRef, ...]
    epistemic_effect_and_transition_refs: tuple[ActorSafeRef, ...]
    permission_record_refs: tuple[ActorSafeRef, ...]
    owning_rule_refs: tuple[ActorSafeRef, ...]
    actor_state_checkpoint_refs: tuple[ActorSafeRef, ...]
    exact_causal_parent_sequence_ref_hash: str
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    entry_hashes: tuple[str, ...]
    decision_ref_hashes: tuple[str, ...]

    def as_core(self) -> dict[str, Any]:
        return {
            "actor_id": self.actor_id,
            "as_of_causal_time": self.as_of_causal_time,
            "source_generated_person_record_hash": self.source_generated_person_record_hash,
            "source_actor_state_hash": self.source_actor_state_hash,
            "source_memory_state_hash": self.source_memory_state_hash,
            "source_epistemic_state_hash": self.source_epistemic_state_hash,
            "adp017_authority_version": self.adp017_authority_version,
            "adp017_authority_hash": self.adp017_authority_hash,
            "canonicalization_profile_id": self.canonicalization_profile_id,
            "causal_event_or_generated_fact_state_refs": [item.as_dict() for item in self.causal_event_or_generated_fact_state_refs],
            "adp016_memory_object_and_transition_refs": [item.as_dict() for item in self.adp016_memory_object_and_transition_refs],
            "canonical_claim_refs": [item.as_dict() for item in self.canonical_claim_refs],
            "epistemic_effect_and_transition_refs": [item.as_dict() for item in self.epistemic_effect_and_transition_refs],
            "permission_record_refs": [item.as_dict() for item in self.permission_record_refs],
            "owning_rule_refs": [item.as_dict() for item in self.owning_rule_refs],
            "actor_state_checkpoint_refs": [item.as_dict() for item in self.actor_state_checkpoint_refs],
            "exact_causal_parent_sequence_ref_hash": self.exact_causal_parent_sequence_ref_hash,
            "actor_perceived_view_refs": [item.as_dict() for item in self.actor_perceived_view_refs],
            "entry_hashes": list(self.entry_hashes),
            "decision_ref_hashes": list(self.decision_ref_hashes),
        }


def make_replay_closure(
    *,
    actor_id: str,
    as_of_causal_time: int,
    source_generated_person_record_hash: str,
    source_actor_state_hash: str,
    source_memory_state_hash: str,
    source_epistemic_state_hash: str,
    exact_causal_parent_sequence_ref_hash: str,
    causal_event_or_generated_fact_state_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    adp016_memory_object_and_transition_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    canonical_claim_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    epistemic_effect_and_transition_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    permission_record_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    owning_rule_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    actor_state_checkpoint_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    actor_perceived_view_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    entry_hashes: Sequence[str] = (),
    decision_ref_hashes: Sequence[str] = (),
) -> ReplayClosure:
    if not isinstance(as_of_causal_time, int) or isinstance(as_of_causal_time, bool) or as_of_causal_time < 0:
        raise M6IntegrityError("as_of_causal_time must be a non-negative causal integer")
    closure = ReplayClosure(
        "",
        "",
        _text(actor_id, "actor_id"),
        as_of_causal_time,
        _hash_text(source_generated_person_record_hash, "source_generated_person_record_hash"),
        _hash_text(source_actor_state_hash, "source_actor_state_hash"),
        _hash_text(source_memory_state_hash, "source_memory_state_hash"),
        _hash_text(source_epistemic_state_hash, "source_epistemic_state_hash"),
        ADP017_VERSION,
        ADP017_HASH,
        CANONICAL_PROFILE,
        _refs(causal_event_or_generated_fact_state_refs, "causal_event_ref"),
        _refs(adp016_memory_object_and_transition_refs, "memory_transition_ref"),
        _refs(canonical_claim_refs, "canonical_claim_ref"),
        _refs(epistemic_effect_and_transition_refs, "epistemic_transition_ref"),
        _refs(permission_record_refs, "permission_record_ref"),
        _refs(owning_rule_refs, "owning_rule_ref"),
        _refs(actor_state_checkpoint_refs, "actor_state_checkpoint_ref"),
        _hash_text(exact_causal_parent_sequence_ref_hash, "exact_causal_parent_sequence_ref_hash"),
        _refs(actor_perceived_view_refs, "actor_perceived_view_ref"),
        tuple(sorted(_hash_text(value, "entry_hash") for value in entry_hashes)),
        tuple(sorted(_hash_text(value, "decision_ref_hash") for value in decision_ref_hashes)),
    )
    h = _domain_hash(REPLAY_DOMAIN, closure.as_core())
    return replace(closure, closure_id=f"AARE-RC:{h}", closure_hash=h)


@dataclass(frozen=True)
class ActorAccessibleRenderEnvelope:
    envelope_id: str
    envelope_schema_version: str
    actor_id: str
    as_of_causal_time: int
    source_generated_person_record_hash: str
    source_actor_state_hash: str
    source_memory_state_hash: str
    source_epistemic_state_hash: str
    adp017_authority_version: str
    adp017_authority_hash: str
    allowed_claim_entries: tuple[ActorSafeClaimEntry, ...]
    explicit_denial_refs: tuple[ActorSafeNonrenderableDecisionRef, ...]
    opaque_provenance_refs: tuple[OpaqueAuditRef, ...]
    envelope_hash: str
    integrity_state: str

    def as_core(self) -> dict[str, Any]:
        return {
            "envelope_schema_version": self.envelope_schema_version,
            "actor_id": self.actor_id,
            "as_of_causal_time": self.as_of_causal_time,
            "source_generated_person_record_hash": self.source_generated_person_record_hash,
            "source_actor_state_hash": self.source_actor_state_hash,
            "source_memory_state_hash": self.source_memory_state_hash,
            "source_epistemic_state_hash": self.source_epistemic_state_hash,
            "adp017_authority_version": self.adp017_authority_version,
            "adp017_authority_hash": self.adp017_authority_hash,
            "allowed_claim_entries": [entry.as_dict() for entry in self.allowed_claim_entries],
            "explicit_denial_refs": [decision.as_dict() for decision in self.explicit_denial_refs],
            "opaque_provenance_refs": [item.as_dict() for item in self.opaque_provenance_refs],
            "integrity_state": self.integrity_state,
        }


def make_actor_accessible_render_envelope(
    *,
    actor_id: str,
    as_of_causal_time: int,
    source_generated_person_record_hash: str,
    source_actor_state_hash: str,
    source_memory_state_hash: str,
    source_epistemic_state_hash: str,
    replay_closure: ReplayClosure,
    allowed_claim_entries: Sequence[ActorSafeClaimEntry] = (),
    explicit_denial_refs: Sequence[ActorSafeNonrenderableDecisionRef] = (),
    other_opaque_provenance_refs: Sequence[OpaqueAuditRef] = (),
    integrity_state: str = "VERIFIED",
) -> ActorAccessibleRenderEnvelope:
    if integrity_state not in {"VERIFIED", "INTEGRITY_FAILURE"}:
        raise M6IntegrityError("integrity_state must be VERIFIED or INTEGRITY_FAILURE")
    if not isinstance(replay_closure, ReplayClosure):
        raise M6IntegrityError("envelope requires exact replay closure")
    if replay_closure.actor_id != actor_id or replay_closure.as_of_causal_time != as_of_causal_time:
        raise M6IntegrityError("replay closure actor/time does not bind envelope")
    expected_source = (
        replay_closure.source_generated_person_record_hash,
        replay_closure.source_actor_state_hash,
        replay_closure.source_memory_state_hash,
        replay_closure.source_epistemic_state_hash,
    )
    actual_source = (
        source_generated_person_record_hash,
        source_actor_state_hash,
        source_memory_state_hash,
        source_epistemic_state_hash,
    )
    if expected_source != actual_source:
        raise M6IntegrityError("replay closure source snapshot does not bind envelope")
    entries = tuple(sorted(allowed_claim_entries, key=lambda item: item.entry_hash))
    decisions = tuple(sorted(explicit_denial_refs, key=lambda item: item.decision_ref_hash))
    if tuple(sorted(entry.entry_hash for entry in entries)) != replay_closure.entry_hashes:
        raise M6IntegrityError("replay closure entry hashes do not match envelope entries")
    if tuple(sorted(item.decision_ref_hash for item in decisions)) != replay_closure.decision_ref_hashes:
        raise M6IntegrityError("replay closure decision hashes do not match envelope decisions")
    replay_root = OpaqueAuditRef(
        "AUDIT_ONLY_REF",
        "ENVELOPE_REPLAY_CLOSURE_ROOT",
        replay_closure.closure_id,
        replay_closure.closure_hash,
    )
    other = tuple(other_opaque_provenance_refs)
    if any(item.audit_role == "ENVELOPE_REPLAY_CLOSURE_ROOT" for item in other):
        raise M6IntegrityError("exactly one envelope replay closure root is permitted")
    opaque = tuple(sorted((replay_root, *other), key=lambda item: item.opaque_ref_hash))
    envelope = ActorAccessibleRenderEnvelope(
        "",
        "1.0.0",
        _text(actor_id, "actor_id"),
        as_of_causal_time,
        _hash_text(source_generated_person_record_hash, "source_generated_person_record_hash"),
        _hash_text(source_actor_state_hash, "source_actor_state_hash"),
        _hash_text(source_memory_state_hash, "source_memory_state_hash"),
        _hash_text(source_epistemic_state_hash, "source_epistemic_state_hash"),
        ADP017_VERSION,
        ADP017_HASH,
        entries,
        decisions,
        opaque,
        "",
        integrity_state,
    )
    h = _domain_hash(ENVELOPE_DOMAIN, envelope.as_core())
    return replace(envelope, envelope_id=f"AARE:{h}", envelope_hash=h)


@dataclass(frozen=True)
class ReceiverSnapshot:
    actor_id: str
    causal_time: int
    source_generated_person_record_hash: str
    source_actor_state_hash: str
    source_memory_state_hash: str
    source_epistemic_state_hash: str
    adp017_authority_version: str = ADP017_VERSION
    adp017_authority_hash: str = ADP017_HASH
    ref_actor_bindings: Mapping[str, str] | None = None


def _verify_entry(entry: ActorSafeClaimEntry, actor_id: str, bindings: Mapping[str, str]) -> None:
    if not isinstance(entry, ActorSafeClaimEntry):
        raise M6IntegrityError("allowed_claim_entries contains wrong runtime type")
    if entry.accessibility_state not in {"CLAIM_ACCESSIBLE", "CLAIM_PARTIALLY_ACCESSIBLE"}:
        raise M6IntegrityError("positive entry has non-positive accessibility state")
    if entry.first_person_permission not in POSITIVE_PERMISSIONS:
        raise M6IntegrityError("positive entry has non-positive permission")
    if entry.accessibility_state == "CLAIM_ACCESSIBLE" and entry.permitted_component_refs:
        raise M6IntegrityError("full entry illegally carries partial component refs")
    if entry.accessibility_state == "CLAIM_PARTIALLY_ACCESSIBLE" and not entry.permitted_component_refs:
        raise M6IntegrityError("partial entry lacks exact permitted component refs")
    if entry.entry_hash != _domain_hash(ENTRY_DOMAIN, entry.as_core()):
        raise M6IntegrityError("entry hash mismatch")
    actor_bound_refs = (
        entry.stance_record_ref,
        *entry.memory_refs,
        *entry.actor_perceived_view_refs,
        *entry.source_transition_refs,
    )
    for ref in actor_bound_refs:
        if bindings.get(ref.key) != actor_id:
            raise M6IntegrityError(f"actor binding missing/mismatched for {ref.kind}")


def _verify_decision(decision: ActorSafeNonrenderableDecisionRef) -> None:
    if not isinstance(decision, ActorSafeNonrenderableDecisionRef):
        raise M6IntegrityError("explicit_denial_refs contains wrong runtime type")
    if decision.first_person_permission not in CONTROL_PERMISSIONS:
        raise M6IntegrityError("nonrenderable decision must be DENY or DEFER")
    if decision.decision_ref_hash != _domain_hash(DECISION_DOMAIN, decision.as_core()):
        raise M6IntegrityError("nonrenderable decision hash mismatch")


def _verify_replay_closure(closure: ReplayClosure, envelope: ActorAccessibleRenderEnvelope) -> None:
    if not isinstance(closure, ReplayClosure):
        raise M6IntegrityError("missing exact replay closure")
    if closure.closure_hash != _domain_hash(REPLAY_DOMAIN, closure.as_core()):
        raise M6IntegrityError("replay closure hash mismatch")
    if closure.closure_id != f"AARE-RC:{closure.closure_hash}":
        raise M6IntegrityError("replay closure identity mismatch")
    if (
        closure.actor_id != envelope.actor_id
        or closure.as_of_causal_time != envelope.as_of_causal_time
        or closure.source_generated_person_record_hash != envelope.source_generated_person_record_hash
        or closure.source_actor_state_hash != envelope.source_actor_state_hash
        or closure.source_memory_state_hash != envelope.source_memory_state_hash
        or closure.source_epistemic_state_hash != envelope.source_epistemic_state_hash
        or closure.adp017_authority_version != ADP017_VERSION
        or closure.adp017_authority_hash != ADP017_HASH
        or closure.canonicalization_profile_id != CANONICAL_PROFILE
    ):
        raise M6IntegrityError("replay closure does not bind exact envelope source/authority snapshot")
    if closure.entry_hashes != tuple(sorted(entry.entry_hash for entry in envelope.allowed_claim_entries)):
        raise M6IntegrityError("replay closure entry hash set mismatch")
    if closure.decision_ref_hashes != tuple(sorted(item.decision_ref_hash for item in envelope.explicit_denial_refs)):
        raise M6IntegrityError("replay closure decision hash set mismatch")
    roots = [item for item in envelope.opaque_provenance_refs if item.audit_role == "ENVELOPE_REPLAY_CLOSURE_ROOT"]
    if len(roots) != 1:
        raise M6IntegrityError("envelope must carry exactly one replay closure root")
    root = roots[0]
    if root.opaque_ref_id != closure.closure_id or root.opaque_ref_hash != closure.closure_hash:
        raise M6IntegrityError("opaque replay root does not bind exact replay closure")


def validate_envelope_integrity(
    envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
) -> None:
    """Validate exact identity, replay, actor/source and frozen ADP-017 bindings."""
    if not isinstance(envelope, ActorAccessibleRenderEnvelope):
        raise M6IntegrityError("wrong envelope runtime type")
    if envelope.envelope_schema_version != "1.0.0":
        raise M6IntegrityError("envelope schema version mismatch")
    if envelope.integrity_state != "VERIFIED":
        raise M6IntegrityError("envelope integrity_state is not VERIFIED")
    if envelope.envelope_hash != _domain_hash(ENVELOPE_DOMAIN, envelope.as_core()):
        raise M6IntegrityError("envelope hash mismatch")
    if envelope.envelope_id != f"AARE:{envelope.envelope_hash}":
        raise M6IntegrityError("envelope identity mismatch")
    if envelope.adp017_authority_version != ADP017_VERSION or envelope.adp017_authority_hash != ADP017_HASH:
        raise M6IntegrityError("envelope ADP-017 binding mismatch")
    if receiver.adp017_authority_version != ADP017_VERSION or receiver.adp017_authority_hash != ADP017_HASH:
        raise M6IntegrityError("receiver ADP-017 binding mismatch")
    if receiver.actor_id != envelope.actor_id:
        raise M6IntegrityError("receiver actor does not match envelope actor")
    if not isinstance(receiver.causal_time, int) or isinstance(receiver.causal_time, bool):
        raise M6IntegrityError("receiver causal time must be an exact integer")
    if receiver.causal_time < envelope.as_of_causal_time:
        raise M6IntegrityError("receiver causal time precedes envelope as_of_causal_time")
    bindings = dict(receiver.ref_actor_bindings or {})
    for entry in envelope.allowed_claim_entries:
        _verify_entry(entry, envelope.actor_id, bindings)
    for decision in envelope.explicit_denial_refs:
        _verify_decision(decision)
    _verify_replay_closure(replay_closure, envelope)


def evaluate_currentness(
    envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
) -> CurrentnessState:
    try:
        validate_envelope_integrity(envelope, replay_closure, receiver)
    except M6IntegrityError:
        return CurrentnessState.INTEGRITY_FAILURE
    current_hashes = (
        receiver.source_generated_person_record_hash,
        receiver.source_actor_state_hash,
        receiver.source_memory_state_hash,
        receiver.source_epistemic_state_hash,
    )
    bound_hashes = (
        envelope.source_generated_person_record_hash,
        envelope.source_actor_state_hash,
        envelope.source_memory_state_hash,
        envelope.source_epistemic_state_hash,
    )
    if current_hashes == bound_hashes:
        return CurrentnessState.CURRENT
    if receiver.causal_time > envelope.as_of_causal_time:
        return CurrentnessState.STALE
    return CurrentnessState.INTEGRITY_FAILURE


@dataclass(frozen=True)
class ActorSafeIngressDecision:
    receiver_state: ReceiverState
    claim_ref: ActorSafeRef | None
    component_refs: tuple[ActorSafeRef, ...]
    first_person_permission: str | None
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    entry_hash: str | None
    positive_semantics: bool

    @property
    def semantic_fingerprint(self) -> str:
        material = {
            "receiver_state": self.receiver_state.value,
            "claim_ref": self.claim_ref.as_dict() if self.claim_ref else None,
            "component_refs": [item.as_dict() for item in self.component_refs],
            "first_person_permission": self.first_person_permission,
            "actor_perceived_view_refs": [item.as_dict() for item in self.actor_perceived_view_refs],
            "entry_hash": self.entry_hash,
            "positive_semantics": self.positive_semantics,
        }
        return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def evaluate_actor_safe_ingress(
    envelope: ActorAccessibleRenderEnvelope,
    replay_closure: ReplayClosure,
    receiver: ReceiverSnapshot,
    requested_claim_ref: ActorSafeRef | Mapping[str, str],
    *,
    session_or_transcript_claim_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
) -> ActorSafeIngressDecision:
    """Implement the frozen terminal receiver order; session refs are inert."""
    requested = _ref(requested_claim_ref, "requested_claim_ref")
    tuple(_ref(item, "session_or_transcript_claim_ref") for item in session_or_transcript_claim_refs)
    currentness = evaluate_currentness(envelope, replay_closure, receiver)
    if currentness is CurrentnessState.INTEGRITY_FAILURE:
        return ActorSafeIngressDecision(ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE, None, (), None, (), None, False)
    if currentness is CurrentnessState.STALE:
        return ActorSafeIngressDecision(ReceiverState.BLOCKED_STALE_ACTOR_SAFE_HANDOFF, None, (), None, (), None, False)
    matching_decisions = [item for item in envelope.explicit_denial_refs if item.claim_ref == requested]
    if len({item.first_person_permission for item in matching_decisions}) > 1:
        return ActorSafeIngressDecision(ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE, None, (), None, (), None, False)
    if any(item.first_person_permission == "DEFER_MISSING_AUTHORITY" for item in matching_decisions):
        return ActorSafeIngressDecision(ReceiverState.DEFERRED_MISSING_AUTHORITY, None, (), None, (), None, False)
    if any(item.first_person_permission == "DENY_FIRST_PERSON_CLAIM" for item in matching_decisions):
        return ActorSafeIngressDecision(ReceiverState.DENIED_EXPLICIT_FIRST_PERSON_CLAIM, None, (), None, (), None, False)
    matching_entries = [item for item in envelope.allowed_claim_entries if item.claim_ref == requested]
    if len(matching_entries) > 1:
        return ActorSafeIngressDecision(ReceiverState.BLOCKED_HANDOFF_INTEGRITY_FAILURE, None, (), None, (), None, False)
    if matching_entries:
        entry = matching_entries[0]
        if entry.accessibility_state == "CLAIM_PARTIALLY_ACCESSIBLE":
            return ActorSafeIngressDecision(
                ReceiverState.READY_PARTIAL_COMPONENT_SCOPE,
                entry.claim_ref,
                entry.permitted_component_refs,
                entry.first_person_permission,
                entry.actor_perceived_view_refs,
                entry.entry_hash,
                True,
            )
        return ActorSafeIngressDecision(
            ReceiverState.READY_FULL_CLAIM_SCOPE,
            entry.claim_ref,
            (),
            entry.first_person_permission,
            entry.actor_perceived_view_refs,
            entry.entry_hash,
            True,
        )
    if not envelope.allowed_claim_entries:
        return ActorSafeIngressDecision(ReceiverState.VALID_EMPTY_NO_RENDERABLE_ACTOR_CLAIMS, None, (), None, (), None, False)
    return ActorSafeIngressDecision(ReceiverState.NO_RENDERABLE_ENTRY_FOR_REQUEST, None, (), None, (), None, False)


@dataclass(frozen=True)
class ScopeCeiling:
    temporal_scope_refs: tuple[str, ...] = ()
    subject_scope_refs: tuple[str, ...] = ()
    referent_scope_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "temporal_scope_refs", tuple(sorted({_text(item, "temporal_scope_ref") for item in self.temporal_scope_refs})))
        object.__setattr__(self, "subject_scope_refs", tuple(sorted({_text(item, "subject_scope_ref") for item in self.subject_scope_refs})))
        object.__setattr__(self, "referent_scope_refs", tuple(sorted({_text(item, "referent_scope_ref") for item in self.referent_scope_refs})))


@dataclass(frozen=True)
class ExpressionProjection:
    claim_ref: ActorSafeRef
    component_refs: tuple[ActorSafeRef, ...]
    actor_perceived_view_refs: tuple[ActorSafeRef, ...]
    temporal_scope_refs: tuple[str, ...]
    subject_scope_refs: tuple[str, ...]
    referent_scope_refs: tuple[str, ...]
    first_person_permission: str
    source_entry_hash: str

    @property
    def semantic_fingerprint(self) -> str:
        material = {
            "claim_ref": self.claim_ref.as_dict(),
            "component_refs": [item.as_dict() for item in self.component_refs],
            "actor_perceived_view_refs": [item.as_dict() for item in self.actor_perceived_view_refs],
            "temporal_scope_refs": list(self.temporal_scope_refs),
            "subject_scope_refs": list(self.subject_scope_refs),
            "referent_scope_refs": list(self.referent_scope_refs),
            "first_person_permission": self.first_person_permission,
            "source_entry_hash": self.source_entry_hash,
        }
        return hashlib.sha256(canonical_json(material).encode("utf-8")).hexdigest()


def _subset(requested: Sequence[str], allowed: Sequence[str], label: str) -> tuple[str, ...]:
    request_set = {_text(item, label) for item in requested}
    if not request_set <= set(allowed):
        raise M6SemanticWideningError(f"{label} widens the actor-safe source scope")
    return tuple(sorted(request_set))


def project_actor_safe_entry(
    decision: ActorSafeIngressDecision,
    *,
    source_scope_ceiling: ScopeCeiling,
    requested_claim_ref: ActorSafeRef | Mapping[str, str],
    requested_first_person_permission: str,
    requested_component_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    requested_actor_perceived_view_refs: Sequence[ActorSafeRef | Mapping[str, str]] = (),
    requested_temporal_scope_refs: Sequence[str] = (),
    requested_subject_scope_refs: Sequence[str] = (),
    requested_referent_scope_refs: Sequence[str] = (),
) -> ExpressionProjection:
    """One-entry monotone projection. Hidden joins have no API surface."""
    if not decision.positive_semantics or decision.claim_ref is None or decision.entry_hash is None:
        raise M6SemanticWideningError("non-positive receiver state cannot be projected")
    requested_claim = _ref(requested_claim_ref, "requested_claim_ref")
    if requested_claim != decision.claim_ref:
        raise M6SemanticWideningError("projection may not add/substitute a claim")
    permission = _text(requested_first_person_permission, "requested_first_person_permission")
    if permission != decision.first_person_permission:
        raise M6SemanticWideningError("permission class substitution is forbidden")
    components = _refs(requested_component_refs, "requested_component_ref")
    if decision.receiver_state is ReceiverState.READY_PARTIAL_COMPONENT_SCOPE:
        if not components:
            raise M6SemanticWideningError("partial access cannot be widened to whole-claim projection")
        if not set(components) <= set(decision.component_refs):
            raise M6SemanticWideningError("component scope widening is forbidden")
    elif components:
        raise M6SemanticWideningError("full claim does not grant unlisted component identities")
    views = _refs(requested_actor_perceived_view_refs, "requested_actor_perceived_view_ref")
    if not set(views) <= set(decision.actor_perceived_view_refs):
        raise M6SemanticWideningError("relationship-view scope widening is forbidden")
    return ExpressionProjection(
        decision.claim_ref,
        components,
        views,
        _subset(requested_temporal_scope_refs, source_scope_ceiling.temporal_scope_refs, "temporal_scope_ref"),
        _subset(requested_subject_scope_refs, source_scope_ceiling.subject_scope_refs, "subject_scope_ref"),
        _subset(requested_referent_scope_refs, source_scope_ceiling.referent_scope_refs, "referent_scope_ref"),
        permission,
        decision.entry_hash,
    )


def assert_behavioral_source_rejected(
    source: Any,
    *,
    declared_source_class: str | None = None,
    representation: str = "DIRECT",
) -> None:
    """Reject direct/indirect upstream, audit and concrete accepted M5 sources."""
    rep = _text(representation, "representation").upper()
    actual_m5 = isinstance(source, (
        ResolvedStructuralContext,
        RSCValidationReceipt,
        StructuralCurrentnessReceipt,
        StructuralPeerUseReceipt,
    ))
    source_class = _text(declared_source_class, "declared_source_class") if declared_source_class else type(source).__name__
    if actual_m5 or source_class in FORBIDDEN_BEHAVIORAL_SOURCE_CLASSES:
        raise M6ForbiddenBehavioralSource(
            f"{source_class} via {rep} is nonpersona/nonexpression evidence and has zero positive M6 effect"
        )
    raise M6ForbiddenBehavioralSource(
        "M6 has no generic behavioral-source admission path; positive semantics require verified actor-safe ingress"
    )


@dataclass(frozen=True)
class ExternalEventFeedback:
    decision: ExternalEventDecision
    admitted_occurrence_count: int
    v3_causal_mutation_count: int
    event_cursor_advance: int
    causal_session_cursor_advance: int
    automatic_actor_effect: bool


def external_event_feedback(decision: ExternalEventDecision | str) -> ExternalEventFeedback:
    try:
        state = ExternalEventDecision(decision)
    except ValueError as exc:
        raise M6IntegrityError("unknown external-event decision") from exc
    if state is ExternalEventDecision.ADMIT:
        return ExternalEventFeedback(state, 1, 1, 1, 1, False)
    return ExternalEventFeedback(state, 0, 0, 0, 0, False)


def situated_expression_behavior_status() -> str:
    """M6 intentionally owns no positive situated-phenomenology behavior."""
    return BLOCKED_NAMED_AUTHORITY_REQUIRED


def require_situated_expression_owner() -> None:
    raise M6NamedAuthorityRequired(
        "situated phenomenology/disclosure/salience/inhibition/affect/interlocutor/register behavior "
        "requires a separately accepted named authority; M6 is only the semantic ceiling"
    )
