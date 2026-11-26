"""R29 sourcefree local correspondence, no out-of-game messaging."""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

class CorrespondenceR29(unittest.TestCase):
    def test_delivery_opening_and_optional_private_afterlife(self):
        for choose in (True,False):
            with self.subTest(choose=choose):
                name='mail'+str(choose)
                rt,n,db=inherited.MaterialSupportR17.build(self,name)
                n.contribute('leave','LEAVE')
                stage='before'; calls=[]; received=[]
                words='A blue bowl is under the stairs.'
                def policy(task,p):
                    calls.append(task)
                    if task=='actor_attempt':
                        self.assertNotIn(words,str(p))
                        rows=p.get('correspondence_attention_options',[])
                        self.assertEqual(len(rows),int(stage=='open'))
                        if stage=='open' and choose:
                            return {'task':task,'action':'ORIENT',
                                'correspondence_attention_id':rows[0]['attention_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        rec=p.get('actual_correspondence_attention_analyst_only')
                        if rec:
                            received.append(deepcopy(rec))
                            self.assertIn(words,str(p['experience']))
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'correspondence_attention_ref':rec['attention_id'],
                                'content':'They wrote about a bowl.','cue_terms':['correspondence']}]}
                        self.assertNotIn(words,str(p))
                        return {'task':task,'candidates':[]}
                    if task=='expression':
                        self.assertNotIn(words,str(p))
                        return {'task':task,'surface':'An ordinary moment.'}
                    raise AssertionError(task)
                svc=ValidatingSemanticService(CallbackLLMProvider(policy));rt.semantic=svc
                initial=deepcopy(rt.ledger.actors())
                n.configure_sourcefree_correspondence('mail','worker','workshop',delay_ticks=1)
                sent=n.send_correspondence('one','mail',words);ref=sent['message_ref']
                self.assertEqual(n.settle_sourcefree_correspondence_delivery(ref),'TRANSPORT_NOT_DUE')
                self.assertEqual(rt.ledger.actors(),initial)
                self.assertEqual(calls,[])
                n.independent_actor_beat('worker')
                count=len(calls);before=deepcopy(rt.ledger.actors())
                self.assertEqual(n.settle_sourcefree_correspondence_delivery(ref),'DELIVERED')
                self.assertEqual(rt.ledger.actors(),before);self.assertEqual(len(calls),count)
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=svc);self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                self.assertEqual(nn.send_correspondence('one','mail',words)['message_ref'],ref)
                stage='open'
                res=nn.independent_actor_beat('worker')
                self.assertEqual(res['attempt'],'ORIENT' if choose else 'WAIT')
                row=cold.ledger.world(name)[1]['neighbor_correspondence'][ref]
                self.assertEqual(row['opened_clock'] is not None,choose)
                self.assertEqual(len(received),int(choose))
                actor=cold.ledger.actor('worker')[1]
                self.assertEqual(len(actor['memories']),int(choose))
                if choose:
                    self.assertEqual(actor['memories'][0]['correspondence_attention'],received[0])
                    self.assertEqual(received[0]['message_ref'],ref)
                self.assertNotIn('visitor',cold.ledger.actors())
                self.assertNotIn(words,str(res))
                self.assertTrue(cold.verify()['valid'])

    def test_revocation_and_no_unissued_open(self):
        rt,n,_=inherited.MaterialSupportR17.build(self,'revoked')
        n.contribute('leave','LEAVE')
        n.configure_sourcefree_correspondence('mail','worker','workshop')
        ref=n.send_correspondence('one','mail','A message.')['message_ref']
        n.revoke_sourcefree_correspondence('mail')
        before=deepcopy(rt.ledger.actors())
        self.assertEqual(n.settle_sourcefree_correspondence_delivery(ref),'TRANSPORT_ROUTE_REVOKED')
        with self.assertRaisesRegex(EncounterRefusal,'CHANNEL_SEND_NOT_AUTHORIZED'):
            n.send_correspondence('two','mail','Another.')
        self.assertEqual(n.send_correspondence('one','mail','A message.')['message_ref'],ref)
        with self.assertRaisesRegex(EncounterRefusal,'MESSAGE_REPLAY_CHANGED_PAYLOAD'):
            n.send_correspondence('one','mail','Changed.')
        self.assertEqual(rt.ledger.actors(),before)
        def forged(task,p):
            if task=='actor_attempt':
                return {'task':task,'action':'ORIENT','correspondence_attention_id':'forged'}
            raise AssertionError(task)
        rt.semantic=ValidatingSemanticService(CallbackLLMProvider(forged))
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(ValueError,'CORRESPONDENCE_UNISSUED'):
            n.independent_actor_beat('worker')
        self.assertEqual(len(rt.ledger.events()),count)
        self.assertEqual(rt.ledger.actors(),before)
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
