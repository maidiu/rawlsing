"""Focused checks for the q101 code-99 response-state correction."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
A = json.loads((R / "01_CORRECTION_RECEIPT.json").read_text())
O = json.loads((R / "02_Q101_CODE99_OVERLAY.json").read_text())


def test_01_old_failure_and_corrected_aggregate():
    old = A["old_classification"]
    new = A["corrected_tally"]
    assert old["code_99_state"] == "SUBSTANTIVE_RESPONSE"
    assert old["valid_answer"] == 7162
    assert old["explicit_nonresponse"] == 171
    assert old["misclassified_count"] == 33
    assert new["valid_answer"] == 7129
    assert new["explicit_nonresponse"] == 204
    assert new["dk"] == 171
    assert new["refusal"] == 33
    assert new["missing_or_unobserved"] == 4
    assert new["observed_response"] == 7333
    assert new["source_record_denominator"] == 7337
    assert new["identity"]["valid_plus_explicit_plus_missing"] == 7337
    assert new["identity"]["equals_source_record_denominator"] is True
    assert A["delta"] == {
        "valid_answer": -33,
        "explicit_nonresponse": 33,
        "missing_or_unobserved": 0,
    }


def test_02_isolated_overlay_changes_only_q101_code99():
    assert O["question_id"] == "q101"
    assert O["native_value"] == 99.0
    assert O["from_response_state"] == "SUBSTANTIVE_RESPONSE"
    assert O["to_response_state"] == "REFUSAL"
    assert O["from_canonical_value"] == "99"
    assert O["to_canonical_value"] is None
    assert O["only_change"] == "q101 response value 99 state/canonical classification"
    assert O["production_config_adopted"] is False
    assert A["overlay_validation"]["schema_valid"] is True
    assert A["overlay_validation"]["only_q101_code99_changed"] is True
    assert A["overlay_validation"]["questions"] == 178
    assert A["overlay_validation"]["response_slots"] == 178


def test_03_same_defect_checked_over_all_selected_metadata_without_extra_change():
    s = A["same_mapping_defect_in_selected_metadata"]
    assert s["selected_fields"] == 42
    assert s["fields_mapped_code99_to_substantive"] == 42
    assert s["correction_applied"] == ["q101"]
    assert s["remaining_uncorrected"] == 41
    assert s["other_fields_changed"] is False
    assert s["question_ids"][0] == "q101"
    assert len(s["question_ids"]) == 42


def test_04_routing_remains_unknown_and_historical_supersession_is_q101_only():
    r = A["routing"]
    assert r["state"] == "ROUTING_UNKNOWN"
    assert r["selected_routing_unknown"] == 42
    assert r["selected_risk_set_unresolved"] == 42
    assert r["accepted_routing_binding"] is False
    assert r["eligibility_denominator_binding"] is False
    assert r["affirmative_evidence"] is False
    h = A["historical_supersession"]
    assert h["superseded_at"] == ["q101"]
    assert h["old_q101"] == {
        "valid_answer": 7162,
        "explicit_nonresponse": 171,
        "missing_or_unobserved": 4,
    }
    assert h["corrected_q101"] == {
        "valid_answer": 7129,
        "explicit_nonresponse": 204,
        "missing_or_unobserved": 4,
    }


def test_05_authority_and_redaction_boundaries():
    c = A["classification_owner"]
    assert c["dedicated_state_classifier_present_in_current_owners"] is False
    assert c["no_new_policy"] is True
    assert c["fields_used"] == [
        "option_group", "is_substantive", "is_refusal", "is_missing", "response_kind",
    ]
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "value_label" not in text
    for key in (
        "original_source_read", "respondent_rows_read", "original_workload_issued",
        "production_config_adopted", "policy_fabricated",
        "routing_inferred_from_counts", "merge", "ci",
    ):
        assert A["limits"][key] is False
