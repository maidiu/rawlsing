"""GT34 OBL055 bounded W2 successor consuming HQ-current OBL056 acceptance receipts.

This module is a distinct successor.  It deliberately leaves the frozen W2 module
untouched and delegates only W2's lawful AVAILABLE -> OPPORTUNITY -> ENCOUNTER
transition machinery.  Authority competence is no longer self-issued by the
executor: each ADP-010 semantic input role must carry a separately issued OBL056
acceptance receipt.  The presently installed OBL056 registry remains zero-positive,
so current-positive execution fails closed.

No subject/contact/applicability semantic proposition is created here.  OBL056
receipts prove only that an already-existing source authority is accepted for an
exact role/scope.  Underlying semantic evidence remains source-owned.
"""
from __future__ import annotations

from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import asdict, replace
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Sequence

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_authenticated as w2


EXECUTOR_ID = "GT34_V3P5_ADP010_OBL056_ACCEPTANCE_BOUND_REPLAY_EXECUTOR"
EXECUTOR_VERSION = "3.0.0"
FROZEN_W2_EXECUTOR_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"
HQ_OBL056_ADOPTION_REF = "9ecae8c4a499dddb364c633b581e9e4d68ad3540"
HQ_OBL056_IMPLEMENTATION_BLOB = "49538b9c36e58e19a6dc293ecac5bc2dff58eebe"
HQ_OBL056_AUTHORITY_HASH = "6c9ab99a7d89835e7fdf405511abd7d6d66ced54b6e2fd8ef1863be842f39123"
HQ_OBL056_EMPTY_REGISTRY_HASH = "ca633451bfe56f86e1b463243bf721772a9ff582227411ed5137a346491b957e"

if acceptance.ACCEPTANCE_AUTHORITY_CONTENT_HASH != HQ_OBL056_AUTHORITY_HASH:
    raise RuntimeError("OBL056 authority hash drift")
if acceptance.REGISTRY_CONTENT_HASH != HQ_OBL056_EMPTY_REGISTRY_HASH:
    raise RuntimeError("OBL056 installed registry hash drift")

# Preserve the exact W2 record/input contracts and error taxonomy.
ExactRef = w2.ExactRef
SubjectMaterializationReceipt = w2.SubjectMaterializationReceipt
CausalUsePermission = w2.CausalUsePermission
SubjectIngressEvidence = w2.SubjectIngressEvidence
ActorPhaseEvidence = w2.ActorPhaseEvidence
PositiveApplicabilityReceipt = w2.PositiveApplicabilityReceipt
OpportunityBasisEvidence = w2.OpportunityBasisEvidence
ContactOccurrenceWitness = w2.ContactOccurrenceWitness
V3OEERealizationRecord = w2.V3OEERealizationRecord
OEEExecutionResult = w2.OEEExecutionResult
OEEAdmissionError = w2.OEEAdmissionError
OEEIntegrityError = w2.OEEIntegrityError

CURRENT_ACCEPTED = w2.CURRENT_ACCEPTED
NONCURRENT_SYNTHETIC_TEST_ONLY = w2.NONCURRENT_SYNTHETIC_TEST_ONLY
STATE_AVAILABLE = w2.STATE_AVAILABLE
STATE_OPPORTUNITY = w2.STATE_OPPORTUNITY
STATE_ENCOUNTER = w2.STATE_ENCOUNTER
EFFECT_OPPORTUNITY = w2.EFFECT_OPPORTUNITY
EFFECT_ENCOUNTER = w2.EFFECT_ENCOUNTER

_ROLE_TRANSITION = {
    acceptance.CAUSAL_USE_PERMISSION: "BASIS_TO_AVAILABLE:ADP010_CAUSAL_USE",
    acceptance.POSITIVE_APPLICABILITY: "AVAILABLE_TO_OPPORTUNITY:POSITIVE_APPLICABILITY",
    acceptance.CONTACT_OCCURRENCE_WITNESS: "OPPORTUNITY_TO_ENCOUNTER:CONTACT_OCCURRENCE_WITNESS",
    acceptance.CONTACT_WITNESS_INDEPENDENCE: "OPPORTUNITY_TO_ENCOUNTER:CONTACT_WITNESS_INDEPENDENCE",
}
_BINDING_SCHEMA = "GT34_OBL055_OBL056_ACCEPTANCE_REPLAY_BINDING@1.0.0"
_PHASE_SCHEMA = "GT34_OBL055_ADP008_PHASE_REPLAY_BINDING@1.0.0"
_SUBJECT_SCHEMA = "GT34_OBL055_SUBJECT_INGRESS_REPLAY_BINDING@1.0.0"
_MANIFEST_DOMAIN = "RAWLSING\0GT34\0OBL055\0ACCEPTANCE_BOUND_REPLAY_V1\0"
_MANIFEST_PREFIX = "urn:rawlsing:gt34:obl055:replay-manifest:"


class OBL055AcceptanceError(OEEAdmissionError):
    pass


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(label: str, value: Any) -> str:
    return sha256((_MANIFEST_DOMAIN + label + "\0" + _canonical(value)).encode("utf-8")).hexdigest()


def _ref_dict(ref: ExactRef) -> dict[str, str]:
    return {"kind": ref.kind, "ref": ref.ref, "content_hash": ref.content_hash}


def _ref_from_dict(value: Mapping[str, Any]) -> ExactRef:
    return ExactRef(str(value["kind"]), str(value["ref"]), str(value["content_hash"]))


def _ev_exact(kind: str, ref: acceptance.EvidenceRef) -> ExactRef:
    return ExactRef(kind, ref.ref, ref.content_hash)


def _authority_exact(kind: str, ref: acceptance.ContentAddressedRef) -> ExactRef:
    return ExactRef(kind, f"urn:rawlsing:authority:{ref.id}@{ref.version}", ref.content_hash)


