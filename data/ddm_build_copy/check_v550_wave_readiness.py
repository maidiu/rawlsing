#!/usr/bin/env python3
"""Run V550 readiness as a standalone validation artifact."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
import sys

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_determinicity_repository_v550 import _assert_facet_ready_view_contract
from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from data.ddm_build_copy.ddm_v550_readiness import build_readiness, load_scope_manifest
from data.ddm_build_copy.ddm_v550_process_guard import claim_readiness_lock, release_readiness_lock
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths, atomic_write_json, load_env_database_url, try_connect_database, write_table

DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks"
DEFAULT_REPORTS_DIR = ROOT / "data" / "ddm_build_copy" / "reports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run V550 readiness as a standalone artifact.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR))
    parser.add_argument("--min-cell-n", type=int, default=50)
    parser.add_argument("--overwrite-shard", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--traceback-timeout-seconds",
        type=float,
        default=0.0,
        help="If set above zero, dump a traceback when verbose execution stays in one frame longer than this many seconds.",
    )
    return parser.parse_args()


def _write_table_bundle(paths: V550ShardPaths, table_name: str, df: pd.DataFrame, layer: str) -> dict[str, object]:
    return write_table(
        df,
        paths=paths,
        table_name=table_name,
        layer=layer,
        write_csv=False,
        write_parquet=True,
        reports_dir=None,
    )


def main() -> int:
    args = parse_args()
    if args.verbose:
        import faulthandler

        faulthandler.enable()
        if args.traceback_timeout_seconds > 0:
            faulthandler.dump_traceback_later(args.traceback_timeout_seconds, repeat=True)

    load_dotenv(Path(args.env_file))
    output_root = Path(args.output_root)
    paths = V550ShardPaths(root=output_root, run_id=args.run_id, shard_id=args.shard_id)
    lock_path = None
    if args.overwrite_shard:
        paths.clean()
    else:
        paths.ensure()
    lock_path = claim_readiness_lock(
        output_root,
        run_id=args.run_id,
        shard_id=args.shard_id,
        source=args.source,
        wave=args.wave,
    )

    status_path = paths.shard_path / "readiness_status.json"
    manifest_path = paths.shard_path / "readiness_manifest.json"
    atomic_write_json(
        status_path,
        {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "status": "running",
            "updated_at": pd.Timestamp.utcnow().isoformat(),
        },
    )

    progress_started = time.monotonic()
    conn = None
    try:
        db_url = load_env_database_url(Path(args.env_file), args.db_url)
        conn, err = try_connect_database(db_url)
        if conn is None:
            raise RuntimeError(f"[V550_SHARD_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")

        canonical_wave = canonical_wave_label(args.source, args.wave)
        print(f"[v550readiness +0s] loading scope manifest for {args.source}/{args.wave}", flush=True)
        scope_df = load_scope_manifest(
            conn,
            [args.source],
            [args.wave],
            [c for c in args.country if c],
            progress_started=progress_started,
            log_prefix=f"scope[{args.source}/{args.wave}]",
        )
        if scope_df.empty:
            raise RuntimeError(f"[V550_NO_SHARDS_DISCOVERED] No source/wave rows matched {args.source}/{args.wave}. Check the shard plan and live DB coverage.")

        if canonical_wave != args.wave:
            scope_df = scope_df.copy()
            scope_df["wave"] = canonical_wave

        _write_table_bundle(paths, "readiness_scope", scope_df, "core")
        print(f"[v550readiness +{time.monotonic() - progress_started:0.0f}s] verifying facet-ready view contract", flush=True)
        facet_started = time.monotonic()
        _assert_facet_ready_view_contract(conn)
        print(f"[v550readiness +{time.monotonic() - progress_started:0.0f}s] facet-ready view contract verified in {time.monotonic() - facet_started:0.1f}s", flush=True)

        country_filters = sorted({str(value) for value in scope_df["country_code"].dropna().astype(str) if str(value).strip()})
        print(f"[v550readiness +{time.monotonic() - progress_started:0.0f}s] building full readiness coverage", flush=True)
        readiness_df, pos_df, weight_df, mapping_df, legacy_df, underpowered_df = build_readiness(
            conn,
            scope_df,
            min_cell_n=args.min_cell_n,
            source_filters=[args.source],
            wave_filters=[canonical_wave],
            country_filters=country_filters,
            progress_started=progress_started,
            log_prefix=f"full_readiness[{args.source}/{args.wave}]",
        )

        counts = readiness_df["readiness_status"].value_counts(dropna=False).to_dict() if not readiness_df.empty and "readiness_status" in readiness_df.columns else {}
        outputs = [
            _write_table_bundle(paths, "substrate_readiness", readiness_df, "core"),
            _write_table_bundle(paths, "position_field_coverage", pos_df, "core"),
            _write_table_bundle(paths, "weight_coverage", weight_df, "core"),
            _write_table_bundle(paths, "mapping_status_coverage", mapping_df, "core"),
            _write_table_bundle(paths, "legacy_leak_report", legacy_df, "audit"),
            _write_table_bundle(paths, "underpowered_quarantine", underpowered_df, "audit"),
        ]

        payload: dict[str, object] = {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "source": args.source,
            "wave": args.wave,
            "country_filters": country_filters,
            "min_cell_n": args.min_cell_n,
            "scope_rows": int(len(scope_df)),
            "readiness_rows": int(len(readiness_df)),
            "position_rows": int(len(pos_df)),
            "weight_rows": int(len(weight_df)),
            "mapping_rows": int(len(mapping_df)),
            "legacy_rows": int(len(legacy_df)),
            "underpowered_rows": int(len(underpowered_df)),
            "readiness_class_counts": {str(k): int(v) for k, v in counts.items()},
            "outputs": outputs,
            "success": True,
            "updated_at": pd.Timestamp.utcnow().isoformat(),
        }
        atomic_write_json(manifest_path, payload)
        atomic_write_json(
            status_path,
            {
                "run_id": args.run_id,
                "shard_id": args.shard_id,
                "status": "success",
                "success": True,
                "updated_at": pd.Timestamp.utcnow().isoformat(),
                "manifest": str(manifest_path),
            },
        )
        print(f"[v550readiness +{time.monotonic() - progress_started:0.0f}s] readiness artifact ready: rows={len(readiness_df)} ready={int(counts.get('ready', 0))} distribution_only={int(counts.get('distribution_only', 0))} underpowered={int(counts.get('underpowered', 0))} mapping_insufficient={int(counts.get('mapping_insufficient', 0))}", flush=True)
        return 0
    except Exception as exc:
        atomic_write_json(
            status_path,
            {
                "run_id": args.run_id,
                "shard_id": args.shard_id,
                "status": "failed",
                "success": False,
                "error": str(exc),
                "updated_at": pd.Timestamp.utcnow().isoformat(),
            },
        )
        raise
    finally:
        if lock_path is not None:
            release_readiness_lock(lock_path)
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
