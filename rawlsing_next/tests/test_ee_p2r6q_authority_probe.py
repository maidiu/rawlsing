from __future__ import annotations

import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FQRA = ROOT / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
COORD = ROOT / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/CANONICAL_COORDINATE_REGISTRY_FINAL_R1.csv"

def _wvs7(row):
    vals = {str(v).strip() for v in row.values()}
    return "WVS" in vals and "W7" in vals

def _trim(row):
    keep = {}
    for k, v in row.items():
        lk = k.lower()
        if any(t in lk for t in ("var", "question", "role", "lane", "status", "text", "display", "source", "wave", "manual", "authority", "unit", "position", "coordinate", "country", "target")):
            keep[k] = v
    return keep

def test_probe_wvs7_minimum_projection_authority():
    payload = {}
    with FQRA.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        payload["fqra_fields"] = reader.fieldnames
        pos, country, pair = [], [], []
        for row in reader:
            if not _wvs7(row):
                continue
            joined = json.dumps(row, ensure_ascii=False)
            if "POSITION_COORDINATE" in joined:
                pos.append(_trim(row))
            if "country" in joined.lower() or "nation" in joined.lower():
                country.append(_trim(row))
            if any(str(v).strip() in {"Q291G5", "Q291P5"} for v in row.values()):
                pair.append(_trim(row))
        payload["position_count"] = len(pos)
        payload["position_rows"] = pos
        payload["country_nation_rows"] = country
        payload["pair_rows"] = pair
    with COORD.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        payload["coord_fields"] = reader.fieldnames
        rows = []
        for row in reader:
            joined = json.dumps(row, ensure_ascii=False)
            if ("country" in joined.lower() or "nation" in joined.lower()) and ("WVS" in joined and ("W7" in joined or "Wave 7" in joined)):
                rows.append(_trim(row))
        payload["coord_country_nation_rows"] = rows
    raise AssertionError("R6Q_AUTHORITY_PROBE=" + json.dumps(payload, ensure_ascii=False, sort_keys=True))