def _receipt_exact(role: str, receipt: acceptance.AcceptanceReceipt) -> ExactRef:
    return ExactRef("OBL056_ACCEPTANCE_RECEIPT_" + role, receipt.receipt_id, receipt.receipt_hash)


def _manifest(kind: str, payload: Mapping[str, Any]) -> ExactRef:
    body = dict(payload)
    raw = _canonical(body).encode("utf-8")
    token = urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    h = _digest(kind, body)
    return ExactRef(kind, _MANIFEST_PREFIX + kind.lower() + ":" + token, h)


def _decode_manifest(ref: ExactRef, expected_kind: str) -> dict[str, Any]:
    w2._ref(ref, expected_kind)
    if ref.kind != expected_kind:
        raise OEEIntegrityError(f"expected {expected_kind}")
    prefix = _MANIFEST_PREFIX + expected_kind.lower() + ":"
    if not ref.ref.startswith(prefix):
        raise OEEIntegrityError(f"{expected_kind} replay-manifest prefix mismatch")
    token = ref.ref[len(prefix):]
    token += "=" * ((4 - len(token) % 4) % 4)
    try:
        body = json.loads(urlsafe_b64decode(token.encode("ascii")).decode("utf-8"))
    except Exception as exc:
        raise OEEIntegrityError(f"{expected_kind} replay-manifest decode failure") from exc
    if not isinstance(body, dict) or ref.content_hash != _digest(expected_kind, body):
        raise OEEIntegrityError(f"{expected_kind} replay-manifest hash mismatch")
    if _manifest(expected_kind, body) != ref:
        raise OEEIntegrityError(f"{expected_kind} replay-manifest is not canonical")
    return body


def _fixed_ref(kind: str, ref: str, hash_value: str) -> ExactRef:
    return ExactRef(kind, ref, hash_value)


OBL056_ACCEPTANCE_AUTHORITY_HASH_REF = _fixed_ref(
    "OBL056_ACCEPTANCE_AUTHORITY_HASH",
    f"urn:rawlsing:gt34:obl056:authority:{acceptance.ACCEPTANCE_AUTHORITY_ID}@{acceptance.ACCEPTANCE_AUTHORITY_VERSION}",
    HQ_OBL056_AUTHORITY_HASH,
)
OBL056_ACCEPTANCE_REGISTRY_HASH_REF = _fixed_ref(
    "OBL056_ACCEPTANCE_REGISTRY_HASH",
    f"urn:rawlsing:gt34:obl056:registry:{acceptance.REGISTRY_ID}@{acceptance.REGISTRY_VERSION}",
    HQ_OBL056_EMPTY_REGISTRY_HASH,
)
OBL056_ACCEPTANCE_RULE_HASH = _digest(
    "OBL056_RULE",
    {
        "receipt_schema": acceptance.RECEIPT_SCHEMA_ID,
        "consumer": acceptance.CONSUMER,
        "roles": list(acceptance.SUPPORTED_ROLES),
        "authority_ceiling": list(acceptance.AUTHORITY_CEILING),
    },
)
OBL056_ACCEPTANCE_RULE_HASH_REF = _fixed_ref(
    "OBL056_ACCEPTANCE_RULE_HASH",
    "urn:rawlsing:gt34:obl056:acceptance-binding-rule@1.0.0",
    OBL056_ACCEPTANCE_RULE_HASH,
)
OBL056_HQ_ADOPTION_HASH = _digest(
    "HQ_ADOPTION",
    [HQ_OBL056_ADOPTION_REF, HQ_OBL056_AUTHORITY_HASH, HQ_OBL056_IMPLEMENTATION_BLOB, HQ_OBL056_EMPTY_REGISTRY_HASH],
)
OBL056_HQ_ADOPTION_PROVENANCE_REF = _fixed_ref(
    "OBL056_HQ_ADOPTION_PROVENANCE",
    "urn:rawlsing:git-commit:" + HQ_OBL056_ADOPTION_REF,
    OBL056_HQ_ADOPTION_HASH,
)
SUCCESSOR_EXECUTOR_HASH = _digest(
    "SUCCESSOR_EXECUTOR",
    [EXECUTOR_ID, EXECUTOR_VERSION, FROZEN_W2_EXECUTOR_BLOB, HQ_OBL056_AUTHORITY_HASH, HQ_OBL056_IMPLEMENTATION_BLOB],
)
SUCCESSOR_EXECUTOR_REF = _fixed_ref(
    "OBL055_SUCCESSOR_EXECUTOR",
    f"urn:rawlsing:gt34:obl055:executor:{EXECUTOR_ID}@{EXECUTOR_VERSION}",
    SUCCESSOR_EXECUTOR_HASH,
)
_FIXED_PROVENANCE = tuple(sorted((
    OBL056_ACCEPTANCE_AUTHORITY_HASH_REF,
    OBL056_ACCEPTANCE_REGISTRY_HASH_REF,
    OBL056_ACCEPTANCE_RULE_HASH_REF,
    OBL056_HQ_ADOPTION_PROVENANCE_REF,
    SUCCESSOR_EXECUTOR_REF,
)))


def _scope_current_grain(receipt: acceptance.AcceptanceReceipt, subject_ref: str, object_ref: ExactRef) -> None:
    if receipt.scope.transition_use_scope != _ROLE_TRANSITION[receipt.role]:
        raise OBL055AcceptanceError("OBL056 receipt transition/use scope mismatch")
    if receipt.currentness_state == CURRENT_ACCEPTED:
        if tuple(receipt.scope.subject_scope) != (subject_ref,):
            raise OBL055AcceptanceError("current OBL056 receipt must bind exact subject scope")
        if tuple(receipt.scope.object_scope) != (object_ref.ref,):
            raise OBL055AcceptanceError("current OBL056 receipt must bind exact object scope")


