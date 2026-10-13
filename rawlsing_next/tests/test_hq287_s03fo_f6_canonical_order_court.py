"""PYAT HQ287 S03FO — separately versioned F6 canonical output-order repair court.

READ-ONLY candidate. Original S03R @34cc7bdb must remain BYTE-IDENTICAL.
This NEW test suite pins candidate S03FO. No SAV/DTA, real source, issuer,
protected CURRENT, EE13 or V3 activity.

Requires complete exact candidate tree at S03FO_CANDIDATE_ROOT and its shared
module on PYTHONPATH. A missing root is a setup HOLD, not a test failure.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import os
import unittest

EXPECTED_S03FO_SHA256 = "ef76ee4f48cc74cc38e0dcf55a3190362d4b55975d3a367ddb43fbadd43a9869"
EXPECTED_S03FO_GIT_BLOB = "fc5e37fa5b2f0eb689593b42d95479d1327cb94c"
EXPECTED_FIXTURE_BLOB = "8e4902df9ef9e6fa63e8e28617543257b8d40b28"
EXPECTED_SHARED_BLOB = "a61365b994e5c3c50de0f598fcf40e90abf757b6"
FROZEN_CONSUMER_CATEGORY_ORDER = (
    ("secure", "formal"), ("secure", "informal"),
    ("insecure", "formal"), ("insecure", "informal"),
)
FROZEN_EXPECTED = tuple(map(F, ("27/50", "3/20", "11/100", "1/5")))


def _git_blob_sha(p: Path) -> str:
    content = p.read_bytes()
    return hashlib.sha1(
        ("blob " + str(len(content)) + "\0").encode("ascii") + content
    ).hexdigest()


def _load(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("HOLD: S03FO file cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exact_modules():
    raw = os.getenv("S03FO_CANDIDATE_ROOT")
    if not raw:
        raise RuntimeError("HOLD: S03FO_CANDIDATE_ROOT missing; no execution qualified")
    root = Path(raw).resolve()
    code = root / "rawlsing_next/pre553_heterogeneous_synthesis.py"
    fixture = root / "WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py"
    shared = root / "rawlsing_next/pre553_empirical_objects.py"
    if not all(p.is_file() for p in (code, fixture, shared)):
        raise RuntimeError("HOLD: S03FO exact code/fixture/shared terrain unavailable")
    if hashlib.sha256(code.read_bytes()).hexdigest() != EXPECTED_S03FO_SHA256:
        raise RuntimeError("HOLD: S03FO SHA256 mismatch")
    if _git_blob_sha(code) != EXPECTED_S03FO_GIT_BLOB:
        raise RuntimeError("HOLD: S03FO git blob mismatch")
    if _git_blob_sha(fixture) != EXPECTED_FIXTURE_BLOB:
        raise RuntimeError("HOLD: original fixture git blob mismatch")
    if _git_blob_sha(shared) != EXPECTED_SHARED_BLOB:
        raise RuntimeError("HOLD: accepted shared semantic_hash owner mismatch")
    from rawlsing_next import pre553_empirical_objects as shared_import
    if _git_blob_sha(Path(shared_import.__file__).resolve()) != EXPECTED_SHARED_BLOB:
        raise RuntimeError("HOLD: executed shared import differs from exact code root")
    return _load(code, "hq287_s03fo_exact"), _load(fixture, "hq287_s03fo_fixture")


class S03FOCanonicalOrderCourt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.method, cls.fixture = _exact_modules()

    def setUp(self):
        self.t, self.s, self.p = self.fixture.fixtures()

    def synth(self):
        return self.method.synthesize(self.t, self.s, self.p)

    def cells(self, bundle):
        return {tuple(row["categories"]): F(row["probability"])
                for row in bundle["candidate"]["distribution"]}

    def test_01_canonical_order_matches_frozen_consumer_contract(self):
        bundle = self.synth()
        actual = [tuple(c["categories"])
                  for c in bundle["candidate"]["distribution"]]
        self.assertEqual(actual, list(FROZEN_CONSUMER_CATEGORY_ORDER))

    def test_02_keyed_fractions_match_frozen_expected(self):
        bundle = self.synth()
        self.assertEqual(tuple(self.cells(bundle)[k]
                               for k in FROZEN_CONSUMER_CATEGORY_ORDER),
                         FROZEN_EXPECTED)
        self.assertEqual(sum(self.cells(bundle).values()), 1)

    def test_03_ordered_categories_field_present(self):
        bundle = self.synth()
        self.assertEqual(bundle["candidate"]["ordered_categories"],
                         [list(k) for k in FROZEN_CONSUMER_CATEGORY_ORDER])

    def test_04_missing_native_cell_refused(self):
        table = self.s[0]["strata"]["majority"]
        lost = table["cells"].pop()
        table["cells"][0]["n"] += lost["n"]
        table["cells"][0]["mass"] += lost["mass"]
        table.pop("design_variance", None)
        with self.assertRaisesRegex(self.method.SynthesisError,
                                    "incomplete native joint domain"):
            self.synth()

    def test_05_outcome_self_conditioning_typed_descriptive(self):
        r = self.method.conditional(self.synth(),
                   {"employment_position": "formal"}, "employment_position")
        self.assertEqual(r["state"], "DESCRIPTIVE_SELF_CONDITIONING")
        self.assertEqual(r["self_conditioning_status"],
                         "OUTCOME_LEAKAGE_TAUTOLOGY")
        self.assertEqual(r["probabilities"], {"formal": "1"})

    def test_06_genuine_conditional_remains_supported(self):
        r = self.method.conditional(self.synth(),
                   {"material_security": "secure"}, "employment_position")
        self.assertEqual(r["state"], "SUPPORTED_MODEL")
        self.assertNotIn("self_conditioning_status", r)
        self.assertEqual(r["probabilities"]["formal"], "18/23")

    def test_07_source_indexed_baseline_retained(self):
        bundle = self.synth()
        self.assertEqual([b["source_id"] for b in bundle["baseline"]],
                         ["A", "B"])
        for baseline in bundle["baseline"]:
            self.assertEqual(baseline["target_applicability"], "SOURCE_NATIVE_ONLY")
            self.assertIsNotNone(baseline["mapped_joint"])

    def test_08_minority_uncovered_refuses_complete_distribution(self):
        for source in self.s:
            del source["strata"]["minority"]
        bundle = self.synth()
        self.assertIsNone(bundle["candidate"]["distribution"])
        self.assertEqual(F(bundle["candidate"]["uncovered_target_mass"]), F(1, 5))

    def test_09_unknown_design_remains_unknown(self):
        for source in self.s:
            for stratum in source["strata"].values():
                stratum.pop("design_variance", None)
        candidate = self.synth()["candidate"]
        self.assertIsNone(candidate["uncertainty"]["sampling_variance"])
        self.assertEqual(candidate["uncertainty"]["sampling_status"],
                         "UNKNOWN_DESIGN")

    def test_10_opposite_joints_produce_opposite_conditional(self):
        self.s = self.s[:1]
        self.p["source_weights"] = {"A": 1}
        for t in self.s[0]["strata"].values():
            t.pop("design_variance", None)
            t["eligible_n"] = 100
            for c, n in zip(t["cells"], (50, 0, 0, 50)):
                c.update(n=n, mass=n)
        one = self.synth()
        for t in self.s[0]["strata"].values():
            for c, n in zip(t["cells"], (0, 50, 50, 0)):
                c.update(n=n, mass=n)
        two = self.synth()
        fn = self.method.conditional
        self.assertEqual(fn(one, {"material_security": "secure"},
                            "employment_position")["probabilities"]["formal"], "1")
        self.assertEqual(fn(two, {"material_security": "secure"},
                            "employment_position")["probabilities"]["formal"], "0")

    def test_11_zero_support_is_not_confident_prediction(self):
        r = self.method.conditional(self.synth(),
               {"material_security": "unobserved"}, "employment_position")
        self.assertEqual(r["state"], "UNAVAILABLE")
        self.assertEqual(r["reason"], "CATEGORY_OUTSIDE_MAPPED_SUPPORT")

    def test_12_no_new_original_source_issuer(self):
        self.s[0]["test_origin"] = False
        with self.assertRaises(self.method.SynthesisError):
            self.synth()

    def test_13_category_keys_not_reassigned(self):
        bundle = self.synth()
        for row in bundle["candidate"]["distribution"]:
            self.assertEqual(len(row["categories"]), 2)
            self.assertIn(row["categories"][0], ("secure", "insecure"))
            self.assertIn(row["categories"][1], ("formal", "informal"))


if __name__ == "__main__":
    unittest.main()
