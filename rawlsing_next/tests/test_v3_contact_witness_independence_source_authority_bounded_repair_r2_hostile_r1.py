from dataclasses import replace
import inspect
import pytest

from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r1 as legacy
from rawlsing_next import v3_contact_witness_independence_source_authority_candidate_r2 as m

NOW = 2_000_000_000


class IntSubclass(int):
    pass


def occurrence():
    return m.OccurrenceEnvelope(
        m.FIXTURE_CLASS,
        "hostile-occ-receipt",
        m.OCCURRENCE_AUTHORITY_ID,
        "hostile-occurrence",
        m.OCCURRENCE_SCOPE,
        "a" * 64,
    )


def source(*, bases=(m.POSITIVE_BASIS,), evidence_digest="b" * 64):
    return m.IndependenceSourceRecord(
        m.FIXTURE_CLASS,
        "DISTINCT_SOURCE_OWNER_WITNESS_RECORD@1.0.0",
        "hostile-source-record",
        m.AUTHORITY_REF,
        "hostile-occurrence",
        m.INDEPENDENCE_SCOPE,
        tuple(bases),
        evidence_digest,
    )


def good_receipt():
    return m.issue_noncurrent_synthetic_receipt(
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=NOW - 10,
        expires_at_epoch=NOW + 10,
    )


def reject(fn, *args, **kwargs):
    with pytest.raises(m.IndependenceProofError):
        fn(*args, **kwargs)


@pytest.mark.parametrize("bad", [True, False])
def test_h01_r1_boolean_issued_at_blocker_is_closed_in_r2(bad):
    reject(
        m.issue_noncurrent_synthetic_receipt,
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=bad,
        expires_at_epoch=2,
    )


@pytest.mark.parametrize("bad", [True, False])
def test_h02_boolean_expiry_fails_closed(bad):
    reject(
        m.issue_noncurrent_synthetic_receipt,
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=1,
        expires_at_epoch=bad,
    )


@pytest.mark.parametrize("bad", [True, False])
def test_h03_boolean_now_fails_closed(bad):
    r = good_receipt()
    reject(
        m.validate_receipt,
        r,
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=bad,
    )


@pytest.mark.parametrize("field", ["issued_at_epoch", "expires_at_epoch"])
def test_h04_digest_consistent_boolean_receipt_timestamp_still_fails(field):
    r = good_receipt()
    mutated = replace(r, **{field: True})
    mutated = replace(mutated, receipt_digest=m.receipt_digest(mutated))
    reject(
        m.validate_receipt,
        mutated,
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=NOW,
    )


@pytest.mark.parametrize("field", ["issued_at_epoch", "expires_at_epoch"])
def test_h05_int_subclass_receipt_timestamp_fails_validation(field):
    r = good_receipt()
    mutated = replace(r, **{field: IntSubclass(getattr(r, field))})
    mutated = replace(mutated, receipt_digest=m.receipt_digest(mutated))
    reject(
        m.validate_receipt,
        mutated,
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=NOW,
    )


@pytest.mark.parametrize(
    "issued,expires",
    [(IntSubclass(1), 2), (1, IntSubclass(2))],
)
def test_h06_int_subclass_issuance_inputs_fail(issued, expires):
    reject(
        m.issue_noncurrent_synthetic_receipt,
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=issued,
        expires_at_epoch=expires,
    )


def test_h07_int_subclass_now_fails_validation():
    reject(
        m.validate_receipt,
        good_receipt(),
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=IntSubclass(NOW),
    )


@pytest.mark.parametrize("bad", [1.0, "1", None])
def test_h08_non_integral_issued_at_fails_closed(bad):
    reject(
        m.issue_noncurrent_synthetic_receipt,
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=bad,
        expires_at_epoch=2,
    )


@pytest.mark.parametrize("bad", [2.0, "2", None])
def test_h09_non_integral_expiry_fails_closed(bad):
    reject(
        m.issue_noncurrent_synthetic_receipt,
        occurrence(),
        source(),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=1,
        expires_at_epoch=bad,
    )


