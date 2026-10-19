"""F6L Phase-A sourcefree world constructors.

All identities are synthetic.  No survey bytes, respondents, persons or real
sources.  Numeric inputs are integers/rational strings.  Input construction is
independent of the native producer; mapping hashes use the published canonical
JSON rule locally, not an import of the producer.
"""
from __future__ import annotations

import copy
import hashlib
import json

from fractions import Fraction as F

TARGET_BASE = {
    "target_id": "F6L_SYN_TARGET",
    "geography": "F6L_SYN_GEO",
    "boundary_ref": "F6L_SYN_BOUNDARY",
    "population": "F6L_SYN_POP",
    "unit": "F6L_SYN_PERSON_UNIT",
    "strata_ref": "F6L_SYN_STRATA_REF",
    "year": 2001,
}


def _semantic_hash(value):
    material = json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _axes(construct_a, construct_b, codes_a, labels_a, codes_b, labels_b):
    return [
        {"item_ref": "F6L_ITEM_A", "construct_ref": construct_a,
         "mapping_ref": "F6L_MAP_A", "scale_ref": "F6L_SCALE_A",
         "polarity_ref": "F6L_POL_A", "instrument_ref": "F6L_INSTR_A",
         "response_semantics_ref": "F6L_RESP_A",
         "category_map": dict(zip(codes_a, labels_a)),
         "review_status": "REVIEWED", "mapping_confidence": "HIGH",
         "scale_status": "REVIEWED", "polarity_status": "REVIEWED"},
        {"item_ref": "F6L_ITEM_B", "construct_ref": construct_b,
         "mapping_ref": "F6L_MAP_B", "scale_ref": "F6L_SCALE_B",
         "polarity_ref": "F6L_POL_B", "instrument_ref": "F6L_INSTR_B",
         "response_semantics_ref": "F6L_RESP_B",
         "category_map": dict(zip(codes_b, labels_b)),
         "review_status": "REVIEWED", "mapping_confidence": "HIGH",
         "scale_status": "REVIEWED", "polarity_status": "REVIEWED"},
    ]


AXES2 = _axes("F6L_MATERIAL", "F6L_ACTION",
              ("m0", "m1"), ("LOW", "HIGH"),
              ("a0", "a1"), ("NO", "YES"))
AXES3 = _axes("F6L_MATERIAL3", "F6L_ACTION3",
              ("m0", "m1", "m2"), ("LOW", "MID", "HIGH"),
              ("a0", "a1"), ("NO", "YES"))


def target(strata):
    t = copy.deepcopy(TARGET_BASE)
    t["strata"] = {k: str(F(v)) for k, v in strata.items()}
    return t


def source(sid, strata_counts, axes=None, *, test_origin=True,
           product_ref=None, sample_id=None):
    """strata_counts: {z: {native_cell_tuple: count}}; complete cross-product.

    The caller supplies every cell of the declared native domain, including
    observed zeroes, because the native contract refuses silently omitted cells.
    """
    axes = copy.deepcopy(axes or AXES2)
    native_grid = [tuple(pair) for pair in
                   __import__("itertools").product(*[list(a["category_map"]) for a in axes])]
    source = {
        "source_id": sid,
        "product_ref": product_ref or ("F6L_PRODUCT_" + sid),
        "survey_lineage": "F6L_LINEAGE_" + sid,
        "sample_id": sample_id or ("F6L_SAMPLE_" + sid),
        "risk_set_ref": "F6L_RISK_" + sid,
        "design_ref": "F6L_DESIGN_" + sid,
        "weight_ref": "F6L_WEIGHT_" + sid,
        "routing_ref": "F6L_ROUTING_" + sid,
        "missingness_ref": "F6L_MISSING_" + sid,
        "permission_ref": "F6L_PERMISSION_" + sid,
        "sampling_limitations": "F6L_SYNTHETIC_SOURCEFREE_ONLY",
        "test_origin": bool(test_origin),
        "scope": {"geography": TARGET_BASE["geography"],
                  "boundary_ref": TARGET_BASE["boundary_ref"],
                  "population": TARGET_BASE["population"],
                  "unit": TARGET_BASE["unit"],
                  "fieldwork_ref": "F6L_FIELDWORK_" + sid,
                  "start_year": 1995, "end_year": 2005},
        "axes": axes,
        "measure_basis": "UNWEIGHTED",
        "dependence_kind": "MEASURED_SAME_SURVEY_JOINT",
        "coadministration_ref": "F6L_COADMIN_" + sid,
        "joint_frontier_ref": "F6L_FRONTIER_" + sid,
        "strata": {},
    }
    for z, counts in strata_counts.items():
        missing = [k for k in native_grid if k not in counts]
        extra = [k for k in counts if k not in native_grid]
        if missing or extra:
            raise ValueError(f"{sid}/{z}: incomplete native domain missing={missing} extra={extra}")
        cells = [{"categories": list(k), "n": int(counts[k]), "mass": int(counts[k])}
                 for k in native_grid]
        source["strata"][z] = {
            "support_ref": "F6L_SUPPORT_" + sid + "_" + z,
            "table_status": "EXHAUSTIVE_DECLARED_JOINT_RISK_SET",
            "eligible_n": sum(int(v) for v in counts.values()),
            "excluded_n": 0,
            "cells": cells,
        }
    return source


