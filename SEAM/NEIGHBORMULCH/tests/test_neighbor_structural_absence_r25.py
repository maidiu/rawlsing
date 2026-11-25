"""Actual qualified care under independent structural history, during
the same absent interval as an independently authored human undertaking.
No simulated visitor action, child memory or actor appraisal of a deadline.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.material_conjunction import admit_authored_structural_history
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

def service():
    def cb(task,packet):
        if task=='development':return {'task':task,'candidates':[]}
        if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
        return {'task':task,'action':'WAIT'}
    return ValidatingSemanticService(CallbackLLMProvider(cb))

class StructuralAbsenceR25(unittest.TestCase):
    def build(self,name,blocked):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r25_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name,semantic=service())
        self.addCleanup(rt.close)
        w=blank_world(name)
        mother=adult('mother','Mother')
        mother['projects']=[{'id':'care','object':'care for child','means':['CARE'],
                            'status':'active','priority':.5},
                            {'id':'practice','object':'practice movement','means':['PRACTICE'],
                             'status':'active','priority':.5}]
        child=newborn('nadia','Nadia')
        spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY','source_ref':'fictional:period_world',
              'positions':[{'id':'p0','actor':'mother','field':'care_access','value':'admitted',
                            'source_ref':'fictional:p0','effective_from':0,'effective_until':5},
                           {'id':'p1','actor':'mother','field':'care_access',
                            'value':'excluded' if blocked else 'admitted',
                            'source_ref':'fictional:p1','effective_from':6,'effective_until':8}],
              'rules':[{'id':'care_gate','operation':'CARE','location':'home',
                        'source_ref':'fictional:care_gate','effective_from':0,'effective_until':8,
                        'all_of':[{'kind':'RECORDED_POSITION','field':'care_access','equals':'admitted'}]}]}
        admit_authored_structural_history(w,{'mother','nadia'},spec)
        rt.ledger.initialize(w,[mother,child],
            source_seals=[('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
        rows=[]
        for kind in ('QUALIFIED_REPRODUCTIVE_CARE','QUALIFIED_ROUTINE_PRACTICE'):
            reg=rt.register_historical_routine_source({
                'kind':kind,'actor':'mother','location':'home','start_clock':0,
                'end_clock':20,'max_hours_per_active_day':3,
                'description':'bounded fictional routine'})
            row={'kind':kind,'actor':'mother','location':'home',
                 'source_ref':reg['source_ref'],'hours_per_active_day':3,
                 'provisional_exposure_fraction':1.0}
            if kind=='QUALIFIED_REPRODUCTIVE_CARE':row['recipient']='nadia'
            else:row.update({'operation':'PRACTICE','mode':'SOLO_COMPONENT_PRACTICE'})
            rows.append(row)
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                   'hearing':True,'sound_path':'audible','legibility':'readable'}},
            'actor_conditions':{a:{'facing':'entrance','visual':True,
                    'light':'lit','sightline':'unobstructed',
                    'hearing':True,'sound_path':'audible'} for a in ('mother','nadia')}},
            request_id='geometry')
        self.assertEqual(n.contribute('arrive','MOVE',destination='home')['status'],'PERFORMED')
        pledge=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='mother',due_clock=6)
        self.assertEqual(pledge['status'],'PERFORMED')
        dep=n.contribute('leave','LEAVE')
        self.assertEqual(rt.ledger.world(name)[1]['clock'],4)
        return rt,n,db,rows,dep['event_ref'],pledge['human_offer_commitment_ref']

    def test_actual_structural_care_and_coincident_deadline_across_cold_absence(self):
        outcomes={}
        for blocked in (True,False):
            with self.subTest(blocked=blocked):
                name='case'+str(blocked)
                rt,n,db,rows,dep,pledge=self.build(name,blocked)
                # At the very same boundary, both owners settle: care
                # eligibility changes and the human window elapses.
                departure_clock=rt.ledger.world(name)[1]['clock']
                initial_age=rt.snapshot('nadia')['age_days']
                first=n.continue_absent_life_until(dep,6,max_segments=12,period_processes=rows)
                self.assertEqual(first['actual_modeled_clock'],6)
                w=rt.ledger.world(name)[1]
                self.assertEqual(n.own_food_commitments()[0]['settled_at_clock'],6)
                self.assertEqual(w['historical_periods'][-1]['elapsed_human_offer_commitment_refs'],[pledge])
                child=rt.snapshot('nadia')
                self.assertEqual(len(child['undergone_care_periods']),1)
                self.assertEqual(child['age_days'],initial_age+6-departure_clock)
                self.assertEqual(child['memories'],[])
                saved=deepcopy(w['historical_periods'])
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=service())
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                result=nn.continue_absent_life_until(dep,9,max_segments=12,period_processes=rows)
                self.assertEqual(result['actual_modeled_clock'],9)
                w=cold.ledger.world(name)[1]
                self.assertEqual(w['historical_periods'][:len(saved)],saved)
                held=[p for period in w['historical_periods'] for p in period.get('structurally_withheld_processes',[])]
                self.assertEqual(len(held),int(blocked))
                if blocked:
                    self.assertEqual(held[0]['operation'],'CARE')
                    self.assertEqual(held[0]['objective_rule_evaluation']['decision'],'BLOCKED')
                self.assertEqual(cold.snapshot('nadia')['age_days'],initial_age+9-departure_clock)
                self.assertEqual(len(cold.snapshot('nadia')['undergone_care_periods']),1 if blocked else 2)
                self.assertEqual(len(cold.snapshot('mother')['practice_exposures']),2)
                # Stop at 12 using the same owner; no retrospective filling.
                nn.continue_absent_life_until(dep,12,period_processes=rows)
                w=cold.ledger.world(name)[1]
                self.assertEqual(w['clock'],12)
                self.assertEqual(w['neighbor_user_events'][-1]['event_ref'],dep)
                self.assertEqual(nn.own_food_commitments()[0]['status'],'WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER')
                self.assertEqual(sum(pledge in p.get('elapsed_human_offer_commitment_refs',[]) for p in w['historical_periods']),1)
                self.assertTrue(any(x['start_clock']>=9 for x in w['reproductive_labor_periods']))
                outcomes[blocked]=sum(x['modeled_labor_hours'] for x in w['reproductive_labor_periods'])
                count=len(cold.ledger.events())
                nn.continue_absent_life_until(dep,12,period_processes=rows)
                self.assertEqual(len(cold.ledger.events()),count)
                self.assertEqual(nn.contribute('return','MOVE',destination='home')['status'],'PERFORMED')
                view=nn.private_surface(nn.new_private_profile())
                self.assertTrue(view['return_context']['intervening_life_not_disclosed'])
                self.assertNotIn('structurally_withheld_processes',str(view))
                self.assertNotIn('undergone_care_periods',str(view))
                self.assertTrue(cold.verify()['valid'])
        self.assertEqual(outcomes[False]-outcomes[True],9.0)

    def test_unqualified_routine_never_becomes_offscreen_visitor_conduct(self):
        rt,n,_,rows,dep,_=self.build('invalid',True)
        before=deepcopy(rt.ledger.world('invalid'))
        actors=deepcopy(rt.ledger.actors())
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'INVALID_ABSENCE_PERIOD_PROCESSES'):
            n.continue_absent_life_until(dep,6,period_processes=[{'kind':'invented_visitor_action'}])
        forged=deepcopy(rows);forged[0]['source_ref']='forged'
        with self.assertRaises(ValueError):
            n.continue_absent_life_until(dep,6,period_processes=forged)
        self.assertEqual(rt.ledger.world('invalid'),before)
        self.assertEqual(rt.ledger.actors(),actors)
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
