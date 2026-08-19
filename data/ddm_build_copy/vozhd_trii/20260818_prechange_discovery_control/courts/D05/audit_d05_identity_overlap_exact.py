#!/usr/bin/env python3
"""D05 exact respondent identity and complete question-pair cotravel audit.

This pass makes two requirements impossible to water down:
1. respondent surrogate identity/collision checks are first-class output;
2. QUESTION_OVERLAP_SUMMARY.csv contains every unordered pair of populated
   questions in each source/wave/country, INCLUDING ZERO-OVERLAP PAIRS.

Zero overlap is physical routing/module evidence and may not disappear merely
because an inner join cannot emit it.

Database access is REPEATABLE READ, READ ONLY. No DDL/DML.
"""
from __future__ import annotations

import csv
import json
import os
import subprocess
from pathlib import Path
from typing import Any

import psycopg2

COURT = Path("data/ddm_build_copy/vozhd_trii/20260818_prechange_discovery_control/courts/D05")
BRANCH = "agent/vozhd-trii-d05-empirical-substrate"

IDENTITY_FIELDS = [
    "scope_type", "source", "wave", "country_code", "respondent_rows",
    "distinct_respondent_ids", "null_respondent_ids", "duplicate_id_groups",
    "duplicate_id_excess_rows", "ids_in_multiple_source_waves",
    "ids_in_multiple_countries", "ids_in_multiple_survey_years",
    "response_rows", "orphan_response_rows", "status"
]
OVERLAP_FIELDS = [
    "source", "wave", "country_code", "question_x", "question_y",
    "respondents_x", "respondents_y", "respondents_overlap",
    "respondents_union", "overlap_pct_of_x", "overlap_pct_of_y",
    "jaccard_pct", "respondents_overlap_unique_each", "cotravel_possible",
    "duplicate_compromised_overlap"
]
FAIL_FIELDS = ["failure_code", "severity", "scope", "message"]


def root() -> Path:
    value = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return Path(value)


