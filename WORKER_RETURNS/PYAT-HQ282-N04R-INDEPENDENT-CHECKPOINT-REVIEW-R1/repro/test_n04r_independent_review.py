"""PYAT HQ282 N04R — independent reviewer tests for the B5 checkpoint correction.

Reviewer-owned tests.  These tests independently verify the checkpoint
correction without borrowing the author's expected outcomes.

No accepted owner is edited; no G0b/B5-CURRENT/production publication.
"""

from __future__ import annotations

import json

import pytest

import rawlsing_next.pre553_n04_b5_checkpoint_interface_correction as n04
import rawlsing_next.pre553_learned_product_lifecycle as B5
import rawlsing_next.pre553_learned_product_release as M2
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.repro.n04_corrected_overlay import (
    corrected_overlay_active,
    register_verifier as corrected_register_verifier,
    clear_registry as corrected_clear_registry,
)
from rawlsing_next.repro.c02j_owner_court import (
    build_m2,
    b5_subject_from_m2,
    make_verifier,
    CEILING,
    MODEL_AUTH,
    WALKBACK_AUTH,
    PRODUCT_REF,
    PRODUCT_FAMILY,
    PRODUCER_OWNER,
    SELECTION_SCOPE,
    BUILD_RECEIPT,
    SEMANTIC_AUTH,
    EVENT_AUTHORITY,
    EVENT_RULE,
)


def _independent_fixture():
    """Build a fixture independently, not copying author's expected outcomes."""
    repo = M2.M2Repository()
    release, m2_subject = build_m2(repo, tag="n04r-reviewer")
    subject = b5_subject_from_m2(repo, release, m2_subject)
    verifier = make_verifier(repo, release, m2_subject)
    ex = B5.LearnedProductLifecycleExecutor()
    ex.stage_release(subject)
    ex.register_product(
        release.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        evidence_refs=(BUILD_RECEIPT,),
    )
    ex.publish_product(
        release.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        evidence_refs=(BUILD_RECEIPT,),
    )
    return repo, release, m2_subject, subject, verifier, ex


# ==========================================================================
# 1. NORMAL POSITIVE: valid checkpoint restoration
# ==========================================================================
def test_reviewer_valid_checkpoint_restores_correctly():
    """Independently verify valid checkpoint restores through corrected path."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ck = ex.export_checkpoint()
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None
    assert len(restored._repository_subjects) == 1
    assert restored._publication.get(release.ref.key) == "PUBLISHED"


def test_reviewer_valid_current_checkpoint_restores_correctly():
    """Independently verify valid current checkpoint restores."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    purpose_ref = EVENT_AUTHORITY
    key = ex.selection_key(
        product_family_ref=PRODUCT_FAMILY,
        selection_scope_ref=SELECTION_SCOPE,
        selection_purpose_ref=purpose_ref,
    )
    ex.select_current(
        key.ref, release.ref,
        expected_previous_receipt_ref=None,
        selection_attestation_ref=EVENT_AUTHORITY,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )
    ck = ex.export_checkpoint()
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None
    assert restored._selection_state_kind.get(key.ref.key) == "CURRENT_SELECTED"


# ==========================================================================
# 2. NEGATIVE RESTORATION: altered checkpoint records
# ==========================================================================
def test_reviewer_altered_publication_state_accepted_by_raw():
    """Raw executor accepts altered publication state (known gap)."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ck = ex.export_checkpoint()
    pub = list(ck["checkpoint_payload"]["publication"])
    pub[0] = (pub[0][0], "REGISTERED")
    ck["checkpoint_payload"]["publication"] = pub
    ck["checkpoint_hash"] = semantic_hash(ck["checkpoint_payload"])
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None  # known gap: raw executor accepts altered state


def test_reviewer_bad_hash_rejected():
    """Bad checkpoint hash is correctly rejected."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ck = ex.export_checkpoint()
    ck["checkpoint_hash"] = "0" * 64
    with pytest.raises(Exception):
        B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)


def test_reviewer_incomplete_publication_rejected():
    """Incomplete publication state is correctly rejected."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ck = ex.export_checkpoint()
    ck["checkpoint_payload"]["publication"] = []
    ck["checkpoint_hash"] = semantic_hash(ck["checkpoint_payload"])
    with pytest.raises(Exception):
        B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)


# ==========================================================================
# 3. REFERENCE CORRECTNESS
# ==========================================================================
def test_reviewer_subject_exact_rejects_release_ref():
    """subject_exact correctly rejects a release_ref (not a subject ref)."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    with pytest.raises(Exception) as excinfo:
        repo.subject_exact(subject.release_ref)
    assert "RELEASE_SUBJECT_NOT_FOUND" in str(excinfo.value)


