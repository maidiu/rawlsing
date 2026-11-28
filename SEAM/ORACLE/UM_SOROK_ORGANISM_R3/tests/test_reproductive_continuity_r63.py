"""R63: material workload, plural care and later independent child address.

The two periods are declared fictional aggregate histories, not individual
episodes or inferred caregiver willingness. Both arms use the same policy.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.organism import eligible
from um_sorok_organism.plural_care_paths import choose_one_grounded_plural_acquisition
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService

class ReproductiveContinuity(unittest.TestCase):
    def arm(self,db,work):
        phase={'stage':'orient'}
        def cb(task,p):
            aid=p.get('actor',{}).get('id')
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='development':
                if aid=='nadia':
                    return {'task':task,'candidates':choose_one_grounded_plural_acquisition(
                        p.get('historically_possible_plural_care',[]))}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if phase['stage']=='care' and aid in ('mother','father'):
                    opts=[o for o in p['practical_options'] if o['operation']=='CARE'
                          and o.get('world_request',{}).get('addressed_party_ref')=='nadia']
                    if opts:return {'task':task,'practical_option_id':opts[0]['option_id']}
                if phase['stage']=='address' and aid=='nadia':
                    opts=[o for o in p['practical_options'] if
                          o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CO_REGULATION']
                    ranked=[]
                    for o in opts:
                        clocks=[x['event_clock'] for x in o.get('personally_sensed_support_history',[])
                                if x.get('bodily_regulation_sensed') is True]
                        if clocks:ranked.append((max(clocks),o))
                    if ranked:
                        chosen=max(ranked,key=lambda t:t[0])[1]
                        return {'task':task,'practical_option_id':chosen['option_id']}
                return {'task':task,'action':'WAIT'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            m=adult('mother','Mother','workshop');m['body']['rest']=.35
            f=adult('father','Father','workshop')
            n=newborn('nadia','Nadia','workshop');n['body']['comfort']=.2
            for a in (m,f):
                a['projects']=[{'id':'care:'+a['id'],'object':'care for Nadia',
                    'means':['CARE'],'addressed_party_ref':'nadia','priority':.6,'status':'active'}]
            m['projects'].append({'id':'wage','object':'subsistence','means':['WORK'],
                                  'priority':.5,'status':'active'})
            w=blank_world()
            rt.ledger.initialize(w,[m,f,n])
            rt.step('father',requested_action='CARE',target='nadia')
            rt.step('mother',requested_action='CARE',target='nadia')
            rt.step('nadia',requested_action='ORIENT')
            rt.step('nadia',requested_action='ORIENT')
            before=rt.ledger.actor('nadia')[1]
            self.assertEqual({x['caregiver_ref'] for x in before['co_regulation_orientations']},
                             {'mother','father'})
            start=rt.ledger.world()[1]['clock']
            src=rt.register_historical_routine_source({'kind':'QUALIFIED_WAGE_LABOR',
                'actor':'mother','location':'workshop','start_clock':start,'end_clock':start+100,
                'max_hours_per_active_day':8,'description':'bounded aggregate wage history'})
            proc={'kind':'QUALIFIED_WAGE_LABOR','actor':'mother','location':'workshop',
                'source_ref':src['source_ref'],'hours_per_active_day':8,'provisional_exposure_fraction':1.}
            for _ in range(2):rt.background(50,[proc] if work else [])
            state=rt.snapshot('mother')
            self.assertEqual(eligible(state['body'],'CARE')[0],not work)
            child=rt.ledger.actor('nadia')[1]
            self.assertEqual(child['age_days'],100)
            self.assertEqual(child['experienced_care_events'],before['experienced_care_events'])
            self.assertEqual(child['co_regulation_orientations'],before['co_regulation_orientations'])
            self.assertEqual(child['memories'],[])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            phase['stage']='care'
            self.assertEqual(rt.step('father')['attempt'],'CARE')
            self.assertEqual(rt.step('mother')['attempt'],'WAIT' if work else 'CARE')
            child=rt.ledger.actor('nadia')[1]
            expected='father' if work else 'mother'
            self.assertEqual(child['experienced_care_events'][-1]['giver_ref'],expected)
            phase['stage']='address'
            choice=rt.plan('nadia')
            self.assertEqual(choice.action,'SIGNAL')
            self.assertEqual(choice.target,expected)
            result=rt.step('nadia')
            self.assertEqual(result['attempt'],'SIGNAL')
            self.assertEqual(result['status'],'PARTIAL') # independently selected WAIT, not assumed care
            current=rt.ledger.actor('nadia')[1]
            self.assertEqual({x['caregiver_ref'] for x in current['co_regulation_orientations']},
                             {'mother','father'})
            self.assertTrue(rt.verify()['valid'])
            return expected
        finally:rt.close()

    def test_wage_history_changes_actual_care_and_child_address(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.arm(Path(d)/'work.sqlite',True),'father')
            self.assertEqual(self.arm(Path(d)/'other.sqlite',False),'mother')
