"""Independent R2 2k call-boundary / cProfile check of the accepted writer.

Production and fixture code are unchanged.  Wrappers only time existing calls.
The profile is a call-boundary decomposition, not a 100k extrapolation.
"""
from __future__ import annotations

import argparse
import cProfile
from collections import defaultdict
import io
import json
from pathlib import Path
import pstats
import shutil
import sys
import time
from typing import Any

REVIEW = Path(__file__).resolve().parents[1]
REPO = REVIEW.parents[1]
AUTHOR = REPO / "WORKER_RETURNS" / "PYAT1006_PHYSICAL_ECONOMICS_R1"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(AUTHOR))

from fixture_1006 import ShapeSpec, build_context
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate
import rawlsing_next.pre553_source_direct_parquet_estate as estate_module
import rawlsing_next.pre553_parquet_carrier as carrier_module
import rawlsing_next.pre553_empirical_objects as objects_module
import rawlsing_next._pre553_direct_i02_sourcefree as sourcefree_module


TIMES: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
COUNTS: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
PHASE = {"current": "setup"}


def wrap(module: Any, attribute: str, label: str) -> None:
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


def wrap_phase(module: Any, attribute: str, label: str, phase: str) -> None:
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


def material() -> dict[str, Any]:
    return {
        "seconds": {
            label: dict(sorted(values.items()))
            for label, values in sorted(TIMES.items())
        },
        "calls": {
            label: dict(sorted(values.items()))
            for label, values in sorted(COUNTS.items())
        },
    }


def top_profile(profile: cProfile.Profile) -> dict[str, Any]:
    stats = pstats.Stats(profile)
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
    return {"top": records[:80]}


def install() -> None:
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
        wrap(module, attribute, label)
    wrap_phase(
        estate_module, "build_sourcefree_direct_i02", "direct_i02_proof", "i02_build"
    )
    wrap_phase(
        estate_module, "_verify_emitted_physical_payloads", "reread_reencode", "verify"
    )
    wrap_phase(
        estate_module, "_reconstructed_v1_release_from_certificate",
        "v1_header", "verify",
    )


