"""OBL060 candidate contact-witness-independence source authority.

Candidate only. No project-current effect; NONCURRENT_SYNTHETIC fixtures only.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
import hashlib
import json
import re

AUTHORITY_ID = "V3_CONTACT_WITNESS_INDEPENDENCE_SOURCE_AUTHORITY_CANDIDATE"
AUTHORITY_VERSION = "1.0.0"
AUTHORITY_REF = f"{AUTHORITY_ID}@{AUTHORITY_VERSION}"
RECEIPT_KIND = "V3_CONTACT_WITNESS_INDEPENDENCE_RECEIPT_CANDIDATE@1.0.0"
OCCURRENCE_AUTHORITY_ID = "V3_EXTERNAL_INTERACTION_EVENT_ADMISSION_RULE@1.0.0"
OCCURRENCE_SCOPE = "ADP-019/EXTERNAL_INTERACTION_EVENT_OCCURRENCE@1.0.0"
INDEPENDENCE_SCOPE = "ADP-010/OEE_CONTACT_WITNESS_INDEPENDENCE@1.0.0"
FIXTURE_CLASS = "NONCURRENT_SYNTHETIC"
POSITIVE_BASIS = "DISTINCT_SOURCE_OWNER_BOUND_WITNESS_RECORD"
REJECTED_BASES = frozenset({
    "SELF_CERTIFICATION", "AUTHORITY_IDENTITY_REUSE", "RECEIPT_REUSE",
    "CO_LOCATION", "CO_PRESENCE", "SAME_GEOGRAPHY_TIME", "SHARED_ENDPOINT",
    "INSTITUTION_CLASSIFICATION", "NARRATIVE_PLAUSIBILITY",
})
_HEX64 = re.compile(r"^[0-9a-f]{64}$")

class IndependenceProofError(ValueError):
    """Fail-closed candidate contract rejection."""

@dataclass(frozen=True)
class OccurrenceEnvelope:
    fixture_class: str
    receipt_id: str
    authority_id: str
    occurrence_id: str
    scope: str
    receipt_digest: str

@dataclass(frozen=True)
class IndependenceSourceRecord:
    fixture_class: str
    record_kind: str
    record_id: str
    source_owner_authority_id: str
    occurrence_id: str
    scope: str
    basis_codes: tuple[str, ...]
    evidence_digest: str

@dataclass(frozen=True)
class IndependenceReceipt:
    fixture_class: str
    receipt_kind: str
    receipt_id: str
    authority_id: str
    occurrence_id: str
    occurrence_authority_id: str
    occurrence_receipt_id: str
    scope: str
    source_record_id: str
    source_record_digest: str
    basis_codes: tuple[str, ...]
    issued_at_epoch: int
    expires_at_epoch: int
    receipt_digest: str

def _canonical_hash(material: object) -> str:
    if hasattr(material, "__dataclass_fields__"):
        material = asdict(material)
    payload = json.dumps(material, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def source_record_digest(record: IndependenceSourceRecord) -> str:
    return _canonical_hash(record)

def _receipt_material(receipt: IndependenceReceipt) -> dict:
    d = asdict(receipt)
    d.pop("receipt_digest", None)
    return d

def receipt_digest(receipt: IndependenceReceipt) -> str:
    return _canonical_hash(_receipt_material(receipt))

def _require_nonempty(value: str, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise IndependenceProofError(f"{label}: missing-or-malformed")

def _require_hex64(value: str, label: str) -> None:
    if not isinstance(value, str) or _HEX64.fullmatch(value) is None:
        raise IndependenceProofError(f"{label}: malformed-digest")

def _validate_common_fixture(*fixture_classes: str) -> None:
    if any(x != FIXTURE_CLASS for x in fixture_classes):
        raise IndependenceProofError("project-current-or-nonsynthetic-fixture-forbidden")

def validate_source_record(record: IndependenceSourceRecord, *, expected_occurrence_id: str,
                           expected_occurrence_authority_id: str = OCCURRENCE_AUTHORITY_ID) -> None:
    if not isinstance(record, IndependenceSourceRecord):
        raise IndependenceProofError("source-record: malformed")
    _validate_common_fixture(record.fixture_class)
    _require_nonempty(expected_occurrence_id, "expected-occurrence-id")
    if expected_occurrence_authority_id != OCCURRENCE_AUTHORITY_ID:
        raise IndependenceProofError("occurrence-authority: mismatch")
    if record.record_kind != "DISTINCT_SOURCE_OWNER_WITNESS_RECORD@1.0.0":
        raise IndependenceProofError("source-record-kind: wrong")
    _require_nonempty(record.record_id, "source-record-id")
    if record.source_owner_authority_id != AUTHORITY_REF:
        raise IndependenceProofError("independence-source-owner-authority: mismatch")
    if record.source_owner_authority_id == expected_occurrence_authority_id:
        raise IndependenceProofError("authority-identity-reuse")
    if record.occurrence_id != expected_occurrence_id:
        raise IndependenceProofError("source-record: wrong-occurrence")
    if record.scope != INDEPENDENCE_SCOPE:
        raise IndependenceProofError("source-record: wrong-scope")
    if not isinstance(record.basis_codes, tuple) or not record.basis_codes:
        raise IndependenceProofError("source-record: malformed-bases")
    bases = set(record.basis_codes)
    rejected = bases & REJECTED_BASES
    if rejected:
        raise IndependenceProofError("rejected-independence-basis:" + ",".join(sorted(rejected)))
    if bases != {POSITIVE_BASIS}:
        raise IndependenceProofError("source-record: unrecognized-or-laundered-basis")
    _require_hex64(record.evidence_digest, "source-evidence")

def issue_noncurrent_synthetic_receipt(occurrence: OccurrenceEnvelope, source_record: IndependenceSourceRecord,
                                       *, receipt_id: str, issued_at_epoch: int,
                                       expires_at_epoch: int) -> IndependenceReceipt:
    if not isinstance(occurrence, OccurrenceEnvelope):
        raise IndependenceProofError("occurrence-envelope: malformed")
    _validate_common_fixture(occurrence.fixture_class, source_record.fixture_class)
    _require_nonempty(occurrence.receipt_id, "occurrence-receipt-id")
    if occurrence.authority_id != OCCURRENCE_AUTHORITY_ID:
        raise IndependenceProofError("occurrence-authority: mismatch")
    if occurrence.scope != OCCURRENCE_SCOPE:
        raise IndependenceProofError("occurrence-envelope: wrong-scope")
    _require_nonempty(occurrence.occurrence_id, "occurrence-id")
    _require_hex64(occurrence.receipt_digest, "occurrence-receipt")
    validate_source_record(source_record, expected_occurrence_id=occurrence.occurrence_id,
                           expected_occurrence_authority_id=occurrence.authority_id)
    _require_nonempty(receipt_id, "independence-receipt-id")
    if receipt_id in {occurrence.receipt_id, source_record.record_id}:
        raise IndependenceProofError("receipt-reuse")
    if source_record.record_id == occurrence.receipt_id:
        raise IndependenceProofError("occurrence-receipt-cannot-be-independence-proof")
    source_digest = source_record_digest(source_record)
    if source_record.evidence_digest == occurrence.receipt_digest:
        raise IndependenceProofError("occurrence-receipt-digest-reuse")
    if not isinstance(issued_at_epoch, int) or not isinstance(expires_at_epoch, int):
        raise IndependenceProofError("receipt-time: malformed")
    if expires_at_epoch <= issued_at_epoch:
        raise IndependenceProofError("receipt-time: invalid-window")
    draft = IndependenceReceipt(FIXTURE_CLASS, RECEIPT_KIND, receipt_id, AUTHORITY_REF,
        occurrence.occurrence_id, occurrence.authority_id, occurrence.receipt_id, INDEPENDENCE_SCOPE,
        source_record.record_id, source_digest, source_record.basis_codes,
        issued_at_epoch, expires_at_epoch, "")
    return IndependenceReceipt(**{**asdict(draft), "receipt_digest": receipt_digest(draft)})

def validate_receipt(receipt: IndependenceReceipt, occurrence: OccurrenceEnvelope,
                     source_record: IndependenceSourceRecord, *, expected_occurrence_id: str,
                     now_epoch: int) -> None:
    if not isinstance(receipt, IndependenceReceipt):
        raise IndependenceProofError("independence-receipt: malformed")
    if not isinstance(occurrence, OccurrenceEnvelope):
        raise IndependenceProofError("occurrence-envelope: malformed")
    _validate_common_fixture(receipt.fixture_class, occurrence.fixture_class, source_record.fixture_class)
    if receipt.receipt_kind != RECEIPT_KIND:
        raise IndependenceProofError("independence-receipt-kind: wrong")
    if receipt.authority_id != AUTHORITY_REF:
        raise IndependenceProofError("independence-authority: mismatch")
    if receipt.authority_id == occurrence.authority_id:
        raise IndependenceProofError("authority-identity-reuse")
    if occurrence.authority_id != OCCURRENCE_AUTHORITY_ID:
        raise IndependenceProofError("occurrence-authority: mismatch")
    if occurrence.scope != OCCURRENCE_SCOPE:
        raise IndependenceProofError("occurrence-envelope: wrong-scope")
    if receipt.scope != INDEPENDENCE_SCOPE:
        raise IndependenceProofError("independence-receipt: wrong-scope")
    if receipt.occurrence_id != expected_occurrence_id or occurrence.occurrence_id != expected_occurrence_id:
        raise IndependenceProofError("wrong-occurrence")
    if receipt.occurrence_authority_id != occurrence.authority_id:
        raise IndependenceProofError("receipt-occurrence-authority: mismatch")
    if receipt.occurrence_receipt_id != occurrence.receipt_id:
        raise IndependenceProofError("receipt-occurrence-binding: mismatch")
    if receipt.receipt_id in {occurrence.receipt_id, source_record.record_id}:
        raise IndependenceProofError("receipt-reuse")
    if source_record.record_id == occurrence.receipt_id:
        raise IndependenceProofError("occurrence-receipt-cannot-be-independence-proof")
    validate_source_record(source_record, expected_occurrence_id=expected_occurrence_id,
                           expected_occurrence_authority_id=occurrence.authority_id)
    if receipt.source_record_id != source_record.record_id:
        raise IndependenceProofError("source-record-binding: mismatch")
    if receipt.source_record_digest != source_record_digest(source_record):
        raise IndependenceProofError("source-record-digest: mismatch")
    if source_record.evidence_digest == occurrence.receipt_digest:
        raise IndependenceProofError("occurrence-receipt-digest-reuse")
    if tuple(receipt.basis_codes) != tuple(source_record.basis_codes):
        raise IndependenceProofError("basis-binding: mismatch")
    if set(receipt.basis_codes) & REJECTED_BASES:
        raise IndependenceProofError("receipt-contains-rejected-basis")
    if set(receipt.basis_codes) != {POSITIVE_BASIS}:
        raise IndependenceProofError("receipt-basis: not-exact-positive-contract")
    _require_hex64(receipt.receipt_digest, "independence-receipt")
    if receipt.receipt_digest != receipt_digest(receipt):
        raise IndependenceProofError("independence-receipt-digest: mismatch")
    if not isinstance(now_epoch, int):
        raise IndependenceProofError("now: malformed")
    if receipt.expires_at_epoch <= receipt.issued_at_epoch:
        raise IndependenceProofError("receipt-time: invalid-window")
    if now_epoch < receipt.issued_at_epoch:
        raise IndependenceProofError("receipt: not-yet-valid")
    if now_epoch >= receipt.expires_at_epoch:
        raise IndependenceProofError("receipt: stale")

FORBIDDEN_EFFECT_SURFACES = frozenset({
    "admit_occurrence", "create_occurrence", "activate_actor", "issue_positive_applicability",
    "issue_causal_use_permission", "create_encounter", "realize_oee",
    "install_project_current_independence", "execute_obl055", "install_obl056_current_positive",
})
