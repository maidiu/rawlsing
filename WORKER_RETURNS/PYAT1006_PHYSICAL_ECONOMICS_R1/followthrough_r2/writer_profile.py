"""Profiled direct-I02 writer call boundaries on the existing fixture.

The accepted writer is invoked unchanged.  Wrappers only time existing calls.
Large-estate scale limits are honest: this profile uses 2,000 respondents; the
10k/100k stage totals are the independent reviewer/senior baseline receipts.
"""
from __future__ import annotations

import argparse
import cProfile
import json
import pstats
from collections import defaultdict
import io
from pathlib import Path
import shutil
import sys
import time
from typing import Any

HERE = Path(__file__).resolve().parent
AUTHOR_ROOT = HERE.parent
REPO = AUTHOR_ROOT.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(AUTHOR_ROOT))

from fixture_1006 import ShapeSpec, build_context
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
import rawlsing_next.pre553_source_direct_parquet_estate as estate_module
import rawlsing_next.pre553_parquet_carrier as carrier_module
import rawlsing_next.pre553_empirical_objects as objects_module
import rawlsing_next._pre553_direct_i02_sourcefree as sourcefree_module


TIMES: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
COUNTS: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
PHASE = {"current": "setup"}


def _wrap(module: Any, attribute: str, label: str) -> None:
    original = getattr(module, attribute)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        phase = PHASE["current"]
        start = time.monotonic()
        try:
            return original(*args, **kwargs)
        finally:
            TIMES[label][phase] += time.monotonic() - start
            COUNTS[label][phase] += 1

    setattr(module, attribute, wrapper)


def _wrap_phase(module: Any, attribute: str, label: str, phase: str) -> None:
    original = getattr(module, attribute)

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        previous = PHASE["current"]
        PHASE["current"] = phase
        start = time.monotonic()
        try:
            return original(*args, **kwargs)
        finally:
            TIMES[label][phase] += time.monotonic() - start
            COUNTS[label][phase] += 1
            PHASE["current"] = previous

    setattr(module, attribute, wrapper)


def _material() -> dict[str, Any]:
    return {
        "seconds": {label: dict(sorted(values.items())) for label, values in sorted(TIMES.items())},
        "calls": {label: dict(sorted(values.items())) for label, values in sorted(COUNTS.items())},
    }


def _top_profile(profile: cProfile.Profile) -> dict[str, Any]:
    stream = io.StringIO()
    stats = pstats.Stats(profile, stream=stream)
    stats.sort_stats("cumulative").print_stats(80)
    cumulative = stream.getvalue()
    stream = io.StringIO()
    stats = pstats.Stats(profile, stream=stream)
    stats.sort_stats("tottime").print_stats(60)
    exclusive = stream.getvalue()
    records = []
    for key, value in stats.stats.items():
        cc, nc, tt, ct, _callers = value
        records.append({
            "file": key[0],
            "line": key[1],
            "function": key[2],
            "primitive_calls": cc,
            "total_calls": nc,
            "tottime_seconds": tt,
            "cumtime_seconds": ct,
        })
    records.sort(key=lambda row: row["cumtime_seconds"], reverse=True)
    return {
        "cumulative_text": cumulative,
        "exclusive_text": exclusive,
        "top": records[:80],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--respondents", type=int, default=2000)
    parser.add_argument("--chunk-rows", type=int, default=512)
    parser.add_argument("--no-cprofile", action="store_true")
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    root = outdir / "estate"
    root.mkdir(mode=0o700)
    ctx = build_context(ShapeSpec(
        name="profile-writer", respondents=args.respondents,
        include_weights=True, tag="PYAT1006-PROFILE-WRITER",
    ))
    result: dict[str, Any] = {
        "schema": "PYAT1006_WRITER_PROFILE@1",
        "estimator": "DIRECT_I02_WRITER_CALL_BOUNDARIES",
        "respondents": args.respondents,
        "events": ctx.shape.event_count,
        "chunk_rows": args.chunk_rows,
        "status": "RUNNING",
    }
    path = outdir / "writer_profile.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Instrument only after context/query construction.
    for module, attribute, label in (
        (objects_module, "canonical_json", "canonical_json"),
        (objects_module, "canonicalize", "canonicalize"),
        (objects_module, "semantic_hash", "semantic_hash"),
        (carrier_module, "canonical_json", "carrier_canonical_json"),
        (carrier_module, "_field_column", "carrier_field_column"),
        (estate_module, "_object_row", "object_row"),
        (estate_module, "_row", "row"),
        (estate_module._Sink, "add", "sink_add"),
        (estate_module._Sink, "flush", "sink_flush"),
        (estate_module._IndexSink, "add", "index_add"),
        (estate_module, "_hash", "root_hash"),
        (sourcefree_module, "_insert_object", "insert_object"),
        (sourcefree_module, "validate_public_carrier_object", "validate_public_object"),
        (sourcefree_module, "_walk_authority_refs", "walk_authority_refs"),
        (sourcefree_module, "_check_relations", "check_relations"),
        (sourcefree_module, "_check_direct_relations", "check_direct_relations"),
        (sourcefree_module, "_hash_original_candidate_projection", "hash_candidate_projection"),
        (sourcefree_module, "_hash_original_replay_manifest", "hash_replay_manifest"),
        (sourcefree_module, "_logical_root", "logical_root"),
        (sourcefree_module, "canonical_json", "sourcefree_canonical_json"),
        (sourcefree_module, "semantic_hash", "sourcefree_semantic_hash"),
    ):
        _wrap(module, attribute, label)
    _wrap_phase(estate_module, "build_sourcefree_direct_i02", "direct_i02_proof", "i02_build")
    _wrap_phase(estate_module, "_verify_emitted_physical_payloads", "reread_reencode", "verify")
    _wrap_phase(estate_module, "_reconstructed_v1_release_from_certificate", "v1_header", "verify")
    profile = None if args.no_cprofile else cProfile.Profile()
    PHASE["current"] = "i02_build"
    start = time.monotonic()
    if profile is not None:
        profile.enable()
    try:
        receipt = write_direct_estate(
            ctx.direct_sections(), ctx.universe.ref, root,
            chunk_rows=args.chunk_rows,
        )
    finally:
        if profile is not None:
            profile.disable()
        PHASE["current"] = "setup"
        wall = time.monotonic() - start
    result.update({
        "wall_seconds": wall,
        "family_counts": dict(receipt.family_counts),
        "retained_bytes": receipt.retained_bytes,
        "call_boundaries": _material(),
        "cprofile": _top_profile(profile) if profile is not None else None,
        "status": "MEASURED",
        "scale_limit": (
            "call-boundary profile is 2,000 respondents; 10k and 100k stage totals "
            "come from the independent review and original baseline receipts, not "
            "from this profile run"
        ),
    })
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "respondents": args.respondents,
        "events": ctx.shape.event_count,
        "wall_seconds": wall,
        "call_boundaries": result["call_boundaries"]["seconds"],
        "top": (result["cprofile"]["top"][:15] if result["cprofile"] else None),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
