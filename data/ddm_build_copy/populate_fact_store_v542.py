#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import duckdb
import pandas as pd
import pyreadstat

MISSING_CODES = {-3, -2, -1, 8, 9, 98, 99, 101, 888, 999, 9999}
MISSING_LABEL_RE = re.compile(
    r"don't know|do not know|\bdk\b|refused|no answer|missing|not applicable|\bn/a\b|\bna\b",
    re.I,
)
WEIGHT_RE = re.compile(r"wt|wgt|weight|pweight|acrosswt|withinwt|afcombwt|africawt", re.I)
NATIVE_ID_RE = re.compile(r"^(respondent|case|interview|serial|id|resp|pid|uuid)[\w\.]*$", re.I)
COUNTRY_RE = re.compile(r"^(country|country_name|countrycode|country_code|ccode|iso2|iso3)$", re.I)
YEAR_RE = re.compile(r"^(year|survey_year|fieldwork_year|interview_year)$", re.I)


def safe(x: Any) -> str:
    if x is None:
        return ""
    try:
        if pd.isna(x):
            return ""
    except Exception:
        pass
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return str(x)


def sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def missing(raw: Any, label: str = "") -> bool:
    t = safe(raw).strip()
    if not t or t.lower() in {"nan", "none", "<na>"}:
        return True
    try:
        v = float(t)
        if abs(v - round(v)) < 1e-9 and int(round(v)) in MISSING_CODES:
            return True
    except Exception:
        pass
    return bool(label and MISSING_LABEL_RE.search(label))


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def log(start: datetime, msg: str) -> None:
    elapsed = int((datetime.now(timezone.utc) - start).total_seconds())
    print(f"[V542 +{elapsed}s] {msg}", flush=True)


def create_tables(con: duckdb.DuckDBPyConnection) -> None:
    sql = """
    CREATE TABLE IF NOT EXISTS respondent_fact (
      respondent_uid VARCHAR PRIMARY KEY,
      native_respondent_id VARCHAR,
      dataset_id VARCHAR,
      source_family VARCHAR,
      wave VARCHAR,
      canonical_wave VARCHAR,
      country VARCHAR,
      country_code VARCHAR,
      row_index BIGINT,
      survey_year INTEGER,
      source_file VARCHAR,
      source_file_sha256 VARCHAR,
      load_batch_id VARCHAR,
      loaded_at_utc TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS respondent_position_fact (
      respondent_uid VARCHAR,
      dataset_id VARCHAR,
      source_family VARCHAR,
      wave VARCHAR,
      position_dimension VARCHAR,
      raw_variable VARCHAR,
      raw_value VARCHAR,
      canonical_value VARCHAR,
      confidence DOUBLE,
      ethical_use_flag VARCHAR,
      load_batch_id VARCHAR
    );

    CREATE TABLE IF NOT EXISTS response_fact (
      respondent_uid VARCHAR,
      dataset_id VARCHAR,
      source_family VARCHAR,
      wave VARCHAR,
      raw_variable VARCHAR,
      raw_value VARCHAR,
      normalized_value VARCHAR,
      value_label VARCHAR,
      missing_flag BOOLEAN,
      final_driver_id VARCHAR,
      question_id VARCHAR,
      question_block_id VARCHAR,
      structural_domain_id VARCHAR,
      driver_facet_id VARCHAR,
      relation_axis_id VARCHAR,
      target_entity_id VARCHAR,
      question_type VARCHAR,
      source_match_type VARCHAR,
      load_batch_id VARCHAR
    );

    CREATE TABLE IF NOT EXISTS survey_weight_fact (
      respondent_uid VARCHAR,
      dataset_id VARCHAR,
      source_family VARCHAR,
      wave VARCHAR,
      weight_type VARCHAR,
      raw_variable VARCHAR,
      weight_value DOUBLE,
      load_batch_id VARCHAR
    );
    """
    for stmt in sql.split(";"):
        if stmt.strip():
            con.execute(stmt)


