from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rawlsing_next.ee_w4_abc_hostile_measurement_harness import (  # noqa: E402
    HOSTILE_CASE_IDS,
    WORKLOAD_SCHEMA,
    execute_harness,
)


def h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write_adapter(tmp_path: Path) -> Path:
    p = tmp_path / "adapter.py"
    p.write_text(
        r'''import argparse, hashlib, json, pathlib
p=argparse.ArgumentParser(); p.add_argument('--request'); p.add_argument('--response'); p.add_argument('--scratch'); p.add_argument('--durable'); p.add_argument('--mode', default='ok'); a=p.parse_args()
req=json.loads(pathlib.Path(a.request).read_text())
scratch=pathlib.Path(a.scratch); durable=pathlib.Path(a.durable); scratch.mkdir(parents=True,exist_ok=True); durable.mkdir(parents=True,exist_ok=True)
payload=req['request'] or {}
if a.mode == 'fail': raise SystemExit(9)
expected=payload.get('semantic_hash') or hashlib.sha256((req['universe_id']+'|'+req['operation_id']).encode()).hexdigest()
if a.mode == 'mismatch': expected='0'*64
if req['action'] in {'REBUILD','INVALIDATE_SOURCE','INVALIDATE_AUTHORITY'}:
    (durable/'state.bin').write_bytes((req['action']+'|'+req['step_id']).encode())
if req['action'] == 'REPLAY':
    (scratch/'replay.tmp').write_bytes(b'x'*17)
tele={'source_open_count':1,'source_decode_count':1,'bytes_read':11,'bytes_written':7,'temporary_spill_bytes':17,'cache_index_bytes_created':5,'rewritten_bytes':13}
if a.mode == 'no-telemetry': tele={}
out={'status':'OK','semantic_output_sha256':expected,'telemetry':tele,'identities':{'deterministic_output_identity':payload.get('identity','ID'),'learned_product_release_identity':payload.get('release','REL'),'learned_product_replay_identity':payload.get('replay','REP')}}
pathlib.Path(a.response).write_text(json.dumps(out, sort_keys=True))
''',
        encoding="utf-8",
    )
    return p


def candidates(adapter: Path, modes=None):
    modes = modes or {"A": "ok", "B": "ok", "C": "ok"}
    return {
        c: {"argv": [sys.executable, str(adapter), "--request", "{request}", "--response", "{response}", "--scratch", "{scratch}", "--durable", "{durable}", "--mode", modes[c]]}
        for c in "ABC"
    }


def step(step_id, universe, operation, phase="cold", action="EXECUTE", *, eligible=True, hostile=None, identity="ID"):
    semantic = h(universe + "|" + operation)
    row = {
        "step_id": step_id,
        "universe_id": universe,
        "operation_id": operation,
        "ee_requirement_ids": ["EE01", "EE16"],
        "phase": phase,
        "action": action,
        "eligibility": {"state": "ELIGIBLE" if eligible else "MISSING_AUTHORITY", "exact_basis": "TEST_FROZEN_AUTHORITY"},
    }
    if eligible and action not in {"DELETE_DURABLE", "DELETE_SCRATCH", "RESET_CANDIDATE_STATE"}:
        row["request"] = {"semantic_hash": semantic, "identity": identity, "release": "REL", "replay": "REP"}
        row["oracle"] = {"semantic_output_sha256": semantic, "identities": {"deterministic_output_identity": identity}}
    if hostile:
        row["hostile_case_id"] = hostile
    return row


def manifest(steps):
    return {"schema": WORKLOAD_SCHEMA, "workload_id": "EEW1.TEST", "steps": steps}


def test_equal_work_ineligible_not_failure_and_no_universe_pooling(tmp_path):
    adapter = write_adapter(tmp_path)
    m = manifest([
        step("s1", "U1", "op1", "cold"),
        step("s2", "U2", "op2", "warm_1"),
        step("s3", "U2", "op3", eligible=False),
    ])
    r = execute_harness(m, candidates(adapter), tmp_path / "run")
    assert r["exact_same_step_order_all_candidates"]
    assert r["candidate_neutral_request_payloads"]
    for c in "ABC":
        assert r["candidate_summary"][c]["eligible_steps"] == 2
        assert r["candidate_summary"][c]["ineligible_steps"] == 1
        assert r["candidate_summary"][c]["candidate_or_oracle_failures"] == 0
        assert r["candidate_summary"][c]["performance_eligible"]
    assert sum(x["outcome"] == "INELIGIBLE_MISSING_AUTHORITY" for x in r["records"]) == 3
    assert all("|U1|" in k or "|U2|" in k for k in r["metric_groups"])
    assert all(v["note"] == "NO_CROSS_UNIVERSE_AGGREGATION" for v in r["metric_groups"].values())


