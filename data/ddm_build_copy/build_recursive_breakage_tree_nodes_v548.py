#!/usr/bin/env python3
"""Build recursive_breakage_tree_nodes from live survey_microdata tables.

This V548 builder uses the existing V547 question determinicity summary as the
root driver hint, then recursively expands majority-position deviation branches
from the live respondent/response tables. It preserves underpowered branches as
summaries instead of collapsing them away.
"""

from __future__ import annotations

import json
import argparse
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import psycopg2
import yaml
from dotenv import load_dotenv
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder


ROOT = Path(__file__).resolve().parents[2]
PACK_ROOT = ROOT / "rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED"
OUT_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
OUT_CSV = OUT_DIR / "V548_recursive_breakage_tree_nodes.csv"
OUT_YAML = OUT_DIR / "V548_recursive_breakage_tree_nodes.yaml"
REVIEW_YAML = PACK_ROOT / "08_REVIEW" / "V548_recursive_breakage_tree_nodes_report.yaml"
QUESTION_SUMMARY_CSV = OUT_DIR / "V547_question_determinicity_summary.csv"
DUCKDB_PATH = ROOT / "data" / "ddm_build_copy" / "rawlsing_ddm_fact_store.duckdb"

RESPONDENTS_TABLE = "survey_microdata_respondents"
RESPONSES_TABLE = "survey_microdata_responses"
FACET_READY_VIEW = "v_ddm_response_long_facet_ready"

POSITION_COLS = [
    "country_code",
    "sex",
    "age_group",
    "education_level",
    "income_level",
    "urban_rural",
    "religion_label",
]

MISSING_CODES = {-1, -2, 8, 9, 98, 99, 101, 999}
MIN_NODE_N_FOR_SPLIT = 50
MIN_OPTION_N_FOR_CHANNEL_INFERENCE = 10
MIN_NODE_N_REPORT_ONLY = 25
MAX_DEPTH = 5
PROGRESS_INTERVAL_SECONDS = 20.0
PROGRESS_QUESTION_STEP = 10


class ProgressReporter:
    def __init__(self, interval_seconds: float = PROGRESS_INTERVAL_SECONDS) -> None:
        self.interval_seconds = interval_seconds
        self.started = time.monotonic()
        self.last_emit = self.started

    def emit(self, message: str) -> None:
        elapsed = time.monotonic() - self.started
        print(f"[V548 +{elapsed:0.0f}s] {message}", flush=True)
        self.last_emit = time.monotonic()

    def maybe_emit(self, message: str, force: bool = False) -> None:
        now = time.monotonic()
        if force or (now - self.last_emit) >= self.interval_seconds:
            self.emit(message)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build recursive_breakage_tree_nodes from live survey_microdata tables.")
    parser.add_argument("--source", default=None, help="Optional source-family filter, e.g. WVS or Afrobarometer.")
    parser.add_argument("--wave", default=None, help="Optional wave filter, e.g. W1 or W7.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append or replace the filtered source in the existing output instead of rewriting the whole file.",
    )
    return parser.parse_args()


def discover_existing_path(candidates: list[Path]) -> Path:
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(str(candidates[0]))


def slugify(text: str) -> str:
    text = str(text).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "node"


def json_default(obj: Any) -> Any:
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if obj is pd.NA:
        return None
    return str(obj)


def family_from_dataset_scope(dataset_scope: str) -> str:
    return str(dataset_scope).strip()


def load_question_summary() -> pd.DataFrame:
    if not QUESTION_SUMMARY_CSV.exists():
        raise FileNotFoundError(QUESTION_SUMMARY_CSV)
    df = pd.read_csv(QUESTION_SUMMARY_CSV)
    required = {"dataset_scope", "question_id", "final_driver_id", "shape_class", "confidence"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"V547 summary missing columns: {sorted(missing)}")
    return df


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


