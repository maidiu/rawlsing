#!/usr/bin/env python3
"""Build question_determinicity_summary from live survey_microdata tables.

This V547 builder uses the already-populated survey_microdata_respondents and
survey_microdata_responses tables plus the canonical question structure / driver
registers. It computes a per-question positional determinicity summary using
mutual information against the structural position dimensions available in
survey_microdata_respondents.

The output is intentionally exploratory_unweighted when no weights are present.
"""

from __future__ import annotations

import csv
import argparse
import os
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder


ROOT = Path(__file__).resolve().parents[2]
PACK_ROOT = ROOT / "rawlsing_v5_ddm_production_continuation_pack_v2_ATTITUDE_CLOUD_LOCKED"
OUT_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
OUT_CSV = OUT_DIR / "V547_question_determinicity_summary.csv"
OUT_YAML = OUT_DIR / "V547_question_determinicity_summary.yaml"
REVIEW_YAML = PACK_ROOT / "08_REVIEW" / "V547_question_determinicity_summary_report.yaml"
STRUCTURE_REGISTER = ROOT / "data" / "ddm_build_copy" / "manifests" / "question_structure_register.csv"
MASTER_PATH = ROOT / "data" / "final_codebooks" / "questions_master_drivers.csv"

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
MISSING_CODES = {"8", "9", "98", "99", "101", "999", "-1", "-2"}
MIN_N = 300
PROGRESS_INTERVAL_SECONDS = 20.0
PROGRESS_SOURCE_STEP = 1
PROGRESS_QUESTION_STEP = 50


@dataclass
class SummaryRow:
    analysis_mode: str
    dataset_scope: str
    canonical_wave: str
    question_id: str
    final_driver_id: str
    target_layer: str
    n: int
    weighted_n: float
    country_code_score: float
    country_code_scope: str
    top_predictor_1: str
    top_predictor_1_score: float
    top_interaction_1: str
    top_interaction_1_gain: float
    shape_class: str
    confidence: float


class ProgressReporter:
    def __init__(self, interval_seconds: float = PROGRESS_INTERVAL_SECONDS) -> None:
        self.interval_seconds = interval_seconds
        self.started = time.monotonic()
        self.last_emit = self.started

    def emit(self, message: str) -> None:
        elapsed = time.monotonic() - self.started
        print(f"[V547 +{elapsed:0.0f}s] {message}", flush=True)
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
    parser = argparse.ArgumentParser(description="Build question_determinicity_summary from live survey_microdata tables.")
    parser.add_argument("--source", default=None, help="Optional source-family filter, e.g. WVS or Afrobarometer.")
    parser.add_argument("--wave", default=None, help="Optional wave filter, e.g. W1 or W7.")
    parser.add_argument(
        "--append",
        action="store_true",
        help="Append or replace the filtered source in the existing output instead of rewriting the whole file.",
    )
    return parser.parse_args()


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


def reset_outputs() -> None:
    for path in [OUT_CSV, OUT_YAML, REVIEW_YAML]:
        if path.exists():
            path.unlink()


def family_from_dataset_id(dataset_id: str) -> str:
    if dataset_id.startswith("Afrobarometer"):
        return "Afrobarometer"
    if dataset_id.startswith("Arab"):
        return "Arab Barometer"
    if dataset_id.startswith("Asian"):
        return "Asian Barometer"
    if dataset_id.startswith("EVS"):
        return "EVS"
    if dataset_id.startswith("Latin"):
        return "Latinobarómetro"
    if dataset_id.startswith("WVS"):
        return "WVS"
    return "unknown"


def _read_binding_source(path: Path, family_key: str, question_key: str, driver_key: str) -> dict[str, dict[str, str]]:
    csv.field_size_limit(sys.maxsize)
    by_family_var: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            final_driver_id = (row.get(driver_key) or "").strip()
            if not final_driver_id or final_driver_id.startswith("metadata::"):
                continue
            raw_variable = (row.get(question_key) or "").strip()
            family = (row.get(family_key) or "").strip()
            if not raw_variable or not family:
                continue
            by_family_var[(family, raw_variable)][final_driver_id] += 1

    out: dict[str, dict[str, str]] = defaultdict(dict)
    for (family, raw_variable), counter in by_family_var.items():
        out[family][raw_variable] = counter.most_common(1)[0][0]
    return out


