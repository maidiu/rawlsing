"""Real original F6M/F6P first-reader examples from frozen post-VOZHD oracle.

All sourcefree; these source strata do not authorize native survey science.
"""
from copy import deepcopy

import pytest

from rawlsing_next import pre553_heterogeneous_synthesis as M
from rawlsing_next._f6_candidate import f6c_oracle_worlds as OW
from rawlsing_next._f6_candidate import f6p_partial_bound_evidence_consumer as P
from rawlsing_next._f6_candidate.f6m_f6p_integration import (
    evaluate_f6m_f6p_sourcefree,
)


def _case(name, request_override=None):
    target, sources, policy = OW.WORLD_BUILDERS[name]()
    conditions, outcome = OW.CONSUMER_REQUEST[name]
    req = {"conditions": dict(conditions), "outcome": outcome}
    if request_override:
        req.update(request_override)
    return evaluate_f6m_f6p_sourcefree(
        target=target, sources=sources, policy=policy, request=req
    )


def test_complete_original_r35_w1_stratified_first_consumer_is_sourcefree_only():
    result = _case("W1_full_coverage_disjoint")
    assert result.product["decision"] == "SYNTHETIC_CANDIDATE"
    assert result.evidence["evidence_state"] == P.SUPPORTED
    assert result.evidence["uncovered_target_mass"] == "0"
    assert result.evidence["supported_point"] == {"formal": "5/8", "informal": "3/8"}
    assert result.evidence["real_use_authorized"] is False
    assert result.evidence["transport"]["permitted"] is False


@pytest.mark.parametrize("world,uncovered", [
    ("W2_mixed_eligibility_trap", "1/4"),
    ("W7_source_excluded_all_strata", "1/2"),
    ("W3_minority_whole_stratum_absent", "1/5"),
])
def test_minorities_or_missing_strata_never_renormalize_into_full_joint(world, uncovered):
    result = _case(world)
    assert result.evidence["evidence_state"] == P.PARTIAL
    assert result.evidence["uncovered_target_mass"] == uncovered
    assert result.evidence["supported_point"] is None
    assert result.product["target_joint_status"] == "NO_COMPLETE_TARGET_JOINT"
    assert result.evidence["covered_subprobability"]
    assert result.evidence["exclusions"]


def test_actual_f6m_f6p_self_conditioning_is_not_predictor():
    result = _case("W4_outcome_leakage")
    assert result.evidence["evidence_state"] == P.SELF_CONDITIONING
    assert result.evidence["supported_point"] is None


def test_actual_f6m_f6p_duplicate_sample_is_not_independent_respondent():
    result = _case("W6_overlap_duplicate_sample")
    assert result.evidence["evidence_state"] == P.INCOMPATIBLE_RESPONDENT
    assert result.evidence["supported_point"] is None


def test_f6p_real_use_and_transport_self_issuance_refused():
    result = _case("W1_full_coverage_disjoint", {"use": "REAL_USE"})
    assert result.evidence["evidence_state"] == P.PROHIBITED
    assert result.evidence["supported_point"] is None
    result = _case("W1_full_coverage_disjoint", {"admission": "OWNER_APPROVED"})
    assert result.evidence["evidence_state"] == P.PROHIBITED
    assert result.evidence["supported_point"] is None


def test_exact_original_f6m_product_is_needed_and_tampering_refused():
    target, sources, policy = OW.WORLD_BUILDERS["W2_mixed_eligibility_trap"]()
    bundle = M.synthesize(target, sources, policy)
    assert P.consume_f6m_evidence(bundle)["evidence_state"] == P.PARTIAL
    forged = deepcopy(bundle)
    forged["candidate"]["uncovered_target_mass"] = "0"
    with pytest.raises(P.ConsumerRefusal, match="BUNDLE_REPLAY_MISMATCH"):
        P.consume_f6m_evidence(forged)
