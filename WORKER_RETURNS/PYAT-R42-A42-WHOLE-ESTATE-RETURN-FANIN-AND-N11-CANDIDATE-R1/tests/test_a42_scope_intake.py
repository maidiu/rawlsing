from __future__ import annotations
from a42 import core

def test_scope_is_full_declared_estate(scope):
    assert scope["source_count"] == 35 and len(scope["cells"]) == 1890
    assert scope["register_151_count"] == 151 and scope["ledger_101_count"] == 101
    assert len(scope["crosswalk_151_101"]["edges"]) == 761
    assert len(scope["crosswalk_151_101"]["unmatched_register_rows"]) == 81

def test_a41_frozen_source_reverifies(scope, gp):
    rec = scope["_a41_scope_preimage"]
    assert rec["commit"] == core.A41_COMMIT
    assert rec["blob_sha1"]

def test_all_13_receipts_are_preimage_verified(receipts):
    assert len(receipts) == 13
    ids = {r["receipt_id"] for r in receipts}
    for rid in ("E41-SOURCEFREE-INTEGRATED","W41-RETAINED-GT2-J04",
                "W41-SOURCEFREE-INTEGRATED","P41-SOURCEFREE-INTEGRATED"):
        assert rid in ids

def test_r41_grades_are_exact(receipts):
    g = {r["receipt_id"]: r["grade"] for r in receipts}
    assert g["E41-SOURCEFREE-INTEGRATED"] == "SOURCEFREE_INTEGRATED_POSITIVE"
    assert g["W41-RETAINED-GT2-J04"] == "HISTORICAL_RETAINED_EVIDENCE"
    assert g["P41-SOURCEFREE-INTEGRATED"] == "SOURCEFREE_INTEGRATED_POSITIVE"
    assert g["E04L-SOURCEFREE-READTHROUGH"] == "INDEPENDENTLY_ACCEPTED_SOURCEFREE"
    assert g["F6P-SOURCEFREE-PARTIAL-BOUND"] == "INDEPENDENTLY_ACCEPTED_SOURCEFREE"
    assert "ORIGINAL_MEASURED_OCCUPANCY" not in g.values()

def test_w41_register_has_all_35(gp):
    reg = core.load_w41_register(gp)
    assert len(reg) == 35
    assert reg["SRC02"]["F5"].startswith("ONLY_EXACT_SCOPED_RETAINED")
