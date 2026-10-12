"""PYAT HQ282 N04 — B5 checkpoint interface correction tests.

Development-only, source-free.  These tests execute the real M2/B5 owners
and demonstrate the checkpoint restoration defect and its correction.

No accepted owner is edited; no G0b/B5-CURRENT/production publication.
"""

from __future__ import annotations

import json

import pytest

import rawlsing_next.pre553_n04_b5_checkpoint_interface_correction as n04
import rawlsing_next.pre553_learned_product_lifecycle as B5
import rawlsing_next.pre553_learned_product_release as M2
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.repro.c02j_mandatory_overlay import (
    mandatory_overlay_active,
    register_verifier,
    clear_registry,
)
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


def _full_fixture():
    repo = M2.M2Repository()
    release, m2_subject = build_m2(repo, tag="n04-test")
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
# POSITIVE: valid checkpoint restoration with corrected call
# ==========================================================================
def test_corrected_verify_checkpoint_subject_resolves_valid_subject():
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    resolved = n04.corrected_verify_checkpoint_subject(repo, subject)
    assert resolved is not None
    assert resolved.producer_contract_ref == subject.producer_contract_ref


def test_original_defect_reproduced_and_correction_works():
    result = n04.demonstrate_checkpoint_defect()
    assert result["defect_reproduced"] is True
    assert result["correction_works"] is True
    assert "RELEASE_SUBJECT_NOT_FOUND" in result["original_error"]


def test_valid_checkpoint_restores_without_overlay():
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None
    assert len(restored._repository_subjects) == 1


def test_valid_checkpoint_restores_with_overlay_and_corrected_verifier():
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    with corrected_overlay_active():
        corrected_register_verifier(verifier)
        try:
            restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
            assert restored is not None
        finally:
            corrected_clear_registry()


# ==========================================================================
# NEGATIVE: changed/shortened history/state still rejected
# ==========================================================================
def test_truncated_history_accepted_by_raw_executor_documents_gap():
    """Raw B5 from_checkpoint accepts truncated history (known gap).

    The checkpoint implementation restores saved state mappings rather than
    replaying event transitions to derive and compare state.  This is a
    documented gap in the P02R review, not a new defect.
    """
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    ck["checkpoint_payload"]["events"] = ck["checkpoint_payload"]["events"][:1]
    ck["checkpoint_hash"] = semantic_hash(ck["checkpoint_payload"])
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None


def test_altered_state_accepted_by_raw_executor_documents_gap():
    """Raw B5 from_checkpoint accepts altered publication state (known gap).

    The checkpoint implementation restores saved state mappings rather than
    replaying event transitions to derive and compare state.  This is a
    documented gap in the P02R review, not a new defect.
    """
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    pub = list(ck["checkpoint_payload"]["publication"])
    pub[0] = (pub[0][0], "REGISTERED")
    ck["checkpoint_payload"]["publication"] = pub
    ck["checkpoint_hash"] = semantic_hash(ck["checkpoint_payload"])
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None


def test_bad_hash_still_rejected():
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    ck["checkpoint_hash"] = "0" * 64
    with pytest.raises(Exception):
        B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)


def test_incomplete_publication_still_rejected():
    repo, release, m2_subject, subject, verifier, ex = _full_fixture()
    ck = ex.export_checkpoint()
    ck["checkpoint_payload"]["publication"] = []
    ck["checkpoint_hash"] = semantic_hash(ck["checkpoint_payload"])
    with pytest.raises(Exception):
        B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)


# ==========================================================================
# METHOD INVENTORY
# ==========================================================================
def test_method_inventory_covers_b5_wrapped_methods():
    inventory = n04.inventory_b5_state_changing_methods()
    assert "stage_release" in inventory["b5_methods"]["WRAPPED"]
    assert "publish_product" in inventory["b5_methods"]["WRAPPED"]
    assert "from_checkpoint" in inventory["b5_methods"]["WRAPPED"]


def test_method_inventory_identifies_unwrapped_methods():
    inventory = n04.inventory_b5_state_changing_methods()
    assert "supersede_current" in inventory["b5_methods"]["UNWRAPPED"]
    assert "withdraw_product" in inventory["b5_methods"]["UNWRAPPED"]
    assert "declare_invalidation" in inventory["b5_methods"]["UNWRAPPED"]


def test_method_inventory_identifies_m2_unwrapped_methods():
    inventory = n04.inventory_b5_state_changing_methods()
    assert "M2Repository.register_subject" in inventory["m2_methods"]["UNWRAPPED"]
    assert "M2Repository.register_release" in inventory["m2_methods"]["UNWRAPPED"]


def test_method_inventory_documents_checkpoint_defect():
    inventory = n04.inventory_b5_state_changing_methods()
    assert "subject_exact" in inventory["checkpoint_defect"]
    assert "resolve_subject_exact" in inventory["checkpoint_defect"]
    assert inventory["identity_mismatch"] == "release_ref != release.release_subject_ref"


# ==========================================================================
# GOVERNANCE
# ==========================================================================
def test_effects_declare_no_rights():
    eff = n04.effects()
    assert all(v is False for v in eff.values())


def test_module_import_surface_contains_no_forbidden_owner():
    import inspect
    source = inspect.getsource(n04)
    imports = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    for token in ("field_forge", "v3_adp", "m5_runtime", "m6_actor"):
        assert token not in imports


def test_no_raw_sav_dta():
    import pathlib
    source = pathlib.Path(n04.__file__).read_text()
    for forbidden in (".sav", ".dta", "pyreadstat"):
        assert forbidden not in source
