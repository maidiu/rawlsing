"""Focused checks for original questionnaire evidence and route/decline states."""
from __future__ import annotations

import json
import sys
from pathlib import Path

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
A = json.loads((R / "04_QUESTIONNAIRE_AUTHORITY_RECEIPT.json").read_text())
P = json.loads((R / "PASSPORT.json").read_text())
from state_machine import classify_state


def test_01_editions_are_identical_and_all_42_have_exact_99_citations():
    e = A["edition_comparison"]
    assert e["byte_identical"] is True
    assert e["extracted_text_identical"] is True
    assert e["edition_delta"] == "NONE; the two supplied files are byte-identical"
    assert A["questionnaire"]["selected_fields"] == 42
    assert A["questionnaire"]["items_with_exact_99_decline"] == 42
    assert A["questionnaire"]["certified_28"] == 28
    assert A["questionnaire"]["held_14"] == 14
    rows = list(__import__("csv").DictReader((R / "evidence/QUESTIONNAIRE_ITEM_CITATIONS.csv").open()))
    assert len(rows) == 42
    assert all(row["response_99"] == "99 = Decline to Answer" for row in rows)
    assert all(int(row["pdf_page"]) >= 2 for row in rows)
    assert all(int(row["response_99_line"]) >= 1 for row in rows)


def test_02_all_14_held_have_exact_item_evidence_but_no_certification():
    held = {row["question_id"]: row for row in A["held_14_authority"]}
    assert set(held) == {
        "q202", "q207", "q210", "q212", "q216", "q222", "q224",
        "q226", "q227", "q228", "q2301", "q2302", "q2311", "q2312",
    }
    for qid, row in held.items():
        assert row["item_response_evidence"] == "99 = Decline to Answer"
        assert row["authority_status"] == "preserved_not_certified"
        assert row["authority_refusal_flag"] == "True"
        assert row["correction_applied"] is False
        assert "competent item-specific authority certification" in row["missing_premise"]
        assert row["eligible"] == "UNKNOWN"
        assert row["routed_or_ineligible"] == "UNKNOWN"
    assert sum(row["code_count"] for row in held.values()) == 1645


def test_03_no_route_rule_and_config_interface_validated():
    q = A["questionnaire"]
    assert q["exact_route_instruction_count"] == 0
    assert all(not pages for pages in q["route_terms"].values())
    assert q["routing_unknown_fields"] == 42
    assert q["routing_known_fields"] == 0
    assert q["eligible_known_fields"] == 0
    assert q["routed_out_known_fields"] == 0
    c = A["config_interface"]
    assert c["normal_schema_valid"] is True
    assert c["config_changed"] is False
    assert c["selected_route_entries"] == 42
    assert c["exact_route_bindings"] == 0
    assert c["exact_eligible_denominators"] == 0
    assert c["route_selector_all_is_not_eligibility_authority"] is True
    assert all(row["typed_state"] == "ROUTING_UNKNOWN" for row in c["rows"])
    assert all(row["eligible"] == "UNKNOWN" and row["routed_or_ineligible"] == "UNKNOWN"
               for row in c["rows"])


def test_04_retained_aggregate_invariants_preserved():
    r = A["retained_aggregate_replay"]
    assert r["corrected"]["valid_answer"] == 275397
    assert r["corrected"]["explicit_nonresponse"] == 23422
    assert r["corrected"]["refusal"] == 2185
    assert r["corrected"]["missing_or_unobserved"] == 9335
    assert r["corrected"]["source_record_denominator"] == 308154
    assert (r["corrected"]["valid_answer"] + r["corrected"]["explicit_nonresponse"]
            + r["corrected"]["missing_or_unobserved"] == 308154)
    assert r["conserved"] is True
    assert r["certified_refusal_delta"] == 2185
    assert r["held_code99_not_applied"] == 1645
    assert r["distinct_refusal_state"] == "EXPLICIT_NONRESPONSE"
    assert r["distinct_ineligible_state"] == "UNKNOWN_ROUTED_OUT_OR_INELIGIBLE"
    assert r["ineligible_or_routed_out_inferred_from_counts"] is False


def test_05_eligible_routed_out_and_declined_are_distinct_states():
    assert classify_state("UNKNOWN", 99, True) == "ROUTING_UNKNOWN"
    assert classify_state("INELIGIBLE", 99, False) == "ROUTED_OUT"
    assert classify_state("ELIGIBLE", 99, True) == "DECLINED"
    assert classify_state("ELIGIBLE", 99, False) == "RESPONSE_SEMANTICS_HELD"
    assert classify_state("ELIGIBLE", 1, True) == "ELIGIBLE_RESPONSE"
    assert len({classify_state("UNKNOWN", 99, True), classify_state("INELIGIBLE", 99, True),
                classify_state("ELIGIBLE", 99, True)}) == 3


def test_06_exact_citation_examples_and_14_page_evidence():
    rows = {row["question_id"]: row for row in
            __import__("csv").DictReader((R / "evidence/QUESTIONNAIRE_ITEM_CITATIONS.csv").open())}
    assert (rows["q101"]["pdf_page"], rows["q101"]["printed_page"]) == ("2", "3")
    assert (rows["q202"]["pdf_page"], rows["q202"]["printed_page"]) == ("3", "4")
    assert (rows["q2312"]["pdf_page"], rows["q2312"]["printed_page"]) == ("7", "8")
    assert rows["q234"]["response_99"] == "99 = Decline to Answer"
    assert all(rows[q]["response_99_pdf_page"] for q in (
        "q202", "q207", "q210", "q212", "q216", "q222", "q224",
        "q226", "q227", "q228", "q2301", "q2302", "q2311", "q2312"))


def test_07_sanitized_passport_runtime_and_limits():
    assert P["sanitized"] is True
    assert P["quota"] == "UNKNOWN"
    assert P["provider"] == "opencode-go"
    assert "deepseek" in P["model"].lower()
    assert A["runtime"]["config_schema_imported"] is True
    assert A["runtime"]["source_config_loaded"] is True
    assert A["runtime"]["quota"] == "UNKNOWN"
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "response_options_all" not in text
    for key in (
        "original_source_read", "respondent_rows_read", "original_workload_issued",
        "production_config_adopted", "universal_code_rule",
        "routing_inferred_from_counts", "policy_fabricated",
        "scientific_issuance", "merge", "ci",
    ):
        assert A["limits"][key] is False
