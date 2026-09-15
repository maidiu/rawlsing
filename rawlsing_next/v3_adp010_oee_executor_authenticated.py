"""GT3/GT4 W2 successor ADP-010 bounded OEE executor.

Distinct candidate successor to historical S3. Historical S3 remains immutable
and unadopted. This module preserves deterministic
AVAILABLE -> OPPORTUNITY -> ENCOUNTER semantics while repairing only the
authentication/replay seams identified by T3.

It does not materialize or classify subjects, infer contact from proximity,
create EXPOSURE, mutate actor state, or create comparator/PSEPF/metabolism/
CAN-008/V2/positive-V3 authority.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
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
ADP010_AUTHORITY_ARTIFACT_BLOB_SHA = "0eac41d081b112255dcfc6dd42a6afab15a2928b"

ADP008_AUTHORITY_ID = "V3_DEVELOPMENTAL_PHASE_RULE"
ADP008_AUTHORITY_VERSION = "1.1.0"
ADP008_REGISTRY_ID = "V3_DEVELOPMENTAL_PHASE_REGISTRY"
ADP008_REGISTRY_VERSION = "1.1.0"
ADP008_AUTHORITY_ARTIFACT_BLOB_SHA = "c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6"

ADP020_AUTHORITY_ID = "ADP-020"
ADP020_AUTHORITY_VERSION = "1.0.0"
ADP020_AUTHORITY_ARTIFACT_BLOB_SHA = "1f13dc7ccc69bda562613d6215acc996a9c092e4"

OBL054_ADOPTION_ARTIFACT_BLOB = "fc46d377dafa5b2c4e274d702e7f26268aa429cb"
OBL054_MATERIALIZER_ID = "GT34_V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_MATERIALIZER"
OBL054_MATERIALIZER_VERSION = "2.0.0"
OBL054_ACCEPTED_ROOT_HASH = "1563a1661d3e0a76e6781633f1b590147e26ab21014674bbe732f68cef6acfa8"
OBL054_PERMIT_HASH = "3eeea2dcfa0a70f1a5b6ce15d41d9f83d84e39ecde816896150fff21e77573dc"
OBL054_PERMIT_ID = (
    "urn:rawlsing:gt34:obl054:one-object-materialization-permit:sha256:"
    + OBL054_PERMIT_HASH
)
OBL053_ADOPTION_ARTIFACT_BLOB = "f561765bad4fdad2bbf4591f35fe7f81f8486428"
HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB = "286ff7b851e920ff2760082d8b2fb194560ab127"
OBL053_AUTHORITY_ID = "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_ENTITY_SEMANTIC_AUTHORITY"
OBL053_AUTHORITY_VERSION = "1.0.0"
OBL053_AUTHORITY_HASH = "867962094705ce13a33b0acfc81918b930dca6ae6d7c22e8094cc1d95bc41b29"
OBL053_GENERATION_SEED_HASH = "b20687b91e0a7a9cc64a96e229e58244041d54b4ea9c73a182b2f9da0cd2ef53"
OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH = "153ff1cd67e27b435cb6ffa4127047802eb06edcc6dab7072cedf9cb3ede7d6c"
OBL053_SEMANTIC_OBJECT_HASH = "9a5fbe9a7c272cb2a60e425f09b206f0d25dd2d95caa07028bdb021130c32547"
OBL053_SEMANTIC_OBJECT_ID = (
    "urn:rawlsing:gt34:generated-nonactor-subject-semantic-object:sha256:"
    + OBL053_SEMANTIC_OBJECT_HASH
)

MATERIALIZER_RECEIPT_SCHEMA = "V3P1_CORRECTED_OWNER_AUTHENTICATED_ONE_OBJECT_SUBJECT_RECEIPT@2.0.0"
MATERIALIZER_OWNER_BINDING_SCHEMA = "V3P1_OWNER_BOUND_SUBJECT_INGRESS_BINDING@1.0.0"
MATERIALIZER_SUBJECT_REF_SCHEME = "RAWLSING_V3_OWNER_PRESERVING_SUBJECT_REF_V1"
MATERIALIZER_OWNER_BINDING_DOMAIN = b"RAWLSING\0GT34-S2\0V3P1-OWNER-BOUND-SUBJECT-INGRESS-V1\0"
MATERIALIZER_SUBJECT_REF_DOMAIN = b"RAWLSING\0GT34-S2\0V3P1-OWNER-PRESERVING-SUBJECT-REF-V1\0"
MATERIALIZER_RECEIPT_DOMAIN = b"RAWLSING\0GT34-U2\0V3P1-AUTHENTICATED-SUBJECT-RECEIPT-V2\0"

DEVELOPMENT_ACTIVE_PHASE = "V3DP_DEVELOPMENT_ACTIVE"
STATE_AVAILABLE = "AVAILABLE"
STATE_OPPORTUNITY = "OPPORTUNITY"
STATE_ENCOUNTER = "ENCOUNTER"
RULE_AVAILABLE = "OEE_CORE_AVAILABLE_BASIS_V1"
RULE_OPPORTUNITY = "OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1"
RULE_ENCOUNTER = "OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1"
RULE_VERSION = "V1"
EFFECT_OPPORTUNITY = "OEE_OPPORTUNITY_ESTABLISHED"
EFFECT_ENCOUNTER = "OEE_ENCOUNTER_OCCURRED"

EP_GENERATED_RUNTIME_FACT = "GENERATED_RUNTIME_FACT"
EP_RESOLVER_CONTEXT = "RESOLVER_DERIVED_CONTEXT"
EP_ADMITTED_CAUSAL_EVENT = "ADMITTED_CAUSAL_EVENT"
_ADMISSIBLE_EP = {
    EP_GENERATED_RUNTIME_FACT,
    EP_RESOLVER_CONTEXT,
    EP_ADMITTED_CAUSAL_EVENT,
}

CONTACT_WITNESS_KIND = "CONTACT_OCCURRENCE_WITNESS"
CONTACT_INDEPENDENCE_KIND = "CONTACT_WITNESS_INDEPENDENCE"
CONTACT_OCCURRENCE_SEMANTIC = "CONTACT_OCCURRENCE"

_INSUFFICIENT_CONTACT = {
    "COLOCATION",
    "CO_LOCATION",
    "COPRESENCE",
    "CO_PRESENCE",
    "SAME_GEOGRAPHY_TIME",
    "SHARED_V555_ENDPOINT",
    "SAME_STRUCTURAL_TARGET",
    "SAME_INSTITUTION_CATEGORY",
    "SIMULTANEOUS_RESOLVER_SELECTION",
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
_AUTH_DOMAIN = "RAWLSING\0GT34-W2\0AUTHENTICATION_BINDING_V1\0"
_FIXED_PROVENANCE_DOMAIN = "RAWLSING\0GT34-W2\0FIXED_AUTHORITY_PROVENANCE_V1\0"

class OEEAdmissionError(ValueError):
    pass

class OEEIntegrityError(OEEAdmissionError):
    pass

@dataclass(frozen=True, order=True, slots=True)
class ExactRef:
    kind: str
    ref: str
    content_hash: str

@dataclass(frozen=True, slots=True)
class SubjectMaterializationReceipt:
    receipt_id: str
    receipt_hash: str
    subject_ref: str
    subject_ref_hash: str
    materializer_id: str
    materializer_version: str
    adoption_artifact_blob: str
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
    currentness_state: str

@dataclass(frozen=True, slots=True)
class CausalUsePermission:
    permission_ref: ExactRef
    authority_id: str
    authority_version: str
    authority_content_hash: str
    authority_acceptance_ref: ExactRef
    subject_ref: str
    semantic_object_ref: ExactRef
    materialization_receipt_ref: ExactRef
    scope: str
    provenance_refs: tuple[ExactRef, ...]
    authentication_ref: ExactRef
    currentness_state: str

@dataclass(frozen=True, slots=True)
class SubjectIngressEvidence:
    subject_ref: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_content_hash: str
    semantic_object_ref: ExactRef
    materialization_receipt: SubjectMaterializationReceipt
    obl054_adoption_artifact_blob: str
    epistemic_class: str
    causal_use_permission: CausalUsePermission
    provenance_refs: tuple[ExactRef, ...]
    authentication_ref: ExactRef
    currentness_state: str

@dataclass(frozen=True, slots=True)
class ActorPhaseEvidence:
    actor_id: str
    phase_state_ref: ExactRef
    phase_state_receipt_ref: ExactRef
    phase_authority_id: str
    phase_authority_version: str
    phase_authority_artifact_blob_sha: str
    phase_registry_id: str
    phase_registry_version: str
    phase_registry_content_hash: str
    base_phase_id: str
    provenance_refs: tuple[ExactRef, ...]
    authentication_ref: ExactRef
    currentness_state: str

@dataclass(frozen=True, slots=True)
class PositiveApplicabilityReceipt:
    receipt: ExactRef
    authority_id: str
    authority_version: str
    authority_content_hash: str
    authority_acceptance_ref: ExactRef
    result: str
    provenance_refs: tuple[ExactRef, ...]
    authentication_ref: ExactRef
    currentness_state: str

@dataclass(frozen=True, slots=True)
class OpportunityBasisEvidence:
    basis_ref: ExactRef
    actor_id: str
    subject_ref: str
    applicability_receipts: tuple[PositiveApplicabilityReceipt, ...]
    context_or_world_receipt_refs: tuple[ExactRef, ...]
    position_or_other_constraint_refs: tuple[ExactRef, ...]
    provenance_refs: tuple[ExactRef, ...]

@dataclass(frozen=True, slots=True)
class ContactOccurrenceWitness:
    witness_ref: ExactRef
    witness_authority_id: str
    witness_authority_version: str
    witness_authority_content_hash: str
    witness_authority_acceptance_ref: ExactRef
    actor_id: str
    subject_ref: str
    occurrence_time: str
    semantic: str
    contact_basis_refs: tuple[ExactRef, ...]
    contact_authentication_ref: ExactRef
    independence_ref: ExactRef
    independence_authority_id: str
    independence_authority_version: str
    independence_authority_content_hash: str
    independence_authority_acceptance_ref: ExactRef
    independence_receipt_ref: ExactRef
    independence_basis_refs: tuple[ExactRef, ...]
    independence_authentication_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    currentness_state: str

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

def _s(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise OEEIntegrityError(f"{field} must be non-empty string")
    value = unicodedata.normalize("NFC", value.strip())
    if not value:
        raise OEEIntegrityError(f"{field} must be non-empty string")
    return value

def _h(value: Any, field: str) -> str:
    value = _s(value, field)
    if not _HASH64.fullmatch(value):
        raise OEEIntegrityError(f"{field} must be lowercase SHA-256 hex")
    return value

def _blob(value: Any, field: str) -> str:
    value = _s(value, field)
    if not _BLOB40.fullmatch(value):
        raise OEEIntegrityError(f"{field} must be lowercase Git SHA-1 hex")
    return value

def _ref(value: Any, field: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise OEEIntegrityError(f"{field} must be ExactRef")
    _s(value.kind, field + ".kind")
    _s(value.ref, field + ".ref")
    _h(value.content_hash, field + ".content_hash")
    return value

def _refs(values: Iterable[ExactRef], field: str, required: bool = False) -> tuple[ExactRef, ...]:
    values = tuple(values)
    if required and not values:
        raise OEEIntegrityError(f"{field} must be non-empty")
    validated = tuple(_ref(v, field) for v in values)
    return tuple(sorted(set(validated)))

def _merge(*groups: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    return _refs((x for group in groups for x in group), "refs", True)

def _norm(value: Any) -> Any:
    if isinstance(value, ExactRef):
        return {"kind": value.kind, "ref": value.ref, "content_hash": value.content_hash}
    if isinstance(value, Mapping):
        return {str(k): _norm(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [_norm(v) for v in value]
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    return value

def _canonical_json(value: Any) -> str:
    return json.dumps(_norm(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _digest(domain: str, value: Any) -> str:
    return sha256((domain + _canonical_json(value)).encode("utf-8")).hexdigest()

def _digest_bytes(domain: bytes, value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return sha256(domain + raw).hexdigest()

def _time(value: Any, field: str) -> str:
    raw = _s(value, field)
    parsed = raw[:-1] + "+00:00" if raw.endswith("Z") else raw
    try:
        dt = datetime.fromisoformat(parsed)
    except ValueError as exc:
        raise OEEIntegrityError(f"{field} must be ISO-8601") from exc
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise OEEIntegrityError(f"{field} must be timezone-aware")
    return dt.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")

def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00")

def _interval(start: Any, end: Any) -> tuple[str, str]:
    start = _time(start, "effective_from")
    end = _time(end, "effective_until")
    if _dt(end) < _dt(start):
        raise OEEIntegrityError("effective_until precedes effective_from")
    return start, end

def _content_ref(kind: str, prefix: str, material: Any) -> ExactRef:
    h = _digest(_AUTH_DOMAIN, material)
    return ExactRef(kind, prefix + h, h)

def _validate_content_ref(ref: ExactRef, kind: str, prefix: str, field: str) -> ExactRef:
    ref = _ref(ref, field)
    if ref.kind != kind or ref.ref != prefix + ref.content_hash:
        raise OEEIntegrityError(f"{field} is not exact content-addressed {kind}")
    return ref

def _authority_acceptance_ref(kind: str, authority_id: str, version: str, content_hash: str, currentness: str) -> ExactRef:
    prefix = f"urn:rawlsing:{kind.lower().replace('_','-')}:sha256:"
    return _content_ref(
        kind,
        prefix,
        {
            "authority_id": authority_id,
            "authority_version": version,
            "authority_content_hash": content_hash,
            "currentness_state": currentness,
        },
    )

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
            ADP010_AUTHORITY_ID,
            ADP010_AUTHORITY_VERSION,
            ADP010_REGISTRY_ID,
            ADP010_REGISTRY_VERSION,
            ADP010_AUTHORITY_ARTIFACT_BLOB_SHA,
            rule_id,
            RULE_VERSION,
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

CURRENT_SEMANTIC_OBJECT_REF = ExactRef(
    "GT34_OBL053_ONE_OBJECT_NONACTOR_SUBJECT_SEMANTIC_OBJECT",
    OBL053_SEMANTIC_OBJECT_ID,
    OBL053_SEMANTIC_OBJECT_HASH,
)
CURRENT_EVIDENCE_REFS = (
    ExactRef(
        "GT34_OBL053_OBJECTIVE_EVIDENCE_RECEIPT",
        "urn:rawlsing:gt34:obl053:objective-evidence-receipt:sha256:" + OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH,
        OBL053_OBJECTIVE_EVIDENCE_RECEIPT_HASH,
    ),
)
CURRENT_PROVENANCE_REFS = (
    ExactRef(
        "GOVERNED_GENERATION_SEED",
        "urn:rawlsing:gt34:obl053:generation-seed:sha256:" + OBL053_GENERATION_SEED_HASH,
        OBL053_GENERATION_SEED_HASH,
    ),
    ExactRef(
        "SEMANTIC_OWNER_AUTHORITY",
        "urn:rawlsing:gt34:obl053:semantic-owner-authority:sha256:" + OBL053_AUTHORITY_HASH,
        OBL053_AUTHORITY_HASH,
    ),
)

def _mat_ref_dict(ref: ExactRef) -> dict[str, str]:
    ref = _ref(ref, "materializer ref")
    return {"kind": ref.kind, "ref_id": ref.ref, "sha256": ref.content_hash}

def _materializer_owner_material(m: SubjectMaterializationReceipt) -> dict[str, Any]:
    return {
        "schema_id": MATERIALIZER_OWNER_BINDING_SCHEMA,
        "semantic_owner_authority": {
            "id": m.semantic_owner_authority_id,
            "version": m.semantic_owner_authority_version,
            "content_hash": m.semantic_owner_authority_hash,
        },
        "semantic_object_ref": _mat_ref_dict(m.semantic_object_ref),
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materializer evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materializer provenance", True)],
    }

def _materializer_subject_material(m: SubjectMaterializationReceipt) -> dict[str, Any]:
    return {
        "scheme": MATERIALIZER_SUBJECT_REF_SCHEME,
        "semantic_owner_authority": {
            "id": m.semantic_owner_authority_id,
            "version": m.semantic_owner_authority_version,
            "content_hash": m.semantic_owner_authority_hash,
        },
        "semantic_object_ref": _mat_ref_dict(m.semantic_object_ref),
        "owner_binding_content_hash": m.owner_binding_content_hash,
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materializer evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materializer provenance", True)],
    }

def _materializer_receipt_body(m: SubjectMaterializationReceipt) -> dict[str, Any]:
    return {
        "schema_id": MATERIALIZER_RECEIPT_SCHEMA,
        "subject_ref": m.subject_ref,
        "subject_ref_hash": m.subject_ref_hash,
        "materializer_id": m.materializer_id,
        "materializer_version": m.materializer_version,
        "adoption_artifact_blob": m.adoption_artifact_blob,
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
        "evidence_refs": [_mat_ref_dict(x) for x in _refs(m.evidence_refs, "materializer evidence", True)],
        "provenance_refs": [_mat_ref_dict(x) for x in _refs(m.provenance_refs, "materializer provenance", True)],
        "replay_input_hash": m.replay_input_hash,
        "integrity_state": m.integrity_state,
        "semantic_owner_transfer": m.semantic_owner_transfer,
        "semantic_fields_interpreted": m.semantic_fields_interpreted,
    }

def _validate_currentness(value: str, expected: str, field: str) -> None:
    if _s(value, field) != expected:
        raise OEEAdmissionError(f"{field} must be {expected}")

def _validate_materialization_receipt(m: Any, currentness: str) -> SubjectMaterializationReceipt:
    if not isinstance(m, SubjectMaterializationReceipt):
        raise OEEIntegrityError("subject materialization receipt wire is required")
    _validate_currentness(m.currentness_state, currentness, "materialization currentness")
    _s(m.receipt_id, "materialization receipt id")
    _h(m.receipt_hash, "materialization receipt hash")
    _s(m.subject_ref, "materialization subject_ref")
    _h(m.subject_ref_hash, "materialization subject_ref_hash")
    _s(m.materializer_id, "materializer id")
    _s(m.materializer_version, "materializer version")
    _blob(m.adoption_artifact_blob, "materializer adoption artifact blob")
    _h(m.accepted_owner_root_hash, "accepted owner root hash")
    _s(m.materialization_permit_id, "materialization permit id")
    _h(m.materialization_permit_hash, "materialization permit hash")
    _s(m.semantic_owner_authority_id, "semantic owner id")
    _s(m.semantic_owner_authority_version, "semantic owner version")
    _h(m.semantic_owner_authority_hash, "semantic owner hash")
    _ref(m.semantic_object_ref, "semantic object ref")
    _h(m.owner_binding_content_hash, "owner binding content hash")
    _refs(m.evidence_refs, "materializer evidence", True)
    _refs(m.provenance_refs, "materializer provenance", True)
    _h(m.replay_input_hash, "materializer replay input hash")
    if m.semantic_owner_transfer is not False or m.semantic_fields_interpreted is not False:
        raise OEEAdmissionError("materializer owner preservation / semantic opacity violated")

    if currentness == CURRENT_ACCEPTED:
        expected = (
            OBL054_MATERIALIZER_ID,
            OBL054_MATERIALIZER_VERSION,
            OBL053_ADOPTION_ARTIFACT_BLOB,
            OBL054_ACCEPTED_ROOT_HASH,
            OBL054_PERMIT_ID,
            OBL054_PERMIT_HASH,
            OBL053_AUTHORITY_ID,
            OBL053_AUTHORITY_VERSION,
            OBL053_AUTHORITY_HASH,
            CURRENT_SEMANTIC_OBJECT_REF,
            CURRENT_EVIDENCE_REFS,
            CURRENT_PROVENANCE_REFS,
            "AUTHENTICATED_FRESH_OBL053_ROOT__OWNER_BOUND_INPUT_VERIFIED",
        )
        actual = (
            m.materializer_id,
            m.materializer_version,
            m.adoption_artifact_blob,
            m.accepted_owner_root_hash,
            m.materialization_permit_id,
            m.materialization_permit_hash,
            m.semantic_owner_authority_id,
            m.semantic_owner_authority_version,
            m.semantic_owner_authority_hash,
            m.semantic_object_ref,
            m.evidence_refs,
            m.provenance_refs,
            m.integrity_state,
        )
        if actual != expected:
            raise OEEAdmissionError("subject ingress is not exact adopted OBL054/current OBL053 materialization contract")
    else:
        if (
            m.materializer_id == OBL054_MATERIALIZER_ID
            or m.adoption_artifact_blob == OBL053_ADOPTION_ARTIFACT_BLOB
            or m.accepted_owner_root_hash == OBL054_ACCEPTED_ROOT_HASH
            or m.materialization_permit_hash == OBL054_PERMIT_HASH
        ):
            raise OEEAdmissionError("synthetic fixture may not masquerade as current OBL054")

    owner_hash = _digest_bytes(MATERIALIZER_OWNER_BINDING_DOMAIN, _materializer_owner_material(m))
    if m.owner_binding_content_hash != owner_hash:
        raise OEEIntegrityError("materializer owner binding mismatch")
    subject_material = _materializer_subject_material(m)
    subject_hash = _digest_bytes(MATERIALIZER_SUBJECT_REF_DOMAIN, subject_material)
    if m.subject_ref_hash != subject_hash:
        raise OEEIntegrityError("materializer subject_ref_hash mismatch")
    if m.subject_ref != "urn:rawlsing:v3:subject:sha256:" + subject_hash:
        raise OEEIntegrityError("materializer subject_ref mismatch")
    replay_hash = sha256(
        json.dumps(subject_material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    if m.replay_input_hash != replay_hash:
        raise OEEIntegrityError("materializer replay_input_hash mismatch")
    receipt_hash = _digest_bytes(MATERIALIZER_RECEIPT_DOMAIN, _materializer_receipt_body(m))
    if m.receipt_hash != receipt_hash:
        raise OEEIntegrityError("materializer receipt hash mismatch")
    if m.receipt_id != (
        "urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:" + receipt_hash
    ):
        raise OEEIntegrityError("materializer receipt id/hash mismatch")
    return m

def _permission_material(p: CausalUsePermission) -> dict[str, Any]:
    return {
        "permission_ref": p.permission_ref,
        "authority": [p.authority_id, p.authority_version, p.authority_content_hash],
        "authority_acceptance_ref": p.authority_acceptance_ref,
        "subject_ref": p.subject_ref,
        "semantic_object_ref": p.semantic_object_ref,
        "materialization_receipt_ref": p.materialization_receipt_ref,
        "scope": p.scope,
        "provenance_refs": _refs(p.provenance_refs, "causal use provenance", True),
        "currentness_state": p.currentness_state,
    }

def _validate_permission(
    p: Any,
    subject_ref: str,
    semantic_object_ref: ExactRef,
    materialization_receipt_ref: ExactRef,
    currentness: str,
) -> CausalUsePermission:
    if not isinstance(p, CausalUsePermission):
        raise OEEIntegrityError("authenticated causal-use permission is required")
    _validate_currentness(p.currentness_state, currentness, "causal use currentness")
    if p.permission_ref.kind != "CAUSAL_USE_PERMISSION":
        raise OEEAdmissionError("causal-use permission ref kind mismatch")
    _ref(p.permission_ref, "causal use permission")
    _s(p.authority_id, "causal use authority id")
    _s(p.authority_version, "causal use authority version")
    _h(p.authority_content_hash, "causal use authority hash")
    expected_accept = _authority_acceptance_ref(
        "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT",
        p.authority_id,
        p.authority_version,
        p.authority_content_hash,
        currentness,
    )
    if p.authority_acceptance_ref != expected_accept:
        raise OEEIntegrityError("causal-use authority acceptance binding mismatch")
    if (p.subject_ref, p.semantic_object_ref, p.materialization_receipt_ref) != (
        subject_ref,
        semantic_object_ref,
        materialization_receipt_ref,
    ):
        raise OEEAdmissionError("causal-use permission does not bind exact subject/object/materialization")
    if p.scope != "ADP010_CAUSAL_USE":
        raise OEEAdmissionError("causal-use permission scope mismatch")
    expected_auth = _content_ref(
        "CAUSAL_USE_PERMISSION_AUTHENTICATION",
        "urn:rawlsing:causal-use-authentication:sha256:",
        _permission_material(p),
    )
    if p.authentication_ref != expected_auth:
        raise OEEIntegrityError("causal-use authentication mismatch")
    return p

def _subject_material(s: SubjectIngressEvidence) -> dict[str, Any]:
    return {
        "subject_ref": s.subject_ref,
        "semantic_owner_authority": [
            s.semantic_owner_authority_id,
            s.semantic_owner_authority_version,
            s.semantic_owner_authority_content_hash,
        ],
        "semantic_object_ref": s.semantic_object_ref,
        "materialization_receipt_ref": ExactRef(
            "SUBJECT_MATERIALIZATION_RECEIPT",
            s.materialization_receipt.receipt_id,
            s.materialization_receipt.receipt_hash,
        ),
        "obl054_adoption_artifact_blob": s.obl054_adoption_artifact_blob,
        "epistemic_class": s.epistemic_class,
        "causal_use_authentication_ref": s.causal_use_permission.authentication_ref,
        "provenance_refs": _refs(s.provenance_refs, "subject provenance", True),
        "currentness_state": s.currentness_state,
    }

def _validate_subject(s: Any, currentness: str) -> tuple[SubjectIngressEvidence, ExactRef]:
    if not isinstance(s, SubjectIngressEvidence):
        raise OEEIntegrityError("subject must be SubjectIngressEvidence")
    _validate_currentness(s.currentness_state, currentness, "subject currentness")
    _s(s.subject_ref, "subject_ref")
    _s(s.semantic_owner_authority_id, "semantic owner id")
    _s(s.semantic_owner_authority_version, "semantic owner version")
    _h(s.semantic_owner_authority_content_hash, "semantic owner hash")
    _ref(s.semantic_object_ref, "semantic object ref")
    _blob(s.obl054_adoption_artifact_blob, "OBL054 adoption artifact blob")
    if currentness == CURRENT_ACCEPTED and s.obl054_adoption_artifact_blob != OBL054_ADOPTION_ARTIFACT_BLOB:
        raise OEEAdmissionError("subject ingress is not bound to adopted OBL054 adoption artifact")
    if currentness == NONCURRENT_SYNTHETIC_TEST_ONLY and s.obl054_adoption_artifact_blob == OBL054_ADOPTION_ARTIFACT_BLOB:
        raise OEEAdmissionError("synthetic subject may not impersonate current OBL054 adoption")
    if s.epistemic_class not in _ADMISSIBLE_EP:
        raise OEEAdmissionError("subject basis epistemic class is not ADP-010-admissible")
    _refs(s.provenance_refs, "subject provenance", True)

    m = _validate_materialization_receipt(s.materialization_receipt, currentness)
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", m.receipt_id, m.receipt_hash)
    if (
        s.subject_ref,
        s.semantic_owner_authority_id,
        s.semantic_owner_authority_version,
        s.semantic_owner_authority_content_hash,
        s.semantic_object_ref,
    ) != (
        m.subject_ref,
        m.semantic_owner_authority_id,
        m.semantic_owner_authority_version,
        m.semantic_owner_authority_hash,
        m.semantic_object_ref,
    ):
        raise OEEAdmissionError("subject ingress does not match exact materialization receipt")
    _validate_permission(
        s.causal_use_permission,
        s.subject_ref,
        s.semantic_object_ref,
        mat_ref,
        currentness,
    )
    expected_auth = _content_ref(
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
        _subject_material(s),
    )
    if s.authentication_ref != expected_auth:
        raise OEEIntegrityError("subject ingress authentication mismatch")
    return s, expected_auth

def _phase_material(a: ActorPhaseEvidence) -> dict[str, Any]:
    return {
        "actor_id": a.actor_id,
        "phase_state_ref": a.phase_state_ref,
        "phase_state_receipt_ref": a.phase_state_receipt_ref,
        "authority": [
            a.phase_authority_id,
            a.phase_authority_version,
            a.phase_authority_artifact_blob_sha,
        ],
        "registry": [
            a.phase_registry_id,
            a.phase_registry_version,
            a.phase_registry_content_hash,
        ],
        "base_phase_id": a.base_phase_id,
        "provenance_refs": _refs(a.provenance_refs, "actor phase provenance", True),
        "currentness_state": a.currentness_state,
    }

def _validate_actor(a: Any, currentness: str) -> tuple[ActorPhaseEvidence, ExactRef]:
    if not isinstance(a, ActorPhaseEvidence):
        raise OEEIntegrityError("actor must be ActorPhaseEvidence")
    _validate_currentness(a.currentness_state, currentness, "phase currentness")
    _s(a.actor_id, "actor_id")
    if _ref(a.phase_state_ref, "phase_state_ref").kind != "V3DevelopmentalPhaseState":
        raise OEEAdmissionError("phase_state_ref must be V3DevelopmentalPhaseState")
    if _ref(a.phase_state_receipt_ref, "phase_state_receipt_ref").kind != "V3DevelopmentalPhaseStateReceipt":
        raise OEEAdmissionError("phase_state_receipt_ref kind mismatch")
    if (
        a.phase_authority_id,
        a.phase_authority_version,
        a.phase_authority_artifact_blob_sha,
        a.phase_registry_id,
        a.phase_registry_version,
        a.phase_registry_content_hash,
    ) != (
        ADP008_AUTHORITY_ID,
        ADP008_AUTHORITY_VERSION,
        ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
        ADP008_REGISTRY_ID,
        ADP008_REGISTRY_VERSION,
        ADP008_REGISTRY_CONTENT_HASH,
    ):
        raise OEEAdmissionError("wrong ADP-008 authority/registry authentication")
    if a.base_phase_id != DEVELOPMENT_ACTIVE_PHASE:
        raise OEEAdmissionError("V3DP_DEVELOPMENT_ACTIVE is required")
    _refs(a.provenance_refs, "actor phase provenance", True)
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

def _validate_app(x: Any, currentness: str) -> tuple[ExactRef, ExactRef]:
    if not isinstance(x, PositiveApplicabilityReceipt) or x.result != "POSITIVE":
        raise OEEAdmissionError("opportunity requires positive applicability")
    _validate_currentness(x.currentness_state, currentness, "applicability currentness")
    if _ref(x.receipt, "applicability receipt").kind != "POSITIVE_APPLICABILITY_RECEIPT":
        raise OEEAdmissionError("applicability receipt kind mismatch")
    _s(x.authority_id, "applicability authority id")
    _s(x.authority_version, "applicability authority version")
    _h(x.authority_content_hash, "applicability authority hash")
    expected_accept = _authority_acceptance_ref(
        "ACCEPTED_APPLICABILITY_AUTHORITY_RECEIPT",
        x.authority_id,
        x.authority_version,
        x.authority_content_hash,
        currentness,
    )
    if x.authority_acceptance_ref != expected_accept:
        raise OEEIntegrityError("applicability authority acceptance mismatch")
    _refs(x.provenance_refs, "applicability provenance", True)
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
        "witness_authority_acceptance_ref": w.witness_authority_acceptance_ref,
        "actor_id": w.actor_id,
        "subject_ref": w.subject_ref,
        "occurrence_time": _time(w.occurrence_time, "contact occurrence time"),
        "semantic": w.semantic,
        "contact_basis_refs": _refs(w.contact_basis_refs, "contact basis refs", True),
        "provenance_refs": _refs(w.provenance_refs, "contact provenance", True),
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
        "independence_basis_refs": _refs(w.independence_basis_refs, "independence basis refs", True),
        "currentness_state": w.currentness_state,
    }

def _validate_contact(
    w: Any,
    actor_id: str,
    subject_ref: str,
    effective_time: str,
    currentness: str,
) -> tuple[ContactOccurrenceWitness, ExactRef, ExactRef]:
    if not isinstance(w, ContactOccurrenceWitness):
        raise OEEAdmissionError("ENCOUNTER requires exact ContactOccurrenceWitness")
    _validate_currentness(w.currentness_state, currentness, "contact currentness")
    wr = _ref(w.witness_ref, "contact witness")
    if wr.kind in _INSUFFICIENT_CONTACT:
        raise OEEAdmissionError("co-location/co-presence or structural proximity is insufficient for ENCOUNTER")
    if wr.kind != CONTACT_WITNESS_KIND:
        raise OEEAdmissionError("contact witness must be exact CONTACT_OCCURRENCE_WITNESS")
    if w.actor_id != actor_id or w.subject_ref != subject_ref:
        raise OEEAdmissionError("contact witness actor/subject mismatch")
    if w.semantic != CONTACT_OCCURRENCE_SEMANTIC:
        raise OEEAdmissionError("contact witness does not assert CONTACT_OCCURRENCE")
    if _time(w.occurrence_time, "contact occurrence time") != effective_time:
        raise OEEAdmissionError("encounter time must equal contact occurrence time")
    _s(w.witness_authority_id, "contact authority id")
    _s(w.witness_authority_version, "contact authority version")
    _h(w.witness_authority_content_hash, "contact authority hash")
    expected_accept = _authority_acceptance_ref(
        "ACCEPTED_CONTACT_OCCURRENCE_AUTHORITY_RECEIPT",
        w.witness_authority_id,
        w.witness_authority_version,
        w.witness_authority_content_hash,
        currentness,
    )
    if w.witness_authority_acceptance_ref != expected_accept:
        raise OEEIntegrityError("contact witness authority acceptance mismatch")
    contact_basis = _refs(w.contact_basis_refs, "contact basis refs", True)
    if any(r.kind in _INSUFFICIENT_CONTACT for r in contact_basis):
        raise OEEAdmissionError("co-location/co-presence/proximity cannot be laundered into contact occurrence")
    expected_contact = _content_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        "urn:rawlsing:contact-occurrence-authentication:sha256:",
        _contact_material(w),
    )
    if w.contact_authentication_ref != expected_contact:
        raise OEEIntegrityError("contact-occurrence authentication mismatch")

    if _ref(w.independence_ref, "independence ref").kind != CONTACT_INDEPENDENCE_KIND:
        raise OEEAdmissionError("contact witness lacks independence proof")
    _s(w.independence_authority_id, "independence authority id")
    _s(w.independence_authority_version, "independence authority version")
    _h(w.independence_authority_content_hash, "independence authority hash")
    expected_ind_accept = _authority_acceptance_ref(
        "ACCEPTED_CONTACT_INDEPENDENCE_AUTHORITY_RECEIPT",
        w.independence_authority_id,
        w.independence_authority_version,
        w.independence_authority_content_hash,
        currentness,
    )
    if w.independence_authority_acceptance_ref != expected_ind_accept:
        raise OEEIntegrityError("contact independence authority acceptance mismatch")
    if _ref(w.independence_receipt_ref, "independence receipt").kind != "CONTACT_WITNESS_INDEPENDENCE_RECEIPT":
        raise OEEAdmissionError("contact independence receipt kind mismatch")
    independence_basis = _refs(w.independence_basis_refs, "independence basis refs", True)
    if any(r.kind in _INSUFFICIENT_CONTACT for r in independence_basis):
        raise OEEAdmissionError("proximity cannot establish contact witness independence")
    expected_ind = _content_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        "urn:rawlsing:contact-independence-authentication:sha256:",
        _independence_material(w, expected_contact),
    )
    if w.independence_authentication_ref != expected_ind:
        raise OEEIntegrityError("contact witness independence authentication mismatch")
    _refs(w.provenance_refs, "contact provenance", True)
    return w, expected_contact, expected_ind

def _within(start: str, end: str, parent: V3OEERealizationRecord) -> None:
    if _dt(start) < _dt(parent.effective_from) or _dt(end) > _dt(parent.effective_until):
        raise OEEAdmissionError("child effective scope must remain within active parent scope")

def _candidate_material(r: V3OEERealizationRecord) -> dict[str, Any]:
    return {
        "executor": [EXECUTOR_ID, EXECUTOR_VERSION],
        "actor_id": r.actor_id,
        "authority": [r.authority_id, r.authority_version],
        "registry": [r.registry_id, r.registry_version],
        "rule": [r.rule_id, r.rule_version],
        "realization_state": r.realization_state,
        "subject_ref": r.subject_ref,
        "parent_record_id": r.parent_record_id,
        "effective_from": r.effective_from,
        "effective_until": r.effective_until,
        "time_granularity": r.time_granularity,
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
    parent_record_id: str | None,
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
        record_id="",
        actor_id=actor.actor_id,
        authority_id=ADP010_AUTHORITY_ID,
        authority_version=ADP010_AUTHORITY_VERSION,
        registry_id=ADP010_REGISTRY_ID,
        registry_version=ADP010_REGISTRY_VERSION,
        rule_id=rule_id,
        rule_version=RULE_VERSION,
        realization_state=state,
        subject_ref=subject.subject_ref,
        parent_record_id=parent_record_id,
        effective_from=start,
        effective_until=end,
        time_granularity=granularity,
        source_candidate_id="",
        source_candidate_replay_hash="",
        context_or_world_receipt_refs=context,
        applicability_receipt_refs=applicability,
        phase_state_ref=actor.phase_state_ref,
        position_or_other_constraint_refs=constraints,
        causal_witness_refs=witnesses,
        rng_decision_receipt_ref=None,
        event_id=None,
        event_effect_kind=effect,
        prior_ledger_anchor_ref=prior,
        provenance_refs=provenance,
        record_hash="",
    )
    candidate_hash = _digest(_CANDIDATE_DOMAIN, _candidate_material(provisional))
    with_candidate = replace(
        provisional,
        source_candidate_id="urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash,
        source_candidate_replay_hash=candidate_hash,
    )
    record_hash = _digest(_RECORD_DOMAIN, _record_identity(with_candidate))
    event_id = None
    if effect is not None:
        event_hash = _digest(_EVENT_DOMAIN, {"record_hash": record_hash, "effect": effect})
        event_id = "urn:rawlsing:v3:oee:event:sha256:" + event_hash
    return replace(
        with_candidate,
        record_id="urn:rawlsing:v3:oee:record:sha256:" + record_hash,
        event_id=event_id,
        record_hash=record_hash,
    )

def _require_exact_provenance(provenance: tuple[ExactRef, ...], state: str) -> None:
    required = set(_required_fixed_provenance(state))
    if not required.issubset(set(provenance)):
        raise OEEIntegrityError("missing exact accepted ADP-010/008/020 provenance")

def _require_auth_ref(provenance: tuple[ExactRef, ...], kind: str, prefix: str) -> None:
    refs = tuple(r for r in provenance if r.kind == kind)
    if not refs:
        raise OEEIntegrityError(f"missing {kind}")
    for ref in refs:
        _validate_content_ref(ref, kind, prefix, kind)

def validate_record(record: Any) -> V3OEERealizationRecord:
    if not isinstance(record, V3OEERealizationRecord):
        raise OEEIntegrityError("record must be V3OEERealizationRecord")
    if (
        record.authority_id,
        record.authority_version,
        record.registry_id,
        record.registry_version,
    ) != (
        ADP010_AUTHORITY_ID,
        ADP010_AUTHORITY_VERSION,
        ADP010_REGISTRY_ID,
        ADP010_REGISTRY_VERSION,
    ):
        raise OEEIntegrityError("ADP-010 authority/registry mismatch")
    if record.realization_state not in _RULES:
        raise OEEIntegrityError("unsupported realization state")
    rule_id, _, _, effect = _RULES[record.realization_state]
    if (record.rule_id, record.rule_version) != (rule_id, RULE_VERSION):
        raise OEEIntegrityError("rule identity mismatch")

    _s(record.actor_id, "actor_id")
    _s(record.subject_ref, "subject_ref")
    _h(record.source_candidate_replay_hash, "source_candidate_replay_hash")
    phase = _ref(record.phase_state_ref, "phase_state_ref")
    if phase.kind != "V3DevelopmentalPhaseState":
        raise OEEIntegrityError("phase_state_ref kind mismatch")
    _ref(record.prior_ledger_anchor_ref, "prior_ledger_anchor_ref")
    context = _refs(record.context_or_world_receipt_refs, "context", True)
    apps = _refs(
        record.applicability_receipt_refs,
        "applicability",
        record.realization_state != STATE_AVAILABLE,
    )
    constraints = _refs(record.position_or_other_constraint_refs, "constraints")
    witnesses = _refs(record.causal_witness_refs, "witnesses", True)
    provenance = _refs(record.provenance_refs, "provenance", True)
    if (
        context != record.context_or_world_receipt_refs
        or apps != record.applicability_receipt_refs
        or constraints != record.position_or_other_constraint_refs
        or witnesses != record.causal_witness_refs
        or provenance != record.provenance_refs
    ):
        raise OEEIntegrityError("record refs are not canonical")
    _interval(record.effective_from, record.effective_until)
    _s(record.time_granularity, "time_granularity")
    if record.rng_decision_receipt_ref is not None:
        raise OEEIntegrityError("ADP-010 core-v1 is ZERO_DRAW")

    _require_exact_provenance(provenance, record.realization_state)
    _require_auth_ref(
        provenance,
        "SUBJECT_INGRESS_AUTHENTICATION",
        "urn:rawlsing:subject-ingress-authentication:sha256:",
    )
    _require_auth_ref(
        provenance,
        "ADP008_PHASE_STATE_AUTHENTICATION",
        "urn:rawlsing:adp008-phase-authentication:sha256:",
    )
    if record.realization_state != STATE_AVAILABLE:
        _require_auth_ref(
            provenance,
            "POSITIVE_APPLICABILITY_AUTHENTICATION",
            "urn:rawlsing:positive-applicability-authentication:sha256:",
        )
    if record.realization_state == STATE_ENCOUNTER:
        _require_auth_ref(
            provenance,
            "CONTACT_OCCURRENCE_AUTHENTICATION",
            "urn:rawlsing:contact-occurrence-authentication:sha256:",
        )
        _require_auth_ref(
            provenance,
            "CONTACT_INDEPENDENCE_AUTHENTICATION",
            "urn:rawlsing:contact-independence-authentication:sha256:",
        )
        kinds = {r.kind for r in witnesses}
        if CONTACT_WITNESS_KIND not in kinds or CONTACT_INDEPENDENCE_KIND not in kinds:
            raise OEEIntegrityError("ENCOUNTER record lacks exact contact/independence witness refs")
        if any(r.kind in _INSUFFICIENT_CONTACT for r in witnesses):
            raise OEEIntegrityError("insufficient proximity evidence cannot be ENCOUNTER witness")
    if record.realization_state == STATE_AVAILABLE:
        kinds = {r.kind for r in witnesses}
        if "SUBJECT_MATERIALIZATION_RECEIPT" not in kinds or "CAUSAL_USE_PERMISSION" not in kinds:
            raise OEEIntegrityError("AVAILABLE record lacks materialization/use witnesses")

    candidate_hash = _digest(_CANDIDATE_DOMAIN, _candidate_material(record))
    if record.source_candidate_replay_hash != candidate_hash:
        raise OEEIntegrityError("source candidate replay hash mismatch")
    if record.source_candidate_id != "urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash:
        raise OEEIntegrityError("source_candidate_id is not derived from candidate material")

    record_hash = _digest(_RECORD_DOMAIN, _record_identity(record))
    if record.record_hash != record_hash or record.record_id != "urn:rawlsing:v3:oee:record:sha256:" + record_hash:
        raise OEEIntegrityError("record identity/hash mismatch")
    event_id = None
    if effect is not None:
        event_hash = _digest(_EVENT_DOMAIN, {"record_hash": record_hash, "effect": effect})
        event_id = "urn:rawlsing:v3:oee:event:sha256:" + event_hash
    if (record.event_id, record.event_effect_kind) != (event_id, effect):
        raise OEEIntegrityError("event identity/effect mismatch")
    return record

class _Executor:
    def __init__(self, currentness: str) -> None:
        if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
            raise OEEIntegrityError("unsupported executor currentness")
        self.currentness = currentness

    def _parent(self, record: Any, expected_state: str, actor_id: str, subject_ref: str) -> V3OEERealizationRecord:
        record = validate_record(record)
        if record.realization_state != expected_state:
            raise OEEAdmissionError(f"expected {expected_state} parent")
        if record.actor_id != actor_id:
            raise OEEAdmissionError("parent actor continuity failure")
        if record.subject_ref != subject_ref:
            raise OEEAdmissionError("parent subject continuity failure")
        return record

    def admit_available(
        self,
        *,
        subject: SubjectIngressEvidence,
        actor: ActorPhaseEvidence,
        effective_from: str,
        effective_until: str,
        time_granularity: str,
        context_or_world_receipt_refs: Iterable[ExactRef],
        prior_ledger_anchor_ref: ExactRef,
        provenance_refs: Iterable[ExactRef],
    ) -> OEEExecutionResult:
        subject, subject_auth = _validate_subject(subject, self.currentness)
        actor, phase_auth = _validate_actor(actor, self.currentness)
        start, end = _interval(effective_from, effective_until)
        granularity = _s(time_granularity, "time_granularity")
        context = _refs(context_or_world_receipt_refs, "context", True)
        prior = _ref(prior_ledger_anchor_ref, "prior_ledger_anchor_ref")
        mat_ref = ExactRef(
            "SUBJECT_MATERIALIZATION_RECEIPT",
            subject.materialization_receipt.receipt_id,
            subject.materialization_receipt.receipt_hash,
        )
        witnesses = _refs(
            (mat_ref, subject.causal_use_permission.permission_ref),
            "available basis witnesses",
            True,
        )
        provenance = _merge(
            subject.provenance_refs,
            actor.provenance_refs,
            context,
            provenance_refs,
            (
                mat_ref,
                subject.causal_use_permission.permission_ref,
                actor.phase_state_ref,
                actor.phase_state_receipt_ref,
                prior,
                subject_auth,
                subject.causal_use_permission.authentication_ref,
                phase_auth,
            ),
            _required_fixed_provenance(STATE_AVAILABLE),
        )
        return OEEExecutionResult(
            _build(
                STATE_AVAILABLE,
                actor,
                subject,
                None,
                start,
                end,
                granularity,
                context,
                (),
                (),
                witnesses,
                prior,
                provenance,
            )
        )

    def admit_opportunity(
        self,
        *,
        parent_available: V3OEERealizationRecord,
        subject: SubjectIngressEvidence,
        actor: ActorPhaseEvidence,
        opportunity_basis: OpportunityBasisEvidence,
        effective_from: str,
        effective_until: str,
        time_granularity: str,
        prior_ledger_anchor_ref: ExactRef,
        provenance_refs: Iterable[ExactRef],
    ) -> OEEExecutionResult:
        subject, subject_auth = _validate_subject(subject, self.currentness)
        actor, phase_auth = _validate_actor(actor, self.currentness)
        parent = self._parent(parent_available, STATE_AVAILABLE, actor.actor_id, subject.subject_ref)
        basis = opportunity_basis
        if not isinstance(basis, OpportunityBasisEvidence):
            raise OEEIntegrityError("opportunity_basis must be OpportunityBasisEvidence")
        if basis.actor_id != actor.actor_id or basis.subject_ref != subject.subject_ref:
            raise OEEAdmissionError("opportunity basis actor/subject mismatch")
        _ref(basis.basis_ref, "basis_ref")
        context = _refs(basis.context_or_world_receipt_refs, "context", True)
        constraints = _refs(basis.position_or_other_constraint_refs, "constraints")
        _refs(basis.provenance_refs, "basis provenance", True)
        if not basis.applicability_receipts:
            raise OEEAdmissionError("opportunity requires positive applicability")
        app_refs: list[ExactRef] = []
        app_auths: list[ExactRef] = []
        for receipt in basis.applicability_receipts:
            ref, auth = _validate_app(receipt, self.currentness)
            app_refs.append(ref)
            app_auths.append(auth)
        apps = _refs(app_refs, "applicability", True)
        start, end = _interval(effective_from, effective_until)
        _within(start, end, parent)
        granularity = _s(time_granularity, "time_granularity")
        prior = _ref(prior_ledger_anchor_ref, "prior_ledger_anchor_ref")
        witnesses = _refs((basis.basis_ref,), "opportunity basis witnesses", True)
        provenance = _merge(
            parent.provenance_refs,
            subject.provenance_refs,
            actor.provenance_refs,
            basis.provenance_refs,
            *(receipt.provenance_refs for receipt in basis.applicability_receipts),
            context,
            constraints,
            provenance_refs,
            (
                basis.basis_ref,
                actor.phase_state_ref,
                actor.phase_state_receipt_ref,
                prior,
                subject_auth,
                phase_auth,
                *app_auths,
            ),
            _required_fixed_provenance(STATE_OPPORTUNITY),
        )
        return OEEExecutionResult(
            _build(
                STATE_OPPORTUNITY,
                actor,
                subject,
                parent.record_id,
                start,
                end,
                granularity,
                context,
                apps,
                constraints,
                witnesses,
                prior,
                provenance,
            )
        )

    def admit_encounter(
        self,
        *,
        parent_opportunity: V3OEERealizationRecord,
        subject: SubjectIngressEvidence,
        actor: ActorPhaseEvidence,
        contact_witness: ContactOccurrenceWitness,
        effective_time: str,
        time_granularity: str,
        prior_ledger_anchor_ref: ExactRef,
        declared_precondition_refs: Iterable[ExactRef],
        provenance_refs: Iterable[ExactRef],
    ) -> OEEExecutionResult:
        subject, subject_auth = _validate_subject(subject, self.currentness)
        actor, phase_auth = _validate_actor(actor, self.currentness)
        parent = self._parent(parent_opportunity, STATE_OPPORTUNITY, actor.actor_id, subject.subject_ref)
        t = _time(effective_time, "effective_time")
        _within(t, t, parent)
        granularity = _s(time_granularity, "time_granularity")
        witness, contact_auth, independence_auth = _validate_contact(
            contact_witness,
            actor.actor_id,
            subject.subject_ref,
            t,
            self.currentness,
        )
        preconditions = _refs(declared_precondition_refs, "preconditions", True)
        prior = _ref(prior_ledger_anchor_ref, "prior_ledger_anchor_ref")
        witnesses = _merge((witness.witness_ref, witness.independence_ref), preconditions)
        context = _refs(parent.context_or_world_receipt_refs, "context", True)
        apps = _refs(parent.applicability_receipt_refs, "applicability", True)
        constraints = _refs(parent.position_or_other_constraint_refs, "constraints")
        provenance = _merge(
            parent.provenance_refs,
            subject.provenance_refs,
            actor.provenance_refs,
            witness.provenance_refs,
            witness.contact_basis_refs,
            witness.independence_basis_refs,
            provenance_refs,
            witnesses,
            (
                actor.phase_state_ref,
                actor.phase_state_receipt_ref,
                prior,
                subject_auth,
                phase_auth,
                contact_auth,
                independence_auth,
            ),
            _required_fixed_provenance(STATE_ENCOUNTER),
        )
        return OEEExecutionResult(
            _build(
                STATE_ENCOUNTER,
                actor,
                subject,
                parent.record_id,
                t,
                t,
                granularity,
                context,
                apps,
                constraints,
                witnesses,
                prior,
                provenance,
            )
        )

_CURRENT_EXECUTOR = _Executor(CURRENT_ACCEPTED)
_NONCURRENT_TEST_EXECUTOR = _Executor(NONCURRENT_SYNTHETIC_TEST_ONLY)

def admit_available(**kwargs: Any) -> OEEExecutionResult:
    return _CURRENT_EXECUTOR.admit_available(**kwargs)

def admit_opportunity(**kwargs: Any) -> OEEExecutionResult:
    return _CURRENT_EXECUTOR.admit_opportunity(**kwargs)

def admit_encounter(**kwargs: Any) -> OEEExecutionResult:
    return _CURRENT_EXECUTOR.admit_encounter(**kwargs)

def _admit_available_noncurrent_for_test(**kwargs: Any) -> OEEExecutionResult:
    return _NONCURRENT_TEST_EXECUTOR.admit_available(**kwargs)

def _admit_opportunity_noncurrent_for_test(**kwargs: Any) -> OEEExecutionResult:
    return _NONCURRENT_TEST_EXECUTOR.admit_opportunity(**kwargs)

def _admit_encounter_noncurrent_for_test(**kwargs: Any) -> OEEExecutionResult:
    return _NONCURRENT_TEST_EXECUTOR.admit_encounter(**kwargs)

def validate_basis_available_opportunity_encounter_chain(
    records: Sequence[V3OEERealizationRecord],
) -> tuple[V3OEERealizationRecord, V3OEERealizationRecord, V3OEERealizationRecord]:
    if len(records) != 3:
        raise OEEAdmissionError("bounded chain must contain exactly AVAILABLE, OPPORTUNITY, ENCOUNTER")
    available, opportunity, encounter = (validate_record(r) for r in records)
    if [r.realization_state for r in (available, opportunity, encounter)] != [
        STATE_AVAILABLE,
        STATE_OPPORTUNITY,
        STATE_ENCOUNTER,
    ]:
        raise OEEAdmissionError("bounded chain state order invalid")
    if opportunity.parent_record_id != available.record_id or encounter.parent_record_id != opportunity.record_id:
        raise OEEAdmissionError("bounded chain parentage invalid")
    if len({r.actor_id for r in (available, opportunity, encounter)}) != 1:
        raise OEEAdmissionError("bounded chain actor continuity failure")
    if len({r.subject_ref for r in (available, opportunity, encounter)}) != 1:
        raise OEEAdmissionError("bounded chain subject continuity failure")
    return available, opportunity, encounter

def authority_identity_manifest() -> dict[str, Any]:
    return {
        "successor": {"executor_id": EXECUTOR_ID, "executor_version": EXECUTOR_VERSION},
        "ADP-010": {
            "authority_id": ADP010_AUTHORITY_ID,
            "authority_version": ADP010_AUTHORITY_VERSION,
            "registry_id": ADP010_REGISTRY_ID,
            "registry_version": ADP010_REGISTRY_VERSION,
            "artifact_blob_sha": ADP010_AUTHORITY_ARTIFACT_BLOB_SHA,
        },
        "ADP-008": {
            "authority_id": ADP008_AUTHORITY_ID,
            "authority_version": ADP008_AUTHORITY_VERSION,
            "registry_id": ADP008_REGISTRY_ID,
            "registry_version": ADP008_REGISTRY_VERSION,
            "artifact_blob_sha": ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
            "required_phase": DEVELOPMENT_ACTIVE_PHASE,
        },
        "ADP-020": {
            "authority_id": ADP020_AUTHORITY_ID,
            "authority_version": ADP020_AUTHORITY_VERSION,
            "artifact_blob_sha": ADP020_AUTHORITY_ARTIFACT_BLOB_SHA,
            "core_rule_rng": "ZERO_DRAW",
        },
        "OBL054": {
            "adoption_artifact_blob": OBL054_ADOPTION_ARTIFACT_BLOB,
            "materializer_id": OBL054_MATERIALIZER_ID,
            "materializer_version": OBL054_MATERIALIZER_VERSION,
            "accepted_root_hash": OBL054_ACCEPTED_ROOT_HASH,
            "permit_id": OBL054_PERMIT_ID,
            "permit_hash": OBL054_PERMIT_HASH,
            "historical_invalid_obl053_adoption_blob": HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB,
        },
        "historical_S3": {
            "semantic_candidate_sha": HISTORICAL_S3_SEMANTIC_CANDIDATE_SHA,
            "evidence_execution_sha": HISTORICAL_S3_EVIDENCE_EXECUTION_SHA,
            "module_blob_sha": HISTORICAL_S3_MODULE_BLOB_SHA,
            "test_blob_sha": HISTORICAL_S3_TEST_BLOB_SHA,
        },
    }

def _fixture_ref(kind: str, tag: str) -> ExactRef:
    h = sha256(tag.encode("utf-8")).hexdigest()
    return ExactRef(kind, f"urn:w2:synthetic:{tag}", h)

def _synthetic_materialization(tag: str = "subject") -> SubjectMaterializationReceipt:
    owner_id = "W2_SYNTHETIC_SUBJECT_OWNER"
    owner_version = "test-1"
    owner_hash = sha256((tag + ":owner").encode()).hexdigest()
    object_ref = _fixture_ref("SYNTHETIC_SEMANTIC_OBJECT", tag + ":object")
    evidence = (_fixture_ref("SYNTHETIC_EVIDENCE", tag + ":evidence"),)
    provenance = (_fixture_ref("SYNTHETIC_PROVENANCE", tag + ":provenance"),)
    dummy = SubjectMaterializationReceipt(
        receipt_id="",
        receipt_hash="0" * 64,
        subject_ref="",
        subject_ref_hash="0" * 64,
        materializer_id="W2_NONCURRENT_SYNTHETIC_MATERIALIZER",
        materializer_version="test-1",
        adoption_artifact_blob="1" * 40,
        accepted_owner_root_hash=sha256((tag + ":root").encode()).hexdigest(),
        materialization_permit_id="urn:w2:synthetic:permit:" + tag,
        materialization_permit_hash=sha256((tag + ":permit").encode()).hexdigest(),
        semantic_owner_authority_id=owner_id,
        semantic_owner_authority_version=owner_version,
        semantic_owner_authority_hash=owner_hash,
        semantic_object_ref=object_ref,
        owner_binding_content_hash="0" * 64,
        evidence_refs=evidence,
        provenance_refs=provenance,
        replay_input_hash="0" * 64,
        integrity_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
        semantic_owner_transfer=False,
        semantic_fields_interpreted=False,
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    owner_binding = _digest_bytes(MATERIALIZER_OWNER_BINDING_DOMAIN, _materializer_owner_material(dummy))
    with_owner = replace(dummy, owner_binding_content_hash=owner_binding)
    subject_material = _materializer_subject_material(with_owner)
    subject_hash = _digest_bytes(MATERIALIZER_SUBJECT_REF_DOMAIN, subject_material)
    subject_ref = "urn:rawlsing:v3:subject:sha256:" + subject_hash
    replay_hash = sha256(
        json.dumps(subject_material, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    with_subject = replace(
        with_owner,
        subject_ref=subject_ref,
        subject_ref_hash=subject_hash,
        replay_input_hash=replay_hash,
    )
    receipt_hash = _digest_bytes(MATERIALIZER_RECEIPT_DOMAIN, _materializer_receipt_body(with_subject))
    return replace(
        with_subject,
        receipt_hash=receipt_hash,
        receipt_id="urn:rawlsing:v3:authenticated-subject-materialization-receipt:sha256:" + receipt_hash,
    )

def _synthetic_subject(tag: str = "subject") -> SubjectIngressEvidence:
    m = _synthetic_materialization(tag)
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", m.receipt_id, m.receipt_hash)
    perm_authority_id = "W2_SYNTHETIC_CAUSAL_USE_OWNER"
    perm_authority_version = "test-1"
    perm_authority_hash = sha256((tag + ":causal-owner").encode()).hexdigest()
    perm_ref = _fixture_ref("CAUSAL_USE_PERMISSION", tag + ":causal-use")
    perm_accept = _authority_acceptance_ref(
        "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT",
        perm_authority_id,
        perm_authority_version,
        perm_authority_hash,
        NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    perm0 = CausalUsePermission(
        permission_ref=perm_ref,
        authority_id=perm_authority_id,
        authority_version=perm_authority_version,
        authority_content_hash=perm_authority_hash,
        authority_acceptance_ref=perm_accept,
        subject_ref=m.subject_ref,
        semantic_object_ref=m.semantic_object_ref,
        materialization_receipt_ref=mat_ref,
        scope="ADP010_CAUSAL_USE",
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", tag + ":causal-prov"),),
        authentication_ref=_fixture_ref("PLACEHOLDER", tag + ":perm-placeholder"),
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    perm = replace(
        perm0,
        authentication_ref=_content_ref(
            "CAUSAL_USE_PERMISSION_AUTHENTICATION",
            "urn:rawlsing:causal-use-authentication:sha256:",
            _permission_material(perm0),
        ),
    )
    s0 = SubjectIngressEvidence(
        subject_ref=m.subject_ref,
        semantic_owner_authority_id=m.semantic_owner_authority_id,
        semantic_owner_authority_version=m.semantic_owner_authority_version,
        semantic_owner_authority_content_hash=m.semantic_owner_authority_hash,
        semantic_object_ref=m.semantic_object_ref,
        materialization_receipt=m,
        obl054_adoption_artifact_blob="2" * 40,
        epistemic_class=EP_GENERATED_RUNTIME_FACT,
        causal_use_permission=perm,
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", tag + ":subject-prov"),),
        authentication_ref=_fixture_ref("PLACEHOLDER", tag + ":subject-placeholder"),
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    return replace(
        s0,
        authentication_ref=_content_ref(
            "SUBJECT_INGRESS_AUTHENTICATION",
            "urn:rawlsing:subject-ingress-authentication:sha256:",
            _subject_material(s0),
        ),
    )

def _synthetic_actor(tag: str = "actor", phase_tag: str = "phase") -> ActorPhaseEvidence:
    a0 = ActorPhaseEvidence(
        actor_id="urn:w2:synthetic:actor:" + tag,
        phase_state_ref=_fixture_ref("V3DevelopmentalPhaseState", tag + ":" + phase_tag + ":state"),
        phase_state_receipt_ref=_fixture_ref("V3DevelopmentalPhaseStateReceipt", tag + ":" + phase_tag + ":receipt"),
        phase_authority_id=ADP008_AUTHORITY_ID,
        phase_authority_version=ADP008_AUTHORITY_VERSION,
        phase_authority_artifact_blob_sha=ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
        phase_registry_id=ADP008_REGISTRY_ID,
        phase_registry_version=ADP008_REGISTRY_VERSION,
        phase_registry_content_hash=ADP008_REGISTRY_CONTENT_HASH,
        base_phase_id=DEVELOPMENT_ACTIVE_PHASE,
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", tag + ":" + phase_tag + ":phase-prov"),),
        authentication_ref=_fixture_ref("PLACEHOLDER", tag + ":phase-placeholder"),
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    return replace(
        a0,
        authentication_ref=_content_ref(
            "ADP008_PHASE_STATE_AUTHENTICATION",
            "urn:rawlsing:adp008-phase-authentication:sha256:",
            _phase_material(a0),
        ),
    )

def _synthetic_app(tag: str = "app", authority_tag: str = "owner") -> PositiveApplicabilityReceipt:
    authority_id = "W2_SYNTHETIC_APPLICABILITY_" + authority_tag
    authority_version = "test-1"
    authority_hash = sha256((tag + ":" + authority_tag).encode()).hexdigest()
    a0 = PositiveApplicabilityReceipt(
        receipt=_fixture_ref("POSITIVE_APPLICABILITY_RECEIPT", tag + ":receipt"),
        authority_id=authority_id,
        authority_version=authority_version,
        authority_content_hash=authority_hash,
        authority_acceptance_ref=_authority_acceptance_ref(
            "ACCEPTED_APPLICABILITY_AUTHORITY_RECEIPT",
            authority_id,
            authority_version,
            authority_hash,
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ),
        result="POSITIVE",
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", tag + ":app-prov"),),
        authentication_ref=_fixture_ref("PLACEHOLDER", tag + ":app-placeholder"),
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    return replace(
        a0,
        authentication_ref=_content_ref(
            "POSITIVE_APPLICABILITY_AUTHENTICATION",
            "urn:rawlsing:positive-applicability-authentication:sha256:",
            _app_material(a0),
        ),
    )

def _synthetic_basis(subject: SubjectIngressEvidence, actor: ActorPhaseEvidence, app: PositiveApplicabilityReceipt | None = None) -> OpportunityBasisEvidence:
    return OpportunityBasisEvidence(
        basis_ref=_fixture_ref("ACTOR_SPECIFIC_OPPORTUNITY_BASIS", "basis"),
        actor_id=actor.actor_id,
        subject_ref=subject.subject_ref,
        applicability_receipts=(app or _synthetic_app(),),
        context_or_world_receipt_refs=(
            _fixture_ref("WORLD_RECEIPT", "world"),
            _fixture_ref("CONTEXT_RECEIPT", "context"),
        ),
        position_or_other_constraint_refs=(_fixture_ref("CONSTRAINT_RECEIPT", "constraint"),),
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", "basis-prov"),),
    )

def _synthetic_contact(
    subject: SubjectIngressEvidence,
    actor: ActorPhaseEvidence,
    authority_tag: str = "owner",
    contact_basis: tuple[ExactRef, ...] | None = None,
    independence_basis: tuple[ExactRef, ...] | None = None,
    witness_kind: str = CONTACT_WITNESS_KIND,
    semantic: str = CONTACT_OCCURRENCE_SEMANTIC,
    occurrence_time: str = "2031-01-01T12:00:00Z",
) -> ContactOccurrenceWitness:
    contact_id = "W2_SYNTHETIC_CONTACT_" + authority_tag
    contact_version = "test-1"
    contact_hash = sha256(("contact:" + authority_tag).encode()).hexdigest()
    ind_id = "W2_SYNTHETIC_INDEPENDENCE_" + authority_tag
    ind_version = "test-1"
    ind_hash = sha256(("ind:" + authority_tag).encode()).hexdigest()
    w0 = ContactOccurrenceWitness(
        witness_ref=_fixture_ref(witness_kind, "contact-witness"),
        witness_authority_id=contact_id,
        witness_authority_version=contact_version,
        witness_authority_content_hash=contact_hash,
        witness_authority_acceptance_ref=_authority_acceptance_ref(
            "ACCEPTED_CONTACT_OCCURRENCE_AUTHORITY_RECEIPT",
            contact_id,
            contact_version,
            contact_hash,
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ),
        actor_id=actor.actor_id,
        subject_ref=subject.subject_ref,
        occurrence_time=occurrence_time,
        semantic=semantic,
        contact_basis_refs=contact_basis or (_fixture_ref("DIRECT_CONTACT_OBSERVATION", "contact-basis"),),
        contact_authentication_ref=_fixture_ref("PLACEHOLDER", "contact-auth-placeholder"),
        independence_ref=_fixture_ref(CONTACT_INDEPENDENCE_KIND, "contact-independence"),
        independence_authority_id=ind_id,
        independence_authority_version=ind_version,
        independence_authority_content_hash=ind_hash,
        independence_authority_acceptance_ref=_authority_acceptance_ref(
            "ACCEPTED_CONTACT_INDEPENDENCE_AUTHORITY_RECEIPT",
            ind_id,
            ind_version,
            ind_hash,
            NONCURRENT_SYNTHETIC_TEST_ONLY,
        ),
        independence_receipt_ref=_fixture_ref("CONTACT_WITNESS_INDEPENDENCE_RECEIPT", "contact-independence-receipt"),
        independence_basis_refs=independence_basis or (_fixture_ref("INDEPENDENT_OBSERVER_CHAIN", "ind-basis"),),
        independence_authentication_ref=_fixture_ref("PLACEHOLDER", "ind-auth-placeholder"),
        provenance_refs=(_fixture_ref("SYNTHETIC_PROVENANCE", "contact-prov"),),
        currentness_state=NONCURRENT_SYNTHETIC_TEST_ONLY,
    )
    contact_auth = _content_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        "urn:rawlsing:contact-occurrence-authentication:sha256:",
        _contact_material(w0),
    )
    w1 = replace(w0, contact_authentication_ref=contact_auth)
    ind_auth = _content_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        "urn:rawlsing:contact-independence-authentication:sha256:",
        _independence_material(w1, contact_auth),
    )
    return replace(w1, independence_authentication_ref=ind_auth)

__all__ = [
    "EXECUTOR_ID",
    "EXECUTOR_VERSION",
    "ADP010_AUTHORITY_ID",
    "ADP010_AUTHORITY_VERSION",
    "ADP010_REGISTRY_ID",
    "ADP010_REGISTRY_VERSION",
    "ADP010_AUTHORITY_ARTIFACT_BLOB_SHA",
    "ADP008_AUTHORITY_ID",
    "ADP008_AUTHORITY_VERSION",
    "ADP008_REGISTRY_ID",
    "ADP008_REGISTRY_VERSION",
    "ADP008_AUTHORITY_ARTIFACT_BLOB_SHA",
    "ADP020_AUTHORITY_ID",
    "ADP020_AUTHORITY_VERSION",
    "ADP020_AUTHORITY_ARTIFACT_BLOB_SHA",
    "OBL054_ADOPTION_ARTIFACT_BLOB",
    "OBL054_MATERIALIZER_ID",
    "OBL054_MATERIALIZER_VERSION",
    "OBL054_ACCEPTED_ROOT_HASH",
    "OBL054_PERMIT_ID",
    "OBL054_PERMIT_HASH",
    "HISTORICAL_INVALID_OBL053_ADOPTION_ARTIFACT_BLOB",
    "DEVELOPMENT_ACTIVE_PHASE",
    "STATE_AVAILABLE",
    "STATE_OPPORTUNITY",
    "STATE_ENCOUNTER",
    "EFFECT_OPPORTUNITY",
    "EFFECT_ENCOUNTER",
    "CONTACT_WITNESS_KIND",
    "CONTACT_INDEPENDENCE_KIND",
    "CONTACT_OCCURRENCE_SEMANTIC",
    "EP_GENERATED_RUNTIME_FACT",
    "EP_RESOLVER_CONTEXT",
    "EP_ADMITTED_CAUSAL_EVENT",
    "ExactRef",
    "SubjectMaterializationReceipt",
    "CausalUsePermission",
    "SubjectIngressEvidence",
    "ActorPhaseEvidence",
    "PositiveApplicabilityReceipt",
    "OpportunityBasisEvidence",
    "ContactOccurrenceWitness",
    "V3OEERealizationRecord",
    "OEEExecutionResult",
    "OEEAdmissionError",
    "OEEIntegrityError",
    "admit_available",
    "admit_opportunity",
    "admit_encounter",
    "validate_record",
    "validate_basis_available_opportunity_encounter_chain",
    "authority_identity_manifest",
]