def _validate_acceptance(
    receipt: acceptance.AcceptanceReceipt,
    *,
    role: str,
    authority_id: str,
    authority_version: str,
    authority_hash: str,
    subject_ref: str,
    object_ref: ExactRef,
    currentness: str,
) -> acceptance.AcceptanceReceipt:
    expected_authority = acceptance.ContentAddressedRef(authority_id, authority_version, authority_hash)
    try:
        out = acceptance.validate_acceptance_receipt(
            receipt,
            expected_role=role,
            expected_accepted_authority_ref=expected_authority,
            expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
            expected_scope=receipt.scope,
            required_currentness=currentness,
        )
    except acceptance.AcceptanceAuthorityError as exc:
        raise OBL055AcceptanceError(f"OBL056 acceptance failed for {role}: {exc}") from exc
    _scope_current_grain(out, subject_ref, object_ref)
    return out


def _binding_payload(
    *,
    receipt: acceptance.AcceptanceReceipt,
    subject_ref: str,
    object_ref: ExactRef,
    semantic_ref: ExactRef,
    evidence_auth_ref: ExactRef,
    auxiliary_ref: ExactRef | None = None,
) -> dict[str, Any]:
    return {
        "schema_id": _BINDING_SCHEMA,
        "role": receipt.role,
        "receipt": asdict(receipt),
        "subject_ref": subject_ref,
        "semantic_object_ref": _ref_dict(object_ref),
        "semantic_evidence_ref": _ref_dict(semantic_ref),
        "evidence_authentication_ref": _ref_dict(evidence_auth_ref),
        "auxiliary_ref": None if auxiliary_ref is None else _ref_dict(auxiliary_ref),
    }


def _binding_refs(
    receipt: acceptance.AcceptanceReceipt,
    *,
    subject_ref: str,
    object_ref: ExactRef,
    semantic_ref: ExactRef,
    evidence_auth_ref: ExactRef,
    auxiliary_ref: ExactRef | None = None,
) -> tuple[ExactRef, ...]:
    role = receipt.role
    manifest = _manifest(
        "OBL056_ACCEPTANCE_BINDING_" + role,
        _binding_payload(
            receipt=receipt,
            subject_ref=subject_ref,
            object_ref=object_ref,
            semantic_ref=semantic_ref,
            evidence_auth_ref=evidence_auth_ref,
            auxiliary_ref=auxiliary_ref,
        ),
    )
    refs = [
        manifest,
        _receipt_exact(role, receipt),
        _authority_exact("OBL056_ACCEPTED_AUTHORITY_" + role, receipt.accepted_authority_ref),
        _ev_exact("OBL056_ACCEPTED_OWNER_" + role, receipt.accepted_authority_owner_jurisdiction_ref),
        _ev_exact("OBL056_SOURCE_ACCEPTANCE_EVIDENCE_" + role, receipt.source_acceptance_evidence_ref),
        semantic_ref,
        evidence_auth_ref,
    ]
    if auxiliary_ref is not None:
        refs.append(auxiliary_ref)
    return tuple(sorted(set(refs)))


def _phase_manifest(actor: ActorPhaseEvidence, phase_auth: ExactRef, currentness: str) -> ExactRef:
    return _manifest(
        "OBL055_ADP008_PHASE_REPLAY_BINDING",
        {
            "schema_id": _PHASE_SCHEMA,
            "currentness_state": currentness,
            "actor_id": actor.actor_id,
            "phase_state_ref": _ref_dict(actor.phase_state_ref),
            "phase_state_receipt_ref": _ref_dict(actor.phase_state_receipt_ref),
            "phase_authentication_ref": _ref_dict(phase_auth),
            "phase_authority": [actor.phase_authority_id, actor.phase_authority_version, actor.phase_authority_artifact_blob_sha],
            "phase_registry": [actor.phase_registry_id, actor.phase_registry_version, actor.phase_registry_content_hash],
            "base_phase_id": actor.base_phase_id,
        },
    )


def _subject_manifest(
    subject: SubjectIngressEvidence,
    subject_auth: ExactRef,
    causal_binding: ExactRef,
    currentness: str,
) -> ExactRef:
    mat = subject.materialization_receipt
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", mat.receipt_id, mat.receipt_hash)
    return _manifest(
        "OBL055_SUBJECT_INGRESS_REPLAY_BINDING",
        {
            "schema_id": _SUBJECT_SCHEMA,
            "currentness_state": currentness,
            "subject_ref": subject.subject_ref,
            "semantic_object_ref": _ref_dict(subject.semantic_object_ref),
            "materialization_receipt_ref": _ref_dict(mat_ref),
            "causal_use_permission_ref": _ref_dict(subject.causal_use_permission.permission_ref),
            "subject_authentication_ref": _ref_dict(subject_auth),
            "causal_use_authentication_ref": _ref_dict(subject.causal_use_permission.authentication_ref),
            "causal_acceptance_binding_ref": _ref_dict(causal_binding),
            "obl054_adoption_artifact_blob": subject.obl054_adoption_artifact_blob,
        },
    )


def _binding_manifest(refs: Iterable[ExactRef], role: str) -> ExactRef:
    matches = tuple(r for r in refs if r.kind == "OBL056_ACCEPTANCE_BINDING_" + role)
    if len(matches) != 1:
        raise OEEIntegrityError(f"expected exactly one {role} acceptance binding")
    return matches[0]


