"""Existing CO posted notice -> finite visitor MII, not institutional truth.
Initial notices are explicitly sourcefree world fixtures, not live news or a
new posting authority. CO INSPECT exercises its actual existing reader.
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

WORDS='The hall is open to everyone today.'
def posted(ref='hall-poster', **kw):
    return {'id':ref,'location':'workshop','public':True,
            'effective_from':0,'effective_until':None,
            'public_text':WORDS,'public_terms':['hall','open'],
            'private_policy_ref':'CONFIDENTIAL_RULE',
            **kw}

class PublicNoticeR10(unittest.TestCase):
    def build(self, notices=None, *, light='lit', sightline='unobstructed',
              legibility='readable', room='workshop', objects=None):
        self.tmp=tempfile.TemporaryDirectory(prefix='neighbor_notice_r10_')
        self.addCleanup(self.tmp.cleanup)
        self.db=str(Path(self.tmp.name)/'world.sqlite')
        self.sidecar=Path(self.tmp.name)/'profile.json'
        self.rt=ConstitutiveRuntime(self.db)
        self.addCleanup(lambda:self.rt.close())
        world=blank_world(self.rt.world_id)
        world['public_notices']=deepcopy([posted()] if notices is None else notices)
        world['material_objects'].update(objects or {})
        self.rt.ledger.initialize(world,[adult('worker','Mara','workshop')])
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{
                loc:{'light':light,'sightline':sightline,
                     'legibility':legibility,'hearing':True,'sound_path':'audible'}
                for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':'entrance','hearing':True,
                 'visual':True,'light':'lit','sightline':'unobstructed',
                 'sound_path':'audible'}},
        },request_id='geometry')
        self.n.contribute('arrive','MOVE',destination=room)
        self.profile=self.n.new_private_profile()

    def view(self, **kw):
        before=deepcopy(self.rt.ledger.world('w1'))
        actors=deepcopy(self.rt.ledger.actors())
        result=self.n.private_surface(self.profile,**kw)
        self.assertEqual(self.rt.ledger.world('w1'),before)
        self.assertEqual(self.rt.ledger.actors(),actors)
        return result

    def look(self, ref='hall-poster', request='read'):
        out=self.n.contribute(request,'LOOK',target_object_ref=ref)
        self.assertEqual(out['status'],'PERFORMED')
        return self.view(command='look',target=ref)

    def test_published_words_are_not_objective_rule_or_actor_knowledge(self):
        self.build()
        first=self.view()['optional']
        self.assertEqual(first['text'],'A public notice is posted here.')
        self.assertFalse(first['published_words_available'])
        self.assertNotIn(WORDS,str(first))
        # A private target selection is not a committed outward LOOK.
        self.assertEqual(self.view(command='look',target='hall-poster')['optional']['text'],
                         first['text'])
        read=self.look()['optional']
        self.assertEqual(read['text'],WORDS)
        self.assertTrue(read['published_words_available'])
        self.assertEqual(read['institutional_truth'],'NOT_ESTABLISHED')
        self.assertNotIn('CONFIDENTIAL_RULE',str(read))
        self.assertEqual(self.rt.ledger.world('w1')[1]['sites']['hall']['access'],'controlled')
        self.assertEqual(self.rt.ledger.actors()['worker'].get('notice_exposures',[]),[])
        self.assertTrue(self.rt.verify()['valid'])

    def test_actor_and_visitor_have_separate_actual_readers(self):
        self.build()
        result=self.rt.step('worker',requested_action='INSPECT',object_ref='hall-poster')
        self.assertEqual(result['status'],'PERFORMED')
        # CO produces actor-private inspection cue; visitor cannot borrow it.
        cue=self.rt.ledger.world('w1')[1]['cues'][-1]
        self.assertEqual(cue['private_to'],'worker')
        self.assertEqual(cue['description'],WORDS)
        self.assertEqual(self.view()['optional']['text'],'A public notice is posted here.')
        before=deepcopy(self.rt.ledger.actors()['worker'])
        self.assertEqual(self.look()['optional']['text'],WORDS)
        self.assertEqual(self.rt.ledger.actors()['worker'],before)

    def test_expired_future_nonpublic_and_other_room_not_readable(self):
        self.build([posted('expired',effective_until=0),
                    posted('future',effective_from=99),
                    posted('private',public=False),
                    posted('elsewhere',location='home')])
        self.assertIsNone(self.view()['optional'])
        for ref in ('expired','future','private','elsewhere'):
            result=self.n.contribute(ref,'LOOK',target_object_ref=ref)
            self.assertEqual(result['status'],'BLOCKED')
        self.assertIsNone(self.view()['optional'])

    def test_expiry_between_outward_turn_and_read_is_not_extended(self):
        self.build([posted(effective_until=2)])
        self.assertEqual(self.rt.ledger.world('w1')[1]['clock'],2)
        result=self.n.contribute('last-moment','LOOK',target_object_ref='hall-poster')
        self.assertEqual(result['status'],'PERFORMED')
        self.assertIsNone(self.view(command='look',target='hall-poster')['optional'])

    def test_visibility_and_legibility_are_distinct_from_actual_turn(self):
        for light,sightline,legibility,expected in (
                ('dark','blocked','readable',None),
                ('lit','partial','readable','A public notice is posted here.'),
                ('lit','unobstructed','unreadable','A public notice is posted here.')):
            with self.subTest(light=light,sightline=sightline,legibility=legibility):
                self.build(light=light,sightline=sightline,legibility=legibility)
                out=self.look()['optional']
                self.assertEqual(out['text'] if out else None,expected)
                if out:
                    self.assertFalse(out['published_words_available'])
                self.rt.close()

    def test_duplicate_source_identity_and_material_collision_refuse(self):
        self.build([posted('dup'),posted('dup',public_text='DIFFERENT WORDS'),
                    posted('collides')],objects={'collides':{
                         'location':'workshop','public_glance':'Object fixture'}})
        self.assertIsNone(self.view()['optional'])
        for ref in ('dup','collides'):
            self.assertEqual(self.n.contribute(ref,'LOOK',target_object_ref=ref)['status'],'BLOCKED')

    def test_cold_exposure_remains_but_expired_notice_is_not_present(self):
        self.build([posted(effective_until=3)])
        self.n.contribute('read','LOOK',target_object_ref='hall-poster')
        first=self.n.private_surface_stored(self.sidecar,command='look',target='hall-poster')
        self.assertEqual(first['optional']['text'],WORDS)
        self.n.contribute('elapsed','WAIT')
        self.rt.close()
        self.rt=ConstitutiveRuntime(self.db)
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.assertIsNone(self.n.private_surface_stored(self.sidecar)['optional'])
        profile=self.n.load_private_profile(self.sidecar)
        self.assertEqual(profile['exposures'][0]['rendered']['optional']['text'],WORDS)
        self.assertEqual(profile['exposures'][0]['rendered']['optional']['institutional_truth'],
                         'NOT_ESTABLISHED')
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':
    unittest.main()