def test_semantic_mismatch_fails_regardless_of_speed(tmp_path):
    adapter = write_adapter(tmp_path)
    r = execute_harness(manifest([step("s1", "U", "op")]), candidates(adapter, {"A":"ok","B":"mismatch","C":"ok"}), tmp_path/"run")
    assert r["candidate_summary"]["B"]["performance_eligible"] is False
    b = next(x for x in r["records"] if x["candidate_id"] == "B")
    assert b["outcome"] == "SEMANTIC_ORACLE_MISMATCH"
    assert b["semantic_oracle_status"] == "FAIL"


def test_candidate_order_does_not_change_logical_receipt(tmp_path):
    adapter = write_adapter(tmp_path)
    m = manifest([step("s1", "U", "op", hostile="H03_EQUAL_MARGINALS_DIFFERENT_KWAY_JOINT")])
    r1 = execute_harness(m, candidates(adapter), tmp_path/"r1", candidate_order=("A","B","C"))
    r2 = execute_harness(m, candidates(adapter), tmp_path/"r2", candidate_order=("C","A","B"))
    assert r1["logical_receipt_sha256"] == r2["logical_receipt_sha256"]


def test_repeat_delete_rebuild_invalidate_replay_preserve_declared_order_and_identity(tmp_path):
    adapter = write_adapter(tmp_path)
    m = manifest([
        step("cold", "U", "build", "cold", "REBUILD", identity="STATE"),
        step("warm1", "U", "query", "warm_1", identity="STATE"),
        step("warm2", "U", "query", "warm_2", identity="STATE"),
        step("warm5", "U", "query", "warm_5", identity="STATE"),
        step("del", "U", "delete", "delete_rebuild", "DELETE_DURABLE"),
        step("rebuild", "U", "build", "delete_rebuild", "REBUILD", identity="STATE"),
        step("srcinv", "U", "source_refresh", "selective_source_invalidation", "INVALIDATE_SOURCE", identity="STATE"),
        step("authinv", "U", "authority_refresh", "selective_authority_invalidation", "INVALIDATE_AUTHORITY", identity="STATE"),
        step("replay", "U", "audit", "replay", "REPLAY", identity="STATE"),
    ])
    r = execute_harness(m, candidates(adapter), tmp_path/"run")
    order = [x["step_id"] for x in r["records"] if x["candidate_id"] == "A"]
    assert order == [x["step_id"] for x in m["steps"]]
    assert all(x["identity_oracle_status"] in {"PASS","NOT_REQUESTED"} for x in r["records"] if x["eligibility_state"] == "ELIGIBLE")
    assert all(r["candidate_summary"][c]["performance_eligible"] for c in "ABC")


def test_omitted_or_incomplete_work_cannot_score_as_win(tmp_path):
    adapter = write_adapter(tmp_path)
    m = manifest([step("s1", "U", "op")])
    r = execute_harness(m, candidates(adapter, {"A":"ok","B":"fail","C":"no-telemetry"}), tmp_path/"run")
    assert r["candidate_summary"]["A"]["performance_eligible"]
    assert not r["candidate_summary"]["B"]["performance_eligible"]
    assert not r["candidate_summary"]["C"]["performance_eligible"]
    assert {x["outcome"] for x in r["records"] if x["candidate_id"] in {"B","C"}} == {"CANDIDATE_NONZERO_EXIT", "MEASUREMENT_TELEMETRY_INCOMPLETE"}


def test_all_frozen_hostile_ids_are_supported():
    assert len(HOSTILE_CASE_IDS) == 20
    assert "H14_RANKED_MULTISELECT_TOPOLOGY" in HOSTILE_CASE_IDS
    assert "H17_MISSING_SEMANTIC_ROUTING_AUTHORITY" in HOSTILE_CASE_IDS
    assert "H20_SELECTIVE_INVALIDATION_EXACT_DETERMINANT_CHANGE" in HOSTILE_CASE_IDS
