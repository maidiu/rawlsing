"""Native structural tests; S04 exports below are synthetic contract fixtures only."""
import hashlib
import json
import os
import unittest
from copy import deepcopy

from native_priority_readers import NativePack
from relational_context import (S04_CONTRACT, S04_GRADE, formation_changes,
    context_contrast, repertoire_contrast, formation_repertoire_contrast)


class Ref:
    def __init__(self, value):
        self.value = value

    def as_dict(self):
        return deepcopy(self.value)


class ExportFixture:
    def __init__(self, count, other, condition):
        n = count + other
        from fractions import Fraction
        self.m = {"contract": S04_CONTRACT, "grade": S04_GRADE,
                  "state": "OBSERVED_FULL_CASE_SUPPORT", "source_fact_ref": "fixture-fact",
                  "source_release_ref": "fixture-release", "source_universe_ref": "fixture-universe",
                  "source_risk_set_ref": "fixture-risk", "source_measure_basis_ref": "fixture-raw",
                  "source_response_semantics_ref": "fixture-semantics", "output_axes": [{"index": 1, "target_ref": "fixture-target"}],
                  "raw_original_full_joint_resolved_n": 100, "raw_source_eligible_n": 100,
                  "raw_selected_full_case_n": n, "conditions": [{"index": 0, "value": condition}],
                  "complete_output_cells": [{"output_states": [i], "raw_count": c,
                      "raw_fraction_of_selected_full_cases": {"$exact_fraction": [Fraction(c,n).numerator, Fraction(c,n).denominator]}}
                      for i,c in enumerate((count, other))]}
        self.reseal()

    def reseal(self):
        d = hashlib.sha256(json.dumps(self.m, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()
        self.ref = Ref({"kind": S04_CONTRACT, "object_id": "urn:rawlsing:s04:general-projection:sha256:"+d,
                        "content_hash": d})

    def material(self):
        return deepcopy(self.m)


class RelationalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = NativePack(os.environ["FF_PRIORITY_PACK"])

    def test_native_epr_status_change(self):
        r = formation_changes(self.p, 660, 1970, 1971)
        f = next(f for f in r["formations"] if f["gwgroupid"] == 66007000)
        self.assertEqual(f["changes"]["status"], {"left":"POWERLESS", "right":"DISCRIMINATED", "state":"DIFFERENT"})
        self.assertEqual(f["left"]["epr_reference_year"], 1970)
        self.assertEqual(f["right"]["epr_reference_year"], 1971)

    def test_native_missing_period_is_not_group_disappearance(self):
        r = formation_changes(self.p, 660, 2019, 2024)
        self.assertTrue(r["formations"])
        self.assertTrue(all(f["state"] == "NO_MATCH" and not f["changes"] for f in r["formations"]))

    def test_native_context(self):
        a = dict(gwid=750, epr_year=2019, economy="IND", wbl_year=2019,
                 join_year=2019, subsample="All", fin_year=2021, fin_group="all", fin_group2="all")
        b = dict(a, gwid=660, economy="LBN")
        r = context_contrast(self.p, a, b)
        self.assertEqual(r["epr"]["state"], "DISTINCT_POLITIES_NO_GROUP_MATCH")
        self.assertEqual(r["findex"]["state"], "DESCRIPTIVE_NATIVE_CONTRAST")
        self.assertEqual(r["findex"]["changes"]["save_any_t_d"]["state"], "DIFFERENT")
        self.assertTrue(any(q["relation"] == "findex" for q in r["next_questions"]))
        self.assertEqual(r["left"]["epr"]["epr_reference_year"], 2019)
        self.assertEqual(r["left"]["findex"]["keys"]["year"], 2021)

    def test_subgroups_not_stitched(self):
        a = dict(gwid=750, epr_year=2019, economy="IND", wbl_year=2019,
                 join_year=2019, subsample="All", fin_year=2021, fin_group="all", fin_group2="all")
        r = context_contrast(self.p, a, dict(a, fin_group="gender", fin_group2="women"))
        self.assertEqual(r["findex"]["state"], "DIFFERENT_PUBLISHED_SUBGROUPS_NO_CELL_CONTRAST")

    def test_same_repertoire_different_native_power(self):
        a, b = ExportFixture(30,20,"A"), ExportFixture(30,20,"B")
        r = formation_repertoire_contrast(self.p, (660,66007000,1970), (660,66007000,1971), a,b)
        self.assertEqual(r["material"]["changes"]["status"]["state"], "DIFFERENT")
        self.assertEqual(r["empirical"]["cells"][0]["difference_right_minus_left"], [0,1])
        self.assertEqual(r["state"], "ALIGNED_HISTORICAL_CLAIM_HELD")
        self.assertEqual(r["empirical"]["left"]["material"], a.m)

    def test_repertoire_difference_and_scope(self):
        a,b = ExportFixture(30,20,"A"), ExportFixture(10,40,"B")
        r = repertoire_contrast(a,b)
        self.assertEqual(r["cells"][0]["difference_right_minus_left"], [-2,5])
        b.m["source_risk_set_ref"] = "different"; b.reseal()
        self.assertEqual(repertoire_contrast(a,b)["state"], "SEPARATE_SCOPES_NO_NUMERICAL_COMPARISON")

    def test_bad_export_and_count(self):
        a,b = ExportFixture(30,20,"A"), ExportFixture(10,40,"B")
        b.m["complete_output_cells"][0]["raw_count"] += 1
        with self.assertRaises(ValueError): repertoire_contrast(a,b)
        b.reseal()
        with self.assertRaises(ValueError): repertoire_contrast(a,b)

    def test_nonpositive_retained(self):
        a,b = ExportFixture(30,20,"A"), ExportFixture(10,40,"B")
        b.m["state"] = "UPSTREAM_SCIENCE_OR_SOURCE_HELD"; b.reseal()
        r = repertoire_contrast(a,b)
        self.assertEqual(r["state"], "UPSTREAM_NONPOSITIVE_RETAINED")
        self.assertEqual(r["cells"], [])


if __name__ == "__main__":
    unittest.main()
