"""Focused checks for SRC04 routing/eligibility authority."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
A = json.loads((R / "01_ROUTING_AUTHORITY_RECEIPT.json").read_text())


def test_01_42_fields_have_no_evidenced_route_or_denominator():
    r = A["routing_interface"]
    assert r["selected_fields"] == 42
    assert r["exact_routing_bindings"] == 0
    assert r["typed_unknown_or_held"] == 42
    assert r["exact_eligibility_denominators"] == 0
    assert r["unresolved_eligibility_denominators"] == 42
    assert r["route_selector_all_is_not_eligibility_authority"] is True
    assert r["normal_configuration_schema_valid"] is True
    assert all(row["routing_rule_exact"] is False for row in A["rows"])
    assert all(row["eligibility_denominator_exact"] is False for row in A["rows"])
    assert all(row["eligible"] == "UNKNOWN" for row in A["rows"])
    assert all(row["routed_or_ineligible"] == "UNKNOWN" for row in A["rows"])


def test_02_28_certified_and_14_held_with_exact_missing_premise():
    c = A["certified_and_held"]
    assert c["certified_count"] == 28
    assert c["held_count"] == 14
    assert len(c["certified"]) == 28
    assert len(c["held"]) == 14
    assert set(c["held"]) == {
        "q202", "q207", "q210", "q212", "q216", "q222", "q224",
        "q226", "q227", "q228", "q2301", "q2302", "q2311", "q2312",
    }
    for qid in c["held"]:
        row = c["held_exact_missing_premise"][qid]
        assert row["status"] == "HELD_UNCERTIFIED"
        assert "competent response-semantics certification" in row["premise"]
        assert row["routed_or_ineligible"] == "UNKNOWN"


def test_03_retained_aggregate_conservation_and_distinct_states():
    r = A["retained_aggregate_replay"]
    assert r["corrected"]["valid_answer"] == 275397
    assert r["corrected"]["explicit_nonresponse"] == 23422
    assert r["corrected"]["refusal"] == 2185
    assert r["corrected"]["missing_or_unobserved"] == 9335
    assert r["corrected"]["source_record_denominator"] == 308154
    assert r["corrected"]["valid_answer"] + r["corrected"]["explicit_nonresponse"] + r["corrected"]["missing_or_unobserved"] == 308154
    assert r["conserved"] is True
    assert r["refusal_vs_substantive_distinction"] is True
    assert r["distinct_refusal_state"] == "EXPLICIT_NONRESPONSE"
    assert r["distinct_ineligible_state"] == "UNKNOWN_ROUTED_OUT_OR_INELIGIBLE"
    assert r["ineligible_or_routed_out_inferred_from_counts"] is False
    assert r["q101"]["corrected_valid"] == 7129
    assert r["q101"]["corrected_explicit"] == 204


def test_04_exact_missing_authority_is_named_not_inferred():
    a = A["authority"]
    assert a["first_missing_question"] == "q101"
    assert a["first_missing_rule_ref"].endswith("q101:unresolved")
    assert a["first_missing_risk_set_ref"].endswith("q101:unresolved")
    assert a["no_routing_rule_found_in_codebook"] is True
    assert a["codebook_route_terms_are_substantive_text_only"] is True
    assert a["codebook_route_term_hits"] == [{
        "classification": "SUBSTANTIVE_TEXT_NOT_A_ROUTING_RULE",
        "question_id": "q221",
        "terms": ["unconditional"],
    }]
    assert a["owner"].startswith("ARAB lane / P3 integration owner")
    assert any("routing" in row["required_native_field"] for row in a["exceptions"]["routing_related"])


def test_05_redaction_and_scope_limits():
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "value_label" not in text
    for key in (
        "original_source_read", "respondent_rows_read", "original_workload_issued",
        "production_config_adopted", "universal_code_rule",
        "routing_inferred_from_counts", "policy_fabricated",
        "scientific_issuance", "merge", "ci",
    ):
        assert A["limits"][key] is False