def normalize_series_to_target(series: pd.Series) -> tuple[pd.Series, str]:
    cleaned = pd.to_numeric(series, errors="coerce")
    cleaned = cleaned.where(~cleaned.isin(list(MISSING_CODES)), np.nan)
    substantive = cleaned.dropna()
    if substantive.empty:
        return pd.Series([np.nan] * len(series), index=series.index), "empty"
    unique = {normalize_code(v) for v in substantive.unique()}
    unique.discard(None)
    presence_like = unique.issubset({"0", "1"}) and len(unique) <= 2
    if presence_like:
        target = cleaned.apply(lambda v: "present" if pd.notna(v) and float(v) != 0 else "absent")
        return target, "presence"
    target = cleaned.apply(normalize_code)
    return target, "single"


def sanitize_position_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["country_code"] = out["country_code"].fillna("").astype(str).str.strip()
    out["sex"] = out["sex"].fillna("").astype(str).str.strip()
    out["education_level"] = pd.to_numeric(out["education_level"], errors="coerce")
    out["income_level"] = pd.to_numeric(out["income_level"], errors="coerce")
    out["age"] = pd.to_numeric(out["age"], errors="coerce")
    out["religion_label"] = out["religion_label"].fillna("").astype(str).str.strip()
    out["urban_rural"] = out["urban_rural"].fillna("").astype(str).str.strip()
    out["age_group"] = pd.cut(
        out["age"],
        bins=[0, 29, 44, 59, 200],
        labels=["18-29", "30-44", "45-59", "60+"],
        include_lowest=True,
        right=True,
    )
    out["age_group"] = out["age_group"].astype(str).replace("nan", "")
    return out


def fetch_question_frame(conn, source: str, var_code: str) -> pd.DataFrame:
    if facet_ready_view_exists(conn):
        query = f"""
            SELECT respondent_id,
                   var_code,
                   value_raw,
                   country_code,
                   sex,
                   age,
                   education_level,
                   income_level,
                   religion_label,
                   urban_rural
            FROM {FACET_READY_VIEW}
            WHERE source = %s
              AND var_code = %s
              AND value_raw IS NOT NULL
            ORDER BY respondent_id
        """
        df = pd.read_sql_query(query, conn, params=(source, var_code))
    else:
        query = f"""
            SELECT r.respondent_id,
                   r.var_code,
                   r.value_raw,
                   s.country_code,
                   s.sex,
                   s.age,
                   s.education_level,
                   s.income_level,
                   s.religion_label,
                   s.urban_rural
            FROM {RESPONSES_TABLE} r
            JOIN {RESPONDENTS_TABLE} s ON s.id = r.respondent_id
            WHERE s.source = %s
              AND r.var_code = %s
              AND r.value_raw IS NOT NULL
            ORDER BY r.respondent_id
        """
        df = pd.read_sql_query(query, conn, params=(source, var_code))
    if df.empty:
        return df
    return sanitize_position_columns(df)


def to_label_frame(df: pd.DataFrame) -> pd.DataFrame:
    target, target_mode = normalize_series_to_target(df["value_raw"])
    out = df.copy()
    out["target"] = target
    out["target_mode"] = target_mode
    out = out.dropna(subset=["target"])
    return out


def distribution_json(target: pd.Series, weighted: bool = False) -> dict[str, Any]:
    counts = Counter(target.dropna().astype(str))
    total = sum(counts.values())
    values = []
    for value, count in counts.most_common():
        share = round(count / total, 6) if total else 0.0
        values.append({"value": value, "count": int(count), "share": share})
    return {"mode": "weighted" if weighted else "unweighted", "total": int(total), "values": values}


def mi_score(feature: pd.Series, target: pd.Series) -> float:
    joined = pd.DataFrame({"feature": feature, "target": target}).dropna()
    if len(joined) < MIN_NODE_N_FOR_SPLIT or joined["feature"].nunique() < 2 or joined["target"].nunique() < 2:
        return float("nan")
    X = LabelEncoder().fit_transform(joined["feature"].astype(str).values).reshape(-1, 1)
    y = LabelEncoder().fit_transform(joined["target"].astype(str).values)
    try:
        score = mutual_info_classif(X, y, discrete_features=True, random_state=0)[0]
    except Exception:
        return float("nan")
    return float(score)


