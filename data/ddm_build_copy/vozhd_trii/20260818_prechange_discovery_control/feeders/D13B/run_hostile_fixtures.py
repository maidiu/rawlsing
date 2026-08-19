#!/usr/bin/env python3
"""Execute all mandatory D13B hostile fixtures fail-closed."""
from __future__ import annotations
import json
from pathlib import Path
from replay_proof_protocol import compare_datasets, failure_codes, shuffled_physical_copy
from hostile_fixtures import load_fixtures

ROOT = Path(__file__).resolve().parent

def _contains_expected(report, expected):
    available=set(failure_codes(report)) | set(report.get("source_blockers",[])) | set(report.get("replay_blockers",[]))
    return all(code in available for code in expected)

def main() -> int:
    fixtures=load_fixtures()
    rows=[]
    for idx,fx in enumerate(fixtures, start=1):
        source=fx["source"]
        good=shuffled_physical_copy(fx["good_replay"], seed=1000+idx)
        hostile=fx["hostile_replay"]
        good_report=compare_datasets(source,good)
        hostile_report=compare_datasets(source,hostile)
        good_ok=good_report["overall_state"]==fx["expected_good_state"]
        hostile_ok=hostile_report["overall_state"]==fx["expected_hostile_state"]
        code_ok=_contains_expected(hostile_report,fx["expected_failure_or_blocked_states"])
        failed_dimensions=[
            d["name"] for d in hostile_report.get("dimensions",[])
            if d["state"] in {"FAIL","BLOCKED"}
        ]
        row={
            "fixture_id":fx["fixture_id"],
            "fixture_name":fx["fixture_name"],
            "required_case":fx["required_case"],
            "expected_good_state":fx["expected_good_state"],
            "actual_good_state":good_report["overall_state"],
            "expected_hostile_state":fx["expected_hostile_state"],
            "actual_hostile_state":hostile_report["overall_state"],
            "expected_codes":fx["expected_failure_or_blocked_states"],
            "actual_codes":failure_codes(hostile_report),
            "failed_or_blocked_dimensions":failed_dimensions,
            "good_state_match":good_ok,
            "hostile_state_match":hostile_ok,
            "expected_code_match":code_ok,
            "fixture_pass":good_ok and hostile_ok and code_ok,
            "physical_order_permutation_exercised":True,
            "aggregate_equality_trap":fx.get("aggregate_equality_trap",""),
        }
        rows.append(row)
    report={
        "court":"D13B",
        "protocol_version":"D13B-REPLAY-PROOF-CONTRACT-v1",
        "fixture_contract_version":"D13B-HOSTILE-FIXTURES-v1",
        "mandatory_fixture_count":26,
        "executed_fixture_count":len(rows),
        "passed_fixture_count":sum(1 for r in rows if r["fixture_pass"]),
        "failed_fixture_count":sum(1 for r in rows if not r["fixture_pass"]),
        "synthetic_fixture_proof_state":"SYNTHETIC_FIXTURE_PROOF_COMPLETE" if len(rows)==26 and all(r["fixture_pass"] for r in rows) else "SYNTHETIC_FIXTURE_PROOF_FAILED",
        "static_proof_state":"STATIC_PROOF_EXECUTABLE",
        "populated_production_state":"POPULATED_PRODUCTION_PROOF_BLOCKED",
        "source_equivalence_state":"SOURCE_EQUIVALENCE_UNPROVEN",
        "fixtures":rows,
    }
    (ROOT/"SYNTHETIC_FIXTURE_PROOF_REPORT.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:report[k] for k in (
        "executed_fixture_count","passed_fixture_count","failed_fixture_count",
        "synthetic_fixture_proof_state","static_proof_state",
        "populated_production_state","source_equivalence_state")},indent=2))
    return 0 if report["failed_fixture_count"]==0 and report["executed_fixture_count"]==26 else 1

if __name__=="__main__":
    raise SystemExit(main())
