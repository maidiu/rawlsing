"""OC4 additional source-free API repair checks. No external issuance or crypto trust."""
from dataclasses import replace
import copy
import pytest
from custody_protocol import (
    EscrowState, Role, MockSigner, CustodyCapsule, SignatureError,
    EditAfterFreezeError, BlindIDPairingError, LeakageError,
    capsule_envelope_commitment, require_second_signature,
    verify_blind_pairing, assert_no_leakage, detect_leakage,
)
from dummy_corpus import build_capsule, build_dummy_corpus, build_model_visible_packet, build_coder_input


def cap():
    return build_capsule("SOURCEFREE_TEST_ONLY", "oc4-frame", build_dummy_corpus())


def bound(c, ctx="ctx", nonce="n"):
    a=MockSigner("custodian-alice", Role.CUSTODIAN).sign(c.content_digest,ctx,nonce,capsule=c)
    b=MockSigner("adjudicator-bob", Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,ctx,nonce,capsule=c)
    return a,b


def test_bounded_full_capsule_pair_positive():
    c=cap();a,b=bound(c)
    assert require_second_signature(c,a,b,c.content_digest,"ctx","n")
    assert MockSigner.verify(a,c.content_digest,"ctx","n")


@pytest.mark.parametrize("field,value", [
    ("capsule_id", "other-id"), ("purpose", "PROSPECTIVE_DESIGN_REVIEW"),
    ("lawful_set_digest", "other-law"), ("freeze_timestamp", 42.),
    ("version", 2), ("content_digest", "other-content"),
    ("schema_version", "NEW"), ("scenario_frame", "other-frame"),
    ("family_graph_digest", "different-family"),
    ("public_projection_digest", "changed-visible"),
    ("hidden_projection_digest", "changed-hidden"),
    ("contribution_digest", "changed-contrib"),
    ("coder_rubric_digest", "changed-rubric"),
    ("split_assignment_digest", "changed-split"),
    ("generation_history_digest", "changed-history"),
    ("rejected_alternatives_digest", "changed-rejected"),
])
def test_original_full_capsule_signatures_reject_field_replay(field,value):
    c=cap();a,b=bound(c)
    altered=replace(c,**{field:value})
    assert capsule_envelope_commitment(c)!=capsule_envelope_commitment(altered)
    with pytest.raises(SignatureError):
        require_second_signature(altered,a,b,c.content_digest,"ctx","n")


def test_raw_content_signature_cannot_claim_envelope():
    c=cap()
    a=MockSigner("custodian-alice",Role.CUSTODIAN).sign(c.content_digest,"ctx","n")
    b=MockSigner("adjudicator-bob",Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","n")
    assert MockSigner.verify(a,c.content_digest,"ctx","n")
    with pytest.raises(SignatureError):
        require_second_signature(c,a,b,c.content_digest,"ctx","n")


def test_wrong_full_capsule_signer_nonce_rejected():
    c=cap();a,b=bound(c)
    with pytest.raises(SignatureError):
        require_second_signature(c,a,b,c.content_digest,"ctx","evil")


def test_materialized_unblind_changes_invisible_before_patch_now_refused():
    e,c=EscrowState(),cap();e.commit(c);e.unblind(c.capsule_id,"runner1");e.release(c.capsule_id)
    assert e.verify_ledger_integrity()
    for key,value in [("capsule_id","forged"),("unblinded_at",-999), ("holder","intruder")]:
        clone=copy.deepcopy(e);clone.unblinded[c.capsule_id][key]=value
        assert not clone.verify_ledger_integrity()


def test_unblind_return_alias_does_not_change_retained_integrity():
    e,c=EscrowState(),cap();e.commit(c)
    receipt=e.unblind(c.capsule_id,"runner1");receipt["unblinded_at"]=-1
    assert e.verify_ledger_integrity()


@pytest.mark.parametrize("nonce", ["", " ", "\t\n"])
def test_no_blank_or_whitespace_nonce(nonce):
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing([{"public_nonce":nonce,"arm":a} for a in "ABC"])


@pytest.mark.parametrize("arm", [[],{},42,None])
def test_invalid_arm_typed_exception(arm):
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing([{"public_nonce":"n","arm":arm},{"public_nonce":"n","arm":"B"},{"public_nonce":"n","arm":"C"}])


@pytest.mark.parametrize("packet", [
    {"menu":[1,2],"request_id":"r"},
    {"menu":[],"request_id":"r"},
    {"menu":["A",None],"request_id":"r"},
    {"public_projection":{"context":["a"]}},
    {"public_projection":{"context":1}},
    {"note":"The answ\u034fer_key is A"},
    {"note":"The answe\u0301r_key is A"},
])
def test_malformed_or_unicode_leaking_visible_projection_refused(packet):
    with pytest.raises(LeakageError):
        assert_no_leakage(packet)


def test_valid_generated_visible_and_coder_packets_stay_safe():
    for case in build_dummy_corpus():
        assert_no_leakage(build_model_visible_packet(case))
        assert_no_leakage(build_coder_input(case,"OPTION_A"))
    assert detect_leakage({"note":"charming"})==[]