def score_position_features(df: pd.DataFrame) -> list[tuple[str, float]]:
    scored: list[tuple[str, float]] = []
    for col in POSITION_COLS:
        if col not in df.columns:
            continue
        score = mi_score(df[col], df["target"])
        if np.isfinite(score):
            scored.append((col, float(score)))
    scored.sort(key=lambda item: (-item[1], item[0]))
    return scored


def choose_predictor(df: pd.DataFrame, summary_row: pd.Series | None, depth: int) -> tuple[str | None, float]:
    if depth == 0 and summary_row is not None:
        top_predictor = str(summary_row.get("top_predictor_1", "")).strip()
        if top_predictor in POSITION_COLS:
            score = mi_score(df[top_predictor], df["target"])
            if np.isfinite(score):
                return top_predictor, float(score)
    scored = score_position_features(df)
    if not scored:
        return None, float("nan")
    return scored[0]


def choose_indicator_value(df: pd.DataFrame, predictor: str, majority_answer: str) -> tuple[str | None, dict[str, Any]]:
    if predictor not in df.columns:
        return None, {}
    subset = df[[predictor, "target"]].dropna()
    if subset.empty:
        return None, {}
    overall_majority_share = (subset["target"] == majority_answer).mean()
    best: dict[str, Any] | None = None
    for value, group in subset.groupby(predictor, dropna=True):
        group = group.dropna(subset=["target"])
        n = int(len(group))
        if n < MIN_OPTION_N_FOR_CHANNEL_INFERENCE:
            continue
        majority_share = float((group["target"] == majority_answer).mean())
        lift = majority_share / overall_majority_share if overall_majority_share > 0 else float("inf")
        candidate = {
            "value": str(value),
            "n": n,
            "majority_share": majority_share,
            "lift": lift,
        }
        if best is None:
            best = candidate
            continue
        if (candidate["majority_share"], candidate["lift"], candidate["n"]) > (
            best["majority_share"],
            best["lift"],
            best["n"],
        ):
            best = candidate
    if best is None:
        return None, {}
    return best["value"], best


def confidence_for_node(n: int, majority_share: float, predictor_score: float, indicator_lift: float) -> float:
    if n <= 0:
        return 0.0
    sample_factor = min(n / 3000.0, 1.0)
    signal_factor = min(max(predictor_score, 0.0) / 0.05, 1.0)
    lift_factor = min(max(indicator_lift, 0.0) / 2.0, 1.0) if np.isfinite(indicator_lift) else 0.0
    majority_factor = min(max(majority_share, 0.0), 1.0)
    return round(min(0.99, 0.22 + 0.32 * sample_factor + 0.22 * signal_factor + 0.14 * lift_factor + 0.10 * majority_factor), 3)


def node_id_for(tree_id: str, path_parts: list[str]) -> str:
    if not path_parts:
        return f"{tree_id}::root"
    return f"{tree_id}::{'/'.join(path_parts)}"