def policy(source_ids, weights, *, min_raw_support=1, maximum_joint_cells=64,
           radii=("1/10", "1/10", "1/10"), overlap_reviews=None):
    ids = sorted(source_ids)
    return {
        "source_weights": {sid: str(F(weights[sid])) for sid in ids},
        "policy_ref": "F6L_POLICY_REF",
        "scope_review_ref": "F6L_SCOPE_REVIEW_REF",
        "conditional_invariance_ref": "F6L_CONDITIONAL_INVARIANCE_REF",
        "target_support_ref": TARGET_BASE["strata_ref"],
        "conditional_invariance_status": "REVIEWED_ASSUMPTION",
        "mapping_bias_radius": radii[0],
        "transport_bias_radius": radii[1],
        "target_share_bias_radius": radii[2],
        "minimum_raw_support": int(min_raw_support),
        "maximum_joint_cells": int(maximum_joint_cells),
        "mapping_hashes": {sid: None for sid in ids},
        "overlap_reviews": (
            {"|".join(sorted(p)): {"status": "DISJOINT", "review_ref": "F6L_OVERLAP_REVIEW_REF"}
             for p in overlap_reviews}
            if overlap_reviews is not None else
            {"|".join(sorted(p)): {"status": "DISJOINT", "review_ref": "F6L_OVERLAP_REVIEW_REF"}
             for p in _pairs(ids)}
        ),
    }


def _pairs(ids):
    out = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            out.append((a, b))
    return out


def seal(world):
    """Fill mapping hashes after all source fields (and test flags) are final."""
    for src in world["sources"]:
        world["policy"]["mapping_hashes"][src["source_id"]] = _semantic_hash(src["axes"])
    return world


def tables_for_engine(world):
    out = {}
    for src in world["sources"]:
        maps = [a["category_map"] for a in src["axes"]]
        per = {}
        for z, table in src["strata"].items():
            masses = {}
            for cell in table["cells"]:
                key = tuple(m[value] for m, value in zip(maps, cell["categories"]))
                masses[key] = masses.get(key, F(0)) + F(cell["mass"])
            per[z] = {"masses": masses, "raw_n": sum(c["n"] for c in table["cells"])}
        out[src["source_id"]] = per
    return out


# --------------------------------------------------------------------------
# Original F6C World B: original uncovered-mass world, exact author bytes.
# --------------------------------------------------------------------------
def original_f6c_world_b(f6c_worlds):
    target, sources, policy = f6c_worlds.world_b()
    return {"world_id": "F6L_P1_ORIGINAL_F6C_WORLD_B_UNCOVERED",
            "target": copy.deepcopy(target),
            "sources": copy.deepcopy(sources),
            "policy": copy.deepcopy(policy),
            "axes": ["material_security", "employment_position"],
            "labels": [["secure", "insecure"], ["formal", "informal"]],
            "origin": "ORIGINAL_F6C_AUTHOR_WORLD_B",
            "note": "Exact author fixture bytes; not modified."}


# --------------------------------------------------------------------------
# P2: novel 2x2, second target stratum uncovered by every source.
# --------------------------------------------------------------------------
def novel_2x2_no_positivity():
    w = {"world_id": "F6L_P2_NOVEL_2X2_UNCOVERED_THIRD",
         "target": target({"Z1": "2/3", "Z2": "1/3"}),
         "sources": [
             source("A", {"Z1": {("m0", "a0"): 7, ("m0", "a1"): 3,
                                  ("m1", "a0"): 5, ("m1", "a1"): 5}}),
             source("B", {"Z1": {("m0", "a0"): 2, ("m0", "a1"): 8,
                                  ("m1", "a0"): 6, ("m1", "a1"): 4}}),
         ],
         "policy": policy(("A", "B"), {"A": 1, "B": 1}),
         "axes": ["F6L_MATERIAL", "F6L_ACTION"],
         "labels": [["LOW", "HIGH"], ["NO", "YES"]],
         "origin": "F6L_PREREGISTERED_NEW"}
    return seal(w)


