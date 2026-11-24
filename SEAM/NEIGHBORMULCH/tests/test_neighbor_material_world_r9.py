"""R9: actual CO manufactured/repaired material artifact -> existing MII.

Research-forced CO actions exercise material settlement, not independently
chosen motive or native psychology. No manufactured object prose fixture.
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
from um_sorok_organism.types import adult, blank_world, GRADE
from neighbor_runtime import NeighborEncounter
import mii


class MaterialWorldR9(unittest.TestCase):
    def build(self, *, light='lit', sightline='unobstructed',
              legibility='readable', visitor_room='home', extras=None):
        self.tmp=tempfile.TemporaryDirectory(prefix='neighbor_material_r9_')
        self.addCleanup(self.tmp.cleanup)
        self.db=str(Path(self.tmp.name)/'world.sqlite')
        self.sidecar=Path(self.tmp.name)/'profile.json'
        self.rt=ConstitutiveRuntime(self.db)
        self.addCleanup(lambda:self.rt.close())
        world=blank_world(self.rt.world_id)
        if extras:
            world['material_objects'].update(extras)
        # Production does not confer ownership: the workshop's independently
        # configured steward controls materials while granting use to maker.
        world['sites']['workshop']['material_use_grants']=['worker']
        self.rt.ledger.initialize(world,[adult('worker','Mara','workshop')])
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{
                room:{'light':light,'sightline':sightline,
                      'legibility':legibility,
                      'hearing':True,'sound_path':'audible'}
                for room in ('workshop','home')},
            'actor_conditions':{'worker':{
                'facing':'entrance','hearing':True,'visual':True,
                'light':'lit','sightline':'unobstructed','sound_path':'audible'}},
        },request_id='geometry')
        self.n.contribute('arrive','MOVE',destination=visitor_room)
        self.profile=self.n.new_private_profile()

    def view(self, **kw):
        before=deepcopy(self.rt.ledger.world('w1'))
        actors=deepcopy(self.rt.ledger.actors())
        out=self.n.private_surface(self.profile,**kw)
        self.assertEqual(self.rt.ledger.world('w1'),before)
        self.assertEqual(self.rt.ledger.actors(),actors)
        return out

    def make(self):
        result=self.rt.step('worker',requested_action='MAKE_OBJECT')
        self.assertEqual(result['status'],'PERFORMED')
        world=self.rt.ledger.world('w1')[1]
        ref=world['public_history'][-1]['worked_material_object_ref']
        obj=world['material_objects'][ref]
        self.assertEqual(obj['maker'],'worker')
        self.assertEqual(obj['owner'],'workshop_steward')
        self.assertNotIn('public_glance',obj)
        self.assertEqual(obj['condition'],.56)
        self.assertTrue(self.rt.verify()['valid'])
        return ref

    def look(self, ref, request_id):
        result=self.n.contribute(request_id,'LOOK',target_object_ref=ref)
        self.assertEqual(result['status'],'PERFORMED')
        return self.view(command='look',target=ref)

    def test_actual_labor_creates_visible_object_without_fixture_prose(self):
        self.build(visitor_room='workshop')
        self.assertIsNone(self.view()['optional'])
        ref=self.make()
        glance=self.view()
        self.assertEqual(glance['optional']['target'],ref)
        self.assertEqual(glance['optional']['text'],'A worked material object is here.')
        close=self.look(ref,'inspect')
        self.assertEqual(close['optional']['text'],'It appears worn.')
        self.assertNotIn('workshop_steward',str(close))
        self.assertNotIn('objective_labor_history',str(close))
        self.assertNotIn('condition',str(close['optional']))
        self.assertEqual(close['recognition'],{})

    def test_actual_repair_changes_same_object_close_surface_not_its_provenance(self):
        self.build(visitor_room='workshop')
        ref=self.make()
        old=self.look(ref,'first')
        repair=self.rt.step('worker',requested_action='REPAIR',object_ref=ref)
        self.assertEqual(repair['status'],'PERFORMED')
        obj=self.rt.ledger.world('w1')[1]['material_objects'][ref]
        self.assertEqual(obj['condition'],.8)
        self.assertEqual(obj['owner'],'workshop_steward')
        self.assertEqual(self.view(command='look',target=ref)['optional']['text'],
                         'A worked material object is here.')
        new=self.look(ref,'second')
        self.assertEqual(old['optional']['target'],new['optional']['target'])
        self.assertEqual(new['optional']['text'],'It appears repaired.')
        self.assertEqual(self.profile['exposures'][-2]['offered'][ref],
                         'A worked material object is here.')
        self.assertNotIn('workshop_steward',str(new))
        self.assertTrue(self.rt.verify()['valid'])

    def test_current_condition_cold_reopens_same_owner_object_without_cache(self):
        self.build(visitor_room='workshop')
        ref=self.make()
        self.n.contribute('first','LOOK',target_object_ref=ref)
        old=self.n.private_surface_stored(self.sidecar,command='look',target=ref)
        self.assertEqual(old['optional']['text'],'It appears worn.')
        self.rt.step('worker',requested_action='REPAIR',object_ref=ref)
        self.rt.close()
        self.rt=ConstitutiveRuntime(self.db)
        self.n=NeighborEncounter(self.rt,'visitor',mii_module=mii)
        self.n.contribute('second','LOOK',target_object_ref=ref)
        new=self.n.private_surface_stored(self.sidecar,command='look',target=ref)
        self.assertEqual(new['optional']['text'],'It appears repaired.')
        profile=self.n.load_private_profile(self.sidecar)
        self.assertEqual([e['offered'][ref] for e in profile['exposures']],
                         ['It appears worn.','It appears repaired.'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_other_room_blocks_outward_target_and_surface(self):
        self.build(visitor_room='home')
        ref=self.make()
        self.assertIsNone(self.view()['optional'])
        result=self.n.contribute('wrong-room','LOOK',target_object_ref=ref)
        self.assertEqual(result['status'],'BLOCKED')
        self.assertEqual(result['potential_actor_evidence'],[])

    def test_darkness_and_partial_detail_do_not_manufacture_reading(self):
        for light,sightline,legibility,expected in (
                ('dark','blocked','readable',None),
                ('lit','partial','readable','A worked material object is here.'),
                ('lit','unobstructed','unreadable','A worked material object is here.')):
            with self.subTest(light=light,sightline=sightline,legibility=legibility):
                self.build(visitor_room='workshop',light=light,sightline=sightline,
                           legibility=legibility)
                ref=self.make()
                out=self.look(ref,'physical')
                actual=out['optional']['text'] if out['optional'] else None
                self.assertEqual(actual,expected)
                self.rt.close()

    def test_hidden_and_wrong_grade_material_records_are_not_public_props(self):
        hidden={'id':'hidden','kind':'WORKED_MATERIAL_ARTIFACT','location':'workshop',
                'condition':.56,'visible':False,'grade':GRADE,
                'public_glance':'HIDDEN LEAK','public_close':'HIDDEN CLOSE'}
        unqualified={**hidden,'id':'unqualified','visible':True,
                     'grade':'UNQUALIFIED','public_glance':'GRADE LEAK'}
        self.build(visitor_room='workshop',extras={'hidden':hidden,'unqualified':unqualified})
        out=self.view()
        self.assertIsNone(out['optional'])
        for ref in ('hidden','unqualified'):
            r=self.n.contribute('look-'+ref,'LOOK',target_object_ref=ref)
            self.assertEqual(r['status'],'BLOCKED')
        self.assertNotIn('LEAK',str(self.view()))

if __name__=='__main__':
    unittest.main()
