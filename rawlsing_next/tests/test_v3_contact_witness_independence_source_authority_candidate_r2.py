from dataclasses import replace
import inspect
import pytest
from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r2 as m

NOW = 2_000_000_000


def occurrence():
    return m.OccurrenceEnvelope(
        m.FIXTURE_CLASS,
        "occ-receipt-001",
        m.OCCURRENCE_AUTHORITY_ID,
        "occ-001",
        m.OCCURRENCE_SCOPE,
        "1" * 64,
    )


def source(*, bases=(m.POSITIVE_BASIS,), occurrence_id="occ-001", authority=m.AUTHORITY_REF,
           evidence_digest="2" * 64, record_id="source-record-001", scope=m.INDEPENDENCE_SCOPE,
           fixture_class=m.FIXTURE_CLASS):
    return m.IndependenceSourceRecord(
        fixture_class,
        "DISTINCT_SOURCE_OWNER_WITNESS_RECORD@1.0.0",
        record_id,
        authority,
        occurrence_id,
        scope,
        tuple(bases),
        evidence_digest,
    )


def receipt(o=None, s=None):
    o = o or occurrence()
    s = s or source()
    return m.issue_noncurrent_synthetic_receipt(
        o,
        s,
        receipt_id="ind-receipt-001",
        issued_at_epoch=NOW - 100,
        expires_at_epoch=NOW + 100,
    )


def reject(fn, *args, **kwargs):
    with pytest.raises(m.IndependenceProofError):
        fn(*args, **kwargs)


def test_positive_noncurrent_synthetic_passes_only_distinct_source_owner_contract():
    o = occurrence(); s = source(); r = receipt(o, s)
    m.validate_receipt(r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)
    assert r.authority_id != o.authority_id
    assert r.source_record_id != o.receipt_id


def test_occurrence_and_independence_authorities_are_distinct():
    assert m.AUTHORITY_REF != m.OCCURRENCE_AUTHORITY_ID


def test_wrong_occurrence_authority_fails_closed():
    o = replace(occurrence(), authority_id=m.AUTHORITY_REF)
    reject(m.issue_noncurrent_synthetic_receipt, o, source(), receipt_id="x", issued_at_epoch=1, expires_at_epoch=2)


def test_source_owner_identity_reuse_fails_closed():
    reject(m.validate_source_record, source(authority=m.OCCURRENCE_AUTHORITY_ID),
           expected_occurrence_id="occ-001", expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_occurrence_receipt_cannot_self_certify_independence():
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(record_id=occurrence().receipt_id),
           receipt_id="ind", issued_at_epoch=1, expires_at_epoch=2)


def test_independence_receipt_cannot_be_replaced_by_occurrence_receipt_reuse():
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id=occurrence().receipt_id,
           issued_at_epoch=1, expires_at_epoch=2)


def test_occurrence_receipt_digest_cannot_be_reused_as_independence_evidence():
    o = occurrence()
    reject(m.issue_noncurrent_synthetic_receipt, o, source(evidence_digest=o.receipt_digest),
           receipt_id="ind", issued_at_epoch=1, expires_at_epoch=2)


@pytest.mark.parametrize("basis", sorted(m.REJECTED_BASES))
def test_each_mandatory_rejection_basis_fails_independently(basis):
    reject(m.validate_source_record, source(bases=(basis,)), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


@pytest.mark.parametrize("mix", [
    tuple(sorted(m.REJECTED_BASES)),
    (m.POSITIVE_BASIS, "CO_LOCATION"),
    (m.POSITIVE_BASIS, "NARRATIVE_PLAUSIBILITY", "SHARED_ENDPOINT"),
    ("CO_PRESENCE", "SAME_GEOGRAPHY_TIME", "INSTITUTION_CLASSIFICATION"),
])
def test_rejected_basis_mixtures_cannot_be_laundered(mix):
    reject(m.validate_source_record, source(bases=mix), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_unknown_basis_cannot_launder_positive():
    reject(m.validate_source_record, source(bases=(m.POSITIVE_BASIS, "PLAUSIBLE_OTHER_BASIS")),
           expected_occurrence_id="occ-001", expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


@pytest.mark.parametrize("bad", ["PROJECT_CURRENT", "CURRENT", "", None])
def test_project_current_or_malformed_fixture_class_fails(bad):
    reject(m.validate_source_record, source(fixture_class=bad), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_occurrence_fails():
    o = occurrence(); s = source(); r = receipt(o, s)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="other", now_epoch=NOW)


def test_wrong_source_occurrence_fails():
    reject(m.validate_source_record, source(occurrence_id="other"), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_source_scope_fails():
    reject(m.validate_source_record, source(scope="WRONG"), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_wrong_occurrence_scope_fails():
    reject(m.issue_noncurrent_synthetic_receipt, replace(occurrence(), scope="WRONG"), source(),
           receipt_id="ind", issued_at_epoch=1, expires_at_epoch=2)


def test_wrong_independence_receipt_scope_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), scope="WRONG")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_wrong_receipt_authority_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), authority_id="OTHER")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_wrong_occurrence_binding_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), occurrence_receipt_id="other")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_wrong_source_record_binding_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), source_record_id="other")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_wrong_source_record_digest_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), source_record_digest="f" * 64)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_malformed_occurrence_digest_fails():
    reject(m.issue_noncurrent_synthetic_receipt, replace(occurrence(), receipt_digest="bad"), source(),
           receipt_id="ind", issued_at_epoch=1, expires_at_epoch=2)


