"""SOROK HQ311 OC5 newly authored **candidate** full-module regression tests.
These are NOT reported executed in OC5. Stage exact OC4 blob and OC1 dummy_corpus
as described in 02_REPRODUCE before running. Sourcefree TEST_ONLY.
"""
from dataclasses import replace
import pytest
from custody_protocol import (MockSigner,Role,SignatureError,LeakageError,
    EscrowState,RevocationError,BlindIDPairingError,require_second_signature,
    capsule_envelope_commitment,verify_blind_pairing,assert_no_leakage,detect_leakage)
from dummy_corpus import build_capsule,build_dummy_corpus

def cap():
    return build_capsule("SOURCEFREE_TEST_ONLY","oc5",build_dummy_corpus())
def sigs(c):
    return (MockSigner("custodian-alice",Role.CUSTODIAN).sign(c.content_digest,"ctx","n",capsule=c),
            MockSigner("adjudicator-bob",Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","n",capsule=c))

def test_full_envelope_positive():
    c=cap();a,b=sigs(c)
    assert require_second_signature(c,a,b,c.content_digest,"ctx","n")

@pytest.mark.parametrize("field,value", [
    ("capsule_id","other"),("purpose","PROSPECTIVE_DESIGN_REVIEW"),
    ("lawful_set_digest","other"),("content_digest","other"),
    ("version",2),("schema_version","changed"),
    ("freeze_timestamp",1.0),("coder_rubric_digest","other"),
    ("split_assignment_digest","other"),("hidden_projection_digest","other")])
def test_full_envelope_replay_refused(field,value):
    c=cap();a,b=sigs(c);altered=replace(c,**{field:value})
    assert capsule_envelope_commitment(c)!=capsule_envelope_commitment(altered)
    with pytest.raises(SignatureError):
        require_second_signature(altered,a,b,c.content_digest,"ctx","n")

def test_bare_digest_signatures_refused():
    c=cap()
    a=MockSigner("custodian-alice",Role.CUSTODIAN).sign(c.content_digest,"ctx","n")
    b=MockSigner("adjudicator-bob",Role.SEMANTIC_ADJUDICATOR).sign(c.content_digest,"ctx","n")
    with pytest.raises(SignatureError):
        require_second_signature(c,a,b,c.content_digest,"ctx","n")

@pytest.mark.parametrize("bad",[object(),12,{"signature_hash":"x"}])
def test_malformed_signature_fails_typed(bad):
    c=cap();a,b=sigs(c)
    with pytest.raises(SignatureError):
        require_second_signature(c,bad,b,c.content_digest,"ctx","n")

@pytest.mark.parametrize("packet",[
    {"public_projection":{"context":"safe","ｃontext":"shadow"}},
    {"public_projection":{"context":"safe","con\u034ftext":"shadow"}},
    {"public_projection":{"context":"safe","CONTÉXT":"shadow"}},
    {"note":"charming","n\u034fote":"shadow"}])
def test_duplicate_normalized_keys_refused(packet):
    with pytest.raises(LeakageError): assert_no_leakage(packet)

def test_benign_and_unicode_positive():
    assert detect_leakage({"note":"charming"})==[]
    with pytest.raises(LeakageError):
        assert_no_leakage({"note":"answ\u034fer_key is A"})

def test_escrow_unblind_timestamp_and_holder_integrity():
    from copy import deepcopy
    e=EscrowState();c=cap();e.commit(c);e.unblind(c.capsule_id,"runner1");e.release(c.capsule_id)
    assert e.verify_ledger_integrity()
    for field,value in (("capsule_id","forged"),("holder","forged"),("unblinded_at",-1)):
        v=deepcopy(e);v.unblinded[c.capsule_id][field]=value
        assert not v.verify_ledger_integrity()

def test_escrow_holder_revoked_before_release():
    e=EscrowState();c=cap();e.commit(c)
    e.authorize_holder("third",Role.CUSTODIAN);e.unblind(c.capsule_id,"third")
    del e.holder_roles["third"]
    with pytest.raises(RevocationError): e.release(c.capsule_id)

def test_strict_blind_pairing():
    good=[{"public_nonce":"n","arm":arm,"case_id":"case"} for arm in "ABC"]
    assert verify_blind_pairing(good)
    bad=[dict(t) for t in good];bad[1]["arm"]=[]
    with pytest.raises(BlindIDPairingError): verify_blind_pairing(bad)
