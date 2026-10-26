"""R153 focused R152 RED successor and evidence checks."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))
if str(RUNTIME.parents[2]) not in sys.path:
    sys.path.insert(0, str(RUNTIME.parents[2]))

import native_evidence_repair as ner  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return ner.build_all()


def test_r152_wvs_administration_default_form_red_is_green(result):
    rec = result["records"]["SRC35"]
    native = rec["evidence_resolution"]["native_objects"]
    assert native is None
    assert rec["evidence_resolution"]["native_occurrence_count"] == 0
    assert rec["evidence_resolution"]["native_source_rule_count"] == 0
    assert rec["evidence_resolution"]["source_inventory_count"] == 0
    assert rec["evidence_resolution"]["held_native_objects"]
    assert "DEFAULT_FORM" not in json.dumps(rec)
    assert "\"administered\"" not in json.dumps(rec)
    for item in rec["pending_native_occurrences"]:
        if item["source_variable_code"] in {"Q291G5", "Q291P5"}:
            assert item["native_occurrence_constructed"] is False
            assert item["native_source_rule_constructed"] is False
            assert item["unit_status"].startswith("PENDING_EXACT_WVS7")
            assert item["topology_status"] == "EXACT_WVS7_SOURCE_TOPOLOGY"
            assert item["risk_set_status"] == "EXACT_WVS7_RISK_SET"
            assert item["forms_status"].startswith("PENDING_EXACT_WVS7")
            assert item["administration_status"].startswith("PENDING_EXACT_WVS7")
            assert item["domain_status"] == "EXACT_TYPED_SURFACE_DOMAIN"


def test_wvs_exact_evidence_and_supported_fields_preserved(result):
    s = result["summary"]
    wvs = s["wvs_evidence"]
    assert wvs["source_sha256"] == "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
    assert wvs["topology"] == "SCALAR_SINGULAR"
    assert wvs["risk_ref"]["content_hash"] == "0bf6a655a35617bec3e54f4d547e89282920e7835e406dcb43b3456774ab87d7"
    assert wvs["unit"] is None and wvs["forms"] is None and wvs["administration"] is None
    assert wvs["package_sha256"] == "c0fa82f9cc2244324fc7cb0306b4244d9320955d71ba8c15ced835cabaed61f6"
    rec = result["records"]["SRC35"]
    for item in rec["pending_native_occurrences"]:
        if item["source_variable_code"] in {"Q291G5", "Q291P5"}:
            assert "domain" in item["resolved_fields"]
            assert "topology" in item["resolved_fields"]
            assert "risk_set" in item["resolved_fields"]
            assert item["unresolved_fields"] == ["unit", "form", "administration"]


def test_conservation_context_and_codebook_rows_preserved(result):
    s = result["summary"]
    assert s["source_count"] == 35
    assert s["b49_item_records"] == 4460
    assert s["typed_surface_only_items"] == 33
    assert s["preparation_items"] == 4493
    assert s["codebook_rows"] == 18276
    assert s["typed_surfaces_consumed"] == 38
    assert s["context_items_retained"] == 3804
    assert s["unmatched_relation_ids"] == 26
    assert all(rec["current_source_identity_or_grant"]["u_root"] is None for rec in result["records"].values())
    assert all(rec["current_source_identity_or_grant"]["e_pre_root"] is None for rec in result["records"].values())
    assert all(rec["native_execution_authorized"] is False for rec in result["records"].values())


def test_lits_partial_fields_are_not_erased(result):
    rec = result["records"]["SRC27"]
    for item in rec["pending_native_occurrences"]:
        if item.get("typed_surface_id") in {"S001", "S002"}:
            assert "domain" in item["resolved_fields"]
            assert "unit" in item["resolved_fields"]
            assert "risk_set" in item["resolved_fields"]
            assert "topology" in item["unresolved_fields"]
            assert item["native_occurrence_constructed"] is False


def test_foreign_scope_and_decoder_refusal(result, monkeypatch, tmp_path):
    bad = dict(result["inputs"]["wvs"]) if "inputs" in result else None
    # build_all does not export inputs; exercise evidence validation directly.
    wvs = json.loads(ner.WVS_PACKAGE_PATH.read_text(encoding="utf-8"))
    bad_wvs = dict(wvs, source_sha256="0" * 64)
    with pytest.raises(ner.EvidenceRepairRefusal, match="WVS7_SOURCE_SCOPE_MISMATCH"):
        ner._wvs_evidence(bad_wvs)
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    ner.write_records(result, tmp_path)
    assert calls["decode"] == 0
    assert (tmp_path / "records" / "SRC35_R153_NATIVE_INPUT.json").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()
