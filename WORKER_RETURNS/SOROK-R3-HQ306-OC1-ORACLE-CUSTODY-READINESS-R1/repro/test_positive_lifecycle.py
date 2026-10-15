"""Positive custody lifecycle tests: full role-separated escrow round-trip."""
from __future__ import annotations

import pytest
import uuid

from custody_protocol import (
    CustodyCapsule,
    EscrowState,
    MockSigner,
    Person,
    Role,
    RoleAssignment,
    ScenarioCase,
    assert_no_leakage,
    detect_leakage,
    require_second_signature,
    roles_conflict,
    verify_purpose,
)
from dummy_corpus import (
    build_dummy_corpus,
    build_capsule,
    build_model_visible_packet,
    build_coder_input,
    semantic_digest,
    DUMMY_SCENARIOS,
)


@pytest.fixture
def corpus():
    return build_dummy_corpus()


def test_positive_full_role_separated_lifecycle(corpus):
    """Complete lifecycle: build → commit → sign → unblind → release."""
    # 1. build capsule
    cap = build_capsule("SOURCEFREE_TEST_ONLY", "dummy_frame_v1", corpus)
    assert cap.purpose == "SOURCEFREE_TEST_ONLY"
    assert cap.schema_version == "CUSTODY_CAPSULE@1"

    # 2. commit to escrow
    escrow = EscrowState()
    escrow.commit(cap)
    assert cap.capsule_id in escrow.committed

    # 3. sign with two distinct non-conflicting roles
    alice = MockSigner("alice", Role.CUSTODIAN)
    bob = MockSigner("bob", Role.SEMANTIC_ADJUDICATOR)
    content = semantic_digest({"capsule": cap.capsule_id})
    nonce = uuid.uuid4().hex
    sig_a = alice.sign(content, "ctx", nonce)
    sig_b = bob.sign(content, "ctx", nonce)
    assert require_second_signature(cap, sig_a, sig_b, content, "ctx", nonce) is True

    # 4. unblind and release
    escrow.unblind(cap.capsule_id, "runner1")
    escrow.release(cap.capsule_id)
    assert cap.capsule_id in escrow.released
    assert escrow.verify_ledger_integrity() is True


def test_positive_no_leakage_in_model_packets(corpus):
    for case in corpus:
        packet = build_model_visible_packet(case)
        assert detect_leakage(packet) == []
        assert_no_leakage(packet)


def test_positive_coder_input_no_arm_leak(corpus):
    for case in corpus:
        coder = build_coder_input(case, "OPTION_A")
        assert detect_leakage(coder) == []
        assert "arm" not in coder
        assert "expected_answer" not in coder


def test_positive_role_separation_enforced():
    assert roles_conflict(Role.SCENARIO_AUTHOR, Role.CUSTODIAN)
    assert roles_conflict(Role.EXPERIMENT_RUNNER, Role.BLIND_CODER)
    assert roles_conflict(Role.GRANT_ISSUER, Role.EXPERIMENT_RUNNER)
    # ACCEPTANCE_REVIEWER is independent of GRANT_ISSUER
    assert not roles_conflict(Role.ACCEPTANCE_REVIEWER, Role.GRANT_ISSUER)
    # SEMANTIC_ADJUDICATOR conflicts with SCENARIO_AUTHOR
    assert roles_conflict(Role.SEMANTIC_ADJUDICATOR, Role.SCENARIO_AUTHOR)


def test_positive_lawful_sets_contain_other_unscorable(corpus):
    for case in corpus:
        assert "OTHER_UNSCORABLE" in case.lawful_answers
        assert case.other_unscorable is True


def test_positive_capsule_deterministic_digest(corpus):
    cap1 = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    cap2 = build_capsule("SOURCEFREE_TEST_ONLY", "frame", corpus)
    # same content → same content_digest (capsule_id differs by uuid)
    assert cap1.content_digest == cap2.content_digest
    assert cap1.lawful_set_digest == cap2.lawful_set_digest


def test_positive_verifiable_mock_signature():
    signer = MockSigner("alice", Role.CUSTODIAN)
    content = semantic_digest({"test": 1})
    nonce = uuid.uuid4().hex
    sig = signer.sign(content, "ctx", nonce)
    assert MockSigner.verify(sig, content, "ctx", nonce) is True
    assert sig.test_only is True
    assert sig.verification_root == "TEST_ONLY_EPHEMERAL_ROOT"


def test_positive_purpose_gate():
    verify_purpose("SOURCEFREE_TEST_ONLY")
    verify_purpose("PROSPECTIVE_DESIGN_REVIEW")
    verify_purpose("CUSTODY_READINESS_PROTOCOL")


def test_positive_blind_id_pairing_ok():
    trials = [
        {"public_nonce": "n1", "arm": "A"},
        {"public_nonce": "n1", "arm": "B"},
        {"public_nonce": "n1", "arm": "C"},
        {"public_nonce": "n2", "arm": "A"},
        {"public_nonce": "n2", "arm": "B"},
        {"public_nonce": "n2", "arm": "C"},
    ]
    from custody_protocol import verify_blind_pairing
    assert verify_blind_pairing(trials) is True