def _receipt_from_dict(value: Mapping[str, Any]) -> acceptance.AcceptanceReceipt:
    def car(x: Mapping[str, Any]) -> acceptance.ContentAddressedRef:
        return acceptance.ContentAddressedRef(str(x["id"]), str(x["version"]), str(x["content_hash"]))
    def ev(x: Mapping[str, Any]) -> acceptance.EvidenceRef:
        return acceptance.EvidenceRef(str(x["ref"]), str(x["content_hash"]))
    scope_raw = value["scope"]
    scope = acceptance.AcceptanceScope(
        str(scope_raw["transition_use_scope"]),
        tuple(scope_raw.get("family_scope", ())),
        tuple(scope_raw.get("subject_scope", ())),
        tuple(scope_raw.get("object_scope", ())),
    )
    return acceptance.AcceptanceReceipt(
        schema_id=str(value["schema_id"]),
        acceptance_authority_ref=car(value["acceptance_authority_ref"]),
        registry_ref=car(value["registry_ref"]),
        registry_entry_ref=ev(value["registry_entry_ref"]),
        role=str(value["role"]),
        accepted_authority_ref=car(value["accepted_authority_ref"]),
        accepted_authority_owner_jurisdiction_ref=ev(value["accepted_authority_owner_jurisdiction_ref"]),
        source_acceptance_evidence_ref=ev(value["source_acceptance_evidence_ref"]),
        decision_state=str(value["decision_state"]),
        consumer=str(value["consumer"]),
        scope=scope,
        negative_limit_refs=tuple(ev(x) for x in value.get("negative_limit_refs", ())),
        currentness_state=str(value["currentness_state"]),
        immutable_provenance=tuple(ev(x) for x in value.get("immutable_provenance", ())),
        receipt_id=str(value["receipt_id"]),
        receipt_hash=str(value["receipt_hash"]),
    )


def _validate_binding_manifest(
    ref: ExactRef,
    *,
    record: V3OEERealizationRecord,
    expected_role: str,
    object_ref: ExactRef,
) -> acceptance.AcceptanceReceipt:
    body = _decode_manifest(ref, "OBL056_ACCEPTANCE_BINDING_" + expected_role)
    if body.get("schema_id") != _BINDING_SCHEMA or body.get("role") != expected_role:
        raise OEEIntegrityError("OBL056 acceptance binding schema/role mismatch")
    if body.get("subject_ref") != record.subject_ref:
        raise OEEIntegrityError("OBL056 acceptance binding subject mismatch")
    if _ref_from_dict(body["semantic_object_ref"]) != object_ref:
        raise OEEIntegrityError("OBL056 acceptance binding semantic object mismatch")
    semantic_ref = _ref_from_dict(body["semantic_evidence_ref"])
    auth_ref = _ref_from_dict(body["evidence_authentication_ref"])
    auxiliary = body.get("auxiliary_ref")
    auxiliary_ref = None if auxiliary is None else _ref_from_dict(auxiliary)
    provenance = set(record.provenance_refs)
    if auth_ref not in provenance or semantic_ref not in provenance:
        raise OEEIntegrityError("acceptance replay evidence/authentication ref missing from provenance")
    if auxiliary_ref is not None and auxiliary_ref not in provenance:
        raise OEEIntegrityError("acceptance replay auxiliary ref missing from provenance")
    receipt = _receipt_from_dict(body["receipt"])
    expected_authority = receipt.accepted_authority_ref
    try:
        acceptance.validate_acceptance_receipt(
            receipt,
            expected_role=expected_role,
            expected_accepted_authority_ref=expected_authority,
            expected_owner_jurisdiction_ref=receipt.accepted_authority_owner_jurisdiction_ref,
            expected_source_acceptance_evidence_ref=receipt.source_acceptance_evidence_ref,
            expected_scope=receipt.scope,
            required_currentness=receipt.currentness_state,
        )
    except acceptance.AcceptanceAuthorityError as exc:
        raise OEEIntegrityError(f"stored OBL056 acceptance receipt no longer validates: {exc}") from exc
    _scope_current_grain(receipt, record.subject_ref, object_ref)
    expected_refs = set(_binding_refs(
        receipt,
        subject_ref=record.subject_ref,
        object_ref=object_ref,
        semantic_ref=semantic_ref,
        evidence_auth_ref=auth_ref,
        auxiliary_ref=auxiliary_ref,
    ))
    if not expected_refs.issubset(provenance):
        raise OEEIntegrityError("stored OBL056 acceptance binding constituents incomplete")
    return receipt


def _single_manifest(record: V3OEERealizationRecord, kind: str) -> dict[str, Any]:
    refs = tuple(r for r in record.provenance_refs if r.kind == kind)
    if len(refs) != 1:
        raise OEEIntegrityError(f"expected exactly one {kind}")
    return _decode_manifest(refs[0], kind)