def load_driver_binding_map() -> dict[str, dict[str, str]]:
    """Map source family -> raw_variable -> final_driver_id, preferring the structure register."""
    candidates: list[dict[str, dict[str, str]]] = []

    if STRUCTURE_REGISTER.exists():
        struct_map = _read_binding_source(STRUCTURE_REGISTER, "source_family", "question_name", "final_driver_id")
        candidates.append(struct_map)

    if MASTER_PATH.exists():
        master_map = _read_binding_source(MASTER_PATH, "source", "var_name", "final_driver_id")
        candidates.append(master_map)

    legacy_candidates = [
        PACK_ROOT / "data" / "ddm_build_copy" / "bindings" / "variable_to_driver_binding.csv",
        ROOT / "data" / "ddm_build_copy" / "bindings" / "variable_to_driver_binding.csv",
    ]
    legacy_path = next((p for p in legacy_candidates if p.exists()), None)
    if legacy_path is not None:
        legacy_map = _read_binding_source(legacy_path, "dataset_id", "raw_variable", "final_driver_id")
        remapped: dict[str, dict[str, str]] = defaultdict(dict)
        for dataset_id, vars_ in legacy_map.items():
            family = family_from_dataset_id(dataset_id)
            if family == "unknown":
                continue
            remapped[family].update(vars_)
        candidates.append(remapped)

    if not candidates:
        raise FileNotFoundError(STRUCTURE_REGISTER)

    out: dict[str, dict[str, str]] = defaultdict(dict)
    for candidate in candidates:
        for family, raw_map in candidate.items():
            fam = family.strip()
            if not fam:
                continue
            for raw_variable, final_driver_id in raw_map.items():
                if raw_variable and final_driver_id and raw_variable not in out[fam]:
                    out[fam][raw_variable] = final_driver_id
    return out


def load_respondents(conn) -> dict[str, pd.DataFrame]:
    query = f"""
        SELECT respondent_id,
               source_family AS source,
               wave,
               country_code,
               survey_year,
               sex,
               age,
               education_level,
               income_level,
               religion_label,
               urban_rural
        FROM respondent_position_fact
        ORDER BY respondent_id
    """
    df = pd.read_sql_query(query, conn)
    df["country_code"] = df["country_code"].fillna("").astype(str).str.strip()
    df["sex"] = df["sex"].fillna("").astype(str).str.strip()
    df["education_level"] = pd.to_numeric(df["education_level"], errors="coerce")
    df["income_level"] = pd.to_numeric(df["income_level"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["religion_label"] = df["religion_label"].fillna("").astype(str).str.strip()
    df["urban_rural"] = df["urban_rural"].fillna("").astype(str).str.strip()
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 29, 44, 59, 200],
        labels=["18-29", "30-44", "45-59", "60+"],
        include_lowest=True,
        right=True,
    )
    df["age_group"] = df["age_group"].astype(str).replace("nan", "")
    out: dict[str, pd.DataFrame] = {}
    for source, sub in df.groupby("source", sort=True):
        out[source] = sub.set_index("respondent_id", drop=False)
    return out


def clean_series(s: pd.Series) -> pd.Series:
    return s.replace({"": np.nan, "nan": np.nan})


def normalize_response_values(values: pd.Series) -> pd.Series:
    out = pd.to_numeric(values, errors="coerce")
    out = out.where(~out.isin([float(x) for x in MISSING_CODES if x.lstrip("-").isdigit()]), np.nan)
    out = out.where(~out.isin([-1, -2, 8, 9, 98, 99, 101, 999]), np.nan)
    return out


def encode_for_mi(series: pd.Series) -> tuple[np.ndarray | None, int]:
    s = clean_series(series.astype(str))
    s = s.replace({"None": np.nan, "nan": np.nan, "<NA>": np.nan})
    s = s.dropna()
    if s.nunique() < 2:
        return None, 0
    enc = LabelEncoder().fit_transform(s.values)
    return enc, len(s)


