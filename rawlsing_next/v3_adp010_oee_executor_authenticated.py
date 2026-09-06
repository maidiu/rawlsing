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
class Posit