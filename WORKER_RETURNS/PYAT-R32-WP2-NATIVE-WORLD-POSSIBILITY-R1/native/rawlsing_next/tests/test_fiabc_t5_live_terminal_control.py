from __future__ import annotations

import copy
import hashlib
import inspect
import json
import types
import pytest

import rawlsing_next.fiabc_live_terminal_control as t5
from rawlsing_next.fiabc_live_terminal_control import (
    CLAIM_SCOPE,
    COURT_CONTRACT_SCHEMA,
    LiveTerminalControlError,
    validate_current_court_contract,
    validate_t4_terminal_accounting_receipt,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _branch_predicate,
    _d_auth,
    _execute,
    _grammar,
    _predicate,
    _qt,
    _query,
    _query_authority,
    _response_leaf,
    _rule,
)

LITS="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS="2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
R1M = "WORKER_RETURNS/FIABC-LM2-R1M-LOCK2-SUCCESSOR-R16-ORACLE/07_FRESH_WVS_ORACLE.json"

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

def test_active_t5_wvs_constitution_is_successor_bound_not_predecessor():
    freeze = {
        "authority_identities": {"WVS7": {"authority": "frozen"}},
        "workload_identities": {"WVS7": {"workload": "frozen"}},
    }
    constitution = t5._court_constitution("WVS7", freeze)
    assert constitution["lock2_hash"] == t5.WVS7_SUCCESSOR_LOCK2
    assert constitution["lock2_replay_hash"] == t5.WVS7_SUCCESSOR_LOCK2_REPLAY
    assert constitution["discovery_authority"] == t5.WVS7_SUCCESSOR_DISCOVERY_AUTHORITY
    assert "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188" not in constitution.values()
    assert "b1aa437406d94b1f81f0ef3c81b885a2fd542749d2e5441747897c016a5dd490" not in constitution.values()
    assert "24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab" not in constitution.values()


def test_wvs_terminal_count_projection_reproduces_frozen_r1m_typed_domain():
    frozen = json.loads(open(R1M, encoding="utf-8").read())
    truth = frozen["truth_payload"]
    rows = truth["expected_fact_manifest"]
    receipts = tuple(
        types.SimpleNamespace(
            typed_state=row["typed_state"],
            coverage_state=row["coverage_state"],
        )
        for row in rows
    )
    expected = truth["expected_learned_product"]["coverage"][
        "typed_terminal_counts"
    ]
    assert len(receipts) == 46
    assert {receipt.coverage_state for receipt in receipts} == {
        "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY"
    }
    assert t5._typed_terminal_counts("WVS7", receipts) == expected == {
        "COVERAGE_LIMITED": 46
    }


def test_lits_terminal_count_projection_preserves_coverage_state_domain():
    receipts = (
        types.SimpleNamespace(
            typed_state="DISCOVERED_RESULT_SUPPORTED",
            coverage_state="EVALUATED_SUPPORTED",
        ),
        types.SimpleNamespace(
            typed_state="VALID_EMPTY",
            coverage_state="EVALUATED_VALID_EMPTY",
        ),
    )
    assert t5._typed_terminal_counts("LITS_I", receipts) == {
        "EVALUATED_SUPPORTED": 1,
        "EVALUATED_VALID_EMPTY": 1,
    }


def test_terminal_count_projection_rejects_unknown_source():
    with pytest.raises(
        LiveTerminalControlError,
        match="unknown source terminal-count compatibility domain",
    ):
        t5._typed_terminal_counts("UNKNOWN", ())


