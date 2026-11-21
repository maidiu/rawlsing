"""NEIGHBORMULCH R2: a visitor joins an *already autonomous* world.

Sourcefree joined test using actual CO ResearchLedger/actor selection and MII.
One visitor moment can be followed by one independent actor event, not a
visitor-commanded response. This is not a general background event scheduler.
"""
from pathlib import Path
import copy
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[3]
for path in (
    ROOT / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P6-ONE-LIVING-HOUSE-R1',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P4-CORE-LOOP-R1',
    ROOT,
    ROOT / 'SEAM' / 'NEIGHBORMULCH',
):
    sys.path.insert(0,str(path))

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import blank_world, adult
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii


GEOMETRY={
    'grade':'SOURCEFREE_TEST_ONLY',
    'user_conditions': {
        'workshop':{'light':'lit','sightline':'unobstructed',
                    'hearing':True,'sound_path':'audible'},
        'home':{'light':'dark','sightline':'blocked',
                'hearing':False,'sound_path':'blocked'},
    },
    'actor_conditions':{
        'worker':{'facing':'away','hearing':True,'visual':True,
                  'light':'lit','sightline':'unobstructed',
                  'sound_path':'audible'},
    },
}


class NeighborLiveInterruptionR2(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='neighbor_r2_')
        self.db=Path(self.temp.name)/'live.sqlite'
        self.rt=ConstitutiveRuntime(self.db)
        self.rt.ledger.initialize(
            blank_world(self.rt.world_id),
            [adult('worker','Worker','workshop')])
        self.visitor=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.visitor.install_sourcefree_conditions(
            copy.deepcopy(GEOMETRY),request_id='geometry')
    def tearDown(self):
        self.rt.close()
        self.temp.cleanup()

    def test_actual_user_arrival_and_an_uncommanded_actor_event_in_one_world(self):
        entered=self.visitor.contribute('arrive','MOVE',destination='workshop')
        self.assertEqual(entered['status'],'PERFORMED')
        before=self.rt.verify()['events']
        result=self.visitor.continue_independent_life_during_visit(
            profile=self.visitor.new_private_profile())
        self.assertEqual(result['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        self.assertEqual(result['source_user_event_ref'],entered['event_ref'])
        self.assertEqual(result['actor_selected_by_existing_initiative'],'worker')
        self.assertTrue(result['no_visitor_selected_actor_intention_or_response'])
        self.assertEqual(result['visitor_surface']['schema'],'SOROK_MII_SURFACE@1')
        self.assertEqual(self.rt.verify()['events'],before+1)
        self.assertEqual(self.rt.ledger.events()[-1]['kind'],'ACTOR_LIFE_TRANSITION')
        self.assertTrue(self.rt.verify()['valid'])

    def test_duplicate_same_user_occasion_does_not_create_two_actor_events(self):
        self.visitor.contribute('arrive','MOVE',destination='workshop')
        first=self.visitor.continue_independent_life_during_visit()
        count=self.rt.verify()['events']
        second=self.visitor.continue_independent_life_during_visit()
        self.assertEqual(second['status'],'ALREADY_ADVANCED_AFTER_USER_OCCASION')
        self.assertFalse(second['new_world_event'])
        self.assertEqual(self.rt.verify()['events'],count)
        self.visitor.contribute('new-speech','SAY',text='A new conversation turn.')
        fresh=self.visitor.continue_independent_life_during_visit()
        self.assertEqual(fresh['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        self.assertNotEqual(fresh['actor_event_receipt'],first['actor_event_receipt'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_visitor_absence_cannot_create_spurious_shared_scene(self):
        count=self.rt.verify()['events']
        with self.assertRaisesRegex(EncounterRefusal,'VISITOR_NOT_PRESENT'):
            self.visitor.continue_independent_life_during_visit()
        self.assertEqual(self.rt.verify()['events'],count)
        self.visitor.contribute('come','MOVE',destination='workshop')
        self.visitor.contribute('leave','LEAVE')
        count=self.rt.verify()['events']
        with self.assertRaisesRegex(EncounterRefusal,'VISITOR_NOT_PRESENT'):
            self.visitor.continue_independent_life_during_visit()
        self.assertEqual(self.rt.verify()['events'],count)

    def test_offscreen_worker_real_activity_without_unauthorized_public_tip(self):
        # Worker is at workshop. Visitor enters home and CANNOT see or hear
        # workshop, even though an independent worker does something there.
        self.visitor.contribute('home-arrival','MOVE',destination='home')
        profile=self.visitor.new_private_profile()
        result=self.visitor.continue_independent_life_during_visit(profile=profile)
        self.assertEqual(result['status'],'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        self.assertEqual(self.rt.ledger.events()[-1]['kind'],'ACTOR_LIFE_TRANSITION')
        surface=result['visitor_surface']
        self.assertEqual(surface['schema'],'SOROK_MII_SURFACE@1')
        self.assertFalse(any(x.get('kind')=='PUBLIC_TIP'
                             for x in surface.get('narration',[])
                             if isinstance(x,dict)))
        self.assertFalse(any(x.get('kind')=='CO_PRESENT_ACTOR'
                             for x in surface.get('narration',[])
                             if isinstance(x,dict)))
        self.assertEqual(self.rt.snapshot('worker')['actor'],'worker')
        self.assertTrue(self.rt.verify()['valid'])

    def test_cold_reopen_keeps_world_and_refuses_repeat(self):
        self.visitor.contribute('arrive','MOVE',destination='workshop')
        one=self.visitor.continue_independent_life_during_visit()
        saved_ids=[e['id'] for e in self.rt.ledger.events()]
        rt2=ConstitutiveRuntime(self.db)
        try:
            neighbor2=NeighborEncounter(rt2,'visitor',mii_module=mii)
            self.assertTrue(rt2.verify()['valid'])
            twice=neighbor2.continue_independent_life_during_visit()
            self.assertEqual(twice['status'],'ALREADY_ADVANCED_AFTER_USER_OCCASION')
            self.assertEqual([e['id'] for e in rt2.ledger.events()],saved_ids)
        finally:
            rt2.close()


if __name__=='__main__':
    unittest.main()
