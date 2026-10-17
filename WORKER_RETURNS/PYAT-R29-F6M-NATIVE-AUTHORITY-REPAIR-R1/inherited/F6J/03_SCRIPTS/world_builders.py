"""F6J synthetic sourcefree world constructors.

All identity material is synthetic. No survey bytes, no respondent links, no
real source, no person. Inputs are integers or rational strings only.
"""
from __future__ import annotations

import copy
from fractions import Fraction as F


def _axes_two(construct_a="SYN_CONSTRUCT_ATTITUDE",
              construct_b="SYN_CONSTRUCT_BEHAVIOUR",
              cats_a=("na0", "na1"), map_a=("X", "Y"),
              cats_b=("nb0", "nb1"), map_b=("U", "V")):
    return [
        {"item_ref": "SYN_ITEM_A", "construct_ref": construct_a,
         "mapping_ref": "SYN_MAP_A", "scale_ref": "SYN_SCALE_A",
         "polarity_ref": "SYN_POL_A", "instrument_ref": "SYN_INSTR_A",
         "response_semantics_ref": "SYN_RESP_A",
         "category_map": dict(zip(cats_a, map_a)),
         "review_status": "REVIEWED", "mapping_confidence": "HIGH",
         "scale_status": "REVIEWED", "polarity_status": "REVIEWED"},
        {"item_ref": "SYN_ITEM_B", "construct_ref": construct_b,
         "mapping_ref": "SYN_MAP_B", "scale_ref": "SYN_SCALE_B",
         "polarity_ref": "SYN_POL_B", "instrument_ref": "SYN_INSTR_B",
         "response_semantics_ref": "SYN_RESP_B",
         "category_map": dict(zip(cats_b, map_b)),
         "review_status": "REVIEWED", "mapping_confidence": "HIGH",
         "scale_status": "REVIEWED", "polarity_status": "REVIEWED"},
    ]


AXES2 = _axes_two()
AXES3 = _axes_two("SYN_CONSTRUCT_ATTITUDE3", "SYN_CONSTRUCT_BEHAVIOUR3",
                  ("nc0", "nc1", "nc2"), ("P", "Q", "R"),
                  ("nd0", "nd1"), ("S", "T"))

TARGET = dict(target_id="SYN_TARGET_A", geography="SYN_GEO_A",
              boundary_ref="SYN_BOUNDARY_1", population="SYN_POP_A",
              unit="SYN_UNIT_PERSON", strata_ref="SYN_STRATA_REF",
              year=2000, strata={})


def target(strata, year=2000, geography="SYN_GEO_A",
           boundary_ref="SYN_BOUNDARY_1", population="SYN_POP_A",
           unit="SYN_UNIT_PERSON", target_id="SYN_TARGET_A"):
    t = copy.deepcopy(TARGET)
    t.update(target_id=target_id, year=year, geography=geography,
             boundary_ref=boundary_ref, population=population, unit=unit)
    t["strata"] = {k: str(F(v)) for k, v in strata.items()}
    return t


