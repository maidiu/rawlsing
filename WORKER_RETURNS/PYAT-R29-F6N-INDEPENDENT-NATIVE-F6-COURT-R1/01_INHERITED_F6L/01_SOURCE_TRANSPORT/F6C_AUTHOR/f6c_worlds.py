"""F6C frozen world fixtures: build the two declared sourcefree study worlds.

Pure construction from 01_FROZEN_SOURCEFREE_STUDY_WORLDS.json. No expected value
is computed here; every expected number lives in the frozen world file and is
asserted by the court. Contract-shaped only: integers / rational strings,
required target_id, complete native joint domains, DISJOINT overlap reviews.
"""
from __future__ import annotations

from copy import deepcopy
from fractions import Fraction as F
from itertools import product

CELLS = [("secure", "formal"), ("secure", "informal"),
         ("insecure", "formal"), ("insecure", "informal")]

NATIVE_CODES = {
    "A": {"material_security": ["secure", "insecure"],
          "employment_position": ["formal", "informal"]},
    "B": {"material_security": ["C1", "C2"],
          "employment_position": ["E1", "E2"]},
}
NATIVE_LABELS = {
    "material_security": ["secure", "insecure"],
    "employment_position": ["formal", "informal"],
}

CONSTRUCTS = ["material_security", "employment_position"]


def _axes(sid: str) -> list:
    out = []
    for i, construct in enumerate(CONSTRUCTS):
        codes = NATIVE_CODES[sid][construct]
        labels = NATIVE_LABELS[construct]
        out.append({
            "item_ref": f"synthetic-{sid}-item-{i}@1",
            "construct_ref": construct,
            "mapping_ref": f"synthetic-{sid}-mapping-{i}@1",
            "mapping_confidence": "HIGH",
            "review_status": "REVIEWED",
            "scale_ref": "named-categories@1",
            "scale_status": "REVIEWED",
            "polarity_ref": "categories-not-score@1",
            "polarity_status": "REVIEWED",
            "instrument_ref": f"synthetic-{sid}-instrument@1",
            "response_semantics_ref": f"synthetic-{sid}-named-response-meanings@1",
            # declared order is insertion order; S03FO canonical order depends on it
            "category_map": dict(zip(codes, labels)),
        })
    return out


def _source(sid: str, tag: str, target: dict, counts: dict) -> dict:
    s = {
        "source_id": sid,
        "product_ref": f"synthetic-{tag}-{sid}-joint-product@1",
        "survey_lineage": f"synthetic-survey-{tag}-{sid}",
        "sample_id": f"independent-{tag}-{sid}",
        "test_origin": True,
        "risk_set_ref": f"synthetic-{tag}-{sid}-eligible-asked-complete@1",
        "design_ref": f"synthetic-{tag}-{sid}-stratified-SRS-fixed-n@1",
        "weight_ref": "unit-weight@1",
        "routing_ref": f"synthetic-{tag}-shared-eligibility@1",
        "missingness_ref": "synthetic-no-missing@1",
        "sampling_limitations": ("Invented fixed-stratum SRS tables; no real-source "
                                 "design/coverage validation"),
        "permission_ref": "SYNTHETIC_ONLY",
        "scope": {k: target[k] for k in ("geography", "boundary_ref", "population", "unit")},
        "measure_basis": "UNWEIGHTED",
        "dependence_kind": "MEASURED_SAME_SURVEY_JOINT",
        "coadministration_ref": f"synthetic-{tag}-{sid}-coadministration@1",
        "joint_frontier_ref": f"synthetic-{tag}-two-item-complete@1",
        "axes": _axes(sid),
        "strata": {},
    }
    s["scope"].update(start_year=target["year"], end_year=target["year"],
                      fieldwork_ref=target["clock"]["fieldwork_ref"])
    for z, cat in counts.items():
        n = sum(cat)
        # COMPLETE native joint domain: full cross-product of the two axes'
        # native category codes, in declared (category_map insertion) order.
        native0 = list(NATIVE_CODES[sid]["material_security"])
        native1 = list(NATIVE_CODES[sid]["employment_position"])
        grid = list(product(native0, native1))
        # mapped (recoded) label grid, same declared order as the native grid
        lab0 = NATIVE_LABELS["material_security"]
        lab1 = NATIVE_LABELS["employment_position"]
        grid_mapped = list(product(lab0, lab1))
        assert len(grid) == len(cat), (sid, z, len(grid), len(cat))
        s["strata"][z] = {
            "eligible_n": n, "excluded_n": 0,
            "table_status": "EXHAUSTIVE_DECLARED_JOINT_RISK_SET",
            "support_ref": f"synthetic-{tag}-{sid}-{z}-support@1",
            "cells": [{"categories": [a, b], "n": v, "mass": v}
                      for (a, b), v in zip(grid, cat)],
            "design_variance": {
                # The native contract requires design variances to be supplied
                # ALREADY for the MAPPED cell probabilities, i.e. keyed by the
                # recoded label, not by the source-native category code.
                "method_ref": "SYNTHETIC_FIXED_STRATUM_MULTINOMIAL_PLUGIN@1",
                "cells": [{"categories": [m0, m1],
                           "variance": str(F(v, n) * (1 - F(v, n)) / n)}
                          for (n0, n1), (m0, m1), v in zip(grid, grid_mapped, cat)],
            },
        }
    return s


