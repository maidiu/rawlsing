"""Actual held food, authored offer, distinct acceptance, material dependency.
Same CO owners for world feeding, participation, learning and recruitment.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_joint_practice_r15 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

def policy(stage, acquire=False):
    fallback=HeuristicSemanticProvider()
    def callback(task,packet):
        if task=='actor_attempt':
            grounds=({'EXPLORATORY_VISITOR_SUPPORT_SIGNAL',
                      'ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY',
                      'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'}
                     if stage in ('explore','generic') else
                     {'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'})
            options=[x for x in packet['practical_options']
                    if x['operation']=='SIGNAL' and x.get('grounds_status') in grounds
                    and x['world_request']['addressed_party_ref']=='visitor']
            if stage!='generic':
                actual=[x for x in options if x.get('human_food_offer_ref')]
                if actual: options=actual
            else:
                options=[x for x in options if not x.get('human_food_offer_ref')]
            if len(options)==1:
                return {'task':task,'action':'SIGNAL',
                        'practical_option_id':options[0]['option_id']}
            if stage=='alternative':
                meals=[x for x in packet['practical_options']
                       if x['operation']=='EAT' and x.get('project_id')=='own-meal']
                if len(meals)==1:
                    return {'task':task,'action':'EAT',
                            'practical_option_id':meals[0]['option_id']}
            return {'task':task,'action':'WAIT'}
        if task=='development':
            return {'task':task,'candidates':(
                packet.get('historically_possible_joint_practices',[])
                if acquire else [])}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(callback))


class MaterialSupportR17(unittest.TestCase):
    def build(self,name,*,held=2,own=1,blocked=False,user_hearing=True,user_visible=True,actor_visible=True):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_r17_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name,semantic=policy('explore'))
        self.addCleanup(rt.close)
        world=blank_world(name)
        world['holdings']={'visitor':{'food':held},'worker':{'food':own}}
        world['sites']['workshop']['food']=0
        if blocked:
            world['institutional_access_rules'].append({
                'id':'withheld-food-right','source_ref':'authored-rule',
                'operation':'FEED','location':'workshop',
                'all_of':[{'kind':'RECORDED_POSITION','field':'food_authority','equals':'allowed'}]})
        actor=adult('worker','Mara','workshop')
        actor['body']['nutrition']=.30
        actor['projects']=[{'id':'own-meal','object':'obtain nourishment',
                           'motive':'ordinary material reproduction',
                           'means':['EAT'],'priority':.4,'status':'active'}]
        rt.ledger.initialize(world,[actor])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit' if user_visible else 'dark',
                'sightline':'unobstructed' if user_visible else 'blocked',
                'hearing':user_hearing,'sound_path':'audible' if user_hearing else 'blocked',
                'legibility':'readable'}
                for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':'entrance','visual':actor_visible,
                'light':'lit' if actor_visible else 'dark',
                'sightline':'unobstructed' if actor_visible else 'blocked',
                'hearing':True,'sound_path':'audible'}}},
            request_id='geometry')
        n.contribute('arrival','MOVE',destination='workshop')
        return rt,n,db

    def test_actual_distributed_nourishment_acquisition_and_loss_of_support(self):
        for acquire in (True,False):
            with self.subTest(acquire=acquire):
                name='acquired' if acquire else 'declined'
                rt,n,db=self.build(name)
                first=n.independent_actor_beat('worker')
                self.assertEqual((first['attempt'],first['status']),('SIGNAL','PARTIAL'))
                before=deepcopy(rt.ledger.actors())
                offered=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                self.assertEqual(offered['status'],'PERFORMED')
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(rt.ledger.world(name)[1]['holdings']['visitor']['food'],2)
                rt.semantic=policy('explore',acquire)
                joined=n.independent_actor_beat('worker')
                self.assertEqual(joined['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
                world=rt.ledger.world(name)[1]
                actor=rt.ledger.actor('worker')[1]
                receipt=world['material_feeding_events'][-1]
                self.assertEqual(receipt['human_authored_offer_ref'],offered['event_ref'])
                self.assertEqual(receipt['food_consumed'],1)
                self.assertEqual(receipt['nutrition_effect'],.12)
                self.assertEqual(world['holdings']['visitor']['food'],1)
                self.assertEqual(world['holdings']['worker']['food'],1)
                self.assertGreater(actor['body']['nutrition'],before['worker']['body']['nutrition'])
                self.assertEqual(len(actor['joint_practices']),int(acquire))
                self.assertEqual(actor['participation_history'][-1]['reciprocated_partner_actor_visible'],'visitor')
                self.assertNotIn('visitor',rt.ledger.actors())
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=policy('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                later=nn.independent_actor_beat('worker')
                self.assertEqual(later['attempt'],'SIGNAL' if acquire else 'WAIT')
                self.assertEqual(later['status'],'PARTIAL' if acquire else 'PERFORMED')
                self.assertEqual(len(cold.ledger.world(name)[1]['material_feeding_events']),1)
                nn.contribute('second-offer','OFFER_FEED',target_actor_ref='worker')
                second=nn.independent_actor_beat('worker')
                self.assertEqual(second['attempt'],'SIGNAL' if acquire else 'WAIT')
                self.assertEqual(len(cold.ledger.world(name)[1]['material_feeding_events']),2 if acquire else 1)
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['visitor']['food'],0 if acquire else 1)
                nn.contribute('leave','LEAVE')
                cold.semantic=policy('alternative')
                independent=nn.independent_actor_beat('worker')
                self.assertEqual((independent['attempt'],independent['status']),('EAT','PERFORMED'))
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['worker']['food'],0)
                self.assertEqual(len(cold.ledger.actor('worker')[1]['joint_practices']),int(acquire))
                exhausted=nn.independent_actor_beat('worker')
                self.assertEqual((exhausted['attempt'],exhausted['status']),('EAT','BLOCKED'))
                self.assertTrue(cold.verify()['valid'])

    def test_no_transfer_for_generic_signal_expired_offer_or_missing_stock(self):
        for mode in ('generic','stale','empty','rule'):
            with self.subTest(mode=mode):
                rt,n,_=self.build(mode,held=0 if mode=='empty' else 1,blocked=mode=='rule')
                first=n.independent_actor_beat('worker')
                self.assertEqual(first['status'],'PARTIAL')
                out=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                self.assertEqual(out['status'],'BLOCKED' if mode in ('empty','rule') else 'PERFORMED')
                if mode=='stale':n.contribute('elapsed','WAIT')
                rt.semantic=policy('generic' if mode=='generic' else 'explore',True)
                result=n.independent_actor_beat('worker')
                self.assertEqual(result['status'],'PARTIAL')
                w=rt.ledger.world(mode)[1]
                self.assertEqual(w['material_feeding_events'],[])
                self.assertEqual(w['holdings']['visitor']['food'],0 if mode=='empty' else 1)
                self.assertEqual(rt.ledger.actor('worker')[1]['joint_practices'],[])
                count=rt.verify()['events']
                self.assertTrue(n.contribute('offer','OFFER_FEED',target_actor_ref='worker')['idempotent_replay'])
                self.assertEqual(rt.verify()['events'],count)
                self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
