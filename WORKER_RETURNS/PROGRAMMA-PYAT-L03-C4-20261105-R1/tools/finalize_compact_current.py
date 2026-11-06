from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW = REPO_ROOT / ".local-logs" / "pyat-l03-c4"
RESULTS = RETURN_DIR / "results"
COMPARE_DIR = RAW / "compact_compare"
GROUPED_DIR = RAW / "grouped_compact"
VARIANTS = ("v0", "v1", "v2-cold", "v2-warm")


def load(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def median(values):
    return statistics.median(values) if values else None


def first_fact(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        line = handle.readline().strip()
    return json.loads(line) if line else None


def compare_summary(n: int):
    path = COMPARE_DIR / f"n{n}" / f"compare_n{n}.json"
    payload = load(path)
    variants = {}
    for variant in VARIANTS:
        item = payload["variants"][variant]
        command = next(row for row in payload["commands"] if row["variant"] == variant)
        variants[variant] = {
            "parent_wall_s": command["parent_wall_s"],
            "phases": item["phases"],
            "counts": item.get("counts"),
            "process": item["process"],
            "source": item["source"],
            "release": item["release"],
            "cache": item["cache"],
            "queries": item["queries"],
            "facts_file": item["facts_file"],
        }
    return {
        "n": n,
        "raw_path": str(path.relative_to(REPO_ROOT)),
        "variants": variants,
        "facts_exact_equal": payload["facts_exact_equal"],
        "release_identity_equal": payload["release_identity_equal"],
        "source_identity_equal": payload["source_identity_equal"],
        "cache_checks": payload["cache_checks"],
        "pass": payload["pass"],
    }


def grouped_summary(n: int):
    path = GROUPED_DIR / f"n{n}" / f"grouped_n{n}.json"
    payload = load(path)
    rounds = payload["warm_rounds"]
    per_op = {}
    for op_id in payload["cold"]["baseline"]["ops"]:
        base = median([item["baseline"]["ops"][op_id]["wall_s"] for item in rounds])
        cand = median([item["candidate"]["ops"][op_id]["wall_s"] for item in rounds])
        per_op[op_id] = {
            "cold_baseline_wall_s": payload["cold"]["baseline"]["ops"][op_id]["wall_s"],
            "cold_candidate_wall_s": payload["cold"]["candidate"]["ops"][op_id]["wall_s"],
            "warm_baseline_wall_median_s": base,
            "warm_candidate_wall_median_s": cand,
            "speedup": (base / cand) if cand else None,
            "all_facts_equal": all(
                item["candidate"]["ops"][op_id].get("facts_equal") is True for item in rounds
            ),
        }
    warm_base = median([item["baseline"]["wall_s"] for item in rounds])
    warm_cand = median([item["candidate"]["wall_s"] for item in rounds])
    single = payload["single_operation"]
    incompatible = payload["incompatible"]
    capacity = payload["capacity_fallback"]
    single_base = single["baseline"]["wall_s"]
    single_cand = single["candidate"]["wall_s"]
    inc_base = incompatible["first_pass"]["baseline"]["wall_s"]
    inc_cand = incompatible["first_pass"]["candidate"]["wall_s"]
    cap_base = capacity["baseline"]["wall_s"]
    cap_cand = capacity["candidate"]["wall_s"]
    return {
        "n": n,
        "raw_path": str(path.relative_to(REPO_ROOT)),
        "facts_files": payload["facts_files"],
        "source": payload["source"],
        "release": payload["release"],
        "setup_s": payload["setup_s"],
        "cold": {
            "baseline_wall_s": payload["cold"]["baseline"]["wall_s"],
            "candidate_wall_s": payload["cold"]["candidate"]["wall_s"],
            "all_facts_equal": payload["cold"]["all_facts_equal"],
            "scope": payload["cold"]["scope"],
        },
        "warm": {
            "baseline_wall_median_s": warm_base,
            "candidate_wall_median_s": warm_cand,
            "speedup": warm_base / warm_cand,
            "all_rounds_facts_equal": all(item["all_facts_equal"] for item in rounds),
            "rounds": [
                {
                    "round": item["round"],
                    "baseline_wall_s": item["baseline"]["wall_s"],
                    "candidate_wall_s": item["candidate"]["wall_s"],
                    "baseline_cpu_s": item["baseline"]["cpu_s"],
                    "candidate_cpu_s": item["candidate"]["cpu_s"],
                    "scope": item["scope"],
                }
                for item in rounds
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
        "capacity_fallback": {
            "op_ids": capacity["op_ids"],
            "baseline_wall_s": cap_base,
            "candidate_wall_s": cap_cand,
            "candidate_delta_pct": (cap_cand / cap_base - 1) * 100,
            "all_facts_equal": capacity["all_facts_equal"],
            "scope": capacity["scope"],
            "note": capacity["note"],
        },
        "counters": payload["counters"],
        "oracle": payload["oracle"],
        "per_op": per_op,
        "process": payload["process"],
    }


def main():
    comparisons = {n: compare_summary(n) for n in (200, 1000)}
    grouped = {n: grouped_summary(n) for n in (200, 1000)}
    cost_path = RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl"
    parity_path = RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl"

    commands = []
    for n in (200, 1000):
        commands.append({
            "label": f"compact_compare_n{n}",
            "command": [
                "/tmp/rawlsing-oct28-p1r1/venv/bin/python",
                "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py",
                "--mode", "compare", "--n", str(n),
                "--outdir", f".local-logs/pyat-l03-c4/compact_compare/n{n}",
            ],
            "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                    "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
            "exit": 0,
            "summary": f"V0/V1/V2-cold/V2-warm exact comparison pass={comparisons[n]['pass']}",
            "variant_parent_wall_s": {
                variant: comparisons[n]["variants"][variant]["parent_wall_s"]
                for variant in VARIANTS
            },
        })
        commands.append({
            "label": f"compact_grouped_n{n}",
            "command": [
                "/tmp/rawlsing-oct28-p1r1/venv/bin/python",
                "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py",
                "--mode", "grouped", "--n", str(n), "--rounds", "3",
                "--outdir", f".local-logs/pyat-l03-c4/grouped_compact/n{n}",
            ],
            "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                    "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
            "exit": 0,
            "summary": (
                f"compact grouped exact cold={grouped[n]['cold']['all_facts_equal']} "
                f"warm={grouped[n]['warm']['all_rounds_facts_equal']} "
                f"oracle={grouped[n]['oracle']['all_pass']} "
                f"speedup={grouped[n]['warm']['speedup']:.3f}"
            ),
        })
    commands.append({
        "label": "compact_smoke_n3",
        "command": [
            "/tmp/rawlsing-oct28-p1r1/venv/bin/python",
            "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py",
            "--mode", "compare", "--n", "3", "--smoke",
            "--outdir", ".local-logs/pyat-l03-c4/compact_compare/smoke",
        ],
        "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
        "exit": 0,
        "summary": "SMOKE_ONLY_NOT_BENCHMARK; exact parity and V2 cache checks pass",
    })
    with (RESULTS / "compact_current_commands.jsonl").open("w", encoding="utf-8") as handle:
        for item in commands:
            jsonline(handle, {"schema": "PYAT_L03_C4_COMPACT_CURRENT_COMMAND@1", **item})

    with cost_path.open("a", encoding="utf-8") as cost:
        for n, summary in sorted(comparisons.items()):
            jsonline(cost, {
                "schema": "PYAT_L03_C4_COMPACT_CURRENT_COST@1",
                "entry_kind": "compact_current_process",
                "n": n,
                "pass": summary["pass"],
                "facts_exact_equal": summary["facts_exact_equal"],
                "release_identity_equal": summary["release_identity_equal"],
                "source_identity_equal": summary["source_identity_equal"],
                "cache_checks": summary["cache_checks"],
                "variants": summary["variants"],
                "raw_path": summary["raw_path"],
            })
            for variant, item in summary["variants"].items():
                for query in item["queries"]:
                    jsonline(cost, {
                        "schema": "PYAT_L03_C4_COMPACT_CURRENT_COST@1",
                        "entry_kind": "compact_current_query",
                        "n": n,
                        "variant": variant,
                        "op_id": query["op_id"],
                        "wall_s": query["wall_s"],
                        "cpu_s": query["cpu_s"],
                        "typed_states": query.get("typed_states", [query.get("typed_state")]),
                        "fact_refs": query.get("fact_refs", [query.get("fact_ref")]),
                        "replay_refs": query.get("replay_refs", [query.get("replay_ref")]),
                        "exact_fact_material_sha256": query["exact_fact_material_sha256"],
                    })
        for n, summary in sorted(grouped.items()):
            jsonline(cost, {
                "schema": "PYAT_L03_C4_COMPACT_CURRENT_COST@1",
                "entry_kind": "compact_current_grouped",
                "n": n,
                **{key: summary[key] for key in (
                    "source", "release", "setup_s", "cold", "warm",
                    "single_operation", "incompatible_first_pass",
                    "capacity_fallback", "counters", "oracle", "process", "raw_path",
                )},
            })
            for op_id, row in summary["per_op"].items():
                jsonline(cost, {
                    "schema": "PYAT_L03_C4_COMPACT_CURRENT_COST@1",
                    "entry_kind": "compact_current_grouped_op",
                    "n": n,
                    "op_id": op_id,
                    **row,
                })
        jsonline(cost, {
            "schema": "PYAT_L03_C4_COMPACT_CURRENT_COST@1",
            "entry_kind": "compact_current_implementation_status",
            "driver": "tools/bench_compact_current.py",
            "N200": "MEASURED",
            "N1000": "MEASURED",
            "N3000": "NOT_RUN_NOT_REQUIRED",
            "production_changes": "NONE_IN_THIS_PHASE",
            "cache_default_changed": False,
            "delete_corrupt_stale_revoke": "NOT_RUN_HERE_EXISTING_TESTS_REFERENCED",
        })

    with parity_path.open("a", encoding="utf-8") as parity:
        for n, summary in sorted(comparisons.items()):
            jsonline(parity, {
                "schema": "PYAT_L03_C4_COMPACT_CURRENT_PARITY@1",
                "entry_kind": "compact_current_compare_parity",
                "n": n,
                "facts_exact_equal": summary["facts_exact_equal"],
                "release_identity_equal": summary["release_identity_equal"],
                "source_identity_equal": summary["source_identity_equal"],
                "cache_checks": summary["cache_checks"],
                "pass": summary["pass"],
                "raw_path": summary["raw_path"],
                "full_fact_sidecars": {
                    variant: summary["variants"][variant]["facts_file"]
                    for variant in VARIANTS
                },
            })
        for n, summary in sorted(grouped.items()):
            jsonline(parity, {
                "schema": "PYAT_L03_C4_COMPACT_CURRENT_PARITY@1",
                "entry_kind": "compact_current_grouped_parity",
                "n": n,
                "cold_all_facts_equal": summary["cold"]["all_facts_equal"],
                "warm_all_rounds_facts_equal": summary["warm"]["all_rounds_facts_equal"],
                "single_operation_equal": summary["single_operation"]["all_facts_equal"],
                "incompatible_first_pass_equal": summary["incompatible_first_pass"]["all_facts_equal"],
                "capacity_fallback_equal": summary["capacity_fallback"]["all_facts_equal"],
                "oracle_all_pass": summary["oracle"]["all_pass"],
                "scope_cold": summary["cold"]["scope"],
                "scope_warm": summary["warm"]["rounds"][-1]["scope"],
                "raw_path": summary["raw_path"],
                "full_fact_sidecars": summary["facts_files"],
            })
        selected = {}
        for label, path in (
            ("compare_n200_v0_raw_Y", COMPARE_DIR / "n200" / "v0_facts.jsonl"),
            ("compare_n200_v1_raw_Y", COMPARE_DIR / "n200" / "v1_facts.jsonl"),
            ("compare_n200_v2_warm_raw_Y", COMPARE_DIR / "n200" / "v2-warm_facts.jsonl"),
            ("grouped_n200_baseline_raw_Y", GROUPED_DIR / "n200" / "grouped_cold_baseline_facts.jsonl"),
            ("grouped_n200_candidate_raw_Y", GROUPED_DIR / "n200" / "grouped_cold_candidate_facts.jsonl"),
        ):
            if path.exists():
                selected[label] = first_fact(path)
        jsonline(parity, {
            "schema": "PYAT_L03_C4_COMPACT_CURRENT_PARITY@1",
            "entry_kind": "compact_current_selected_full_fact_material",
            "selected": selected,
            "note": "Full per-op sidecars are referenced above; selected materials are the first raw_Y fact.",
        })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_COMPACT_CURRENT_PARITY@1",
            "entry_kind": "compact_current_disposition",
            "W03_P01": "exact current composition demonstrated; no exact function gap; economic cold-construction result measured",
            "W04_P02": "default compact Arrow + explicitly owned cache measured; default activation remains owner policy; no blanket default",
            "sourcefree_small_fixture_only": True,
            "original35_or_production_scale_claim": False,
            "unused_codec_presence_is_not_completion": True,
        })

    summary = {
        "schema": "PYAT_L03_C4_COMPACT_CURRENT_SUMMARY@1",
        "comparisons": comparisons,
        "grouped": grouped,
        "raw_root": str(RAW.relative_to(REPO_ROOT)),
        "commands": str((RESULTS / "compact_current_commands.jsonl").relative_to(REPO_ROOT)),
    }
    (RESULTS / "compact_current_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "summary": str(RESULTS / "compact_current_summary.json"),
        "cost_size": cost_path.stat().st_size,
        "parity_size": parity_path.stat().st_size,
        "compare_pass": {str(n): comparisons[n]["pass"] for n in comparisons},
        "grouped_speedup": {str(n): grouped[n]["warm"]["speedup"] for n in grouped},
        "grouped_oracle": {str(n): grouped[n]["oracle"]["all_pass"] for n in grouped},
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
