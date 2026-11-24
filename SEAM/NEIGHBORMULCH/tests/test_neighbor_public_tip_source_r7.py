"""R7 existing sourcefree MII surface: CO generated public tip is an
UNTYPED expression, not a licence for hearing an unseen actor's thoughts.
No new narration engine, actor cause, world writer or sensory source.
"""
from pathlib import Path
import sys
import tempfile
import unittest

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


class PublicTipOwnerGateR7(unittest.TestCase):
    def build(self, *, sightline='unobstructed',light='lit',hearing=True):
        self.tmp=tempfile.TemporaryDirectory(prefix='neighbor_tip_r7_')
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(str(Path(self.tmp.name)/'world.sqlite'))
        self.addCleanup(lambda:self.rt.close())
        world=blank_world(self.rt.world_id)
        self.rt.ledger.initialize(world,[adult('worker','Worker','workshop')])
        self.neighbor=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.neighbor.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{
                'workshop':{'light':light,'sightline':sightline,
                            'hearing':hearing,
                            'sound_path':'audible' if hearing else 'blocked'},
                'home':{'light':'dark','sightline':'blocked',
                        'hearing':False,'sound_path':'blocked'},
            },
            'actor_conditions':{
                'worker':{'facing':'entrance','hearing':True,'visual':True,
                          'light':'lit','sightline':'unobstructed',
                          'sound_path':'audible'},
            },
        },request_id='geometry')
        self.neighbor.contribute('arrival','MOVE',destination='workshop')
        return self.neighbor

    def _actual_actor_beat(self):
        result=self.neighbor.independent_actor_beat('worker')
        self.assertEqual(result['receipt'],self.rt.ledger.events()[-1]['id'])
        self.assertEqual(self.rt.ledger.events()[-1]['kind'],'ACTOR_LIFE_TRANSITION')
        self.assertTrue(isinstance(result['public_tip'],str) and result['public_tip'])
        self.assertTrue(self.rt.verify()['valid'])
        return result

    def _tips(self,view):
        return [x for x in view['mandatory'] if x['kind']=='PUBLIC_TIP']

    def test_audibility_cannot_qualify_untyped_silent_actor_expression(self):
        self.build(sightline='blocked',light='dark',hearing=True)
        actual=self._actual_actor_beat()
        view=self.neighbor.private_surface(self.neighbor.new_private_profile())
        self.assertFalse(self._tips(view))
        self.assertNotIn(actual['public_tip'],str(view))

    def test_partial_sightline_cannot_claim_recognized_expression(self):
        self.build(sightline='partial',light='lit',hearing=True)
        self._actual_actor_beat()
        view=self.neighbor.private_surface(self.neighbor.new_private_profile())
        self.assertFalse(self._tips(view))

    def test_visible_actual_co_receipt_may_show_bounded_public_expression(self):
        self.build(sightline='unobstructed',light='lit',hearing=False)
        actual=self._actual_actor_beat()
        world=self.rt.ledger.world('w1')[1]
        self.assertEqual(world['positions']['worker'],'workshop')
        view=self.neighbor.private_surface(self.neighbor.new_private_profile())
        tips=self._tips(view)
        self.assertEqual(len(tips),1)
        self.assertEqual(tips[0]['text'],actual['public_tip'][:500])
        self.assertEqual(tips[0]['modality_grade'],
                         'SOURCEFREE_VISUAL_ONLY_UNTYPED')
        self.assertNotIn('private_pre_event_psychodynamics',str(view))

    def test_forged_receipt_cannot_represent_an_actual_actor_tip(self):
        self.build(sightline='unobstructed',light='lit',hearing=False)
        actual=self._actual_actor_beat()
        self.neighbor._last_actor_tip=('not-a-ledger-event',
                                       self.rt.ledger.world('w1')[1]['clock'],
                                       actual['public_tip'])
        view=self.neighbor.private_surface(self.neighbor.new_private_profile())
        self.assertFalse(self._tips(view))

    def test_real_tip_invalidated_by_later_distinct_world_event(self):
        self.build(sightline='unobstructed',light='lit',hearing=False)
        self._actual_actor_beat()
        self.neighbor.contribute('elapsed','WAIT')
        view=self.neighbor.private_surface(self.neighbor.new_private_profile())
        self.assertFalse(self._tips(view))


if __name__=='__main__':
    unittest.main()
