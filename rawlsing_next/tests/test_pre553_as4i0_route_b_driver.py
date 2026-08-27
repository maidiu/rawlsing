from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
from rawlsing_next.pre553_as4i0_route_b_driver import FILES,DA,RuntimeCatalogPreimageMissing,SealValidationError,load_and_validate_as3r2,require_runtime_catalog_payload

BANKED=Path(__file__).resolve().parents[2]/"data"/"ddm_build_copy"/"recovery_integration"/"semantic_relation_R1_through_Job3"/"R1_20260825"/"AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827"/"banked_as3r2"

class TestAS4I0(unittest.TestCase):
    def copy(self):
        t=tempfile.TemporaryDirectory(); r=Path(t.name)
        for f in FILES.values(): (r/f).write_bytes((BANKED/f).read_bytes())
        return t,r
    def test_exact_seal(self):
        s=load_and_validate_as3r2(BANKED); self.assertEqual(s.documents["da"]["content_hash"],DA); self.assertEqual((len(s.predicate_refs),len(s.query_refs)),(19,3))
    def test_wrong_authority_fails_closed(self):
        t,r=self.copy()
        with t:
            p=r/FILES["da"]; x=json.loads(p.read_text()); x["content_hash"]="0"*64; p.write_text(json.dumps(x))
            with self.assertRaises(SealValidationError): load_and_validate_as3r2(r)
    def test_wrong_frontier_fails_closed(self):
        t,r=self.copy()
        with t:
            p=r/FILES["frontier"]; x=json.loads(p.read_text()); x["official_frontier_ref"]["content_hash"]="0"*64; p.write_text(json.dumps(x))
            with self.assertRaises(SealValidationError): load_and_validate_as3r2(r)
    def test_malformed_fails_closed(self):
        t,r=self.copy()
        with t:
            (r/FILES["binding"]).write_text("{")
            with self.assertRaises(SealValidationError): load_and_validate_as3r2(r)
    def test_missing_runtime_preimages_fail_closed(self):
        s=load_and_validate_as3r2(BANKED)
        with self.assertRaises(RuntimeCatalogPreimageMissing) as cm: require_runtime_catalog_payload(BANKED/"__absent__.json",s)
        self.assertIn("AS4I0-B01",str(cm.exception))
    def test_no_hidden_runtime_payload_banked(self):
        self.assertFalse(any("runtime_catalog_objects" in p.name for p in BANKED.iterdir()))
if __name__=="__main__": unittest.main()
