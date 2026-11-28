"""R20 actual R34 full owner course as reusable lab input, no provider spend."""
import unittest
from inference_lab_r34 import capture_r34, replay_r34
from inference_lab_cli import fixture_arms, replay_owner_course
from test_inference_lab_campaign_r19 import config, HEAD
from um_sorok_organism.inference_lab import compare_frozen
from um_sorok_organism.inference_lab_campaign import build_plan, verify_plan
from um_sorok_organism.inference_lab_admission import evaluate_admissions
from um_sorok_organism.types import canonical, digest

class AcquiredLifeIntakeR20(unittest.TestCase):
    def test_actual_r34_capture_replay_admission_and_preflight(self):
        doc,state,witness=capture_r34(HEAD,with_admissions=True)
        course=state["course"]
        rows=doc["payload"]["rows"]
        self.assertEqual(len(rows),sum(x["calls"] for x in course["cost"]["by_task"].values()))
        self.assertEqual(len(witness["payload"]["rows"]),sum(r["task"]=="development" for r in rows))
        self.assertTrue(state["verification"]["valid"])
        self.assertGreaterEqual(course["actual_material_project_exercises"],3)
        self.assertEqual(course["mother_actual_later_operation"],"ORIENT")
        self.assertEqual(replay_owner_course(doc,HEAD),state)
        cfg=config();plan=build_plan(doc,cfg,per_stratum=2)
        p=verify_plan(doc,cfg,plan)
        result=compare_frozen(doc,fixture_arms(doc),sequence_ids=[r["seq"] for r in p["cases"]],
                              rotate_arms=True)
        self.assertEqual(len(result["observations"]),p["planned_calls"])
        self.assertTrue(all(r["equals_recorded_proposal"] for r in result["observations"]))
        admissions=evaluate_admissions(doc,witness,result)
        self.assertTrue(admissions["observations"])
        self.assertTrue(all(r["matches_recorded_admission"] for r in admissions["observations"]))
        self.assertEqual(digest(state),doc["payload"]["owner_state_sha256"])
        self.assertLess(p["arms"]["E"]["request_bytes"],p["arms"]["F"]["request_bytes"])
        print("INFERENCE_LAB_R20 "+canonical({"workload_calls":len(rows),
            "admission_witnesses":len(witness["payload"]["rows"]),
            "events":course["events"],"clock":course["clock"],
            "material_exercises":course["actual_material_project_exercises"],
            "mother_actual_later_operation":course["mother_actual_later_operation"],
            "cases":len(p["cases"]),"planned_calls":p["planned_calls"],
            "matched_scratch_admissions":len(admissions["observations"]),
            "wire":p["arms"],"coverage":p["coverage"],"complete_recorded_state_equal":True,
            "sourcefree_not_live":True,"network_calls":0}))

if __name__=="__main__":unittest.main()
