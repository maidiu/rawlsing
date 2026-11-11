from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
P2X = REPO / "WORKER_RETURNS" / "EE-P2X"
EXPECT = json.loads((P2X / "09_LOCAL_COURT_FROZEN_EXPECTATIONS.json").read_text(encoding="utf-8"))
CONTRACT = json.loads((P2X / "10_LOCAL_COURT_RECEIPT_CONTRACT.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location("ee_p2x_verify", P2X / "12_verify_ee_p2x_local_court.py")
verify = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(verify)

def test_frozen_lock_and_runtime_identities_are_exact():
    assert EXPECT["hq"]["checkpoint_id"] == "20260918T0210-0400"
    assert EXPECT["hq"]["handoff_commit"] == "10c91b1e03285b50cae7a39ab1458826712c52b5"
    assert EXPECT["lock2"]["hash"] == "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
    assert EXPECT["runtime"] == {
        "platform": "Darwin x86_64",
        "python": "3.11.3",
        "pyreadstat": "1.3.6",
        "pyarrow": "25.0.1",
        "darwin_ru_maxrss_unit": "BYTES",
        "same_physical_host_required": True,
    }

def test_wvs_lock2_frontier_is_exact_46_and_canonical():
    xs = EXPECT["lock2"]["candidate_hashes"]
    assert len(xs) == 46
    assert len(set(xs)) == 46
    assert xs == sorted(xs)
    assert EXPECT["lock2"]["family_shape"] == {
        "UNARY_SOCIAL_FORK": 10,
        "PAIR_RESPONSE_COTRAVEL": 1,
        "BRANCH_CONDITIONED_DISTRIBUTION": 10,
        "BOUNDED_K_WAY_RESPONSE_CONFIGURATION": 25,
    }
    assert sum(EXPECT["lock2"]["family_shape"].values()) == 46
    assert len(EXPECT["lock2"]["predicate_hashes"]) == 11
    assert len(EXPECT["lock2"]["query_hashes"]) == 3

def test_lits_governed_learned_product_expectations_are_prebound():
    x = EXPECT["sources"]["LITS_I"]["learned"]
    assert x["candidate_count"] == 50
    assert x["independently_executed_roles"] == 77
    assert x["terminal_counts"] == {"EVALUATED_SUPPORTED":49,"EVALUATED_VALID_EMPTY":1}
    assert x["expected_fresh_product_sha256"] == "47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d"
    assert x["expected_semantic_replay_hash"] == "301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5"

def test_preserved_stage_files_are_exact_and_repetition_forbidden():
    for stage in EXPECT["preserved_completed_stages"].values():
        p = REPO / stage["receipt_path"]
        assert p.exists()
        assert verify.sha256_file(p) == stage["receipt_sha256"]
        assert stage["repetition"] == "FORBIDDEN"

def test_lock1_and_p2r1_seam_git_blobs_are_exact():
    lock1 = REPO / EXPECT["lock1"]["manifest_json_path"]
    seam = REPO / EXPECT["execution_seam"]["path"]
    assert verify.git_blob_sha1(lock1) == EXPECT["lock1"]["manifest_json_git_blob_sha1"]
    assert verify.git_blob_sha1(seam) == EXPECT["execution_seam"]["git_blob_sha1"]

def test_metric_slot_rejects_pending_and_untyped_missing_values():
    with pytest.raises(verify.CourtBlocker):
        verify.validate_metric_slot(
            "bytes_read",
            {"state":"PENDING_LOCAL_DARWIN","value":None,"unit":"UNSET","reason":"pending"},
            False,
        )
    with pytest.raises(verify.CourtBlocker):
        verify.validate_metric_slot(
            "bytes_read",
            {"state":"MEASURED","value":None,"unit":"bytes","reason":None},
            False,
        )

def test_preserved_not_captured_exception_is_cell_bounded():
    slot={"state":"NOT_CAPTURED_PRESERVED_STAGE","value":None,"unit":"count",
          "reason":"Historical repetition-forbidden stage did not capture this metric."}
    verify.validate_metric_slot("source_open_count", slot, True)
    with pytest.raises(verify.CourtBlocker):
        verify.validate_metric_slot("source_open_count", slot, False)

def test_cpu_unavailable_state_is_narrowly_bounded():
    slot={"state":"UNAVAILABLE_ON_HOST_WITH_REASON","value":None,"unit":"ns","reason":"host API unavailable"}
    verify.validate_metric_slot("cpu_user_ns", slot, False)
    with pytest.raises(verify.CourtBlocker):
        verify.validate_metric_slot("bytes_read", slot, False)

def test_contract_contains_no_scalar_or_selection_surface():
    assert CONTRACT["final_verifier"]["pass_terminal"] == "PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE"
    assert CONTRACT["final_verifier"]["never_manufacture_missing_evidence"] is True
    forbidden=set(CONTRACT["final_verifier"]["forbidden_output_keys"])
    assert {"aggregate_score","magic_score","score","ranking","winner","selected_candidate","selection"} <= forbidden

def test_wvs_c_is_preserved_nonblocking_and_never_executable():
    assert EXPECT["wvs_c"] == {
        "required_disposition":"WVS7_C__CURRENT_PORTABILITY_FAILURE",
        "blocks_wvs_a_or_b":False,
        "synthetic_fallback_forbidden":True,
    }
    assert "WVS7/C" not in verify.EXECUTABLE

def test_not_reached_metric_is_legal_only_for_attempted_stopped_cell():
    slot={"state":"NOT_REACHED_AUTHORIZED_STOP","value":None,"unit":"ns",
          "reason":"Stopped by typed candidate-local failure before this stage."}
    verify.validate_metric_slot("audit_wall_ns", slot, False, True)
    with pytest.raises(verify.CourtBlocker):
        verify.validate_metric_slot("audit_wall_ns", slot, False, False)
