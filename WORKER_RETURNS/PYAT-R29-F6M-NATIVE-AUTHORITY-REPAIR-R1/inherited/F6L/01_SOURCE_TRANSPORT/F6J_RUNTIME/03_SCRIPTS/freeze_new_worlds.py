"""F6J — freeze NEW independent perturbation worlds + exact-rational expectations.

ORDERING DISCIPLINE: this runs BEFORE any candidate test file, JUnit, log or
verdict of the F6C candidate is read. Its output is committed and pushed as a
freeze before that inspection.

ORIGIN LABELS (commission requirement — do not conflate):
  PREREGISTERED_NEW_F6J        genuinely new to this court, frozen blind to
                               candidate test output, values chosen by F6J.
  POST_DISCLOSURE_REPLICATION  built from the author's PUBLICLY DISCLOSED
                               headline values. These CANNOT be called blind
                               pre-freeze. Replication targets only.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
STAGE = RET / "01_STAGED_NATIVE"
sys.path.insert(0, str(STAGE))
sys.path.insert(0, str(RET / "03_SCRIPTS"))

from expectations_engine import (  # noqa: E402
    expected_standardization, expected_sensitivity, expected_conditional,
    expected_frechet, l1, s)
import world_builders as W  # noqa: E402

from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402

FROZEN_AT_UTC = "2026-10-17T02:25:00Z"

NEW = "PREREGISTERED_NEW_F6J"
REPL = "POST_DISCLOSURE_REPLICATION"

worlds = []
falsifiers = []


def add(wid, origin, purpose, target, sources, pol, expectations, notes=""):
    for src in sources:
        pol["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
    worlds.append({
        "world_id": wid, "origin": origin, "purpose": purpose,
        "perturbation_axis": purpose,
        "target": target, "sources": sources, "policy": pol,
        "expectations": expectations, "notes": notes,
    })


def exp(q=None, lower=None, upper=None, uncovered=None, extra=None):
    e = {}
    if q is not None:
        e["joint"] = {str(k): s(v) for k, v in sorted(q["joint"].items())}
        e["lower"] = {str(k): s(v) for k, v in sorted(q["lower"].items())}
        e["upper"] = {str(k): s(v) for k, v in sorted(q["upper"].items())}
        e["uncovered_target_mass"] = s(q["uncovered"])
        e["covered_subprobability_sum"] = s(sum(q["joint"].values(), F(0)))
        e["distribution_is_null"] = q["uncovered"] != 0
    e.update(extra or {})
    return e


# ---------------------------------------------------------------- N1
# PREREGISTERED falsifier of the commission's "pooled baseline L1 6/25 vs 0".
# With ONE source and ONE target stratum the candidate must equal the baseline
# mapped joint EXACTLY. L1 must be 0, not 6/25.
c1 = {("na0", "nb0"): 5, ("na0", "nb1"): 3, ("na1", "nb0"): 1, ("na1", "nb1"): 7}
s1 = W.source("S1", {"Z1": {"counts": c1}})
t1 = W.target({"Z1": 1})
p1 = W.policy(["S1"], {"S1": "1"}, overlap_reviews={})
q1 = expected_standardization(t1["strata"], W.tables_from_sources([s1]),
                              {"S1": F(1)}, 1)
m1 = W.normalised_masses(c1, s1["axes"])
add("N1_SINGLE_SOURCE_IDENTITY", NEW,
    "single-source single-stratum identity: candidate must equal baseline mapped joint",
    t1, [s1], p1,
    exp(q1, extra={
        "preregistered_l1_candidate_vs_baseline_mapped_joint": "0",
        "preregistered_identity_holds": True,
        "baseline_mapped_joint": {str(k): s(v) for k, v in sorted(m1.items())},
        "rejected_claim": "pooled baseline L1 = 6/25",
        "reason": "with one source and one stratum, alpha=1 and share=1, so the "
                  "standardized joint IS the source mapped joint; any nonzero L1 "
                  "is an arithmetic defect, not a scientific difference",
    }),
    "Counts 5,3,1,7 over 2x2 domain, total 16.")

# ---------------------------------------------------------------- N2
c2a = {("na0", "nb0"): 8, ("na0", "nb1"): 4, ("na1", "nb0"): 2, ("na1", "nb1"): 2}
c2b = {("na0", "nb0"): 2, ("na0", "nb1"): 2, ("na1", "nb0"): 4, ("na1", "nb1"): 8}
sA = W.source("S1", {"Z1": {"counts": c2a}})
sB = W.source("S2", {"Z1": {"counts": c2b}})
t2 = W.target({"Z1": 1})
p2 = W.policy(["S1", "S2"], {"S1": "1", "S2": "1"},
              overlap_reviews=W.disjoint_review([("S1", "S2")]))
q2 = expected_standardization(t2["strata"], W.tables_from_sources([sA, sB]),
                              {"S1": F(1), "S2": F(1)}, 1)
add("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX", NEW,
    "two-source equiweight mixture: equiweight is a mixing coefficient, not calibration",
    t2, [sA, sB], p2,
    exp(q2, extra={
        "preregistered_joint": {str(k): s(v) for k, v in sorted(q2["joint"].items())},
        "preregistered_alpha_S1": "1/2",
        "preregistered_alpha_S2": "1/2",
        "preregistered_l1_S1_vs_joint": s(l1(
            W.normalised_masses(c2a, sA["axes"]), q2["joint"])),
        "claim_falsified": "two-source equiweights are scientific calibration",
        "falsification_reason": "alpha is a normalized weight ratio with no design, "
                                "no variance and no calibration target; it is an "
                                "arbitrary mixing coefficient",
    }),
    "Counts 8,4,2,2 and 2,2,4,8, totals 16 each.")

# ---------------------------------------------------------------- N3
p3 = W.policy(["S1", "S2"], {"S1": "3", "S2": "1"},
              overlap_reviews=W.disjoint_review([("S1", "S2")]))
q3 = expected_standardization(t2["strata"], W.tables_from_sources([sA, sB]),
                              {"S1": F(3), "S2": F(1)}, 1)
p3s = W.policy(["S1", "S2"], {"S1": "30", "S2": "10"},
               overlap_reviews=W.disjoint_review([("S1", "S2")]))
q3s = expected_standardization(t2["strata"], W.tables_from_sources([sA, sB]),
                               {"S1": F(30), "S2": F(10)}, 1)
add("N3_WEIGHT_PERTURBATION", NEW,
    "weight perturbation and weight-scale invariance",
    t2, [sA, sB], p3,
    exp(q3, extra={
        "preregistered_alpha_S1": "3/4",
        "preregistered_alpha_S2": "1/4",
        "preregistered_weight_scale_invariance": {
            "weights_3_1": {str(k): s(v) for k, v in sorted(q3["joint"].items())},
            "weights_30_10": {str(k): s(v) for k, v in sorted(q3s["joint"].items())},
            "identical": q3["joint"] == q3s["joint"],
        },
        "preregistered_weights_3_1_joint": {str(k): s(v) for k, v in sorted(q3["joint"].items())},
    }),
    "Only weight RATIOS enter; absolute scale is inert. That is itself evidence "
    "that the weights are not a scientific calibration.")

# ---------------------------------------------------------------- N4 target shares
t4a = W.target({"Z1": "3/4", "Z2": "1/4"})
t4b = W.target({"Z1": "1/4", "Z2": "3/4"})
sC = W.source("S1", {"Z1": {"counts": c2a}, "Z2": {"counts": c2b}})
sD = W.source("S2", {"Z1": {"counts": c2a}, "Z2": {"counts": c2b}})
p4 = W.policy(["S1", "S2"], {"S1": "1", "S2": "1"},
              overlap_reviews=W.disjoint_review([("S1", "S2")]))
q4a = expected_standardization(t4a["strata"], W.tables_from_sources([sC, sD]),
                               {"S1": F(1), "S2": F(1)}, 1)
q4b = expected_standardization(t4b["strata"], W.tables_from_sources([sC, sD]),
                               {"S1": F(1), "S2": F(1)}, 1)
add("N4_TARGET_SHARE_SHIFT", NEW,
    "target-share perturbation with stratum-specific mixes",
    t4a, [sC, sD], p4,
    exp(q4a, extra={
        "preregistered_shares_3_4_1_4": {str(k): s(v) for k, v in sorted(q4a["joint"].items())},
        "preregistered_shares_1_4_3_4": {str(k): s(v) for k, v in sorted(q4b["joint"].items())},
        "preregistered_shares_1_2_1_2": {str(k): s(v) for k, v in sorted(
            expected_standardization({"Z1": F(1, 2), "Z2": F(1, 2)},
                                     W.tables_from_sources([sC, sD]),
                                     {"S1": F(1), "S2": F(1)}, 1)["joint"].items())},
    }),
    "Both sources carry the SAME stratum tables, so source weights are inert and "
    "only target shares move the estimate. This isolates the target-share channel.")

# ---------------------------------------------------------------- N5 no positivity
c5 = {("na0", "nb0"): 70, ("na0", "nb1"): 10, ("na1", "nb0"): 10, ("na1", "nb1"): 10}
s5 = W.source("S1", {"Z1": {"counts": c5}})
t5 = W.target({"Z1": "4/5", "Z2": "1/5"})
p5 = W.policy(["S1"], {"S1": "1"})
q5 = expected_standardization(t5["strata"], W.tables_from_sources([s5]),
                              {"S1": F(1)}, 1)
add("N5_NO_POSITIVITY_UNCOVERED_MASS", NEW,
    "no-positivity: a target stratum with zero eligible source support",
    t5, [s5], p5,
    exp(q5, extra={
        "preregistered_distribution_is_null": True,
        "preregistered_covered_subprobability_sum": s(sum(q5["joint"].values(), F(0))),
        "preregistered_widened_upper": {str(k): s(v) for k, v in sorted(q5["upper"].items())},
        "preregistered_uncovered": s(q5["uncovered"]),
        "preregistered_old_unwiden_upper_cell_XU": s(q5["joint"][("X","U")]),
        "preregistered_corrected_upper_cell_XU": s(q5["upper"][("X","U")]),
        "preregistered_correction": "old 14/25 -> corrected 19/25 by adding the "
                                    "uncovered share 1/5 = 5/25; omitting it "
                                    "understates every upper bound",
    }),
    "Counts 70,10,10,10 total 100 -> p=(7/10,1/10,1/10,1/10). Target strata "
    "Z1=4/5 covered by S1, Z2=1/5 has NO eligible source.")

# ---------------------------------------------------------------- N6 parallel correction
c6 = {("nu0",): 31, ("nu1",): 7, ("nu2",): 2}
ax6 = [{"item_ref": "SYN_ITEM_U", "construct_ref": "SYN_CONSTRUCT_UNARY",
        "mapping_ref": "SYN_MAP_U", "scale_ref": "SYN_SCALE_U",
        "polarity_ref": "SYN_POL_U", "instrument_ref": "SYN_INSTR_U",
        "response_semantics_ref": "SYN_RESP_U",
        "category_map": {"nu0": "P", "nu1": "Q", "nu2": "R"},
        "review_status": "REVIEWED", "mapping_confidence": "HIGH",
        "scale_status": "REVIEWED", "polarity_status": "REVIEWED"}]
s6 = W.source("S1", {"Z1": {"counts": c6}}, axes_override=ax6)
t6 = W.target({"Z1": "4/5", "Z2": "1/5"})
p6 = W.policy(["S1"], {"S1": "1"})
q6 = expected_standardization(t6["strata"], W.tables_from_sources([s6]),
                              {"S1": F(1)}, 1)
add("N6_PARALLEL_ARITHMETIC_CORRECTION", NEW,
    "parallel uncovered-share arithmetic correction on a 3-category unary axis",
    t6, [s6], p6,
    exp(q6, extra={
        "preregistered_old_upper_31_50": "31/50",
        "preregistered_corrected_upper_41_50": "41/50",
        "preregistered_old_upper_7_50": "7/50",
        "preregistered_corrected_upper_17_50": "17/50",
        "preregistered_correction_rule": "corrected = covered + uncovered share "
                                         "(1/5 = 10/50); 31/50 -> 41/50 and "
                                         "7/50 -> 17/50",
        "preregistered_widened_upper": {str(k): s(v) for k, v in sorted(q6["upper"].items())},
    }),
    "Counts 31,7,2 total 40 -> p=(31/40,7/40,2/40). Covered=(31/50,7/50,2/50) "
    "summing to 4/5; uncovered 1/5 widens each upper by 1/5.")

# ---------------------------------------------------------------- N7 domain exclusion
c7 = {("na0", "nb0"): 20, ("na0", "nb1"): 10, ("na1", "nb0"): 6, ("na1", "nb1"): 4}
s7 = W.source("S1", {"Z1": {"counts": c7}})
t7 = W.target({"Z1": 1})
p7 = W.policy(["S1"], {"S1": "1"})
q7 = expected_standardization(t7["strata"], W.tables_from_sources([s7]),
                              {"S1": F(1)}, 1)
add("N7_COMPLETE_DOMAIN_CONTROL", NEW,
    "complete-domain control before the exclusion attack",
    t7, [s7], p7,
    exp(q7, extra={"preregistered_cell_count": 4, "preregistered_domain_size": 4}),
    "Counts 20,10,6,4 total 40.")

# ---------------------------------------------------------------- N8 minority / small support
c8 = {("na0", "nb0"): 3, ("na0", "nb1"): 1, ("na1", "nb0"): 24, ("na1", "nb1"): 72}
s8a = W.source("S1", {"Z1": {"counts": c8}})
c8b = {("na0", "nb0"): 25, ("na0", "nb1"): 25, ("na1", "nb0"): 25, ("na1", "nb1"): 25}
s8b = W.source("S2", {"Z1": {"counts": c8b}})
t8 = W.target({"Z1": 1})
p8 = W.policy(["S1", "S2"], {"S1": "1", "S2": "1"}, min_raw_support=1,
              overlap_reviews=W.disjoint_review([("S1", "S2")]))
q8 = expected_standardization(t8["strata"], W.tables_from_sources([s8a, s8b]),
                              {"S1": F(1), "S2": F(1)}, 1)
p8b = W.policy(["S1", "S2"], {"S1": "1", "S2": "1"}, min_raw_support=5,
               overlap_reviews=W.disjoint_review([("S1", "S2")]))
q8b = expected_standardization(t8["strata"], W.tables_from_sources([s8a, s8b]),
                               {"S1": F(1), "S2": F(1)}, 5)
add("N8_MINORITY_REPRESENTATION_AND_SUPPORT_THRESHOLD", NEW,
    "minority category representation and minimum_raw_support threshold interaction",
    t8, [s8a, s8b], p8,
    exp(q8, extra={
        "minority_cell": "X|U",
        "minority_counts_S1": 3,
        "minority_native_share_S1": s(F(3, 100)),
        "preregistered_min_support_1": {str(k): s(v) for k, v in sorted(q8["joint"].items())},
        "preregistered_min_support_5": {str(k): s(v) for k, v in sorted(q8b["joint"].items())},
        "preregistered_threshold_changes_estimate": q8["joint"] != q8b["joint"],
        "preregistered_alpha_S1_at_1": "1/2",
        "preregistered_alpha_S1_at_5": "0 (excluded: raw_n=3 < 5)",
    }),
    "S1 has a genuine minority cell of 3 respondents in na0|nb0. Raising "
    "minimum_raw_support above 3 silently DROPS S1 entirely and renormalizes "
    "alpha onto S2 alone, which erases the minority estimate.")

# ---------------------------------------------------------------- N9 source swap
s9a = W.source("S1", {"Z1": {"counts": c2a}, "Z2": {"counts": c2b}})
s9b = W.source("S2", {"Z1": {"counts": c2b}, "Z2": {"counts": c2a}})
p9 = W.policy(["S1", "S2"], {"S1": "1", "S2": "1"},
              overlap_reviews=W.disjoint_review([("S1", "S2")]))
q9 = expected_standardization(t4a["strata"], W.tables_from_sources([s9a, s9b]),
                              {"S1": F(1), "S2": F(1)}, 1)
add("N9_SOURCE_SWAP", NEW,
    "source-swap perturbation: which source supplies which stratum",
    t4a, [s9a, s9b], p9,
    exp(q9, extra={
        "preregistered_swapped_joint": {str(k): s(v) for k, v in sorted(q9["joint"].items())},
        "preregistered_matches_N4_target_share": q9["joint"] == q4a["joint"],
        "preregistered_reason": "both sources are eligible in both strata and "
                                "equiweighted, so swapping which source supplies "
                                "which stratum is inert; the estimate depends only "
                                "on the stratum tables and target shares",
    }),
    "Positive control for the source-swap channel.")

# ---------------------------------------------------------------- R1 post-disclosure
cA = {("na0", "nb0"): 26, ("na0", "nb1"): 5, ("na1", "nb0"): 5, ("na1", "nb1"): 14}
sA1 = W.source("S1", {"Z1": {"counts": cA}})
tA = W.target({"Z1": 1})
pA = W.policy(["S1"], {"S1": "1"})
qA = expected_standardization(tA["strata"], W.tables_from_sources([sA1]),
                              {"S1": F(1)}, 1)
condA = expected_conditional(qA["joint"], qA["keys"], W.construct_refs(sA1["axes"]),
                             {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
add("R1_AUTHOR_WORLD_A_PUBLIC_HEADLINE", REPL,
    "replication of the author's PUBLICLY DISCLOSED World A headline",
    tA, [sA1], pA,
    exp(qA, extra={
        "publicly_disclosed_world_A": ["13/25", "1/10", "1/10", "7/25"],
        "is_blind_prefreeze": False,
        "label": "POST_DISCLOSURE_REPLICATION",
        "preregistered_conditional_P_U_given_X": s(condA["probabilities"].get("U", F(0))),
        "preregistered_conditional_denominator_P_X": s(condA["denominator"]),
        "preregistered_note": "this world yields 26/31, NOT 4/5; 26/31 and 4/5 are "
                              "different worlds and must not be conflated",
    }),
    "Counts 26,5,5,14 total 50 reproduce the public headline "
    "13/25, 1/10, 1/10, 7/25. CANNOT be called blind pre-freeze.")

# ---------------------------------------------------------------- R2 post-disclosure conditional 4/5
cB = {("na0", "nb0"): 20, ("na0", "nb1"): 5, ("na1", "nb0"): 5, ("na1", "nb1"): 20}
sB1 = W.source("S1", {"Z1": {"counts": cB}})
tB = W.target({"Z1": 1})
pB = W.policy(["S1"], {"S1": "1"})
qB = expected_standardization(tB["strata"], W.tables_from_sources([sB1]),
                              {"S1": F(1)}, 1)
condB = expected_conditional(qB["joint"], qB["keys"], W.construct_refs(sB1["axes"]),
                             {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
add("R2_F6J_CONDITIONAL_FOUR_FIFTHS", NEW,
    "independent new world whose conditional is exactly 4/5",
    tB, [sB1], pB,
    exp(qB, extra={
        "preregistered_conditional_P_U_given_X": s(condB["probabilities"].get("U", F(0))),
        "preregistered_conditional_denominator_P_X": s(condB["denominator"]),
        "preregistered_joint": {str(k): s(v) for k, v in sorted(qB["joint"].items())},
        "contrasts_with": "R1 yields 26/31 on a DIFFERENT world",
    }),
    "Counts 20,5,5,20 total 50 -> joint (2/5,1/10,1/10,2/5). "
    "P(U|X) = (2/5)/(2/5+1/10) = 4/5.")

# ---------------------------------------------------------------- R3 post-disclosure World B
cC = {("na0", "nb0"): 10, ("na0", "nb1"): 10, ("na1", "nb0"): 5, ("na1", "nb1"): 5}
sC1 = W.source("S1", {"Z1": {"counts": cC}})
tC = W.target({"Z1": 1})
pC = W.policy(["S1"], {"S1": "1"})
qC = expected_standardization(tC["strata"], W.tables_from_sources([sC1]),
                              {"S1": F(1)}, 1)
add("R3_AUTHOR_WORLD_B_MASS_ONE_FIFTH", REPL,
    "replication of the author's PUBLICLY DISCLOSED World B 1/5 mass",
    tC, [sC1], pC,
    exp(qC, extra={
        "publicly_disclosed_world_B_mass": "1/5",
        "is_blind_prefreeze": False,
        "label": "POST_DISCLOSURE_REPLICATION",
    }),
    "Counts 10,10,5,5 total 30. Mass one-fifth is visible in the "
    "(na1,*) block: 5/30 + 5/30 = 1/3 of total; the 1/5 mass is the "
    "(na1,nb1) cell share of the na1 block. Replication target only.")

# ---------------------------------------------------------------- R4 Frechet / cross-survey
fr = expected_frechet(F(1, 2), F(1, 2))
falsifiers.append({
    "id": "F5_CROSS_SURVEY_PERSON_NEVER_INVENTED",
    "claim_attacked": "the independence scenario p*q is a measured joint",
    "preregistered_frechet_p_half_q_half": {
        "lower": s(fr["lower"]), "upper": s(fr["upper"]),
        "independence_scenario": s(fr["independence_scenario"]),
    },
    "preregistered_verdict": "FALSIFIED",
    "reason": "Fréchet bounds are unidentified cross-channel bounds; p*q is a "
              "scenario, explicitly not a measured joint, and no cross-survey "
              "respondent link exists to measure it",
})

# ---------------------------------------------------------------- decision falsifiers
falsifiers += [
    {
        "id": "F1_MISLEADING_DECISION_WHEN_DISTRIBUTION_NULL",
        "claim_attacked": "decision 'SYNTHETIC_CANDIDATE' is admissible when the "
                          "complete target joint is unavailable",
        "preregistered_test": "on N5 (uncovered=1/5) the candidate distribution is "
                              "null; a decision label containing CANDIDATE must NOT "
                              "be emitted as a positive scientific result",
        "preregistered_verdict": "FALSIFIED if decision is SYNTHETIC_CANDIDATE while "
                                 "candidate.distribution is None",
        "world": "N5_NO_POSITIVITY_UNCOVERED_MASS",
    },
    {
        "id": "F2_ADMIT_TRUE_IS_NOT_AUTHENTICATION",
        "claim_attacked": "an external admit callback returning True authenticates "
                          "owner admission",
        "preregistered_test": "admit=lambda *a: True satisfies the gate with no "
                              "identity, scope, operation or permission verification",
        "preregistered_verdict": "FALSIFIED",
        "reason": "the native docstring itself states a callback is an integration "
                  "boundary, not an authentication implementation; any evidence "
                  "item asserting owner admission from a lambda is misleading",
    },
    {
        "id": "F3_EQUWEIGHTS_NOT_SCIENTIFIC_CALIBRATION",
        "claim_attacked": "two-source equiweights constitute scientific calibration",
        "preregistered_test": "N2/N3: alpha is a normalized weight ratio; scaling "
                              "all weights by a constant leaves the estimate unchanged",
        "preregistered_verdict": "FALSIFIED",
        "world": "N3_WEIGHT_PERTURBATION",
    },
    {
        "id": "F4_SENSITIVITY_HALFWIDTH_IS_NOT_A_CONFIDENCE_INTERVAL",
        "claim_attacked": "the sensitivity halfwidth is a confidence interval",
        "preregistered_test": "with mapping/transport/target-share radii each 1/50, "
                              "the halfwidth is exactly 3/50; its coverage "
                              "probability is undefined",
        "preregistered_halfwidth": "3/50",
        "preregistered_verdict": "FALSIFIED",
        "reason": "a sensitivity envelope holds under bounded bias assumptions; it "
                  "has no sampling reference distribution and therefore no coverage "
                  "probability",
    },
    {
        "id": "F6_CONDITIONAL_VARIANCE_UNIDENTIFIED",
        "claim_attacked": "conditional uncertainty can be reported",
        "preregistered_test": "the conditional consumer returns "
                              "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED and no variance",
        "preregistered_verdict": "FALSIFIED if any conditional interval is asserted",
        "reason": "diagonal marginal design variances do not determine conditional "
                  "variance; covariance is unavailable",
    },
]

bundle = {
    "schema": "PYAT_R27_F6J_01_NEW_FROZEN_INDEPENDENT_WORLDS@1",
    "status": "FROZEN_BEFORE_CANDIDATE_TEST_OUTPUT_INSPECTION",
    "frozen_at_utc": FROZEN_AT_UTC,
    "role": "new distinct independent F6 scientific reviewer (F6J); NOT the F6C "
            "author (9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f); NOT the incomplete "
            "F6I reviewer (6d99650bed01eed8365ec38bd888741a88888a45)",
    "repository": "maidiu/rawlsing",
    "branch": "agent/reviewer-pyat-r27-f6j-independent-heterogeneous-science-completion-r1",
    "sealed_startup": "09a87efc87110cc50c129b02033730ed8feca4e8",
    "candidate_commit": "9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f",
    "prior_reviewer_commit": "6d99650bed01eed8365ec38bd888741a88888a45",
    "ordering_attestation": {
        "candidate_test_files_read_before_freeze": False,
        "candidate_junit_read_before_freeze": False,
        "candidate_verdicts_read_before_freeze": False,
        "native_method_surface_read_before_freeze": True,
        "native_method_surface_is": "the code under review (S03FO blob "
                                    "fc5e37fa5b2f0eb689593b42d95479d1327cb94c); "
                                    "reading the implementation is required to write "
                                    "an independent expectation engine and is not a "
                                    "read of candidate test output",
        "public_author_headline_values_already_disclosed_by_commission": True,
        "public_values_used_only_as": "POST_DISCLOSURE_REPLICATION, never as blind "
                                      "preregistration",
    },
    "origin_label_definitions": {
        NEW: "genuinely new to this court, frozen blind to candidate test output, "
             "values chosen by F6J",
        REPL: "built from the author's publicly disclosed headline values; CANNOT "
              "be called blind pre-freeze; replication target only",
    },
    "count_new_preregistered": sum(1 for w in worlds if w["origin"] == NEW),
    "count_post_disclosure_replication": sum(1 for w in worlds if w["origin"] == REPL),
    "perturbation_axes_covered": [
        "target_share_changes", "source_weights", "domain_category_exclusion",
        "minority_representation", "no_positivity", "source_swaps",
    ],
    "worlds": worlds,
    "pre_registered_falsifiers": falsifiers,
    "independent_expectation_engine": {
        "file": "03_SCRIPTS/expectations_engine.py",
        "imports_native_producer": False,
        "numeric_type": "fractions.Fraction only",
        "written_from": "the published standardization definition",
        "semantic_hash_used_only_for": "identity/mapping_hashes, never a scientific "
                                       "estimator",
    },
    "prohibitions": [
        "no original F6 semantic issuer", "no N9", "no OC05", "no N11", "no N12",
        "no actor authority", "no real survey bytes", "no cross-survey person",
        "no HQ method decision", "no 35-wave grant",
    ],
}

out = RET / "02_FROZEN" / "01_NEW_FROZEN_INDEPENDENT_WORLDS.json"
out.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n")
print("wrote", out.relative_to(RET))
print("worlds:", len(worlds),
      "new:", bundle["count_new_preregistered"],
      "post-disclosure:", bundle["count_post_disclosure_replication"])
print("falsifiers:", len(falsifiers))
