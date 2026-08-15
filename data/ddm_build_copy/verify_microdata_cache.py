#!/usr/bin/env python3
"""Verify the loaded survey microdata cache after reloads.

This is a lightweight Postgres sanity check for the reload path. It reports:
- total respondent/response counts
- counts by source family
- response coverage by source family
- families with respondents but no response rows

It is intentionally read-only and safe to run while waiting for reloads to
finish, though the final numbers should be read after the reload settles.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import psycopg2
import yaml
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "ddm_build_copy" / "reports"
OUT_YAML = OUT_DIR / "microdata_cache_verification.yaml"
OUT_CSV = OUT_DIR / "microdata_cache_verification.csv"

RESPONDENTS_TABLE = "survey_microdata_respondents"
RESPONSES_TABLE = "survey_microdata_responses"


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is missing; cannot verify the live microdata cache.")
    return psycopg2.connect(db_url)


def run_verification() -> tuple[pd.DataFrame, dict]:
    conn = connect_db()
    try:
        respondents = pd.read_sql_query(
            f"""
            SELECT source, country_code, survey_year
            FROM {RESPONDENTS_TABLE}
            ORDER BY source, country_code, survey_year
            """,
            conn,
        )
        responses = pd.read_sql_query(
            f"""
            SELECT s.source, COUNT(*) AS response_rows
            FROM {RESPONSES_TABLE} r
            JOIN {RESPONDENTS_TABLE} s ON s.id = r.respondent_id
            GROUP BY s.source
            ORDER BY s.source
            """,
            conn,
        )
        total_respondents = len(respondents)
        total_responses = int(
            pd.read_sql_query(f"SELECT COUNT(*) AS n FROM {RESPONSES_TABLE}", conn).iloc[0]["n"]
        )
        respondent_by_source = respondents.groupby("source").size().reset_index(name="respondents")
        summary = respondent_by_source.merge(responses, on="source", how="left")
        summary["response_rows"] = summary["response_rows"].fillna(0).astype(int)
        summary["response_rows_per_respondent"] = summary.apply(
            lambda r: round(r["response_rows"] / r["respondents"], 3) if r["respondents"] else 0.0,
            axis=1,
        )
        summary = summary.sort_values(["respondents", "source"], ascending=[False, True]).reset_index(drop=True)

        manifest = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status": "ok" if total_respondents and total_responses else "degraded",
            "total_respondents": int(total_respondents),
            "total_responses": int(total_responses),
            "families": summary.to_dict(orient="records"),
            "families_with_zero_responses": summary.loc[summary["response_rows"] == 0, "source"].astype(str).tolist(),
            "notes": [
                "This report only checks the live Postgres cache tables.",
                "Read it after the reload finishes to avoid partial-run noise.",
            ],
        }
        return summary, manifest
    finally:
        conn.close()


def main() -> int:
    load_env()
    summary, manifest = run_verification()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUT_CSV, index=False)
    OUT_YAML.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    print(f"total_respondents: {manifest['total_respondents']}")
    print(f"total_responses: {manifest['total_responses']}")
    for row in summary.itertuples(index=False):
        print(f"  {row.source}: respondents={row.respondents} responses={row.response_rows} ratio={row.response_rows_per_respondent}")
    if manifest["families_with_zero_responses"]:
        print("families_with_zero_responses:", ", ".join(manifest["families_with_zero_responses"]))
    print(f"YAML: {OUT_YAML}")
    print(f"CSV: {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
