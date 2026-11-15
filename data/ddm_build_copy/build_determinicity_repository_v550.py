#!/usr/bin/env python3
"""Build the V550 determinicity repository."""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
import json, logging, os, re, sys, time, warnings
from typing import Any

import numpy as np
import pandas as pd
from data.ddm_build_copy.build_source_structure_validator import canonical_wave_label
from dotenv import load_dotenv

warnings.filterwarnings(
    "ignore",
    message=r"pandas only supports SQLAlchemy connectable.*",
    category=UserWarning,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from data.ddm_build_copy.ddm_v550_branching import (
    SECONDARY_INDICATOR_SUMMARY_COLUMNS,
    branch_nodes_rows,
    indicator_answer_matrix_rows,
    indicator_summary_rows,
    outlier_cohort_rows,
    prepare_question_frame,
    secondary_indicator_summary_rows,
)
from data.ddm_build_copy.ddm_v550_clouds import (
    BRANCH_POSITION_SIGNATURE_COLUMNS,
    BRANCH_RELATION_CO_SIGNATURE_COLUMNS,
    QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS,
    build_attitude_cloud_rows,
    build_co_signature_rows,
    build_position_signature_rows,
    reset_attitude_cloud_state,
    should_emit_cloud_tables,
    valid_cloud_feature,
)
from data.ddm_build_copy.ddm_v550_manifest import build_manifest, utc_now
from data.ddm_build_copy.ddm_v550_distributions import build_distribution_tables
from data.ddm_build_copy.ddm_v550_metrics import classify_weight_status, dominant_response, distribution_entropy
from data.ddm_build_copy.ddm_v550_position_distribution import POSITION_DISTRIBUTION_COLUMNS, build_position_distribution_rows
from data.ddm_build_copy.ddm_v550_question_use import build_question_use_contract, build_question_use_contract_row
from data.ddm_build_copy.ddm_v550_source_structure import build_source_structure_population_audit, load_question_structure_register, match_source_structure_row, write_source_structure_population_audit
from data.ddm_build_copy.ddm_v550_readiness import POSITION_FIELDS, build_readiness, load_scope_manifest
from data.ddm_build_copy.ddm_v550_family_overlay import canonical_family_key, canonical_wave_key, wave_aliases, waves_equivalent
from data.ddm_build_copy.ddm_v550_response_options import build_response_option_map, normalize_response_code, response_semantics_contract_hash
from data.ddm_build_copy.ddm_v550_shared_cache import cached_query_frame, question_structural_mapping_select_columns, shared_cache_root
from data.ddm_build_copy.ddm_v550_storage import connect_from_env, ensure_directories, make_run_id, read_table_any, write_manifest, write_table
from data.ddm_build_copy.ddm_v550_clouds import CLOUD_ENGINE_VERSION
from data.ddm_build_copy.ddm_v550_validation import validate_attitude_cloud_rows
from data.ddm_build_copy.ddm_v550_support import DEFAULT_SUPPORT_CAP
from data.ddm_build_copy.ddm_v550_source_structure import _normalized_join_key
from data.ddm_build_copy.ddm_v550_io import normalize_family
from data.ddm_build_copy.ddm_v550_var_aliases import question_var_code_variants, resolve_question_var_aliases

QUESTION_VAR_ALIAS_LOOKUP_VERSION = "latinobarometro_alias_v1"


def _response_var_lookup_key(value: Any) -> str:
    cleaned = str(value or "").strip().upper()
    if not cleaned:
        return ""
    return re.sub(r"[^A-Z0-9]+", "", cleaned)

DEFAULT_OUTPUT_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550"
DEFAULT_REPORTS_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
DEFAULT_VALIDATION_ROOT = ROOT / "data" / "ddm_repository_copy" / "v550" / "validation"
DEFAULT_ENV_FILE = ROOT / ".env"
DEFAULT_RESPONDENT_SCHEMA = ROOT / "data" / "ddm_build_copy" / "reports" / "respondent_wave_schema_template.csv"
DEFAULT_CODEBOOK_ROOT = ROOT / "data" / "FINAL CODEBOOKS" / "FINAL FINAL CODEBOOKS"
DEFAULT_QUESTIONS_MASTER_DRIVERS = ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_drivers.csv"
DEFAULT_QUESTIONS_MASTER_SEMANTIC = ROOT / "chatgpt_v550_readiness_addendum" / "codebooks" / "questions_master_semantic.csv"
DEFAULT_STRUCTURE_REGISTER = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_structure_register.csv"
DEFAULT_TAXONOMY = ROOT / "chatgpt_v550_readiness_addendum" / "manifests" / "question_type_taxonomy.yaml"
DEFAULT_REPRESENTATIVE_LIMIT = 50
CHECKPOINT_ROOT_NAME = "checkpoints"
CHECKPOINT_TABLE_DIR = "question_tables"
CHECKPOINT_COMPLETE_SUFFIX = ".complete"
PROGRESS_INTERVAL_SECONDS = 15.0
FINALIZE_SOURCE_CHOICES = ("auto", "memory", "checkpoint")
PIPELINE_PROCESS_TOTAL = 51
PIPELINE_PROCESS_LABELS = {
    "question_universe": 32,
    "answer_distribution": 33,
    "country_answer_distribution": 34,
    "position_indicator_summary": 35,
    "indicator_answer_matrix": 36,
    "outlier_cohort_summary": 37,
    "secondary_indicator_summary": 38,
    "recursive_branch_nodes": 39,
    "branch_co_signature": 40,
    "question_response_attitude_cloud": 41,
    "mapping_gap_report": 42,
    "response_option_manual_review": 43,
    "cloud_exclusion_audit": 44,
    "scope_manifest": 45,
    "substrate_readiness": 46,
    "position_field_coverage": 47,
    "weight_coverage": 48,
    "mapping_status_coverage": 49,
    "legacy_leak_report": 50,
    "underpowered_quarantine": 51,
}
PIPELINE_PROCESS_TOTAL = 51
PIPELINE_PROCESS_LABELS = {
    "question_universe": 12,
    "answer_distribution": 13,
    "country_answer_distribution": 14,
    "position_indicator_summary": 15,
    "indicator_answer_matrix": 16,
    "outlier_cohort_summary": 17,
    "secondary_indicator_summary": 18,
    "recursive_branch_nodes": 19,
    "branch_co_signature": 20,
    "question_response_attitude_cloud": 21,
    "mapping_gap_report": 22,
}


def _process_label(table_name: str) -> str:
    idx = PIPELINE_PROCESS_LABELS.get(table_name)
    return f" ({idx}/{PIPELINE_PROCESS_TOTAL})" if idx else ""


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and not pd.isna(value):
        return value != 0
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off", "", "nan", "none"}:
        return False
    return default


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the V550 determinicity repository (baseline/legacy mode). For production full-corpus execution use plan_v550_wave_shards.py + build_determinicity_wave_shard_v550.py + merge_determinicity_shards_v550.py."
    )
    parser.add_argument("--db-url", default=None)
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE))
    parser.add_argument("--response-option-map", default=None, help="Optional prebuilt response-option map parquet/csv.")
    parser.add_argument("--readiness-root", default=None)
    parser.add_argument("--respondent-schema-template", default=str(DEFAULT_RESPONDENT_SCHEMA))
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--wave", action="append", default=[])
    parser.add_argument("--country", action="append", default=[])
    parser.add_argument("--min-cell-n", type=int, default=50)
    parser.add_argument("--min-branch-n", type=int, default=DEFAULT_SUPPORT_CAP)
    parser.add_argument("--min-answer-n", type=int, default=DEFAULT_SUPPORT_CAP)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument(
        "--cloud-mode",
        default="auto",
        choices=("auto", "full", "off", "share"),
        help="How to emit cloud tables. 'auto' preserves the current threshold, 'full' always emits, 'off' never emits, 'share' uses a wave-respondent share gate.",
    )
    parser.add_argument(
        "--cloud-max-branch-rows",
        type=int,
        default=1000,
        help="Maximum branch-frame rows allowed for cloud emission in auto/share mode.",
    )
    parser.add_argument(
        "--cloud-max-branch-share",
        type=float,
        default=None,
        help="Optional wave-respondent share threshold for cloud emission in share mode.",
    )
    parser.add_argument("--max-questions", type=int, default=None)
    parser.add_argument("--limit-questions", type=int, default=None)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR))
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--write-csv", dest="write_csv", action="store_true", default=True)
    parser.add_argument("--no-write-csv", dest="write_csv", action="store_false")
    parser.add_argument("--write-parquet", dest="write_parquet", action="store_true", default=True)
    parser.add_argument("--no-write-parquet", dest="write_parquet", action="store_false")
    parser.add_argument("--write-postgres", action="store_true", default=False)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="Run a tiny smoke test: one wave and a small question cap.")
    parser.add_argument("--smoke-questions", type=int, default=5, help="Question cap when --smoke is set.")
    parser.add_argument("--resume", action="store_true", help="Skip questions that already have checkpoint files in the run directory.")
    parser.add_argument(
        "--v550-prepared-substrate-mode",
        default="off",
        choices=("off", "country", "chunked"),
        help="Pre-harmonize the shared question cache once per country or in chunks before the question loop. 'off' preserves the legacy hot path.",
    )
    parser.add_argument(
        "--finalize-source",
        default="auto",
        choices=FINALIZE_SOURCE_CHOICES,
        help="How to finalize wave tables: 'auto' uses memory on fresh runs and checkpoint reloads on resume, 'memory' never reloads final tables from disk, and 'checkpoint' always reloads final tables from disk.",
    )
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def _load_response_option_map(path: str | None) -> pd.DataFrame:
    if not path:
        return pd.DataFrame()
    p = Path(path)
    if not p.exists():
        fallback_candidates = [
            ROOT / "data" / "ddm_build_copy" / "reports" / "V550_response_option_map.csv",
            ROOT / "data" / "ddm_build_copy" / "reports" / "response_option_map.csv",
        ]
        for fallback in fallback_candidates:
            if fallback.exists():
                return pd.read_csv(fallback, low_memory=False)
        return pd.DataFrame()
    if p.suffix.lower() == ".parquet":
        return pd.read_parquet(p)
    return pd.read_csv(p, low_memory=False)


_QUESTION_LIST_COLUMNS = [
    "source",
    "raw_wave",
    "canonical_wave",
    "country_code",
    "var_code",
    "question_id",
    "question_block_id",
    "driver_id",
    "driver_facet_id",
    "relation_axis_id",
    "target_entity_id",
    "mapping_status",
    "legacy_final_driver_id",
    "question_type",
    "handling_rule",
    "recommended_computation",
    "final_driver_scope",
    "source_structure_classification",
    "source_structure_source",
    "source_structure_join_key",
    "source_structure_join_confidence",
    "source_structure_fields_joined",
    "source_structure_review_required",
    "question_rows",
    "n_respondents",
]


def _wave_match_candidates(source: str, raw_wave: str) -> list[str]:
    raw_wave = str(raw_wave)
    canonical = canonical_wave_label(str(source), raw_wave)
    candidates = [raw_wave]
    if canonical and canonical not in candidates:
        candidates.append(canonical)
    return candidates


def _build_question_list(scope_df: pd.DataFrame, mapping_df: pd.DataFrame, max_questions: int | None) -> pd.DataFrame:
    if scope_df.empty or mapping_df.empty:
        return pd.DataFrame({col: pd.Series(dtype="object") for col in _QUESTION_LIST_COLUMNS})
    scope = scope_df.rename(columns={"wave": "raw_wave"}).copy()
    scope["source"] = scope["source"].astype(str)
    scope["raw_wave"] = scope["raw_wave"].astype(str)
    scope["canonical_wave"] = scope.apply(lambda row: canonical_wave_label(str(row["source"]), str(row["raw_wave"])), axis=1)
    scope["country_code"] = scope["country_code"].astype(str)
    scope["wave_match"] = scope.apply(lambda row: _wave_match_candidates(str(row["source"]), str(row["raw_wave"])), axis=1)
    scope = scope.explode("wave_match", ignore_index=True)
    scope["wave_match"] = scope["wave_match"].astype(str)
    mapping = mapping_df.copy()
    mapping["source"] = mapping["source"].astype(str)
    mapping["raw_wave"] = mapping["wave"].astype(str)
    mapping["canonical_wave"] = mapping.apply(lambda row: canonical_wave_label(str(row["source"]), str(row["raw_wave"])), axis=1)
    mapping["wave_match"] = mapping.apply(lambda row: _wave_match_candidates(str(row["source"]), str(row["raw_wave"])), axis=1)
    mapping = mapping.explode("wave_match", ignore_index=True)
    mapping["wave_match"] = mapping["wave_match"].astype(str)
    merged = scope.merge(mapping, on=["source", "wave_match"], how="inner", suffixes=("_scope", "_mapping"))
    merged["raw_wave"] = merged["raw_wave_scope"].astype(str)
    merged["canonical_wave"] = merged["canonical_wave_scope"].astype(str)
    merged["mapping_wave"] = merged["canonical_wave_mapping"].astype(str)
    merged["question_rows"] = 0
    merged["n_respondents"] = 0
    for column in _QUESTION_LIST_COLUMNS:
        if column not in merged.columns:
            merged[column] = pd.NA
    merged = merged.drop(columns=[col for col in ["raw_wave_scope", "raw_wave_mapping", "wave_match", "canonical_wave_scope", "canonical_wave_mapping"] if col in merged.columns])
    merged = merged[_QUESTION_LIST_COLUMNS].drop_duplicates()
    merged = merged.sort_values(["source", "canonical_wave", "country_code", "var_code"]).reset_index(drop=True)
    if max_questions is not None and len(merged) > max_questions:
        merged = merged.head(max_questions)
    return merged