def validate_record(record: Any) -> V3OEERealizationRecord:
    record = w2.validate_record(record)
    provenance = set(record.provenance_refs)
    if not set(_FIXED_PROVENANCE).issubset(provenance):
        raise OEEIntegrityError("missing exact HQ-current OBL056/successor provenance")

    phase = _single_manifest(record, "OBL055_ADP008_PHASE_REPLAY_BINDING")
    if phase.get("schema_id") != _PHASE_SCHEMA or phase.get("actor_id") != record.actor_id:
        raise OEEIntegrityError("ADP-008 phase replay actor/schema mismatch")
    if _ref_from_dict(phase["phase_state_ref"]) != record.phase_state_ref:
        raise OEEIntegrityError("ADP-008 phase replay state mismatch")
    if tuple(phase.get("phase_authority", ())) != (
        w2.ADP008_AUTHORITY_ID, w2.ADP008_AUTHORITY_VERSION, w2.ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,
    ):
        raise OEEIntegrityError("ADP-008 phase replay authority mismatch")
    if tuple(phase.get("phase_registry", ())) != (
        w2.ADP008_REGISTRY_ID, w2.ADP008_REGISTRY_VERSION, w2.ADP008_REGISTRY_CONTENT_HASH,
    ) or phase.get("base_phase_id") != w2.DEVELOPMENT_ACTIVE_PHASE:
        raise OEEIntegrityError("ADP-008 phase replay registry/base-phase mismatch")
    for key in ("phase_state_receipt_ref", "phase_authentication_ref"):
        if _ref_from_dict(phase[key]) not in provenance:
            raise OEEIntegrityError("ADP-008 phase replay constituent missing")

    subject = _single_manifest(record, "OBL055_SUBJECT_INGRESS_REPLAY_BINDING")
    if subject.get("schema_id") != _SUBJECT_SCHEMA or subject.get("subject_ref") != record.subject_ref:
        raise OEEIntegrityError("subject ingress replay identity mismatch")
    object_ref = _ref_from_dict(subject["semantic_object_ref"])
    for key in ("materialization_receipt_ref", "causal_use_permission_ref", "subject_authentication_ref", "causal_use_authentication_ref"):
        if _ref_from_dict(subject[key]) not in provenance:
            raise OEEIntegrityError("subject ingress replay constituent missing")

    role_refs: dict[str, list[ExactRef]] = {role: [] for role in acceptance.SUPPORTED_ROLES}
    for role in acceptance.SUPPORTED_ROLES:
        role_refs[role] = [r for r in record.provenance_refs if r.kind == "OBL056_ACCEPTANCE_BINDING_" + role]

    if len(role_refs[acceptance.CAUSAL_USE_PERMISSION]) != 1:
        raise OEEIntegrityError("record lacks exact causal-use OBL056 acceptance binding")
    causal_binding_ref = role_refs[acceptance.CAUSAL_USE_PERMISSION][0]
    if _ref_from_dict(subject["causal_acceptance_binding_ref"]) != causal_binding_ref:
        raise OEEIntegrityError("subject ingress/causal acceptance replay binding mismatch")
    receipts: dict[str, list[acceptance.AcceptanceReceipt]] = {role: [] for role in acceptance.SUPPORTED_ROLES}
    receipts[acceptance.CAUSAL_USE_PERMISSION].append(_validate_binding_manifest(
        causal_binding_ref, record=record, expected_role=acceptance.CAUSAL_USE_PERMISSION, object_ref=object_ref
    ))

    if record.realization_state in {STATE_OPPORTUNITY, STATE_ENCOUNTER}:
        if not role_refs[acceptance.POSITIVE_APPLICABILITY]:
            raise OEEIntegrityError("record lacks positive-applicability OBL056 acceptance binding")
        bound_app_refs: set[ExactRef] = set()
        for ref in role_refs[acceptance.POSITIVE_APPLICABILITY]:
            body = _decode_manifest(ref, ref.kind)
            bound_app_refs.add(_ref_from_dict(body["semantic_evidence_ref"]))
            receipts[acceptance.POSITIVE_APPLICABILITY].append(_validate_binding_manifest(
                ref, record=record, expected_role=acceptance.POSITIVE_APPLICABILITY, object_ref=object_ref
            ))
        if bound_app_refs != set(record.applicability_receipt_refs):
            raise OEEIntegrityError("applicability replay bindings do not cover exact record receipts")
    elif role_refs[acceptance.POSITIVE_APPLICABILITY]:
        raise OEEIntegrityError("AVAILABLE may not carry positive-applicability acceptance bindings")

    if record.realization_state == STATE_ENCOUNTER:
        if len(role_refs[acceptance.CONTACT_OCCURRENCE_WITNESS]) != 1 or len(role_refs[acceptance.CONTACT_WITNESS_INDEPENDENCE]) != 1:
            raise OEEIntegrityError("ENCOUNTER requires exactly one occurrence and one independence acceptance binding")
        occurrence = _validate_binding_manifest(
            role_refs[acceptance.CONTACT_OCCURRENCE_WITNESS][0],
            record=record,
            expected_role=acceptance.CONTACT_OCCURRENCE_WITNESS,
            object_ref=object_ref,
        )
        independence = _validate_binding_manifest(
            role_refs[acceptance.CONTACT_WITNESS_INDEPENDENCE][0],
            record=record,
            expected_role=acceptance.CONTACT_WITNESS_INDEPENDENCE,
            object_ref=object_ref,
        )
        try:
            acceptance.validate_contact_acceptance_pair(occurrence, independence)
        except acceptance.AcceptanceAuthorityError as exc:
            raise OEEIntegrityError(f"contact acceptance pair invalid: {exc}") from exc
        receipts[acceptance.CONTACT_OCCURRENCE_WITNESS].append(occurrence)
        receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE].append(independence)
    elif role_refs[acceptance.CONTACT_OCCURRENCE_WITNESS] or role_refs[acceptance.CONTACT_WITNESS_INDEPENDENCE]:
        raise OEEIntegrityError("non-ENCOUNTER record may not carry contact acceptance bindings")

    currentness = {r.currentness_state for values in receipts.values() for r in values}
    if len(currentness) != 1 or phase.get("currentness_state") not in currentness or subject.get("currentness_state") not in currentness:
        raise OEEIntegrityError("acceptance/subject/phase currentness replay mismatch")

    # Base W2 already reconstructs and verifies its ADP-010 authority/registry/rule
    # provenance, candidate hash, source_candidate_id, record hash, and event id.
    # Re-run exact source identity after all OBL055 replay manifests have validated.
    candidate_hash = w2._digest(w2._CANDIDATE_DOMAIN, w2._candidate_material(record))
    if record.source_candidate_replay_hash != candidate_hash or record.source_candidate_id != "urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash:
        raise OEEIntegrityError("OBL055 source_candidate_id/replay grain mismatch")
    return record


def _validated_subject_actor(subject: SubjectIngressEvidence, actor: ActorPhaseEvidence, currentness: str) -> tuple[ExactRef, ExactRef]:
    _, subject_auth = w2._validate_subject(subject, currentness)
    _, phase_auth = w2._validate_actor(actor, currentness)
    return subject_auth, phase_auth


