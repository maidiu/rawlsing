"""Joined first consumer: one psychologically continuing Nadia, two histories.

SPOKEN versus UNSPOKEN changes an objective adult public activity, not the
newborn's preloaded goal. The child's initial action is actor-selected;
subsequent time and beats are real existing world and psychological owners.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.joined_longitudinal_demo import run_counterfactual


class JoinedActualDevelopment(unittest.TestCase):
    def test_matched_households_diverge_through_nadia_own_action(self):
        with tempfile.TemporaryDirectory() as path:
            result=run_counterfactual(path,days=8,beats=6)
            self.assertTrue(result["early_historical_cultural_divergence_observed"])
            yes=result["contrast"]["spoken"]
            no=result["contrast"]["unspoken"]
            self.assertEqual(yes["father_source_action"],"SPEAK")
            self.assertEqual(no["father_source_action"],"REST")
            self.assertEqual(yes["world_object_owner"],"father")
            self.assertEqual(no["world_object_owner"],"father")
            self.assertEqual(yes["actor_selected_nadia_action"],"INSPECT")
            self.assertEqual(yes["actor_selected_nadia_status"],"PERFORMED")
            self.assertEqual(len(yes["early_nadia_after"]["cultural_practice_refs"]),1)
            self.assertEqual(no["early_nadia_after"]["cultural_practice_refs"],[])
            self.assertEqual(yes["independent_beats_reported"],6)
            self.assertEqual(no["independent_beats_reported"],6)
            self.assertEqual(yes["later_nadia"],yes["cold_nadia"])
            self.assertEqual(no["later_nadia"],no["cold_nadia"])
            self.assertTrue(yes["cold_integrity"]["valid"])
            self.assertTrue(no["cold_integrity"]["valid"])
            self.assertEqual(result["external_pyat_correspondence"],"NOT_ISSUED")
            self.assertTrue(result["nadia_action_not_externally_requested"])

    def test_separate_cold_sourcefree_runs_are_reproducible(self):
        with tempfile.TemporaryDirectory() as path:
            a=run_counterfactual(Path(path)/"one",days=7,beats=5)
            b=run_counterfactual(Path(path)/"two",days=7,beats=5)
            for which in ("spoken","unspoken"):
                self.assertEqual(a["contrast"][which]["later_nadia"],
                                 b["contrast"][which]["later_nadia"])
                self.assertEqual(a["contrast"][which]["cold_integrity"]["last_hash"],
                                 b["contrast"][which]["cold_integrity"]["last_hash"])

    def test_invalid_future_budget_does_not_begin_a_sourcefree_life(self):
        with tempfile.TemporaryDirectory() as path:
            with self.assertRaises(ValueError):
                run_counterfactual(path,days=-1,beats=1)
            with self.assertRaises(ValueError):
                run_counterfactual(path,days=4,beats=25)
            self.assertEqual(list(Path(path).glob("*.sqlite3")),[])


if __name__=="__main__":
    unittest.main()
