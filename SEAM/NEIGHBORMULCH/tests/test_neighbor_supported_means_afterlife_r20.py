"""The same room becomes a different practical situation after nonresponse.
Actual support, independently authored trial, lived interruption, solo relief,
optional functional correspondence, actual trial, consolidation and suspension.
"""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter
import mii

def policy(stage, nominate=True, consolidate=True, seen=None):
    fallback=HeuristicSemanticProvider()
    def cb(task,packet):
        if task=='actor_attempt':
            alternatives=packet['practical_options']
            trials=packet['possible_end_trials']
            if stage=='supported_trial':
                choices=[t for t in trials if t.get('selected_human_food_offer_ref')]
                if len(choices)==1:return {'task':task,'possible_end_trial_id':choices[0]['trial_id']}
            if stage=='recruit':
                choices=[t for t in trials if t.get('functional_bridge_ref') and t['operation']=='EAT']
                if len(choices)==1:return {'task':task,'possible_end_trial_id':choices[0]['trial_id']}
            if stage=='independent':
                choices=[x for x in alternatives if x['operation']=='EAT' and x.get('project_id')=='own-meal']
                if len(choices)==1:return {'task':task,'practical_option_id':choices[0]['option_id']}
            if stage in ('seed','interrupt'):
                choices=[x for x in alternatives if x['operation']=='SIGNAL'
                         and x['world_request']['addressed_party_ref']=='visitor'
                         and bool(x.get('human_food_offer_ref'))==(stage=='seed')]
                if len(choices)==1:return {'task':task,'practical_option_id':choices[0]['option_id']}
            return {'task':task,'action':'WAIT'}
        if task=='development':
            e=packet['experience']
            if stage=='seed' and e.get('own_action')=='SIGNAL' and e.get('status')=='PERFORMED' and not packet['actor_possible_ends']:
                sign=next(c for c in e['perceived_cues'] if c['kind']=='visitor_food_offer')
                return {'task':task,'candidates':[{
                    'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':sign['id'],
                    'possible_object':'seek bodily nourishment','possible_means':['SIGNAL'],
                    'cue_terms':['food']}]}
            candidates=[c for c in packet.get('historically_proposed_functional',[])
                         if c.get('dissimilar_means_basis',{}).get('interrupted_supported_trial_basis')]
            revisions=packet.get('historically_possible_functional_revisions',[])
            if seen is not None:seen.extend(deepcopy(candidates+revisions))
            if stage=='independent' and candidates and nominate:
                return {'task':task,'candidates':candidates[:1]}
            return {'task':task,'candidates':revisions if consolidate else []}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(cb))

