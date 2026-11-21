"""Exact R21 + protected MII sourcefree first-consumer regression court.

This test imports the EXISTING repository modules. It must be run on a checked
out, immutable Git SHA; local contract-spy tests alone do not validate it.
It does not claim that post-R21 organism R23–R25 has been reconciled.
"""
from __future__ import annotations
import copy
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'SEAM' / 'ORACLE' / 'UM_SOROK_ORGANISM_R3'))
sys.path.insert(0, str(ROOT / 'WORKER_RETURNS' / 'SOROK-P5-CONTINUOUS-EXPERIENCE-R1'))
sys.path.insert(0, str(ROOT / 'WORKER_RETURNS' / 'SOROK-P6-ONE-LIVING-HOUSE-R1'))
sys.path.insert(0, str(ROOT / 'WORKER_RETURNS' / 'SOROK-P4-CORE-LOOP-R1'))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'SEAM' / 'NEIGHBORMULCH'))

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world
import mii
from neighbor_runtime import NeighborEncounter, EncounterRefusal


GEOMETRY = {'grade':'SOURCEFREE_TEST_ONLY',
    'user_conditions': {
        'workshop': {'light':'lit', 'sightline':'unobstructed',
                     'hearing':True, 'sound_path':'audible'},
        'home': {'light':'dark', 'sightline':'blocked',
                 'hearing':False, 'sound_path':'blocked'},
    },
    'actor_conditions': {
        'worker': {'facing':'away', 'hearing':True, 'visual':True,
                   'light':'lit', 'sightline':'unobstructed',
                   'sound_path':'audible'},
    },
}


