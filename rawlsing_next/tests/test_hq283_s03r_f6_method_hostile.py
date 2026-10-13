"""S03R independent hostile court: requires exact separate S03 checkout.
NOT executed by browser reviewer. Do NOT run this against user survey files.
Run only after setting S03_CANDIDATE_ROOT to checked-out SHA
69a1686528bb46c2db3051a75710989a46fe5c45. This module does not
merge or copy candidate implementation into reviewer branch.
"""
import hashlib
import importlib.util
import os
import unittest
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

EXPECTED_SHA = "818638c937a9b1b64ac400dcb8e33337310f6c793417a1558f838edb01eb4841"
EXPECTED_FIXTURE_GIT_BLOB = "8e4902df9ef9e6fa63e8e28617543257b8d40b28"
EXPECTED_SHARED_HASHING_GIT_BLOB = "a61365b994e5c3c50de0f598fcf40e90abf757b6"


def _git_blob_sha(path):
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()



def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("candidate module cannot be loaded")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _candidate_modules():
    root_text = os.getenv("S03_CANDIDATE_ROOT")
    if not root_text:
        raise RuntimeError("HOLD: S03_CANDIDATE_ROOT absent; no project runtime executed")
    root = Path(root_text).resolve()
    impl = root / "rawlsing_next/pre553_heterogeneous_synthesis.py"
    fixtures = root / "WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py"
    if not impl.is_file() or not fixtures.is_file():
        raise RuntimeError("HOLD: exact S03 candidate files unavailable")
    if hashlib.sha256(impl.read_bytes()).hexdigest() != EXPECTED_SHA:
        raise RuntimeError("HOLD: candidate SHA256 mismatch")
    if _git_blob_sha(fixtures) != EXPECTED_FIXTURE_GIT_BLOB:
        raise RuntimeError("HOLD: frozen S03 fixture Git blob identity mismatch")
    shared = root / "rawlsing_next/pre553_empirical_objects.py"
    if not shared.is_file() or _git_blob_sha(shared) != EXPECTED_SHARED_HASHING_GIT_BLOB:
        raise RuntimeError("HOLD: S03 semantic_hash dependency mismatch")
    from rawlsing_next import pre553_empirical_objects as loaded_shared
    if _git_blob_sha(Path(loaded_shared.__file__).resolve()) != EXPECTED_SHARED_HASHING_GIT_BLOB:
        raise RuntimeError("HOLD: executed import resolves a different shared dependency")
    return _load(impl, "hq283_s03r_exact_candidate"), _load(fixtures, "hq283_s03r_fixture")


