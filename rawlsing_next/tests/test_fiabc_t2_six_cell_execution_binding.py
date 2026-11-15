import json
from pathlib import Path

import pytest

from rawlsing_next import ee_p2x_darwin_court_driver as driver
from rawlsing_next.pre553_candidate_c_production_binding import (
    LITS_I_CURRENT_SPEC,
    WVS7_CURRENT_SPEC,
)

REPO = Path(__file__).resolve().parents[2]
CURRENT = REPO / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
HISTORICAL = REPO / "WORKER_RETURNS/EE-P2X-CONTINUATION-REDUCER-R1/01_CONTINUATION_STATE_MACHINE.json"


def test_current_manifest_admits_exact_six_cells_and_rejects_historical_map_as_current():
    machine = driver.load_current_execution_manifest(CURRENT)
    pairs = [(c["source"], c["candidate"]) for c in machine.document["current_capabilities"]]
    assert pairs == [
        ("LITS_I","A"),("LITS_I","B"),("LITS_I","C"),
        ("WVS7","A"),("WVS7","B"),("WVS7","C"),
    ]
    assert all(c["status"] == "CURRENT_EXECUTABLE" for c in machine.document["current_capabilities"])
    with pytest.raises(driver.ContinuationMapError):
        driver.load_current_execution_manifest(HISTORICAL)


def test_candidate_c_current_scope_is_source_backed_without_identity_substitution():
    machine = driver.load_current_execution_manifest(CURRENT)
    c = machine.document["candidate_c_binding"]
    assert c["policy"] == "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS"
    assert c["candidate_b_identity_substitution_allowed"] is False
    assert c["historical_failure_receipts_are_current_capability_law"] is False
    assert c["LITS_I"]["permitted_accelerators"] == [
        "CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE",
        "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK",
    ]
    assert c["LITS_I"]["applicable_accelerators_current_f02"] == []
    assert c["LITS_I"]["q310_q311_required"] is True
    assert c["LITS_I"]["cacc3_allowed"] is False
    assert c["WVS7"]["permitted_accelerators"] == []
    assert c["WVS7"]["wvs_specific_cacc_allowed"] is False
    assert LITS_I_CURRENT_SPEC.applicable_accelerators == ()
    assert WVS7_CURRENT_SPEC.permitted_accelerators == ()


def test_candidate_c_stages_are_current_not_preserved_failure_law():
    machine = driver.load_current_execution_manifest(CURRENT)
    for source in ("LITS_I","WVS7"):
        assert machine.get(f"{source}/C/S01_CANDIDATE_PREPARATION_BUILD").disposition == "READY__RUN_LOCALLY"
        assert machine.get(f"{source}/C/S02_C11_REACHABILITY").disposition == "READY__RUN_LOCALLY"
    for sid in ("S12_STALE_CACHE_OR_PERSISTENT_STATE","S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
        sp = machine.get(f"WVS7/C/{sid}")
        assert sp.disposition == "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW"
        assert sp.evidence_or_stop_law_ref == "C_ZERO_ACCELERATOR_NO_CACHE"


def test_source_root_equality_is_court_wide_and_alternate_sources_are_forbidden():
    doc = json.loads(CURRENT.read_text(encoding="utf-8"))
    law = doc["source_root_law"]
    assert law["same_canonical_root_required_across_candidates"] is True
    assert law["alternate_edition_export_cleaned_source_allowed"] is False
    for cap in doc["current_capabilities"]:
        assert doc["sources"][cap["source"]]["sha256"] == law["canonical_source_sha256"][cap["source"]]
    derivative = law["preserved_or_prebuilt_derivative_substitution"]
    assert derivative["allowed_only_if_same_canonical_source_sha_proven"] is True
    assert derivative["accounting_classification_required"] is True


def test_live_backend_no_longer_contains_historical_candidate_c_hard_stops():
    text = (REPO / "rawlsing_next/ee_p2x_darwin_stage_backend.py").read_text(encoding="utf-8")
    assert "LiTS-C exact F02 q310/q311 reachability nonqualification" not in text
    assert "LiTS-C exact current q310/q311 reachability nonqualification" not in text
    assert "WVS-C has no backend execution path" not in text
    assert "_compose_current_candidate_c" in text
    assert "_assert_r5_canonical_source_root" in text
