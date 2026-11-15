"""Focused checks for the phase-A selected reuse ledger."""
from __future__ import annotations

import json
from pathlib import Path

R = Path(__file__).resolve().parent
L = json.loads((R / "01_SELECTED_REUSE_LEDGER.json").read_text())
P = json.loads((R / "03_IMPORT_PROBE.json").read_text())
PASSPORT = json.loads((R / "PASSPORT.json").read_text())


def test_01_s39_s47_selected_sources_are_exact():
    current = L["current_s39_s47"]
    assert current["all_exact"] is True
    assert len(current["selected_functions"]) == 24
    assert all(e["source_exact"] is True for e in current["selected_functions"])
    assert all(e["source_sha256"] == e["installed_sha256"]
               for e in current["selected_functions"])
    assert all(e["source_commit"] for e in current["selected_functions"])
    assert all(e["git_blob"] for e in current["selected_functions"])


def test_02_s47_chain_and_p2_first_reader_import():
    mro = P["s47_mro"]
    assert P["s47_contains_s39_s47"] is True
    assert mro[:9] == [
        "S47Session", "S46Session", "S45Session", "S44Session",
        "S43Session", "S42Session", "S41Session", "S40GeneratedSession",
        "S39GeneratedSession",
    ]
    assert P["p2_product_fanin_import"] == "OK"
    assert P["session_started"] is False
    assert P["model_called"] is False
    assert P["respondent_data_read"] is False
    assert L["consumer_binding"]["first_reader_compatibility"] == "PASS_SCOPED_START_VERIFY"


def test_03_original_v3_exactness_is_held_not_claimed():
    orig = L["original_v3"]
    assert orig["all_exact"] is False
    assert orig["decision"] == "HOLD_ORIGINAL_V3_EXACT_BYTES_AND_DEPENDENCY_CLOSURE"
    by_key = {e["key"]: e for e in orig["selected_functions"]}
    assert by_key["M01-BACKBONE"]["actual_local"]["actual_sha256"] != by_key["M01-BACKBONE"]["expected_source"]
    assert by_key["M25-RUN-ONE"]["actual_local"]["actual_sha256"] != by_key["M25-RUN-ONE"]["expected_source"]
    assert by_key["M25-RUN-N"]["actual_local"]["exact_file"] is True
    assert by_key["M26-DERIVED"]["actual_local"]["exact_file"] is True
    assert by_key["M21-PRESSURE-FLOW"]["actual_local"]["actual_sha256"] is None
    assert by_key["M01-YEAR-RECORD"]["actual_local"]["actual_sha256"] is None
    assert by_key["M30-PERSONA-SHEET"]["actual_local"]["exact_file"] is False
    assert by_key["M30-IDENTITY-INIT"]["actual_local"]["exact_file"] is False
    assert all(e["current_consumer"] == "NONE_PROVEN_AT_PREMAIN"
               for e in orig["selected_functions"])
    assert orig["adapter"] is None


def test_04_original_v3_compatibility_import_is_bounded_and_incomplete():
    imports = P["v3_compatibility_imports"]
    assert imports["v3.core.state"]["status"] == "IMPORT_OK"
    assert imports["v3.engine.yearly_step"]["status"] == "IMPORT_OK"
    assert imports["v3.engine.step_runner"]["status"] == "IMPORT_OK"
    assert imports["v3.core.derived"]["status"] == "IMPORT_OK"
    assert imports["v3.engine.llm_contract"]["status"] == "IMPORT_OK"
    assert imports["v3.render.phenomenology"]["status"] == "IMPORT_OK"
    assert imports["v3.psyche.flow"]["status"] == "IMPORT_FAILED"
    assert imports["v3.core.year_record"]["status"] == "IMPORT_FAILED"


def test_05_p2_consumer_and_interval_owner_are_present(tmp_path):
    p2_methods = P["p2_product_fanin_methods"]
    for name in ("start", "open", "admit_later_event", "read_later_event",
                 "public_opportunity", "do_help", "say", "attend", "status",
                 "current_interval_state"):
        assert name in p2_methods
    keys = {e["key"] for e in L["current_p2"]["selected_functions"]}
    assert {"P2-FANIN", "P2-LATER-ADMIT", "P2-LATER-READ", "P2-INTERVAL"} <= keys
    assert L["consumer_binding"]["runtime_started"] is True
    assert L["consumer_binding"]["first_reader_compatibility"] == "PASS_SCOPED_START_VERIFY"
    assert L["consumer_binding"]["first_reader_smoke"]["status"] == "STARTED_VERIFIED_CLOSED"
    assert L["consumer_binding"]["first_reader_smoke"]["verify"]["ok"] is True
    assert L["consumer_binding"]["first_reader_smoke"]["state_removed"] is True

    # Retained receipts establish the earlier cut; this invocation must also
    # reach the actual accepted owner and its current verification reader.
    import sys
    sys.path.insert(0, str(R.parent / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
    from developmental_recursion.p2_owner import load_p2
    with load_p2().start(tmp_path / "live-owner") as fanin:
        live = fanin.verify_public()
        assert live["ok"] is True
        assert live["event_count"] >= 1
        assert fanin.root_hash


def test_06_architecture_and_source_archive_identity_are_explicit():
    arch = L["architecture"]
    assert arch["commit"] == "fbfc529230d8b3c13f824cfac31741a5dfaa57e5"
    assert arch["blob_sha1"] == "1a888b6a0eaa3d74e0a8afed715b4cd20785a5b2"
    assert arch["status"] == "USER_SETTLED__IMPLEMENTATION_NOT_VERIFIED"
    src = L["source_retrieval"]
    assert src["architecture_commit"] == "commit"
    assert src["s50_commit"] == "commit"
    assert src["w1c_commit"] == "commit"
    assert src["rcf_a_commit"] == "commit"
    assert src["source_archive"]["staging_root_present"] is False
    assert src["source_archive"]["zip_present"] is False
    assert src["source_archive"]["status"] == "EXACT_ARCHIVE_BYTES_UNAVAILABLE__CURRENT_V3_COMPATIBILITY_FALLBACK_PRESENT"
    assert src["source_archive"]["observed_sha256_from_rcf_a"] == "3f2c5ed925273153a4f300f75e54524729f0b4fef9974957be1f3cd887c91289"


def test_07_s50_projection_is_exact_code_but_not_current_consumer():
    s50 = L["s50"]
    assert s50["source_commit"] == "515b9a8ee45672c97051df4efef679117a679525"
    assert s50["source_exact"] is True
    assert "S50Session.materialize_legacy_projection" in s50["symbol"]
    assert s50["adapter_or_hold"] == "HOLD_EXACT_ARCHIVE_AND_ACTUAL_ROOT_STATE"
    assert "NONE_PROVEN" in s50["compatible_current_consumer"]


def test_08_no_adapter_no_native_or_production_crossing():
    assert L["original_v3"]["adapter"] is None
    assert L["current_s39_s47"]["adapter"] is None
    assert L["current_p2"]["adapter"] is None
    for key in (
        "original_v3_native_claim", "source_archive_read", "session_started",
        "model_called", "respondent_rows_read", "production_config_edited",
        "new_engine_or_scheduler", "new_psychological_rule", "adapter_emitted",
        "frozen_output_substituted", "merge", "ci",
    ):
        assert L["limits"][key] is False
    assert PASSPORT["quota"] == "UNKNOWN"
    assert PASSPORT["sanitized"] is True
    assert PASSPORT["model"] == "deepseek-v4.1-flash#max"
    assert PASSPORT["effort"] == "MAX"
