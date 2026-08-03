#!/usr/bin/env python3
"""Build question_response_attitude_cloud_summary from live survey microdata.

This is the runtime implementation for V549b. It anchors attitude clouds to
question responses, answer-presence/absence, and recursive branch nodes, then
scores the attitudinal / opinion items that travel with those anchors in the
same respondent universe.
"""

from __future__ import annotations

import json
import os
import argparse
import time
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import psycopg2
import pyarrow as pa
import pyarrow.parquet as pq
import yaml
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
DDM_ROOT = ROOT / "data" / "ddm_build_copy"
OUT_PARQUET = DDM_ROOT / "parquet" / "question_response_attitude_cloud_summary.parquet"
OUT_ANCHOR_PARQUET = DDM_ROOT / "parquet" / "attitude_cloud_anchor.parquet"
OUT_REVIEW = ROOT / "rawlsing_v5_locked_build_pack_v1" / "04_REVIEW_AND_CI"
CHECKPOINT_DIR = DDM_ROOT / "checkpoints" / "question_response_attitude_cloud_summary_v549b"
ANCHOR_REPORT = OUT_REVIEW / "V549b_anchor_response_cloud_report.yaml"
EXCLUSION_REPORT = OUT_REVIEW / "V549b_cloud_feature_exclusion_report.yaml"
DUCKDB_PATH = DDM_ROOT / "rawlsing_ddm_fact_store.duckdb"
QUESTION_MASTER = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"
STRUCTURE_REGISTER = DDM_ROOT / "manifests" / "question_structure_register.csv"
QUESTION_RELATION_REGISTRY = DDM_ROOT / "bindings" / "question_relation_registry.csv"
QUESTION_DETERMINICITY = DDM_ROOT / "reports" / "V547_question_determinicity_summary.csv"
RECURSIVE_TREES = DDM_ROOT / "reports" / "V548_recursive_breakage_tree_nodes.csv"

RESPONDENTS_TABLE = "survey_microdata_respondents"
RESPONSES_TABLE = "survey_microdata_responses"

MIN_ANCHOR_N = 50
TOP_N_CANDIDATES = 10
TOP_N_ANSWER_CODES = 2
MIN_CANDIDATE_VALID_N = 50
MIN_BRANCH_N = 25
PROGRESS_INTERVAL_SECONDS = 15.0
PROGRESS_ITEM_STEP = 50

POSITION_COLS = [
    "country_code",
    "sex",
    "age_group",
    "education_level",
    "income_level",
    "urban_rural",
    "religion_label",
]


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "<na>", "none"}:
        return ""
    return text


def normalize_family(name: str) -> str:
    value = clean(name)
    if value == "Latinobarometro":
        return "Latinobarómetro"
    return value


def slugify(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", str(value)).strip("_") or "slice"


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing; the live microdata tables are not reachable.")
    return psycopg2.connect(db_url)


def normalize_code(value: Any) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        fval = float(value)
    except Exception:
        text = str(value).strip()
        return text if text else None
    if pd.isna(fval):
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


def safe_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        f = float(value)
    except Exception:
        return default
    return default if pd.isna(f) else f


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def load_master() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_MASTER)
    return df


def load_structure_register() -> pd.DataFrame:
    df = pd.read_csv(STRUCTURE_REGISTER)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    if "source_family" in df.columns:
        df["source_family"] = df["source_family"].map(normalize_family)
    return df


def load_relation_registry() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_RELATION_REGISTRY)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    if "source_family" in df.columns:
        df["source_family"] = df["source_family"].map(normalize_family)
    return df


def load_v547() -> pd.DataFrame:
    df = pd.read_csv(QUESTION_DETERMINICITY)
    return df


def load_v548() -> pd.DataFrame:
    df = pd.read_csv(RECURSIVE_TREES)
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build question-response attitude clouds from live survey microdata."
    )
    parser.add_argument(
        "--source",
        default=None,
        help="Optional source-family filter, e.g. WVS or Afrobarometer.",
    )
    parser.add_argument(
        "--wave",
        default=None,
        help="Optional wave filter, e.g. W1 or W7.",
    )
    parser.add_argument(
        "--country",
        default=None,
        help="Optional country-code filter, e.g. US or ZW.",
    )
    return parser.parse_args()


def load_respondents(conn) -> pd.DataFrame:
    query = f"""
        SELECT id AS respondent_id,
               source,
               country_code,
               survey_year,
               sex,
               age,
               education_level,
               income_level,
               religion_label,
               urban_rural
        FROM {RESPONDENTS_TABLE}
        ORDER BY id
    """
    df = pd.read_sql_query(query, conn)
    df["country_code"] = df["country_code"].fillna("").astype(str).str.strip()
    df["sex"] = df["sex"].fillna("").astype(str).str.strip()
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["education_level"] = pd.to_numeric(df["education_level"], errors="coerce")
    df["income_level"] = pd.to_numeric(df["income_level"], errors="coerce")
    df["religion_label"] = df["religion_label"].fillna("").astype(str).str.strip()
    df["urban_rural"] = df["urban_rural"].fillna("").astype(str).str.strip()
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 29, 44, 59, 200],
        labels=["18-29", "30-44", "45-59", "60+"],
        include_lowest=True,
        right=True,
    ).astype(str).replace("nan", "")
    return df


