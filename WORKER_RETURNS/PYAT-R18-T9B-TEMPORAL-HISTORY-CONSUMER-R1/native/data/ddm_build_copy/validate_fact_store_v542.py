#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb
import pandas as pd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--duckdb", required=True)
    ap.add_argument("--source-manifest", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    con = duckdb.connect(args.duckdb, read_only=True)
    tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
    required = ["respondent_fact", "respondent_position_fact", "response_fact", "survey_weight_fact"]
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}

    for table in required:
        if table not in tables:
            errors.append(f"missing table {table}")
            counts[table] = 0
            continue
        counts[table] = int(con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        if table != "survey_weight_fact" and counts[table] == 0:
            errors.append(f"{table} empty")
        if table == "survey_weight_fact" and counts[table] == 0:
            warnings.append("survey_weight_fact empty; no weight rows detected")

    if "respondent_fact" in tables:
        dup = int(con.execute("SELECT COUNT(*) - COUNT(DISTINCT respondent_uid) FROM respondent_fact").fetchone()[0])
        if dup:
            errors.append(f"duplicate respondent_uid {dup}")

    if {"response_fact", "respondent_fact"} <= tables:
        orphan = int(
            con.execute(
                "SELECT COUNT(*) FROM response_fact x LEFT JOIN respondent_fact r ON r.respondent_uid = x.respondent_uid WHERE r.respondent_uid IS NULL"
            ).fetchone()[0]
        )
        if orphan:
            errors.append(f"orphan response_fact rows {orphan}")

    if {"respondent_position_fact", "respondent_fact"} <= tables:
        orphan = int(
            con.execute(
                "SELECT COUNT(*) FROM respondent_position_fact x LEFT JOIN respondent_fact r ON r.respondent_uid = x.respondent_uid WHERE r.respondent_uid IS NULL"
            ).fetchone()[0]
        )
        if orphan:
            errors.append(f"orphan respondent_position_fact rows {orphan}")

    if {"survey_weight_fact", "respondent_fact"} <= tables:
        orphan = int(
            con.execute(
                "SELECT COUNT(*) FROM survey_weight_fact x LEFT JOIN respondent_fact r ON r.respondent_uid = x.respondent_uid WHERE r.respondent_uid IS NULL"
            ).fetchone()[0]
        )
        if orphan:
            errors.append(f"orphan survey_weight_fact rows {orphan}")

    manifest = pd.read_csv(args.source_manifest, dtype=str, keep_default_na=False)
    expected = len(manifest)
    actual = int(
        con.execute(
            "SELECT COUNT(DISTINCT dataset_id || '::' || COALESCE(source_family,'') || '::' || COALESCE(wave,'')) FROM respondent_fact"
        ).fetchone()[0]
        if "respondent_fact" in tables
        else 0
    )
    if actual and actual < expected:
        warnings.append(f"dataset coverage incomplete {actual}/{expected}")

    reports = repo / "data/ddm_build_copy/reports"
    reports.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([{"table": t, "rows": counts.get(t, 0)} for t in required]).to_csv(
        reports / "V542_fact_store_table_counts.csv", index=False
    )
    report = {"status": "green" if not errors else "blocked", "errors": errors, "warnings": warnings, "table_counts": counts}
    (reports / "V542_fact_store_validation_report.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
