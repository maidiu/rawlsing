from __future__ import annotations

import json
import shutil
import statistics
import sys
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW_REPEATS = REPO_ROOT / ".local-logs" / "pyat-l03-c4" / "repeats"
RAW_RESULTS = REPO_ROOT / ".local-logs" / "pyat-l03-c4" / "raw-results"
RESULTS = RETURN_DIR / "results"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def compact_ref_list(values):
    if not values:
        return values
    first = values[0]
    if isinstance(first, list):
        return values
    return [
        [item.get("object_id"), item.get("content_hash")]
        if isinstance(item, Mapping) else item
        for item in values
    ]


def trim_fact(fact: Mapping[str, Any], *, n: int, op_id: str) -> Mapping[str, Any]:
    trimmed = dict(fact)
    if n > 200:
        trimmed["risk_set_member_refs"] = compact_ref_list(fact.get("risk_set_member_refs"))
        trimmed["denominator_member_refs"] = compact_ref_list(
            fact.get("denominator_member_refs")
        )
    keep_provenance = op_id == "all_K_raw" and n in (1000, 3000)
    if n > 200 and not keep_provenance:
        trimmed["source_empirical_provenance_refs"] = None
        trimmed["dependency_refs"] = None
    return trimmed


def main():
    repeat_summaries = {}
    repeat_lines = []
    for n in (1000, 3000):
        path = RAW_REPEATS / f"main_native_n{n}_repeats4.json"
        if not path.exists():
            continue
        payload = load_json(path)
        by_op = {}
        for op in payload["ops"]:
            by_op.setdefault(op["op_id"], {})[op["repeat"]] = op
            repeat_lines.append({
                "schema": "PYAT_L03_C4_PHASE1_COST@1",
                "entry_kind": "op_repeat",
                "scenario": "main",
                "n": n,
                "kind": "native",
                "repeat": op["repeat"],
                "op_id": op["op_id"],
                "group": op["group"],
                "wall_s": op["wall_s"],
                "cpu_s": op["cpu_s"],
                "peak_rss_bytes_after_op": op["ru_maxrss_bytes_after"],
                "index_reused_from_previous": op["index_reused_from_previous"],
                "index_count_after": op["index_after"]["count"],
                "fact_ref": op["fact"]["fact_ref"],
                "replay_ref": op["fact"]["replay_ref"],
                "typed_state": op["fact"]["typed_state"],
                "raw_denominator_support": op["fact"]["raw_denominator_support"],
                "oracle_ok": op["oracle_ok"],
                "oracle_skipped": op["oracle_skipped"],
            })
        summary = {}
        for op_id, repeats in sorted(by_op.items()):
            warm = [repeats[index]["wall_s"] for index in (1, 2, 3) if index in repeats]
            warm_cpu = [repeats[index]["cpu_s"] for index in (1, 2, 3) if index in repeats]
            summary[op_id] = {
                "cold_index_wall_s": repeats[0]["wall_s"] if 0 in repeats else None,
                "warm_wall_s": warm,
                "warm_wall_median_s": statistics.median(warm) if warm else None,
                "warm_wall_min_s": min(warm) if warm else None,
                "warm_wall_max_s": max(warm) if warm else None,
                "warm_cpu_median_s": statistics.median(warm_cpu) if warm_cpu else None,
            }
        repeat_summaries[str(n)] = summary

    cost_path = RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl"
    if repeat_lines:
        with cost_path.open("a", encoding="utf-8") as handle:
            for line in repeat_lines:
                jsonline(handle, line)
            for n, summary in sorted(repeat_summaries.items()):
                jsonline(handle, {
                    "schema": "PYAT_L03_C4_PHASE1_COST@1",
                    "entry_kind": "repeat_summary",
                    "scenario": "main",
                    "n": int(n),
                    "kind": "native",
                    "method": "four sequential passes on one repository; pass 0 cold index, passes 1-3 warm",
                    "ops": summary,
                })

    parity_path = RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl"
    temp_path = parity_path.with_suffix(".tmp")
    with parity_path.open("r", encoding="utf-8") as source, temp_path.open(
        "w", encoding="utf-8"
    ) as destination:
        for line in source:
            entry = json.loads(line)
            if entry.get("entry_kind") == "baseline_exact_fact":
                entry["exact_fact"] = trim_fact(
                    entry["exact_fact"], n=entry["n"], op_id=entry["op_id"]
                )
            jsonline(destination, entry)
    temp_path.replace(parity_path)

    report = {
        "schema": "PYAT_L03_C4_PHASE1_REPEAT_SUMMARY@1",
        "method": "four sequential passes on one repository; pass 0 cold index, passes 1-3 warm",
        "n": repeat_summaries,
        "raw_repeat_files": [
            str((RAW_REPEATS / f"main_native_n{n}_repeats4.json").relative_to(REPO_ROOT))
            for n in (1000, 3000)
            if (RAW_REPEATS / f"main_native_n{n}_repeats4.json").exists()
        ],
    }
    (RESULTS / "repeat_summary.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    RAW_RESULTS.mkdir(parents=True, exist_ok=True)
    for path in sorted(RESULTS.glob("*.json")):
        if path.name in {"driver_summary.json", "repeat_summary.json"}:
            continue
        shutil.move(str(path), str(RAW_RESULTS / path.name))
    print(json.dumps({
        "cost_bytes": cost_path.stat().st_size,
        "parity_bytes": parity_path.stat().st_size,
        "raw_results": str(RAW_RESULTS),
        "repeat_summary": str(RESULTS / "repeat_summary.json"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
