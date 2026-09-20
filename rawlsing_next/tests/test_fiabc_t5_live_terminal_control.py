from __future__ import annotations

import copy
import pytest

from rawlsing_next.fiabc_live_terminal_control import (
    CLAIM_SCOPE,
    COURT_CONTRACT_SCHEMA,
    LiveTerminalControlError,
    validate_current_court_contract,
)

LITS="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS="2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"

def _manifest():
    return {
        "schema":"RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0",
        "sources":{"LITS_I":{"sha256":LITS},"WVS7":{"sha256":WVS}},
    }

def _contract():
    import json
    from pathlib import Path
    p=Path("WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json")
    return json.loads(p.read_text(encoding="utf-8"))

def test_current_six_cell_contract_passes_static_identity_gate():
    assert len(validate_current_court_contract(_contract(),_manifest())) == 64

def test_missing_sixth_current_capability_fails_closed():
    doc=_contract(); doc["cells"].pop()
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_historical_lits_c_failure_cannot_be_current_capability():
    doc=_contract()
    doc["cells"][2]["current_capability_ref"]="WORKER_RETURNS/EE-P2X/05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json"
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_historical_wvs_c_failure_cannot_be_current_capability():
    doc=_contract()
    doc["cells"][5]["current_capability_ref"]="WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json"
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_candidate_owner_drift_fails_closed():
    doc=_contract(); doc["candidate_owner_blobs"]["C"]="0"*40
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_t1_runtime_package_blob_drift_fails_closed():
    doc=_contract()
    doc["preservation_anchors"]["t1_runtime_packaging"]["lits_materializer"]["blob"]="0"*40
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_t3_process_isolation_blob_drift_fails_closed():
    doc=_contract()
    doc["preservation_anchors"]["t3_freeze_and_isolation"]["process_envelope"]["blob"]="0"*40
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_t4_accounting_surface_absence_fails_closed():
    doc=_contract()
    doc["t4_accounting_required_surfaces"]["actual_lifecycle_actions"]=False
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_historical_continuation_cannot_become_current_law():
    doc=_contract()
    doc["current_execution_manifest"]["historical_continuation_is_current_law"]=True
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())

def test_r35_may_not_be_merged_or_overclaimed_in_t5():
    doc=_contract(); doc["r35_post_t5_convergence"]["merged_in_t5"]=True
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())
    doc=_contract(); doc["claim_boundary"]["capability_105_cells"]=True
    with pytest.raises(LiveTerminalControlError):
        validate_current_court_contract(doc,_manifest())
