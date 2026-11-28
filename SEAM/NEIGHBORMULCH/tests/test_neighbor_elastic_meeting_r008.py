"""R008 elastic agreement: actual withdrawal, fresh assent, opportunity cost.

The original appointment and its actor's assent remain ledger history.
No invented notice, no transfer of assent and no new human calendar.
"""
from copy import deepcopy
import unittest
from test_neighbor_meeting_time_r38 import MeetingTimeR38
from neighbor_runtime import NeighborEncounter,EncounterRefusal
from um_sorok_organism.runtime import ConstitutiveRuntime
import mii

class ElasticMeetingCourt(unittest.TestCase):
    def test_cancel_and_repropose_independent_assent_or_earned_wage(self):
        for choice in ('accept','work'):
            with self.subTest(choice=choice):
                helper=MeetingTimeR38()
                self.addCleanup(helper.doCleanups)
                rt,n,db,state,sem,old,due=helper.build(choice)
                self.assertEqual(n.independent_actor_beat('worker')['attempt'],'ACCEPT_MEETING')
                self.assertEqual(helper.row(rt,old)['accepted_at_clock'],4)
                n.contribute('depart','LEAVE')
                before=deepcopy(rt.ledger.actors())
                snapshot=deepcopy(rt.ledger.world())
                with self.assertRaisesRegex(EncounterRefusal,'MEETING_WITHDRAWAL_NOT_QUALIFIED'):
                    NeighborEncounter(rt,'outsider',mii_module=mii).contribute(
                        'steal','WITHDRAW_MEETING',target_commitment_ref=old)
                self.assertEqual(rt.ledger.world(),snapshot)
                withdrawal=n.contribute('cancel','WITHDRAW_MEETING',target_commitment_ref=old)
                self.assertEqual(withdrawal['potential_actor_evidence'],[])
                self.assertEqual(rt.ledger.actors(),before)
                self.assertEqual(rt.ledger.world()[1]['clock'],6)
                self.assertTrue(n.contribute('cancel','WITHDRAW_MEETING',
                    target_commitment_ref=old)['idempotent_replay'])
                prior=deepcopy(rt.ledger.events())
                row=helper.row(rt,old)
                self.assertEqual(row['status'],'WITHDRAWN_BY_AUTHORED_ACT')
                self.assertEqual(row['withdrawn_from_status'],'ACCEPTED')
                self.assertEqual(row['accepted_at_clock'],4)
                self.assertEqual(row['settled_at_clock'],6)
                rt.close()
                cold=ConstitutiveRuntime(db,semantic=sem)
                self.addCleanup(cold.close)
                n=NeighborEncounter(cold,'visitor',mii_module=mii)
                self.assertEqual(n.own_meetings()[0]['status'],'WITHDRAWN_BY_AUTHORED_ACT')
                n.contribute('return','MOVE',destination='workshop')
                before=deepcopy(cold.ledger.world())
                with self.assertRaisesRegex(EncounterRefusal,'MEETING_REPLACEMENT_NOT_QUALIFIED'):
                    n.contribute('same','PROPOSE_MEETING',target_actor_ref='worker',
                                 target_commitment_ref=old,due_clock=due)
                self.assertEqual(cold.ledger.world(),before)
                proposal=n.contribute('new','PROPOSE_MEETING',target_actor_ref='worker',
                                       target_commitment_ref=old,due_clock=16)
                new=proposal['meeting_ref'];self.assertNotEqual(new,old)
                self.assertEqual(helper.row(cold,new)['status'],'PROPOSED')
                self.assertEqual(helper.row(cold,old)['replacement_meeting_ref'],new)
                self.assertEqual(helper.row(cold,new)['replaces_meeting_ref'],old)
                self.assertEqual(cold.ledger.events()[:len(prior)],prior)
                state['phase']=choice
                act=n.independent_actor_beat('worker')
                self.assertEqual((act['attempt'],act['status']),
                    ('ACCEPT_MEETING' if choice=='accept' else 'WORK','PERFORMED'))
                self.assertEqual(cold.ledger.world()[1]['accounts'].get('worker',0),
                                 0 if choice=='accept' else .25)
                self.assertEqual(helper.row(cold,new)['status'],
                                 'ACCEPTED' if choice=='accept' else 'PROPOSED')
                # Both histories remain actual; the newly offered meeting
                # cannot silently consume the old assent or its clock.
                before=deepcopy(cold.ledger.world())
                with self.assertRaisesRegex(EncounterRefusal,'MEETING_REPLACEMENT_NOT_QUALIFIED'):
                    n.contribute('duplicate-replacement','PROPOSE_MEETING',
                        target_actor_ref='worker',target_commitment_ref=old,due_clock=20)
                self.assertEqual(cold.ledger.world(),before)
                n.contribute('depart-again','LEAVE')
                state['phase']='wait'
                departure=cold.ledger.world()[1]['neighbor_user_events'][-1]['event_ref']
                n.continue_absent_life_until(departure,12)
                if choice=='accept':
                    n.contribute('arrive-new','MOVE',destination='workshop')
                    n.contribute('new-checkin','CHECK_IN_MEETING',target_commitment_ref=new)
                    state['phase']='meet'
                    self.assertEqual(n.independent_actor_beat('worker')['attempt'],'MEET_VISITOR')
                    self.assertEqual(helper.row(cold,new)['status'],'MEETING_PERFORMED')
                else:
                    n.continue_absent_life_until(departure,17)
                    self.assertEqual(helper.row(cold,new)['status'],'ELAPSED_WITHOUT_ACTOR_ASSENT')
                rows={x['id']:x for x in n.own_meetings()}
                self.assertEqual(rows[old]['status'],'WITHDRAWN_BY_AUTHORED_ACT')
                self.assertEqual(rows[old]['replacement_meeting_ref'],new)
                self.assertTrue(cold.verify()['valid'])

if __name__=='__main__':unittest.main()