@pytest.mark.parametrize("bad", [NOW + 0.5, str(NOW), None])
def test_h10_non_integral_now_fails_closed(bad):
    reject(
        m.validate_receipt,
        good_receipt(),
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=bad,
    )


def test_h11_legacy_r1_boolean_receipt_cannot_be_laundered_through_r2_validation():
    r = legacy.issue_noncurrent_synthetic_receipt(
        occurrence(),
        source(),
        receipt_id="legacy-malformed",
        issued_at_epoch=True,
        expires_at_epoch=2,
    )
    assert r.issued_at_epoch is True
    reject(
        m.validate_receipt,
        r,
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=1,
    )


def test_h12_exact_builtin_integer_positive_fixture_passes():
    r = good_receipt()
    m.validate_receipt(
        r,
        occurrence(),
        source(),
        expected_occurrence_id="hostile-occurrence",
        now_epoch=NOW,
    )


def test_h13_r2_preserves_authority_and_scope_contract():
    assert m.AUTHORITY_REF == legacy.AUTHORITY_REF
    assert m.RECEIPT_KIND == legacy.RECEIPT_KIND
    assert m.OCCURRENCE_AUTHORITY_ID == legacy.OCCURRENCE_AUTHORITY_ID
    assert m.OCCURRENCE_SCOPE == legacy.OCCURRENCE_SCOPE
    assert m.INDEPENDENCE_SCOPE == legacy.INDEPENDENCE_SCOPE
    assert m.FIXTURE_CLASS == legacy.FIXTURE_CLASS == "NONCURRENT_SYNTHETIC"
    assert m.REJECTED_BASES == legacy.REJECTED_BASES


def test_h14_occurrence_and_independence_authorities_remain_distinct():
    assert m.AUTHORITY_REF != m.OCCURRENCE_AUTHORITY_ID


@pytest.mark.parametrize("basis", sorted(m.REJECTED_BASES))
def test_h15_every_mandatory_rejection_basis_remains_rejected(basis):
    reject(
        m.validate_source_record,
        source(bases=(basis,)),
        expected_occurrence_id="hostile-occurrence",
        expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID,
    )


def test_h16_positive_plus_rejected_basis_cannot_be_laundered():
    reject(
        m.validate_source_record,
        source(bases=(m.POSITIVE_BASIS, "NARRATIVE_PLAUSIBILITY")),
        expected_occurrence_id="hostile-occurrence",
        expected_occurrence_authority_id=m.OCCURRENCE_AUTHORITY_ID,
    )


def test_h17_occurrence_receipt_reuse_remains_forbidden():
    o = occurrence()
    reject(
        m.issue_noncurrent_synthetic_receipt,
        o,
        source(),
        receipt_id=o.receipt_id,
        issued_at_epoch=1,
        expires_at_epoch=2,
    )


def test_h18_occurrence_digest_reuse_remains_forbidden():
    o = occurrence()
    reject(
        m.issue_noncurrent_synthetic_receipt,
        o,
        source(evidence_digest=o.receipt_digest),
        receipt_id="hostile-independence-receipt",
        issued_at_epoch=1,
        expires_at_epoch=2,
    )


def test_h19_no_forbidden_effect_surface_was_added():
    assert not (set(dir(m)) & m.FORBIDDEN_EFFECT_SURFACES)


def test_h20_repair_surface_is_exact_integer_guard_only():
    src = inspect.getsource(m)
    assert "type(value) is not int" in src
    assert "isinstance(value, int)" not in src
    for forbidden in (
        "admit_occurrence",
        "create_occurrence",
        "activate_actor",
        "issue_positive_applicability",
        "issue_causal_use_permission",
        "create_encounter",
        "realize_oee",
        "install_project_current_independence",
        "execute_obl055",
        "install_obl056_current_positive",
    ):
        assert forbidden not in set(dir(m))
