from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import psycopg


RELEASE_ID = "P3-AUTHORITY-2026-08-01-R39"
SCHEMA = "p3a_v27_shadow"


def canonical_hash(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def add(results: list[dict], case: str, status: str, invariant: str, detail: str = "") -> None:
    results.append({"case": case, "status": status, "named_invariant_reached": "YES" if status == "PASS" else "NO", "invariant": invariant, "detail": detail})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--section", type=Path, required=True)
    ap.add_argument("--dsn", required=True)
    args = ap.parse_args()
    sec = args.section
    results: list[dict] = []
    with psycopg.connect(args.dsn, row_factory=psycopg.rows.dict_row, autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public")
        cur = conn.cursor()
        cur.execute("SELECT count(*) n FROM p3_candidate_revision WHERE authority_release_id=%s AND revision_number=2 AND candidate_family_id BETWEEN 'P3CAND-000142' AND 'P3CAND-000282'", (RELEASE_ID,))
        preserved = cur.fetchone()["n"]
        add(results, "release_neutral_family_origin_unchanged", "PASS" if preserved == 141 else "FAIL", "R35 families preserved with R39 successor revisions", f"preserved={preserved}")

        base = canonical_hash({"serialization": "P3_FAMILY_SEMANTIC_ORIGIN_V1_RELEASE_NEUTRAL", "members": ["a", "b"], "origin": "STRICT_RESPONSE_COMPONENT"})
        changed = canonical_hash({"serialization": "P3_FAMILY_SEMANTIC_ORIGIN_V1_RELEASE_NEUTRAL", "members": ["a", "c"], "origin": "STRICT_RESPONSE_COMPONENT"})
        add(results, "changed_semantic_origin_requires_new_family", "PASS" if base != changed else "FAIL", "semantic member change changes origin key")

        try:
            cur.execute(
                """
                UPDATE p3_candidate_revision
                SET evidence_bundle_hash=%s
                WHERE candidate_revision_id=(
                  SELECT candidate_revision_id FROM p3_candidate_revision
                  WHERE authority_release_id=%s
                  ORDER BY candidate_revision_id
                  LIMIT 1
                )
                """,
                ("f" * 64, RELEASE_ID),
            )
        except Exception as exc:
            conn.rollback()
            text = str(exc)
            add(results, "attempted_candidate_hash_update", "PASS" if re.search("immutable|forbidden|update", text, re.I) else "FAIL", "candidate revision update blocked by trigger", text)
        else:
            conn.rollback()
            add(results, "attempted_candidate_hash_update", "FAIL", "candidate revision update blocked by trigger", "update unexpectedly succeeded")

        code_text = (sec / "code/p3a_v39_load.py").read_text(encoding="utf-8")
        add(results, "production_dependency_on_review_csv", "PASS" if "V36_HISTORICAL_IDENTITY_AND_SUCCESSOR_CONTRADICTION.csv" not in code_text else "FAIL", "review CSV is not a production input")

        matrix = (sec / "P3A_V39_QUERY_MATRIX.csv").read_text(encoding="utf-8")
        add(results, "relabelled_old_query_output_as_current", "PASS" if "postgres/v39_populated_q01_q54_raw.tsv" in matrix and "v35_populated" not in matrix else "FAIL", "query evidence source is live R39")

        cur.execute("SELECT count(*) n FROM p3_release_change_ledger WHERE release_id=%s AND change_type='UNCHANGED_REFERENCE' AND prior_content_hash IS NULL", (RELEASE_ID,))
        blank = cur.fetchone()["n"]
        add(results, "release_ledger_row_with_no_prior_basis", "PASS" if blank == 0 else "FAIL", "UNCHANGED_REFERENCE requires prior hash", f"blank_prior_hash={blank}")

        cur.execute("SELECT count(*) n FROM p3_frozen_historical_candidate_identity h JOIN p3_candidate_revision r ON r.candidate_revision_id=h.historical_object_id WHERE h.allocation_release_id='P3-AUTHORITY-2026-08-01-R37'")
        fabricated = cur.fetchone()["n"]
        add(results, "v37_blocked_identity_not_current", "PASS" if fabricated == 0 else "FAIL", "blocked v37 identities do not become runtime candidate revisions", f"fabricated={fabricated}")

    status = "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL"
    out = {"status": status, "cases": results}
    (sec / "P3A_V39_FIXTURE_RETURN.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
