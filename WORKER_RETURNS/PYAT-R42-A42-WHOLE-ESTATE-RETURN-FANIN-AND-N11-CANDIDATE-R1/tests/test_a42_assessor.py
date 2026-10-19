from __future__ import annotations
from a42 import core

def test_n11_not_ready_zero_original(acc):
    v = acc["verdict"]
    assert v["n11_state"] == "N11_NOT_READY"
    assert v["original_measured_occupied_cells"] == 0
    assert v["original_measured_missing_cells"] == 1890
    assert v["can_self_adopt_n11"] is False

def test_retained_cells_are_w41_scoped(acc):
    cells = {c["cell_id"]: c for c in acc["cells"]}
    for cid in ("SRC02.S25","SRC02.S26","SRC02.F5"):
        assert cells[cid]["consumed_grade"] == "HISTORICAL_RETAINED_EVIDENCE"
    # AS2B historical LiTS cells remain
    assert cells["SRC27.S15"]["consumed_grade"] == "HISTORICAL_SCOPE_POSITIVE"
    assert cells["SRC27.S20"]["consumed_grade"] == "HISTORICAL_SCOPE_POSITIVE"

def test_functional_maturity_includes_all_r41_gates(acc):
    fm = acc["functional_maturity"]
    for g in ("F1","F2","F3","F4"):
        assert fm[g]["functional_grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"
    assert fm["F5"]["functional_grade"] == "HISTORICAL_RETAINED_EVIDENCE"
    assert fm["F8"]["functional_grade"] == "SOURCEFREE_INTEGRATED_POSITIVE"
    assert set(acc["verdict"]["functional_evidence_gates"]) == {"F1","F2","F3","F4","F5","F6","F7","F8"}

def test_global_f6_f7_f8_remain_unaccepted(acc):
    v = acc["verdict"]
    assert v["global_relations_open"] == 3 and v["global_relations_closed"] == 0
    for row in acc["f1_f8_rows"]:
        if row.get("source_id") == "GLOBAL":
            assert row["cell_status"].startswith("OPEN_GLOBAL_OBLIGATION")

def test_81_unmatched_are_unresolved_not_invented(acc):
    v = acc["verdict"]
    assert v["unmatched_register_rows"] == 81
    assert v["unmatched_still_unresolved"] == 81
    assert v["unmatched_resolved_by_competent_retirement"] == 0
    assert len(acc["unmatched_register_resolution"]) == 81
    assert all(x["resolution"] == "STILL_MISSING__UNRESOLVED" for x in acc["unmatched_register_resolution"])

def test_283_f_rows(acc):
    assert len(acc["f1_f8_rows"]) == 283
    assert sum(1 for r in acc["f1_f8_rows"] if r.get("source_id") != "GLOBAL") == 280
    assert sum(1 for r in acc["f1_f8_rows"] if r.get("source_id") == "GLOBAL") == 3

def test_delta_preserves_original_zero(acc):
    d = acc["delta"]
    assert d["old_a41_original_measured"] == d["new_a42_original_measured"] == 0
    assert d["no_new_original_occupied_cells"] is True
    assert d["new_missing_expected"] == 1778
