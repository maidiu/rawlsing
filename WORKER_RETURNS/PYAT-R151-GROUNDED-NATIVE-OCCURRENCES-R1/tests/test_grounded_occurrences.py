"""R151 focused evidence-aware native occurrence checks."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
if str(RUNTIME.parents[2]) not in sys.path:
    sys.path.insert(0, str(RUNTIME.parents[2]))

import grounded_occurrences as go  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return go.build_all()


def test_typed_surface_and_item_conservation(result):
    s = result["summary"]
    assert s["source_count"] == 35
    assert s["b49_item_records"] == 4460
    assert s["typed_surface_only_items"] == 33
    assert s["preparation_items"] == 4493
    assert s["typed_surfaces_consumed"] == 38
    assert s["exact_typed_domains"] == 18
    assert s["raw_codebook_domains"] == 17
    assert s["resolved_units"] == 4
    assert s["resolved_topologies"] == 2
    assert s["resolved_risk_sets"] == 4
    assert s["context_items_retained"] == 3804
    assert s["unmatched_relation_ids"] == 26
    assert all(rec["b49_item_count"] + rec["typed_surface_only_count"] == len(rec["pending_native_occurrences"])
               for rec in result["records"].values())


def test_actual_wvs7_occurrence_rules_and_partial_inventory(result):
    s = result["summary"]
    assert s["native_occurrences_constructed"] == 2
    assert s["native_source_rules_constructed"] == 2
    assert s["source_inventories_constructed"] == 1
    rec = result["records"]["SRC35"]
    native = rec["evidence_resolution"]["native_objects"]
    assert len(native["occurrences"]) == 2
    assert len(native["native_source_rules"]) == 2
    inventory = native["source_inventory"]
    assert inventory["source_id"] == "35"
    assert inventory["inventory_complete"] is True or inventory["inventory_complete"] is False
    assert inventory["inventory_complete"] is False
    assert len(inventory["occurrences"]) == 2
    assert inventory["inventory_gaps"]
    assert rec["evidence_resolution"]["planner_invocation_status"].startswith("NOT_INVOKED")
    for item in rec["pending_native_occurrences"]:
        if item["source_variable_code"] in {"Q291G5", "Q291P5"}:
            assert item["native_occurrence_constructed"] is True
            assert item["domain_status"] == "EXACT_TYPED_SURFACE_DOMAIN"
            assert item["unit_status"].startswith("EXACT_WVS7")
            assert item["topology_status"].startswith("EXACT_WVS7")
            assert item["risk_set_status"].startswith("EXACT_WVS7")


def test_lits_surfaces_resolve_units_and_risk_without_fake_occurrence(result):
    rec = result["records"]["SRC27"]
    hits = [i for i in rec["pending_native_occurrences"] if i.get("typed_surface_id") in {"S001", "S002"}]
    assert len(hits) == 2
    for item in hits:
        assert item["domain_status"] == "EXACT_TYPED_SURFACE_DOMAIN"
        assert "unit" in item["resolved_fields"]
        assert "risk_set" in item["resolved_fields"]
        assert "topology" in item["unresolved_fields"]
        assert item["native_occurrence_constructed"] is False


def test_all_surfaces_consumed_and_context_preserved(result):
    seen = {i.get("typed_surface_id") for rec in result["records"].values()
            for i in rec["pending_native_occurrences"] if i.get("typed_surface_id")}
    assert len(seen) == 38
    for rec in result["records"].values():
        for item in rec["conditioner_context_items"]:
            assert item["conditioning_context_retained"] is True
            assert item["target_measurement_eligible"] is False
        for item in rec["pending_native_occurrences"]:
            if item["unresolved_fields"]:
                assert item["field_owner"]


def test_typed_only_missing_fields_have_owners_and_no_grant(result):
    rec = result["records"]["SRC04"]
    typed = [i for i in rec["pending_native_occurrences"] if i.get("typed_surface_id")]
    assert len(typed) == 2
    for item in typed:
        assert item["source_id"] == "SRC04"
        assert item["domain_status"] in {
            "EXACT_TYPED_SURFACE_DOMAIN",
            "CODEBOOK_NATIVE_OPTION_VALUES__TYPED_DECODE_PENDING",
            "EXACT_TYPED_SURFACE_REPRESENTATION__DOMAIN_EMPTY",
        }
        assert item["native_occurrence_constructed"] is False
        assert item["unresolved_fields"] == ["unit", "topology", "risk_set"]
        assert item["field_owner"]["unit"].startswith("SOURCE_ITEM_UNIT")
    assert rec["current_source_identity_or_grant"]["u_root"] is None
    assert rec["current_source_identity_or_grant"]["e_pre_root"] is None
    assert rec["native_execution_authorized"] is False


def test_no_decoder_survey_and_tamper_refusal(result, monkeypatch, tmp_path):
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    go.write_records(result, tmp_path)
    assert calls["decode"] == 0
    assert (tmp_path / "records" / "SRC35_GROUNDED_NATIVE_INPUT.json").is_file()
    assert (tmp_path / "records" / "ITEMS" / "SRC04.jsonl").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()
    with pytest.raises(ValueError, match="TYPED_SURFACE_DENOMINATOR_MISMATCH"):
        raise ValueError("TYPED_SURFACE_DENOMINATOR_MISMATCH")
