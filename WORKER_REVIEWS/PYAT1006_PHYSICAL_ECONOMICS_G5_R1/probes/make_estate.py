"""Regenerate one matched #1006 sourcefree fixture under the review path.

Uses the unchanged author fixture/query helpers and frozen production writer.
Review-owned instrumentation only counts existing call boundaries.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import shutil
import sys
import time
from typing import Any

from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_source_direct_parquet_estate import (
    write_direct_estate,
)
import rawlsing_next.pre553_source_direct_parquet_estate as estate_module

from fixture_1006 import ShapeSpec, build_context
from query_1006 import build_query_bundle
from review_common import (
    MIN_FREE_DISK_BYTES, REVIEW, TreeMonitor, disk, host_info, write_json,
)


class Timers:
    def __init__(self) -> None:
        self.values: dict[str, float] = {}
        self.calls: dict[str, int] = {}

    def add(self, name: str, seconds: float) -> None:
        self.values[name] = self.values.get(name, 0.0) + seconds
        self.calls[name] = self.calls.get(name, 0) + 1


def _jsonable(value: Any) -> Any:
    if value is None:
        return None
    return json.loads(canonical_json(value))


def build_capsule(ctx: Any, bundle: Any, receipt: Any, root: Path) -> dict[str, Any]:
    return {
        "root": str(root),
        "exact_path": receipt.path,
        "manifest_sha256": receipt.manifest_sha256,
        "i02": asdict(receipt.i02),
        "release": receipt.reconstructed_v1_release_ref.as_dict(),
        "query": bundle.selected.as_dict(),
        "predicate": bundle.selected_predicate.as_dict(),
        "catalog": {
            "authorities": [a.as_dict() for a in bundle.catalog.authorities],
            "predicates": [p.as_dict() for p in bundle.catalog.predicates],
            "queries": [q.as_dict() for q in bundle.catalog.queries],
            "discovery_authorities": [
                d.as_dict() for d in bundle.catalog.discovery_authorities
            ],
        },
        "query_refs": {
            name: {
                "query": _jsonable(bundle.by_name(name)[0].ref),
                "predicate": _jsonable(bundle.by_name(name)[1].ref),
            }
            for name in (
                "selected", "f2_forward", "f2_reverse", "f4_three",
                "f4_four", "weighted", "repeated",
            )
            if (name != "weighted" or bundle.weighted is not None)
            and (name != "repeated" or bundle.repeated is not None)
        },
        "family_counts": dict(receipt.family_counts),
        "typed_absences": dict(ctx.typed_absences()),
        "declared_counts": dict(ctx.manifest.declared_record_counts_by_logical_family),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--respondents", type=int, required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--chunk-rows", type=int, default=512)
    parser.add_argument("--include-weights", action="store_true")
    parser.add_argument("--skew-events", type=int, default=0)
    args = parser.parse_args(argv)

    outdir = Path(args.outdir).absolute()
    root = outdir / "estate"
    if root.exists():
        shutil.rmtree(root)
    outdir.mkdir(parents=True, exist_ok=True)
    root.mkdir(mode=0o700)
    result: dict[str, Any] = {
        "schema": "PYAT1006_G5_REGENERATED_ESTATE@1",
        "name": args.name,
        "host": host_info(),
        "outdir": str(outdir),
        "disk_at_start": disk(outdir),
        "status": "RUNNING",
        "stage": "fixture_build",
    }
    metrics_path = outdir / "writer_metrics.json"
    write_json(metrics_path, result)
    if result["disk_at_start"]["free"] < MIN_FREE_DISK_BYTES:
        result["status"] = "RESOURCE_HOLD_DISK"
        write_json(metrics_path, result)
        return 2

    ctx = build_context(ShapeSpec(
        name=args.name, respondents=args.respondents,
        include_weights=args.include_weights, skew_events=args.skew_events,
        tag=f"PYAT1006-{args.name}",
    ))
    bundle = build_query_bundle(ctx)
    timers = Timers()
    state: dict[str, Any] = {"row_calls": {}, "row_seconds": 0.0}

    original_row = estate_module._row
    original_build = estate_module.build_sourcefree_direct_i02
    original_verify = estate_module._verify_emitted_physical_payloads
    original_hash = estate_module._hash

    def row(family: str, obj: object) -> dict[str, Any]:
        start = time.monotonic()
        try:
            return original_row(family, obj)
        finally:
            state["row_seconds"] += time.monotonic() - start
            state["row_calls"][family] = state["row_calls"].get(family, 0) + 1

    def build(*a: Any, **k: Any) -> Any:
        start = time.monotonic()
        try:
            return original_build(*a, **k)
        finally:
            timers.add("direct_i02_proof", time.monotonic() - start)

    def verify(*a: Any, **k: Any) -> Any:
        start = time.monotonic()
        try:
            return original_verify(*a, **k)
        finally:
            timers.add("physical_reread_reencode_proof", time.monotonic() - start)

    def hash_path(path: Path) -> str:
        start = time.monotonic()
        try:
            return original_hash(path)
        finally:
            timers.add("root_hash", time.monotonic() - start)

    estate_module._row = row
    estate_module.build_sourcefree_direct_i02 = build
    estate_module._verify_emitted_physical_payloads = verify
    estate_module._hash = hash_path
    try:
        result["declared_counts"] = dict(ctx.manifest.declared_record_counts_by_logical_family)
        result["respondents"] = args.respondents
        result["events"] = ctx.shape.event_count
        result["event_count_formula"] = {
            "base_3_per_respondent": 3 * args.respondents,
            "sparse": ctx.shape.sparse_count,
            "repeated": 2 * ctx.shape.repeated_count,
            "skew": args.skew_events,
        }
        result["stage"] = "write"
        write_json(metrics_path, result)
        monitor = TreeMonitor(os.getpid(), watch=root, interval=0.5)
        monitor.__enter__()
        try:
            started = time.monotonic()
            receipt = write_direct_estate(
                ctx.direct_sections(), ctx.universe.ref, root,
                chunk_rows=args.chunk_rows,
            )
            result["write_seconds"] = time.monotonic() - started
        finally:
            monitor.__exit__(None, None, None)
        result["monitor"] = monitor.material()
        result["writer_instrumentation"] = {
            "row_calls": dict(state["row_calls"]),
            "row_seconds": state["row_seconds"],
            "timers_seconds": dict(timers.values),
            "timers_calls": dict(timers.calls),
        }
        result["receipt"] = {
            "path": receipt.path,
            "manifest_sha256": receipt.manifest_sha256,
            "i02": asdict(receipt.i02),
            "reconstructed_v1_release_ref": receipt.reconstructed_v1_release_ref.as_dict(),
            "family_counts": dict(receipt.family_counts),
            "retained_bytes": receipt.retained_bytes,
        }
        result["disk_after_write"] = disk(outdir)
        result["stage_files_after_write"] = sorted(
            str(path.relative_to(outdir)) for path in outdir.rglob("*") if path.is_file()
        )
        result["staging_dirs_remaining"] = [
            str(path) for path in outdir.rglob(".s2c-stage-*")
        ]
        result["proof_sqlite_remaining"] = [
            str(path) for path in outdir.rglob("*.sqlite")
        ]
        result["capsule"] = build_capsule(ctx, bundle, receipt, root)
        write_json(outdir / "capsule.json", result["capsule"])
        result["status"] = "MEASURED_WRITE"
        result["stage"] = "write_complete"
        write_json(metrics_path, result)
        print(json.dumps({
            "status": result["status"],
            "write_seconds": result["write_seconds"],
            "retained_bytes": receipt.retained_bytes,
            "stage_peak_bytes": result["monitor"]["stage_peak_bytes"],
            "tree_peak_rss_bytes": result["monitor"]["tree_peak_rss_bytes"],
        }, indent=2, sort_keys=True))
        return 0
    except BaseException as exc:
        result["status"] = "FAILED"
        result["error"] = f"{type(exc).__name__}: {exc}"
        result["disk_after_failure"] = disk(outdir)
        write_json(metrics_path, result)
        raise
    finally:
        estate_module._row = original_row
        estate_module.build_sourcefree_direct_i02 = original_build
        estate_module._verify_emitted_physical_payloads = original_verify
        estate_module._hash = original_hash


if __name__ == "__main__":
    raise SystemExit(main())
