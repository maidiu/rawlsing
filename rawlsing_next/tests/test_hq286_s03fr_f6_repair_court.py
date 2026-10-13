"""PYAT HQ286 S03FR — separately versioned independent F6 repair court.

READ-ONLY candidate. Original S03R @34cc7bdb28664ecbc707528470c2b4397aa96f12
must remain BYTE-IDENTICAL; do not edit/rename/overwrite it. This NEW test
suite pins candidate S03F @bb739fb6d60b40876566ec6320ff6eec2388e8cf.
No SAV/DTA, real source, issuer, protected CURRENT, EE13 or V3 activity.

Requires complete exact candidate tree at S03F_CANDIDATE_ROOT and its shared
module on PYTHONPATH. A missing root is a setup HOLD, not a test failure.
Tests with 'strict' express unmet consumer/issuer acceptance and are expected
RED from static code inspection; DO NOT xfail or weaken them to force green.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import os
import unittest

S03F_COMMIT = "bb739fb6d60b40876566ec6320ff6eec2388e8cf"
S03R_IMMUTABLE_COMMIT = "34cc7bdb28664ecbc707528470c2b4397aa96f12"
EXPECTED_S03F_SHA256 = "818638c937a9b1b64ac400dcb8e33337310f6c793417a1558f838edb01eb4841"
EXPECTED_S03F_GIT_BLOB = "b1b05e7d60f92357fb31cbea99e5b432415cc7b0"
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
        raise RuntimeError("HOLD: S03F file cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _exact_modules():
    raw = os.getenv("S03F_CANDIDATE_ROOT")
    if not raw:
        raise RuntimeError("HOLD: S03F_CANDIDATE_ROOT missing; no execution qualified")
    root = Path(raw).resolve()
    code = root / "rawlsing_next/pre553_heterogeneous_synthesis.py"
    fixture = root / "WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py"
    shared = root / "rawlsing_next/pre553_empirical_objects.py"
    if not all(p.is_file() for p in (code, fixture, shared)):
        raise RuntimeError("HOLD: S03F exact code/fixture/shared terrain unavailable")
    if hashlib.sha256(code.read_bytes()).hexdigest() != EXPECTED_S03F_SHA256:
        raise RuntimeError("HOLD: S03F SHA256 mismatch")
    if _git_blob_sha(code) != EXPECTED_S03F_GIT_BLOB:
        raise RuntimeError("HOLD: S03F git blob mismatch")
    if _git_blob_sha(fixture) != EXPECTED_FIXTURE_BLOB:
        raise RuntimeError("HOLD: original fixture git blob mismatch")
    if _git_blob_sha(shared) != EXPECTED_SHARED_BLOB:
        raise RuntimeError("HOLD: accepted shared semantic_hash owner mismatch")
    from rawlsing_next import pre553_empirical_objects as shared_import
    if _git_blob_sha(Path(shared_import.__file__).resolve()) != EXPECTED_SHARED_BLOB:
        raise RuntimeError("HOLD: executed shared import differs from exact code root")
    return _load(code, "hq286_s03fr_s03f_exact"), _load(fixture, "hq286_s03fr_fixture")


class S03FRIndependentRepairCourt(unittest.TestCase):
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

    def test_01_independent_keyed_four_cell_oracle_passes(self):
        bundle = self.synth()
        self.assertEqual(tuple(self.cells(bundle)[k]
                               for k in FROZEN_CONSUMER_CATEGORY_ORDER),
                         FROZEN_EXPECTED)
        self.assertEqual(sum(self.cells(bundle).values()), 1)

    def test_02_missing_native_cell_with_redistributed_support_refused(self):
        table = self.s[0]["strata"]["majority"]
        lost = table["cells"].pop()
        table["cells"][0]["n"] += lost["n"]
        table["cells"][0]["mass"] += lost["mass"]
        table.pop("design_variance", None)
        with self.assertRaisesRegex(self.method.SynthesisError,
                                    "incomplete native joint domain"):
            self.synth()

    def test_03_explicit_zero_cell_omission_still_refused(self):
        table = self.s[0]["strata"]["majority"]
        table.pop("design_variance", None)
        zero_cell = table["cells"][3]
        table["cells"][3] = dict(zero_cell, n=0, mass=0)
        table["cells"][0]["n"] += zero_cell["n"]
        table["cells"][0]["mass"] += zero_cell["mass"]
        table["cells"].pop()
        with self.assertRaisesRegex(self.method.SynthesisError,
                                    "incomplete native joint domain"):
            self.synth()

    def test_04_outcome_self_conditioning_typed_descriptive_not_predictive(self):
        r = self.method.conditional(self.synth(),
                   {"employment_position": "formal"}, "employment_position")
        self.assertEqual(r["state"], "DESCRIPTIVE_SELF_CONDITIONING")
        self.assertEqual(r["self_conditioning_status"],
                         "OUTCOME_LEAKAGE_TAUTOLOGY")
        self.assertEqual(r["probabilities"], {"formal": "1"})
        self.assertIsNone(r["observed_denominator"])
        self.assertEqual(r["evidence_mode"], "INFERRED")

    def test_05_genuine_different_variable_conditional_remains_inferred(self):
        r = self.method.conditional(self.synth(),
                   {"material_security": "secure"}, "employment_position")
        self.assertEqual(r["state"], "SUPPORTED_MODEL")
        self.assertNotIn("self_conditioning_status", r)
        self.assertEqual(r["probabilities"]["formal"], "18/23")
        self.assertEqual(r["uncertainty"],
                         "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED")

    def test_06_source_indexed_baseline_retained_and_transport_inferred(self):
        bundle = self.synth()
        self.assertEqual([b["source_id"] for b in bundle["baseline"]],
                         ["A", "B"])
        for source, baseline in zip(self.s, bundle["baseline"]):
            self.assertEqual(baseline["native_summary"], source)
            self.assertEqual(baseline["target_applicability"], "SOURCE_NATIVE_ONLY")
            self.assertIsNotNone(baseline["mapped_joint"])
        self.assertEqual(bundle["candidate"]["evidence_mode"], "INFERRED")
        self.assertIsNone(bundle["candidate"]["sample_size"])
        self.assertEqual(bundle["real_source_qualification"],
                         "EXTERNAL_REVIEW_REQUIRED")

    def test_07_minority_uncovered_refuses_complete_target_distribution(self):
        for source in self.s:
            del source["strata"]["minority"]
        bundle = self.synth()
        self.assertIsNone(bundle["candidate"]["distribution"])
        self.assertEqual(F(bundle["candidate"]["uncovered_target_mass"]), F(1, 5))
        self.assertEqual(sum(F(c["probability"])
                for c in bundle["candidate"]["covered_subprobability"]), F(4, 5))

    def test_08_unknown_design_remains_unknown(self):
        for source in self.s:
            for stratum in source["strata"].values():
                stratum.pop("design_variance", None)
        candidate = self.synth()["candidate"]
        self.assertIsNone(candidate["uncertainty"]["sampling_variance"])
        self.assertEqual(candidate["uncertainty"]["sampling_status"],
                         "UNKNOWN_DESIGN")

    def test_09_opposite_same_marginal_joints_produce_opposite_conditional(self):
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
        self.assertEqual(fn(one, {}, "employment_position")["probabilities"],
                         fn(two, {}, "employment_position")["probabilities"])

    def test_10_zero_target_support_is_not_a_confident_prediction(self):
        r = self.method.conditional(self.synth(),
               {"material_security": "unobserved"}, "employment_position")
        self.assertEqual(r["state"], "UNAVAILABLE")
        self.assertEqual(r["reason"], "CATEGORY_OUTSIDE_MAPPED_SUPPORT")

    def test_11_original_order_contract_strict_unmet(self):
        # Deliberate strict acceptance: original S03R 01 requires THIS order,
        # not a category-key normalisation applied after the fact.
        actual = [tuple(c["categories"])
                  for c in self.synth()["candidate"]["distribution"]]
        self.assertEqual(actual, list(FROZEN_CONSUMER_CATEGORY_ORDER))

    def test_12_no_new_original_source_issuer(self):
        self.s[0]["test_origin"] = False
        with self.assertRaises(self.method.SynthesisError):
            self.synth()

    def test_13_declared_domain_not_original_source_custody(self):
        # Demonstrates that an *internally self-declared* smaller domain is
        # accepted as a DIFFERENT synthetic experiment. This is NOT a waiver
        # to use such a table as an admitted original-source product.
        source = self.s[0]
        source["axes"][0]["category_map"] = {"secure": "secure"}
        for table in source["strata"].values():
            retained = [c for c in table["cells"] if c["categories"][0] == "secure"]
            missing = [c for c in table["cells"] if c["categories"][0] != "secure"]
            extra = sum(c["n"] for c in missing)
            retained[0]["n"] += extra
            retained[0]["mass"] += extra
            table["cells"] = retained
            table.pop("design_variance", None)
        from rawlsing_next.pre553_empirical_objects import semantic_hash
        self.p["mapping_hashes"]["A"] = semantic_hash(source["axes"])
        bundle = self.synth()
        self.assertEqual(bundle["baseline"][0]["native_summary"]["axes"][0]
                         ["category_map"], {"secure": "secure"})
        self.assertIsNone(bundle["candidate"])
        self.assertIn("NO_COMMON_JOINT_ESTIMAND_KEEP_COMPLEMENTARY_CHANNELS",
                      bundle["refusals"]["B"])

if __name__ == "__main__":
    unittest.main()
