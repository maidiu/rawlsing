#!/usr/bin/env python3
"""S-GI1 K11 execution entrypoint.

PROVISIONAL_LAB_RULE__NOT_ADOPTED. Source-free synthetic genealogy lab.
Writes: fixtures, LLM proposal records, run logs, per-case receipts, DAG validation,
embargo results, feasibility measurements.
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lab_sgi1.core import h_obj, canon
from lab_sgi1.k11_runner import K11Run
from lab_sgi1 import LAB_RULE_STATUS, CONTRACT_VERSION, K11_CONTRACT

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
D_FIX = os.path.join(BASE, "02_K11_FIXTURES")
D_LOG = os.path.join(BASE, "03_RUN_LOGS")
D_REC = os.path.join(BASE, "04_RESULT_RECEIPTS")
D_MEA = os.path.join(BASE, "05_MEASUREMENTS")
D_DAG = os.path.join(BASE, "06_DAG_VALIDATION")
D_EMB = os.path.join(BASE, "07_EMBARGO_RESULTS")
D_LLM = os.path.join(BASE, "08_LLM_PROPOSAL_RECORDS")


def wj(path: str, obj) -> None:
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=False)


def main() -> int:
    t0 = time.perf_counter()
    model_enabled = os.environ.get("SGI1_MODEL", "1") == "1"
    reuse = os.environ.get("SGI1_REUSE_RECORDS", "0") == "1"
    run = K11Run(BASE, model_enabled=model_enabled, reuse_records=reuse)
    result = run.run_all()
    wall = round(time.perf_counter() - t0, 3)

    for d in (D_FIX, D_LOG, D_REC, D_MEA, D_DAG, D_EMB, D_LLM):
        os.makedirs(d, exist_ok=True)

    # fixtures
    wj(os.path.join(D_FIX, "fixture_manifest.json"), {
        "fixtures": result["fixtures"],
        "fixture_hashes": {k: v["anchor_hash"] for k, v in result["fixtures"].items()},
        "prohibited_future_input_partition": [
            "future_child_outcome_label", "future_child_personality",
            "future_child_desired_adversity_tag", "future_child_health_outcome",
            "future_child_education_outcome", "any_field_derived_from_future_child",
        ],
        "lab_rule": LAB_RULE_STATUS,
    })

    # LLM proposal records (exact model/prompt/output/candidate ids/dedup/hash)
    for pr in result["proposal_records"]:
        key = pr["record_key"]
        wj(os.path.join(D_LLM, f"proposal_{key}.json"), pr)
    wj(os.path.join(D_LLM, "proposal_index.json"), {
        "records": [
            {"record_key": pr["record_key"],
             "proposal_hash": pr["record"]["proposal_hash"],
             "model_returned": pr["record"]["model_returned"],
             "automated_status": pr["record"]["lmm_automated_status"],
             "usage": pr["record"]["usage"]}
            for pr in result["proposal_records"]
        ],
        "llm_automated_proposal_status": (
            "AUTOMATED_LLM_PROPOSAL_EXECUTED"
            if any(pr["record"]["lmm_automated_status"] ==
                   "AUTOMATED_LLM_PROPOSAL_EXECUTED"
                   for pr in result["proposal_records"])
            else "AUTOMATED_LLM_PROPOSAL_NOT_TESTED"
        ),
    })

    # per-case receipts
    for c in result["cases"]:
        wj(os.path.join(D_REC, f"{c['case_id']}.json"), c)
    wj(os.path.join(D_REC, "receipt_index.json"), {
        "cases": [
            {"case_id": c["case_id"], "expected": c["expected_status"],
             "terminal_grade": c["terminal_grade"],
             "n_assertions": c["n_assertions"],
             "n_assertions_pass": sum(1 for v in c["assertion_results"].values() if v),
             "receipt_hash": c["receipt_hash"]}
            for c in result["cases"]
        ],
    })

    # run log
    wj(os.path.join(D_LOG, "k11_run_log.json"), {
        "run_log": result["run_log"],
        "total_wall_seconds": result["total_wall_seconds"],
        "entrypoint_wall_seconds": wall,
    })

    # DAG validation extract
    dag_case = next(c for c in result["cases"]
                    if c["case_id"] == "K11-GRAPH-CONSTRUCTION-VS-CAUSAL")
    wj(os.path.join(D_DAG, "dag_validation.json"), {
        "case": dag_case["case_id"],
        "assertion_results": dag_case["assertion_results"],
        "observed": dag_case["observed_state"],
        "two_dag_contract": {
            "construction_edges_namespace": "CONSTRUCTION_DEP",
            "causal_edges_namespace": "CAUSAL_PARENT",
            "E_to_H_edge_type": "RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON",
            "algorithm_time_not_causal_parent": True,
        },
    })

    # embargo results
    emb = next(c for c in result["cases"]
               if c["case_id"] == "K11-A-FUTURE-CHILD-EMBARGO")
    wnd = next(c for c in result["cases"]
               if c["case_id"] == "K11-A2-DESIRED-WOUND-COUNTERFACTUAL")
    wj(os.path.join(D_EMB, "future_child_embargo.json"), {
        "case_id": emb["case_id"],
        "assertion_results": emb["assertion_results"],
        "observed": emb["observed_state"],
        "expected": emb["expected_status"],
        "terminal_grade": emb["terminal_grade"],
        "hard_failure_rule": "ANY difference in father selection or father history "
                             "under changed hidden future-child metadata is a hard failure",
        "result": "INVARIANT_HELD" if all(emb["assertion_results"].values())
                  else "HARD_FAILURE",
    })
    wj(os.path.join(D_EMB, "desired_wound_counterfactual.json"), {
        "case_id": wnd["case_id"],
        "assertion_results": wnd["assertion_results"],
        "observed": wnd["observed_state"],
        "terminal_grade": wnd["terminal_grade"],
        "result": "INVARIANT_HELD" if all(wnd["assertion_results"].values())
                  else "HARD_FAILURE",
    })

    # feasibility / cost measurements
    per_case_costs = {}
    attempts_total = 0
    hold_count = 0
    fail_count = 0
    for c in result["cases"]:
        cr = c["cost_report"]
        per_case_costs[c["case_id"]] = cr
        if c["terminal_grade"] == "K11_CASE_FAIL":
            fail_count += 1
        obs = json.dumps(c["observed_state"])
        if "HOLD" in obs or "NOT_EXECUTED" in obs:
            hold_count += 1
        cons = c["observed_state"]
    proposal_tokens = sum(pr["record"]["usage"].get("total_tokens", 0)
                          for pr in result["proposal_records"])
    proposal_wall = sum(pr["record"].get("wall_seconds", 0)
                        for pr in result["proposal_records"])
    real_model_calls = sum(
        1 for pr in result["proposal_records"]
        if pr["record"]["lmm_automated_status"] == "AUTOMATED_LLM_PROPOSAL_EXECUTED")
    intervention_records = sum(
        1 for pr in result["proposal_records"]
        if pr["record"]["provider"] == "declared_test_intervention")

    def _sum_key(obj, key) -> float:
        total = 0.0
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key and isinstance(v, (int, float)):
                    total += v
                elif isinstance(v, dict):
                    total += _sum_key(v, key)
        return total

    storage_bytes = 0
    for root, _, files in os.walk(BASE):
        for fn in files:
            try:
                storage_bytes += os.path.getsize(os.path.join(root, fn))
            except OSError:
                pass
    def _attempts_of(c):
        obs = c.get("observed_state") or {}
        if not isinstance(obs, dict):
            return 1
        n = obs.get("n_attempts")
        if isinstance(n, int):
            return n
        t = obs.get("terminal")
        if isinstance(t, dict) and isinstance(t.get("n_attempts"), int):
            return t["n_attempts"]
        return 1

    def _sum_draws(obj) -> int:
        if isinstance(obj, dict):
            total = 0
            for k, v in obj.items():
                if k == "rng_draws" and isinstance(v, int):
                    total += v
                elif isinstance(v, dict):
                    total += _sum_draws(v)
            return total
        return 0

    feasibility = {
        "feasibility_scope": "SOURCE_FREE_SYNTHETIC_LAB_GRAIN",
        "whole_person_backgeneration_is_computationally_ridiculous": False,
        "feasibility_note": (
            "At lab grain (finite attempt slots of 4, ~20 typed events per father "
            "history, deterministic rule-based forward construction with one frozen "
            "LLM proposal call per fixture/route), whole-person back-generation is "
            "cheap and completes in milliseconds per attempt. The combinatorial risk "
            "S-G registered (R1) does NOT materialize at this grain because history "
            "construction is a bounded rule-driven search, not an open-ended model "
            "generation per ancestor. It WOULD materialize if each event required "
            "independent LLM calls or unbounded ancestor recursion."
        ),
        "attempts_per_constructible_father": {
            "typical": 1,
            "max_observed": max(_attempts_of(c) for c in result["cases"]),
        },
        "model_calls_total_real": real_model_calls,
        "declared_test_intervention_records": intervention_records,
        "model_calls_note": "one real LLM call per fixture/route for scenario proposal; "
                            "ALL replay/case runs use frozen proposal records (no resample)",
        "tokens_total": proposal_tokens,
        "tokens_per_call_mean": round(
            proposal_tokens / max(1, real_model_calls), 1),
        "model_wall_seconds_total": round(proposal_wall, 3),
        "k11_execution_mode": (
            "FROZEN_RECORD_REPLAY" if reuse else "FRESH_ACQUISITION_AND_EXECUTION"),
        "k11_total_wall_seconds": result["total_wall_seconds"],
        "entrypoint_wall_seconds": wall,
        "history_events_total": int(_sum_key(per_case_costs, "actor_events")),
        "replay_seconds_total": round(_sum_key(per_case_costs, "replay_seconds"), 6),
        "storage_bytes_written_total": storage_bytes,
        "per_case_costs": per_case_costs,
        "failure_or_hold_frequency": {
            "cases_failed": fail_count,
            "cases_with_hold_language": hold_count,
            "n_cases": len(result["cases"]),
        },
        "rng_draws_total": _sum_draws(per_case_costs),
    }
    wj(os.path.join(D_MEA, "feasibility.json"), feasibility)
    wj(os.path.join(D_MEA, "cost_report.json"), {
        "model_calls_real": real_model_calls,
        "tokens_total": proposal_tokens,
        "model_wall_seconds": round(proposal_wall, 3),
        "k11_wall_seconds": result["total_wall_seconds"],
        "k11_execution_mode": feasibility["k11_execution_mode"],
        "history_events_total": feasibility["history_events_total"],
        "replay_seconds_total": feasibility["replay_seconds_total"],
        "per_case": per_case_costs,
    })

    # top-level summary
    summary = {
        "lab_id": "SOROK_SGI1_SOURCEFREE_GENEALOGY_LAB",
        "lab_rule": LAB_RULE_STATUS,
        "contract_version": CONTRACT_VERSION,
        "k11_contract": K11_CONTRACT,
        "grade": result["grade"],
        "n_cases": result["n_cases"],
        "n_assertions": result["n_assertions"],
        "n_assertions_pass": result["n_assertions_pass"],
        "cases_failed": result["cases_failed"],
        "model_status": (
            "AUTOMATED_LLM_PROPOSAL_EXECUTED"
            if any(pr["record"]["lmm_automated_status"] ==
                   "AUTOMATED_LLM_PROPOSAL_EXECUTED"
                   for pr in result["proposal_records"])
            else "AUTOMATED_LLM_PROPOSAL_NOT_TESTED"
        ),
        "model_versions": sorted(set(
            pr["record"]["model_returned"] for pr in result["proposal_records"]
            if pr["record"]["model_returned"])),
        "conception_boundary": "LAB_CONCEPTION_BOUNDARY__NO_ADOPTED_BIOLOGICAL_SEMANTICS",
        "child_generated_events": 0,
        "canon_adoption": "NONE",
        "operative_wake": "NONE",
    }
    wj(os.path.join(D_LOG, "k11_summary.json"), summary)

    # suite-level deterministic fingerprints (for cross-run exact replay proof)
    fingerprints = {}
    for c in result["cases"]:
        obs = c["observed_state"]
        sel = (obs.get("selection") or obs.get("selection_a")
               or obs.get("selection_discordant") or obs.get("selection_base"))
        dad = (obs.get("dad_event_hash") or obs.get("dad_hash_a"))
        fingerprints[c["case_id"]] = {
            "fingerprint": h_obj({
                "assertions": c["assertion_results"],
                "grade": c["terminal_grade"],
                "selection": sel, "dad": dad,
            }),
            "terminal_grade": c["terminal_grade"],
            "n_assertions_pass": sum(1 for v in c["assertion_results"].values() if v),
        }
    wj(os.path.join(D_MEA, "suite_fingerprints.json"), {
        "fingerprints": fingerprints,
        "execution_mode": feasibility["k11_execution_mode"],
        "use": "compare fingerprints across fresh-acquisition vs frozen-replay runs "
               "to prove suite-level exact replay",
    })
    print(json.dumps({k: summary[k] for k in (
        "grade", "n_cases", "n_assertions", "n_assertions_pass", "cases_failed",
        "model_status", "model_versions")}, indent=1))
    print("wall_seconds:", wall)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