def branch(repo: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def qrows(conn, query: str, params=None) -> list[dict[str, Any]]:
    with conn.cursor() as cur:
        cur.execute(query, params)
        names = [d.name if hasattr(d, "name") else d[0] for d in cur.description]
        return [dict(zip(names, row)) for row in cur.fetchall()]


def identity_rows(conn) -> list[dict[str, Any]]:
    global_row = qrows(conn, """
      WITH idg AS (
        SELECT id,
               COUNT(*)::bigint n,
               COUNT(DISTINCT (source, COALESCE(wave,'')))::bigint source_waves,
               COUNT(DISTINCT COALESCE(country_code,''))::bigint countries,
               COUNT(DISTINCT survey_year)::bigint years
        FROM public.survey_microdata_respondents
        GROUP BY id
      ), rc AS (
        SELECT COUNT(*)::bigint response_rows,
               COUNT(*) FILTER (WHERE r.id IS NULL)::bigint orphan_response_rows
        FROM public.survey_microdata_responses x
        LEFT JOIN public.survey_microdata_respondents r ON r.id=x.respondent_id
      )
      SELECT 'GLOBAL'::text scope_type,''::text source,''::text wave,''::text country_code,
             COUNT(*)::bigint respondent_rows,
             COUNT(DISTINCT r.id)::bigint distinct_respondent_ids,
             COUNT(*) FILTER (WHERE r.id IS NULL)::bigint null_respondent_ids,
             (SELECT COUNT(*) FROM idg WHERE n>1)::bigint duplicate_id_groups,
             (SELECT COALESCE(SUM(n-1),0) FROM idg WHERE n>1)::bigint duplicate_id_excess_rows,
             (SELECT COUNT(*) FROM idg WHERE source_waves>1)::bigint ids_in_multiple_source_waves,
             (SELECT COUNT(*) FROM idg WHERE countries>1)::bigint ids_in_multiple_countries,
             (SELECT COUNT(*) FROM idg WHERE years>1)::bigint ids_in_multiple_survey_years,
             rc.response_rows,rc.orphan_response_rows
      FROM public.survey_microdata_respondents r CROSS JOIN rc
      GROUP BY rc.response_rows,rc.orphan_response_rows
    """)[0]

    # Compute scoped duplicate counts from one row per scoped respondent ID.
    # This avoids multiplying duplicate metrics by joining duplicate respondent
    # rows back to their own grouped counts.
    scoped = qrows(conn, """
      WITH g AS (
        SELECT source,COALESCE(wave,'') wave,COALESCE(country_code,'') country_code,
               id,COUNT(*)::bigint n
        FROM public.survey_microdata_respondents
        GROUP BY 1,2,3,4
      ), resp AS (
        SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,
               COUNT(x.*)::bigint response_rows
        FROM public.survey_microdata_respondents r
        LEFT JOIN public.survey_microdata_responses x ON x.respondent_id=r.id
        GROUP BY 1,2,3
      )
      SELECT 'SOURCE_WAVE_COUNTRY'::text scope_type,
             g.source,g.wave,g.country_code,
             SUM(g.n)::bigint respondent_rows,
             COUNT(*)::bigint distinct_respondent_ids,
             COUNT(*) FILTER (WHERE g.id IS NULL)::bigint null_respondent_ids,
             COUNT(*) FILTER (WHERE g.n>1)::bigint duplicate_id_groups,
             COALESCE(SUM(g.n-1) FILTER (WHERE g.n>1),0)::bigint duplicate_id_excess_rows,
             0::bigint ids_in_multiple_source_waves,
             0::bigint ids_in_multiple_countries,
             0::bigint ids_in_multiple_survey_years,
             COALESCE(MAX(resp.response_rows),0)::bigint response_rows,
             0::bigint orphan_response_rows
      FROM g
      LEFT JOIN resp USING(source,wave,country_code)
      GROUP BY 1,2,3,4 ORDER BY 2,3,4
    """)

    output = [global_row] + scoped
    bad_fields = [
        "null_respondent_ids", "duplicate_id_groups",
        "ids_in_multiple_source_waves", "ids_in_multiple_countries",
        "ids_in_multiple_survey_years", "orphan_response_rows"
    ]
    for row in output:
        row["status"] = (
            "IDENTITY_FAILURE"
            if any(int(row.get(field) or 0) > 0 for field in bad_fields)
            else "OK"
        )
    return output


def stream_complete_overlap(conn, path: Path) -> tuple[int, int]:
    """Write all unordered question pairs, including zero-overlap pairs."""
    query = """
      WITH rq AS (
        SELECT r.source,COALESCE(r.wave,'') wave,COALESCE(r.country_code,'') country_code,
               resp.respondent_id,UPPER(COALESCE(resp.var_code,'')) var_code,
               COUNT(*)::bigint n_rows
        FROM public.survey_microdata_responses resp
        JOIN public.survey_microdata_respondents r ON r.id=resp.respondent_id
        WHERE COALESCE(resp.var_code,'')<>''
        GROUP BY 1,2,3,4,5
      ), t AS (
        SELECT source,wave,country_code,var_code,COUNT(*)::bigint n
        FROM rq GROUP BY 1,2,3,4
      ), pairs AS (
        SELECT x.source,x.wave,x.country_code,
               x.var_code question_x,y.var_code question_y,
               x.n respondents_x,y.n respondents_y
        FROM t x JOIN t y
          ON y.source=x.source AND y.wave=x.wave AND y.country_code=x.country_code
         AND y.var_code>x.var_code
      ), ov AS (
        SELECT x.source,x.wave,x.country_code,
               x.var_code question_x,y.var_code question_y,
               COUNT(*)::bigint respondents_overlap,
               COUNT(*) FILTER (WHERE x.n_rows=1 AND y.n_rows=1)::bigint respondents_overlap_unique_each,
               COUNT(*) FILTER (WHERE x.n_rows>1 OR y.n_rows>1)::bigint duplicate_compromised_overlap
        FROM rq x JOIN rq y
          ON y.source=x.source AND y.wave=x.wave AND y.country_code=x.country_code
         AND y.respondent_id=x.respondent_id AND y.var_code>x.var_code
        GROUP BY 1,2,3,4,5
      )
      SELECT p.source,p.wave,p.country_code,p.question_x,p.question_y,
             p.respondents_x,p.respondents_y,
             COALESCE(o.respondents_overlap,0)::bigint respondents_overlap,
             (p.respondents_x+p.respondents_y-COALESCE(o.respondents_overlap,0))::bigint respondents_union,
             CASE WHEN p.respondents_x>0
                  THEN ROUND(100.0*COALESCE(o.respondents_overlap,0)/p.respondents_x,6) ELSE 0 END overlap_pct_of_x,
             CASE WHEN p.respondents_y>0
                  THEN ROUND(100.0*COALESCE(o.respondents_overlap,0)/p.respondents_y,6) ELSE 0 END overlap_pct_of_y,
             CASE WHEN (p.respondents_x+p.respondents_y-COALESCE(o.respondents_overlap,0))>0
                  THEN ROUND(100.0*COALESCE(o.respondents_overlap,0)/(p.respondents_x+p.respondents_y-COALESCE(o.respondents_overlap,0)),6)
                  ELSE 0 END jaccard_pct,
             COALESCE(o.respondents_overlap_unique_each,0)::bigint respondents_overlap_unique_each,
             (COALESCE(o.respondents_overlap,0)>0) cotravel_possible,
             COALESCE(o.duplicate_compromised_overlap,0)::bigint duplicate_compromised_overlap
      FROM pairs p LEFT JOIN ov o
        ON (o.source,o.wave,o.country_code,o.question_x,o.question_y)=
           (p.source,p.wave,p.country_code,p.question_x,p.question_y)
      ORDER BY 1,2,3,4,5
    """
    pair_count = 0
    zero_count = 0
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(OVERLAP_FIELDS)
        cur = conn.cursor(name="d05_complete_overlap_stream")
        cur.itersize = 10000
        cur.execute(query)
        for row in cur:
            pair_count += 1
            if int(row[7]) == 0:
                zero_count += 1
            writer.writerow(row)
        cur.close()
    return pair_count, zero_count


def main() -> int:
    repo = root()
    out = repo / COURT
    failures: list[dict[str, str]] = []
    observed_branch = branch(repo)
    if observed_branch != BRANCH:
        failures.append({
            "failure_code": "D05_E_WRONG_BRANCH", "severity": "FATAL",
            "scope": "repository", "message": f"expected {BRANCH}; found {observed_branch}"
        })

    db = os.getenv("DATABASE_URL", "")
    if not db:
        failures.append({
            "failure_code": "D05_E_DATABASE_URL_MISSING", "severity": "FATAL",
            "scope": "database", "message": "DATABASE_URL absent"
        })
        write_csv(out / "IDENTITY_OVERLAP_FAILURES.csv", FAIL_FIELDS, failures)
        return 10

    conn = None
    try:
        conn = psycopg2.connect(db)
        conn.set_session(readonly=True, autocommit=False, isolation_level="REPEATABLE READ")
        read_only = qrows(conn, "SHOW transaction_read_only")[0]["transaction_read_only"]
        if str(read_only).lower() != "on":
            raise RuntimeError("D05_E_NOT_READ_ONLY")

        ids = identity_rows(conn)
        write_csv(out / "RESPONDENT_IDENTITY_AUDIT.csv", IDENTITY_FIELDS, ids)
        pair_count, zero_count = stream_complete_overlap(conn, out / "QUESTION_OVERLAP_SUMMARY.csv")

        if ids[0]["status"] != "OK":
            failures.append({
                "failure_code": "D05_F_RESPONDENT_IDENTITY", "severity": "FATAL",
                "scope": "GLOBAL",
                "message": "respondent identity/collision invariant failed; inspect RESPONDENT_IDENTITY_AUDIT.csv"
            })

        (out / "QUESTION_OVERLAP_COMPLETENESS.json").write_text(
            json.dumps({
                "unordered_question_pairs_emitted": pair_count,
                "zero_overlap_pairs_emitted": zero_count,
                "zero_overlap_pairs_are_retained": True,
                "query_semantics": "all populated var pairs per source/wave/country; left join same-respondent overlap"
            }, indent=2, sort_keys=True) + "\n",
            encoding="utf-8"
        )
        write_csv(out / "IDENTITY_OVERLAP_FAILURES.csv", FAIL_FIELDS, failures)
        conn.rollback()
        return 15 if any(item["severity"] == "FATAL" for item in failures) else 0
    except Exception as exc:
        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass
        failures.append({
            "failure_code": "D05_E_IDENTITY_OVERLAP_QUERY_FAILED", "severity": "FATAL",
            "scope": "runtime", "message": f"{type(exc).__name__}: {exc}"
        })
        write_csv(out / "IDENTITY_OVERLAP_FAILURES.csv", FAIL_FIELDS, failures)
        return 15


if __name__ == "__main__":
    raise SystemExit(main())
