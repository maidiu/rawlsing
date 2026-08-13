#!/usr/bin/env python3
"""Planner for V550 wave shards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_readiness import discover_shardable_source_waves
from data.ddm_build_copy.ddm_v550_readiness import load_scope_manifest
from data.ddm_build_copy.ddm_v550_storage import load_env_database_url, try_connect_database
from data.ddm_build_copy.ddm_v550_shards import shard_id_for
DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_PLAN_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "shard_plans"
DEFAULT_RESPONDENT_SCHEMA = ROOT / "data" / "ddm_build_copy" / "reports" / "respondent_wave_schema_template.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan V550 wave shards. Produce one shard per source/wave cell.")
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--respondent-schema-template", default=str(DEFAULT_RESPONDENT_SCHEMA))
    parser.add_argument("--readiness-root", default=None)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--wave", action="append", default=[])
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--output-root", default=str(ROOT / "data" / "ddm_repository_copy" / "v550"))
    parser.add_argument("--min-cell-n", type=int, default=50)
    parser.add_argument("--shared-respondent-substrate-mode", default="off", choices=("off", "write"))
    parser.add_argument("--joint-configuration-registry-path", default=None)
    parser.add_argument("--joint-configuration-id", action="append", default=[])
    parser.add_argument("--require-db", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--static-only", action="store_true", default=False)
    parser.add_argument(
        "--full-readiness",
        action="store_true",
        default=False,
        help="When DB-backed planning is available, compute the full readiness payload instead of the faster launchable scope plan.",
    )
    parser.add_argument("--write-shell-script", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def make_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    digest = hashlib.sha1(stamp.encode("utf-8")).hexdigest()[:8]
    return f"v550_{stamp}_{digest}"


def _append_shared_substrate_command_args(cmd: str, args: argparse.Namespace) -> str:
    if args.shared_respondent_substrate_mode != "off":
        cmd += f" --shared-respondent-substrate-mode {args.shared_respondent_substrate_mode}"
        cmd += " --v550-prepared-substrate-mode country"
    if args.joint_configuration_registry_path:
        cmd += f" --joint-configuration-registry-path {args.joint_configuration_registry_path}"
    for joint_configuration_id in args.joint_configuration_id:
        cmd += f" --joint-configuration-id {joint_configuration_id}"
    return cmd


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none", "null"} else text


def _parse_country_count(value: object) -> tuple[int, str]:
    text = _clean_text(value)
    if not text:
        return 0, "unknown"
    lowered = text.lower()
    if "single-country constant" in lowered:
        return 1, "single_country_constant"
    match = re.search(r"\((\d+)\s+substantive countries?\)", lowered)
    if match:
        return int(match.group(1)), "parsed_substantive_count"
    match = re.search(r"(\d+)\s+substantive countries?", lowered)
    if match:
        return int(match.group(1)), "parsed_substantive_count"
    match = re.fullmatch(r"(\d+)\s*-\s*(\d+)", lowered)
    if match:
        lo = int(match.group(1))
        hi = int(match.group(2))
        if lo == 1 and hi >= 1:
            return hi, "parsed_numeric_range"
    match = re.search(r"(\d+)\s*-\s*(\d+)", lowered)
    if match:
        lo = int(match.group(1))
        hi = int(match.group(2))
        if lo == 1 and hi >= 1:
            return hi, "parsed_numeric_range"
    if "country" in lowered:
        return 0, "country_label_only"
    return 0, "unknown"


def _static_plan_from_template(template_path: Path, run_id: str) -> pd.DataFrame:
    if not template_path.exists():
        return pd.DataFrame()
    template = pd.read_csv(template_path, low_memory=False)
    if template.empty:
        return pd.DataFrame()
    group_cols = [col for col in ["source_family", "wave"] if col in template.columns]
    if len(group_cols) < 2:
        return pd.DataFrame()
    rows = []

    def _to_int(value: object, default: int = 0) -> int:
        try:
            if pd.isna(value):
                return default
        except Exception:
            pass
        try:
            return int(float(str(value).strip()))
        except Exception:
            return default

    def _count_present(group: pd.DataFrame, columns: list[str]) -> int:
        return sum(1 for col in columns if col in group.columns and group[col].fillna("").astype(str).str.strip().ne("").any())

    for key, group in template.groupby(group_cols, dropna=False):
        if not isinstance(key, tuple):
            key = (key,)
        source, wave = key[0], key[1]
        source = str(source)
        wave = str(wave)
        countries: list[str] = []
        shard_id = shard_id_for(source, wave)
        country_count = 0
        country_count_status = "unknown"
        if "country_calculable_range" in group.columns and not group.empty:
            country_count, country_count_status = _parse_country_count(group["country_calculable_range"].iloc[0])
        respondent_count = _to_int(group["total_respondents"].iloc[0]) if "total_respondents" in group.columns and not group.empty else 0
        weight_status = "unknown"
        if "survey_weight_variable_status" in group.columns and not group.empty:
            weight_status = _clean_text(group["survey_weight_variable_status"].iloc[0]) or "unknown"
        position_field_count = _count_present(group, [
            "sex_var",
            "age_var",
            "education_var",
            "income_var",
            "survey_weight_var",
            "urban_rural_var",
            "religion_var",
            "marital_var",
            "employment_var",
            "class_var",
            "household_var",
            "language_var",
            "region_var",
            "ethnicity_var",
        ])
        rows.append(
            {
                "run_id": run_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "source": source,
                "source_family": source,
                "wave": wave,
                "canonical_wave": wave,
                "countries": countries,
                "country_count": country_count,
                "country_count_status": country_count_status,
                "respondent_count": respondent_count,
                "response_row_count": 0,
                "mapped_row_count": 0,
                "facet_row_count": 0,
                "position_field_count": position_field_count,
                "weight_status": weight_status,
                "readiness_status": "template_only",
                "skip_by_default": False,
                "skip_reason": None,
                "estimated_question_count": position_field_count,
                "output_dir": str(ROOT / "data" / "ddm_repository_copy" / "v550" / "shard_runs" / run_id / shard_id),
                "shard_id": shard_id,
                "command": (
                    "python data/ddm_build_copy/build_determinicity_wave_shard_v550.py "
                    f"--run-id {run_id} --shard-id {shard_id} --source {source} --wave {wave} "
                    "--write-csv --write-parquet --verbose"
                ),
            }
        )
    return pd.DataFrame(rows)


def _db_launchable_plan(conn, run_id: str, filters: dict[str, list[str]]) -> pd.DataFrame:
    scope = load_scope_manifest(
        conn,
        filters.get("source") or None,
        filters.get("wave") or None,
        filters.get("country") or None,
    )
    if scope.empty:
        return pd.DataFrame()

    template_path = DEFAULT_RESPONDENT_SCHEMA
    template = pd.DataFrame()
    if template_path.exists():
        try:
            template = pd.read_csv(template_path, low_memory=False)
        except Exception:
            template = pd.DataFrame()
    template_group = pd.DataFrame()
    if not template.empty and {"source_family", "wave"}.issubset(template.columns):
        template_group = template.groupby(["source_family", "wave"], dropna=False).first().reset_index()

    rows: list[dict[str, object]] = []
    for (source, wave), group in scope.groupby(["source", "wave"], sort=False):
        countries = sorted({str(c) for c in group["country_code"].dropna().astype(str) if str(c).strip()})
        shard_id = shard_id_for(str(source), str(wave))
        respondent_count = int(group["respondents"].sum())
        template_row = pd.DataFrame()
        if not template_group.empty:
            template_row = template_group[
                template_group["source_family"].astype(str).eq(str(source)) & template_group["wave"].astype(str).eq(str(wave))
            ]
        country_count = len(countries)
        country_count_status = "db_scope"
        position_field_count = 0
        weight_status = "unknown"
        estimated_question_count = 0
        if not template_row.empty:
            first = template_row.iloc[0]
            if "country_calculable_range" in first and pd.notna(first["country_calculable_range"]):
                parsed_count, parsed_status = _parse_country_count(first["country_calculable_range"])
                if parsed_count > 0:
                    country_count = parsed_count
                    country_count_status = parsed_status
            if "survey_weight_variable_status" in first and pd.notna(first["survey_weight_variable_status"]):
                weight_status = _clean_text(first["survey_weight_variable_status"]) or "unknown"
            position_field_count = sum(
                1
                for col in [
                    "sex_var",
                    "age_var",
                    "education_var",
                    "income_var",
                    "survey_weight_var",
                    "urban_rural_var",
                    "religion_var",
                    "marital_var",
                    "employment_var",
                    "class_var",
                    "household_var",
                    "language_var",
                    "region_var",
                    "ethnicity_var",
                ]
                if col in template_row.columns and template_row.iloc[0][col]
            )
            estimated_question_count = position_field_count
        rows.append(
            {
                "run_id": run_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "source": str(source),
                "source_family": str(source),
                "wave": str(wave),
                "canonical_wave": str(wave),
                "countries": countries,
                "country_count": country_count,
                "country_count_status": country_count_status,
                "respondent_count": respondent_count,
                "response_row_count": 0,
                "mapped_row_count": 0,
                "facet_row_count": 0,
                "position_field_count": position_field_count,
                "weight_status": weight_status,
                "readiness_status": "launchable_scope",
                "skip_by_default": False,
                "skip_reason": None,
                "estimated_question_count": estimated_question_count,
                "output_dir": str(ROOT / "data" / "ddm_repository_copy" / "v550" / "shard_runs" / run_id / shard_id),
                "shard_id": shard_id,
                "command": (
                    "python data/ddm_build_copy/build_determinicity_wave_shard_v550.py "
                    f"--run-id {run_id} --shard-id {shard_id} --source {source} --wave {wave} "
                    "--write-csv --write-parquet --verbose"
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(["source", "wave"]).reset_index(drop=True)


def _apply_plan_filters(plan_df: pd.DataFrame, source_filters: list[str], wave_filters: list[str], country_filters: list[str]) -> pd.DataFrame:
    if plan_df.empty:
        return plan_df
    if source_filters:
        plan_df = plan_df[plan_df["source"].isin(source_filters)]
    if wave_filters:
        plan_df = plan_df[plan_df["wave"].isin(wave_filters)]
    if country_filters and "countries" in plan_df.columns:
        plan_df = plan_df[plan_df["countries"].apply(lambda vals: any(c in set(vals) for c in country_filters))]
    return plan_df


def main() -> int:
    args = parse_args()
    load_dotenv(Path(args.env_file))
    run_id = args.run_id or make_run_id()
    output_root = Path(args.output_root)
    plan_root = output_root / "shard_plans" / run_id
    plan_root.mkdir(parents=True, exist_ok=True)

    source_filters = [s for s in args.source if s]
    wave_filters = [w for w in args.wave if w]
    country_filters = [c for c in args.country if c]
    filters = {"source": source_filters, "wave": wave_filters, "country": country_filters}

    db_url = load_env_database_url(Path(args.env_file), args.db_url)
    conn = None
    try:
        if not args.static_only:
            conn, err = try_connect_database(db_url)
            if conn is None:
                if args.require_db:
                    raise RuntimeError(f"[V550_DB_UNAVAILABLE] Could not connect to Postgres using {args.env_file} or --db-url. Original error: {err}")
        if conn is None:
            plan_df = _static_plan_from_template(Path(args.respondent_schema_template), run_id)
        else:
            if args.full_readiness:
                plan_df = discover_shardable_source_waves(conn, None, filters)
            else:
                plan_df = _db_launchable_plan(conn, run_id, filters)
        plan_df = _apply_plan_filters(plan_df, source_filters, wave_filters, country_filters)
        if plan_df.empty:
            raise RuntimeError("[V550_NO_SHARDS_DISCOVERED] No source/wave shards matched the requested filters. Check --source, --wave, DB coverage, and respondent schema template.")

        commands = []
        rows = []
        for row in plan_df.itertuples(index=False):
            shard_id = shard_id_for(str(row.source), str(row.wave))
            cmd = (
                "python data/ddm_build_copy/build_determinicity_wave_shard_v550.py "
                f"--run-id {run_id} --shard-id {shard_id} --source {row.source} --wave {row.wave} "
                "--write-csv --write-parquet --verbose"
            )
            if row.canonical_wave and str(row.canonical_wave) != str(row.wave):
                cmd += f" --canonical-wave {row.canonical_wave}"
            cmd = _append_shared_substrate_command_args(cmd, args)
            rows.append(
                {
                    "run_id": run_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "source": row.source,
                    "source_family": row.source_family,
                    "wave": row.wave,
                    "canonical_wave": row.canonical_wave,
                    "shard_id": shard_id,
                    "country_count": int(row.country_count),
                    "country_count_status": getattr(row, "country_count_status", "unknown"),
                    "respondent_count": int(row.respondent_count),
                    "response_row_count": int(row.response_row_count),
                    "mapped_row_count": int(row.mapped_row_count),
                    "facet_row_count": int(row.facet_row_count),
                    "position_field_count": int(row.position_field_count),
                    "weight_status": row.weight_status,
                    "readiness_status": row.readiness_status,
                    "skip_by_default": bool(row.skip_by_default),
                    "skip_reason": row.skip_reason,
                    "estimated_question_count": int(row.estimated_question_count),
                    "shared_respondent_substrate_mode": args.shared_respondent_substrate_mode,
                    "joint_configuration_registry_path": args.joint_configuration_registry_path or "",
                    "joint_configuration_ids": list(args.joint_configuration_id),
                    "output_dir": str(output_root / "shard_runs" / run_id / shard_id),
                    "command": cmd,
                }
            )
            if not row.skip_by_default:
                commands.append(cmd)

        plan_df = pd.DataFrame(rows)
        plan_json = {
            "run_id": run_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "planner_version": "v1",
            "repo_root": str(ROOT),
            "db_used": conn is not None,
            "filters": filters,
            "thresholds": {"min_cell_n": args.min_cell_n},
            "shared_respondent_substrate_mode": args.shared_respondent_substrate_mode,
            "joint_configuration_registry_path": args.joint_configuration_registry_path or "",
            "joint_configuration_ids": list(args.joint_configuration_id),
            "shards": rows,
        }

        (plan_root / "shard_plan.json").write_text(json.dumps(plan_json, indent=2, ensure_ascii=False), encoding="utf-8")
        plan_df.to_csv(plan_root / "shard_plan.csv", index=False)
        if args.write_shell_script:
            script_path = plan_root / "run_all_shards.sh"
            script_path.write_text("#!/usr/bin/env bash\nset -euo pipefail\n\n" + "\n".join(commands) + "\n", encoding="utf-8")
            script_path.chmod(0o755)
        (plan_root / "planner_manifest.json").write_text(
            json.dumps(
                {
                    "run_id": run_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "shard_count": int(len(plan_df)),
                    "non_skipped_shard_count": int(len(commands)),
                    "db_used": conn is not None,
                    "shared_respondent_substrate_mode": args.shared_respondent_substrate_mode,
                    "joint_configuration_registry_path": args.joint_configuration_registry_path or "",
                    "success": True,
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        if args.verbose:
            print(json.dumps(plan_json, indent=2, ensure_ascii=False))
        return 0
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