def build_node_rows(
    df: pd.DataFrame,
    *,
    tree_id: str,
    question_id: str,
    final_driver_id: str,
    dataset_scope: str,
    canonical_wave: str,
    summary_row: pd.Series | None,
    depth: int,
    parent_node_id: str | None,
    branch_type: str,
    path_parts: list[str],
    removed_answers: list[str],
    rows: list[dict[str, Any]],
    allow_recursive: bool = True,
) -> None:
    node_id = node_id_for(tree_id, path_parts)
    distribution = distribution_json(df["target"])
    total_n = int(len(df))
    weighted_n = float(total_n)
    unique_targets = int(df["target"].nunique(dropna=True))
    majority_answer = None
    majority_count = 0
    majority_share = 0.0
    if total_n > 0 and unique_targets > 0:
        counts = df["target"].value_counts(dropna=True)
        majority_answer = str(counts.index[0])
        majority_count = int(counts.iloc[0])
        majority_share = float(majority_count / total_n)

    predictor, predictor_score = choose_predictor(df, summary_row, depth)
    indicator_value = None
    indicator_stats: dict[str, Any] = {}
    if predictor and majority_answer is not None:
        indicator_value, indicator_stats = choose_indicator_value(df, predictor, majority_answer)

    indicator_lift = float(indicator_stats.get("lift", float("nan"))) if indicator_stats else float("nan")
    can_expand = (
        total_n >= MIN_NODE_N_FOR_SPLIT
        and unique_targets >= 2
        and depth < MAX_DEPTH
        and predictor is not None
        and indicator_value is not None
        and np.isfinite(predictor_score)
    )

    expanded_here = allow_recursive and can_expand

    if total_n < MIN_NODE_N_REPORT_ONLY:
        stop_reason = "underpowered_report_only"
    elif unique_targets < 2:
        stop_reason = "single_target"
    elif predictor is None or not np.isfinite(predictor_score):
        stop_reason = "no_predictor_signal"
    elif indicator_value is None:
        stop_reason = "no_indicator_channel"
    elif depth >= MAX_DEPTH:
        stop_reason = "max_depth"
    elif expanded_here:
        stop_reason = "expanded"
    else:
        stop_reason = "branch_summary_only"

    confidence = confidence_for_node(total_n, majority_share, float(predictor_score) if np.isfinite(predictor_score) else 0.0, indicator_lift)
    next_best_indicator = f"{predictor}={indicator_value}" if predictor and indicator_value is not None else ""
    row = {
        "tree_id": tree_id,
        "node_id": node_id,
        "parent_node_id": parent_node_id or "",
        "depth": int(depth),
        "canonical_wave": canonical_wave,
        "conditions_json": json.dumps(
            {
                "question_id": question_id,
                "final_driver_id": final_driver_id,
                "dataset_scope": dataset_scope,
                "canonical_wave": canonical_wave,
                "branch_type": branch_type,
                "path_parts": path_parts,
                "removed_answers": removed_answers,
                "majority_answer": majority_answer,
                "majority_answer_count": majority_count,
                "majority_answer_share": round(majority_share, 6),
                "predictor": predictor,
                "predictor_score": round(float(predictor_score), 6) if np.isfinite(predictor_score) else None,
                "indicator_value": indicator_value,
                "indicator_value_n": int(indicator_stats.get("n", 0)) if indicator_stats else 0,
                "indicator_value_majority_share": round(float(indicator_stats.get("majority_share", 0.0)), 6)
                if indicator_stats
                else None,
                "indicator_value_lift": round(float(indicator_stats.get("lift", 0.0)), 6) if indicator_stats else None,
                "target_mode": "presence" if set(df["target"].dropna().unique()).issubset({"present", "absent"}) else "single",
                "can_expand": expanded_here,
            },
            sort_keys=True,
            default=json_default,
        ),
        "response_distribution_json": json.dumps(distribution, sort_keys=True, default=json_default),
        "next_best_indicator": next_best_indicator,
        "branch_type": branch_type,
        "n": total_n,
        "weighted_n": weighted_n,
        "stop_reason": stop_reason,
        "confidence": confidence,
    }
    rows.append(row)

    if not (allow_recursive and can_expand):
        return

    if predictor is None or indicator_value is None:
        return

    major_mask = df[predictor].astype(str) == str(indicator_value)
    majority_group = df[major_mask]
    minority_group = df[~major_mask]
    majority_answer_mask = df["target"].astype(str) == str(majority_answer)
    branches = [
        ("majority_position_conformity", df[major_mask & majority_answer_mask]),
        ("majority_position_deviation", df[major_mask & ~majority_answer_mask]),
        ("minority_position_convergence", df[~major_mask & majority_answer_mask]),
        ("minority_position_divergence", df[~major_mask & ~majority_answer_mask]),
    ]

    for branch_name, branch_df in branches:
        if branch_df.empty:
            continue
        child_path = path_parts + [slugify(branch_name)]
        if branch_name == "majority_position_deviation" and len(branch_df) >= MIN_NODE_N_FOR_SPLIT and depth + 1 < MAX_DEPTH:
            build_node_rows(
                branch_df,
                tree_id=tree_id,
                question_id=question_id,
                final_driver_id=final_driver_id,
                dataset_scope=dataset_scope,
                canonical_wave=canonical_wave,
                summary_row=summary_row,
                depth=depth + 1,
                parent_node_id=node_id,
                branch_type=branch_name,
                path_parts=child_path,
                removed_answers=removed_answers + ([str(majority_answer)] if majority_answer is not None else []),
                rows=rows,
                allow_recursive=True,
            )
            continue

        # Branch summaries are kept even when underpowered, but are not recursively expanded.
        build_node_rows(
            branch_df,
            tree_id=tree_id,
            question_id=question_id,
            final_driver_id=final_driver_id,
            dataset_scope=dataset_scope,
            canonical_wave=canonical_wave,
            summary_row=summary_row,
            depth=depth + 1,
            parent_node_id=node_id,
            branch_type=branch_name,
            path_parts=child_path,
            removed_answers=removed_answers + ([str(majority_answer)] if branch_name == "majority_position_deviation" and majority_answer is not None else []),
            rows=rows,
            allow_recursive=False,
        )