def _causal_binding(
    subject: SubjectIngressEvidence,
    receipt: acceptance.AcceptanceReceipt,
    currentness: str,
) -> tuple[ExactRef, tuple[ExactRef, ...]]:
    p = subject.causal_use_permission
    receipt = _validate_acceptance(
        receipt,
        role=acceptance.CAUSAL_USE_PERMISSION,
        authority_id=p.authority_id,
        authority_version=p.authority_version,
        authority_hash=p.authority_content_hash,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        currentness=currentness,
    )
    refs = _binding_refs(
        receipt,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        semantic_ref=p.permission_ref,
        evidence_auth_ref=p.authentication_ref,
    )
    return _binding_manifest(refs, acceptance.CAUSAL_USE_PERMISSION), refs


def _app_bindings(
    subject: SubjectIngressEvidence,
    apps: Sequence[PositiveApplicabilityReceipt],
    acceptance_receipts: Sequence[acceptance.AcceptanceReceipt],
    currentness: str,
) -> tuple[ExactRef, ...]:
    by_authority: dict[tuple[str, str, str], acceptance.AcceptanceReceipt] = {}
    for receipt in acceptance_receipts:
        key = (receipt.accepted_authority_ref.id, receipt.accepted_authority_ref.version, receipt.accepted_authority_ref.content_hash)
        if key in by_authority and by_authority[key].receipt_id != receipt.receipt_id:
            raise OBL055AcceptanceError("multiple applicability acceptance receipts for one authority are ambiguous")
        by_authority[key] = receipt
    required = {(x.authority_id, x.authority_version, x.authority_content_hash) for x in apps}
    if set(by_authority) != required:
        raise OBL055AcceptanceError("applicability acceptance receipts do not exactly cover source authorities")
    refs: list[ExactRef] = []
    for x in apps:
        key = (x.authority_id, x.authority_version, x.authority_content_hash)
        receipt = _validate_acceptance(
            by_authority[key],
            role=acceptance.POSITIVE_APPLICABILITY,
            authority_id=x.authority_id,
            authority_version=x.authority_version,
            authority_hash=x.authority_content_hash,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            currentness=currentness,
        )
        refs.extend(_binding_refs(
            receipt,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            semantic_ref=x.receipt,
            evidence_auth_ref=x.authentication_ref,
        ))
    return tuple(sorted(set(refs)))


def _common_replay_refs(
    subject: SubjectIngressEvidence,
    actor: ActorPhaseEvidence,
    subject_auth: ExactRef,
    phase_auth: ExactRef,
    causal_binding: ExactRef,
    currentness: str,
) -> tuple[ExactRef, ...]:
    mat = subject.materialization_receipt
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", mat.receipt_id, mat.receipt_hash)
    return tuple(sorted(set((
        *_FIXED_PROVENANCE,
        _phase_manifest(actor, phase_auth, currentness),
        _subject_manifest(subject, subject_auth, causal_binding, currentness),
        actor.phase_state_receipt_ref,
        phase_auth,
        mat_ref,
        subject.causal_use_permission.permission_ref,
        subject.causal_use_permission.authentication_ref,
        subject_auth,
    ))))


