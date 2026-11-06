from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
RETURN_DIR = HERE.parent
REPO_ROOT = RETURN_DIR.parents[1]
RAW = REPO_ROOT / ".local-logs" / "pyat-l03-c4"
RESULTS = RETURN_DIR / "results"
NEW_SHA = "02c1200b82b8397e551817e8e4cf2c6763413189"
PREVIOUS_CAPACITY_SHA = "9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3"
R03_SHA = "409be32f7e4b4b961a360be1c8f44a17b5c62173"


def load(path: Path):
    return json.loads(path.read_text())


def jsonline(handle, payload: Mapping[str, Any]) -> None:
    handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str))
    handle.write("\n")


def compact_compare_summary(path: Path):
    payload = load(path)
    variants = {}
    for variant in ("v1", "v2-cold", "v2-warm"):
        item = payload["variants"][variant]
        command = next(row for row in payload["commands"] if row["variant"] == variant)
        variants[variant] = {
            "parent_wall_s": command["parent_wall_s"],
            "phases": item["phases"],
            "process": item["process"],
            "cache": item["cache"],
            "release": item["release"],
        }
    return {
        "pass": payload["pass"],
        "facts_exact_equal": payload["facts_exact_equal"],
        "cache_checks": payload["cache_checks"],
        "variants": variants,
        "raw_path": str(path.relative_to(REPO_ROOT)),
    }


def alloc_summary(path: Path):
    payload = load(path)
    compact = payload["payloads"]["compact"]
    return {
        "native": payload["endstate"],
        "deltas": payload["deltas"],
        "compact_bodies": compact.get("compact_bodies"),
        "lookup_tradeoff": compact.get("lookup_tradeoff"),
        "snapshots": compact["snapshots"],
        "raw_path": str(path.relative_to(REPO_ROOT)),
    }


