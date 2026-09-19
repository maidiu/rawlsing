from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BLOCK = "EE_P2R6P_BLOCK__WVS7_GOVERNED_C11_PROJECTION_COORDINATE_SEMANTICS_AUTHORITY_ABSENT"
CATALOG = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
ACTIVE = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"


def _j(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_historical_lits_blocker_is_superseded_without_claiming_backend_pass():
    hist = _j("WORKER_RETURNS/EE-P2R6P/01_HISTORICAL_BE1_BLOCKER_SUPERSESSION.json")
    lits = _j("WORKER_RETURNS/EE-P2R6P/02_LITS_BACKEND_BINDING_RECEIPT.json")
    assert hist["historical_lits_blocker_superseded"] is True
    assert hist["complete_backend_adoptable"] is False
    assert lits["runtime_catalog_identity"] == CATALOG
    assert lits["active_binding"] == ACTIVE
    assert lits["candidate_A_owner_seam"] == "PASS"
    assert lits["candidate_B_owner_seam"] == "PASS"


def test_wvs_lock2_is_accepted_but_coordinate_authority_is_absent():
    wvs = _j("WORKER_RETURNS/EE-P2R6P/03_WVS_BACKEND_BINDING_RECEIPT.json")
    assert wvs["lock2"] == LOCK2
    assert wvs["lock2_runtime_authority"] == "PASS"
    assert wvs["governed_c11_projection"] == "BLOCKED"
    assert wvs["first_missing_authority_kind"] == "COORDINATE_SEMANTICS"
    assert "COORDINATE_SEMANTICS" not in wvs["p2f2_authority_kinds"]
    assert wvs["block_terminal"] == BLOCK


def test_accepted_owner_requires_explicit_complete_projection():
    facade = (ROOT / "rawlsing_next/pre553_source_backed_c11_facade.py").read_text(encoding="utf-8")
    assert "class GovernedC11Projection" in facade
    assert "self.coordinate_slots" in facade
    assert "projection omits mandatory governed semantic input" in facade
    assert "explicit governed projection required; no semantic inference permitted" in facade


def test_r6p_does_not_materialize_partial_production_backend():
    assert not (ROOT / "rawlsing_next/ee_p2x_darwin_stage_backend.py").exists()
    neg = _j("WORKER_RETURNS/EE-P2R6P/05_BACKEND_NEGATIVE_COURT.json")
    assert neg["production_backend_materialized"] is False
    assert neg["new_wvs_semantic_authority_created"] is False
    assert neg["carrier_access"] is False
    assert neg["performance_measurement"] is False


def test_stage_coverage_stops_at_first_wvs_projection_precondition():
    cov = _j("WORKER_RETURNS/EE-P2R6P/04_STAGE_COVERAGE_MATRIX.json")
    assert cov["overall_disposition"] == "BLOCKED_BEFORE_COMPLETE_BACKEND_IMPLEMENTATION"
    assert cov["WVS7"]["A"]["first_blocked_stage"] == "S01_CANDIDATE_PREPARATION_BUILD"
    assert cov["WVS7"]["B"]["first_blocked_stage"] == "S01_CANDIDATE_PREPARATION_BUILD"
    assert cov["WVS7"]["C"]["backend_path"] == "NONE__PRESERVED_PORTABILITY_FAILURE"
    assert cov["LITS_I"]["C"]["disposition"] == "C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION"
