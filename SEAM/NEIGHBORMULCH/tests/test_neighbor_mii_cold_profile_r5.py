"""R5: cold human-facing continuity using EXISTING protected MII sidecar,
without creating another world/actor writer or storing human psychographics
in the simulated Other. Sourcefree, trusted application profile path only.
"""
from __future__ import annotations
import copy
import json
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


class ColdHumanMIIContinuityR5(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='neighbor_mii_cold_r5_')
        self.addCleanup(self.tmp.cleanup)
        self.db = str(Path(self.tmp.name) / 'world.sqlite')
        self.sidecar = Path(self.tmp.name) / 'mii_private_profiles.json'
        self.rt = ConstitutiveRuntime(self.db)
        self.addCleanup(lambda: self.rt.close())
        world = blank_world(self.rt.world_id)
        world['material_objects'] = {
            'a_mug': {'id': 'a_mug', 'location': 'workshop',
                      'public_glance': 'A plain mug on the bench',
                      'grade': 'SOURCEFREE_TEST_ONLY'},
            'z_bill': {'id': 'z_bill', 'location': 'workshop',
                       'public_glance': 'A folded bill on the bench',
                       'public_close': 'A sourcefree close line',
                       'grade': 'SOURCEFREE_TEST_ONLY'},
        }
        self.rt.ledger.initialize(world, [adult('worker', 'Mara', 'workshop')])
        self.enc = NeighborEncounter(self.rt, 'visitor', mii_module=mii)
        self.enc.install_sourcefree_conditions({
            'grade': 'SOURCEFREE_TEST_ONLY',
            'user_conditions': {
                'workshop': {'light': 'lit', 'sightline': 'unobstructed',
                             'legibility': 'readable',
                             'hearing': True, 'sound_path': 'audible'},
                'home': {'light': 'dark', 'sightline': 'blocked',
                         'legibility': 'unreadable',
                         'hearing': False, 'sound_path': 'blocked'}},
            'actor_conditions': {'worker': {
                'facing': 'entrance', 'hearing': True, 'visual': True,
                'light': 'lit', 'sightline': 'unobstructed',
                'sound_path': 'audible'}},
        }, request_id='geometry')
        self.enc.contribute('arrive', 'MOVE', destination='workshop')

    def _reopen(self):
        self.rt.close()
        self.rt = ConstitutiveRuntime(self.db)
        self.enc = NeighborEncounter(self.rt, 'visitor', mii_module=mii)
        self.assertTrue(self.rt.verify()['valid'])

    def _seed_adaptive(self):
        profile = self.enc.new_private_profile()
        profile['mode'] = 'ADAPTIVE'
        profile['policy'] = mii.ADAPTIVE_POLICY_VERSION
        profile['learning_enabled'] = True
        self.enc.save_private_profile(self.sidecar, profile)
        return profile

    def test_cold_user_attention_changes_only_the_mii_selected_surface(self):
        self._seed_adaptive()
        self.enc.contribute('looking', 'LOOK', target_object_ref='z_bill')
        before = copy.deepcopy(self.rt.ledger.world('w1'))
        first = self.enc.private_surface_stored(self.sidecar, command='look',
                                                target='z_bill')
        self.assertEqual(first['optional']['text'], 'A sourcefree close line')
        self.assertEqual(self.rt.ledger.world('w1'), before)
        learned = self.enc.load_private_profile(self.sidecar)
        self.assertEqual(learned['hypotheses']['z_bill']['observations'], 1)
        self._reopen()
        before = copy.deepcopy(self.rt.ledger.world('w1'))
        after = self.enc.private_surface_stored(self.sidecar)
        self.assertEqual(after['optional']['target'], 'z_bill')
        self.assertEqual(after['optional']['selection_basis'], 'ADAPTIVE_HYPOTHESIS')
        self.assertEqual(after['optional']['text'], 'A folded bill on the bench')
        self.assertEqual(self.rt.ledger.world('w1'), before)
        self.assertNotIn('visitor', self.rt.ledger.actors())

    def test_same_committed_look_mii_exposure_idempotent_across_cold_reopen(self):
        self._seed_adaptive()
        self.enc.contribute('looking', 'LOOK', target_object_ref='z_bill')
        self.enc.private_surface_stored(self.sidecar, command='look', target='z_bill')
        p = self.enc.load_private_profile(self.sidecar)
        self.assertEqual(len(p['exposures']), 1)
        self._reopen()
        self.enc.private_surface_stored(self.sidecar, command='look', target='z_bill')
        p2 = self.enc.load_private_profile(self.sidecar)
        self.assertEqual(len(p2['exposures']), 1)
        self.assertEqual(p2['hypotheses']['z_bill']['observations'], 1)

    def test_visitor_profiles_separate_under_shared_mii_store_and_one_world(self):
        self._seed_adaptive()
        self.enc.contribute('looking', 'LOOK', target_object_ref='z_bill')
        self.enc.private_surface_stored(self.sidecar, command='look', target='z_bill')
        another = NeighborEncounter(self.rt, 'visitor-two', mii_module=mii)
        another.contribute('other-arrive', 'MOVE', destination='workshop')
        view = another.private_surface_stored(self.sidecar)
        self.assertEqual(view['optional']['target'], 'a_mug')
        other_profile = another.load_private_profile(self.sidecar)
        self.assertFalse(other_profile['hypotheses'])
        original = self.enc.load_private_profile(self.sidecar)
        self.assertEqual(original['hypotheses']['z_bill']['observations'], 1)
        self.assertNotEqual(original['scope'], other_profile['scope'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_private_profile_corruption_resets_without_actor_or_world_effect(self):
        self._seed_adaptive()
        self.enc.contribute('looking', 'LOOK', target_object_ref='z_bill')
        self.enc.private_surface_stored(self.sidecar, command='look', target='z_bill')
        corrupted = json.loads(self.sidecar.read_text(encoding='utf8'))
        corrupted['exposures'][0]['rendered']['optional']['text'] = 'FORGED_READING'
        self.sidecar.write_text(json.dumps(corrupted), encoding='utf8')
        before = copy.deepcopy(self.rt.ledger.world('w1'))
        profile = self.enc.load_private_profile(self.sidecar)
        self.assertEqual(profile.get('reset_reason'), 'EXPOSURE_TAMPER')
        self.assertFalse(profile['hypotheses'])
        self.assertEqual(self.rt.ledger.world('w1'), before)
        self.assertTrue(self.rt.verify()['valid'])

    def test_cross_scope_profile_save_refused_without_sidecar_write(self):
        another = NeighborEncounter(self.rt, 'visitor-two', mii_module=mii)
        incompatible = another.new_private_profile()
        before = copy.deepcopy(self.rt.ledger.world('w1'))
        with self.assertRaisesRegex(EncounterRefusal, 'MII_PROFILE_SCOPE_MISMATCH'):
            self.enc.save_private_profile(self.sidecar, incompatible)
        self.assertFalse(self.sidecar.exists())
        self.assertEqual(self.rt.ledger.world('w1'), before)

    def test_persisting_human_gaze_does_not_make_co_actor_follow_it(self):
        self._seed_adaptive()
        self.enc.contribute('looking', 'LOOK', target_object_ref='z_bill')
        viewer_before = copy.deepcopy(self.rt.ledger.actor('worker'))
        self.enc.private_surface_stored(self.sidecar, command='look', target='z_bill')
        self.assertEqual(self.rt.ledger.actor('worker'), viewer_before)
        future = self.enc.continue_independent_life_during_visit()
        self.assertEqual(future['status'], 'INDEPENDENT_ACTOR_WORLD_EVENT_COMMITTED')
        self.assertNotIn('visitor', self.rt.ledger.actors())
        self._reopen()
        self.assertEqual(self.enc.load_private_profile(self.sidecar)
                         ['hypotheses']['z_bill']['observations'], 1)
        self.assertEqual(self.enc.continue_independent_life_during_visit()['status'],
                         'ALREADY_ADVANCED_AFTER_USER_OCCASION')


if __name__ == '__main__':
    unittest.main()
