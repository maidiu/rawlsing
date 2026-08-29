import json,tempfile,unittest
from pathlib import Path
from validate_b07_v550j_source_family_authority import validate
HERE=Path(__file__).resolve().parent
ARAB=HERE/"ARAB_BAROMETER_V550J_SOURCE_FAMILY_AUTHORITY_R1.json"
AFRO=HERE/"AFROBAROMETER_V550J_SOURCE_FAMILY_AUTHORITY_R1.json"
class B07AuthorityTests(unittest.TestCase):
    def test_registries_validate(self): self.assertEqual(validate(ARAB),[]); self.assertEqual(validate(AFRO),[])
    def test_exact_canary_ids_and_members(self):
        a=json.loads(ARAB.read_text()); f=json.loads(AFRO.read_text())
        self.assertEqual(a["admitted_configurations"][0]["configuration_id"],"JCFG-ARAB-I-POLITICAL-KNOWLEDGE"); self.assertEqual([m["member_id"] for m in a["admitted_configurations"][0]["members"]],["q2571","q2572"])
        self.assertEqual(f["admitted_configurations"][0]["configuration_id"],"JCFG-AFRO-R1-MIP-RANKED"); self.assertEqual([m["member_id"] for m in f["admitted_configurations"][0]["members"]],["mip1","mip2"])
    def test_rank_and_set_semantics_remain_distinct(self):
        a=json.loads(ARAB.read_text()); f=json.loads(AFRO.read_text()); self.assertIn("SET_DISTINCT_TARGETS",a["admitted_configurations"][0]["member_order_semantics"]); self.assertIn("ORDER_SIGNIFICANT",f["admitted_configurations"][0]["member_order_semantics"])
    def test_denominator_not_promoted(self):
        for p in (ARAB,AFRO):
            d=json.loads(p.read_text()); self.assertFalse(d["global_recovery_denominator"]["source_family_slice_materialized"]); self.assertFalse(d["full_family_completeness_claim"]); self.assertFalse(d["production_wide_execution_authorized"])
    def test_archive08_stays_nonauthoritative(self):
        for p in (ARAB,AFRO): self.assertIn("NONAUTHORITATIVE",json.loads(p.read_text())["archive08_status"])
    def test_mutated_completeness_fails(self):
        d=json.loads(ARAB.read_text()); d["full_family_completeness_claim"]=True
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.json"; p.write_text(json.dumps(d)); self.assertIn("forbidden_full_family_completeness_claim",validate(p))
    def test_mutated_hash_fails(self):
        d=json.loads(AFRO.read_text()); d["known_source_waves"].append("R10")
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"x.json"; p.write_text(json.dumps(d)); self.assertIn("authority_content_hash_mismatch",validate(p))
    def test_no_cross_source_portability(self):
        for p in (ARAB,AFRO): self.assertIn("cross-source portability",json.loads(p.read_text())["admitted_configurations"][0]["forbidden_inference"])
if __name__=="__main__": unittest.main()