def _policy(tag: str, target: dict, sids, overlap_pair, review_ref) -> dict:
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    return {
        "policy_ref": f"synthetic-{tag}-standardization-decision@1",
        "scope_review_ref": f"synthetic-{tag}-scope-review@1",
        "conditional_invariance_ref": f"synthetic-{tag}-equal-risk-set-law-assumption@1",
        "conditional_invariance_status": "REVIEWED_ASSUMPTION",
        "target_support_ref": target["strata_ref"],
        "minimum_raw_support": 1,
        "maximum_joint_cells": 64,
        "source_weights": {s: 1 for s in sids},
        "mapping_hashes": {},   # filled by caller (needs semantic_hash of axes)
        "overlap_reviews": {overlap_pair: {"status": "DISJOINT",
                                           "review_ref": review_ref}},
        # NOTE: integers / rational strings only. A float here is the documented
        # cause of the prior F6B smoke SynthesisError.
        "mapping_bias_radius": "1/100",
        "transport_bias_radius": "1/20",
        "target_share_bias_radius": 0,
    }


def world_a() -> tuple:
    target = {"target_id": "SYNTHETIC_F6C_WORLD_A_2012_ADULT_WORK_RISK_SET",
              "geography": "Synthetic Region A", "boundary_ref": "synthetic-boundary-A@1",
              "year": 2012,
              "population": "resident adults in shared eligible/asked work risk set",
              "unit": "adult respondent", "strata_ref": "synthetic-population-register-A@1",
              "strata": {"majority": "4/5", "minority": "1/5"},
              "clock": {"start_year": 2012, "end_year": 2012,
                        "fieldwork_ref": "synthetic-2012-A@1"}}
    counts = {"A": {"majority": [64, 10, 10, 16], "minority": [16, 10, 10, 64]},
              "B": {"majority": [56, 10, 10, 24], "minority": [24, 10, 10, 56]}}
    sources = [_source(sid, "F6CA", target, counts[sid]) for sid in ("A", "B")]
    policy = _policy("F6CA", target, ("A", "B"), "A|B",
                     "synthetic-independent-sampling@1")
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    policy["mapping_hashes"] = {s["source_id"]: semantic_hash(s["axes"]) for s in sources}
    return target, sources, policy


def world_b() -> tuple:
    target = {"target_id": "SYNTHETIC_F6C_WORLD_B_2012_ADULT_WORK_RISK_SET",
              "geography": "Synthetic Region B", "boundary_ref": "synthetic-boundary-B@1",
              "year": 2012,
              "population": "resident adults in shared eligible/asked work risk set",
              "unit": "adult respondent", "strata_ref": "synthetic-population-register-B@1",
              "strata": {"majority": "3/5", "minority": "1/5", "remote_territory": "1/5"},
              "clock": {"start_year": 2012, "end_year": 2012,
                        "fieldwork_ref": "synthetic-2012-B@1"}}
    counts = {"A": {"majority": [70, 10, 10, 10], "minority": [10, 10, 10, 70]},
              "B": {"majority": [10, 10, 10, 70], "minority": [70, 10, 10, 10]}}
    sources = [_source(sid, "F6CB", target, counts[sid]) for sid in ("A", "B")]
    policy = _policy("F6CB", target, ("A", "B"), "A|B",
                     "synthetic-independent-sampling-B@1")
    from rawlsing_next.pre553_empirical_objects import semantic_hash
    policy["mapping_hashes"] = {s["source_id"]: semantic_hash(s["axes"]) for s in sources}
    return target, sources, policy


def naive_pooled_mixture(sources) -> list:
    """Explicit comparison computation (NOT a producer output).

    Equal-weight mixture of the two source POOLED joints, ignoring the target's
    stratum composition. Native category codes are recoded to mapped labels so
    the two sources are comparable. Used only to quantify what stratum
    conditioning buys. This is my analysis, not a native producer output.
    """
    from fractions import Fraction as Fr
    label0 = dict(zip(NATIVE_CODES["B"]["material_security"], NATIVE_LABELS["material_security"]))
    label1 = dict(zip(NATIVE_CODES["B"]["employment_position"], NATIVE_LABELS["employment_position"]))
    pooled = {}
    for s in sources:
        acc = {}
        for table in s["strata"].values():
            for c in table["cells"]:
                a0, a1 = c["categories"]
                k = (label0.get(a0, a0), label1.get(a1, a1))
                acc[k] = acc.get(k, Fr(0)) + Fr(c["mass"])
        tot = sum(acc.values(), Fr(0))
        for k, v in acc.items():
            pooled[k] = pooled.get(k, Fr(0)) + v / tot
    n = len(sources)
    return [str(pooled.get(k, Fr(0)) / n) for k in CELLS]
