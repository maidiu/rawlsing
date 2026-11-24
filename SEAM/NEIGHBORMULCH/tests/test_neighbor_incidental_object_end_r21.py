"""A performed operation's previously unselected good can become a new
object-specific activity, without rewriting the earlier project.
"""
from copy import deepcopy
import unittest
import test_neighbor_material_participation_r13 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider,ValidatingSemanticService,HeuristicSemanticProvider)
from um_sorok_organism.unintended_goods import one_sourcefree_provisional_end
from neighbor_runtime import NeighborEncounter
import mii

def initial_actor(actor):
    actor['projects']=[{
        'id':'production-duty','object':'meet an existing production obligation',
        'motive':'existing livelihood obligation','means':['MAKE_OBJECT'],
        'priority':.4,'status':'active',
        'expected_difference':{'feature':'discharge production obligation',
                               'direction':'CHANGE','sign_tags':['quota_completed']}}]

def policy(stage,*,nominate=True,seen=None,forge=False):
    fallback=HeuristicSemanticProvider()
    def callback(task,packet):
        if task=='actor_attempt':
            options=packet['practical_options']
            if stage=='make':
                choices=[a for a in options if a['operation']=='MAKE_OBJECT'
                         and a['project_id']=='production-duty']
            elif stage=='trial':
                choices=[t for t in packet['possible_end_trials']
                         if t['operation']=='INSPECT' and t.get('source_material_object_ref')]
                if len(choices)==1:
                    return {'task':task,'possible_end_trial_id':choices[0]['trial_id']}
                raise AssertionError('one actual object-bound trial required')
            elif stage=='inspect':
                choices=[a for a in options if a['operation']=='INSPECT'
                         and a.get('grounds_status')=='PRESENT_MATERIAL_OBJECT_NOT_ASSUMED_MOTIVE']
            elif stage=='recruit':
                choices=[a for a in options if a['operation']=='REPAIR'
                         and a.get('project_id') and a['project_id']!='production-duty']
                if seen is not None:seen.extend(deepcopy(choices))
            else:choices=[]
            if len(choices)==1:return {'task':task,'practical_option_id':choices[0]['option_id']}
            return {'task':task,'action':'WAIT'}
        if task=='development':
            if stage=='make':
                qualified=[q for q in packet['historically_possible_incidental_goods']
                           if q.get('incidental_object_end_basis')]
                if len(qualified)!=1:raise AssertionError('one actual qualified incidental good required')
                return {'task':task,'candidates':one_sourcefree_provisional_end(
                    qualified,{'possible_ends':packet['actor_possible_ends']})}
            if stage=='inspect':
                candidates=packet['historically_possible_incidental_takeup']
                if seen is not None:seen.extend(deepcopy(candidates))
                if nominate and len(candidates)==1:
                    q=deepcopy(candidates[0])
                    if forge:q['source_trial_ref']='forged-trial'
                    return {'task':task,'candidates':[{
                        'kind':'TAKE_UP_POSSIBLE_END','possible_end_ref':q['possible_end_ref'],
                        'later_perceived_cue_ref':q['later_perceived_cue_ref'],
                        'incidental_takeup_basis':q,'means':['REPAIR'],'priority':.6}]}
            return {'task':task,'candidates':[]}
        return fallback.propose(task,packet)
    return ValidatingSemanticService(CallbackLLMProvider(callback))

class IncidentalObjectEndR21(unittest.TestCase):
    def build(self,name):
        rt,n,db,ref=inherited.MaterialParticipationR13.build(
            self,name,True,actor_setup=initial_actor,initial_semantic=policy('make'))
        actor=rt.snapshot('worker')
        self.assertEqual(len(actor['possible_ends']),1)
        end=actor['possible_ends'][0]
        self.assertEqual(end['incidental_object_end_basis']['original_project_ref'],'production-duty')
        self.assertEqual(end['origin_material_object_ref'],ref)
        self.assertEqual(len(actor['projects']),1)
        self.assertEqual(actor['projects'][0]['operational_history'][0]['operation'],'MAKE_OBJECT')
        self.assertEqual(actor['projects'][0]['operational_history'][0]['project'],'production-duty')
        self.assertEqual(n.contribute('human-repair','REPAIR',target_object_ref=ref)['status'],'PERFORMED')
        return rt,n,db,ref,end,deepcopy(actor['projects'][0]['operational_history'][0])

    def test_distinct_trial_and_takeup_change_actual_cold_object_activity(self):
        for trial,nominate in ((True,True),(True,False),(False,True)):
            with self.subTest(trial=trial,nominate=nominate):
                name='arm'+str(trial)+str(nominate)
                rt,n,db,ref,end,original=self.build(name)
                rt.semantic=policy('trial' if trial else 'inspect',nominate=False)
                self.assertEqual(n.independent_actor_beat('worker')['attempt'],'INSPECT')
                a=rt.snapshot('worker')
                self.assertEqual(len(a['possible_ends'][0].get('trial_history',[])),int(trial))
                self.assertEqual(len(a['projects']),1)
                if trial:self.assertEqual(a['possible_ends'][0]['trial_history'][0]['source_material_object_ref'],ref)
                seen=[]
                rt.semantic=policy('inspect',nominate=nominate,seen=seen)
                self.assertEqual(n.independent_actor_beat('worker')['attempt'],'INSPECT')
                a=rt.snapshot('worker')
                self.assertEqual(len(seen),int(trial))
                acquired=trial and nominate
                self.assertEqual(len(a['projects']),1+int(acquired))
                self.assertEqual(a['projects'][0]['operational_history'][0],original)
                if acquired:
                    p=a['projects'][1]
                    self.assertEqual(p['material_object_ref'],ref)
                    self.assertEqual(p['possible_end_ref'],end['id'])
                    self.assertEqual(p['incidental_takeup_basis']['origin_incidental_good_ref'],
                                     end['incidental_object_end_basis']['id'])
                    self.assertEqual(p['origin'][0],end['origin_event'])
                rt.close()
                choices=[]
                cold=ConstitutiveRuntime(db,world_id=name,semantic=policy('recruit',seen=choices))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                actual=nn.independent_actor_beat('worker')
                self.assertEqual(actual['attempt'],'REPAIR' if acquired else 'WAIT')
                self.assertEqual(len(choices),int(acquired))
                self.assertEqual(cold.ledger.world(name)[1]['material_objects'][ref]['condition'],1.0 if acquired else .8)
                if acquired:
                    self.assertEqual(choices[0]['world_request']['material_object_ref'],ref)
                    self.assertEqual(cold.snapshot('worker')['projects'][1]['operational_history'][-1]['operation'],'REPAIR')
                self.assertEqual(cold.snapshot('worker')['projects'][0]['operational_history'][0],original)
                self.assertTrue(cold.verify()['valid'])

    def test_forged_later_trial_basis_cannot_commit(self):
        rt,n,_,ref,end,original=self.build('forgery')
        rt.semantic=policy('trial')
        n.independent_actor_beat('worker')
        before=deepcopy(rt.ledger.world('forgery'))
        actors=deepcopy(rt.ledger.actors())
        count=len(rt.ledger.events())
        rt.semantic=policy('inspect',forge=True)
        with self.assertRaisesRegex(ValueError,'INCIDENTAL_END_NEEDS_DISTINCT_LIVED_TRIAL_AND_REENCOUNTER'):
            n.independent_actor_beat('worker')
        self.assertEqual(rt.ledger.world('forgery'),before)
        self.assertEqual(rt.ledger.actors(),actors)
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
