from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def _rows(name):
    with (ROOT/name).open(encoding="utf-8") as h:
        return list(csv.DictReader(h))

def test_exact_positive_membership_and_order():
    rows=_rows("04_POSITIVE_CONFIGURATION_MEMBER_LEDGER.csv")
    south=[r["var_code"] for r in rows if r["source_family"]=="South Asia"]
    lits=[r["var_code"] for r in rows if r["source_family"]=="LiTS"]
    assert south==["c13f","c13h"]
    assert lits==["q301_1","q301_8","q301_11"]

def test_no_product_scope_promotion():
    rows=_rows("04_POSITIVE_CONFIGURATION_MEMBER_LEDGER.csv")
    assert all(r["product_variant_status"]=="BLOCKED_ROUTING_MEMBER_APPLICABILITY" for r in rows)

def test_raw_frontier_is_not_laundered_into_local_rows():
    rows=_rows("05_DENOMINATOR_AND_DEPENDENCY_LEDGER.csv")
    r=next(x for x in rows if x["ledger_id"]=="B09-D01")
    assert r["exact_known_state"]=="2499 structures / 15990 memberships"
    assert r["disposition"]=="BLOCKED_ROW_IDENTITIES_NOT_MATERIALIZED_ON_B09_START"

def test_archive08_remains_quarantined():
    rows=_rows("05_DENOMINATOR_AND_DEPENDENCY_LEDGER.csv")
    r=next(x for x in rows if x["ledger_id"]=="B09-D08")
    assert r["disposition"]=="QUARANTINED_NON_AUTHORITATIVE"