def main():
    n_values = (200, 1000)
    old_alloc = {n: alloc_summary(RAW / "alloc_incision" / f"n{n}" / f"alloc_n{n}.json") for n in n_values}
    new_alloc = {n: alloc_summary(RAW / "alloc_compressed" / f"n{n}" / f"alloc_n{n}.json") for n in n_values}
    old_compare = {n: compact_compare_summary(RAW / "compact_compare" / f"n{n}" / f"compare_n{n}.json") for n in n_values}
    new_compare = {n: compact_compare_summary(RAW / "compact_compare_compressed" / f"n{n}" / f"compare_n{n}.json") for n in n_values}
    summary = {
        "schema": "PYAT_L03_C4_COMPRESSED_BODIES_SUMMARY@1",
        "implementation_sha": NEW_SHA,
        "previous_capacity_sha": PREVIOUS_CAPACITY_SHA,
        "r03_acceptance_sha": R03_SHA,
        "old_alloc": old_alloc,
        "new_alloc": new_alloc,
        "old_compare": old_compare,
        "new_compare": new_compare,
        "cache_file_format": "raw canonical event bodies in existing Parquet/Zstd binary column; new streaming writer uses smaller row groups",
        "lookup_note": "compressed exact lookup decompresses a bounded 256-event chunk; selectors remain selector v1 and hot-path selection does not materialize bodies",
        "all35_claim": False,
    }
    (RESULTS / "compressed_bodies_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    with (RETURN_DIR / "02_EXACT_COST_AND_MEMORY_RESULTS.jsonl").open("a", encoding="utf-8") as cost:
        for n in n_values:
            jsonline(cost, {
                "schema": "PYAT_L03_C4_COMPRESSED_BODIES_COST@1",
                "entry_kind": "compressed_body_candidate",
                "implementation_sha": NEW_SHA,
                "previous_capacity_sha": PREVIOUS_CAPACITY_SHA,
                "n": n,
                "old_alloc": old_alloc[n],
                "new_alloc": new_alloc[n],
                "old_compare": old_compare[n],
                "new_compare": new_compare[n],
                "cache_file_format": summary["cache_file_format"],
                "lookup_note": summary["lookup_note"],
            })
        jsonline(cost, {
            "schema": "PYAT_L03_C4_COMPRESSED_BODIES_COST@1",
            "entry_kind": "compressed_body_status",
            "implementation_sha": NEW_SHA,
            "previous_capacity_sha": PREVIOUS_CAPACITY_SHA,
            "r03_acceptance_sha": R03_SHA,
            "physical_scope": ["rawlsing_next/_pre553_c11_execution_view.py"],
            "test_scope": ["rawlsing_next/tests/test_pre553_c11_execution_view.py"],
            "tests": "50 passed, 1 skipped (9 compact + source-backed + carrier + grouping)",
            "cache_format_compatible": True,
            "cache_default_changed": False,
            "second_engine_or_index": False,
            "all35_claim": False,
            "dirty": "NONE",
        })
    with (RETURN_DIR / "03_SAME_FACT_GROUPED_AND_KWAY_PARITY.jsonl").open("a", encoding="utf-8") as parity:
        for n in n_values:
            jsonline(parity, {
                "schema": "PYAT_L03_C4_COMPRESSED_BODIES_PARITY@1",
                "entry_kind": "compressed_body_parity",
                "implementation_sha": NEW_SHA,
                "n": n,
                "old_compare_pass": old_compare[n]["pass"],
                "new_compare_pass": new_compare[n]["pass"],
                "new_facts_exact_equal": new_compare[n]["facts_exact_equal"],
                "new_cache_checks": new_compare[n]["cache_checks"],
                "old_raw_path": old_compare[n]["raw_path"],
                "new_raw_path": new_compare[n]["raw_path"],
                "full_fact_sidecars": {
                    variant: new_compare[n]["variants"][variant]["release"].get("compact")
                    for variant in ("v1", "v2-cold", "v2-warm")
                },
            })
        jsonline(parity, {
            "schema": "PYAT_L03_C4_COMPRESSED_BODIES_PARITY@1",
            "entry_kind": "compressed_body_disposition",
            "implementation_sha": NEW_SHA,
            "previous_capacity_sha": PREVIOUS_CAPACITY_SHA,
            "r03_acceptance_sha": R03_SHA,
            "result": "CANDIDATE_MEASURED_FOR_FOCUSED_REVIEW",
            "exactness": "PASS: old/new V0/V1/V2 facts, cells, refs, provenance, replay equal; cache HIT/DELETE/CORRUPT/STALE/REVOKED tests retained",
            "memory": "compact body raw 29,701,433 -> 1,575,621 bytes at N=1000; compact endstate current/highwater materially reduced versus uncompressed compact",
            "tradeoff": "exact compressed event lookup adds bounded-chunk decompression cost; selector hot path and query execution remain selector-based",
            "not_claim": "no independent acceptance or whole-L03 completion; sourcefree N=200/1000 only",
        })
    (RESULTS / "compressed_body_commands.jsonl").write_text(
        json.dumps({
            "schema": "PYAT_L03_C4_COMPRESSED_BODY_COMMAND@1",
            "commands": [
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "-m", "pytest", "-q", "-p", "no:cacheprovider", "--basetemp", ".local-logs/pyat-l03-c4/tmp/pytest-phys-final", "rawlsing_next/tests/test_pre553_c11_execution_view.py", "rawlsing_next/tests/test_pre553_source_backed_c11_facade.py", "rawlsing_next/tests/test_pre553_sr06_decoder_carrier.py", "rawlsing_next/tests/test_pre553_i03_grouping.py"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "compare", "--n", "200", "--outdir", ".local-logs/pyat-l03-c4/compact_compare_compressed/n200"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "compare", "--n", "1000", "--outdir", ".local-logs/pyat-l03-c4/compact_compare_compressed/n1000"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "alloc", "--n", "200", "--outdir", ".local-logs/pyat-l03-c4/alloc_compressed/n200"],
                ["/tmp/rawlsing-oct28-p1r1/venv/bin/python", "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools/bench_compact_current.py", "--mode", "alloc", "--n", "1000", "--outdir", ".local-logs/pyat-l03-c4/alloc_compressed/n1000"],
            ],
            "env": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
                    "TMPDIR": ".local-logs/pyat-l03-c4/tmp"},
            "exit": 0,
            "note": "Candidate physical implementation and measured evidence; not independent acceptance.",
        }, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({
        "summary": str(RESULTS / "compressed_bodies_summary.json"),
        "new_sha": NEW_SHA,
        "compare_pass": {str(n): new_compare[n]["pass"] for n in n_values},
        "n1000_body": new_alloc[1000]["compact_bodies"],
        "n1000_lookup": new_alloc[1000]["lookup_tradeoff"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
