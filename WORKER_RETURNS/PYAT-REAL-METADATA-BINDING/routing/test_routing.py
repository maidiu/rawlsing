"""Focused checks for accepted SRC04 routing/denominator metadata."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
A = json.loads((R / "01_ROUTING_RECEIPT.json").read_text())


def test_01_accepted_42_slot_slice_and_null_form_repeat():
    a = A["accepted_slice"]
    assert a["selected_response_slots"] == 42
    assert a["selected_coordinate_slots"] == 2
    assert len(a["selected_question_ids"]) == 42
    assert a["single_interview_row"] is True
    assert a["form_id"] is None
    assert a["repeat_id"] is None
    assert a["form_repeat_identifiers_fabricated"] is False
    assert a["release_ref"]["content_hash"] == "fc111cfa78d0fc23b5c72c1dc4b45c39d35c66c394662d7b901f5422df3370ec"


def test_02_prior_accepted_tally_and_consumer_are_preserved():
    p = A["prior_tally_consumer"]
    assert p["focused_recheck_verdict"] == "PASS"
    assert p["focused_recheck_acceptance"] == "D1_OBSERVED_SAMPLE_DESCRIPTIVE_TALLY_ACCEPTED"
    assert p["tally_ref"] == "87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022"
    assert p["replay_ref"]["content_hash"] == "8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f"
    assert p["tally_product_sha256"] == "d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0"
    assert p["consumer_api"] == "rawlsing_next.pre553_carrier_execution.materialize_public_object"
    assert p["routing_state"] == "ROUTING_UNKNOWN"
    assert p["population_or_eligibility_claims"] == "NONE"
    assert p["event_presence_count"] == 308154
    assert p["observed_response_denominator_total"] == 298819
    assert p["answered_substantive_denominator_total"] == 277582
    assert p["missing_or_unobserved_total"] == 9335


def test_03_all_42_routing_entries_unknown_and_no_exact_denominator():
    r = A["routing_authority"]
    assert r["config_routing_entries"] == 178
    assert r["selected_routing_entries"] == 42
    assert r["selected_routing_unknown"] == 42
    assert r["selected_risk_set_unresolved"] == 42
    assert r["selected_exact_skip_rules"] == 0
    assert r["accepted_routing_binding"] is False
    assert r["source_record_denominator_binding"] is True
    assert r["eligibility_denominator_binding"] is False
    assert r["routing_inferred_from_observed_counts"] is False
    first = A["first_missing"]
    assert first["question_id"] == "q101"
    assert first["current_typed_state"] == "ROUTING_UNKNOWN"
    assert first["missing_rule_ref"].endswith("q101:unresolved")
    assert first["missing_risk_set_ref"].endswith("q101:unresolved")
    assert first["fields"] == [
        "routing[].typed_state", "routing[].routing_rule_ref",
        "routing[].risk_set_ref", "risk_set_refs",
    ]


def test_04_consumer_probe_distinguishes_response_not_route():
    c = A["consumer_probe"]
    assert c["question_id"] == "q101"
    assert c["valid_answer"] == 7162
    assert c["explicit_nonresponse"] == 171
    assert c["missing_or_unobserved"] == 4
    assert c["source_record_denominator"] == 7337
    assert c["eligible"] is None
    assert c["routed_out"] is None
    assert c["routing_rule_exact"] is False
    assert "eligibility and routed-out are not distinguishable" in c["consequence"]
    assert A["option_authority"]["rows_total"] == 12160
    assert A["option_authority"]["rows_selected_42"] == 367
    assert all(row["response_option_authority_rows"] > 0 for row in A["rows"])


def test_05_redaction_and_authority_boundaries():
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "value_label" not in text
    for key in (
        "original_source_read", "respondent_rows_read", "original_workload_issued",
        "production_edit", "merge", "ci", "policy_fabricated",
        "routing_inferred_from_observed_counts",
    ):
        assert A["limits"][key] is False
