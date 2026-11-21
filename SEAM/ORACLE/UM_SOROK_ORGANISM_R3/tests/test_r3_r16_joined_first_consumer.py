"""JOINED SORACLE R3 + REMONT R16 integration court.

Runs the real R3 material-object cultural first consumer on the R16 exact
ResearchLedger and asserts a cold-reopened R16 source/snapshot chain, without
pretending the author has run this suite.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.storage import ResearchLedger
from um_sorok_organism.types import adult,stable_id,copy
from um_sorok_organism.development import admit,InvalidDevelopment

SEED={
    "source_ref":"SOURCEFREE_FICTIONAL_PARENT_NOT_PYAT",
    "answers":{"fictional_instrument_field":"fictional_no_source_truth"},
    "fictional_seed":{"projects":[{"object":"already acquired ordinary speech",
        "means":["SPEAK"],"priority":.2,"cue_terms":["home"]}]},
}

class JoinedCulturalLifeIntegrity(unittest.TestCase):
    def test_nadia_learns_from_father_and_cold_integrity_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/"joined.sqlite3")
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize([("father","Father",SEED),("mother","Mother",SEED)])
                made=rt.step("father",requested_action="MAKE_OBJECT")
                self.assertEqual(made["status"],"PERFORMED")
                world=rt.ledger.world("w1")[1]
                objects=list(world["material_objects"])
                self.assertEqual(len(objects),1)
                artifact=objects[0]
                speech=rt.step("father",requested_action="SPEAK",object_ref=artifact)
                self.assertEqual(speech["status"],"PERFORMED")
                n_before=rt.snapshot("nadia")
                self.assertEqual(len(n_before["cultural_demonstrations"]),1)
                self.assertEqual(n_before["body"]["language"],0.0)
                # Critical first consumer: researcher does not choose her
                # INSPECT. The actor's sourced public material exposure does.
                own=rt.step("nadia")
                self.assertEqual(own["attempt"],"INSPECT")
                self.assertEqual(own["status"],"PERFORMED")
                n_after=rt.snapshot("nadia")
                self.assertEqual(len(n_after["cultural_reference_practices"]),1)
                self.assertEqual(n_after["cultural_reference_practices"][0][
                    "object_ref"],artifact)
                self.assertEqual(rt.ledger.world("w1")[1][
                    "material_objects"][artifact]["owner"],"father")
                self.assertTrue(rt.verify()["valid"])
            finally:
                rt.close()
            # Cold reader is the actual R16 repaired source-/snapshot-aware
            # ledger, not a separate toy SQLite mock.
            reopened=ResearchLedger(path)
            try:
                self.assertTrue(reopened.verify_chain()["valid"])
                self.assertEqual(len(reopened.actor("nadia")[1][
                    "cultural_reference_practices"]),1)
            finally:
                reopened.close()

    def test_r16_current_trial_blocks_other_end_without_erasing_r3_history(self):
        a=adult("a","A")
        a["possible_ends"]=[
            {"id":"end_a","origin_event":"prior_a",
             "experience_ref":"prior_ex_a","possible_object":"a",
             "possible_means":["SING"],"cue_terms":["song"],
             "status":"POSSIBLE_NOT_ACQUIRED_MOTIVE"},
            {"id":"end_b","origin_event":"prior_b",
             "experience_ref":"prior_ex_b","possible_object":"b",
             "possible_means":["SING"],"cue_terms":["song"],
             "status":"POSSIBLE_NOT_ACQUIRED_MOTIVE"}]
        ex={"actor":"a","ref":"here","own_action":"SING",
            "status":"PERFORMED","participated":True,
            "felt_enactment":{"attempted_operation":"SING"},
            "perceived_cues":[{"id":"audible_song","tags":["song"]}]}
        trial={"trial_id":stable_id("end_trial",{
                    "actor":"a","clock":4,"end":"end_a","operation":"SING"}),
               "actor":"a","as_of_clock":4,"possible_end_ref":"end_a",
               "operation":"SING","origin_event":"prior_a",
               "origin_experience_ref":"prior_ex_a","actor_project_ref":None}
        before=copy(a)
        with self.assertRaisesRegex(InvalidDevelopment,
                                     "CURRENT_TRIAL_NOT_MATURE_MOTIVE"):
            admit(a,ex,"here_event",[
                {"kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":"end_b",
                 "means":["SING"],"priority":.35}],issued_trial=trial)
        self.assertEqual(a,before)

    def test_r16_trial_cannot_reorganize_existing_project(self):
        a=adult("a","A");before=copy(a)
        ex={"actor":"a","ref":"here","own_action":"SING",
            "participated":True,"status":"PERFORMED",
            "perceived_cues":[{"id":"song"}]}
        with self.assertRaisesRegex(InvalidDevelopment,
                            "CURRENT_TRIAL_CANNOT_REORGANIZE_DURABLE_PROJECT"):
            admit(a,ex,"here_event",
                  [{"kind":"REORGANIZE_PROJECT","project_id":"fictional"}],
                  issued_trial={"actor":"a","trial_id":"provided_trial"})
        self.assertEqual(a,before)

if __name__=="__main__":
    unittest.main()
