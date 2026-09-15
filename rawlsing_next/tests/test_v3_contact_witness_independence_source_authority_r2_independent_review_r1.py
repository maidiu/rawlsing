from dataclasses import replace
import inspect
import pytest

from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r1 as r1
from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r2 as m

REVIEWER_ID = "RABOCHII_SUBV_E_OBL060_R2_LAWFUL_INDEPENDENT_REVIEWER_R1"
NOW = 2_000_000_000


class IntSubclass(int):
    pass


def occurrence(*, fixture_class=m.FIXTURE_CLASS, authority=m.OCCURRENCE_AUTHORITY_ID,
               scope=m.OCCURRENCE_SCOPE, occurrence_id="occ-review-001",
               receipt_id="occ-receipt-review-001", receipt_digest="1" * 64):
    return m.OccurrenceEnvelope(
        fixture_class,
        receipt_id,
        authority,
        occurrence_id,
        scope,
        receipt_digest,
    )


def source(*, fixture_class=m.FIXTURE_CLASS, kind="DISTINCT_SOURCE_OWNER_WITNESS_RECORD@1.0.0",
           record_id="source-review-001", authority=m.AUTHORITY_REF,
           occurrence_id="occ-review-001", scope=m.INDEPENDENCE_SCOPE,
           bases=(m.POSITIVE_BASIS,), evidence_digest="2" * 64):
    return m.IndependenceSourceRecord(
        fixture_class,
        kind,
        record_id,
        authority,
        occurrence_id,
        scope,
        tuple(bases) if isinstance(bases, tuple) else bases,
        evidence_digest,
    )


def receipt(o=None, s=None, *, receipt_id="ind-review-001",
            issued_at_epoch=NOW - 100, expires_at_epoch=NOW + 100):
    o = o or occurrence()
    s = s or source()
    return m.issue_noncurrent_synthetic_receipt(
        o,
        s,
        receipt_id=receipt_id,
        issued_at_epoch=issued_at_epoch,
        expires_at_epoch=expires_at_epoch,
    )


def reject(fn, *args, **kwargs):
    with pytest.raises(m.IndependenceProofError):
        fn(*args, **kwargs)


def recompute(r):
    draft = replace(r, receipt_digest="")
    return replace(draft, receipt_digest=m.receipt_digest(draft))


def test_review_identity_is_independent_from_both_authority_roles():
    assert REVIEWER_ID != m.AUTHORITY_REF
    assert REVIEWER_ID != m.OCCURRENCE_AUTHORITY_ID
    assert m.AUTHORITY_REF != m.OCCURRENCE_AUTHORITY_ID


def test_r2_preserves_r1_authority_and_jurisdiction_identities():
    assert m.AUTHORITY_REF == r1.AUTHORITY_REF
    assert m.RECEIPT_KIND == r1.RECEIPT_KIND
    assert m.OCCURRENCE_AUTHORITY_ID == r1.OCCURRENCE_AUTHORITY_ID
    assert m.OCCURRENCE_SCOPE == r1.OCCURRENCE_SCOPE
    assert m.INDEPENDENCE_SCOPE == r1.INDEPENDENCE_SCOPE
    assert m.FIXTURE_CLASS == r1.FIXTURE_CLASS == "NONCURRENT_SYNTHETIC"


def test_lawful_noncurrent_synthetic_control_passes_narrowly():
    o = occurrence(); s = source(); r = receipt(o, s)
    m.validate_receipt(r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)
    assert r.authority_id != o.authority_id
    assert r.receipt_id != o.receipt_id
    assert r.source_record_id != o.receipt_id