def _question_structural_mapping_select_columns(conn) -> list[str]:
    return question_structural_mapping_select_columns(conn)


def _load_wave_question_mapping(conn, wave_source: str, wave_wave: str) -> pd.DataFrame:
    canonical_wave = canonical_wave_label(wave_source, wave_wave)
    wave_candidates = list(
        dict.fromkeys(
            [
                str(wave_wave),
                str(canonical_wave),
                *wave_aliases(wave_source, wave_wave),
                *wave_aliases(wave_source, canonical_wave),
            ]
        )
    )
    wave_candidates = [value for value in wave_candidates if str(value).strip()]
    select_columns = _question_structural_mapping_select_columns(conn)
    payload = {
        "query": "question_structural_mapping_slice_alias_aware",
        "source": str(wave_source),
        "requested_wave": str(wave_wave),
        "waves": sorted({str(value) for value in wave_candidates}),
        "select_columns": select_columns,
    }

    def _query() -> pd.DataFrame:
        qsm_rel = os.getenv("DDM_QSM_RELATION", "question_structural_mapping")
        sql = f"""
            SELECT {", ".join(select_columns)}
            FROM {qsm_rel}
            WHERE source = %(source)s AND wave = ANY(%(waves)s)
            ORDER BY
                CASE WHEN final_driver_origin = 'legacy_calibration_residual' THEN 1 ELSE 0 END,
                var_code,
                loaded_at DESC
        """
        exact = pd.read_sql_query(sql, conn, params={"source": wave_source, "waves": wave_candidates})

        # The normalized authority tables preserve source-native labels in some
        # waves (for example, ``World Values Survey`` rather than ``WVS``).
        # Preflight already treats those as the same survey family; V550 must
        # use the same canonical family identity rather than silently becoming
        # GSS-only through exact source-string equality. Query the wave slice
        # and merge every row belonging to the same canonical family so a
        # partially populated exact label cannot hide additional alias rows.
        fallback_sql = f"""
            SELECT {", ".join(select_columns)}
            FROM {qsm_rel}
            WHERE wave = ANY(%(waves)s)
            ORDER BY
                CASE WHEN final_driver_origin = 'legacy_calibration_residual' THEN 1 ELSE 0 END,
                source,
                var_code,
                loaded_at DESC
        """
        candidates = pd.read_sql_query(fallback_sql, conn, params={"waves": wave_candidates})
        requested_family = canonical_family_key(wave_source)
        if not candidates.empty and "source" in candidates.columns:
            matched = candidates[
                candidates["source"].map(lambda value: canonical_family_key(value) == requested_family)
            ].copy()
        else:
            matched = candidates.iloc[0:0].copy()

        combined = pd.concat([exact, matched], ignore_index=True, sort=False)
        if combined.empty:
            return combined
        combined["source"] = str(wave_source)
        combined["wave"] = str(wave_wave)
        dedupe_columns = [column for column in select_columns if column in combined.columns]
        combined = combined.drop_duplicates(subset=dedupe_columns, keep="first")
        if "final_driver_origin" in combined.columns:
            combined["_r1_authority_priority"] = (
                combined["final_driver_origin"] != "legacy_calibration_residual"
            ).astype(int)
        sort_columns = [column for column in ("var_code", "_r1_authority_priority", "loaded_at") if column in combined.columns]
        if sort_columns:
            ascending = [True, False, False][:len(sort_columns)]
            combined = combined.sort_values(sort_columns, ascending=ascending, kind="mergesort")
        if "_r1_authority_priority" in combined.columns:
            combined = combined.drop(columns=["_r1_authority_priority"])
        return combined.reset_index(drop=True)

    frame = cached_query_frame(
        "mapping",
        payload,
        _query,
        cache_root=shared_cache_root(),
        metadata={
            "source_table": "question_structural_mapping",
            "source": str(wave_source),
            "requested_wave": str(wave_wave),
            "waves": sorted({str(value) for value in wave_candidates}),
            "select_columns": select_columns,
        },
    )
    if not frame.empty and "wave" in frame.columns:
        equivalent = frame["wave"].map(lambda value: waves_equivalent(wave_source, value, wave_wave))
        frame = frame[equivalent].copy()
        frame["wave"] = str(wave_wave)
    missing_optional = [column for column in ["question_type", "handling_rule", "recommended_computation", "final_driver_scope", "source_structure_classification"] if column not in frame.columns]
    for column in missing_optional:
        frame[column] = pd.NA
    frame.attrs["missing_structure_columns"] = missing_optional
    return frame


def _assert_columns(df: pd.DataFrame, required: list[str], context: str) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise RuntimeError(f"{context} is missing required columns: {missing}")


def _assert_live_contracts(scope_df: pd.DataFrame, readiness_df: pd.DataFrame, wave_mapping_df: pd.DataFrame, wave_question_rows: pd.DataFrame | None = None) -> None:
    _assert_columns(scope_df, ["source", "wave", "country_code", "respondents"], "scope_df")
    _assert_columns(readiness_df, ["source", "wave", "country_code", "readiness_status"], "readiness_df")
    _assert_columns(wave_mapping_df, ["source", "wave", "var_code", "question_id", "driver_id", "driver_facet_id", "question_block_id", "relation_axis_id", "target_entity_id", "mapping_status", "legacy_final_driver_id"], "question_structural_mapping")
    if wave_question_rows is not None:
        _assert_columns(
            wave_question_rows,
            [
                "source",
                "canonical_wave",
                "country_code",
                "var_code",
                "question_id",
                "question_block_id",
                "driver_id",
                "driver_facet_id",
                "relation_axis_id",
                "target_entity_id",
                "mapping_status",
                "legacy_final_driver_id",
                "question_type",
                "handling_rule",
                "recommended_computation",
                "final_driver_scope",
                "source_structure_classification",
            ],
            "wave_question_rows",
        )


