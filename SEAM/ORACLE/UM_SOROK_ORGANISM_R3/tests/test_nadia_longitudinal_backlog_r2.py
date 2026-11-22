"""SORACLE R2 longitudinal first-consumer court: Nadia is the tested subject.

No invented auto-grown adult role, retroactive feeling, or script-selected
developmental proposal. Two continuing actual worlds differ only in whether
Nadia personally experienced an unanswered call before genuine subsequent
care. A sourcefree counterfactual witness, not human science.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime


PARENT={
    "source_ref":"fictional_parent_source_not_empirical_PYAT",
    "source_grade":"UNQUALIFIED_WHOLE_SURVEY_TEST_FICTION",
    "answers":{"fictional_test_question":"fictional_test_answer"},
    "fictional_seed":{"projects":[]}
}


def create_life(path):
    rt=ConstitutiveRuntime(str(path))
    rt.initialize([
        ("mother","Mother",PARENT),
        ("father","Father",PARENT)])
    return rt


def live_to_early_care(rt,*,unfinished_call):
    # The mother has an objectively independent worksite situation. The
    # daughter's next possibilities do not require simulating a trade union.
    gone=rt.step("mother",requested_action="MOVE",object_ref="workshop")
    if gone["status"]!="PERFORMED":
        raise AssertionError(gone)
    if unfinished_call:
        unfinished=rt.step("nadia",requested_action="SIGNAL",target="mother")
        if unfinished["status"]!="PARTIAL":
            raise AssertionError(unfinished)
    else:
        # Preserve world clock without forging a failed addressed attempt.
        rest=rt.step("nadia",requested_action="WAIT")
        if rest["status"]!="PERFORMED":
            raise AssertionError(rest)
    care=rt.step("father",requested_action="CARE",target="nadia")
    if care["status"]!="PERFORMED":
        raise AssertionError(care)
    return rt.snapshot("nadia")


class LongitudinalBecoming(unittest.TestCase):
    def test_same_later_care_different_prior_life_creates_different_psyche(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=create_life(Path(tmp)/"a.sqlite")
            b=create_life(Path(tmp)/"b.sqlite")
            try:
                experienced=live_to_early_care(a,unfinished_call=True)
                not_experienced=live_to_early_care(b,unfinished_call=False)
                a_ends=[x for x in experienced.get("possible_ends",[])
                    if x.get("genesis_family")==(
                        "SENSED_INTERRUPTION_THEN_RELIEF")]
                b_ends=[x for x in not_experienced.get("possible_ends",[])
                    if x.get("genesis_family")==(
                        "SENSED_INTERRUPTION_THEN_RELIEF")]
                self.assertEqual(len(a_ends),1)
                self.assertEqual(len(b_ends),0)
                self.assertEqual(a_ends[0]["status"],
                                 "POSSIBLE_NOT_ACQUIRED_MOTIVE")
                self.assertEqual(experienced["projects"],
                                 not_experienced["projects"])
                self.assertEqual(experienced["self_model"],{})
                self.assertEqual(not_experienced["self_model"],{})
                self.assertEqual(a.ledger.world("w1")[1]["clock"],
                                 b.ledger.world("w1")[1]["clock"])
                # Each subject retains different actual history, even when
                # a shared present encounter/source is subsequently available.
                self.assertNotEqual(
                    experienced["lived_genesis_episodes"],
                    not_experienced["lived_genesis_episodes"])
                self.assertTrue(a.verify()["valid"])
                self.assertTrue(b.verify()["valid"])
            finally:
                a.close();b.close()

    def test_compressed_maturation_and_later_autonomous_beats_preserve_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            rt=create_life(Path(tmp)/"life.sqlite")
            try:
                earlier=live_to_early_care(rt,unfinished_call=True)
                initial_ids={x["id"] for x in earlier["possible_ends"]}
                self.assertTrue(initial_ids)
                rt.background(30,processes=[])
                matured=rt.snapshot("nadia")
                self.assertEqual(matured["age_days"],30)
                self.assertTrue(initial_ids.issubset(
                    {x["id"] for x in matured["possible_ends"]}))
                # Schedule actor opportunities, NOT scripted identities
                # and not omniscient post-hoc model reasons.
                rt.continue_without_user(beats=3)
                subsequent=rt.snapshot("nadia")
                self.assertTrue(initial_ids.issubset(
                    {x["id"] for x in subsequent["possible_ends"]}))
                self.assertEqual(subsequent["role"],"child")
                self.assertNotIn("psychodynamic_genesis_proven",
                                 subsequent["self_model"])
                self.assertTrue(rt.verify()["valid"])
            finally:
                rt.close()


if __name__=="__main__":
    unittest.main()
