#!/usr/bin/env python3
"""Additive typed-source/graph preservation against the mainMAC R6 reference."""
import copy,hashlib,importlib.util,json,pathlib,sys,unittest
from r7_typed import validate,load_mainmac,ROOT

reference=ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6/tools/test_r6.py'
spec=importlib.util.spec_from_file_location('mainmac_reference_tests',reference)
# mainMAC tests import `r6` bare, isolate module identity from active tools
M=load_mainmac();sys.modules['r6']=M
T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)

def fixture():
    nodes,edges,routes=T.gen_graph()
    return {'schema':'ANVIL_R7_TYPED_BOUNDARY_WITNESS','source_cut':M.POL['operating_cut'],
        'mainmac_policy_sha256':hashlib.sha256((ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6/contracts/policy.json').read_bytes()).hexdigest(),
        'claims':[T.sample_claim(),T.sample_meta()],'graph':{'nodes':nodes,'edges':edges,'routes':routes}}

class Typed(unittest.TestCase):
    def setUp(self):self.obj=fixture()
    def test_original_example_good(self):self.assertEqual([],validate(self.obj))
    def test_model_not_observed(self):self.obj['claims'][0]['source_status']='MODEL_OR_FICTION';self.assertTrue(validate(self.obj))
    def test_world_actor_reduced_to_src(self):
        self.obj['graph']['routes']['WORLD_TO_ACTOR']['edge_ids']=['e1'];self.assertTrue(validate(self.obj))
    def test_wave_false_comparability(self):self.obj['claims'][0]['claim_wave_comparable']=True;self.assertTrue(validate(self.obj))
    def test_household_to_person(self):self.obj['claims'][0]['source_unit']='HOUSEHOLD';self.assertTrue(validate(self.obj))
    def test_policy_pin_required(self):self.obj.pop('mainmac_policy_sha256');self.assertTrue(validate(self.obj))
if __name__=='__main__':unittest.main(verbosity=2)
