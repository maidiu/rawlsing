#!/usr/bin/env python3
"""Unit tests for the independent C05R2B hostile validator."""
import copy, unittest
import validate_c05r2b_receipts as v

class TestOracle(unittest.TestCase):
    def setUp(self):
        self.a=v.synthetic_valid_run(); self.b=copy.deepcopy(self.a)
    def test_synthetic_control(self): self.assertEqual(v.validate_pair(self.a,self.b),[])
    def assertHostile(self,fn):
        fn(self.a,self.b); self.assertTrue(v.validate_pair(self.a,self.b))
    def test_wrong_source(self): self.assertHostile(lambda a,b:a["source"].__setitem__("sha256","0"*64))
    def test_wrong_authority(self): self.assertHostile(lambda a,b:a["as3r2"].__setitem__("discovery_authority_ref",v._ref("DiscoveryAuthority@1.0.0","wrong")))
    def test_wrong_frontier(self): self.assertHostile(lambda a,b:a["i05"].__setitem__("evaluated_frontier_ref",v._ref("PRE553_I05_EVALUATED_FRONTIER","wrong")))
    def test_missing_candidate(self): self.assertHostile(lambda a,b:a["i05"]["receipts"].pop())
    def test_corrupt_receipt(self): self.assertHostile(lambda a,b:a["i05"]["receipts"][0].pop("replay_ref"))
    def test_fresh_process_mismatch(self): self.assertHostile(lambda a,b:b["i05"]["receipts"][0].__setitem__("typed_state","NONCOMPARABLE"))
    def test_hidden_persistence(self): self.assertHostile(lambda a,b:a["route_b"].__setitem__("persistent_transformed_empirical_payload_bytes",1))
    def test_i04_positive_manufacture(self): self.assertHostile(lambda a,b:a["i04"].__setitem__("positive_pre_v3_structural_product","FORBIDDEN"))
if __name__=="__main__": unittest.main()
