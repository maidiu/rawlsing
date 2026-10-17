"""F6J — NEW adversarial court. Genuinely new science, not author regression.

Every expectation in this file was frozen and pushed at
e476ccc090ae0175a540e94c5c382d7e2a8453f0 BEFORE any candidate test output was
read. None of these tests exists in the inherited 24 or the author 57.

They cover: exact-rational recomputation, the pre-registered falsifiers,
sample/clock/risk/geo/mapping refusals, minority representation, source swaps,
domain category exclusions, and the consumer contract.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

import pytest

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "03_SCRIPTS"))

from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, complementary_binary_bounds, SynthesisError, METHOD)
import world_builders as W  # noqa: E402
from expectations_engine import (  # noqa: E402
    expected_standardization, expected_frechet, l1, s)

FROZEN = json.loads((RET / "02_FROZEN/01_NEW_FROZEN_INDEPENDENT_WORLDS.json").read_text())
WORLDS = {w["world_id"]: w for w in FROZEN["worlds"]}
ROLES = {"PREREGISTERED_NEW_F6J": "PREREGISTERED_NEW_F6J",
         "POST_DISCLOSURE_REPLICATION": "POST_DISCLOSURE_REPLICATION"}


def run(wid, admit=lambda *_: True, policy=None, sources=None, target=None):
    w = WORLDS[wid]
    pol = deepcopy(policy or w["policy"])
    srcs = deepcopy(sources or w["sources"])
    tgt = deepcopy(target or w["target"])
    given = dict(pol.get("mapping_hashes") or {})
    for src in srcs:
        if src["source_id"] not in given or given[src["source_id"]] is None:
            pol.setdefault("mapping_hashes", {})[src["source_id"]] = semantic_hash(src["axes"])
    return synthesize(tgt, srcs, pol, admit=admit)


def cells(m):
    return {tuple(c["categories"]): F(c["probability"]) for c in m}


# =============================================== 0. provenance honesty
def test_f6j_world_origin_labels_are_explicit_and_not_conflated():
    """Publicly disclosed author examples must never be labelled blind preregistration."""
    origins = {w["world_id"]: w["origin"] for w in FROZEN["worlds"]}
    assert set(origins.values()) == {"PREREGISTERED_NEW_F6J", "POST_DISCLOSURE_REPLICATION"}
    assert origins["R1_AUTHOR_WORLD_A_PUBLIC_HEADLINE"] == "POST_DISCLOSURE_REPLICATION"
    assert origins["R3_AUTHOR_WORLD_B_MASS_ONE_FIFTH"] == "POST_DISCLOSURE_REPLICATION"
    assert origins["N1_SINGLE_SOURCE_IDENTITY"] == "PREREGISTERED_NEW_F6J"
    assert FROZEN["ordering_attestation"]["candidate_test_files_read_before_freeze"] is False
    assert FROZEN["ordering_attestation"]["candidate_junit_read_before_freeze"] is False
    n_new = FROZEN["count_new_preregistered"]
    n_repl = FROZEN["count_post_disclosure_replication"]
    assert n_new >= 6, n_new
    assert n_repl == 2, n_repl
    assert set(FROZEN["perturbation_axes_covered"]) == {
        "target_share_changes", "source_weights", "domain_category_exclusion",
        "minority_representation", "no_positivity", "source_swaps"}


# =============================================== 1. exact rational recomputation
@pytest.mark.parametrize("wid", sorted(WORLDS))
def test_f6j_native_reproduces_independent_exact_rational_expectation(wid):
    out = run(wid)
    e = WORLDS[wid]["expectations"]
    cand = out["candidate"]
    exp_joint = {eval(k): F(v) for k, v in e["joint"].items()}
    obs = cells(cand["covered_subprobability"])
    assert obs == exp_joint, wid
    assert F(cand["uncovered_target_mass"]) == F(e["uncovered_target_mass"]), wid
    assert sum(obs.values(), F(0)) == F(e["covered_subprobability_sum"]), wid
    assert (cand["distribution"] is None) == bool(e["distribution_is_null"]), wid


def test_f6j_single_source_identity_falsifies_pooled_baseline_l1_six_twentyfifths():
    """Commission: 'pooled baseline L1 6/25 vs correct 0'. Correct is 0."""
    out = run("N1_SINGLE_SOURCE_IDENTITY")
    cand = out["candidate"]
    base = out["baseline"][0]
    assert base["mapped_joint"] is not None
    dist = cells(cand["distribution"])
    mapped = cells(base["mapped_joint"])
    assert l1(dist, mapped) == 0
    assert WORLDS["N1_SINGLE_SOURCE_IDENTITY"]["expectations"][
        "preregistered_l1_candidate_vs_baseline_mapped_joint"] == "0"
    assert s(l1(dist, mapped)) == "0"
    assert s(l1(dist, mapped)) != "6/25"


def test_f6j_nopepositivity_null_distribution_and_covered_sum_four_fifths():
    out = run("N5_NO_POSITIVITY_UNCOVERED_MASS")
    cand = out["candidate"]
    assert cand["distribution"] is None
    covered = cells(cand["covered_subprobability"])
    assert sum(covered.values(), F(0)) == F(4, 5)
    assert F(cand["uncovered_target_mass"]) == F(1, 5)


def test_f6j_nopepositivity_widened_upper_is_nineteen_25_and_seven_25():
    out = run("N5_NO_POSITIVITY_UNCOVERED_MASS")
    bounds = {tuple(b["categories"]): (F(b["lower"]), F(b["upper"]))
              for b in out["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]}
    assert bounds[("X", "U")][1] == F(19, 25)
    assert bounds[("X", "V")][1] == F(7, 25)
    assert bounds[("Y", "U")][1] == F(7, 25)
    assert bounds[("Y", "V")][1] == F(7, 25)


def test_f6j_arithmetic_correction_old_14_over_25_to_19_over_25():
    """Omitting the uncovered share understates every upper bound by exactly 1/5."""
    out = run("N5_NO_POSITIVITY_UNCOVERED_MASS")
    covered = cells(out["candidate"]["covered_subprobability"])
    bounds = {tuple(b["categories"]): (F(b["lower"]), F(b["upper"]))
              for b in out["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]}
    old = covered[("X", "U")]          # 14/25, the un-widened value
    assert old == F(14, 25)
    assert bounds[("X", "U")][1] == F(19, 25)
    assert bounds[("X", "U")][1] - old == F(1, 5)


def test_f6j_parallel_arithmetic_correction_31_50_to_41_50_and_7_50_to_17_50():
    out = run("N6_PARALLEL_ARITHMETIC_CORRECTION")
    covered = cells(out["candidate"]["covered_subprobability"])
    bounds = {tuple(b["categories"]): (F(b["lower"]), F(b["upper"]))
              for b in out["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]}
    assert covered[("P",)] == F(31, 50)
    assert covered[("Q",)] == F(7, 50)
    assert bounds[("P",)][1] == F(41, 50)
    assert bounds[("Q",)][1] == F(17, 50)
    assert bounds[("P",)][1] - covered[("P",)] == F(1, 5)
    assert bounds[("Q",)][1] - covered[("Q",)] == F(1, 5)
    assert sum(covered.values(), F(0)) == F(4, 5)


# =============================================== 2. conditional 26/31 vs 4/5
def test_f6j_author_world_a_conditional_is_26_over_31_not_4_over_5():
    out = run("R1_AUTHOR_WORLD_A_PUBLIC_HEADLINE")
    c = conditional(out, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
    assert F(c["probabilities"]["U"]) == F(26, 31)
    assert F(c["model_denominator_mass"]) == F(31, 50)
    assert F(c["probabilities"]["U"]) != F(4, 5)


def test_f6j_new_world_conditional_is_exactly_4_over_5():
    out = run("R2_F6J_CONDITIONAL_FOUR_FIFTHS")
    c = conditional(out, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
    assert F(c["probabilities"]["U"]) == F(4, 5)
    assert F(c["model_denominator_mass"]) == F(1, 2)
    assert F(c["probabilities"]["U"]) != F(26, 31)


def test_f6j_the_two_conditionals_come_from_different_worlds_and_are_not_interchangeable():
    a = run("R1_AUTHOR_WORLD_A_PUBLIC_HEADLINE")
    b = run("R2_F6J_CONDITIONAL_FOUR_FIFTHS")
    da = cells(a["candidate"]["distribution"])
    db = cells(b["candidate"]["distribution"])
    assert da != db
    assert da[("X", "U")] == F(13, 25) and db[("X", "U")] == F(2, 5)
    ca = conditional(a, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
    cb = conditional(b, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
    assert F(ca["probabilities"]["U"]) == F(26, 31)
    assert F(cb["probabilities"]["U"]) == F(4, 5)


# =============================================== 3. pre-registered falsifiers
def test_f6j_f1_decision_is_synthetic_candidate_even_when_distribution_is_null():
    out = run("N5_NO_POSITIVITY_UNCOVERED_MASS")
    assert out["decision"] == "SYNTHETIC_CANDIDATE"
    assert out["candidate"]["distribution"] is None
    assert F(out["candidate"]["uncovered_target_mass"]) == F(1, 5)


def test_f6j_f1b_null_decision_divergence_is_systematic_not_fixture_artefact():
    for wid in ("N5_NO_POSITIVITY_UNCOVERED_MASS", "N6_PARALLEL_ARITHMETIC_CORRECTION"):
        out = run(wid)
        assert out["decision"] == "SYNTHETIC_CANDIDATE", wid
        assert out["candidate"]["distribution"] is None, wid


def test_f6j_f2_unqualified_admit_lambda_is_not_authentication():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs, tgt = deepcopy(w["sources"]), deepcopy(w["target"])
    pol = deepcopy(w["policy"])
    for src in srcs:
        src["test_origin"] = False
        pol["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    seen = []

    def lam(*a):
        seen.append(a[2])
        return True

    out = synthesize(tgt, srcs, pol, admit=lam)
    assert out["candidate"] is not None
    assert len(seen) == 4
    assert set(seen) == {"SOURCE_INDEXED_BASELINE", "TARGET_JOINT_STANDARDIZATION"}


def test_f6j_f2b_synthetic_source_bypasses_admission_entirely():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs, tgt = deepcopy(w["sources"]), deepcopy(w["target"])
    pol = deepcopy(w["policy"])
    for src in srcs:
        pol["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    seen = []

    def lam(*a):
        seen.append(1)
        return True

    synthesize(tgt, srcs, pol, admit=lam)
    assert seen == []


def test_f6j_f2c_real_source_without_admission_fails_closed():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs, tgt = deepcopy(w["sources"]), deepcopy(w["target"])
    pol = deepcopy(w["policy"])
    for src in srcs:
        src["test_origin"] = False
        pol["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    with pytest.raises(SynthesisError):
        synthesize(tgt, srcs, pol, admit=None)


def test_f6j_f3_equiweights_are_not_scientific_calibration():
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")
    sup = out["candidate"]["support"]["Z1"]["sources"]
    assert [F(x["conditional_source_weight"]) for x in sup] == [F(1, 2), F(1, 2)]
    w3 = WORLDS["N3_WEIGHT_PERTURBATION"]
    pol3 = deepcopy(w3["policy"])
    for src in w3["sources"]:
        pol3["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    a = synthesize(w3["target"], w3["sources"], pol3, admit=lambda *_: True)
    pol30 = deepcopy(w3["policy"])
    pol30["source_weights"] = {"S1": "30", "S2": "10"}
    for src in w3["sources"]:
        pol30["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    b = synthesize(w3["target"], w3["sources"], pol30, admit=lambda *_: True)
    assert cells(a["candidate"]["distribution"]) == cells(b["candidate"]["distribution"])


def test_f6j_f4_sensitivity_halfwidth_3_over_50_is_not_a_confidence_interval():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    pol = deepcopy(w["policy"])
    pol.update(mapping_bias_radius="1/50", transport_bias_radius="1/50",
               target_share_bias_radius="1/50")
    for src in w["sources"]:
        pol["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    out = synthesize(w["target"], w["sources"], pol, admit=lambda *_: True)
    b = out["candidate"]["uncertainty"]["bias_sensitivity_bounds"][0]
    half = (F(b["upper"]) - F(b["lower"])) / 2
    assert half == F(3, 50)
    assert "not confidence intervals" in out["candidate"]["uncertainty"]["limitations"]
    assert "coverage" not in json.dumps(out["candidate"]["uncertainty"]).lower()


def test_f6j_f5_cross_survey_person_is_never_invented():
    fr = complementary_binary_bounds("1/2", "1/2")
    assert fr["dependence"] == "UNIDENTIFIED"
    assert fr["scenario_is_measured"] is False
    ind = expected_frechet(F(1, 2), F(1, 2))
    assert F(fr["lower"]) == ind["lower"] and F(fr["upper"]) == ind["upper"]
    assert F(fr["independence_scenario"]) == ind["independence_scenario"]
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")
    assert "NO_CROSS_SURVEY_RESPONDENT_LINKS" in out["candidate"]["dependence"]


def test_f6j_f6_conditional_variance_is_unidentified():
    out = run("R2_F6J_CONDITIONAL_FOUR_FIFTHS")
    c = conditional(out, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
    assert c["uncertainty"] == "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED"
    assert "variance" not in json.dumps(c).lower()
    assert c["observed_denominator"] is None


def test_f6j_self_conditioning_is_refused_as_tautology():
    out = run("R2_F6J_CONDITIONAL_FOUR_FIFTHS")
    c = conditional(out, {"SYN_CONSTRUCT_BEHAVIOUR": "U"}, "SYN_CONSTRUCT_BEHAVIOUR")
    assert c["state"] == "DESCRIPTIVE_SELF_CONDITIONING"
    assert c["self_conditioning_status"] == "OUTCOME_LEAKAGE_TAUTOLOGY"


# =============================================== 4. refusals
def test_f6j_geo_refusal_target_scope_mismatch():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    tgt = deepcopy(w["target"]); tgt["geography"] = "SYN_GEO_OTHER"
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", target=tgt)
    for sid in ("S1", "S2"):
        assert "TARGET_SCOPE_MISMATCH" in out["refusals"][sid]
    assert out["candidate"] is None
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_clock_refusal_time_not_applicable():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    tgt = deepcopy(w["target"]); tgt["year"] = 1900
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", target=tgt)
    for sid in ("S1", "S2"):
        assert "TIME_NOT_APPLICABLE" in out["refusals"][sid]
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_mapping_refusal_unqualified_mapping():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs = deepcopy(w["sources"])
    srcs[0]["axes"][0]["mapping_confidence"] = "LOW"
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", sources=srcs)
    assert "MAPPING_UNQUALIFIED" in out["refusals"]["S1"]
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_mapping_refusal_preimage_mismatch():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    pol = deepcopy(w["policy"])
    pol["mapping_hashes"] = {"S1": "0" * 64, "S2": "0" * 64}
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", policy=pol)
    assert "MAPPING_REVIEW_PREIMAGE_MISMATCH" in out["refusals"]["S1"]
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_overlap_refusal_unresolved():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    pol = deepcopy(w["policy"])
    pol["overlap_reviews"] = {}
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", policy=pol)
    assert any(d["reason"] == "OVERLAP_UNRESOLVED" for d in out["overlap_diagnostics"])
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_sample_refusal_duplicate_sample():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs = deepcopy(w["sources"])
    srcs[1]["product_ref"] = srcs[0]["product_ref"]
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", sources=srcs)
    assert any(d["reason"] == "DUPLICATE_SAMPLE" for d in out["overlap_diagnostics"])
    assert out["decision"] == "SOURCE_INDEXED_BACKOFF"


def test_f6j_risk_refusal_suppressed_cells_cannot_become_zero():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    srcs = deepcopy(w["sources"])
    srcs[0]["strata"]["Z1"]["table_status"] = "SUPPRESSED"
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", sources=srcs)


def test_f6j_risk_refusal_incomplete_joint_domain():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    srcs = deepcopy(w["sources"])
    srcs[0]["strata"]["Z1"]["cells"] = srcs[0]["strata"]["Z1"]["cells"][:3]
    srcs[0]["strata"]["Z1"]["eligible_n"] = 3
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", sources=srcs)


def test_f6j_denominator_exclusion_conservation_enforced():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    srcs = deepcopy(w["sources"])
    srcs[0]["strata"]["Z1"]["eligible_n"] += 5
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", sources=srcs)


def test_f6j_unweighted_mass_must_equal_raw_count():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    srcs = deepcopy(w["sources"])
    srcs[0]["strata"]["Z1"]["cells"][0]["mass"] = 6
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", sources=srcs)


def test_f6j_weighted_raw_zero_support_mismatch_refused():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    srcs = deepcopy(w["sources"])
    srcs[0]["strata"]["Z1"]["cells"][0]["n"] = 0
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", sources=srcs)


def test_f6j_target_shares_must_sum_to_one():
    w = WORLDS["N1_SINGLE_SOURCE_IDENTITY"]
    tgt = deepcopy(w["target"]); tgt["strata"] = {"Z1": "1/2"}
    with pytest.raises(SynthesisError):
        run("N1_SINGLE_SOURCE_IDENTITY", target=tgt)


def test_f6j_zero_weight_is_refused_not_silently_dropped():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    pol = deepcopy(w["policy"])
    pol["source_weights"] = {"S1": "1", "S2": "0"}
    with pytest.raises(SynthesisError):
        run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", policy=pol)


def test_f6j_dependence_kind_must_be_measured_same_survey_joint():
    w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
    srcs = deepcopy(w["sources"])
    srcs[0]["dependence_kind"] = "MODELED_DEPENDENCE"
    with pytest.raises(SynthesisError):
        run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", sources=srcs)


# =============================================== 5. minority / source swap / shares
def test_f6j_minority_cell_survives_but_threshold_is_not_a_cell_guard():
    """minimum_raw_support gates the STRATUM TOTAL, not the minority cell.

    FINDING: a genuine minority cell of 3 respondents inside a stratum of 100 is
    never pruned by minimum_raw_support, because the threshold is applied to the
    stratum's summed raw count. The threshold therefore cannot be described as a
    minority-representation guard.
    """
    out1 = run("N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD")
    d1 = cells(out1["candidate"]["distribution"])
    # the minority cell X|U is present and nonzero
    assert d1[("X", "U")] > 0
    # raising the threshold above the minority cell count (3) does NOT drop S1,
    # because S1's stratum total is 100
    w = WORLDS["N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD"]
    pol5 = deepcopy(w["policy"]); pol5["minimum_raw_support"] = 5
    out5 = run("N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD", policy=pol5)
    assert cells(out5["candidate"]["distribution"]) == d1
    assert [x["source_id"] for x in out5["candidate"]["support"]["Z1"]["sources"]] == ["S1", "S2"]


def test_f6j_threshold_above_every_stratum_total_yields_no_positivity():
    """Both frozen N8 sources have stratum total 100; a 200 threshold excludes
    both, so the target becomes fully uncovered and the distribution is null."""
    w = WORLDS["N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD"]
    pol = deepcopy(w["policy"]); pol["minimum_raw_support"] = 200
    out = run("N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD", policy=pol)
    sup = out["candidate"]["support"]["Z1"]
    assert sup["excluded_sources"] == ["S1", "S2"]
    assert sup["sources"] == []
    assert out["candidate"]["distribution"] is None
    assert F(out["candidate"]["uncovered_target_mass"]) == 1


def test_f6j_stratum_level_threshold_exclusion_renormalizes_alpha():
    """A source IS excluded when its STRATUM TOTAL falls below the threshold,
    and alpha then renormalizes onto the survivors.

    Local inputs, not a frozen world: S1 total 100, S2 total 200, threshold 150.
    """
    w = WORLDS["N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD"]
    srcs = deepcopy(w["sources"])
    srcs[1]["strata"]["Z1"]["cells"] = [
        {"categories": ["na0", "nb0"], "n": 50, "mass": 50},
        {"categories": ["na0", "nb1"], "n": 50, "mass": 50},
        {"categories": ["na1", "nb0"], "n": 50, "mass": 50},
        {"categories": ["na1", "nb1"], "n": 50, "mass": 50}]
    srcs[1]["strata"]["Z1"]["eligible_n"] = 200
    pol = deepcopy(w["policy"]); pol["minimum_raw_support"] = 150
    out = run("N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD",
              policy=pol, sources=srcs)
    sup = out["candidate"]["support"]["Z1"]
    assert sup["excluded_sources"] == ["S1"]
    assert [x["source_id"] for x in sup["sources"]] == ["S2"]
    assert F(sup["sources"][0]["conditional_source_weight"]) == 1
    d = cells(out["candidate"]["distribution"])
    assert d == {("X", "U"): F(1, 4), ("X", "V"): F(1, 4),
                 ("Y", "U"): F(1, 4), ("Y", "V"): F(1, 4)}


def test_f6j_source_swap_equalizes_stratum_mixes_and_makes_target_shares_inert():
    """Swapping which source supplies which stratum equalizes the two stratum
    mixes, so the estimate becomes invariant to the target shares."""
    w = WORLDS["N9_SOURCE_SWAP"]
    a = run("N9_SOURCE_SWAP")
    tgt = deepcopy(w["target"]); tgt["strata"] = {"Z1": "1/4", "Z2": "3/4"}
    b = run("N9_SOURCE_SWAP", target=tgt)
    da, db = cells(a["candidate"]["distribution"]), cells(b["candidate"]["distribution"])
    assert da == db
    assert da == {("X", "U"): F(5, 16), ("X", "V"): F(3, 16),
                  ("Y", "U"): F(3, 16), ("Y", "V"): F(5, 16)}
    ref = run("N4_TARGET_SHARE_SHIFT")
    assert cells(ref["candidate"]["distribution"]) != da


def test_f6j_target_share_shift_moves_the_estimate():
    w = WORLDS["N4_TARGET_SHARE_SHIFT"]
    a = run("N4_TARGET_SHARE_SHIFT")
    tgt = deepcopy(w["target"]); tgt["strata"] = {"Z1": "1/4", "Z2": "3/4"}
    b = run("N4_TARGET_SHARE_SHIFT", target=tgt)
    assert cells(a["candidate"]["distribution"]) != cells(b["candidate"]["distribution"])


def test_f6j_weight_perturbation_moves_the_estimate():
    a = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")
    b = run("N3_WEIGHT_PERTURBATION")
    assert cells(a["candidate"]["distribution"]) != cells(b["candidate"]["distribution"])


# =============================================== 6. provenance / no person
def test_f6j_no_person_no_calibration_no_real_source_claimed():
    out = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")
    assert out["test_origin"] is True
    assert out["real_source_qualification"] == "EXTERNAL_REVIEW_REQUIRED"
    cand = out["candidate"]
    assert cand["sample_size"] is None
    assert "NO_CROSS_SURVEY_RESPONDENT_LINKS" in cand["dependence"]
    assert cand["evidence_mode"] == "INFERRED"
    ceilings = [n.get("authority_ceiling") for n in out["evidence_graph"]]
    assert "DESCRIPTIVE_SOCIOLOGICAL_MODEL_ONLY" in ceilings
    assert "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE" in ceilings
    # FINDING: the TRANSFORMED 'mapped:*' nodes carry no authority_ceiling at all,
    # while the MEASURED 'native:*' nodes and the inferred target_joint do.
    missing = [n["node_id"] for n in out["evidence_graph"] if "authority_ceiling" not in n]
    assert missing and all(nid.startswith("mapped:") for nid in missing)
    js = json.dumps(out).lower()
    assert "respondent_id" not in js and "person_id" not in js


def test_f6j_method_identity_and_native_blob_are_pinned():
    assert METHOD == "PRE553_TARGET_JOINT_STANDARDIZATION@1"
    src = (RET / "01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py")
    import subprocess
    blob = subprocess.run(["git", "hash-object", str(src)], capture_output=True,
                          text=True, check=True).stdout.strip()
    assert blob == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
