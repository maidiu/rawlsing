"""Run the PYAT #1006 baseline shapes sequentially under the 6 GiB tree cap."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any

from instrument_1006 import stats
from resources_1006 import (
    CAP_BYTES,
    MIN_FREE_DISK_BYTES,
    disk,
    host_info,
    run_monitored,
)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def _shape_config(name: str) -> dict[str, Any]:
    presets = {
        "diag-1k": {
            "respondents": 1000, "include_weights": True, "skew_events": 0,
            "repeat": 10, "fresh": 10, "native": True, "timeout": 1800,
            "batch_units": "selected,f2_forward,f2_reverse,f4_three,f4_four,i05",
        },
        "diag-10k": {
            "respondents": 10000, "include_weights": True, "skew_events": 0,
            "repeat": 10, "fresh": 10, "native": True, "timeout": 2400,
            "batch_units": "selected,f2_forward,f2_reverse,f4_three,f4_four,i05",
        },
        "diag-10k-fast": {
            "respondents": 10000, "include_weights": True, "skew_events": 0,
            "repeat": 5, "fresh": 5, "native": True, "timeout": 3000,
            "batch_units": "selected,f2_reverse,f4_three,i05",
        },
        "diag-50k": {
            "respondents": 50000, "include_weights": True, "skew_events": 0,
            "repeat": 10, "fresh": 10, "native": True, "timeout": 3600,
            "batch_units": "selected,f2_reverse,f4_three,i05",
        },
        "hist-100k": {
            "respondents": 100000, "include_weights": True, "skew_events": 0,
            "repeat": 10, "fresh": 10, "native": True, "timeout": 5400,
            "batch_units": "selected,f2_reverse,f4_three,i05",
        },
        "scale-50k": {
            "respondents": 50000, "include_weights": True, "skew_events": 0,
            "repeat": 0, "fresh": 0, "native": False, "timeout": 3600,
            "batch_units": "", "stop_after": "write",
            "query_names": "selected,f2_reverse,f4_three",
        },
        "scale-100k": {
            "respondents": 100000, "include_weights": True, "skew_events": 0,
            "repeat": 0, "fresh": 0, "native": False, "timeout": 5400,
            "batch_units": "", "stop_after": "write",
            "query_names": "selected,f2_reverse,f4_three",
        },
        "skew-1k": {
            "respondents": 1000, "include_weights": True, "skew_events": 2000,
            "repeat": 5, "fresh": 5, "native": True, "timeout": 1800,
            "batch_units": "selected,f4_three,i05",
        },
    }
    return presets[name]


def _run_worker(
    name: str, config: dict[str, Any], *, outdir: Path, env: dict[str, str],
    chunk_rows: int,
) -> dict[str, Any]:
    workdir = outdir / "estates" / name
    workdir.mkdir(parents=True, exist_ok=True)
    out = outdir / f"{name}.metrics.json"
    command = [
        sys.executable, str(HERE / "shape_worker.py"),
        "--name", name,
        "--respondents", str(config["respondents"]),
        "--workdir", str(workdir),
        "--out", str(out),
        "--chunk-rows", str(chunk_rows),
        "--repeat", str(config["repeat"]),
        "--batch-units", config["batch_units"],
        "--query-names", config.get(
            "query_names",
            "selected,f2_forward,f2_reverse,f4_three,f4_four,weighted",
        ),
    ]
    if config["include_weights"]:
        command.append("--include-weights")
    if config["skew_events"]:
        command.extend(["--skew-events", str(config["skew_events"])])
    if not config["native"]:
        command.append("--no-native-readers")
    if config.get("stop_after"):
        command.extend(["--stop-after", config["stop_after"]])
    command.append("--time-sections")
    start = time.monotonic()
    monitored = run_monitored(
        command, cwd=REPO, env=env, timeout_seconds=config["timeout"],
        cap_bytes=CAP_BYTES,
    )
    metrics: dict[str, Any] = {
        "name": name,
        "command": command,
        "monitored": {
            key: value for key, value in monitored.items() if key not in ("stdout", "stderr")
        },
        "stdout_tail": monitored["stdout"][-2000:],
        "stderr_tail": monitored["stderr"][-4000:],
        "wall_seconds": time.monotonic() - start,
    }
    if out.exists():
        metrics["worker"] = json.loads(out.read_text(encoding="utf-8"))
    else:
        metrics["worker"] = None
    metrics["disk_after"] = disk(outdir)
    return metrics


def _run_fresh(
    name: str, config: dict[str, Any], *, outdir: Path, env: dict[str, str],
    worker: dict[str, Any],
) -> dict[str, Any]:
    count = config["fresh"]
    if not count:
        return {"n": 0, "status": "NOT_REQUESTED"}
    capsule = worker.get("capsule")
    if not capsule:
        return {"n": 0, "status": "NOT_RUN_NO_CAPSULE"}
    capsule_path = outdir / "estates" / name / "fresh-capsule.json"
    capsule_path.write_text(json.dumps(capsule, sort_keys=True), encoding="utf-8")
    command = [sys.executable, str(HERE / "fresh_probe.py"), str(capsule_path)]
    values = []
    admission_values = []
    failures = []
    tree_peaks = []
    for index in range(count):
        monitored = run_monitored(
            command, cwd=REPO, env=env, timeout_seconds=300,
            cap_bytes=CAP_BYTES,
        )
        record = {
            "index": index,
            "returncode": monitored["returncode"],
            "seconds": monitored["seconds"],
            "process_tree": monitored["process_tree"],
            "stderr_tail": monitored["stderr"][-2000:],
        }
        if monitored["returncode"] == 0:
            try:
                payload = json.loads(monitored["stdout"])
                record["payload"] = payload
                values.append(float(payload["query_seconds"]))
                admission_values.append(float(payload["admission_seconds"]))
            except (ValueError, KeyError) as exc:
                record["parse_error"] = f"{type(exc).__name__}: {exc}"
                failures.append(record)
        else:
            failures.append(record)
        tree_peaks.append(monitored["process_tree"]["tree_peak_rss_bytes"])
    return {
        "n": len(values),
        "requested": count,
        "status": "MEASURED" if len(values) == count else "PARTIAL_OR_FAILED",
        "query_seconds": values,
        "query_stats": stats(values),
        "admission_seconds": admission_values,
        "admission_stats": stats(admission_values),
        "tree_peak_rss_bytes": max(tree_peaks, default=0),
        "failures": failures,
    }


def _baseline_row(record: dict[str, Any]) -> dict[str, Any]:
    worker = record.get("worker") or {}
    timers = worker.get("timers", {}).get("seconds", {})
    audit = worker.get("parquet_audit", {})
    queries = worker.get("queries", {})
    fresh = record.get("fresh", {})
    native = worker.get("native_readers", {})
    return {
        "shape": record["name"],
        "status": worker.get("status", "NO_WORKER_METRICS"),
        "respondents": worker.get("shape", {}).get("respondents"),
        "events": worker.get("respondents_vs_events", {}).get("events"),
        "events_per_respondent": (
            worker.get("respondents_vs_events", {}).get("events", 0)
            / worker.get("respondents_vs_events", {}).get("respondents", 1)
            if worker.get("respondents_vs_events", {}).get("respondents")
            else None
        ),
        "write_seconds": worker.get("write_seconds"),
        "direct_i02_proof_seconds": timers.get("direct_i02_proof"),
        "physical_reread_reencode_seconds": timers.get("physical_reread_reencode_proof"),
        "root_hash_seconds": timers.get("root_hash"),
        "row_projection_seconds": worker.get("writer_instrumentation", {}).get("row_seconds"),
        "cold_admission_seconds": worker.get("cold_admission_seconds"),
        "cold_admission_hash_calls": worker.get("cold_admission_hash_calls"),
        "session_build_seconds_total": timers.get("cold_session_posting_index_build"),
        "session_build_calls": worker.get("timers", {}).get("calls", {}).get(
            "cold_session_posting_index_build"
        ),
        "selected_first_seconds": queries.get("selected", {}).get("seconds"),
        "f2_forward_seconds": queries.get("f2_forward", {}).get("seconds"),
        "f2_reverse_seconds": queries.get("f2_reverse", {}).get("seconds"),
        "f4_three_seconds": queries.get("f4_three", {}).get("seconds"),
        "f4_four_seconds": queries.get("f4_four", {}).get("seconds"),
        "weighted_seconds": queries.get("weighted", {}).get("seconds"),
        "i05_seconds": worker.get("i05", {}).get("seconds"),
        "batch_seconds": worker.get("batch", {}).get("seconds"),
        "normal_seconds": native.get("normal_seconds"),
        "resume_completed_seconds": native.get("resume_completed_seconds"),
        "resume_partial_seconds": native.get("resume_partial_seconds"),
        "resume_absent_seconds": native.get("resume_absent_seconds"),
        "same_process_n": worker.get("selected_repeat", {}).get("stats", {}).get("n"),
        "same_process_p50": worker.get("selected_repeat", {}).get("stats", {}).get("p50"),
        "same_process_p95": worker.get("selected_repeat", {}).get("stats", {}).get("p95"),
        "fresh_process_n": fresh.get("n"),
        "fresh_process_p50": fresh.get("query_stats", {}).get("p50"),
        "fresh_process_p95": fresh.get("query_stats", {}).get("p95"),
        "retained_bytes": worker.get("retained_bytes"),
        "parquet_bytes": audit.get("total_bytes"),
        "parquet_rows": audit.get("total_rows"),
        "parquet_row_groups": audit.get("total_row_groups"),
        "stage_peak_bytes": worker.get("stage_monitor", {}).get("stage_peak_bytes"),
        "proof_sqlite_peak_bytes": worker.get("stage_monitor", {}).get(
            "proof_sqlite_peak_bytes"
        ),
        "object_materializations_total": worker.get("object_materializations_total"),
        "process_tree_peak_rss_bytes": record.get("monitored", {}).get(
            "process_tree", {}
        ).get("tree_peak_rss_bytes"),
        "cap_exceeded": record.get("monitored", {}).get("process_tree", {}).get(
            "cap_exceeded"
        ),
        "killed_for_cap": record.get("monitored", {}).get("killed_for_cap"),
        "timed_out": record.get("monitored", {}).get("timed_out"),
        "disk_free_after": record.get("disk_after", {}).get("free"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--shapes", default="diag-1k,diag-10k,diag-50k,hist-100k,skew-1k")
    parser.add_argument("--chunk-rows", type=int, default=512)
    parser.add_argument("--skip-fresh", action="store_true")
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    outdir.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO) + os.pathsep + str(HERE)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    start = time.monotonic()
    results = {
        "schema": "PYAT1006_BASELINE@1",
        "host": host_info(outdir),
        "cap_bytes": CAP_BYTES,
        "min_free_disk_bytes": MIN_FREE_DISK_BYTES,
        "chunk_rows": args.chunk_rows,
        "shapes_requested": args.shapes.split(","),
        "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    records = []
    for name in args.shapes.split(","):
        config = _shape_config(name)
        outdir_current = outdir
        before = disk(outdir_current)
        if before["free"] < MIN_FREE_DISK_BYTES:
            records.append({
                "name": name, "status": "RESOURCE_HOLD_DISK",
                "disk_before": before, "worker": None,
            })
            continue
        record = _run_worker(
            name, config, outdir=outdir_current, env=env,
            chunk_rows=args.chunk_rows,
        )
        worker = record.get("worker") or {}
        if not args.skip_fresh and worker.get("status") in (
            "MEASURED", "MEASURED_PARTIAL_STOPPED_AFTER_QUERIES"
        ):
            record["fresh"] = _run_fresh(
                name, config, outdir=outdir_current, env=env, worker=worker,
            )
        else:
            record["fresh"] = {
                "n": 0,
                "status": "NOT_RUN_WORKER_NOT_MEASURED_OR_SKIPPED",
            }
        records.append(record)
        (outdir / f"{name}.monitored.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    results["records"] = records
    results["baseline_rows"] = [_baseline_row(record) for record in records]
    results["seconds_total"] = time.monotonic() - start
    results["disk_after"] = disk(outdir)
    (outdir / "baseline.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "baseline": str(outdir / "baseline.json"),
        "rows": results["baseline_rows"],
        "seconds_total": results["seconds_total"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
