"""R23 actual expressive reentry course: private actor and visitor boundaries."""
import tempfile
from pathlib import Path
import unittest

from inference_lab_surface_r23 import capture_surface, verify_surface
from um_sorok_organism.inference_lab import save_report, load_workload, _local_read
from um_sorok_organism.inference_lab_campaign import build_plan
from um_sorok_organism.types import canonical, copy, digest

HEAD="a"*40

class SurfaceIntakeR23(unittest.TestCase):
    def test_actual_acquired_and_unheard_unacquired_unaddressed(self):
        results={}
        for arm in ("acquired","unheard","unacquired","unaddressed"):
            doc,witness,r=capture_surface(HEAD,arm)
            results[arm]=r
            self.assertEqual(r["visitor_surface_semantic_calls"],0)
            self.assertEqual(r["network_calls"],0)
            self.assertIsNone(r["provider_tokens"])
            self.assertGreater(r["expression_calls"],0)
            self.assertEqual(len(r["F_E_wire_bytes"]),2)
            self.assertEqual(r["course_outcome"]["heard"],arm!="unheard")
            if arm=="acquired":
                with tempfile.TemporaryDirectory() as tmp:
                    p=Path(tmp);save_report(p/"w",doc);save_report(p/"v",witness)
                    self.assertEqual(verify_surface(load_workload(p/"w"),_local_read(p/"v"),
                                                   source_head=HEAD),r)
                    self.assertEqual((p/"v").stat().st_mode&0o777,0o600)
                bad=copy(doc);row=bad["payload"]["rows"][r["target_expression_seq"]]
                row["proposal"]["surface"]="invented words"
                row["proposal_digest"]=digest(row["proposal"]);bad["sha256"]=digest(bad["payload"])
                with self.assertRaisesRegex(ValueError,"EXPRESSION_EVENT_MISMATCH"):
                    verify_surface(bad,witness,source_head=HEAD)
                bad=copy(witness);bad["surfaces"][0]["view"]["mandatory"]=[]
                with self.assertRaisesRegex(ValueError,"WITNESS_BINDING"):
                    verify_surface(doc,bad,source_head=HEAD)
                with self.assertRaisesRegex(ValueError,"SURFACE_OWNER_QUALIFICATION"):
                    build_plan(doc,{},sequence_ids=[r["target_expression_seq"]])
        a,b,c,d=(results[x] for x in ("acquired","unheard","unacquired","unaddressed"))
        self.assertEqual(a["course_outcome"]["cadence"],"HALTING")
        self.assertEqual(a["course_outcome"]["cadence"],b["course_outcome"]["cadence"])
        self.assertIsNone(c["course_outcome"]["cadence"])
        self.assertTrue(a["course_outcome"]["formed"])
        self.assertTrue(b["course_outcome"]["formed"])
        self.assertFalse(d["course_outcome"]["formed"])
        print("INFERENCE_LAB_R23 "+canonical({k:{x:y for x,y in v.items()
            if x not in ("source_head","workload_sha256","witness_sha256")}
            for k,v in results.items()}))

if __name__=="__main__":unittest.main()