# --------------------------------------------------------------------------
# P3: novel 3x2, second target stratum uncovered.
# --------------------------------------------------------------------------
def novel_3cat_no_positivity():
    grid_a = {("m0", "a0"): 10, ("m0", "a1"): 5,
              ("m1", "a0"): 15, ("m1", "a1"): 10,
              ("m2", "a0"): 5, ("m2", "a1"): 5}
    grid_b = {("m0", "a0"): 5, ("m0", "a1"): 10,
              ("m1", "a0"): 5, ("m1", "a1"): 15,
              ("m2", "a0"): 10, ("m2", "a1"): 5}
    w = {"world_id": "F6L_P3_NOVEL_3X2_UNCOVERED_QUARTER",
         "target": target({"Z1": "3/4", "Z2": "1/4"}),
         "sources": [source("A3", {"Z1": grid_a}, AXES3),
                     source("B3", {"Z1": grid_b}, AXES3)],
         "policy": policy(("A3", "B3"), {"A3": 1, "B3": 1}),
         "axes": ["F6L_MATERIAL3", "F6L_ACTION3"],
         "labels": [["LOW", "MID", "HIGH"], ["NO", "YES"]],
         "origin": "F6L_PREREGISTERED_NEW"}
    return seal(w)


# --------------------------------------------------------------------------
# P4/P7/P10/P11: genuine complete target positive, asymmetric weights.
# --------------------------------------------------------------------------
def positive_2x2():
    w = {"world_id": "F6L_P11_COMPLETE_POSITIVE",
         "target": target({"Z1": "1/2", "Z2": "1/2"}),
         "sources": [
             source("S1", {"Z1": {("m0", "a0"): 3, ("m0", "a1"): 1,
                                   ("m1", "a0"): 1, ("m1", "a1"): 1},
                            "Z2": {("m0", "a0"): 1, ("m0", "a1"): 1,
                                   ("m1", "a0"): 1, ("m1", "a1"): 3}}),
             source("S2", {"Z1": {("m0", "a0"): 1, ("m0", "a1"): 1,
                                   ("m1", "a0"): 1, ("m1", "a1"): 3},
                            "Z2": {("m0", "a0"): 3, ("m0", "a1"): 1,
                                   ("m1", "a0"): 1, ("m1", "a1"): 1}}),
         ],
         "policy": policy(("S1", "S2"), {"S1": 3, "S2": 1}),
         "axes": ["F6L_MATERIAL", "F6L_ACTION"],
         "labels": [["LOW", "HIGH"], ["NO", "YES"]],
         "origin": "F6L_PREREGISTERED_NEW"}
    return seal(w)


def positive_2x2_substituted():
    """Same identities/weights as positive_2x2, S2 source table substituted."""
    w = positive_2x2()
    w["world_id"] = "F6L_P10_SOURCE_SUBSTITUTION"
    w["sources"][1]["strata"]["Z1"]["cells"] = [
        {"categories": ["m0", "a0"], "n": 2, "mass": 2},
        {"categories": ["m0", "a1"], "n": 2, "mass": 2},
        {"categories": ["m1", "a0"], "n": 1, "mass": 1},
        {"categories": ["m1", "a1"], "n": 1, "mass": 1},
    ]
    w["sources"][1]["strata"]["Z2"]["cells"] = [
        {"categories": ["m0", "a0"], "n": 1, "mass": 1},
        {"categories": ["m0", "a1"], "n": 2, "mass": 2},
        {"categories": ["m1", "a0"], "n": 2, "mass": 2},
        {"categories": ["m1", "a1"], "n": 1, "mass": 1},
    ]
    for z in ("Z1", "Z2"):
        w["sources"][1]["strata"][z]["eligible_n"] = 6
    # mapping hashes are unchanged: only the table changed, not the axes
    return seal(w)


# --------------------------------------------------------------------------
# P5/P8: distributed source support and a minority cell that is not a gate.
# --------------------------------------------------------------------------
def distributed_support(min_raw_support=1):
    w = {"world_id": "F6L_P8_DISTRIBUTED_SUPPORT_MINORITY",
         "target": target({"Z1": "1"}),
         "sources": [
             source("S1", {"Z1": {("m0", "a0"): 3, ("m0", "a1"): 47,
                                   ("m1", "a0"): 25, ("m1", "a1"): 25}}),
             source("S2", {"Z1": {("m0", "a0"): 50, ("m0", "a1"): 50,
                                   ("m1", "a0"): 50, ("m1", "a1"): 50}}),
         ],
         "policy": policy(("S1", "S2"), {"S1": 1, "S2": 1},
                          min_raw_support=min_raw_support),
         "axes": ["F6L_MATERIAL", "F6L_ACTION"],
         "labels": [["LOW", "HIGH"], ["NO", "YES"]],
         "origin": "F6L_PREREGISTERED_NEW"}
    return seal(w)


def with_origin(world, test_origin):
    """Return a deep copy with every source's caller-declared test flag set."""
    w = copy.deepcopy(world)
    for src in w["sources"]:
        src["test_origin"] = bool(test_origin)
    return seal(w)


def mixed_origin(world):
    """Make S1 real and S2 caller-declared test origin."""
    w = copy.deepcopy(world)
    w["sources"][0]["test_origin"] = False
    w["sources"][1]["test_origin"] = True
    return seal(w)