def build_tree_for_question(summary_row: pd.Series, conn) -> list[dict[str, Any]]:
    dataset_scope = str(summary_row["dataset_scope"])
    canonical_wave = str(summary_row.get("canonical_wave", "") or "")
    question_id = str(summary_row["question_id"])
    final_driver_id = str(summary_row["final_driver_id"])
    var_code = question_id.split(":", 1)[1] if ":" in question_id else question_id
    frame = fetch_question_frame(conn, dataset_scope, var_code)
    if frame.empty:
        return []
    labeled = to_label_frame(frame)
    if labeled.empty:
        return []

    rows: list[dict[str, Any]] = []
    build_node_rows(
        labeled,
        tree_id=question_id,
        question_id=question_id,
        final_driver_id=final_driver_id,
        dataset_scope=dataset_scope,
        canonical_wave=canonical_wave,
        summary_row=summary_row,
        depth=0,
        parent_node_id=None,
        branch_type="root",
        path_parts=[],
        removed_answers=[],
        rows=rows,
        allow_recursive=True,
    )
    return rows


def append_csv_rows(path: Path, df: pd.DataFrame) -> None:
    if df.empty:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    header = not path.exists()
    df.to_csv(path, mode="a", index=False, header=header)


def load_existing_rows(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    return df


def write_duckdb_table(df: pd.DataFrame, append: bool = False) -> str | None:
    try:
        import duckdb  # type: ignore
    except Exception:
        return None
    if df.empty:
        return str(DUCKDB_PATH)
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(str(DUCKDB_PATH))
    try:
        conn.register("df_view", df)
        if append:
            existing_tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}
            if "recursive_breakage_tree_nodes" in existing_tables:
                conn.execute("INSERT INTO recursive_breakage_tree_nodes SELECT * FROM df_view")
            else:
                conn.execute("CREATE TABLE recursive_breakage_tree_nodes AS SELECT * FROM df_view")
        else:
            conn.execute("CREATE OR REPLACE TABLE recursive_breakage_tree_nodes AS SELECT * FROM df_view")
        return str(DUCKDB_PATH)
    finally:
        conn.close()


