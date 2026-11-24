"""Run against the actual uploaded priority pack; no raw rows exported by tests."""
import os
import unittest
from pathlib import Path

from native_priority_readers import NativePack, JOIN_STATUS, partition


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = NativePack(Path(os.environ["FF_PRIORITY_PACK"]))

    def test_shapes(self):
        for source, expected in {"EPR": (4339, 11), "ED": (871, 20), "TEK": (643, 5),
                                 "WBL": (10260, 56), "JOIN": (14628, 103),
                                 "FINDEX": (8577, 438)}.items():
            self.assertEqual(self.p.load(source)[0].shape, expected)

    def test_epr_reference_year(self):
        a = self.p.select("EPR", {"gwid": 660}, year=2019)
        self.assertEqual(len(a["rows"]), 11)
        self.assertTrue(all(r["values"]["from"] <= 2019 <= r["values"]["to"] for r in a["rows"]))
        self.assertEqual(self.p.select("EPR", {"gwid": 660}, year=2024)["status"], "NO_MATCH")

    def test_group_namespaces(self):
        a = self.p.select("ED", {"gwid": 2, "gwgroupid": 201000})
        self.assertEqual(len(a["rows"]), 1)
        self.assertEqual(self.p.select("ED", {"gwid": 660, "gwgroupid": 201000})["status"], "NO_MATCH")
        a = self.p.select("TEK", {"tekid": 101})
        self.assertGreaterEqual(len({r["values"]["gwid"] for r in a["rows"]}), 2)

    def test_wbl_zero_and_year(self):
        a = self.p.select("WBL", {"economycode": "USA", "year": 2019})["rows"][0]["values"]
        self.assertEqual(a["mtrnity_days"], 0)
        self.assertEqual(a["reportyr"], 2020)
        self.assertEqual(a["gr4_13obeymrd"], 1)
        self.assertEqual(self.p.select("WBL", {"economycode": "USA", "year": 2024})["status"], "NO_MATCH")

    def test_join_partition(self):
        d = self.p.load("JOIN")[0]
        complete = d[list(JOIN_STATUS)].dropna()
        self.assertEqual(len(complete), 14141)
        self.assertTrue(((complete.sum(axis=1) - 1).abs() <= 1e-6).all())
        a = self.p.select("JOIN", {"Country Code": "IND", "Year of survey": 2019, "Subsample": "All"})
        self.assertEqual(len(a["rows"]), 1)
        self.assertEqual(partition(a["rows"][0]["values"])["status"], "COMPLETE")
        self.assertEqual(partition(dict(zip(JOIN_STATUS, [0.5, None, 0.2, 0.1])))["status"], "PARTIAL")
        self.assertEqual(partition(dict(zip(JOIN_STATUS, [0.5, 0.1, 0.2, 0.1])))["status"], "NONUNIT_SUM")

    def test_findex_margins(self):
        a = self.p.select("FINDEX", {"codewb": "IND", "year": 2021, "group": "all", "group2": "all"})
        self.assertEqual(len(a["rows"]), 1)
        self.assertAlmostEqual(a["rows"][0]["values"]["save_any_t_d"], 0.235477, places=5)
        self.assertEqual(self.p.select("FINDEX", {"codewb": "IND", "year": 2021, "group": "gender", "group2": "poorest 40%"})["status"], "NO_MATCH")

    def test_context_independent_clocks(self):
        a = self.p.context(gwid=750, epr_year=2019, economy="IND", wbl_year=2019,
                           join_year=2019, subsample="All", fin_year=2021, fin_group="all", fin_group2="all")
        self.assertEqual(a["epr"]["epr_reference_year"], 2019)
        self.assertEqual(a["findex"]["keys"]["year"], 2021)
        self.assertEqual(a["alignment"], "CALLER_SELECTED_KEYS_NOT_QUALIFIED_CROSSWALK")
        self.assertEqual(a["join"]["rows"][0]["employment_partition"]["status"], "COMPLETE")
        self.assertEqual(len(a["formations"]), len(a["epr"]["rows"]))


if __name__ == "__main__":
    unittest.main()
