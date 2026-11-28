"""R21 actual R34 event-bound accounting and explicit matched pilot cases."""
import unittest
from inference_lab_r34 import capture_r34
from inference_lab_lifecycle_r21 import account_course, PILOT
from um_sorok_organism.inference_lab_campaign import build_plan, verify_plan
from um_sorok_organism.types import canonical, copy, digest
from test_inference_lab_campaign_r19 import config, HEAD

class LifecycleR21(unittest.TestCase):
    def test_actual_lifecycle_and_targeted_pilot(self):
        doc,state,witness=capture_r34(HEAD,with_admissions=True)
        report=account_course(doc,state,witness)
        stages={r["stage"]:r for r in report["stages"]}
        self.assertEqual(report["total"]["calls"],66)
        self.assertEqual(report["initialization"]["calls"],2)
        self.assertEqual(len(stages),16)
        self.assertEqual(sum(r["calls"] for r in stages.values())+2,66)
        self.assertEqual(sum(r["F_wire_bytes"] for r in stages.values())
                         +report["initialization"]["F_wire_bytes"],report["total"]["F_wire_bytes"])
        self.assertEqual(len(report["pilot_cases"]),7)
        self.assertTrue(all(stages["material_exercise_"+str(i)]["by_task"]["development"]>0
                            for i in range(1,4)))
        seq=[r["seq"] for r in report["pilot_cases"]]
        cfg=config();plan=build_plan(doc,cfg,sequence_ids=seq)
        p=verify_plan(doc,cfg,plan)
        self.assertEqual(p["planned_calls"],14)
        self.assertEqual([r["seq"] for r in p["cases"]],seq)
        for bad in ([seq[0],seq[0]],list(reversed(seq)),[66],[]):
            with self.assertRaisesRegex(ValueError,"EXPLICIT_SEQUENCE"):
                build_plan(doc,cfg,sequence_ids=bad)
        changed=copy(plan);changed["payload"]["selection"]["sequence_ids"]=seq[:-1]
        changed["sha256"]=digest(changed["payload"])
        with self.assertRaisesRegex(ValueError,"RECONSTRUCTION_MISMATCH"):
            verify_plan(doc,cfg,changed)
        print("INFERENCE_LAB_R21 "+canonical({
            "total":report["total"],"initialization":report["initialization"],
            "stages":[{k:v for k,v in r.items() if k not in ("event_id","sequence_ids")} for r in report["stages"]],
            "pilot_cases":[{k:v for k,v in r.items() if k not in ("packet_digest","event_id")} for r in report["pilot_cases"]],
            "pilot_wire":p["arms"],"network_calls":0}))