def test_source_owner_cannot_collapse_into_occurrence_authority():
    s = source(authority=m.OCCURRENCE_AUTHORITY_ID)
    reject(m.validate_source_record, s, expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_occurrence_authority_fails_closed():
    o = occurrence(authority=m.AUTHORITY_REF)
    reject(m.issue_noncurrent_synthetic_receipt, o, source(), receipt_id="x",
           issued_at_epoch=1, expires_at_epoch=2)


def test_receipt_authority_cannot_collapse_into_occurrence_authority():
    o = occurrence(); s = source(); r = replace(receipt(o, s), authority_id=o.authority_id)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_occurrence_receipt_cannot_be_source_record_self_certification():
    o = occurrence(); s = source(record_id=o.receipt_id)
    reject(m.issue_noncurrent_synthetic_receipt, o, s, receipt_id="ind-x",
           issued_at_epoch=1, expires_at_epoch=2)


def test_occurrence_receipt_id_cannot_be_independence_receipt_id():
    o = occurrence()
    reject(m.issue_noncurrent_synthetic_receipt, o, source(), receipt_id=o.receipt_id,
           issued_at_epoch=1, expires_at_epoch=2)


def test_source_record_id_cannot_be_independence_receipt_id():
    s = source()
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), s, receipt_id=s.record_id,
           issued_at_epoch=1, expires_at_epoch=2)


def test_occurrence_receipt_digest_cannot_be_source_evidence():
    o = occurrence(); s = source(evidence_digest=o.receipt_digest)
    reject(m.issue_noncurrent_synthetic_receipt, o, s, receipt_id="ind-x",
           issued_at_epoch=1, expires_at_epoch=2)


@pytest.mark.parametrize("basis", sorted(m.REJECTED_BASES))
def test_each_mandatory_rejection_basis_fails_independently(basis):
    reject(m.validate_source_record, source(bases=(basis,)),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


@pytest.mark.parametrize("bases", [
    (m.POSITIVE_BASIS, "CO_LOCATION"),
    (m.POSITIVE_BASIS, "NARRATIVE_PLAUSIBILITY", "SHARED_ENDPOINT"),
    tuple(sorted(m.REJECTED_BASES)),
    ("CO_PRESENCE", "SAME_GEOGRAPHY_TIME", "INSTITUTION_CLASSIFICATION"),
    (m.POSITIVE_BASIS, "PLAUSIBLE_OTHER_BASIS"),
    (m.POSITIVE_BASIS, " co_location "),
    (m.POSITIVE_BASIS, "Co_Location"),
])
def test_rejection_or_unknown_basis_mixtures_cannot_launder(bases):
    reject(m.validate_source_record, source(bases=bases),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_non_tuple_basis_container_is_malformed():
    s = source(bases=[m.POSITIVE_BASIS])
    reject(m.validate_source_record, s, expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


@pytest.mark.parametrize("fixture", ["PROJECT_CURRENT", "CURRENT", "NONCURRENT", "", None])
def test_non_synthetic_source_fixture_fails(fixture):
    reject(m.validate_source_record, source(fixture_class=fixture),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


@pytest.mark.parametrize("fixture", ["PROJECT_CURRENT", "CURRENT", "", None])
def test_non_synthetic_occurrence_fixture_fails(fixture):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(fixture_class=fixture), source(),
           receipt_id="ind-x", issued_at_epoch=1, expires_at_epoch=2)


def test_wrong_expected_occurrence_fails():
    o = occurrence(); s = source(); r = receipt(o, s)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="other", now_epoch=NOW)


def test_wrong_source_occurrence_fails():
    reject(m.validate_source_record, source(occurrence_id="other"),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_occurrence_scope_fails():
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(scope="WRONG"), source(),
           receipt_id="ind-x", issued_at_epoch=1, expires_at_epoch=2)


def test_wrong_independence_scope_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), scope="WRONG")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_source_scope_fails():
    reject(m.validate_source_record, source(scope="WRONG"),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_source_owner_authority_fails():
    reject(m.validate_source_record, source(authority="OTHER_AUTHORITY@1.0.0"),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_receipt_occurrence_authority_binding_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), occurrence_authority_id="OTHER")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_occurrence_receipt_binding_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), occurrence_receipt_id="other")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_source_record_binding_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), source_record_id="other")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_source_record_digest_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), source_record_digest="f" * 64)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_malformed_occurrence_digest_fails():
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(receipt_digest="bad"), source(),
           receipt_id="ind-x", issued_at_epoch=1, expires_at_epoch=2)


