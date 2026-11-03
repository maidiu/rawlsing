"""Independent review assertions over the reviewer-owned F6 evidence.

Read-only with respect to the candidate.  These tests assert the reviewer's
measured receipts, not the candidate's self-authored labels.
"""
from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path

R = Path(__file__).resolve().parent
E = json.loads((R / "evidence/replay_f6_review.json").read_text())


def test_01_exact_pins_and_candidate_scope():
    p = E["pins"]
    assert p["all_pins_match"] is True
    assert p["actual"]["wp2_blob"] == "55e567e4d0780c251bf949268d3d477abdc76a9b"
    assert p["actual"]["f6p_consumer_blob"] == "8fa992899293f454d7abded36831a4b4a362df8e"
    assert p["actual"]["f6m_candidate_blob"] == "2df811d76db258d98d89ffb43c830cb221ff9a7d"
    assert p["actual"]["f6m_corrected_A_blob"] == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
    assert p["actual"]["f6m_A0_blob"] == "182cc7970d7624f6614015f5a51d0602e1630d52"
    assert p["actual"]["independent_test_blob"] == "3b42b05e7d1de6a1046c22e532dc77827cb2f9c6"
    assert p["run0_equals_run1"] is True
    assert all(path.startswith("WORKER_RETURNS/PDEV01-F6-COMPARISON/")
               for path in p["candidate_commit_scope"] if path)


def test_02_w1_point_matches_frozen_oracle():
    r = E["replay"]["W1_full_coverage_disjoint"]
    assert r["summary"]["evidence_state"] == "SUPPORTED_SYNTHESIS"
    assert r["summary"]["uncovered_target_mass"] == "0"
    assert r["summary"]["supported_point"] == {"formal": "5/8", "informal": "3/8"}
    assert r["checks"]["bounds"]["all_lower_le_upper"] is True
    assert r["checks"]["bounds"]["covered_inside_bounds"] is True


def test_03_partial_worlds_preserve_mass_and_refuse_points():
    expected = {
        "W2_mixed_eligibility_trap": "1/4",
        "W7_source_excluded_all_strata": "1/2",
        "W3_minority_whole_stratum_absent": "1/5",
    }
    for world, uncovered in expected.items():
        r = E["replay"][world]
        assert r["summary"]["evidence_state"] == "PARTIAL_IDENTIFICATION"
        assert r["summary"]["uncovered_target_mass"] == uncovered
        assert r["summary"]["supported_point"] is None
        covered = sum(Q(v) for v in r["summary"]["covered_subprobability"].values())
        assert covered + Q(uncovered) == 1
        assert r["checks"]["bounds"]["all_lower_le_upper"] is True
        assert r["checks"]["bounds"]["covered_inside_bounds"] is True
        assert r["checks"]["bounds"]["bias_widens_base"] is True


def test_04_wp2_boundary_is_raw_keyerror_not_authored_type():
    b = E["wp2_boundary"]
    raw = b["raw_observation"]
    authored = b["authored_diagnostic"]
    assert raw["exception_type"] == "KeyError"
    assert raw["exception_args"] == ["native_bundle"]
    assert raw["exception_str"] == "'native_bundle'"
    assert raw["first_missing_field"] == "native_bundle"
    assert raw["f6p_supplies_native_bundle"] is False
    assert raw["f6p_supplies_native_conditional_consumer"] is False
    assert authored["code"] == "F6P_EVIDENCE_NOT_F6M_NATIVE_BUNDLE_SIDECAR"
    assert authored["emitted_by_wp2"] is False
    assert authored["emitted_by_f6p"] is False
    assert authored["authored_in_candidate_run_comparison"] is True
    assert authored["classification"] == "COMPARISON_LOCAL_LABEL_NOT_RECEIVER_TYPED_REFUSAL"


def test_05_exact_tree_has_no_current_f6p_receiver_but_no_global_claim():
    s = E["scope_scan"]
    assert s["scope"] == "EXACT_TREE_ONLY"
    assert s["no_rawlsing_next_f6p_terms"] is True
    assert s["wp2_is_candidate_stage_only"] is True
    assert s["n9_f6_schema_reference"] is False
    assert s["n9_f6_import_reference"] is False
    assert s["guard_returns_guard_only"] is True
    assert s["guard_has_f6_schema"] is False
    assert s["successor_elsewhere_claim"].startswith("NOT_MADE")


def test_06_semantics_match_candidate_but_output_hash_is_root_sensitive():
    for world, row in E["candidate_summary_comparison"].items():
        assert row["semantic_summary_equal"] is True, world
        assert row["path_only_difference"] is True, world
        assert row["output_hash_equal"] is False, world
    assert E["verdict_inputs"]["candidate_output_hash_is_root_sensitive"] is True


def test_07_f6c_invariance_is_supported_by_pinned_historical_outputs_not_just_receipt():
    f = E["f6c_historical_receiver_outputs"]
    assert f["commit"] == "c1ebe091fa2bd12b254e5599cf37975fe438d462"
    assert f["receipt_contains_output_bodies"] is False
    assert f["receipt_names_output_paths"] is True
    assert f["nonparent_consumer_invariant"] is True
    assert f["generic_without_f6_sidecars_invariant"] is True
    assert f["actual_c1_returns_invariant"] is True
    assert f["cases_invariant"] is True
    assert f["f6_sidecars_differ_by_method_variant"] is True
    assert f["wp2_code_edited"] is False
