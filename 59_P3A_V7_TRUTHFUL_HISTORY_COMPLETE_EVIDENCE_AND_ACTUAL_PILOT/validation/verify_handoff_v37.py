from pathlib import Path
import csv
import json
import subprocess
import sys

import psycopg


ROOT = Path(sys.argv[1]).resolve()
SEC = ROOT / "59_P3A_V7_TRUTHFUL_HISTORY_COMPLETE_EVIDENCE_AND_ACTUAL_PILOT"
DSN = sys.argv[2]
RELEASE = "P3-AUTHORITY-2026-08-01-R37"
fail = []


def load_json(rel):
    p = SEC / rel
    if not p.exists():
        fail.append(f"missing {rel}")
        return {}
    return json.loads(p.read_text())


def load_rows(rel):
    p = SEC / rel
    if not p.exists():
        fail.append(f"missing {rel}")
        return []
    return list(csv.DictReader(p.open()))


def db_rows(cur, sql, args=()):
    cur.execute(sql, args)
    return [dict(r) for r in cur.fetchall()]


required = [
    "P3A_V37_HISTORICAL_IDENTITY_IMPORT.csv",
    "P3A_V37_HISTORICAL_EVIDENCE_STATUS.csv",
    "P3A_V37_FAMILY_ORIGIN_COMPARISON.csv",
    "P3A_V37_FAMILY_AND_REVISION_GENEALOGY.csv",
    "P3A_V37_RELEASE_CHANGE_LEDGER.csv",
    "P3A_V37_ALL_CANDIDATE_HASH_RECONCILIATION.csv",
    "P3A_V37_TYPED_CONSTRAINT_SCHEMA_RETURN.json",
    "P3A_V37_PILOT_STRATA_ELIGIBILITY.csv",
    "P3A_V37_PILOT_CANDIDATE_STRATA.csv",
    "P3A_V37_PILOT_PACKET_COVERAGE.csv",
    "P3A_V37_FIXTURE_RETURN.json",
    "P3A_V37_QUERY_MATRIX.csv",
    "P3A_V37_OBJECT_COUNTS.json",
    "outputs/P3A_V37_TYPED_CONSTRAINT_MUTATION_RETURN.json",
]
for rel in required:
    if not (SEC / rel).exists():
        fail.append(f"missing {rel}")

audit = {r["r35_candidate_family_id"]: r for r in load_rows("V36_HISTORICAL_IDENTITY_AND_SUCCESSOR_CONTRADICTION.csv")}
with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row) as conn:
    conn.execute("SET search_path TO p3a_v27_shadow, public")
    cur = conn.cursor()
    hist = db_rows(cur, "SELECT * FROM p3_frozen_historical_candidate_identity ORDER BY historical_identity_id")
    if len(hist) != 564:
        fail.append("frozen historical identity count not 564")
    for h in hist:
        if h["allocation_release_id"] == "P3-AUTHORITY-2026-08-01-R35":
            prior = audit[h["historical_family_id"] or h["historical_object_id"]]
            if h["evidence_status"] != "EXACT_PRIOR_ARTIFACT":
                fail.append("R35 historical identity is not exact prior artifact")
            if h["origin_key"] != prior["r35_actual_origin_key"] or h["evidence_bundle_hash"] != prior["r35_actual_evidence_bundle_hash"]:
                fail.append(f"R35 historical values mismatch {h['historical_identity_id']}")
        if h["allocation_release_id"] == "P3-AUTHORITY-2026-08-01-R31":
            if h["evidence_status"] != "IDENTITY_ONLY_NO_HASH_AUTHORITY" or h["origin_key"] is not None or h["evidence_bundle_hash"] is not None:
                fail.append("R31 identity-only row is not explicit unknown")
    revs = db_rows(cur, "SELECT * FROM p3_candidate_revision WHERE authority_release_id=%s ORDER BY candidate_revision_id", (RELEASE,))
    if len(revs) != 141 or revs[0]["candidate_revision_id"] != "P3CANDREV-000283-R0001" or revs[-1]["candidate_revision_id"] != "P3CANDREV-000423-R0001":
        fail.append("R37 candidate revision range/count mismatch")
    if any(r["revision_number"] != 1 for r in revs):
        fail.append("R37 Branch B revisions are not all R0001")
    genealogy = db_rows(cur, "SELECT * FROM p3_candidate_revision_genealogy WHERE authority_release_id=%s", (RELEASE,))
    if len(genealogy) != 141 or any(g["genealogy_branch"] != "CHANGED_ORIGIN_NEW_FAMILY" or g["predecessor_source"] != "FROZEN_HISTORY" for g in genealogy):
        fail.append("genealogy rows do not prove Branch B frozen predecessor mapping")
    ledger_count = db_rows(cur, "SELECT count(*) n FROM p3_release_change_ledger WHERE release_id=%s", (RELEASE,))[0]["n"]
    if ledger_count < 141:
        fail.append("release change ledger is not populated")
    bad_base = db_rows(cur, """
      SELECT count(*) n FROM p3_candidate_revision cr
      LEFT JOIN (SELECT candidate_revision_id,count(*) n FROM p3_candidate_component_link GROUP BY 1) cl USING(candidate_revision_id)
      LEFT JOIN (SELECT candidate_revision_id,count(*) n FROM p3_candidate_attachment_projection GROUP BY 1) ap USING(candidate_revision_id)
      WHERE cr.authority_release_id=%s AND cr.candidate_origin_type IN ('STRICT_RESPONSE_COMPONENT','PROPOSITION_ONLY_SEED')
        AND (coalesce(cl.n,0)<>1 OR coalesce(ap.n,0)<>0)
    """, (RELEASE,))[0]["n"]
    if bad_base != 0:
        fail.append("malformed current base candidates exist")

