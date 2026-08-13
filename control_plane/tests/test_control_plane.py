import importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location("rawlsingctl",ROOT/"control_plane"/"rawlsingctl.py")
ctl=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(ctl)
class ControlPlaneTests(unittest.TestCase):
    def test_repo_validates(self):
        errors,_=ctl.validate_repo(); self.assertEqual(errors,[])
    def test_phase_d_is_closed_and_frontier_is_v552(self):
        current=ctl.load("current.json"); self.assertEqual(current["active_frontier"],"V552_REACCEPTANCE"); receipt=json.loads((ROOT/"control_plane"/"receipts"/f'{current["latest_accepted_receipt"]}.json').read_text()); self.assertEqual(receipt["terminal"],"PHASE_D_GATE_CLOSED"); self.assertTrue(receipt["accepted"])
    def test_35_wave_release_is_locked(self):
        graph=ctl.load("pipeline_graph.json"); node={x["id"]:x for x in graph["nodes"]}["APP_GATE_35"]; self.assertEqual(node["status"],"LOCKED"); self.assertEqual(node["entry_gate"],"BOUNDED_V550_TO_V558_ARCHITECTURE_ACCEPTED")
    def test_courts_have_claim_ceilings(self):
        for court in ctl.load("courts.json")["courts"]: self.assertTrue(court["allowed_claims"]); self.assertTrue(court["forbidden_claims"])
    def test_repair_stack_accounting(self):
        r=ctl.load("repair_stack.json"); self.assertEqual(r["done_count"],16); self.assertEqual(r["partial_not_closed"],[4,5,6,9,10,11,12,13]); self.assertEqual(r["in_progress"],[25])
    def test_implementation_change_does_not_require_vozhd(self):
        p=ctl.load("change_policy.json"); self.assertFalse(p["classes"]["C0_IMPLEMENTATION"]["requires_vozhd"]); self.assertTrue(p["classes"]["C2_AUTHORITY"]["requires_vozhd"]); self.assertTrue(p["classes"]["C3_ARCHITECTURE"]["requires_vozhd"])
    def test_static_and_synthetic_cannot_claim_empirical_readiness(self):
        courts={c["id"]:c for c in ctl.load("courts.json")["courts"]}; self.assertIn("empirical readiness",courts["REPO_STATIC"]["forbidden_claims"]); self.assertIn("empirical archetype satisfaction",courts["SYNTHETIC_CONTRACT"]["forbidden_claims"])
if __name__=="__main__": unittest.main()