def main() -> int:
    load_env()
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_YAML.parent.mkdir(parents=True, exist_ok=True)

    summary = load_question_summary()
    available_sources = sorted(summary["dataset_scope"].astype(str).unique().tolist())
    if args.source:
        summary = summary[summary["dataset_scope"].astype(str) == args.source].copy()
        if summary.empty:
            raise RuntimeError(
                f"V548 source filter {args.source!r} matched nothing. Available source families: {available_sources}"
            )
    if args.wave and "canonical_wave" in summary.columns:
        summary = summary[summary["canonical_wave"].astype(str) == args.wave].copy()
        if summary.empty:
            raise RuntimeError(f"V548 wave filter {args.wave!r} matched nothing in the filtered summary.")
    conn = connect_db()
    reporter = ProgressReporter()
    processed_questions = 0
    skipped_questions = 0
    source_scopes = []
    question_ids: set[str] = set()
    total_rows = 0
    branch_types: Counter[str] = Counter()
    stop_reasons: Counter[str] = Counter()
    existing = load_existing_rows(OUT_CSV) if args.append else pd.DataFrame()
    if not args.append:
        if OUT_CSV.exists():
            OUT_CSV.unlink()
        if OUT_YAML.exists():
            OUT_YAML.unlink()
        if REVIEW_YAML.exists():
            REVIEW_YAML.unlink()
        if OUT_DUCKDB.exists():
            try:
                import duckdb  # type: ignore

                conn0 = duckdb.connect(str(OUT_DUCKDB))
                try:
                    conn0.execute("DROP TABLE IF EXISTS recursive_breakage_tree_nodes")
                finally:
                    conn0.close()
            except Exception:
                pass
    elif not existing.empty:
        if args.source and "tree_id" in existing.columns:
            prefix = f"{args.source}:"
            existing = existing[~existing["tree_id"].astype(str).str.startswith(prefix)]
        if args.wave and "canonical_wave" in existing.columns:
            existing = existing[existing["canonical_wave"].astype(str) != args.wave]
        existing.to_csv(OUT_CSV, index=False)
    try:
        reporter.emit(
            f"loaded V547 summary rows={len(summary)} unique_sources={summary['dataset_scope'].nunique()}"
        )
        for row in summary.itertuples(index=False):
            source_scopes.append(str(row.dataset_scope))
            if processed_questions % PROGRESS_QUESTION_STEP == 0:
                reporter.maybe_emit(
                    f"scanning question {processed_questions + skipped_questions + 1}/{len(summary)} "
                    f"source={row.dataset_scope} question={row.question_id}",
                    force=(processed_questions + skipped_questions == 0),
                )
            rows = build_tree_for_question(pd.Series(row._asdict()), conn)
            if not rows:
                skipped_questions += 1
                continue
            processed_questions += 1
            df_rows = pd.DataFrame(rows)
            append_csv_rows(OUT_CSV, df_rows)
            write_duckdb_table(df_rows, append=True)
            total_rows += len(df_rows)
            question_ids.add(str(row.question_id))
            branch_types.update(df_rows["branch_type"].astype(str).value_counts().to_dict())
            stop_reasons.update(df_rows["stop_reason"].astype(str).value_counts().to_dict())
            if processed_questions % PROGRESS_QUESTION_STEP == 0:
                reporter.emit(
                    f"processed_questions={processed_questions} skipped={skipped_questions} rows={total_rows}"
                )
    finally:
        conn.close()

    if total_rows == 0:
        raise RuntimeError("V548 produced no tree rows.")
    yaml_payload = {
        "pack_id": "V548_RECURSIVE_POSITIONAL_BREAKAGE_TREES",
        "status": "green_recursive_breakage_tree_nodes_written",
        "processed_questions": int(processed_questions),
        "skipped_questions": int(skipped_questions),
        "row_count": int(total_rows),
        "tree_count": int(len(question_ids)),
        "source_scopes": sorted(set(source_scopes)),
        "branch_types": {k: int(v) for k, v in branch_types.items()},
        "stop_reasons": {k: int(v) for k, v in stop_reasons.items()},
        "output_file": str(OUT_CSV),
        "duckdb_file": str(DUCKDB_PATH),
        "limitations": [
            "Recursive expansion follows majority-position deviation branches only.",
            "Weights are exploratory_unweighted because the live respondents table does not include a weight column.",
            "Presence-mode handling is limited to binary 0/1 style items detected from the live responses.",
        ],
    }
    OUT_YAML.write_text(yaml.safe_dump(yaml_payload, sort_keys=False), encoding="utf-8")
    REVIEW_YAML.write_text(yaml.safe_dump(yaml_payload, sort_keys=False), encoding="utf-8")
    reporter.emit(
        f"finished processed_questions={processed_questions} skipped={skipped_questions} rows={total_rows}"
    )
    print(f"V548 wrote {total_rows} recursive_breakage_tree_nodes rows to {OUT_CSV}")
    print(f"Processed questions: {processed_questions}; skipped: {skipped_questions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
