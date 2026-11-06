from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW = REPO_ROOT / ".local-logs" / "pyat-l03-c4" / "alloc_incision"
RESULTS = RETURN_DIR / "results"
CAPACITY_SHA = "9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3"
PREVIOUS_R03_SHA = "409be32f7e4b4b961a360be1c8f44a17b5c62173"
ASSESSMENT_SHA = "5dfef26d5ba25d2848d8e7a1b137e29c2d3b544d"


def load(path: Path):
    return json.loads(path.read_text())


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def main():
    datasets = {}
    for n in (200, 1000):
        datasets[str(n)] = load(RAW / f"n{n}" / f"alloc_n{n}.json")
    repeat = load(RAW / "repeat_n1000" / "alloc_n1000.json")
    facts_equal = {}
    for n, payload in datasets.items():
        native_fact = payload["payloads"]["native"]["phases"]["first_query"]
        compact_fact = payload["payloads"]["compact"]["phases"]["first_query"]
        facts_equal[n] = (
            native_fact["exact_fact_material_sha256"] == compact_fact["exact_fact_material_sha256"]
            and native_fact["fact_ref"] == compact_fact["fact_ref"]
            and native_fact["replay_ref"] == compact_fact["replay_ref"]
        )
    summary = {
        "schema": "PYAT_L03_C4_ALLOC_INCISION_SUMMARY@1",
        "implementation_sha_under_measurement": PREVIOUS_R03_SHA,
        "capacity_repair_sha": CAPACITY_SHA,
        "phase3_assessment_sha": ASSESSMENT_SHA,
        "datasets": datasets,
        "repeat_n1000": repeat,
        "native_compact_facts_equal": facts_equal,
        "causal": {
            "fixed_arrow_import_runtime": "same Arrow import + minimal array in native and compact controls",
            "native_control": "full native release/repository/first consumer with Arrow runtime initialized",
            "compact_live_python": "compact endstate has lower Python tracemalloc than native after dropping native events",
            "compact_arrow_body": "compact retains an Arrow binary event-body array (~29.7 MB at N=1000)",
            "compact_resident_extra": "remaining current-RSS difference is chiefly compact conversion overlap/allocator retention, not a measured redundant live Python copy",
            "repair_dependency": "reducing this materially requires a streaming/lazy I02 candidate/replay ABI or compact conversion before full native object materialization; selector v1/I02/ref/replay must remain exact",
        },
        "no_physical_code_change": True,
        "no_all35_claim": True,
    }
    (RESULTS / "alloc_incision_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl").open("a", encoding="utf-8") as cost:
        for n, payload in datasets.items():
            jsonline(cost, {
                "schema": "PYAT_L03_C4_ALLOC_INCISION_COST@1",
                "entry_kind": "alloc_incision_process",
                "n": int(n),
                "implementation_sha_under_measurement": PREVIOUS_R03_SHA,
                "capacity_repair_sha": CAPACITY_SHA,
                "deltas": payload["deltas"],
                "endstate": payload["endstate"],
                "payloads": payload["payloads"],
                "raw_path": str((RAW / f"n{n}" / f"alloc_n{n}.json").relative_to(REPO_ROOT)),
            })
            for variant in ("arrow", "native", "compact"):
                for snap in payload["payloads"][variant]["snapshots"]:
                    jsonline(cost, {
                        "schema": "PYAT_L03_C4_ALLOC_INCISION_COST@1",
                        "entry_kind": "alloc_snapshot",
                        "n": int(n),
                        "variant": variant,
                        "label": snap["label"],
                        "current_rss_bytes": snap["current_rss_bytes"],
                        "ru_maxrss_bytes": snap["ru_maxrss_bytes"],
                        "tracemalloc": snap["tracemalloc"],
                        "arrow": snap["arrow"],
                    })
        jsonline(cost, {
            "schema": "PYAT_L03_C4_ALLOC_INCISION_COST@1",
            "entry_kind": "alloc_repeat_n1000",
            "payload": repeat,
            "raw_path": str((RAW / "repeat_n1000" / "alloc_n1000.json").relative_to(REPO_ROOT)),
        })
        jsonline(cost, {
            "schema": "PYAT_L03_C4_ALLOC_INCISION_COST@1",
            "entry_kind": "alloc_incision_status",
            "implementation_sha_under_measurement": PREVIOUS_R03_SHA,
            "capacity_repair_sha": CAPACITY_SHA,
            "phase3_assessment_sha": ASSESSMENT_SHA,
            "physical_code_changed": False,
            "selection": "NO_SMALL_RETAINED_COPY_TO_REMOVE",
            "repair_dependency": "streaming/lazy I02 candidate/replay ABI or compact conversion during validation; separate owner decision",
            "delete_corrupt_stale_revoke": "NOT_RUN_HERE",
            "n3000": "NOT_RUN",
        })
    with (RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl").open("a", encoding="utf-8") as parity:
        for n, payload in datasets.items():
            jsonline(parity, {
                "schema": "PYAT_L03_C4_ALLOC_INCISION_PARITY@1",
                "entry_kind": "alloc_incision_fact_parity",
                "n": int(n),
                "native_compact_facts_equal": facts_equal[n],
                "native_fact": payload["payloads"]["native"]["phases"]["first_query"],
                "compact_fact": payload["payloads"]["compact"]["phases"]["first_query"],
                "raw_path": str((RAW / f"n{n}" / f"alloc_n{n}.json").relative_to(REPO_ROOT)),
            })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_ALLOC_INCISION_PARITY@1",
            "entry_kind": "alloc_incision_disposition",
            "implementation_sha_under_measurement": PREVIOUS_R03_SHA,
            "capacity_repair_sha": CAPACITY_SHA,
            "assessment": "compact economic target NOT_FULFILLED; remaining RSS gap is fixed Arrow runtime + required Arrow body + conversion/allocator retention",
            "small_retained_copy_found": False,
            "physical_code_change": "NONE",
            "exact_dependency": "I02 candidate/validation and _compact_public_objects currently require full native event materialization before compact construction; removing that overlap requires a streaming/lazy candidate/replay or incremental compact ABI, owned by HQ/owner",
            "all35_claim": False,
        })
    (RESULTS / "alloc_incision_commands.jsonl").write_text(
        json.dumps({
            "schema": "PYAT_L03_C4_ALLOC_INCISION_COMMAND@1",
            "label": "alloc_incision_n200_n1000",
            "commands": [
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "alloc", "--n", "200", "--outdir", ".local-logs/pyat-l03-c4/alloc_incision/n200"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "alloc", "--n", "1000", "--outdir", ".local-logs/pyat-l03-c4/alloc_incision/n1000"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "alloc", "--n", "1000", "--outdir", ".local-logs/pyat-l03-c4/alloc_incision/repeat_n1000"],
            ],
            "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                    "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
            "exit": 0,
            "note": "Allocation incision only; no physical code change.",
        }, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "summary": str(RESULTS / "alloc_incision_summary.json"),
        "facts_equal": facts_equal,
        "n1000_endstate": datasets["1000"]["endstate"],
        "deltas_1000": datasets["1000"]["deltas"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
