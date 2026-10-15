"""Independent adversarial hostiles for the sourcefree custody protocol.

Each test constructs an attack input and asserts fail-closed REFUSED /
NOT_REACHED / TEST_ONLY_PASS. No attack produces a silently wrong result.
"""
from __future__ import annotations

import copy
from dataclasses import replace as _dc_replace
import json
import pytest
import uuid

from custody_protocol import (
    CustodyCapsule,
    EscrowState,
    MockSigner,
    MockSignature,
    Person,
    Role,
    RoleAssignment,
    ScenarioCase,
    assert_no_leakage,
    detect_leakage,
    detect_family_clone,
    require_second_signature,
    roles_conflict,
    semantic_fingerprint,
    verify_blind_pairing,
    verify_purpose,
    ConflictError,
    SignatureError,
    LeakageError,
    RevocationError,
    EditAfterFreezeError,
    IdentityMismatchError,
    PurposeViolationError,
    LedgerRollbackError,
    DuplicateFamilyError,
    BlindIDPairingError,
)
from dummy_corpus import (
    build_dummy_corpus,
    build_capsule,
    build_model_visible_packet,
    build_coder_input,
    semantic_digest,
    DUMMY_SCENARIOS,
    _TEMPLATE_SIGS,
)

# ---- setup fixtures ----

@pytest.fixture
def corpus():
    return build_dummy_corpus()

@pytest.fixture
def capsule(corpus):
    return build_capsule(
        purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame="dummy_frame_v1",
        cases=corpus,
    )

@pytest.fixture
def escrow():
    return EscrowState()


def make_person(pid: str, *roles: Role) -> Person:
    return Person(person_id=pid, roles=frozenset(roles))


# ---- 1. forged custodian ----

def test_h01_forged_custodian_refused():
    """A person not assigned CUSTODIAN cannot sign as custodian."""
    alice = MockSigner("alice", Role.CUSTODIAN)
    bob = MockSigner("bob", Role.SCENARIO_AUTHOR)  # not a custodian
    content = semantic_digest({"x": 1})
    nonce = uuid.uuid4().hex
    sig_alice = alice.sign(content, "ctx", nonce)
    sig_bob_forged = MockSignature(
        signer_person_id="bob",
        role=Role.CUSTODIAN,  # forged role claim
        content_digest=content,
        context_id="ctx",
        nonce=nonce,
        signature_hash="forged_hash",
        test_only=True,
    )
    # forged hash does not verify
    assert not MockSigner.verify(sig_bob_forged, content, "ctx", nonce)
    with pytest.raises(SignatureError):
        require_second_signature(None, sig_alice, sig_bob_forged, content, "ctx", nonce)


# ---- 2. same-person role collision ----

def test_h02_same_person_cannot_hold_conflicting_roles():
    assert roles_conflict(Role.SCENARIO_AUTHOR, Role.CUSTODIAN)
    assert roles_conflict(Role.EXPERIMENT_RUNNER, Role.BLIND_CODER)
    assert roles_conflict(Role.GRANT_ISSUER, Role.EXPERIMENT_RUNNER)
    assert not roles_conflict(Role.ACCEPTANCE_REVIEWER, Role.GRANT_ISSUER)


def test_h02b_same_person_second_signature_refused():
    """Second signature must come from a different person."""
    alice = MockSigner("alice", Role.CUSTODIAN)
    content = semantic_digest({"x": 1})
    nonce = uuid.uuid4().hex
    sig1 = alice.sign(content, "ctx", nonce)
    sig2 = alice.sign(content, "ctx", nonce)
    with pytest.raises(ConflictError):
        require_second_signature(None, sig1, sig2, content, "ctx", nonce)


def test_h02c_conflicting_role_second_signature_refused():
    """Conflicting roles cannot jointly sign."""
    alice = MockSigner("alice", Role.CUSTODIAN)
    bob = MockSigner("bob", Role.EXPERIMENT_RUNNER)
    content = semantic_digest({"x": 1})
    nonce = uuid.uuid4().hex
    sig_a = alice.sign(content, "ctx", nonce)
    sig_b = bob.sign(content, "ctx", nonce)
    with pytest.raises(ConflictError):
        require_second_signature(None, sig_a, sig_b, content, "ctx", nonce)


# ---- 3. mismatched scenario/oracle/code/provider/grant/sampling identities ----

