"""F6N Phase-A additional falsifiers, built on the frozen F6L worlds.

These are reviewer-side sourcefree constructions only.  No author code is
edited and no original survey data is touched.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[2]
F6L = RET / "01_INHERITED_F6L"
sys.path.insert(0, str(F6L / "02_PHASE_A/03_SCRIPTS"))
sys.path.insert(0, str(F6L / "01_STAGED_NATIVE"))

import f6l_worlds as W  # noqa: E402


def rare_renormalization(threshold=150):
    """3-category world: R1 has a rare cell and is excluded by total support.

    R1 total 100: the rare (HIGH, NO)=0 / (HIGH, YES)=1 cell lives only here.
    R2 total 200 survives threshold 150.  A complete R2-only joint would silently
    renormalize away R1's target share and the rare-category information.
    """
    target = W.target({"Z1": "1"})
    r1 = W.source("R1", {"Z1": {
        ("m0", "a0"): 1, ("m0", "a1"): 49,
        ("m1", "a0"): 25, ("m1", "a1"): 24,
        ("m2", "a0"): 0, ("m2", "a1"): 1,
    }}, W.AXES3)
    r2 = W.source("R2", {"Z1": {
        ("m0", "a0"): 25, ("m0", "a1"): 25,
        ("m1", "a0"): 25, ("m1", "a1"): 25,
        ("m2", "a0"): 50, ("m2", "a1"): 50,
    }}, W.AXES3)
    return W.seal({
        "world_id": "F6N_RARE_CATEGORY_RENORMALIZATION",
        "target": target,
        "sources": [r1, r2],
        "policy": W.policy(("R1", "R2"), {"R1": 1, "R2": 1},
                           min_raw_support=threshold),
        "axes": ["F6L_MATERIAL3", "F6L_ACTION3"],
        "labels": [["LOW", "MID", "HIGH"], ["NO", "YES"]],
    })


def positive_world():
    w = W.positive_2x2()
    w = copy.deepcopy(w)
    w["world_id"] = "F6N_POSITIVE_COMPLETE_SOURCEFREE"
    return w


def scope_mismatch():
    w = positive_world()
    w["sources"][0]["scope"]["population"] = "F6N_FOREIGN_POPULATION"
    return W.seal(w)


def mapping_hash_substitution():
    w = positive_world()
    # Change the source mapping material but deliberately leave the frozen
    # policy mapping hash at the pristine value.
    w["sources"][0]["axes"][0]["category_map"] = {
        "m0": "LOWX", "m1": "HIGHX"}
    return w


def product_ref_substitution():
    w = positive_world()
    a, b = w["sources"]
    a["product_ref"], b["product_ref"] = b["product_ref"], a["product_ref"]
    return W.seal(w)


def duplicate_source_identity():
    w = positive_world()
    a, b = w["sources"]
    b["product_ref"] = a["product_ref"]
    b["survey_lineage"] = a["survey_lineage"]
    b["sample_id"] = a["sample_id"]
    return W.seal(w)
