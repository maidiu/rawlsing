"""Focused proof for the universal 35-source configuration-to-current-C11 seam."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from rawlsing_next.source_configuration.library import SOURCE_IDS
from rawlsing_next.universal_source_to_c11.cold_restore import cold_restore
from rawlsing_next.universal_source_to_c11.consumer import receive_fixture_release
from rawlsing_next.universal_source_to_c11.ledger import build_ledger
from rawlsing_next.universal_source_to_c11.negative import run_negative_suite
from rawlsing_next.universal_source_to_c11.provenance import (
    R157_CANDIDATE,
    R157_REVIEW_CUT,
    current_owner_abi,
    imported_cut_manifest,
    verify_imported_cut,
)
from rawlsing_next.universal_source_to_c11.registry import UniversalSourceRegistry

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def registry() -> UniversalSourceRegistry:
    return UniversalSourceRegistry()


def test_imported_r157_cut_is_exact(registry):
    manifest = imported_cut_manifest(include_sha256=False)
    verification = verify_imported_cut(manifest)
    assert verification["ok"], verification["failures"]
    assert manifest["r157_candidate"] == R157_CANDIDATE
    assert manifest["r157_review_cut"] == R157_REVIEW_CUT
    assert manifest["file_count"] == len(manifest["files"])
    assert manifest["file_count"] >= 450
    assert all(entry["git_blob"] == entry["working_blob"] for entry in manifest["files"])


def test_ledger_preserves_all35_scope_and_dispositions(registry):
    ledger = build_ledger(registry)
    totals = ledger["totals"]
    assert totals == {
        "sources": 35,
        "physical_slots": 18_413,
        "original_items": 18_276,
        "exact_relation_joins": 18_250,
        "unmatched_relation_ids": 26,
        "held_slots": 1_653,
        "fixture_releases": 35,
        "not_run": 24,
        "fixture_only": 11,
    }
    assert ledger["source_scope"] == "ALL_35_DECLARED_SOURCES"
    assert ledger["single_wave_target"] is False
    assert ledger["original_source_execution"] == "NOT_RUN"
    assert ledger["original_respondent_rows_read"] is False
    assert ledger["original_source_bytes_copied_or_uploaded"] is False
    assert ledger["universal_native_source_package_mandate"] is False
    assert ledger["goal_complete"] is False
    assert ledger["independent_review_required"] is True
    assert [row["source_id"] for row in ledger["sources"]] == list(SOURCE_IDS)
    assert {row["disposition"] for row in ledger["sources"]} == {"NOT_RUN", "FIXTURE_ONLY"}
    assert all(row["original_execution"] == "NOT_RUN" for row in ledger["sources"])
    assert all(row["source_read_performed"] is False for row in ledger["sources"])
    unmatched = [item for row in ledger["sources"] for item in row["unmatched_relation_ids"]]
    assert len(unmatched) == 26 == len(set(unmatched))
    assert sum(row["exact_relation_joins"] for row in ledger["sources"]) == 18_250


@pytest.mark.parametrize("source_id", SOURCE_IDS)
def test_fixture_release_through_current_c11_consumer(registry, source_id):
    receipt = receive_fixture_release(registry, source_id)
    expected = registry.slot(source_id).index_row["release_ref"]
    assert receipt.release_ref == expected
    assert receipt.facade_release_ref == expected
    assert receipt.repository_release_refs == (expected,)
    assert receipt.ingest_accepted is True
    assert receipt.ingest_disposition == "ACCEPTED_C11_LOGICAL_RELEASE"
    assert receipt.semantic_release_hash == expected["content_hash"]
    assert set(receipt.m01_m18_coverage) == {f"M{i:02d}" for i in range(1, 19)}
    assert receipt.original_execution == "NOT_RUN"
    assert receipt.source_read_performed is False
    assert receipt.original_respondent_rows_read is False
    assert receipt.source_bytes_copied is False
    assert receipt.original_workload_issued is False
    assert receipt.native_source_package_required is False
    assert receipt.projection_counts["respondents"] == receipt.fixture_row_count
    assert receipt.projection_counts["response_slots"] >= 0


def test_negative_refusals_are_fail_closed(registry):
    result = run_negative_suite(registry)
    assert result["passed"] is True, result
    names = {check["name"] for check in result["checks"]}
    assert names == {
        "unknown_source_refused",
        "cross_source_fixture_refused",
        "fixture_original_sha_reuse_refused",
        "fixture_reader_refused",
        "wrong_active_source_sha_refused",
        "original_execution_not_run_for_all_35",
        "no_original_source_byte_carriers_bundled",
        "original_plan_metadata_only",
    }


def test_cold_restore_is_byte_identical_and_exact():
    result = cold_restore("SRC26")
    assert result["ok"] is True, result
    assert result["rebuilt_index_byte_identical"] is True
    assert result["committed_index_sha256"] == result["rebuilt_index_sha256"]
    assert result["release_ref"]["content_hash"] == (
        "528ca5c34f7d9fd3c92ae5832d7be0001fec001a1053a046ba899a1ceda3164f")
    assert result["ingest_disposition"] == "ACCEPTED_C11_LOGICAL_RELEASE"
    assert result["source_read_performed"] is False
    assert result["original_execution"] == "NOT_RUN"


def test_current_owner_abi_is_exact_and_additive():
    abi = current_owner_abi()
    assert abi["no_new_engine"] is True
    assert abi["no_replacement_c11_i03_batch"] is True
    assert abi["native_source_package_required"] is False
    assert abi["current_consumer"]["facade"]["module"] == "rawlsing_next.pre553_source_backed_c11_facade"
    assert abi["current_consumer"]["ingest"]["module"] == "rawlsing_next.pre553_c11_ingest"
    for row in abi["owner_files"]:
        path = ROOT / row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        assert path.stat().st_size == row["bytes"]


def test_original_execution_and_source_bytes_remain_absent(registry):
    for source_id in registry.source_ids:
        document = registry.slot(source_id).original_config.document
        scope = document["supported_scope"]
        assert scope["native_validation_expectation"] == "NOT_RUN"
        assert scope["original_source_execution"] == "NOT_PERFORMED_UNDER_R157_PREPARATION"
        assert registry.slot(source_id).fixture_config.active_source_sha256 != (
            registry.slot(source_id).original_config.original_source_sha256)
    carriers = []
    for relative in ("rawlsing_next/source_configuration", "source_pre553_validation"):
        for path in (ROOT / relative).rglob("*"):
            if path.is_file() and path.suffix.lower() in {".sav", ".dta", ".por", ".db", ".mdb", ".accdb"}:
                carriers.append(path)
    assert carriers == []
