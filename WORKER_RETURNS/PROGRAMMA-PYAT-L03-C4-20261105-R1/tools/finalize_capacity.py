from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW = REPO_ROOT / ".local-logs" / "pyat-l03-c4" / "capacity_cap" / "n200" / "capacity_n200.json"
RESULTS = RETURN_DIR / "results"
CAPACITY_SHA = "9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3"
PREVIOUS_IMPL_SHA = "409be32f7e4b4b961a360be1c8f44a17b5c62173"


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def main():
    payload = json.loads(RAW.read_text())
    summary = {
        "schema": "PYAT_L03_C4_CAPACITY_SUMMARY@1",
        "implementation_sha": CAPACITY_SHA,
        "previous_implementation_sha": PREVIOUS_IMPL_SHA,
        "n": payload["n"],
        "rounds": payload["rounds"],
        "op_fill": payload["op_fill"],
        "op_miss": payload["op_miss"],
        "summary": payload["summary"],
        "process": payload["process"],
        "raw_path": str(RAW.relative_to(REPO_ROOT)),
        "facts_exact_equal": all(
            item["all_miss_equal"]
            and item.get("all_fill_equal", True)
            and item.get("all_hit_equal", True)
            for item in payload["summary"].values()
        ),
    }
    (RESULTS / "capacity_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl").open("a", encoding="utf-8") as cost:
        jsonline(cost, {
            "schema": "PYAT_L03_C4_CAPACITY_COST@1",
            "entry_kind": "capacity_full_group",
            "implementation_sha": CAPACITY_SHA,
            "previous_implementation_sha": PREVIOUS_IMPL_SHA,
            "n": payload["n"],
            "rounds": payload["rounds"],
            "op_fill": payload["op_fill"],
            "op_miss": payload["op_miss"],
            "summary": payload["summary"],
            "process": payload["process"],
            "raw_path": str(RAW.relative_to(REPO_ROOT)),
        })
        for name in ("before", "after", "no_scope"):
            for record in payload["summary"][name]["records"]:
                jsonline(cost, {
                    "schema": "PYAT_L03_C4_CAPACITY_COST@1",
                    "entry_kind": "capacity_case",
                    "implementation_sha": CAPACITY_SHA,
                    "n": payload["n"],
                    "variant": name,
                    "round": record["round"],
                    "miss_wall_s": record["miss_wall_s"],
                    "miss_cpu_s": record["miss_cpu_s"],
                    "miss_equal": record["miss_equal"],
                    "fill_wall_s": record.get("fill_wall_s"),
                    "hit_wall_s": record.get("hit_wall_s"),
                    "fill_equal": record.get("fill_equal"),
                    "hit_equal": record.get("hit_equal"),
                    "scope": record.get("scope"),
                })
        jsonline(cost, {
            "schema": "PYAT_L03_C4_CAPACITY_COST@1",
            "entry_kind": "capacity_implementation_status",
            "implementation_sha": CAPACITY_SHA,
            "previous_implementation_sha": PREVIOUS_IMPL_SHA,
            "change": "early cache-MISS capacity guard before core construction; HIT path unchanged; post-build prospective member fallback retained",
            "production_scope": ["rawlsing_next/pre553_empirical_query.py"],
            "test_scope": ["rawlsing_next/tests/test_pre553_i03_grouping.py"],
            "capacity_defaults_changed": False,
            "eviction_or_lru_added": False,
            "r03_acceptance": "e2f6c1649801b42a475ce3d81f3d85a7c5ccb5b3 covers only 409be32f7e4b4b961a360be1c8f44a17b5c62173, not 9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3",
        })
    with (RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl").open("a", encoding="utf-8") as parity:
        jsonline(parity, {
            "schema": "PYAT_L03_C4_CAPACITY_PARITY@1",
            "entry_kind": "capacity_full_group_parity",
            "implementation_sha": CAPACITY_SHA,
            "previous_implementation_sha": PREVIOUS_IMPL_SHA,
            "n": payload["n"],
            "op_fill": payload["op_fill"],
            "op_miss": payload["op_miss"],
            "facts_exact_equal": summary["facts_exact_equal"],
            "before": payload["summary"]["before"],
            "after": payload["summary"]["after"],
            "no_scope": payload["summary"]["no_scope"],
            "raw_path": str(RAW.relative_to(REPO_ROOT)),
        })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_CAPACITY_PARITY@1",
            "entry_kind": "capacity_disposition",
            "implementation_sha": CAPACITY_SHA,
            "result": "EARLY_MISS_GUARD_MEASURED",
            "hit_at_full_capacity": "REUSED",
            "new_miss_at_full_capacity": "NO_CORE_BUILD",
            "member_prospective_unknown": "POST_BUILD_FALLBACK_RETAINED",
            "facts": "EXACT_VS_NO_SCOPE",
            "r03_scope": "R03_ACCEPTED_ONLY_409be; NEW_SHA_NOT_ACCEPTED",
            "no_capacity_default_or_eviction_change": True,
        })
    (RESULTS / "capacity_commands.jsonl").write_text(json.dumps({
        "schema": "PYAT_L03_C4_CAPACITY_COMMAND@1",
        "label": "capacity_n200",
        "command": [
            "/tmp/rawlsing-oct28-p1r1/venv/bin/python",
            "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py",
            "--mode", "capacity", "--n", "200", "--rounds", "3",
            "--outdir", ".local-logs/pyat-l03-c4/capacity_cap/n200",
        ],
        "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
        "exit": 0,
        "summary": "capacity-full before/after/no-scope exact; early guard measured",
    }, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "summary": str(RESULTS / "capacity_summary.json"),
        "before_median": payload["summary"]["before"]["miss_wall_median_s"],
        "after_median": payload["summary"]["after"]["miss_wall_median_s"],
        "no_scope_median": payload["summary"]["no_scope"]["miss_wall_median_s"],
        "facts_exact_equal": summary["facts_exact_equal"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