class JoinedR21Neighbor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='neighbormulch_r21_')
        self.db = str(Path(self.tmp.name) / 'one-world.sqlite')
        self.runtime = ConstitutiveRuntime(self.db)
        # Peripheral adult, not user-dependent Nadia, no invented survey source.
        world = blank_world(self.runtime.world_id)
        self.runtime.ledger.initialize(world, [adult('worker','Mara','workshop')])
        self.neighbor = NeighborEncounter(self.runtime,'visitor',mii_module=mii)
        self.neighbor.install_sourcefree_conditions(copy.deepcopy(GEOMETRY),request_id='initial_light')

    def tearDown(self):
        self.runtime.close()
        self.tmp.cleanup()

    def test_joined_user_event_actor_reception_and_cold_replay(self):
        before = self.runtime.snapshot('worker')
        entered = self.neighbor.contribute('come','MOVE',destination='workshop')
        self.assertEqual(entered['status'],'PERFORMED')
        self.assertEqual([x['modality'] for x in entered['potential_actor_evidence']], ['auditory'])
        # Use the REAL organism's actor-access reader on the committed cue.
        access = self.runtime.see('worker')
        self.assertTrue(any(x['kind']=='visitor_footsteps' for x in access['cues']))
        self.assertEqual(self.runtime.snapshot('worker')['actor'], before['actor'])
        speech = self.neighbor.contribute('said','SAY',text='This bench is in the way.')
        self.assertEqual(speech['actor_uptake'],'NOT_ESTABLISHED')
        access2 = self.runtime.see('worker')
        self.assertTrue(any(x['kind']=='visitor_speech' and
                            x['description']=='This bench is in the way.'
                            for x in access2['cues']))
        # The actual organism owns any independently selected continuation.
        changed = self.neighbor.independent_actor_beat('worker')
        self.assertIn('receipt',changed)
        self.assertNotEqual(changed['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
        # This sign was eligible for pre-action recruitment; the existing
        # organism's actual actor-specific pre-event readset must conserve it.
        # DO NOT misstate sensory availability as conscious perceived memory.
        occurred = self.runtime.ledger.events()[-1]
        self.assertEqual(occurred['kind'],'ACTOR_LIFE_TRANSITION')
        pre = occurred['envelope']['payload']['private_pre_event_psychodynamics']['worker']
        speech_refs = [row['cue_ref'] for row in speech['potential_actor_evidence']]
        self.assertTrue(speech_refs)
        for cue_ref in speech_refs:
            self.assertIn(cue_ref,pre['readset'],
                          'Actor policy lost qualified world event before situated recruitment')
        # The after-world subjective receipt may show only this actor's
        # current act. A source-eligible visitor sound is NOT automatically
        # an attended, understood or durable psychologically lived sign.
        lived = occurred['envelope']['payload']['private_actor_experience_receipts']['worker']
        self.assertTrue(lived['perceived_cues'])
        profile = self.neighbor.new_private_profile()
        world_before = self.runtime.ledger.world('w1')
        view = self.neighbor.private_surface(profile)
        self.assertEqual(view['schema'],'SOROK_MII_SURFACE@1')
        self.assertEqual(self.runtime.ledger.world('w1'),world_before)
        self.assertEqual(len(profile['exposures']),1)
        first_event_ids=[row['id'] for row in self.runtime.ledger.events()]
        self.assertTrue(self.runtime.verify())
        self.runtime.close()
        self.runtime=ConstitutiveRuntime(self.db)
        self.neighbor=NeighborEncounter(self.runtime,'visitor',mii_module=mii)
        self.assertTrue(self.runtime.verify())
        self.assertEqual([row['id'] for row in self.runtime.ledger.events()],first_event_ids)
        old=self.neighbor.contribute('come','MOVE',destination='workshop')
        self.assertTrue(old['idempotent_replay'])
        self.assertEqual(old['receipt'],entered['receipt'])
        self.assertEqual([row['id'] for row in self.runtime.ledger.events()],first_event_ids)

    def test_ordinary_work_continues_before_and_after_user_encounter(self):
        # The user is an interruption of independent material life, not its
        # scene-generator or the owner of the adult's practical initiative.
        prior=self.neighbor.independent_actor_beat('worker')
        self.assertIn('receipt',prior)
        pre_contact = [e['id'] for e in self.runtime.ledger.events()]
        self.assertFalse(self.runtime.ledger.world('w1')[1].get('neighbor_users'))
        self.neighbor.contribute('arrive','MOVE',destination='workshop')
        self.neighbor.contribute('leave','LEAVE')
        after=self.neighbor.independent_actor_beat('worker')
        self.assertIn('receipt',after)
        events=self.runtime.ledger.events()
        self.assertIn(prior['receipt'],[e['id'] for e in events])
        self.assertIn(after['receipt'],[e['id'] for e in events])
        self.assertTrue(all(e in [x['id'] for x in events] for e in pre_contact))
        self.assertNotIn('visitor',self.runtime.ledger.actors())
        self.assertTrue(self.runtime.verify())

    def test_private_exposure_does_not_recruit_actor_or_create_event(self):
        self.neighbor.contribute('come','MOVE',destination='workshop')
        profile=self.neighbor.new_private_profile()
        world_before=copy.deepcopy(self.runtime.ledger.world('w1'))
        count=len(self.runtime.ledger.events())
        self.neighbor.private_surface(profile,command='look')
        self.assertEqual(self.runtime.ledger.world('w1'),world_before)
        self.assertEqual(len(self.runtime.ledger.events()),count)

    def test_no_source_no_event_and_no_fake_actor(self):
        self.assertNotIn('visitor',self.runtime.ledger.actors())
        with self.assertRaisesRegex(EncounterRefusal,'USER_CANNOT_IMPERSONATE_ACTOR'):
            NeighborEncounter(self.runtime,'worker',mii_module=mii)
        with self.assertRaisesRegex(EncounterRefusal,'UNKNOWN_USER_OPERATION'):
            self.neighbor.contribute('gain','MAKE_WORKER_LIKE_ME')
        _,world=self.runtime.ledger.world('w1')
        self.assertNotIn('visitor',world['positions'])


if __name__=='__main__':
    unittest.main()
