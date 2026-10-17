"""GT34 OBL055 R2 successor: exact source-evidence replay reconstruction.

This is the smallest successor to the first OBL056-acceptance-bound repair.
It preserves both frozen W2 and the first repair unchanged.  The sole additional
mechanism is a content-addressed source replay bundle.  validate_record rebuilds
the original W2 source evidence objects from that bundle, reruns W2's existing
source validators, then cross-checks every OBL056 acceptance binding against the
reconstructed source.  No underlying semantic proposition or authority is minted.
"""
from __future__ import annotations

from base64 import urlsafe_b64decode, urlsafe_b64encode
from dataclasses import asdict, replace
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Sequence

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_authenticated as w2
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as r1


EXECUTOR_ID = "GT34_V3P5_ADP010_OBL056_RECONSTRUCTED_REPLAY_EXECUTOR"
EXECUTOR_VERSION = "3.1.0"
FROZEN_W2_EXECUTOR_BLOB = "54d9acba40f0eb1db8bb03aec3c1bb900f849588"
FROZEN_R1_REPAIR_BLOB = "fa169dbb525475c17b2495a5b35aa300aa809881"
HQ_OBL056_AUTHORITY_HASH = r1.HQ_OBL056_AUTHORITY_HASH
HQ_OBL056_IMPLEMENTATION_BLOB = r1.HQ_OBL056_IMPLEMENTATION_BLOB
HQ_OBL056_EMPTY_REGISTRY_HASH = r1.HQ_OBL056_EMPTY_REGISTRY_HASH
HQ_OBL056_ADOPTION_REF = r1.HQ_OBL056_ADOPTION_REF

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
OBL055AcceptanceError = r1.OBL055AcceptanceError

CURRENT_ACCEPTED = w2.CURRENT_ACCEPTED
NONCURRENT_SYNTHETIC_TEST_ONLY = w2.NONCURRENT_SYNTHETIC_TEST_ONLY
STATE_AVAILABLE = w2.STATE_AVAILABLE
STATE_OPPORTUNITY = w2.STATE_OPPORTUNITY
STATE_ENCOUNTER = w2.STATE_ENCOUNTER

_BUNDLE_SCHEMA = "GT34_OBL055_RECONSTRUCTED_SOURCE_REPLAY_BUNDLE@1.0.0"
_BUNDLE_PREFIX = "urn:rawlsing:gt34:obl055:source-replay-bundle:"
_BUNDLE_DOMAIN = "RAWLSING\0GT34\0OBL055\0SOURCE_REPLAY_RECONSTRUCTION_R2\0"
_BUNDLE_KIND = {
    STATE_AVAILABLE: "OBL055_SOURCE_REPLAY_BUNDLE_AVAILABLE",
    STATE_OPPORTUNITY: "OBL055_SOURCE_REPLAY_BUNDLE_OPPORTUNITY",
    STATE_ENCOUNTER: "OBL055_SOURCE_REPLAY_BUNDLE_ENCOUNTER",
}


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _digest(label: str, value: Any) -> str:
    return sha256((_BUNDLE_DOMAIN + label + "\0" + _canonical(value)).encode("utf-8")).hexdigest()


R2_SUCCESSOR_HASH = _digest(
    "EXECUTOR",
    [EXECUTOR_ID, EXECUTOR_VERSION, FROZEN_W2_EXECUTOR_BLOB, FROZEN_R1_REPAIR_BLOB, HQ_OBL056_AUTHORITY_HASH],
)
R2_SUCCESSOR_REF = ExactRef(
    "OBL055_RECONSTRUCTED_REPLAY_EXECUTOR",
    f"urn:rawlsing:gt34:obl055:executor:{EXECUTOR_ID}@{EXECUTOR_VERSION}",
    R2_SUCCESSOR_HASH,
)


def _xr(value: Mapping[str, Any]) -> ExactRef:
    return ExactRef(str(value["kind"]), str(value["ref"]), str(value["content_hash"]))


def _xrs(values: Sequence[Mapping[str, Any]]) -> tuple[ExactRef, ...]:
    return tuple(_xr(x) for x in values)


