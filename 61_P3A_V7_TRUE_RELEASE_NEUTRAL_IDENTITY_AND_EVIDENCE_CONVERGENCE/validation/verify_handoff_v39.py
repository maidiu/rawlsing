from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R39"
SCHEMA = "p3a_v27_shadow"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--section", type=Path, required=True)
    ap.add_argument("--dsn", required=True)
    args = ap.parse_args()
    sec = args.section
    failures: list[str] = []
    def expect(label: str, ok: bool) -> None:
        if not ok:
            failures.append(label)

    code = (sec / "code/p3a_v39_load.py").read_text(encoding="utf-8")
    expect("review CSV remains production dependency", "V36_HISTORICAL_IDENTITY_AND_SUCCESSOR_CONTRADICTION.csv" not in code)
    expect("finalize-hashes update path remains", "UPDATE p3_candidate_revision SET evidence_bundle_hash" not in (sec / "code/p3a_v39_packets.py").read_text(encoding="utf-8"))
    expect("candidate revision immutable trigger missing", "p3_candidate_revision_immutable" in (sec / "sql/p3_postgresql_compatible_ddl_v7_v39.sql").read_text(encoding="utf-8"))

    with psycopg.connect(args.dsn, row_factory=psycopg.rows.dict_row) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        def one(sql: str, params=()) -> int:
            cur.execute(sql, params)
            return int(cur.fetchone()["n"])
        expect("R39 successor revision count", one("SELECT count(*) n FROM p3_candidate_revision WHERE authority_release_id=%s", (RELEASE_ID,)) == 141)
        expect("R39 did not append to R35 family namespace", one("SELECT count(*) n FROM p3_candidate_revision WHERE authority_release_id=%s AND revision_number=2 AND candidate_family_id BETWEEN 'P3CAND-000142' AND 'P3CAND-000282'", (RELEASE_ID,)) == 141)
        expect("v37 blocked identities not frozen", one("SELECT count(*) n FROM p3_frozen_historical_candidate_identity WHERE allocation_release_id='P3-AUTHORITY-2026-08-01-R37'") == 282)
        expect("v37 blocked identities became revisions", one("SELECT count(*) n FROM p3_frozen_historical_candidate_identity h JOIN p3_candidate_revision r ON r.candidate_revision_id=h.historical_object_id WHERE h.allocation_release_id='P3-AUTHORITY-2026-08-01-R37'") == 0)
        expect("semantic family origins missing", one("SELECT count(*) n FROM p3_candidate_family_semantic_origin WHERE authority_release_id=%s", (RELEASE_ID,)) == 141)
        expect("release ledger missing", one("SELECT count(*) n FROM p3_release_change_ledger WHERE release_id=%s", (RELEASE_ID,)) > 0)
        expect("bad unchanged reference ledger rows", one("SELECT count(*) n FROM p3_release_change_ledger WHERE release_id=%s AND change_type='UNCHANGED_REFERENCE' AND prior_content_hash IS NULL", (RELEASE_ID,)) == 0)

    qrows = rows(sec / "P3A_V39_QUERY_MATRIX.csv")
    expect("query matrix not live R39", qrows and all(r["source"] == "postgres/v39_populated_q01_q54_raw.tsv" for r in qrows))
    proxy = {r["stratum"]: r for r in rows(sec / "P3A_V39_PILOT_STRATA_ELIGIBILITY.csv")}
    expect("exact-only proxy still selected", proxy.get("exact_only_authority", {}).get("selected_count") == "0")
    expect("precedence proxy still selected", proxy.get("precedence_overlap_conflict", {}).get("selected_count") == "0")
    fixture = json.loads((sec / "P3A_V39_FIXTURE_RETURN.json").read_text(encoding="utf-8"))
    expect("fixture failure", fixture.get("status") == "PASS")
    packet_return = json.loads((sec / "outputs/p3a_v39_packet_build_return.json").read_text(encoding="utf-8"))
    expect("packet build failure", packet_return.get("status") == "PASS" and len(packet_return.get("packets", [])) == 4)

    out = {"status": "PASS" if not failures else "FAIL", "failures": failures}
    (sec / "outputs/verify_handoff_v39_return.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