def _tv(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / 2


class S03RIndependentHostiles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.method, cls.fixture = _candidate_modules()

    def setUp(self):
        self.t, self.s, self.p = self.fixture.fixtures()

    def run_candidate(self):
        return self.method.synthesize(self.t, self.s, self.p)

    def dist(self, bundle):
        return [F(x["probability"]) for x in bundle["candidate"]["distribution"]]

    def test_01_independent_four_cell_oracle(self):
        got = self.dist(self.run_candidate())
        self.assertEqual(got, list(map(F, ["27/50", "3/20", "11/100", "1/5"])))
        A = list(map(F, ["16/25", "1/10", "1/10", "4/25"]))
        B = list(map(F, ["1/5", "1/5", "9/50", "21/50"]))
        held = list(map(F, ["27/50", "3/20", "11/100", "1/5"]))
        bad = list(map(F, ["1/10", "1/10", "1/10", "7/10"]))
        self.assertEqual((_tv(A, held), _tv(B, held), _tv(got, held)),
                         (F(1, 10), F(17, 50), F(0)))
        self.assertEqual((_tv(A, bad), _tv(B, bad), _tv(got, bad)),
                         (F(27, 50), F(7, 25), F(1, 2)))

    def test_02_opposite_joints_same_marginals(self):
        self.s = self.s[:1]
        self.p["source_weights"] = {"A": 1}
        for z in self.s[0]["strata"].values():
            z.pop("design_variance", None)
            z["eligible_n"] = 100
            for cell, n in zip(z["cells"], [50, 0, 0, 50]):
                cell.update(n=n, mass=n)
        aligned = self.run_candidate()
        for z in self.s[0]["strata"].values():
            for cell, n in zip(z["cells"], [0, 50, 50, 0]):
                cell.update(n=n, mass=n)
        anti = self.run_candidate()
        fn = self.method.conditional
        x = {"material_security": "secure"}
        self.assertEqual(fn(aligned, x, "employment_position")["probabilities"]["formal"], "1")
        self.assertEqual(fn(anti, x, "employment_position")["probabilities"]["formal"], "0")
        self.assertEqual(fn(aligned, {}, "employment_position")["probabilities"],
                         fn(anti, {}, "employment_position")["probabilities"])

    def test_03_uncovered_target_not_renormalized(self):
        for source in self.s:
            del source["strata"]["minority"]
        b = self.run_candidate()
        self.assertIsNone(b["candidate"]["distribution"])
        self.assertEqual(F(b["candidate"]["uncovered_target_mass"]), F(1, 5))
        self.assertEqual(sum(F(x["probability"]) for x in b["candidate"]["covered_subprobability"]), F(4, 5))

    def test_04_population_shift_rejected(self):
        self.s[1]["scope"]["population"] = "different survey eligibility"
        b = self.run_candidate()
        self.assertIsNone(b["candidate"])
        self.assertIn("TARGET_SCOPE_MISMATCH", b["refusals"]["B"])

    def test_05_unequal_design_unknown_not_precision_claim(self):
        self.s[0]["measure_basis"] = "WEIGHTED"
        for z in self.s[0]["strata"].values():
            z.pop("design_variance", None)
            z["cells"][0]["mass"] *= 2
        b = self.run_candidate()
        self.assertIsNone(b["candidate"]["uncertainty"]["sampling_variance"])
        self.assertEqual(b["candidate"]["uncertainty"]["sampling_status"], "UNKNOWN_DESIGN")

    def test_06_nonadmitted_real_source_held(self):
        self.s[0]["test_origin"] = False
        with self.assertRaises(self.method.SynthesisError):
            self.run_candidate()

    def test_07_missing_native_joint_cell_must_not_be_silent_zero(self):
        # ADVERSARIAL REPAIR EXPECTATION. Conserves eligible count, and lies
        # about exhaustive status while omitting an original domain category.
        # Expected to FAIL in current S03 until explicit zero-domain proof.
        majority = self.s[0]["strata"]["majority"]
        lost = majority["cells"].pop()
        majority["cells"][0]["n"] += lost["n"]
        majority["cells"][0]["mass"] += lost["mass"]
        majority.pop("design_variance", None)
        with self.assertRaises(self.method.SynthesisError):
            self.run_candidate()

    def test_08_outcome_predicate_requires_tautology_warning(self):
        # ADVERSARIAL REPAIR EXPECTATION. Expected to FAIL current S03;
        # descriptive P(Y|Y) is not predictive information.
        b = self.run_candidate()
        r = self.method.conditional(b, {"employment_position": "formal"}, "employment_position")
        self.assertEqual(r["probabilities"], {"formal": "1"})
        self.assertEqual(r.get("self_conditioning_status"), "OUTCOME_LEAKAGE_TAUTOLOGY")

    def test_09_distinct_family_issuer_is_not_implied(self):
        # General estimator may work on same-family samples, but a real F6
        # two-original-family product would still require external issuance.
        self.s[1]["survey_lineage"] = self.s[0]["survey_lineage"]
        b = self.run_candidate()
        self.assertIsNotNone(b["candidate"])
        self.assertEqual(b["real_source_qualification"], "EXTERNAL_REVIEW_REQUIRED")
        self.assertIsNone(b["candidate"]["sample_size"])

    def test_10_inferred_conditional_uncertainty_stays_unknown(self):
        b = self.run_candidate()
        r = self.method.conditional(b, {"material_security": "secure"}, "employment_position")
        self.assertEqual(r["evidence_mode"], "INFERRED")
        self.assertIsNone(r["observed_denominator"])
        self.assertEqual(r["uncertainty"], "CONDITIONAL_UNCERTAINTY_NOT_IDENTIFIED")

    def test_11_complementary_binary_only_frechet_not_measured_joint(self):
        b = self.method.complementary_binary_bounds("3/5", "7/10")
        self.assertEqual((b["lower"], b["upper"]), ("3/10", "3/5"))
        self.assertEqual(b["independence_scenario"], "21/50")
        self.assertIs(b["scenario_is_measured"], False)


if __name__ == "__main__":
    unittest.main()