def _assert_facet_ready_view_contract(conn) -> None:
    required = [
        "respondent_id",
        "source",
        "wave",
        "canonical_wave",
        "country_code",
        "survey_year",
        "var_code",
        "value_raw",
        "value_text",
        "weight_value",
        "weight_name",
        "weight_status",
        "sex",
        "age",
        "age_group",
        "education_level",
        "income_level",
        "religion_label",
        "urban_rural",
        "region",
        "ethnicity",
        "language",
        "employment",
        "marital",
        "household_size",
        "position_source_table",
        "position_completeness_score",
        "question_id",
        "question_block_id",
        "structural_domain_id",
        "driver_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_id",
        "mapping_status",
        "legacy_final_driver_id",
        "legacy_driver_leak_flag",
    ]
    resp_rel = os.getenv("DDM_RESPONSE_LONG_RELATION", "v_ddm_response_long_facet_ready")
    if "." in resp_rel:
        resp_schema, resp_table = resp_rel.split(".", 1)
        schema_clause = f"AND table_schema = '{resp_schema}'"
    else:
        resp_table = resp_rel
        schema_clause = ""
    sql = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{resp_table}'
        {schema_clause}
        ORDER BY ordinal_position
    """.format(resp_table=resp_table, schema_clause=schema_clause)
    cols = pd.read_sql_query(sql, conn)["column_name"].tolist()
    missing = [col for col in required if col not in cols]
    if missing:
        raise RuntimeError(f"{resp_rel} is missing required columns: {missing}")


def _iter_wave_scopes(scope_df: pd.DataFrame) -> list[tuple[str, str, pd.DataFrame]]:
    if scope_df.empty:
        return []
    ordered = scope_df.sort_values(["source", "wave", "country_code"]).reset_index(drop=True)
    wave_groups: list[tuple[str, str, pd.DataFrame]] = []
    for (source, wave), wave_scope in ordered.groupby(["source", "wave"], sort=False):
        wave_groups.append((str(source), str(wave), wave_scope.reset_index(drop=True).copy()))
    return wave_groups


def _safe_weight_status(series: pd.Series | None) -> str:
    status, _valid = classify_weight_status(series)
    return status


def _clean(value: Any) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    text = str(value).strip()
    return "" if text.lower() in {"nan", "none"} else text


def _first_nonempty(series: pd.Series, default: Any = "") -> Any:
    if series.empty:
        return default
    cleaned = series.fillna("").astype(str).str.strip()
    cleaned = cleaned[cleaned.ne("")]
    if cleaned.empty:
        return default
    return cleaned.iloc[0]



def _first_clean_value(*values: Any) -> str:
    for value in values:
        cleaned = _clean(value)
        if cleaned:
            return cleaned
    return ""


def _ordered_clean_variants(values: list[Any], *, normalized_join: bool = False) -> list[str]:
    """Return stable, non-empty lookup variants without NaN-like tokens."""
    out: list[str] = []
    for value in values:
        cleaned = _clean(value)
        if not cleaned:
            continue
        candidates = [cleaned]
        if normalized_join:
            normalized = _normalized_join_key(cleaned)
            if normalized:
                candidates.append(normalized)
        for candidate in candidates:
            candidate = _clean(candidate)
            if candidate and candidate not in out:
                out.append(candidate)
    return out


def _response_semantics_source_variants(source: Any) -> list[str]:
    raw = _clean(source)
    normalized_family = normalize_family(raw)
    canonical = canonical_family_key(raw)
    canonical_normalized = canonical_family_key(normalized_family or raw or canonical)
    return _ordered_clean_variants(
        [raw, normalized_family, canonical, canonical_normalized],
        normalized_join=True,
    )


def _response_semantics_wave_variants(source: Any, *waves: Any) -> list[str]:
    source_base = normalize_family(_clean(source)) or _clean(source) or canonical_family_key(_clean(source))
    values: list[Any] = []
    for wave in waves:
        cleaned = _clean(wave)
        if not cleaned:
            continue
        values.extend([cleaned, canonical_wave_key(source_base, cleaned)])
        values.extend(wave_aliases(source_base, cleaned))
    return _ordered_clean_variants(values, normalized_join=True)


def _response_semantics_var_variants(source: Any, wave: Any, var_code: Any) -> list[str]:
    cleaned = _clean(var_code)
    alias_variants = question_var_code_variants(source, wave, cleaned)
    return _ordered_clean_variants(
        [cleaned, cleaned.lower(), cleaned.upper(), *alias_variants],
        normalized_join=True,
    )


def _response_semantics_value_variants(*values: Any) -> list[str]:
    candidates: list[Any] = []
    for value in values:
        cleaned = _clean(value)
        if not cleaned:
            continue
        candidates.extend([cleaned, normalize_response_code(cleaned)])
    return _ordered_clean_variants(candidates, normalized_join=True)


def _response_semantics_key_candidates(
    *,
    source: Any,
    waves: list[Any],
    var_code: Any,
    values: list[Any],
) -> list[tuple[str, str, str, str]]:
    keys: list[tuple[str, str, str, str]] = []
    for source_variant in _response_semantics_source_variants(source):
        for wave_variant in _response_semantics_wave_variants(source, *waves):
            for var_variant in _response_semantics_var_variants(source, wave_variant, var_code):
                for value_variant in _response_semantics_value_variants(*values):
                    key = (source_variant, wave_variant, var_variant, value_variant)
                    if key not in keys:
                        keys.append(key)
    return keys

def _lookup_response_semantics(response_map: pd.DataFrame) -> dict[tuple[str, str, str, str], dict[str, Any]]:
    """Build a response-semantics lookup with symmetric family/wave/var/value keys.

    The same key-expansion helper is used here and by the live-row lookup below.
    This prevents case-only variable mismatches (Q2011 vs q2011) and canonical
    wave aliases (W2 vs II) from silently degrading packet authority to
    observed-only semantics.
    """
    lookup: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    if response_map.empty:
        return lookup
    for row in response_map.itertuples(index=False):
        row_dict = row._asdict()
        source = _first_clean_value(row_dict.get("source_family"), row_dict.get("source"))
        waves = [row_dict.get("wave", ""), row_dict.get("canonical_wave", "")]
        var_code = _first_clean_value(
            row_dict.get("var_name"),
            row_dict.get("var_code"),
            row_dict.get("question_id"),
            row_dict.get("variable_id"),
        )
        values = [
            row_dict.get("value_code_normalized", ""),
            row_dict.get("value_code", ""),
            row_dict.get("response_value_normalized", ""),
            row_dict.get("value_label_clean", ""),
            row_dict.get("response_label", ""),
            row_dict.get("normalized_response_label", ""),
        ]
        for key in _response_semantics_key_candidates(
            source=source,
            waves=waves,
            var_code=var_code,
            values=values,
        ):
            existing = lookup.get(key)
            if existing is None:
                lookup[key] = row_dict
                continue
            # Prefer the row carrying explicit packet provenance over a generic
            # or observed-only row if aliases collapse onto the same key.
            existing_status = _clean(existing.get("response_semantics_status", "")).lower()
            candidate_status = _clean(row_dict.get("response_semantics_status", "")).lower()
            if existing_status in {"", "observed_only"} and candidate_status not in {"", "observed_only"}:
                lookup[key] = row_dict
    return lookup


def _question_rows(
    conn,
    question_row: pd.Series,
    filters: dict[str, list[str]],
    *,
    response_semantics_contract_hash: str = "",
) -> pd.DataFrame:
    def _sql_literal(value: str) -> str:
        return "'" + str(value).replace("'", "''") + "'"

    wave_candidates = list(
        dict.fromkeys(
            [
                str(question_row.get("raw_wave", "")),
                str(question_row.get("canonical_wave", "")),
                canonical_wave_label(str(question_row.get("source", "")), str(question_row.get("raw_wave", ""))),
            ]
        )
    )
    wave_values = [value for value in wave_candidates if str(value).strip()]
    if not wave_values:
        wave_values = [canonical_wave_label(str(question_row.get("source", "")), str(question_row.get("raw_wave", "")))]
    wave_clause = " OR ".join([f"canonical_wave = {_sql_literal(value)}" for value in wave_values])
    var_codes = question_var_code_variants(question_row["source"], question_row.get("canonical_wave", ""), question_row["var_code"])
    var_clause = " OR ".join([f"REGEXP_REPLACE(UPPER(var_code), '[^A-Z0-9]+', '', 'g') = {_sql_literal(_response_var_lookup_key(value))}" for value in var_codes])
    resp_rel = os.getenv("DDM_RESPONSE_LONG_RELATION", "v_ddm_response_long_facet_ready")
    sql = """
        SELECT *
        FROM {resp_rel}
        WHERE source = {source}
          AND ({wave_clause})
          AND country_code = {country_code}
          AND ({var_clause})
    """.format(
        resp_rel=resp_rel,
        source=_sql_literal(question_row["source"]),
        wave_clause=wave_clause,
        country_code=_sql_literal(question_row["country_code"]),
        var_clause=var_clause,
    )
    return pd.read_sql_query(sql, conn)


def _prefetch_question_rows_by_country(
    conn,
    question_rows: pd.DataFrame,
    progress_started: float | None = None,
    *,
    response_semantics_contract_hash: str = "",
) -> dict[str, pd.DataFrame]:
    def _sql_literal(value: str) -> str:
        return "'" + str(value).replace("'", "''") + "'"

    if question_rows.empty:
        return {}
    if "source" not in question_rows.columns or "country_code" not in question_rows.columns:
        return {}

    source_values = {str(value) for value in question_rows["source"].dropna().astype(str) if str(value).strip()}
    if len(source_values) != 1:
        return {}
    source = next(iter(source_values))
    cache: dict[str, pd.DataFrame] = {}
    country_codes = sorted({str(value) for value in question_rows["country_code"].dropna().astype(str) if str(value).strip()})
    if not country_codes:
        return cache

    wave_candidates = list(
        dict.fromkeys(
            [
                str(question_rows["raw_wave"].iloc[0]) if "raw_wave" in question_rows.columns and not question_rows.empty else "",
                str(question_rows["canonical_wave"].iloc[0]) if "canonical_wave" in question_rows.columns and not question_rows.empty else "",
                canonical_wave_label(
                    str(question_rows["source"].iloc[0]) if not question_rows.empty else "",
                    str(question_rows["raw_wave"].iloc[0]) if "raw_wave" in question_rows.columns and not question_rows.empty else "",
                ),
            ]
        )
    )
    wave_candidates = [value for value in wave_candidates if str(value).strip()]
    if not wave_candidates:
        wave_candidates = [canonical_wave_label(source, str(question_rows["raw_wave"].iloc[0]) if "raw_wave" in question_rows.columns and not question_rows.empty else "")]
    wave_clause = " OR ".join([f"canonical_wave = {_sql_literal(value)}" for value in wave_candidates])
    selected_alias_codes: list[str] = []
    for item in question_rows.itertuples(index=False):
        aliases = question_var_code_variants(source, wave_candidates[0] if wave_candidates else "", getattr(item, "var_code", ""))
        for alias in aliases:
            if alias and alias not in selected_alias_codes:
                selected_alias_codes.append(alias)
    for country_code in country_codes:
        if progress_started is not None:
            _log_progress(progress_started, f"prefetching response slice for country {country_code}")
        resp_rel = os.getenv("DDM_RESPONSE_LONG_RELATION", "v_ddm_response_long_facet_ready")
        country_sql = """
            SELECT *
            FROM {resp_rel}
            WHERE source = {source}
              AND ({wave_clause})
              AND country_code = {country_code}
              AND REGEXP_REPLACE(UPPER(var_code), '[^A-Z0-9]+', '', 'g') = ANY(%(selected_codes)s)
            ORDER BY var_code, respondent_id
        """.format(
            resp_rel=resp_rel,
            source=_sql_literal(source),
            wave_clause=wave_clause,
            country_code=_sql_literal(country_code),
        )
        df = pd.read_sql_query(
            country_sql,
            conn,
            params={"selected_codes": [_response_var_lookup_key(value) for value in selected_alias_codes]},
        )
        if not df.empty and "var_code" in df.columns:
            df = df.copy()
            df["var_code"] = df["var_code"].astype(str).str.upper()
            df = df.set_index("var_code", drop=False)
        cache[country_code] = df
        if progress_started is not None:
            _log_progress(progress_started, f"prefetched response slice for country {country_code}: {len(df)} rows")
    return cache


def _prepare_v550_question_row_cache(
    question_row_cache: dict[str, pd.DataFrame],
    semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]],
    *,
    response_semantics_contract_hash: str,
    mode: str,
    progress_started: float | None = None,
) -> tuple[dict[str, pd.DataFrame], dict[str, int]]:
    stats = {
        "v550_harmonization_call_count_prepared": 0,
        "v550_harmonization_row_count_prepared": 0,
        "v550_harmonization_call_count_per_question": 0,
        "v550_harmonization_row_count_per_question": 0,
        "v550_harmonization_call_count_fallback": 0,
        "v550_harmonization_row_count_fallback": 0,
    }
    if mode == "off":
        return question_row_cache, stats

    prepared_cache: dict[str, pd.DataFrame] = {}
    chunk_size = 100_000 if mode == "chunked" else None

    for country_code, frame in question_row_cache.items():
        if frame is None:
            prepared_cache[country_code] = pd.DataFrame()
            continue
        if frame.empty:
            prepared_cache[country_code] = frame.copy()
            continue

        if mode == "country":
            prepared = _harmonize_question_frame(
                frame,
                semantics_lookup,
                response_semantics_contract_hash=response_semantics_contract_hash,
            )
            stats["v550_harmonization_call_count_prepared"] += 1
            stats["v550_harmonization_row_count_prepared"] += int(len(frame))
        else:
            chunks: list[pd.DataFrame] = []
            effective_chunk_size = chunk_size or len(frame)
            for start in range(0, len(frame), effective_chunk_size):
                chunk = frame.iloc[start : start + effective_chunk_size].copy()
                prepared_chunk = _harmonize_question_frame(
                    chunk,
                    semantics_lookup,
                    response_semantics_contract_hash=response_semantics_contract_hash,
                )
                chunks.append(prepared_chunk)
                stats["v550_harmonization_call_count_prepared"] += 1
                stats["v550_harmonization_row_count_prepared"] += int(len(chunk))
            prepared = pd.concat(chunks, ignore_index=True, sort=False) if chunks else frame.iloc[0:0].copy()

        if "var_code" in prepared.columns:
            prepared = prepared.copy()
            prepared["var_code"] = prepared["var_code"].astype(str).str.upper()
            prepared = prepared.set_index("var_code", drop=False)
        prepared_cache[country_code] = prepared
        if progress_started is not None:
            _log_progress(progress_started, f"prepared harmonized response cache for country {country_code}: {len(prepared)} rows via {mode}")

    return prepared_cache, stats



def _question_rows_from_cache(question_row: pd.Series, question_row_cache: dict[str, pd.DataFrame]) -> pd.DataFrame:
    country_code = str(question_row.get("country_code", ""))
    source = str(question_row.get("source", ""))
    wave = str(question_row.get("canonical_wave", "") or question_row.get("raw_wave", ""))
    alias_info = resolve_question_var_aliases(source, wave, question_row.get("var_code", ""))
    required_source_names = [str(value).upper() for value in alias_info.get("source_var_names", []) if str(value).strip()]
    lookup_variants = question_var_code_variants(source, wave, question_row.get("var_code", ""))
    cached = question_row_cache.get(country_code)
    if cached is None or cached.empty:
        return pd.DataFrame(columns=cached.columns if cached is not None else None)
    if "var_code" not in cached.columns:
        return pd.DataFrame()
    index_variants = [str(value).upper() for value in lookup_variants if str(value).strip()]
    if not index_variants:
        return pd.DataFrame(columns=cached.columns)
    if alias_info.get("source_mapping_type") == "explicit_multiselect_children":
        available_required = [value for value in required_source_names if value in cached.index]
        if len(available_required) != len(required_source_names) or not available_required:
            return pd.DataFrame(columns=cached.columns)
        out = cached.loc[available_required].copy()
    elif alias_info.get("source_mapping_type") == "explicit_alias":
        available = [value for value in required_source_names if value in cached.index]
        if not available:
            available = [value for value in index_variants if value in cached.index]
        if not available:
            return pd.DataFrame(columns=cached.columns)
        out = cached.loc[[available[0]]].copy()
    else:
        available = [value for value in index_variants if value in cached.index]
        if not available:
            return pd.DataFrame(columns=cached.columns)
        out = cached.loc[[available[0]]].copy()
    if "canonical_wave" in out.columns:
        wave_candidates = list(
            dict.fromkeys(
                [
                    str(question_row.get("raw_wave", "")),
                    str(question_row.get("canonical_wave", "")),
                    canonical_wave_label(str(question_row.get("source", "")), str(question_row.get("raw_wave", ""))),
                ]
            )
        )
        out = out[out["canonical_wave"].astype(str).isin({str(value) for value in wave_candidates if str(value).strip()})]
    if not out.empty:
        out = out.copy()
        out["canonical_var_name"] = alias_info["canonical_var_name"]
        out["source_var_name"] = alias_info["source_var_name"]
        out["source_var_names"] = " | ".join(alias_info["source_var_names"]) if alias_info["source_var_names"] else ""
        out["source_mapping_type"] = alias_info["source_mapping_type"]
        out["source_mapping_authority"] = alias_info["source_mapping_authority"]
        out["source_mapping_query_var_codes"] = " | ".join(alias_info["query_var_codes"])
    return out.reset_index(drop=True)


def _load_question_checkpoint_tables(
    paths,
    question_index: int,
    question_row: pd.Series,
    table_names: list[str],
) -> dict[str, pd.DataFrame]:
    loaded: dict[str, pd.DataFrame] = {}
    for table_name in table_names:
        path = _question_checkpoint_path(paths, table_name, question_index, question_row)
        if path.exists():
            loaded[table_name] = pd.read_parquet(path)
    return loaded


def _slugify(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(value))
    out = out.strip("_")
    return out or "item"


def _question_key(question_row: pd.Series) -> str:
    return "__".join(
        _slugify(str(question_row.get(field, "")))
        for field in ["source", "canonical_wave", "country_code", "var_code", "question_id"]
    )


def _checkpoint_table_dir(paths, table_name: str) -> Path:
    path = paths.run_path / CHECKPOINT_ROOT_NAME / CHECKPOINT_TABLE_DIR / table_name
    path.mkdir(parents=True, exist_ok=True)
    return path


def _question_checkpoint_path(paths, table_name: str, question_index: int, question_row: pd.Series) -> Path:
    key = _question_key(question_row)
    return _checkpoint_table_dir(paths, table_name) / f"{question_index:06d}__{key}.parquet"


def _question_checkpoint_complete_path(paths, question_index: int, question_row: pd.Series) -> Path:
    key = _question_key(question_row)
    return _checkpoint_table_dir(paths, "question_universe") / f"{question_index:06d}__{key}{CHECKPOINT_COMPLETE_SUFFIX}"


def _question_use_contract_checkpoint_hash(question_row: pd.Series) -> str:
    contract_row = build_question_use_contract_row(
        question_row.to_dict(),
        survey_family=str(question_row.get("source") or question_row.get("source_family") or ""),
        canonical_wave=str(question_row.get("canonical_wave") or question_row.get("wave") or ""),
    )
    return str(contract_row.get("question_use_contract_hash", "") or "")


def _question_checkpoint_exists(paths, question_index: int, question_row: pd.Series) -> bool:
    if not _question_checkpoint_complete_path(paths, question_index, question_row).exists():
        return False
    checkpoint_path = _question_checkpoint_path(paths, "question_use_contract", question_index, question_row)
    if not checkpoint_path.exists():
        return False
    try:
        checkpoint = pd.read_parquet(checkpoint_path)
    except Exception:
        return False
    if checkpoint.empty or "question_use_contract_hash" not in checkpoint.columns:
        return False
    saved_hash_series = checkpoint["question_use_contract_hash"].fillna("").astype(str).str.strip()
    saved_hash_series = saved_hash_series[saved_hash_series.ne("")]
    if saved_hash_series.empty:
        return False
    saved_hash = str(saved_hash_series.iloc[0])
    current_hash = _question_use_contract_checkpoint_hash(question_row)
    if not current_hash:
        return False
    return saved_hash == current_hash


def _write_question_checkpoint(paths, table_name: str, question_index: int, question_row: pd.Series, frame: pd.DataFrame) -> None:
    out_path = _question_checkpoint_path(paths, table_name, question_index, question_row)
    frame.to_parquet(out_path, index=False)


def _mark_question_complete(paths, question_index: int, question_row: pd.Series) -> None:
    out_path = _question_checkpoint_complete_path(paths, question_index, question_row)
    out_path.write_text("complete\n", encoding="utf-8")


def _combine_checkpoint_tables(paths, table_name: str) -> pd.DataFrame:
    table_dir = _checkpoint_table_dir(paths, table_name)
    paths_list = sorted(table_dir.glob("*.parquet"))
    if not paths_list:
        return pd.DataFrame()
    frames = [pd.read_parquet(path) for path in paths_list]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True, sort=False)


def _combine_wave_checkpoint_tables(paths, table_name: str, question_rows: pd.DataFrame, progress_started: float | None = None) -> pd.DataFrame:
    if question_rows.empty:
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    if progress_started is not None:
        _log_progress(progress_started, f"combining {table_name} checkpoints ({len(question_rows)} questions)")
    for idx, row in enumerate(question_rows.itertuples(index=False), start=1):
        qrow = pd.Series(row._asdict())
        checkpoint_index = qrow.get("checkpoint_index", idx)
        try:
            checkpoint_index = int(checkpoint_index)
        except Exception:
            checkpoint_index = idx
        path = _question_checkpoint_path(paths, table_name, checkpoint_index, qrow)
        if path.exists():
            frames.append(pd.read_parquet(path))
            if progress_started is not None and (idx == 1 or idx % 50 == 0 or idx == len(question_rows)):
                _log_progress(progress_started, f"combined {table_name}{_process_label(table_name)}: read {idx}/{len(question_rows)} checkpoint files")
    if not frames:
        if progress_started is not None:
            _log_progress(progress_started, f"combined {table_name}{_process_label(table_name)}: 0 rows")
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True, sort=False)
    if progress_started is not None:
        _log_progress(progress_started, f"combined {table_name}{_process_label(table_name)}: {len(combined)} rows")
    return combined


def _cloud_replay_allowed(manifest: dict[str, Any]) -> tuple[bool, str]:
    if not bool(manifest.get("cloud_replay_allowed", False)):
        return False, "cloud_replay_not_explicitly_allowed"
    if str(manifest.get("cloud_engine_version", "")).strip() != CLOUD_ENGINE_VERSION:
        return False, "cloud_engine_version_mismatch"
    return True, ""


def _question_use_contract_replay_hash(paths) -> str:
    contract_path = paths.core / "question_use_contract.parquet"
    if not contract_path.exists():
        return ""
    try:
        contract = read_table_any(contract_path)
    except Exception:
        return ""
    if contract.empty:
        return ""
    columns = [
        "source",
        "wave",
        "canonical_wave",
        "question_id",
        "var_code",
        "semantic_role",
        "semantic_subrole",
        "directionality_policy",
        "allowed_as_attitude_cloud_anchor",
        "allowed_as_attitude_cloud_feature",
        "allowed_as_v551_relation_evidence",
        "source_structure_classification",
        "final_driver_scope",
        "mapping_status",
        "relation_axis_id",
        "target_entity_id",
        "driver_id",
        "driver_facet_id",
        "question_use_contract_joined",
        "source_structure_fields_joined",
    ]
    for column in columns:
        if column not in contract.columns:
            contract[column] = ""
    payload = (
        contract[columns]
        .fillna("")
        .astype(str)
        .sort_values(by=["source", "wave", "canonical_wave", "question_id", "var_code"], kind="mergesort")
        .to_dict(orient="records")
    )
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


def _load_replayed_cloud_tables(paths, progress_started: float | None = None, current_question_use_contract_hash: str | None = None) -> pd.DataFrame | None:
    manifest_path = paths.clouds / "cloud_refresh_manifest.json"
    attitude_path = paths.clouds / "question_response_attitude_cloud.parquet"
    if not manifest_path.exists() or not attitude_path.exists():
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if current_question_use_contract_hash is None:
        current_question_use_contract_hash = _question_use_contract_replay_hash(paths)
    allowed, blocked_reason = _cloud_replay_allowed(manifest)
    if not allowed:
        _write_json_report(
            paths.clouds / "cloud_replay_audit.json",
            {
                "cloud_engine_version": manifest.get("cloud_engine_version", ""),
                "cloud_replay_allowed": False,
                "blocked_reason": blocked_reason,
                "question_response_attitude_cloud_rows": 0,
                "created_at": utc_now(),
            },
        )
        if progress_started is not None:
            _log_progress(progress_started, f"skipping cloud replay: {blocked_reason}")
        return None
    manifest_question_use_hash = str(manifest.get("question_use_contract_hash", "") or "").strip()
    if not manifest_question_use_hash or not current_question_use_contract_hash or manifest_question_use_hash != current_question_use_contract_hash:
        _write_json_report(
            paths.clouds / "cloud_replay_audit.json",
            {
                "cloud_engine_version": manifest.get("cloud_engine_version", ""),
                "cloud_replay_allowed": False,
                "blocked_reason": "cloud_question_use_contract_hash_mismatch",
                "manifest_question_use_contract_hash": manifest_question_use_hash,
                "current_question_use_contract_hash": current_question_use_contract_hash,
                "question_response_attitude_cloud_rows": 0,
                "created_at": utc_now(),
            },
        )
        if progress_started is not None:
            _log_progress(progress_started, "skipping cloud replay: question_use_contract hash mismatch or missing")
        return None
    attitude_cloud = read_table_any(attitude_path)
    attitude_status = str(manifest.get("question_response_attitude_cloud_status", "")).strip().lower()
    if attitude_status.startswith("disabled") and not attitude_cloud.empty:
        _write_json_report(
            paths.clouds / "cloud_replay_audit.json",
            {
                "cloud_engine_version": manifest.get("cloud_engine_version", ""),
                "cloud_replay_allowed": False,
                "blocked_reason": "disabled_attitude_cloud_manifest_does_not_allow_non_empty_replay",
                "question_response_attitude_cloud_rows": int(len(attitude_cloud)),
                "created_at": utc_now(),
            },
        )
        if progress_started is not None:
            _log_progress(progress_started, "skipping cloud replay: disabled attitude cloud manifest does not permit non-empty replay payload")
        return None
    validation_issues = validate_attitude_cloud_rows(attitude_cloud)
    if validation_issues:
        _write_json_report(
            paths.clouds / "cloud_replay_audit.json",
            {
                "cloud_engine_version": manifest.get("cloud_engine_version", ""),
                "cloud_replay_allowed": False,
                "blocked_reason": "replayed_attitude_cloud_validation_failed",
                "question_response_attitude_cloud_rows": int(len(attitude_cloud)),
                "cloud_validation_issues": validation_issues,
                "created_at": utc_now(),
            },
        )
        if progress_started is not None:
            _log_progress(progress_started, "skipping cloud replay: attitude cloud validation failed")
        return None
    _write_json_report(
        paths.clouds / "cloud_replay_audit.json",
        {
            "cloud_engine_version": manifest.get("cloud_engine_version", ""),
            "cloud_replay_allowed": True,
            "blocked_reason": "",
            "manifest_question_use_contract_hash": manifest_question_use_hash,
            "current_question_use_contract_hash": current_question_use_contract_hash,
            "question_response_attitude_cloud_rows": int(len(attitude_cloud)),
            "question_response_attitude_cloud_status": manifest.get("question_response_attitude_cloud_status", ""),
            "branch_co_signature_status": manifest.get("branch_co_signature_status", ""),
            "created_at": utc_now(),
        },
    )
    if progress_started is not None:
        _log_progress(
            progress_started,
            "replaying cloud outputs from clouds/question_response_attitude_cloud.parquet",
        )
    return attitude_cloud


def _concat_frames(frames: list[pd.DataFrame]) -> pd.DataFrame:
    non_empty = [frame for frame in frames if frame is not None and not frame.empty]
    if not non_empty:
        return pd.DataFrame()
    return pd.concat(non_empty, ignore_index=True, sort=False)


def _log_progress(progress_started: float, message: str) -> None:
    elapsed = time.monotonic() - progress_started
    print(f"[v550b +{elapsed:0.0f}s] {message}", flush=True)


def _process_label(table_name: str) -> str:
    idx = PIPELINE_PROCESS_LABELS.get(table_name)
    return f" ({idx}/{PIPELINE_PROCESS_TOTAL})" if idx else ""


def _resolve_finalize_source(requested: str, *, resume_requested: bool, resume_skipped_questions: int) -> str:
    requested = str(requested or "auto").strip().lower()
    if requested not in FINALIZE_SOURCE_CHOICES:
        raise ValueError(f"Unsupported finalize source: {requested}")
    if requested == "auto":
        return "checkpoint" if resume_requested or resume_skipped_questions > 0 else "memory"
    if requested == "memory" and (resume_requested or resume_skipped_questions > 0):
        raise RuntimeError("finalize-source=memory is not safe when resume skips are present; use auto or checkpoint.")
    return requested


def _finalize_wave_checkpoint_tables(
    paths,
    *,
    finalize_source: str,
    wave_question_rows: pd.DataFrame,
    wave_table_accumulators: dict[str, list[pd.DataFrame]],
    wave_progress_started: float | None = None,
) -> tuple[dict[str, pd.DataFrame], dict[str, int]]:
    question_level_tables = [
        "question_universe",
        "question_use_contract",
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
    ]
    finalize_source = str(finalize_source or "memory").strip().lower()
    if finalize_source == "memory":
        wave_tables = {table_name: _concat_frames(wave_table_accumulators.get(table_name, [])) for table_name in question_level_tables}
        return wave_tables, {"finalize_rows_from_memory": int(sum(len(frame) for frames in wave_table_accumulators.values() for frame in frames)), "finalize_rows_from_checkpoint": 0, "finalize_checkpoint_table_reads": 0}

    if wave_progress_started is not None:
        _log_progress(wave_progress_started, f"finalizing wave tables from checkpoint files ({finalize_source})")
    wave_tables = {
        "question_universe": _combine_wave_checkpoint_tables(paths, "question_universe", wave_question_rows, wave_progress_started),
        "question_use_contract": _combine_wave_checkpoint_tables(paths, "question_use_contract", wave_question_rows, wave_progress_started),
        "answer_distribution": _combine_wave_checkpoint_tables(paths, "answer_distribution", wave_question_rows, wave_progress_started),
        "country_answer_distribution": _combine_wave_checkpoint_tables(paths, "country_answer_distribution", wave_question_rows, wave_progress_started),
        "position_indicator_summary": _combine_wave_checkpoint_tables(paths, "position_indicator_summary", wave_question_rows, wave_progress_started),
        "indicator_answer_matrix": _combine_wave_checkpoint_tables(paths, "indicator_answer_matrix", wave_question_rows, wave_progress_started),
        "outlier_cohort_summary": _combine_wave_checkpoint_tables(paths, "outlier_cohort_summary", wave_question_rows, wave_progress_started),
        "secondary_indicator_summary": _combine_wave_checkpoint_tables(paths, "secondary_indicator_summary", wave_question_rows, wave_progress_started),
        "recursive_branch_nodes": _combine_wave_checkpoint_tables(paths, "recursive_branch_nodes", wave_question_rows, wave_progress_started),
        "branch_position_signature": _combine_wave_checkpoint_tables(paths, "branch_position_signature", wave_question_rows, wave_progress_started),
        "branch_relation_co_signature": _combine_wave_checkpoint_tables(paths, "branch_relation_co_signature", wave_question_rows, wave_progress_started),
        "branch_co_signature": _combine_wave_checkpoint_tables(paths, "branch_co_signature", wave_question_rows, wave_progress_started),
        "question_response_attitude_cloud": _combine_wave_checkpoint_tables(paths, "question_response_attitude_cloud", wave_question_rows, wave_progress_started),
        "mapping_gap_report": _combine_wave_checkpoint_tables(paths, "mapping_gap_report", wave_question_rows, wave_progress_started),
    }
    return wave_tables, {
        "finalize_rows_from_memory": 0,
        "finalize_rows_from_checkpoint": int(sum(len(frame) for frame in wave_tables.values())),
        "finalize_checkpoint_table_reads": len(question_level_tables),
    }


def _write_json_report(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _wave_warning_report(
    *,
    run_id: str,
    wave_index: int,
    wave_total: int,
    wave_source: str,
    wave_wave: str,
    wave_question_rows: pd.DataFrame,
    wave_readiness_df: pd.DataFrame,
    wave_weight_df: pd.DataFrame,
    wave_mapping_df: pd.DataFrame,
    wave_legacy_df: pd.DataFrame,
    wave_underpowered_df: pd.DataFrame,
    wave_tables: dict[str, pd.DataFrame],
    response_review: pd.DataFrame,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    warnings: list[dict[str, Any]] = []

    def add_warning(code: str, severity: str, message: str, **details: Any) -> None:
        warnings.append(
            {
                "code": code,
                "severity": severity,
                "message": message,
                "wave_source": wave_source,
                "wave": wave_wave,
                "details": details,
            }
        )

    if wave_question_rows.empty:
        add_warning("no_questions", "high", "This wave produced no question rows after scope and mapping were applied.")
    if not wave_readiness_df.empty:
        non_ready = wave_readiness_df[~wave_readiness_df["readiness_status"].isin(["ready", "distribution_only"])]
        if not non_ready.empty:
            add_warning(
                "coverage_not_ready",
                "high",
                "Some scope rows are not fully ready for determinicity analysis.",
                counts=non_ready["readiness_status"].value_counts(dropna=False).to_dict(),
            )
        if "weight_status" in wave_readiness_df.columns:
            unweighted = wave_readiness_df[wave_readiness_df["weight_status"].eq("unweighted_only")]
            if not unweighted.empty:
                add_warning(
                    "weight_missing",
                    "medium",
                    "Some or all rows in this wave do not have loaded weights.",
                    rows=int(len(unweighted)),
                    respondent_rows=int(unweighted["respondents"].fillna(0).sum()),
                )
        if "legacy_leak_flag" in wave_readiness_df.columns:
            legacy = wave_readiness_df[wave_readiness_df["legacy_leak_flag"]]
            if not legacy.empty:
                add_warning(
                    "legacy_leak",
                    "medium",
                    "Legacy driver mappings are still present for some rows in this wave.",
                    rows=int(len(legacy)),
                )
    if not wave_underpowered_df.empty:
        add_warning(
            "underpowered_rows",
            "medium",
            "Some scope rows were marked underpowered by readiness.",
            rows=int(len(wave_underpowered_df)),
        )
    if not wave_mapping_df.empty:
        if "legacy_leak_rows" in wave_mapping_df.columns:
            legacy_rows = wave_mapping_df["legacy_leak_rows"].fillna(0).astype(int)
            if legacy_rows.sum() > 0:
                add_warning(
                    "mapping_leak",
                    "medium",
                    "Question structural mapping still has legacy leak rows for this wave.",
                    rows=int(legacy_rows.sum()),
                )
        if "mapped_rows" in wave_mapping_df.columns and wave_mapping_df["mapped_rows"].fillna(0).sum() == 0:
            add_warning(
                "mapping_insufficient",
                "high",
                "This wave has no mapped rows in question_structural_mapping.",
            )
    if not wave_weight_df.empty:
        weight_rows = int(wave_weight_df["weight_rows"].fillna(0).sum()) if "weight_rows" in wave_weight_df.columns else 0
        primary_weight_rows = int(wave_weight_df["primary_weight_rows"].fillna(0).sum()) if "primary_weight_rows" in wave_weight_df.columns else 0
        if weight_rows == 0:
            add_warning("weight_absent", "medium", "No survey_weight_fact rows were loaded for this wave.")
        elif primary_weight_rows == 0:
            add_warning("weight_primary_missing", "medium", "Weight rows exist, but none were marked primary for this wave.")
    if not response_review.empty:
        add_warning(
            "response_option_manual_review",
            "low",
            "The response-option builder still has manual-review items in the source map.",
            rows=int(len(response_review)),
        )
    for table_name, frame in wave_tables.items():
        if frame.empty and table_name in {"question_universe", "answer_distribution"} and not wave_question_rows.empty:
            add_warning(
                "empty_output",
                "high",
                f"{table_name} ended up empty for this wave even though questions were processed.",
            )

    summary = {
        "run_id": run_id,
        "wave_index": wave_index,
        "wave_total": wave_total,
        "wave_source": wave_source,
        "wave": wave_wave,
        "question_rows": int(len(wave_question_rows)),
        "readiness_rows": int(len(wave_readiness_df)),
        "warnings": warnings,
    }
    return warnings, summary


def _wave_report_dir(paths, wave_source: str, wave_wave: str) -> Path:
    return paths.run_path / "waves" / f"{_slugify(wave_source)}__{_slugify(wave_wave)}"


def _harmonize_question_frame(
    df: pd.DataFrame,
    semantics_lookup: dict[tuple[str, str, str, str], dict[str, Any]],
    *,
    response_semantics_contract_hash: str = "",
) -> pd.DataFrame:
    if df.empty:
        return df
    out = df.copy().reset_index(drop=True)
    raw_codes = out["value_raw"].map(normalize_response_code) if "value_raw" in out.columns else pd.Series([""] * len(out), index=out.index, dtype="object")
    text_codes = out["value_text"].map(normalize_response_code) if "value_text" in out.columns else pd.Series([""] * len(out), index=out.index, dtype="object")
    out["response_value_normalized"] = raw_codes.fillna("").astype(str)
    out.loc[out["response_value_normalized"].str.strip().eq(""), "response_value_normalized"] = text_codes.fillna("").astype(str)
    out.loc[out["response_value_normalized"].str.strip().eq(""), "response_value_normalized"] = out.get("value_text", pd.Series([""] * len(out), index=out.index)).fillna("").astype(str)
    out.loc[out["response_value_normalized"].str.strip().eq(""), "response_value_normalized"] = out.get("value_raw", pd.Series([""] * len(out), index=out.index)).fillna("").astype(str)

    columns: dict[str, list[Any]] = {
        "response_label": [],
        "normalized_response_label": [],
        "response_family": [],
        "normalization_confidence": [],
        "response_direction": [],
        "response_intensity": [],
        "polarity": [],
        "ordinal_rank": [],
        "scale_min": [],
        "scale_max": [],
        "scale_direction": [],
        "directionality_status": [],
        "is_substantive": [],
        "is_missing": [],
        "is_special": [],
        "is_dk": [],
        "is_refusal": [],
        "is_iap": [],
        "is_not_asked": [],
        "is_inapplicable": [],
        "response_option_map_matched": [],
        "response_semantics_status": [],
        "response_semantics_source": [],
        "response_semantics_contract_hash": [],
    }

    for row in out.itertuples(index=False):
        source = getattr(row, "source", "")
        waves = [getattr(row, "wave", ""), getattr(row, "canonical_wave", "")]
        var_code = _first_clean_value(getattr(row, "var_code", ""), getattr(row, "var_name", ""), getattr(row, "question_id", ""))
        normalized_code = _clean(getattr(row, "response_value_normalized", ""))
        values = [
            normalized_code,
            getattr(row, "value_raw", ""),
            getattr(row, "value_text", ""),
        ]
        sem: dict[str, Any] = {}
        for key in _response_semantics_key_candidates(
            source=source,
            waves=waves,
            var_code=var_code,
            values=values,
        ):
            candidate = semantics_lookup.get(key)
            if candidate:
                sem = candidate
                break

        matched = bool(sem)
        label = _first_clean_value(
            sem.get("response_label"),
            sem.get("normalized_response_label"),
            sem.get("value_label_clean"),
            getattr(row, "value_text", ""),
            getattr(row, "value_raw", ""),
            normalized_code,
        ) or normalized_code
        normalized_label = _first_clean_value(sem.get("normalized_response_label"), sem.get("value_label_clean"), label) or label

        if matched:
            is_substantive = _to_bool(sem.get("is_substantive", False))
            is_missing = _to_bool(sem.get("is_missing", False))
            is_dk = _to_bool(sem.get("is_dk", False))
            is_refusal = _to_bool(sem.get("is_refusal", False))
            is_iap = _to_bool(sem.get("is_iap", False))
            is_not_asked = _to_bool(sem.get("is_not_asked", False))
            is_inapplicable = _to_bool(sem.get("is_inapplicable", False))
            explicit_special = _to_bool(sem.get("is_special", False))
            is_special = explicit_special or is_missing or is_dk or is_refusal or is_iap or is_not_asked or is_inapplicable
            status = _clean(sem.get("response_semantics_status", ""))
            source_value = _clean(sem.get("response_semantics_source", ""))
            contract_hash = _clean(sem.get("response_semantics_contract_hash", "")) or response_semantics_contract_hash
            confidence = _clean(sem.get("normalization_confidence", ""))
            direction = _clean(sem.get("response_direction", ""))
            intensity = sem.get("response_intensity", None)
            polarity = _clean(sem.get("polarity", ""))
            ordinal_rank = sem.get("ordinal_rank", None)
            scale_min = sem.get("scale_min", None)
            scale_max = sem.get("scale_max", None)
            scale_direction = _clean(sem.get("scale_direction", ""))
            directionality_status = _clean(sem.get("directionality_status", "")) or "unknown"
        else:
            is_substantive = False
            is_missing = normalized_code in {"", "nan", "none"}
            is_dk = is_refusal = is_iap = is_not_asked = is_inapplicable = False
            is_special = is_missing
            status = "observed_only"
            source_value = "observed_response_row"
            contract_hash = response_semantics_contract_hash
            confidence = "observed_only"
            direction = ""
            intensity = None
            polarity = ""
            ordinal_rank = None
            scale_min = None
            scale_max = None
            scale_direction = ""
            directionality_status = "NOT_CERTIFIED_SPECIAL" if is_special else "not_certified"

        if is_special:
            direction = ""
            intensity = None
            polarity = ""
            ordinal_rank = None
            scale_min = None
            scale_max = None
            scale_direction = ""
            directionality_status = "NOT_CERTIFIED_SPECIAL"

        values_out = {
            "response_label": label,
            "normalized_response_label": normalized_label,
            "response_family": _clean(sem.get("response_family", "")) if matched else "",
            "normalization_confidence": confidence,
            "response_direction": direction,
            "response_intensity": intensity,
            "polarity": polarity,
            "ordinal_rank": ordinal_rank,
            "scale_min": scale_min,
            "scale_max": scale_max,
            "scale_direction": scale_direction,
            "directionality_status": directionality_status,
            "is_substantive": is_substantive,
            "is_missing": is_missing,
            "is_special": is_special,
            "is_dk": is_dk,
            "is_refusal": is_refusal,
            "is_iap": is_iap,
            "is_not_asked": is_not_asked,
            "is_inapplicable": is_inapplicable,
            "response_option_map_matched": matched,
            "response_semantics_status": status,
            "response_semantics_source": source_value,
            "response_semantics_contract_hash": contract_hash,
        }
        for column, value in values_out.items():
            columns[column].append(value)

    for column, values in columns.items():
        out[column] = values
    return out


def _summary_question_meta(df: pd.DataFrame, question_row: pd.Series, readiness_row: pd.Series | None = None) -> dict[str, Any]:
    alias_info = resolve_question_var_aliases(question_row.get("source", ""), question_row.get("canonical_wave", ""), question_row.get("var_code", ""))
    dominant_series = df["normalized_response_label"].fillna("").astype(str) if "normalized_response_label" in df.columns else df["response_value_normalized"].fillna("").astype(str)
    response_label, response_pct = dominant_response(dominant_series, df["weight_value"] if "weight_value" in df.columns else None)
    has_response_option_map = bool(df["response_option_map_matched"].fillna(False).any()) if "response_option_map_matched" in df.columns else False
    response_direction = _first_nonempty(df["response_direction"], "") if "response_direction" in df.columns else ""
    response_intensity = _first_nonempty(df["response_intensity"], "") if "response_intensity" in df.columns else ""
    polarity = _first_nonempty(df["polarity"], "") if "polarity" in df.columns else ""
    ordinal_rank = _first_nonempty(df["ordinal_rank"], "") if "ordinal_rank" in df.columns else ""
    scale_min = _first_nonempty(df["scale_min"], "") if "scale_min" in df.columns else ""
    scale_max = _first_nonempty(df["scale_max"], "") if "scale_max" in df.columns else ""
    scale_direction = _first_nonempty(df["scale_direction"], "") if "scale_direction" in df.columns else ""
    directionality_status = _first_nonempty(df["directionality_status"], "unknown") if "directionality_status" in df.columns else "unknown"
    response_semantics_status = _first_nonempty(df["response_semantics_status"], "observed_only") if "response_semantics_status" in df.columns else "observed_only"
    response_semantics_source = _first_nonempty(df["response_semantics_source"], "observed_response_row") if "response_semantics_source" in df.columns else "observed_response_row"
    response_semantics_contract_hash = _first_nonempty(df["response_semantics_contract_hash"], "") if "response_semantics_contract_hash" in df.columns else ""
    return {
        "run_id": "",
        "source": question_row["source"],
        "source_family": question_row["source"],
        "wave": question_row["canonical_wave"],
        "canonical_wave": question_row["canonical_wave"],
        "country_code": question_row["country_code"],
        "survey_year": int(df["survey_year"].dropna().iloc[0]) if "survey_year" in df.columns and df["survey_year"].notna().any() else None,
        "canonical_var_name": alias_info["canonical_var_name"],
        "source_var_name": alias_info["source_var_name"],
        "source_var_names": " | ".join(alias_info["source_var_names"]) if alias_info["source_var_names"] else "",
        "source_mapping_type": alias_info["source_mapping_type"],
        "source_mapping_authority": alias_info["source_mapping_authority"],
        "var_code": question_row["var_code"],
        "var_name": question_row["var_code"],
        "question_id": question_row["question_id"],
        "question_text": str(df["question_text"].dropna().iloc[0]) if "question_text" in df.columns and df["question_text"].notna().any() else "",
        "driver_id": question_row.get("driver_id", ""),
        "driver_facet_id": question_row.get("driver_facet_id", ""),
        "relation_axis_id": question_row.get("relation_axis_id", ""),
        "target_entity_id": question_row.get("target_entity_id", ""),
        "mapping_status": question_row.get("mapping_status", ""),
        "legacy_final_driver_id": question_row.get("legacy_final_driver_id", ""),
        "legacy_driver_leak_flag": _to_bool(question_row.get("legacy_final_driver_id", "") and not question_row.get("driver_facet_id", "")),
        "question_type": question_row.get("question_type", ""),
        "handling_rule": question_row.get("handling_rule", ""),
        "recommended_computation": question_row.get("recommended_computation", ""),
        "source_structure_classification": question_row.get("source_structure_classification", ""),
        "response_direction": response_direction,
        "response_intensity": response_intensity,
        "polarity": polarity,
        "ordinal_rank": ordinal_rank,
        "scale_min": scale_min,
        "scale_max": scale_max,
        "scale_direction": scale_direction,
        "directionality_status": directionality_status,
        "response_family": str(df["response_family"].dropna().astype(str).iloc[0]) if "response_family" in df.columns and df["response_family"].notna().any() else "",
        "response_semantics_status": response_semantics_status,
        "response_semantics_source": response_semantics_source,
        "response_semantics_contract_hash": response_semantics_contract_hash,
        "has_response_option_map": has_response_option_map,
        "response_option_confidence_min": "",
        "response_option_confidence_max": "",
        "n_response_rows": int(len(df)),
        "n_respondents": int(df["respondent_id"].nunique()),
        "n_countries": int(df["country_code"].nunique()) if "country_code" in df.columns else 0,
        "weight_status": _safe_weight_status(df["weight_value"] if "weight_value" in df.columns else None),
        "readiness_status": readiness_row.get("readiness_status", "") if readiness_row is not None else "",
        "dominant_response_value": response_label,
        "dominant_response_pct": response_pct,
        "created_at": pd.Timestamp.utcnow().isoformat(),
    }


def _carry_forward_summary(question_use_contract: pd.DataFrame, *, run_id: str = "") -> pd.DataFrame:
    columns = [
        "run_id",
        "question_id",
        "var_code",
        "source",
        "wave",
        "canonical_wave",
        "semantic_role",
        "v551_evidence_role",
        "carry_forward_status",
        "carry_forward_reason",
        "carry_forward_layer",
        "allowed_as_context_distribution",
        "allowed_as_parent_prior_coordinate",
        "allowed_as_temporal_pressure_indicator",
        "allowed_as_runtime_persona_evidence",
        "allowed_as_v551_relation_evidence",
        "question_type",
        "handling_rule",
        "mapping_status",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_fields_joined",
        "created_at",
    ]
    if question_use_contract.empty:
        return pd.DataFrame(columns=columns)
    frame = question_use_contract.copy()
    for column in [
        "allowed_as_context_distribution",
        "allowed_as_parent_prior_coordinate",
        "allowed_as_temporal_pressure_indicator",
        "allowed_as_runtime_persona_evidence",
        "allowed_as_v551_relation_evidence",
    ]:
        if column not in frame.columns:
            frame[column] = False
    for column in [
        "semantic_role",
        "v551_evidence_role",
        "question_type",
        "handling_rule",
        "mapping_status",
        "source_structure_classification",
        "source_structure_basis",
        "source_structure_confidence",
        "source_structure_source",
        "source_structure_fields_joined",
    ]:
        if column not in frame.columns:
            frame[column] = ""

    def _status(row: pd.Series) -> tuple[str, str, str]:
        if _to_bool(row.get("allowed_as_runtime_persona_evidence"), False):
            return "context_forwardable", "runtime_persona_context", "persona"
        if _to_bool(row.get("allowed_as_temporal_pressure_indicator"), False):
            return "context_forwardable", "temporal_pressure_context", "pressure"
        if _to_bool(row.get("allowed_as_parent_prior_coordinate"), False):
            return "context_forwardable", "parent_prior_context", "prior"
        if _to_bool(row.get("allowed_as_context_distribution"), False):
            return "context_forwardable", "distribution_context", "context"
        return "context_holdout", "not_forwardable", "holdout"

    statuses = frame.apply(_status, axis=1, result_type="expand")
    frame["carry_forward_status"] = statuses[0]
    frame["carry_forward_reason"] = statuses[1]
    frame["carry_forward_layer"] = statuses[2]
    frame["run_id"] = run_id
    frame["created_at"] = utc_now()
    return frame.loc[:, columns]


def main() -> int:
    args = parse_args()
    load_dotenv(Path(args.env_file))
    run_id = args.run_id or make_run_id("v550b")
    paths = ensure_directories(Path(args.output_root), run_id)
    conn = connect_from_env(args.db_url, Path(args.env_file))
    source_filters = [s for s in args.source if s]
    wave_filters = [w for w in args.wave if w]
    country_filters = [c for c in args.country if c]
    filters = {"source": source_filters, "wave": wave_filters, "country": country_filters}

    codebook_roots = [DEFAULT_CODEBOOK_ROOT]
    questions_master_drivers = DEFAULT_QUESTIONS_MASTER_DRIVERS
    questions_master_semantic = DEFAULT_QUESTIONS_MASTER_SEMANTIC
    question_structure_register = DEFAULT_STRUCTURE_REGISTER
    question_type_taxonomy = DEFAULT_TAXONOMY
    source_structure_register = load_question_structure_register(question_structure_register)

    response_map = _load_response_option_map(args.response_option_map) if args.response_option_map else pd.DataFrame()
    if response_map.empty:
        response_map, response_review, response_manifest = build_response_option_map(
            codebook_roots=codebook_roots,
            questions_master_drivers=questions_master_drivers,
            questions_master_semantic=questions_master_semantic,
            question_structure_register=question_structure_register,
            question_type_taxonomy=question_type_taxonomy,
            db_conn=conn,
            limit_questions=args.limit_questions,
        )
    else:
        response_review = pd.DataFrame()
        response_manifest = {"option_rows": len(response_map), "manual_review_rows": 0, "warnings": ["Loaded response option map from supplied path."]}

    semantics_lookup = _lookup_response_semantics(response_map)
    response_semantics_contract = response_semantics_contract_hash(response_map) if not response_map.empty else ""

    try:
        progress_started = time.monotonic()
        _log_progress(progress_started, "loading scope manifest")
        scope_df = load_scope_manifest(conn, source_filters, wave_filters, country_filters)
        scope_df = scope_df.sort_values(["source", "wave", "country_code"]).reset_index(drop=True)
        if args.smoke and not scope_df.empty:
            scope_df = scope_df.head(1).reset_index(drop=True)
        _log_progress(progress_started, f"scope manifest loaded: {len(scope_df)} scope rows")
        _log_progress(progress_started, "verifying facet-ready view contract")
        _assert_facet_ready_view_contract(conn)
        _log_progress(progress_started, "facet-ready view contract verified")
        wave_scopes = _iter_wave_scopes(scope_df)
        if not wave_scopes:
            raise RuntimeError("No scope rows found for the requested filters.")

        response_review = response_review if isinstance(response_review, pd.DataFrame) else pd.DataFrame(response_review)
        accumulators: dict[str, list[pd.DataFrame]] = {
            "question_universe": [],
            "question_use_contract": [],
            "position_distribution": [],
            "answer_distribution": [],
            "country_answer_distribution": [],
            "position_indicator_summary": [],
            "indicator_answer_matrix": [],
            "outlier_cohort_summary": [],
            "secondary_indicator_summary": [],
            "recursive_branch_nodes": [],
            "branch_position_signature": [],
            "branch_relation_co_signature": [],
            "branch_co_signature": [],
            "question_response_attitude_cloud": [],
            "mapping_gap_report": [],
            "scope_manifest": [],
            "substrate_readiness": [],
            "position_field_coverage": [],
            "weight_coverage": [],
            "mapping_status_coverage": [],
            "legacy_leak_report": [],
            "underpowered_quarantine": [pd.DataFrame()],
        }

        completed_questions = 0
        skipped_questions = 0
        resume_skipped_questions = 0
        harmonization_call_count_hot_path = 0
        harmonization_row_count_hot_path = 0
        harmonization_call_count_fallback = 0
        harmonization_row_count_fallback = 0
        empty_question_waves = 0
        question_budget = args.smoke_questions if args.smoke else (args.max_questions if args.max_questions is not None else args.limit_questions)
        total_questions = 0
        budget_exhausted = False
        run_warnings: list[str] = []
        wave_warning_summaries: list[dict[str, Any]] = []
        performance_wave_profiles: list[dict[str, Any]] = []

        for wave_idx, (wave_source, wave_wave, wave_scope_df) in enumerate(wave_scopes, start=1):
            if question_budget is not None and question_budget <= 0:
                break

            wave_country_filters = sorted({str(value) for value in wave_scope_df["country_code"].dropna().astype(str) if str(value).strip()})
            wave_canonical = canonical_wave_label(wave_source, wave_wave)
            if wave_canonical != wave_wave:
                wave_scope_df = wave_scope_df.copy()
                wave_scope_df["wave"] = wave_canonical
                wave_wave = wave_canonical
            _log_progress(progress_started, f"wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: building readiness")
            wave_readiness_df, wave_pos_df, wave_weight_df, wave_mapping_coverage_df, wave_legacy_df, wave_underpowered_df = build_readiness(
                conn,
                wave_scope_df,
                min_cell_n=args.min_cell_n,
                source_filters=[wave_source],
                wave_filters=[wave_wave],
                country_filters=wave_country_filters,
                progress_started=progress_started,
                log_prefix=f"full_readiness[{wave_source}/{wave_wave}]",
            )
            _log_progress(progress_started, f"wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: loading question mappings")
            wave_question_mapping_df = _load_wave_question_mapping(conn, wave_source, wave_wave)
            missing_structure_columns = list(wave_question_mapping_df.attrs.get("missing_structure_columns", []))
            if missing_structure_columns:
                run_warnings.append(
                    f"Wave {wave_source} / {wave_wave}: question_structural_mapping missing optional columns {missing_structure_columns}"
                )
            _assert_live_contracts(wave_scope_df, wave_readiness_df, wave_question_mapping_df)

            accumulators["scope_manifest"].append(wave_scope_df)
            accumulators["substrate_readiness"].append(wave_readiness_df)
            accumulators["position_field_coverage"].append(wave_pos_df)
            accumulators["weight_coverage"].append(wave_weight_df)
            accumulators["mapping_status_coverage"].append(wave_mapping_coverage_df)
            accumulators["legacy_leak_report"].append(wave_legacy_df)
            accumulators["underpowered_quarantine"].append(wave_underpowered_df)
            _log_progress(progress_started, f"wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: building question list")
            wave_question_rows = _build_question_list(wave_scope_df, wave_question_mapping_df, question_budget)
            wave_source_structure_audit = build_source_structure_population_audit(wave_question_rows, source_structure_register)
            validation_dir = DEFAULT_VALIDATION_ROOT / f"{_slugify(wave_source)}_{_slugify(wave_wave)}"
            write_source_structure_population_audit(wave_source_structure_audit, validation_dir / "source_structure_population_audit.csv")
            if wave_question_rows.empty:
                empty_question_waves += 1
                run_warnings.append(f"Wave {wave_source} / {wave_wave} produced no question rows.")
                if args.verbose:
                    elapsed = time.monotonic() - progress_started
                    print(f"[v550b +{elapsed:0.0f}s] wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: no question rows", flush=True)
                continue
            _assert_live_contracts(wave_scope_df, wave_readiness_df, wave_question_mapping_df, wave_question_rows)

            total_questions += len(wave_question_rows)
            readiness_lookup = {
                (str(r.source), str(r.wave), str(r.country_code)): r._asdict() for r in wave_readiness_df.itertuples(index=False)
            }

            if args.verbose:
                elapsed = time.monotonic() - progress_started
                print(
                    f"[v550b +{elapsed:0.0f}s] wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: questions={len(wave_question_rows)} countries={len(wave_country_filters)}",
                    flush=True,
                )
            _log_progress(progress_started, f"wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: processing questions")
            reset_attitude_cloud_state()
            wave_resume_skipped_questions = 0
            wave_table_accumulators: dict[str, list[pd.DataFrame]] = {
                "question_universe": [],
                "question_use_contract": [],
                "answer_distribution": [],
                "country_answer_distribution": [],
                "position_indicator_summary": [],
                "indicator_answer_matrix": [],
                "outlier_cohort_summary": [],
                "secondary_indicator_summary": [],
                "recursive_branch_nodes": [],
                "branch_position_signature": [],
                "branch_relation_co_signature": [],
                "branch_co_signature": [],
                "question_response_attitude_cloud": [],
                "mapping_gap_report": [],
            }
            question_row_cache = _prefetch_question_rows_by_country(
                conn,
                wave_question_rows,
                progress_started,
                response_semantics_contract_hash=response_semantics_contract,
            )
            question_row_cache, prepared_cache_stats = _prepare_v550_question_row_cache(
                question_row_cache,
                semantics_lookup,
                response_semantics_contract_hash=response_semantics_contract,
                mode=args.v550_prepared_substrate_mode,
                progress_started=progress_started,
            )
            prepared_substrate_mode = args.v550_prepared_substrate_mode != "off"

            for idx, q in enumerate(wave_question_rows.itertuples(index=False), start=1):
                qrow = pd.Series(q._asdict())
                qkey = _question_key(qrow)
                if args.resume and _question_checkpoint_exists(paths, idx, qrow):
                    skipped_questions += 1
                    resume_skipped_questions += 1
                    wave_resume_skipped_questions += 1
                    if args.verbose:
                        elapsed = time.monotonic() - progress_started
                        print(f"[v550b +{elapsed:0.0f}s] skip question {idx}/{len(wave_question_rows)} {qkey} (checkpoint exists)", flush=True)
                    continue

                df = _question_rows_from_cache(qrow, question_row_cache)
                if df.empty:
                    fallback_df = _question_rows(
                        conn,
                        qrow,
                        filters,
                        response_semantics_contract_hash=response_semantics_contract,
                    )
                    if fallback_df.empty:
                        # A no-row question is usually a country-level not-asked or otherwise empty cell.
                        # Count it as handled so we can complete the wave without fabricating response rows.
                        skipped_questions += 1
                        _mark_question_complete(paths, idx, qrow)
                        if args.verbose:
                            elapsed = time.monotonic() - progress_started
                            print(f"[v550b +{elapsed:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: no rows returned; counted as skipped", flush=True)
                        continue
                    if prepared_substrate_mode:
                        harmonization_call_count_fallback += 1
                        harmonization_row_count_fallback += len(fallback_df)
                    else:
                        harmonization_call_count_hot_path += 1
                        harmonization_row_count_hot_path += len(fallback_df)
                    df = _harmonize_question_frame(
                        fallback_df,
                        semantics_lookup,
                        response_semantics_contract_hash=response_semantics_contract,
                    )
                elif not prepared_substrate_mode:
                    harmonization_call_count_hot_path += 1
                    harmonization_row_count_hot_path += len(df)
                    df = _harmonize_question_frame(df, semantics_lookup, response_semantics_contract_hash=response_semantics_contract)
                else:
                    pass
                qmeta = _summary_question_meta(df, qrow, readiness_lookup.get((qrow["source"], qrow["canonical_wave"], qrow["country_code"])))
                qmeta["run_id"] = run_id
                qmeta["shard_id"] = f"{wave_source}__{wave_wave}"
                source_structure_row, source_structure_join_key, source_structure_join_confidence = match_source_structure_row({**qrow.to_dict(), **qmeta}, source_structure_register)
                qrow = qrow.copy()
                for key, value in source_structure_row.items():
                    qrow[key] = value
                    qmeta[key] = value
                qrow["source_structure_join_key"] = source_structure_join_key
                qrow["source_structure_join_confidence"] = source_structure_join_confidence
                qmeta["source_structure_join_key"] = source_structure_join_key
                qmeta["source_structure_join_confidence"] = source_structure_join_confidence
                question_use_contract_row = build_question_use_contract_row(
                    {
                        **qmeta,
                        "source_structure_fields_joined": bool(qmeta.get("source_structure_fields_joined", False)),
                        "question_type": qrow.get("question_type", qmeta.get("question_type", "")),
                        "handling_rule": qrow.get("handling_rule", qmeta.get("handling_rule", "")),
                        "recommended_computation": qrow.get("recommended_computation", qmeta.get("recommended_computation", "")),
                        "final_driver_scope": qrow.get("final_driver_scope", qmeta.get("final_driver_scope", "")),
                        "source_structure_classification": qrow.get("source_structure_classification", qmeta.get("source_structure_classification", "")),
                    },
                    survey_family=wave_source,
                    canonical_wave=wave_wave,
                )
                qmeta.update(question_use_contract_row)
                qmeta["question_use_contract_joined"] = True
                weight_status, weights, answer_df, country_answer_df, mapping_gap_df, underpowered_df = build_distribution_tables(
                    df,
                    qmeta,
                    min_answer_n=args.min_answer_n,
                    min_cell_n=args.min_cell_n,
                    semantics_lookup=semantics_lookup,
                )
                if not _to_bool(qmeta.get("allowed_as_response_distribution", False)):
                    answer_df = answer_df.iloc[0:0].copy()
                    country_answer_df = country_answer_df.iloc[0:0].copy()
                qmeta["weight_status"] = weight_status
                question_universe_df = pd.DataFrame([qmeta])
                _write_question_checkpoint(paths, "question_universe", idx, qrow, question_universe_df)
                wave_table_accumulators["question_universe"].append(question_universe_df)
                question_use_contract_df = pd.DataFrame([question_use_contract_row])
                _write_question_checkpoint(paths, "question_use_contract", idx, qrow, question_use_contract_df)
                wave_table_accumulators["question_use_contract"].append(question_use_contract_df)
                if not mapping_gap_df.empty:
                    _write_question_checkpoint(paths, "mapping_gap_report", idx, qrow, mapping_gap_df)
                    wave_table_accumulators["mapping_gap_report"].append(mapping_gap_df)
                if not underpowered_df.empty:
                    accumulators["underpowered_quarantine"].append(underpowered_df)
                _write_question_checkpoint(paths, "answer_distribution", idx, qrow, answer_df)
                wave_table_accumulators["answer_distribution"].append(answer_df)
                _write_question_checkpoint(paths, "country_answer_distribution", idx, qrow, country_answer_df)
                wave_table_accumulators["country_answer_distribution"].append(country_answer_df)

                branch_df = prepare_question_frame(df)
                question_meta = {
                    **qmeta,
                    "source_structure_fields_joined": bool(qmeta.get("source_structure_fields_joined", False)),
                    "question_type": qrow.get("question_type", qmeta.get("question_type", "")),
                    "handling_rule": qrow.get("handling_rule", qmeta.get("handling_rule", "")),
                    "recommended_computation": qrow.get("recommended_computation", qmeta.get("recommended_computation", "")),
                }
                position_summary_df = pd.DataFrame(indicator_summary_rows(branch_df, question_meta, weights))
                secondary_summary_df = pd.DataFrame(
                    secondary_indicator_summary_rows(branch_df, question_meta, weights),
                    columns=SECONDARY_INDICATOR_SUMMARY_COLUMNS,
                )
                indicator_matrix_df = pd.DataFrame(indicator_answer_matrix_rows(branch_df, question_meta, weights))
                outlier_summary_df = pd.DataFrame(outlier_cohort_rows(branch_df, question_meta))
                recursive_nodes_df = pd.DataFrame(branch_nodes_rows(branch_df, question_meta, max_depth=args.max_depth, min_branch_n=args.min_branch_n))
                _write_question_checkpoint(paths, "position_indicator_summary", idx, qrow, position_summary_df)
                _write_question_checkpoint(paths, "secondary_indicator_summary", idx, qrow, secondary_summary_df)
                _write_question_checkpoint(paths, "indicator_answer_matrix", idx, qrow, indicator_matrix_df)
                _write_question_checkpoint(paths, "outlier_cohort_summary", idx, qrow, outlier_summary_df)
                _write_question_checkpoint(paths, "recursive_branch_nodes", idx, qrow, recursive_nodes_df)
                wave_table_accumulators["position_indicator_summary"].append(position_summary_df)
                wave_table_accumulators["secondary_indicator_summary"].append(secondary_summary_df)
                wave_table_accumulators["indicator_answer_matrix"].append(indicator_matrix_df)
                wave_table_accumulators["outlier_cohort_summary"].append(outlier_summary_df)
                wave_table_accumulators["recursive_branch_nodes"].append(recursive_nodes_df)
                wave_respondents = int(question_meta.get("n_respondents", 0) or 0)
                if should_emit_cloud_tables(
                    len(branch_df),
                    cloud_mode=args.cloud_mode,
                    cloud_max_branch_rows=args.cloud_max_branch_rows,
                    cloud_max_branch_share=args.cloud_max_branch_share,
                    wave_respondents=wave_respondents,
                ):
                    branch_position_signature_df = pd.DataFrame(build_position_signature_rows(branch_df, question_meta))
                    branch_relation_co_signature_df = pd.DataFrame(build_co_signature_rows(branch_df, question_meta))
                    branch_co_signature_df = branch_relation_co_signature_df.copy()
                    question_response_attitude_cloud_df = pd.DataFrame(build_attitude_cloud_rows(branch_df, question_meta))
                    _write_question_checkpoint(paths, "branch_position_signature", idx, qrow, branch_position_signature_df)
                    _write_question_checkpoint(paths, "branch_relation_co_signature", idx, qrow, branch_relation_co_signature_df)
                    _write_question_checkpoint(paths, "branch_co_signature", idx, qrow, branch_co_signature_df)
                    _write_question_checkpoint(paths, "question_response_attitude_cloud", idx, qrow, question_response_attitude_cloud_df)
                    wave_table_accumulators["branch_position_signature"].append(branch_position_signature_df)
                    wave_table_accumulators["branch_relation_co_signature"].append(branch_relation_co_signature_df)
                    wave_table_accumulators["branch_co_signature"].append(branch_co_signature_df)
                    wave_table_accumulators["question_response_attitude_cloud"].append(question_response_attitude_cloud_df)

                _mark_question_complete(paths, idx, qrow)

                completed_questions += 1
                if args.verbose and (idx == 1 or idx % 50 == 0 or idx == len(wave_question_rows)):
                    elapsed = time.monotonic() - progress_started
                    print(
                        f"[v550b +{elapsed:0.0f}s] question {idx}/{len(wave_question_rows)} {qkey}: rows={len(df)} completed={completed_questions} skipped={skipped_questions}",
                        flush=True,
                    )
                elif completed_questions % 10 == 0:
                    elapsed = time.monotonic() - progress_started
                    print(
                        f"[v550b +{elapsed:0.0f}s] progress {completed_questions}/{total_questions} questions complete ({skipped_questions} skipped)",
                        flush=True,
                    )

            position_distribution = build_position_distribution_rows(
                question_row_cache,
                run_id=run_id,
                shard_id=f"{wave_source}__{wave_wave}",
                source=wave_source,
                source_family=wave_source,
                wave=wave_wave,
                canonical_wave=canonical_wave_label(wave_source, wave_wave),
            )

            finalize_source = _resolve_finalize_source(
                args.finalize_source,
                resume_requested=bool(args.resume),
                resume_skipped_questions=wave_resume_skipped_questions,
            )
            wave_tables, finalize_profile = _finalize_wave_checkpoint_tables(
                paths,
                finalize_source=finalize_source,
                wave_question_rows=wave_question_rows,
                wave_table_accumulators=wave_table_accumulators,
                wave_progress_started=progress_started,
            )
            wave_tables["position_distribution"] = position_distribution if not position_distribution.empty else pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)
            finalize_profile.update(
                {
                    "wave_index": wave_idx,
                    "wave_source": wave_source,
                    "wave": wave_wave,
                    "finalize_source_requested": args.finalize_source,
                    "finalize_source_effective": finalize_source,
                    "harmonization_call_count": int(harmonization_call_count_hot_path),
                    "harmonization_row_count": int(harmonization_row_count_hot_path),
                    "v550_harmonization_call_count_prepared": int(prepared_cache_stats["v550_harmonization_call_count_prepared"]),
                    "v550_harmonization_row_count_prepared": int(prepared_cache_stats["v550_harmonization_row_count_prepared"]),
                    "v550_harmonization_call_count_per_question": int(prepared_cache_stats["v550_harmonization_call_count_per_question"] + harmonization_call_count_hot_path),
                    "v550_harmonization_row_count_per_question": int(prepared_cache_stats["v550_harmonization_row_count_per_question"] + harmonization_row_count_hot_path),
                    "v550_harmonization_call_count_fallback": int(prepared_cache_stats["v550_harmonization_call_count_fallback"] + harmonization_call_count_fallback),
                    "v550_harmonization_row_count_fallback": int(prepared_cache_stats["v550_harmonization_row_count_fallback"] + harmonization_row_count_fallback),
                    "v550_prepared_substrate_mode": args.v550_prepared_substrate_mode,
                    "question_rows": int(len(wave_question_rows)),
                    "resume_skipped_questions": int(wave_resume_skipped_questions),
                    "wave_output_rows": int(sum(len(frame) for frame in wave_tables.values())),
                }
            )
            performance_wave_profiles.append(finalize_profile)
            replayed_cloud_tables = _load_replayed_cloud_tables(paths, progress_started)
            if replayed_cloud_tables is not None:
                replayed_attitude_cloud = replayed_cloud_tables
                wave_tables["question_response_attitude_cloud"] = replayed_attitude_cloud
                wave_tables["branch_co_signature"] = wave_tables["branch_relation_co_signature"].copy()
                _log_progress(
                    progress_started,
                    f"using replayed cloud outputs: question_response_attitude_cloud={len(replayed_attitude_cloud)} branch_co_signature=relation_alias",
                )
            branch_position_signature_status = "empty_no_position_features" if wave_tables["branch_position_signature"].empty else "enabled_diagnostic"
            branch_relation_cosignature_status = "disabled_no_contract_allowlist" if wave_tables["branch_relation_co_signature"].empty else "enabled_contract_gated"
            branch_co_signature_status = "compatibility_relation_only_alias_or_disabled" if wave_tables["branch_co_signature"].empty else "relation_only_compatibility_alias"
            question_response_attitude_cloud_status = "disabled_until_cross_question_engine" if wave_tables["question_response_attitude_cloud"].empty else "prototype_diagnostic"
            if wave_tables["branch_position_signature"].empty:
                wave_tables["branch_position_signature"] = pd.DataFrame(columns=BRANCH_POSITION_SIGNATURE_COLUMNS)
            if wave_tables["branch_relation_co_signature"].empty:
                wave_tables["branch_relation_co_signature"] = pd.DataFrame(columns=BRANCH_RELATION_CO_SIGNATURE_COLUMNS)
            if wave_tables["branch_co_signature"].empty:
                wave_tables["branch_co_signature"] = pd.DataFrame(columns=BRANCH_RELATION_CO_SIGNATURE_COLUMNS)
            if wave_tables["question_response_attitude_cloud"].empty:
                wave_tables["question_response_attitude_cloud"] = pd.DataFrame(columns=QUESTION_RESPONSE_ATTITUDE_CLOUD_COLUMNS)
            for table_name, frame in wave_tables.items():
                accumulators[table_name].append(frame)

            wave_warnings, wave_summary = _wave_warning_report(
                run_id=run_id,
                wave_index=wave_idx,
                wave_total=len(wave_scopes),
                wave_source=wave_source,
                wave_wave=wave_wave,
                wave_question_rows=wave_question_rows,
                wave_readiness_df=wave_readiness_df,
                wave_weight_df=wave_weight_df,
                wave_mapping_df=wave_mapping_coverage_df,
                wave_legacy_df=wave_legacy_df,
                wave_underpowered_df=wave_underpowered_df,
                wave_tables=wave_tables,
                response_review=response_review,
            )
            wave_report_dir = _wave_report_dir(paths, wave_source, wave_wave)
            _write_json_report(wave_report_dir / "warnings.json", wave_summary)
            wave_warning_summaries.append(wave_summary)
            for warning in wave_warnings:
                run_warnings.append(f"{warning['wave_source']} {warning['wave']}: {warning['code']} - {warning['message']}")

            if question_budget is not None:
                question_budget -= len(wave_question_rows)
                if question_budget <= 0 and wave_idx < len(wave_scopes):
                    budget_exhausted = True
            _log_progress(progress_started, f"wave {wave_idx}/{len(wave_scopes)} {wave_source} / {wave_wave}: completed")

        if args.dry_run:
            print(json.dumps({"scope_rows": len(scope_df), "waves": len(wave_scopes), "readiness_rows": sum(len(frame) for frame in accumulators["substrate_readiness"]), "question_rows": total_questions, "response_option_rows": len(response_map)}, indent=2))
            return 0

        q_universe = _concat_frames(accumulators["question_universe"])
        question_use_contract = _concat_frames(accumulators["question_use_contract"])
        position_distribution = _concat_frames(accumulators["position_distribution"])
        answer_distribution = _concat_frames(accumulators["answer_distribution"])
        country_answer_distribution = _concat_frames(accumulators["country_answer_distribution"])
        position_summary = _concat_frames(accumulators["position_indicator_summary"])
        indicator_matrix = _concat_frames(accumulators["indicator_answer_matrix"])
        outlier_summary = _concat_frames(accumulators["outlier_cohort_summary"])
        secondary_summary = _concat_frames(accumulators["secondary_indicator_summary"])
        recursive_nodes = _concat_frames(accumulators["recursive_branch_nodes"])
        branch_position_sig = _concat_frames(accumulators["branch_position_signature"])
        branch_relation_sig = _concat_frames(accumulators["branch_relation_co_signature"])
        branch_co_sig = _concat_frames(accumulators["branch_co_signature"])
        attitude_cloud = _concat_frames(accumulators["question_response_attitude_cloud"])
        mapping_gap = _concat_frames(accumulators["mapping_gap_report"])
        carry_forward_summary = _carry_forward_summary(question_use_contract, run_id=run_id)
        readiness_df = _concat_frames(accumulators["substrate_readiness"])
        pos_df = _concat_frames(accumulators["position_field_coverage"])
        weight_df = _concat_frames(accumulators["weight_coverage"])
        mapping_df = _concat_frames(accumulators["mapping_status_coverage"])
        legacy_df = _concat_frames(accumulators["legacy_leak_report"])
        underpowered_df = _concat_frames(accumulators["underpowered_quarantine"])
        all_questions_completed = (
            not budget_exhausted
            and empty_question_waves == 0
            and total_questions > 0
            and completed_questions + skipped_questions == total_questions
        )
        performance_profile = {
            "run_id": run_id,
            "stage": "determinicity_repository",
            "finalize_source_requested": args.finalize_source,
            "v550_prepared_substrate_mode": args.v550_prepared_substrate_mode,
            "finalize_source_effective_counts": {
                source: int(sum(1 for profile in performance_wave_profiles if profile.get("finalize_source_effective") == source))
                for source in FINALIZE_SOURCE_CHOICES
            },
            "harmonization_call_count": int(harmonization_call_count_hot_path),
            "harmonization_row_count": int(harmonization_row_count_hot_path),
            "v550_harmonization_call_count_prepared": int(sum(profile.get("v550_harmonization_call_count_prepared", 0) for profile in performance_wave_profiles)),
            "v550_harmonization_row_count_prepared": int(sum(profile.get("v550_harmonization_row_count_prepared", 0) for profile in performance_wave_profiles)),
            "v550_harmonization_call_count_per_question": int(sum(profile.get("v550_harmonization_call_count_per_question", 0) for profile in performance_wave_profiles)),
            "v550_harmonization_row_count_per_question": int(sum(profile.get("v550_harmonization_row_count_per_question", 0) for profile in performance_wave_profiles)),
            "v550_harmonization_call_count_fallback": int(sum(profile.get("v550_harmonization_call_count_fallback", 0) for profile in performance_wave_profiles)),
            "v550_harmonization_row_count_fallback": int(sum(profile.get("v550_harmonization_row_count_fallback", 0) for profile in performance_wave_profiles)),
            "resume_skipped_questions": int(resume_skipped_questions),
            "wave_finalize_profiles": performance_wave_profiles,
        }

        if secondary_summary.empty:
            secondary_summary = pd.DataFrame(columns=SECONDARY_INDICATOR_SUMMARY_COLUMNS)
        if recursive_nodes.empty:
            recursive_nodes = pd.DataFrame(columns=["run_id", "question_id", "node_id", "parent_node_id", "branch_depth", "split_indicator", "split_value", "node_entropy", "entropy_gain_from_parent", "stop_reason", "branch_type", "dominant_response", "dominant_response_pct"])
        if mapping_gap.empty:
            mapping_gap = pd.DataFrame(columns=["run_id", "gap_type", "response_value", "n_unweighted"])
        if question_use_contract.empty:
            question_use_contract = pd.DataFrame(columns=[
                "question_id",
                "var_code",
                "semantic_role",
                "v551_evidence_role",
                "gss2010_structural_overlay_used",
                "gss2010_structural_overlay_basis",
                "gss2010_structural_overlay_review_required",
                "allowed_as_response_distribution",
                "allowed_as_position_distribution",
                "allowed_as_context_distribution",
                "allowed_as_demographic_predictor",
                "allowed_as_branch_splitter",
                "allowed_as_branch_position_signature",
                "allowed_as_branch_relation_cosignature",
                "allowed_as_attitude_cloud_anchor",
                "allowed_as_attitude_cloud_feature",
                "allowed_as_v551_relation_evidence",
                "allowed_as_parent_prior_coordinate",
                "allowed_as_temporal_pressure_indicator",
                "allowed_as_runtime_persona_evidence",
                "question_type",
                "handling_rule",
                "mapping_status",
                "question_block_id",
                "structural_domain_id",
                "relation_axis_id",
                "target_entity_id",
                "driver_id",
                "driver_facet_id",
                "target_entity_rule",
                "final_driver_scope",
                "source_structure_classification",
                "source_structure_basis",
                "source_structure_confidence",
                "source_structure_source",
                "source_structure_fields_joined",
            ])
        if position_distribution.empty:
            position_distribution = pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)
        if attitude_cloud.empty:
            attitude_cloud = pd.DataFrame(columns=["run_id", "anchor_question_id", "cloud_feature", "cloud_value", "n_unweighted", "demographic_feature_excluded_flag"])
        if branch_position_sig.empty:
            branch_position_sig = pd.DataFrame(columns=[
                "run_id",
                "anchor_question_id",
                "feature_rank",
                "predictor_family",
                "feature_name",
                "feature_value",
                "association_score",
                "association_metric",
                "normalized_mutual_information",
                "cramers_v",
                "n_unweighted",
                "n_unique_feature_values",
                "n_unique_response_values",
                "target_dominant_response",
                "target_dominant_response_share",
                "feature_kind",
                "demographic_feature_excluded_flag",
            ])
        if branch_relation_sig.empty:
            branch_relation_sig = pd.DataFrame(columns=[
                "run_id",
                "anchor_question_id",
                "feature_rank",
                "predictor_family",
                "feature_name",
                "feature_value",
                "association_score",
                "association_metric",
                "normalized_mutual_information",
                "cramers_v",
                "n_unweighted",
                "n_unique_feature_values",
                "n_unique_response_values",
                "target_dominant_response",
                "target_dominant_response_share",
                "feature_kind",
                "demographic_feature_excluded_flag",
            ])
        if branch_co_sig.empty:
            branch_co_sig = pd.DataFrame(columns=[
                "run_id",
                "anchor_question_id",
                "feature_rank",
                "predictor_family",
                "feature_name",
                "feature_value",
                "association_score",
                "association_metric",
                "normalized_mutual_information",
                "cramers_v",
                "n_unweighted",
                "n_unique_feature_values",
                "n_unique_response_values",
                "target_dominant_response",
                "target_dominant_response_share",
                "feature_kind",
                "demographic_feature_excluded_flag",
            ])
        if "question_use_contract" in wave_tables and wave_tables["question_use_contract"].empty:
            wave_tables["question_use_contract"] = pd.DataFrame(columns=[
                "question_id",
                "var_code",
                "semantic_role",
                "v551_evidence_role",
                "allowed_as_response_distribution",
                "allowed_as_position_distribution",
                "allowed_as_context_distribution",
                "allowed_as_demographic_predictor",
                "allowed_as_branch_splitter",
                "allowed_as_branch_position_signature",
                "allowed_as_branch_relation_cosignature",
                "allowed_as_attitude_cloud_anchor",
                "allowed_as_attitude_cloud_feature",
                "allowed_as_v551_relation_evidence",
                "allowed_as_parent_prior_coordinate",
                "allowed_as_temporal_pressure_indicator",
                "allowed_as_runtime_persona_evidence",
                "question_type",
                "handling_rule",
                "mapping_status",
                "relation_axis_id",
                "target_entity_id",
                "driver_id",
                "final_driver_scope",
                "source_structure_classification",
                "source_structure_basis",
                "source_structure_confidence",
                "source_structure_source",
                "source_structure_fields_joined",
            ])
        if "position_distribution" in wave_tables and wave_tables["position_distribution"].empty:
            wave_tables["position_distribution"] = pd.DataFrame(columns=POSITION_DISTRIBUTION_COLUMNS)

        outputs = [
            ("question_universe", q_universe, "core"),
            ("question_use_contract", question_use_contract, "core"),
            ("position_distribution", position_distribution, "determinicity"),
            ("answer_distribution", answer_distribution, "distributions"),
            ("country_answer_distribution", country_answer_distribution, "distributions"),
            ("position_indicator_summary", position_summary, "determinicity"),
            ("indicator_answer_matrix", indicator_matrix, "determinicity"),
            ("outlier_cohort_summary", outlier_summary, "determinicity"),
            ("secondary_indicator_summary", secondary_summary, "determinicity"),
            ("recursive_branch_nodes", recursive_nodes, "determinicity"),
            ("branch_position_signature", branch_position_sig, "clouds"),
            ("branch_relation_co_signature", branch_relation_sig, "clouds"),
            ("branch_co_signature", branch_co_sig, "clouds"),
            ("question_response_attitude_cloud", attitude_cloud, "clouds"),
            ("mapping_gap_report", mapping_gap, "audit"),
            ("underpowered_quarantine", underpowered_df, "audit"),
            ("response_option_manual_review", response_review, "audit"),
            ("scope_manifest", scope_df, "core"),
            ("substrate_readiness", readiness_df, "core"),
            ("position_field_coverage", pos_df, "core"),
            ("weight_coverage", weight_df, "core"),
            ("mapping_status_coverage", mapping_df, "core"),
            ("question_carry_forward_summary", carry_forward_summary, "context"),
            ("legacy_leak_report", legacy_df, "audit"),
        ]

        written_tables: list[str] = []
        csv_written: list[str] = []
        row_counts: dict[str, int] = {}
        total_outputs = len(outputs)
        for output_idx, (table_name, frame, layer) in enumerate(outputs, start=1):
            if frame is None:
                continue
            if frame.empty and table_name not in {"response_option_manual_review", "mapping_gap_report", "underpowered_quarantine", "legacy_leak_report"}:
                # still write empty canonical outputs for schema completeness
                frame = frame.copy()
            _log_progress(progress_started, f"writing {output_idx}/{total_outputs} {layer}/{table_name}{_process_label(table_name)} ({len(frame)} rows)")
            meta = write_table(
                frame,
                paths=paths,
                table_name=table_name,
                layer=layer,
                write_csv=args.write_csv,
                write_parquet=args.write_parquet,
                report_name=f"V550_{table_name}.csv",
                reports_dir=Path(args.reports_dir),
                extra_schema={"description": f"V550 {table_name} output."},
            )
            written_tables.append(f"{layer}/{table_name}.parquet")
            csv_written.append(f"V550_{table_name}.csv")
            row_counts[table_name] = len(frame)

        _log_progress(progress_started, "writing manifest")
        manifest = build_manifest(
            run_id=run_id,
            version="v550b",
            stage="determinicity_repository",
            repo_root=ROOT,
            run_path=paths.run_path,
            input_db_used=True,
            source_filters=source_filters,
            wave_filters=wave_filters,
            country_filters=country_filters,
            thresholds={"min_cell_n": args.min_cell_n, "min_branch_n": args.min_branch_n, "min_answer_n": args.min_answer_n, "max_depth": args.max_depth},
            script_versions={"build_determinicity_repository_v550.py": "v1"},
            input_row_counts={"scope_rows": len(scope_df), "question_rows": len(question_rows), "response_option_rows": len(response_map)},
            output_row_counts=row_counts,
            readiness_class_counts=readiness_df["readiness_status"].value_counts().to_dict(),
            warnings=[
                *run_warnings,
                "Country is excluded as a within-country predictor.",
                "Attitude clouds exclude demographic variables.",
                "Rows below thresholds are quarantined rather than dropped.",
                "Question-level checkpoint Parquet files are written under the run directory so the job can be resumed with --resume.",
                "Question coverage must be complete for the manifest to be marked successful.",
            ],
            errors=[],
            files_written=written_tables,
            csv_mirrors_written=csv_written,
            postgres_tables_written=[],
            postgres_views_written=[],
            success=all_questions_completed,
        )
        manifest["branch_position_signature_status"] = branch_position_signature_status
        manifest["branch_relation_cosignature_status"] = branch_relation_cosignature_status
        manifest["branch_co_signature_status"] = branch_co_signature_status
        manifest["question_response_attitude_cloud_status"] = question_response_attitude_cloud_status
        write_manifest(paths, manifest)
        _write_json_report(paths.run_path / "performance_profile.json", performance_profile)
        _log_progress(progress_started, "writing wave warnings summary")
        _write_json_report(paths.run_path / "wave_warnings.json", {"run_id": run_id, "waves": wave_warning_summaries})
        _log_progress(progress_started, "promoting latest run")
        if all_questions_completed:
            paths.promote_latest()
        if args.verbose:
            _log_progress(progress_started, "final manifest ready")
            print(json.dumps(manifest, indent=2, ensure_ascii=False))
        return 0 if all_questions_completed else 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
