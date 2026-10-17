import importlib.util
from pathlib import Path
from copy import deepcopy
from fractions import Fraction as F
import unittest

from rawlsing_next.pre553_heterogeneous_synthesis import (
    synthesize, conditional, complementary_binary_bounds, SynthesisError,
)
from rawlsing_next.pre553_empirical_objects import semantic_hash

RETURN = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1"
spec = importlib.util.spec_from_file_location("s03_fixtures", RETURN / "repro/fixtures.py")
fixture_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture_module)
fixtures = fixture_module.fixtures


def table(bundle):
    return {tuple(c["categories"]): F(c["probability"]) for c in bundle["candidate"]["distribution"]}


class HeterogeneousSynthesisTests(unittest.TestCase):
    def setUp(self):
        self.t, self.s, self.p = fixtures()

    def run_method(self):
        return synthesize(self.t, self.s, self.p)

    def test_frozen_expected_target_joint(self):
        expected = dict(zip(fixture_module.CELLS, map(F, ["27/50", "3/20", "11/100", "1/5"])))
        self.assertEqual(table(self.run_method()), expected)

    def test_add_remove_reweight_value_effect(self):
        equal = self.run_method()
        self.p["source_weights"]["A"] = 3
        triple = self.run_method()
        self.assertEqual([table(triple)[k] for k in fixture_module.CELLS], list(map(F, ["14/25", "1/8", "21/200", "21/100"])))
        del self.p["source_weights"]["B"]
        self.s.pop()
        only = self.run_method()
        self.assertEqual([table(only)[k] for k in fixture_module.CELLS], list(map(F, ["29/50", "1/10", "1/10", "11/50"])))
        receipts = [conditional(b, {"material_security": "secure"}, "employment_position") for b in [only, equal, triple]]
        self.assertEqual([F(r["probabilities"]["formal"]) for r in receipts], [F(29,34), F(18,23), F(112,137)])
        self.assertEqual(len({r["values_read_hash"] for r in receipts}), 3)

    def test_native_joints_and_support_are_preserved(self):
        b = self.run_method()
        for original, result in zip(self.s, b["baseline"]):
            self.assertEqual(result["native_summary"], original)
            self.assertEqual(result["input_hash"], semantic_hash(original))
        self.assertIsNone(b["candidate"]["sample_size"])
        self.assertEqual(b["candidate"]["evidence_mode"], "INFERRED")

    def test_population_time_boundary_unit_refusal(self):
        for key, value in [("population", "children"), ("unit", "household"), ("geography", "other"), ("boundary_ref", "different")]:
            with self.subTest(key=key):
                t = deepcopy(self.t); t[key] = value
                b = synthesize(t, self.s, self.p)
                self.assertIsNone(b["candidate"])
                self.assertIn("TARGET_SCOPE_MISMATCH", b["refusals"]["A"])
        self.t["year"] = 2013
        self.assertIn("TIME_NOT_APPLICABLE", self.run_method()["refusals"]["B"])

    def test_wrong_scale_polarity_and_mapping_preimage(self):
        for field in ["scale_ref", "polarity_ref", "category_map"]:
            with self.subTest(field=field):
                s = deepcopy(self.s)
                s[1]["axes"][0][field] = {"1": "insecure", "2": "secure"} if field == "category_map" else "wrong"
                b = synthesize(self.t, s, self.p)
                self.assertIsNone(b["candidate"])
                self.assertIsNone(b["baseline"][1]["mapped_joint"])
                self.assertIn("MAPPING_REVIEW_PREIMAGE_MISMATCH", b["refusals"]["B"])
        self.s[0]["axes"][0]["scale_status"] = "BLOCKED"
        self.assertIn("SCALE_OR_POLARITY_UNQUALIFIED", self.run_method()["refusals"]["A"])

    def test_unqualified_atlas_mapping_keeps_native(self):
        self.s[0]["axes"][0]["mapping_confidence"] = "LOW"
        b = self.run_method()
        self.assertIsNone(b["candidate"])
        self.assertIsNone(b["baseline"][0]["mapped_joint"])
        self.assertEqual(b["baseline"][0]["native_summary"], self.s[0])

    def test_overlap_alias_duplicate_and_unknown(self):
        self.p["overlap_reviews"] = {}
        self.assertEqual(self.run_method()["overlap_diagnostics"][0]["reason"], "OVERLAP_UNRESOLVED")
        self.p["overlap_reviews"]["A|B"] = {"status": "DISJOINT", "review_ref": "claimed"}
        self.s[1]["sample_id"] = self.s[0]["sample_id"]
        self.s[1]["survey_lineage"] = self.s[0]["survey_lineage"]
        b = self.run_method()
        self.assertEqual(b["overlap_diagnostics"][0]["reason"], "DUPLICATE_SAMPLE")
        self.assertEqual(len(b["baseline"]), 2)

    def test_duplicate_source_id_rejected(self):
        self.s.append(deepcopy(self.s[0]))
        with self.assertRaises(SynthesisError): self.run_method()

    def test_fabricated_joint_rejected(self):
        self.s[0]["dependence_kind"] = "INDEPENDENT_MARGINALS"
        with self.assertRaises(SynthesisError): self.run_method()

    def test_complementary_constructs_backoff_and_frechet(self):
        self.s[1]["axes"][0]["construct_ref"] = "life_satisfaction"
        b = self.run_method()
        self.assertIsNone(b["candidate"])
        self.assertIn("NO_COMMON_JOINT_ESTIMAND_KEEP_COMPLEMENTARY_CHANNELS", b["refusals"]["B"])
        bounds = complementary_binary_bounds("3/5", "7/10")
        self.assertEqual((bounds["lower"], bounds["upper"], bounds["independence_scenario"]), ("3/10", "3/5", "21/50"))
        self.assertFalse(bounds["scenario_is_measured"])

    def test_minority_and_rare_pattern_not_pruned(self):
        b = self.run_method()
        self.assertEqual(b["candidate"]["support"]["minority"]["target_share"], "1/5")
        self.assertTrue(all(v > 0 for v in table(b).values()))
        self.assertEqual(b["baseline"][0]["native_summary"]["strata"]["minority"]["cells"][0]["n"], 1)

    def test_missing_stratum_no_renormalization(self):
        for s in self.s: del s["strata"]["minority"]
        b = self.run_method()
        self.assertIsNone(b["candidate"]["distribution"])
        self.assertEqual(b["candidate"]["uncovered_target_mass"], "1/5")
        self.assertEqual(sum(F(c["probability"]) for c in b["candidate"]["covered_subprobability"]), F(4,5))
        self.assertEqual(conditional(b, {}, "employment_position")["state"], "UNAVAILABLE")
        self.assertTrue(all(F(x["upper"]) - F(x["lower"]) >= F(1,5) for x in b["candidate"]["uncertainty"]["source_disagreement_and_uncovered_bounds"]))

    def test_union_support_local_weights_explicit(self):
        del self.s[0]["strata"]["minority"]
        b = self.run_method()
        self.assertIsNotNone(b["candidate"]["distribution"])
        z = b["candidate"]["support"]["minority"]
        self.assertEqual(z["excluded_sources"], ["A"])
        self.assertEqual(z["sources"][0]["coefficient"], "1/5")

    def test_design_variance_inflation_and_unknown(self):
        before = self.run_method()["candidate"]["uncertainty"]["sampling_variance"]
        for s in self.s:
            for t in s["strata"].values():
                for c in t["design_variance"]["cells"]: c["variance"] = str(4 * F(c["variance"]))
        after = self.run_method()["candidate"]["uncertainty"]["sampling_variance"]
        self.assertEqual([F(c["variance"]) for c in after], [4 * F(c["variance"]) for c in before])
        del self.s[0]["strata"]["majority"]["design_variance"]
        u = self.run_method()["candidate"]["uncertainty"]
        self.assertIsNone(u["sampling_variance"])
        self.assertEqual(u["sampling_status"], "UNKNOWN_DESIGN")

    def test_bias_uncertainty_expands_without_changing_point(self):
        before = self.run_method()
        self.p["transport_bias_radius"] = "1/5"
        after = self.run_method()
        self.assertEqual(table(before), table(after))
        for x,y in zip(before["candidate"]["uncertainty"]["bias_sensitivity_bounds"], after["candidate"]["uncertainty"]["bias_sensitivity_bounds"]):
            self.assertLessEqual(F(y["lower"]), F(x["lower"]))
            self.assertGreaterEqual(F(y["upper"]), F(x["upper"]))

    def test_equal_marginals_opposite_joints(self):
        self.s = self.s[:1]; self.p["source_weights"] = {"A": 1}
        for z in self.s[0]["strata"].values():
            z.pop("design_variance")
            z["eligible_n"] = 100
            for c,n in zip(z["cells"], [50,0,0,50]): c.update(n=n, mass=n)
        aligned = self.run_method()
        for z in self.s[0]["strata"].values():
            for c,n in zip(z["cells"], [0,50,50,0]): c.update(n=n, mass=n)
        opposite = self.run_method()
        self.assertEqual(conditional(aligned, {}, "employment_position")["probabilities"], conditional(opposite, {}, "employment_position")["probabilities"])
        self.assertEqual(conditional(aligned, {"material_security":"secure"}, "employment_position")["probabilities"]["formal"], "1")
        self.assertEqual(conditional(opposite, {"material_security":"secure"}, "employment_position")["probabilities"]["formal"], "0")
        self.assertEqual(conditional(opposite, {"material_security":"secure", "employment_position":"formal"}, "employment_position")["state"], "ZERO_MODEL_SUPPORT")

    def test_cumulative_condition_and_zero_support(self):
        b = self.run_method()
        r = conditional(b, {"material_security":"secure", "employment_position":"informal"}, "employment_position")
        self.assertEqual(r["model_denominator_mass"], "3/20")
        self.assertEqual(r["probabilities"], {"informal":"1"})
        self.assertEqual(conditional(b, {"material_security":"unavailable"}, "employment_position")["state"], "UNAVAILABLE")

    def test_consumer_rejects_mutated_values(self):
        b = self.run_method()
        b["candidate"]["distribution"][0]["probability"] = "1"
        with self.assertRaises(SynthesisError): conditional(b, {}, "employment_position")

    def test_replay_and_irrelevant_source_order(self):
        b = self.run_method()
        self.s.reverse()
        self.assertEqual(b, self.run_method())
        replay = b["replay"]
        self.assertEqual(b, synthesize(**replay))

    def test_real_permissions_are_not_inferred(self):
        self.s[0]["test_origin"] = False
        with self.assertRaises(SynthesisError): self.run_method()
        calls=[]
        def deny_transport(s,t,op):
            calls.append(op); return op == "SOURCE_INDEXED_BASELINE"
        b = synthesize(self.t, self.s, self.p, deny_transport)
        self.assertIsNone(b["candidate"])
        self.assertIn("TRANSPORT_PERMISSION_NOT_ADMITTED", b["refusals"]["A"])
        self.assertEqual(calls, ["SOURCE_INDEXED_BASELINE", "TARGET_JOINT_STANDARDIZATION"])

    def test_denominator_suppression_weight_and_nonfinite(self):
        for change in ["denominator", "suppression", "weight", "nan"]:
            with self.subTest(change=change):
                s = deepcopy(self.s)
                z=s[0]["strata"]["majority"]
                if change == "denominator": z["eligible_n"] += 1
                if change == "suppression": z["table_status"] = "SUPPRESSED"
                if change == "weight": z["cells"][0]["mass"] = -1
                if change == "nan": z["cells"][0]["mass"] = "NaN"
                with self.assertRaises(SynthesisError): synthesize(self.t,s,self.p)

    def test_survey_weight_change_is_a_value_change(self):
        before = self.run_method()
        self.s[0]["measure_basis"] = "WEIGHTED"
        self.s[0]["weight_ref"] = "synthetic-reviewed-weight-change@1"
        for t in self.s[0]["strata"].values():
            t.pop("design_variance")
            t["cells"][0]["mass"] *= 2
        after = self.run_method()
        self.assertNotEqual(table(before), table(after))
        self.assertEqual(before["baseline"][1], after["baseline"][1])
        self.assertIsNone(after["candidate"]["uncertainty"]["sampling_variance"])

    def test_support_threshold_is_diagnostic_not_rare_cell_pruning(self):
        self.p["minimum_raw_support"] = 20
        b = self.run_method()
        self.assertEqual(b["candidate"]["support"]["minority"]["excluded_sources"], ["A"])
        self.assertEqual(b["baseline"][0]["native_summary"]["strata"]["minority"]["cells"][0]["n"], 1)

    def test_joint_budget_keeps_frontier_visible(self):
        self.p["maximum_joint_cells"] = 3
        b = self.run_method()
        self.assertIsNone(b["candidate"])
        self.assertIn("JOINT_DOMAIN_EXCEEDS_BUDGET", b["refusals"]["A"])
        self.assertEqual(b["baseline"][0]["native_summary"]["joint_frontier_ref"], "synthetic-two-item-complete@1")


if __name__ == "__main__": unittest.main()
