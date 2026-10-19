"""A41 expected-scope tests: the frozen independent universe is complete."""
from __future__ import annotations


def test_frozen_scope_has_all_35_waves_and_1890_cells(scope):
    assert scope["source_count"] == 35
    assert len(scope["waves"]) == 35
    assert [w["source_id"] for w in scope["waves"]] == [f"SRC{i:02d}" for i in range(1, 36)]
    assert scope["expected_cell_count"] == 1890
    assert len(scope["cells"]) == 1890
    assert scope["expected_source_axis_cells"] == 1050
    assert scope["expected_ee_axis_cells"] == 560
    assert scope["expected_f_axis_cells"] == 280


def test_frozen_scope_axes_are_30_16_8(scope):
    assert scope["axis_counts"] == {"source_native": 30, "ee_engine": 16, "f_gate": 8, "total": 54}
    assert scope["axis_ids"][:3] == ["S01", "S02", "S03"]
    assert scope["axis_ids"][30] == "EE01"
    assert scope["axis_ids"][-1] == "F8"


def test_frozen_scope_carries_151_and_101_and_crosswalk(scope):
    assert scope["register_151_count"] == 151
    assert scope["ledger_101_count"] == 101
    assert len(scope["register_151_ids"]) == 151
    assert len(scope["ledger_101_ids"]) == 101
    cw = scope["crosswalk_151_101"]
    assert cw["is_proved_normalization_theorem"] is False
    assert len(cw["edges"]) == 761
    assert len(cw["unmatched_register_rows"]) == 81
    assert len(cw["unmatched_ledger_rows"]) == 7
    assert cw["split_register_rows"] and cw["merge_ledger_rows"]


def test_frozen_scope_declared_documents_match_preimages(scope, gp):
    for key, rec in scope["declared_documents"].items():
        verified = gp.verify(scope["startup_commit"], rec["path"],
                             expect_blob_sha1=rec["blob_sha1"])
        assert verified["blob_sha1"] == rec["blob_sha1"]


def test_frozen_scope_digest_is_stable(scope):
    import hashlib
    import json
    body = {k: v for k, v in scope.items()
            if k not in ("scope_digest", "freeze_order_discipline")}
    digest = hashlib.sha256(
        json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert digest == scope["scope_digest"]


def test_every_cell_carries_identity_and_expected_u_e_pre(scope):
    for cell in scope["cells"]:
        identity = cell["identity"]
        for facet in ("source", "edition", "item", "response", "risk", "design", "operation"):
            assert facet in identity
        assert cell["expected_u_e_pre"]["expected_u_e_pre_status"] == \
            "UNISSUED_EXPECTED_NOT_INTRINSICALLY_INAPPLICABLE"
        assert cell["expected_u_e_pre"]["issued_eligible_operation_count"] is None
        assert cell["expected_u_e_pre"]["permitted_current_original35_source_rights"] == 0


def test_global_f6_f7_f8_are_global_obligations(scope):
    g = scope["global_relations"]
    assert set(g) == {"cross_family_F6", "temporal_F7", "possibility_F8"}
    for rel in g.values():
        assert "OPEN_GLOBAL_OBLIGATION" in rel["expected_status"]
