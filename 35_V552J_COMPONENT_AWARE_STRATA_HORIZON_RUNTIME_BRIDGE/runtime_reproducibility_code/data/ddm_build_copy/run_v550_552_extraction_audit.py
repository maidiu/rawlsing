#!/usr/bin/env python3
"""Standalone runner for the V550–V552 extraction audit sidecar.

Loads outputs from V550, V551, V552, and V550J stages for a given
source/wave/country slice, cross-references them into a readiness
report and numeric wrapper audit, and writes the results.

Usage:
    python3 data/ddm_build_copy/run_v550_552_extraction_audit.py \
        --run-id <run_id> \
        --source GSS --wave 1972 --country US \
        --v550-root data/ddm_repository_copy/v550 \
        --v551-root data/ddm_repository_copy/v551/runs \
        --v552-root data/ddm_repository_copy/v552/runs \
        --v550j-root data/ddm_repository_copy/v550j \
        --output-root data/ddm_repository_copy/extraction_audit
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.v550_552_extraction_audit import build_v550_552_extraction_audit_package


def _load_parquet(path: Path, *, label: str = "", verbose: bool = False) -> pd.DataFrame:
    if not path.exists():
        if verbose:
            print(f"  [{label}] not found: {path}", flush=True)
        return pd.DataFrame()
    try:
        df = pd.read_parquet(path)
        if verbose:
            print(f"  [{label}] loaded {len(df)} rows from {path}", flush=True)
        return df
    except Exception as exc:
        if verbose:
            print(f"  [{label}] error loading {path}: {exc}", flush=True)
        return pd.DataFrame()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-stage extraction audit for V550/V551/V552/V550J."
    )
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--canonical-wave", default=None,
                        help="Defaults to --wave if not set.")
    parser.add_argument("--country-code", default=None,
                        help="Defaults to --country if not set.")
    parser.add_argument("--country", default=None,
                        help="Alias for --country-code.")

    parser.add_argument("--v550-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550"))
    parser.add_argument("--v551-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v551" / "runs"))
    parser.add_argument("--v552-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v552" / "runs"))
    parser.add_argument("--v550j-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550j"))

    parser.add_argument("--output-root", default=None,
                        help="Defaults to <v550-root>/extraction_audit if not set.")
    parser.add_argument("--write-csv", action="store_true", default=False)
    parser.add_argument("--write-parquet", action="store_true", default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    progress_started = time.monotonic()

    run_id = args.run_id
    source = args.source
    wave = args.wave
    canonical_wave = args.canonical_wave or wave
    country_code = args.country_code or args.country or ""

    v550_root = Path(args.v550_root)
    v551_root = Path(args.v551_root)
    v552_root = Path(args.v552_root)
    v550j_root = Path(args.v550j_root)

    output_root = Path(args.output_root or str(v550_root / "extraction_audit"))
    out_dir = output_root / "runs" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    verbose = args.verbose

    if verbose:
        print(f"[audit] Loading stage outputs for {source} / {wave} / {country_code}", flush=True)

    # ── V550 outputs ────────────────────────────────────────────────
    v550_run_dir = v550_root / "runs" / run_id
    v550_outputs: dict[str, pd.DataFrame] = {}

    carry_forward = _load_parquet(
        v550_run_dir / "core" / "question_carry_forward_summary.parquet",
        label="v550_carry_forward", verbose=verbose,
    )
    if not carry_forward.empty:
        v550_outputs["question_carry_forward_summary"] = carry_forward

    attitude_cloud = _load_parquet(
        v550_run_dir / "clouds" / "question_response_attitude_cloud.parquet",
        label="v550_attitude_cloud", verbose=verbose,
    )
    if not attitude_cloud.empty:
        v550_outputs["question_response_attitude_cloud"] = attitude_cloud

    # ── V551 outputs ────────────────────────────────────────────────
    v551_run_dir = v551_root / run_id
    v551_outputs: dict[str, pd.DataFrame] = {}

    for table_name in [
        "numeric_wrapper_audit",
        "relation_evidence_atoms",
        "relation_review_surface",
        "blocked_signal_audit",
        "certification_candidate_bridge",
    ]:
        df = _load_parquet(
            v551_run_dir / f"{table_name}.parquet",
            label=f"v551_{table_name}", verbose=verbose,
        )
        if not df.empty or table_name in ("numeric_wrapper_audit",):
            v551_outputs[table_name] = df

    # V551 bridge (may be large; load only as fallback)
    bridge = _load_parquet(
        v551_run_dir / "certification_candidate_bridge.parquet",
        label="v551_bridge", verbose=verbose,
    )
    if not bridge.empty:
        v551_outputs["bridge"] = bridge

    # ── V552 outputs ────────────────────────────────────────────────
    v552_run_dir = v552_root / run_id
    v552_outputs: dict[str, pd.DataFrame] = {}

    directionality_gap = _load_parquet(
        v552_run_dir / "audits" / "v552_directionality_gap_surface.parquet",
        label="v552_directionality_gap", verbose=verbose,
    )
    if not directionality_gap.empty:
        v552_outputs["v552_directionality_gap_surface"] = directionality_gap

    status_pressure = _load_parquet(
        v552_run_dir / "audits" / "v552_status_pressure_review_surface.parquet",
        label="v552_status_pressure", verbose=verbose,
    )
    if not status_pressure.empty:
        v552_outputs["v552_status_pressure_review_surface"] = status_pressure

    # ── V550J outputs ───────────────────────────────────────────────
    v550j_outputs: dict[str, pd.DataFrame] = {}
    shard_id = f"{source}__{canonical_wave}"
    v550j_pattern_dir = v550j_root / "runs" / run_id / shard_id / "joint_patterns"

    review_surface = _load_parquet(
        v550j_pattern_dir / "joint_pattern_association_review_surface.parquet",
        label="v550j_review_surface", verbose=verbose,
    )
    if not review_surface.empty:
        v550j_outputs["joint_pattern_association_review_surface"] = review_surface

    # ── Build extraction audit package ──────────────────────────────
    if verbose:
        print(f"[audit] Building extraction audit package...", flush=True)

    package = build_v550_552_extraction_audit_package(
        run_id=run_id,
        source=source,
        wave=wave,
        canonical_wave=canonical_wave,
        country_code=country_code,
        v550_outputs=v550_outputs,
        v551_outputs=v551_outputs,
        v552_outputs=v552_outputs,
        v550j_outputs=v550j_outputs,
    )

    # ── Write outputs ───────────────────────────────────────────────
    written: list[dict[str, Any]] = []
    for table_name, frame in package.items():
        if frame is None or frame.empty:
            continue
        parquet_path = out_dir / f"{table_name}.parquet"
        csv_path = out_dir / f"{table_name}.csv"
        if args.write_parquet:
            frame.to_parquet(parquet_path, index=False)
        if args.write_csv:
            frame.to_csv(csv_path, index=False)
        written.append({
            "table_name": table_name,
            "rows": int(len(frame)),
            "parquet": str(parquet_path) if args.write_parquet else "",
            "csv": str(csv_path) if args.write_csv else "",
        })
        if verbose:
            print(f"  [audit] wrote {table_name}: {len(frame)} rows", flush=True)

    elapsed = time.monotonic() - progress_started

    # ── Manifest ────────────────────────────────────────────────────
    manifest = {
        "run_id": run_id,
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "written_tables": written,
        "elapsed_seconds": round(elapsed, 2),
    }
    manifest_path = out_dir / "v550_552_extraction_audit_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # ── Performance profile ──────────────────────────────────────────
    profile = {
        "run_id": run_id,
        "compiler_name": "v550_552_extraction_audit",
        "elapsed_seconds": round(elapsed, 2),
        "source": source,
        "wave": wave,
        "canonical_wave": canonical_wave,
        "country_code": country_code,
        "output_tables": [entry["table_name"] for entry in written],
        "total_output_rows": int(sum(entry["rows"] for entry in written)),
    }
    profile_path = out_dir / "v550_552_extraction_audit_performance_profile.json"
    profile_path.write_text(
        json.dumps(profile, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    if verbose:
        print(f"[audit] Done in {elapsed:.1f}s — {len(written)} tables, manifest at {manifest_path}", flush=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
