#!/usr/bin/env python3
"""Replay the V550 cloud layer for an existing shard without rebuilding the full shard."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from data.ddm_build_copy.build_response_option_map_v550 import build_response_option_map
from data.ddm_build_copy.build_determinicity_repository_v550 import (
    _combine_wave_checkpoint_tables,
    _harmonize_question_frame,
    _load_response_option_map,
    _lookup_response_semantics,
    _log_progress,
    _prefetch_question_rows_by_country,
    _question_use_contract_replay_hash,
    _summary_question_meta,
    _write_json_report,
    _write_question_checkpoint,
)
from data.ddm_build_copy.ddm_v550_branching import prepare_question_frame
from data.ddm_build_copy.ddm_v550_clouds import (
    BRANCH_RELATION_CO_SIGNATURE_COLUMNS,
    CLOUD_ENGINE_VERSION,
    QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS,
    build_attitude_cloud_rows,
    build_co_signature_rows,
    should_emit_cloud_tables,
    reset_attitude_cloud_state,
)
from data.ddm_build_copy.ddm_v550_question_use import build_question_use_contract_row
from data.ddm_build_copy.ddm_v550_manifest import utc_now
from data.ddm_build_copy.ddm_v550_readiness import load_scope_manifest
from data.ddm_build_copy.ddm_v550_schema import forbidden_cloud_feature_row_count, validate_no_forbidden_cloud_features
from data.ddm_build_copy.ddm_v550_storage import V550ShardPaths, load_env_database_url, read_table_any, try_connect_database, write_table
from data.ddm_build_copy.ddm_v550_shared_respondent_substrate import SharedSubstratePaths, load_shared_respondent_substrate

DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_CODEBOOK_ROOT = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
DEFAULT_RESPONSE_OPTION_MAP = ROOT / "data" / "ddm_build_copy" / "reports" / "V550_response_option_map.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Replay the V550 cloud layer for an existing shard.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--shard-id", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--canonical-wave", default=None)
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--response-option-map", default=str(DEFAULT_RESPONSE_OPTION_MAP))
    parser.add_argument(
        "--cloud-mode",
        default="full",
        choices=("auto", "full", "off", "share"),
        help="Cloud replay policy. 'full' emits clouds for every question, 'auto' preserves the old threshold, 'off' skips cloud emission, 'share' uses a respondent share gate.",
    )
    parser.add_argument("--cloud-max-branch-rows", type=int, default=1000)
    parser.add_argument("--cloud-max-branch-share", type=float, default=None)
    parser.add_argument(
        "--prefetch-cache-dir",
        default=None,
        help="Optional directory for cached country-level prefetch slices. If omitted, a cache under the shard run is used.",
    )
    parser.add_argument(
        "--refresh-prefetch-cache",
        action="store_true",
        help="Ignore any existing cached country slices and refresh them from the database.",
    )
    parser.add_argument("--prepared-substrate-root", default=None, help="Shared respondent substrate root. Defaults to shard checkpoints/respondent_substrate.")
    parser.add_argument("--forbid-database-access", action="store_true", help="Reject replay paths that would query PostgreSQL.")
    parser.add_argument("--overwrite", action="store_true", default=True)
    parser.add_argument("--no-overwrite", dest="overwrite", action="store_false")
    parser.add_argument("--verbose", action="store_true")
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
        country_values = sorted({str(value).strip().upper() for value in frame.get("country_code_norm", frame.get("country_code", pd.Series(dtype="object"))).dropna() if str(value).strip()})
        if "var_code" in frame.columns:
            frame = frame.copy()
            frame["var_code"] = frame["var_code"].astype(str).str.upper()
            frame = frame.set_index("var_code", drop=False)
        for country_code in country_values:
            cache[country_code] = frame
    return cache


def _load_question_rows_from_checkpoints(qdir: Path) -> pd.DataFrame:
    paths = sorted(qdir.glob("*.parquet"))
    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_parquet(path)
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True, sort=False)
    sort_cols = [col for col in ["source", "canonical_wave", "country_code", "var_code", "question_id"] if col in out.columns]
    if sort_cols:
        out = out.sort_values(sort_cols).reset_index(drop=True)
    return out


def _load_response_option_map_live(path: str) -> pd.DataFrame:
    response_map = _load_response_option_map(path)
    if not response_map.empty:
        return response_map
    codebook_roots = [DEFAULT_CODEBOOK_ROOT]
    questions_master_drivers = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
    questions_master_semantic = ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_semantic.csv"
    question_structure_register = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_structure_register.csv"
    question_type_taxonomy = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_type_taxonomy.yaml"
    response_map, _, _ = build_response_option_map(
        codebook_roots=codebook_roots,
        questions_master_drivers=questions_master_drivers,
        questions_master_semantic=questions_master_semantic,
        question_structure_register=question_structure_register,
        question_type_taxonomy=question_type_taxonomy,
        db_conn=None,
        limit_questions=None,
    )
    return response_map


def _sql_literal(value: str) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def _normalize_token(value: Any) -> str:
    return str(value or "").strip()


def _normalize_key(value: Any) -> str:
    return _normalize_token(value).upper()


def _wave_aliases_for_source_family(source_family: Any, wave: Any) -> list[str]:
    family = _normalize_token(source_family)
    cleaned = _normalize_token(wave)
    if not cleaned:
        return []
    if family == "EVS":
        mapping = {
            "1981": ["1981", "W1", "Wave 1"],
            "W1": ["1981", "W1", "Wave 1"],
            "Wave 1": ["1981", "W1", "Wave 1"],
            "1990": ["1990", "W2", "Wave 2"],
            "W2": ["1990", "W2", "Wave 2"],
            "Wave 2": ["1990", "W2", "Wave 2"],
            "1999": ["1999", "W3", "Wave 3"],
            "W3": ["1999", "W3", "Wave 3"],
            "Wave 3": ["1999", "W3", "Wave 3"],
            "2008": ["2008", "W4", "Wave 4"],
            "W4": ["2008", "W4", "Wave 4"],
            "Wave 4": ["2008", "W4", "Wave 4"],
            "2017": ["2017", "W5", "Wave 5"],
            "W5": ["2017", "W5", "Wave 5"],
            "Wave 5": ["2017", "W5", "Wave 5"],
        }
        return mapping.get(cleaned, [cleaned])
    if family == "Arab Barometer":
        mapping = {
            "I": ["I", "W1", "Wave 1"],
            "W1": ["W1", "I", "Wave 1"],
            "Wave 1": ["Wave 1", "W1", "I"],
            "II": ["II", "W2", "Wave 2"],
            "W2": ["W2", "II", "Wave 2"],
            "Wave 2": ["Wave 2", "W2", "II"],
            "III": ["III", "W3", "Wave 3"],
            "W3": ["W3", "III", "Wave 3"],
            "Wave 3": ["Wave 3", "W3", "III"],
            "IV": ["IV", "W4", "Wave 4"],
            "W4": ["W4", "IV", "Wave 4"],
            "Wave 4": ["Wave 4", "W4", "IV"],
            "V": ["V", "W5", "Wave 5"],
            "W5": ["W5", "V", "Wave 5"],
            "Wave 5": ["Wave 5", "W5", "V"],
            "VI": ["VI", "W6", "Wave 6"],
            "W6": ["W6", "VI", "Wave 6"],
            "Wave 6": ["Wave 6", "W6", "VI"],
            "VII": ["VII", "W7", "Wave 7"],
            "W7": ["W7", "VII", "Wave 7"],
            "Wave 7": ["Wave 7", "W7", "VII"],
            "VIII": ["VIII", "W8", "Wave 8"],
            "W8": ["W8", "VIII", "Wave 8"],
            "Wave 8": ["Wave 8", "W8", "VIII"],
        }
        return mapping.get(cleaned, [cleaned])
    return [cleaned]


def _wave_candidates_for_replay(question_row: pd.Series, requested_wave: str, canonical_wave: str) -> list[str]:
    wave_candidates = list(
        dict.fromkeys(
            [
                _normalize_token(requested_wave),
                _normalize_token(canonical_wave),
                _normalize_token(question_row.get("raw_wave", "")),
                _normalize_token(question_row.get("wave", "")),
                _normalize_token(question_row.get("canonical_wave", "")),
                _normalize_token(canonical_wave),
            ]
        )
    )
    wave_values = []
    seen = set()
    for value in wave_candidates:
        cleaned = _normalize_token(value)
        if not cleaned:
            continue
        for alias in _wave_aliases_for_source_family(question_row.get("source_family", question_row.get("source", "")), cleaned):
            normalized = _normalize_key(alias)
            if normalized in seen:
                continue
            seen.add(normalized)
            wave_values.append(alias)
    return wave_values or [str(canonical_wave)]


def _count_question_rows(conn, qrow: pd.Series, requested_wave: str, canonical_wave: str) -> int:
    wave_clause = " OR ".join([f"canonical_wave = {_sql_literal(value)}" for value in _wave_candidates_for_replay(qrow, requested_wave, canonical_wave)])
    sql = f"""
        SELECT COUNT(*) AS n
        FROM v_ddm_response_long_facet_ready
        WHERE source = {_sql_literal(_normalize_token(qrow.get("source", "")))}
          AND ({wave_clause})
          AND country_code = {_sql_literal(_normalize_token(qrow.get("country_code", "")))}
          AND UPPER(var_code) = UPPER({_sql_literal(_normalize_token(qrow.get("var_code", "")))})
    """
    return int(pd.read_sql_query(sql, conn).iloc[0]["n"])


def _question_rows_from_cache_replay(question_row: pd.Series, question_row_cache: dict[str, pd.DataFrame]) -> pd.DataFrame:
    country_code = _normalize_key(question_row.get("country_code", ""))
    var_code = _normalize_key(question_row.get("var_code", ""))
    cached = question_row_cache.get(country_code)
    if cached is None or cached.empty:
        return pd.DataFrame(columns=cached.columns if cached is not None else None)
    if "var_code" not in cached.columns:
        return pd.DataFrame()
    if var_code not in cached.index:
        return pd.DataFrame(columns=cached.columns)
    return cached.loc[[var_code]].copy().reset_index(drop=True)


def _question_rows_replay(conn, question_row: pd.Series, requested_wave: str, canonical_wave: str) -> pd.DataFrame:
    wave_clause = " OR ".join([f"canonical_wave = {_sql_literal(value)}" for value in _wave_candidates_for_replay(question_row, requested_wave, canonical_wave)])
    sql = f"""
        SELECT *
        FROM v_ddm_response_long_facet_ready
        WHERE source = {_sql_literal(_normalize_token(question_row.get("source", "")))}
          AND ({wave_clause})
          AND country_code = {_sql_literal(_normalize_token(question_row.get("country_code", "")))}
          AND UPPER(var_code) = UPPER({_sql_literal(_normalize_token(question_row.get("var_code", "")))})
    """
    return pd.read_sql_query(sql, conn)


def _prefetch_cache_dir(shard_paths: V550ShardPaths, override: str | None) -> Path:
    if override:
        return Path(override)
    return shard_paths.run_path / "clouds" / "prefetch_cache"


def _prefetch_cache_path(cache_dir: Path, country_code: str) -> Path:
    return cache_dir / f"{_normalize_key(country_code)}.parquet"


def _load_prefetch_cache(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    frame = pd.read_parquet(path)
    if not frame.empty and "var_code" in frame.columns:
        frame = frame.copy()
        frame["var_code"] = frame["var_code"].astype(str).str.upper().str.strip()
        if "country_code" in frame.columns:
            frame["country_code"] = frame["country_code"].astype(str).str.upper().str.strip()
        if "canonical_wave" in frame.columns:
            frame["canonical_wave"] = frame["canonical_wave"].astype(str).str.upper().str.strip()
        frame = frame.set_index("var_code", drop=False)
    return frame


def _write_prefetch_cache(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(path, index=False)


def _reset_cloud_checkpoint_dir(shard_paths: V550ShardPaths, table_name: str) -> None:
    checkpoint_dir = shard_paths.checkpoints / "question_tables" / table_name
    if checkpoint_dir.exists():
        for path in checkpoint_dir.glob("*.parquet"):
            path.unlink()
        for path in checkpoint_dir.glob("*.complete"):
            path.unlink()


def main() -> int:
    args = parse_args()
    load_dotenv(Path(args.env_file))
    progress_started = time.monotonic()
    output_root = Path(args.output_root)
    shard_paths = V550ShardPaths(root=output_root, run_id=args.run_id, shard_id=args.shard_id)
    shard_paths.ensure()
    conn = None

    try:
        canonical_wave = str(args.canonical_wave or canonical_wave_label(args.source, args.wave))
        qdir = shard_paths.checkpoints / "question_tables" / "question_universe"
        if not qdir.exists():
            raise SystemExit(f"[V550_CLOUD_REPLAY_MISSING] Missing question_universe checkpoint directory: {qdir}")
        question_rows = _load_question_rows_from_checkpoints(qdir)
        if question_rows.empty:
            raise SystemExit(f"[V550_CLOUD_REPLAY_EMPTY] No question_universe checkpoint rows found in {qdir}")
        if "canonical_wave" in question_rows.columns:
            allowed_waves = {_normalize_key(args.wave), _normalize_key(canonical_wave)}
            question_rows = question_rows[question_rows["canonical_wave"].astype(str).str.upper().isin(allowed_waves)].reset_index(drop=True)
        if question_rows.empty:
            raise SystemExit(f"[V550_CLOUD_REPLAY_EMPTY] No question rows matched {args.source}/{args.wave} in {qdir}")

        if args.verbose:
            _log_progress(progress_started, f"loaded {len(question_rows)} question checkpoint rows")
        response_map = _load_response_option_map_live(args.response_option_map)
        semantics_lookup = _lookup_response_semantics(response_map)
        requested_wave = str(args.wave)
        prefetch_cache_dir = _prefetch_cache_dir(shard_paths, args.prefetch_cache_dir)

        readiness_path = shard_paths.core / "substrate_readiness.parquet"
        readiness_df = read_table_any(readiness_path) if readiness_path.exists() else pd.DataFrame()
        readiness_lookup: dict[tuple[str, str, str], pd.Series] = {}
        if not readiness_df.empty and {"source", "wave", "country_code"}.issubset(readiness_df.columns):
            for _, row in readiness_df.iterrows():
                readiness_lookup[(str(row["source"]), str(row["wave"]), str(row["country_code"]))] = row

        substrate_root = Path(args.prepared_substrate_root) if args.prepared_substrate_root else shard_paths.respondent_substrate
        question_row_cache: dict[str, pd.DataFrame] = _load_shared_substrate_cache(substrate_root)
        if args.verbose and question_row_cache:
            _log_progress(progress_started, f"loaded shared respondent substrate cache: countries={len(question_row_cache)}")
        respondent_cache_source = "shared_respondent_substrate" if question_row_cache else "postgres_legacy_replay"

        if args.verbose and not question_row_cache:
            if args.forbid_database_access:
                raise SystemExit("[V550_CLOUD_REPLAY_DATABASE_ACCESS_FORBIDDEN] shared respondent substrate is required")
            conn, err = try_connect_database(load_env_database_url(Path(args.env_file), args.db_url))
            if conn is None:
                raise SystemExit(f"[V550_SHARD_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")
            sample_rows = question_rows.head(3)
            for idx, qrow in enumerate(sample_rows.itertuples(index=False), start=1):
                qrow_series = pd.Series(qrow._asdict())
                sample_count = _count_question_rows(conn, qrow_series, requested_wave, canonical_wave)
                _log_progress(
                    progress_started,
                    f"sample question {idx}: source={qrow_series.get('source', '')} wave={qrow_series.get('canonical_wave', '')} country={qrow_series.get('country_code', '')} var={qrow_series.get('var_code', '')} rows={sample_count}",
                )

        source_values = {str(value) for value in question_rows["source"].dropna().astype(str) if str(value).strip()}
        if not question_row_cache and len(source_values) == 1:
            if args.forbid_database_access:
                raise SystemExit("[V550_CLOUD_REPLAY_DATABASE_ACCESS_FORBIDDEN] shared respondent substrate is required")
            if conn is None:
                conn, err = try_connect_database(load_env_database_url(Path(args.env_file), args.db_url))
                if conn is None:
                    raise SystemExit(f"[V550_SHARD_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")
            source = next(iter(source_values))
            country_codes = sorted({str(value) for value in question_rows["country_code"].dropna().astype(str) if str(value).strip()})
            wave_clause = " OR ".join([f"canonical_wave = {_sql_literal(value)}" for value in _wave_candidates_for_replay(question_rows.iloc[0], requested_wave, canonical_wave)])
            sql = f"""
                SELECT *
                FROM v_ddm_response_long_facet_ready
                WHERE source = {_sql_literal(source)}
                  AND ({wave_clause})
                  AND country_code = {{country_code}}
                ORDER BY var_code, respondent_id
            """
            for country_code in country_codes:
                cache_path = _prefetch_cache_path(prefetch_cache_dir, country_code)
                cached_frame = None if args.refresh_prefetch_cache else _load_prefetch_cache(cache_path)
                if cached_frame is not None:
                    question_row_cache[_normalize_key(country_code)] = cached_frame
                    if progress_started is not None:
                        _log_progress(progress_started, f"loaded cached response slice for country {country_code}: {len(cached_frame)} rows")
                    continue
                if progress_started is not None:
                    _log_progress(progress_started, f"prefetching response slice for country {country_code}")
                country_sql = sql.format(country_code=_sql_literal(country_code))
                df = pd.read_sql_query(country_sql, conn)
                if not df.empty and "var_code" in df.columns:
                    df = df.copy()
                    df["var_code"] = df["var_code"].astype(str).str.upper().str.strip()
                    df["country_code"] = df["country_code"].astype(str).str.upper().str.strip()
                    df["canonical_wave"] = df["canonical_wave"].astype(str).str.upper().str.strip()
                    df = df.set_index("var_code", drop=False)
                question_row_cache[_normalize_key(country_code)] = df
                if not df.empty:
                    _write_prefetch_cache(cache_path, df.reset_index(drop=True))
                if progress_started is not None:
                    _log_progress(progress_started, f"prefetched response slice for country {country_code}: {len(df)} rows")
        elif not question_row_cache:
            raise SystemExit("[V550_CLOUD_REPLAY_UNSAFE] question rows span multiple sources; replay helper expects exactly one source.")
        branch_files_written = 0
        cloud_files_written = 0
        cloud_mode = str(args.cloud_mode or "full")
        if args.overwrite:
            _reset_cloud_checkpoint_dir(shard_paths, "branch_co_signature")
            _reset_cloud_checkpoint_dir(shard_paths, "question_response_attitude_cloud")
        reset_attitude_cloud_state()

        for idx, qrow in enumerate(question_rows.itertuples(index=False), start=1):
            qrow = pd.Series(qrow._asdict())
            df = _question_rows_from_cache_replay(qrow, question_row_cache)
            if df.empty:
                df = _question_rows_replay(conn, qrow, requested_wave, canonical_wave)
            if df.empty:
                if args.verbose and (idx == 1 or idx % 50 == 0 or idx == len(question_rows)):
                    _log_progress(progress_started, f"cloud replay {idx}/{len(question_rows)}: no rows returned, skipping")
                continue
            df = _harmonize_question_frame(df, semantics_lookup)
            readiness_row = readiness_lookup.get((str(qrow.get("source", "")), str(qrow.get("wave", "")), str(qrow.get("country_code", ""))))
            qmeta = _summary_question_meta(df, qrow, readiness_row)
            qmeta["run_id"] = args.run_id
            qmeta["shard_id"] = args.shard_id
            qmeta["canonical_wave"] = canonical_wave
            qmeta["wave"] = canonical_wave
            qmeta.update(build_question_use_contract_row(qrow.to_dict()))
            qmeta["question_type"] = str(qrow.get("question_type", ""))
            qmeta["handling_rule"] = str(qrow.get("handling_rule", ""))
            qmeta["recommended_computation"] = str(qrow.get("recommended_computation", ""))
            branch_df = prepare_question_frame(df)
            wave_respondents = int(qmeta.get("n_respondents", 0) or 0)
            emit_clouds = should_emit_cloud_tables(
                len(branch_df),
                cloud_mode=cloud_mode,
                cloud_max_branch_rows=args.cloud_max_branch_rows,
                cloud_max_branch_share=args.cloud_max_branch_share,
                wave_respondents=wave_respondents,
            )
            if not emit_clouds:
                continue
            branch_co_signature_df = pd.DataFrame(build_co_signature_rows(branch_df, qmeta))
            question_response_attitude_cloud_df = pd.DataFrame(build_attitude_cloud_rows(branch_df, qmeta))
            question_index = idx
            if args.overwrite:
                _write_question_checkpoint(shard_paths, "branch_co_signature", question_index, qrow, branch_co_signature_df)
                _write_question_checkpoint(shard_paths, "question_response_attitude_cloud", question_index, qrow, question_response_attitude_cloud_df)
            branch_files_written += 1
            cloud_files_written += 1
            if args.verbose and (idx == 1 or idx % 50 == 0 or idx == len(question_rows)):
                _log_progress(progress_started, f"cloud replay {idx}/{len(question_rows)}: wrote clouds rows={len(branch_co_signature_df)}/{len(question_response_attitude_cloud_df)}")

        branch_co_sig = _combine_wave_checkpoint_tables(shard_paths, "branch_co_signature", question_rows, progress_started)
        attitude_cloud = _combine_wave_checkpoint_tables(shard_paths, "question_response_attitude_cloud", question_rows, progress_started)
        if branch_co_sig.empty:
            branch_co_sig = pd.DataFrame(columns=BRANCH_RELATION_CO_SIGNATURE_COLUMNS)
        if attitude_cloud.empty:
            attitude_cloud = pd.DataFrame(columns=QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS)
        cloud_exclusion_rows: list[dict[str, Any]] = []
        for table_name, frame in [("branch_co_signature", branch_co_sig), ("question_response_attitude_cloud", attitude_cloud)]:
            for issue in validate_no_forbidden_cloud_features(frame):
                affected_rows = forbidden_cloud_feature_row_count(frame, issue)
                cloud_exclusion_rows.append(
                    {
                        "run_id": args.run_id,
                        "shard_id": args.shard_id,
                        "table_name": table_name,
                        "issue": issue,
                        "severity": "high",
                        "row_count": int(affected_rows),
                    }
                )
        cloud_exclusion_audit = pd.DataFrame(cloud_exclusion_rows, columns=["run_id", "shard_id", "table_name", "issue", "severity", "row_count"])
        write_table(branch_co_sig, paths=shard_paths, table_name="branch_co_signature", layer="clouds", write_csv=False, write_parquet=True, report_name="V550_branch_co_signature.csv", reports_dir=None)
        write_table(attitude_cloud, paths=shard_paths, table_name="question_response_attitude_cloud", layer="clouds", write_csv=False, write_parquet=True, report_name="V550_question_response_attitude_cloud.csv", reports_dir=None)
        write_table(cloud_exclusion_audit, paths=shard_paths, table_name="cloud_exclusion_audit", layer="audit", write_csv=False, write_parquet=True, report_name="V550_cloud_exclusion_audit.csv", reports_dir=None)
        question_use_contract_hash = _question_use_contract_replay_hash(shard_paths)
        summary = {
            "run_id": args.run_id,
            "shard_id": args.shard_id,
            "source": args.source,
            "wave": args.wave,
            "canonical_wave": canonical_wave,
            "cloud_engine_version": CLOUD_ENGINE_VERSION,
            "cloud_replay_allowed": True,
            "cloud_mode": cloud_mode,
            "cloud_max_branch_rows": args.cloud_max_branch_rows,
            "cloud_max_branch_share": args.cloud_max_branch_share,
            "question_rows": int(len(question_rows)),
            "question_use_contract_hash": question_use_contract_hash,
            "branch_co_signature_rows": int(len(branch_co_sig)),
            "question_response_attitude_cloud_rows": int(len(attitude_cloud)),
            "branch_co_signature_status": "relation_only_compatibility_alias" if not branch_co_sig.empty else "compatibility_relation_only_alias_or_disabled",
            "question_response_attitude_cloud_status": "disabled_until_cross_question_engine" if attitude_cloud.empty else "prototype_diagnostic",
            "cloud_exclusion_rows": int(len(cloud_exclusion_audit)),
            "prefetch_cache_dir": str(prefetch_cache_dir),
            "respondent_cache_source": respondent_cache_source,
            "db_used": respondent_cache_source == "postgres_legacy_replay",
            "prefetch_cache_refresh": bool(args.refresh_prefetch_cache),
            "prefetch_cache_files": int(len(list(prefetch_cache_dir.glob("*.parquet")))) if prefetch_cache_dir.exists() else 0,
            "updated_at": utc_now(),
        }
        _write_json_report(shard_paths.clouds / "cloud_refresh_manifest.json", summary)
        if args.verbose:
            _log_progress(progress_started, f"cloud replay complete: branch_co_signature={len(branch_co_sig)} question_response_attitude_cloud={len(attitude_cloud)}")
        return 0
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
