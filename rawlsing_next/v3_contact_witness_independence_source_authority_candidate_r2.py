"""OBL060 bounded-repair R2 contact-witness-independence source authority.

Successor wrapper over the frozen R1 candidate. The only semantic repair is exact-integer
receipt-time enforcement so Python booleans cannot satisfy integer timestamp requirements.
Candidate only. No project-current effect; NONCURRENT_SYNTHETIC fixtures only.
"""
from __future__ import annotations

from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r1 as _r1

AUTHORITY_ID = _r1.AUTHORITY_ID
AUTHORITY_VERSION = _r1.AUTHORITY_VERSION
AUTHORITY_REF = _r1.AUTHORITY_REF
RECEIPT_KIND = _r1.RECEIPT_KIND
OCCURRENCE_AUTHORITY_ID = _r1.OCCURRENCE_AUTHORITY_ID
OCCURRENCE_SCOPE = _r1.OCCURRENCE_SCOPE
INDEPENDENCE_SCOPE = _r1.INDEPENDENCE_SCOPE
FIXTURE_CLASS = _r1.FIXTURE_CLASS
POSITIVE_BASIS = _r1.POSITIVE_BASIS
REJECTED_BASES = _r1.REJECTED_BASES
FORBIDDEN_EFFECT_SURFACES = _r1.FORBIDDEN_EFFECT_SURFACES

IndependenceProofError = _r1.IndependenceProofError
OccurrenceEnvelope = _r1.OccurrenceEnvelope
IndependenceSourceRecord = _r1.IndependenceSourceRecord
IndependenceReceipt = _r1.IndependenceReceipt

source_record_digest = _r1.source_record_digest
receipt_digest = _r1.receipt_digest
validate_source_record = _r1.validate_source_record


def _require_exact_int(value: object, label: str) -> None:
    """Require the exact built-in int type; bool and int subclasses fail closed."""
    if type(value) is not int:
        raise IndependenceProofError(f"{label}: malformed")


def issue_noncurrent_synthetic_receipt(
    occurrence: OccurrenceEnvelope,
    source_record: IndependenceSourceRecord,
    *,
    receipt_id: str,
    issued_at_epoch: int,
    expires_at_epoch: int,
) -> IndependenceReceipt:
    _require_exact_int(issued_at_epoch, "receipt-issued-at")
    _require_exact_int(expires_at_epoch, "receipt-expires-at")
    return _r1.issue_noncurrent_synthetic_receipt(
        occurrence,
        source_record,
        receipt_id=receipt_id,
        issued_at_epoch=issued_at_epoch,
        expires_at_epoch=expires_at_epoch,
    )


def validate_receipt(
    receipt: IndependenceReceipt,
    occurrence: OccurrenceEnvelope,
    source_record: IndependenceSourceRecord,
    *,
    expected_occurrence_id: str,
    now_epoch: int,
) -> None:
    if not isinstance(receipt, IndependenceReceipt):
        raise IndependenceProofError("independence-receipt: malformed")
    _require_exact_int(receipt.issued_at_epoch, "receipt-issued-at")
    _require_exact_int(receipt.expires_at_epoch, "receipt-expires-at")
    _require_exact_int(now_epoch, "now")
    _r1.validate_receipt(
        receipt,
        occurrence,
        source_record,
        expected_occurrence_id=expected_occurrence_id,
        now_epoch=now_epoch,
    )
