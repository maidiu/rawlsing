from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R40"
SCHEMA = "p3a_v27_shadow"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", type=Path, required=True)
    ap.add_argument("--dsn", required=True)
    args = ap.parse_args()
    sec = args.section
    failures: list[str] = []

    def expect(label: str, ok: bool) -> None:
        if not ok:
            failures.append(label)

    with psycopg.connect(args.dsn, row_factory=psycopg.rows.dict_row) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()

        def one(sql: str) -> int:
            cur.execute(sql)
            return int(cur.fetchone()["n"])

        expect("current candidate revisions", one(f"SELECT count(*) n FROM p3_candidate_revision WHERE authority_release_id='{RELEASE_ID}'") == 141)
        expect("snapshots", one(f"SELECT count(*) n FROM p3_candidate_evidence_snapshot WHERE authority_release_id='{RELEASE_ID}'") == 141)
        expect("promoted stages", one(f"SELECT count(*) n FROM p3a_build_stage.candidate_evidence_bundle WHERE authority_release_id='{RELEASE_ID}' AND stage_status='PROMOTED'") == 141)
        expect("stage authority leakage", one("SELECT count(*) n FROM p3_object_registry WHERE object_id LIKE 'P3A-V40-BUILD-RUN%'") == 0)
        expect("status events", one(f"SELECT count(*) n FROM p3_candidate_revision_current_stage WHERE authority_release_id='{RELEASE_ID}'") == 141)
        expect("snapshot mismatch", one(f"SELECT count(*) n FROM p3_candidate_revision r JOIN p3_candidate_evidence_snapshot s USING(candidate_revision_id) WHERE r.authority_release_id='{RELEASE_ID}' AND r.evidence_bundle_hash<>s.evidence_bundle_hash") == 0)

    convergence = rows(sec / "P3A_V40_DATABASE_PACKET_HASH_CONVERGENCE.csv")
    expect("packet convergence", convergence and all(r["all_hashes_match"] == "YES" for r in convergence))
    q = rows(sec / "P3A_V40_QUERY_MATRIX.csv")
    applicable_failures = [r["query_or_gate"] for r in q if r["status"] == "FAIL" and r["query_or_gate"] not in {"q01b_postpromotion_pointer", "q15b_no_unadjudicated_at_p3_close"}]
    expect("applicable query failures", not applicable_failures)
    fixture = json.loads((sec / "P3A_V40_FIXTURE_RETURN.json").read_text(encoding="utf-8"))
    expect("fixture return", fixture.get("status") == "PASS")
    packet_return = json.loads((sec / "outputs/p3a_v40_packet_build_return.json").read_text(encoding="utf-8"))
    expect("packet build return", packet_return.get("status") == "PASS")

    out = {"status": "PASS" if not failures else "FAIL", "failures": failures}
    (sec / "outputs/verify_handoff_v40_return.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
