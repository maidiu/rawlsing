"""A41 assessor tests: the whole-estate accounting is coherent and honest."""
from __future__ import annotations


def test_n11_is_not_ready_with_zero_original_occupancy(accounting):
    v = accounting["verdict"]
    assert v["n11_state"] == "N11_NOT_READY"
    assert v["can_self_adopt_n11"] is False
    assert v["original_measured_occupied_cells"] == 0
    assert v["total_cells"] == 1890


def test_grade_tally_is_non_substitutable(accounting):
    t = accounting["grade_tally"]
    assert t.get("ACCOUNTED_IDENTITY_ONLY__NOT_OCCUPIED") == 70
    assert t.get("DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER") == 35
    assert t.get("HISTORICAL_SCOPE_POSITIVE__NOT_CURRENT_OCCUPANCY") == 2
    assert t.get("SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY") == 2
    assert t.get("MISSING_EXPECTED_ORIGINAL_SCIENCE__NOT_INTRINSICALLY_INAPPLICABLE") == 1781
    assert t.get("ORIGINAL_MEASURED_OCCUPANCY") is None
    assert sum(t.values()) == 1890


def test_every_missing_cell_names_an_owner_and_authority(accounting):
    for cell in accounting["cells"]:
        if cell["consumed_grade"] is None:
            m = cell["missing_obligation"]
            assert m["owner"].startswith("COMPETENT_ORIGINAL35")
            assert m["expected_authority"]
            assert m["expected_u_e_pre_status"] == \
                "UNISSUED_EXPECTED_NOT_INTRINSICALLY_INAPPLICABLE"


def test_c11_blocker_covers_all_35_waves_at_release_axis(accounting):
    blocked = [c for c in accounting["cells"]
               if c["consumed_grade"] == "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER"]
    assert len(blocked) == 35
    assert all(c["axis_id"] == "S19" for c in blocked)
    assert {c["source_id"] for c in blocked} == {f"SRC{i:02d}" for i in range(1, 36)}


def test_sourcefree_evidence_never_fills_original_cells(accounting):
    for cell in accounting["cells"]:
        if cell["consumed_grade"] == "SOURCEFREE_LOCAL_POSITIVE":
            assert cell["cell_status"] == "SOURCEFREE_LOCAL_POSITIVE__NOT_ORIGINAL_OCCUPANCY"
        assert cell["cell_status"] != "ORIGINAL_MEASURED_OCCUPANCY"


def test_global_f6_f7_f8_remain_open_and_cannot_be_closed_by_wave_cells(accounting):
    v = accounting["verdict"]
    assert v["global_relations_open"] == 3
    assert v["global_relations_closed"] == 0
    globals_rows = [r for r in accounting["f1_f8_rows"] if r.get("source_id") == "GLOBAL"]
    assert {r["global_relation_name"] for r in globals_rows} == \
        {"cross_family_F6", "temporal_F7", "possibility_F8"}
    for r in globals_rows:
        assert r["local_pass_cannot_close_global"] is True
        assert "UNCLOSED" in r["cell_status"]


def test_per_wave_f6_f7_f8_rows_flag_global_unclosable(accounting):
    f678 = [r for r in accounting["f1_f8_rows"]
            if r["gate_id"] in ("F6", "F7", "F8") and r.get("source_id") != "GLOBAL"]
    assert len(f678) == 105
    assert all(r["local_pass_cannot_close_global"] for r in f678)


def test_f1_f8_matrix_has_280_wave_rows_and_3_global(accounting):
    rows = accounting["f1_f8_rows"]
    assert len(rows) == 283
    assert sum(1 for r in rows if r.get("source_id") != "GLOBAL") == 280
    assert sum(1 for r in rows if r.get("source_id") == "GLOBAL") == 3


def test_crosswalk_retains_unmatched_rows(accounting):
    cw = accounting["crosswalk_151_101"]
    assert cw["is_proved_normalization_theorem"] is False
    assert len(cw["unmatched_register_rows"]) == 81
    assert len(cw["unmatched_ledger_rows"]) == 7


def test_receipt_summary_records_all_kinds(accounting):
    kinds = {r["occupancy_kind"] for r in accounting["receipt_summary"]}
    assert "ORIGINAL_MEASURED_OCCUPANCY" not in kinds
    assert {"SOURCEFREE_LOCAL_POSITIVE", "DOCUMENTARY_IDENTITY_RECONCILIATION",
            "HISTORICAL_SCOPE_POSITIVE", "DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER"} <= kinds
