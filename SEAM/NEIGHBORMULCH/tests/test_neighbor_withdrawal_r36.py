"""R36: prospective withdrawal, separate correspondence, actual continuing care."""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as support
import test_neighbor_structural_absence_r25 as care
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from neighbor_runtime import NeighborEncounter,EncounterRefusal
import mii

class WithdrawalR36(unittest.TestCase):
    def test_withdrawal_and_separate_delivery_opening_and_independent_eating(self):
        for mode in ('none','revoked','unopened','opened'):
            with self.subTest(mode=mode):
                rt,n,db=support.MaterialSupportR17.build(self,'withdraw'+mode)
                name=rt.world_id
                due=rt.ledger.world(name)[1]['clock']+9
                p=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
                ident=p['human_offer_commitment_ref']
                n.configure_sourcefree_correspondence('mail','worker','workshop')
                n.contribute('leave','LEAVE')
                before=deepcopy(rt.ledger.actors())
                w=n.contribute('withdraw','WITHDRAW_PLEDGE',target_commitment_ref=ident)
                self.assertEqual(w['status'],'PERFORMED')
                self.assertEqual(w['potential_actor_evidence'],[])
                self.assertEqual(rt.ledger.actors(),before)
                row=n.own_food_commitments()[0]
                self.assertEqual(row['status'],'WITHDRAWN_BY_AUTHORED_ACT')
                self.assertEqual(row['withdrawal_user_event_ref'],w['event_ref'])
                self.assertFalse(rt.ledger.world(name)[1]['neighbor_users']['visitor']['present'])
                self.assertEqual(rt.ledger.world(name)[1]['holdings']['visitor']['food'],2)
                count=len(rt.ledger.events())
                self.assertTrue(n.contribute('withdraw','WITHDRAW_PLEDGE',
                    target_commitment_ref=ident)['idempotent_replay'])
                self.assertEqual(len(rt.ledger.events()),count)
                with self.assertRaisesRegex(EncounterRefusal,'REQUEST_REPLAY_CHANGED_PAYLOAD'):
                    n.contribute('withdraw','WITHDRAW_PLEDGE',target_commitment_ref='other')
                with self.assertRaisesRegex(EncounterRefusal,'HUMAN_WITHDRAWAL_WINDOW_NOT_PENDING'):
                    n.contribute('again','WITHDRAW_PLEDGE',target_commitment_ref=ident)
                other=NeighborEncounter(rt,'other',mii_module=mii)
                with self.assertRaisesRegex(EncounterRefusal,'HUMAN_WITHDRAWAL_NO_OWN_COMMITMENT'):
                    other.contribute('foreign','WITHDRAW_PLEDGE',target_commitment_ref=ident)
                self.assertEqual(len(rt.ledger.events()),count)
                words='I withdraw my earlier promise to offer food.'
                msg=None
                if mode!='none':
                    msg=n.send_correspondence('notice','mail',words)['message_ref']
                    if mode=='revoked':n.revoke_sourcefree_correspondence('mail')
                phase='before';received=[]
                def cb(task,p):
                    if task=='actor_attempt':
                        self.assertNotIn(words,str(p))
                        if phase=='open':
                            opts=p.get('correspondence_attention_options',[])
                            self.assertEqual(len(opts),int(mode in ('opened','unopened')))
                            if opts and mode=='opened':
                                return {'task':task,'action':'ORIENT','correspondence_attention_id':opts[0]['attention_id']}
                        if phase=='eat' and received:
                            opts=[x for x in p['practical_options'] if x.get('project_id')=='own-meal' and x['operation']=='EAT']
                            self.assertEqual(len(opts),1)
                            return {'task':task,'action':'EAT','practical_option_id':opts[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        rec=p.get('actual_correspondence_attention_analyst_only')
                        if rec:
                            self.assertIn(words,str(p['experience']))
                            received.append(deepcopy(rec))
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'correspondence_attention_ref':rec['attention_id'],
                                'content':'The visitor wrote that the offer is withdrawn.',
                                'cue_terms':['correspondence']}]}
                        return {'task':task,'candidates':[]}
                    if task=='expression':
                        self.assertNotIn(words,str(p))
                        return {'task':task,'surface':'Ordinary activity.'}
                    raise AssertionError(task)
                svc=ValidatingSemanticService(CallbackLLMProvider(cb));rt.semantic=svc
                n.independent_actor_beat('worker')
                if msg:
                    self.assertEqual(n.settle_sourcefree_correspondence_delivery(msg),
                        'TRANSPORT_ROUTE_REVOKED' if mode=='revoked' else 'DELIVERED')
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=svc);self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                phase='open';nn.independent_actor_beat('worker')
                self.assertEqual(len(cold.ledger.actor('worker')[1]['memories']),int(mode=='opened'))
                phase='eat'
                # Later selection uses actor-owned historical memory via controlled policy;
                # not a direct objective withdrawal -> automatic knowledge edge.
                def later(task,p):
                    if task=='actor_attempt':
                        if any('The visitor wrote that the offer is withdrawn.' in str(x)
                               for x in p.get('private_rehearsal_options',[])):
                            opts=[x for x in p['practical_options'] if x.get('project_id')=='own-meal' and x['operation']=='EAT']
                            return {'task':task,'action':'EAT','practical_option_id':opts[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    return cb(task,p)
                cold.semantic=ValidatingSemanticService(CallbackLLMProvider(later))
                self.assertEqual(nn.independent_actor_beat('worker')['attempt'],'EAT' if mode=='opened' else 'WAIT')
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['worker']['food'],0 if mode=='opened' else 1)
                self.assertEqual(nn.own_food_commitments()[0],row)
                self.assertTrue(cold.verify()['valid'])

    def test_withdrawal_cannot_erase_cost_or_fulfill_old_promise(self):
        rt,n,db,rows,dep,ident=care.StructuralAbsenceR25.build(self,'actualcare',False)
        # Already clock 4, due 6. Explicit withdrawal at 5, independent care
        # still advances through the due boundary without fabricated visitor offer.
        w=n.contribute('withdraw','WITHDRAW_PLEDGE',target_commitment_ref=ident)
        self.assertEqual(w['status'],'PERFORMED')
        self.assertEqual(n.own_food_commitments()[0]['settled_at_clock'],5)
        # Original departure still qualifies absence; withdrawal is not reentry.
        rt.background(2,processes=rows)
        self.assertEqual(n.own_food_commitments()[0]['status'],'WITHDRAWN_BY_AUTHORED_ACT')
        child=rt.snapshot('nadia')
        self.assertTrue(child['undergone_care_periods'])
        self.assertEqual(child['memories'],[])
        old=deepcopy(rt.ledger.world('actualcare')[1]['historical_periods'])
        n.contribute('return','MOVE',destination='home')
        new=n.contribute('new','PLEDGE_OFFER',target_actor_ref='mother',
            due_clock=rt.ledger.world('actualcare')[1]['clock']+5)
        self.assertNotEqual(new['human_offer_commitment_ref'],ident)
        self.assertEqual(rt.ledger.world('actualcare')[1]['historical_periods'],old)
        self.assertEqual(n.own_food_commitments()[0]['status'],'WITHDRAWN_BY_AUTHORED_ACT')
        self.assertTrue(rt.verify()['valid'])

    def test_exclusive_deadline_and_fulfillment_irreversible(self):
        for fulfilled in (False,True):
            rt,n,_=support.MaterialSupportR17.build(self,'boundary'+str(fulfilled))
            due=rt.ledger.world(rt.world_id)[1]['clock']+3
            p=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
            n.contribute('offer' if fulfilled else 'wait','OFFER_FEED' if fulfilled else 'WAIT',
                         **({'target_actor_ref':'worker'} if fulfilled else {}))
            before=deepcopy(rt.ledger.world(rt.world_id))
            count=len(rt.ledger.events())
            with self.assertRaisesRegex(EncounterRefusal,'HUMAN_WITHDRAWAL_WINDOW_NOT_PENDING'):
                n.contribute('withdraw','WITHDRAW_PLEDGE',target_commitment_ref=p['human_offer_commitment_ref'])
            self.assertEqual(rt.ledger.world(rt.world_id),before)
            self.assertEqual(len(rt.ledger.events()),count)
            n.contribute('next','WAIT')
            self.assertEqual(n.own_food_commitments()[0]['status'],
                'OFFER_AUTHORED_IN_WINDOW' if fulfilled else 'WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER')
            self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
