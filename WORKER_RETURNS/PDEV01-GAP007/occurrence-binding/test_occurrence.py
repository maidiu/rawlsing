"""Focused checks for the P1 conditional/joint occurrence-binding attempt."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
A = json.loads((HERE / "01_ACCOUNTING.json").read_text())


def test_01_plan_identity_and_all_conditional_joint_entries_accounted():
    p = A["p1_plan"]
    assert p["plan_ref"] == "e0d4180cbfc43a1ddc5965ff20afb9cb284676c6c4981d9681d3e35121ac59ea"
    assert p["operation_count"] == 840
    assert p["conditional_count"] == 210
    assert p["joint_count"] == 210
    assert p["conditional_joint_accounted"] == 420
    assert p["operation_refs_unique"] is True
    assert len(A["accounting"]) == 420
    assert {row["operation_kind"] for row in A["accounting"]} == {"CONDITIONAL", "JOINT"}
    assert len({row["operation_ref"]["content_hash"] for row in A["accounting"]}) == 420


def test_02_first_missing_is_item_occurrence_not_a_name_or_policy():
    r = A["resolution"]
    assert r["status"] == "HOLD_FIRST_EXACT_INPUT_MISSING"
    assert r["p1_sourceitem_refs_exact_in_c11"] == 0
    assert r["p1_code_matches_in_c11"] == 420
    assert r["r03_candidate_keys_are_name_only"] is True
    assert r["r03_candidate_policy_exact"] is False
    first = r["first_missing"]
    assert first["first_p1_item_registry_ref"] == "urn:test:programma:itemregistry:g00"
    assert first["first_p1_item_registry_content_present"] is False
    assert first["first_p1_target_sourceitem"]["kind"] == "SourceItem"
    assert first["first_p1_conditioner_sourceitem"]["kind"] == "SourceItem"
    assert first["first_c11_target_question_ref"]["kind"] == "QUESTION_NATIVE"
    assert first["first_c11_conditioner_question_ref"]["kind"] == "QUESTION_NATIVE"
    assert first["first_r03_candidate_target_key"]["option_id"] is None
    assert first["first_r03_candidate_conditioner_key"]["repeat_id"] is None
    assert A["additional_gates"]["item_occurrence"]["accepted"] is False
    assert A["additional_gates"]["r03_policy_direction_risk"]["exact_policy_present"] is False


def test_03_no_end_to_end_execution_or_invented_binding():
    r = A["resolution"]
    assert r["end_to_end_replay_attempted"] is False
    assert r["executed_operations"] == 0
    assert r["unsupported_entries"] == 420
    assert r["status_counts"] == {"TYPED_REFUSAL": 420}
    assert r["reason_counts"] == {
        "P1_SOURCEITEM_TO_C11_R03_OCCURRENCE_BINDING_ABSENT": 420}
    assert r["condition_value_counts"] == {"0": 210, "1": 210}
    assert r["target_value_available_in_c11"] == 420
    assert r["condition_value_available_in_c11"] == 210
    assert r["c11_source_identity_equal_to_p1_wave"] == 0
    assert r["catalog_probe"]["attempted"] is True
    assert r["catalog_probe"]["catalog_only_not_execution"] is True
    assert r["catalog_probe"]["catalog_query_count"] == 2
    assert A["scope"]["policy_manufactured"] is False
    assert A["scope"]["occurrence_mapping_manufactured"] is False
    assert A["scope"]["production_edit"] is False
