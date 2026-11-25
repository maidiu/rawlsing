"""Explicit human undertaking and actual world-time boundary; not a
fictional calendar event, recipient assent, or account-retention device."""
from copy import deepcopy
import unittest
import test_neighbor_material_support_r17 as inherited
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.continuity_clock import next_discontinuity
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii

class CommitmentTimeR24(unittest.TestCase):
    def build(self,name,**kw):
        return inherited.MaterialSupportR17.build(self,name,**kw)

    def test_actual_deadline_absence_and_late_offer_do_not_rewrite_history(self):
        for pledged in (True,False):
            with self.subTest(pledged=pledged):
                name='window'+str(pledged)
                rt,n,db=self.build(name)
                clock=rt.ledger.world(name)[1]['clock']
                due=clock+6
                before=deepcopy(rt.ledger.actors())
                if pledged:
                    pledge=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
                    self.assertEqual(pledge['status'],'PERFORMED')
                    self.assertEqual(len(pledge['potential_actor_evidence']),1)
                    self.assertEqual(n.own_food_commitments()[0]['status'],'PENDING')
                    count=len(rt.ledger.events())
                    self.assertEqual(n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)['human_offer_commitment_ref'],pledge['human_offer_commitment_ref'])
                    self.assertEqual(len(rt.ledger.events()),count)
                    with self.assertRaises(EncounterRefusal):
                        n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due+1)
                else:
                    n.contribute('not-a-promise','WAIT')
                    self.assertEqual(n.own_food_commitments(),[])
                self.assertEqual(rt.ledger.actors(),before)
                dep=n.contribute('departure','LEAVE')
                # A source-qualified deadline changes actual compression
                # cut; a mundane departure does not create an obligation.
                rt.close()
                cold=ConstitutiveRuntime(db,world_id=name,semantic=inherited.policy('explore'))
                self.addCleanup(cold.close)
                nn=NeighborEncounter(cold,'visitor',mii_module=mii)
                # Earlier ephemeral sensory signs may expire first; no
                # actor/visitor response is invented by the scheduler.
                cuts=[]
                for _ in range(12):
                    w=cold.ledger.world(name)[1]
                    if w['clock']>=due:break
                    t=cold.advance_to_discontinuity(horizon=due-w['clock'])
                    if t['historical_discontinuity']:cuts.append(t['historical_discontinuity']['kind'])
                self.assertEqual(cold.ledger.world(name)[1]['clock'],due)
                self.assertEqual('HUMAN_OFFER_WINDOW_ELAPSES' in cuts,pledged)
                records=nn.own_food_commitments()
                self.assertEqual(len(records),int(pledged))
                if pledged:
                    self.assertEqual(records[0]['status'],'WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER')
                    self.assertEqual(records[0]['settled_at_clock'],due)
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['visitor']['food'],2)
                self.assertFalse(cold.ledger.world(name)[1]['material_feeding_events'])
                # No human act synthesized in absent world time.
                self.assertEqual(cold.ledger.world(name)[1]['neighbor_user_events'][-1]['event_ref'],dep['event_ref'])
                nn.contribute('return','MOVE',destination='workshop')
                offer=nn.contribute('late','OFFER_FEED',target_actor_ref='worker')
                self.assertNotIn('human_offer_commitment_ref',offer)
                self.assertEqual(nn.independent_actor_beat('worker')['status'],'PERFORMED')
                self.assertEqual(cold.ledger.world(name)[1]['holdings']['visitor']['food'],1)
                self.assertEqual(nn.own_food_commitments(),records)
                self.assertTrue(cold.verify()['valid'])

    def test_offer_fulfills_undertaking_not_acceptance_or_body_effect(self):
        for accept in (True,False):
            with self.subTest(accept=accept):
                name='fulfill'+str(accept)
                rt,n,_=self.build(name)
                due=rt.ledger.world(name)[1]['clock']+5
                p=n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
                # Distinct actual recipient opportunity to receive the sign.
                self.assertTrue(any(c['kind']=='visitor_offer_undertaking' for c in rt.see('worker')['cues']))
                self.assertEqual(n.own_food_commitments()[0]['status'],'PENDING')
                before=deepcopy(rt.ledger.actors())
                offer=n.contribute('offer','OFFER_FEED',target_actor_ref='worker')
                self.assertEqual(offer['human_offer_commitment_ref'],p['human_offer_commitment_ref'])
                record=n.own_food_commitments()[0]
                self.assertEqual(record['status'],'OFFER_AUTHORED_IN_WINDOW')
                self.assertEqual(record['fulfillment_user_event_ref'],offer['event_ref'])
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(rt.ledger.world(name)[1]['holdings']['visitor']['food'],2)
                rt.semantic=inherited.policy('explore' if accept else 'generic')
                nn=NeighborEncounter(rt,'bystander',mii_module=mii)
                self.assertEqual(nn.own_food_commitments(),[])
                n.independent_actor_beat('worker')
                self.assertEqual(len(rt.ledger.world(name)[1]['material_feeding_events']),int(accept))
                self.assertEqual(n.own_food_commitments()[0],record)
                self.assertTrue(rt.verify()['valid'])

    def test_deadline_at_exclusive_boundary_and_invalid_undertaking(self):
        rt,n,_=self.build('boundary')
        clock=rt.ledger.world('boundary')[1]['clock']
        before=deepcopy(rt.ledger.world('boundary'))
        count=len(rt.ledger.events())
        with self.assertRaisesRegex(ValueError,'HUMAN_OFFER_INVALID_DEADLINE'):
            n.contribute('past','PLEDGE_OFFER',target_actor_ref='worker',due_clock=clock+1)
        self.assertEqual(rt.ledger.world('boundary'),before)
        self.assertEqual(len(rt.ledger.events()),count)
        due=clock+3
        n.contribute('pledge','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due)
        with self.assertRaisesRegex(ValueError,'HUMAN_OFFER_ALREADY_PENDING'):
            n.contribute('duplicate','PLEDGE_OFFER',target_actor_ref='worker',due_clock=due+2)
        n.contribute('wait','WAIT')
        at=n.contribute('boundary','OFFER_FEED',target_actor_ref='worker')
        self.assertEqual(rt.ledger.world('boundary')[1]['clock'],due)
        self.assertNotIn('human_offer_commitment_ref',at)
        self.assertEqual(n.own_food_commitments()[0]['status'],'WINDOW_ELAPSED_WITHOUT_AUTHORED_OFFER')
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':unittest.main()
