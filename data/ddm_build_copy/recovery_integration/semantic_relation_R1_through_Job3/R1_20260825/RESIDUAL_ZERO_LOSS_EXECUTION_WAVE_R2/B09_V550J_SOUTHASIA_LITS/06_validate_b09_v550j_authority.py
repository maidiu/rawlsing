#!/usr/bin/env python3
from __future__ import annotations
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POS = ROOT / "04_POSITIVE_CONFIGURATION_MEMBER_LEDGER.csv"
BLK = ROOT / "05_DENOMINATOR_AND_DEPENDENCY_LEDGER.csv"

EXPECTED = {
    ("South Asia","JCFG-SOUTH-ASIA-W1-INSTITUTION-TRUST"): [
        (1,"c13f","army_trust"),
        (2,"c13h","parliament_trust"),
    ],
    ("LiTS","JCFG-LITS-2006-TRANSITION-EVALUATION"): [
        (1,"q301_1","economy_vs_1989_evaluation"),
        (2,"q301_8","children_future_evaluation"),
        (3,"q301_11","corruption_vs_1989_evaluation"),
    ],
}

def main() -> int:
    rows=list(csv.DictReader(POS.open(encoding="utf-8")))
    grouped={}
    for r in rows:
        key=(r["source_family"],r["joint_configuration_id"])
        grouped.setdefault(key,[]).append((int(r["item_order"]),r["var_code"],r["item_role"]))
        assert r["configuration_status"]=="GOVERNED_BOUNDED_CANARY_ONLY"
        assert r["product_variant_status"]=="BLOCKED_ROUTING_MEMBER_APPLICABILITY"
    assert grouped==EXPECTED, (grouped, EXPECTED)

    blockers=list(csv.DictReader(BLK.open(encoding="utf-8")))
    ids={r["ledger_id"] for r in blockers}
    assert ids=={f"B09-D{i:02d}" for i in range(1,11)}
    global_row=next(r for r in blockers if r["ledger_id"]=="B09-D01")
    assert global_row["exact_known_state"]=="2499 structures / 15990 memberships"
    assert global_row["disposition"]=="BLOCKED_ROW_IDENTITIES_NOT_MATERIALIZED_ON_B09_START"
    assert any(r["disposition"]=="QUARANTINED_NON_AUTHORITATIVE" for r in blockers)
    assert sum(r["disposition"]=="GOVERNED_BOUNDED_CANARY_ONLY" for r in blockers)==2

    out={
      "status":"PASS_FAIL_CLOSED_SERIALIZATION_VALIDATION",
      "positive_configurations":2,
      "positive_members":len(rows),
      "denominator_dependency_rows":len(blockers),
      "product_complete_authority":False,
      "archive08_promoted":False,
      "routing_sibling_results_consumed":False,
    }
    print(json.dumps(out,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
