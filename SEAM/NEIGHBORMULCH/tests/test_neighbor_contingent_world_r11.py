"""R11 actual independently qualified CO world occasion -> MII sensory exposure.
Sourcefree local sign only. No asserted news, event consequence or actor uptake.
"""
from copy import deepcopy
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

class ContingentWorldR11(unittest.TestCase):
    def build(self, name='w1', *, audible=True, room='workshop'):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_contingent_r11_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        rt=ConstitutiveRuntime(db,world_id=name)
        self.addCleanup(lambda:rt.close())
        rt.ledger.initialize(blank_world(name),[adult('worker','Mara','workshop')])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'dark','sightline':'blocked',
                 'hearing':audible,'sound_path':'audible' if audible else 'blocked'}
                 for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,
                'light':'lit','sightline':'unobstructed','hearing':True,
                'sound_path':'audible'}},
        },request_id='geometry')
        n.contribute('arrive','MOVE',destination=room)
        return rt,n,db

    def offer(self, rt, *, location='workshop',requires=None):
        return {'offer_id':'common-occasion',
                'at_world_clock':rt.ledger.world(rt.world_id)[1]['clock'],
                'location':location,'kind':'external_occurrence_sign',
                'tags':['offered_sign'],
                'description':'ANALYST CLAIM NOT HUMAN SPOKEN WORDS',
                'required_actor_locations':{'worker':'workshop'} if requires is None else requires}

    def signs(self, rt, n):
        before=deepcopy(rt.ledger.world(rt.world_id))
        actors=deepcopy(rt.ledger.actors())
        view=n.private_surface(n.new_private_profile())
        self.assertEqual(rt.ledger.world(rt.world_id),before)
        self.assertEqual(rt.ledger.actors(),actors)
        return [x for x in view['mandatory']
                if x.get('source')=='EXISTING_CO_BRANCH_LOCAL_CONTINGENT_SIGN']

    def test_same_offered_occasion_different_actual_lives_different_encounters(self):
        a,na,_=self.build('branch_A')
        b,nb,_=self.build('branch_B')
        a.step('worker',requested_action='REST')
        b.step('worker',requested_action='MOVE',object_ref='home')
        proposed=self.offer(a)
        self.assertEqual(proposed['at_world_clock'],self.offer(b)['at_world_clock'])
        before=b.verify()['events']
        admitted=a.offer_contingent_world_notice(proposed)
        refused=b.offer_contingent_world_notice(proposed)
        self.assertEqual(admitted['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
        self.assertEqual(refused['status'],'INAPPLICABLE_ACTOR_LIFE_DIVERGED')
        self.assertEqual(b.verify()['events'],before)
        signs=self.signs(a,na)
        self.assertEqual(len(signs),1)
        self.assertEqual(signs[0]['source_event_ref'],admitted['receipt'])
        self.assertEqual(signs[0]['source_cue_ref'],admitted['cue_ref'])
        self.assertEqual(signs[0]['external_event_truth'],'NOT_ESTABLISHED')
        self.assertNotIn('ANALYST CLAIM',str(signs))
        self.assertNotIn('worker',str(signs))
        self.assertEqual(self.signs(b,nb),[])
        self.assertTrue(any(c['id']==admitted['cue_ref'] for c in a.see('worker')['cues']))
        self.assertTrue(a.verify()['valid'] and b.verify()['valid'])

    def test_actual_public_sound_cold_reopens_without_actor_or_user_knowledge_write(self):
        rt,n,db=self.build()
        before=deepcopy(rt.ledger.actors())
        proposal=self.offer(rt)
        admitted=rt.offer_contingent_world_notice(proposal)
        self.assertEqual(rt.ledger.actors(),before)
        self.assertEqual(admitted['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
        sign=self.signs(rt,n)
        self.assertEqual(len(sign),1)
        rt.close()
        cold=ConstitutiveRuntime(db)
        self.addCleanup(cold.close)
        cn=NeighborEncounter(cold,'visitor',mii_module=mii)
        self.assertEqual(self.signs(cold,cn),sign)
        self.assertEqual(cold.offer_contingent_world_notice(proposal)['status'],
                         'ALREADY_ADMITTED_IN_THIS_WORLD')
        self.assertEqual(self.signs(cold,cn),sign)
        self.assertTrue(cold.verify()['valid'])

    def test_actual_local_occurrence_not_automatically_audible_to_visitor(self):
        for audible,room in ((False,'workshop'),(True,'home')):
            with self.subTest(audible=audible,room=room):
                rt,n,_=self.build(audible=audible,room=room)
                result=rt.offer_contingent_world_notice(self.offer(rt))
                self.assertEqual(result['status'],'ADMITTED_SOURCEFREE_NOTICE_ONLY')
                self.assertEqual(self.signs(rt,n),[])

    def test_stale_occurrence_not_persistent_sound_or_backdated_exposure(self):
        rt,n,_=self.build()
        rt.offer_contingent_world_notice(self.offer(rt))
        self.assertEqual(len(self.signs(rt,n)),1)
        n.contribute('later','WAIT')
        self.assertEqual(self.signs(rt,n),[])
        self.assertTrue(rt.verify()['valid'])

    def test_generic_analyst_fixture_does_not_impersonate_contingent_owner(self):
        rt,n,_=self.build()
        rt.cue(kind='external_occurrence_sign',tags=['offered_sign'],
               location='workshop',description='ANALYST CLAIM',modality='auditory')
        self.assertEqual(self.signs(rt,n),[])
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
