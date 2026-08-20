#!/usr/bin/env python3
"""Clean-sideline runtime for the frozen M5 RSC / V3 structural peer-prior seam.

The accepted M4 runtime remains the sole owner of V558 exact resolution.  M5
replays that exact resolver, binds its immutable evidence, and may materialize a
ResolvedStructuralContext only with explicit currentness authority.  Structural
peer eligibility is not V3 mutation authority and this module exposes no actor
state mutation or empirical-prior synthesis surface.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Sequence

from rawlsing_next.m4_v557_v558_publication_repository import (
    M4IntegrityError,
    PermissionWideningError,
    ClosureIntegrityError,
    ReferenceClassError,
    AuthorityRef,
    ContextQuery,
    ExactRef,
    RepositoryEntry,
    ResolverPolicy,
    ResolutionResult,
    SelectionRecord,
    V558RepositoryBundle,
    FORBIDDEN_CLASSES,
    PERMISSION_ATOMS,
    RSC_SCHEMA,
    exact_ref,
    resolve_v558,
    semantic_hash,
)

M5_CONTRACT_ID = "M5_V3_STRUCTURAL_PEER_PRIOR_SEAM@1.0.0"
M5_CONTRACT_CORE_SHA256 = "54b9d262ec60ff8794f34d9caf68227275d272dc7d6b2254a9c84c996622d9f2"
M5_MACHINE_SIGNATURE_ID = "M4_TO_M5_RSC_MACHINE_SIGNATURE@1.0.0"
M5_CURRENTNESS_SCHEMA = "M5_STRUCTURAL_CURRENTNESS_RECEIPT@1.0.0"
M5_FIDELITY_SCHEMA = "M5_RSC_COVERAGE_FIDELITY_PROFILE@1.0.0"
M5_VALIDATION_SCHEMA = "M5_RSC_VALIDATION_RECEIPT@1.0.0"
V3_PEER_REQUIREMENT_SCHEMA = "V3PeerPriorRequirementDeclaration@1.0.0"
M5_PEER_USE_SCHEMA = "M5_STRUCTURAL_PEER_USE_RECEIPT@1.0.0"
M5_RSC_SUCCESS = "M5_RSC_VALIDATED_FOR_DECLARED_STRUCTURAL_PEER_USE"
M5_PEER_EFFECT = "STRUCTURAL_CONTEXT_ELIGIBILITY_ONLY__NOT_V3_MUTATION_PERMISSION"
BOUNDED_FAIL_CLOSED = "FAIL_CLOSED_ZERO_STRUCTURAL_PEER_EFFECT"

FROZEN_M5_FAILURE_CODES = frozenset({
    "M5_RSC_RUNTIME_INSTANCE_MISSING",
    "M5_RSC_SCHEMA_MISMATCH",
    "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
    "M5_RSC_SIGNATURE_MISMATCH",
    "M5_RSC_PRODUCER_BINDING_MISMATCH",
    "M5_RSC_PERMISSION_PROOF_INVALID",
    "M5_RSC_REFERENCE_CLOSURE_INVALID",
    "M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT",
    "M5_RSC_PROVENANCE_AUTHORITY_VIOLATION",
})

M5_MACHINE_SIGNATURE_FIELDS = (
    "rsc_schema_id_version",
    "rsc_context_id",
    "rsc_context_content_hash",
    "repository_bundle_id",
    "repository_bundle_content_hash",
    "context_query_id",
    "context_query_hash",
    "resolver_policy_id_version_hash",
    "resolution_receipt_id",
    "resolution_receipt_hash",
    "resolved_entry_set_digest",
    "preserved_negative_entry_set_digest",
    "deferred_unresolved_entry_set_digest",
    "selection_record_set_digest",
    "coverage_fidelity_profile_id_hash",
    "refresh_metadata_id_hash",
    "provenance_root_digest",
    "producer_binding_digest",
    "permission_subset_proof_digest",
    "reference_closure_digest",
)

PEER_REQUIREMENT_VALUES = frozenset({"REQUIRED", "OPTIONAL_BY_EXACT_OWNER_RULE", "NOT_USED"})
FORBIDDEN_ACTOR_OUTPUTS = frozenset({
    "generated_structural_position",
    "memory",
    "belief",
    "knowledge",
    "relationship",
    "action",
    "response",
    "persona",
    "voice",
})


class M5RuntimeIntegrityError(ValueError):
    """Fail-closed runtime error.

    ``code`` is either one of the already-frozen M5 failure tokens or the
    bounded non-semantic fail-closed behavior for stale/partial/M4-level
    resolver failures where stage-close intentionally froze no new M5 enum.
    """

    def __init__(self, code: str, reason: str):
        if code not in FROZEN_M5_FAILURE_CODES and code != BOUNDED_FAIL_CLOSED:
            raise ValueError("M5 runtime may not invent a new semantic failure code")
        self.code = code
        self.reason = reason
        super().__init__(f"{code}: {reason}")


class StructuralCurrentnessState(str, Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"
    REFRESH_REQUIRED = "REFRESH_REQUIRED"
    INVALID = "INVALID"


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", f"{name} must be a non-empty string"
        )
    out = value.strip()
    if out.lower() in {"latest", "default", "*"}:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            f"{name} may not use mutable/latest/default authority selection",
        )
    return out


def _ref_key(ref: ExactRef) -> tuple[str, str, str]:
    return ref.kind, ref.object_id, ref.content_hash


def _forbidden_semantic_class(name: str) -> bool:
    if name in FORBIDDEN_CLASSES:
        return True
    upper = name.upper()
    return (
        upper.startswith("V2_")
        or upper.startswith("V3_")
        or "ACTOR" in upper
        or "PERSONA" in upper
        or "PHENOMENOLOG" in upper
        or "RENDER" in upper
        or "VOICE" in upper
        or "PSYCHE" in upper
    )


@dataclass(frozen=True)
class StructuralCurrentnessReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    state: StructuralCurrentnessState
    authority_ref: AuthorityRef
    structural_currentness_basis_ref: ExactRef
    decision_effective_time_ref: ExactRef
    resolution_receipt_ref: ExactRef
    previous_currentness_ref: ExactRef | None = None
    refresh_reason_ref: ExactRef | None = None

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M5_STRUCTURAL_CURRENTNESS_RECEIPT", self.receipt_id, self.receipt_hash)


def _currentness_material(
    *,
    state: StructuralCurrentnessState,
    authority_ref: AuthorityRef,
    structural_currentness_basis_ref: ExactRef,
    decision_effective_time_ref: ExactRef,
    resolution_receipt_ref: ExactRef,
    previous_currentness_ref: ExactRef | None,
    refresh_reason_ref: ExactRef | None,
) -> dict[str, Any]:
    return {
        "schema": M5_CURRENTNESS_SCHEMA,
        "state": state.value,
        "authority_ref": authority_ref.as_dict(),
        "structural_currentness_basis_ref": structural_currentness_basis_ref.as_dict(),
        "decision_effective_time_ref": decision_effective_time_ref.as_dict(),
        "resolution_receipt_ref": resolution_receipt_ref.as_dict(),
        "previous_currentness_ref": previous_currentness_ref.as_dict() if previous_currentness_ref else None,
        "refresh_reason_ref": refresh_reason_ref.as_dict() if refresh_reason_ref else None,
    }


def make_structural_currentness_receipt(
    resolution: ResolutionResult,
    *,
    state: StructuralCurrentnessState | str,
    authority_ref: AuthorityRef,
    structural_currentness_basis_ref: ExactRef | Mapping[str, str],
    decision_effective_time_ref: ExactRef | Mapping[str, str],
    previous_currentness: StructuralCurrentnessReceipt | None = None,
    refresh_reason_ref: ExactRef | Mapping[str, str] | None = None,
) -> StructuralCurrentnessReceipt:
    if not isinstance(resolution, ResolutionResult):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "currentness must bind an exact accepted M4 ResolutionResult",
        )
    if not isinstance(authority_ref, AuthorityRef):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "currentness authority must be an exact AuthorityRef",
        )
    try:
        current_state = StructuralCurrentnessState(state)
        basis_ref = exact_ref(structural_currentness_basis_ref, "structural_currentness_basis_ref")
        time_ref = exact_ref(decision_effective_time_ref, "decision_effective_time_ref")
        reason_ref = exact_ref(refresh_reason_ref, "refresh_reason_ref") if refresh_reason_ref is not None else None
    except (ValueError, M4IntegrityError) as exc:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", str(exc)
        ) from exc
    previous_ref = previous_currentness.ref if previous_currentness is not None else None
    material = _currentness_material(
        state=current_state,
        authority_ref=authority_ref,
        structural_currentness_basis_ref=basis_ref,
        decision_effective_time_ref=time_ref,
        resolution_receipt_ref=resolution.receipt.ref,
        previous_currentness_ref=previous_ref,
        refresh_reason_ref=reason_ref,
    )
    h = semantic_hash(material)
    return StructuralCurrentnessReceipt(
        f"M5CUR:{h}",
        h,
        M5_CURRENTNESS_SCHEMA,
        current_state,
        authority_ref,
        basis_ref,
        time_ref,
        resolution.receipt.ref,
        previous_ref,
        reason_ref,
    )


def refresh_structural_currentness(
    previous: StructuralCurrentnessReceipt,
    resolution: ResolutionResult,
    *,
    state: StructuralCurrentnessState | str,
    authority_ref: AuthorityRef,
    structural_currentness_basis_ref: ExactRef | Mapping[str, str],
    decision_effective_time_ref: ExactRef | Mapping[str, str],
    refresh_reason_ref: ExactRef | Mapping[str, str],
) -> StructuralCurrentnessReceipt:
    """Create a prospective successor; the prior receipt is immutable history."""
    if not isinstance(previous, StructuralCurrentnessReceipt):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "refresh requires the exact prior currentness receipt",
        )
    return make_structural_currentness_receipt(
        resolution,
        state=state,
        authority_ref=authority_ref,
        structural_currentness_basis_ref=structural_currentness_basis_ref,
        decision_effective_time_ref=decision_effective_time_ref,
        previous_currentness=previous,
        refresh_reason_ref=refresh_reason_ref,
    )


def _validate_currentness(receipt: StructuralCurrentnessReceipt, resolution: ResolutionResult) -> None:
    if not isinstance(receipt, StructuralCurrentnessReceipt) or receipt.schema != M5_CURRENTNESS_SCHEMA:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "currentness receipt schema/type mismatch"
        )
    expected_material = _currentness_material(
        state=receipt.state,
        authority_ref=receipt.authority_ref,
        structural_currentness_basis_ref=receipt.structural_currentness_basis_ref,
        decision_effective_time_ref=receipt.decision_effective_time_ref,
        resolution_receipt_ref=receipt.resolution_receipt_ref,
        previous_currentness_ref=receipt.previous_currentness_ref,
        refresh_reason_ref=receipt.refresh_reason_ref,
    )
    h = semantic_hash(expected_material)
    if receipt.receipt_hash != h or receipt.receipt_id != f"M5CUR:{h}":
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "currentness receipt hash/identity mismatch"
        )
    if receipt.resolution_receipt_ref != resolution.receipt.ref:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "currentness receipt does not bind the exact M4 resolution receipt",
        )
    if receipt.state is not StructuralCurrentnessState.CURRENT:
        raise M5RuntimeIntegrityError(
            BOUNDED_FAIL_CLOSED,
            f"structural currentness is {receipt.state.value}; immutability alone is not currentness",
        )


@dataclass(frozen=True)
class V3PeerPriorRequirementDeclaration:
    declaration_id: str
    declaration_content_hash: str
    schema: str
    transition_owner_authority_ref: AuthorityRef
    transition_class: str
    structural_peer_requirement: str
    empirical_peer_requirement: str
    structural_peer_operation_ref: ExactRef | None
    empirical_read_permission_id: str | None
    effective_time_rule_ref: ExactRef
    causal_parent_rule_ref: ExactRef

    @property
    def ref(self) -> ExactRef:
        return ExactRef("V3_PEER_PRIOR_REQUIREMENT_DECLARATION", self.declaration_id, self.declaration_content_hash)


def _peer_requirement_material(
    *,
    transition_owner_authority_ref: AuthorityRef,
    transition_class: str,
    structural_peer_requirement: str,
    empirical_peer_requirement: str,
    structural_peer_operation_ref: ExactRef | None,
    empirical_read_permission_id: str | None,
    effective_time_rule_ref: ExactRef,
    causal_parent_rule_ref: ExactRef,
) -> dict[str, Any]:
    return {
        "schema": V3_PEER_REQUIREMENT_SCHEMA,
        "transition_owner_authority_ref": transition_owner_authority_ref.as_dict(),
        "transition_class": transition_class,
        "structural_peer_requirement": structural_peer_requirement,
        "empirical_peer_requirement": empirical_peer_requirement,
        "structural_peer_operation_ref": structural_peer_operation_ref.as_dict() if structural_peer_operation_ref else None,
        "empirical_read_permission_id": empirical_read_permission_id,
        "effective_time_rule_ref": effective_time_rule_ref.as_dict(),
        "causal_parent_rule_ref": causal_parent_rule_ref.as_dict(),
    }


def make_v3_peer_prior_requirement_declaration(
    *,
    transition_owner_authority_ref: AuthorityRef,
    transition_class: str,
    structural_peer_requirement: str,
    empirical_peer_requirement: str = "NOT_USED",
    structural_peer_operation_ref: ExactRef | Mapping[str, str] | None,
    empirical_read_permission_id: str | None = None,
    effective_time_rule_ref: ExactRef | Mapping[str, str],
    causal_parent_rule_ref: ExactRef | Mapping[str, str],
) -> V3PeerPriorRequirementDeclaration:
    if not isinstance(transition_owner_authority_ref, AuthorityRef):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "transition owner authority must be an exact AuthorityRef",
        )
    transition = _text(transition_class, "transition_class")
    if structural_peer_requirement not in PEER_REQUIREMENT_VALUES or empirical_peer_requirement not in PEER_REQUIREMENT_VALUES:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "peer requirement value is not frozen"
        )
    try:
        operation_ref = exact_ref(structural_peer_operation_ref, "structural_peer_operation_ref") if structural_peer_operation_ref is not None else None
        effective_ref = exact_ref(effective_time_rule_ref, "effective_time_rule_ref")
        parent_ref = exact_ref(causal_parent_rule_ref, "causal_parent_rule_ref")
    except M4IntegrityError as exc:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", str(exc)
        ) from exc
    if structural_peer_requirement == "NOT_USED" and operation_ref is not None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "NOT_USED structural peer may not carry an operation ref",
        )
    if structural_peer_requirement != "NOT_USED" and operation_ref is None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "used structural peer requires an exact owner operation ref",
        )
    if empirical_peer_requirement == "NOT_USED" and empirical_read_permission_id is not None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "NOT_USED empirical peer may not carry a read-permission id",
        )
    empirical_permission = _text(empirical_read_permission_id, "empirical_read_permission_id") if empirical_read_permission_id is not None else None
    material = _peer_requirement_material(
        transition_owner_authority_ref=transition_owner_authority_ref,
        transition_class=transition,
        structural_peer_requirement=structural_peer_requirement,
        empirical_peer_requirement=empirical_peer_requirement,
        structural_peer_operation_ref=operation_ref,
        empirical_read_permission_id=empirical_permission,
        effective_time_rule_ref=effective_ref,
        causal_parent_rule_ref=parent_ref,
    )
    h = semantic_hash(material)
    return V3PeerPriorRequirementDeclaration(
        f"V3PEERREQ:{h}",
        h,
        V3_PEER_REQUIREMENT_SCHEMA,
        transition_owner_authority_ref,
        transition,
        structural_peer_requirement,
        empirical_peer_requirement,
        operation_ref,
        empirical_permission,
        effective_ref,
        parent_ref,
    )


def _validate_peer_requirement(declaration: V3PeerPriorRequirementDeclaration) -> None:
    if not isinstance(declaration, V3PeerPriorRequirementDeclaration) or declaration.schema != V3_PEER_REQUIREMENT_SCHEMA:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "peer requirement declaration type/schema mismatch"
        )
    material = _peer_requirement_material(
        transition_owner_authority_ref=declaration.transition_owner_authority_ref,
        transition_class=declaration.transition_class,
        structural_peer_requirement=declaration.structural_peer_requirement,
        empirical_peer_requirement=declaration.empirical_peer_requirement,
        structural_peer_operation_ref=declaration.structural_peer_operation_ref,
        empirical_read_permission_id=declaration.empirical_read_permission_id,
        effective_time_rule_ref=declaration.effective_time_rule_ref,
        causal_parent_rule_ref=declaration.causal_parent_rule_ref,
    )
    h = semantic_hash(material)
    if declaration.declaration_content_hash != h or declaration.declaration_id != f"V3PEERREQ:{h}":
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "peer requirement declaration hash/identity mismatch"
        )


@dataclass(frozen=True)
class RSCEntry:
    resolution_key: str
    selection_record_ref: ExactRef
    canonical_producer_family: str
    producer_object_ref: ExactRef
    producer_locator_ref: ExactRef
    resolver_allowed_uses: tuple[str, ...]
    decision_state: str
    closure_digest: str


@dataclass(frozen=True)
class CoverageFidelityProfile:
    profile_id: str
    profile_hash: str
    schema: str
    resolution_result_state: str
    query_item_count: int
    selected_count: int
    unresolved_count: int
    complete: bool

    @property
    def id_hash(self) -> str:
        return f"{self.profile_id}|{self.profile_hash}"


@dataclass(frozen=True)
class ResolvedStructuralContext:
    schema: str
    context_id: str
    context_content_hash: str
    repository_ref: ExactRef
    context_query_id: str
    context_query_hash: str
    resolver_policy_id: str
    resolver_policy_version: str
    resolver_policy_hash: str
    resolution_receipt_ref: ExactRef
    resolution_result_state: str
    resolved_entries: tuple[RSCEntry, ...]
    resolved_entry_set_digest: str
    preserved_negative_entry_set_digest: str
    deferred_unresolved_entry_set_digest: str
    selection_record_set_digest: str
    coverage_fidelity_profile: CoverageFidelityProfile
    currentness_receipt_ref: ExactRef
    provenance_root_digest: str
    producer_binding_digest: str
    permission_subset_proof_digest: str
    reference_closure_digest: str
    machine_signature_id: str
    machine_signature_value: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef(RSC_SCHEMA, self.context_id, self.context_content_hash)


@dataclass(frozen=True)
class RSCValidationReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    rsc_ref: ExactRef
    currentness_ref: ExactRef
    result: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M5_RSC_VALIDATION_RECEIPT", self.receipt_id, self.receipt_hash)


@dataclass(frozen=True)
class StructuralPeerUseReceipt:
    receipt_id: str
    receipt_hash: str
    schema: str
    rsc_ref: ExactRef
    validation_receipt_ref: ExactRef
    peer_requirement_ref: ExactRef
    requested_use: str
    required_resolution_keys: tuple[str, ...]
    effect: str
    actor_state_effect: bool

    @property
    def ref(self) -> ExactRef:
        return ExactRef("M5_STRUCTURAL_PEER_USE_RECEIPT", self.receipt_id, self.receipt_hash)


def _exact_m4_resolution(
    repository: V558RepositoryBundle,
    query: ContextQuery,
    resolution: ResolutionResult,
    *,
    policy: ResolverPolicy,
    external_store: Mapping[str, Mapping[str, Any]] | None,
) -> ResolutionResult:
    try:
        expected = resolve_v558(repository, query, policy=policy, external_store=external_store)
    except PermissionWideningError as exc:
        raise M5RuntimeIntegrityError("M5_RSC_PERMISSION_PROOF_INVALID", str(exc)) from exc
    except ReferenceClassError as exc:
        raise M5RuntimeIntegrityError("M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT", str(exc)) from exc
    except ClosureIntegrityError as exc:
        raise M5RuntimeIntegrityError("M5_RSC_REFERENCE_CLOSURE_INVALID", str(exc)) from exc
    except M4IntegrityError as exc:
        raise M5RuntimeIntegrityError("M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", str(exc)) from exc
    if not isinstance(resolution, ResolutionResult):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "M5 requires an exact M4 ResolutionResult"
        )
    if resolution.resolved_structural_context is not None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "accepted M4 runtime must leave resolved_structural_context as None",
        )
    if (
        resolution.selection_records != expected.selection_records
        or resolution.resolved_entries != expected.resolved_entries
        or resolution.receipt != expected.receipt
    ):
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH",
            "supplied M4 evidence differs from deterministic exact re-resolution",
        )
    return expected


def _repository_entry_for_selection(
    repository: V558RepositoryBundle, selection: SelectionRecord
) -> RepositoryEntry:
    if selection.locator_ref is None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PRODUCER_BINDING_MISMATCH", "selected resolution lacks producer locator"
        )
    matches = [entry for entry in repository.entries if entry.locator.ref == selection.locator_ref]
    if len(matches) != 1:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PRODUCER_BINDING_MISMATCH", "selected locator is missing or ambiguous in exact repository"
        )
    entry = matches[0]
    try:
        RepositoryEntry(entry.obj, entry.governance, entry.locator)
    except (M4IntegrityError, PermissionWideningError) as exc:
        raise M5RuntimeIntegrityError("M5_RSC_PRODUCER_BINDING_MISMATCH", str(exc)) from exc
    if _forbidden_semantic_class(entry.obj.semantic_class):
        raise M5RuntimeIntegrityError(
            "M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT",
            "actor/V2/V3/persona/render object cannot enter structural peer semantics",
        )
    return entry


def _derive_evidence(
    repository: V558RepositoryBundle, query: ContextQuery, resolution: ResolutionResult
) -> tuple[tuple[RSCEntry, ...], str, str, str, str, CoverageFidelityProfile, str, str, str, str]:
    if resolution.receipt.result_state not in {"RESOLUTION_COMPLETE", "RESOLUTION_COMPLETE_VALID_EMPTY"}:
        raise M5RuntimeIntegrityError(
            BOUNDED_FAIL_CLOSED,
            f"M4 result {resolution.receipt.result_state} cannot fabricate a current structural peer",
        )
    if resolution.receipt.unresolved_keys:
        raise M5RuntimeIntegrityError(
            BOUNDED_FAIL_CLOSED, "unresolved required M4 keys forbid RSC materialization"
        )
    selection_by_key: dict[str, SelectionRecord] = {}
    for selection in resolution.selection_records:
        if selection.resolution_key in selection_by_key:
            raise M5RuntimeIntegrityError(
                "M5_RSC_REFERENCE_CLOSURE_INVALID", "duplicate exact SelectionRecord resolution key"
            )
        selection_by_key[selection.resolution_key] = selection
    resolved_by_key = {entry.resolution_key: entry for entry in resolution.resolved_entries}
    if len(resolved_by_key) != len(resolution.resolved_entries):
        raise M5RuntimeIntegrityError(
            "M5_RSC_REFERENCE_CLOSURE_INVALID", "duplicate exact ResolvedEntry resolution key"
        )
    selected_keys = {s.resolution_key for s in resolution.selection_records if s.decision == "SELECTED"}
    if set(resolved_by_key) != selected_keys:
        raise M5RuntimeIntegrityError(
            "M5_RSC_REFERENCE_CLOSURE_INVALID", "SelectionRecord and ResolvedEntry sets disagree"
        )
    if any(s.decision != "SELECTED" for s in resolution.selection_records):
        raise M5RuntimeIntegrityError(
            BOUNDED_FAIL_CLOSED, "complete RSC cannot silently retain denied/deferred/ambiguous selections"
        )

    rsc_entries: list[RSCEntry] = []
    provenance_material: list[dict[str, Any]] = []
    producer_material: list[dict[str, Any]] = []
    permission_material: list[dict[str, Any]] = []
    closure_material: list[dict[str, Any]] = []
    negative_material: list[dict[str, Any]] = []
    for resolved in resolution.resolved_entries:
        selection = selection_by_key.get(resolved.resolution_key)
        if selection is None or selection.decision != "SELECTED":
            raise M5RuntimeIntegrityError(
                "M5_RSC_REFERENCE_CLOSURE_INVALID", "ResolvedEntry lacks exact SELECTED SelectionRecord"
            )
        entry = _repository_entry_for_selection(repository, selection)
        if (
            selection.producer_object_ref != resolved.producer_object_ref
            or selection.producer_object_ref != entry.obj.ref
            or resolved.producer_locator_ref != entry.locator.ref
            or resolved.canonical_producer_family != entry.obj.producer_family
            or tuple(resolved.resolver_allowed_uses) != tuple(selection.resolver_allowed_uses)
            or resolved.decision_state != entry.obj.typed_state
        ):
            raise M5RuntimeIntegrityError(
                "M5_RSC_PRODUCER_BINDING_MISMATCH", "resolved producer identity/locator/family binding changed"
            )
        resolver_uses = set(selection.resolver_allowed_uses)
        if (
            not resolver_uses <= set(selection.v557_allowed_uses)
            or not set(selection.v557_allowed_uses) <= set(selection.producer_allowed_uses)
            or not resolver_uses <= set(entry.governance.v557_allowed_uses)
            or not set(entry.governance.v557_allowed_uses) <= set(entry.obj.producer_allowed_uses)
        ):
            raise M5RuntimeIntegrityError(
                "M5_RSC_PERMISSION_PROOF_INVALID", "resolver/V557/producer permission subset proof widened"
            )
        if not selection.closure_digest:
            raise M5RuntimeIntegrityError(
                "M5_RSC_REFERENCE_CLOSURE_INVALID", "selected M4 root lacks exact closure digest"
            )
        rsc_entries.append(RSCEntry(
            resolved.resolution_key,
            selection.ref,
            resolved.canonical_producer_family,
            resolved.producer_object_ref,
            resolved.producer_locator_ref,
            tuple(resolved.resolver_allowed_uses),
            resolved.decision_state,
            selection.closure_digest,
        ))
        provenance_material.append({
            "producer_object_ref": entry.obj.ref.as_dict(),
            "producer_locator_ref": entry.locator.ref.as_dict(),
            "provenance_locator": entry.locator.provenance_locator,
        })
        producer_material.append({
            "resolution_key": resolved.resolution_key,
            "producer_family": entry.obj.producer_family,
            "producer_object_ref": entry.obj.ref.as_dict(),
            "producer_locator_ref": entry.locator.ref.as_dict(),
            "selection_record_ref": selection.ref.as_dict(),
        })
        permission_material.append({
            "resolution_key": resolved.resolution_key,
            "selection_record_ref": selection.ref.as_dict(),
            "producer_allowed_uses": list(selection.producer_allowed_uses),
            "v557_allowed_uses": list(selection.v557_allowed_uses),
            "resolver_allowed_uses": list(selection.resolver_allowed_uses),
            "m4_closure_digest": selection.closure_digest,
        })
        closure_material.append({
            "resolution_key": resolved.resolution_key,
            "selection_record_ref": selection.ref.as_dict(),
            "m4_closure_digest": selection.closure_digest,
            "repository_ref": repository.ref.as_dict(),
        })
        negative_material.append({
            "resolution_key": resolved.resolution_key,
            "typed_state": selection.typed_state,
            "decision": selection.decision,
            "m4_closure_digest": selection.closure_digest,
        })

    entries_out = tuple(sorted(rsc_entries, key=lambda entry: entry.resolution_key))
    resolved_digest = semantic_hash([
        {
            "resolution_key": entry.resolution_key,
            "selection_record_ref": entry.selection_record_ref.as_dict(),
            "canonical_producer_family": entry.canonical_producer_family,
            "producer_object_ref": entry.producer_object_ref.as_dict(),
            "producer_locator_ref": entry.producer_locator_ref.as_dict(),
            "resolver_allowed_uses": list(entry.resolver_allowed_uses),
            "decision_state": entry.decision_state,
            "closure_digest": entry.closure_digest,
        }
        for entry in entries_out
    ])
    negative_digest = semantic_hash(sorted(negative_material, key=lambda item: item["resolution_key"]))
    deferred_digest = semantic_hash({
        "unresolved_keys": list(resolution.receipt.unresolved_keys),
        "nonselected": [
            {"resolution_key": s.resolution_key, "decision": s.decision, "typed_state": s.typed_state}
            for s in resolution.selection_records if s.decision != "SELECTED"
        ],
    })
    selection_digest = semantic_hash([s.ref.as_dict() for s in resolution.selection_records])
    fidelity_material = {
        "schema": M5_FIDELITY_SCHEMA,
        "resolution_result_state": resolution.receipt.result_state,
        "query_item_count": len(query.items),
        "selected_count": len(resolution.resolved_entries),
        "unresolved_count": len(resolution.receipt.unresolved_keys),
        "complete": True,
    }
    fidelity_hash = semantic_hash(fidelity_material)
    fidelity = CoverageFidelityProfile(
        f"M5FID:{fidelity_hash}",
        fidelity_hash,
        M5_FIDELITY_SCHEMA,
        resolution.receipt.result_state,
        len(query.items),
        len(resolution.resolved_entries),
        len(resolution.receipt.unresolved_keys),
        True,
    )
    provenance_digest = semantic_hash(sorted(
        provenance_material,
        key=lambda item: (
            item["producer_object_ref"]["kind"],
            item["producer_object_ref"]["object_id"],
            item["producer_object_ref"]["content_hash"],
        ),
    ))
    producer_digest = semantic_hash(sorted(producer_material, key=lambda item: item["resolution_key"]))
    permission_digest = semantic_hash(sorted(permission_material, key=lambda item: item["resolution_key"]))
    reference_digest = semantic_hash({
        "repository_ref": repository.ref.as_dict(),
        "resolution_receipt_ref": resolution.receipt.ref.as_dict(),
        "closure_records": sorted(closure_material, key=lambda item: item["resolution_key"]),
    })
    return (
        entries_out,
        resolved_digest,
        negative_digest,
        deferred_digest,
        selection_digest,
        fidelity,
        provenance_digest,
        producer_digest,
        permission_digest,
        reference_digest,
    )


def _rsc_content_material(
    *,
    repository: V558RepositoryBundle,
    query: ContextQuery,
    policy: ResolverPolicy,
    resolution: ResolutionResult,
    entries: Sequence[RSCEntry],
    resolved_entry_set_digest: str,
    preserved_negative_entry_set_digest: str,
    deferred_unresolved_entry_set_digest: str,
    selection_record_set_digest: str,
    fidelity: CoverageFidelityProfile,
    currentness: StructuralCurrentnessReceipt,
    provenance_root_digest: str,
    producer_binding_digest: str,
    permission_subset_proof_digest: str,
    reference_closure_digest: str,
) -> dict[str, Any]:
    return {
        "schema": RSC_SCHEMA,
        "m5_contract_id": M5_CONTRACT_ID,
        "m5_contract_core_sha256": M5_CONTRACT_CORE_SHA256,
        "repository_ref": repository.ref.as_dict(),
        "context_query_id": query.query_id,
        "context_query_hash": query.query_hash,
        "resolver_policy": policy.as_dict(),
        "resolution_receipt_ref": resolution.receipt.ref.as_dict(),
        "resolution_result_state": resolution.receipt.result_state,
        "resolved_entries": [
            {
                "resolution_key": entry.resolution_key,
                "selection_record_ref": entry.selection_record_ref.as_dict(),
                "canonical_producer_family": entry.canonical_producer_family,
                "producer_object_ref": entry.producer_object_ref.as_dict(),
                "producer_locator_ref": entry.producer_locator_ref.as_dict(),
                "resolver_allowed_uses": list(entry.resolver_allowed_uses),
                "decision_state": entry.decision_state,
                "closure_digest": entry.closure_digest,
            }
            for entry in entries
        ],
        "resolved_entry_set_digest": resolved_entry_set_digest,
        "preserved_negative_entry_set_digest": preserved_negative_entry_set_digest,
        "deferred_unresolved_entry_set_digest": deferred_unresolved_entry_set_digest,
        "selection_record_set_digest": selection_record_set_digest,
        "coverage_fidelity_profile": {
            "id": fidelity.profile_id,
            "hash": fidelity.profile_hash,
            "schema": fidelity.schema,
        },
        "currentness_receipt_ref": currentness.ref.as_dict(),
        "provenance_root_digest": provenance_root_digest,
        "producer_binding_digest": producer_binding_digest,
        "permission_subset_proof_digest": permission_subset_proof_digest,
        "reference_closure_digest": reference_closure_digest,
    }


def _machine_signature(
    *,
    context_id: str,
    context_content_hash: str,
    repository: V558RepositoryBundle,
    query: ContextQuery,
    policy: ResolverPolicy,
    resolution: ResolutionResult,
    resolved_entry_set_digest: str,
    preserved_negative_entry_set_digest: str,
    deferred_unresolved_entry_set_digest: str,
    selection_record_set_digest: str,
    fidelity: CoverageFidelityProfile,
    currentness: StructuralCurrentnessReceipt,
    provenance_root_digest: str,
    producer_binding_digest: str,
    permission_subset_proof_digest: str,
    reference_closure_digest: str,
) -> str:
    material = {
        "rsc_schema_id_version": RSC_SCHEMA,
        "rsc_context_id": context_id,
        "rsc_context_content_hash": context_content_hash,
        "repository_bundle_id": repository.repository_id,
        "repository_bundle_content_hash": repository.repository_hash,
        "context_query_id": query.query_id,
        "context_query_hash": query.query_hash,
        "resolver_policy_id_version_hash": f"{policy.policy_id}|{policy.policy_version}|{policy.policy_hash}",
        "resolution_receipt_id": resolution.receipt.receipt_id,
        "resolution_receipt_hash": resolution.receipt.receipt_hash,
        "resolved_entry_set_digest": resolved_entry_set_digest,
        "preserved_negative_entry_set_digest": preserved_negative_entry_set_digest,
        "deferred_unresolved_entry_set_digest": deferred_unresolved_entry_set_digest,
        "selection_record_set_digest": selection_record_set_digest,
        "coverage_fidelity_profile_id_hash": fidelity.id_hash,
        "refresh_metadata_id_hash": f"{currentness.receipt_id}|{currentness.receipt_hash}",
        "provenance_root_digest": provenance_root_digest,
        "producer_binding_digest": producer_binding_digest,
        "permission_subset_proof_digest": permission_subset_proof_digest,
        "reference_closure_digest": reference_closure_digest,
    }
    return semantic_hash([[field, material[field]] for field in M5_MACHINE_SIGNATURE_FIELDS])


def _build_expected_rsc(
    repository: V558RepositoryBundle,
    query: ContextQuery,
    resolution: ResolutionResult,
    currentness: StructuralCurrentnessReceipt,
    *,
    policy: ResolverPolicy,
    external_store: Mapping[str, Mapping[str, Any]] | None,
) -> ResolvedStructuralContext:
    exact_resolution = _exact_m4_resolution(
        repository, query, resolution, policy=policy, external_store=external_store
    )
    _validate_currentness(currentness, exact_resolution)
    (
        entries,
        resolved_digest,
        negative_digest,
        deferred_digest,
        selection_digest,
        fidelity,
        provenance_digest,
        producer_digest,
        permission_digest,
        reference_digest,
    ) = _derive_evidence(repository, query, exact_resolution)
    content = _rsc_content_material(
        repository=repository,
        query=query,
        policy=policy,
        resolution=exact_resolution,
        entries=entries,
        resolved_entry_set_digest=resolved_digest,
        preserved_negative_entry_set_digest=negative_digest,
        deferred_unresolved_entry_set_digest=deferred_digest,
        selection_record_set_digest=selection_digest,
        fidelity=fidelity,
        currentness=currentness,
        provenance_root_digest=provenance_digest,
        producer_binding_digest=producer_digest,
        permission_subset_proof_digest=permission_digest,
        reference_closure_digest=reference_digest,
    )
    context_hash = semantic_hash(content)
    context_id = f"RSC:{context_hash}"
    signature = _machine_signature(
        context_id=context_id,
        context_content_hash=context_hash,
        repository=repository,
        query=query,
        policy=policy,
        resolution=exact_resolution,
        resolved_entry_set_digest=resolved_digest,
        preserved_negative_entry_set_digest=negative_digest,
        deferred_unresolved_entry_set_digest=deferred_digest,
        selection_record_set_digest=selection_digest,
        fidelity=fidelity,
        currentness=currentness,
        provenance_root_digest=provenance_digest,
        producer_binding_digest=producer_digest,
        permission_subset_proof_digest=permission_digest,
        reference_closure_digest=reference_digest,
    )
    return ResolvedStructuralContext(
        RSC_SCHEMA,
        context_id,
        context_hash,
        repository.ref,
        query.query_id,
        query.query_hash,
        policy.policy_id,
        policy.policy_version,
        policy.policy_hash,
        exact_resolution.receipt.ref,
        exact_resolution.receipt.result_state,
        entries,
        resolved_digest,
        negative_digest,
        deferred_digest,
        selection_digest,
        fidelity,
        currentness.ref,
        provenance_digest,
        producer_digest,
        permission_digest,
        reference_digest,
        M5_MACHINE_SIGNATURE_ID,
        signature,
    )


def materialize_resolved_structural_context(
    repository: V558RepositoryBundle,
    query: ContextQuery,
    resolution: ResolutionResult,
    currentness: StructuralCurrentnessReceipt,
    *,
    policy: ResolverPolicy = ResolverPolicy(),
    external_store: Mapping[str, Mapping[str, Any]] | None = None,
) -> ResolvedStructuralContext:
    """Materialize only from complete exact M4 evidence and explicit CURRENT evidence."""
    return _build_expected_rsc(
        repository, query, resolution, currentness, policy=policy, external_store=external_store
    )


def _rsc_self_material(rsc: ResolvedStructuralContext) -> dict[str, Any]:
    fidelity = rsc.coverage_fidelity_profile
    return {
        "schema": rsc.schema,
        "m5_contract_id": M5_CONTRACT_ID,
        "m5_contract_core_sha256": M5_CONTRACT_CORE_SHA256,
        "repository_ref": rsc.repository_ref.as_dict(),
        "context_query_id": rsc.context_query_id,
        "context_query_hash": rsc.context_query_hash,
        "resolver_policy": {
            "id": rsc.resolver_policy_id,
            "version": rsc.resolver_policy_version,
            "content_hash": rsc.resolver_policy_hash,
        },
        "resolution_receipt_ref": rsc.resolution_receipt_ref.as_dict(),
        "resolution_result_state": rsc.resolution_result_state,
        "resolved_entries": [
            {
                "resolution_key": entry.resolution_key,
                "selection_record_ref": entry.selection_record_ref.as_dict(),
                "canonical_producer_family": entry.canonical_producer_family,
                "producer_object_ref": entry.producer_object_ref.as_dict(),
                "producer_locator_ref": entry.producer_locator_ref.as_dict(),
                "resolver_allowed_uses": list(entry.resolver_allowed_uses),
                "decision_state": entry.decision_state,
                "closure_digest": entry.closure_digest,
            }
            for entry in rsc.resolved_entries
        ],
        "resolved_entry_set_digest": rsc.resolved_entry_set_digest,
        "preserved_negative_entry_set_digest": rsc.preserved_negative_entry_set_digest,
        "deferred_unresolved_entry_set_digest": rsc.deferred_unresolved_entry_set_digest,
        "selection_record_set_digest": rsc.selection_record_set_digest,
        "coverage_fidelity_profile": {
            "id": fidelity.profile_id,
            "hash": fidelity.profile_hash,
            "schema": fidelity.schema,
        },
        "currentness_receipt_ref": rsc.currentness_receipt_ref.as_dict(),
        "provenance_root_digest": rsc.provenance_root_digest,
        "producer_binding_digest": rsc.producer_binding_digest,
        "permission_subset_proof_digest": rsc.permission_subset_proof_digest,
        "reference_closure_digest": rsc.reference_closure_digest,
    }


def validate_resolved_structural_context(
    rsc: ResolvedStructuralContext | None,
    repository: V558RepositoryBundle,
    query: ContextQuery,
    resolution: ResolutionResult,
    currentness: StructuralCurrentnessReceipt,
    *,
    policy: ResolverPolicy = ResolverPolicy(),
    external_store: Mapping[str, Mapping[str, Any]] | None = None,
) -> RSCValidationReceipt:
    if rsc is None:
        raise M5RuntimeIntegrityError(
            "M5_RSC_RUNTIME_INSTANCE_MISSING", "actual runtime ResolvedStructuralContext is required"
        )
    if not isinstance(rsc, ResolvedStructuralContext) or rsc.schema != RSC_SCHEMA:
        raise M5RuntimeIntegrityError(
            "M5_RSC_SCHEMA_MISMATCH", "ResolvedStructuralContext type/schema/version mismatch"
        )
    if any(_forbidden_semantic_class(entry.producer_object_ref.kind) for entry in rsc.resolved_entries):
        raise M5RuntimeIntegrityError(
            "M5_RSC_FORBIDDEN_REFERENCE_CLASS_PRESENT", "forbidden actor/V2/V3 reference class in RSC"
        )
    expected = _build_expected_rsc(
        repository, query, resolution, currentness, policy=policy, external_store=external_store
    )
    if rsc.producer_binding_digest != expected.producer_binding_digest:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PRODUCER_BINDING_MISMATCH", "producer binding digest differs from exact M4 evidence"
        )
    if rsc.permission_subset_proof_digest != expected.permission_subset_proof_digest:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PERMISSION_PROOF_INVALID", "item-wise permission proof digest differs from exact M4 evidence"
        )
    if rsc.reference_closure_digest != expected.reference_closure_digest:
        raise M5RuntimeIntegrityError(
            "M5_RSC_REFERENCE_CLOSURE_INVALID", "positive/negative closure digest differs from exact M4 evidence"
        )
    if rsc.provenance_root_digest != expected.provenance_root_digest:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PROVENANCE_AUTHORITY_VIOLATION", "provenance digest differs from exact origin evidence"
        )
    if rsc.machine_signature_id != M5_MACHINE_SIGNATURE_ID or rsc.machine_signature_value != expected.machine_signature_value:
        raise M5RuntimeIntegrityError(
            "M5_RSC_SIGNATURE_MISMATCH", "M4-to-M5 RSC machine signature mismatch"
        )
    own_hash = semantic_hash(_rsc_self_material(rsc))
    if rsc.context_content_hash != own_hash or rsc.context_id != f"RSC:{own_hash}":
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "RSC context identity/content hash mismatch"
        )
    if rsc != expected:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "RSC differs from deterministic exact materialization"
        )
    material = {
        "schema": M5_VALIDATION_SCHEMA,
        "rsc_ref": rsc.ref.as_dict(),
        "currentness_ref": currentness.ref.as_dict(),
        "result": M5_RSC_SUCCESS,
    }
    h = semantic_hash(material)
    return RSCValidationReceipt(
        f"M5RSCVAL:{h}", h, M5_VALIDATION_SCHEMA, rsc.ref, currentness.ref, M5_RSC_SUCCESS
    )


def _validate_validation_receipt(receipt: RSCValidationReceipt, rsc: ResolvedStructuralContext) -> None:
    if not isinstance(receipt, RSCValidationReceipt) or receipt.schema != M5_VALIDATION_SCHEMA or receipt.rsc_ref != rsc.ref:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "peer use requires exact validation receipt for this RSC"
        )
    material = {
        "schema": receipt.schema,
        "rsc_ref": receipt.rsc_ref.as_dict(),
        "currentness_ref": receipt.currentness_ref.as_dict(),
        "result": receipt.result,
    }
    h = semantic_hash(material)
    if receipt.receipt_hash != h or receipt.receipt_id != f"M5RSCVAL:{h}" or receipt.result != M5_RSC_SUCCESS:
        raise M5RuntimeIntegrityError(
            "M5_RSC_IDENTITY_OR_CONTENT_HASH_MISMATCH", "validation receipt hash/result mismatch"
        )


def bind_structural_peer_use(
    rsc: ResolvedStructuralContext,
    validation_receipt: RSCValidationReceipt,
    peer_requirement: V3PeerPriorRequirementDeclaration,
    *,
    requested_use: str,
    required_resolution_keys: Sequence[str],
) -> StructuralPeerUseReceipt:
    """Bind structural eligibility only; no actor state is accepted or returned."""
    if not isinstance(rsc, ResolvedStructuralContext):
        raise M5RuntimeIntegrityError("M5_RSC_SCHEMA_MISMATCH", "structural peer must be exact RSC")
    _validate_validation_receipt(validation_receipt, rsc)
    _validate_peer_requirement(peer_requirement)
    if peer_requirement.structural_peer_requirement == "NOT_USED" or peer_requirement.structural_peer_operation_ref is None:
        raise M5RuntimeIntegrityError(
            BOUNDED_FAIL_CLOSED, "transition owner declaration does not authorize structural-peer consultation"
        )
    use = _text(requested_use, "requested_use")
    if use not in PERMISSION_ATOMS:
        raise M5RuntimeIntegrityError(
            "M5_RSC_PERMISSION_PROOF_INVALID", "requested structural use is not a frozen M4 permission atom"
        )
    keys = tuple(_text(key, "required_resolution_key") for key in required_resolution_keys)
    if not keys or len(set(keys)) != len(keys):
        raise M5RuntimeIntegrityError(
            "M5_RSC_REFERENCE_CLOSURE_INVALID", "peer use requires a unique non-empty exact resolution-key set"
        )
    by_key = {entry.resolution_key: entry for entry in rsc.resolved_entries}
    for key in keys:
        entry = by_key.get(key)
        if entry is None:
            raise M5RuntimeIntegrityError(
                "M5_RSC_REFERENCE_CLOSURE_INVALID", "declared structural peer key is absent from RSC"
            )
        if use not in entry.resolver_allowed_uses:
            raise M5RuntimeIntegrityError(
                "M5_RSC_PERMISSION_PROOF_INVALID", "RSC availability cannot widen resolver-authorized use"
            )
    material = {
        "schema": M5_PEER_USE_SCHEMA,
        "rsc_ref": rsc.ref.as_dict(),
        "validation_receipt_ref": validation_receipt.ref.as_dict(),
        "peer_requirement_ref": peer_requirement.ref.as_dict(),
        "requested_use": use,
        "required_resolution_keys": list(keys),
        "effect": M5_PEER_EFFECT,
        "actor_state_effect": False,
    }
    h = semantic_hash(material)
    return StructuralPeerUseReceipt(
        f"M5PEERUSE:{h}",
        h,
        M5_PEER_USE_SCHEMA,
        rsc.ref,
        validation_receipt.ref,
        peer_requirement.ref,
        use,
        keys,
        M5_PEER_EFFECT,
        False,
    )
