"""35-source configuration ledger and disposition preservation."""
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping

from rawlsing_next.source_configuration.evidence import verify_evidence_manifest

from .provenance import R157_CANDIDATE, R157_PLAN_SEAL, R157_REVIEW_CUT
from .registry import FIXTURE_ONLY, NOT_RUN, UniversalSourceRegistry

LEDGER_SCHEMA = "PYAT_777_UNIVERSAL_SOURCE_TO_C11_LEDGER@1.0.0"
EXPECTED = {
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


def ledger_row(registry: UniversalSourceRegistry, source_id: str) -> dict[str, Any]:
    slot = registry.slot(source_id)
    roster = slot.roster_row
    index = slot.index_row
    hashes = registry.config_hashes(source_id)
    unmatched = list(roster.get("unmatched_relation_ids", ()))
    return {
        "source_id": source_id,
        "family": slot.family,
        "wave": slot.wave,
        "lane": index.get("lane"),
        "status": index["status"],
        "disposition": slot.disposition,
        "original_execution": NOT_RUN,
        "fixture_release": "PROVEN_CURRENT_C11_CONSUMER",
        "declared_supported": slot.declared_supported,
        "physical_slots": int(roster["physical_columns"]),
        "original_items": int(roster["original_items"]),
        "exact_relation_joins": int(roster["exact_relation_matches"]),
        "unmatched_relation_ids": unmatched,
        "unmatched_count": len(unmatched),
        "held_slots": int(index.get("held", {}).get("held_slots", 0)),
        "original_config_path": index["original_config_path"],
        "fixture_config_path": index["fixture_config_path"],
        "fixture_path": index["fixture_path"],
        "native_results_path": index["native_results_path"],
        **hashes,
        "fixture_row_count": slot.fixture_stream.row_count,
        "fixture_release_ref": dict(index["release_ref"]),
        "source_read_performed": False,
        "original_respondent_rows_read": False,
        "source_bytes_copied": False,
    }


def build_ledger(registry: UniversalSourceRegistry) -> dict[str, Any]:
    rows = [ledger_row(registry, source_id) for source_id in registry.source_ids]
    dispositions = Counter(row["disposition"] for row in rows)
    totals = {
        "sources": len(rows),
        "physical_slots": sum(row["physical_slots"] for row in rows),
        "original_items": sum(row["original_items"] for row in rows),
        "exact_relation_joins": sum(row["exact_relation_joins"] for row in rows),
        "unmatched_relation_ids": sum(row["unmatched_count"] for row in rows),
        "held_slots": sum(row["held_slots"] for row in rows),
        "fixture_releases": sum(1 for row in rows if row["fixture_release"] == "PROVEN_CURRENT_C11_CONSUMER"),
        "not_run": dispositions.get(NOT_RUN, 0),
        "fixture_only": dispositions.get(FIXTURE_ONLY, 0),
    }
    if totals != EXPECTED:
        raise AssertionError(f"35-source ledger totals drift: {totals!r}")
    manifest = verify_evidence_manifest()
    if not manifest["ok"]:
        raise AssertionError(f"portable evidence manifest failed: {manifest['failures']!r}")
    return {
        "schema": LEDGER_SCHEMA,
        "plan_seal": R157_PLAN_SEAL,
        "r157_candidate": R157_CANDIDATE,
        "r157_review_cut": R157_REVIEW_CUT,
        "source_scope": "ALL_35_DECLARED_SOURCES",
        "single_wave_target": False,
        "generic_factory": "rawlsing_next.source_configuration.factory",
        "current_consumer_receive_seam": "rawlsing_next.universal_source_to_c11.consumer.receive_fixture_release",
        "original_source_execution": "NOT_RUN",
        "original_respondent_rows_read": False,
        "original_source_bytes_copied_or_uploaded": False,
        "original_source_execution_performed": False,
        "universal_native_source_package_mandate": False,
        "totals": totals,
        "evidence_manifest": {
            "ok": manifest["ok"],
            "counts": manifest["manifest"]["counts"],
            "plan_seal": manifest["manifest"]["plan_seal"],
        },
        "first_real_source_dependency": {
            "type": "EXTERNAL_SOURCE_SELECTION_RIGHTS_BYTES_ISSUER",
            "sequence": [
                "source_and_wave_selection_by_the_authorized_owner",
                "rights_and_target_use_determination",
                "external_source_bytes_and_custody_locator",
                "current issuer decision / source-read permission",
                "separately issued original workload",
            ],
            "present": False,
            "manufactured_success": False,
            "note": "No original source, respondent file, SAV/DTA/DB byte or source-read grant is present or claimed.",
        },
        "independent_review_required": True,
        "goal_complete": False,
        "sources": rows,
    }
