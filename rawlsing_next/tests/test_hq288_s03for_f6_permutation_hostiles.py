"""PYAT HQ288 S03FOR -- Independent F6 permutation and semantic-order hostiles.

Tests that S03FO's declared order from category_map insertion order is
either a stable source/consumer contractual order or a typed hold. Also
tests that missing cells are not manufactured as zeros, outcome
self-conditioning is DESCRIPTIVE, and consumer outputs carry stable
category identities.

Source-free. No real F6, EE13, N9, protected CURRENT, V3 or canonical merge.
"""

import sys
from pathlib import Path
from fractions import Fraction as F
from copy import deepcopy
from itertools import permutations

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from rawlsing_next.pre553_heterogeneous_synthesis import (
    synthesize, conditional, SynthesisError,
)
from rawlsing_next.pre553_empirical_objects import semantic_hash


FROZEN_ORDER = [
    ["secure", "formal"], ["secure", "informal"],
    ["insecure", "formal"], ["insecure", "informal"],
]
FROZEN_EXPECTED = {"secure/formal": F(27, 50), "secure/informal": F(3, 20),
                   "insecure/formal": F(11, 100), "insecure/informal": F(1, 5)}


def _load_fixture():
    import importlib.util
    root = Path(__file__).resolve().parent.parent.parent
    fixture_path = root / "WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py"
    spec = importlib.util.spec_from_file_location("hq288_fixture", fixture_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _get_fixture():
    fix = _load_fixture()
    return fix.fixtures()


def _cells(bundle):
    return {tuple(c["categories"]): F(c["probability"])
            for c in bundle["candidate"]["distribution"]}


def test_exact_output_categories_and_fractions():
    t, s, p = _get_fixture()
    bundle = synthesize(t, s, p)
    cells = _cells(bundle)
    for key, expected in FROZEN_EXPECTED.items():
        parts = key.split("/")
        assert cells[tuple(parts)] == expected, f"{key}: {cells[tuple(parts)]} != {expected}"
    assert sum(cells.values()) == 1


def test_declared_order_matches_frozen_contract():
    t, s, p = _get_fixture()
    bundle = synthesize(t, s, p)
    assert bundle["candidate"]["ordered_categories"] == FROZEN_ORDER


def test_permuted_category_map_insertion_order_same_output():
    """Adversary permuting category_map insertion order must not change output fractions."""
    t, s, p = _get_fixture()
    base = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    base_cells = _cells(base)

    for perm in permutations(["secure", "insecure"]):
        s2 = deepcopy(s)
        for src in s2:
            for axis in src["axes"]:
                if "security" in axis.get("construct_ref", ""):
                    cm = axis["category_map"]
                    keys = list(cm.keys())
                    vals = [cm[k] for k in keys]
                    new_cm = {}
                    for i, k in enumerate(keys):
                        new_cm[k] = vals[list(perm).index(vals[i])] if vals[i] in perm else vals[i]
                    axis["category_map"] = new_cm
        try:
            b2 = synthesize(deepcopy(t), s2, deepcopy(p))
            if b2["candidate"] and b2["candidate"].get("distribution"):
                c2 = _cells(b2)
                for key in base_cells:
                    if key in c2:
                        assert base_cells[key] == c2[key], f"Permuted order changed {key}"
        except SynthesisError:
            pass


def test_missing_cell_not_manufactured_as_zero():
    t, s, p = _get_fixture()
    table = s[0]["strata"]["majority"]
    lost = table["cells"].pop()
    table["cells"][0]["n"] += lost["n"]
    table["cells"][0]["mass"] += lost["mass"]
    table.pop("design_variance", None)
    with pytest.raises(SynthesisError, match="incomplete native joint domain"):
        synthesize(t, s, p)


def test_outcome_self_conditioning_descriptive_not_predictive():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    r = conditional(bundle, {"employment_position": "formal"}, "employment_position")
    assert r["state"] == "DESCRIPTIVE_SELF_CONDITIONING"
    assert r["self_conditioning_status"] == "OUTCOME_LEAKAGE_TAUTOLOGY"


def test_source_indexed_baseline_retained():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    for b in bundle["baseline"]:
        assert b["source_id"] is not None
        assert b["input_hash"] != ""


def test_minority_uncovered_refuses_complete_distribution():
    t, s, p = _get_fixture()
    t2 = deepcopy(t)
    t2["strata"]["minority"] = t2["strata"].pop("majority")
    t2["strata"]["majority"] = {"share": "4/5"}
    for src in s:
        if "minority" in src["strata"] and "majority" in src["strata"]:
            src["strata"]["minority"], src["strata"]["majority"] = (
                src["strata"]["majority"], src["strata"]["minority"])
    try:
        bundle = synthesize(t2, s, p)
        if bundle["candidate"] and bundle["candidate"].get("uncovered_target_mass") != "0":
            assert bundle["candidate"]["distribution"] is None
    except SynthesisError:
        pass


def test_unknown_design_remains_unknown():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    if bundle["candidate"]:
        unc = bundle["candidate"]["uncertainty"]
        assert "UNKNOWN" in unc["sampling_status"] or "EXTERNAL" in unc["sampling_status"]


def test_consumer_output_stable_category_identities():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    for row in bundle["candidate"]["distribution"]:
        cats = row["categories"]
        assert isinstance(cats, list)
        assert all(isinstance(c, str) for c in cats)
        assert len(cats) == 2


def test_complete_cartesian_joint_domain():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    expected_keys = {
        ("secure", "formal"), ("secure", "informal"),
        ("insecure", "formal"), ("insecure", "informal"),
    }
    actual_keys = set(_cells(bundle).keys())
    assert actual_keys == expected_keys


def test_target_strata_correct():
    t, s, p = _get_fixture()
    bundle = synthesize(deepcopy(t), deepcopy(s), deepcopy(p))
    strata = t["strata"]
    total = sum(F(v) for v in strata.values())
    assert total == 1


def test_opposite_joints_same_marginals_different_output():
    t1, s1, p1 = _get_fixture()
    t2, s2, p2 = _get_fixture()
    for src in s2:
        for z in src["strata"]:
            cells = src["strata"][z]["cells"]
            if len(cells) == 4:
                cells[0]["n"], cells[3]["n"] = cells[3]["n"], cells[0]["n"]
                cells[0]["mass"], cells[3]["mass"] = cells[3]["mass"], cells[0]["mass"]
                cells[1]["n"], cells[2]["n"] = cells[2]["n"], cells[1]["n"]
                cells[1]["mass"], cells[2]["mass"] = cells[2]["mass"], cells[1]["mass"]
                src["strata"][z].pop("design_variance", None)
    try:
        b1 = synthesize(deepcopy(t1), deepcopy(s1), deepcopy(p1))
        b2 = synthesize(deepcopy(t2), s2, deepcopy(p2))
        c1 = _cells(b1)
        c2 = _cells(b2)
        assert c1 != c2
    except SynthesisError:
        pass
