from dataclasses import replace
import pytest
from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r1 as m

NOW=2_000_000_000

def occ(**kw):
    x=m.OccurrenceEnvelope(m.FIXTURE_CLASS,"occ-r",m.OCCURRENCE_AUTHORITY_ID,"occ-1",m.OCCURRENCE_SCOPE,"1"*64)
    return replace(x,**kw)

def src(**kw):
    x=m.IndependenceSourceRecord(m.FIXTURE_CLASS,"DISTINCT_SOURCE_OWNER_WITNESS_RECORD@1.0.0",
        "src-r",m.AUTHORITY_REF,"occ-1",m.INDEPENDENCE_SCOPE,(m.POSITIVE_BASIS,),"2"*64)
    return replace(x,**kw)

def issue(o=None,s=None,**kw):
    return m.issue_noncurrent_synthetic_receipt(o or occ(),s or src(),receipt_id="ind-r",
        issued_at_epoch=kw.get("issued",NOW-10),expires_at_epoch=kw.get("expires",NOW+10))

def test_h01_lawful_noncurrent_synthetic_control_still_passes():
    o=occ(); s=src(); r=issue(o,s)
    m.validate_receipt(r,o,s,expected_occurrence_id="occ-1",now_epoch=NOW)

def test_h02_boolean_timestamp_encoding_is_malformed_and_must_fail_closed():
    with pytest.raises(m.IndependenceProofError):
        m.issue_noncurrent_synthetic_receipt(occ(),src(),receipt_id="ind-r",issued_at_epoch=True,expires_at_epoch=2)

@pytest.mark.parametrize("bad", [1.5,"2","",None])
def test_h03_other_noninteger_issue_timestamps_fail(bad):
    with pytest.raises(m.IndependenceProofError):
        m.issue_noncurrent_synthetic_receipt(occ(),src(),receipt_id="ind-r",issued_at_epoch=bad,expires_at_epoch=3)

@pytest.mark.parametrize("kind", ["OCCURRENCE_RECEIPT@1.0.0","", "LATEST"])
def test_h04_wrong_independence_receipt_kind_fails(kind):
    o=occ(); s=src(); r=replace(issue(o,s),receipt_kind=kind)
    with pytest.raises(m.IndependenceProofError):
        m.validate_receipt(r,o,s,expected_occurrence_id="occ-1",now_epoch=NOW)

def test_h05_wrong_source_record_kind_fails():
    with pytest.raises(m.IndependenceProofError):
        m.validate_source_record(src(record_kind="OCCURRENCE_RECEIPT@1.0.0"),expected_occurrence_id="occ-1",
                                 expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)

@pytest.mark.parametrize("basis", ["self_certification"," CO_LOCATION ","NARRATIVE-PLAUSIBILITY"])
def test_h06_rejected_basis_renamings_do_not_launder(basis):
    with pytest.raises(m.IndependenceProofError):
        m.validate_source_record(src(basis_codes=(m.POSITIVE_BASIS,basis)),expected_occurrence_id="occ-1",
                                 expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)

def test_h07_occurrence_receipt_digest_reuse_fails_even_with_positive_basis():
    o=occ()
    with pytest.raises(m.IndependenceProofError):
        m.issue_noncurrent_synthetic_receipt(o,src(evidence_digest=o.receipt_digest),receipt_id="ind-r",
                                             issued_at_epoch=1,expires_at_epoch=2)

def test_h08_source_owner_cannot_be_occurrence_authority():
    with pytest.raises(m.IndependenceProofError):
        m.validate_source_record(src(source_owner_authority_id=m.OCCURRENCE_AUTHORITY_ID),
                                 expected_occurrence_id="occ-1",expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)

def test_h09_project_current_fixture_cannot_cross_contract():
    with pytest.raises(m.IndependenceProofError):
        m.validate_source_record(src(fixture_class="PROJECT_CURRENT"),expected_occurrence_id="occ-1",
                                 expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID)

def test_h10_time_tamper_breaks_receipt_integrity():
    o=occ(); s=src(); r=replace(issue(o,s),expires_at_epoch=NOW+999)
    with pytest.raises(m.IndependenceProofError):
        m.validate_receipt(r,o,s,expected_occurrence_id="occ-1",now_epoch=NOW)

def test_h11_review_adds_no_effect_surface():
    assert not (set(dir(m)) & m.FORBIDDEN_EFFECT_SURFACES)
