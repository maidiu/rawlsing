"""Same CO R37–39 formation and reorganization through actual human offers.
No synthetic actor, preloaded dependent project, or direct psychic mutation.
"""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from neighbor_runtime import NeighborEncounter
import mii

def initial(actor):
    actor['projects']=[]
    actor['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}

def policy(stage,*,reorganize=True,seen=None):
    fallback=HeuristicSemanticProvider()
    def cb(task,packet):
        if task=='actor_attempt':
            options=packet['practical_options']
            if stage in ('first','supported','interrupt','renew'):
                choices=[x for x in options if x['operation']=='SIGNAL'
                         and x.get('project_id') is None
                         and x['world_request']['addressed_party_ref']=='visitor'
                         and x.get('grounds_status') in (
                             'EXPLORATORY_VISITOR_SUPPORT_SIGNAL',
                             'HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE',
                             'ACTOR_PREVIOUSLY_EXPERIENCED_CONTINGENT_COACTIVITY')
                         and bool(x.get('human_food_offer_ref'))==(stage in ('supported','renew'))]
            elif stage=='trial':
                trials=[t for t in packet['possible_end_trials'] if t['operation']=='EAT']
                if len(trials)!=1:raise AssertionError('unique dependency trial required')
                return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
            elif stage in ('independent','revisit'):
                return {'task':task,'action':'EAT'}
            elif stage=='project':
                choices=[x for x in options if x['operation']=='EAT' and x.get('project_id')]
            elif stage in ('invite','accept'):
                choices=[x for x in options if x['operation']=='SIGNAL'
                         and x.get('project_id') and x.get('dependency_conditional_means_ref')
                         and bool(x.get('human_food_offer_ref'))==(stage=='accept')]
                if seen is not None:seen.extend(deepcopy(choices))
            else:choices=[]
            if len(choices)==1:return {'task':task,'practical_option_id':choices[0]['option_id']}
            return {'task':task,'action':'WAIT'}
        if task=='development':
            if stage=='supported':
                candidates=packet['historically_possible_joint_practices']
            elif stage=='independent':
                candidates=[g for g in packet['historically_possible_genetic_ends']
                            if g.get('dependency_loss_basis')]
            elif stage=='revisit':
                candidates=packet['historically_possible_dependency_takeups']
            elif stage=='renew':
                candidates=packet['historically_possible_dependency_project_reorganizations']
                if seen is not None:seen.extend(deepcopy(candidates))
                if not reorganize:candidates=[]
            else:candidates=[]
            return {'task':task,'candidates':candidates}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(cb))

