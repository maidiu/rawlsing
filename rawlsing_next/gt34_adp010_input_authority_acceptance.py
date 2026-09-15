"""OBL056 candidate: exact ADP-010 input-authority acceptance binding only."""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
import unicodedata
from typing import Any

ACCEPTANCE_AUTHORITY_ID = "GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY"
ACCEPTANCE_AUTHORITY_VERSION = "1.0.0"
REGISTRY_ID = ACCEPTANCE_AUTHORITY_ID
REGISTRY_VERSION = "1.0.0"
RECEIPT_SCHEMA_ID = "GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_RECEIPT@1.0.0"
ENTRY_SCHEMA_ID = "GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_ENTRY@1.0.0"
REGISTRY_SNAPSHOT_SCHEMA_ID = "GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY_SNAPSHOT@1.0.0"
CONSUMER = "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0"
CAUSAL_USE_PERMISSION = "CAUSAL_USE_PERMISSION"
POSITIVE_APPLICABILITY = "POSITIVE_APPLICABILITY"
CONTACT_OCCURRENCE_WITNESS = "CONTACT_OCCURRENCE_WITNESS"
CONTACT_WITNESS_INDEPENDENCE = "CONTACT_WITNESS_INDEPENDENCE"
SUPPORTED_ROLES = (
    CAUSAL_USE_PERMISSION,
    POSITIVE_APPLICABILITY,
    CONTACT_OCCURRENCE_WITNESS,
    CONTACT_WITNESS_INDEPENDENCE,
)
CURRENT_ACCEPTED = "CURRENT_ACCEPTED"
NONCURRENT_SYNTHETIC_TEST_ONLY = "NONCURRENT_SYNTHETIC_TEST_ONLY"
CANDIDATE_NOT_ADOPTED = "CANDIDATE_NOT_ADOPTED"
ACCEPT = "ACCEPT"
AUTHORITY_CEILING = (
    "NO_SUBJECT_IDENTITY_OR_CLASSIFICATION",
    "NO_CAUSAL_USE_SEMANTIC_TRUTH",
    "NO_APPLICABILITY_SEMANTIC_TRUTH",
    "NO_CONTACT_OCCURRENCE",
    "NO_CONTACT_INDEPENDENCE_FACT",
    "NO_ENCOUNTER",
    "NO_EXPOSURE",
    "NO_EXTERNAL_EVENT_ADMISSION",
    "NO_COMPARATOR",
    "NO_PSEPF",
    "NO_METABOLISM",
    "NO_CAN_008",
    "NO_V2",
    "NO_POSITIVE_V3_ACTOR_MUTATION",
    "NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION",
)
_DOMAIN = "RAWLSING\0GT34\0OBL056\0ADP010_INPUT_AUTHORITY_ACCEPTANCE_V1\0"


class AcceptanceAuthorityError(ValueError):
    pass


class AcceptanceIntegrityError(AcceptanceAuthorityError):
    pass


class AcceptanceMissingAuthority(AcceptanceAuthorityError):
    pass


class AcceptanceOutOfScope(AcceptanceAuthorityError):
    pass


def _norm(v: Any) -> Any:
    if isinstance(v, str):
        return unicodedata.normalize("NFC", v)
    if isinstance(v, dict):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_norm(x) for x in v]
    return v


