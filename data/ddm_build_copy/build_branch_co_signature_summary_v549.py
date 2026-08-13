#!/usr/bin/env python3
"""Build branch_co_signature_summary from live survey_microdata tables.

This V549 builder treats branch membership from V548 recursive trees as the
anchor and asks which other attitudinal/opinion items travel with that branch
inside the same respondent universe. It also materializes a practical
question_relation_registry proxy from the semantic question master so V549b has
an explicit registry to consume.
"""

from __future__ import annotations

import json
import os
import re
import time
import argparse
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import psycopg2
import yaml
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
PACK_ROOT = ROOT / "rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED"
OUT_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
OUT_BINDINGS_DIR = ROOT / "data" / "ddm_build_copy" / "bindings"
OUT_DUCKDB = ROOT / "data" / "ddm_build_copy" / "rawlsing_ddm_fact_store.duckdb"
CHECKPOINT_DIR = OUT_DIR / "checkpoints" / "branch_co_signature_summary_v549"
QUESTIONS_MASTER = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
STRUCTURE_REGISTER = ROOT / "data" / "ddm_build_copy" / "manifests" / "question_structure_register.csv"
V547_CSV = OUT_DIR / "V547_question_determinicity_summary.csv"
V548_CSV = OUT_DIR / "V548_recursive_breakage_tree_nodes.csv"

BRANCH_OUT_CSV = OUT_DIR / "V549_branch_co_signature_summary.csv"
BRANCH_OUT_YAML = OUT_DIR / "V549_branch_co_signature_summary.yaml"
BRANCH_REVIEW_YAML = PACK_ROOT / "08_REVIEW" / "V549_branch_co_signature_summary_report.yaml"
REGISTRY_OUT_CSV = OUT_BINDINGS_DIR / "question_relation_registry.csv"
REGISTRY_OUT_YAML = OUT_BINDINGS_DIR / "question_relation_registry.yaml"

RESPONDENTS_TABLE = "survey_microdata_respondents"
RESPONSES_TABLE = "survey_microdata_responses"
FACET_READY_VIEW = "v_ddm_response_long_facet_ready"

MIN_BRANCH_N = 25
TOP_N_PER_BRANCH = 8
PROGRESS_INTERVAL_SECONDS = 15.0
PROGRESS_ITEM_STEP = 50


@dataclass
class BranchNode:
    row: pd.Series
    parent: str | None
    branch_type: str
    conditions: dict[str, Any]