class HumanProjectReconstitutionR23(unittest.TestCase):
    def build(self,name):
        return inherited.MaterialSupportR17.build(self,name,held=4,own=4,actor_setup=initial)
    def history(self,name,reorganize):
        rt,n,db=self.build(name)
        def beat(stage,**kw):
            rt.semantic=policy(stage,**kw)
            return n.independent_actor_beat('worker')
        self.assertEqual(beat('first')['status'],'PARTIAL')
        n.contribute('first-offer','OFFER_FEED',target_actor_ref='worker')
        self.assertEqual(beat('supported')['status'],'PERFORMED')
        practice=deepcopy(rt.snapshot('worker')['joint_practices'])
        self.assertEqual(len(practice),1)
        self.assertEqual(beat('interrupt')['status'],'PARTIAL')
        self.assertEqual(beat('independent')['status'],'PERFORMED')
        end=rt.snapshot('worker')['possible_ends'][0]
        self.assertEqual(end['dependency_loss_basis']['historical_counterpart_ref'],'visitor')
        self.assertEqual(beat('trial')['status'],'PERFORMED')
        for _ in range(8):beat('wait')
        self.assertEqual(beat('revisit')['status'],'PERFORMED')
        actor=rt.snapshot('worker')
        self.assertEqual(len(actor['projects']),1)
        self.assertEqual(actor['projects'][0]['means'],['EAT'])
        self.assertEqual(beat('project')['status'],'PERFORMED')
        self.assertEqual(beat('project')['status'],'BLOCKED')
        prior=deepcopy(rt.snapshot('worker')['projects'][0])
        for _ in range(12):beat('wait')
        # Restore actual bodily capacity rather than edit the actor.
        rt.step('worker',requested_action='REST')
        n.contribute('renewed-offer','OFFER_FEED',target_actor_ref='worker')
        seen=[]
        self.assertEqual(beat('renew',reorganize=reorganize,seen=seen)['status'],'PERFORMED')
        self.assertEqual(len(seen),1)
        actor=rt.snapshot('worker')
        project=actor['projects'][0]
        self.assertEqual(project['id'],prior['id'])
        self.assertEqual(project['origin'],prior['origin'])
        self.assertEqual(project['operational_history'],prior['operational_history'])
        self.assertEqual(project['means'],['EAT','SIGNAL'] if reorganize else ['EAT'])
        self.assertEqual(actor['joint_practices'],practice)
        self.assertEqual(rt.ledger.world(name)[1]['holdings']['visitor']['food'],2)
        self.assertTrue(rt.verify()['valid'])
        return rt,n,db,project

    def test_human_history_reorganizes_same_project_and_cold_fresh_cooperation(self):
        for reorganize in (True,False):
            with self.subTest(reorganize=reorganize):
                name='arm'+str(reorganize)
                rt,n,db,project=self.history(name,reorganize)
                rt.close()
                seen=[]
                cold=ConstitutiveRuntime(db,world_id=name,semantic=policy('invite',seen=seen))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                invitation=nn.independent_actor_beat('worker')
                self.assertEqual(invitation['attempt'],'SIGNAL' if reorganize else 'WAIT')
                self.assertEqual(len(seen),int(reorganize))
                if reorganize:
                    self.assertEqual(invitation['status'],'PARTIAL')
                    self.assertEqual(seen[0]['project_id'],project['id'])
                    self.assertEqual(seen[0]['counterpart_participation_kind'],'HUMAN_AUTHORED_NEIGHBOR')
                self.assertEqual(len(cold.ledger.world(name)[1]['material_feeding_events']),2)
                offer=nn.contribute('new-offer','OFFER_FEED',target_actor_ref='worker')
                cold.semantic=policy('accept')
                accepted=nn.independent_actor_beat('worker')
                self.assertEqual(accepted['attempt'],'SIGNAL' if reorganize else 'WAIT')
                world=cold.ledger.world(name)[1]
                self.assertEqual(len(world['material_feeding_events']),2+int(reorganize))
                self.assertEqual(world['holdings']['visitor']['food'],2-int(reorganize))
                if reorganize:
                    self.assertEqual(world['material_feeding_events'][-1]['human_authored_offer_ref'],offer['event_ref'])
                    self.assertEqual(cold.snapshot('worker')['projects'][0]['operational_history'][-1]['operation'],'SIGNAL')
                nn.contribute('departure','LEAVE')
                cold.semantic=policy('invite')
                self.assertEqual(nn.independent_actor_beat('worker')['attempt'],'WAIT')
                self.assertEqual(cold.snapshot('worker')['projects'][0]['means'],project['means'])
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertTrue(cold.verify()['valid'])

    def test_current_offer_does_not_convert_project_invitation_into_acceptance(self):
        rt,n,_,project=self.history('generic',True)
        n.contribute('fresh','OFFER_FEED',target_actor_ref='worker')
        rt.semantic=policy('invite')
        self.assertEqual(n.independent_actor_beat('worker')['status'],'PARTIAL')
        self.assertEqual(rt.ledger.world('generic')[1]['holdings']['visitor']['food'],2)
        self.assertEqual(len(rt.ledger.world('generic')[1]['material_feeding_events']),2)
        rt.semantic=policy('accept')
        self.assertEqual(n.independent_actor_beat('worker')['attempt'],'WAIT')
        self.assertEqual(rt.snapshot('worker')['projects'][0]['id'],project['id'])
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
