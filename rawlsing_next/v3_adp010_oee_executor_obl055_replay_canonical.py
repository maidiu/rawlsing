"""GT34 OBL055 R3 successor: canonical exact replay receipt reconstruction.

This is the smallest successor to the failed R2 replay-reconstruction court.
It preserves frozen W2, the OBL056-acceptance-bound R1 repair, and the R2 replay
bundle format.  The sole defect repair is representation-safe cross-checking of
an OBL056 receipt reconstructed from the R2 source bundle against the exact
JSON-decoded receipt stored in the R1 acceptance-binding manifest.  Tuple/list
wire normalization is handled by canonical JSON equality; semantic content is
not relaxed, inferred, or minted.
"""
from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
import json
from typing import Any, Mapping, Sequence

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_authenticated as w2
import rawlsing_next.v3_adp010_oee_executor_obl055_acceptance_bound as r1
import rawlsing_next.v3_adp010_oee_executor_obl055_replay_reconstructed as r2


EXECUTOR_ID = "GT34_V3P5_ADP010_OBL056_CANONICAL_RECONSTRUCTED_REPLAY_EXECUTOR"
EXECUTOR_VERSION = "3.1.1"
FROZEN_W2_EXECUTOR_BLOB = r2.FROZEN_W2_EXECUTOR_BLOB
FROZEN_R1_REPAIR_BLOB = r2.FROZEN_R1_REPAIR_BLOB
FROZEN_R2_REPAIR_BLOB = "eb9c91b705a01868d99d3e3a564b611749e028f8"
HQ_OBL056_AUTHORITY_HASH = r2.HQ_OBL056_AUTHORITY_HASH
HQ_OBL056_IMPLEMENTATION_BLOB = r2.HQ_OBL056_IMPLEMENTATION_BLOB
HQ_OBL056_EMPTY_REGISTRY_HASH = r2.HQ_OBL056_EMPTY_REGISTRY_HASH
HQ_OBL056_ADOPTION_REF = r2.HQ_OBL056_ADOPTION_REF

ExactRef = r2.ExactRef
SubjectMaterializationReceipt = r2.SubjectMaterializationReceipt
CausalUsePermission = r2.CausalUsePermission
SubjectIngressEvidence = r2.SubjectIngressEvidence
ActorPhaseEvidence = r2.ActorPhaseEvidence
PositiveApplicabilityReceipt = r2.PositiveApplicabilityReceipt
OpportunityBasisEvidence = r2.OpportunityBasisEvidence
ContactOccurrenceWitness = r2.ContactOccurrenceWitness
V3OEERealizationRecord = r2.V3OEERealizationRecord
OEEExecutionResult = r2.OEEExecutionResult
OEEAdmissionError = r2.OEEAdmissionError
OEEIntegrityError = r2.OEEIntegrityError
OBL055AcceptanceError = r2.OBL055AcceptanceError

CURRENT_ACCEPTED = r2.CURRENT_ACCEPTED
NONCURRENT_SYNTHETIC_TEST_ONLY = r2.NONCURRENT_SYNTHETIC_TEST_ONLY
STATE_AVAILABLE = r2.STATE_AVAILABLE
STATE_OPPORTUNITY = r2.STATE_OPPORTUNITY
STATE_ENCOUNTER = r2.STATE_ENCOUNTER
R2_SUCCESSOR_REF = r2.R2_SUCCESSOR_REF
_BUNDLE_KIND = r2._BUNDLE_KIND

_R3_DOMAIN = "RAWLSING\0GT34\0OBL055\0SOURCE_REPLAY_CANONICAL_R3\0"
_R3_MATERIAL = [
    EXECUTOR_ID,
    EXECUTOR_VERSION,
    FROZEN_W2_EXECUTOR_BLOB,
    FROZEN_R1_REPAIR_BLOB,
    FROZEN_R2_REPAIR_BLOB,
    HQ_OBL056_AUTHORITY_HASH,
]
R3_SUCCESSOR_HASH = sha256(
    (_R3_DOMAIN + json.dumps(_R3_MATERIAL, sort_keys=True, separators=(",", ":"))).encode("utf-8")
).hexdigest()
R3_SUCCESSOR_REF = ExactRef(
    "OBL055_CANONICAL_RECONSTRUCTED_REPLAY_EXECUTOR",
    f"urn:rawlsing:gt34:obl055:executor:{EXECUTOR_ID}@{EXECUTOR_VERSION}",
    R3_SUCCESSOR_HASH,
)

