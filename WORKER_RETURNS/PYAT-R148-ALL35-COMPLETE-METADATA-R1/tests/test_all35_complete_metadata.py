"""R148 focused complete all35 metadata/native-preparation checks."""
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

import all35_complete_metadata as cm  # noqa: E402
from rawlsing_next.pre553_issued_workload import OriginalWaveIdentity  # noqa: E402


@pytest.fixture(scope="module")
def result():
    return cm.build_all35()


def test_all35_current_metadata_complete(result):
    s = result["summary"]
    assert s["source_count"] == 35
    assert s["current_metadata_available_count"] == 35
    assert s["missing_current_metadata_count"] == 0
    assert s["current_metadata_rows"] == 18276
    assert s["new_current_metadata_rows"] == 2581
    assert s["newly_completed_metadata_sources"] == ["SRC04", "SRC05", "SRC06", "SRC07", "SRC11", "SRC13"]
    assert len(s["prior_reused_metadata_sources"]) == 29
    assert s["full35_denominator"] == 35
    assert s["excluded_from_full35_denominator"] == 0
    assert "STAGED_CURRENT_METADATA_DOCUMENT" not in s["current_unresolved_counts"]
    for sid, rec in result["records"].items():
        assert rec["current_metadata"]["status"] in {
            "CURRENT_METADATA_DOCUMENT_STAGED_AND_PINNED",
            "PRIOR_R145_CURRENT_METADATA_BINDING_REUSED",
        }, sid
        assert rec["current_metadata"]["row_accounting_path"]
        assert rec["current_metadata"].get("rows", 0) > 0


def test_new_six_full_row_accounting_hashes_and_duplicates(result):
    expected = {"SRC04": 181, "SRC05": 468, "SRC06": 359, "SRC07": 690, "SRC11": 370, "SRC13": 513}
    for sid, count in expected.items():
        rec = result["records"][sid]
        rows = result["new_rows"][sid]
        assert len(rows) == count == rec["current_metadata"]["rows"]
        assert len({row["var_name"] for row in rows}) == count
        assert len({row["row_hash"] for row in rows}) == count
        assert all(row["retained"] is True for row in rows)
        assert all(row["scientific_role"] == "UNASSIGNED_PENDING_EXACT_SEMANTIC_AUTHORITY" for row in rows)
        assert rec["current_metadata"]["sha256"] == next(
            item["sha256"] for item in result["inputs"]["staged"] if item["source_id"] == sid)
        assert rec["row_count_contradiction"] is None


def test_prior29_exact_reuse_and_contradictions_preserved(result):
    s = result["summary"]
    assert set(s["row_count_contradictions"]) == {"SRC01", "SRC24", "SRC26"}
    assert s["row_count_contradictions"]["SRC01"]["current_codebook_rows"] == 144
    assert s["row_count_contradictions"]["SRC24"]["research_identity_count"] == 206
    assert s["row_count_contradictions"]["SRC26"]["current_codebook_rows"] == 195
    assert result["records"]["SRC23"]["current_metadata"]["status"] == "PRIOR_R145_CURRENT_METADATA_BINDING_REUSED"
    assert result["records"]["SRC01"]["current_metadata"]["row_accounting_path"].startswith(
        "WORKER_RETURNS/PYAT-R147-ALL35-CURRENT-METADATA-R1/")
    assert result["records"]["SRC23"]["current_metadata"]["row_accounting_path"].startswith(
        "WORKER_RETURNS/PYAT-R145-CURRENT-SOURCE-PACKAGE-BINDING-R1/")


def test_historical_labels_and_full35_denominator_preserved(result):
    s = result["summary"]
    assert s["historical_exclusion_provenance_only"] == ["SRC35"]
    assert result["records"]["SRC35"]["full35_denominator"] is True
    assert result["records"]["SRC35"]["excluded_from_full35_denominator"] is False
    assert result["records"]["SRC35"]["current_representation_status"].startswith("HISTORICAL_EXCLUSION_PROVENANCE_ONLY")
    assert result["records"]["SRC02"]["current_representation_status"].startswith("PARTIAL_DOCUMENTARY_AUTHORITY")
    assert result["records"]["SRC14"]["current_representation_status"].startswith("DOCUMENTARY_REALIZATION_AUTHORIZED")
    for sid in ("SRC13", "SRC16", "SRC17"):
        assert result["records"][sid]["current_representation_status"].startswith("DOCUMENTARY_AUTHORITY_CLOSED")
    assert all("HISTORICAL_REPRESENTATION_AUTHORITY" not in rec["current_unresolved"]
               for rec in result["records"].values())
    assert s["current_unresolved_counts"]["CURRENT_REPRESENTATION_AUTHORITY_NOT_ESTABLISHED"] == 11
    assert s["current_unresolved_counts"]["EXACT_L2_RESIDUAL_SEMANTIC_SET"] == 3


def test_native_preparation_grounded_but_no_bundle_or_grant(result):
    for sid, rec in result["records"].items():
        wave = rec["native_preparation"]["original_wave_identity"]
        identity = OriginalWaveIdentity(
            wave["atlas_id"], wave["dataset_id"], wave["source_family"], wave["wave"])
        assert identity.atlas_id == sid
        assert rec["native_preparation"]["native_preimage_bundle_status"].startswith("NOT_CREATED")
        template = rec["source_read_request_template"]
        assert template["status"].startswith("TEMPLATE_ONLY")
        assert template["source_sha256"] is None
        assert rec["survey_file_touched"] is False
        assert rec["source_read_grant_present"] is False
        assert rec["native_execution_authorized"] is False
        assert "render_all35_current_preparation.py --source-id" in rec["next_runnable_invocation"]


def test_refusal_tamper_and_no_decoder_call(result, monkeypatch, tmp_path):
    with pytest.raises(cm.CompleteMetadataRefusal, match="GIT_OBJECT_UNAVAILABLE"):
        cm._r147_record("SRC99")
    staged = dict(result["inputs"]["staged"][0])
    staged["sha256"] = "0" * 64
    bad = dict(result["inputs"])
    bad["staged"] = [staged] + result["inputs"]["staged"][1:]
    with pytest.raises(cm.CompleteMetadataRefusal, match="NEW_METADATA_HASH_OR_BYTES_MISMATCH"):
        rec_base = cm._r147_record(staged["source_id"])
        cm._augment_new(staged["source_id"], rec_base, staged, result["inputs"]["packets"][staged["source_id"]])
    calls = {"decode": 0}
    def decode(*args, **kwargs):
        calls["decode"] += 1
        raise AssertionError("decoder called")
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_sav", decode)
    monkeypatch.setattr("rawlsing_next.pre553_physical_decoder.decode_dta", decode)
    cm.write_records(result, tmp_path)
    assert calls["decode"] == 0
    assert (tmp_path / "records" / "SRC13_CURRENT_METADATA_PREPARATION.json").is_file()
    assert (tmp_path / "records" / "ROW_ACCOUNTING" / "SRC13.jsonl").is_file()
    assert (tmp_path / "records" / "SUMMARY.json").is_file()
