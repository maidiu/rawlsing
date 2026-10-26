"""R150 focused B49-to-native-input checks."""
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

import scientific_native_input as sni  # noqa: E402
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceIdentity  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return sni.build_all()


def test_all35_item_accounting_and_compiler_reuse(result):
    s = result["summary"]
    b49 = result["inputs"]["b49"]
    assert s["source_count"] == 35
    assert s["b49_item_records"] == 4460
    assert s["b49_sources_with_items"] == ["SRC01", "SRC24", "SRC26", "SRC27", "SRC28", "SRC29", "SRC30"]
    assert s["selected_u_candidate"] == 371
    assert s["held"] == 285
    assert s["excluded_non_u_context"] == 3804
    assert s["unmatched_relation_ids"] == 26
    assert s["codebook_joined"] == 4460
    assert s["codebook_missing"] == 0
    assert s["native_identities"] == 35
    assert s["selected_packages"] == 35
    assert s["pending_occurrences"] == 4460
    assert isinstance(result["inputs"]["corpus"], b49.SourceAuthorityCorpus)
    assert len(result["inputs"]["corpus"].sources) == 35


def test_lits_grounded_first_and_typed_native_identity(result):
    expected = {"SRC27": (50, 7, 1141, 1198), "SRC28": (116, 9, 502, 627),
                "SRC29": (98, 51, 1141, 1290), "SRC30": (107, 192, 1020, 1319)}
    for sid, (selected, held, excluded, total) in expected.items():
        rec = result["records"][sid]
        counts = rec["item_counts"]
        assert (counts["selected_u_candidate"], counts["held"],
                counts["excluded_non_u_context"], counts["total"]) == (selected, held, excluded, total)
        ident = rec["native_source_identity"]
        typed = NativeSourceIdentity(
            source_id=ident["source_id"], family=ident["family"], wave=ident["wave"],
            canonical_filename=ident["canonical_filename"],
            declared_sha256=ident["declared_sha256"],
            source_format=ident["source_format"], expected_rows=ident["expected_rows"])
        assert typed.source_id == sid
        assert rec["selected_source_rule_package"]["schema"].startswith("PRE553_SELECTED")
        assert rec["native_source_rule_status"].startswith("PENDING_")
        assert rec["native_source_inventory_status"].startswith("NOT_CONSTRUCTED")
        assert rec["source_read_grant_present"] is False
        assert rec["survey_file_touched"] is False


def test_item_join_direction_routing_unit_and_context_lanes(result):
    rec = result["records"]["SRC27"]
    items = rec["pending_native_occurrences"]
    assert len(items) == 1198
    assert all(item["codebook_join_status"] == "EXACT_CODEBOOK_VAR_JOIN" for item in items)
    assert all(item["unit_status"] == "PENDING_EXACT_ITEM_UNIT" for item in items)
    assert all(item["topology_status"] == "PENDING_EXACT_ITEM_TOPOLOGY" for item in items)
    assert all(item["risk_set_status"] == "PENDING_EXACT_RISK_SET" for item in items)
    assert any(item["semantic_direction"] == "NOT_CERTIFIED"
               and item["conditioning_context_retained"] is True
               for item in items)
    context = rec["conditioner_context_items"]
    assert context
    assert all(item["conditioning_context_retained"] is True for item in context)
    assert all(item["target_measurement_eligible"] is False for item in context)
    assert rec["item_counts"]["excluded_non_u_context"] == len(context)


def test_unmatched_relation_ids_held_and_all35_successors_named(result):
    total_unmatched = 0
    for sid, rec in result["records"].items():
        total_unmatched += len(rec["unmatched_relation_ids"])
        if not rec["item_counts"]["total"]:
            assert rec["successor_target"]
            assert rec["native_source_rule_status"].startswith("PENDING_")
        for item in rec["pending_native_occurrences"]:
            if item["implementation_id"] in rec["unmatched_relation_ids"]:
                assert item["compiler_status"] == "HELD_UNRESOLVED"
                assert item["compiler_reason"] == "FQRA_RELATION_ID_UNMATCHED__HELD_NOT_PROMOTED"
    assert total_unmatched == 26


def test_no_source_or_grant_claim_and_no_decoder_call(result, monkeypatch):
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    assert calls["decode"] == 0
    for rec in result["records"].values():
        assert rec["current_source_identity_or_grant"]["u_root"] is None
        assert rec["current_source_identity_or_grant"]["e_pre_root"] is None
        assert rec["frontier_status"].startswith("UNSIGNED_PENDING")
        assert rec["native_execution_authorized"] is False


def test_refuses_bad_pin_source_and_records_export(result, monkeypatch, tmp_path):
    with pytest.raises(sni.ScientificNativeInputRefusal, match="B49_SOURCE_ID_NOT_NUMERIC"):
        sni._source_id(type("S", (), {"source_id": "not-numeric"})())
    original = sni._bytes_sha
    monkeypatch.setattr(sni, "_bytes_sha", lambda value: "0" * 64)
    with pytest.raises(sni.ScientificNativeInputRefusal, match="STAGED_B49_PIN_MISMATCH"):
        sni.load_inputs()
    monkeypatch.setattr(sni, "_bytes_sha", original)
    sni.write_records(result, tmp_path)
    assert (tmp_path / "records" / "SRC27_SCIENTIFIC_NATIVE_INPUT.json").is_file()
    assert (tmp_path / "records" / "ITEMS" / "SRC27.jsonl").is_file()
    assert (tmp_path / "records" / "PACKAGES" / "SRC27.json").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()


def test_consumer_requirements_and_next_calls_are_explicit(result):
    rec = result["records"]["SRC27"]
    assert [x["consumer_id"] for x in rec["consumer_requirements"]] == [
        "F1_EMPIRICAL_CLOSURE", "F2_DISCOVERY_AND_NO_DROP",
        "F3_M1_LEARNED_DISPOSITION", "F4_FF_V553_CONFRONTATION"]
    assert rec["next_original_source_read_call"]["function"].endswith("decode_with_source_read_permission")
    assert rec["next_original_source_read_call"]["status"].startswith("NOT_RUN")
    assert rec["next_native_workload_call"]["function"].endswith("prepare_production_discovery")
    assert rec["next_native_workload_call"]["status"].startswith("UNSIGNED_PLANNING_ONLY")
    assert "complete native U" in rec["indispensable_unbound"]
    assert rec["already_grounded"]
    assert result["records"]["SRC24"]["family_label_resolution"].startswith("LATINOBAROMETRO")
    assert all(not rec["codebook_collisions"] for rec in result["records"].values())