# Preserve exact R2 bundle/readdress helpers for attack replay and diagnostics.
_state_bundle = r2._state_bundle
_decode_bundle = r2._decode_bundle
_bundle_ref = r2._bundle_ref
_readdress = r2._readdress
_basis = r2._basis


def _receipt_wire_equal(stored: Mapping[str, Any], reconstructed: acceptance.AcceptanceReceipt) -> bool:
    """Compare exact receipt content at the canonical JSON wire grain.

    JSON round-trip changes tuple-valued dataclass fields into arrays.  Canonical
    JSON equality treats only that representation change as equivalent while
    still rejecting added, removed, renamed, or mutated receipt content.
    """
    try:
        return r2._canonical(dict(stored)) == r2._canonical(asdict(reconstructed))
    except (TypeError, ValueError):
        return False


def _assert_base_binding(
    record: V3OEERealizationRecord,
    *,
    role: str,
    semantic_ref: ExactRef,
    auth_ref: ExactRef,
    receipt: acceptance.AcceptanceReceipt,
    auxiliary_ref: ExactRef | None = None,
) -> None:
    matches = []
    for body in r2._base_binding_bodies(record, role):
        try:
            semantic_matches = r1._ref_from_dict(body["semantic_evidence_ref"]) == semantic_ref
            auth_matches = r1._ref_from_dict(body["evidence_authentication_ref"]) == auth_ref
            receipt_matches = _receipt_wire_equal(body["receipt"], receipt)
            auxiliary = body.get("auxiliary_ref")
            auxiliary_matches = (
                (auxiliary is None and auxiliary_ref is None)
                or (
                    auxiliary is not None
                    and auxiliary_ref is not None
                    and r1._ref_from_dict(auxiliary) == auxiliary_ref
                )
            )
        except (KeyError, TypeError, ValueError):
            continue
        if semantic_matches and auth_matches and receipt_matches and auxiliary_matches:
            matches.append(body)
    if len(matches) != 1:
        raise OEEIntegrityError(f"reconstructed {role} source does not match exact stored OBL056 binding")


def _validate_causal(record, subject, causal_receipt, currentness):
    permission = subject.causal_use_permission
    materialization = subject.materialization_receipt
    materialization_ref = ExactRef(
        "SUBJECT_MATERIALIZATION_RECEIPT",
        materialization.receipt_id,
        materialization.receipt_hash,
    )
    w2._validate_permission(
        permission,
        subject.subject_ref,
        subject.semantic_object_ref,
        materialization_ref,
        currentness,
    )
    r1._validate_acceptance(
        causal_receipt,
        role=acceptance.CAUSAL_USE_PERMISSION,
        authority_id=permission.authority_id,
        authority_version=permission.authority_version,
        authority_hash=permission.authority_content_hash,
        subject_ref=subject.subject_ref,
        object_ref=subject.semantic_object_ref,
        currentness=currentness,
    )
    _assert_base_binding(
        record,
        role=acceptance.CAUSAL_USE_PERMISSION,
        semantic_ref=permission.permission_ref,
        auth_ref=permission.authentication_ref,
        receipt=causal_receipt,
    )