def mi_score(feature: pd.Series, target: pd.Series) -> float:
    joined = pd.DataFrame({"feature": feature, "target": target}).dropna()
    if len(joined) < MIN_N or joined["feature"].nunique() < 2 or joined["target"].nunique() < 2:
        return float("nan")
    X = LabelEncoder().fit_transform(joined["feature"].astype(str).values).reshape(-1, 1)
    y = LabelEncoder().fit_transform(joined["target"].astype(str).values)
    try:
        score = mutual_info_classif(X, y, discrete_features=True, random_state=0)[0]
    except Exception:
        return float("nan")
    return float(score)


def pair_mi_score(feature_a: pd.Series, feature_b: pd.Series, target: pd.Series) -> float:
    joined = pd.DataFrame({"a": feature_a, "b": feature_b, "target": target}).dropna()
    if len(joined) < MIN_N or joined["a"].nunique() < 2 or joined["b"].nunique() < 2 or joined["target"].nunique() < 2:
        return float("nan")
    pair = (joined["a"].astype(str) + "||" + joined["b"].astype(str)).values
    X = LabelEncoder().fit_transform(pair).reshape(-1, 1)
    y = LabelEncoder().fit_transform(joined["target"].astype(str).values)
    try:
        score = mutual_info_classif(X, y, discrete_features=True, random_state=0)[0]
    except Exception:
        return float("nan")
    return float(score)


def explain_shape(top_mi: float, gain: float, n: int) -> str:
    if not np.isfinite(top_mi) or n < MIN_N:
        return "sparse"
    if top_mi < 0.005:
        return "flat"
    if gain > max(0.01, top_mi * 0.25):
        return "interaction"
    if top_mi >= 0.02:
        return "main_effect"
    return "mixed"


def confidence_score(top_mi: float, n: int) -> float:
    if not np.isfinite(top_mi) or n <= 0:
        return 0.0
    sample_factor = min(n / 2000.0, 1.0)
    mi_factor = min(top_mi / 0.05, 1.0)
    return round(min(0.99, 0.35 + 0.35 * sample_factor + 0.30 * mi_factor), 3)


def load_bound_questions(source: str, wave: str | None = None) -> pd.DataFrame:
    if not STRUCTURE_REGISTER.exists():
        raise FileNotFoundError(STRUCTURE_REGISTER)
    df = pd.read_csv(STRUCTURE_REGISTER)
    for col in df.columns:
        if df[col].dtype == "O":
            df[col] = df[col].fillna("").astype(str)
    df["source_family"] = df["source_family"].astype(str).str.strip()
    df["canonical_wave"] = df["canonical_wave"].astype(str).str.strip()
    df["question_name"] = df["question_name"].astype(str).str.strip()
    df = df[df["source_family"] == source]
    if wave:
        df = df[df["canonical_wave"] == wave]
    df = df[df["question_name"] != ""].copy()
    df = df[["question_name", "canonical_wave"]].drop_duplicates().sort_values(["canonical_wave", "question_name"])
    return df.reset_index(drop=True)


def load_questions_for_source(conn, source: str, questions: list[str]) -> dict[str, int]:
    if not questions:
        return {}
    query = f"""
        SELECT r.var_code, COUNT(*) AS n
        FROM {RESPONSES_TABLE} r
        JOIN {RESPONDENTS_TABLE} s ON s.id = r.respondent_id
        WHERE s.source = %s
          AND r.var_code = ANY(%s)
          AND r.value_raw IS NOT NULL
        GROUP BY r.var_code
        ORDER BY r.var_code
    """
    qdf = pd.read_sql_query(query, conn, params=(source, questions))
    return {str(row.var_code): int(row.n) for row in qdf.itertuples(index=False)}