def test_wvs_runtime_successor_fallbacks_remain_opt_in(monkeypatch):
    import rawlsing_next.ee_p2x_darwin_stage_backend as backend
    import rawlsing_next.pre553_carrier_execution as carrier
    import rawlsing_next.pre553_runtime_context as runtime_context

    assert "return binding,projection,None" in inspect.getsource(backend._compose_wvs)

    sentinel = object()
    executor = types.SimpleNamespace(
        runtime_catalog=types.SimpleNamespace(
            discovery_authority_refs=("wvs-discovery",)
        ),
        execute_i05=lambda **kwargs: sentinel,
    )
    binding = types.SimpleNamespace(executor=executor)

    def forbidden_bind_runtime(*args, **kwargs):
        raise AssertionError("WVS predecessor path must not bind runtime successors")

    monkeypatch.setattr(runtime_context, "bind_runtime", forbidden_bind_runtime)
    monkeypatch.setattr(
        carrier,
        "learned_empirical_execution_receipt",
        lambda result: {"result_is_sentinel": result is sentinel},
    )
    result, receipt = backend._i05(binding, None)
    assert result is sentinel
    assert receipt == {"result_is_sentinel": True}

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

def test_t4_terminal_accounting_receipt_missing_fails_closed():
    with pytest.raises(LiveTerminalControlError):
        validate_t4_terminal_accounting_receipt(None)

def test_t4_terminal_accounting_receipt_byte_drift_fails_closed(tmp_path):
    p=tmp_path/"telemetry.json"
    p.write_text(json.dumps({"status":"PASS"})+"\\n",encoding="utf-8")
    good=hashlib.sha256(p.read_bytes()).hexdigest()
    row={
        "schema":"FIABC_T4_LIVE_ACCOUNTING_BINDING@1.0.0",
        "semantic_state_modified":False,
        "candidate_neutral_c0_excluded":True,
        "telemetry_receipt_path":str(p),
        "telemetry_receipt_sha256":good,
    }
    assert validate_t4_terminal_accounting_receipt(row)["telemetry_receipt_sha256"]==good
    row["telemetry_receipt_sha256"]="0"*64
    with pytest.raises(LiveTerminalControlError):
        validate_t4_terminal_accounting_receipt(row)


def test_constituent_i03_uses_retained_exact_fact_preimages_without_catalog_fallback():
    from rawlsing_next.tests.test_pre553_empirical_query import _build_source

    source = _build_source("fiabc-retained-i03", [
        {"id": "R1", "responses": {"X": 1, "Y": 1}},
        {"id": "R2", "responses": {"X": 0, "Y": 0}},
    ])
    qauth = _query_authority("fiabc-retained-i03")
    dauth = _d_auth("fiabc-retained-i03-discovery")
    all_p = _branch_predicate(source, qauth, tag="all")
    x1 = _predicate(source, qauth, _response_leaf(source, qauth, "X", 1), tag="x1")
    yq = _query(source, qauth, all_p, ("Y",), tag="y")
    validation = {"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"}
    grammar = _grammar(
        operation="I03-OP-fiabc-retained-i03-discovery",
        atoms=[_atom("ALL", all_p, "BRANCH"), _atom("X1", x1, "RESPONSE")],
        templates=[_qt("Y", yq)],
        rules=[_rule(
            "pair", "PAIR_RESPONSE_COTRAVEL", "SINGLE_ATOM",
            atom_ids=("X1",), baseline_atom_id="ALL", query_template_id="Y",
            validation=validation,
        )],
    )
    result = _execute(source, qauth, dauth, grammar, (all_p, x1), (yq,))

    def forbidden_rerun(**kwargs):
        raise AssertionError("derived query ref must not be fuzzy-resolved from template catalog")

    binding = types.SimpleNamespace(
        executor=types.SimpleNamespace(execute_i03=forbidden_rerun)
    )
    rows, facts, closure = t5._constituent_i03(binding, result)
    assert len(rows) == 1
    assert {tuple(sorted(row["ref"].items())) for row in facts} == {
        tuple(sorted(ref.as_dict().items())) for ref in result.empirical_fact_refs
    }
    assert len(closure) == 64

    missing = types.SimpleNamespace(
        receipts=result.receipts,
        empirical_fact_refs=result.empirical_fact_refs,
        empirical_facts=(),
    )
    with pytest.raises(LiveTerminalControlError, match="preimages"):
        t5._constituent_i03(binding, missing)
