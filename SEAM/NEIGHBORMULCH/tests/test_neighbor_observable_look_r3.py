"""R3 first-consumer court: outward LOOK versus private ATTEND.
Real CO ResearchLedger/actor, sourcefree visibility, MII, autonomous
continuation, and SQLite replay. Never grants visitor/actor mind-reading.
"""
from pathlib import Path
import copy
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
for part in (
    ROOT / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P6-ONE-LIVING-HOUSE-R1',
    ROOT / 'WORKER_RETURNS' / 'SOROK-P4-CORE-LOOP-R1',
    ROOT, ROOT / 'SEAM' / 'NEIGHBORMULCH',
):
    sys.path.insert(0, str(part))

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii


class ObservableVisitorR3(unittest.TestCase):
    def build(self, *, facing='entrance', hearing=True, visual=True, actor_location='workshop'):
        self.temp = tempfile.TemporaryDirectory(prefix='neighbor_r3_')
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / 'one_world.sqlite'
        self.rt = ConstitutiveRuntime(self.db)
        self.addCleanup(lambda: self.rt.close())
        world = blank_world(self.rt.world_id)
        world['material_objects']['bill'] = {
            'id': 'bill', 'location': 'workshop',
            'public_glance': 'A paper bill lies on the bench',
            'grade': 'SOURCEFREE_TEST_ONLY'}
        self.rt.ledger.initialize(world, [adult('worker', 'Worker', actor_location)])
        self.enc = NeighborEncounter(self.rt, 'visitor', mii_module=mii)
        source = {'grade': 'SOURCEFREE_TEST_ONLY',
                  'user_conditions': {
                      'workshop': {'light': 'lit', 'sightline': 'unobstructed',
                                   'hearing': True, 'sound_path': 'audible'},
                      'home': {'light': 'dark', 'sightline': 'blocked',
                               'hearing': False, 'sound_path': 'blocked'}},
                  'actor_conditions': {
                      'worker': {'facing': facing, 'hearing': hearing, 'visual': visual,
                                 'light': 'lit', 'sightline': 'unobstructed',
                                 'sound_path': 'audible' if hearing else 'blocked'}}}
        self.enc.install_sourcefree_conditions(source, request_id='geometry')
        self.enc.contribute('arrival', 'MOVE', destination='workshop')
        return self.enc

    def test_one_world_look_cover_two_modalities_no_mind_reading(self):
        self.build()
        count = self.rt.verify()['events']
        result = self.enc.contribute('glance', 'LOOK', target_object_ref='bill',
                                     cover_text='What time does the workshop close?')
        self.assertEqual(result['status'], 'PERFORMED')
        self.assertEqual(self.rt.verify()['events'], count + 1)
        self.assertEqual({s['modality'] for s in result['potential_actor_evidence']},
                         {'auditory', 'visual'})
        self.assertEqual({s['basis'] for s in result['potential_actor_evidence']},
                         {'visitor_speech', 'visitor_glance'})
        event = self.rt.ledger.world('w1')[1]['neighbor_user_events'][-1]
        self.assertEqual(event['visitor_reading'], 'NOT_ESTABLISHED')
        self.assertEqual(event['other_actor_interpretation'], 'NOT_ESTABLISHED')
        self.assertTrue(self.rt.verify()['valid'])

    def test_look_visual_opportunity_does_not_issue_knowledge_or_uptake(self):
        self.build()
        response = self.enc.contribute('glance', 'LOOK', target_object_ref='bill')
        self.assertEqual([x['modality'] for x in response['potential_actor_evidence']],
                         ['visual'])
        access = self.rt.see('worker')
        self.assertTrue(any(x['kind'] == 'visitor_glance' for x in access['cues']))
        self.assertFalse(any('bill' in str(x.get('description')) for x in access['cues']
                             if x['kind'] == 'visitor_glance'))
        self.assertEqual(response['actor_uptake'], 'NOT_ESTABLISHED')

    def test_behind_hearing_without_vision(self):
        self.build(facing='away')
        response = self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                       cover_text='Ordinary words.')
        self.assertEqual([x['modality'] for x in response['potential_actor_evidence']],
                         ['auditory'])

    def test_visual_but_no_hearing(self):
        self.build(hearing=False)
        response = self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                       cover_text='Words that are not audible.')
        self.assertEqual([x['modality'] for x in response['potential_actor_evidence']],
                         ['visual'])

    def test_actor_elsewhere_does_not_receive_glance_or_cover(self):
        self.build(actor_location='home')
        response = self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                       cover_text='Hi?')
        self.assertEqual(response['potential_actor_evidence'], [])

    def test_private_mii_attention_does_not_touch_world_actor_or_clock(self):
        self.build()
        profile = self.enc.new_private_profile()
        world = copy.deepcopy(self.rt.ledger.world('w1'))
        actor = copy.deepcopy(self.rt.ledger.actor('worker'))
        count = len(self.rt.ledger.events())
        view = self.enc.private_surface(profile, command='look')
        self.assertEqual(view['schema'], 'SOROK_MII_SURFACE@1')
        self.assertEqual(self.rt.ledger.world('w1'), world)
        self.assertEqual(self.rt.ledger.actor('worker'), actor)
        self.assertEqual(len(self.rt.ledger.events()), count)

    def test_unknown_object_blocked_without_cover_or_actor_knowledge(self):
        self.build()
        for rid in ('unknown1', 'unknown2'):
            response = self.enc.contribute(rid, 'LOOK',
                                           target_object_ref='unknown-object',
                                           cover_text='This cannot be heard.')
            self.assertEqual(response['status'], 'BLOCKED')
            self.assertEqual(response['potential_actor_evidence'], [])
        self.assertTrue(self.rt.verify()['valid'])

    def test_replay_conflict_fails_and_old_move_replay_is_unchanged(self):
        self.build()
        self.assertTrue(self.enc.contribute('arrival', 'MOVE',
                                            destination='workshop')['idempotent_replay'])
        first = self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                    cover_text='Unchanged.')
        ids = [e['id'] for e in self.rt.ledger.events()]
        second = self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                     cover_text='Unchanged.')
        self.assertTrue(second['idempotent_replay'])
        self.assertEqual(first['event_ref'], second['event_ref'])
        with self.assertRaisesRegex(EncounterRefusal, 'REQUEST_REPLAY_CHANGED_PAYLOAD'):
            self.enc.contribute('look', 'LOOK', target_object_ref='bill',
                                cover_text='Changed.')
        self.assertEqual([e['id'] for e in self.rt.ledger.events()], ids)

    def test_look_to_real_actor_life_and_cold_reopen(self):
        self.build()
        look = self.enc.contribute('look', 'LOOK', target_object_ref='bill')
        cue_refs = [x['cue_ref'] for x in look['potential_actor_evidence']]
        continuing = self.enc.continue_independent_life_during_visit()
        self.assertEqual(continuing['status'], 'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        self.assertNotIn('actor_operation', continuing)
        event = self.rt.ledger.events()[-1]
        self.assertEqual(event['kind'], 'ACTOR_LIFE_TRANSITION')
        readset = event['envelope']['payload']['private_pre_event_psychodynamics']['worker']['readset']
        for ref in cue_refs:
            self.assertIn(ref, readset)
        ids = [e['id'] for e in self.rt.ledger.events()]
        self.rt.close()
        self.rt = ConstitutiveRuntime(self.db)
        self.enc = NeighborEncounter(self.rt, 'visitor', mii_module=mii)
        self.assertTrue(self.rt.verify()['valid'])
        self.assertEqual([e['id'] for e in self.rt.ledger.events()], ids)
        self.assertTrue(self.enc.contribute('look', 'LOOK',
                                            target_object_ref='bill')['idempotent_replay'])
        self.assertEqual(self.enc.continue_independent_life_during_visit()['status'],
                         'ALREADY_ADVANCED_AFTER_USER_OCCASION')
        self.assertEqual([e['id'] for e in self.rt.ledger.events()], ids)

    def test_user_cannot_force_actor_or_convert_settings_to_diegesis(self):
        self.build()
        with self.assertRaisesRegex(EncounterRefusal, 'UNAUTHORED_LOOK_OR_COVER'):
            self.enc.contribute('cover', 'WAIT', cover_text='I control you.')
        with self.assertRaisesRegex(EncounterRefusal, 'UNKNOWN_USER_OPERATION'):
            self.enc.contribute('settings', 'DELETE_ACCOUNT')
        with self.assertRaisesRegex(EncounterRefusal, 'INVALID_LOOK_TARGET'):
            self.enc.contribute('look-no-target', 'LOOK')
        self.assertTrue(self.rt.verify()['valid'])


if __name__ == '__main__':
    unittest.main()
