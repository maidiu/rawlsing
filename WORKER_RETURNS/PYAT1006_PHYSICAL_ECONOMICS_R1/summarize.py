"""Extract compact, reviewable evidence from the large local run JSONs."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from instrument_1006 import stats


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _query_summary(queries: dict[str, Any]) -> dict[str, Any]:
    return {
        name: {
            "seconds": row.get("seconds"),
            "fact_states": [fact.get("typed_state") for fact in row.get("facts", ())],
            "denominators": [
                fact.get("raw_denominator_support") for fact in row.get("facts", ())
            ],
            "fact_refs": [fact.get("ref") for fact in row.get("facts", ())],
        }
        for name, row in queries.items()
    }


def _shape(
    name: str, baseline: Path, *, query_probe: Path | None = None,
    fresh_override: Path | None = None, repeat_override: Path | None = None,
    session_probe: Path | None = None, extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    document = _load(baseline)
    record = document["records"][0]
    worker = record.get("worker") or {}
    timers = worker.get("timers", {}).get("seconds", {})
    calls = worker.get("timers", {}).get("calls", {})
    audit = worker.get("parquet_audit", {})
    writer = worker.get("writer_instrumentation", {})
    result: dict[str, Any] = {
        "shape": name,
        "respondents": worker.get("shape", {}).get("respondents"),
        "events": worker.get("respondents_vs_events", {}).get("events"),
        "events_per_respondent": (
            worker.get("respondents_vs_events", {}).get("events", 0)
            / worker.get("respondents_vs_events", {}).get("respondents", 1)
            if worker.get("respondents_vs_events", {}).get("respondents")
            else None
        ),
        "status": worker.get("status"),
        "declared_counts": worker.get("declared_counts"),
        "write": {
            "total_seconds": worker.get("write_seconds"),
            "direct_i02_proof_seconds": timers.get("direct_i02_proof"),
            "physical_reread_reencode_seconds": timers.get(
                "physical_reread_reencode_proof"
            ),
            "root_hash_seconds": timers.get("root_hash"),
            "row_projection_seconds": writer.get("row_seconds"),
            "row_calls": writer.get("row_calls"),
            "row_body_bytes": writer.get("row_body_bytes"),
            "sink_flush_calls": writer.get("sink_flush_calls"),
            "hash_calls": writer.get("hash_calls"),
            "hash_bytes": writer.get("hash_bytes"),
        },
        "physical": {
            "retained_bytes": worker.get("retained_bytes"),
            "parquet_bytes": audit.get("total_bytes"),
            "parquet_rows": audit.get("total_rows"),
            "parquet_row_groups": audit.get("total_row_groups"),
            "stage_peak_bytes": worker.get("stage_monitor", {}).get("stage_peak_bytes"),
            "proof_sqlite_peak_bytes": worker.get("stage_monitor", {}).get(
                "proof_sqlite_peak_bytes"
            ),
            "members": {
                member: {
                    "bytes": row.get("bytes"),
                    "rows": row.get("rows"),
                    "row_groups": row.get("row_groups"),
                }
                for member, row in audit.get("members", {}).items()
            },
        },
        "cold": {
            "admission_seconds": worker.get("cold_admission_seconds"),
            "hash_calls": worker.get("cold_admission_hash_calls"),
            "session_build_seconds_total": timers.get(
                "cold_session_posting_index_build"
            ),
            "session_build_calls": calls.get("cold_session_posting_index_build"),
        },
        "queries": _query_summary(worker.get("queries", {})),
        "i05": {
            key: value for key, value in (worker.get("i05") or {}).items()
            if key != "fact_refs"
        },
        "batch": {
            key: value for key, value in (worker.get("batch") or {}).items()
            if key != "receipt_refs"
        },
        "native_readers": {
            key: value for key, value in (worker.get("native_readers") or {}).items()
            if not key.endswith("output_refs")
        },
        "same_process": worker.get("selected_repeat", {}).get("stats"),
        "fresh": record.get("fresh", {}),
        "process_tree": record.get("monitored", {}).get("process_tree", {}),
        "disk": {
            "after": record.get("disk_after"),
            "at_start": worker.get("host", {}).get("disk_at_start"),
        },
        "object_materializations_total": worker.get("object_materializations_total"),
        "extra": extra or {},
    }
    if repeat_override and repeat_override.exists():
        override = _load(repeat_override)
        values = list(worker.get("selected_repeat", {}).get("seconds", ()))
        values.extend(override.get("selected_repeat", {}).get("seconds", ()))
        result["same_process"] = stats(values)
        result["same_process_values"] = values
    if fresh_override and fresh_override.exists():
        override = _load(fresh_override)
        result["fresh"] = override
    if query_probe and query_probe.exists():
        probe = _load(query_probe)
        result["queries"] = _query_summary(probe.get("queries", {}))
        result["query_probe_status"] = probe.get("status")
        if probe.get("selected_repeat"):
            result["same_process"] = probe["selected_repeat"].get("stats")
    if session_probe and session_probe.exists():
        probe = _load(session_probe)
        result["cold"]["admission_seconds"] = probe.get("admission_seconds")
        result["cold"]["session_build_seconds"] = probe.get("session_build_seconds")
        result["cold"]["temporary_bytes_during_session"] = probe.get(
            "temporary_bytes_during_session"
        )
        result["cold"]["events"] = probe.get("events")
        result["cold"]["members"] = probe.get("members")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    root = Path(args.root)
    shapes = [
        _shape(
            "diag-1k", root / "suite-1k" / "baseline.json",
        ),
        _shape(
            "diag-10k", root / "suite-10k" / "baseline.json",
            repeat_override=root / "suite-10k" / "repeat_probe_5.json",
            fresh_override=root / "suite-10k" / "fresh_probe_10.json",
        ),
        _shape(
            "skew-1k", root / "suite-skew-1k" / "baseline.json",
        ),
        _shape(
            "scale-50k", root / "suite-50k-write" / "baseline.json",
            query_probe=root / "suite-50k-write" / "query_probe.json",
            session_probe=root / "suite-50k-write" / "session_probe.json",
            extra={
                "query_probe_note": (
                    "The 50k query probe measured all three requested queries; its "
                    "status remained PARTIAL_RUNNING because a harness repeat-section "
                    "bug raised after the measurements. The query timings are real."
                )
            },
        ),
        _shape(
            "hist-100k", root / "suite-100k-write" / "baseline.json",
            query_probe=root / "suite-100k-write" / "query_probe.json",
            session_probe=root / "suite-100k-write" / "session_probe.json",
        ),
    ]
    monitored = _load(Path(__file__).with_name("evidence") / "query_probe_monitored.json")
    for item in shapes:
        item["query_probe_monitored"] = monitored.get("shapes", {}).get(item["shape"])
    summary = {
        "schema": "PYAT1006_BASELINE_SUMMARY@1",
        "shapes": shapes,
        "limits": {
            "fixture": "SOURCEFREE SYNTHETIC, NOT ORIGINAL35 OR #1001",
            "true_source_decode": "NOT_RUN_PENDING_997_HANDOFF",
            "full_native_readers": (
                "1k/10k/skew: attempted; 50k/100k: NOT_RUN in this run because "
                "the measured per-query cost already makes the standalone full "
                "vertical impractical inside the command budget"
            ),
            "ten_fresh_100k": "NOT_RUN_MEASURED_COST",
        },
    }
    out = Path(args.out)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "summary": str(out),
        "shapes": [
            {
                "shape": item["shape"],
                "respondents": item["respondents"],
                "events": item["events"],
                "write_seconds": item["write"]["total_seconds"],
                "selected_seconds": item["queries"].get("selected", {}).get("seconds"),
                "f4_three_seconds": item["queries"].get("f4_three", {}).get("seconds"),
                "same_process": item["same_process"],
                "fresh_n": item.get("fresh", {}).get("n"),
                "process_tree_peak": item["process_tree"].get("tree_peak_rss_bytes"),
                "cap_exceeded": item["process_tree"].get("cap_exceeded"),
            }
            for item in shapes
        ],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
