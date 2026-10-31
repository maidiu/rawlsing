#!/usr/bin/env python3
"""
Run the same MI (mutual information) logic as Phase 1A on survey_microdata for a barometer.

Output: demographic determinicity ranking (mean MI across questions) to CSV.
Compare to WVS Phase 1A ranking to validate whether a single BROADEN_ORDER is justified.

Usage (from repo root):
  python3 v2/run_determinicity_survey_microdata.py [--source Afrobarometer] [--out data/determinicity_ranking_afrobarometer.csv]

Requires: survey_microdata_respondents + survey_microdata_responses populated for the source.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass
if not os.environ.get("DATABASE_URL") and (ROOT / ".env").exists():
    with open(ROOT / ".env", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == "DATABASE_URL" and v:
                    os.environ["DATABASE_URL"] = v
                    break

# Demographic columns we have in survey_microdata_respondents (conceptually aligned with WVS)
DEMO_COLS = [
    "country_code",
    "sex",
    "age_group",
    "education_level",
    "income_level",
    "urban_rural",
    "religion",
]
AGE_BINS = [18, 30, 45, 60, 121]
MIN_RESPONDENTS_PER_QUESTION = 300


def get_db_connection():
    import psycopg2
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        conn = psycopg2.connect(db_url)
    else:
        conn = psycopg2.connect(
            host=os.environ.get("PGHOST", "localhost"),
            database=os.environ.get("PGDATABASE", "Rawlsing—WVS"),
            user=os.environ.get("PGUSER", "postgres"),
            password=os.environ.get("PGPASSWORD", ""),
        )
    return conn


def load_var_codes_for_source(source: str) -> list[str]:
    """Load var_code suffixes from item_content_map for items starting with source prefix."""
    path = ROOT / "data" / "final_codebooks" / "item_content_map.csv"
    if not path.exists():
        return []
    prefixes = []
    if source == "Afrobarometer":
        prefixes = ["Afrobarometer:R1:", "Afrobarometer:R9:"]
    elif source == "Latinobarómetro":
        prefixes = ["Latinobarómetro:1995:", "Latinobarómetro:2024:"]
    elif source == "Arab Barometer":
        prefixes = ["Arab Barometer:W1:", "Arab Barometer:W8:"]
    elif source == "Asian Barometer":
        prefixes = ["Asian Barometer:W1:", "Asian Barometer:W6:"]
    else:
        prefixes = [f"{source}:"]
    var_codes = set()
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.lower().startswith("item_id"):
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            item_id = parts[0].strip()
            for prefix in prefixes:
                if item_id.startswith(prefix):
                    suffix = item_id[len(prefix):].strip()
                    if suffix:
                        var_codes.add(suffix)
                    break
    return sorted(var_codes)


def run_mi_for_source(source: str, out_path: Path | None) -> pd.DataFrame:
    conn = get_db_connection()
    cur = conn.cursor()

    # Respondents with demographics (columns may be NULL if loader didn't populate them)
    cur.execute("""
        SELECT id AS respondent_id, country_code, sex, age,
               education_level, income_level, urban_rural,
               religion_label
        FROM survey_microdata_respondents
        WHERE source = %s
          AND country_code IS NOT NULL
    """, (source,))
    cols = [d[0] for d in cur.description]
    respondents = pd.DataFrame(cur.fetchall(), columns=cols)
    cur.close()
    conn.close()

    if len(respondents) < MIN_RESPONDENTS_PER_QUESTION:
        print(f"Too few respondents for {source}: {len(respondents)}")
        return pd.DataFrame()

    # Age binning (age may be missing for some loaders)
    if "age" not in respondents.columns:
        respondents["age"] = np.nan
    respondents["age"] = pd.to_numeric(respondents["age"], errors="coerce")
    respondents = respondents[respondents["age"].notna()]
    respondents["age_group"] = pd.cut(
        respondents["age"],
        bins=AGE_BINS,
        labels=[f"{AGE_BINS[i]}-{AGE_BINS[i+1]-1}" for i in range(len(AGE_BINS)-1)],
        right=False,
    )
    if "religion_label" in respondents.columns:
        respondents["religion"] = respondents["religion_label"].fillna("").astype(str)
    else:
        respondents["religion"] = ""
    respondents = respondents.drop(columns=["religion_label"] if "religion_label" in respondents.columns else [], errors="ignore")
    if "age" in respondents.columns:
        respondents = respondents.drop(columns=["age"], errors="ignore")

    # Require only demographics that are present; drop rows missing on those we have
    required = [c for c in ["country_code", "sex", "age_group"] if c in respondents.columns]
    for col in required:
        respondents = respondents[respondents[col].notna()]
    # Optionally drop missing on others only if column has mostly non-null (so we can use it in MI)
    for col in ["education_level", "income_level", "urban_rural", "religion"]:
        if col in respondents.columns and respondents[col].notna().sum() >= MIN_RESPONDENTS_PER_QUESTION:
            respondents = respondents[respondents[col].notna()]
    if len(respondents) < MIN_RESPONDENTS_PER_QUESTION:
        print(f"Too few respondents after dropping missing: {len(respondents)}")
        return pd.DataFrame()

    var_codes = load_var_codes_for_source(source)
    if not var_codes:
        print(f"No var_codes found in item_content_map for {source}")
        return pd.DataFrame()

    conn = get_db_connection()
    cur = conn.cursor()

    # Per-question MI
    results = []
    source_cols = [c for c in DEMO_COLS if c in respondents.columns]
    rid_set = set(respondents["respondent_id"])

    for i, var_code in enumerate(var_codes):
        if (i + 1) % 20 == 0:
            print(f"  Question {i+1}/{len(var_codes)} ...")
        cur.execute("""
            SELECT respondent_id, value_raw
            FROM survey_microdata_responses
            WHERE respondent_id = ANY(%s) AND var_code = %s AND value_raw IS NOT NULL
        """, (list(rid_set), var_code))
        rows = cur.fetchall()
        if len(rows) < MIN_RESPONDENTS_PER_QUESTION:
            continue
        resp_df = pd.DataFrame(rows, columns=["respondent_id", "value_raw"])
        resp_df["value_raw"] = pd.to_numeric(resp_df["value_raw"], errors="coerce")
        resp_df = resp_df[resp_df["value_raw"].notna()]
        resp_df = resp_df[(resp_df["value_raw"] >= 0) & (resp_df["value_raw"] <= 100)]
        if len(resp_df) < MIN_RESPONDENTS_PER_QUESTION:
            continue
        df_q = respondents.merge(resp_df, on="respondent_id", how="inner")
        if len(df_q) < MIN_RESPONDENTS_PER_QUESTION:
            continue
        y = LabelEncoder().fit_transform(df_q["value_raw"].astype(str).values)
        for col in source_cols:
            X_raw = df_q[col].astype(str).fillna("").values
            if len(np.unique(X_raw)) < 2:
                continue
            try:
                X = LabelEncoder().fit_transform(X_raw).reshape(-1, 1)
                mi_vals = mutual_info_classif(X, y, discrete_features=True, random_state=0)
                results.append({"var_code": var_code, "demographic": col, "mi": float(mi_vals[0])})
            except Exception:
                continue

    cur.close()
    conn.close()

    if not results:
        print("No MI results.")
        return pd.DataFrame()

    df_res = pd.DataFrame(results)
    summary = df_res.groupby("demographic")["mi"].agg(["mean", "median", "count"]).reset_index()
    summary = summary.sort_values("mean", ascending=False).reset_index(drop=True)
    summary["rank"] = summary.index + 1
    summary["source"] = source
    print(f"\nDeterminicity ranking for {source} (mean MI across {df_res['var_code'].nunique()} questions):")
    print(summary[["demographic", "mean", "rank"]].to_string(index=False))

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(out_path, index=False)
        print(f"\nWrote {out_path}")

    return summary


def main():
    parser = argparse.ArgumentParser(description="Run MI determinicity ranking on survey_microdata")
    parser.add_argument("--source", default="Afrobarometer", help="Source: Afrobarometer, Latinobarómetro, Arab Barometer, Asian Barometer")
    parser.add_argument("--out", default=None, help="Output CSV path")
    args = parser.parse_args()
    out_path = Path(args.out) if args.out else ROOT / "data" / f"determinicity_ranking_{args.source.replace(' ', '_').lower()}.csv"
    run_mi_for_source(args.source, out_path)


if __name__ == "__main__":
    main()