EXPECTED_TABLE_COLUMNS = {
    "respondent_fact": [
        "respondent_uid",
        "native_respondent_id",
        "dataset_id",
        "source_family",
        "wave",
        "canonical_wave",
        "country",
        "country_code",
        "row_index",
        "survey_year",
        "source_file",
        "source_file_sha256",
        "load_batch_id",
        "loaded_at_utc",
    ],
    "respondent_position_fact": [
        "respondent_uid",
        "dataset_id",
        "source_family",
        "wave",
        "position_dimension",
        "raw_variable",
        "raw_value",
        "canonical_value",
        "confidence",
        "ethical_use_flag",
        "load_batch_id",
    ],
    "response_fact": [
        "respondent_uid",
        "dataset_id",
        "source_family",
        "wave",
        "raw_variable",
        "raw_value",
        "normalized_value",
        "value_label",
        "missing_flag",
        "final_driver_id",
        "question_id",
        "question_block_id",
        "structural_domain_id",
        "driver_facet_id",
        "relation_axis_id",
        "target_entity_id",
        "question_type",
        "source_match_type",
        "load_batch_id",
    ],
    "survey_weight_fact": [
        "respondent_uid",
        "dataset_id",
        "source_family",
        "wave",
        "weight_type",
        "raw_variable",
        "weight_value",
        "load_batch_id",
    ],
}


def ensure_fact_table_schema(con: duckdb.DuckDBPyConnection) -> bool:
    existing_tables = {r[0] for r in con.execute("SHOW TABLES").fetchall()}
    if not existing_tables:
        create_tables(con)
        return False
    mismatch = False
    for table, expected_cols in EXPECTED_TABLE_COLUMNS.items():
        if table not in existing_tables:
            mismatch = True
            continue
        existing_cols = [r[1] for r in con.execute(f"PRAGMA table_info('{table}')").fetchall()]
        if existing_cols != expected_cols:
            mismatch = True
    if mismatch:
        for table in EXPECTED_TABLE_COLUMNS:
            con.execute(f"DROP TABLE IF EXISTS {table}")
        create_tables(con)
    return mismatch


