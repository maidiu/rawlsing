"""F6P frozen A/B/C method oracle: corrected S03FO, repaired F6M, no-pooling C."""
from __future__ import annotations

import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from f6p_fixtures import MODULES, build, request  # noqa: E402

import f6c_method_c as MC  # noqa: E402
import f6c_oracle_worlds as OW  # noqa: E402
import f6p_partial_bound_evidence_consumer as C  # noqa: E402

A = MODULES["A"]
B = MODULES["B"]


def _cond(mod, bundle, world):
    conditions, outcome = OW.CONSUMER_REQUEST[world]
    return mod.conditional(bundle, dict(conditions), outcome)


def _c_bounds(world):
    return MC.nopooling_bounds(*OW.WORLD_BUILDERS[world]())


def test_w1_ab_invariance_and_c_no_pooling_bounds():
    ba = build("A", "W1_full_coverage_disjoint")
    bb = build("B", "W1_full_coverage_disjoint")
    ca = _cond(A, ba, "W1_full_coverage_disjoint")
    cb = _cond(B, bb, "W1_full_coverage_disjoint")
    assert ca["probabilities"] == cb["probabilities"] == {"formal": "5/8", "informal": "3/8"}
    assert ba["candidate"]["uncovered_target_mass"] == "0"
    assert bb["candidate"]["uncovered_target_mass"] == "0"
    c = _c_bounds("W1_full_coverage_disjoint")
    assert c["total_unknown_mass"] == "1"
    assert c["joint_status"] == "NOT_IDENTIFIED_NO_POOLING_NO_TRANSPORT_PERMISSION"
    assert c["target_marginal_bounds_employment_position"] == {
        "formal": {"lower": "0", "upper": "1"},
        "informal": {"lower": "0", "upper": "1"}}


def test_w2_a_full_coverage_b_partial_c_bounds():
    ba = build("A", "W2_mixed_eligibility_trap")
    bb = build("B", "W2_mixed_eligibility_trap")
    assert ba["candidate"]["uncovered_target_mass"] == "0"
    assert ba["candidate"]["distribution"] is not None
    ca = _cond(A, ba, "W2_mixed_eligibility_trap")
    assert ca["probabilities"] == {"formal": "7/10", "informal": "3/10"}
    assert bb["candidate"]["uncovered_target_mass"] == "1/4"
    assert bb["candidate"]["distribution"] is None
    assert bb["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    c = _c_bounds("W2_mixed_eligibility_trap")
    assert c["total_unknown_mass"] == "1"
    assert c["joint_status"] == "NOT_IDENTIFIED_NO_POOLING_NO_TRANSPORT_PERMISSION"
    ra = C.consume_f6m_evidence(ba, request("W2_mixed_eligibility_trap"))
    rb = C.consume_f6m_evidence(bb, request("W2_mixed_eligibility_trap"))
    assert ra["evidence_state"] == C.FALSE_FULL
    assert rb["evidence_state"] == C.PARTIAL
    assert rb["uncovered_target_mass"] == "1/4"
    assert rb["supported_point"] is None


def test_w7_a_full_coverage_b_partial():
    ba = build("A", "W7_source_excluded_all_strata")
    bb = build("B", "W7_source_excluded_all_strata")
    assert ba["candidate"]["uncovered_target_mass"] == "0"
    ca = _cond(A, ba, "W7_source_excluded_all_strata")
    assert ca["probabilities"] == {"formal": "3/5", "informal": "2/5"}
    assert bb["candidate"]["uncovered_target_mass"] == "1/2"
    assert bb["candidate"]["distribution"] is None
    assert bb["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    c = _c_bounds("W7_source_excluded_all_strata")
    assert c["total_unknown_mass"] == "1"
    ra = C.consume_f6m_evidence(ba, request("W7_source_excluded_all_strata"))
    rb = C.consume_f6m_evidence(bb, request("W7_source_excluded_all_strata"))
    assert ra["evidence_state"] == C.FALSE_FULL
    assert rb["evidence_state"] == C.PARTIAL
    assert rb["supported_point"] is None


def test_w3_a_mislabels_b_names_exclusions():
    ba = build("A", "W3_minority_whole_stratum_absent")
    bb = build("B", "W3_minority_whole_stratum_absent")
    assert ba["candidate"]["uncovered_target_mass"] == "1/5"
    assert ba["candidate"]["distribution"] is None
    assert ba["decision"] == "SYNTHETIC_CANDIDATE"
    assert bb["candidate"]["uncovered_target_mass"] == "1/5"
    assert bb["decision"] == "PARTIAL_IDENTIFICATION_ONLY"
    ra = C.consume_f6m_evidence(ba, request("W3_minority_whole_stratum_absent"))
    rb = C.consume_f6m_evidence(bb, request("W3_minority_whole_stratum_absent"))
    assert ra["evidence_state"] == C.INCONSISTENT
    assert rb["evidence_state"] == C.PARTIAL
    assert {e["source_id"] for e in rb["exclusions"]} == {"S_A", "S_B"}
    assert {e["reason"] for e in rb["exclusions"]} == {"NO_SOURCE_STRATUM"}


def test_c_bounds_are_not_points_and_f6m_bounds_are_partial():
    for world in ("W1_full_coverage_disjoint", "W2_mixed_eligibility_trap",
                  "W7_source_excluded_all_strata"):
        c = _c_bounds(world)
        assert c["total_unknown_mass"] == "1"
        for bound in c["target_marginal_bounds_employment_position"].values():
            assert bound == {"lower": "0", "upper": "1"}
    rb = C.consume_f6m_evidence(build("B", "W2_mixed_eligibility_trap"),
                                request("W2_mixed_eligibility_trap"))
    assert rb["supported_point"] is None
    assert rb["bounds"]
    for bound in rb["bounds"]:
        assert F(bound["lower"]) <= F(bound["upper"])
    assert rb["covered_subprobability"] and rb["uncovered_target_mass"] == "1/4"
