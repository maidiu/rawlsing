from __future__ import annotations

import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FQRA = ROOT / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"

def test_exact_accepted_position_coordinate_subset():
    rows = []
    with FQRA.open("r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("source") != "WVS" or row.get("wave") != "W7":
                continue
            if row.get("manual_semantic_role") != "POSITION_COORDINATE":
                continue
            rows.append({
                "var_code": row.get("var_code"),
                "question_id": row.get("question_id"),
                "display_text": row.get("display_text"),
                "manual_question_text": row.get("manual_question_text"),
                "manual_semantic_role": row.get("manual_semantic_role"),
                "manual_semantic_subrole": row.get("manual_semantic_subrole"),
                "manual_position_conditioning": row.get("manual_position_conditioning"),
                "manual_position_modifiers": row.get("manual_position_modifiers"),
                "manual_source_authority": row.get("manual_source_authority"),
                "p2_semantic_role": row.get("p2_semantic_role"),
                "p2_semantic_subrole": row.get("p2_semantic_subrole"),
                "p2_canonical_disposition": row.get("p2_canonical_disposition"),
                "p2_exact_question_text": row.get("p2_exact_question_text"),
                "p2_source_authority": row.get("p2_source_authority"),
                "p2_deep_review_status": row.get("p2_deep_review_status"),
                "p2_response_binding_status": row.get("p2_response_binding_status"),
                "authority_rule_id": row.get("authority_rule_id"),
            })
    countryish = [r for r in rows if any(
        token in json.dumps(r, ensure_ascii=False).lower()
        for token in ("country", "nation", "iso 3166", "geograph", "region", "s003", "s024")
    )]
    raise AssertionError("R6Q_EXACT_POSITION_COORDINATES=" + json.dumps({
        "count": len(rows),
        "countryish": countryish,
        "all": rows,
    }, ensure_ascii=False, sort_keys=True))