class ProgressReporter:
    def __init__(self, interval_seconds: float = PROGRESS_INTERVAL_SECONDS) -> None:
        self.interval_seconds = interval_seconds
        self.started = time.monotonic()
        self.last_emit = self.started

    def emit(self, message: str) -> None:
        elapsed = time.monotonic() - self.started
        print(f"[V549 +{elapsed:0.0f}s] {message}", flush=True)
        self.last_emit = time.monotonic()

    def maybe_emit(self, message: str, force: bool = False) -> None:
        now = time.monotonic()
        if force or (now - self.last_emit) >= self.interval_seconds:
            self.emit(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build branch co-signatures from live survey microdata.")
    parser.add_argument("--source", default=None, help="Optional source-family filter, e.g. WVS or Afrobarometer.")
    parser.add_argument("--wave", default=None, help="Optional wave filter, e.g. W1 or W7.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append or replace the filtered slice in the existing output instead of rewriting the whole file.",
    )
    return parser.parse_args()


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing; the live microdata tables are not reachable.")
    return psycopg2.connect(db_url)


def facet_ready_view_exists(conn) -> bool:
    cur = conn.cursor()
    cur.execute("SELECT to_regclass(%s)", (f"public.{FACET_READY_VIEW}",))
    exists = cur.fetchone()[0] is not None
    cur.close()
    return bool(exists)


def infer_question_family(final_driver_id: str, scope: str) -> str:
    d = (final_driver_id or "").lower()
    scope = (scope or "").lower()
    if "metadata::" in d or scope == "metadata":
        return "metadata"
    if "religious" in d:
        return "religious_authority"
    if "trust" in d:
        return "institutional_trust"
    if "authority" in d or "democracy" in d or "regime" in d or "military" in d:
        return "authority_deference"
    if "family" in d or "collectiv" in d or "parent" in d or "child" in d or "obedi" in d:
        return "family_hierarchy"
    if "outgroup" in d or "foreign" in d or "immigrant" in d or "nationality" in d or "ethnic" in d:
        return "outgroup_tolerance"
    if "discrimin" in d or "gender" in d or "harass" in d:
        return "gender_authority"
    if "wasta" in d or "bribe" in d or "corrupt" in d:
        return "wasta_corruption"
    if "civic" in d or "speech" in d or "protest" in d or "vote" in d:
        return "civic_agency"
    if "economic" in d or "income" in d or "mobility" in d or "work" in d or "poverty" in d or "inequality" in d:
        return "economic_mobility"
    if "security" in d or "conflict" in d or "war" in d or "disaster" in d or "crime" in d:
        return "neighborhood_security"
    return "civic_agency"


def infer_response_mode(display_text: str, response_options: str | float | None, option_count: int) -> str:
    text = f"{display_text or ''} {response_options or ''}".lower()
    if "select all" in text or "check all" in text or "multiple response" in text:
        return "multi_select"
    if option_count and option_count > 1:
        return "single_choice"
    return "unknown"


def safe_int(value: Any, default: int = 0) -> int:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return default
    try:
        return int(value)
    except Exception:
        try:
            return int(float(value))
        except Exception:
            return default


def normalize_code(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return None
    try:
        fval = float(value)
    except Exception:
        text = str(value).strip()
        return text if text else None
    if np.isnan(fval):
        return None
    if abs(fval - round(fval)) < 1e-9:
        return str(int(round(fval)))
    return f"{fval:.6f}".rstrip("0").rstrip(".")


def normalize_series(series: pd.Series) -> pd.Series:
    out = series.copy()
    out = out.replace({None: np.nan, "": np.nan, "nan": np.nan, "<NA>": np.nan})
    out = pd.to_numeric(out, errors="ignore")
    if pd.api.types.is_numeric_dtype(out):
        out = out.where(~out.isin([-1, -2, 8, 9, 98, 99, 101, 999]), np.nan)
        out = out.apply(normalize_code)
    else:
        out = out.apply(lambda x: normalize_code(x))
    return out.astype("object")


def safe_json(obj: Any) -> Any:
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if obj is pd.NA:
        return None
    return str(obj)


def load_question_master() -> pd.DataFrame:
    if STRUCTURE_REGISTER.exists():
        df = pd.read_csv(STRUCTURE_REGISTER)
        for col in df.columns:
            if df[col].dtype == "O":
                df[col] = df[col].fillna("").astype(str)
        required = {"source_family", "canonical_wave", "question_name", "question_type", "final_driver_id", "final_driver_label"}
        missing = required - set(df.columns)
        if missing:
            raise RuntimeError(f"question_structure_register.csv missing columns: {sorted(missing)}")
        if QUESTIONS_MASTER.exists():
            master = pd.read_csv(QUESTIONS_MASTER, low_memory=False)
            for col in master.columns:
                if master[col].dtype == "O":
                    master[col] = master[col].fillna("").astype(str)
            master_required = {"source", "wave", "var_name", "final_driver_id", "final_driver_label"}
            missing_master = master_required - set(master.columns)
            if missing_master:
                raise RuntimeError(f"questions_master_drivers.csv missing columns: {sorted(missing_master)}")
            master = master.rename(columns={"source": "source_family", "wave": "canonical_wave", "var_name": "question_name"})
            merge_keys = ["source_family", "canonical_wave", "question_name"]
            merge_cols = [
                "source_family",
                "canonical_wave",
                "question_name",
                "final_driver_id",
                "final_driver_scope",
                "final_driver_label",
                "final_driver_origin",
                "semantic_scope",
                "semantic_primary_driver",
                "semantic_secondary_driver",
                "semantic_shared_driver",
                "semantic_regional_driver",
                "semantic_notes",
            ]
            merge_cols = [col for col in merge_cols if col in master.columns and col in df.columns and col not in merge_keys]
            if merge_cols:
                overlay = master[merge_keys + merge_cols].drop_duplicates(
                    subset=merge_keys
                )
                df = df.merge(
                    overlay,
                    on=merge_keys,
                    how="left",
                    suffixes=("", "_master"),
                )
                for col in merge_cols:
                    master_col = f"{col}_master"
                    if master_col in df.columns:
                        df[col] = df[master_col].where(df[master_col].astype(str).str.len() > 0, df[col])
                        df.drop(columns=[master_col], inplace=True)
        return df

    if not QUESTIONS_MASTER.exists():
        raise FileNotFoundError(QUESTIONS_MASTER)
    df = pd.read_csv(QUESTIONS_MASTER)
    required = {"source", "wave", "var_name", "display_text", "option_count", "response_options", "semantic_scope", "final_driver_id", "final_driver_label"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"questions_master_drivers.csv missing columns: {sorted(missing)}")
    return df


def build_question_relation_registry(master: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in master.itertuples(index=False):
        scope = str(getattr(row, "semantic_scope", "") or getattr(row, "scope", "") or "")
        final_driver_id = str(getattr(row, "final_driver_id", "") or "")
        if scope == "metadata" or final_driver_id.startswith("metadata::"):
            continue
        source = str(getattr(row, "source_family", "") or getattr(row, "source", "") or "")
        wave = str(getattr(row, "canonical_wave", "") or getattr(row, "wave", "") or "")
        var_name = str(
            getattr(row, "matched_source_column", "")
            or getattr(row, "matched_codebook_var", "")
            or getattr(row, "question_name", "")
            or getattr(row, "var_name", "")
            or ""
        )
        display_text = str(getattr(row, "question_text", "") or getattr(row, "display_text", "") or "")
        response_options = getattr(row, "response_options", None) or getattr(row, "question_text", None)
        option_count = safe_int(getattr(row, "response_option_count", 0) or getattr(row, "option_count", 0), 0)
        question_family = infer_question_family(final_driver_id, scope)
        target_layers = "attitude_cloud"
        authority_target_if_any = final_driver_id if any(k in question_family for k in ["authority", "religious", "family"]) else ""
        question_type = str(getattr(row, "question_type", "") or "")
        response_mode = question_type if question_type in {"single_choice", "multi_select", "matrix", "split_block", "open_text", "stem", "derived_or_reference"} else infer_response_mode(display_text, response_options, option_count)
        relation_channels = "attitude_cloud,branch_co_signature"
        answer_option_ontology_ref = str(
            getattr(row, "semantic_content_id", "")
            or getattr(row, "exact_content_id", "")
            or getattr(row, "access_expression", "")
            or ""
        )
        polarity = "mixed"
        surface_export_allowed = "yes"
        rows.append(
            {
                "source_family": source,
                "wave": wave,
                "item_id": f"{source}:{var_name}",
                "final_driver_id": final_driver_id,
                "question_family": question_family,
                "response_mode": response_mode,
                "target_layers": target_layers,
                "authority_target_if_any": authority_target_if_any,
                "relation_channels": relation_channels,
                "answer_option_ontology_ref": answer_option_ontology_ref,
                "polarity": polarity,
                "surface_export_allowed": surface_export_allowed,
            }
        )
    registry = pd.DataFrame(rows).drop_duplicates(subset=["source_family", "wave", "item_id", "final_driver_id"])
    return registry


def write_registry(registry: pd.DataFrame) -> None:
    OUT_BINDINGS_DIR.mkdir(parents=True, exist_ok=True)
    registry.to_csv(REGISTRY_OUT_CSV, index=False)
    payload = {
        "status": "green_question_relation_registry_proxy_written",
        "row_count": int(len(registry)),
        "sources": sorted(registry["source_family"].dropna().astype(str).unique().tolist()),
        "output_file": str(REGISTRY_OUT_CSV),
        "limitations": [
            "This registry is a practical proxy derived from the canonical semantic master.",
            "Response mode and question_family are heuristic but stable enough for branch-cloud extraction.",
        ],
    }
    REGISTRY_OUT_YAML.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(value)).strip("_") or "slice"


def write_slice_checkpoint(source: str, out: pd.DataFrame) -> Path:
    slice_dir = CHECKPOINT_DIR / slugify(source)
    slice_dir.mkdir(parents=True, exist_ok=True)
    out_path = slice_dir / "V549_branch_co_signature_summary.csv"
    out.to_csv(out_path, index=False)
    (slice_dir / "slice_report.yaml").write_text(
        yaml.safe_dump(
            {
                "source_family": source,
                "row_count": int(len(out)),
                "branch_count": int(out["branch_id"].nunique()) if not out.empty else 0,
                "output_file": str(out_path),
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return out_path


def append_csv_rows(path: Path, df: pd.DataFrame) -> None:
    if df.empty:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    header = not path.exists()
    df.to_csv(path, mode="a", index=False, header=header)


def reset_outputs() -> None:
    for path in [BRANCH_OUT_CSV, BRANCH_OUT_YAML, BRANCH_REVIEW_YAML]:
        if path.exists():
            path.unlink()
    if OUT_DUCKDB.exists():
        try:
            import duckdb  # type: ignore

            conn = duckdb.connect(str(OUT_DUCKDB))
            try:
                conn.execute("DROP TABLE IF EXISTS branch_co_signature_summary")
            finally:
                conn.close()
        except Exception:
            pass


def load_v547() -> pd.DataFrame:
    if not V547_CSV.exists():
        raise FileNotFoundError(V547_CSV)
    df = pd.read_csv(V547_CSV)
    return df


def load_v548() -> pd.DataFrame:
    if not V548_CSV.exists():
        raise FileNotFoundError(V548_CSV)
    df = pd.read_csv(V548_CSV)
    return df


def parse_conditions(value: str) -> dict[str, Any]:
    if not isinstance(value, str) or not value.strip():
        return {}
    try:
        return json.loads(value)
    except Exception:
        return {}


def crosstab_cramers_v(branch_mask: pd.Series, item_values: pd.Series) -> tuple[float, int]:
    joined = pd.DataFrame({"branch": branch_mask, "value": item_values}).dropna()
    if len(joined) < MIN_BRANCH_N:
        return float("nan"), int(len(joined))
    ct = pd.crosstab(joined["branch"].astype(int), joined["value"].astype(str))
    if ct.shape[0] < 2 or ct.shape[1] < 2:
        return float("nan"), int(len(joined))
    observed = ct.to_numpy(dtype=float)
    total = observed.sum()
    if total <= 0:
        return float("nan"), int(len(joined))
    row_sums = observed.sum(axis=1, keepdims=True)
    col_sums = observed.sum(axis=0, keepdims=True)
    expected = row_sums @ col_sums / total
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.nansum((observed - expected) ** 2 / np.where(expected == 0, np.nan, expected))
    phi2 = chi2 / total
    r, k = observed.shape
    denom = max(1, min(k - 1, r - 1))
    v = float(np.sqrt(phi2 / denom)) if denom > 0 else float("nan")
    return v, int(len(joined))


def infer_effect_direction(branch_values: pd.Series, all_values: pd.Series) -> str:
    branch_values = branch_values.dropna().astype(str)
    all_values = all_values.dropna().astype(str)
    if branch_values.empty or all_values.empty:
        return "unknown"
    branch_mode = branch_values.mode().iloc[0]
    branch_share = float((branch_values == branch_mode).mean())
    overall_share = float((all_values == branch_mode).mean())
    if branch_mode in {"present", "absent"}:
        return branch_mode if branch_share >= overall_share else f"depleted_{branch_mode}"
    return f"branch_enriched_{branch_mode}" if branch_share >= overall_share else f"branch_depleted_{branch_mode}"


def confidence(branch_n: int, valid_n: int, score: float) -> float:
    sample = min(branch_n / 500.0, 1.0)
    support = min(valid_n / 2000.0, 1.0)
    signal = min(max(score, 0.0) / 0.2, 1.0) if np.isfinite(score) else 0.0
    return round(min(0.99, 0.20 + 0.35 * sample + 0.25 * support + 0.20 * signal), 3)


def build_branch_mask(
    node_id: str,
    node_map: dict[str, BranchNode],
    anchor_target: pd.Series,
    position_df: pd.DataFrame,
    cache: dict[str, pd.Series],
) -> pd.Series:
    if node_id in cache:
        return cache[node_id]
    node = node_map[node_id]
    if not node.parent:
        mask = anchor_target.notna()
        cache[node_id] = mask
        return mask
    if node.parent not in node_map:
        mask = pd.Series([False] * len(position_df), index=position_df.index)
        cache[node_id] = mask
        return mask
    parent_mask = build_branch_mask(node.parent, node_map, anchor_target, position_df, cache)
    parent = node_map[node.parent]
    parent_cond = parent.conditions
    predictor = parent_cond.get("predictor")
    indicator = str(parent_cond.get("indicator_value", ""))
    majority_answer = str(parent_cond.get("majority_answer", ""))
    if predictor not in position_df.columns:
        mask = pd.Series([False] * len(position_df), index=position_df.index)
        cache[node_id] = mask
        return mask
    pos = position_df[predictor].astype(str)
    target = anchor_target.astype(str)
    branch_type = node.branch_type
    if branch_type == "majority_position_conformity":
        mask = parent_mask & (pos == indicator) & (target == majority_answer)
    elif branch_type == "majority_position_deviation":
        mask = parent_mask & (pos == indicator) & (target != majority_answer)
    elif branch_type == "minority_position_convergence":
        mask = parent_mask & (pos != indicator) & (target == majority_answer)
    elif branch_type == "minority_position_divergence":
        mask = parent_mask & (pos != indicator) & (target != majority_answer)
    else:
        mask = parent_mask
    cache[node_id] = mask
    return mask


def load_source_frame(conn, source: str, variables: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    var_list = sorted({v for v in variables if v})
    if not var_list:
        raise RuntimeError(f"no variables for source {source}")
    placeholders = ",".join(["%s"] * len(var_list))
    respondents_query = f"""
        SELECT id AS respondent_id,
               country_code,
               survey_year,
               wave,
               dataset_id,
               source_file,
               upload_date
        FROM {RESPONDENTS_TABLE}
        WHERE source = %s
        ORDER BY id
    """
    respondents = pd.read_sql_query(respondents_query, conn, params=(source,)).set_index("respondent_id")
    respondents["country_code"] = respondents["country_code"].fillna("").astype(str).str.strip()
    respondents["survey_year"] = pd.to_numeric(respondents["survey_year"], errors="coerce")
    respondents["wave"] = respondents["wave"].fillna("").astype(str).str.strip()
    respondents["dataset_id"] = respondents["dataset_id"].fillna("").astype(str).str.strip()
    respondents["source_file"] = respondents["source_file"].fillna("").astype(str).str.strip()
    respondents["upload_date"] = respondents["upload_date"].astype(str)
    respondents["sex"] = ""
    respondents["age"] = float("nan")
    respondents["education_level"] = float("nan")
    respondents["income_level"] = float("nan")
    respondents["religion_label"] = ""
    respondents["urban_rural"] = ""
    respondents["age_group"] = ""

    if facet_ready_view_exists(conn):
        responses_query = f"""
            SELECT respondent_id,
                   var_code,
                   value_raw
            FROM {FACET_READY_VIEW}
            WHERE source = %s
              AND var_code IN ({placeholders})
            ORDER BY respondent_id
        """
        responses = pd.read_sql_query(responses_query, conn, params=(source, *var_list)).dropna(subset=["var_code"])
    else:
        responses_query = f"""
            SELECT r.respondent_id,
                   r.var_code,
                   r.value_raw
            FROM {RESPONSES_TABLE} r
            JOIN {RESPONDENTS_TABLE} s
              ON s.id = r.respondent_id
            WHERE s.source = %s
              AND r.var_code IN ({placeholders})
            ORDER BY r.respondent_id
        """
        responses = pd.read_sql_query(responses_query, conn, params=(source, *var_list)).dropna(subset=["var_code"])
    if responses.empty:
        wide = pd.DataFrame(index=respondents.index)
    else:
        responses["value"] = responses["value_raw"].map(normalize_code)
        responses = responses.dropna(subset=["value"])
        wide = responses.pivot_table(index="respondent_id", columns="var_code", values="value", aggfunc="first")
    wide = wide.reindex(respondents.index)
    return respondents, wide


def summarize_branch(
    branch_id: str,
    branch_mask: pd.Series,
    anchor_question_id: str,
    source: str,
    canonical_wave: str,
    question_frame: pd.DataFrame,
    candidate_items: dict[str, str],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    branch_n = int(branch_mask.sum())
    if branch_n < MIN_BRANCH_N:
        return rows
    anchor_var = anchor_question_id.split(":", 1)[1]
    base_branch_values = question_frame[anchor_var][branch_mask].dropna().astype(str)
    base_all_values = question_frame[anchor_var].dropna().astype(str)
    for item_id, final_driver_id in candidate_items.items():
        if item_id == anchor_question_id:
            continue
        var_name = item_id.split(":", 1)[1]
        if var_name not in question_frame.columns:
            continue
        item_values = question_frame[var_name]
        valid_join = branch_mask & item_values.notna()
        valid_n = int(valid_join.sum())
        if valid_n < MIN_BRANCH_N:
            continue
        score, joined_n = crosstab_cramers_v(branch_mask, item_values)
        if not np.isfinite(score):
            continue
        branch_values = item_values[branch_mask]
        direction = infer_effect_direction(branch_values, item_values)
        rows.append(
            {
                "source_family": source,
                "canonical_wave": canonical_wave,
                "question_id": anchor_question_id,
                "branch_id": branch_id,
                "correlated_item_id": item_id,
                "correlated_driver_id": final_driver_id,
                "correlation_score": round(float(score), 6),
                "effect_direction": direction,
                "relation_channel": "attitude_cloud",
                "confidence": confidence(branch_n, joined_n, float(score)),
            }
        )
    rows.sort(key=lambda r: (-r["correlation_score"], r["correlated_item_id"]))
    return rows[:TOP_N_PER_BRANCH]


def write_duckdb(df: pd.DataFrame, append: bool = False) -> None:
    try:
        import duckdb  # type: ignore
    except Exception:
        return
    if df.empty:
        return
    OUT_DUCKDB.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(OUT_DUCKDB))
    try:
        conn.register("branch_df", df)
        if append:
            existing_tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}
            if "branch_co_signature_summary" in existing_tables:
                conn.execute("INSERT INTO branch_co_signature_summary SELECT * FROM branch_df")
            else:
                conn.execute("CREATE TABLE branch_co_signature_summary AS SELECT * FROM branch_df")
        else:
            conn.execute("CREATE OR REPLACE TABLE branch_co_signature_summary AS SELECT * FROM branch_df")
    finally:
        conn.close()


def main() -> int:
    load_env()
    args = parse_args()
    if not args.append:
        reset_outputs()
    master = load_question_master()
    registry = build_question_relation_registry(master)
    write_registry(registry)
    reporter = ProgressReporter()
    reporter.emit(
        f"loaded question master rows={len(master)} registry_rows={len(registry)} "
        f"sources={registry['source_family'].dropna().astype(str).nunique()}"
    )

    v547 = load_v547()
    v548 = load_v548()
    conn = connect_db()
    reporter.emit(f"loaded v547_rows={len(v547)} v548_rows={len(v548)}")

    source_summaries: list[dict[str, Any]] = []
    branch_ids: set[str] = set()
    total_rows = 0
    candidate_sources = sorted(set(v547["dataset_scope"].astype(str)))
    available_sources = sorted(set(v547["dataset_scope"].astype(str)))
    if args.source:
        candidate_sources = [s for s in candidate_sources if s == args.source]
    reporter.emit(f"starting branch scan sources={len(candidate_sources)}")
    if args.source and not candidate_sources:
        raise RuntimeError(
            f"V549 source filter {args.source!r} matched nothing. Available source families: {available_sources}"
        )

    try:
        for source_index, source in enumerate(candidate_sources, start=1):
            source_mask = v547["dataset_scope"].astype(str) == source
            if args.wave and "canonical_wave" in v547.columns:
                source_mask = source_mask & (v547["canonical_wave"].astype(str) == args.wave)
            source_qs = v547.loc[source_mask, "question_id"].astype(str).tolist()
            candidate_items = {
                row.question_id: row.final_driver_id
                for row in v547.itertuples(index=False)
                if str(row.dataset_scope) == source and (not args.wave or str(getattr(row, "canonical_wave", "")) == args.wave)
            }
            if not source_qs:
                continue
            reporter.emit(
                f"source {source_index}/{len(candidate_sources)} {source}: questions={len(source_qs)} candidate_items={len(candidate_items)}"
            )
            respondents, wide = load_source_frame(conn, source, [q.split(":", 1)[1] for q in source_qs])
            reporter.emit(f"source {source}: respondents={len(respondents)} wide_rows={len(wide)}")
            source_trees = v548.loc[v548["tree_id"].astype(str).isin(source_qs)].copy()
            tree_groups = list(source_trees.groupby("tree_id", sort=True))
            source_rows: list[dict[str, Any]] = []
            source_total_rows = 0
            for question_index, (question_id, tree_df) in enumerate(tree_groups, start=1):
                question_wave = ""
                if "canonical_wave" in v547.columns:
                    match = v547.loc[v547["question_id"].astype(str) == question_id, "canonical_wave"]
                    if not match.empty:
                        question_wave = str(match.iloc[0])
                tree_df = tree_df.copy()
                node_map: dict[str, BranchNode] = {}
                for trow in tree_df.itertuples(index=False):
                    conditions = parse_conditions(getattr(trow, "conditions_json", ""))
                    parent_raw = getattr(trow, "parent_node_id", "")
                    if pd.isna(parent_raw) or not str(parent_raw).strip() or str(parent_raw).lower() == "nan":
                        parent_id = None
                    else:
                        parent_id = str(parent_raw)
                    node_map[str(trow.node_id)] = BranchNode(
                        row=pd.Series(trow._asdict()),
                        parent=parent_id,
                        branch_type=str(getattr(trow, "branch_type", "")),
                        conditions=conditions,
                    )
                anchor_var = question_id.split(":", 1)[1]
                if anchor_var not in wide.columns:
                    continue
                anchor_target = wide[anchor_var]
                cache: dict[str, pd.Series] = {}
                root_id = f"{question_id}::root"
                question_rows: list[dict[str, Any]] = []
                reporter.emit(
                    f"question {question_index}/{len(tree_groups)} {question_id}: tree_nodes={len(tree_df)} anchor_var={anchor_var}"
                )
                for node_id, node in node_map.items():
                    if node.branch_type == "root":
                        continue
                    node_conditions = node.row.get("conditions_json")
                    node_data = parse_conditions(node_conditions if isinstance(node_conditions, str) else "")
                    if int(node.row.get("n", 0) or 0) < MIN_BRANCH_N:
                        continue
                    mask = build_branch_mask(node_id, node_map, anchor_target, respondents, cache)
                    if int(mask.sum()) < MIN_BRANCH_N:
                        continue
                    branch_id = node_id
                    if total_rows % PROGRESS_ITEM_STEP == 0:
                        reporter.maybe_emit(
                            f"branch scan on {source} question={question_id} branch={branch_id} rows={total_rows}"
                        )
                    branch_rows = summarize_branch(
                        branch_id=branch_id,
                        branch_mask=mask,
                        anchor_question_id=question_id,
                        source=source,
                        canonical_wave=question_wave,
                        question_frame=wide,
                        candidate_items=candidate_items,
                    )
                    question_rows.extend(branch_rows)
                    source_rows.extend(branch_rows)
                    source_total_rows += len(branch_rows)
                    total_rows += len(branch_rows)
                    branch_ids.add(branch_id)
                    append_csv_rows(BRANCH_OUT_CSV, pd.DataFrame(branch_rows))
                    if len(question_rows) >= PROGRESS_ITEM_STEP:
                        write_duckdb(pd.DataFrame(question_rows), append=True)
                        question_rows.clear()
                source_summaries.append(
                    {
                        "source": source,
                        "question_count": len(source_qs),
                        "tree_count": int(source_trees["tree_id"].nunique()),
                        "branch_rows": source_total_rows,
                    }
                )
                if question_rows:
                    write_duckdb(pd.DataFrame(question_rows), append=True)
                    question_rows.clear()
                    reporter.maybe_emit(
                    f"done question {question_index}/{len(tree_groups)} {question_id}: total_rows={total_rows}",
                    force=True,
                )
            if source_rows:
                checkpoint_path = write_slice_checkpoint(source, pd.DataFrame(source_rows))
                reporter.emit(f"checkpoint written for source {source}: {checkpoint_path}")
    finally:
        conn.close()

    if total_rows == 0:
        raise RuntimeError("V549 produced no branch co-signature rows.")

    payload = {
        "pack_id": "V549_BRANCH_CO_SIGNATURE_AND_COVARIANCE",
        "status": "green_branch_co_signature_summary_written",
        "row_count": int(total_rows),
        "branch_count": int(len(branch_ids)),
        "source_scopes": sorted(set(v547["dataset_scope"].astype(str))),
        "source_summaries": source_summaries,
        "output_file": str(BRANCH_OUT_CSV),
        "registry_file": str(REGISTRY_OUT_CSV),
        "duckdb_file": str(OUT_DUCKDB),
        "limitations": [
            "Only branches with n >= 25 are summarized.",
            "Co-signatures are computed against the same-source attitudinal question universe from V547.",
            "The question_relation_registry is a practical proxy derived from questions_master_drivers.csv.",
        ],
    }
    BRANCH_OUT_YAML.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    BRANCH_REVIEW_YAML.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    reporter.emit(f"finished on {total_rows} rows across {len(branch_ids)} branches")
    print(f"V549 wrote {total_rows} branch_co_signature_summary rows to {BRANCH_OUT_CSV}")
    print(f"Registry rows written to {REGISTRY_OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
