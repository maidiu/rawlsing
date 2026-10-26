"""R146 focused all35 existing-binding reuse checks."""
from __future__ import annotations

import copy
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

import all35_reuse_binder as ab  # noqa: E402


def _result():
    return ab.build_all35()


def test_all35_exact_source_ids_and_native_wave_identities():
    r = _result()
    s = r["summary"]
    assert s["source_count"] == 35
    assert s["source_ids"] == [f"SRC{i:02d}" for i in range(1, 36)]
    assert len(set(s["source_ids"])) == 35
    for source_id in s["source_ids"]:
        rec = r["records"][source_id]
        packet = r["inputs"][2][source_id]
        wave = rec["native_original_wave_identity"]
        expected = packet["required_original_wave_identity"]
        assert wave == {
            "atlas_id": expected["atlas_id"],
            "dataset_id": expected["dataset_id"],
            "source_family": expected["source_family"],
            "wave": expected["wave"],
        }
        closed = {row["source_id"]: row for row in r["inputs"][1]}
        assert rec["historical_canonical_sha256"] == closed[source_id]["canonical_sha256"]
        assert rec["survey_file_touched"] is False
        assert rec["source_read_grant_present"] is False
        assert rec["native_execution_authorized"] is False
        assert rec["source_specific_index_refs"], source_id
        assert all(ref["git_object_verified"] for ref in rec["source_specific_index_refs"])


def test_existing_binding_states_and_unresolved_are_preserved():
    r = _result()
    s = r["summary"]
    assert s["binding_state_counts"] == {
        "EXISTING_BINDING_WITH_HISTORICAL_REPRESENTATION_BLOCKER": 15,
        "EXISTING_PARTIAL_BINDING_WITH_L2_RESIDUAL_SET": 3,
        "EXISTING_USABLE_METADATA_BINDING_WITH_FULL_CODEBOOK": 3,
        "EXISTING_USABLE_METADATA_BINDING__NO_STAGED_CODEBOOK": 13,
        "INTENTIONALLY_EXCLUDED_BY_AUTHORITY72": 1,
    }
    assert s["sources_with_current_access_permission"] == 0
    assert s["sources_with_current_edition_hash"] == 0
    assert s["sources_with_current_u_e_pre"] == 0
    assert s["total_codebook_rows_reused"] == 3317
    assert s["sources_with_r145_full_codebook"] == ["SRC22", "SRC23", "SRC30"]
    assert s["survey_files_touched"] == 0
    closed = {row["source_id"]: row for row in r["inputs"][1]}
    packets = r["inputs"][2]
    for source_id, rec in r["records"].items():
        row = closed[source_id]
        packet = packets[source_id]
        assert rec["existing_closed35_binding"]["census"] == row["historical_representation"]["census"]
        assert rec["existing_closed35_binding"]["prep72_launch_class"] == row["historical_prep72_launch_class"]
        assert rec["existing_closed35_binding"]["later_packet_selected_fields"] == row["later_packet_selected_fields"]
        assert rec["existing_u43_binding"]["native_entrypoint"] == packet["native_entrypoint"]
        assert rec["existing_u43_binding"]["reason"] == packet["source"]["reason"]
        assert rec["country_resolution"]["rows_sha256"] == ab._sha(packet["source"]["historical_country_rows"])
        assert "CURRENT_SOURCE_ACCESS_PERMISSION" in rec["unresolved"]
        assert "SCIENTIFIC_E_PRE" in rec["unresolved"]


def test_r145_full_codebook_accounting_is_reused_not_reinterpreted():
    r = _result()
    for source_id, count in (("SRC23", 980), ("SRC22", 1018), ("SRC30", 1319)):
        rec = r["records"][source_id]
        reuse = rec["r145_codebook_reuse"]
        assert reuse["status"] == "R145_FULL_CODEBOOK_ROW_ACCOUNTING_AVAILABLE"
        assert reuse["rows"] == count
        assert reuse["row_accounting_sha256"]
        assert reuse["dictionary"]["sha256"]
        assert reuse["note"].startswith("codebook rows are not the administered universe")
        assert rec["binding_state"] == "EXISTING_USABLE_METADATA_BINDING_WITH_FULL_CODEBOOK"
    assert r["summary"]["total_codebook_rows_reused"] == 3317


def test_unknown_source_and_unbound_packet_hash_are_explicit():
    with pytest.raises(ab.All35BindingRefusal, match="UNKNOWN_OR_INCOMPLETE_SOURCE_ID"):
        ab.build_source("SRC99")
    r = _result()
    rec = r["records"]["SRC01"]
    assert rec["historical_hash_binding_status"] in {
        "CLOSED35_AND_U43_HISTORICAL_HASH_MATCH",
        "U43_ORIGINAL_MANIFEST_HASH_UNBOUND__CLOSED35_HISTORICAL_HASH_USED_FOR_NAVIGATION_ONLY",
    }
    assert rec["historical_identity_status"] == "HISTORICAL_NAVIGATION_ONLY_NOT_CURRENT_GRANT_OR_EDITION"


def test_no_decoder_or_survey_path_is_invoked(monkeypatch, tmp_path):
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    r = _result()
    assert calls["decode"] == 0
    ab.write_records(r, tmp_path)
    assert (tmp_path / "records" / "SRC23_REUSE_PREPARATION.json").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()
    assert r["summary"]["survey_files_touched"] == 0


def test_consumer_requirements_and_next_invocation_are_concrete():
    r = _result()
    rec = r["records"]["SRC23"]
    assert [x["consumer_id"] for x in rec["consumer_requirements"]] == [
        "F1_EMPIRICAL_CLOSURE", "F2_DISCOVERY_AND_NO_DROP",
        "F3_M1_LEARNED_DISPOSITION", "F4_FF_V553_CONFRONTATION"]
    assert "render_source_preparation.py --source-id SRC23" in rec["next_runnable_invocation"]
    assert rec["prospective_u_e_pre"]["u_root"] is None
    assert rec["prospective_u_e_pre"]["e_pre_root"] is None
    assert rec["prospective_u_e_pre"]["state"] == "NULL_WITH_CAUSE"