class SupportedMeansAfterlifeR20(unittest.TestCase):
    def build(self,name):
        return inherited.MaterialSupportR17.build(self,name,held=2,own=4)
    def history(self,name,interrupted,nominate=True):
        rt,n,db=self.build(name)
        n.contribute('seed','OFFER_FEED',target_actor_ref='worker')
        rt.semantic=policy('seed')
        self.assertEqual(n.independent_actor_beat('worker')['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
        n.contribute('trial','OFFER_FEED',target_actor_ref='worker')
        rt.semantic=policy('supported_trial')
        self.assertEqual(n.independent_actor_beat('worker')['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
        a=rt.snapshot('worker')
        end=a['possible_ends'][0]
        self.assertEqual(len(end['trial_history']),1)
        self.assertEqual(end['trial_history'][0]['offered_by_ref'],'visitor')
        self.assertEqual(rt.ledger.world(name)[1]['holdings']['visitor']['food'],0)
        rt.semantic=policy('interrupt' if interrupted else 'wait')
        r=n.independent_actor_beat('worker')
        self.assertEqual((r['attempt'],r['status']),('SIGNAL','PARTIAL') if interrupted else ('WAIT','PERFORMED'))
        n.contribute('departure','LEAVE')
        seen=[]
        rt.semantic=policy('independent',nominate=nominate,seen=seen)
        r=n.independent_actor_beat('worker')
        self.assertEqual((r['attempt'],r['status']),('EAT','PERFORMED'))
        a=rt.snapshot('worker')
        self.assertEqual(a['possible_ends'][0],end)
        self.assertEqual(len(seen),int(interrupted))
        bridges=[b for b in a['functional_bindings'] if b.get('dissimilar_means_basis',{}).get('interrupted_supported_trial_basis')]
        self.assertEqual(len(bridges),int(interrupted and nominate))
        if bridges:
            self.assertIn('nutrition',bridges[0]['dissimilar_means_basis']['shared_lived_relief_axes'])
            self.assertEqual(bridges[0]['dissimilar_means_basis']['earlier_location'],'workshop')
            self.assertEqual(bridges[0]['dissimilar_means_basis']['later_location'],'workshop')
        self.assertEqual(rt.ledger.world(name)[1]['holdings']['worker']['food'],3)
        self.assertTrue(rt.verify()['valid'])
        return rt,n,db,bridges

    def test_interruption_and_optional_acquisition_change_cold_recruitment(self):
        for interrupted,nominate in ((True,True),(True,False),(False,True)):
            with self.subTest(interrupted=interrupted,nominate=nominate):
                name='arm'+str(interrupted)+str(nominate)
                rt,n,db,bridges=self.history(name,interrupted,nominate)
                before=rt.snapshot('worker')
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=policy('recruit'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                self.assertEqual(cold.snapshot('worker')['functional_bindings'],before['functional_bindings'])
                chosen=nn.independent_actor_beat('worker')
                self.assertEqual(chosen['attempt'],'EAT' if bridges else 'WAIT')
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['worker']['food'],2 if bridges else 3)
                if bridges:
                    self.assertEqual(cold.snapshot('worker')['possible_ends'][0]['trial_history'][-1]['functional_bridge_ref'],bridges[0]['id'])
                self.assertTrue(cold.verify()['valid'])

    def test_actual_repeated_alternative_consolidates_and_material_exhaustion_suspends(self):
        rt,n,db,bridges=self.history('revision',True)
        bridge=bridges[0]
        rt.semantic=policy('recruit')
        self.assertEqual(n.independent_actor_beat('worker')['attempt'],'EAT')
        # Actual elapsed actor activity reduces nutrition; no body edits.
        rt.semantic=policy('wait')
        for _ in range(30):n.independent_actor_beat('worker')
        rt.semantic=policy('independent')
        self.assertEqual(n.independent_actor_beat('worker')['status'],'PERFORMED')
        b=next(b for b in rt.snapshot('worker')['functional_bindings'] if b['id']==bridge['id'])
        self.assertEqual(b['status'],'ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS')
        self.assertEqual(b['dissimilar_means_basis'],bridge['dissimilar_means_basis'])
        rt.close()
        cold=ConstitutiveRuntime(db,world_id='revision',semantic=policy('recruit'))
        self.addCleanup(cold.close)
        nn=NeighborEncounter(cold,'visitor',mii_module=mii)
        self.assertEqual(nn.independent_actor_beat('worker')['attempt'],'EAT')
        self.assertEqual(cold.ledger.world('revision')[1]['holdings']['worker']['food'],0)
        self.assertEqual(nn.independent_actor_beat('worker')['status'],'BLOCKED')
        final=next(b for b in cold.snapshot('worker')['functional_bindings'] if b['id']==bridge['id'])
        self.assertEqual(final['status'],'SUSPENDED_CONDITIONAL_FUNCTIONAL_MEANS')
        self.assertEqual([r['mode'] for r in final['revision_history']],['CONSOLIDATE','SUSPEND'])
        self.assertEqual(final['revision_history'][0],b['revision_history'][0])
        self.assertEqual(cold.snapshot('worker')['possible_ends'][0]['possible_means'],['SIGNAL'])
        self.assertEqual(nn.independent_actor_beat('worker')['attempt'],'WAIT')
        self.assertTrue(cold.verify()['valid'])

if __name__=='__main__':unittest.main()