def test_malformed_source_evidence_digest_fails():
    reject(m.validate_source_record, source(evidence_digest="bad"),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_malformed_independence_receipt_digest_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), receipt_digest="bad")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_receipt_digest_tamper_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), receipt_id="tampered")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_receipt_kind_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), receipt_kind="WRONG")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_wrong_source_record_kind_fails():
    reject(m.validate_source_record, source(kind="WRONG"),
           expected_occurrence_id="occ-review-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_malformed_receipt_object_fails_closed():
    reject(m.validate_receipt, {}, occurrence(), source(),
           expected_occurrence_id="occ-review-001", now_epoch=NOW)


@pytest.mark.parametrize("bad", [True, False, 1.0, "1", None, IntSubclass(1)])
def test_r2_issuance_rejects_non_exact_int_issued_at(bad):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind-x",
           issued_at_epoch=bad, expires_at_epoch=2)


@pytest.mark.parametrize("bad", [True, False, 2.0, "2", None, IntSubclass(2)])
def test_r2_issuance_rejects_non_exact_int_expires_at(bad):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind-x",
           issued_at_epoch=1, expires_at_epoch=bad)


@pytest.mark.parametrize("field,bad", [
    ("issued_at_epoch", True),
    ("issued_at_epoch", False),
    ("issued_at_epoch", IntSubclass(NOW - 100)),
    ("issued_at_epoch", float(NOW - 100)),
    ("expires_at_epoch", True),
    ("expires_at_epoch", False),
    ("expires_at_epoch", IntSubclass(NOW + 100)),
    ("expires_at_epoch", float(NOW + 100)),
])
def test_r2_validation_rejects_non_exact_int_receipt_timestamps(field, bad):
    o = occurrence(); s = source(); r = replace(receipt(o, s), **{field: bad})
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


@pytest.mark.parametrize("bad", [True, False, IntSubclass(NOW), float(NOW), str(NOW), None])
def test_r2_validation_rejects_non_exact_int_now(bad):
    o = occurrence(); s = source(); r = receipt(o, s)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=bad)


def test_r1_boolean_timestamp_receipt_cannot_launder_through_r2_validation():
    o = occurrence(); s = source()
    malformed_r1 = r1.issue_noncurrent_synthetic_receipt(
        o, s, receipt_id="r1-bool-receipt", issued_at_epoch=True, expires_at_epoch=2
    )
    assert malformed_r1.issued_at_epoch is True
    reject(m.validate_receipt, malformed_r1, o, s,
           expected_occurrence_id=o.occurrence_id, now_epoch=1)


@pytest.mark.parametrize("issued,expires", [(10, 10), (11, 10)])
def test_invalid_time_windows_fail(issued, expires):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind-x",
           issued_at_epoch=issued, expires_at_epoch=expires)


def test_stale_receipt_fails():
    o = occurrence(); s = source()
    r = receipt(o, s, issued_at_epoch=NOW - 20, expires_at_epoch=NOW - 10)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_not_yet_valid_receipt_fails():
    o = occurrence(); s = source()
    r = receipt(o, s, issued_at_epoch=NOW + 10, expires_at_epoch=NOW + 20)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


@pytest.mark.parametrize("bases", [
    (m.POSITIVE_BASIS, "CO_LOCATION"),
    (m.POSITIVE_BASIS, "UNKNOWN_OTHER"),
])
def test_recomputed_receipt_digest_cannot_launder_bad_basis(bases):
    o = occurrence(); s = source(); r = receipt(o, s)
    bad = recompute(replace(r, basis_codes=bases))
    reject(m.validate_receipt, bad, o, s, expected_occurrence_id=o.occurrence_id, now_epoch=NOW)


def test_forbidden_effect_surfaces_are_absent():
    assert not (set(dir(m)) & m.FORBIDDEN_EFFECT_SURFACES)


def test_candidate_has_no_external_io_or_current_mutation_mechanism():
    src = inspect.getsource(m)
    for forbidden in ("requests", "urllib", "subprocess", "sqlite", "psycopg", "boto3", "open(", "Path("):
        assert forbidden not in src
    assert m.FIXTURE_CLASS == "NONCURRENT_SYNTHETIC"


def test_r2_repair_is_narrow_wrapper_with_exact_int_gate():
    src = inspect.getsource(m)
    assert "type(value) is not int" in src
    assert "_r1.issue_noncurrent_synthetic_receipt" in src
    assert "_r1.validate_receipt" in src
    assert "isinstance(value, int)" not in src
