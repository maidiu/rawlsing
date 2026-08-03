from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SQL = ROOT / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK/sql/P3_DDL_VALIDATION_QUERIES_v7.sql"


def q17_statement() -> str:
    text = SQL.read_text(encoding="utf-8")
    match = re.search(r"SELECT CASE .*? AS q17_candidate_event_contiguous .*?;", text)
    assert match, "q17 statement not found"
    return match.group(0)


def psql(sql: str) -> str:
    env = {**os.environ, "PGOPTIONS": "-c search_path=pg_temp,p3a_v27_shadow,public"}
    cmd = [
        "psql",
        "-h",
        "127.0.0.1",
        "-p",
        "55432",
        "-U",
        "rawlsing_p3a_owner",
        "-d",
        "rawlsing_p3a_v27_test",
        "-v",
        "ON_ERROR_STOP=1",
        "-At",
        "-c",
        sql,
    ]
    lines = subprocess.run(
        cmd, check=True, text=True, capture_output=True, env=env
    ).stdout.splitlines()
    return lines[-1].strip()


def test_q17_projects_and_groups_by_candidate_revision_id():
    stmt = q17_statement()
    assert "SELECT candidate_revision_id,MIN(event_ordinal)" in stmt
    assert "GROUP BY candidate_revision_id" in stmt
    assert "SELECT candidate_family_id,MIN(event_ordinal)" not in stmt
    assert "GROUP BY candidate_family_id" not in stmt


def test_q17_empty_state_passes():
    sql = "CREATE TEMP TABLE p3_candidate_status_event(candidate_family_id text, candidate_revision_id text, event_ordinal int); " + q17_statement()
    assert psql(sql) == "PASS"


def test_q17_two_revisions_same_family_each_contiguous_pass():
    sql = """
    CREATE TEMP TABLE p3_candidate_status_event(candidate_family_id text, candidate_revision_id text, event_ordinal int);
    INSERT INTO p3_candidate_status_event VALUES
      ('P3CAND-000001','P3CANDREV-000001-R0001',1),
      ('P3CAND-000001','P3CANDREV-000001-R0001',2),
      ('P3CAND-000001','P3CANDREV-000001-R0002',1),
      ('P3CAND-000001','P3CANDREV-000001-R0002',2);
    """ + q17_statement()
    assert psql(sql) == "PASS"


def test_q17_one_revision_with_gap_fails():
    sql = """
    CREATE TEMP TABLE p3_candidate_status_event(candidate_family_id text, candidate_revision_id text, event_ordinal int);
    INSERT INTO p3_candidate_status_event VALUES
      ('P3CAND-000001','P3CANDREV-000001-R0001',1),
      ('P3CAND-000001','P3CANDREV-000001-R0001',3);
    """ + q17_statement()
    assert psql(sql) == "FAIL"


def test_q17_cross_revision_gap_is_not_hidden_by_family_grouping():
    sql = """
    CREATE TEMP TABLE p3_candidate_status_event(candidate_family_id text, candidate_revision_id text, event_ordinal int);
    INSERT INTO p3_candidate_status_event VALUES
      ('P3CAND-000001','P3CANDREV-000001-R0001',1),
      ('P3CAND-000001','P3CANDREV-000001-R0001',3),
      ('P3CAND-000001','P3CANDREV-000001-R0002',1),
      ('P3CAND-000001','P3CANDREV-000001-R0002',2);
    """ + q17_statement()
    assert psql(sql) == "FAIL"