sys.path.insert(0, str(SEC / "code"))
sys.path.insert(0, str(SEC / "validation"))
from p3a_v37_packets import build_packet

with psycopg.connect(DSN, row_factory=psycopg.rows.dict_row, autocommit=False) as conn:
    conn.execute("SET search_path TO p3a_v27_shadow, public")
    cur = conn.cursor()
    for i, row in enumerate(db_rows(cur, "SELECT candidate_revision_id,evidence_bundle_hash FROM p3_candidate_revision WHERE authority_release_id=%s ORDER BY candidate_revision_id", (RELEASE,)), 1):
        _, _, h = build_packet(cur, row["candidate_revision_id"], i, update_db_hash=False)
        if h != row["evidence_bundle_hash"]:
            fail.append(f"candidate hash mismatch {row['candidate_revision_id']}")
            break
    conn.rollback()

packet_return = load_json("outputs/p3a_v37_packet_build_return.json")
if packet_return.get("status") != "PASS":
    fail.append("packet build return not PASS")
selected = {r["candidate_revision_id"] for r in packet_return.get("pilot", {}).get("index", [])}
packeted = {r["candidate_revision_id"] for r in packet_return.get("packets", [])}
if selected != packeted:
    fail.append("pilot selected set does not equal packeted set")
if len(packeted) > 40:
    fail.append("pilot packet count exceeds 40")
for v in packet_return.get("packets", []):
    if v.get("returncode") != 0:
        fail.append(f"packet validator failed {v.get('candidate_revision_id')}")

typed = load_json("outputs/P3A_V37_TYPED_CONSTRAINT_MUTATION_RETURN.json")
if typed.get("status") != "PASS" or typed.get("returncode") == 0:
    fail.append("stripped typed redirect mutation did not fail")

fixture = load_json("P3A_V37_FIXTURE_RETURN.json")
if fixture.get("status") != "PASS":
    fail.append("fixture return not PASS")
for r in fixture.get("results", []):
    if r.get("case") == "mutation_stale_evidence_hash" and "evidence bundle hash does not recompute" not in (r.get("stdout", "") + r.get("stderr", "")):
        fail.append("stale hash fixture did not reach hash invariant")
teardown = (SEC / "postgres/v37_fixture_teardown_check.txt").read_text() if (SEC / "postgres/v37_fixture_teardown_check.txt").exists() else ""
if "does not exist" not in teardown:
    fail.append("fixture database teardown not proven")

qfails = sorted(r["query_or_gate"] for r in load_rows("P3A_V37_QUERY_MATRIX.csv") if r.get("status") == "FAIL")
if qfails != ["q01b_postpromotion_pointer", "q15b_no_unadjudicated_at_p3_close"]:
    fail.append(f"unexpected query failures {qfails}")

print(json.dumps({"status": "FAIL" if fail else "PASS", "failures": fail}, indent=2))
sys.exit(1 if fail else 0)
