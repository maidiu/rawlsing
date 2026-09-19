from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

from rawlsing_next.sdtf_r4_generic_batch_adapter import (
    ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT,
    ELIGIBLE_FOR_SEPARATE_SELECTION,
    NOT_PROJECTABLE,
    ROW_IDENTITY_CONFLICT,
    SATISFIED_CURRENT,
    adapt_generic_r4_batch,
)


def _artifact_module():
    root = Path(__file__).resolve().parents[2]
    path = root / "WORKER_RETURNS/ASTRA-D10-R1/02_M10_M01_CANDIDATE_ENVELOPE.py"
    spec = importlib.util.spec_from_file_location("astra_d10_r1_m10_m01", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_astra_d10_r1_exact_candidate_envelope_projects_candidate_not_current():
    m = _artifact_module()
    first = adapt_generic_r4_batch(m.BATCH_ENVELOPE)
    second = adapt_generic_r4_batch(m.BATCH_ENVELOPE)

    assert first.batch_ref.as_dict() == m.EXPECTED["batch_ref"]
    assert first.batch_ref == second.batch_ref
    assert first.batch_receipt_ref == second.batch_receipt_ref
    assert first.batch_receipt_ref.as_dict() == m.EXPECTED["batch_receipt_ref"]
    assert len(first.candidate_receipts) == 1

    receipt = first.candidate_receipts[0]
    assert receipt.candidate_row_ref.as_dict() == m.EXPECTED["candidate_row_ref"]
    assert receipt.ref.as_dict() == m.EXPECTED["candidate_receipt_ref"]
    assert receipt.integrity_failures == ()
    assert receipt.blocking_refs == ()
    assert receipt.runtime_projection_state == ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
    assert receipt.runtime_projection_state == m.EXPECTED["runtime_projection_state"]
    assert receipt.current_selection_state == ELIGIBLE_FOR_SEPARATE_SELECTION
    assert receipt.current_selection_state == m.EXPECTED["current_selection_state"]
    assert receipt.runtime_binding_ref is not None
    assert receipt.runtime_binding_ref.as_dict() == m.EXPECTED["runtime_binding_ref"]
    assert len(receipt.determinant_states) == 28
    assert all(state in {SATISFIED_CURRENT, "NOT_APPLICABLE"} for _, state in receipt.determinant_states)
    assert len(receipt.package_states) == 6
    assert all(state == SATISFIED_CURRENT for _, state in receipt.package_states)

    binding = receipt.runtime_binding
    assert binding is not None
    assert binding.rule_currentness.value == "CANDIDATE_NOT_CURRENT"
    assert binding.rule_current_selection_evidence_refs == ()
    assert binding.rule_noncurrent_disposition_refs == ()
    assert binding.value_mode.value == "NONNUMERIC"
    assert binding.calibration_authority.disposition.value == "NOT_APPLICABLE"
    assert binding.measurement_authority.disposition.value == "NOT_APPLICABLE"
    assert binding.estimand_authority.disposition.value == "NOT_APPLICABLE"
    assert binding.identification_authority.disposition.value == "NOT_APPLICABLE"
    assert binding.rule_owner.disposition.value == "BOUND"
    assert binding.causal_use_authority.disposition.value == "BOUND"
    assert [x.value for x in binding.mechanism_classes] == ["P1 MATERIAL_ACCESS_DEPENDENCY"]

    row = m.BATCH_ENVELOPE["candidate_rows"][0]
    assert row["snapshot"]["row_generation"] == 0
    assert row["snapshot"]["predecessor_row_ref"] is None
    cells = row["snapshot"]["requirement_cells"]
    assert cells[23]["state"] == "NOT_APPLICABLE"
    assert cells[23]["na_basis_ref"]["content_hash"] == "0a72c9453ad55f1934f1e9953c3557a56893083ec32efb8e9a7fc03d0bb6244e"
    assert cells[25]["resolved_value"] == "CANDIDATE_NOT_CURRENT"
    assert cells[26]["resolved_value"] == []
    assert cells[27]["resolved_value"] == []

    boundaries = m.artifact()["boundaries"]
    assert boundaries == {
        "numeric_calibration_inferred": False,
        "rule_current_accepted_issued": False,
        "current_actor_or_world_application_fact_created": False,
        "occupant_or_witness_created": False,
        "topology_created": False,
        "v3_person_state_created": False,
        "obl063_used": False,
    }


def test_astra_d10_r1_governed_change_sensitivity_fails_closed():
    m = _artifact_module()
    mutated = copy.deepcopy(m.BATCH_ENVELOPE)
    mutated["candidate_rows"][0]["snapshot"]["requirement_cells"][25]["resolved_value"] = "CURRENT_ACCEPTED"

    result = adapt_generic_r4_batch(mutated)
    receipt = result.candidate_receipts[0]
    assert ROW_IDENTITY_CONFLICT in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None
    assert receipt.runtime_binding_ref is None
