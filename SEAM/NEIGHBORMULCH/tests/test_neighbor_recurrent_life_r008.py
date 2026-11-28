"""Actor-produced ordinary-life premises, not imposed schedules or daily memories.

Sourcefree controlled semantic proposals on actual actor-selected histories.
The older child's initial project is an explicit fixture; R007 separately
executes the historical entrance and birth. No live-model/empirical claim.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from constitutive_life_campaign import CourseWire
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.organism import mature
from um_sorok_organism.semantics import ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.routine_sources import LIVED_CLASS, acquired_routine_processes
from neighbor_runtime import NeighborEncounter
import mii

class RecurrentLife(unittest.TestCase):
    def setup_course(self,db,adopt=True):
        phase={'op':'WAIT','forge':False,'adopt':adopt,'offers':[]}
        def policy(task,p):
            if task=='expression':
                self.assertNotIn('routine_exercise_analytic_only',str(p.get('actor_accessible',{})))
                return {'task':task,'surface':'Ordinary life continues.'}
            if task=='development':
                offers=p.get('historically_possible_recurrent_routines',[])
                if offers:
                    phase['offers'].extend(deepcopy(offers))
                if offers and phase['adopt']:
                    basis=deepcopy(offers[0]['basis'])
                    if phase['forge']:basis['exercises'][0]['event_ref']='forged'
                    candidate={'kind':'ACQUIRE_RECURRENT_ROUTINE','basis':basis,
                        'window_days':60,'hours_per_active_day':2.,
                        'provisional_exposure_fraction':.75}
                    if basis['operation']=='FEED':candidate['food_units_per_active_day']=1.
                    return {'task':task,'candidates':[candidate]}
                return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if p.get('requesting_actor'):return {'task':task,'action':'REFUSE'}
                op=phase['op']
                rows=[x for x in p.get('practical_options',[]) if x['operation']==op
                      and x.get('project_id') in ('care','wage','practice','meal')]
                if rows and op not in ('REST','WAIT'):
                    return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':op}
            raise AssertionError(task)
        wire=CourseWire('E',policy);service=ValidatingSemanticService(wire)
        rt=ConstitutiveRuntime(str(db),semantic=service)
        mother=adult('mother','Mother')
        father=adult('father','Father','workshop')
        child=newborn('nadia','Nadia');mature(child,365)
        child['body']['nutrition']=.35
        child['body']['comfort']=.15
        mother['projects']=[
            {'id':'care','object':'care for Nadia','means':['CARE','FEED'],
             'addressed_party_ref':'nadia','priority':.7,'status':'active'},
            {'id':'meal','object':'eat own meal','means':['EAT'],
             'priority':.5,'status':'active'}]
        father['projects']=[{'id':'wage','object':'subsistence labor','means':['WORK'],
                              'priority':.7,'status':'active'}]
        child['projects']=[{'id':'practice','object':'practice own embodied movements',
                            'means':['PRACTICE'],'priority':.7,'status':'active'}]
        w=blank_world();w['sites']['home']['food']=12
        rt.ledger.initialize(w,[mother,father,child])
        return rt,phase,service,wire

    def beat(self,rt,phase,aid,op):
        phase['op']=op
        result=rt.step(aid)
        self.assertNotEqual(result['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
        self.assertEqual(result['attempt'],op)
        self.assertEqual(result['status'],'PERFORMED')
        return result

    def course(self,db,adopt):
        rt,phase,service,wire=self.setup_course(db,adopt)
        def world():return rt.ledger.world()[1]
        try:
            # Same actual independently selected prior courses in both arms.
            for _ in range(3):
                self.beat(rt,phase,'mother','CARE')
                self.beat(rt,phase,'mother','REST')
                self.beat(rt,phase,'father','WORK')
                self.beat(rt,phase,'father','REST')
                self.beat(rt,phase,'nadia','PRACTICE')
                self.beat(rt,phase,'nadia','REST')
            for _ in range(3):
                self.beat(rt,phase,'mother','FEED')
                self.beat(rt,phase,'mother','REST')
            self.assertEqual({x['basis']['operation'] for x in phase['offers']},
                             {'CARE','WORK','PRACTICE','FEED'})
            registry=world()['routine_source_registry']
            self.assertEqual(len(registry),4 if adopt else 0)
            for src in registry.values():
                self.assertEqual(src['evidence_class'],LIVED_CLASS)
                self.assertEqual(len(set(src['basis_event_refs'])),3)
                self.assertEqual(src['registered_at_world_clock'],src['from_clock'])
                self.assertTrue(src['not_observed_daily_events'])
            self.assertEqual(len(world()['material_feeding_events']),3)
            self.assertEqual(world()['sites']['home']['food'],9)
            prior=deepcopy(rt.ledger.actor('nadia')[1])
            prior_micro=deepcopy(world()['public_history'])
            before_wage=world()['accounts']['father']
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            n.install_sourcefree_conditions({'grade':'SOURCEFREE_TEST_ONLY',
                'user_conditions':{'home':{'light':'lit','sightline':'unobstructed',
                    'hearing':True,'sound_path':'audible','legibility':'readable'}},
                'actor_conditions':{aid:{'facing':'entrance','visual':True,'light':'lit',
                    'sightline':'unobstructed','hearing':True,'sound_path':'audible'}
                    for aid in ('mother','father','nadia')}},request_id='geometry')
            n.contribute('arrive','MOVE',destination='home')
            n.contribute('depart','LEAVE')
            human=deepcopy(world()['neighbor_user_events'])
            dep=human[-1]['event_ref'];start=world()['clock']
            cadence={'cadence_origin':start,'ordinary_span':35,'detail_beats':3}
            # No caller-supplied routine schedule: dynamic acquired source
            # windows have to be consumed by the continuing history owner.
            phase['op']='WAIT'
            part=n.continue_absent_life_until(dep,start+35,max_segments=1,
                         historical_cadence=cadence)
            self.assertTrue(part['new_world_events'])
            rt.close();rt=ConstitutiveRuntime(str(db),semantic=service)
            n=NeighborEncounter(rt,'visitor',mii_module=mii)
            after=n.continue_absent_life_until(dep,start+35,historical_cadence=cadence)
            self.assertEqual(after['status'],'AT_OR_PAST_ABSENCE_TARGET')
            self.assertEqual(world()['neighbor_user_events'],human)
            self.assertEqual(world()['public_history'][:len(prior_micro)],prior_micro)
            current=rt.ledger.actor('nadia')[1]
            self.assertEqual(current['experienced_care_events'],prior['experienced_care_events'])
            self.assertEqual(current['memories'],prior['memories'])
            self.assertEqual(current['age_days'],prior['age_days']+35)
            self.assertEqual(len(world()['material_feeding_events']),3)
            self.assertEqual(bool(world().get('reproductive_labor_periods')),adopt)
            self.assertEqual(bool(world().get('wage_labor_periods')),adopt)
            self.assertEqual(bool(world().get('material_provisioning_periods')),adopt)
            self.assertEqual(bool(current['practice_exposures']),adopt)
            if adopt:
                self.assertEqual(world()['sites']['home']['food'],0)
                self.assertGreater(world()['accounts']['father'],before_wage)
                self.assertTrue(any(x['uncovered_food_units']>0 for x in world()['material_provisioning_periods']))
                for period in world()['historical_periods']:
                    for p in period['processes']:
                        src=registry[p['source_ref']]
                        self.assertLessEqual(src['from_clock'],period['start'])
                        self.assertLessEqual(period['end'],src['through_clock'])
                self.assertTrue(all(sum(1 for x in phase['offers'] if x['basis']['operation']==op)>=1
                                    for op in ('CARE','WORK','PRACTICE','FEED')))
            else:self.assertEqual(world()['sites']['home']['food'],9)
            nutrition=current['body']['nutrition']
            # Cold return, actual new independently selected meal has a
            # material consequence caused by the admitted historical course.
            self.assertEqual(n.contribute('return','MOVE',destination='home')['status'],'PERFORMED')
            phase['op']='EAT';meal=n.independent_actor_beat('mother')
            self.assertEqual(meal['attempt'],'EAT')
            self.assertEqual(meal['status'],'BLOCKED' if adopt else 'PERFORMED')
            surface=n.private_surface(n.new_private_profile())
            self.assertNotIn('basis_event_refs',str(surface))
            self.assertNotIn('recurrent_routines',str(surface))
            self.assertNotIn('visitor',rt.ledger.actors())
            self.assertTrue(rt.verify()['valid'])
            return {'nutrition':nutrition,'meal':meal['status'],
                    'sources':len(registry),'clock':world()['clock'],
                    'periods':len(world()['historical_periods']),
                    'wages':world()['accounts']['father'],
                    'practice':len(current['practice_exposures'])}
        finally:rt.close()

    def test_actual_household_routines_form_and_change_material_later_course(self):
        with tempfile.TemporaryDirectory() as d:
            yes=self.course(Path(d)/'yes.sqlite',True)
            no=self.course(Path(d)/'no.sqlite',False)
            self.assertGreater(yes['nutrition'],no['nutrition'])
            self.assertGreater(yes['wages'],no['wages'])
            self.assertEqual(yes['clock'],no['clock'])
            self.assertEqual((yes['meal'],no['meal']),('BLOCKED','PERFORMED'))
            print('R008_RECURRENT_HOUSEHOLD',yes,no)

    def test_forged_history_and_process_are_atomic_and_location_requalifies(self):
        with tempfile.TemporaryDirectory() as d:
            rt,phase,service,_=self.setup_course(Path(d)/'atomic.sqlite')
            try:
                for _ in range(2):
                    self.beat(rt,phase,'mother','CARE')
                    self.beat(rt,phase,'mother','REST')
                w=deepcopy(rt.ledger.world());actors=deepcopy(rt.ledger.actors())
                count=rt.verify()['events']
                phase['forge']=True;phase['op']='CARE'
                with self.assertRaisesRegex(InvalidDevelopment,'LIVED_ROUTINE_UNQUALIFIED_BASIS'):
                    rt.step('mother')
                self.assertEqual(rt.ledger.world(),w)
                self.assertEqual(rt.ledger.actors(),actors)
                self.assertEqual(rt.verify()['events'],count)
                phase['forge']=False;self.beat(rt,phase,'mother','CARE')
                world=rt.ledger.world()[1];p=acquired_routine_processes(world)[0]
                version=deepcopy(rt.ledger.world())
                with self.assertRaisesRegex(ValueError,'LIVED_ROUTINE_SOURCE_PROCESS_MISMATCH'):
                    rt.continue_mixed_history(world['clock']+5,
                        period_processes=[{**p,'hours_per_active_day':1.}])
                self.assertEqual(rt.ledger.world(),version)
                self.assertEqual(rt.step('mother',requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
                start=rt.ledger.world()[1]['clock'];phase['op']='WAIT'
                rt.continue_mixed_history(start+4,cadence_origin=start,ordinary_span=30)
                world=rt.ledger.world()[1]
                self.assertFalse(world.get('reproductive_labor_periods',[]))
                self.assertTrue(any(x['reason']=='ACTOR_ELSEWHERE' for period in world['historical_periods']
                                    for x in period.get('situationally_withheld_processes',[])))
                self.assertEqual(rt.step('mother',requested_action='MOVE',object_ref='home')['status'],'PERFORMED')
                start=rt.ledger.world()[1]['clock']
                rt.continue_mixed_history(start+4,cadence_origin=start,ordinary_span=30)
                self.assertTrue(rt.ledger.world()[1].get('reproductive_labor_periods'))
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

if __name__=='__main__':unittest.main()
