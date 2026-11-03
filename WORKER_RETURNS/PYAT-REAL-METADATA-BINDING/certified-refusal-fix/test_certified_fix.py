"""Focused checks for the 28-entry certified refusal overlay."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
A = json.loads((R / "01_CERTIFIED_RECEIPT.json").read_text())
O = json.loads((R / "02_CERTIFIED_OVERLAY.json").read_text())


def test_01_28_certified_and_14_held_partition_42():
    v = A["validation"]
    assert v["selected_fields"] == 42
    assert v["certified_entries"] == 28
    assert v["held_entries"] == 14
    assert v["only_certified_entries_changed"] is True
    assert v["held_entries_changed"] is False
    assert v["schema_valid"] is True
    assert len(O["entries"]) == 28
    assert len(O["held_uncertified"]) == 14
    assert O["universal_code_rule"] is False
    assert O["authority_join"] == "per-item allowlist + exact option authority row"


def test_02_q101_and_aggregate_conservation():
    q = A["q101"]
    assert (q["old_valid"], q["old_explicit"]) == (7162, 171)
    assert (q["corrected_valid"], q["corrected_explicit"]) == (7129, 204)
    assert q["missing"] == 4 and q["total"] == 7337
    old = A["aggregate"]["old"]
    new = A["aggregate"]["corrected"]
    assert old["valid_answer"] == 277582
    assert old["explicit_nonresponse"] == 21237
    assert old["missing_or_unobserved"] == 9335
    assert old["source_record_denominator"] == 308154
    assert new["valid_answer"] == 275397
    assert new["explicit_nonresponse"] == 23422
    assert new["refusal"] == 2185
    assert new["missing_or_unobserved"] == 9335
    assert new["observed_response"] == 298819
    assert new["source_record_denominator"] == 308154
    assert new["valid_answer"] + new["explicit_nonresponse"] + new["missing_or_unobserved"] == new["source_record_denominator"]
    assert A["aggregate"]["conserved"] is True
    assert A["aggregate"]["refusal_vs_substantive_distinction"] is True


def test_03_per_item_certified_entries_are_exact_and_complete():
    certified = A["certified"]
    assert len(certified) == 28
    assert {row["question_id"] for row in certified} == {
        "q101", "q102", "q103", "q2011", "q2012", "q2013", "q2014",
        "q2015", "q204", "q205", "q206", "q211", "q2131", "q2132",
        "q2133", "q2134", "q2135", "q214", "q215", "q219", "q221",
        "q2251", "q2252", "q2321", "q2322", "q2323", "q2324", "q234",
    }
    assert all(row["code_count"] > 0 for row in certified)
    assert all(row["corrected_valid"] + row["corrected_explicit"] + row["missing"] == row["total"] for row in certified)


def test_04_held_entries_remain_substantive_and_routing_unknown():
    held = A["held"]
    assert len(held) == 14
    assert all(row["status"] == "HELD_UNCERTIFIED" for row in held)
    assert all(row["current_state"] == "SUBSTANTIVE_RESPONSE" for row in held)
    assert all(row["code_count"] > 0 for row in held)
    r = A["routing"]
    assert r["state"] == "ROUTING_UNKNOWN"
    assert r["selected_routing_unknown"] == 42
    assert r["selected_risk_set_unresolved"] == 42
    assert r["accepted_routing_binding"] is False
    assert r["eligibility_denominator_binding"] is False
    assert r["preserved"] is True


def test_05_redaction_and_limits():
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "value_label" not in text
    for key in (
        "original_source_read", "respondent_rows_read", "original_workload_issued",
        "production_config_adopted", "routing_inferred_from_counts",
        "policy_fabricated", "merge", "ci",
    ):
        assert A["limits"][key] is False
