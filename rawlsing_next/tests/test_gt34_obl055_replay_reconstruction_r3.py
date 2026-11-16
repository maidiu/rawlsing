from __future__ import annotations

from dataclasses import asdict
import json

import pytest

import rawlsing_next.gt34_adp010_input_authority_acceptance as acceptance
import rawlsing_next.v3_adp010_oee_executor_obl055_replay_canonical as oee
import rawlsing_next.tests.test_gt34_obl055_replay_reconstruction_r2 as r2_court


@pytest.fixture(autouse=True)
def _run_exact_r2_attack_surface_against_r3(monkeypatch):
    monkeypatch.setattr(r2_court, "oee", oee)


def test_r3_00_exact_wire_normalization_repairs_only_tuple_list_roundtrip():
    receipt = oee.synthetic_acceptance_receipts()[acceptance.CAUSAL_USE_PERMISSION]
    wire = json.loads(oee.r2._canonical(asdict(receipt)))
    assert oee._receipt_wire_equal(wire, receipt)

    mutated = dict(wire)
    mutated["role"] = acceptance.POSITIVE_APPLICABILITY
    assert not oee._receipt_wire_equal(mutated, receipt)

    augmented = dict(wire)
    augmented["caller_added_semantics"] = True
    assert not oee._receipt_wire_equal(augmented, receipt)


def test_r3_01_successor_provenance_is_additive_and_zero_positive():
    *_, av = r2_court.available()
    assert oee.R2_SUCCESSOR_REF in av.record.provenance_refs
    assert oee.R3_SUCCESSOR_REF in av.record.provenance_refs
    assert acceptance.candidate_registry_artifact()["current_positive_entries"] == []
    assert acceptance.candidate_registry_artifact()["positive_fallback"] is False


# Re-run the exact R2/H1 replay-reconstruction defect suite against the R3
# successor.  Function objects retain the R2 court's helper globals, while the
# autouse fixture redirects only its executor-under-test to R3.
test_r3_02_mechanical_chain_reconstructs_all_source_objects = r2_court.test_r2_01_mechanical_chain_reconstructs_all_source_objects
test_r3_03_h1_causal_semantic_ref_swap_is_closed = r2_court.test_r2_02_h1_causal_semantic_ref_swap_is_closed
test_r3_04_h1_causal_auth_ref_swap_is_closed = r2_court.test_r2_03_h1_causal_auth_ref_swap_is_closed
test_r3_05_h1_subject_auth_ref_swap_is_closed = r2_court.test_r2_04_h1_subject_auth_ref_swap_is_closed
test_r3_06_h1_phase_pointer_swaps_are_closed = r2_court.test_r2_05_h1_phase_pointer_swaps_are_closed
test_r3_07_h1_app_auth_ref_swap_is_closed = r2_court.test_r2_06_h1_app_auth_ref_swap_is_closed
test_r3_08_h1_contact_pointer_swaps_are_closed = r2_court.test_r2_07_h1_contact_pointer_swaps_are_closed
test_r3_09_source_bundle_itself_cannot_be_relabelled_and_readdressed = r2_court.test_r2_08_source_bundle_itself_cannot_be_relabelled_and_readdressed
test_r3_10_zero_positive_and_no_semantic_authority_widening = r2_court.test_r2_09_zero_positive_and_no_semantic_authority_widening
