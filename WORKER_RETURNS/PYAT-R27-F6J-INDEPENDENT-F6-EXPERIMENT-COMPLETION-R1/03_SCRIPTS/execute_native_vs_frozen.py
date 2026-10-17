"""F6J — execute the ACTUAL pinned native producer on the frozen worlds.

Compares real native output against the expectations this reviewer froze and
pushed at e476ccc090ae0175a540e94c5c382d7e2a8453f0 BEFORE reading any candidate
test output.

Native under test: pre553_heterogeneous_synthesis.py
  git blob fc5e37fa5b2f0eb689593b42d95479d1327cb94c
  candidate staging commit 9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f
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
    synthesize, conditional, complementary_binary_bounds, SynthesisError,
    METHOD)
from expectations_engine import s, l1  # noqa: E402

FROZEN = json.loads((RET / "02_FROZEN/01_NEW_FROZEN_INDEPENDENT_WORLDS.json").read_text())


def cells_to_map(cells):
    return {tuple(c["categories"]): F(c["probability"]) for c in cells}


def run_world(w):
    target = w["target"]
    sources = w["sources"]
    policy = w["policy"]
    out = synthesize(target, sources, policy, admit=lambda *_: True)
    cand = out["candidate"]
    e = w["expectations"]
    exp_joint = {eval(k) if k.startswith("(") else k: F(v)
                 for k, v in e["joint"].items()}
    exp_lower = {eval(k): F(v) for k, v in e["lower"].items()}
    exp_upper = {eval(k): F(v) for k, v in e["upper"].items()}
    obs = {
        "world_id": w["world_id"],
        "origin": w["origin"],
        "decision": out["decision"],
        "test_origin": out["test_origin"],
        "refusals": out["refusals"],
        "overlap_diagnostics": out["overlap_diagnostics"],
    }
    checks = []
    if cand is None:
        obs["candidate"] = None
        checks.append(("candidate_present", False, False))
    else:
        dist = (cells_to_map(cand["distribution"])
                if cand["distribution"] is not None else None)
        covered = cells_to_map(cand["covered_subprobability"])
        bounds = {(tuple(b["categories"])):
                  (F(b["lower"]), F(b["upper"]))
                  for b in cand["uncertainty"]["source_disagreement_and_uncovered_bounds"]}
        sens = {(tuple(b["categories"])):
                (F(b["lower"]), F(b["upper"]))
                for b in cand["uncertainty"]["bias_sensitivity_bounds"]}
        obs["candidate"] = {
            "ordered_categories": [list(k) for k in cand["ordered_categories"]],
            "distribution": ({str(k): s(v) for k, v in sorted(dist.items())}
                             if dist is not None else None),
            "covered_subprobability": {str(k): s(v) for k, v in sorted(covered.items())},
            "uncovered_target_mass": cand["uncovered_target_mass"],
            "lower": {str(k): s(bounds[k][0]) for k in sorted(bounds)},
            "upper": {str(k): s(bounds[k][1]) for k in sorted(bounds)},
            "bias_sensitivity": {str(k): [s(sens[k][0]), s(sens[k][1])]
                                 for k in sorted(sens)},
            "sampling_status": cand["uncertainty"]["sampling_status"],
            "sampling_variance": cand["uncertainty"]["sampling_variance"],
            "limitations": cand["uncertainty"]["limitations"],
            "dependence": cand["dependence"],
            "sample_size": cand["sample_size"],
        }
        # --- comparisons against the frozen independent expectations ---
        checks.append(("joint_matches_frozen", covered == exp_joint, True))
        checks.append(("uncovered_matches_frozen",
                       F(cand["uncovered_target_mass"]) == e_uncovered(e), True))
        checks.append(("lower_matches_frozen",
                       {k: bounds[k][0] for k in bounds} == exp_lower, True))
        checks.append(("upper_matches_frozen",
                       {k: bounds[k][1] for k in bounds} == exp_upper, True))
        checks.append(("distribution_null_matches_frozen",
                       (dist is None) == bool(e["distribution_is_null"]), True))
        if dist is not None:
            checks.append(("distribution_equals_covered_when_fully_covered",
                           dist == covered, True))
        exp_sums = F(e["covered_subprobability_sum"])
        checks.append(("covered_sum_matches_frozen",
                       sum(covered.values(), F(0)) == exp_sums, True))
    obs["checks"] = [{"name": n, "observed": o, "expected": x, "pass": o == x}
                     for n, o, x in checks]
    return obs


def e_uncovered(e):
    return F(e["uncovered_target_mass"])


def main():
    results = [run_world(w) for w in FROZEN["worlds"]]
    total = sum(len(r["checks"]) for r in results)
    passed = sum(1 for r in results for c in r["checks"] if c["pass"])
    payload = {
        "schema": "PYAT_R27_F6J_NATIVE_VS_FROZEN_EXECUTION@1",
        "native_method": METHOD,
        "native_git_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
        "candidate_commit": "9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f",
        "frozen_commit": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
        "admit_callback": "lambda *a: True  (deliberately unqualified; see falsifier F2)",
        "comparisons_total": total,
        "comparisons_passed": passed,
        "comparisons_failed": total - passed,
        "worlds": results,
    }
    out = RET / "07_EVIDENCE" / "native_vs_frozen.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"native vs frozen: {passed}/{total} comparisons match")
    for r in results:
        bad = [c for c in r["checks"] if not c["pass"]]
        flag = "OK " if not bad else "DIFF"
        print(f"  {flag} {r['world_id']:52s} decision={r['decision']}")
        for c in bad:
            print(f"        - {c['name']}: observed={c['observed']} expected={c['expected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