def run_one(outdir: Path, *, respondents: int, chunk_rows: int, profile_it: bool) -> dict[str, Any]:
    if outdir.exists():
        shutil.rmtree(outdir)
    outdir.mkdir(parents=True)
    root = outdir / "estate"
    root.mkdir(mode=0o700)
    ctx = build_context(ShapeSpec(
        name="r2-writer-profile", respondents=respondents,
        include_weights=True, tag="PYAT1006-R2-WRITER-PROFILE",
    ))
    TIMES.clear()
    COUNTS.clear()
    PHASE["current"] = "i02_build"
    profile = cProfile.Profile() if profile_it else None
    start = time.monotonic()
    if profile is not None:
        profile.enable()
    try:
        receipt = write_direct_estate(
            ctx.direct_sections(), ctx.universe.ref, root, chunk_rows=chunk_rows,
        )
    finally:
        if profile is not None:
            profile.disable()
        PHASE["current"] = "setup"
        wall = time.monotonic() - start
    result = {
        "schema": "PYAT1006_R2_WRITER_PROFILE@1",
        "respondents": respondents,
        "events": ctx.shape.event_count,
        "chunk_rows": chunk_rows,
        "profile": profile_it,
        "wall_seconds": wall,
        "retained_bytes": receipt.retained_bytes,
        "family_counts": dict(receipt.family_counts),
        "call_boundaries": material(),
        "cprofile": top_profile(profile) if profile is not None else None,
    }
    sec = result["call_boundaries"]["seconds"]
    result["derived"] = {
        "direct_i02_proof_seconds": sec.get("direct_i02_proof", {}).get("i02_build"),
        "reread_reencode_seconds": sec.get("reread_reencode", {}).get("verify"),
        "root_hash_seconds": sum(sec.get("root_hash", {}).values()),
        "row_total_seconds": sum(sec.get("row", {}).values()),
        "row_first_seconds": sec.get("row", {}).get("i02_build"),
        "row_verify_seconds": sec.get("row", {}).get("verify"),
        "sink_add_seconds": sec.get("sink_add", {}).get("i02_build"),
        "sink_flush_seconds": sec.get("sink_flush", {}).get("i02_build"),
        "insert_object_seconds": sec.get("insert_object", {}).get("i02_build"),
        "validate_public_object_seconds": sec.get("validate_public_object", {}).get("i02_build"),
        "logical_root_seconds": sec.get("logical_root", {}).get("i02_build"),
        "candidate_hash_seconds": sec.get("hash_candidate_projection", {}).get("i02_build"),
        "replay_hash_seconds": sec.get("hash_replay_manifest", {}).get("i02_build"),
        "relations_seconds": (
            sec.get("check_relations", {}).get("i02_build", 0.0)
            + sec.get("check_direct_relations", {}).get("i02_build", 0.0)
        ),
        "stage_sum_seconds": (
            (sec.get("direct_i02_proof", {}).get("i02_build", 0.0))
            + (sec.get("reread_reencode", {}).get("verify", 0.0))
            + sum(sec.get("root_hash", {}).values())
        ),
    }
    if profile is not None:
        top = result["cprofile"]["top"]
        sqlite = next(
            (row for row in top if row["function"] == "<method 'execute' of 'sqlite3.Connection' objects>"),
            None,
        )
        semantic_hash = next(
            (row for row in top if row["function"] == "semantic_hash" and row["file"].endswith("pre553_empirical_objects.py")),
            None,
        )
        semantic_projection = next(
            (row for row in top if row["function"] == "semantic_projection"),
            None,
        )
        canonicalize = next(
            (row for row in top if row["function"] == "canonicalize"),
            None,
        )
        isinstance_row = next(
            (row for row in top if row["function"] == "<built-in method builtins.isinstance>"),
            None,
        )
        result["derived"]["profile"] = {
            "sqlite_execute_tottime_seconds": sqlite["tottime_seconds"] if sqlite else None,
            "sqlite_execute_share_of_wall": (
                sqlite["tottime_seconds"] / wall if sqlite else None
            ),
            "semantic_hash_calls": semantic_hash["total_calls"] if semantic_hash else None,
            "semantic_projection_calls": (
                semantic_projection["total_calls"] if semantic_projection else None
            ),
            "first_pass_objects": COUNTS["sink_add"]["i02_build"],
            "semantic_hash_per_object": (
                semantic_hash["total_calls"] / COUNTS["sink_add"]["i02_build"]
                if semantic_hash else None
            ),
            "canonicalize_tottime_seconds": (
                canonicalize["tottime_seconds"] if canonicalize else None
            ),
            "isinstance_tottime_seconds": (
                isinstance_row["tottime_seconds"] if isinstance_row else None
            ),
        }
    (outdir / "writer_profile.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--respondents", type=int, default=2000)
    parser.add_argument("--chunk-rows", type=int, default=512)
    args = parser.parse_args(argv)
    outdir = Path(args.outdir).absolute()
    install()
    unprofiled = run_one(
        outdir / "unprofiled", respondents=args.respondents,
        chunk_rows=args.chunk_rows, profile_it=False,
    )
    profiled = run_one(
        outdir / "profiled", respondents=args.respondents,
        chunk_rows=args.chunk_rows, profile_it=True,
    )
    summary = {
        "schema": "PYAT1006_R2_WRITER_PROFILE_SUMMARY@1",
        "scale_limit": "2,000 respondents; 10k/100k values are independent baseline receipts, not extrapolations",
        "unprofiled": unprofiled,
        "profiled": profiled,
    }
    (outdir / "writer_profile_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({
        "unprofiled": {
            "wall_seconds": unprofiled["wall_seconds"],
            "derived": unprofiled["derived"],
        },
        "profiled": {
            "wall_seconds": profiled["wall_seconds"],
            "derived": profiled["derived"],
        },
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