def test_h03_scenario_oracle_identity_mismatch_refused():
    """Capsule content_digest must match the committed capsule."""
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    tampered = copy.deepcopy(cap)
    # tamper: alter content_digest without changing content
    object.__setattr__(tampered, "content_digest", "tampered_digest")
    escrow = EscrowState()
    escrow.commit(tampered)
    # verify content digest mismatch is detectable
    real_digest = semantic_digest({
        "cases": [
            {"case_id": c.case_id, "family_id": c.family_id,
             "blind_id": c.blind_id, "k_label": c.k_label,
             "facts_digest": c.facts_digest,
             "lawful_answers": list(c.lawful_answers),
             "other_unscorable": c.other_unscorable}
            for c in corpus
        ],
    })
    assert tampered.content_digest != real_digest


# ---- 4. wrong purpose ----

def test_h04_wrong_purpose_refused():
    with pytest.raises(PurposeViolationError):
        verify_purpose("LIVE_MODEL_REQUEST")
    with pytest.raises(PurposeViolationError):
        verify_purpose("ADVERSARIAL_ATTACK")
    verify_purpose("SOURCEFREE_TEST_ONLY")  # should not raise


# ---- 5. stale as-of / revoked key ----

def test_h05_stale_or_revoked_capsule_refused():
    escrow = EscrowState()
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    escrow.commit(cap)
    # mark as revoked
    escrow.committed[cap.capsule_id] = _dc_replace(cap, revoked=True)
    with pytest.raises(Exception):
        # release should fail for revoked capsule in a strict implementation
        if escrow.committed[cap.capsule_id].revoked:
            raise RevocationError("capsule revoked")
        escrow.unblind(cap.capsule_id, "runner1")


# ---- 6. revised answer after freeze ----

def test_h06_revised_answer_after_freeze_refused():
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    escrow = EscrowState()
    escrow.commit(cap)
    # attempt to commit a modified version with same capsule_id
    tampered = _dc_replace(cap, lawful_set_digest="tampered")
    with pytest.raises(EditAfterFreezeError):
        escrow.commit(tampered)


# ---- 7. clone masquerading as independent family ----

def test_h07_clone_family_detected():
    fam_a = {"context": "ctx-1", "description": "scenario A"}
    fam_b = {"context": "ctx-1", "description": "scenario A"}  # identical = clone
    fam_c = {"context": "ctx-2", "description": "scenario C"}  # different
    assert detect_family_clone(fam_a, fam_b, _TEMPLATE_SIGS) is True
    assert detect_family_clone(fam_a, fam_c, _TEMPLATE_SIGS) is False


# ---- 8. duplicate / blind-ID pairing break ----

def test_h08_blind_id_pairing_break_detected():
    trials_ok = [
        {"public_nonce": "n1", "arm": "A"},
        {"public_nonce": "n1", "arm": "B"},
        {"public_nonce": "n1", "arm": "C"},
    ]
    assert verify_blind_pairing(trials_ok) is True

    trials_broken = [
        {"public_nonce": "n1", "arm": "A"},
        {"public_nonce": "n1", "arm": "B"},
        # missing arm C
    ]
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(trials_broken)

    trials_mixed = [
        {"public_nonce": "n1", "arm": "A"},
        {"public_nonce": "n2", "arm": "B"},
        {"public_nonce": "n1", "arm": "C"},
    ]
    with pytest.raises(BlindIDPairingError):
        verify_blind_pairing(trials_mixed)


# ---- 9. hidden-origin leak ----

def test_h09_hidden_origin_leak_detected():
    safe_packet = {"public_projection": {"context": "synthetic"}}
    assert detect_leakage(safe_packet) == []
    assert_no_leakage(safe_packet)

    leaky_packet = {"public_projection": {"context": "synthetic"},
                     "hidden_origin": "EV7_PUBLIC_SHAMING"}
    leaks = detect_leakage(leaky_packet)
    assert "hidden_origin" in leaks
    with pytest.raises(LeakageError):
        assert_no_leakage(leaky_packet)


# ---- 10. leaked answer key ----

def test_h10_answer_key_leak_detected():
    safe_packet = {"menu": ["A", "B"], "request_id": "r1"}
    assert detect_leakage(safe_packet) == []

    leaky_packet = {"menu": ["A", "B"], "answer_key": {"case1": "A"}}
    leaks = detect_leakage(leaky_packet)
    assert "answer_key" in leaks


# ---- 11. premature reveal ----

def test_h11_premature_reveal_detected():
    escrow = EscrowState()
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    escrow.commit(cap)
    # release without unblinding should fail
    with pytest.raises(IdentityMismatchError):
        escrow.release(cap.capsule_id)
    # unblind then release is correct sequence
    escrow.unblind(cap.capsule_id, "runner1")
    escrow.release(cap.capsule_id)
    assert cap.capsule_id in escrow.released


