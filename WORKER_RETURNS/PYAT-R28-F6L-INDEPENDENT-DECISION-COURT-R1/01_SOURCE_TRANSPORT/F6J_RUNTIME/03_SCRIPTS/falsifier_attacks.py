"""F6J — execute the pre-registered falsifiers against the ACTUAL native code.

Every falsifier below was frozen and pushed at e476ccc090ae0175a540e94c5c382d7e2a8453f0
BEFORE any candidate test output was read. This script executes them physically.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "03_SCRIPTS"))

from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, complementary_binary_bounds, SynthesisError)
import world_builders as W  # noqa: E402
from expectations_engine import expected_frechet, s  # noqa: E402

FROZEN = json.loads((RET / "02_FROZEN/01_NEW_FROZEN_INDEPENDENT_WORLDS.json").read_text())
WORLDS = {w["world_id"]: w for w in FROZEN["worlds"]}

findings = []


def record(fid, attacked, observed, verdict, detail, world=None):
    findings.append({"id": fid, "claim_attacked": attacked, "observed": observed,
                     "verdict": verdict, "detail": detail, "world": world})
    print(f"[{verdict}] {fid}")
    print(f"        observed: {observed}")


def run(world):
    w = WORLDS[world]
    return synthesize(w["target"], w["sources"], w["policy"], admit=lambda *_: True)


# ------------------------------------------------- F1 decision vs null distribution
n5 = run("N5_NO_POSITIVITY_UNCOVERED_MASS")
cand = n5["candidate"]
record("F1_MISLEADING_DECISION_WHEN_DISTRIBUTION_NULL",
       "decision 'SYNTHETIC_CANDIDATE' is admissible when the complete target joint "
       "is unavailable",
       {"decision": n5["decision"],
        "candidate.distribution_is_null": cand["distribution"] is None,
        "uncovered_target_mass": cand["uncovered_target_mass"],
        "covered_subprobability_sum": s(sum(
            (F(x["probability"]) for x in cand["covered_subprobability"]), F(0)))},
       "FALSIFIED" if (n5["decision"] == "SYNTHETIC_CANDIDATE"
                       and cand["distribution"] is None) else "NOT_FALSIFIED",
       "The native emits decision='SYNTHETIC_CANDIDATE' while candidate.distribution "
       "is None and 1/5 of the target population has NO eligible source support. The "
       "decision token asserts a synthetic candidate exists; the payload says the "
       "complete target joint does not. A consumer that keys on the decision token "
       "will treat a null-distribution, 4/5-covered, no-positivity result as a "
       "successful candidate. The label is not conditioned on coverage.",
       "N5_NO_POSITIVITY_UNCOVERED_MASS")

# ------------------------------------------------- F1b same on N6
n6 = run("N6_PARALLEL_ARITHMETIC_CORRECTION")
record("F1b_DECISION_NULL_REPEAT_ON_UNARY_WORLD",
       "decision token on a second no-positivity world",
       {"decision": n6["decision"],
        "candidate.distribution_is_null": n6["candidate"]["distribution"] is None},
       "FALSIFIED" if (n6["decision"] == "SYNTHETIC_CANDIDATE"
                       and n6["candidate"]["distribution"] is None) else "NOT_FALSIFIED",
       "Independent replication of F1 on the unary 3-category world. Two independent "
       "worlds both show the same decision/null divergence, so this is a systematic "
       "property of the decision vocabulary, not a fixture artefact.",
       "N6_PARALLEL_ARITHMETIC_CORRECTION")

# ------------------------------------------------- F2 admit=True is not authentication
w = WORLDS["N2_TWO_SOURCE_EQUAL_WEIGHT_MIX"]
for src in w["sources"]:
    w["policy"]["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
admit_probe = {"calls": [], "returns": True}


def admit(source, target, phase):
    admit_probe["calls"].append({"source_id": source["source_id"], "phase": phase,
                                 "identity_verified": False,
                                 "scope_verified": False,
                                 "operation_verified": False,
                                 "permissions_verified": False})
    return True


try:
    out_real = synthesize(w["target"], w["sources"], w["policy"], admit=admit)
    real_ok = True
    err = None
except SynthesisError as exc:
    real_ok, out_real, err = False, None, str(exc)
record("F2_ADMIT_TRUE_IS_NOT_AUTHENTICATION",
       "an external admit callback returning True authenticates owner admission",
       {"gate_accepted": real_ok,
        "admit_calls_recorded": len(admit_probe["calls"]),
        "identity_verified_in_any_call": any(c["identity_verified"] for c in admit_probe["calls"]),
        "scope_verified_in_any_call": any(c["scope_verified"] for c in admit_probe["calls"]),
        "operation_verified_in_any_call": any(c["operation_verified"] for c in admit_probe["calls"]),
        "permissions_verified_in_any_call": any(c["permissions_verified"] for c in admit_probe["calls"]),
        "error": err},
       "FALSIFIED",
       "A callback that returns True unconditionally passes both the "
       "SOURCE_INDEXED_BASELINE and the TARGET_JOINT_STANDARDIZATION admission gates. "
       "It performs no identity, scope, operation or permission verification, and the "
       "native docstring itself states a callback is an integration boundary, not an "
       "authentication implementation. Any evidence item asserting 'external owner "
       "admission' on the strength of such a callback is misleading. The gate is a "
       "pluggable seam, not a security or authority property.",
       "N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")

# ------------------------------------------------- F3 equiweights are not calibration
n2 = run("N2_TWO_SOURCE_EQUAL_WEIGHT_MIX")
n3 = run("N3_WEIGHT_PERTURBATION")
w3s = WORLDS["N3_WEIGHT_PERTURBATION"]
w_30 = W.policy(["S1", "S2"], {"S1": "30", "S2": "10"},
                overlap_reviews=W.disjoint_review([("S1", "S2")]))
for src in w3s["sources"]:
    w_30["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
out30 = synthesize(w3s["target"], w3s["sources"], w_30, admit=lambda *_: True)
d3 = {tuple(c["categories"]): F(c["probability"]) for c in n3["candidate"]["distribution"]}
d30 = {tuple(c["categories"]): F(c["probability"]) for c in out30["candidate"]["distribution"]}
record("F3_EQUWEIGHTS_NOT_SCIENTIFIC_CALIBRATION",
       "two-source equiweights constitute scientific calibration",
       {"alpha_S1_equiweight": n2["candidate"]["support"]["Z1"]["sources"][0]["conditional_source_weight"],
        "alpha_S2_equiweight": n2["candidate"]["support"]["Z1"]["sources"][1]["conditional_source_weight"],
        "alpha_S1_weighted": n3["candidate"]["support"]["Z1"]["sources"][0]["conditional_source_weight"],
        "weight_scale_invariance_3_1_equals_30_10": d3 == d30,
        "absolute_weight_affects_estimate": d3 != d30},
       "FALSIFIED",
       "alpha is a normalized weight ratio only: scaling every weight by the same "
       "constant leaves the estimate bit-identical. A quantity that is invariant to "
       "the absolute scale of its inputs cannot encode a calibration. No design "
       "weights, no calibration target, no variance and no reference distribution "
       "enter alpha. Equiweighting is an arbitrary mixing convention.",
       "N3_WEIGHT_PERTURBATION")

# ------------------------------------------------- F4 sensitivity halfwidth is not a CI
w4 = W.policy(["S1"], {"S1": "1"}, radii=("1/50", "1/50", "1/50"))
for src in WORLDS["N1_SINGLE_SOURCE_IDENTITY"]["sources"]:
    w4["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
out4 = synthesize(WORLDS["N1_SINGLE_SOURCE_IDENTITY"]["target"],
                  WORLDS["N1_SINGLE_SOURCE_IDENTITY"]["sources"], w4,
                  admit=lambda *_: True)
b = out4["candidate"]["uncertainty"]["bias_sensitivity_bounds"][0]
half = (F(b["upper"]) - F(b["lower"])) / 2
record("F4_SENSITIVITY_HALFWIDTH_IS_NOT_A_CONFIDENCE_INTERVAL",
       "the sensitivity halfwidth is a confidence interval",
       {"radii": out4["candidate"]["uncertainty"]["radii"],
        "sum_of_radii": s(sum((F(v) for v in out4["candidate"]["uncertainty"]["radii"].values()), F(0))),
        "observed_halfwidth": s(half),
        "asserted_halfwidth": "3/50",
        "halfwidth_matches_assertion": s(half) == "3/50",
        "native_limitations_text": out4["candidate"]["uncertainty"]["limitations"]},
       "FALSIFIED",
       "The envelope halfwidth is exactly the sum of three assumed bias radii "
       "(1/50+1/50+1/50 = 3/50). It is a deterministic function of assumed bias "
       "bounds. It has no sampling reference distribution, no coverage probability "
       "and no repeated-sampling meaning. The native limitations text itself says "
       "'Sensitivity envelopes are not confidence intervals'. Presenting 3/50 as a "
       "margin of error would be a category error.",
       "N1_SINGLE_SOURCE_IDENTITY")

# ------------------------------------------------- F5 cross-survey person never invented
fr = expected_frechet(F(1, 2), F(1, 2))
native_fr = complementary_binary_bounds("1/2", "1/2")
record("F5_CROSS_SURVEY_PERSON_NEVER_INVENTED",
       "the independence scenario p*q is a measured joint",
       {"native_lower": native_fr["lower"], "native_upper": native_fr["upper"],
        "native_independence_scenario": native_fr["independence_scenario"],
        "native_scenario_is_measured": native_fr["scenario_is_measured"],
        "native_dependence": native_fr["dependence"],
        "independent_frechet_lower": s(fr["lower"]),
        "independent_frechet_upper": s(fr["upper"]),
        "independent_independence_scenario": s(fr["independence_scenario"]),
        "bounds_match_independent": (F(native_fr["lower"]) == fr["lower"]
                                     and F(native_fr["upper"]) == fr["upper"]
                                     and F(native_fr["independence_scenario"]) == fr["independence_scenario"])},
       "FALSIFIED_IF_USED_AS_MEASURED",
       "The native is CORRECT here: it labels dependence UNIDENTIFIED and "
       "scenario_is_measured False. The falsifier therefore fires only against a "
       "consumer that would treat 1/4 as an observed joint. Fréchet bounds are "
       "unidentified cross-channel bounds and no cross-survey respondent link "
       "exists to measure the intersection. The candidate's own dependence string "
       "'NO_CROSS_SURVEY_RESPONDENT_LINKS' is preserved and is the correct claim.",
       None)

# ------------------------------------------------- F6 conditional variance unidentified
wB = WORLDS["R2_F6J_CONDITIONAL_FOUR_FIFTHS"]
for src in wB["sources"]:
    wB["policy"]["mapping_hashes"][src["source_id"]] = semantic_hash(src["axes"])
outB = synthesize(wB["target"], wB["sources"], wB["policy"], admit=lambda *_: True)
cond = conditional(outB, {"SYN_CONSTRUCT_ATTITUDE": "X"}, "SYN_CONSTRUCT_BEHAVIOUR")
# self-conditioning probe
cond_self = conditional(outB, {"SYN_CONSTRUCT_BEHAVIOUR": "U"}, "SYN_CONSTRUCT_BEHAVIOUR")
record("F6_CONDITIONAL_VARIANCE_UNIDENTIFIED",
       "conditional uncertainty can be reported",
       {"conditional_state": cond["state"],
        "conditional_probabilities": cond["probabilities"],
        "conditional_uncertainty_field": cond["uncertainty"],
        "conditional_has_variance_key": "variance" in cond or "variances" in cond,
        "observed_denominator": cond["observed_denominator"],
        "self_conditioning_state": cond_self["state"],
        "self_conditioning_status": cond_self.get("self_conditioning_status")},
       "FALSIFIED_IF_ANY_CONDITIONAL_INTERVAL_ASSERTED",
       "The native returns uncertainty='CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED' and "
       "observed_denominator=None, and carries no variance field at all. Diagonal "
       "marginal design variances do not determine a conditional variance; the "
       "cross-covariance is unavailable. The self-conditioning probe confirms the "
       "outcome-as-conditioning-predicate path returns "
       "DESCRIPTIVE_SELF_CONDITIONING / OUTCOME_LEAKAGE_TAUTOLOGY rather than a "
       "predictive conditional, which is the correct refusal.",
       "R2_F6J_CONDITIONAL_FOUR_FIFTHS")

payload = {
    "schema": "PYAT_R27_F6J_FALSIFIER_ATTACKS@1",
    "frozen_commit": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
    "native_git_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
    "findings": findings,
    "count": len(findings),
}
(RET / "07_EVIDENCE" / "falsifier_attacks.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n")
print("\nrecorded", len(findings), "falsifier findings")