def _canonical_json(v: Any) -> str:
    return json.dumps(_norm(v), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(label: str, v: Any) -> str:
    return sha256((_DOMAIN + label + "\0" + _canonical_json(v)).encode()).hexdigest()


@dataclass(frozen=True, order=True, slots=True)
class ContentAddressedRef:
    id: str
    version: str
    content_hash: str


@dataclass(frozen=True, order=True, slots=True)
class EvidenceRef:
    ref: str
    content_hash: str


@dataclass(frozen=True, slots=True)
class AcceptanceScope:
    transition_use_scope: str
    family_scope: tuple[str, ...] = ()
    subject_scope: tuple[str, ...] = ()
    object_scope: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class AcceptanceEntry:
    schema_id: str
    role: str
    accepted_authority_ref: ContentAddressedRef
    accepted_authority_owner_jurisdiction_ref: EvidenceRef
    source_acceptance_evidence_ref: EvidenceRef
    decision_state: str
    consumer: str
    scope: AcceptanceScope
    negative_limit_refs: tuple[EvidenceRef, ...]
    currentness_state: str
    immutable_provenance: tuple[EvidenceRef, ...]
    entry_id: str
    entry_hash: str


@dataclass(frozen=True, slots=True)
class AcceptanceReceipt:
    schema_id: str
    acceptance_authority_ref: ContentAddressedRef
    registry_ref: ContentAddressedRef
    registry_entry_ref: EvidenceRef
    role: str
    accepted_authority_ref: ContentAddressedRef
    accepted_authority_owner_jurisdiction_ref: EvidenceRef
    source_acceptance_evidence_ref: EvidenceRef
    decision_state: str
    consumer: str
    scope: AcceptanceScope
    negative_limit_refs: tuple[EvidenceRef, ...]
    currentness_state: str
    immutable_provenance: tuple[EvidenceRef, ...]
    receipt_id: str
    receipt_hash: str


@dataclass(frozen=True, slots=True)
class AcceptanceRegistrySnapshot:
    schema_id: str
    acceptance_authority_ref: ContentAddressedRef
    registry_ref: ContentAddressedRef
    currentness_state: str
    adoption_current_selection_evidence_refs: tuple[EvidenceRef, ...]
    immutable_provenance: tuple[EvidenceRef, ...]
    entries: tuple[AcceptanceEntry, ...]


_TRANSITION_USE_BY_ROLE = {
    CAUSAL_USE_PERMISSION: "BASIS_TO_AVAILABLE:ADP010_CAUSAL_USE",
    POSITIVE_APPLICABILITY: "AVAILABLE_TO_OPPORTUNITY:POSITIVE_APPLICABILITY",
    CONTACT_OCCURRENCE_WITNESS: "OPPORTUNITY_TO_ENCOUNTER:CONTACT_OCCURRENCE_WITNESS",
    CONTACT_WITNESS_INDEPENDENCE: "OPPORTUNITY_TO_ENCOUNTER:CONTACT_WITNESS_INDEPENDENCE",
}
_AUTHORITY_MATERIAL = {
    "authority_id": ACCEPTANCE_AUTHORITY_ID,
    "authority_version": ACCEPTANCE_AUTHORITY_VERSION,
    "grain": "EXACT_ALREADY_EXISTING_AUTHORITY_ACCEPTANCE_FOR_ONE_ADP010_INPUT_ROLE_AND_SCOPE_ONLY",
    "consumer": CONSUMER,
    "supported_roles": SUPPORTED_ROLES,
    "status": CANDIDATE_NOT_ADOPTED,
    "authority_ceiling": AUTHORITY_CEILING,
    "contract_revision": "R2_FUTURE_CURRENT_EXACT_MEMBERSHIP_AND_CONTACT_CONSTITUENT_VALIDATION",
    "future_current_law": "CURRENT_ACCEPTED_REQUIRES_EXACT_GOVERNED_REGISTRY_MEMBERSHIP_AND_ADOPTION_CURRENT_SELECTION_EVIDENCE",
    "contact_pair_law": "VALIDATE_BOTH_CONSTITUENT_ACCEPTANCE_RECEIPTS_BEFORE_PAIR_DISTINCTNESS",
}
ACCEPTANCE_AUTHORITY_CONTENT_HASH = _digest("AUTHORITY", _AUTHORITY_MATERIAL)
ACCEPTANCE_AUTHORITY_REF = ContentAddressedRef(
    ACCEPTANCE_AUTHORITY_ID, ACCEPTANCE_AUTHORITY_VERSION, ACCEPTANCE_AUTHORITY_CONTENT_HASH
)


def _ev(label: str, v: Any) -> EvidenceRef:
    h = _digest("EVIDENCE:" + label, v)
    return EvidenceRef("urn:rawlsing:gt34:obl056:evidence:" + label + ":sha256:" + h, h)


def _entry_body(e: AcceptanceEntry) -> dict[str, Any]:
    return {
        "schema_id": e.schema_id,
        "role": e.role,
        "accepted_authority_ref": asdict(e.accepted_authority_ref),
        "accepted_authority_owner_jurisdiction_ref": asdict(e.accepted_authority_owner_jurisdiction_ref),
        "source_acceptance_evidence_ref": asdict(e.source_acceptance_evidence_ref),
        "decision_state": e.decision_state,
        "consumer": e.consumer,
        "scope": asdict(e.scope),
        "negative_limit_refs": [asdict(x) for x in e.negative_limit_refs],
        "currentness_state": e.currentness_state,
        "immutable_provenance": [asdict(x) for x in e.immutable_provenance],
    }


def _check_entry_integrity(e: AcceptanceEntry) -> None:
    h = _digest("ENTRY", _entry_body(e))
    if e.entry_hash != h or e.entry_id != "urn:rawlsing:gt34:obl056:acceptance-entry:sha256:" + h:
        raise AcceptanceIntegrityError("registry entry content/hash mismatch")


def _registry_material(
    *,
    acceptance_authority_ref: ContentAddressedRef,
    currentness_state: str,
    adoption_current_selection_evidence_refs: tuple[EvidenceRef, ...],
    immutable_provenance: tuple[EvidenceRef, ...],
    entries: tuple[AcceptanceEntry, ...],
) -> dict[str, Any]:
    return {
        "registry_schema_id": REGISTRY_SNAPSHOT_SCHEMA_ID,
        "registry_id": REGISTRY_ID,
        "registry_version": REGISTRY_VERSION,
        "acceptance_authority_ref": asdict(acceptance_authority_ref),
        "receipt_schema_id": RECEIPT_SCHEMA_ID,
        "consumer": CONSUMER,
        "supported_roles": SUPPORTED_ROLES,
        "currentness_state": currentness_state,
        "adoption_current_selection_evidence_refs": [asdict(x) for x in adoption_current_selection_evidence_refs],
        "immutable_provenance": [asdict(x) for x in immutable_provenance],
        "current_positive_entries": [{"entry_id": e.entry_id, "entry_hash": e.entry_hash} for e in entries],
    }


def _make_registry_snapshot(
    entries: tuple[AcceptanceEntry, ...],
    *,
    currentness_state: str,
    adoption_current_selection_evidence_refs: tuple[EvidenceRef, ...] = (),
    immutable_provenance: tuple[EvidenceRef, ...] = (),
) -> AcceptanceRegistrySnapshot:
    for e in entries:
        _check_entry_integrity(e)
        if e.role not in SUPPORTED_ROLES:
            raise AcceptanceOutOfScope("unsupported registry role")
        if e.consumer != CONSUMER or e.decision_state != ACCEPT:
            raise AcceptanceMissingAuthority("registry contains nonpositive/out-of-scope entry")
        if e.currentness_state != currentness_state:
            raise AcceptanceOutOfScope("registry entry currentness mismatch")
    if currentness_state == CURRENT_ACCEPTED:
        if not adoption_current_selection_evidence_refs:
            raise AcceptanceMissingAuthority("current registry requires adoption/current-selection evidence")
        if not immutable_provenance:
            raise AcceptanceMissingAuthority("current registry requires immutable provenance")
        if any(not e.immutable_provenance for e in entries):
            raise AcceptanceMissingAuthority("current registry entry requires immutable provenance")
        allowed = set(adoption_current_selection_evidence_refs)
        if any(e.source_acceptance_evidence_ref not in allowed for e in entries):
            raise AcceptanceMissingAuthority("current entry source evidence is not governed by current registry selection")
    elif currentness_state != CANDIDATE_NOT_ADOPTED:
        raise AcceptanceOutOfScope("unsupported registry currentness")
    material = _registry_material(
        acceptance_authority_ref=ACCEPTANCE_AUTHORITY_REF,
        currentness_state=currentness_state,
        adoption_current_selection_evidence_refs=adoption_current_selection_evidence_refs,
        immutable_provenance=immutable_provenance,
        entries=entries,
    )
    h = _digest("REGISTRY", material)
    return AcceptanceRegistrySnapshot(
        REGISTRY_SNAPSHOT_SCHEMA_ID,
        ACCEPTANCE_AUTHORITY_REF,
        ContentAddressedRef(REGISTRY_ID, REGISTRY_VERSION, h),
        currentness_state,
        adoption_current_selection_evidence_refs,
        immutable_provenance,
        entries,
    )


_CURRENT_REGISTRY = _make_registry_snapshot((), currentness_state=CANDIDATE_NOT_ADOPTED)
_CURRENT_ENTRIES: tuple[AcceptanceEntry, ...] = _CURRENT_REGISTRY.entries
REGISTRY_REF = _CURRENT_REGISTRY.registry_ref
REGISTRY_CONTENT_HASH = REGISTRY_REF.content_hash


def _make_entry(role: str) -> AcceptanceEntry:
    ar = ContentAddressedRef(
        "SYNTHETIC_EXISTING_" + role + "_AUTHORITY",
        "1.0.0",
        _digest("SYNTH_ACCEPTED:" + role, {"role": role}),
    )
    owner = _ev("synthetic-owner-" + role.lower(), {"role": role})
    source = _ev("synthetic-source-" + role.lower(), {"role": role, "accepted": True})
    prov = (_ev("synthetic-provenance", {"mode": NONCURRENT_SYNTHETIC_TEST_ONLY}),)
    scope = AcceptanceScope(
        _TRANSITION_USE_BY_ROLE[role],
        ("SYNTHETIC_TEST_FAMILY",),
        ("SYNTHETIC_TEST_SUBJECT",),
        ("SYNTHETIC_TEST_OBJECT",),
    )
    p = AcceptanceEntry(
        ENTRY_SCHEMA_ID, role, ar, owner, source, ACCEPT, CONSUMER, scope, (),
        NONCURRENT_SYNTHETIC_TEST_ONLY, prov, "PENDING", "0" * 64
    )
    h = _digest("ENTRY", _entry_body(p))
    return replace(p, entry_id="urn:rawlsing:gt34:obl056:acceptance-entry:sha256:" + h, entry_hash=h)


_SYNTH_ENTRIES = tuple(_make_entry(r) for r in SUPPORTED_ROLES)
_SYNTH_AUTHORITY_REF = ContentAddressedRef(
    ACCEPTANCE_AUTHORITY_ID + "_SYNTHETIC_TEST",
    "1.0.0",
    _digest("SYNTH_AUTHORITY", {"roles": SUPPORTED_ROLES, "currentness": NONCURRENT_SYNTHETIC_TEST_ONLY}),
)
_SYNTH_REGISTRY_REF = ContentAddressedRef(
    REGISTRY_ID + "_SYNTHETIC_TEST",
    "1.0.0",
    _digest("SYNTH_REGISTRY", [e.entry_hash for e in _SYNTH_ENTRIES]),
)


def _receipt_body(r: AcceptanceReceipt) -> dict[str, Any]:
    return {
        "schema_id": r.schema_id,
        "acceptance_authority_ref": asdict(r.acceptance_authority_ref),
        "registry_ref": asdict(r.registry_ref),
        "registry_entry_ref": asdict(r.registry_entry_ref),
        "role": r.role,
        "accepted_authority_ref": asdict(r.accepted_authority_ref),
        "accepted_authority_owner_jurisdiction_ref": asdict(r.accepted_authority_owner_jurisdiction_ref),
        "source_acceptance_evidence_ref": asdict(r.source_acceptance_evidence_ref),
        "decision_state": r.decision_state,
        "consumer": r.consumer,
        "scope": asdict(r.scope),
        "negative_limit_refs": [asdict(x) for x in r.negative_limit_refs],
        "currentness_state": r.currentness_state,
        "immutable_provenance": [asdict(x) for x in r.immutable_provenance],
    }


def _issue_for_refs(e: AcceptanceEntry, acceptance_authority_ref: ContentAddressedRef, registry_ref: ContentAddressedRef) -> AcceptanceReceipt:
    p = AcceptanceReceipt(
        RECEIPT_SCHEMA_ID,
        acceptance_authority_ref,
        registry_ref,
        EvidenceRef(e.entry_id, e.entry_hash),
        e.role,
        e.accepted_authority_ref,
        e.accepted_authority_owner_jurisdiction_ref,
        e.source_acceptance_evidence_ref,
        e.decision_state,
        e.consumer,
        e.scope,
        e.negative_limit_refs,
        e.currentness_state,
        e.immutable_provenance,
        "PENDING",
        "0" * 64,
    )
    h = _digest("RECEIPT", _receipt_body(p))
    return replace(p, receipt_id="urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:" + h, receipt_hash=h)


def _issue(e: AcceptanceEntry) -> AcceptanceReceipt:
    return _issue_for_refs(e, _SYNTH_AUTHORITY_REF, _SYNTH_REGISTRY_REF)


def issue_noncurrent_synthetic_test_receipt(role: str) -> AcceptanceReceipt:
    if role not in SUPPORTED_ROLES:
        raise AcceptanceOutOfScope("unsupported role")
    return _issue(next(e for e in _SYNTH_ENTRIES if e.role == role))


def _check_integrity(r: AcceptanceReceipt) -> None:
    h = _digest("RECEIPT", _receipt_body(r))
    if r.receipt_hash != h or r.receipt_id != "urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:" + h:
        raise AcceptanceIntegrityError("acceptance receipt content/hash mismatch")


def _entry_matches_receipt(e: AcceptanceEntry, r: AcceptanceReceipt) -> bool:
    return (
        e.role == r.role
        and e.accepted_authority_ref == r.accepted_authority_ref
        and e.accepted_authority_owner_jurisdiction_ref == r.accepted_authority_owner_jurisdiction_ref
        and e.source_acceptance_evidence_ref == r.source_acceptance_evidence_ref
        and e.decision_state == r.decision_state
        and e.consumer == r.consumer
        and e.scope == r.scope
        and e.negative_limit_refs == r.negative_limit_refs
        and e.currentness_state == r.currentness_state
        and e.immutable_provenance == r.immutable_provenance
    )


def _validate_registry_snapshot_integrity(snapshot: AcceptanceRegistrySnapshot) -> None:
    if snapshot.schema_id != REGISTRY_SNAPSHOT_SCHEMA_ID:
        raise AcceptanceIntegrityError("registry snapshot schema mismatch")
    if snapshot.acceptance_authority_ref != ACCEPTANCE_AUTHORITY_REF:
        raise AcceptanceIntegrityError("registry acceptance-authority mismatch")
    material = _registry_material(
        acceptance_authority_ref=snapshot.acceptance_authority_ref,
        currentness_state=snapshot.currentness_state,
        adoption_current_selection_evidence_refs=snapshot.adoption_current_selection_evidence_refs,
        immutable_provenance=snapshot.immutable_provenance,
        entries=snapshot.entries,
    )
    h = _digest("REGISTRY", material)
    if snapshot.registry_ref != ContentAddressedRef(REGISTRY_ID, REGISTRY_VERSION, h):
        raise AcceptanceIntegrityError("registry snapshot content/hash mismatch")


def _validate_against_registry(r: AcceptanceReceipt, snapshot: AcceptanceRegistrySnapshot, *, required_currentness: str) -> AcceptanceReceipt:
    _validate_registry_snapshot_integrity(snapshot)
    if snapshot.currentness_state != required_currentness:
        raise AcceptanceMissingAuthority("registry is not current for required state")
    if required_currentness == CURRENT_ACCEPTED:
        if not snapshot.adoption_current_selection_evidence_refs:
            raise AcceptanceMissingAuthority("current registry lacks adoption/current-selection evidence")
        if not snapshot.immutable_provenance:
            raise AcceptanceMissingAuthority("current registry lacks immutable provenance")
    if r.acceptance_authority_ref != snapshot.acceptance_authority_ref or r.registry_ref != snapshot.registry_ref:
        raise AcceptanceIntegrityError("issuer/registry mismatch")
    matches = [
        e for e in snapshot.entries
        if _entry_matches_receipt(e, r) and r.registry_entry_ref == EvidenceRef(e.entry_id, e.entry_hash)
    ]
    if len(matches) != 1:
        raise AcceptanceMissingAuthority("no exact positive registry entry")
    e = matches[0]
    _check_entry_integrity(e)
    if required_currentness == CURRENT_ACCEPTED:
        if not e.immutable_provenance:
            raise AcceptanceMissingAuthority("current registry entry lacks immutable provenance")
        if e.source_acceptance_evidence_ref not in set(snapshot.adoption_current_selection_evidence_refs):
            raise AcceptanceMissingAuthority("entry source evidence is not selected by current registry")
    return r


def validate_acceptance_receipt(
    r: AcceptanceReceipt,
    *,
    expected_role: str,
    expected_accepted_authority_ref: ContentAddressedRef,
    expected_owner_jurisdiction_ref: EvidenceRef,
    expected_source_acceptance_evidence_ref: EvidenceRef,
    expected_scope: AcceptanceScope,
    required_currentness: str,
) -> AcceptanceReceipt:
    if not isinstance(r, AcceptanceReceipt):
        raise AcceptanceMissingAuthority("exact receipt required")
    _check_integrity(r)
    if r.role != expected_role or expected_role not in SUPPORTED_ROLES:
        raise AcceptanceOutOfScope("role mismatch")
    if r.consumer != CONSUMER:
        raise AcceptanceOutOfScope("consumer mismatch")
    if r.accepted_authority_ref != expected_accepted_authority_ref:
        raise AcceptanceOutOfScope("authority identity/version/hash mismatch")
    if r.accepted_authority_owner_jurisdiction_ref != expected_owner_jurisdiction_ref:
        raise AcceptanceOutOfScope("owner/jurisdiction mismatch")
    if r.source_acceptance_evidence_ref != expected_source_acceptance_evidence_ref:
        raise AcceptanceOutOfScope("source evidence mismatch")
    if r.scope != expected_scope:
        raise AcceptanceOutOfScope("transition/use/family/subject/object scope mismatch")
    if r.currentness_state != required_currentness:
        raise AcceptanceOutOfScope("currentness mismatch")
    if r.decision_state != ACCEPT:
        raise AcceptanceMissingAuthority("nonpositive")
    if required_currentness == CURRENT_ACCEPTED:
        return _validate_against_registry(r, _CURRENT_REGISTRY, required_currentness=CURRENT_ACCEPTED)
    if required_currentness != NONCURRENT_SYNTHETIC_TEST_ONLY:
        raise AcceptanceOutOfScope("unknown currentness")
    if r.acceptance_authority_ref != _SYNTH_AUTHORITY_REF or r.registry_ref != _SYNTH_REGISTRY_REF:
        raise AcceptanceIntegrityError("issuer/registry mismatch")
    matches = [e for e in _SYNTH_ENTRIES if _entry_matches_receipt(e, r)]
    if len(matches) != 1:
        raise AcceptanceMissingAuthority("no exact positive registry entry")
    e = matches[0]
    _check_entry_integrity(e)
    if r.registry_entry_ref != EvidenceRef(e.entry_id, e.entry_hash):
        raise AcceptanceIntegrityError("entry binding mismatch")
    return r


def _validate_contact_constituent(r: AcceptanceReceipt, expected_role: str) -> AcceptanceReceipt:
    if not isinstance(r, AcceptanceReceipt):
        raise AcceptanceMissingAuthority("exact receipt required")
    return validate_acceptance_receipt(
        r,
        expected_role=expected_role,
        expected_accepted_authority_ref=r.accepted_authority_ref,
        expected_owner_jurisdiction_ref=r.accepted_authority_owner_jurisdiction_ref,
        expected_source_acceptance_evidence_ref=r.source_acceptance_evidence_ref,
        expected_scope=r.scope,
        required_currentness=r.currentness_state,
    )


def validate_contact_acceptance_pair(o: AcceptanceReceipt, i: AcceptanceReceipt) -> tuple[AcceptanceReceipt, AcceptanceReceipt]:
    o = _validate_contact_constituent(o, CONTACT_OCCURRENCE_WITNESS)
    i = _validate_contact_constituent(i, CONTACT_WITNESS_INDEPENDENCE)
    if o.receipt_id == i.receipt_id or o.receipt_hash == i.receipt_hash:
        raise AcceptanceOutOfScope("contact occurrence and independence require distinct acceptance receipts")
    if o.accepted_authority_ref == i.accepted_authority_ref:
        raise AcceptanceOutOfScope("contact occurrence and independence require distinct accepted authorities")
    return o, i


def candidate_registry_artifact() -> dict[str, Any]:
    return {
        "schema_id": "GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY_ARTIFACT@1.0.0",
        "status": CANDIDATE_NOT_ADOPTED,
        "acceptance_authority_ref": asdict(ACCEPTANCE_AUTHORITY_REF),
        "registry_ref": asdict(REGISTRY_REF),
        "receipt_schema_id": RECEIPT_SCHEMA_ID,
        "consumer": CONSUMER,
        "supported_roles": list(SUPPORTED_ROLES),
        "current_positive_entries": [],
        "current_registry_state": _CURRENT_REGISTRY.currentness_state,
        "future_current_contract": {
            "representable": True,
            "requires_exact_governed_registry_membership": True,
            "requires_adoption_current_selection_evidence": True,
            "requires_immutable_entry_provenance": True,
            "requires_immutable_registry_provenance": True,
            "no_latest_default_fuzzy_fallback": True,
            "caller_receipt_cannot_install_registry_membership": True,
        },
        "authority_ceiling": list(AUTHORITY_CEILING),
        "positive_fallback": False,
        "generic_project_wide_authority": False,
    }


def receipt_schema_artifact() -> dict[str, Any]:
    return {
        "schema_id": RECEIPT_SCHEMA_ID,
        "required_fields": [
            "acceptance_authority_ref", "registry_ref", "registry_entry_ref", "role",
            "accepted_authority_ref", "accepted_authority_owner_jurisdiction_ref",
            "source_acceptance_evidence_ref", "decision_state", "consumer",
            "scope.transition_use_scope", "scope.family_scope", "scope.subject_scope",
            "scope.object_scope", "negative_limit_refs", "currentness_state",
            "immutable_provenance", "receipt_id", "receipt_hash",
        ],
        "positive_decision_state": ACCEPT,
        "current_positive_requires_separate_adoption": True,
        "current_positive_requires_exact_registry_membership": True,
        "current_entry_requires_immutable_provenance": True,
        "current_registry_requires_adoption_current_selection_evidence": True,
        "contact_pair_validates_constituents_first": True,
        "synthetic_currentness": NONCURRENT_SYNTHETIC_TEST_ONLY,
    }
