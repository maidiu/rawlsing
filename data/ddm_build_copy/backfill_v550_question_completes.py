#!/usr/bin/env python3
"""Backfill missing question_universe .complete markers for a V550 shard.

This is a recovery utility for shards where question parquet outputs exist,
but some skipped-question completion markers were not written.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from data.ddm_build_copy.build_determinicity_repository_v550 import (
    ROOT,
    _build_question_list,
    _load_wave_question_mapping,
    _question_checkpoint_complete_path,
    load_dotenv,
    load_scope_manifest,
    connect_from_env,
)
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill missing V550 question completion markers.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--output-root", type=Path, default=ROOT / "data" / "ddm_repository_copy" / "v550")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_dotenv(args.env_file)
    conn = connect_from_env(args.db_url, args.env_file)
    try:
        scope_df = load_scope_manifest(conn, [args.source], [args.wave], [])
        if scope_df.empty:
            raise RuntimeError(f"No scope rows found for {args.source}/{args.wave}.")
        mapping_df = _load_wave_question_mapping(conn, args.source, args.wave)
        if mapping_df.empty:
            raise RuntimeError(f"No question mapping rows found for {args.source}/{args.wave}.")
        question_df = _build_question_list(scope_df, mapping_df, None)
        if question_df.empty:
            raise RuntimeError(f"No question rows could be built for {args.source}/{args.wave}.")

        paths = V550ShardPaths(args.output_root, args.run_id, args.shard_id)
        paths.ensure()

        created = 0
        existing = 0
        for idx, (_, qrow) in enumerate(question_df.iterrows(), start=1):
            complete_path = _question_checkpoint_complete_path(paths, idx, qrow)
            if complete_path.exists():
                existing += 1
                continue
            if not args.dry_run:
                complete_path.write_text("complete\n", encoding="utf-8")
            created += 1
            if args.verbose and created % 100 == 0:
                print(f"backfilled {created} complete markers...", flush=True)

        print(
            f"done: source={args.source} wave={args.wave} rows={len(question_df)} existing={existing} created={created} dry_run={args.dry_run}",
            flush=True,
        )
        return 0
    finally:
        try:
            conn.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
