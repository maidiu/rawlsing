from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW = REPO_ROOT / ".local-logs" / "pyat-l03-c4" / "phase2"
RESULTS = RETURN_DIR / "results"


def load(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def median(values):
    return statistics.median(values) if values else None


def summarize_main(payload):
    n = payload["n"]
    cold = payload["cold"]
    rounds = payload["warm_rounds"]
    per_op = {}
    for op_id in cold["baseline"]["ops"]:
        base = [round_data["baseline"]["ops"][op_id]["wall_s"] for round_data in rounds]
        cand = [round_data["candidate"]["ops"][op_id]["wall_s"] for round_data in rounds]
        base_med = median(base)
        cand_med = median(cand)
        per_op[op_id] = {
            "baseline_wall_med_s": base_med,
            "candidate_wall_med_s": cand_med,
            "speedup": (base_med / cand_med) if cand_med else None,
            "baseline_cpu_med_s": median([
                round_data["baseline"]["ops"][op_id]["cpu_s"] for round_data in rounds
            ]),
            "candidate_cpu_med_s": median([
                round_data["candidate"]["ops"][op_id]["cpu_s"] for round_data in rounds
            ]),
        }
    base_med = median([round_data["baseline"]["wall_s"] for round_data in rounds])
    cand_med = median([round_data["candidate"]["wall_s"] for round_data in rounds])
    single = payload["single_operation"]
    single_base = next(iter(single["baseline"].values()))["wall_s"]
    single_cand = next(iter(single["candidate"].values()))["wall_s"]
    incompatible = payload["incompatible"]
    inc_base = incompatible["first_pass"]["baseline"]["wall_s"]
    inc_cand = incompatible["first_pass"]["candidate"]["wall_s"]
    return {
        "n": n,
        "rounds": payload["rounds"],
        "fixture_build_s": payload["timings"]["fixture_build_s"],
        "cold": {
            "baseline_wall_s": cold["baseline"]["wall_s"],
            "candidate_wall_s": cold["candidate"]["wall_s"],
            "candidate_delta_pct": (cold["candidate"]["wall_s"] / cold["baseline"]["wall_s"] - 1) * 100,
            "all_facts_equal": cold["all_facts_equal"],
            "scope": cold["scope"],
        },
        "warm": {
            "baseline_wall_median_s": base_med,
            "candidate_wall_median_s": cand_med,
            "speedup": base_med / cand_med,
            "all_rounds_facts_equal": all(round_data["all_facts_equal"] for round_data in rounds),
            "rounds": [
                {
                    "round": round_data["round"],
                    "baseline_wall_s": round_data["baseline"]["wall_s"],
                    "candidate_wall_s": round_data["candidate"]["wall_s"],
                    "baseline_cpu_s": round_data["baseline"]["cpu_s"],
                    "candidate_cpu_s": round_data["candidate"]["cpu_s"],
                    "scope": round_data["scope"],
                }
                for round_data in rounds
            ],
        },
        "single_operation": {
            "op_id": single["op_id"],
            "baseline_wall_s": single_base,
            "candidate_wall_s": single_cand,
            "candidate_delta_pct": (single_cand / single_base - 1) * 100,
            "all_facts_equal": single["all_facts_equal"],
            "scope": single["scope"],
        },
        "incompatible_first_pass": {
            "op_ids": incompatible["op_ids"],
            "baseline_wall_s": inc_base,
            "candidate_wall_s": inc_cand,
            "candidate_delta_pct": (inc_cand / inc_base - 1) * 100,
            "all_facts_equal": incompatible["first_pass"]["all_facts_equal"],
            "scope": incompatible["first_pass"]["scope"],
        },
        "counters": payload["counters"],
        "per_op": per_op,
        "source": payload["source"],
        "process": payload["process"],
    }


def main():
    summaries = {}
    for n in (200, 1000, 3000):
        path = RAW / f"main_n{n}.json"
        if path.exists():
            summaries[str(n)] = summarize_main(load(path))
    small = load(RAW / "small_fixtures.json") if (RAW / "small_fixtures.json").exists() else None

    cost_path = RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl"
    parity_path = RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl"
    with cost_path.open("a", encoding="utf-8") as cost, parity_path.open("a", encoding="utf-8") as parity:
        for n, summary in sorted(summaries.items()):
            jsonline(cost, {
                "schema": "PYAT_L03_C4_PHASE2_COST@1",
                "entry_kind": "phase2_process",
                "n": int(n),
                "fixture_build_s": summary["fixture_build_s"],
                "cold": summary["cold"],
                "warm": summary["warm"],
                "single_operation": summary["single_operation"],
                "incompatible_first_pass": summary["incompatible_first_pass"],
                "counters": summary["counters"],
                "source": summary["source"],
                "process": summary["process"],
            })
            for op_id, row in summary["per_op"].items():
                jsonline(cost, {
                    "schema": "PYAT_L03_C4_PHASE2_COST@1",
                    "entry_kind": "phase2_op_paired",
                    "n": int(n),
                    "op_id": op_id,
                    **row,
                })
            raw = load(RAW / f"main_n{n}.json")
            for pass_name, pass_data in (
                ("cold", raw["cold"]),
                ("single_operation", raw["single_operation"]),
                ("incompatible_first_pass", raw["incompatible"]["first_pass"]),
                ("incompatible_second_pass", raw["incompatible"]["second_pass"]),
            ):
                if pass_name == "cold":
                    baseline = pass_data["baseline"]
                    candidate = pass_data["candidate"]
                    scope = pass_data["scope"]
                    equal = pass_data["all_facts_equal"]
                elif pass_name == "single_operation":
                    baseline = next(iter(pass_data["baseline"].values()))
                    candidate = next(iter(pass_data["candidate"].values()))
                    scope = pass_data["scope"]
                    equal = pass_data["all_facts_equal"]
                else:
                    baseline = pass_data["baseline"]
                    candidate = pass_data["candidate"]
                    scope = pass_data["scope"]
                    equal = pass_data["all_facts_equal"]
                jsonline(parity, {
                    "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                    "entry_kind": "phase2_pass_parity",
                    "n": int(n),
                    "pass": pass_name,
                    "all_facts_equal": equal,
                    "scope": scope,
                })
            for op_id in raw["cold"]["baseline"]["ops"]:
                base = raw["cold"]["baseline"]["ops"][op_id]
                cand = raw["cold"]["candidate"]["ops"][op_id]
                jsonline(parity, {
                    "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                    "entry_kind": "phase2_op_exact_parity",
                    "n": int(n),
                    "op_id": op_id,
                    "exact_fact_material_equal":
                        base["exact_fact_material_sha256"] == cand["exact_fact_material_sha256"],
                    "fact_refs_equal": base["fact_refs"] == cand["fact_refs"],
                    "replay_refs_equal": base["replay_refs"] == cand["replay_refs"],
                    "baseline_facts": base["facts"],
                    "candidate_facts": cand["facts"],
                })
            for op_id, selected in raw["selected_full_facts"].items():
                if int(n) == 200:
                    jsonline(parity, {
                        "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                        "entry_kind": "phase2_selected_full_fact_parity",
                        "n": int(n),
                        "op_id": op_id,
                        "equal": selected["equal"],
                        "baseline_full_facts": selected["baseline"],
                        "candidate_full_facts": selected["candidate"],
                    })
                else:
                    jsonline(parity, {
                        "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                        "entry_kind": "phase2_selected_full_fact_digest",
                        "n": int(n),
                        "op_id": op_id,
                        "equal": selected["equal"],
                        "baseline_full_fact_sha256": __import__("hashlib").sha256(
                            json.dumps(selected["baseline"], sort_keys=True, separators=(",", ":")).encode()
                        ).hexdigest(),
                        "candidate_full_fact_sha256": __import__("hashlib").sha256(
                            json.dumps(selected["candidate"], sort_keys=True, separators=(",", ":")).encode()
                        ).hexdigest(),
                        "raw_full_material": str(
                            (RAW / f"main_n{n}.json").relative_to(REPO_ROOT)
                        ),
                    })

        if small is not None:
            for entry in small["entries"]:
                jsonline(parity, {
                    "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                    "entry_kind": "phase2_small_fixture",
                    **entry,
                })
            jsonline(parity, {
                "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
                "entry_kind": "phase2_not_administered_limitation",
                "statement": small["not_administered_contract"],
            })

        jsonline(cost, {
            "schema": "PYAT_L03_C4_PHASE2_COST@1",
            "entry_kind": "phase2_implementation_status",
            "P2_execution_local_grouped_AND_risk_target": "IMPLEMENTED",
            "P3_bitmap_or_posting_index": "NOT_IMPLEMENTED_NOT_WARRANTED",
            "P4_new_persistent_engine": "NOT_IMPLEMENTED_NOT_WARRANTED",
            "production_scope": [
                "rawlsing_next/_pre553_query_eval.py",
                "rawlsing_next/pre553_empirical_query.py",
                "rawlsing_next/pre553_carrier_execution.py",
                "rawlsing_next/pre553_discovery_exact.py",
                "rawlsing_next/pre553_issued_workload.py",
            ],
            "select_respondent_events_abi": "v1 unchanged",
            "cache_default_policy_changed": False,
            "original35_or_native_claim": False,
        })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_PHASE2_PARITY@1",
            "entry_kind": "phase2_grouped_status",
            "P2": "IMPLEMENTED_AND_MEASURED",
            "P3": "NOT_IMPLEMENTED_NOT_WARRANTED",
            "P4": "NOT_IMPLEMENTED_NOT_WARRANTED",
            "native_fact_per_operation": True,
            "replay_per_operation": True,
            "cross_scope_sharing": "NONE",
        })

    summary = {
        "schema": "PYAT_L03_C4_PHASE2_SUMMARY@1",
        "implementation": "execution-local compatible grouped AND-risk/target core reuse",
        "measurements": summaries,
        "small_fixtures": small,
        "raw_path": str(RAW.relative_to(REPO_ROOT)),
    }
    (RESULTS / "phase2_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "summary": str(RESULTS / "phase2_summary.json"),
        "n_values": sorted(summaries, key=int),
        "cost_size": cost_path.stat().st_size,
        "parity_size": parity_path.stat().st_size,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
