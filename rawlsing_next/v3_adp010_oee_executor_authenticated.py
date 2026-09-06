"""GT3/GT4 W2 successor ADP-010 bounded OEE executor.

Distinct candidate successor to historical S3.  Historical S3 remains immutable
at semantic candidate 5bed04b83f0dc61e500da26130892e46ce9c86ff and module
blob cd6e978eea25384482ef2ab75547b8d33bcc4fb7.

This module preserves only deterministic BASIS->AVAILABLE->OPPORTUNITY->
ENCOUNTER semantics.  It adds authentication and reconstructible replay
bindings required by the T3 hostile audit.  It never materializes a subject,
classifies a subject, infers contact from proximity, creates EXPOSURE, mutates
actor state, or creates comparator/PSEPF/metabolism/CAN-008/V2 authority.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from hashlib import sha1, sha256
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

EXECUTOR_ID = "GT34_V3P5_ADP010_AUTHENTICATED_REPLAY_EXECUTOR"
EXECUTOR_VERSION = "2.0.0"
HISTORICAL_S3_SEMANTIC_CANDIDATE_SHA = "5bed04b83f0dc61e500da26130892e46ce9c86ff"
HISTORICAL_S3_EVIDENCE_EXECUTION_SHA = "c70808c993b7e236e5535a03e22fe89cc3759d1e"
HISTORICAL_S3_MODULE_BLOB_SHA = "cd6e978eea25384482ef2ab75547b8d33bcc4fb7"
HISTORICAL_S3_TEST_BLOB_SHA = "0d29a69e9f88beb72ebfb4ddb85bdb5c40fc74d5"

ADP010_AUTHORITY_ID = "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE"
ADP010_AUTHORITY_VERSION = "1.0.0"
ADP010_REGISTRY_ID = "V3_OEE_REALIZATION_RULE_REGISTRY"
ADP010_REGISTRY_VERSION = "1.0.0"
ADP010_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.json"
ADP010_AUTHORITY_ARTIFACT_BLOB_SHA = "0eac41d081b112255dcfc6dd42a6afab15a2928b"

ADP008_AUTHORITY_ID = "V3_DEVELOPMENTAL_PHASE_RULE"
ADP008_AUTHORITY_VERSION = "1.1.0"
ADP008_REGISTRY_ID = "V3_DEVELOPMENTAL_PHASE_REGISTRY"
ADP008_REGISTRY_VERSION = "1.1.0"
ADP008_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_008_V3_DEVELOPMENTAL_PHASE/AUTHORITY.json"
ADP008_AUTHORITY_ARTIFACT_BLOB_SHA = "c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6"

ADP020_AUTHORITY_ID = "ADP-020"
ADP020_AUTHORITY_VERSION = "1.0.0"
ADP020_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG/AUTHORITY.json"
ADP020_AUTHORITY_ARTIFACT_BLOB_SHA = "1f13dc7ccc69bda562613d6215acc996a9c092e4"

OBL054_ADOPTION_ARTIFACT_BLOB = "fc46d377dafa5b2c4e274d702e7f26268aa429cb"
OBL054_MATERIALIZER_ID = "GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER"
OBL054_MATERIALIZER_VERSION = "2.0.0"
OBL054_ACCEPTED_ROOT_HASH = "1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8"
OBL054_PERMIT_HASH = "3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc"
OBL054_PERMIT_ID = "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:" + OBL054_PERMIT_HASH
OBL053_ADOPTION_ARTIFACT_BLOB = "f561765bad4fdad2bbf4591f35fe7f81f8486428"
HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB = "286ff7b851e920ff2760082d8b2fb194560ab127"
OBL053_AUTHORITY_ID = "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY"
OBL053_AUTHORITY_VERSION = "1.0.0"
OBL053_AUTHORITY_HASH = "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
OBL053_SEMANTIC_OBJECT_ID = (
    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
    "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
)
OBL053_SEMANTIC_OBJECT_HASH = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"

MATERIALIZER_RECEIPT_SCHEMA = "V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_RECEIPT@2.0.0"
MATERIALIZER_SUBJECT_REF_SCHEME = "RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1"
MATERIALIZER_OWNER_BINDING_SCHEMA = "V3P1_OWNER_BOUND_SUBJECT_INGRESS_BINDING@1.0.0"
MATERIALIZER_SUBJECT_REF_DOMAIN = b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
MATERIALIZER_OWNER_BINDING_DOMAIN = b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
MATERIALIZER_RECEIPT_DOMAIN = b"RAWLSING\0GT34-U2\0V3P1-AUTHENTICATED-SUBJECT-RECEIPT-V2\0"

DEVELOPMENT_ACTIVE_PHASE = "V3DP_DEVELOPMENT_ACTIVE"
STATE_AVAILABLE, STATE_OPPORTUNITY, STATE_ENCOUNTER = "AVAILABLE", "OPPORTUNITY", "ENCOUNTER"
RULE_AVAILABLE = "OEE_CORE_AVAILABLE_BASIS_V1"
RULE_OPPORTUNITY = "OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1"
RULE_ENCOUNTER = "OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1"
RULE_VERSION = "V1"
EFFECT_OPPORTUNITY, EFFECT_ENCOUNTER = "OEE_OPPORTUNITY_ESTABLISHED", "OEE_ENCOUNTER_OCCURRED"
CONTACT_WITNESS_KIND = "CONTACT_OCCURRENCE_WITNESS"
CONTACT_INDEPENDENCE_KIND = "CONTACT_WITNESS_INDEPENDENCE"
CONTACT_OCCURRENCE_SEMANTIC = "CONTACT_OCCURRENCE"
EP_GENERATED_RUNTIME_FACT = "GENERATED_RUNTIME_FACT"
EP_RESOLVER_CONTEXT = "RESOLVER_DERIVED_CONTEXT"
EP_ADMITTED_CAUSAL_EVENT = "ADMITTED_CAUSAL_EVENT"
_ADMISSIBLE_EP = {EP_GENERATED_RUNTIME_FACT, EP_RESOLVER_CONTEXT, EP_ADMITTED_CAUSAL_EVENT}
_INSUFFICIENT_CONTACT = {
    "COLOCATION", "CO_LOCATION", "COPRESENCE", "CO_PRESENCE",
    "SAME_GEOGRAPHY_TIME", "SHARED_V555_ENDPOINT", "SAME_STRUCTURAL_TARGET",
    "SAME_INSTITUTION_CATEGORY", "SIMULTANEOUS_RESOLVER_SELECTION",
    "NARRATIVE_PLAUSIBILITY",
}
CURRENT_ACCEPTED = "CURRENT_ACCEPTED"
NONCURRENT_SYNTHETIC_TEST_ONLY = "NONCURRENT_SYNTHETIC_TEST_ONLY"

_HASH64 = re.compile(r"^[0-9a-f]{64}$")
_BLOB40 = re.compile(r"^[0-9a-f]{40}$")
_SUBJECT_URN = re.compile(r"^urn:rawlsing:v3:subject:sha256:([0-9a-f]{64})$")
_RECORD_DOMAIN = "RAWLSING\0ADP-010\0V3_OEE_REALIZATION_RECORD_V1\0"
_CANDIDATE_DOMAIN = "RAWLSING\0ADP-010\0OEE_CANDIDATE_AUTHENTICATED_REPLAY_V2\0"
_EVENT_DOMAIN = "RAWLSING\0ADP-010\0OEE_EVENT_V1\0"
_AUTH_BINDING_DOMAIN = "RAWLSING\0GT34-W2\0AUTHENTICATION_BINDING_V1\0"
_FIXED_PROVENANCE_DOMAIN = "RAWLSING\0GT34-W2\0FIXED_AUTHORITY_PROVENANCE_V1\0"

class OEEAdmissionError(ValueError):
    pass

class OEEIntegrityError(OEEAdmissionError):
    pass

@dataclass(frozen=True, slots=True)
class ExactRef:
    kind: str
    ref: str
    content_hash: str

@dataclass(frozen=True, slots=True)
class MaterializationReceiptContent:
    receipt_id: str
    receipt_hash: str
    subject_ref: str
    subject_ref_hash: str
    materializer_id: str
    materializer_version: str
    obl054_adoption_artifact_blob: str
    obl053_adoption_artifact_blob: str
    accepted_owner_root_hash: str
    materialization_permit_id: str
    materialization_permit_hash: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_hash: str
    semantic_object_ref: ExactRef
    owner_binding_content_hash: str
    evidence_refs: tuple[ExactRef, ...]
    provenance_refs: tuple[ExactRef, ...]
    replay_input_hash: str
    integrity_state: str
    semantic_owner_transfer: bool
    semantic_fields_interpreted: bool
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class CausalUsePermissionAuthentication:
    authority_id: str
    authority_version: str
    authority_content_hash: str
    authority_acceptance_ref: ExactRef
    permission_receipt_ref: ExactRef
    subject_ref: str
    semantic_object_hash: str
    materialization_receipt_ref: ExactRef
    scope: str
    provenance_refs: tuple[ExactRef, ...]
    authentication_ref: ExactRef
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class SubjectIngressEvidence:
    # Historical S3 positional surface retained; authentication extensions follow.
    subject_ref: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_content_hash: str
    semantic_object_hash: str
    materialization_receipt: ExactRef
    epistemic_class: str
    causal_use_permission: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    semantic_object_id: str | None = None
    materialization_receipt_content: MaterializationReceiptContent | None = None
    causal_use_authentication: CausalUsePermissionAuthentication | None = None
    ingress_authentication_ref: ExactRef | None = None
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class ActorPhaseEvidence:
    actor_id: str
    phase_state_ref: ExactRef
    phase_authority_id: str = ADP008_AUTHORITY_ID
    phase_authority_version: str = ADP008_AUTHORITY_VERSION
    phase_authority_artifact_blob_sha: str = ADP008_AUTHORITY_ARTIFACT_BLOB_SHA
    base_phase_id: str = DEVELOPMENT_ACTIVE_PHASE
    provenance_refs: tuple[ExactRef, ...] = ()
    phase_state_receipt_ref: ExactRef | None = None
    phase_registry_id: str = ADP008_REGISTRY_ID
    phase_registry_version: str = ADP008_REGISTRY_VERSION
    phase_registry_content_hash: str | None = None
    authentication_ref: ExactRef | None = None
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class PositiveApplicabilityReceipt:
    receipt: ExactRef
    authority_id: str
    authority_version: str
    authority_content_hash: str
    result: str
    provenance_refs: tuple[ExactRef, ...]
    authority_acceptance_ref: ExactRef | None = None
    authentication_ref: ExactRef | None = None
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class OpportunityBasisEvidence:
    basis_ref: ExactRef
    actor_id: str
    subject_ref: str
    applicability_receipts: tuple[PositiveApplicabilityReceipt, ...]
    context_or_world_receipt_refs: tuple[ExactRef, ...]
    position_or_other_constraint_refs: tuple[ExactRef, ...] = ()
    provenance_refs: tuple[ExactRef, ...] = ()

@dataclass(frozen=True, slots=True)
class ContactOccurrenceWitness:
    witness_ref: ExactRef
    witness_authority_id: str
    witness_authority_version: str
    witness_authority_content_hash: str
    actor_id: str
    subject_ref: str
    occurrence_time: str
    semantic: str
    independence_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    authority_acceptance_ref: ExactRef | None = None
    contact_basis_refs: tuple[ExactRef, ...] = ()
    authentication_ref: ExactRef | None = None
    independence_authority_id: str | None = None
    independence_authority_version: str | None = None
    independence_authority_content_hash: str | None = None
    independence_authority_acceptance_ref: ExactRef | None = None
    independence_receipt_ref: ExactRef | None = None
    independence_basis_refs: tuple[ExactRef, ...] = ()
    independence_authentication_ref: ExactRef | None = None
    currentness_state: str = CURRENT_ACCEPTED

@dataclass(frozen=True, slots=True)
class V3OEERealizationRecord:
    record_id: str
    actor_id: str
    authority_id: str
    authority_version: str
    registry_id: str
    registry_version: str
    rule_id: str
    rule_version: str
    realization_state: str
    subject_ref: str
    parent_record_id: str | None
    effective_from: str
    effective_until: str
    time_granularity: str
    source_candidate_id: str
    source_candidate_replay_hash: str
    context_or_world_receipt_refs: tuple[ExactRef, ...]
    applicability_receipt_refs: tuple[ExactRef, ...]
    phase_state_ref: ExactRef
    position_or_other_constraint_refs: tuple[ExactRef, ...]
    causal_witness_refs: tuple[ExactRef, ...]
    rng_decision_receipt_ref: ExactRef | None
    event_id: str | None
    event_effect_kind: str | None
    prior_ledger_anchor_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    record_hash: str

@dataclass(frozen=True, slots=True)
class OEEExecutionResult:
    record: V3OEERealizationRecord

_RULES = {
    STATE_AVAILABLE: (RULE_AVAILABLE, "BASIS_TO_AVAILABLE", None, None),
    STATE_OPPORTUNITY: (RULE_OPPORTUNITY, "AVAILABLE_TO_OPPORTUNITY", STATE_AVAILABLE, EFFECT_OPPORTUNITY),
    STATE_ENCOUNTER: (RULE_ENCOUNTER, "OPPORTUNITY_TO_ENCOUNTER", STATE_OPPORTUNITY, EFFECT_ENCOUNTER),
}

def _s(v: Any, n: str) -> str:
    if not isinstance(v, str):
        raise OEEIntegrityError(f"{n} must be non-empty string")
    out = unicodedata.normalize("NFC", v.strip())
    if not out:
        raise OEEIntegrityError(f"{n} must be non-empty string")
    return out

def _h(v: Any, n: str) -> str:
    v = _s(v, n)
    if not _HASH64.fullmatch(v):
        raise OEEIntegrityError(f"{n} must be lowercase SHA-256 hex")
    return v

def _blob(v: Any, n: str) -> str:
    v = _s(v, n)
    if not _BLOB40.fullmatch(v):
        raise OEEIntegrityError(f"{n} must be lowercase Git SHA-1 hex")
    return v

def _ref(v: Any, n: str) -> ExactRef:
    if not isinstance(v, ExactRef):
        raise OEEIntegrityError(f"{n} must be ExactRef")
    _s(v.kind, n + ".kind")
    _s(v.ref, n + ".ref")
    _h(v.content_hash, n + ".content_hash")
    return v

def _refs(xs: Iterable[ExactRef], n: str, required: bool = False) -> tuple[ExactRef, ...]:
    xs = tuple(xs)
    if required and not xs:
        raise OEEIntegrityError(f"{n} must be non-empty")
    validated = tuple(_ref(x, n) for x in xs)
    keyed = {(x.kind, x.ref, x.content_hash): x for x in validated}
    return tuple(keyed[k] for k in sorted(keyed))

def _merge(*groups: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return _refs((x for g in groups for x in g), "refs", True)

def _time(v: Any, n: str) -> str:
    raw = _s(v, n)
    p = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        dt = datetime.fromisoformat(p)
    except ValueError as e:
        raise OEEIntegrityError(f"{n} must be ISO-8601") from e
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise OEEIntegrityError(f"{n} must be timezone-aware")
    return dt.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

def _dt(v: str) -> datetime:
    return datetime.fromisoformat(v[:-1] + "+00:00")

def _interval(a: Any, b: Any) -> tuple[str, str]:
    a, b = _time(a, "effective_from"), _time(b, "effective_until")
    if _dt(b) < _dt(a):
        raise OEEIntegrityError("effective_until precedes effective_from")
    return a, b

def _norm(v: Any) -> Any:
    if isinstance(v, ExactRef):
        return {"kind": v.kind, "ref": v.ref, "content_hash": _h(v.content_hash, "content_hash")}
    if isinstance(v, Mapping):
        return {str(k): _norm(x) for k, x in v.items()}
    if isinstance(v, (tuple, list)):
        return [_norm(x) for x in v]
    if isinstance(v, str):
        return unicodedata.normalize("NFC", v)
    return v

def _canonical_json(v: Any) -> str:
    return json.dumps(_norm(v), sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _digest(domain: str, v: Any) -> str:
    return sha256((domain + _canonical_json(v)).encode("utf-8")).hexdigest()

def _digest_bytes(domain: bytes, v: Any) -> str:
    return sha256(domain + json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()

def _content_ref(kind: str, prefix: str, material: Any, *, domain: str = _AUTH_BINDING_DOMAIN) -> ExactRef:
    digest = _digest(domain, material)
    return ExactRef(kind, prefix + digest, digest)

def _validate_content_addressed_ref(ref: ExactRef, n: str, kind: str, prefix: str) -> ExactRef:
    r = _ref(ref, n)
    if r.kind != kind:
        raise OEEIntegrityError(f"{n} kind mismatch")
    if r.ref != prefix + r.content_hash:
        raise OEEIntegrityError(f"{n} is not content-addressed")
    return r

def _fixed_ref(kind: str, ref: str, material: Any) -> ExactRef:
    return ExactRef(kind, ref, _digest(_FIXED_PROVENANCE_DOMAIN, material))

ADP010_AUTHORITY_HASH_REF = _fixed_ref(
    "ADP010_AUTHORITY_HASH",
    f"urn:rawlsing:authority-artifact:git-blob:{ADP010_AUTHORITY_ARTIFACT_BLOB_SHA}",
    [ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION, ADP010_AUTHORITY_ARTIFACT_BLOB_SHA],
)
ADP010_REGISTRY_HASH_REF = _fixed_ref(
    "ADP010_REGISTRY_HASH",
    f"urn:rawlsing:registry:{ADP010_REGISTRY_ID}@{ADP010_REGISTRY_VERSION}",
    [ADP010_REGISTRY_ID, ADP010_REGISTRY_VERSION, ADP010_AUTHORITY_ARTIFACT_BLOB_SHA],
)
ADP008_AUTHORITY_HASH_REF = _fixed_ref(
    "ADP008_AUTHORITY_HASH",
    f"urn:rawlsing:authority-artifact:git-blob:{ADP008_AUTHORITY_ARTIFACT_BLOB_SHA}",
    [ADP008_AUTHORITY_ID, ADP008_AUTHORITY_VERSION, ADP008_AUTHORITY_ARTIFACT_BLOB_SHA],
)
ADP008_REGISTRY_CONTENT_HASH = _digest(
    _FIXED_PROVENANCE_DOMAIN,
    [ADP008_REGISTRY_ID, ADP008_REGISTRY_VERSION, ADP008_AUTHORITY_ARTIFACT_BLOB_SHA],
)
ADP008_REGISTRY_HASH_REF = ExactRef(
    "ADP008_REGISTRY_HASH",
    f"urn:rawlsing:registry:{ADP008_REGISTRY_ID}@{ADP008_REGISTRY_VERSION}",
    ADP008_REGISTRY_CONTENT_HASH,
)
ADP020_AUTHORITY_HASH_REF = _fixed_ref(
    "ADP020_AUTHORITY_HASH",
    f"urn:rawlsing:authority-artifact:git-blob:{ADP020_AUTHORITY_ARTIFACT_BLOB_SHA}",
    [ADP020_AUTHORITY_ID, ADP020_AUTHORITY_VERSION, ADP020_AUTHORITY_ARTIFACT_BLOB_SHA],
)

def _rule_hash_ref(state: str) -> ExactRef:
    rule_id = _RULES[state][0]
    return _fixed_ref(
        "ADP010_RULE_HASH",
        f"urn:rawlsing:adp010:rule:{rule_id}@{RULE_VERSION}",
        [
            ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION,
            ADP010_REGISTRY_ID, ADP010_REGISTRY_VERSION,
            ADP010_AUTHORITY_ARTIFACT_BLOB_SHA, rule_id, RULE_VERSION,
        ],
    )

def _required_fixed_provenance(state: str) -> tuple[ExactRef, ...]:
    return _refs(
        (
            ADP010_AUTHORITY_HASH_REF,
            ADP010_REGISTRY_HASH_REF,
            _rule_hash_ref(state),
            ADP008_AUTHORITY_HASH_REF,
            ADP008_REGISTRY_HASH_REF,
            ADP020_AUTHORITY_HASH_REF,
        ),
        "fixed provenance",
        True,
    )

def _mat_ref_dict(ref: ExactRef) -> dict[str, str]:
    r = _ref(ref, "semantic_object_ref")
    return {"kind": r.kind, "ref_id": r.ref, "sha256": r.content_hash}

def _materializer_owner_material(m: MaterializationReceiptContent) -> dict[str, Any]:
    return {
        "schema_id": MATERIALIZER_OWNER_BINDING_SCHEMA,
        "semantic_owner_authority": {
            "id": m.semantic_owner_authority_id,
            "version": m.semantic_owner_authority_version,
            "content_hash": m.semantic_owner_authority_hash,
        },
        "semantic_object_ref": _mat_ref_dict(m.semantic_object_ref),
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materialization evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materialization provenance", True)],
    }

def _materializer_subject_identity_material(m: MaterializationReceiptContent) -> dict[str, Any]:
    return {
        "scheme": MATERIALIZER_SUBJECT_REF_SCHEME,
        "semantic_owner_authority": {
            "id": m.semantic_owner_authority_id,
            "version": m.semantic_owner_authority_version,
            "content_hash": m.semantic_owner_authority_hash,
        },
        "semantic_object_ref": _mat_ref_dict(m.semantic_object_ref),
        "owner_binding_content_hash": m.owner_binding_content_hash,
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materialization evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materialization provenance", True)],
    }

def _materializer_receipt_body(m: MaterializationReceiptContent) -> dict[str, Any]:
    return {
        "schema_id": MATERIALIZER_RECEIPT_SCHEMA,
        "subject_ref": m.subject_ref,
        "subject_ref_hash": m.subject_ref_hash,
        "materializer_id": m.materializer_id,
        "materializer_version": m.materializer_version,
        "adoption_artifact_blob": m.obl053_adoption_artifact_blob,
        "accepted_owner_root_hash": m.accepted_owner_root_hash,
        "materialization_permit_id": m.materialization_permit_id,
        "materialization_permit_hash": m.materialization_permit_hash,
        "semantic_owner_authority": {
            "id": m.semantic_owner_authority_id,
            "version": m.semantic_owner_authority_version,
            "content_hash": m.semantic_owner_authority_hash,
        },
        "semantic_object_ref": _mat_ref_dict(m.semantic_object_ref),
        "owner_binding_content_hash": m.owner_binding_content_hash,
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materialization evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materialization provenance", True)],
        "replay_input_hash": m.replay_input_hash,
        "integrity_state": m.integrity_state,
        "semantic_owner_transfer": m.semantic_owner_transfer,
        "semantic_fields_interpreted": m.semantic_fields_interpreted,
    }

def _validate_currentness(value: str, *, allow_noncurrent: bool, n: str) -> str:
    value = _s(value, n)
    if allow_noncurrent:
        if value != NONCURRENT_SYNTHETIC_TEST_ONLY:
            raise OEEAdmissionError(f"{n} must be NONCURRENT_SYNTHETIC_TEST_ONLY in synthetic court")
    elif value != CURRENT_ACCEPTED:
        raise OEEAdmissionError(f"{n} must be CURRENT_ACCEPTED")
    return value

def _validate_materialization_receipt(
    m: MaterializationReceiptContent,
    *,
    allow_noncurrent: bool,
) -> MaterializationReceiptContent:
    if not isinstance(m, MaterializationReceiptContent):
        raise OEEIntegrityError("materialization receipt content is required")
    _validate_currentness(m.currentness_state, allow_noncurrent=allow_noncurrent, n="materialization currentness")
    _s(m.receipt_id, "materialization receipt id")
    _h(m.receipt_hash, "materialization receipt hash")
    _s(m.subject_ref, "materialization subject_ref")
    _h(m.subject_ref_hash, "materialization subject_ref_hash")
    _s(m.materializer_id, "materializer id")
    _s(m.materializer_version, "materializer version")
    _blob(m.obl054_adoption_artifact_blob, "OBL054 adoption artifact blob")
    _blob(m.obl053_adoption_artifact_blob, "OBL053 adoption artifact blob")
    _h(m.accepted_owner_root_hash, "accepted owner root hash")
    _s(m.materialization_permit_id, "materialization permit id")
    _h(m.materialization_permit_hash, "materialization permit hash")
    _s(m.semantic_owner_authority_id, "semantic owner id")
    _s(m.semantic_owner_authority_version, "semantic owner version")
    _h(m.semantic_owner_authority_hash, "semantic owner hash")
    _ref(m.semantic_object_ref, "semantic object ref")
    _h(m.owner_binding_content_hash, "owner binding hash")
    _refs(m.evidence_refs, "materialization evidence", True)
    _refs(m.provenance_refs, "materialization provenance", True)
    _h(m.replay_input_hash, "materialization replay input hash")
    _s(m.integrity_state, "materialization integrity state")
    if m.semantic_owner_transfer is not False or m.semantic_fields_interpreted is not False:
        raise OEEAdmissionError("materializer semantic opacity/owner preservation violated")

    if not allow_noncurrent:
        expected = (
            OBL054_MATERIALIZER_ID,
            OBL054_MATERIALIZER_VERSION,
            OBL054_ADOPTION_ARTIFACT_BLOB,
            OBL053_ADOPTION_ARTIFACT_BLOB,
            OBL054_ACCEPTED_ROOT_HASH,
            OBL054_PERMIT_ID,
            OBL054_PERMIT_HASH,
            OBL053_AUTHORITY_ID,
            OBL053_AUTHORITY_VERSION,
            OBL053_AUTHORITY_HASH,
            OBL053_SEMANTIC_OBJECT_ID,
            OBL053_SEMANTIC_OBJECT_HASH,
        )
        actual = (
            m.materializer_id,
            m.materializer_version,
            m.obl054_adoption_artifact_blob,
            m.obl053_adoption_artifact_blob,
            m.accepted_owner_root_hash,
            m.materialization_permit_id,
            m.materialization_permit_hash,
            m.semantic_owner_authority_id,
            m.semantic_owner_authority_version,
            m.semantic_owner_authority_hash,
            m.semantic_object_ref.ref,
            m.semantic_object_ref.content_hash,
        )
        if actual != expected:
            raise OEEAdmissionError("subject ingress is not bound to exact adopted OBL054/current OBL053 root")
        if m.integrity_state != "AUTHENTICATED_FRESH_OBL053_ROOT__OWNER_BOUND_INPUT_VERIFIED":
            raise OEEAdmissionError("materialization receipt integrity state is not current")
    else:
        if m.materializer_id == OBL054_MATERIALIZER_ID and m.obl054_adoption_artifact_blob == OBL054_ADOPTION_ARTIFACT_BLOB:
            raise OEEAdmissionError("noncurrent synthetic fixture may not masquerade as current OBL054")

    expected_owner_binding = _digest_bytes(
        MATERIALIZER_OWNER_BINDING_DOMAIN,
        _materializer_owner_material(m),
    )
    if m.owner_binding_content_hash != expected_owner_binding:
        raise OEEIntegrityError("materialization owner binding hash mismatch")
    subject_material = _materializer_subject_identity_material(m)
    expected_subject_hash = _digest_bytes(MATERIALIZER_SUBJECT_REF_DOMAIN, subject_material)
    if m.subject_ref_hash != expected_subject_hash:
        raise OEEIntegrityError("materialization subject_ref_hash mismatch")
    if not allow_noncurrent:
        if m.subject_ref != f"urn:rawlsing:v3:subject:sha256:{expected_subject_hash}":
            raise OEEIntegrityError("materialization subject_ref identity mismatch")
    expected_replay = sha256(
        json.dumps(subject_material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    if m.replay_input_hash != expected_replay:
        raise OEEIntegrityError("materialization replay_input_hash mismatch")
    expected_receipt_hash = _digest_bytes(MATERIALIZER_RECEIPT_DOMAIN, _materializer_receipt_body(m))
    if m.receipt_hash != expected_receipt_hash:
        raise OEEIntegrityError("materialization receipt hash mismatch")
    if not m.receipt_id.endswith(m.receipt_hash):
        raise OEEIntegrityError("materialization receipt id/hash mismatch")
    return m

def _causal_use_material(c: CausalUsePermissionAuthentication, permission_ref: ExactRef) -> dict[str, Any]:
    return {
        "authority": [c.authority_id, c.authority_version, c.authority_content_hash],
        "authority_acceptance_ref": c.authority_acceptance_ref,
        "permission_ref": permission_ref,
        "permission_receipt_ref": c.permission_receipt_ref,
        "subject_ref": c.subject_ref,
        "semantic_object_hash": c.semantic_object_hash,
        "materialization_receipt_ref": c.materialization_receipt_ref,
        "scope": c.scope,
        "provenance_refs": _refs(c.provenance_refs, "causal use provenance", True),
        "currentness_state": c.currentness_state,
    }

def _validate_causal_use(
    c: CausalUsePermissionAuthentication,
    permission_ref: ExactRef,
    materialization_ref: ExactRef,
    subject_ref: str,
    semantic_object_hash: str,
    *,
    allow_noncurrent: bool,
) -> ExactRef:
    if not isinstance(c, CausalUsePermissionAuthentication):
        raise OEEIntegrityError("authenticated causal-use permission is required")
    _validate_currentness(c.currentness_state, allow_noncurrent=allow_noncurrent, n="causal use currentness")
    _s(c.authority_id, "causal use authority id")
    _s(c.authority_version, "causal use authority version")
    _h(c.authority_content_hash, "causal use authority hash")
    _validate_content_addressed_ref(
        c.authority_acceptance_ref,
        "causal use authority acceptance",
        "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT",
        "urn:rawlsing:accepted-causal-use-authority:sha256:",
    )
    _ref(permission_ref, "causal use permission")
    _ref(c.permission_receipt_ref, "causal use permission receipt")
    if (c.subject_ref, c.semantic_object_hash, c.materialization_receipt_ref) != (
        subject_ref, semantic_object_hash, materialization_ref
    ):
        raise OEEAdmissionError("causal-use permission does not bind exact subject/materialization/object")
    _s(c.scope, "causal use scope")
    _refs(c.provenance_refs, "causal use provenance", True)
    expected = _content_ref(
        "CAUSAL_USE_PERMISSION_AUTHENTICATION",
        "urn:rawlsing:causal-use-authentication:sha256:",
        _causal_use_material(c, permission_ref),
    )
    if c.authentication_ref != expected:
        raise OEEIntegrityError("causal-use authentication mismatch")
    return expected

def _subject_ingress_material(
    s: SubjectIngressEvidence,
    materialization: MaterializationReceiptContent,
    causal_auth_ref: ExactRef,
) -> dict[str, Any]:
    return {
        "subject_ref": s.subject_ref,
        "semantic_owner_authority": [
            s.semantic_owner_authority_id,
            s.semantic_owner_authority_version,
            s.semantic_owner_authority_content_hash,
        ],
        "semantic_object": [s.semantic_object_id, s.semantic_object_hash],
        "materialization_receipt_ref": s.materialization_receipt,
        "materialization_receipt_wire": _materializer_receipt_body(materialization),
        "materialization_receipt_id": materialization.receipt_id,
        "materialization_receipt_hash": materialization.receipt_hash,
        "obl054_adoption_artifact_blob": materialization.obl054_adoption_artifact_blob,
        "accepted_owner_root_hash": materialization.accepted_owner_root_hash,
        "materialization_permit": [
            materialization.materialization_permit_id,
            materialization.materialization_permit_hash,
        ],
        "causal_use_permission": s.causal_use_permission,
        "causal_use_authentication_ref": causal_auth_ref,
        "epistemic_class": s.epistemic_class,
        "provenance_refs": _refs(s.provenance_refs, "subject provenance", True),
        "currentness_state": s.currentness_state,
    }

def _legacy_fixture_auth_ref(kind: str, material: Any) -> ExactRef:
    prefixes = {
        "SUBJECT_INGRESS_AUTHENTICATION": "urn:rawlsing:subject-ingress-authentication:sha256:",
        "ADP008_PHASE_STATE_AUTHENTICATION": "urn:rawlsing:adp008-phase-authentication:sha256:",
        "POSITIVE_APPLICABILITY_AUTHENTICATION": "urn:rawlsing:positive-applicability-authentication:sha256:",
        "CONTACT_OCCURRENCE_AUTHENTICATION": "urn:rawlsing:contact-occurrence-authentication:sha256:",
        "CONTACT_INDEPENDENCE_AUTHENTICATION": "urn:rawlsing:contact-independence-authentication:sha256:",
    }
    try:
        prefix = prefixes[kind]
    except KeyError as exc:
        raise OEEIntegrityError("unsupported legacy compatibility authentication kind") from exc
    return _content_ref(kind, prefix, material)

def _legacy_subject_auth(s: SubjectIngressEvidence) -> ExactRef:
    if (
        s.semantic_owner_authority_id != "SYNTHETIC_EXACT_SUBJECT_OWNER"
        or s.semantic_owner_authority_version != "1.0.0"
        or s.semantic_owner_authority_content_hash != sha256(b"owner").hexdigest()
        or s.materialization_receipt.kind != "SUBJECT_MATERIALIZATION_RECEIPT"
        or s.causal_use_permission.kind != "CAUSAL_USE_PERMISSION"
    ):
        raise OEEAdmissionError("legacy synthetic subject fixture is not trusted by W2 compatibility court")
    return _legacy_fixture_auth_ref(
        "SUBJECT_INGRESS_AUTHENTICATION",
        [
            s.subject_ref, s.semantic_owner_authority_id, s.semantic_owner_authority_version,
            s.semantic_owner_authority_content_hash, s.semantic_object_hash,
            s.materialization_receipt, s.causal_use_permission,
            _refs(s.provenance_refs, "subject provenance", True),
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ],
    )

def _validate_subject(
    s: Any,
    *,
    allow_noncurrent: bool,
    allow_legacy: bool,
) -> tuple[SubjectIngressEvidence, ExactRef]:
    if not isinstance(s, SubjectIngressEvidence):
        raise OEEIntegrityError("subject must be SubjectIngressEvidence")
    _s(s.subject_ref, "subject_ref")
    _s(s.semantic_owner_authority_id, "semantic_owner_authority_id")
    _s(s.semantic_owner_authority_version, "semantic_owner_authority_version")
    _h(s.semantic_owner_authority_content_hash, "semantic_owner_authority_content_hash")
    _h(s.semantic_object_hash, "semantic_object_hash")
    materialization_ref = _ref(s.materialization_receipt, "materialization_receipt")
    permission_ref = _ref(s.causal_use_permission, "causal_use_permission")
    _refs(s.provenance_refs, "subject.provenance_refs", True)
    if s.epistemic_class not in _ADMISSIBLE_EP:
        raise OEEAdmissionError("subject basis epistemic class is not ADP-010-admissible")

    if allow_legacy and s.materialization_receipt_content is None:
        return s, _legacy_subject_auth(s)

    _validate_currentness(s.currentness_state, allow_noncurrent=allow_noncurrent, n="subject ingress currentness")
    if s.semantic_object_id is None:
        raise OEEIntegrityError("semantic_object_id is required")
    m = _validate_materialization_receipt(
        s.materialization_receipt_content,
        allow_noncurrent=allow_noncurrent,
    )
    expected_mat_ref = ExactRef(
        "SUBJECT_MATERIALIZATION_RECEIPT",
        m.receipt_id,
        m.receipt_hash,
    )
    if materialization_ref != expected_mat_ref:
        raise OEEIntegrityError("materialization receipt ref/content mismatch")
    if (
        s.subject_ref,
        s.semantic_owner_authority_id,
        s.semantic_owner_authority_version,
        s.semantic_owner_authority_content_hash,
        s.semantic_object_id,
        s.semantic_object_hash,
    ) != (
        m.subject_ref,
        m.semantic_owner_authority_id,
        m.semantic_owner_authority_version,
        m.semantic_owner_authority_hash,
        m.semantic_object_ref.ref,
        m.semantic_object_ref.content_hash,
    ):
        raise OEEAdmissionError("subject ingress fields do not match exact materialization receipt")
    causal_auth_ref = _validate_causal_use(
        s.causal_use_authentication,
        permission_ref,
        materialization_ref,
        s.subject_ref,
        s.semantic_object_hash,
        allow_noncurrent=allow_noncurrent,
    )
    expected_ingress = _content_ref(
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
        _subject_ingress_material(s, m, causal_auth_ref),
    )
    if s.ingress_authentication_ref != expected_ingress:
        raise OEEIntegrityError("subject ingress authentication mismatch")
    return s, expected_ingress

def _phase_material(a: ActorPhaseEvidence) -> dict[str, Any]:
    return {
        "actor_id": a.actor_id,
        "phase_state_ref": a.phase_state_ref,
        "phase_state_receipt_ref": a.phase_state_receipt_ref,
        "phase_authority": [
            a.phase_authority_id,
            a.phase_authority_version,
            a.phase_authority_artifact_blob_sha,
        ],
        "phase_registry": [
            a.phase_registry_id,
            a.phase_registry_version,
            a.phase_registry_content_hash,
        ],
        "base_phase_id": a.base_phase_id,
        "provenance_refs": _refs(a.provenance_refs, "actor provenance", True),
        "currentness_state": a.currentness_state,
    }

def _legacy_phase_auth(a: ActorPhaseEvidence) -> ExactRef:
    return _legacy_fixture_auth_ref(
        "ADP008_PHASE_STATE_AUTHENTICATION",
        [
            a.actor_id, a.phase_state_ref,
            a.phase_authority_id, a.phase_authority_version, a.phase_authority_artifact_blob_sha,
            a.base_phase_id, _refs(a.provenance_refs, "actor provenance", True),
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ],
    )

def _validate_actor(
    a: Any,
    *,
    allow_noncurrent: bool,
    allow_legacy: bool,
) -> tuple[ActorPhaseEvidence, ExactRef]:
    if not isinstance(a, ActorPhaseEvidence):
        raise OEEIntegrityError("actor must be ActorPhaseEvidence")
    _s(a.actor_id, "actor_id")
    r = _ref(a.phase_state_ref, "phase_state_ref")
    if r.kind != "V3DevelopmentalPhaseState":
        raise OEEAdmissionError("phase_state_ref must be V3DevelopmentalPhaseState")
    if (
        a.phase_authority_id,
        a.phase_authority_version,
        a.phase_authority_artifact_blob_sha,
        a.phase_registry_id,
        a.phase_registry_version,
    ) != (
        ADP008_AUTHORITY_ID,
        ADP008_AUTHORITY_VERSION,
        ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
        ADP008_REGISTRY_ID,
        ADP008_REGISTRY_VERSION,
    ):
        raise OEEAdmissionError("wrong ADP-008 authority/registry binding")
    _blob(a.phase_authority_artifact_blob_sha, "phase authority blob")
    if a.base_phase_id != DEVELOPMENT_ACTIVE_PHASE:
        raise OEEAdmissionError("V3DP_DEVELOPMENT_ACTIVE is required")
    _refs(a.provenance_refs, "actor.provenance_refs", True)

    if allow_legacy and a.phase_state_receipt_ref is None:
        return a, _legacy_phase_auth(a)

    _validate_currentness(a.currentness_state, allow_noncurrent=allow_noncurrent, n="phase currentness")
    _ref(a.phase_state_receipt_ref, "phase state receipt")
    if a.phase_registry_content_hash != ADP008_REGISTRY_CONTENT_HASH:
        raise OEEAdmissionError("ADP-008 phase registry content hash mismatch")
    expected = _content_ref(
        "ADP008_PHASE_STATE_AUTHENTICATION",
        "urn:rawlsing:adp008-phase-authentication:sha256:",
        _phase_material(a),
    )
    if a.authentication_ref != expected:
        raise OEEIntegrityError("ADP-008 phase-state authentication mismatch")
    return a, expected

def _app_material(x: PositiveApplicabilityReceipt) -> dict[str, Any]:
    return {
        "receipt": x.receipt,
        "authority": [x.authority_id, x.authority_version, x.authority_content_hash],
        "authority_acceptance_ref": x.authority_acceptance_ref,
        "result": x.result,
        "provenance_refs": _refs(x.provenance_refs, "applicability provenance", True),
        "currentness_state": x.currentness_state,
    }

def _legacy_app_auth(x: PositiveApplicabilityReceipt) -> ExactRef:
    if (
        x.authority_id != "SYNTHETIC_APPLICABILITY_OWNER"
        or x.authority_version != "1.0.0"
        or x.authority_content_hash != sha256(b"app-owner").hexdigest()
    ):
        raise OEEAdmissionError("legacy synthetic applicability owner is not trusted by W2 compatibility court")
    return _legacy_fixture_auth_ref("POSITIVE_APPLICABILITY_AUTHENTICATION", _app_material(x))

def _validate_app(
    x: Any,
    *,
    allow_noncurrent: bool,
    allow_legacy: bool,
) -> tuple[ExactRef, ExactRef]:
    if not isinstance(x, PositiveApplicabilityReceipt) or x.result != "POSITIVE":
        raise OEEAdmissionError("opportunity requires positive applicability")
    _ref(x.receipt, "applicability receipt")
    _s(x.authority_id, "applicability authority")
    _s(x.authority_version, "applicability version")
    _h(x.authority_content_hash, "applicability authority hash")
    _refs(x.provenance_refs, "applicability provenance", True)

    if allow_legacy and x.authentication_ref is None:
        return x.receipt, _legacy_app_auth(x)

    _validate_currentness(x.currentness_state, allow_noncurrent=allow_noncurrent, n="applicability currentness")
    _validate_content_addressed_ref(
        x.authority_acceptance_ref,
        "applicability authority acceptance",
        "ACCEPTED_APPLICABILITY_AUTHORITY_RECEIPT",
        "urn:rawlsing:accepted-applicability-authority:sha256:",
    )
    expected = _content_ref(
        "POSITIVE_APPLICABILITY_AUTHENTICATION",
        "urn:rawlsing:positive-applicability-authentication:sha256:",
        _app_material(x),
    )
    if x.authentication_ref != expected:
        raise OEEIntegrityError("positive applicability authentication mismatch")
    return x.receipt, expected

def _contact_material(w: ContactOccurrenceWitness) -> dict[str, Any]:
    return {
        "witness_ref": w.witness_ref,
        "witness_authority": [
            w.witness_authority_id,
            w.witness_authority_version,
            w.witness_authority_content_hash,
        ],
        "authority_acceptance_ref": w.authority_acceptance_ref,
        "actor_id": w.actor_id,
        "subject_ref": w.subject_ref,
        "occurrence_time": _time(w.occurrence_time, "contact occurrence time"),
        "semantic": w.semantic,
        "contact_basis_refs": _refs(w.contact_basis_refs, "contact basis", True),
        "provenance_refs": _refs(w.provenance_refs, "witness provenance", True),
        "currentness_state": w.currentness_state,
    }

def _independence_material(w: ContactOccurrenceWitness, contact_auth: ExactRef) -> dict[str, Any]:
    return {
        "contact_authentication_ref": contact_auth,
        "independence_ref": w.independence_ref,
        "independence_authority": [
            w.independence_authority_id,
            w.independence_authority_version,
            w.independence_authority_content_hash,
        ],
        "independence_authority_acceptance_ref": w.independence_authority_acceptance_ref,
        "independence_receipt_ref": w.independence_receipt_ref,
        "independence_basis_refs": _refs(w.independence_basis_refs, "independence basis", True),
        "currentness_state": w.currentness_state,
    }

def _legacy_contact_auth(w: ContactOccurrenceWitness) -> tuple[ExactRef, ExactRef]:
    if (
        w.witness_authority_id != "SYNTHETIC_CONTACT_OCCURRENCE_OWNER"
        or w.witness_authority_version != "1.0.0"
        or w.witness_authority_content_hash != sha256(b"contact-owner").hexdigest()
    ):
        raise OEEAdmissionError("legacy synthetic contact owner is not trusted by W2 compatibility court")
    contact_auth = _legacy_fixture_auth_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        [
            w.witness_ref, w.witness_authority_id, w.witness_authority_version,
            w.witness_authority_content_hash, w.actor_id, w.subject_ref,
            _time(w.occurrence_time, "contact occurrence time"), w.semantic,
            _refs(w.provenance_refs, "witness provenance", True),
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ],
    )
    independence_auth = _legacy_fixture_auth_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        [contact_auth, w.independence_ref, NONCURRENT_SYNTHETIC_TEST_ONLY],
    )
    return contact_auth, independence_auth

def _validate_contact(
    w: Any,
    actor_id: str,
    subject_ref: str,
    effective_time: str,
    *,
    allow_noncurrent: bool,
    allow_legacy: bool,
) -> tuple[ContactOccurrenceWitness, ExactRef, ExactRef]:
    if not isinstance(w, ContactOccurrenceWitness):
        raise OEEAdmissionError("ENCOUNTER requires exact ContactOccurrenceWitness")
    wr = _ref(w.witness_ref, "contact witness")
    if wr.kind in _INSUFFICIENT_CONTACT:
        raise OEEAdmissionError("co-location/co-presence or structural proximity is insufficient for ENCOUNTER")
    if wr.kind != CONTACT_WITNESS_KIND:
        raise OEEAdmissionError("contact witness must be independently supplied contact-occurrence witness")
    if w.actor_id != actor_id or w.subject_ref != subject_ref:
        raise OEEAdmissionError("contact witness actor/subject mismatch")
    _s(w.witness_authority_id, "witness authority")
    _s(w.witness_authority_version, "witness authority version")
    _h(w.witness_authority_content_hash, "witness authority hash")
    if w.semantic != CONTACT_OCCURRENCE_SEMANTIC:
        raise OEEAdmissionError("contact witness does not assert CONTACT_OCCURRENCE")
    if _time(w.occurrence_time, "contact occurrence time") != effective_time:
        raise OEEAdmissionError("encounter time must equal contact occurrence time")
    ir = _ref(w.independence_ref, "independence ref")
    if ir.kind != CONTACT_INDEPENDENCE_KIND:
        raise OEEAdmissionError("contact witness lacks independence proof")
    _refs(w.provenance_refs, "witness provenance", True)

    if allow_legacy and w.authentication_ref is None:
        return w, *_legacy_contact_auth(w)

    _validate_currentness(w.currentness_state, allow_noncurrent=allow_noncurrent, n="contact currentness")
    _validate_content_addressed_ref(
        w.authority_acceptance_ref,
        "contact authority acceptance",
        "ACCEPTED_CONTACT_OCCURRENCE_AUTHORITY_RECEIPT",
        "urn:rawlsing:accepted-contact-authority:sha256:",
    )
    contact_basis = _refs(w.contact_basis_refs, "contact basis", True)
    if any(x.kind in _INSUFFICIENT_CONTACT for x in contact_basis):
        raise OEEAdmissionError("co-location/co-presence/proximity cannot be contact-occurrence basis")
    expected_contact = _content_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        "urn:rawlsing:contact-occurrence-authentication:sha256:",
        _contact_material(w),
    )
    if w.authentication_ref != expected_contact:
        raise OEEIntegrityError("contact-occurrence authentication mismatch")

    _s(w.independence_authority_id, "independence authority id")
    _s(w.independence_authority_version, "independence authority version")
    _h(w.independence_authority_content_hash, "independence authority hash")
    _validate_content_addressed_ref(
        w.independence_authority_acceptance_ref,
        "independence authority acceptance",
        "ACCEPTED_CONTACT_INDEPENDENCE_AUTHORITY_RECEIPT",
        "urn:rawlsing:accepted-contact-independence-authority:sha256:",
    )
    _ref(w.independence_receipt_ref, "independence receipt")
    independence_basis = _refs(w.independence_basis_refs, "independence basis", True)
    if any(x.kind in _INSUFFICIENT_CONTACT for x in independence_basis):
        raise OEEAdmissionError("proximity cannot establish contact-witness independence")
    expected_ind = _content_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        "urn:rawlsing:contact-independence-authentication:sha256:",
        _independence_material(w, expected_contact),
    )
    if w.independence_authentication_ref != expected_ind:
        raise OEEIntegrityError("contact-witness independence authentication mismatch")
    return w, expected_contact, expected_ind

def _within(a: str, b: str, parent: V3OEERealizationRecord) -> None:
    if _dt(a) < _dt(parent.effective_from) or _dt(b) > _dt(parent.effective_until):
        raise OEEAdmissionError("child effective scope must remain within active parent scope")

def _candidate_material_from_record(r: V3OEERealizationRecord) -> dict[str, Any]:
    # Every mutable persisted record field except self-derived IDs/hashes/event ID
    # is committed here. validate_record() recomputes this exact material.
    return {
        "executor": [EXECUTOR_ID, EXECUTOR_VERSION],
        "actor_id": r.actor_id,
        "authority": [r.authority_id, r.authority_version],
        "registry": [r.registry_id, r.registry_version],
        "rule": [r.rule_id, r.rule_version],
        "realization_state": r.realization_state,
        "subject_ref": r.subject_ref,
        "parent_record_id": r.parent_record_id,
        "effective_scope": [r.effective_from, r.effective_until, r.time_granularity],
        "context_or_world_receipt_refs": r.context_or_world_receipt_refs,
        "applicability_receipt_refs": r.applicability_receipt_refs,
        "phase_state_ref": r.phase_state_ref,
        "position_or_other_constraint_refs": r.position_or_other_constraint_refs,
        "causal_witness_refs": r.causal_witness_refs,
        "rng_decision_receipt_ref": r.rng_decision_receipt_ref,
        "event_effect_kind": r.event_effect_kind,
        "prior_ledger_anchor_ref": r.prior_ledger_anchor_ref,
        "provenance_refs": r.provenance_refs,
    }

def _record_identity(r: V3OEERealizationRecord) -> dict[str, Any]:
    return {
        "actor": r.actor_id,
        "authority": [r.authority_id, r.authority_version],
        "registry": [r.registry_id, r.registry_version],
        "rule": [r.rule_id, r.rule_version],
        "state": r.realization_state,
        "subject": r.subject_ref,
        "parent": r.parent_record_id,
        "effective_scope": [r.effective_from, r.effective_until, r.time_granularity],
        "canonical_witnesses": r.causal_witness_refs,
        "candidate_replay_hash": r.source_candidate_replay_hash,
        "rng_decision_receipt_ref": r.rng_decision_receipt_ref,
    }

def _build(
    state: str,
    actor: ActorPhaseEvidence,
    subject: SubjectIngressEvidence,
    parent: str | None,
    start: str,
    end: str,
    granularity: str,
    context: tuple[ExactRef, ...],
    applicability: tuple[ExactRef, ...],
    constraints: tuple[ExactRef, ...],
    witnesses: tuple[ExactRef, ...],
    prior: ExactRef,
    provenance: tuple[ExactRef, ...],
) -> V3OEERealizationRecord:
    rule_id, _, _, effect = _RULES[state]
    provisional = V3OEERealizationRecord(
        "", actor.actor_id, ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION,
        ADP010_REGISTRY_ID, ADP010_REGISTRY_VERSION, rule_id, RULE_VERSION,
        state, subject.subject_ref, parent, start, end, granularity, "", "",
        context, applicability, actor.phase_state_ref, constraints, witnesses,
        None, None, effect, prior, provenance, "",
    )
    candidate_hash = _digest(_CANDIDATE_DOMAIN, _candidate_material_from_record(provisional))
    candidate_id = f"urn:rawlsing:v3:oee:candidate:sha256:{candidate_hash}"
    with_candidate = replace(
        provisional,
        source_candidate_id=candidate_id,
        source_candidate_replay_hash=candidate_hash,
    )
    record_hash = _digest(_RECORD_DOMAIN, _record_identity(with_candidate))
    event = None if effect is None else (
        f"urn:rawlsing:v3:oee:event:sha256:"
        f"{_digest(_EVENT_DOMAIN, {'record_hash': record_hash, 'effect': effect})}"
    )
    return replace(
        with_candidate,
        record_id=f"urn:rawlsing:v3:oee:record:sha256:{record_hash}",
        event_id=event,
        record_hash=record_hash,
    )

def _required_ref_present(provenance: tuple[ExactRef, ...], required: ExactRef, label: str) -> None:
    if required not in provenance:
        raise OEEIntegrityError(f"missing exact {label} provenance")

def validate_record(r: Any) -> V3OEERealizationRecord:
    if not isinstance(r, V3OEERealizationRecord):
        raise OEEIntegrityError("record must be V3OEERealizationRecord")
    if (
        r.authority_id, r.authority_version, r.registry_id, r.registry_version
    ) != (
        ADP010_AUTHORITY_ID, ADP010_AUTHORITY_VERSION, ADP010_REGISTRY_ID, ADP010_REGISTRY_VERSION
    ):
        raise OEEIntegrityError("ADP-010 authority/registry mismatch")
    if r.realization_state not in _RULES:
        raise OEEIntegrityError("unsupported realization state")
    rule_id, _, _, effect = _RULES[r.realization_state]
    if (r.rule_id, r.rule_version) != (rule_id, RULE_VERSION):
        raise OEEIntegrityError("rule identity mismatch")
    _s(r.actor_id, "actor_id")
    _s(r.subject_ref, "subject_ref")
    _h(r.source_candidate_replay_hash, "source_candidate_replay_hash")
    _ref(r.phase_state_ref, "phase_state_ref")
    if r.phase_state_ref.kind != "V3DevelopmentalPhaseState":
        raise OEEIntegrityError("phase_state_ref kind mismatch")
    _ref(r.prior_ledger_anchor_ref, "prior_ledger_anchor_ref")
    context = _refs(r.context_or_world_receipt_refs, "context", True)
    apps = _refs(r.applicability_receipt_refs, "applicability", r.realization_state != STATE_AVAILABLE)
    constraints = _refs(r.position_or_other_constraint_refs, "constraints")
    witnesses = _refs(r.causal_witness_refs, "witnesses", True)
    provenance = _refs(r.provenance_refs, "provenance", True)
    if (
        context != r.context_or_world_receipt_refs
        or apps != r.applicability_receipt_refs
        or constraints != r.position_or_other_constraint_refs
        or witnesses != r.causal_witness_refs
        or provenance != r.provenance_refs
    ):
        raise OEEIntegrityError("record refs are not canonical")
    _interval(r.effective_from, r.effective_until)
    _s(r.time_granularity, "time_granularity")
    if r.rng_decision_receipt_ref is not None:
        raise OEEIntegrityError("ADP-010 core-v1 is ZERO_DRAW")

    for req, label in (
        (ADP010_AUTHORITY_HASH_REF, "ADP-010 authority hash"),
        (ADP010_REGISTRY_HASH_REF, "ADP-010 registry hash"),
        (_rule_hash_ref(r.realization_state), "ADP-010 rule hash"),
        (ADP008_AUTHORITY_HASH_REF, "ADP-008 authority hash"),
        (ADP008_REGISTRY_HASH_REF, "ADP-008 registry hash"),
        (ADP020_AUTHORITY_HASH_REF, "ADP-020 authority hash"),
    ):
        _required_ref_present(provenance, req, label)

    by_kind: dict[str, list[ExactRef]] = {}
    for item in provenance:
        by_kind.setdefault(item.kind, []).append(item)
    def require_auth(kind: str, prefix: str, label: str, *, at_least: int = 1) -> None:
        refs = by_kind.get(kind, [])
        if len(refs) < at_least:
            raise OEEIntegrityError(f"missing exact {label}")
        for item in refs:
            _validate_content_addressed_ref(item, label, kind, prefix)

    require_auth(
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
        "subject ingress authentication",
    )
    require_auth(
        "ADP008_PHASE_STATE_AUTHENTICATION",
        "urn:rawlsing:adp008-phase-authentication:sha256:",
        "ADP-008 phase-state authentication",
    )
    if r.realization_state != STATE_AVAILABLE:
        require_auth(
            "POSITIVE_APPLICABILITY_AUTHENTICATION",
            "urn:rawlsing:positive-applicability-authentication:sha256:",
            "positive applicability authentication",
        )
    if r.realization_state == STATE_ENCOUNTER:
        require_auth(
            "CONTACT_OCCURRENCE_AUTHENTICATION",
            "urn:rawlsing:contact-occurrence-authentication:sha256:",
            "contact-occurrence authentication",
        )
        require_auth(
            "CONTACT_INDEPENDENCE_AUTHENTICATION",
            "urn:rawlsing:contact-independence-authentication:sha256:",
            "contact-witness independence authentication",
        )
        kinds = {x.kind 