def load_question_frame(conn, source: str, var_code: str) -> pd.DataFrame:
    if facet_ready_view_exists(conn):
        query = f"""
            SELECT
                respondent_id,
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
        """
        df = pd.read_sql_query(query, conn, params=(source, var_code))
    else:
        query = f"""
            SELECT r.respondent_id,
                   r.var_code,
                   r.value_raw,
                   p.country_code,
                   p.sex,
                   p.age,
                   p.education_level,
                   p.income_level,
                   p.religion_label,
                   p.urban_rural
            FROM {RESPONSES_TABLE} r
            JOIN respondent_position_fact p ON p.respondent_id = r.respondent_id
            WHERE p.source_family = %s
              AND r.var_code = %s
              AND r.value_raw IS NOT NULL
        """
        df = pd.read_sql_query(query, conn, params=(source, var_code))
    if df.empty:
        return df
    df["response_value"] = normalize_response_values(df["value_raw"])
    df = df[df["response_value"].notna()].copy()
    df["country_code"] = df["country_code"].fillna("").astype(str).str.strip()
    df["sex"] = df["sex"].fillna("").astype(str).str.strip()
    df["education_level"] = pd.to_numeric(df["education_level"], errors="coerce")
    df["income_level"] = pd.to_numeric(df["income_level"], errors="coerce")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
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


