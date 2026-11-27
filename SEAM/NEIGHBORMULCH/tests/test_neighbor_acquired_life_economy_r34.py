"""R34 executed joined course; mock transport not live-model sufficiency."""
import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from constitutive_life_campaign import run_campaign, developmental_projection, size
from copy import deepcopy
from um_sorok_organism.types import canonical

class AcquiredLifeEconomyR34(unittest.TestCase):
    def test_joined_course_actual_consequences_and_wire_cost(self):
        arms=run_campaign()
        f,e,p,b,a=[arms[x] for x in ('F','E','P','Lbad','F_abstain')]
        self.assertEqual(f['state_digest'],e['state_digest'])
        self.assertEqual(f['wire_witness_digest'],e['wire_witness_digest'])
        self.assertEqual(f['actual_independent_course'],e['actual_independent_course'])
        def total(x,key):
            return sum(row[key] for row in x['cost']['by_task'].values())
        self.assertEqual(total(f,'calls'),total(e,'calls'))
        self.assertLess(total(e,'request_bytes'),total(f,'request_bytes'))
        self.assertEqual(p['state_digest'],f['state_digest'])
        self.assertEqual(p['actual_independent_course'],f['actual_independent_course'])
        self.assertEqual(total(p,'calls'),total(f,'calls'))
        self.assertLess(p['cost']['by_task']['development']['packet_bytes'],
                        f['cost']['by_task']['development']['packet_bytes'])
        self.assertGreater(p['cost']['projection_routes'].get('PROJECTED_ROTATING_PERIPHERY',0),0)
        self.assertGreater(p['cost']['projection_routes'].get('FULL_PERIODIC_OR_NO_ROSTER',0),0)
        for row in (f,e,p):
            self.assertEqual(row['new_material_project'],1)
            self.assertGreaterEqual(row['actual_material_project_exercises'],3)
            self.assertEqual(row['mother_actual_later_operation'],'ORIENT')
        for row in (b,a):
            self.assertEqual(row['new_material_project'],0)
            self.assertEqual(row['actual_material_project_exercises'],0)
            self.assertEqual(row['mother_actual_later_operation'],'WAIT')
        print('NEIGHBOR_R34_ACQUIRED_LIFE '+canonical(arms))

    def test_projection_retains_all_nonroster_fields_and_independent_expansion(self):
        full={'selected_constitution':{'candidate_actions':[
            {'action':str(i),'practical_alternatives':[{'binding_status':'LEGAL','detail':'x'*5000}]}
            for i in range(4)],'readset':['exact'],'currents':[{'opposed':True}]},
            'experience':{'actor':'a','perceived_cues':[{'id':'x'}]},
            'historically_possible_cross_object_significance':[{'basis':'exact'}],
            'historical_psychodynamic_context':{'untouched':True}}
        snapshot=deepcopy(full)
        for i in (1,2,3,4):
            p,route=developmental_projection(full,i)
            self.assertEqual(full,snapshot)
            if i==4:
                self.assertEqual(p,full)
                continue
            self.assertLess(size(p),size(full))
            self.assertEqual(p['experience'],full['experience'])
            self.assertEqual(p['selected_constitution']['currents'],full['selected_constitution']['currents'])
            self.assertEqual(p['historically_possible_cross_object_significance'],full['historically_possible_cross_object_significance'])
            self.assertEqual(p['developmental_roster_projection_analytic_only']['peripheral_exact_row'],
                full['selected_constitution']['candidate_actions'][i-1])

if __name__=='__main__':unittest.main()
