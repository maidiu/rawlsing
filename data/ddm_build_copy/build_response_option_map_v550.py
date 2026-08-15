#!/usr/bin/env python3
"""Build the V550 response-option normalization map."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_manifest import build_manifest
from data.ddm_build_copy.ddm_v550_response_options import build_response_option_map
from data.ddm_build_copy.ddm_v550_storage import connect_from_env, ensure_directories, make_run_id, write_manifest, write_table

DEFAULT_CODEBOOK_ROOT = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
DEFAULT_QUESTIONS_MASTER_DRIVERS = ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_drivers.csv"
DEFAULT_QUESTIONS_MASTER_SEMANTIC = ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_semantic.csv"
DEFAULT_STRUCTURE_REGISTER = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_structure_register.csv"
DEFAULT_TAXONOMY = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_type_taxonomy.yaml"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_REPORTS_DIR = ROOT / "data" / "ddm_build_copy" / "reports"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the V550 response-option normalization map.")
    parser.add_argument("--codebooks-root", action="append", default=[], help="Root directory containing final codebook CSVs.")
    parser.add_argument(
        "--only-codebook",
        action="append",
        default=[],
        help="Only process codebooks whose basename or full path matches this value. Repeatable.",
    )
    parser.add_argument("--questions-master-drivers", default=str(DEFAULT_QUESTIONS_MASTER_DRIVERS))
    parser.add_argument("--questions-master-semantic", default=str(DEFAULT_QUESTIONS_MASTER_SEMANTIC))
    parser.add_argument("--question-structure-register", default=str(DEFAULT_STRUCTURE_REGISTER))
    parser.add_argument("--question-type-taxonomy", default=str(DEFAULT_TAXONOMY))
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR))
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--write-csv", dest="write_csv", action="store_true", default=True)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", dest="write_parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--write-postgres", action="store_true", default=False)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--limit-questions", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(Path(args.env_file))
    run_id = args.run_id or make_run_id("v550a")
    paths = ensure_directories(Path(args.output_root), run_id)

    codebook_roots = [Path(p) for p in args.codebooks_root] if args.codebooks_root else [DEFAULT_CODEBOOK_ROOT]
    if args.verbose:
        print(f"[V550a] run_id={run_id}")
        print(f"[V550a] codebook_roots={[str(p) for p in codebook_roots]}")

    db_conn = None
    if args.db_url or os.environ.get("DATABASE_URL"):
        db_conn = connect_from_env(args.db_url, Path(args.env_file))

    try:
        if args.verbose:
            started = pd.Timestamp.utcnow()
            print(f"[V550a] starting response-option map build at {started.isoformat()}", flush=True)
            print("[V550a] stage 1/4: parse and normalize codebooks", flush=True)
        out, review, parse_manifest = build_response_option_map(
            codebook_roots=codebook_roots,
            only_codebooks=[clean for clean in args.only_codebook if clean],
            questions_master_drivers=Path(args.questions_master_drivers),
            questions_master_semantic=Path(args.questions_master_semantic) if args.questions_master_semantic else None,
            question_structure_register=Path(args.question_structure_register) if args.question_structure_register else None,
            question_type_taxonomy=Path(args.question_type_taxonomy) if args.question_type_taxonomy else None,
            db_conn=db_conn,
            limit_questions=args.limit_questions,
            verbose=args.verbose,
        )

        if args.dry_run:
            print(json.dumps(parse_manifest, indent=2, ensure_ascii=False))
            return 0

        files_written: list[str] = []
        csv_written: list[str] = []
        if args.verbose:
            print("[V550a] stage 2/4: writing canonical response-option map tables", flush=True)
        out_meta = write_table(
            out,
            paths=paths,
            table_name="response_option_map",
            layer="core",
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
            report_name="V550_response_option_map.csv",
            reports_dir=Path(args.reports_dir),
            extra_schema={"description": "Canonical response-option normalization map for V550."},
        )
        files_written.append("core/response_option_map.parquet")
        if args.write_csv:
            csv_written.append("V550_response_option_map.csv")

        if args.verbose:
            print("[V550a] stage 3/4: writing manual-review audit table", flush=True)
        review_meta = write_table(
            review,
            paths=paths,
            table_name="response_option_manual_review",
            layer="audit",
            write_csv=args.write_csv,
            write_parquet=args.write_parquet,
            report_name="V550_response_option_manual_review.csv",
            reports_dir=Path(args.reports_dir),
            extra_schema={"description": "Rows requiring manual review because codebook parsing was incomplete."},
        )
        files_written.append("audit/response_option_manual_review.parquet")
        if args.write_csv:
            csv_written.append("V550_response_option_manual_review.csv")

        read_errors = [row for row in parse_manifest.get("file_summaries", []) if row.get("status") != "ok"]
        errors = []
        if read_errors:
            errors.append("some_codebooks_failed_to_read")
        if len(out) == 0:
            errors.append("no_response_option_rows_produced")

        if args.verbose:
            print("[V550a] stage 4/4: writing manifest and promotion metadata", flush=True)
        manifest = build_manifest(
            run_id=run_id,
            version="v550a",
            stage="response_option_map",
            repo_root=ROOT,
            run_path=paths.run_path,
            input_db_used=db_conn is not None,
            source_filters=[],
            wave_filters=[],
            country_filters=[],
            thresholds={},
            script_versions={"build_response_option_map_v550.py": "v1"},
            input_row_counts=parse_manifest,
            output_row_counts={"response_option_map": len(out), "response_option_manual_review": len(review)},
            readiness_class_counts={},
            warnings=parse_manifest.get("warnings", []),
            errors=errors,
            files_written=files_written,
            csv_mirrors_written=csv_written,
            postgres_tables_written=[],
            postgres_views_written=[],
            success=not errors,
        )
        write_manifest(paths, manifest)
        if not args.dry_run and not errors:
            paths.promote_latest()
        if args.verbose:
            elapsed = pd.Timestamp.utcnow()
            print(f"[V550a] finished response-option map build at {elapsed.isoformat()}", flush=True)
            print(
                f"[V550a] summary files_scanned={parse_manifest.get('files_scanned', 0)} files_loaded={parse_manifest.get('files_loaded', 0)} option_rows={len(out)} review_rows={len(review)}",
                flush=True,
            )
            print(json.dumps(manifest, indent=2, ensure_ascii=False))
        if errors:
            return 1
        return 0
    finally:
        if db_conn is not None:
            db_conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
