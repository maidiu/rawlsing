#!/usr/bin/env python3
"""Replay the post-question V550 shard outputs from checkpoint artifacts.

This runner does not rerun per-question execution, but it does:
- reload the respondent cache needed for downstream derived tables
- reconstruct checkpointed question-level tables
- rebuild the bridge
- write the full post-question output set and refreshed manifests

It is intended for checkpoint-driven recovery when the question-building
stage has already completed or checkpoint parquet files already exist.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_determinicity_wave_shard_v550 import _launch_readiness_from_scope, _load_readiness_bundle
from data.ddm_build_copy.ddm_v550_bridge import build_bridge_causal_summary, build_bridge_lane_audits, write_v551_bridge_index_for_shard
from data.ddm_build_copy.ddm_v550_branching import branch_nodes_rows, indicator_answer_matrix_rows, indicator_summary_rows, outlier_cohort_rows, prepare_question_frame, secondary_indicator_summary_rows
from data.ddm_build_copy.ddm_v550_clouds import BRANCH_POSITION_SIGNATURE_COLUMNS, BRANCH_RELATION_CO_SIGNATURE_COLUMNS, QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS, build_attitude_cloud_rows, build_co_signature_rows, build_position_signature_rows, should_emit_cloud_tables
from data.ddm_build_copy.ddm_v550_manifest import build_shard_manifest, utc_now
from data.ddm_build_copy.ddm_v550_position_distribution import POSITION_DISTRIBUTION_COLUMNS, build_position_distribution_rows
from data.ddm_build_copy.build_determinicity_repository_v550 import (
    CHECKPOINT_COMPLETE_SUFFIX,
    _combine_wave_checkpoint_tables,
    _log_progress,
    _load_response_option_map,
    _question_checkpoint_complete_path,
    _question_checkpoint_exists,
    _question_key,
    _question_checkpoint_path,
    _prefetch_question_rows_by_country,
    _prepare_v550_question_row_cache,
    _load_replayed_cloud_tables,
    _wave_warning_report,
    _write_json_report,
)
from data.ddm_build_copy.build_determinicity_wave_shard_v550 import _missing_question_checkpoint_keys
from data.ddm_build_copy.ddm_v550_response_options import response_semantics_contract_hash
from data.ddm_build_copy.ddm_v550_schema import V551_BRIDGE_INDEX_SCHEMA
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths, atomic_write_json, load_env_database_url, try_connect_database, write_table
from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import SharedSubstratePaths, load_shared_respondent_substrate
from data.ddm_build_copy.ddm_v550_validation import validate_v551_bridge_rows
from data.ddm_build_copy.ddm_v550_validation import validate_attitude_cloud_rows, validate_position_signature_rows, validate_relation_signature_rows

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_WRITE_CSV = False
BRIDGE_AUDIT_MAX_ROWS = 250_000
POST_ASSEMBLY_SNAPSHOT_DIRNAME = "post_assembly_state"
PIPELINE_PROCESS_TOTAL = 51
PIPELINE_PROCESS_LABELS = {
    "question_universe": 12,
    "question_use_contract": 12,
    "answer_distribution": 13,
    "country_answer_distribution": 14,
    "position_indicator_summary": 15,
    "indicator_answer_matrix": 16,
    "outlier_cohort_summary": 17,
    "secondary_indicator_summary": 18,
    "recursive_branch_nodes": 19,
    "branch_position_signature": 20,
    "branch_relation_co_signature": 20,
    "branch_co_signature": 20,
    "question_response_attitude_cloud": 21,
    "mapping_gap_report": 22,
    "response_option_manual_review": 45,
    "cloud_exclusion_audit": 46,
    "scope_manifest": 47,
    "substrate_readiness": 48,
    "position_field_coverage": 49,
    "weight_coverage": 50,
    "mapping_status_coverage": 51,
    "legacy_leak_report": 52,
    "underpowered_quarantine": 53,
}



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rebuild V550 bridge artifacts directly from completed checkpoints.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--source", default=None)
    parser.add_argument("--wave", default=None)
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--response-option-map", default=None)
    parser.add_argument("--readiness-artifact", default=None)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--reports-dir", default=str(ROOT / "data" / "ddm_build_copy" / "reports"))
    parser.add_argument("--min-cell-n", type=int, default=50)
    parser.add_argument("--min-answer-n", type=int, default=50)
    parser.add_argument("--min-branch-n", type=int, default=50)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--v550-prepared-substrate-mode", default="off", choices=("off", "country", "chunked"))
    parser.add_argument("--prepared-substrate-root", default=None, help="Shared respondent substrate root. Defaults to shard checkpoints/respondent_substrate.")
    parser.add_argument("--forbid-database-access", action="store_true", help="Reject recovery paths that would query PostgreSQL.")
    parser.add_argument("--cloud-mode", default="auto", choices=("auto", "full", "off", "share"))
    parser.add_argument("--cloud-max-branch-rows", type=int, default=1000)
    parser.add_argument("--cloud-max-branch-share", type=float, default=None)
    parser.add_argument("--write-csv", action="store_true", default=DEFAULT_WRITE_CSV)
    parser.add_argument(
        "--resume-final-write-only",
        action="store_true",
        help="Reload a persisted post-assembly snapshot and rewrite the final output tables without recomputing the heavy intermediates.",
    )
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--refresh-manifest",
        action="store_true",
        default=True,
        help="Rewrite shard_manifest.json with the rebuilt bridge counts.",
    )
    parser.add_argument(
        "--no-refresh-manifest",
        dest="refresh_manifest",
        action="store_false",
        help="Do not rewrite shard_manifest.json.",
    )
    parser.add_argument(
        "--refresh-status",
        action="store_true",
        default=True,
        help="Rewrite shard_status.json after refreshing the manifest.",
    )
    parser.add_argument(
        "--no-refresh-status",
        dest="refresh_status",
        action="store_false",
        help="Do not rewrite shard_status.json.",
    )
    return parser.parse_args()


def _load_shared_substrate_cache(root: Path) -> dict[str, pd.DataFrame]:
    cache: dict[str, pd.DataFrame] = {}
    for manifest_path in sorted(root.glob("source=*/wave=*/country_code=*/v550_shared_respondent_substrate_manifest.json")):
        substrate_root = manifest_path.parent
        paths = SharedSubstratePaths(
            root=substrate_root,
            parquet_path=substrate_root / "v550_shared_respondent_substrate.parquet",
            schema_path=substrate_root / "v550_shared_respondent_substrate.schema.json",
            manifest_path=manifest_path,
            validation_path=substrate_root / "v550_shared_respondent_substrate_validation.json",
            complete_path=substrate_root / "COMPLETE",
        )
        frame, _manifest, _validation = load_shared_respondent_substrate(paths)
        if "country_code_norm" in frame.columns:
            country_values = sorted({str(value).strip().upper() for value in frame["country_code_norm"].dropna() if str(value).strip()})
        else:
            country_values = sorted({str(value).strip().upper() for value in frame.get("country_code", pd.Series(dtype="object")).dropna() if str(value).strip()})
        if "var_code" in frame.columns:
            frame = frame.copy()
            frame["var_code"] = frame["var_code"].astype(str).str.upper()
            frame = frame.set_index("var_code", drop=False)
        for country_code in country_values:
            cache[country_code] = frame
    return cache


def _load_checkpoint_frame(table_dir: Path) -> pd.DataFrame:
    paths = sorted(table_dir.glob("*.parquet"))
    if not paths:
        return pd.DataFrame()
    frames = [pd.read_parquet(path) for path in paths]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def _question_universe_qdir(paths: V550ShardPaths) -> Path:
    return paths.checkpoints / "question_tables" / "question_universe"


def _question_universe_checkpoint_count(paths: V550ShardPaths) -> int:
    qdir = _question_universe_qdir(paths)
    if not qdir.exists():
        return 0
    return len(list(qdir.glob("*.parquet")))


def _question_rows_from_question_universe_checkpoints(paths: V550ShardPaths) -> pd.DataFrame:
    qdir = _question_universe_qdir(paths)
    paths_list = sorted(qdir.glob("*.parquet"))
    if not paths_list:
        raise FileNotFoundError(f"No question_universe checkpoint files found in {qdir}")
    frames: list[pd.DataFrame] = []
    for path in paths_list:
        frame = pd.read_parquet(path)
        if frame.empty:
            continue
        frame = frame.copy()
        try:
            checkpoint_index = int(path.name.split("__", 1)[0])
        except Exception:
            checkpoint_index = None
        frame["checkpoint_index"] = checkpoint_index
        frame["checkpoint_file"] = path.name
        frames.append(frame)
    if not frames:
        raise FileNotFoundError(f"No question_universe checkpoint files found in {qdir}")
    question_rows = pd.concat(frames, ignore_index=True, sort=False)
    return question_rows.reset_index(drop=True)


def _discover_latest_complete_shard_root(output_root: Path, shard_id: str) -> tuple[str, str, int] | None:
    shard_runs_root = output_root / "shard_runs"
    if not shard_runs_root.exists():
        return None
    candidates: list[tuple[float, str, str, int]] = []
    for run_dir in shard_runs_root.iterdir():
        if not run_dir.is_dir():
            continue
        candidate = run_dir / shard_id
        if not candidate.is_dir():
            continue
        qdir = candidate / "checkpoints" / "question_tables" / "question_universe"
        count = len(list(qdir.glob("*.parquet"))) if qdir.exists() else 0
        if count <= 0:
            continue
        score = max(candidate.stat().st_mtime, qdir.stat().st_mtime if qdir.exists() else candidate.stat().st_mtime)
        candidates.append((score, run_dir.name, shard_id, count))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    _, run_id, discovered_shard_id, count = candidates[0]
    return run_id, discovered_shard_id, count


def _resolve_source_paths(output_root: Path, run_id: str, shard_id: str) -> tuple[V550ShardPaths, str]:
    requested_paths = V550ShardPaths(root=output_root, run_id=run_id, shard_id=shard_id)
    if _question_universe_checkpoint_count(requested_paths) > 0:
        return requested_paths, "requested"
    discovered = _discover_latest_complete_shard_root(output_root, shard_id)
    if discovered is None:
        raise FileNotFoundError(
            f"No completed question_universe checkpoints found for shard_id={shard_id} under {output_root / 'shard_runs'}"
        )
    discovered_run_id, discovered_shard_id, count = discovered
    return V550ShardPaths(root=output_root, run_id=discovered_run_id, shard_id=discovered_shard_id), f"discovered({count} question_universe checkpoints)"


def _bridge_table_from_checkpoints(paths: V550ShardPaths, table_name: str, question_rows: pd.DataFrame, *, verbose: bool = False, progress_started: float | None = None) -> pd.DataFrame:
    return _combine_wave_checkpoint_tables(paths, table_name, question_rows, progress_started if verbose else None)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _process_label(table_name: str) -> str:
    idx = PIPELINE_PROCESS_LABELS.get(table_name)
    return f" ({idx}/{PIPELINE_PROCESS_TOTAL})" if idx else ""


def _output_table_path(paths: V550ShardPaths, table_name: str, layer: str) -> Path:
    layer_dir = {
        "core": paths.core,
        "distributions": paths.distributions,
        "determinicity": paths.determinicity,
        "clouds": paths.clouds,
        "audit": paths.audit,
        "schemas": paths.schemas,
    }.get(layer, paths.core)
    return layer_dir / f"{table_name}.parquet"


def _post_assembly_snapshot_dir(paths: V550ShardPaths) -> Path:
    return paths.checkpoints / POST_ASSEMBLY_SNAPSHOT_DIRNAME


def _write_post_assembly_snapshot(paths: V550ShardPaths, tables: dict[str, pd.DataFrame]) -> None:
    snapshot_dir = _post_assembly_snapshot_dir(paths)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    meta: dict[str, Any] = {"tables": {}}
    for table_name, frame in tables.items():
        if frame is None:
            continue
        path = snapshot_dir / f"{table_name}.parquet"
        frame.to_parquet(path, index=False)
        meta["tables"][table_name] = {"rows": int(len(frame)), "path": str(path)}
    _write_json_report(snapshot_dir / "snapshot_manifest.json", meta)


def _load_post_assembly_snapshot(paths: V550ShardPaths) -> dict[str, pd.DataFrame] | None:
    snapshot_dir = _post_assembly_snapshot_dir(paths)
    manifest_path = snapshot_dir / "snapshot_manifest.json"
    if not manifest_path.exists():
        return None
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    tables = payload.get("tables", {})
    loaded: dict[str, pd.DataFrame] = {}
    for table_name in tables:
        table_path = snapshot_dir / f"{table_name}.parquet"
        if not table_path.exists():
            return None
        loaded[table_name] = pd.read_parquet(table_path)
    return loaded


def _load_existing_bridge_meta_and_frame(shard_paths: V550ShardPaths) -> tuple[dict[str, Any], pd.DataFrame, list[dict[str, Any]]]:
    bridge_path = shard_paths.bridge / "v551_bridge_index.parquet"
    warnings_path = shard_paths.bridge / "v551_bridge_warnings.json"
    if not bridge_path.exists():
        raise FileNotFoundError(f"Existing bridge parquet is required for resume-final-write-only: {bridge_path}")
    bridge_frame = pd.read_parquet(bridge_path)
    bridge_warnings: dict[str, Any] = {}
    if warnings_path.exists():
        try:
            bridge_warnings = json.loads(warnings_path.read_text(encoding="utf-8"))
        except Exception:
            bridge_warnings = {}
    eligible_rows = int(bridge_frame["v551_eligible"].fillna(False).astype(bool).sum()) if ("v551_eligible" in bridge_frame.columns and not bridge_frame.empty) else 0
    bridge_meta = {
        "bridge_rows": int(bridge_warnings.get("bridge_rows", len(bridge_frame))),
        "eligible_rows": int(bridge_warnings.get("eligible_rows", eligible_rows)),
        "excluded_rows": int(bridge_warnings.get("excluded_rows", max(int(len(bridge_frame)) - eligible_rows, 0))),
        "numeric_only_label_excluded_rows": int(bridge_warnings.get("numeric_only_label_excluded_rows", 0)),
    }
    bridge_issues = validate_v551_bridge_rows(bridge_frame)
    return bridge_meta, bridge_frame, bridge_issues


def _load_scope_frame(shard_paths: V550ShardPaths, readiness_scope: pd.DataFrame | None) -> pd.DataFrame:
    scope_path = shard_paths.shard_path / "shard_scope.parquet"
    if scope_path.exists():
        scope_df = pd.read_parquet(scope_path)
        if not scope_df.empty:
            return scope_df
    if readiness_scope is not None and not readiness_scope.empty:
        return readiness_scope.copy()
    return pd.DataFrame()


def _resolve_readiness_root(output_root: Path, run_id: str, shard_id: str, requested: str | None) -> Path | None:
    candidates = []
    if requested:
        candidates.append(Path(requested))
    candidates.append(output_root / "readiness_checks" / "shard_runs" / run_id / shard_id)
    candidates.append(ROOT / "data" / "ddm_repository_copy" / "v550" / "readiness_checks" / "shard_runs" / run_id / shard_id)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def main() -> int:
    args = parse_args()
    output_root = Path(args.output_root)
    shard_paths, source_mode = _resolve_source_paths(output_root, args.run_id, args.shard_id)
    shard_paths.ensure()
    load_dotenv(Path(args.env_file))

    progress_started = time.monotonic() if args.verbose else None
    if args.verbose:
        _log_progress(progress_started, f"loading question_universe checkpoints ({source_mode})")

    question_rows = _question_rows_from_question_universe_checkpoints(shard_paths)
    missing_checkpoints = [q for q in _missing_question_checkpoint_keys(shard_paths, question_rows) if q]
    if missing_checkpoints and args.verbose:
        _log_progress(
            progress_started,
            "missing question completion sentinels detected; proceeding from available checkpoint parquet files: "
            + ", ".join(missing_checkpoints[:10])
            + ("" if len(missing_checkpoints) <= 10 else f" ... (+{len(missing_checkpoints) - 10} more)"),
        )
    if args.verbose:
        _log_progress(progress_started, f"question checkpoints verified: {len(question_rows)} questions")

    source = str(args.source or (question_rows["source"].dropna().astype(str).iloc[0] if "source" in question_rows.columns and not question_rows.empty else ""))
    wave = str(args.wave or (question_rows["canonical_wave"].dropna().astype(str).iloc[0] if "canonical_wave" in question_rows.columns and not question_rows.empty else ""))
    countries = sorted({str(value) for value in question_rows["country_code"].dropna().astype(str) if str(value).strip()}) if "country_code" in question_rows.columns else []

    readiness_root = _resolve_readiness_root(output_root, args.run_id, args.shard_id, args.readiness_artifact)
    readiness_df = pos_df = weight_df = mapping_df = legacy_df = underpowered_df = readiness_scope_df = pd.DataFrame()
    if readiness_root is not None:
        try:
            readiness_df, pos_df, weight_df, mapping_df, legacy_df, underpowered_df, readiness_scope_df = _load_readiness_bundle(readiness_root)
        except Exception:
            readiness_df = pos_df = weight_df = mapping_df = legacy_df = underpowered_df = readiness_scope_df = pd.DataFrame()

    scope_df = _load_scope_frame(shard_paths, readiness_scope_df)
    if scope_df.empty:
        raise FileNotFoundError("Could not load shard scope for checkpoint replay.")

    core_tables_written: dict[str, int] = {}
    wave_tables: dict[str, pd.DataFrame]
    response_review = pd.DataFrame()
    question_row_cache = pd.DataFrame()
    respondent_cache_source = "not_loaded"
    respondent_cache_db_used = False
    bridge_meta: dict[str, Any]
    bridge_frame = pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
    bridge_issues: list[dict[str, Any]] = []

    if args.resume_final_write_only:
        snapshot_tables = _load_post_assembly_snapshot(shard_paths)
        if snapshot_tables is None:
            raise RuntimeError(
                "resume-final-write-only requires an existing post_assembly_state snapshot. "
                "Run once without --resume-final-write-only to seed checkpoints/post_assembly_state, then rerun with resume."
            )
        if args.verbose:
            _log_progress(progress_started, f"loaded post-assembly snapshot: {', '.join(sorted(snapshot_tables.keys()))}")
        wave_tables = snapshot_tables
        if "branch_co_signature" not in wave_tables and "branch_relation_co_signature" in wave_tables:
            wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
        if "position_distribution" not in wave_tables:
            raise RuntimeError("resume-final-write-only requires a post_assembly_state snapshot containing position_distribution.")
        if "branch_position_signature" not in wave_tables:
            wave_tables["branch_position_signature"] = pd.DataFrame(columns=BRANCH_POSITION_SIGNATURE_COLUMNS)
        if "branch_relation_co_signature" not in wave_tables:
            wave_tables["branch_relation_co_signature"] = pd.DataFrame(columns=BRANCH_RELATION_CO_SIGNATURE_COLUMNS)
        if "question_response_attitude_cloud" not in wave_tables:
            wave_tables["question_response_attitude_cloud"] = pd.DataFrame(columns=QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS)
        bridge_meta, bridge_frame, bridge_issues = _load_existing_bridge_meta_and_frame(shard_paths)
    else:
        response_map = _load_response_option_map(args.response_option_map) if args.response_option_map else pd.DataFrame()
        if response_map.empty:
            for fallback in [
                Path(args.reports_dir) / "V550_response_option_map.csv",
                Path(args.reports_dir) / "response_option_map.csv",
                ROOT / "data" / "ddm_build_copy" / "reports" / "V550_response_option_map.csv",
                ROOT / "data" / "ddm_build_copy" / "reports" / "response_option_map.csv",
            ]:
                if fallback.exists():
                    response_map = pd.read_csv(fallback, low_memory=False)
                    break
        response_semantics_contract = response_semantics_contract_hash(response_map) if not response_map.empty else ""
        semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        if not response_map.empty:
            for row in response_map.itertuples(index=False):
                semantics_lookup[(str(getattr(row, "source", "")), str(getattr(row, "wave", "")), str(getattr(row, "var_name", "")), str(getattr(row, "value_code_normalized", "")) or str(getattr(row, "value_label_clean", "")))] = row._asdict()

        if args.verbose:
            _log_progress(progress_started, "loading respondent cache for downstream outputs")
        substrate_root = Path(args.prepared_substrate_root) if args.prepared_substrate_root else shard_paths.respondent_substrate
        question_row_cache = _load_shared_substrate_cache(substrate_root)
        if not question_row_cache:
            if args.forbid_database_access:
                raise RuntimeError("V550_RECOVERY_DATABASE_ACCESS_FORBIDDEN: shared respondent substrate is required")
            conn = None
            try:
                db_url = load_env_database_url(Path(args.env_file), args.db_url)
                if not db_url:
                    raise RuntimeError("DATABASE_URL is missing. Provide --db-url or a valid --env-file.")
                conn, err = try_connect_database(db_url)
                if conn is None:
                    raise RuntimeError(f"Could not connect to Postgres using --db-url/--env-file. Original error: {err}")
                question_row_cache = _prefetch_question_rows_by_country(conn, question_rows, progress_started)
                respondent_cache_source = "postgres_legacy_replay"
                respondent_cache_db_used = True
                question_row_cache, _prepared_stats = _prepare_v550_question_row_cache(
                    question_row_cache,
                    semantics_lookup,
                    response_semantics_contract_hash=response_semantics_contract,
                    mode=args.v550_prepared_substrate_mode,
                    progress_started=progress_started,
                )
            finally:
                if conn is not None:
                    try:
                        conn.close()
                    except Exception:
                        pass
        else:
            respondent_cache_source = "shared_respondent_substrate"
            respondent_cache_db_used = False
            if args.verbose:
                _log_progress(progress_started, f"loaded shared respondent substrate cache: countries={len(question_row_cache)}")

        if args.verbose:
            _log_progress(progress_started, "loading checkpoint tables for core/bridge/post-question rebuild")

        core_question_universe = _combine_wave_checkpoint_tables(shard_paths, "question_universe", question_rows, progress_started if args.verbose else None)
        core_question_use_contract = _combine_wave_checkpoint_tables(shard_paths, "question_use_contract", question_rows, progress_started if args.verbose else None)
        if core_question_universe.empty:
            core_question_universe = pd.DataFrame(columns=question_rows.columns)
        if core_question_use_contract.empty:
            core_question_use_contract = pd.DataFrame()

        for table_name, frame in [
            ("question_universe", core_question_universe),
            ("question_use_contract", core_question_use_contract),
        ]:
            write_table(
                frame,
                paths=shard_paths,
                table_name=table_name,
                layer="core",
                write_csv=args.write_csv,
                write_parquet=True,
                report_name=f"V550_{table_name}.csv",
                reports_dir=Path(args.reports_dir),
                extra_schema={"description": f"Rebuilt V550 {table_name} from completed checkpoints."},
            )
            core_tables_written[table_name] = int(len(frame))
            if args.verbose:
                _log_progress(progress_started, f"core table rebuilt: {table_name} ({len(frame)} rows)")

        wave_tables = {
            "question_universe": question_rows,
            "question_use_contract": _combine_wave_checkpoint_tables(shard_paths, "question_use_contract", question_rows, progress_started if args.verbose else None),
            "answer_distribution": _combine_wave_checkpoint_tables(shard_paths, "answer_distribution", question_rows, progress_started if args.verbose else None),
            "country_answer_distribution": _combine_wave_checkpoint_tables(shard_paths, "country_answer_distribution", question_rows, progress_started if args.verbose else None),
            "position_indicator_summary": _combine_wave_checkpoint_tables(shard_paths, "position_indicator_summary", question_rows, progress_started if args.verbose else None),
            "indicator_answer_matrix": _combine_wave_checkpoint_tables(shard_paths, "indicator_answer_matrix", question_rows, progress_started if args.verbose else None),
            "outlier_cohort_summary": _combine_wave_checkpoint_tables(shard_paths, "outlier_cohort_summary", question_rows, progress_started if args.verbose else None),
            "secondary_indicator_summary": _combine_wave_checkpoint_tables(shard_paths, "secondary_indicator_summary", question_rows, progress_started if args.verbose else None),
            "recursive_branch_nodes": _combine_wave_checkpoint_tables(shard_paths, "recursive_branch_nodes", question_rows, progress_started if args.verbose else None),
            "branch_position_signature": _combine_wave_checkpoint_tables(shard_paths, "branch_position_signature", question_rows, progress_started if args.verbose else None),
            "branch_relation_co_signature": _combine_wave_checkpoint_tables(shard_paths, "branch_relation_co_signature", question_rows, progress_started if args.verbose else None),
            "branch_co_signature": pd.DataFrame(),
            "question_response_attitude_cloud": _combine_wave_checkpoint_tables(shard_paths, "question_response_attitude_cloud", question_rows, progress_started if args.verbose else None),
            "mapping_gap_report": _combine_wave_checkpoint_tables(shard_paths, "mapping_gap_report", question_rows, progress_started if args.verbose else None),
        }
        wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
        if wave_tables["branch_position_signature"].empty:
            wave_tables["branch_position_signature"] = pd.DataFrame(columns=BRANCH_POSITION_SIGNATURE_COLUMNS)
        if wave_tables["branch_relation_co_signature"].empty:
            wave_tables["branch_relation_co_signature"] = pd.DataFrame(columns=BRANCH_RELATION_CO_SIGNATURE_COLUMNS)
        if wave_tables["question_response_attitude_cloud"].empty:
            wave_tables["question_response_attitude_cloud"] = pd.DataFrame(columns=QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS)

        position_distribution_df = build_position_distribution_rows(
            question_row_cache,
            run_id=args.run_id,
            shard_id=args.shard_id,
            source=source,
            source_family=source,
            wave=wave,
            canonical_wave=wave,
        )
        wave_tables["position_distribution"] = position_distribution_df if not position_distribution_df.empty else pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)

        replayed_cloud_tables = _load_replayed_cloud_tables(shard_paths, progress_started)
        if replayed_cloud_tables is not None:
            wave_tables["question_response_attitude_cloud"] = replayed_cloud_tables
            wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
            if args.verbose:
                _log_progress(progress_started, f"using replayed cloud outputs: question_response_attitude_cloud={len(replayed_cloud_tables)} branch_co_signature=relation_alias")

        snapshot_tables = _load_post_assembly_snapshot(shard_paths)
        if snapshot_tables is not None:
            if args.verbose:
                _log_progress(progress_started, f"overlaying post-assembly snapshot tables: {', '.join(sorted(snapshot_tables.keys()))}")
            for table_name, frame in snapshot_tables.items():
                wave_tables[table_name] = frame

        _write_post_assembly_snapshot(shard_paths, wave_tables)

    if readiness_df.empty and pos_df.empty and weight_df.empty and mapping_df.empty and legacy_df.empty and underpowered_df.empty:
        readiness_df, pos_df, weight_df, mapping_df, legacy_df, underpowered_df = _launch_readiness_from_scope(scope_df)

    if args.verbose:
        _log_progress(
            progress_started,
            "bridge inputs ready from checkpoints 1/11: "
            + ", ".join(
                f"{name}={len(frame)}"
                for name, frame in wave_tables.items()
                if name in {
                    "question_universe",
                    "answer_distribution",
                    "country_answer_distribution",
                    "position_indicator_summary",
                    "indicator_answer_matrix",
                    "outlier_cohort_summary",
                    "secondary_indicator_summary",
                    "recursive_branch_nodes",
                    "branch_position_signature",
                    "branch_relation_co_signature",
                    "branch_co_signature",
                    "question_response_attitude_cloud",
                    "mapping_gap_report",
                }
            ),
        )

    bridge_path = shard_paths.bridge / "v551_bridge_index.parquet"
    if not args.resume_final_write_only:
        bridge_meta = write_v551_bridge_index_for_shard(
            wave_tables,
            run_id=args.run_id,
            shard_id=args.shard_id,
            bridge_path=bridge_path,
            csv_path=shard_paths.csv_mirrors / "v551_bridge_index.csv",
            write_csv=args.write_csv,
            progress_started=progress_started,
            directionality_authority_dir=ROOT / "data" / "ddm_build_copy" / "directionality_authority",
            survey_family=source,
            canonical_wave=wave,
        )
        bridge_frame = pd.read_parquet(bridge_path) if bridge_path.exists() else pd.DataFrame(columns=V551_BRIDGE_INDEX_SCHEMA["required_columns"])
        bridge_issues = validate_v551_bridge_rows(bridge_frame)
        bridge_warnings = {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "bridge_rows": int(bridge_meta["bridge_rows"]),
            "eligible_rows": int(bridge_meta["eligible_rows"]),
            "excluded_rows": int(bridge_meta["excluded_rows"]),
            "numeric_only_label_excluded_rows": int(bridge_meta.get("numeric_only_label_excluded_rows", 0)),
            "issues": bridge_issues,
        }

        (shard_paths.bridge / "v551_bridge_index.schema.json").write_text(
            json.dumps({"row_count": bridge_meta["bridge_rows"], "columns": list(V551_BRIDGE_INDEX_SCHEMA["required_columns"])}, indent=2),
            encoding="utf-8",
        )
        _write_json_report(shard_paths.bridge / "v551_bridge_warnings.json", bridge_warnings)
        (shard_paths.bridge / "v551_bridge_validation_report.json").write_text(json.dumps({"issues": bridge_issues}, indent=2), encoding="utf-8")

        bridge_causal_summary = build_bridge_causal_summary(bridge_frame)
        _write_json_report(shard_paths.bridge / "v551_bridge_causal_summary.json", bridge_causal_summary)

        if int(bridge_meta["bridge_rows"]) <= BRIDGE_AUDIT_MAX_ROWS:
            bridge_audits = build_bridge_lane_audits(bridge_frame)
            for audit_name, audit_frame in bridge_audits.items():
                audit_path = shard_paths.bridge / f"{audit_name}.csv"
                audit_frame.to_csv(audit_path, index=False)
        else:
            _write_json_report(
                shard_paths.bridge / "v551_bridge_audit_summary.json",
                {
                    "run_id": args.run_id,
                    "shard_id": args.shard_id,
                    "bridge_rows": int(bridge_meta["bridge_rows"]),
                    "eligible_rows": int(bridge_meta["eligible_rows"]),
                    "excluded_rows": int(bridge_meta["excluded_rows"]),
                    "bridge_audit_mode": "summary_only",
                    "bridge_audit_threshold": BRIDGE_AUDIT_MAX_ROWS,
                    "note": "Row-level bridge audits skipped because the bridge exceeded the audit threshold; summary-only mode preserves validation and manifest outputs without materializing the large audit tables.",
                },
            )
    else:
        if args.verbose:
            _log_progress(progress_started, f"reusing existing bridge artifacts from {bridge_path}")

    cloud_exclusion_rows: list[dict[str, Any]] = []
    validator_map = {
        "branch_position_signature": validate_position_signature_rows,
        "branch_relation_co_signature": validate_relation_signature_rows,
        "branch_co_signature": validate_relation_signature_rows,
        "question_response_attitude_cloud": validate_attitude_cloud_rows,
    }
    for table_name, validator in validator_map.items():
        frame = wave_tables.get(table_name, pd.DataFrame())
        if args.verbose:
            _log_progress(progress_started, f"validating cloud exclusions for {table_name}: {len(frame)} rows")
        for issue in validator(frame):
            cloud_exclusion_rows.append(
                {
                    "run_id": args.run_id,
                    "shard_id": args.shard_id,
                    "table_name": table_name,
                    "issue": issue,
                    "severity": "high",
                    "row_count": int(len(frame)),
                }
            )
    cloud_exclusion_audit = pd.DataFrame(cloud_exclusion_rows, columns=["run_id", "shard_id", "table_name", "issue", "severity", "row_count"])
    wave_tables["cloud_exclusion_audit"] = cloud_exclusion_audit

    wave_warnings, wave_summary = _wave_warning_report(
        run_id=args.run_id,
        wave_index=1,
        wave_total=1,
        wave_source=source,
        wave_wave=wave,
        wave_question_rows=question_rows,
        wave_readiness_df=readiness_df,
        wave_weight_df=weight_df,
        wave_mapping_df=mapping_df,
        wave_legacy_df=legacy_df,
        wave_underpowered_df=underpowered_df,
        wave_tables=wave_tables,
        response_review=response_review,
    )
    _write_json_report(shard_paths.warnings_path, wave_summary)

    if not args.resume_final_write_only:
        _write_post_assembly_snapshot(shard_paths, wave_tables)

    _log_progress(progress_started, "assembling final output tables 32/51")
    outputs: list[str] = []
    row_counts: dict[str, int] = {}
    output_tables = [
        ("question_universe", wave_tables["question_universe"], "core"),
        ("question_use_contract", wave_tables["question_use_contract"], "core"),
        ("position_distribution", wave_tables["position_distribution"], "determinicity"),
        ("answer_distribution", wave_tables["answer_distribution"], "distributions"),
        ("country_answer_distribution", wave_tables["country_answer_distribution"], "distributions"),
        ("position_indicator_summary", wave_tables["position_indicator_summary"], "determinicity"),
        ("indicator_answer_matrix", wave_tables["indicator_answer_matrix"], "determinicity"),
        ("outlier_cohort_summary", wave_tables["outlier_cohort_summary"], "determinicity"),
        ("secondary_indicator_summary", wave_tables["secondary_indicator_summary"], "determinicity"),
        ("recursive_branch_nodes", wave_tables["recursive_branch_nodes"], "determinicity"),
        ("branch_position_signature", wave_tables["branch_position_signature"], "clouds"),
        ("branch_relation_co_signature", wave_tables["branch_relation_co_signature"], "clouds"),
        ("branch_co_signature", wave_tables["branch_co_signature"], "clouds"),
        ("question_response_attitude_cloud", wave_tables["question_response_attitude_cloud"], "clouds"),
        ("mapping_gap_report", wave_tables["mapping_gap_report"], "audit"),
        ("response_option_manual_review", response_review, "audit"),
        ("cloud_exclusion_audit", wave_tables["cloud_exclusion_audit"], "audit"),
        ("scope_manifest", scope_df, "core"),
        ("substrate_readiness", readiness_df, "core"),
        ("position_field_coverage", pos_df, "core"),
        ("weight_coverage", weight_df, "core"),
        ("mapping_status_coverage", mapping_df, "core"),
        ("legacy_leak_report", legacy_df, "audit"),
        ("underpowered_quarantine", underpowered_df, "audit"),
    ]
    for output_idx, (table_name, frame, layer) in enumerate(output_tables, start=1):
        if frame is None:
            continue
        write_started = time.monotonic()
        _log_progress(progress_started, f"writing {output_idx}/{len(output_tables)} {layer}/{table_name}{_process_label(table_name)} ({len(frame)} rows)")
        meta = write_table(
            frame,
            paths=shard_paths,
            table_name=table_name,
            layer=layer,
            write_csv=args.write_csv,
            write_parquet=True,
            report_name=f"V550_{table_name}.csv",
            reports_dir=Path(args.reports_dir),
            extra_schema={"description": f"V550 shard {table_name} output."},
        )
        outputs.append(meta["parquet_path"])
        row_counts[table_name] = len(frame)
        _log_progress(progress_started, f"finished writing {output_idx}/{len(output_tables)} {layer}/{table_name}{_process_label(table_name)} in {time.monotonic() - write_started:0.1f}s")

    all_questions_completed = True
    high_severity_warning = any(str(item.get("severity", "")).lower() == "high" for item in wave_warnings)
    bridge_ok = not bool(bridge_issues)
    manifest = build_shard_manifest(
        run_id=args.run_id,
        shard_id=args.shard_id,
        source=source,
        source_family=source,
        wave=wave,
        canonical_wave=wave,
        created_at=utc_now(),
        completed_at=utc_now(),
        success=all_questions_completed,
        output_root=output_root,
        inputs={
            "checkpoint_replay": True,
            "db_used": respondent_cache_db_used,
            "respondent_cache_source": respondent_cache_source,
            "response_option_map": args.response_option_map or "built",
            "filters": {"country": countries},
        },
        rows_by_table=row_counts,
        warnings=[f"{w['wave_source']} {w['wave']}: {w['code']} - {w['message']}" for w in wave_warnings],
        errors=[],
        outputs=outputs,
        bridge_rows=int(bridge_meta["bridge_rows"]),
        v551_eligible_count=int(bridge_meta["eligible_rows"]),
        v551_excluded_count=int(bridge_meta["excluded_rows"]),
        promotable=all_questions_completed and bridge_ok and cloud_exclusion_audit.empty and not high_severity_warning,
    )
    manifest["question_response_attitude_cloud_status"] = "disabled_until_cross_question_engine" if wave_tables["question_response_attitude_cloud"].empty else "prototype_diagnostic"
    manifest["branch_position_signature_status"] = "empty_no_position_features" if wave_tables["branch_position_signature"].empty else "enabled_diagnostic"
    manifest["branch_relation_co_signature_status"] = "disabled_no_contract_allowlist" if wave_tables["branch_relation_co_signature"].empty else "enabled_contract_gated"
    manifest["branch_co_signature_status"] = "compatibility_relation_only_alias_or_disabled" if wave_tables["branch_co_signature"].empty else "relation_only_compatibility_alias"
    manifest["position_distribution_rows"] = int(len(wave_tables["position_distribution"]))
    atomic_write_json(shard_paths.manifest_path, manifest)
    atomic_write_json(
        shard_paths.status_path,
        {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "status": "success",
            "success": True,
            "promotable": bool(manifest.get("promotable", False)),
            "core_tables_rebuilt": core_tables_written,
            "updated_at": utc_now(),
            "bridge_rebuilt_at": utc_now(),
        },
    )

    print(
        json.dumps(
            {
                "shard_path": str(shard_paths.shard_path),
                "bridge_rows": int(bridge_meta["bridge_rows"]),
                "eligible_rows": int(bridge_meta["eligible_rows"]),
                "excluded_rows": int(bridge_meta["excluded_rows"]),
                "bridge_validation_issues": bridge_issues,
                "core_tables_rebuilt": core_tables_written,
                "bridge_path": str(bridge_path),
                "manifest_path": str(shard_paths.manifest_path),
                "status_path": str(shard_paths.status_path),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