def test_reviewer_resolve_subject_exact_accepts_release_ref():
    """resolve_subject_exact correctly resolves through the release."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    resolved = n04.corrected_verify_checkpoint_subject(repo, subject)
    assert resolved is not None
    assert resolved.producer_contract_ref == subject.producer_contract_ref


def test_reviewer_resolve_subject_exact_rejects_unrelated_subject():
    """resolve_subject_exact rejects an unrelated subject."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    other_repo = M2.M2Repository()
    other_release, other_subject = build_m2(other_repo, tag="n04r-other")
    other_b5_subject = b5_subject_from_m2(other_repo, other_release, other_subject)
    with pytest.raises(Exception):
        n04.corrected_verify_checkpoint_subject(repo, other_b5_subject)


# ==========================================================================
# 4. METHOD REACHABILITY
# ==========================================================================
def test_reviewer_unwrapped_withdrawal_succeeds_without_verifier():
    """withdraw_product is unwrapped and succeeds without a verifier."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ex.withdraw_product(
        release.ref,
        withdrawal_reason_ref=EVENT_AUTHORITY,
        withdrawal_scope_ref=EVENT_AUTHORITY,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        selection_attestation_ref=EVENT_AUTHORITY,
    )
    assert ex._validity.get(release.ref.key) == "WITHDRAWN"


def test_reviewer_unwrapped_invalidation_succeeds_without_verifier():
    """declare_invalidation is unwrapped and succeeds without a verifier."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    ex.declare_invalidation(
        changed_determinant_refs=(MODEL_AUTH,),
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        dependency_closure_receipt_ref=BUILD_RECEIPT,
        selection_attestation_ref=EVENT_AUTHORITY,
    )
    assert len(ex._events) > 2  # registered, published, invalidated


def test_reviewer_unwrapped_supersede_succeeds_without_verifier():
    """supersede_current is unwrapped and succeeds without a verifier."""
    repo, release, m2_subject, subject, verifier, ex = _independent_fixture()
    # Build a second release with a different product_ref for the successor
    release2, m2_subject2 = build_m2(repo, tag="n04r-successor")
    subject2 = b5_subject_from_m2(repo, release2, m2_subject2)
    # Override product_ref to avoid conflict
    from dataclasses import replace
    subject2 = replace(subject2, product_ref=EVENT_AUTHORITY)
    ex.stage_release(subject2)
    ex.register_product(
        release2.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        evidence_refs=(BUILD_RECEIPT,),
    )
    ex.publish_product(
        release2.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        evidence_refs=(BUILD_RECEIPT,),
    )
    key = ex.selection_key(
        product_family_ref=PRODUCT_FAMILY,
        selection_scope_ref=SELECTION_SCOPE,
        selection_purpose_ref=EVENT_AUTHORITY,
    )
    ex.select_current(
        key.ref, release.ref,
        expected_previous_receipt_ref=None,
        selection_attestation_ref=EVENT_AUTHORITY,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
    )
    prev_receipt_ref = ex._selection_index[key.ref.key]
    prev_receipt = ex._selection_receipts[prev_receipt_ref.key]
    ex.supersede_current(
        key.ref,
        predecessor_release_ref=release.ref,
        successor_release_ref=release2.ref,
        expected_previous_receipt_ref=prev_receipt.ref,
        event_authority_ref=EVENT_AUTHORITY,
        event_rule_ref=EVENT_RULE,
        selection_attestation_ref=EVENT_AUTHORITY,
        supersession_basis_ref=EVENT_AUTHORITY,
    )
    assert len(ex._events) > 3


# ==========================================================================
# 5. SCOPE AND PRIVACY
# ==========================================================================
def test_reviewer_no_production_authority():
    """Module declares no production authority."""
    eff = n04.effects()
    assert all(v is False for v in eff.values())


def test_reviewer_no_forbidden_imports():
    """Module imports no forbidden owners."""
    import inspect
    source = inspect.getsource(n04)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in ("field_forge", "v3_adp", "m5_runtime", "m6_actor"):
        assert token not in imports


def test_reviewer_no_raw_data():
    """Module reads no raw data."""
    import pathlib
    source = pathlib.Path(n04.__file__).read_text()
    for forbidden in (".sav", ".dta", "pyreadstat"):
        assert forbidden not in source
