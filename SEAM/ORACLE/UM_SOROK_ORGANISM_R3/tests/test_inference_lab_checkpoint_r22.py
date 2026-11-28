"""R22 uses the actual existing P2/P3 course, not an invented checkpoint."""
import tempfile
from pathlib import Path
import unittest

from inference_lab_checkpoint_r22 import capture_checkpoint, verify_checkpoint, FIXTURE
from um_sorok_organism.inference_lab import save_report, load_workload, _local_read
from um_sorok_organism.inference_lab_campaign import build_plan
from um_sorok_organism.types import canonical, copy, digest

HEAD="a"*40

class CheckpointIntakeR22(unittest.TestCase):
    def test_actual_p3_checkpoint_capture_and_boundary_refusals(self):
        doc,witness,report=capture_checkpoint(HEAD)
        self.assertEqual(report["calls"],3)
        self.assertEqual(report["ordinary_calls"],1)
        self.assertEqual(report["realized_events"],6)
        self.assertEqual([r["prior_events"] for r in report["rows"]],[0,3,3])
        self.assertEqual([r["next_events"] for r in report["rows"]],[3,3,0])
        self.assertEqual(report["second_event_recruited_records"],2)
        self.assertEqual(report["stored_retrospective_proposals"],2)
        self.assertEqual(report["scope"],"P3_SOURCEFREE_OWNER_EFFECTS_NOT_MODEL_INDUCED")
        self.assertEqual(report["network_calls"],0)
        self.assertIsNone(report["provider_tokens"])
        with tempfile.TemporaryDirectory() as tmp:
            t=Path(tmp);save_report(t/"workload",doc);save_report(t/"witness",witness)
            saved=verify_checkpoint(load_workload(t/"workload",source_head=HEAD),
                _local_read(t/"witness"),source_head=HEAD)
            self.assertEqual(saved,{k:v for k,v in report.items() if k!="owner_measurement"})
            self.assertEqual((t/"witness").stat().st_mode&0o777,0o600)
        # A freshly rehashed provider packet still must bind the actual
        # accessible records, not a fabricated or reordered retrospective.
        bad=copy(doc);row=bad["payload"]["rows"][1]
        row["packet"]["previous"]["events"].reverse()
        row["packet_digest"]=digest(row["packet"]);bad["sha256"]=digest(bad["payload"])
        with self.assertRaisesRegex(ValueError,"PRIOR_ACCESS_MISMATCH"):
            verify_checkpoint(bad,witness,source_head=HEAD)
        bad=copy(doc);row=bad["payload"]["rows"][1]
        row["proposal"]["prospective"].reverse()
        row["proposal_digest"]=digest(row["proposal"]);bad["sha256"]=digest(bad["payload"])
        with self.assertRaisesRegex(ValueError,"PROSPECTIVE_COMMITMENT_MISMATCH"):
            verify_checkpoint(bad,witness,source_head=HEAD)
        bad=copy(witness);bad["stop"]["clock"]+=1
        with self.assertRaisesRegex(ValueError,"WITNESS_BINDING"):
            verify_checkpoint(doc,bad,source_head=HEAD)
        with self.assertRaisesRegex(ValueError,"CHECKPOINT_REQUIRES_SEPARATE_OWNER_QUALIFIED_TRANSPORT"):
            build_plan(doc,{},sequence_ids=[1])
        print("INFERENCE_LAB_R22 "+canonical({k:v for k,v in report.items()
            if k not in ("owner_measurement","workload_sha256","local_witness_sha256","source_head")}))

    def test_actual_owner_control_no_retrospective_effect_claim(self):
        _,_,report=capture_checkpoint(HEAD,control=True)
        self.assertEqual(report["calls"],3)
        self.assertEqual(report["second_event_recruited_records"],0)
        self.assertEqual(report["second_event_modes"],["inspect_alone"])
        self.assertEqual(report["stored_retrospective_proposals"],2)
        print("INFERENCE_LAB_R22_CONTROL "+canonical({
            "calls":report["calls"],"request_bytes":report["request_bytes"],
            "second_event_modes":report["second_event_modes"],
            "second_event_recruited_records":report["second_event_recruited_records"],
            "stored_retrospective_proposals":report["stored_retrospective_proposals"],
            "network_calls":0}))

if __name__=="__main__":unittest.main()
