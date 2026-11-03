"""Focused checks for the real SRC04 metadata-to-C11/R03 binding."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
A = json.loads((R / "01_REDACTED_RECEIPT.json").read_text())


def test_01_real_edition_mapping_and_existing_c11_caller():
    s = A["source"]
    c = A["c11"]
    m = A["mapping"]
    assert s["source_id"] == "SRC04"
    assert s["edition_sha256"] == "2a48ba4b2f23d022a2dfe4b8a0cc685febbd82579b5434f9ecd96ed4c1243d18"
    assert s["row_count"] == 7337
    assert s["column_count"] == 181
    assert s["source_config_sha256"] == "eb4c051ff2845bf3c8c7b5bfee08ea4c9879c7a5264cf1aa6290e3fd457bc900"
    assert s["config_canonical_sha256"] == "0e86814b62eb51dc9da22793b6de3e3598c3415632accb80f33bac965185f284"
    assert s["crosswalk_sha256"] == "034d626365249941618d66f6103a557209fce5d95362e3ddf77e29f2fe7fba23"
    assert s["validation_results_sha256"] == "c008704857b415e1a4515e55ae417097836fa37d628a0e521e9715d839fe5ee7"
    assert s["validation_status"] == "PASS"
    assert s["fixture_config_sha256"] == "7f69af5cfafe07123c211707df353b37da4e9375adfa6e55c5df42a930cfebaa"
    assert s["fixture_sha256"] == "e02e85388de86aa0ce66fa37ac59a6d3071537ea514788a54baf3964cbb44353"
    assert m["crosswalk_entries"] == 181
    assert m["config_items"] == 181
    assert m["response_slots"] == 178
    assert c["caller"].endswith("build_governed_c11_projection")
    assert c["respondents"] == 7337
    assert c["questions"] == 178
    assert c["response_slots"] == 178
    assert c["coordinate_slots"] == 3
    assert c["routing_facts"] == 1305986
    assert c["projection_ref"]["content_hash"] == "60206b998f89711801fa689283c20a6589281b77575a5ab002ad7c8cf23a51a8"
    assert c["original_source_read_performed"] is False


def test_02_fixture_native_release_matches_existing_c11_evidence():
    f = A["c11"]["fixture_release"]
    assert f["release_ref"]["content_hash"] == "9026fa33bb5739b87b06309f12e1d31fe6fd21fb471237eda870d6d278d47f42"
    assert f["public_objects"] == 2880
    assert f["expected_validation_release_matches"] is True
    assert f["fixture_source_sha256"] == "506d92179dcb76a3b1d5e0710d95472fa20313fcaf8b77cb6f548924c6e5d51b"
    assert f["fixture_rows"] == 8


def test_03_r03_normal_entrypoint_candidates_and_first_missing_gate():
    r = A["r03"]
    assert r["entrypoint"].endswith("OccurrenceKey")
    assert r["candidate_count"] == 178
    assert r["unique_candidate_count"] == 178
    assert r["item_identity_available"] is True
    assert r["form_exact"] is False
    assert r["repeat_exact"] is False
    assert r["route_exact"] is False
    assert r["policy_exact"] is False
    assert r["inventory_constructed"] is False
    assert r["execution_performed"] is False
    assert r["routing_unknown_count"] == 178
    assert r["risk_set_unresolved_count"] == 178
    first = A["first_missing"]
    assert "form/repetition" in first["artifact"]
    assert first["fields"] == [
        "supported_scope.supported_form_slice",
        "OccurrenceKey.form_id",
        "OccurrenceKey.repeat_id",
    ]
    assert first["owner"].startswith("ARAB lane / P3 integration owner")
    assert first["next_missing"]["counts"]["routing_unknown"] == 178
    assert first["next_missing"]["counts"]["risk_set_unresolved"] == 178


def test_04_redaction_and_authority_boundaries():
    text = json.dumps(A, sort_keys=True)
    assert "question_text" not in text
    assert "value_label" not in text
    assert "response_options_all" not in text
    for key in (
        "original_source_read", "restricted_material_published",
        "original_workload_issued", "production_edit", "merge", "ci",
        "policy_fabricated", "r03_execution",
    ):
        assert A["limits"][key] is False
    assert A["owner_limits"]["source_form_route_risk"].startswith("ARAB lane / P3")
    assert A["owner_limits"]["r03_policy_direction"].startswith("R03 GrammarPolicy")
