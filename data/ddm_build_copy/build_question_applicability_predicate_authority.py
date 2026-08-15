#!/usr/bin/env python3
"""Compile fail-closed, provenance-bearing applicability authority."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
UNIVERSE = ROOT / "authority/active_35wave_question_universe_v1.csv"
OUT = ROOT / "authority/question_applicability_predicate_authority_v1.json"
VERSION = "question_applicability_predicate_authority_v1"
FALLBACK = "DO_NOT_INFER_APPLICABILITY_FROM_COLUMN_EXISTENCE_OR_EMPIRICAL_COOCCURRENCE"


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def main():
    df = pd.read_csv(UNIVERSE, dtype=str).fillna("")
    rows = []
    source_hash = hashlib.sha256(UNIVERSE.read_bytes()).hexdigest()
    for r in df.to_dict("records"):
        key = f"{r['source_family']}::{r['canonical_wave']}::{r['country_code_scope']}::{r['var_code']}"
        row = {
            "applicability_authority_id": "QAPA35V1::" + hashlib.sha256(key.encode()).hexdigest()[:24],
            "source_family": r["source_family"],
            "wave": r["canonical_wave"],
            "country_module_scope": r["country_code_scope"],
            "question_implementation_id": key,
            "source_variable_code": r["var_code"],
            "applicability_class": "EXPLICIT_UNKNOWN_UNRESOLVED",
            "predicate": {"operator": "UNRESOLVED", "subject": "respondent", "scope": r["country_code_scope"]},
            "parent_or_gating_question_ids": [],
            "permitted_respondent_universe": "UNKNOWN",
            "authority_status": "FAIL_CLOSED_UNRESOLVED",
            "source_authority_path": str(UNIVERSE),
            "source_sha256": source_hash,
            "source_locator": f"row_payload_hash={r['row_payload_hash']}",
            "supporting_excerpt_or_rule": "No source-native executable routing predicate was asserted by the active authority row.",
            "unresolved_reason": "SOURCE_NATIVE_APPLICABILITY_PREDICATE_NOT_COMPILED",
            "prohibited_fallback": FALLBACK,
        }
        row["closure_hash"] = digest(row)
        rows.append(row)
    payload = {"authority_version": VERSION, "source_question_universe": str(UNIVERSE), "source_question_universe_sha256": source_hash, "row_count": len(rows), "rows": rows}
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "row_count": len(rows), "authority_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(), "authority_status": "FAIL_CLOSED_UNRESOLVED_UNTIL_SOURCE_PREDICATE_EVIDENCE_IS_COMPILED"}, indent=2))


if __name__ == "__main__":
    main()