def test_malformed_source_evidence_digest_fails():
    reject(m.validate_source_record, source(evidence_digest="bad"), expected_occurrence_id="occ-001",
           expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)


def test_malformed_independence_receipt_digest_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), receipt_digest="bad")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_tampered_receipt_digest_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), receipt_id="tampered")
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_stale_receipt_fails():
    o = occurrence(); s = source()
    r = m.issue_noncurrent_synthetic_receipt(o, s, receipt_id="ind", issued_at_epoch=NOW - 20, expires_at_epoch=NOW - 10)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_not_yet_valid_receipt_fails():
    o = occurrence(); s = source()
    r = m.issue_noncurrent_synthetic_receipt(o, s, receipt_id="ind", issued_at_epoch=NOW + 10, expires_at_epoch=NOW + 20)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_invalid_time_window_fails():
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind", issued_at_epoch=10, expires_at_epoch=10)


def test_receipt_basis_tamper_fails():
    o = occurrence(); s = source(); r = replace(receipt(o, s), basis_codes=(m.POSITIVE_BASIS, "CO_LOCATION"))
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


def test_malformed_object_fails_closed():
    reject(m.validate_receipt, {}, occurrence(), source(), expected_occurrence_id="occ-001", now_epoch=NOW)


@pytest.mark.parametrize("bad", [True, False])
def test_repair_boolean_issued_at_fails_closed_at_issuance(bad):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind",
           issued_at_epoch=bad, expires_at_epoch=2)


@pytest.mark.parametrize("bad", [True, False])
def test_repair_boolean_expires_at_fails_closed_at_issuance(bad):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind",
           issued_at_epoch=1, expires_at_epoch=bad)


@pytest.mark.parametrize("field", ["issued_at_epoch", "expires_at_epoch"])
def test_repair_boolean_receipt_timestamp_fails_closed_at_validation(field):
    o = occurrence(); s = source(); r = receipt(o, s)
    bad = replace(r, **{field: True})
    reject(m.validate_receipt, bad, o, s, expected_occurrence_id="occ-001", now_epoch=NOW)


@pytest.mark.parametrize("bad", [True, False])
def test_repair_boolean_now_fails_closed_at_validation(bad):
    o = occurrence(); s = source(); r = receipt(o, s)
    reject(m.validate_receipt, r, o, s, expected_occurrence_id="occ-001", now_epoch=bad)


class IntSubclass(int):
    pass


@pytest.mark.parametrize("bad", [IntSubclass(1)])
def test_repair_integer_subclasses_fail_closed(bad):
    reject(m.issue_noncurrent_synthetic_receipt, occurrence(), source(), receipt_id="ind",
           issued_at_epoch=bad, expires_at_epoch=2)


def test_forbidden_effect_surfaces_are_absent():
    assert not (set(dir(m)) & m.FORBIDDEN_EFFECT_SURFACES)


def test_module_has_no_project_current_mutation_or_external_io_imports():
    src = inspect.getsource(m)
    for forbidden in ("requests", "urllib", "subprocess", "sqlite", "psycopg", "boto3", "open(", "Path("):
        assert forbidden not in src
    assert m.FIXTURE_CLASS == "NONCURRENT_SYNTHETIC"
