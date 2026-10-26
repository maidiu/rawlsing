"""R147 focused current-metadata/all35 reconciliation checks."""
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

import current_metadata_reuse as cm  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return cm.build_all35()


def test_all35_current_metadata_consumption(result):
    s = result["summary"]
    assert s["source_count"] == 35
    assert s["full35_denominator"] == 35
    assert s["excluded_from_full35_denominator"] == 0
    assert s["staged_current_metadata_count"] == 26
    assert s["prior_r145_metadata_count"] == 3
    assert s["current_metadata_available_count"] == 29
    assert s["missing_current_metadata_count"] == 6
    assert s["current_metadata_rows"] == 15695
    missing = {sid for sid, rec in result["records"].items()
               if rec["current_metadata"]["status"].startswith("CURRENT_METADATA_DOCUMENT_NOT_STAGED")}
    assert missing == {"SRC04", "SRC05", "SRC06", "SRC07", "SRC11", "SRC13"}
    for sid in missing:
        assert result["records"][sid]["current_metadata"]["needed_document"]
    assert result["records"]["SRC23"]["current_metadata"]["status"] == "PRIOR_R145_CURRENT_METADATA_BINDING_REUSED"
    assert result["records"]["SRC01"]["current_metadata"]["status"] == "CURRENT_METADATA_DOCUMENT_STAGED_AND_PINNED"


def test_historical_labels_reconciled_not_current_automatic_blockers(result):
    s = result["summary"]
    assert s["historical_exclusion_provenance_only"] == ["SRC35"]
    assert result["records"]["SRC35"]["full35_denominator"] is True
    assert result["records"]["SRC35"]["excluded_from_full35_denominator"] is False
    assert result["records"]["SRC35"]["current_representation_status"].startswith("HISTORICAL_EXCLUSION_PROVENANCE_ONLY")
    assert result["records"]["SRC02"]["current_representation_status"].startswith("PARTIAL_DOCUMENTARY_AUTHORITY")
    assert result["records"]["SRC03"]["current_representation_status"].startswith("PARTIAL_DOCUMENTARY_AUTHORITY")
    assert result["records"]["SRC24"]["current_representation_status"].startswith("PARTIAL_DOCUMENTARY_AUTHORITY")
    assert result["records"]["SRC14"]["current_representation_status"].startswith("DOCUMENTARY_REALIZATION_AUTHORIZED")
    for sid in ("SRC13", "SRC16", "SRC17"):
        assert result["records"][sid]["current_representation_status"].startswith("DOCUMENTARY_AUTHORITY_CLOSED")
    assert all("HISTORICAL_REPRESENTATION_AUTHORITY" not in rec["current_unresolved"]
               for rec in result["records"].values())
    assert all("L2_RESIDUAL_SURFACES" not in rec["current_unresolved"]
               for rec in result["records"].values())
    assert s["current_unresolved_counts"]["CURRENT_REPRESENTATION_AUTHORITY_NOT_ESTABLISHED"] == 11
    assert s["current_unresolved_counts"]["EXACT_L2_RESIDUAL_SEMANTIC_SET"] == 3
    assert s["current_unresolved_counts"]["CURRENT_RELEASE_HASH"] == 1


def test_current_codebook_row_accounting_and_contradictions(result):
    assert set(result["summary"]["row_count_contradictions"]) == {"SRC01", "SRC24", "SRC26"}
    assert result["summary"]["row_count_contradictions"]["SRC01"]["current_codebook_rows"] == 144
    assert result["summary"]["row_count_contradictions"]["SRC24"]["research_identity_count"] == 206
    assert result["summary"]["row_count_contradictions"]["SRC26"]["current_codebook_rows"] == 195
    record = result["records"]["SRC01"]
    rows = record["_row_records"]
    assert len(rows) == 144
    assert len({row["var_name"] for row in rows}) == 144
    assert len({row["row_hash"] for row in rows}) == 144
    assert all(row["retained"] is True for row in rows)
    assert all(row["scientific_role"] == "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY" for row in rows)
    staged_rows = sum(len(result["records"][sid]["_row_records"])
                      for sid, rec in result["records"].items()
                      if rec["current_metadata"]["status"].startswith("CURRENT_METADATA_DOCUMENT_STAGED"))
    assert staged_rows == 12378


def test_reuses_r146_bindings_and_exact_treatment_refs(result):
    rec = result["records"]["SRC02"]
    assert rec["existing_binding_reuse"]["r146_binding_state"]
    assert rec["existing_binding_reuse"]["governing_index_refs"]
    assert rec["existing_binding_reuse"]["country_resolution"]["rows_sha256"]
    assert rec["completed_treatment_reuse"]["index_ref"]["git_object_verified"] is True
    assert "RESIDUAL" in rec["completed_treatment_reuse"]["terminal"]
    assert result["records"]["SRC16"]["completed_treatment_reuse"]["terminal"].startswith("CLOSED35_L2_GSS1972")
    assert result["records"]["SRC35"]["full35_denominator"] is True


def test_wrong_or_unknown_metadata_refuses(result):
    with pytest.raises(cm.CurrentMetadataRefusal, match="UNKNOWN_OR_INCOMPLETE_SOURCE_ID"):
        cm.build_source("SRC99", inputs=result["inputs"])
    staged = dict(result["inputs"]["staged"][0])
    staged["sha256"] = "0" * 64
    bad_inputs = dict(result["inputs"])
    bad_inputs["staged"] = [staged] + result["inputs"]["staged"][1:]
    with pytest.raises(cm.CurrentMetadataRefusal, match="CURRENT_METADATA_HASH_OR_BYTES_MISMATCH"):
        cm.build_source(staged["source_id"], inputs=bad_inputs)


def test_no_decoder_or_survey_file_and_records_are_written(result, monkeypatch, tmp_path):
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    cm.write_records(result, tmp_path)
    assert calls["decode"] == 0
    assert result["summary"]["survey_files_touched"] == 0
    assert (tmp_path / "records" / "SRC01_CURRENT_METADATA_PREPARATION.json").is_file()
    assert (tmp_path / "records" / "ROW_ACCOUNTING" / "SRC01.jsonl").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()