def compute_rows(
    source_filter: str | None = None,
    wave_filter: str | None = None,
    append: bool = False,
) -> List[SummaryRow]:
    load_env()
    binding_map = load_driver_binding_map()
    conn = connect_db()
    reporter = ProgressReporter()
    try:
        if not append:
            reset_outputs()
        respondents_by_source = load_respondents(conn)
        if source_filter:
            respondents_by_source = {
                source: respondents
                for source, respondents in respondents_by_source.items()
                if source == source_filter
            }
        reporter.emit(
            f"loaded respondents sources={len(respondents_by_source)} "
            f"bound_sources={len(binding_map)}"
        )
        if source_filter and source_filter not in binding_map:
            raise RuntimeError(
                f"V547 source filter {source_filter!r} matched nothing. Available source families: {sorted(binding_map)}"
            )
        rows: List[SummaryRow] = []
        shapes: Counter[str] = Counter()
        existing = load_existing_rows(OUT_CSV) if append else pd.DataFrame()
        if not existing.empty:
            if source_filter and "dataset_scope" in existing.columns:
                existing = existing[existing["dataset_scope"].astype(str) != source_filter]
            if wave_filter and "canonical_wave" in existing.columns:
                existing = existing[existing["canonical_wave"].astype(str) != wave_filter]
            existing.to_csv(OUT_CSV, index=False)
        for source_index, (source, respondents) in enumerate(respondents_by_source.items(), start=1):
            if source not in binding_map:
                continue
            bound_questions_df = load_bound_questions(source, wave_filter)
            bound_questions = bound_questions_df["question_name"].tolist()
            if not bound_questions:
                continue
            reporter.emit(
                f"source {source_index}/{len(respondents_by_source)}: {source} "
                f"respondents={len(respondents)} bound_questions={len(bound_questions)}"
            )
            question_counts = load_questions_for_source(conn, source, bound_questions)
            if not question_counts:
                reporter.emit(f"source {source}: no questions found", force=True)
                continue
            reporter.emit(f"source {source}: questions={len(question_counts)}")
            for question_index, (var_code, raw_n) in enumerate(sorted(question_counts.items(), key=lambda x: (-x[1], x[0])), start=1):
                final_driver_id = binding_map[source].get(var_code)
                if not final_driver_id:
                    continue
                question_wave = ""
                if not bound_questions_df.empty:
                    match = bound_questions_df.loc[bound_questions_df["question_name"].astype(str) == var_code, "canonical_wave"]
                    if not match.empty:
                        question_wave = str(match.iloc[0])
                reporter.maybe_emit(
                    f"source {source}: question {question_index}/{len(question_counts)} var={var_code} raw_n={raw_n}",
                    force=(question_index == 1 or question_index == len(question_counts)),
                )
                frame = load_question_frame(conn, source, var_code)
                if frame.empty or len(frame) < MIN_N:
                    continue

                # Align respondent-level position predictors.
                demo = respondents.loc[respondents.index.intersection(frame["respondent_id"])]
                merged = frame.set_index("respondent_id").join(
                    demo[POSITION_COLS + ["survey_year"]],
                    how="inner",
                    rsuffix="_resp",
                )
                if len(merged) < MIN_N:
                    continue

                target = merged["response_value"].astype(str)
                country_code_score = mi_score(merged["country_code"], target)
                predictor_scores: Dict[str, float] = {}
                predictors = {}
                for col in POSITION_COLS:
                    if col == "country_code":
                        continue
                    predictors[col] = merged[col]
                    score = mi_score(predictors[col], target)
                    if np.isfinite(score):
                        predictor_scores[col] = score

                if not predictor_scores and not np.isfinite(country_code_score):
                    continue

                top_predictor_name = "country_code"
                top_predictor_score = float(country_code_score)
                country_code_scope = "baseline_zero_predictor"
                if predictor_scores:
                    top_predictor = max(predictor_scores.items(), key=lambda kv: kv[1])
                    top_predictor_name, top_predictor_score = top_predictor
                elif np.isfinite(country_code_score):
                    country_code_scope = "fallback_top_predictor"

                best_pair_name = ""
                best_pair_gain = float("nan")
                best_pair_score = float("nan")
                best_pair_base = float("nan")
                cols = list(predictor_scores.keys())
                for i in range(len(cols)):
                    for j in range(i + 1, len(cols)):
                        a = cols[i]
                        b = cols[j]
                        pair_score = pair_mi_score(predictors[a], predictors[b], target)
                        if not np.isfinite(pair_score):
                            continue
                        base = max(predictor_scores.get(a, float("nan")), predictor_scores.get(b, float("nan")))
                        gain = pair_score - base if np.isfinite(base) else pair_score
                        if not np.isfinite(best_pair_score) or pair_score > best_pair_score:
                            best_pair_name = f"{a}+{b}"
                            best_pair_score = pair_score
                            best_pair_gain = gain
                            best_pair_base = base

                n = int(len(merged))
                shape = explain_shape(top_predictor_score, best_pair_gain if np.isfinite(best_pair_gain) else 0.0, n)
                conf = confidence_score(top_predictor_score, n)
                rows.append(
                    SummaryRow(
                        analysis_mode="within_country",
                        dataset_scope=source,
                        canonical_wave=question_wave,
                        question_id=f"{source}:{var_code}",
                        final_driver_id=final_driver_id,
                        target_layer="position",
                        n=n,
                        weighted_n=float(n),
                        country_code_score=round(float(country_code_score), 6) if np.isfinite(country_code_score) else float("nan"),
                        country_code_scope=country_code_scope,
                        top_predictor_1=top_predictor_name,
                        top_predictor_1_score=round(float(top_predictor_score), 6),
                        top_interaction_1=best_pair_name,
                        top_interaction_1_gain=round(float(best_pair_gain), 6) if np.isfinite(best_pair_gain) else 0.0,
                        shape_class=shape,
                        confidence=conf,
                    )
                )
                shapes[shape] += 1
                append_csv_rows(OUT_CSV, pd.DataFrame([rows[-1].__dict__]))
                if question_index % PROGRESS_QUESTION_STEP == 0:
                    reporter.maybe_emit(
                        f"source {source}: processed {question_index}/{len(question_counts)} questions rows={len(rows)}",
                        force=True,
                    )
            if rows:
                payload = {
                    "status": "green_question_determinicity_summary_written",
                    "analysis_mode": "within_country",
                    "country_code_policy": "baseline_zero_predictor",
                    "row_count": int(len(rows)),
                    "source_scopes": sorted(set(r.dataset_scope for r in rows)),
                    "top_shapes": dict(shapes),
                    "output_file": str(OUT_CSV),
                }
                OUT_YAML.write_text("\n".join(f"{k}: {repr(v)}" for k, v in payload.items()) + "\n", encoding="utf-8")
                REVIEW_YAML.write_text(
                    "\n".join(
                        [
                            "pack_id: V547_QUESTION_LEVEL_POSITIONAL_DETERMINICITY",
                            f"status: {payload['status']}",
                            f"row_count: {payload['row_count']}",
                            f"output_file: {payload['output_file']}",
                            f"source_scopes: {payload['source_scopes']}",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )
        return rows
    finally:
        conn.close()


def main() -> int:
    args = parse_args()
    rows = compute_rows(args.source, args.wave, args.append)
    print(f"V547 wrote {len(rows)} question_determinicity_summary rows to {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
