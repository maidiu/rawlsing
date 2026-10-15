"""OC2 executable test-only regressions against real custody API; no test-side forged exceptions."""
from dataclasses import replace
import pytest
from custody_protocol import (
    EscrowState, Role, MockSigner, require_second_signature,
    RevocationError, PurposeViolationError, IdentityMismatchError,
    SignatureError, LedgerRollbackError, EditAfterFreezeError,
    BlindIDPairingError, LeakageError, verify_blind_pairing,
    assert_no_leakage, detect_leakage,
)
from dummy_corpus import build_capsule, build_dummy_corpus, build_model_visible_packet


def capsule():
    return build_capsule("SOURCEFREE_TEST_ONLY", "oc2", build_dummy_corpus())


def test_inactive_revoked_capsule_refused_at_commit():
    with pytest.raises(RevocationError):
        EscrowState().commit(replace(capsule(), revoked=True))


def test_inactive_expired_capsule_refused_at_commit():
    with pytest.raises(RevocationError):
        EscrowState().commit(replace(capsule(), expired=True))


def test_unauthorized_purpose_refused_at_commit():
    with pytest.raises(PurposeViolationError):
        EscrowState().commit(replace(capsule(), purpose="LIVE_MODEL_REQUEST"))


def test_unissued_holder_rejected_via_actual_unblind():
    e, c = EscrowState(), capsule()
    e.commit(c)
    with pytest.raises(IdentityMismatchError):
        e.unblind(c.capsule_id, "stranger")


def test_explicit_mock_holder_grant_and_revocation_at_release():
    e, c = EscrowState(), capsule()
    e.commit(c)
    e.authorize_holder("mock-custodian", Role.CUSTODIAN)
    e.unblind(c.capsule_id, "mock-custodian")
    e.holder_roles.pop("mock-custodian")
    with pytest.raises(RevocationError):
        e.release(c.capsule_id)


def test_signature_binds_content_and_rejects_alien_capsule():
    c = capsule()
    a = MockSigner("custodian-alice", Role.CUSTODIAN).sign(c.content_digest,"ctx","nonce")
    b = MockSigner("adjudicator-bob", Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","nonce")
    assert require_second_signature(c,a,b,c.content_digest,"ctx","nonce")
    with pytest.raises(SignatureError):
        require_second_signature(replace(c, content_digest="alien"),a,b,c.content_digest,"ctx","nonce")


def test_mock_signature_no_capsule_refused():
    c = capsule()
    a = MockSigner("custodian-alice", Role.CUSTODIAN).sign(c.content_digest,"ctx","nonce")
    b = MockSigner("adjudicator-bob", Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","nonce")
    with pytest.raises(SignatureError):
        require_second_signature(None,a,b,c.content_digest,"ctx","nonce")


def test_public_credential_not_a_role_assignment():
    c = capsule()
    a = MockSigner("unassigned-person", Role.CUSTODIAN).sign(c.content_digest,"ctx","nonce")
    b = MockSigner("adjudicator-bob", Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","nonce")
    with pytest.raises(SignatureError):
        require_second_signature(c,a,b,c.content_digest,"ctx","nonce")


def _three():
    e, c = EscrowState(), capsule()
    e.commit(c); e.unblind(c.capsule_id,"runner1"); e.release(c.capsule_id)
    return e,c


def test_no_rollback_even_with_valid_seq():
    e,c = _three()
    with pytest.raises(LedgerRollbackError):
        e.rollback_ledger(1)
    assert e.verify_ledger_integrity()


def test_ledger_op_tamper_visible():
    e,c = _three()
    e.ledger[1]["op"]="RELEASE"
    assert not e.verify_ledger_integrity()


def test_ledger_state_divergence_visible():
    e,c = _three()
    e.released.clear()
    assert not e.verify_ledger_integrity()


def test_committed_capsule_replaced_detection():
    e,c = EscrowState(),capsule()
    e.commit(c)
    e.committed[c.capsule_id]=replace(c,content_digest="forged")
    assert not e.verify_ledger_integrity()
    with pytest.raises(EditAfterFreezeError):
        e.unblind(c.capsule_id,"runner1")


def test_exposure_uncommitted_is_refused():
    with pytest.raises(IdentityMismatchError):
        EscrowState().record_exposure("ghost","recipient","development")


def test_exact_abc_and_duplicate_refusal():
    good=[{"public_nonce":"trial1","arm":a} for a in "ABC"]
    assert verify_blind_pairing(good)
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(good+[dict(good[0])])


def test_join_mismatch_refusal():
    t=[{"public_nonce":"trial1","arm":a,"case_id":f"case-{i}"} for i,a in enumerate("ABC")]
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(t)


def test_encoded_hidden_origin_refused():
    with pytest.raises(LeakageError):
        assert_no_leakage({"hidden\u200b_origin":"synthetic"})


def test_nested_unknown_packet_field_refused():
    with pytest.raises(LeakageError):
        assert_no_leakage({"public_projection":{"context":"synthetic","solution":{"truth":"A"}}})


def test_benign_substring_not_false_positive():
    packet={"note":"charming"}
    assert detect_leakage(packet)==[]


def test_generator_public_packets_remain_safe():
    for c in build_dummy_corpus():
        assert_no_leakage(build_model_visible_packet(c))
