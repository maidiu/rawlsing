from __future__ import annotations

import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FQRA = ROOT / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
RET = ROOT / "WORKER_RETURNS/EE-P2R6Q"
TERMINAL = "EE_P2R6Q_BLOCK__WVS7_CURRENT_SURVEY_COUNTRY_POSITION_COORDINATE_AUTHORITY_ABSENT"


def _j(name):
    return json.loads((RET / name).read_text(encoding="utf-8"))


def _wvs7_rows():
    with FQRA.open("r", encoding="utf-8-sig", newline="") as fh:
        return [r for r in csv.DictReader(fh) if r.get("source") == "WVS" and r.get("wave") == "W7"]


def test_exact_position_count_and_current_country_role():
    rows = _wvs7_rows()
    positions = [r for r in rows if r.get("manual_semantic_role") == "POSITION_COORDINATE"]
    assert len(positions) == 81
    b = [r for r in rows if r.get("var_code") == "B_COUNTRY"]
    assert len(b) == 1
    b = b[0]
    assert b["question_id"] == "WVS:W7:B_COUNTRY"
    assert b["p2_exact_question_text"] == "ISO 3166-1 numeric country code"
    assert b["manual_semantic_role"] == "ADMINISTRATIVE_METADATA"
    assert b["p2_semantic_role"] == "ADMINISTRATIVE_METADATA"
    assert b["p2_canonical_disposition"] == "STRUCTURAL_CONTEXT"
    assert not any(r.get("var_code") == "B_COUNTRY" for r in positions)
    assert not any(r.get("p2_exact_question_text") == "ISO 3166-1 numeric country code" for r in positions)


def test_nearest_position_coordinate_is_subnational_not_direct_country():
    rows = _wvs7_rows()
    n = [r for r in rows if r.get("var_code") == "N_REGION_ISO"]
    assert len(n) == 1
    n = n[0]
    assert n["manual_semantic_role"] == "POSITION_COORDINATE"
    assert n["p2_canonical_disposition"] == "POSITION_COORDINATE"
    assert n["p2_exact_question_text"] == "Region ISO 3166-2"
    assert n["p2_exact_question_text"] != "ISO 3166-1 numeric country code"


def test_governed_block_and_full_independent_field_audit():
    reduction = _j("01_MINIMUM_COORDINATE_REQUIREMENT_REDUCTION.json")
    adjudication = _j("02_FQRA_TO_C11_COORDINATE_OWNERSHIP_ADJUDICATION.json")
    assert reduction["terminal"] == TERMINAL
    assert adjudication["terminal"] == TERMINAL
    assert reduction["coordinate_authority_identity"] is None
    assert reduction["coordinate_slot_identity"] is None
    assert reduction["projection_identity"] is None
    audit = adjudication["independent_projection_field_audit"]
    assert audit["universes"].startswith("CLOSED")
    assert audit["respondents"].startswith("CLOSED")
    assert audit["questions"].startswith("CLOSED")
    assert audit["coordinate_slots"].startswith("BLOCKED")
    assert audit["weight_slots"] == "CLOSED__EMPTY_RAW_UNWEIGHTED"
    assert audit["projection_identity_ref"].startswith("NOT_ISSUED")


def test_invalid_b_country_materializer_is_removed():
    assert not (RET / "08_WVS7_FROZEN_P2_PROJECTION_MATERIALIZER.py").exists()
    assert not (RET / "03_COORDINATE_SEMANTICS_AUTHORITY.json").exists()
    assert not (RET / "04_GOVERNED_COORDINATE_SLOT_PREIMAGE.json").exists()
    assert not (RET / "05_COMPLETE_WVS7_FROZEN_P2_PROJECTION_AUTHORITY.json").exists()
    assert not (RET / "06_PROJECTION_BINDING_RECEIPT.json").exists()
    assert not (RET / "07_PROJECTION_NEGATIVE_COURT.json").exists()
