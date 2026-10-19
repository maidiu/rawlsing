from __future__ import annotations
import copy
import pytest
from a42 import core
from frozen_a41.a41.gitpreimage import PreimageError

def _without(receipts, rid):
    return [r for r in receipts if r["receipt_id"] != rid]

def _assess(scope, receipts, w41reg, old):
    return core.assess_v2(scope, receipts, w41reg, old)

def test_a42_a41_identity_cells_present(acc):
    n = sum(1 for c in acc["cells"]
            if c["consumed_grade"] == "DOCUMENTARY_IDENTITY_RECONCILIATION")
    assert n == 70

def test_a42_e41_functional_F1_F4_present(acc):
    fm = acc["functional_maturity"]
    for g in ("F1", "F2", "F3", "F4"):
        assert fm[g]["functional_grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"

def test_a42_w41_retained_cells_present(acc):
    cells = {c["cell_id"]: c for c in acc["cells"]}
    for cid in ("SRC02.S25", "SRC02.S26", "SRC02.F5"):
        assert cells[cid]["consumed_grade"] == "HISTORICAL_RETAINED_EVIDENCE"

def test_a42_p41_F8_present(acc):
    assert acc["functional_maturity"]["F8"]["functional_grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"

def test_a42_input_deletion_e41_drops_F1F4(acc, receipts, scope, w41reg, old_manifest):
    cut = _assess(scope, _without(receipts, "E41-SOURCEFREE-INTEGRATED"), w41reg, old_manifest)
    for g in ("F1", "F2", "F3", "F4"):
        assert cut["functional_maturity"][g]["functional_grade"] is None

def test_a42_input_deletion_w41_drops_retained_cells(acc, receipts, scope, w41reg, old_manifest):
    cut = _assess(scope, _without(receipts, "W41-RETAINED-GT2-J04"), w41reg, old_manifest)
    cells = {c["cell_id"]: c for c in cut["cells"]}
    assert cells["SRC02.S25"]["consumed_grade"] is None
    assert cells["SRC02.S26"]["consumed_grade"] is None
    assert cells["SRC02.F5"]["consumed_grade"] is None

def test_a42_input_deletion_p41_drops_integrated_F8(acc, receipts, scope, w41reg, old_manifest):
    cut = _assess(scope, _without(receipts, "P41-SOURCEFREE-INTEGRATED"), w41reg, old_manifest)
    assert cut["functional_maturity"]["F8"]["functional_grade"] != "SOURCEFREE_INTEGRATED_POSITIVE"

def test_a42_input_deletion_a41_accounting_drops_identity(acc, receipts, scope, w41reg, old_manifest):
    cut = _assess(scope, _without(receipts, "O35B-ORIGINAL35-ACCOUNTING"), w41reg, old_manifest)
    n = sum(1 for c in cut["cells"]
            if c["consumed_grade"] == "DOCUMENTARY_IDENTITY_RECONCILIATION")
    assert n == 0

def test_a42_rejects_test_only_promotion_to_original(scope, bank, gp):
    b = copy.deepcopy(bank)
    t = next(r for r in b["receipts"] if r["receipt_id"] == "E41-SOURCEFREE-INTEGRATED")
    t["grade"] = "ORIGINAL_MEASURED_OCCUPANCY"
    with pytest.raises(PreimageError):
        core.ingest_r41_bank(b, gp, scope)

def test_a42_preserves_f6_unknown_mass(acc):
    r = next(x for x in acc["receipts"] if x["receipt_id"] == "W41-SOURCEFREE-INTEGRATED")
    ub = r["unknown_bounds"]
    assert ub["uncovered_target_mass_W2"] == "1/4"
    assert ub["uncovered_target_mass_W3"] == "1/5"
    assert ub["uncovered_target_mass_W7"] == "1/2"
    assert ub["F6_N9_join"].startswith("HOLD")

def test_a42_preserves_f7_no_measured_pair(acc):
    r = next(x for x in acc["receipts"] if x["receipt_id"] == "W41-SOURCEFREE-INTEGRATED")
    assert r["unknown_bounds"]["measured_pairs"] == []
    assert r["unknown_bounds"]["Ghana_measured_change"] is None
    f7 = [x for x in acc["f1_f8_rows"]
          if x.get("global_relation_name") == "temporal_F7"][0]
    assert f7["cell_status"].startswith("OPEN_GLOBAL_OBLIGATION")

def test_a42_rejects_forged_consumer_and_future_clock(scope, bank, gp):
    b = copy.deepcopy(bank)
    t = next(r for r in b["receipts"] if r["receipt_id"] == "P41-SOURCEFREE-INTEGRATED")
    t["downstream_consumer_read_refs"] = ["forged.consumer"]
    with pytest.raises(PreimageError, match="CONSUMER_REF"):
        core.ingest_r41_bank(b, gp, scope)
    b2 = copy.deepcopy(bank)
    t2 = next(r for r in b2["receipts"] if r["receipt_id"] == "P41-SOURCEFREE-INTEGRATED")
    t2["currentness"] = {"archive_or_current": "CURRENT", "as_of": "2099-01-01T00:00:00-0400"}
    with pytest.raises(PreimageError, match="CLOCK_VIOLATION"):
        core.ingest_r41_bank(b2, gp, scope)

def test_a42_tampered_preimage_refused(scope, bank, gp):
    b = copy.deepcopy(bank)
    t = next(r for r in b["receipts"] if r["receipt_id"] == "E41-SOURCEFREE-INTEGRATED")
    t["artifacts"][0]["blob_sha1"] = "0" * 40
    with pytest.raises(PreimageError):
        core.ingest_r41_bank(b, gp, scope)
