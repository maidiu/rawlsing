"""R27 sourcefree joined cross-continuity occasion court.

Same offered historical *occasion* may yield distinct admissible world signs
across already divergent real SQLite actor/world histories. This court does
not simulate traffic injuries, illness, real news, actual drug efficacy or
other unissued physical/medical/psychological law.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.continuity_clock import qualify_contingent_world_notice
from um_sorok_organism.types import copy


PARENT = {
    'source_ref': 'r27_sourcefree_not_an_empirical_respondent',
    'answers': {'R27_FICTIONAL': 'NATIVE_SOURCE_UNISSUED'},
    'fictional_seed': {'projects': []},
}


def notice(clock=0, requires=None, offer='COMMON-20261121-01'):
    return {
        'offer_id':offer,
        'at_world_clock':clock,
        'location':'home',
        'kind':'offered_external_occurrence_sign',
        'tags':['offered_news','world_notice'],
        'description':'A sourcefree common occurrence has a potentially audible local sign.',
        'required_actor_locations':(
            {'mother':'home'} if requires is None else requires),
    }


class ContingentWorldNoticeR27(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        root=Path(self.tmp.name)
        self.a=ConstitutiveRuntime(root/'branch_A.sqlite',world_id='branch_A')
        self.b=ConstitutiveRuntime(root/'branch_B.sqlite',world_id='branch_B')
        for rt in (self.a,self.b):
            rt.initialize([('mother','Mother',PARENT)])
    def tearDown(self):
        self.a.close()
        self.b.close()
        self.tmp.cleanup()
    def test_same_offer_in_two_worlds_qualified_by_actually_divergent_lives(self):
        # One world has a mother at home; the other a real performed MOVE.
        keep=self.a.step('mother',requested_action='REST')
        move=self.b.step('mother',requested_action='MOVE',
                         object_ref='workshop')
        self.assertEqual(keep['status'],'PERFORMED')
        self.assertEqual(move['status'],'PERFORMED')
        self.assertEqual(self.a.ledger.world('branch_A')[1]['positions']['mother'],'home')
        self.assertEqual(self.b.ledger.world('branch_B')[1]['positions']['mother'],'workshop')
        proposed=notice(clock=1)
        before_b=self.b.verify()['events']
        accepted=self.a.offer_contingent_world_notice(proposed)
        denied=self.b.offer_contingent_world_notice(proposed)
        self.assertEqual(accepted['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
        self.assertEqual(denied['status'],'INAPPLICABLE_ACTOR_LIFE_DIVERGED')
        self.assertTrue(denied['no_world_write'])
        self.assertEqual(self.b.verify()['events'],before_b)
        self.assertNotEqual(self.a.ledger.world('branch_A')[1]['clock'],
                            self.b.ledger.world('branch_B')[1]['clock'])
        self.assertEqual(len([c for c in self.a.see('mother')['cues']
                              if c['id']==accepted['cue_ref']]),1)
        self.assertEqual(len([c for c in self.b.see('mother')['cues']
                              if c.get('contingent_offer_id')==proposed['offer_id']]),0)
        self.assertEqual(self.a.snapshot('mother')['memories'],[])
        self.assertEqual(self.b.snapshot('mother')['memories'],[])
        self.assertTrue(self.a.verify()['valid'])
        self.assertTrue(self.b.verify()['valid'])

    def test_same_world_independent_eligible_offers_do_not_merge_histories(self):
        proposed=notice(requires={})
        aa=self.a.offer_contingent_world_notice(proposed)
        bb=self.b.offer_contingent_world_notice(proposed)
        self.assertEqual(aa['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
        self.assertEqual(bb['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
        for rt,wid in ((self.a,'branch_A'),(self.b,'branch_B')):
            world=rt.ledger.world(wid)[1]
            self.assertEqual(len([c for c in world['cues']
                         if c.get('contingent_offer_id')==proposed['offer_id']]),1)
            self.assertEqual(rt.snapshot('mother')['memories'],[])
            self.assertTrue(rt.verify()['valid'])
        self.assertNotEqual(aa['receipt'],bb['receipt'])

    def test_replay_is_idempotent_and_mutated_offer_fails_closed(self):
        proposed=notice()
        first=self.a.offer_contingent_world_notice(proposed)
        event_count=self.a.verify()['events']
        repeated=self.a.offer_contingent_world_notice(proposed)
        self.assertEqual(repeated['status'],'ALREADY_ADMITTED_IN_THIS_WORLD')
        self.assertEqual(repeated['cue_ref'],first['cue_ref'])
        self.assertEqual(self.a.verify()['events'],event_count)
        mutation={**proposed,'description':'Same id but changed source content'}
        with self.assertRaisesRegex(ValueError,'CONTINGENT_NOTICE_CONFLICTING_REPLAY'):
            self.a.offer_contingent_world_notice(mutation)
        self.assertEqual(self.a.verify()['events'],event_count)

    def test_clock_mismatch_or_lost_local_site_does_not_invent_event(self):
        count=self.a.verify()['events']
        result=self.a.offer_contingent_world_notice(notice(clock=3))
        self.assertEqual(result['status'],'INAPPLICABLE_WORLD_CLOCK')
        self.assertEqual(self.a.verify()['events'],count)
        # A future hypothetical with an absent material site is a negative,
        # never a license to invent that site or change family locations.
        current=self.a.ledger.world('branch_A')[1]
        missing=copy(current)
        missing['sites'].pop('home')
        self.assertEqual(qualify_contingent_world_notice(
            missing,self.a.ledger.actors(),notice())['status'],
            'INAPPLICABLE_SITE_NO_LONGER_EXISTS')

    def test_forged_person_and_invalid_offer_fail_before_any_write(self):
        prior=self.a.verify()['events']
        for bad in (
            notice(requires={'stranger':'home'}),
            notice(requires={'mother':'nowhere'}),
            {**notice(),'at_world_clock':True},
            {**notice(),'tags':['okay',None]},
            {**notice(),'tags':[],'hijack':'actor_private_state'},
            {**notice(),'offer_id':''},
        ):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.a.offer_contingent_world_notice(bad)
                self.assertEqual(self.a.verify()['events'],prior)

    def test_cold_restore_recovers_branch_owned_event_without_other_branch(self):
        proposed=notice()
        receipt=self.a.offer_contingent_world_notice(proposed)
        path=Path(self.tmp.name)/'branch_A.sqlite'
        cold=ConstitutiveRuntime(path,world_id='branch_A')
        try:
            self.assertTrue(cold.verify()['valid'])
            self.assertEqual(cold.offer_contingent_world_notice(proposed)
                            ['status'],'ALREADY_ADMITTED_IN_THIS_WORLD')
            self.assertEqual(cold.offer_contingent_world_notice(proposed)
                            ['cue_ref'],receipt['cue_ref'])
            self.assertTrue(cold.verify()['valid'])
            self.assertFalse(any(c.get('contingent_offer_id')
                                 for c in self.b.ledger.world('branch_B')[1]['cues']))
        finally:
            cold.close()


if __name__ == '__main__':
    unittest.main()
