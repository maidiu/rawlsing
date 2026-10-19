"""Recompute the frozen oracle by first principles, with NO producer imported.

This script validates 01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json itself.
It reads only the declared source-native counts and the declared target
stratum shares, and does arithmetic with fractions.Fraction. It never imports
candidate A, A0, B or C, so agreement here is not contaminated by a producer.

Deliberately a separate program from the court, so a mistake in the oracle
cannot hide inside a mistake in the candidate harness.

Two mixture rules are computed side by side:

  PLANNED-SHARE  (what method B must do): a source that carries a table for a
                 stratum but fails the aggregate support gate keeps its PLANNED
                 weight as unknown mass. Denominator is over PLANNED sources.

  RENORMALIZING  (what method A actually does): the denominator is over
                 ELIGIBLE sources only, so a dropped source's planned share is
                 silently redistributed onto survivors and unknown mass is
                 counted only when NO source is eligible.

The producer emits ONE mixed target joint, not per-stratum rows. This script
mixes the strata first and then reads the conditional off the mixed joint.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

ORACLE = Path(__file__).resolve().parents[1] / "01_FROZEN_ESTIMANDS_AND_INDEPENDENT_ORACLE.json"

SIDS = ("S_A", "S_B")
# grid order: secure|formal, secure|informal, insecure|formal, insecure|informal
W = {
    "W1": {"shares": {"majority": F(1, 2), "minority": F(1, 2)},
           "counts": {"S_A": {"majority": [40, 10, 25, 25], "minority": [25, 25, 10, 40]},
                      "S_B": {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]}},
           "min_support": 30},
    "W2": {"shares": {"majority": F(1, 2), "minority": F(1, 2)},
           "counts": {"S_A": {"majority": [40, 10, 25, 25], "minority": [4, 2, 1, 3]},
                      "S_B": {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]}},
           "min_support": 30},
    "W3": {"shares": {"majority": F(4, 5), "minority": F(1, 5)},
           "counts": {"S_A": {"majority": [40, 10, 25, 25]},
                      "S_B": {"majority": [20, 30, 25, 25]}},
           "min_support": 30},
    "W7": {"shares": {"majority": F(1, 2), "minority": F(1, 2)},
           "counts": {"S_A": {"majority": [2, 1, 1, 2], "minority": [1, 1, 1, 2]},
                      "S_B": {"majority": [20, 30, 25, 25], "minority": [40, 10, 25, 25]}},
           "min_support": 30},
}


def _eligible(world, sid, z):
    c = world["counts"][sid].get(z)
    return c is not None and sum(c) >= world["min_support"] and sum(c) > 0


def planned_share(world):
    joint = [F(0)] * 4
    uncovered = F(0)
    for z, share in world["shares"].items():
        planned = [s for s in SIDS if z in world["counts"][s]]
        eligible = [s for s in planned if _eligible(world, s, z)]
        denom, elig_w = F(len(planned)), F(len(eligible))
        missing = share * (1 - elig_w / denom) if denom else share
        uncovered += missing
        covered_share = share - missing
        if not eligible:
            continue
        for s in eligible:
            c = world["counts"][s][z]
            m = sum(c)
            for i, v in enumerate(c):
                joint[i] += covered_share * (1 / elig_w) * (F(v) / m)
    return joint, uncovered


def renormalizing(world):
    joint = [F(0)] * 4
    uncovered = F(0)
    for z, share in world["shares"].items():
        eligible = [s for s in SIDS if _eligible(world, s, z)]
        denom = F(len(eligible))
        if not denom:
            uncovered += share
            continue
        for s in eligible:
            c = world["counts"][s][z]
            m = sum(c)
            for i, v in enumerate(c):
                joint[i] += share * (1 / denom) * (F(v) / m)
    return joint, uncovered


def conditional(joint):
    """P(employment_position = o | material_security = secure), read off the
    single mixed target joint. Cells 0,1 are secure."""
    denom = joint[0] + joint[1]
    return None if not denom else (joint[0] / denom, joint[1] / denom, denom)


def main():
    frozen = json.loads(ORACLE.read_text())
    failures, checks, obs = [], 0, {}

    def eq(label, got, want):
        nonlocal checks
        checks += 1
        if str(got) != str(want):
            failures.append(f"{label}: got {got!r} want {want!r}")

    expected = {
        "W1": {"joint": ["5/16", "3/16", "17/80", "23/80"], "uncovered": "0",
               "renorm_uncovered": "0", "cond": ("5/8", "3/8", "1/2")},
        "W2": {"joint": ["1/4", "1/8", "3/16", "3/16"], "uncovered": "1/4",
               "renorm_joint": ["7/20", "3/20", "1/4", "1/4"], "renorm_uncovered": "0",
               "renorm_cond": ("7/10", "3/10", "1/2")},
        "W3": {"uncovered": "1/5", "renorm_uncovered": "1/5"},
        "W7": {"joint": ["3/20", "1/10", "1/8", "1/8"], "uncovered": "1/2",
               "renorm_joint": ["3/10", "1/5", "1/4", "1/4"], "renorm_uncovered": "0",
               "renorm_cond": ("3/5", "2/5", "1/2")},
    }

    for name, world in W.items():
        jp, up = planned_share(world)
        jr, ur = renormalizing(world)
        obs[name] = {"planned_share_joint": [str(x) for x in jp],
                     "planned_share_uncovered": str(up),
                     "renormalizing_joint": [str(x) for x in jr],
                     "renormalizing_uncovered": str(ur)}
        e = expected[name]
        eq(f"{name}.planned_share_uncovered", up, e["uncovered"])
        eq(f"{name}.renormalizing_uncovered", ur, e["renorm_uncovered"])
        if "joint" in e:
            for i, want in enumerate(e["joint"]):
                eq(f"{name}.planned_share_joint[{i}]", jp[i], want)
            eq(f"{name}.planned_share_joint_sums_to", sum(jp), 1 - up)
        if "renorm_joint" in e:
            for i, want in enumerate(e["renorm_joint"]):
                eq(f"{name}.renormalizing_joint[{i}]", jr[i], want)
            eq(f"{name}.renormalizing_joint_sums_to", sum(jr), 1)
        for tag, jv in (("cond", jp), ("renorm_cond", jr)):
            if tag in e:
                f, i, d = conditional(jv)
                eq(f"{name}.{tag}.formal", f, e[tag][0])
                eq(f"{name}.{tag}.informal", i, e[tag][1])
                eq(f"{name}.{tag}.denominator", d, e[tag][2])

    # The decisive structural claim: A reports full coverage while B does not.
    for name in ("W2", "W7"):
        eq(f"{name}.divergence_A_says_covered_B_does_not",
           (obs[name]["renormalizing_uncovered"] == "0"
            and obs[name]["planned_share_uncovered"] != "0"), "True")

    # frozen-file agreement
    c1 = frozen["cases"]["W1_full_coverage_disjoint"]["oracle"]
    for i, k in enumerate(("secure|formal", "secure|informal",
                           "insecure|formal", "insecure|informal")):
        eq(f"frozen.W1[{k}]", c1["joint_cell_probabilities_in_declared_order"][k],
           expected["W1"]["joint"][i])
    eq("frozen.W1.uncovered", c1["uncovered_target_mass"], expected["W1"]["uncovered"])
    eq("frozen.W1.cond.formal", c1["conditional_probabilities"]["formal"], expected["W1"]["cond"][0])
    eq("frozen.W1.cond.informal", c1["conditional_probabilities"]["informal"], expected["W1"]["cond"][1])
    eq("frozen.W1.cond.denom", c1["conditional_model_denominator_mass"], expected["W1"]["cond"][2])

    c2 = frozen["cases"]["W2_mixed_eligibility_trap"]["oracle"]
    eq("frozen.W2.uncovered", c2["uncovered_target_mass"], expected["W2"]["uncovered"])
    for i, k in enumerate(("secure|formal", "secure|informal",
                           "insecure|formal", "insecure|informal")):
        eq(f"frozen.W2.covered[{k}]", c2["covered_subprobability_in_declared_order"][k],
           expected["W2"]["joint"][i])
    eq("frozen.W2.covered_sums_to", c2["covered_subprobability_sums_to"], "3/4")
    eq("frozen.W2.A.tidy_point_formal",
       c2["method_A_tidy_point"]["conditional_probabilities"]["formal"],
       expected["W2"]["renorm_cond"][0])
    eq("frozen.W2.A.tidy_point_informal",
       c2["method_A_tidy_point"]["conditional_probabilities"]["informal"],
       expected["W2"]["renorm_cond"][1])
    eq("frozen.W2.A.uncovered", c2["method_A_tidy_point"]["uncovered_target_mass"], "0")

    c7 = frozen["cases"]["W7_source_excluded_all_strata"]["oracle"]
    eq("frozen.W7.uncovered", c7["expected_uncovered_target_mass"], expected["W7"]["uncovered"])
    eq("frozen.W7.A.uncovered", c7["method_A_tidy_point"]["uncovered_target_mass"],
       expected["W7"]["renorm_uncovered"])

    c3 = frozen["cases"]["W3_minority_whole_stratum_absent"]["oracle"]
    eq("frozen.W3.uncovered", c3["uncovered_target_mass"], expected["W3"]["uncovered"])

    print(json.dumps({
        "checks": checks,
        "failures": failures,
        "verdict": "ORACLE_SELFCHECK_PASS" if not failures else "ORACLE_SELFCHECK_FAIL",
        "observations": obs,
        "decisive_finding": (
            "In W2 and W7 the renormalizing rule (method A) reports "
            "uncovered_target_mass = 0 and emits a confident point, while the "
            "planned-share rule (method B) reports 1/4 and 1/2 unknown mass "
            "respectively. Method A cannot distinguish a stratum that was "
            "adequately measured from one whose planned evidence was "
            "partly destroyed."),
    }, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())