def _materialization(value: Mapping[str, Any]) -> SubjectMaterializationReceipt:
    return SubjectMaterializationReceipt(
        receipt_id=str(value["receipt_id"]),
        receipt_hash=str(value["receipt_hash"]),
        subject_ref=str(value["subject_ref"]),
        subject_ref_hash=str(value["subject_ref_hash"]),
        materializer_id=str(value["materializer_id"]),
        materializer_version=str(value["materializer_version"]),
        adoption_artifact_blob=str(value["adoption_artifact_blob"]),
        accepted_owner_root_hash=str(value["accepted_owner_root_hash"]),
        materialization_permit_id=str(value["materialization_permit_id"]),
        materialization_permit_hash=str(value["materialization_permit_hash"]),
        semantic_owner_authority_id=str(value["semantic_owner_authority_id"]),
        semantic_owner_authority_version=str(value["semantic_owner_authority_version"]),
        semantic_owner_authority_hash=str(value["semantic_owner_authority_hash"]),
        semantic_object_ref=_xr(value["semantic_object_ref"]),
        owner_binding_content_hash=str(value["owner_binding_content_hash"]),
        evidence_refs=_xrs(value["evidence_refs"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        replay_input_hash=str(value["replay_input_hash"]),
        integrity_state=str(value["integrity_state"]),
        semantic_owner_transfer=bool(value["semantic_owner_transfer"]),
        semantic_fields_interpreted=bool(value["semantic_fields_interpreted"]),
        currentness_state=str(value["currentness_state"]),
    )


def _permission(value: Mapping[str, Any]) -> CausalUsePermission:
    return CausalUsePermission(
        permission_ref=_xr(value["permission_ref"]),
        authority_id=str(value["authority_id"]),
        authority_version=str(value["authority_version"]),
        authority_content_hash=str(value["authority_content_hash"]),
        authority_acceptance_ref=_xr(value["authority_acceptance_ref"]),
        subject_ref=str(value["subject_ref"]),
        semantic_object_ref=_xr(value["semantic_object_ref"]),
        materialization_receipt_ref=_xr(value["materialization_receipt_ref"]),
        scope=str(value["scope"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        authentication_ref=_xr(value["authentication_ref"]),
        currentness_state=str(value["currentness_state"]),
    )


def _subject(value: Mapping[str, Any]) -> SubjectIngressEvidence:
    return SubjectIngressEvidence(
        subject_ref=str(value["subject_ref"]),
        semantic_owner_authority_id=str(value["semantic_owner_authority_id"]),
        semantic_owner_authority_version=str(value["semantic_owner_authority_version"]),
        semantic_owner_authority_content_hash=str(value["semantic_owner_authority_content_hash"]),
        semantic_object_ref=_xr(value["semantic_object_ref"]),
        materialization_receipt=_materialization(value["materialization_receipt"]),
        obl054_adoption_artifact_blob=str(value["obl054_adoption_artifact_blob"]),
        epistemic_class=str(value["epistemic_class"]),
        causal_use_permission=_permission(value["causal_use_permission"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        authentication_ref=_xr(value["authentication_ref"]),
        currentness_state=str(value["currentness_state"]),
    )


def _actor(value: Mapping[str, Any]) -> ActorPhaseEvidence:
    return ActorPhaseEvidence(
        actor_id=str(value["actor_id"]),
        phase_state_ref=_xr(value["phase_state_ref"]),
        phase_state_receipt_ref=_xr(value["phase_state_receipt_ref"]),
        phase_authority_id=str(value["phase_authority_id"]),
        phase_authority_version=str(value["phase_authority_version"]),
        phase_authority_artifact_blob_sha=str(value["phase_authority_artifact_blob_sha"]),
        phase_registry_id=str(value["phase_registry_id"]),
        phase_registry_version=str(value["phase_registry_version"]),
        phase_registry_content_hash=str(value["phase_registry_content_hash"]),
        base_phase_id=str(value["base_phase_id"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        authentication_ref=_xr(value["authentication_ref"]),
        currentness_state=str(value["currentness_state"]),
    )


def _app(value: Mapping[str, Any]) -> PositiveApplicabilityReceipt:
    return PositiveApplicabilityReceipt(
        receipt=_xr(value["receipt"]),
        authority_id=str(value["authority_id"]),
        authority_version=str(value["authority_version"]),
        authority_content_hash=str(value["authority_content_hash"]),
        authority_acceptance_ref=_xr(value["authority_acceptance_ref"]),
        result=str(value["result"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        authentication_ref=_xr(value["authentication_ref"]),
        currentness_state=str(value["currentness_state"]),
    )


def _basis(value: Mapping[str, Any]) -> OpportunityBasisEvidence:
    return OpportunityBasisEvidence(
        basis_ref=_xr(value["basis_ref"]),
        actor_id=str(value["actor_id"]),
        subject_ref=str(value["subject_ref"]),
        applicability_receipts=tuple(_app(x) for x in value["applicability_receipts"]),
        context_or_world_receipt_refs=_xrs(value["context_or_world_receipt_refs"]),
        position_or_other_constraint_refs=_xrs(value["position_or_other_constraint_refs"]),
        provenance_refs=_xrs(value["provenance_refs"]),
    )


def _contact(value: Mapping[str, Any]) -> ContactOccurrenceWitness:
    return ContactOccurrenceWitness(
        witness_ref=_xr(value["witness_ref"]),
        witness_authority_id=str(value["witness_authority_id"]),
        witness_authority_version=str(value["witness_authority_version"]),
        witness_authority_content_hash=str(value["witness_authority_content_hash"]),
        witness_authority_acceptance_ref=_xr(value["witness_authority_acceptance_ref"]),
        actor_id=str(value["actor_id"]),
        subject_ref=str(value["subject_ref"]),
        occurrence_time=str(value["occurrence_time"]),
        semantic=str(value["semantic"]),
        contact_basis_refs=_xrs(value["contact_basis_refs"]),
        contact_authentication_ref=_xr(value["contact_authentication_ref"]),
        independence_ref=_xr(value["independence_ref"]),
        independence_authority_id=str(value["independence_authority_id"]),
        independence_authority_version=str(value["independence_authority_version"]),
        independence_authority_content_hash=str(value["independence_authority_content_hash"]),
        independence_authority_acceptance_ref=_xr(value["independence_authority_acceptance_ref"]),
        independence_receipt_ref=_xr(value["independence_receipt_ref"]),
        independence_basis_refs=_xrs(value["independence_basis_refs"]),
        independence_authentication_ref=_xr(value["independence_authentication_ref"]),
        provenance_refs=_xrs(value["provenance_refs"]),
        currentness_state=str(value["currentness_state"]),
    )


def _receipt(value: Mapping[str, Any]) -> acceptance.AcceptanceReceipt:
    return r1._receipt_from_dict(value)


def _bundle_ref(state: str, body: Mapping[str, Any]) -> ExactRef:
    kind = _BUNDLE_KIND[state]
    raw = _canonical(dict(body)).encode("utf-8")
    token = urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    h = _digest(kind, body)
    return ExactRef(kind, _BUNDLE_PREFIX + kind.lower() + ":" + token, h)


def _decode_bundle(ref: ExactRef, state: str) -> dict[str, Any]:
    kind = _BUNDLE_KIND[state]
    w2._ref(ref, "OBL055 R2 replay bundle")
    if ref.kind != kind:
        raise OEEIntegrityError("OBL055 R2 replay bundle kind mismatch")
    prefix = _BUNDLE_PREFIX + kind.lower() + ":"
    if not ref.ref.startswith(prefix):
        raise OEEIntegrityError("OBL055 R2 replay bundle prefix mismatch")
    token = ref.ref[len(prefix):]
    token += "=" * ((4 - len(token) % 4) % 4)
    try:
        body = json.loads(urlsafe_b64decode(token.encode("ascii")).decode("utf-8"))
    except Exception as exc:
        raise OEEIntegrityError("OBL055 R2 replay bundle decode failure") from exc
    if not isinstance(body, dict) or ref.content_hash != _digest(kind, body) or _bundle_ref(state, body) != ref:
        raise OEEIntegrityError("OBL055 R2 replay bundle integrity/canonicalization mismatch")
    return body


def _state_bundle(record: V3OEERealizationRecord) -> dict[str, Any]:
    kind = _BUNDLE_KIND[record.realization_state]
    refs = [x for x in record.provenance_refs if x.kind == kind]
    if len(refs) != 1:
        raise OEEIntegrityError(f"expected exactly one {kind}")
    return _decode_bundle(refs[0], record.realization_state)


def _readdress(record: V3OEERealizationRecord, provenance_refs: Iterable[ExactRef]) -> V3OEERealizationRecord:
    x = replace(record, provenance_refs=tuple(sorted(set(provenance_refs))))
    candidate_hash = w2._digest(w2._CANDIDATE_DOMAIN, w2._candidate_material(x))
    x = replace(
        x,
        source_candidate_id="urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash,
        source_candidate_replay_hash=candidate_hash,
    )
    record_hash = w2._digest(w2._RECORD_DOMAIN, w2._record_identity(x))
    event_id = None
    if x.event_effect_kind is not None:
        event_hash = w2._digest(w2._EVENT_DOMAIN, {"record_hash": record_hash, "effect": x.event_effect_kind})
        event_id = "urn:rawlsing:v3:oee:event:sha256:" + event_hash
    return replace(
        x,
        record_id="urn:rawlsing:v3:oee:record:sha256:" + record_hash,
        record_hash=record_hash,
        event_id=event_id,
    )


def _source_bundle(
    *,
    state: str,
    currentness: str,
    subject: SubjectIngressEvidence,
    actor: ActorPhaseEvidence,
    causal_receipt: acceptance.AcceptanceReceipt,
    parent_record_id: str | None,
    opportunity_basis: OpportunityBasisEvidence | None = None,
    applicability_receipts: Sequence[acceptance.AcceptanceReceipt] = (),
    contact_witness: ContactOccurrenceWitness | None = None,
    occurrence_receipt: acceptance.AcceptanceReceipt | None = None,
    independence_receipt: acceptance.AcceptanceReceipt | None = None,
) -> dict[str, Any]:
    return {
        "schema_id": _BUNDLE_SCHEMA,
        "state": state,
        "currentness_state": currentness,
        "parent_record_id": parent_record_id,
        "subject_ingress_evidence": asdict(subject),
        "actor_phase_evidence": asdict(actor),
        "causal_use_acceptance_receipt": asdict(causal_receipt),
        "opportunity_basis_evidence": None if opportunity_basis is None else asdict(opportunity_basis),
        "applicability_acceptance_receipts": [asdict(x) for x in applicability_receipts],
        "contact_occurrence_witness": None if contact_witness is None else asdict(contact_witness),
        "contact_occurrence_acceptance_receipt": None if occurrence_receipt is None else asdict(occurrence_receipt),
        "contact_independence_acceptance_receipt": None if independence_receipt is None else asdict(independence_receipt),
    }


def _base_binding_bodies(record: V3OEERealizationRecord, role: str) -> list[dict[str, Any]]:
    kind = "OBL056_ACCEPTANCE_BINDING_" + role
    return [r1._decode_manifest(x, kind) for x in record.provenance_refs if x.kind == kind]


def _assert_base_binding(
    record: V3OEERealizationRecord,
    *,
    role: str,
    semantic_ref: ExactRef,
    auth_ref: ExactRef,
    receipt: acceptance.AcceptanceReceipt,
    auxiliary_ref: ExactRef | None = None,
) -> None:
    bodies = _base_binding_bodies(record, role)
    matches = [
        b for b in bodies
        if r1._ref_from_dict(b["semantic_evidence_ref"]) == semantic_ref
        and r1._ref_from_dict(b["evidence_authentication_ref"]) == auth_ref
        and b["receipt"] == asdict(receipt)
        and ((b.get("auxiliary_ref") is None and auxiliary_ref is None) or (
            b.get("auxiliary_ref") is not None and auxiliary_ref is not None and r1._ref_from_dict(b["auxiliary_ref"]) == auxiliary_ref
        ))
    ]
    if len(matches) != 1:
        raise OEEIntegrityError(f"reconstructed {role} source does not match exact stored OBL056 binding")


def _validate_causal(record, subject, causal_receipt, currentness):
    p = subject.causal_use_permission
    mat = subject.materialization_receipt
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", mat.receipt_id, mat.receipt_hash)
    w2._validate_permission(p, subject.subject_ref, subject.semantic_object_ref, mat_ref, currentness)
    r1._validate_acceptance(
        causal_receipt,
        role=acceptance.CAUSAL_USE_PERMISSION,
        authority_id=p.authority_id,
        authority_version=p.authority_version,
        authority_hash=p.authority_content_hash,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        currentness=currentness,
    )
    _assert_base_binding(
        record,
        role=acceptance.CAUSAL_USE_PERMISSION,
        semantic_ref=p.permission_ref,
        auth_ref=p.authentication_ref,
        receipt=causal_receipt,
    )


def _validate_apps(record, subject, basis, app_acceptances, currentness):
    if basis.actor_id != record.actor_id or basis.subject_ref != record.subject_ref:
        raise OEEIntegrityError("reconstructed opportunity basis actor/subject mismatch")
    apps = tuple(basis.applicability_receipts)
    if {x.receipt for x in apps} != set(record.applicability_receipt_refs):
        raise OEEIntegrityError("reconstructed applicability source set mismatch")
    by_authority = {
        (x.accepted_authority_ref.id, x.accepted_authority_ref.version, x.accepted_authority_ref.content_hash): x
        for x in app_acceptances
    }
    if len(by_authority) != len(app_acceptances):
        raise OEEIntegrityError("ambiguous reconstructed applicability acceptance receipts")
    required = {(x.authority_id, x.authority_version, x.authority_content_hash) for x in apps}
    if set(by_authority) != required:
        raise OEEIntegrityError("reconstructed applicability acceptance set mismatch")
    for app in apps:
        receipt_ref, auth_ref = w2._validate_app(app, currentness)
        key = (app.authority_id, app.authority_version, app.authority_content_hash)
        receipt = by_authority[key]
        r1._validate_acceptance(
            receipt,
            role=acceptance.POSITIVE_APPLICABILITY,
            authority_id=app.authority_id,
            authority_version=app.authority_version,
            authority_hash=app.authority_content_hash,
            subject_ref=subject.subject_ref,
            object_ref=subject.semantic_object_ref,
            currentness=currentness,
        )
        _assert_base_binding(
            record,
            role=acceptance.POSITIVE_APPLICABILITY,
            semantic_ref=receipt_ref,
            auth_ref=auth_ref,
            receipt=receipt,
        )
    if len(_base_binding_bodies(record, acceptance.POSITIVE_APPLICABILITY)) != len(apps):
        raise OEEIntegrityError("extra or missing stored applicability binding")


def _validate_contact(record, subject, witness, occurrence_receipt, independence_receipt, currentness):
    witness, contact_auth, independence_auth = w2._validate_contact(
        witness,
        record.actor_id,
        record.subject_ref,
        record.effective_from,
        currentness,
    )
    if not {witness.witness_ref, witness.independence_ref}.issubset(set(record.causal_witness_refs)):
        raise OEEIntegrityError("reconstructed contact witness refs do not bind record witnesses")
    r1._validate_acceptance(
        occurrence_receipt,
        role=acceptance.CONTACT_OCCURRENCE_WITNESS,
        authority_id=witness.witness_authority_id,
        authority_version=witness.witness_authority_version,
        authority_hash=witness.witness_authority_content_hash,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        currentness=currentness,
    )
    r1._validate_acceptance(
        independence_receipt,
        role=acceptance.CONTACT_WITNESS_INDEPENDENCE,
        authority_id=witness.independence_authority_id,
        authority_version=witness.independence_authority_version,
        authority_hash=witness.independence_authority_content_hash,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        currentness=currentness,
    )
    try:
        acceptance.validate_contact_acceptance_pair(occurrence_receipt, independence_receipt)
    except acceptance.AcceptanceAuthorityError as exc:
        raise OEEIntegrityError(f"reconstructed contact acceptance pair invalid: {exc}") from exc
    _assert_base_binding(
        record,
        role=acceptance.CONTACT_OCCURRENCE_WITNESS,
        semantic_ref=witness.witness_ref,
        auth_ref=contact_auth,
        receipt=occurrence_receipt,
    )
    _assert_base_binding(
        record,
        role=acceptance.CONTACT_WITNESS_INDEPENDENCE,
        semantic_ref=witness.independence_receipt_ref,
        auth_ref=independence_auth,
        receipt=independence_receipt,
        auxiliary_ref=witness.independence_ref,
    )


def validate_record(record: Any) -> V3OEERealizationRecord:
    record = r1.validate_record(record)
    if R2_SUCCESSOR_REF not in set(record.provenance_refs):
        raise OEEIntegrityError("missing exact OBL055 R2 successor provenance")
    body = _state_bundle(record)
    if body.get("schema_id") != _BUNDLE_SCHEMA or body.get("state") != record.realization_state:
        raise OEEIntegrityError("OBL055 R2 replay bundle state/schema mismatch")
    if body.get("parent_record_id") != record.parent_record_id:
        raise OEEIntegrityError("OBL055 R2 replay bundle parent mismatch")
    currentness = str(body.get("currentness_state"))
    if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
        raise OEEIntegrityError("OBL055 R2 replay bundle currentness invalid")

    try:
        subject = _subject(body["subject_ingress_evidence"])
        actor = _actor(body["actor_phase_evidence"])
        causal_receipt = _receipt(body["causal_use_acceptance_receipt"])
    except Exception as exc:
        raise OEEIntegrityError("OBL055 R2 source replay reconstruction failed") from exc

    subject, subject_auth = w2._validate_subject(subject, currentness)
    actor, phase_auth = w2._validate_actor(actor, currentness)
    if subject.subject_ref != record.subject_ref or actor.actor_id != record.actor_id or actor.phase_state_ref != record.phase_state_ref:
        raise OEEIntegrityError("reconstructed subject/actor does not bind record identity")

    subject_manifest = r1._single_manifest(record, "OBL055_SUBJECT_INGRESS_REPLAY_BINDING")
    phase_manifest = r1._single_manifest(record, "OBL055_ADP008_PHASE_REPLAY_BINDING")
    mat = subject.materialization_receipt
    mat_ref = ExactRef("SUBJECT_MATERIALIZATION_RECEIPT", mat.receipt_id, mat.receipt_hash)
    exact_subject_fields = {
        "subject_ref": subject.subject_ref,
        "semantic_object_ref": r1._ref_dict(subject.semantic_object_ref),
        "materialization_receipt_ref": r1._ref_dict(mat_ref),
        "causal_use_permission_ref": r1._ref_dict(subject.causal_use_permission.permission_ref),
        "subject_authentication_ref": r1._ref_dict(subject_auth),
        "causal_use_authentication_ref": r1._ref_dict(subject.causal_use_permission.authentication_ref),
        "obl054_adoption_artifact_blob": subject.obl054_adoption_artifact_blob,
        "currentness_state": currentness,
    }
    for key, value in exact_subject_fields.items():
        if subject_manifest.get(key) != value:
            raise OEEIntegrityError(f"reconstructed subject replay mismatch: {key}")
    exact_phase_fields = {
        "actor_id": actor.actor_id,
        "phase_state_ref": r1._ref_dict(actor.phase_state_ref),
        "phase_state_receipt_ref": r1._ref_dict(actor.phase_state_receipt_ref),
        "phase_authentication_ref": r1._ref_dict(phase_auth),
        "phase_authority": [actor.phase_authority_id, actor.phase_authority_version, actor.phase_authority_artifact_blob_sha],
        "phase_registry": [actor.phase_registry_id, actor.phase_registry_version, actor.phase_registry_content_hash],
        "base_phase_id": actor.base_phase_id,
        "currentness_state": currentness,
    }
    for key, value in exact_phase_fields.items():
        if phase_manifest.get(key) != value:
            raise OEEIntegrityError(f"reconstructed phase replay mismatch: {key}")

    _validate_causal(record, subject, causal_receipt, currentness)

    basis_raw = body.get("opportunity_basis_evidence")
    app_acceptance_raw = body.get("applicability_acceptance_receipts") or []
    if record.realization_state == STATE_AVAILABLE:
        if basis_raw is not None or app_acceptance_raw or body.get("contact_occurrence_witness") is not None:
            raise OEEIntegrityError("AVAILABLE R2 bundle contains downstream semantic material")
    else:
        if basis_raw is None:
            raise OEEIntegrityError("OPPORTUNITY/ENCOUNTER R2 bundle lacks exact opportunity basis")
        basis = _basis(basis_raw)
        app_acceptances = tuple(_receipt(x) for x in app_acceptance_raw)
        _validate_apps(record, subject, basis, app_acceptances, currentness)

    contact_raw = body.get("contact_occurrence_witness")
    occurrence_raw = body.get("contact_occurrence_acceptance_receipt")
    independence_raw = body.get("contact_independence_acceptance_receipt")
    if record.realization_state == STATE_ENCOUNTER:
        if contact_raw is None or occurrence_raw is None or independence_raw is None:
            raise OEEIntegrityError("ENCOUNTER R2 bundle lacks exact contact constituents")
        _validate_contact(
            record,
            subject,
            _contact(contact_raw),
            _receipt(occurrence_raw),
            _receipt(independence_raw),
            currentness,
        )
    elif contact_raw is not None or occurrence_raw is not None or independence_raw is not None:
        raise OEEIntegrityError("non-ENCOUNTER R2 bundle contains contact semantic material")

    candidate_hash = w2._digest(w2._CANDIDATE_DOMAIN, w2._candidate_material(record))
    if record.source_candidate_replay_hash != candidate_hash or record.source_candidate_id != "urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash:
        raise OEEIntegrityError("OBL055 R2 source_candidate_id/replay grain mismatch")
    return record


def _seal(record: V3OEERealizationRecord, body: Mapping[str, Any]) -> OEEExecutionResult:
    bundle = _bundle_ref(record.realization_state, body)
    record = _readdress(record, (*record.provenance_refs, R2_SUCCESSOR_REF, bundle))
    return OEEExecutionResult(validate_record(record))


class _Executor:
    def __init__(self, currentness: str) -> None:
        if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
            raise OEEIntegrityError("unsupported OBL055 R2 currentness")
        self.currentness = currentness

    def admit_available(self, *, causal_use_acceptance_receipt, subject, actor, effective_from, effective_until, time_granularity, context_or_world_receipt_refs, prior_ledger_anchor_ref, provenance_refs):
        fn = r1.admit_available if self.currentness == CURRENT_ACCEPTED else r1._admit_available_noncurrent_for_test
        result = fn(
            causal_use_acceptance_receipt=causal_use_acceptance_receipt,
            subject=subject,
            actor=actor,
            effective_from=effective_from,
            effective_until=effective_until,
            time_granularity=time_granularity,
            context_or_world_receipt_refs=context_or_world_receipt_refs,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            provenance_refs=provenance_refs,
        )
        body = _source_bundle(
            state=STATE_AVAILABLE,
            currentness=self.currentness,
            subject=subject,
            actor=actor,
            causal_receipt=causal_use_acceptance_receipt,
            parent_record_id=None,
        )
        return _seal(result.record, body)

    def admit_opportunity(self, *, causal_use_acceptance_receipt, applicability_acceptance_receipts, parent_available, subject, actor, opportunity_basis, effective_from, effective_until, time_granularity, prior_ledger_anchor_ref, provenance_refs):
        validate_record(parent_available)
        fn = r1.admit_opportunity if self.currentness == CURRENT_ACCEPTED else r1._admit_opportunity_noncurrent_for_test
        result = fn(
            causal_use_acceptance_receipt=causal_use_acceptance_receipt,
            applicability_acceptance_receipts=applicability_acceptance_receipts,
            parent_available=parent_available,
            subject=subject,
            actor=actor,
            opportunity_basis=opportunity_basis,
            effective_from=effective_from,
            effective_until=effective_until,
            time_granularity=time_granularity,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            provenance_refs=provenance_refs,
        )
        body = _source_bundle(
            state=STATE_OPPORTUNITY,
            currentness=self.currentness,
            subject=subject,
            actor=actor,
            causal_receipt=causal_use_acceptance_receipt,
            parent_record_id=parent_available.record_id,
            opportunity_basis=opportunity_basis,
            applicability_receipts=tuple(applicability_acceptance_receipts),
        )
        return _seal(result.record, body)

    def admit_encounter(self, *, causal_use_acceptance_receipt, applicability_acceptance_receipts, contact_occurrence_acceptance_receipt, contact_independence_acceptance_receipt, parent_opportunity, subject, actor, contact_witness, effective_time, time_granularity, prior_ledger_anchor_ref, declared_precondition_refs, provenance_refs):
        validate_record(parent_opportunity)
        parent_bundle = _state_bundle(parent_opportunity)
        parent_basis_raw = parent_bundle.get("opportunity_basis_evidence")
        if parent_basis_raw is None:
            raise OEEIntegrityError("parent R2 opportunity lacks replay basis")
        parent_basis = _basis(parent_basis_raw)
        fn = r1.admit_encounter if self.currentness == CURRENT_ACCEPTED else r1._admit_encounter_noncurrent_for_test
        result = fn(
            causal_use_acceptance_receipt=causal_use_acceptance_receipt,
            applicability_acceptance_receipts=applicability_acceptance_receipts,
            contact_occurrence_acceptance_receipt=contact_occurrence_acceptance_receipt,
            contact_independence_acceptance_receipt=contact_independence_acceptance_receipt,
            parent_opportunity=parent_opportunity,
            subject=subject,
            actor=actor,
            contact_witness=contact_witness,
            effective_time=effective_time,
            time_granularity=time_granularity,
            prior_ledger_anchor_ref=prior_ledger_anchor_ref,
            declared_precondition_refs=declared_precondition_refs,
            provenance_refs=provenance_refs,
        )
        body = _source_bundle(
            state=STATE_ENCOUNTER,
            currentness=self.currentness,
            subject=subject,
            actor=actor,
            causal_receipt=causal_use_acceptance_receipt,
            parent_record_id=parent_opportunity.record_id,
            opportunity_basis=parent_basis,
            applicability_receipts=tuple(applicability_acceptance_receipts),
            contact_witness=contact_witness,
            occurrence_receipt=contact_occurrence_acceptance_receipt,
            independence_receipt=contact_independence_acceptance_receipt,
        )
        return _seal(result.record, body)


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


def validate_basis_available_opportunity_encounter_chain(records: Sequence[V3OEERealizationRecord]):
    if len(records) != 3:
        raise OEEAdmissionError("bounded chain must contain exactly AVAILABLE, OPPORTUNITY, ENCOUNTER")
    a, o, e = (validate_record(x) for x in records)
    return w2.validate_basis_available_opportunity_encounter_chain((a, o, e))


def authority_identity_manifest() -> dict[str, Any]:
    out = dict(r1.authority_identity_manifest())
    out["successor"] = {
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "frozen_w2_executor_blob": FROZEN_W2_EXECUTOR_BLOB,
        "frozen_r1_repair_blob": FROZEN_R1_REPAIR_BLOB,
    }
    return out


synthetic_acceptance_receipts = r1.synthetic_acceptance_receipts
_synthetic_subject = r1._synthetic_subject
_synthetic_actor = r1._synthetic_actor
_synthetic_app = r1._synthetic_app
_synthetic_basis = r1._synthetic_basis
_synthetic_contact = r1._synthetic_contact