def load_wide_responses(conn, source: str, variables: list[str]) -> pd.DataFrame:
    variables = sorted({v for v in variables if v})
    if not variables:
        return pd.DataFrame()
    placeholders = ",".join(["%s"] * len(variables))
    query = f"""
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
    df = pd.read_sql_query(query, conn, params=(source, *variables))
    if df.empty:
        return pd.DataFrame()
    df["value"] = df["value_raw"].map(normalize_code)
    df = df.dropna(subset=["value"])
    wide = df.pivot_table(index="respondent_id", columns="var_code", values="value", aggfunc="first")
    return wide


def crosstab_cramers_v(anchor_mask: pd.Series, item_values: pd.Series) -> tuple[float, int]:
    joined = pd.DataFrame({"anchor": anchor_mask.astype(bool), "value": item_values}).dropna()
    if len(joined) < MIN_CANDIDATE_VALID_N:
        return float("nan"), int(len(joined))
    ct = pd.crosstab(joined["anchor"].astype(int), joined["value"].astype(str))
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
    denom = max(1, min(observed.shape[0] - 1, observed.shape[1] - 1))
    return float(np.sqrt(phi2 / denom)), int(len(joined))


def infer_effect_direction(anchor_values: pd.Series, all_values: pd.Series) -> str:
    anchor_values = anchor_values.dropna().astype(str)
    all_values = all_values.dropna().astype(str)
    if anchor_values.empty or all_values.empty:
        return "mixed"
    anchor_mode = anchor_values.mode().iloc[0]
    anchor_share = float((anchor_values == anchor_mode).mean())
    overall_share = float((all_values == anchor_mode).mean())
    if anchor_mode in {"present", "absent"}:
        return anchor_mode if anchor_share >= overall_share else f"depleted_{anchor_mode}"
    return f"branch_enriched_{anchor_mode}" if anchor_share >= overall_share else f"branch_depleted_{anchor_mode}"


def confidence(anchor_n: int, valid_n: int, score: float) -> float:
    sample = min(anchor_n / 300.0, 1.0)
    support = min(valid_n / 2000.0, 1.0)
    signal = min(max(score, 0.0) / 0.25, 1.0) if np.isfinite(score) else 0.0
    return round(min(0.99, 0.22 + 0.34 * sample + 0.24 * support + 0.20 * signal), 3)


class ProgressReporter:
    def __init__(self, interval_seconds: float = PROGRESS_INTERVAL_SECONDS) -> None:
        self.interval_seconds = interval_seconds
        self.started = time.monotonic()
        self.last_emit = self.started

    def emit(self, message: str) -> None:
        elapsed = time.monotonic() - self.started
        print(f"[V549b +{elapsed:0.0f}s] {message}", flush=True)
        self.last_emit = time.monotonic()

    def maybe_emit(self, message: str, force: bool = False) -> None:
        now = time.monotonic()
        if force or (now - self.last_emit) >= self.interval_seconds:
            self.emit(message)


def choose_country(value: str) -> str:
    value = clean(value)
    return value if value else "ALL"


def build_branch_masks_for_question(question_var: str, v548: pd.DataFrame, respondents: pd.DataFrame, wide: pd.DataFrame) -> dict[str, pd.Series]:
    node_map: dict[str, dict[str, Any]] = {}
    for row in v548.itertuples(index=False):
        node_map[str(row.node_id)] = {
            "parent": clean(getattr(row, "parent_node_id", "")) or None,
            "branch_type": clean(getattr(row, "branch_type", "")),
            "conditions": json.loads(clean(getattr(row, "conditions_json", "{}")) or "{}"),
        }

    cache: dict[str, pd.Series] = {}

    def build(node_id: str) -> pd.Series:
        if node_id in cache:
            return cache[node_id]
        node = node_map[node_id]
        if not node["parent"]:
            if question_var not in wide.columns:
                mask = pd.Series([False] * len(respondents), index=respondents.index)
            else:
                mask = wide[question_var].notna()
            cache[node_id] = mask
            return mask
        parent_id = node["parent"]
        if parent_id not in node_map:
            mask = pd.Series([False] * len(respondents), index=respondents.index)
            cache[node_id] = mask
            return mask
        parent_mask = build(parent_id)
        parent = node_map[parent_id]
        predictor = clean(parent["conditions"].get("predictor"))
        indicator = clean(parent["conditions"].get("indicator_value"))
        majority_answer = clean(parent["conditions"].get("majority_answer"))
        if predictor not in respondents.columns:
            mask = pd.Series([False] * len(respondents), index=respondents.index)
            cache[node_id] = mask
            return mask
        pos = respondents[predictor].astype(str)
        target = wide[question_var].astype(str) if question_var in wide.columns else pd.Series([""] * len(respondents), index=respondents.index)
        if node["branch_type"] == "majority_position_conformity":
            mask = parent_mask & (pos == indicator) & (target.astype(str) == majority_answer)
        elif node["branch_type"] == "majority_position_deviation":
            mask = parent_mask & (pos == indicator) & (target.astype(str) != majority_answer)
        elif node["branch_type"] == "minority_position_convergence":
            mask = parent_mask & (pos != indicator) & (target.astype(str) == majority_answer)
        elif node["branch_type"] == "minority_position_divergence":
            mask = parent_mask & (pos != indicator) & (target.astype(str) != majority_answer)
        else:
            mask = parent_mask
        cache[node_id] = mask
        return mask

    for node_id in node_map:
        cache[node_id] = build(node_id)
    return cache


def get_candidate_registry(structure: pd.DataFrame, relation_registry: pd.DataFrame, source: str, wave: str) -> pd.DataFrame:
    reg = relation_registry.copy()
    reg = reg[(reg["source_family"].astype(str) == source) & (reg["wave"].astype(str) == wave)].copy()
    if reg.empty:
        return reg
    struct = structure.copy()
    struct = struct[struct["source_family"].astype(str) == source]
    struct = struct[struct["canonical_wave"].astype(str) == wave]
    struct = struct[struct["question_type"].isin(["single_choice", "multi_select", "matrix", "split_block"])]
    keep_cols = [
        "source_family",
        "canonical_wave",
        "question_name",
        "question_id",
        "question_type",
        "access_pattern",
        "access_expression",
        "final_driver_id",
        "final_driver_label",
        "final_driver_scope",
        "semantic_scope",
    ]
    struct = struct[keep_cols].drop_duplicates(subset=["question_id"])
    reg["var_name"] = reg["item_id"].astype(str).str.split(":").str[-1]
    merged = reg.merge(struct, left_on=["source_family", "wave", "var_name"], right_on=["source_family", "canonical_wave", "question_name"], how="inner", suffixes=("", "_struct"))
    merged = merged[merged["surface_export_allowed"].astype(str).str.lower().isin(["yes", "true", "1"])]
    merged = merged[merged["relation_channels"].astype(str).str.contains("attitude_cloud", na=False)]
    merged = merged[merged["final_driver_scope"].astype(str) != "metadata"]
    return merged


def top_answer_codes(series: pd.Series, limit: int = TOP_N_ANSWER_CODES) -> list[str]:
    counts = Counter(series.dropna().astype(str))
    out = []
    for value, count in counts.most_common():
        if value in {"", "nan", "None"}:
            continue
        out.append(value)
        if len(out) >= limit:
            break
    return out


def build_single_answer_anchors(
    source: str,
    wave: str,
    country: str,
    respondents: pd.DataFrame,
    source_wide: pd.DataFrame,
    candidate_items: pd.DataFrame,
    reporter: ProgressReporter | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    anchors: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    if source_wide.empty:
        return anchors, rows, exclusions

    anchor_candidates = candidate_items[candidate_items["question_type"].isin(["single_choice", "multi_select", "matrix", "split_block"])]
    q_values = anchor_candidates["item_id"].astype(str).unique()
    for q_index, q in enumerate(q_values, start=1):
        var_name = q.split(":", 2)[-1]
        if var_name not in source_wide.columns:
            continue
        series = source_wide[var_name].dropna()
        if series.empty:
            continue
        answer_codes = top_answer_codes(series, TOP_N_ANSWER_CODES)
        for answer_code in answer_codes:
            anchor_id = f"{source}:{wave}:{country}:{var_name}={answer_code}"
            anchor_mask = source_wide[var_name].astype(str) == answer_code
            anchor_n = int(anchor_mask.sum())
            if anchor_n < MIN_ANCHOR_N:
                exclusions.append(
                    {
                        "anchor_id": anchor_id,
                        "reason": "anchor_n_below_threshold",
                        "anchor_n": anchor_n,
                        "source_family": source,
                        "wave": wave,
                        "country": country,
                    }
                )
                continue
            universe_id = f"{source}:{wave}:{country}:{var_name}"
            anchors.append(
                {
                    "anchor_id": anchor_id,
                    "anchor_type": "single_answer",
                    "source_family": source,
                    "wave": wave,
                    "country": country,
                    "item_id": q,
                    "driver_id": clean(candidate_items.loc[candidate_items["item_id"] == q, "final_driver_id"].iloc[0]) if not candidate_items.loc[candidate_items["item_id"] == q].empty else "",
                    "answer_code": answer_code,
                    "branch_id": "",
                    "condition_json": json.dumps({"var_name": var_name, "answer_code": answer_code}),
                    "allowed_for_profile_posterior": True,
                    "allowed_for_strata_tension": True,
                    "confidence": round(min(0.99, 0.45 + min(anchor_n / 500.0, 0.3)), 3),
                }
            )

            for cand_index, (_, cand) in enumerate(candidate_items.iterrows(), start=1):
                if reporter is not None and cand_index % PROGRESS_ITEM_STEP == 0:
                    reporter.maybe_emit(
                        f"single_answer on {source}/{wave}/{country} anchor={var_name} "
                        f"candidate={cand_item_id} cand_index={cand_index}/{len(candidate_items)} "
                        f"rows={len(rows)} exclusions={len(exclusions)}"
                    )
                cand_item_id = clean(cand["item_id"])
                cand_var = cand_item_id.split(":", 2)[-1]
                if cand_item_id == q or cand_var not in source_wide.columns:
                    continue
                if clean(cand["question_type"]) in {"stem", "derived_or_reference"}:
                    exclusions.append(
                        {
                            "anchor_id": anchor_id,
                            "candidate_item_id": cand_item_id,
                            "reason": "non_attitude_candidate",
                            "candidate_driver_id": clean(cand.get("final_driver_id")),
                        }
                    )
                    continue
                candidate_values = source_wide[cand_var]
                valid_n = int(pd.DataFrame({"a": anchor_mask, "b": candidate_values}).dropna().shape[0])
                if valid_n < MIN_CANDIDATE_VALID_N:
                    continue
                score, _ = crosstab_cramers_v(anchor_mask, candidate_values)
                if not np.isfinite(score):
                    continue
                anchor_vals = candidate_values[anchor_mask]
                direction = infer_effect_direction(anchor_vals, candidate_values)
                rows.append(
                    {
                        "source_family": source,
                        "wave": wave,
                        "country": country,
                        "anchor_id": anchor_id,
                        "anchor_type": "single_answer",
                        "anchor_item_id": q,
                        "anchor_driver_id": clean(candidate_items.loc[candidate_items["item_id"] == q, "final_driver_id"].iloc[0]) if not candidate_items.loc[candidate_items["item_id"] == q].empty else "",
                        "anchor_answer_code": answer_code,
                        "anchor_condition_json": json.dumps({"var_name": var_name, "answer_code": answer_code}),
                        "respondent_universe_id": universe_id,
                        "candidate_item_id": cand_item_id,
                        "candidate_driver_id": clean(cand.get("final_driver_id")),
                        "candidate_answer_code": "",
                        "candidate_relation_channel": "attitude_cloud",
                        "association_metric": "cramers_v",
                        "association_score": round(float(score), 6),
                        "effect_direction": direction,
                        "anchor_n": anchor_n,
                        "candidate_valid_n": valid_n,
                        "weighted_anchor_n": float(anchor_n),
                        "weighted_candidate_valid_n": float(valid_n),
                        "confidence": confidence(anchor_n, valid_n, float(score)),
                        "support_depth": "single_answer",
                        "warnings_json": json.dumps([]),
                    }
                )
        if reporter is not None:
            reporter.maybe_emit(
                f"single_answer on {source}/{wave}/{country} question={q} "
                f"question_index={q_index}/{len(q_values)} anchors={len(anchors)} rows={len(rows)} exclusions={len(exclusions)}",
                force=True,
            )
    return anchors, rows, exclusions


def build_answer_presence_anchors(
    source: str,
    wave: str,
    country: str,
    respondents: pd.DataFrame,
    source_wide: pd.DataFrame,
    candidate_items: pd.DataFrame,
    reporter: ProgressReporter | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    anchors: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    if source_wide.empty:
        return anchors, rows, exclusions

    binary_items = candidate_items[candidate_items["question_type"].isin(["multi_select", "split_block"])].copy()
    for cand_index, (_, cand) in enumerate(binary_items.iterrows(), start=1):
        if reporter is not None and cand_index % PROGRESS_ITEM_STEP == 0:
            reporter.maybe_emit(
                f"presence on {source}/{wave}/{country} anchor={item_id} answer_code={answer_code} "
                f"cand={cand_index}/{len(binary_items)} rows={len(rows)} exclusions={len(exclusions)}"
            )
        item_id = clean(cand["item_id"])
        var_name = item_id.split(":", 2)[-1]
        if var_name not in source_wide.columns:
            continue
        series = source_wide[var_name]
        if series.dropna().empty:
            continue
        uniq = set(series.dropna().astype(str).unique().tolist())
        if not uniq.intersection({"0", "1", "present", "absent"}):
            continue
        for answer_code, anchor_type in [("1", "answer_presence"), ("0", "answer_absence")]:
            anchor_mask = series.astype(str) == answer_code
            anchor_n = int(anchor_mask.sum())
            if anchor_n < MIN_ANCHOR_N:
                continue
            anchor_id = f"{source}:{wave}:{country}:{var_name}#{anchor_type}:{answer_code}"
            anchors.append(
                {
                    "anchor_id": anchor_id,
                    "anchor_type": anchor_type,
                    "source_family": source,
                    "wave": wave,
                    "country": country,
                    "item_id": item_id,
                    "driver_id": clean(cand.get("final_driver_id")),
                    "answer_code": answer_code,
                    "branch_id": "",
                    "condition_json": json.dumps({"var_name": var_name, "answer_code": answer_code, "anchor_type": anchor_type}),
                    "allowed_for_profile_posterior": True,
                    "allowed_for_strata_tension": True,
                    "confidence": round(min(0.99, 0.42 + min(anchor_n / 600.0, 0.3)), 3),
                }
            )
            universe_id = f"{source}:{wave}:{country}:{var_name}:{anchor_type}"
            for other_index, (_, other) in enumerate(candidate_items.iterrows(), start=1):
                if reporter is not None and other_index % PROGRESS_ITEM_STEP == 0:
                    reporter.maybe_emit(
                        f"presence on {source}/{wave}/{country} anchor={var_name}:{answer_type} "
                        f"candidate={cand_item_id} other_index={other_index}/{len(candidate_items)} "
                        f"rows={len(rows)} exclusions={len(exclusions)}"
                    )
                cand_item_id = clean(other["item_id"])
                cand_var = cand_item_id.split(":", 2)[-1]
                if cand_item_id == item_id or cand_var not in source_wide.columns:
                    continue
                if clean(other["question_type"]) in {"stem", "derived_or_reference"}:
                    exclusions.append(
                        {
                            "anchor_id": anchor_id,
                            "candidate_item_id": cand_item_id,
                            "reason": "non_attitude_candidate",
                            "candidate_driver_id": clean(other.get("final_driver_id")),
                        }
                    )
                    continue
                candidate_values = source_wide[cand_var]
                valid_n = int(pd.DataFrame({"a": anchor_mask, "b": candidate_values}).dropna().shape[0])
                if valid_n < MIN_CANDIDATE_VALID_N:
                    continue
                score, _ = crosstab_cramers_v(anchor_mask, candidate_values)
                if not np.isfinite(score):
                    continue
                direction = infer_effect_direction(candidate_values[anchor_mask], candidate_values)
                rows.append(
                    {
                        "source_family": source,
                        "wave": wave,
                        "country": country,
                        "anchor_id": anchor_id,
                        "anchor_type": anchor_type,
                        "anchor_item_id": item_id,
                        "anchor_driver_id": clean(cand.get("final_driver_id")),
                        "anchor_answer_code": answer_code,
                        "anchor_condition_json": json.dumps({"var_name": var_name, "answer_code": answer_code, "anchor_type": anchor_type}),
                        "respondent_universe_id": universe_id,
                        "candidate_item_id": cand_item_id,
                        "candidate_driver_id": clean(other.get("final_driver_id")),
                        "candidate_answer_code": "",
                        "candidate_relation_channel": "attitude_cloud",
                        "association_metric": "cramers_v",
                        "association_score": round(float(score), 6),
                        "effect_direction": direction,
                        "anchor_n": anchor_n,
                        "candidate_valid_n": valid_n,
                        "weighted_anchor_n": float(anchor_n),
                        "weighted_candidate_valid_n": float(valid_n),
                        "confidence": confidence(anchor_n, valid_n, float(score)),
                        "support_depth": "answer_presence",
                        "warnings_json": json.dumps([]),
                    }
                )
    return anchors, rows, exclusions


def build_branch_node_anchors(
    source: str,
    wave: str,
    respondents: pd.DataFrame,
    source_wide: pd.DataFrame,
    candidate_items: pd.DataFrame,
    v548: pd.DataFrame,
    reporter: ProgressReporter | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    anchors: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    if source_wide.empty or v548.empty:
        return anchors, rows, exclusions

    tree_groups = list(v548.groupby("tree_id", sort=True))
    for question_index, (question_id, tree_df) in enumerate(tree_groups, start=1):
        q_var = clean(question_id).split(":", 2)[-1]
        if q_var not in source_wide.columns:
            continue
        masks = build_branch_masks_for_question(q_var, tree_df, respondents, source_wide)
        for row in tree_df.itertuples(index=False):
            branch_id = clean(row.node_id)
            if branch_id not in masks:
                continue
            mask = masks[branch_id]
            branch_n = int(mask.sum())
            if branch_n < MIN_BRANCH_N:
                continue
            country = choose_country(respondents.loc[mask, "country_code"].mode().iloc[0] if mask.any() and not respondents.loc[mask, "country_code"].dropna().empty else "ALL")
            anchor_id = f"{source}:{wave}:{country}:{branch_id}"
            anchors.append(
                {
                    "anchor_id": anchor_id,
                    "anchor_type": "branch_node",
                    "source_family": source,
                    "wave": wave,
                    "country": country,
                    "item_id": question_id,
                    "driver_id": "",
                    "answer_code": "",
                    "branch_id": branch_id,
                    "condition_json": clean(getattr(row, "conditions_json", "")),
                    "allowed_for_profile_posterior": True,
                    "allowed_for_strata_tension": True,
                    "confidence": round(min(0.99, 0.35 + min(branch_n / 500.0, 0.4)), 3),
                }
            )
            universe_id = f"{source}:{wave}:{country}:{branch_id}"
            for cand_index, (_, cand) in enumerate(candidate_items.iterrows(), start=1):
                if reporter is not None and cand_index % PROGRESS_ITEM_STEP == 0:
                    reporter.maybe_emit(
                        f"branch on {source}/{wave}/{country} question={question_id} "
                        f"branch={branch_id} candidate={cand_item_id} cand_index={cand_index}/{len(candidate_items)} "
                        f"rows={len(rows)} exclusions={len(exclusions)}"
                    )
                cand_item_id = clean(cand["item_id"])
                cand_var = clean(cand.get("var_name")) or cand_item_id.split(":", 2)[-1]
                if cand_var not in source_wide.columns or cand_item_id == question_id:
                    continue
                if clean(cand["question_type"]) in {"stem", "derived_or_reference"}:
                    exclusions.append(
                        {
                            "anchor_id": anchor_id,
                            "candidate_item_id": cand_item_id,
                            "reason": "non_attitude_candidate",
                            "candidate_driver_id": clean(cand.get("final_driver_id")),
                        }
                    )
                    continue
                candidate_values = source_wide[cand_var]
                valid_n = int(pd.DataFrame({"a": mask, "b": candidate_values}).dropna().shape[0])
                if valid_n < MIN_CANDIDATE_VALID_N:
                    continue
                score, _ = crosstab_cramers_v(mask, candidate_values)
                if not np.isfinite(score):
                    continue
                direction = infer_effect_direction(candidate_values[mask], candidate_values)
                rows.append(
                    {
                        "source_family": source,
                        "wave": wave,
                        "country": country,
                        "anchor_id": anchor_id,
                        "anchor_type": "branch_node",
                        "anchor_item_id": question_id,
                        "anchor_driver_id": "",
                        "anchor_answer_code": "",
                        "anchor_condition_json": clean(getattr(row, "conditions_json", "")),
                        "respondent_universe_id": universe_id,
                        "candidate_item_id": cand_item_id,
                        "candidate_driver_id": clean(cand.get("final_driver_id")),
                        "candidate_answer_code": "",
                        "candidate_relation_channel": "attitude_cloud",
                        "association_metric": "cramers_v",
                        "association_score": round(float(score), 6),
                        "effect_direction": direction,
                        "anchor_n": branch_n,
                        "candidate_valid_n": valid_n,
                        "weighted_anchor_n": float(branch_n),
                        "weighted_candidate_valid_n": float(valid_n),
                        "confidence": confidence(branch_n, valid_n, float(score)),
                        "support_depth": "branch_node",
                        "warnings_json": json.dumps([]),
                    }
                )
    return anchors, rows, exclusions


def dedupe_and_rank(df: pd.DataFrame, top_n: int = TOP_N_CANDIDATES) -> pd.DataFrame:
    if df.empty:
        return df
    sort_cols = ["anchor_id", "association_score", "confidence", "candidate_valid_n", "candidate_item_id"]
    ascending = [True, False, False, False, True]
    df = df.sort_values(sort_cols, ascending=ascending).reset_index(drop=True)
    df = df.groupby("anchor_id", as_index=False, group_keys=False).head(top_n)
    return df.reset_index(drop=True)


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table = pa.Table.from_pandas(df, preserve_index=False)
    pq.write_table(table, path)


def write_duckdb(df: pd.DataFrame, table_name: str) -> None:
    try:
        import duckdb  # type: ignore
    except Exception:
        return
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        conn.register("tmp_df", df)
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM tmp_df")
    finally:
        conn.close()


def write_slice_checkpoint(
    source: str,
    wave: str,
    country: str,
    rows_df: pd.DataFrame,
    anchors_df: pd.DataFrame,
    exclusions_df: pd.DataFrame,
) -> tuple[Path, Path, Path]:
    slice_dir = CHECKPOINT_DIR / f"{slugify(source)}__{slugify(wave)}__{slugify(country)}"
    slice_dir.mkdir(parents=True, exist_ok=True)
    rows_path = slice_dir / "question_response_attitude_cloud_summary.parquet"
    anchors_path = slice_dir / "attitude_cloud_anchor.parquet"
    exclusions_path = slice_dir / "cloud_feature_exclusion_report.csv"
    write_parquet(rows_df, rows_path)
    write_parquet(anchors_df, anchors_path)
    exclusions_df.to_csv(exclusions_path, index=False)
    (slice_dir / "slice_report.yaml").write_text(
        yaml.safe_dump(
            {
                "source_family": source,
                "wave": wave,
                "country": country,
                "rows": int(len(rows_df)),
                "anchors": int(len(anchors_df)),
                "exclusions": int(len(exclusions_df)),
                "rows_file": str(rows_path),
                "anchors_file": str(anchors_path),
                "exclusions_file": str(exclusions_path),
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return rows_path, anchors_path, exclusions_path


def combine_slice_parquets(paths: list[Path]) -> pd.DataFrame:
    if not paths:
        return pd.DataFrame()
    frames = [pd.read_parquet(path) for path in paths if path.exists()]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def main() -> int:
    load_env()
    args = parse_args()
    structure = load_structure_register()
    relation_registry = load_relation_registry()
    v547 = load_v547()
    v548 = load_v548()
    conn = connect_db()
    respondents = load_respondents(conn)
    reporter = ProgressReporter()
    reporter.emit(
        f"loaded base tables structure_rows={len(structure)} relation_rows={len(relation_registry)} "
        f"v547_rows={len(v547)} v548_rows={len(v548)} respondent_rows={len(respondents)}"
    )

    anchors_all: list[dict[str, Any]] = []
    rows_all: list[dict[str, Any]] = []
    exclusions_all: list[dict[str, Any]] = []
    rows_checkpoint_paths: list[Path] = []
    anchors_checkpoint_paths: list[Path] = []
    exclusions_checkpoint_paths: list[Path] = []

    try:
        source_wave_pairs = (
            relation_registry[["source_family", "wave"]]
            .dropna()
            .drop_duplicates()
            .assign(source_family=lambda d: d["source_family"].map(normalize_family))
        )
        source_wave_pairs = source_wave_pairs[source_wave_pairs["source_family"].isin(structure["source_family"].dropna().astype(str).unique().tolist())]
        if args.source:
            source_wave_pairs = source_wave_pairs[source_wave_pairs["source_family"].astype(str) == normalize_family(args.source)]
        if args.wave:
            source_wave_pairs = source_wave_pairs[source_wave_pairs["wave"].astype(str) == str(args.wave)]
        source_list = sorted(source_wave_pairs["source_family"].dropna().astype(str).unique().tolist())
        total_sources = len(source_list)
        reporter.emit(
            f"starting scan sources={total_sources} source_filter={args.source or 'ALL'} "
            f"wave_filter={args.wave or 'ALL'} country_filter={args.country or 'ALL'}"
        )
        for source_index, source in enumerate(source_list, start=1):
            source_waves = sorted(source_wave_pairs.loc[source_wave_pairs["source_family"].astype(str) == source, "wave"].astype(str).unique().tolist())
            reporter.emit(f"source {source_index}/{total_sources}: {source} waves={source_waves}")
            for wave_index, wave in enumerate(source_waves, start=1):
                source_resp = respondents[respondents["source"].astype(str).map(normalize_family) == source].copy()
                if source_resp.empty:
                    continue
                reporter.emit(
                    f"preparing slice {source}/{wave}: source_resp={len(source_resp)} "
                    f"countries={source_resp['country_code'].nunique(dropna=True)}"
                )
                candidate_items = get_candidate_registry(structure, relation_registry, source, wave)
                if candidate_items.empty:
                    reporter.emit(f"skip slice {source}/{wave}: no candidate items after registry filter")
                    continue
                reporter.emit(
                    f"slice {source}/{wave}: candidate_items={len(candidate_items)} "
                    f"unique_items={candidate_items['item_id'].nunique()}"
                )
                source_wide_items = [clean(i).split(":", 2)[-1] for i in candidate_items["item_id"].astype(str).tolist()]
                reporter.emit(f"loading wide responses for {source}/{wave}: variables={len(source_wide_items)}")
                source_wide = load_wide_responses(conn, source, source_wide_items)
                if source_wide.empty:
                    reporter.emit(f"skip slice {source}/{wave}: no wide responses returned")
                    continue
                reporter.emit(f"loaded wide responses for {source}/{wave}: rows={len(source_wide)} cols={len(source_wide.columns)}")
                country_groups = source_resp["country_code"].fillna("").astype(str).replace("", "ALL").unique().tolist()
                country_list = sorted(country_groups)
                for country_index, country in enumerate(country_list, start=1):
                    if args.country and str(country) != str(args.country):
                        continue
                    if country == "ALL":
                        resp = source_resp.copy()
                    else:
                        resp = source_resp[source_resp["country_code"].astype(str) == country].copy()
                    if resp.empty:
                        continue
                    reporter.emit(
                        f"slice {source_index}/{total_sources} {source}/{wave} country={country} "
                        f"{country_index}/{len(country_list)} respondents={len(resp)} candidate_items={len(candidate_items)}"
                    )
                    resp_idx = resp["respondent_id"].tolist()
                    wide = source_wide.loc[source_wide.index.intersection(resp_idx)].copy()
                    if wide.empty:
                        reporter.emit(f"skip slice {source}/{wave}/{country}: no overlapping wide rows")
                        continue
                    resp = resp.set_index("respondent_id", drop=False).loc[wide.index].copy()
                    reporter.emit(
                        f"building anchors for {source}/{wave}/{country}: "
                        f"wide_rows={len(wide)} branch_tree_rows={len(v548[v548['tree_id'].astype(str).str.startswith(f'{source}:') | v548['tree_id'].astype(str).str.startswith(source)])}"
                    )

                    a1, r1, e1 = build_single_answer_anchors(source, wave, country, resp, wide, candidate_items, reporter=reporter)
                    a2, r2, e2 = build_answer_presence_anchors(source, wave, country, resp, wide, candidate_items, reporter=reporter)
                    a3, r3, e3 = build_branch_node_anchors(
                        source=source,
                        wave=wave,
                        respondents=resp,
                        source_wide=wide,
                        candidate_items=candidate_items,
                        v548=v548[v548["tree_id"].astype(str).str.startswith(f"{source}:") | v548["tree_id"].astype(str).str.startswith(source)],
                        reporter=reporter,
                    )

                    anchors_all.extend(a1 + a2 + a3)
                    rows_all.extend(r1 + r2 + r3)
                    exclusions_all.extend(e1 + e2 + e3)
                    slice_rows_df = pd.DataFrame(r1 + r2 + r3)
                    slice_anchors_df = pd.DataFrame(a1 + a2 + a3).drop_duplicates(subset=["anchor_id"])
                    slice_exclusions_df = pd.DataFrame(e1 + e2 + e3)
                    if not slice_rows_df.empty:
                        rows_path, anchors_path, exclusions_path = write_slice_checkpoint(
                            source, wave, country, slice_rows_df, slice_anchors_df, slice_exclusions_df
                        )
                        rows_checkpoint_paths.append(rows_path)
                        anchors_checkpoint_paths.append(anchors_path)
                        exclusions_checkpoint_paths.append(exclusions_path)
                    reporter.maybe_emit(
                        f"done slice {source}/{wave}/{country}: anchors={len(anchors_all)} rows={len(rows_all)} exclusions={len(exclusions_all)}",
                        force=True,
                    )
    finally:
        conn.close()

    if not rows_all:
        raise RuntimeError("V549b produced no attitude-cloud rows.")

    anchors_df = combine_slice_parquets(anchors_checkpoint_paths)
    rows_df = combine_slice_parquets(rows_checkpoint_paths)
    rows_df = dedupe_and_rank(rows_df, TOP_N_CANDIDATES)
    exclusions_df = pd.concat([pd.read_csv(p) for p in exclusions_checkpoint_paths if p.exists()], ignore_index=True) if exclusions_checkpoint_paths else pd.DataFrame()
    reporter.emit(
        f"postprocess rows={len(rows_df)} anchors={len(anchors_df)} exclusions={len(exclusions_df)}"
    )

    # Ensure schema-compatible columns are present.
    for col in [
        "source_family",
        "wave",
        "country",
        "anchor_id",
        "anchor_type",
        "anchor_item_id",
        "anchor_driver_id",
        "anchor_answer_code",
        "anchor_condition_json",
        "respondent_universe_id",
        "candidate_item_id",
        "candidate_driver_id",
        "candidate_answer_code",
        "candidate_relation_channel",
        "association_metric",
        "association_score",
        "effect_direction",
        "anchor_n",
        "candidate_valid_n",
        "weighted_anchor_n",
        "weighted_candidate_valid_n",
        "confidence",
        "support_depth",
        "warnings_json",
    ]:
        if col not in rows_df.columns:
            rows_df[col] = ""

    rows_df = rows_df[
        [
            "source_family",
            "wave",
            "country",
            "anchor_id",
            "anchor_type",
            "anchor_item_id",
            "anchor_driver_id",
            "anchor_answer_code",
            "anchor_condition_json",
            "respondent_universe_id",
            "candidate_item_id",
            "candidate_driver_id",
            "candidate_answer_code",
            "candidate_relation_channel",
            "association_metric",
            "association_score",
            "effect_direction",
            "anchor_n",
            "candidate_valid_n",
            "weighted_anchor_n",
            "weighted_candidate_valid_n",
            "confidence",
            "support_depth",
            "warnings_json",
        ]
    ].copy()

    write_parquet(rows_df, OUT_PARQUET)
    write_parquet(anchors_df, OUT_ANCHOR_PARQUET)
    write_duckdb(rows_df, "question_response_attitude_cloud_summary")
    write_duckdb(anchors_df, "attitude_cloud_anchor")

    feature_exclusions = {
        "status": "green_v549b_attitude_cloud_written",
        "attitude_cloud_rows": int(len(rows_df)),
        "anchor_rows": int(len(anchors_df)),
        "source_families": sorted(rows_df["source_family"].dropna().astype(str).unique().tolist()),
        "waves": sorted(rows_df["wave"].dropna().astype(str).unique().tolist()),
        "anchor_types": rows_df["anchor_type"].value_counts().to_dict(),
        "excluded_rows": int(len(exclusions_df)),
        "excluded_reasons": exclusions_df["reason"].value_counts().to_dict() if not exclusions_df.empty else {},
        "notes": [
            "V549b is built as a same-source, same-wave, country-scoped practical proxy.",
            "Candidate features exclude structural stems and metadata-like rows.",
            "Cloud rows are ranked per anchor and capped to the strongest candidates.",
        ],
        "output_file": str(OUT_PARQUET),
        "anchor_output_file": str(OUT_ANCHOR_PARQUET),
        "duckdb_file": str(DUCKDB_PATH),
    }

    anchor_report = {
        "status": "green_v549b_anchor_cloud_report_written",
        "anchor_rows": int(len(anchors_df)),
        "attitude_cloud_rows": int(len(rows_df)),
        "source_families": sorted(anchors_df["source_family"].dropna().astype(str).unique().tolist()) if not anchors_df.empty else [],
        "waves": sorted(anchors_df["wave"].dropna().astype(str).unique().tolist()) if not anchors_df.empty else [],
        "country_scope_summary": anchors_df["country"].value_counts().to_dict() if not anchors_df.empty else {},
        "allowed_for_profile_posterior_count": int(anchors_df["allowed_for_profile_posterior"].astype(str).str.lower().isin(["true", "1", "yes"]).sum()) if not anchors_df.empty else 0,
        "allowed_for_strata_tension_count": int(anchors_df["allowed_for_strata_tension"].astype(str).str.lower().isin(["true", "1", "yes"]).sum()) if not anchors_df.empty else 0,
        "output_file": str(OUT_ANCHOR_PARQUET),
        "summary_file": str(OUT_PARQUET),
    }

    OUT_REVIEW.mkdir(parents=True, exist_ok=True)
    reporter.emit("writing parquet and review reports")
    ANCHOR_REPORT.write_text(yaml.safe_dump(anchor_report, sort_keys=False), encoding="utf-8")
    EXCLUSION_REPORT.write_text(yaml.safe_dump(feature_exclusions, sort_keys=False), encoding="utf-8")
    reporter.emit(f"finished anchors={len(anchors_df)} rows={len(rows_df)} exclusions={len(exclusions_df)}")

    print(f"V549b wrote {len(rows_df)} attitude-cloud rows to {OUT_PARQUET}")
    print(f"V549b wrote {len(anchors_df)} anchors to {OUT_ANCHOR_PARQUET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
