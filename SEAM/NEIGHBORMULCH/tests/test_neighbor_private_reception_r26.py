"""R26: actual human contribution is not identical to an Other's experience.
Reuse R24's performed undertaking, R45's focal and private formation, and
the existing independent life scheduler, cold ledger and finite MII reader.
"""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from neighbor_runtime import NeighborEncounter
import mii

class PrivateReceptionR26(unittest.TestCase):
    def test_identical_human_undertaking_differential_private_afterlife(self):
        outcomes={}
        for attend in (True,False):
            with self.subTest(attend=attend):
                name='private'+str(attend)
                rt,n,db=inherited.MaterialSupportR17.build(self,name)
                stage='attend'
                receipts=[]; rehearsals=[]
                def policy(task,packet):
                    if task=='expression':
                        self.assertNotIn('undertaking_attention_receipt',packet['actor_accessible'])
                        return {'task':task,'surface':'An ordinary interval.'}
                    if task=='actor_attempt':
                        if stage=='attend':
                            rows=packet['undertaking_attention_options']
                            self.assertEqual(len(rows),1)
                            self.assertEqual(rows[0]['source_kind'],'HUMAN_AUTHORED_NEIGHBOR')
                            self.assertEqual(rows[0]['counterpart_ref'],'visitor')
                            self.assertNotIn('status',rows[0])
                            if attend:
                                return {'task':task,'action':'ORIENT',
                                    'undertaking_attention_id':rows[0]['attention_id']}
                            return {'task':task,'action':'ORIENT'}
                        if stage=='rehearse':
                            rows=[x for x in packet['private_rehearsal_options']
                                  if x.get('undertaking_attention')]
                            self.assertEqual(len(rows),int(attend))
                            if rows:return {'task':task,'action':'WAIT',
                                'private_rehearsal_id':rows[0]['rehearsal_id'],
                                'private_rehearsal_content':'Perhaps I can rest without waiting.'}
                        if stage=='trial':
                            rows=[x for x in packet['possible_end_trials']
                                  if x.get('private_rehearsal_ref')]
                            if rows:return {'task':task,'possible_end_trial_id':rows[0]['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        rec=packet.get('actual_undertaking_attention_analyst_only')
                        if rec:
                            receipts.append(deepcopy(rec))
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'undertaking_attention_ref':rec['attention_id'],
                                'cue_terms':['visitor_offer_undertaking'],
                                'content':'The visitor undertook to offer food later.'}]}
                        rec=packet.get('actual_private_rehearsal_analyst_only')
                        if rec:
                            rehearsals.append(deepcopy(rec))
                            return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                                'rehearsal_ref':rec['id'],'possible_object':'rest without awaiting an offer',
                                'possible_means':['REST']}]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                service=ValidatingSemanticService(CallbackLLMProvider(policy))
                rt.semantic=service
                due=rt.ledger.world(name)[1]['clock']+6
                initial=deepcopy(rt.ledger.actor('worker')[1])
                promise=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
                self.assertEqual(promise['status'],'PERFORMED')
                self.assertEqual(rt.ledger.actor('worker')[1],initial)
                beat=n.continue_independent_life_during_visit(profile=n.new_private_profile())
                self.assertEqual(beat['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
                actor=rt.ledger.actor('worker')[1]
                self.assertEqual(len(receipts),int(attend))
                self.assertEqual(len(actor['memories']),int(attend))
                if attend:
                    rec=receipts[0]
                    self.assertEqual(rec['source_event_ref'],promise['event_ref'])
                    self.assertEqual(rec['commitment_ref'],promise['human_offer_commitment_ref'])
                    self.assertEqual(actor['memories'][0]['undertaking_attention'],rec)
                self.assertNotIn('undertaking_attention',str(beat['visitor_surface']))
                self.assertNotIn('The visitor undertook',str(beat['visitor_surface']))
                self.assertEqual(n.own_food_commitments()[0]['status'],'PENDING')
                dep=n.contribute('departure','LEAVE')
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=service)
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                nn.continue_absent_life_until(dep['event_ref'],due,max_segments=12)
                self.assertEqual(nn.own_food_commitments()[0]['status'],'WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER')
                self.assertEqual(cold.ledger.actor('worker')[1]['memories'],actor['memories'])
                stage='rehearse'
                nn.independent_actor_beat('worker')
                self.assertEqual(len(rehearsals),int(attend))
                own=cold.ledger.actor('worker')[1]
                self.assertEqual(len(own['possible_ends']),int(attend))
                if attend:
                    self.assertEqual(own['possible_ends'][0]['private_undertaking_attention'],receipts[0])
                stage='trial'
                outcomes[attend]=nn.independent_actor_beat('worker')['attempt']
                world=cold.ledger.world(name)[1]
                self.assertEqual(world['neighbor_user_events'][-1]['event_ref'],dep['event_ref'])
                self.assertEqual(world['holdings']['visitor']['food'],2)
                self.assertEqual(world['material_feeding_events'],[])
                nn.contribute('return','MOVE',destination='workshop')
                surface=nn.private_surface(nn.new_private_profile())
                self.assertNotIn('private_rehearsal',str(surface))
                self.assertNotIn('rest without awaiting',str(surface))
                self.assertTrue(cold.verify()['valid'])
        self.assertEqual(outcomes,{True:'REST',False:'WAIT'})

if __name__=='__main__':unittest.main()
