"""Actual CO R27 + MII public-occurrence first reader, sourcefree.
Research-requested actions exercise world settlement, not actor-chosen intent.
"""
from pathlib import Path
import sys
import tempfile
import unittest
from copy import deepcopy

ROOT=Path(__file__).resolve().parents[3]
for p in (ROOT/'SEAM'/'ORACLE'/'UM_SOROK_ORGANISM_R3',
          ROOT/'WORKER_RETURNS'/'SOROK-P5-CONTINUOUS-EXPERIENCE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P6-ONE-LIVING-HOUSE-R1',
          ROOT/'WORKER_RETURNS'/'SOROK-P4-CORE-LOOP-R1',
          ROOT, ROOT/'SEAM'/'NEIGHBORMULCH'):
    sys.path.insert(0,str(p))
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult, blank_world
from neighbor_runtime import NeighborEncounter
import mii

class PublicOccurrenceR8(unittest.TestCase):
    def build(self, *, visible=False, audible=True, visitor_room='workshop'):
        self.tmp=tempfile.TemporaryDirectory(prefix='neighbor_public_r8_')
        self.addCleanup(self.tmp.cleanup)
        self.db=str(Path(self.tmp.name)/'world.sqlite')
        self.rt=ConstitutiveRuntime(self.db)
        self.addCleanup(lambda:self.rt.close())
        self.rt.ledger.initialize(blank_world(self.rt.world_id),
                                  [adult('worker','Worker','workshop')])
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{
                room:{'light':'lit' if visible else 'dark',
                      'sightline':'unobstructed' if visible else 'blocked',
                      'hearing':audible,
                      'sound_path':'audible' if audible else 'blocked'}
                for room in ('workshop','home')},
            'actor_conditions':{'worker':{
                'facing':'entrance','hearing':True,'visual':True,
                'light':'lit','sightline':'unobstructed','sound_path':'audible'}},
        },request_id='geometry')
        self.n.contribute('arrive','MOVE',destination=visitor_room)

    def signs(self):
        before=deepcopy(self.rt.ledger.world('w1'))
        actors=deepcopy(self.rt.ledger.actors())
        view=self.n.private_surface(self.n.new_private_profile())
        self.assertEqual(before,self.rt.ledger.world('w1'))
        self.assertEqual(actors,self.rt.ledger.actors())
        return [row for row in view['mandatory'] if row['kind']=='CO_PUBLIC_OCCURRENCE']

    def act(self,action,**kw):
        result=self.rt.step('worker',requested_action=action,**kw)
        self.assertTrue(self.rt.verify()['valid'])
        return result

    def test_auditory_world_speech_without_vision_or_prose_tip(self):
        self.build()
        result=self.act('SPEAK')
        self.assertEqual(result['status'],'PERFORMED')
        signs=self.signs()
        self.assertEqual(len(signs),1)
        sign=signs[0]
        self.assertEqual(sign['modality'],'auditory')
        self.assertEqual(sign['source_event_ref'],result['receipt'])
        self.assertEqual(sign['source_cue_ref'],self.rt.ledger.world('w1')[1]['cues'][-1]['id'])
        self.assertEqual(sign['speaker_identity'],'NOT_ESTABLISHED')
        self.assertEqual(sign['lexical_content'],'NOT_CAPTURED_OR_RECONSTRUCTED')
        self.assertNotIn('worker',str(sign))
        self.assertNotIn('SPEECH_PERFORMED',str(sign))

    def test_same_occurrence_cold_reopens_without_narrator_cache(self):
        self.build()
        self.act('SPEAK')
        before=self.signs()
        self.assertEqual(len(before),1)
        self.rt.close()
        self.rt=ConstitutiveRuntime(self.db)
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.assertEqual(self.signs(),before)
        self.assertTrue(self.rt.verify()['valid'])

    def test_blocked_sound_and_other_room_are_not_received(self):
        for audible,room in ((False,'workshop'),(True,'home')):
            with self.subTest(audible=audible,room=room):
                self.build(audible=audible,visitor_room=room)
                self.act('SPEAK')
                self.assertEqual(self.signs(),[])
                self.rt.close()

    def test_silent_action_is_not_audible_and_visible_orientation_is_visible(self):
        self.build(visible=True,audible=False)
        self.act('ORIENT')
        signs=self.signs()
        self.assertEqual(len(signs),1)
        self.assertEqual(signs[0]['modality'],'visual')
        self.act('SPEAK')
        self.assertEqual(self.signs(),[])

    def test_partial_speech_no_fabricated_performed_utterance(self):
        self.build()
        result=self.act('SPEAK',object_ref='nonexistent')
        self.assertNotEqual(result['status'],'PERFORMED')
        self.assertEqual(self.signs(),[])

    def test_stale_occurrence_does_not_become_ongoing_sound(self):
        self.build()
        self.act('SPEAK')
        self.assertEqual(len(self.signs()),1)
        self.n.contribute('later','WAIT')
        self.assertEqual(self.signs(),[])

if __name__=='__main__':
    unittest.main()