def insert_df(con: duckdb.DuckDBPyConnection, table: str, df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    con.register("_df", df)
    cols = ", ".join(df.columns)
    con.execute(f"INSERT INTO {table} ({cols}) SELECT {cols} FROM _df")
    con.unregister("_df")
    return len(df)


def first_present_col(df: pd.DataFrame, candidates: Iterable[str]) -> str:
    lowered = {c.lower(): c for c in df.columns}
    for cand in candidates:
        if cand.lower() in lowered:
            return lowered[cand.lower()]
    return ""


def first_nonempty_series(df: pd.DataFrame, candidates: Iterable[str]) -> tuple[str, pd.Series | None]:
    col = first_present_col(df, candidates)
    if not col:
        return "", None
    return col, df[col]


def decode_series(series: pd.Series, label_map: dict[str, str]) -> pd.Series:
    if series is None:
        return pd.Series(dtype=str)
    raw = series.map(safe)
    if not label_map:
        return raw
    return raw.map(lambda x: label_map.get(x, x))


def make_uid(dataset_id: str, row_index: int, native_id: str) -> str:
    seed = f"{dataset_id}::{row_index}::{native_id or ''}"
    return sha_text(seed)


def build_driver_map(qmd: pd.DataFrame) -> dict[tuple[str, str, str], dict[str, str]]:
    out: dict[tuple[str, str, str], dict[str, str]] = {}
    for _, r in qmd.iterrows():
        source = safe(r.get("source"))
        wave = safe(r.get("wave"))
        var_name = safe(r.get("var_name"))
        if not source or not wave or not var_name:
            continue
        key = (source, wave, var_name)
        cur = out.setdefault(
            key,
            {
                "final_driver_id": "",
                "question_block_id": "",
                "structural_domain_id": "",
                "driver_facet_id": "",
                "relation_axis_id": "",
                "target_entity_id": "",
                "mapping_status": "",
            },
        )
        for field in list(cur):
            val = safe(r.get(field))
            if val and not cur[field]:
                cur[field] = val
        if not cur["final_driver_id"]:
            cur["final_driver_id"] = safe(r.get("final_driver_id"))
    return out


def build_question_map(
    qreg: pd.DataFrame,
    driver_map: dict[tuple[str, str, str], dict[str, str]],
    include_unregistered: bool,
) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    for _, r in qreg.iterrows():
        dataset_id = safe(r.get("dataset_id"))
        col = safe(r.get("matched_source_column")) or safe(r.get("question_name"))
        if not dataset_id or not col:
            continue
        source_present = safe(r.get("source_present")).strip().lower() == "yes"
        if not source_present and not include_unregistered:
            continue
        key = (dataset_id, col)
        cur = out.setdefault(
            key,
            {
                "question_id": "",
                "final_driver_id": "",
                "question_block_id": "",
                "structural_domain_id": "",
                "driver_facet_id": "",
                "relation_axis_id": "",
                "target_entity_id": "",
                "question_type": "",
                "source_match_type": "",
            },
        )
        for field in list(cur):
            val = safe(r.get(field))
            if val and not cur[field]:
                cur[field] = val
        if not cur["question_id"]:
            cur["question_id"] = safe(r.get("question_id")) or f"{safe(r.get('source_family'))}:{col}"
        if not cur["final_driver_id"]:
            cur["final_driver_id"] = safe(r.get("final_driver_id"))
        if not cur["question_type"]:
            cur["question_type"] = safe(r.get("question_type"))
        if not cur["source_match_type"]:
            cur["source_match_type"] = safe(r.get("source_match_type"))
        driver_key = (safe(r.get("source_family")), safe(r.get("wave")), col)
        if driver_key in driver_map:
            for field, val in driver_map[driver_key].items():
                if val and not cur.get(field):
                    cur[field] = val
    return out


def build_position_map(demo: pd.DataFrame) -> dict[tuple[str, str, str], dict[str, float | str]]:
    out = {}
    for _, r in demo.iterrows():
        out[(safe(r.get("source_family")), safe(r.get("wave")), safe(r.get("var_name")))] = {
            "dimension": safe(r.get("demographic_kind")),
            "confidence": float(safe(r.get("demographic_confidence")) or 0.5),
        }
    return out


def build_metadata_lookup(qreg: pd.DataFrame) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    for _, r in qreg.iterrows():
        dataset_id = safe(r.get("dataset_id"))
        driver = safe(r.get("final_driver_id"))
        col = safe(r.get("matched_source_column"))
        if not dataset_id or not driver or not col:
            continue
        if not driver.startswith("metadata::metadata_"):
            continue
        entry = out.setdefault(dataset_id, {})
        if driver == "metadata::metadata_country" and "country" not in entry:
            entry["country"] = col
        elif driver == "metadata::metadata_country_code" and "country_code" not in entry:
            entry["country_code"] = col
        elif "metadata::metadata_year" in driver and "survey_year" not in entry:
            entry["survey_year"] = col
        elif driver == "metadata::metadata_wave" and "native_wave" not in entry:
            entry["native_wave"] = col
        elif "metadata::metadata_respondent_id" in driver and "native_respondent_id" not in entry:
            entry["native_respondent_id"] = col
    return out


def read_file(path: Path, fmt: str):
    if fmt == "sav":
        return pyreadstat.read_sav(str(path), apply_value_formats=False)
    if fmt == "dta":
        return pyreadstat.read_dta(str(path), apply_value_formats=False)
    raise ValueError(f"unsupported format: {fmt}")


def write_dataset_report(repo: Path, row: dict[str, Any]) -> None:
    reports = repo / "data/ddm_build_copy/reports"
    reports.mkdir(parents=True, exist_ok=True)
    out = reports / "V542_population_dataset_manifest.csv"
    df = pd.DataFrame([row])
    if out.exists():
        df.to_csv(out, mode="a", header=False, index=False)
    else:
        df.to_csv(out, index=False)


def load_existing_manifest(repo: Path) -> pd.DataFrame:
    path = repo / "data/ddm_build_copy/reports/V542_population_dataset_manifest.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source-manifest", required=True)
    ap.add_argument("--question-register", required=True)
    ap.add_argument("--demographic-register", required=True)
    ap.add_argument("--questions-master-drivers", required=True)
    ap.add_argument("--duckdb", required=True)
    ap.add_argument("--replace", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--dataset-id")
    ap.add_argument("--source-family")
    ap.add_argument("--wave")
    ap.add_argument("--include-unregistered-columns", action="store_true")
    ap.add_argument("--skip-missing-responses", action="store_true")
    args = ap.parse_args()

    start = datetime.now(timezone.utc)
    repo = Path(args.repo_root).resolve()
    manifest = load_csv(Path(args.source_manifest))
    qreg = load_csv(Path(args.question_register))
    demo = load_csv(Path(args.demographic_register))
    qmd = load_csv(Path(args.questions_master_drivers))

    if args.dataset_id:
        manifest = manifest[manifest.dataset_id.eq(args.dataset_id)]
    if args.source_family:
        manifest = manifest[manifest.source_family.eq(args.source_family)]
    if args.wave:
        manifest = manifest[manifest.wave.eq(args.wave)]

    driver_map = build_driver_map(qmd)
    question_map = build_question_map(qreg, driver_map, include_unregistered=args.include_unregistered_columns)
    position_map = build_position_map(demo)
    metadata_lookup = build_metadata_lookup(qreg)

    con = duckdb.connect(args.duckdb)
    schema_repaired = ensure_fact_table_schema(con)
    if args.replace:
        for table in ["respondent_fact", "respondent_position_fact", "response_fact", "survey_weight_fact"]:
            con.execute(f"DELETE FROM {table}")
        reports = repo / "data/ddm_build_copy/reports"
        for report_name in ["V542_population_dataset_manifest.csv", "V542_population_report.json"]:
            report_path = reports / report_name
            if report_path.exists():
                report_path.unlink()

    batch = "V542_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    report_rows: list[dict[str, Any]] = []
    existing_manifest = load_existing_manifest(repo) if args.resume and not args.replace else pd.DataFrame()
    completed_ids = set()
    if not existing_manifest.empty and "dataset_id" in existing_manifest.columns and "status" in existing_manifest.columns:
        completed_ids = set(
            existing_manifest.loc[existing_manifest["status"].eq("green_loaded"), "dataset_id"].astype(str).tolist()
        )
    if schema_repaired:
        log(start, "fact table schema repaired to canonical V542 layout")
    log(start, f"starting batch={batch} datasets={len(manifest)} include_unregistered={args.include_unregistered_columns}")

    for idx, ds in enumerate(manifest.itertuples(index=False), start=1):
        did = safe(getattr(ds, "dataset_id", ""))
        src = safe(getattr(ds, "source_family", ""))
        wave = safe(getattr(ds, "wave", ""))
        fmt = safe(getattr(ds, "format", "")).lower()
        raw_path = Path(safe(getattr(ds, "path", "")))
        if not raw_path.is_absolute():
            raw_path = repo / raw_path
        row_report = {
            "load_batch_id": batch,
            "dataset_id": did,
            "source_family": src,
            "wave": wave,
            "raw_file": str(raw_path),
            "status": "error",
            "raw_rows": 0,
            "raw_columns": 0,
            "respondent_fact_rows": 0,
            "respondent_position_fact_rows": 0,
            "response_fact_rows": 0,
            "survey_weight_fact_rows": 0,
            "missing_response_rows": 0,
            "skipped_unregistered_columns": 0,
            "error": "",
        }

        if not raw_path.exists():
            row_report["error"] = "missing raw file"
            report_rows.append(row_report)
            write_dataset_report(repo, row_report)
            log(start, f"dataset {idx}/{len(manifest)} {did}: missing raw file")
            continue

        if args.resume and did in completed_ids:
            row_report["status"] = "skipped_completed"
            row_report["raw_rows"] = int(
                con.execute("SELECT COUNT(*) FROM respondent_fact WHERE dataset_id = ?", [did]).fetchone()[0]
            )
            row_report["respondent_fact_rows"] = row_report["raw_rows"]
            report_rows.append(row_report)
            log(start, f"dataset {idx}/{len(manifest)} {did}: already complete, skipping")
            continue

        try:
            log(start, f"dataset {idx}/{len(manifest)} {did}: reading {raw_path.name}")
            if args.resume:
                existing_rows = int(
                    con.execute("SELECT COUNT(*) FROM respondent_fact WHERE dataset_id = ?", [did]).fetchone()[0]
                )
                if existing_rows:
                    log(start, f"dataset {idx}/{len(manifest)} {did}: clearing partial rows before rerun rows={existing_rows}")
                    for table in [
                        "response_fact",
                        "respondent_position_fact",
                        "survey_weight_fact",
                        "respondent_fact",
                    ]:
                        con.execute(f"DELETE FROM {table} WHERE dataset_id = ?", [did])
            df, meta = read_file(raw_path, fmt)
            labels = getattr(meta, "variable_value_labels", {}) or {}
            fsha = file_sha(raw_path)
            loaded_at = datetime.now(timezone.utc).replace(tzinfo=None)
            canonical_wave = safe(qreg.loc[qreg.dataset_id.eq(did), "canonical_wave"].dropna().astype(str).head(1).squeeze()) or wave

            row_report["raw_rows"] = int(len(df))
            row_report["raw_columns"] = int(len(df.columns))

            native_id_col = first_present_col(
                df,
                [
                    metadata_lookup.get(did, {}).get("native_respondent_id", ""),
                    "respondent_id",
                    "caseid",
                    "case_id",
                    "serial",
                    "serialno",
                    "interviewid",
                    "interview_id",
                    "respid",
                    "respondentid",
                    "id",
                ],
            )
            native_ids = df[native_id_col].map(safe) if native_id_col else pd.Series([""] * len(df))
            country_col = first_present_col(
                df,
                [
                    metadata_lookup.get(did, {}).get("country", ""),
                    "country",
                    "country_name",
                    "COUNTRY",
                    "countrycode",
                    "country_code",
                    "ccode",
                    "iso2",
                    "iso3",
                ],
            )
            country_code_col = first_present_col(
                df,
                [
                    metadata_lookup.get(did, {}).get("country_code", ""),
                    "country_code",
                    "countrycode",
                    "ccode",
                    "iso2",
                    "iso3",
                ],
            )
            survey_year_col = first_present_col(
                df,
                [
                    metadata_lookup.get(did, {}).get("survey_year", ""),
                    "survey_year",
                    "year",
                    "fieldwork_year",
                    "interview_year",
                ],
            )

            respondent_rows = []
            country_series = decode_series(df[country_col], labels.get(country_col, {})) if country_col else pd.Series([""] * len(df))
            country_code_series = decode_series(df[country_code_col], labels.get(country_code_col, {})) if country_code_col else pd.Series([""] * len(df))
            survey_year_series = pd.to_numeric(df[survey_year_col], errors="coerce") if survey_year_col else pd.Series([pd.NA] * len(df))
            for row_index in range(len(df)):
                native_id = safe(native_ids.iloc[row_index]) if len(native_ids) else ""
                respondent_rows.append(
                    {
                        "respondent_uid": make_uid(did, row_index, native_id),
                        "native_respondent_id": native_id,
                        "dataset_id": did,
                        "source_family": src,
                        "wave": wave,
                        "canonical_wave": canonical_wave,
                        "country": safe(country_series.iloc[row_index]) if len(country_series) else "",
                        "country_code": safe(country_code_series.iloc[row_index]) if len(country_code_series) else "",
                        "row_index": row_index,
                        "survey_year": None
                        if (survey_year_col == "" or pd.isna(survey_year_series.iloc[row_index]))
                        else int(float(survey_year_series.iloc[row_index])),
                        "source_file": str(raw_path),
                        "source_file_sha256": fsha,
                        "load_batch_id": batch,
                        "loaded_at_utc": loaded_at,
                    }
                )
            respondent_fact = pd.DataFrame(respondent_rows)
            inserted = insert_df(con, "respondent_fact", respondent_fact)
            row_report["respondent_fact_rows"] = int(inserted)

            # Respondent-position facts, one column at a time.
            pos_count = 0
            pos_cols = [c for c in df.columns if (src, wave, c) in position_map]
            for col_idx, c in enumerate(pos_cols, start=1):
                info = position_map[(src, wave, c)]
                ser = df[c]
                labmap = labels.get(c, {})
                rows = []
                for row_index, raw in enumerate(ser.tolist()):
                    rv = safe(raw)
                    if not rv:
                        continue
                    canonical = labmap.get(rv, rv)
                    rows.append(
                        {
                            "respondent_uid": respondent_fact.iloc[row_index]["respondent_uid"],
                            "dataset_id": did,
                            "source_family": src,
                            "wave": wave,
                            "position_dimension": info["dimension"],
                            "raw_variable": c,
                            "raw_value": rv,
                            "canonical_value": canonical,
                            "confidence": float(info["confidence"]),
                            "ethical_use_flag": "allowed_structural_position",
                            "load_batch_id": batch,
                        }
                    )
                pos_count += insert_df(con, "respondent_position_fact", pd.DataFrame(rows))
                if col_idx % 25 == 0:
                    log(start, f"dataset {did}: positions {col_idx}/{len(pos_cols)} rows={pos_count}")
            row_report["respondent_position_fact_rows"] = int(pos_count)

            # Survey weights, one column at a time.
            weight_count = 0
            weight_cols = [c for c in df.columns if WEIGHT_RE.search(c)]
            for col_idx, c in enumerate(weight_cols, start=1):
                vals = pd.to_numeric(df[c], errors="coerce")
                rows = []
                for row_index, val in enumerate(vals.tolist()):
                    if pd.isna(val):
                        continue
                    rows.append(
                        {
                            "respondent_uid": respondent_fact.iloc[row_index]["respondent_uid"],
                            "dataset_id": did,
                            "source_family": src,
                            "wave": wave,
                            "weight_type": c,
                            "raw_variable": c,
                            "weight_value": float(val),
                            "load_batch_id": batch,
                        }
                    )
                weight_count += insert_df(con, "survey_weight_fact", pd.DataFrame(rows))
            row_report["survey_weight_fact_rows"] = int(weight_count)

            # Response facts, one column at a time.
            resp_count = 0
            miss_count = 0
            qcols = [c for c in df.columns if (did, c) in question_map]
            for col_idx, c in enumerate(qcols, start=1):
                bind = question_map[(did, c)]
                ser = df[c]
                labmap = labels.get(c, {})
                rows = []
                for row_index, raw in enumerate(ser.tolist()):
                    rv = safe(raw)
                    lab = labmap.get(rv, "")
                    m = missing(rv, lab)
                    if m:
                        miss_count += 1
                        if args.skip_missing_responses:
                            continue
                    rows.append(
                        {
                            "respondent_uid": respondent_fact.iloc[row_index]["respondent_uid"],
                            "dataset_id": did,
                            "source_family": src,
                            "wave": wave,
                            "raw_variable": c,
                            "raw_value": rv,
                            "normalized_value": "" if m else rv,
                            "value_label": lab,
                            "missing_flag": bool(m),
                            "final_driver_id": bind["final_driver_id"],
                            "question_id": bind["question_id"],
                            "question_block_id": bind["question_block_id"],
                            "structural_domain_id": bind["structural_domain_id"],
                            "driver_facet_id": bind["driver_facet_id"],
                            "relation_axis_id": bind["relation_axis_id"],
                            "target_entity_id": bind["target_entity_id"],
                            "question_type": bind["question_type"],
                            "source_match_type": bind["source_match_type"],
                            "load_batch_id": batch,
                        }
                    )
                resp_count += insert_df(con, "response_fact", pd.DataFrame(rows))
                if col_idx % 25 == 0:
                    log(start, f"dataset {did}: responses {col_idx}/{len(qcols)} rows={resp_count} missing={miss_count}")
            row_report["response_fact_rows"] = int(resp_count)
            row_report["missing_response_rows"] = int(miss_count)
            row_report["skipped_unregistered_columns"] = int(len(df.columns) - len(qcols))
            row_report["status"] = "green_loaded"

            con.commit()
            report_rows.append(row_report)
            write_dataset_report(repo, row_report)
            log(
                start,
                f"dataset {idx}/{len(manifest)} {did}: loaded rows={len(df)} resp={resp_count} pos={pos_count} wt={weight_count}",
            )
        except Exception as exc:
            row_report["error"] = repr(exc)
            report_rows.append(row_report)
            write_dataset_report(repo, row_report)
            log(start, f"dataset {idx}/{len(manifest)} {did}: failed {exc!r}")

    reports = repo / "data/ddm_build_copy/reports"
    reports.mkdir(parents=True, exist_ok=True)
    summary = {
        "status": "green_loaded"
        if all(r["status"] in {"green_loaded", "skipped_completed"} for r in report_rows if r["dataset_id"])
        else "partial",
        "load_batch_id": batch,
        "table_counts": {
            t: con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            for t in ["respondent_fact", "respondent_position_fact", "response_fact", "survey_weight_fact"]
        },
        "datasets_attempted": len(report_rows),
        "datasets_loaded": sum(1 for r in report_rows if r["status"] == "green_loaded"),
        "datasets_skipped": sum(1 for r in report_rows if r["status"] == "skipped_completed"),
        "datasets_failed": sum(1 for r in report_rows if r["status"] not in {"green_loaded", "skipped_completed"}),
    }
    (reports / "V542_population_report.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0 if summary["datasets_failed"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
