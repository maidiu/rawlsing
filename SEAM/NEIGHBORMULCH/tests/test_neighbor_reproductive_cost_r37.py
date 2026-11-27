"""R37: actual support vs withdrawn undertaking, independent third-party
care and the material bearer of its cost; no knowledge of cancellation.
"""
import unittest
from copy import deepcopy
from pathlib import Path
import tempfile
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world,canonical
from um_sorok_organism.material_provisioning import perform_one_actual_feeding
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter
import mii

class ReproductiveCostR37(unittest.TestCase):
    def course(self,mode,source=None,commons=0,decline=False,forge=False):
        phase='receive'; packets={}
        def cb(task,p):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            aid=p['actor']['id']; opts=p['practical_options']
            packets[aid]=deepcopy(p)
            if aid=='dependent' and phase=='receive':
                choices=[x for x in opts if x['operation']=='SIGNAL'
                         and x['world_request']['addressed_party_ref']=='visitor']
                actual=[x for x in choices if x.get('human_food_offer_ref')]
                generic=[x for x in choices if not x.get('human_food_offer_ref')]
                chosen=(actual if actual and mode!='unaccepted' else generic)
                self.assertEqual(len(chosen),1)
                return {'task':task,'practical_option_id':chosen[0]['option_id']}
            if aid=='carer' and phase=='care':
                # The same policy reads an actual incomplete signal, never the
                # visitor's commitment status or the dependent's private body.
                incomplete=any(x.get('kind')=='performed_signal'
                    and x.get('source_actor')=='dependent'
                    and x.get('description')=='ATTEMPT_NOT_COMPLETED'
                    for x in p['accessible']['cues'])
                if incomplete and not decline:
                    choices=[x for x in opts if x['operation']=='FEED'
                             and x.get('project_id')=='care'
                             and x['world_request']['addressed_party_ref']=='dependent'
                             and x.get('selected_feeding_source')==source]
                    self.assertEqual(len(choices),1)
                    return {'task':task,'practical_option_id':
                        'not-an-issued-option' if forge else choices[0]['option_id']}
            if aid=='carer' and phase=='meal':
                return {'task':task,'action':'EAT','project_id':'meal'}
            return {'task':task,'action':'WAIT'}
        sem=ValidatingSemanticService(CallbackLLMProvider(cb))
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'life.sqlite')
            rt=ConstitutiveRuntime(db,semantic=sem)
            try:
                w=blank_world()
                w['sites']['home']['food']=0
                w['sites']['home']['mutual_aid_food']=commons
                w['holdings']={'visitor':{'food':1},'carer':{'food':1},'dependent':{'food':0}}
                dep=adult('dependent','Dependent')
                dep['body']['nutrition']=.30
                carer=adult('carer','Carer')
                carer['projects']=[
                    {'id':'care','object':'feed another','means':['FEED'],
                     'addressed_party_ref':'dependent','priority':.5,'status':'active'},
                    {'id':'meal','object':'own meal','means':['EAT'],
                     'priority':.5,'status':'active'}]
                rt.ledger.initialize(w,[dep,carer])
                n=NeighborEncounter(rt,'visitor',mii_module=mii)
                n.install_sourcefree_conditions({
                    'grade':'SOURCEFREE_TEST_ONLY',
                    'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                        'hearing':True,'sound_path':'audible','legibility':'readable'}},
                    'actor_conditions':{a:{'facing':'entrance','visual':True,
                        'light':'lit','sightline':'unobstructed','hearing':True,
                        'sound_path':'audible'} for a in ('dependent','carer')}},
                    request_id='geometry')
                n.contribute('arrival','MOVE',destination='home')
                pledge=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='dependent',
                    due_clock=rt.ledger.world()[1]['clock']+6)
                before=deepcopy(rt.ledger.actors())
                if mode=='withdrawn':
                    act=n.contribute('withdraw','WITHDRAW_PLEDGE',
                        target_commitment_ref=pledge['human_offer_commitment_ref'])
                else:
                    act=n.contribute('offer','OFFER_FEED',target_actor_ref='dependent')
                self.assertEqual(act['status'],'PERFORMED')
                self.assertEqual(rt.ledger.actors(),before)
                first=n.independent_actor_beat('dependent')
                fed=(mode=='fulfilled')
                self.assertEqual(first['status'],'PERFORMED' if fed else 'PARTIAL')
                phase='care'
                if forge:
                    before=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
                    with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
                        n.independent_actor_beat('carer')
                    self.assertEqual(rt.ledger.world(),before)
                    self.assertEqual(rt.ledger.actors(),actors)
                    return
                response=n.independent_actor_beat('carer')
                substituted=not fed and not decline
                self.assertEqual(response['attempt'],'FEED' if substituted else 'WAIT')
                world=rt.ledger.world()[1]
                rows=world['material_feeding_events']
                self.assertEqual(len(rows),int(fed or substituted))
                if rows:
                    self.assertEqual(rows[0]['giver'],'visitor' if fed else 'carer')
                    self.assertEqual(rows[0]['recipient'],'dependent')
                if substituted and source:
                    self.assertEqual(rows[0]['explicit_actor_selected_food_source'],source)
                    self.assertEqual(rows[0]['food_pool_before']-rows[0]['food_pool_after'],1)
                self.assertNotIn('withdrawal_user_event_ref',canonical(packets['carer']))
                self.assertNotIn('WITHDRAWN_BY_AUTHORED_ACT',canonical(packets['carer']))
                self.assertNotIn('visitor',rt.ledger.actors())
                labor=deepcopy(world['social_reproductive_labor'])
                self.assertEqual(len(labor),int(fed or substituted))
                meal_stock=world['holdings']['carer']['food']
                pool=world['sites']['home']['mutual_aid_food']
                rest=rt.ledger.actor('carer')[1]['body']['rest']
                practiced=len(rt.ledger.actor('carer')[1]['performed_feeding_events'])
                self.assertEqual(practiced,int(substituted))
                self.assertEqual(rt.ledger.actor('dependent')[1]['memories'],[])
                # Actual cost survives cold return and affects a later
                # independently chosen meal. No automatic gratitude/resentment.
                rt.close()
                rt=ConstitutiveRuntime(db,semantic=sem)
                n=NeighborEncounter(rt,'visitor',mii_module=mii)
                phase='meal'
                meal=n.independent_actor_beat('carer')
                self.assertEqual(rt.ledger.world()[1]['social_reproductive_labor'],labor)
                self.assertTrue(rt.verify()['valid'])
                return (meal_stock,pool,rest,meal['status'],practiced)
            finally:rt.close()

    def test_withdrawal_and_unaccepted_offer_redistribute_cost_not_commitment_label(self):
        fulfilled=self.course('fulfilled')
        withdrawn=self.course('withdrawn')
        unaccepted=self.course('unaccepted')
        declined=self.course('withdrawn',decline=True)
        self.assertEqual(fulfilled[0],1)
        self.assertEqual(withdrawn[0],0)
        self.assertEqual(withdrawn,unaccepted)
        self.assertLess(withdrawn[2],fulfilled[2])
        self.assertEqual(withdrawn[3],'BLOCKED')
        self.assertEqual(fulfilled[3],'PERFORMED')
        self.assertEqual(declined[0],1)
        self.assertEqual(declined[4],0)

    def test_distinct_material_sources_preserve_distinct_bearers(self):
        own=self.course('withdrawn',source='GIVER_HELD_FOOD',commons=1)
        common=self.course('withdrawn',source='MUTUAL_AID_FOOD',commons=1)
        self.assertEqual(own[:2],(0,1))
        self.assertEqual(common[:2],(1,0))
        self.assertEqual(own[2:],common[2:])

    def test_forged_actor_selection_rolls_back(self):
        self.course('withdrawn',source='MUTUAL_AID_FOOD',commons=1,forge=True)

    def test_explicit_unavailable_source_does_not_fallback_to_private_stock(self):
        w=blank_world();w['positions']={'carer':'home','dependent':'home'}
        w['holdings']={'carer':{'food':1}}
        actors={'carer':adult('carer','Carer'),'dependent':adult('dependent','Dependent')}
        before=deepcopy((w,actors))
        result=perform_one_actual_feeding(w,actors,'carer','dependent','home',
            'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE',
            selected_food_source='MUTUAL_AID_FOOD')
        self.assertEqual(result['status'],'BLOCKED')
        self.assertEqual((w,actors),before)

if __name__=='__main__':unittest.main()
