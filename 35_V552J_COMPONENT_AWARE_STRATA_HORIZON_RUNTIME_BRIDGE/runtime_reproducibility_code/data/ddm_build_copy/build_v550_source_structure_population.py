#!/usr/bin/env python3
"""Build the source-structure population audit for a source/wave pair."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_determinicity_repository_v550 import _assert_facet_ready_view_contract, _assert_live_contracts, _build_question_list, _load_wave_question_mapping
from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from data.ddm_build_copy.ddm_v550_readiness import load_scope_manifest
from data.ddm_build_copy.ddm_v550_source_structure import build_source_structure_population_audit, load_question_structure_register, write_source_structure_population_audit
from data.ddm_build_copy.ddm_v550_storage import load_env_database_url, try_connect_database

DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "validation"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the source-structure population audit for a source/wave pair.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--canonical-wave", default=None)
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--limit-questions", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(Path(args.env_file))
    db_url = load_env_database_url(Path(args.env_file), args.db_url)
    conn, err = try_connect_database(db_url)
    if conn is None:
        raise RuntimeError(f"[V550_SHARD_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")

    progress_started = time.monotonic()
    canonical_wave = str(args.canonical_wave or canonical_wave_label(args.source, args.wave))
    output_root = Path(args.output_root)
    validation_dir = output_root / f"{args.source}_{canonical_wave}"
    if args.overwrite and validation_dir.exists():
        for path in validation_dir.glob("*"):
            if path.is_file():
                path.unlink()
    validation_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"[v550source +0s] loading scope manifest for {args.source}/{args.wave}", flush=True)
        scope_df = load_scope_manifest(conn, [args.source], [args.wave], [c for c in args.country if c], progress_started=progress_started, log_prefix=f"scope[{args.source}/{args.wave}]")
        if scope_df.empty:
            raise RuntimeError(f"[V550_NO_SHARDS_DISCOVERED] No source/wave rows matched {args.source}/{args.wave}.")
        if canonical_wave != args.wave:
            scope_df = scope_df.copy()
            scope_df["wave"] = canonical_wave
        print(f"[v550source +{time.monotonic() - progress_started:0.0f}s] verifying facet-ready view contract", flush=True)
        _assert_facet_ready_view_contract(conn)
        wave_question_mapping_df = _load_wave_question_mapping(conn, args.source, canonical_wave)
        source_structure_register = load_question_structure_register()
        question_rows = _build_question_list(scope_df, wave_question_mapping_df, args.limit_questions)
        audit_df = build_source_structure_population_audit(question_rows, source_structure_register)
        audit_path = validation_dir / "source_structure_population_audit.csv"
        write_source_structure_population_audit(audit_df, audit_path)
        manifest = {
            "run_id": args.run_id,
            "source": args.source,
            "wave": args.wave,
            "canonical_wave": canonical_wave,
            "row_count": int(len(audit_df)),
            "source_structure_fields_joined": bool(audit_df.get("source_structure_fields_joined", pd.Series(dtype=bool)).fillna(False).any()) if not audit_df.empty else False,
            "review_required_rows": int(audit_df.get("review_required", pd.Series(dtype=bool)).fillna(False).sum()) if not audit_df.empty else 0,
            "output_file": str(audit_path),
            "success": True,
            "updated_at": pd.Timestamp.utcnow().isoformat(),
        }
        (validation_dir / "source_structure_population_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        (validation_dir / "source_structure_population_status.json").write_text(json.dumps({"run_id": args.run_id, "status": "success", "success": True, "updated_at": pd.Timestamp.utcnow().isoformat()}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[v550source +{time.monotonic() - progress_started:0.0f}s] source-structure population audit ready: rows={len(audit_df)}", flush=True)
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
