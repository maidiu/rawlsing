#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "authority/active_35wave_question_universe_v1.csv"
AUTH = ROOT / "authority/question_applicability_predicate_authority_v1.json"
FALLBACK = "DO_NOT_INFER_APPLICABILITY_FROM_COLUMN_EXISTENCE_OR_EMPIRICAL_COOCCURRENCE"

def main() -> int:
    d = json.loads(AUTH.read_text())
    rows = d.get("rows", [])
    failures = []
    if d.get("authority_version") != "question_applicability_predicate_authority_v1": failures.append("version")
    if len(rows) != 700: failures.append("coverage_not_700_selected_rows")
    ids = [r.get("applicability_authority_id") for r in rows]
    if len(ids) != len(set(ids)): failures.append("duplicate_authority_ids")
    for i, r in enumerate(rows):
        if r.get("authority_status") not in {"SOURCE_EXPLICIT", "FAIL_CLOSED_UNRESOLVED"}: failures.append(f"row_{i}_invalid_status")
        if not r.get("predicate"): failures.append(f"row_{i}_missing_predicate")
        if r.get("prohibited_fallback") != FALLBACK: failures.append(f"row_{i}_fallback_policy")
        if len(r.get("closure_hash", "")) != 64: failures.append(f"row_{i}_closure_hash")
    print(json.dumps({"status":"PASS" if not failures else "FAIL","rows":len(rows),"failures":failures,"authority_sha256":hashlib.sha256(AUTH.read_bytes()).hexdigest()},indent=2))
    return 0 if not failures else 1

if __name__ == "__main__": sys.exit(main())