def _validate_apps(record, subject, basis, app_acceptances, currentness):
    if basis.actor_id != record.actor_id or basis.subject_ref != record.subject_ref:
        raise OEEIntegrityError("reconstructed opportunity basis actor/subject mismatch")
    apps = tuple(basis.applicability_receipts)
    if {item.receipt for item in apps} != set(record.applicability_receipt_refs):
        raise OEEIntegrityError("reconstructed applicability source set mismatch")
    by_authority = {
        (
            item.accepted_authority_ref.id,
            item.accepted_authority_ref.version,
            item.accepted_authority_ref.content_hash,
        ): item
        for item in app_acceptances
    }
    if len(by_authority) != len(app_acceptances):
        raise OEEIntegrityError("ambiguous reconstructed applicability acceptance receipts")
    required = {
        (item.authority_id, item.authority_version, item.authority_content_hash)
        for item in apps
    }
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
    if len(r2._base_binding_bodies(record, acceptance.POSITIVE_APPLICABILITY)) != len(apps):
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
    provenance = set(record.provenance_refs)
    if R2_SUCCESSOR_REF not in provenance or R3_SUCCESSOR_REF not in provenance:
        raise OEEIntegrityError("missing exact OBL055 R2/R3 successor provenance")
    body = r2._state_bundle(record)
    if body.get("schema_id") != r2._BUNDLE_SCHEMA or body.get("state") != record.realization_state:
        raise OEEIntegrityError("OBL055 R3 replay bundle state/schema mismatch")
    if body.get("parent_record_id") != record.parent_record_id:
        raise OEEIntegrityError("OBL055 R3 replay bundle parent mismatch")
    currentness = str(body.get("currentness_state"))
    if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
        raise OEEIntegrityError("OBL055 R3 replay bundle currentness invalid")

    try:
        subject = r2._subject(body["subject_ingress_evidence"])
        actor = r2._actor(body["actor_phase_evidence"])
        causal_receipt = r2._receipt(body["causal_use_acceptance_receipt"])
    except Exception as exc:
        raise OEEIntegrityError("OBL055 R3 source replay reconstruction failed") from exc

    subject, subject_auth = w2._validate_subject(subject, currentness)
    actor, phase_auth = w2._validate_actor(actor, currentness)
    if (
        subject.subject_ref != record.subject_ref
        or actor.actor_id != record.actor_id
        or actor.phase_state_ref != record.phase_state_ref
    ):
        raise OEEIntegrityError("reconstructed subject/actor does not bind record identity")

    subject_manifest = r1._single_manifest(record, "OBL055_SUBJECT_INGRESS_REPLAY_BINDING")
    phase_manifest = r1._single_manifest(record, "OBL055_ADP008_PHASE_REPLAY_BINDING")
    materialization = subject.materialization_receipt
    materialization_ref = ExactRef(
        "SUBJECT_MATERIALIZATION_RECEIPT",
        materialization.receipt_id,
        materialization.receipt_hash,
    )
    exact_subject_fields = {
        "subject_ref": subject.subject_ref,
        "semantic_object_ref": r1._ref_dict(subject.semantic_object_ref),
        "materialization_receipt_ref": r1._ref_dict(materialization_ref),
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
        "phase_authority": [
            actor.phase_authority_id,
            actor.phase_authority_version,
            actor.phase_authority_artifact_blob_sha,
        ],
        "phase_registry": [
            actor.phase_registry_id,
            actor.phase_registry_version,
            actor.phase_registry_content_hash,
        ],
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
            raise OEEIntegrityError("AVAILABLE R3 bundle contains downstream semantic material")
    else:
        if basis_raw is None:
            raise OEEIntegrityError("OPPORTUNITY/ENCOUNTER R3 bundle lacks exact opportunity basis")
        basis = r2._basis(basis_raw)
        app_acceptances = tuple(r2._receipt(item) for item in app_acceptance_raw)
        _validate_apps(record, subject, basis, app_acceptances, currentness)

    contact_raw = body.get("contact_occurrence_witness")
    occurrence_raw = body.get("contact_occurrence_acceptance_receipt")
    independence_raw = body.get("contact_independence_acceptance_receipt")
    if record.realization_state == STATE_ENCOUNTER:
        if contact_raw is None or occurrence_raw is None or independence_raw is None:
            raise OEEIntegrityError("ENCOUNTER R3 bundle lacks exact contact constituents")
        _validate_contact(
            record,
            subject,
            r2._contact(contact_raw),
            r2._receipt(occurrence_raw),
            r2._receipt(independence_raw),
            currentness,
        )
    elif contact_raw is not None or occurrence_raw is not None or independence_raw is not None:
        raise OEEIntegrityError("non-ENCOUNTER R3 bundle contains contact semantic material")

    candidate_hash = w2._digest(w2._CANDIDATE_DOMAIN, w2._candidate_material(record))
    if (
        record.source_candidate_replay_hash != candidate_hash
        or record.source_candidate_id != "urn:rawlsing:v3:oee:candidate:sha256:" + candidate_hash
    ):
        raise OEEIntegrityError("OBL055 R3 source_candidate_id/replay grain mismatch")
    return record


def _seal(record: V3OEERealizationRecord, body: Mapping[str, Any]) -> OEEExecutionResult:
    bundle = r2._bundle_ref(record.realization_state, body)
    record = r2._readdress(
        record,
        (*record.provenance_refs, R2_SUCCESSOR_REF, R3_SUCCESSOR_REF, bundle),
    )
    return OEEExecutionResult(validate_record(record))


class _Executor:
    def __init__(self, currentness: str) -> None:
        if currentness not in {CURRENT_ACCEPTED, NONCURRENT_SYNTHETIC_TEST_ONLY}:
            raise OEEIntegrityError("unsupported OBL055 R3 currentness")
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
        return _seal(
            result.record,
            r2._source_bundle(
                state=STATE_AVAILABLE,
                currentness=self.currentness,
                subject=subject,
                actor=actor,
                causal_receipt=causal_use_acceptance_receipt,
                parent_record_id=None,
            ),
        )

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
        return _seal(
            result.record,
            r2._source_bundle(
                state=STATE_OPPORTUNITY,
                currentness=self.currentness,
                subject=subject,
                actor=actor,
                causal_receipt=causal_use_acceptance_receipt,
                parent_record_id=parent_available.record_id,
                opportunity_basis=opportunity_basis,
                applicability_receipts=tuple(applicability_acceptance_receipts),
            ),
        )

    def admit_encounter(self, *, causal_use_acceptance_receipt, applicability_acceptance_receipts, contact_occurrence_acceptance_receipt, contact_independence_acceptance_receipt, parent_opportunity, subject, actor, contact_witness, effective_time, time_granularity, prior_ledger_anchor_ref, declared_precondition_refs, provenance_refs):
        validate_record(parent_opportunity)
        parent_bundle = r2._state_bundle(parent_opportunity)
        parent_basis_raw = parent_bundle.get("opportunity_basis_evidence")
        if parent_basis_raw is None:
            raise OEEIntegrityError("parent R3 opportunity lacks replay basis")
        parent_basis = r2._basis(parent_basis_raw)
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
        return _seal(
            result.record,
            r2._source_bundle(
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
            ),
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


def validate_basis_available_opportunity_encounter_chain(records: Sequence[V3OEERealizationRecord]):
    if len(records) != 3:
        raise OEEAdmissionError("bounded chain must contain exactly AVAILABLE, OPPORTUNITY, ENCOUNTER")
    available, opportunity, encounter = (validate_record(record) for record in records)
    return w2.validate_basis_available_opportunity_encounter_chain((available, opportunity, encounter))


def authority_identity_manifest() -> dict[str, Any]:
    out = dict(r2.authority_identity_manifest())
    out["r3_successor"] = {
        "executor_id": EXECUTOR_ID,
        "executor_version": EXECUTOR_VERSION,
        "frozen_w2_executor_blob": FROZEN_W2_EXECUTOR_BLOB,
        "frozen_r1_repair_blob": FROZEN_R1_REPAIR_BLOB,
        "frozen_r2_repair_blob": FROZEN_R2_REPAIR_BLOB,
        "repair_grain": "CANONICAL_JSON_RECEIPT_WIRE_EQUIVALENCE_ONLY",
    }
    return out


synthetic_acceptance_receipts = r2.synthetic_acceptance_receipts
_synthetic_subject = r2._synthetic_subject
_synthetic_actor = r2._synthetic_actor
_synthetic_app = r2._synthetic_app
_synthetic_basis = r2._synthetic_basis
_synthetic_contact = r2._synthetic_contact