def source(sid, strata_tables, axes=None, *, sample_id=None,
           product_ref=None, test_origin=True, measure_basis="UNWEIGHTED",
           geography="SYN_GEO_A", boundary_ref="SYN_BOUNDARY_1",
           population="SYN_POP_A", unit="SYN_UNIT_PERSON",
           start_year=1990, end_year=2010, axes_override=None):
    """strata_tables: {z: {"counts": {cellkey: int}, "excluded_n": int}}

    UNWEIGHTED: mass == n exactly (integers). cells are native category tuples.
    """
    axes = copy.deepcopy(axes_override if axes_override is not None
                         else (axes or AXES2))
    cells_out = {}
    for z, spec in strata_tables.items():
        counts = spec["counts"]
        cells = [{"categories": list(k), "n": int(n), "mass": int(n)}
                 for k, n in counts.items()]
        eligible_n = sum(int(n) for n in counts.values()) + int(spec.get("excluded_n", 0))
        cells_out[z] = {
            "support_ref": "SYN_SUPPORT_" + z,
            "table_status": "EXHAUSTIVE_DECLARED_JOINT_RISK_SET",
            "eligible_n": int(eligible_n),
            "excluded_n": int(spec.get("excluded_n", 0)),
            "cells": cells,
        }
        if "design_variance" in spec:
            cells_out[z]["design_variance"] = spec["design_variance"]
    return {
        "source_id": sid,
        "product_ref": product_ref or ("SYN_PRODUCT_" + sid),
        "survey_lineage": "SYN_LINEAGE_" + sid,
        "sample_id": sample_id or ("SYN_SAMPLE_" + sid),
        "risk_set_ref": "SYN_RISK_" + sid,
        "design_ref": "SYN_DESIGN_" + sid,
        "weight_ref": "SYN_WEIGHT_" + sid,
        "routing_ref": "SYN_ROUTING_" + sid,
        "missingness_ref": "SYN_MISSING_" + sid,
        "permission_ref": "SYN_PERMISSION_" + sid,
        "sampling_limitations": "SYNTHETIC_SOURCEFREE_LIMITATIONS",
        "test_origin": test_origin,
        "scope": {"geography": geography, "boundary_ref": boundary_ref,
                  "population": population, "unit": unit,
                  "fieldwork_ref": "SYN_FIELDWORK_" + sid,
                  "start_year": int(start_year), "end_year": int(end_year)},
        "axes": axes,
        "measure_basis": measure_basis,
        "dependence_kind": "MEASURED_SAME_SURVEY_JOINT",
        "coadministration_ref": "SYN_COADMIN_" + sid,
        "joint_frontier_ref": "SYN_FRONTIER_" + sid,
        "strata": cells_out,
    }


def policy(source_ids, weights, *, min_raw_support=1, maximum_joint_cells=64,
           radii=("1/10", "1/10", "1/10"), overlap_reviews=None):
    ids = sorted(source_ids)
    return {
        "source_weights": {sid: str(F(weights[sid])) for sid in ids},
        "policy_ref": "SYN_POLICY_REF",
        "scope_review_ref": "SYN_SCOPE_REVIEW_REF",
        "conditional_invariance_ref": "SYN_CONDITIONAL_INVARIANCE_REF",
        "target_support_ref": "SYN_TARGET_SUPPORT_REF",
        "conditional_invariance_status": "REVIEWED_ASSUMPTION",
        "mapping_bias_radius": radii[0],
        "transport_bias_radius": radii[1],
        "target_share_bias_radius": radii[2],
        "minimum_raw_support": int(min_raw_support),
        "maximum_joint_cells": int(maximum_joint_cells),
        "mapping_hashes": {sid: None for sid in ids},
        "overlap_reviews": overlap_reviews or {},
    }


def disjoint_review(pairs, ref="SYN_OVERLAP_REVIEW_REF"):
    return {"|".join(sorted(p)): {"status": "DISJOINT", "review_ref": ref}
            for p in pairs}


def normalised_masses(counts, axes=None):
    """Exact-rational normalized cell masses from integer counts.

    When `axes` is given the keys are converted native -> mapped so they line up
    with the native producer's `ordered_categories`.
    """
    maps = [a["category_map"] for a in axes] if axes else None
    out = {}
    for k, v in counts.items():
        key = tuple(m[x] for m, x in zip(maps, k)) if maps else k
        out[key] = out.get(key, F(0)) + F(v)
    tot = sum(out.values(), F(0))
    return {k: (v / tot if tot else F(0)) for k, v in out.items()}


def tables_from_sources(sources):
    """Extract the exact-rational MAPPED table view the expectation engine needs.

    Cell keys are MAPPED category values, matching the native producer's
    `_mapped()` and its `ordered_categories` construction.
    """
    out = {}
    for s_ in sources:
        sid = s_["source_id"]
        maps = [a["category_map"] for a in s_["axes"]]
        out[sid] = {}
        for z, t in s_["strata"].items():
            masses = {}
            for c in t["cells"]:
                k = tuple(m[v] for m, v in zip(maps, c["categories"]))
                masses[k] = masses.get(k, F(0)) + F(c["mass"])
            out[sid][z] = {"masses": masses,
                           "raw_n": sum(c["n"] for c in t["cells"])}
    return out


def construct_refs(axes):
    return [a["construct_ref"] for a in axes]
