"""R12: committed departure -> CO-owned life -> actual changed encounter.

Paired controls use the same initial produced/repaired artifact and visitor
exposure. No user-selected offscreen action or reconstructed private diary.
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
from neighbor_runtime import NeighborEncounter, EncounterRefusal
import mii


class AbsenceReturnR12(unittest.TestCase):
    def build(self, name):
        tmp=tempfile.TemporaryDirectory(prefix='neighbor_absence_r12_')
        self.addCleanup(tmp.cleanup)
        db=str(Path(tmp.name)/'world.sqlite')
        profile=Path(tmp.name)/'profile.json'
        rt=ConstitutiveRuntime(db,world_id=name)
        self.addCleanup(rt.close)
        world=blank_world(name)
        world['sites']['workshop']['material_use_grants']=['worker']
        rt.ledger.initialize(world,[adult('worker','Mara','workshop')])
        n=NeighborEncounter(rt,'visitor',mii_module=mii)
        n.install_sourcefree_conditions({
            'grade':'SOURCEFREE_TEST_ONLY',
            'user_conditions':{loc:{'light':'lit','sightline':'unobstructed',
                 'hearing':True,'sound_path':'audible','legibility':'readable'}
                 for loc in ('workshop','home')},
            'actor_conditions':{'worker':{'facing':'entrance','visual':True,
                 'light':'lit','sightline':'unobstructed','hearing':True,
                 'sound_path':'audible'}},
        },request_id='geometry')
        n.contribute('arrival','MOVE',destination='workshop')
        made=rt.step('worker',requested_action='MAKE_OBJECT')
        self.assertEqual(made['status'],'PERFORMED')
        ref=rt.ledger.world(name)[1]['public_history'][-1]['worked_material_object_ref']
        fixed=rt.step('worker',requested_action='REPAIR',object_ref=ref)
        self.assertEqual(fixed['status'],'PERFORMED')
        n.contribute('first-look','LOOK',target_object_ref=ref)
        before=n.private_surface_stored(profile,command='look',target=ref)
        self.assertEqual(before['optional']['text'],'It appears repaired.')
        dep=n.contribute('depart','LEAVE')
        return rt,n,db,profile,ref,dep['event_ref']

    def return_and_look(self, rt,n,profile,ref):
        arrival=n.contribute('return','MOVE',destination='workshop')
        self.assertEqual(arrival['status'],'PERFORMED')
        view=n.private_surface_stored(profile)
        self.assertEqual(view['return_context']['arrival_event_ref'],arrival['event_ref'])
        self.assertTrue(view['return_context']['intervening_life_not_disclosed'])
        self.assertNotIn('historical_periods',str(view))
        self.assertNotIn('private_actor',str(view))
        n.contribute('second-look','LOOK',target_object_ref=ref)
        return view,n.private_surface_stored(profile,command='look',target=ref)

    def test_actual_absent_life_changes_later_material_encounter_vs_immediate_return(self):
        a,na,db,pa,oa,da=self.build('elapsed')
        b,nb,_,pb,ob,dbref=self.build('immediate')
        start=a.ledger.world('elapsed')[1]['clock']
        self.assertEqual(start,b.ledger.world('immediate')[1]['clock'])
        original=deepcopy(a.ledger.world('elapsed')[1]['material_objects'][oa])
        body_before=a.ledger.actor('worker')[1]
        prior_ids=[e['id'] for e in a.ledger.events()]
        with self.assertRaisesRegex(EncounterRefusal,'USER_NOT_PRESENT'):
            na.private_surface_stored(pa)
        # Force a segmented continuation with an actual expiring world sign.
        a.cue(kind='ordinary_noise',location='workshop',modality='auditory')
        target=start+350
        first=na.continue_absent_life_until(da,target,max_segments=1)
        self.assertEqual(first['status'],'HELD_AT_BOUNDED_ABSENCE_CONTINUATION')
        self.assertLess(first['actual_modeled_clock'],target)
        # Cold resume on the absolute cut: no elapsed interval is repeated.
        a.close()
        a=ConstitutiveRuntime(db,world_id='elapsed')
        self.addCleanup(a.close)
        na=NeighborEncounter(a,'visitor',mii_module=mii)
        final=na.continue_absent_life_until(da,target)
        self.assertEqual(final['actual_modeled_clock'],target)
        count=len(a.ledger.events())
        retry=na.continue_absent_life_until(da,target)
        self.assertFalse(retry['new_world_events'])
        self.assertEqual(len(a.ledger.events()),count)
        events=a.ledger.events()
        self.assertEqual([e['id'] for e in events[:len(prior_ids)]],prior_ids)
        intervening=events[len(prior_ids):]
        self.assertTrue(any(e['kind']=='COMPRESSED_ORDINARY_LIFE' for e in intervening))
        activity=[e for e in intervening if e['kind']=='ACTOR_LIFE_TRANSITION']
        self.assertTrue(activity)
        self.assertTrue(all(e['envelope']['payload']['actor_selection_grade'] !=
                            'INJECTED_NOT_NATIVE_ACTOR_CHOICE' for e in activity))
        later=a.ledger.actor('worker')[1]
        self.assertGreater(later['age_days'],body_before['age_days'])
        obj=a.ledger.world('elapsed')[1]['material_objects'][oa]
        self.assertEqual(obj['owner'],original['owner'])
        self.assertEqual(obj['maker'],original['maker'])
        self.assertTrue(obj.get('objective_condition_history'))
        self.assertLess(obj['condition'],.65)
        va,close_a=self.return_and_look(a,na,pa,oa)
        vb,close_b=self.return_and_look(b,nb,pb,ob)
        self.assertGreater(va['return_context']['modeled_clock_difference'],
                           vb['return_context']['modeled_clock_difference'])
        self.assertEqual(close_a['optional']['target'],oa)
        self.assertEqual(close_a['optional']['text'],'It appears worn.')
        self.assertEqual(close_b['optional']['text'],'It appears repaired.')
        saved=na.load_private_profile(pa)
        self.assertEqual(saved['exposures'][0]['offered'][oa],'It appears repaired.')
        self.assertEqual(saved['exposures'][-1]['offered'][oa],'It appears worn.')
        self.assertTrue(a.verify()['valid'] and b.verify()['valid'])

    def test_departure_identity_and_shared_presence_bound_absence_not_user_action(self):
        rt,n,_,_,_,dep=self.build('guards')
        start=rt.ledger.world('guards')[1]['clock']
        before=len(rt.ledger.events())
        for ref,cut,reason in (
                ('forged',start+5,'NO_CURRENT_QUALIFIED_DEPARTURE'),
                (dep,start-1,'ABSENCE_TARGET_PRECEDES_DEPARTURE'),
                (dep,True,'INVALID_ABSENCE_TARGET_CLOCK')):
            with self.subTest(reason=reason):
                with self.assertRaisesRegex(EncounterRefusal,reason):
                    n.continue_absent_life_until(ref,cut)
        self.assertEqual(len(rt.ledger.events()),before)
        # Repeating LEAVE while absent must not establish a new departure.
        repeated=n.contribute('leave-again','LEAVE')
        with self.assertRaisesRegex(EncounterRefusal,'NO_CURRENT_QUALIFIED_DEPARTURE'):
            n.continue_absent_life_until(repeated['event_ref'],start+5)
        other=NeighborEncounter(rt,'other',mii_module=mii)
        other.contribute('arrive','MOVE',destination='workshop')
        before=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'WORLD_HAS_PRESENT_VISITOR'):
            n.continue_absent_life_until(dep,start+5)
        self.assertEqual(len(rt.ledger.events()),before)
        other.contribute('depart','LEAVE')
        n.contribute('return','MOVE',destination='workshop')
        before=len(rt.ledger.events())
        with self.assertRaisesRegex(EncounterRefusal,'NO_CURRENT_QUALIFIED_DEPARTURE'):
            n.continue_absent_life_until(dep,start+10)
        self.assertEqual(len(rt.ledger.events()),before)
        self.assertTrue(rt.verify()['valid'])


if __name__=='__main__':
    unittest.main()