class _Executor:
    def __init__(self, currentness: str) -> None:
        if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
            raise OEEIntegrityError("unsupported OBL055 successor currentness")
        self.currentness = currentness

    def admit_available(
        self,
        *,
        causal_use_acceptance_receipt: acceptance.AcceptanceReceipt,
        subject: SubjectIngressEvidence,
        actor: ActorPhaseEvidence,
        effective_from: str,
        effective_until: str,
        time_granularity: str,
        context_or_world_receipt_refs: Iterable[ExactRef],
        prior_ledger_anchor_ref: ExactRef,
        provenance_refs: Iterable[ExactRef],
    ) -> OEEExecutionResult:
        subject_auth, phase_auth = _validated_subject_actor(subject, actor, self.currentness)
        causal_manifest, causal_refs = _causal_binding(subject, causal_use_acceptance_receipt, self.currentness)
        replay = _common_replay_refs(subject, actor, subject_auth, phase_auth, causal_manifest, self.currentness)
        extra = tuple(sorted(set((*provenance_refs, *causal_refs, *replay))))
        fn = w2.admit_available if self.currentness == CURRENT_ACCEPTED else w2._admit_available_noncurrent_for_test
        result = fn(
            subject=subject,
            actor=actor,
            effective_from=effective_from,
            effective_until=effective_until,
            time_granularity=time_granularity,
            context_or_world_receipt_refs=context_or_world_receipt_refs,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            provenance_refs=extra,
        )
        return OEEExecutionResult(validate_record(result.record))

    def admit_opportunity(
        self,
        *,
        causal_use_acceptance_receipt: acceptance.AcceptanceReceipt,
        applicability_acceptance_receipts: Sequence[acceptance.AcceptanceReceipt],
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
        validate_record(parent_available)
        subject_auth, phase_auth = _validated_subject_actor(subject, actor, self.currentness)
        causal_manifest, causal_refs = _causal_binding(subject, causal_use_acceptance_receipt, self.currentness)
        if not isinstance(opportunity_basis, OpportunityBasisEvidence):
            raise OEEIntegrityError("opportunity_basis must be OpportunityBasisEvidence")
        apps = tuple(opportunity_basis.applicability_receipts)
        for app in apps:
            w2._validate_app(app, self.currentness)
        app_refs = _app_bindings(subject, apps, tuple(applicability_acceptance_receipts), self.currentness)
        replay = _common_replay_refs(subject, actor, subject_auth, phase_auth, causal_manifest, self.currentness)
        extra = tuple(sorted(set((*provenance_refs, *causal_refs, *app_refs, *replay))))
        fn = w2.admit_opportunity if self.currentness == CURRENT_ACCEPTED else w2._admit_opportunity_noncurrent_for_test
        result = fn(
            parent_available=parent_available,
            subject=subject,
            actor=actor,
            opportunity_basis=opportunity_basis,
            effective_from=effective_from,
            effective_until=effective_until,
            time_granularity=time_granularity,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            provenance_refs=extra,
        )
        return OEEExecutionResult(validate_record(result.record))

    def admit_encounter(
        self,
        *,
        causal_use_acceptance_receipt: acceptance.AcceptanceReceipt,
        applicability_acceptance_receipts: Sequence[acceptance.AcceptanceReceipt],
        contact_occurrence_acceptance_receipt: acceptance.AcceptanceReceipt,
        contact_independence_acceptance_receipt: acceptance.AcceptanceReceipt,
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
        validate_record(parent_opportunity)
        subject_auth, phase_auth = _validated_subject_actor(subject, actor, self.currentness)
        causal_manifest, causal_refs = _causal_binding(subject, causal_use_acceptance_receipt, self.currentness)

        parent_app_bodies = [
            _decode_manifest(r, r.kind)
            for r in parent_opportunity.provenance_refs
            if r.kind == "OBL056_ACCEPTANCE_BINDING_" + acceptance.POSITIVE_APPLICABILITY
        ]
        if not parent_app_bodies:
            raise OEEIntegrityError("parent opportunity lacks applicability acceptance replay bindings")
        parent_authorities = {
            (
                b["receipt"]["accepted_authority_ref"]["id"],
                b["receipt"]["accepted_authority_ref"]["version"],
                b["receipt"]["accepted_authority_ref"]["content_hash"],
            )
            for b in parent_app_bodies
        }
        provided_authorities = {
            (r.accepted_authority_ref.id, r.accepted_authority_ref.version, r.accepted_authority_ref.content_hash)
            for r in applicability_acceptance_receipts
        }
        if parent_authorities != provided_authorities:
            raise OBL055AcceptanceError("encounter applicability acceptance receipts do not replay exact parent authorities")
        for receipt in applicability_acceptance_receipts:
            _validate_acceptance(
                receipt,
                role=acceptance.POSITIVE_APPLICABILITY,
                authority_id=receipt.accepted_authority_ref.id,
                authority_version=receipt.accepted_authority_ref.version,
                authority_hash=receipt.accepted_authority_ref.content_hash,
                subject_ref=subject.subject_ref,
                object_ref=subject.semantic_object_ref,
                currentness=self.currentness,
            )

        t = w2._time(effective_time, "effective_time")
        witness, contact_auth, independence_auth = w2._validate_contact(
            contact_witness, actor.actor_id, subject.subject_ref, t, self.currentness
        )
        occurrence = _validate_acceptance(
            contact_occurrence_acceptance_receipt,
            role=acceptance.CONTACT_OCCURRENCE_WITNESS,
            authority_id=witness.witness_authority_id,
            authority_version=witness.witness_authority_version,
            authority_hash=witness.witness_authority_content_hash,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            currentness=self.currentness,
        )
        independence = _validate_acceptance(
            contact_independence_acceptance_receipt,
            role=acceptance.CONTACT_WITNESS_INDEPENDENCE,
            authority_id=witness.independence_authority_id,
            authority_version=witness.independence_authority_version,
            authority_hash=witness.independence_authority_content_hash,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            currentness=self.currentness,
        )
        try:
            acceptance.validate_contact_acceptance_pair(occurrence, independence)
        except acceptance.AcceptanceAuthorityError as exc:
            raise OBL055AcceptanceError(f"contact occurrence/independence acceptance pair rejected: {exc}") from exc
        occurrence_refs = _binding_refs(
            occurrence,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            semantic_ref=witness.witness_ref,
            evidence_auth_ref=contact_auth,
        )
        independence_refs = _binding_refs(
            independence,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            semantic_ref=witness.independence_receipt_ref,
            evidence_auth_ref=independence_auth,
            auxiliary_ref=witness.independence_ref,
        )
        replay = _common_replay_refs(subject, actor, subject_auth, phase_auth, causal_manifest, self.currentness)
        extra = tuple(sorted(set((
            *provenance_refs,
            *causal_refs,
            *replay,
            *occurrence_refs,
            *independence_refs,
            *(r for r in parent_opportunity.provenance_refs if r.kind.startswith("OBL056_ACCEPTANCE_BINDING_" + acceptance.POSITIVE_APPLICABILITY)),
        ))))
        # Parent provenance already carries the complete applicability receipt constituents;
        # W2 merges parent provenance into ENCOUNTER, so no local semantic re-issuance occurs.
        fn = w2.admit_encounter if self.currentness == CURRENT_ACCEPTED else w2._admit_encounter_noncurrent_for_test
        result = fn(
            parent_opportunity=parent_opportunity,
            subject=subject,
            actor=actor,
            contact_witness=contact_witness,
            effective_time=effective_time,
            time_granularity=time_granularity,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            declared_precondition_refs=declared_precondition_refs,
            provenance_refs=extra,
        )
        return OEEExecutionResult(validate_record(result.record))


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
    available_record, opportunity_record, encounter_record = (validate_record(r) for r in records)
    return w2.validate_basis_available_opportunity_encounter_chain(
        (available_record, opportunity_record, encounter_record)
    )


def authority_identity_manifest() -> dict[str, Any]:
    out = w2.authority_identity_manifest()
    out = dict(out)
    out["successor"] = {
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "frozen_w2_executor_blob": FROZEN_W2_EXECUTOR_BLOB,
    }
    out["OBL056"] = {
        "hq_adoption_ref": HQ_OBL056_ADOPTION_REF,
        "acceptance_authority_id": acceptance.ACCEPTANCE_AUTHORITY_ID,
        "acceptance_authority_version": acceptance.ACCEPTANCE_AUTHORITY_VERSION,
        "acceptance_authority_hash": HQ_OBL056_AUTHORITY_HASH,
        "implementation_blob": HQ_OBL056_IMPLEMENTATION_BLOB,
        "installed_registry_hash": HQ_OBL056_EMPTY_REGISTRY_HASH,
        "installed_current_positive_entry_count": 0,
        "positive_fallback": False,
    }
    return out


# Non-current mechanical fixtures.  These cannot issue or install current authority.
def synthetic_acceptance_receipts() -> dict[str, acceptance.AcceptanceReceipt]:
    return {role: acceptance.issue_noncurrent_synthetic_test_receipt(role) for role in acceptance.SUPPORTED_ROLES}


def _synthetic_subject(receipt: acceptance.AcceptanceReceipt | None = None, tag: str = "subject") -> SubjectIngressEvidence:
    receipt = receipt or synthetic_acceptance_receipts()[acceptance.CAUSAL_USE_PERMISSION]
    subject = w2._synthetic_subject(tag)
    p = subject.causal_use_permission
    ar = receipt.accepted_authority_ref
    p0 = replace(
        p,
        authority_id=ar.id,
        authority_version=ar.version,
        authority_content_hash=ar.content_hash,
        authority_acceptance_ref=w2._authority_acceptance_ref(
            "ACCEPTED_CAUSAL_USE_AUTHORITY_RECEIPT", ar.id, ar.version, ar.content_hash, NONCURRENT_SYNTHETIC_TEST_ONLY
        ),
        authentication_ref=w2._fixture_ref("PLACEHOLDER", tag + ":obl055-causal-auth"),
    )
    p1 = replace(
        p0,
        authentication_ref=w2._content_ref(
            "CAUSAL_USE_PERMISSION_AUTHENTICATION",
            "urn:rawlsing:causal-use-authentication:sha256:",
            w2._permission_material(p0),
        ),
    )
    s0 = replace(subject, causal_use_permission=p1, authentication_ref=w2._fixture_ref("PLACEHOLDER", tag + ":obl055-subject-auth"))
    return replace(
        s0,
        authentication_ref=w2._content_ref(
            "SUBJECT_INGRESS_AUTHENTICATION",
            "urn:rawlsing:subject-ingress-authentication:sha256:",
            w2._subject_material(s0),
        ),
    )


def _synthetic_actor(tag: str = "actor", phase_tag: str = "phase") -> ActorPhaseEvidence:
    return w2._synthetic_actor(tag, phase_tag)


def _synthetic_app(receipt: acceptance.AcceptanceReceipt | None = None, tag: str = "app") -> PositiveApplicabilityReceipt:
    receipt = receipt or synthetic_acceptance_receipts()[acceptance.POSITIVE_APPLICABILITY]
    app = w2._synthetic_app(authority_tag=tag)
    ar = receipt.accepted_authority_ref
    a0 = replace(
        app,
        authority_id=ar.id,
        authority_version=ar.version,
        authority_content_hash=ar.content_hash,
        authority_acceptance_ref=w2._authority_acceptance_ref(
            "ACCEPTED_APPLICABILITY_AUTHORITY_RECEIPT", ar.id, ar.version, ar.content_hash, NONCURRENT_SYNTHETIC_TEST_ONLY
        ),
        authentication_ref=w2._fixture_ref("PLACEHOLDER", tag + ":obl055-app-auth"),
    )
    return replace(
        a0,
        authentication_ref=w2._content_ref(
            "POSITIVE_APPLICABILITY_AUTHENTICATION",
            "urn:rawlsing:positive-applicability-authentication:sha256:",
            w2._app_material(a0),
        ),
    )


def _synthetic_basis(subject: SubjectIngressEvidence, actor: ActorPhaseEvidence, app: PositiveApplicabilityReceipt | None = None) -> OpportunityBasisEvidence:
    return w2._synthetic_basis(subject, actor, app or _synthetic_app())


def _synthetic_contact(
    subject: SubjectIngressEvidence,
    actor: ActorPhaseEvidence,
    occurrence_receipt: acceptance.AcceptanceReceipt | None = None,
    independence_receipt: acceptance.AcceptanceReceipt | None = None,
    **kwargs: Any,
) -> ContactOccurrenceWitness:
    receipts = synthetic_acceptance_receipts()
    occurrence_receipt = occurrence_receipt or receipts[acceptance.CONTACT_OCCURRENCE_WITNESS]
    independence_receipt = independence_receipt or receipts[acceptance.CONTACT_WITNESS_INDEPENDENCE]
    witness = w2._synthetic_contact(subject, actor, **kwargs)
    oa = occurrence_receipt.accepted_authority_ref
    ia = independence_receipt.accepted_authority_ref
    w0 = replace(
        witness,
        witness_authority_id=oa.id,
        witness_authority_version=oa.version,
        witness_authority_content_hash=oa.content_hash,
        witness_authority_acceptance_ref=w2._authority_acceptance_ref(
            "ACCEPTED_CONTACT_OCCURRENCE_AUTHORITY_RECEIPT", oa.id, oa.version, oa.content_hash, NONCURRENT_SYNTHETIC_TEST_ONLY
        ),
        independence_authority_id=ia.id,
        independence_authority_version=ia.version,
        independence_authority_content_hash=ia.content_hash,
        independence_authority_acceptance_ref=w2._authority_acceptance_ref(
            "ACCEPTED_CONTACT_INDEPENDENCE_AUTHORITY_RECEIPT", ia.id, ia.version, ia.content_hash, NONCURRENT_SYNTHETIC_TEST_ONLY
        ),
        contact_authentication_ref=w2._fixture_ref("PLACEHOLDER", "obl055-contact-auth"),
        independence_authentication_ref=w2._fixture_ref("PLACEHOLDER", "obl055-independence-auth"),
    )
    contact_auth = w2._content_ref(
        "CONTACT_OCCURRENCE_AUTHENTICATION",
        "urn:rawlsing:contact-occurrence-authentication:sha256:",
        w2._contact_material(w0),
    )
    w1 = replace(w0, contact_authentication_ref=contact_auth)
    independence_auth = w2._content_ref(
        "CONTACT_INDEPENDENCE_AUTHENTICATION",
        "urn:rawlsing:contact-independence-authentication:sha256:",
        w2._independence_material(w1, contact_auth),
    )
    return replace(w1, independence_authentication_ref=independence_auth)
