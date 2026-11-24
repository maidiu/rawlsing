"""An actual offer, an independent particular refusal, and silence differ.
R19 uses the existing world, practical alternatives, and private MII reader.
"""
from copy import deepcopy
from pathlib import Path
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter
import mii

def signs(view):
    return [x['text'] for x in view['mandatory']
            if x['kind']=='CO_PUBLIC_OCCURRENCE']

def refusal_policy(choice, seen=None):
    fallback=HeuristicSemanticProvider()
    def cb(task,packet):
        if task=='actor_attempt':
            choices=[x for x in packet['practical_options']
                     if x.get('grounds_status')=='CURRENT_PARTICULAR_FOOD_OFFER_REFUSAL']
            if seen is not None:seen.extend(deepcopy(choices))
            if choice=='refuse' and len(choices)==1:
                return {'task':task,'practical_option_id':choices[0]['option_id']}
            if choice=='generic' and choices:
                return {'task':task,'action':'REFUSE'}
            if choice=='accept':
                choices=[x for x in packet['practical_options']
                         if x.get('binding_status')=='CURRENT_HELD_FOOD_OFFER_ACCEPTANCE']
                if len(choices)==1:return {'task':task,'practical_option_id':choices[0]['option_id']}
            return {'task':task,'action':'WAIT'}
        if task=='development':return {'task':task,'candidates':[]}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(cb))

class MaterialRefusalR19(unittest.TestCase):
    def build(self,name,**kwargs):
        return inherited.MaterialSupportR17.build(self,name,**kwargs)

    def test_refusal_acceptance_and_abstention_are_different_material_histories(self):
        for choice in ('refuse','accept','wait','generic'):
            with self.subTest(choice=choice):
                rt,n,db=self.build(choice)
                # The actor first encounters an independently authored offer.
                other=NeighborEncounter(rt,'bystander',mii_module=mii)
                other.contribute('arrive','MOVE',destination='workshop')
                offer=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                self.assertEqual(offer['status'],'PERFORMED')
                seen=[]
                rt.semantic=refusal_policy(choice,seen)
                profile=n.new_private_profile()
                # Existing scheduler chooses actual continuing actor.
                beat=n.continue_independent_life_during_visit(profile=profile)
                self.assertEqual(beat['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
                self.assertEqual(len(seen),1)
                self.assertEqual(seen[0]['human_food_offer_ref'],offer['event_ref'])
                last=rt.ledger.events()[-1]
                payload=last['envelope']['payload']
                actual=payload['actual']
                w=rt.ledger.world(choice)[1]
                self.assertEqual(w['holdings']['visitor']['food'],2-int(choice=='accept'))
                self.assertEqual(len(w['material_feeding_events']),int(choice=='accept'))
                self.assertEqual(actual.get('human_food_offer_refused_event_ref'),
                                 offer['event_ref'] if choice=='refuse' else None)
                observed=signs(beat['visitor_surface'])
                self.assertEqual('The offered food is declined.' in observed,choice=='refuse')
                self.assertEqual('The offered food is taken.' in observed,choice=='accept')
                self.assertNotIn('The offered food is declined.',
                                 signs(other.private_surface(other.new_private_profile())))
                if choice=='refuse':
                    self.assertEqual(actual['outcome'],'PARTICULAR_HUMAN_FOOD_OFFER_REFUSED')
                    self.assertEqual(actual['status'],'PERFORMED')
                    exp=payload['private_actor_experience_receipts']['worker']
                    self.assertIsNone(exp['reciprocated_partner'])
                    self.assertTrue(any(c.get('visitor_event_ref')==offer['event_ref']
                                        for c in exp['perceived_cues']))
                    self.assertFalse(any(x['kind']=='PUBLIC_TIP'
                                         for x in beat['visitor_surface']['mandatory']))
                    self.assertEqual(rt.ledger.actor('worker')[1]['joint_practices'],[])
                    sidecar=Path(db).with_suffix('.mii.json')
                    n.save_private_profile(sidecar,profile)
                    before=deepcopy(rt.ledger.world(choice))
                    rt.close()
                    cold=ConstitutiveRuntime(db,world_id=choice,semantic=refusal_policy('accept'))
                    self.addCleanup(cold.close)
                    nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                    self.assertEqual(signs(nn.private_surface_stored(sidecar)),observed)
                    self.assertEqual(cold.ledger.world(choice),before)
                    # Prior refusal doesn't grant permanent refusal or assent.
                    fresh=nn.contribute('fresh','OFFER_FEED',target_actor_ref='worker')
                    self.assertNotEqual(fresh['event_ref'],offer['event_ref'])
                    nn.independent_actor_beat('worker')
                    final=cold.ledger.world(choice)[1]
                    self.assertEqual(final['holdings']['visitor']['food'],1)
                    self.assertEqual(final['material_feeding_events'][-1]['human_authored_offer_ref'],
                                     fresh['event_ref'])
                    self.assertEqual(len(final['material_feeding_events']),1)
                    self.assertTrue(cold.verify()['valid'])
                else:
                    self.assertTrue(rt.verify()['valid'])

    def test_expired_or_unrelated_offer_cannot_be_refused_as_particular(self):
        for mode in ('expired','unrelated','no_stock','unseen'):
            with self.subTest(mode=mode):
                rt,n,_=self.build(mode,held=0 if mode=='no_stock' else 2,
                                  actor_visible=mode!='unseen')
                if mode=='unrelated':
                    # Actual unrelated speech is not a material offer.
                    n.contribute('unrelated','SAY',text='Hello.')
                else:
                    offered=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                    if mode=='unseen':self.assertEqual(offered['status'],'PERFORMED')
                    if mode=='expired':n.contribute('elapsed','WAIT')
                seen=[]
                rt.semantic=refusal_policy('refuse',seen)
                result=n.independent_actor_beat('worker')
                self.assertEqual(seen,[])
                self.assertEqual(result['attempt'],'WAIT')
                self.assertNotIn('The offered food is declined.',signs(n.private_surface(n.new_private_profile())))
                self.assertEqual(rt.ledger.world(mode)[1]['material_feeding_events'],[])
                self.assertTrue(rt.verify()['valid'])

    def test_stale_refusal_option_cannot_bind_a_later_event(self):
        rt,n,_=self.build('stale_option')
        n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
        seen=[]
        rt.semantic=refusal_policy('wait',seen)
        n.independent_actor_beat('worker')
        self.assertEqual(len(seen),1)
        old=seen[0]['option_id']
        n.contribute('fresh','OFFER_FEED',target_actor_ref='worker')
        before=deepcopy(rt.ledger.world('stale_option'))
        actors=deepcopy(rt.ledger.actors())
        count=len(rt.ledger.events())
        fallback=HeuristicSemanticProvider()
        def forged(task,packet):
            if task=='actor_attempt':return {'task':task,'practical_option_id':old}
            return fallback.propose(task,packet)
        rt.semantic=ValidatingSemanticService(CallbackLLMProvider(forged))
        with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
            n.independent_actor_beat('worker')
        self.assertEqual(rt.ledger.world('stale_option'),before)
        self.assertEqual(rt.ledger.actors(),actors)
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
