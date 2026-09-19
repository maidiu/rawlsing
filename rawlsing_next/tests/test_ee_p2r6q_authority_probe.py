from __future__ import annotations

import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FQRA = ROOT / "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"

def test_probe_wvs7_minimum_projection_authority():
    with FQRA.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        print("FQRA_FIELDS=" + json.dumps(reader.fieldnames, ensure_ascii=False))
        pos = []
        country = []
        pair = []
        for row in reader:
            vals = set(str(v) for v in row.values())
            joined = json.dumps(row, ensure_ascii=False)
            is_wvs7 = ("WVS" in vals or any(str(v).strip()=="WVS" for v in row.values())) and ("W7" in vals or any(str(v).strip()=="W7" for v in row.values()))
            if not is_wvs7:
                continue
            if "POSITION_COORDINATE" in joined:
                keep = {k:v for k,v in row.items() if any(t in k.lower() for t in ("var","question","role","lane","status","text","display","source","wave","manual","authority","unit","position"))}
                pos.append(keep)
            if "country" in joined.lower() or "nation" in joined.lower():
                country.append(row)
            if any(str(v).strip() in {"Q291G5","Q291P5"} for v in row.values()):
                pair.append(row)
    print("WVS7_POSITION_COORDINATES=" + json.dumps(pos, ensure_ascii=False, sort_keys=True))
    print("WVS7_COUNTRY_NATION_ROWS=" + json.dumps(country, ensure_ascii=False, sort_keys=True))
    print("WVS7_PAIR_ROWS=" + json.dumps(pair, ensure_ascii=False, sort_keys=True))
    assert len(pos) == 81
    assert len(pair) == 2
