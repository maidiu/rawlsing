"""R4: inherited P6 outward ORIENT/INSPECT distinction, protected MII
glance/close/attention and CO actor-eligible sensory history in ONE ledger.
Sourcefree first consumer, not a native human/actor scientific rule.
"""
from __future__ import annotations
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
for path in (ROOT / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P6-ONE-LIVING-HOUSE-R1',
             ROOT / 'WORKER_RETURNS' / 'SOROK-P4-CORE-LOOP-R1',
             ROOT, ROOT / 'SEAM' / 'NEIGHBORMULCH'):
    sys.path.insert(0, str(path))

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii


class P6MIICOR4(unittest.TestCase):
    def build(self, *, legibility='unreadable', sightline='unobstructed',
              light='lit', object_grade='SOURCEFREE_TEST_ONLY',
              actor_facing='entrance'):
        self.tmp = tempfile.TemporaryDirectory(prefix='neighbor_p6mii_r4_')
        self.addCleanup(self.tmp.cleanup)
        self.db = str(Path(self.tmp.name) / 'one_world.sqlite')
        self.runtime = ConstitutiveRuntime(self.db)
        self.addCleanup(lambda: self.runtime.close())
        world = blank_world(self.runtime.world_id)
        self.full_text = 'PRIVATE-LINE-FROM-QUALIFIED-CLOSE-DETAIL'
        item = {'id': 'bill', 'location': 'workshop',
                'public_glance': 'A printed sheet lies on the workbench.',
                'public_close': self.full_text}
        if object_grade is not None:
            item['grade'] = object_grade
        world['material_objects']['bill'] = item
        self.runtime.ledger.initialize(world, [adult('worker', 'Mara', 'workshop')])
        self.neighbor = NeighborEncounter(self.runtime, 'visitor', mii_module=mii)
        geometry = {
            'grade': 'SOURCEFREE_TEST_ONLY',
            'user_conditions': {
                'workshop': {'light': light, 'sightline': sightline,
                             'legibility': legibility,
                             'hearing': True, 'sound_path': 'audible'},
                'home': {'light': 'dark', 'sightline': 'blocked',
                         'legibility': 'unknown',
                         'hearing': False, 'sound_path': 'blocked'},
            },
            'actor_conditions': {
                'worker': {'facing': actor_facing, 'hearing': True,
                           'visual': True, 'light': 'lit',
                           'sightline': 'unobstructed',
                           'sound_path': 'audible'},
            },
        }
        self.neighbor.install_sourcefree_conditions(copy.deepcopy(geometry),
                                                     request_id='geometry')
        self.neighbor.contribute('arrival', 'MOVE', destination='workshop')
        return self.neighbor

    def test_outward_glance_visible_but_unreadable_with_separate_actor_access(self):
        self.build()
        profile = self.neighbor.new_private_profile()
        world_before = copy.deepcopy(self.runtime.ledger.world('w1'))
        unread = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertEqual(unread['optional']['text'],
                         'A printed sheet lies on the workbench.')
        self.assertEqual(self.runtime.ledger.world('w1'), world_before)
        actual = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill')
        self.assertEqual(actual['status'], 'PERFORMED')
        self.assertIn('visitor_glance',
                      [e['basis'] for e in actual['potential_actor_evidence']])
        after = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertNotIn(self.full_text, str(after))
        self.assertEqual(after['optional']['text'],
                         'A printed sheet lies on the workbench.')
        self.assertEqual(self.runtime.ledger.world('w1')[1]['neighbor_user_events'][-1]
                         ['visitor_reading'], 'NOT_ESTABLISHED')
        self.assertTrue(self.runtime.verify()['valid'])

    def test_committed_outward_and_readable_close_only_under_existing_mii_gate(self):
        self.build(legibility='readable')
        profile = self.neighbor.new_private_profile()
        before = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertNotIn(self.full_text, str(before))
        op = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill')
        self.assertEqual(op['status'], 'PERFORMED')
        world_before_view = copy.deepcopy(self.runtime.ledger.world('w1'))
        actor_before_view = copy.deepcopy(self.runtime.ledger.actor('worker'))
        after = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertEqual(after['optional']['text'], self.full_text)
        self.assertEqual(after['optional']['selection_basis'], 'EXPLICIT_USER_TARGET')
        self.assertEqual(self.runtime.ledger.world('w1'), world_before_view)
        self.assertEqual(self.runtime.ledger.actor('worker'), actor_before_view)
        self.assertNotIn(self.full_text,
            str(self.runtime.ledger.world('w1')[1]['neighbor_user_events'][-1]
                ['perceptual_candidates']))
        self.assertNotIn(self.full_text, str(self.runtime.see('worker')['cues']))

    def test_partial_sightline_allows_mii_glance_but_not_close(self):
        self.build(legibility='readable', sightline='partial')
        op = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill')
        self.assertEqual(op['status'], 'PERFORMED')
        view = self.neighbor.private_surface(
            self.neighbor.new_private_profile(), command='look', target='bill')
        self.assertEqual(view['optional']['text'],
                         'A printed sheet lies on the workbench.')
        self.assertNotIn(self.full_text, str(view))

    def test_darkness_does_not_retroactively_forbid_bodily_turn(self):
        self.build(light='dark', legibility='readable')
        op = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill')
        self.assertEqual(op['status'], 'PERFORMED')
        self.assertTrue(any(e['basis'] == 'visitor_glance'
                            for e in op['potential_actor_evidence']))
        view = self.neighbor.private_surface(
            self.neighbor.new_private_profile(), command='look', target='bill')
        self.assertIsNone(view['optional'])
        self.assertNotIn(self.full_text, str(view))

    def test_no_source_issued_close_even_if_bill_has_text(self):
        self.build(legibility='readable', object_grade=None)
        self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill')
        view = self.neighbor.private_surface(
            self.neighbor.new_private_profile(), command='look', target='bill')
        self.assertNotIn(self.full_text, str(view))
        self.assertEqual(view['optional']['text'],
                         'A printed sheet lies on the workbench.')

    def test_mii_profile_scope_must_match_user_and_world(self):
        self.build(legibility='readable')
        attacker_profile = NeighborEncounter(
            self.runtime, 'different-user', mii_module=mii).new_private_profile()
        world_before = copy.deepcopy(self.runtime.ledger.world('w1'))
        with self.assertRaisesRegex(EncounterRefusal, 'MII_PROFILE_SCOPE_MISMATCH'):
            self.neighbor.private_surface(attacker_profile, command='look',
                                          target='bill')
        self.assertEqual(self.runtime.ledger.world('w1'), world_before)
        self.assertEqual(attacker_profile['exposures'], [])

    def test_existing_mii_adaptive_exposure_is_private_and_idempotent(self):
        self.build(legibility='readable')
        profile = self.neighbor.new_private_profile()
        profile['mode'] = 'ADAPTIVE'
        profile['learning_enabled'] = True
        profile['policy'] = mii.ADAPTIVE_POLICY_VERSION
        self.neighbor.contribute('look', 'LOOK', target_object_ref='bill')
        world_before = copy.deepcopy(self.runtime.ledger.world('w1'))
        view1 = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertEqual(view1['optional']['text'], self.full_text)
        self.assertEqual(profile['hypotheses']['bill']['observations'], 1)
        first_count = len(profile['exposures'])
        view2 = self.neighbor.private_surface(profile, command='look', target='bill')
        self.assertEqual(view2['optional']['text'], self.full_text)
        self.assertEqual(len(profile['exposures']), first_count)
        self.assertEqual(profile['hypotheses']['bill']['observations'], 1)
        self.assertEqual(self.runtime.ledger.world('w1'), world_before)

    def test_actor_own_uncommanded_next_life_retains_glance_cue_not_user_reading(self):
        self.build(legibility='unreadable')
        op = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill',
                                      cover_text='Did you see the weather?')
        selected = self.neighbor.continue_independent_life_during_visit()
        self.assertEqual(selected['status'], 'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        event = self.runtime.ledger.events()[-1]
        pre = event['envelope']['payload']['private_pre_event_psychodynamics']['worker']
        for sign in op['potential_actor_evidence']:
            self.assertIn(sign['cue_ref'], pre['readset'])
        self.assertNotIn(self.full_text, str(pre))
        events = [row['id'] for row in self.runtime.ledger.events()]
        self.runtime.close()
        self.runtime = ConstitutiveRuntime(self.db)
        self.neighbor = NeighborEncounter(self.runtime, 'visitor', mii_module=mii)
        self.assertTrue(self.runtime.verify()['valid'])
        self.assertEqual(events, [row['id'] for row in self.runtime.ledger.events()])
        replay = self.neighbor.contribute('glance', 'LOOK', target_object_ref='bill',
                                          cover_text='Did you see the weather?')
        self.assertTrue(replay['idempotent_replay'])

    def test_invalid_legibility_refused_before_world_change(self):
        self.build()
        version, world = self.runtime.ledger.world('w1')
        other = NeighborEncounter(self.runtime, 'somebody-else', mii_module=mii)
        conditions = copy.deepcopy(world['neighbor_sensory_source'])
        conditions['user_conditions']['workshop']['legibility'] = 'magic-xray'
        with self.assertRaisesRegex(EncounterRefusal,
                                    'INVALID_USER_SENSORY_CONDITIONS'):
            other.install_sourcefree_conditions(conditions, request_id='tamper')
        self.assertEqual(self.runtime.ledger.world('w1'), (version, world))


if __name__ == '__main__':
    unittest.main()
