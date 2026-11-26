"""A surrendered entry right is not a deleted history, nor a restored right
when another person later privately values the same relationship."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as support
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

class RuptureR30(unittest.TestCase):
    def build(self,name):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name,semantic=support.policy('explore'))
        self.addCleanup(rt.close)
        w=blank_world(name)
        w['sites']['workshop'].update(access='controlled',admitted=['visitor','worker','other'])
        w['holdings']={'visitor':{'food':2},'worker':{'food':1}}
        w['sites']['workshop']['food']=0
        a=adult('worker','Mara','workshop');a['body']['nutrition']=.30
        a['projects']=[{'id':'own-meal','object':'obtain nourishment',
                        'means':['EAT'],'priority':.4,'status':'active'}]
        rt.ledger.initialize(w,[a])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit','sightline':'unobstructed',
                'hearing':True,'sound_path':'audible','legibility':'readable'}
                for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,'sound_path':'audible'}}},
            request_id='geometry')
        self.assertEqual(n.contribute('arrive','MOVE',destination='workshop')['status'],'PERFORMED')
        return rt,n,db

    def test_rupture_keeps_acquired_practice_and_can_form_new_private_end(self):
        for reflect in (True,False):
            with self.subTest(reflect=reflect):
                name='rupture'+str(reflect)
                rt,n,db=self.build(name)
                self.assertEqual(n.independent_actor_beat('worker')['status'],'PARTIAL')
                offer=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                rt.semantic=support.policy('explore',True)
                self.assertEqual(n.independent_actor_beat('worker')['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
                prior=deepcopy(rt.ledger.actor('worker')[1]['joint_practices'])
                self.assertEqual(len(prior),1)
                with self.assertRaisesRegex(EncounterRefusal,'DEPART_BEFORE_SURRENDER'):
                    n.surrender_entry_permission('too-soon','workshop')
                n.configure_sourcefree_correspondence('mail','worker','workshop')
                n.contribute('departure','LEAVE')
                before=deepcopy(rt.ledger.actors())
                closure=n.surrender_entry_permission('return','workshop')
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(n.surrender_entry_permission('return','workshop')['surrender_ref'],closure['surrender_ref'])
                self.assertEqual(n.contribute('blocked','MOVE',destination='workshop')['status'],'BLOCKED')
                self.assertEqual(rt.ledger.world(name)[1]['sites']['workshop']['admitted'],['worker','other'])
                # The separate contact path survives. Its actual authored
                # words are not proof of apology, healing, or comprehension.
                msg=n.send_correspondence('farewell','mail','I will not come back to the workshop.')['message_ref']
                stage='before';rehearsals=[]
                def policy(task,p):
                    if task=='actor_attempt':
                        if stage=='open':
                            rows=p['correspondence_attention_options']
                            return {'task':task,'action':'ORIENT','correspondence_attention_id':rows[0]['attention_id']}
                        if stage=='reflect':
                            rows=[x for x in p['private_rehearsal_options'] if x.get('correspondence_attention')]
                            self.assertEqual(len(rows),1)
                            if reflect:
                                return {'task':task,'action':'WAIT','private_rehearsal_id':rows[0]['rehearsal_id'],
                                    'private_rehearsal_content':'The help mattered; perhaps I can rest without waiting for another visit.'}
                        if stage=='trial':
                            rows=[x for x in p['possible_end_trials'] if x.get('private_rehearsal_ref')]
                            self.assertEqual(len(rows),int(reflect))
                            if rows:return {'task':task,'possible_end_trial_id':rows[0]['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        rec=p.get('actual_correspondence_attention_analyst_only')
                        if rec:return {'task':task,'candidates':[{'kind':'MEMORY',
                            'correspondence_attention_ref':rec['attention_id'],
                            'content':'The visitor says the visits will end.','cue_terms':['correspondence']}]}
                        rec=p.get('actual_private_rehearsal_analyst_only')
                        if rec:
                            rehearsals.append(deepcopy(rec))
                            return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                                'rehearsal_ref':rec['id'],'possible_object':'rest without awaiting a visit',
                                'possible_means':['REST']}]}
                        return {'task':task,'candidates':[]}
                    if task=='expression':return {'task':task,'surface':'An ordinary interval.'}
                    raise AssertionError(task)
                svc=ValidatingSemanticService(CallbackLLMProvider(policy));rt.semantic=svc
                n.independent_actor_beat('worker')
                self.assertEqual(n.settle_sourcefree_correspondence_delivery(msg),'DELIVERED')
                stage='open';n.independent_actor_beat('worker')
                mem=deepcopy(rt.ledger.actor('worker')[1]['memories'][0])
                self.assertEqual(mem['correspondence_attention']['message_ref'],msg)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=svc);self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                stage='reflect';nn.independent_actor_beat('worker')
                self.assertEqual(len(rehearsals),int(reflect))
                actor=cold.ledger.actor('worker')[1]
                self.assertEqual(actor['joint_practices'],prior)
                self.assertEqual(len(actor['possible_ends']),int(reflect))
                if reflect:
                    self.assertEqual(actor['possible_ends'][0]['private_correspondence_attention'],mem['correspondence_attention'])
                stage='trial';self.assertEqual(nn.independent_actor_beat('worker')['attempt'],'REST' if reflect else 'WAIT')
                self.assertEqual(nn.contribute('blocked-again','MOVE',destination='workshop')['status'],'BLOCKED')
                world=cold.ledger.world(name)[1]
                self.assertEqual(world['sites']['workshop']['admitted'],['worker','other'])
                self.assertTrue(world['neighbor_correspondence_routes']['mail']['active'])
                self.assertEqual(len(world['material_feeding_events']),1)
                self.assertEqual(world['material_feeding_events'][0]['human_authored_offer_ref'],offer['event_ref'])
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertTrue(cold.verify()['valid'])

    def test_public_and_foreign_access_not_surrenderable(self):
        rt,n,_=self.build('guard')
        n.contribute('leave','LEAVE')
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'NO_CONTROLLED_ENTRY_PERMISSION'):
            n.surrender_entry_permission('public','home')
        with self.assertRaisesRegex(EncounterRefusal,'NO_OWN_ENTRY_PERMISSION'):
            n.surrender_entry_permission('foreign','hall')
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