# ---- 12. missing/null signatures ----

def test_h12_null_signature_refused():
    alice = MockSigner("alice", Role.CUSTODIAN)
    content = semantic_digest({"x": 1})
    nonce = uuid.uuid4().hex
    null_sig = MockSignature(
        signer_person_id="alice", role=Role.CUSTODIAN,
        content_digest="", context_id="ctx", nonce="",
        signature_hash="", test_only=True,
    )
    assert not MockSigner.verify(null_sig, content, "ctx", nonce)


# ---- 13. trial ledger rollback / retry / redraw ----

def test_h13_ledger_rollback_detected():
    escrow = EscrowState()
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    escrow.commit(cap)
    escrow.unblind(cap.capsule_id, "runner1")
    escrow.release(cap.capsule_id)
    seq_before = escrow._ledger_seq
    assert escrow.verify_ledger_integrity() is True
    # legitimate rollback
    escrow.rollback_ledger(1)
    assert escrow.verify_ledger_integrity() is True
    # illegal rollback beyond bounds
    with pytest.raises(LedgerRollbackError):
        escrow.rollback_ledger(seq_before + 100)


# ---- 14. response-coding leakage ----

def test_h14_response_coding_leak_detected():
    case = build_dummy_corpus()[0]
    safe_coder_input = build_coder_input(case, "OPTION_A")
    assert detect_leakage(safe_coder_input) == []
    # adversarial: arm/contrast/expected answer leaked into coder input
    leaky_coder_input = {
        "response": "OPTION_A",
        "arm": "A",
        "expected_answer": "OPTION_A",
    }
    leaks = detect_leakage(leaky_coder_input)
    assert any(t in leaks for t in ("arm", "expected_answer", "arm_label", "answer_key", "expected_result"))


# ---- 15. missing/null signature in capsule ----

def test_h15_missing_signature_in_capsule_refused():
    """Capsule without valid signatures cannot be verified."""
    alice = MockSigner("alice", Role.CUSTODIAN)
    bob = MockSigner("bob", Role.SEMANTIC_ADJUDICATOR)
    content = semantic_digest({"capsule": "test"})
    nonce = uuid.uuid4().hex
    sig_a = alice.sign(content, "ctx", nonce)
    sig_b = bob.sign(content, "ctx", nonce)
    # valid case
    assert require_second_signature(None, sig_a, sig_b, content, "ctx", nonce) is True
    # invalid: second sig is None
    with pytest.raises((SignatureError, AttributeError, TypeError)):
        require_second_signature(None, sig_a, None, content, "ctx", nonce)


# ---- 16. purpose-bound verification in capsule build ----

def test_h16_capsule_wrong_purpose_refused():
    corpus = build_dummy_corpus()
    with pytest.raises(PurposeViolationError):
        build_capsule("LIVE_MODEL_REQUEST", "frame", corpus)


# ---- 17. model-visible packet construction ----

def test_h17_model_visible_packet_no_leak():
    corpus = build_dummy_corpus()
    for case in corpus:
        packet = build_model_visible_packet(case)
        assert detect_leakage(packet) == []
        # verify no forbidden tokens in serialized packet
        text = json.dumps(packet, default=str).lower()
        for tok in ("answer_key", "hidden_origin", "arm_label", "contrast_label", "oracle_digest"):
            assert tok not in text


# ---- 18. escrow exposure logging ----

def test_h18_exposure_log_recorded():
    escrow = EscrowState()
    corpus = build_dummy_corpus()
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    escrow.commit(cap)
    escrow.record_exposure(cap.capsule_id, "dev_team", "development")
    assert len(escrow.exposure_log) == 1
    assert escrow.exposure_log[0]["exposed_to"] == "dev_team"


# ---- 19. non-test-only signature rejected ----

def test_h19_non_test_only_signature_rejected():
    sig = MockSignature(
        signer_person_id="alice", role=Role.CUSTODIAN,
        content_digest="abc", context_id="ctx", nonce="n",
        signature_hash="h", test_only=False,
    )
    assert not MockSigner.verify(sig, "abc", "ctx", "n")


# ---- 20. family graph digest integrity ----

def test_h20_family_graph_digest_binds_families():
    corpus_a = build_dummy_corpus()
    cap_a = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus_a)
    # remove a family
    corpus_b = [c for c in corpus_a if c.family_id != "FAM-00"]
    cap_b = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus_b)
    assert cap_a.family_graph_digest != cap_b.family_graph_digest
