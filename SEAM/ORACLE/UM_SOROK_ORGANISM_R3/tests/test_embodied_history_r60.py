"""Same age, distinct exercised bodily history, actual later activity.

Sourcefree functional witness. The child project is an explicit matched
fixture, not a claim about developmental motive genesis.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.types import newborn, blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.organism import conserved_motor_exercise, eligible
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService


class EmbodiedHistoricalReadiness(unittest.TestCase):
    def make(self,db,stage):
        def model(task,packet):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='actor_attempt':
                names={x['action'] for x in packet['options']}
                if stage['phase']=='exercise':
                    action=stage['exercise']
                elif stage['phase']=='later':
                    action='SING' if 'SING' in names else 'WAIT'
                else:action='WAIT'
                self.assertIn(action,names)
                return {'task':task,'action':action}
            raise AssertionError(task)
        return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(model)))

    def initialize(self,rt):
        child=newborn('nadia','Nadia')
        child['projects']=[{'id':'movement','object':'explore movement and sound',
                            'means':['PRACTICE','SING'],'status':'active','priority':.5}]
        w=blank_world()
        rt.ledger.initialize(w,[child])

    def arm(self,db,practiced):
        stage={'phase':'quiet','exercise':'PRACTICE' if practiced else 'WAIT'}
        rt=self.make(db,stage)
        try:
            self.initialize(rt)
            rt.background(100)
            self.assertFalse(eligible(rt.snapshot('nadia')['body'],'SING')[0])
            stage['phase']='exercise'
            actual=rt.step('nadia')
            self.assertEqual(actual['attempt'],stage['exercise'])
            self.assertEqual(actual['status'],'PERFORMED')
            rt.background(30)
            a=rt.snapshot('nadia')
            self.assertEqual(a['age_days'],130)
            self.assertEqual(conserved_motor_exercise(rt.ledger.actor('nadia')[1]),.008 if practiced else 0)
            self.assertEqual(a['vocal_coordination_practices'],[])
            self.assertEqual(a['body']['language'],0)
            self.assertEqual(a['memories'],[])
            self.assertEqual(a['practice_exposures'],[])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=self.make(db,stage)
        try:
            self.assertEqual(cold.snapshot('nadia'),a)
            stage['phase']='later'
            names={x['action'] for x in cold.situated('nadia')['candidate_actions']}
            self.assertEqual('SING' in names,practiced)
            result=cold.step('nadia')
            self.assertEqual(result['attempt'],'SING' if practiced else 'WAIT')
            self.assertEqual(result['status'],'PERFORMED')
            self.assertTrue(cold.verify()['valid'])
            return a['body']['motor']
        finally:cold.close()

    def test_same_elapsed_age_distinct_actual_exercise_then_independent_action(self):
        with tempfile.TemporaryDirectory() as d:
            exercised=self.arm(Path(d)/'exercise.sqlite',True)
            comparison=self.arm(Path(d)/'wait.sqlite',False)
            self.assertAlmostEqual(exercised-comparison,.008,places=5)

    def test_future_maturation_cannot_retroactively_qualify_ordinary_practice(self):
        stage={'phase':'quiet'}
        with tempfile.TemporaryDirectory() as d:
            rt=self.make(Path(d)/'period.sqlite',stage)
            try:
                self.initialize(rt)
                source=rt.register_historical_routine_source({
                    'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
                    'start_clock':0,'end_clock':200,'max_hours_per_active_day':1,
                    'description':'bounded hypothetical vocal practice'})
                process={'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
                    'source_ref':source['source_ref'],'hours_per_active_day':1,
                    'provisional_exposure_fraction':1.,'operation':'SING',
                    'mode':'SOLO_COMPONENT_PRACTICE'}
                first=rt.background(160,processes=[process])['period']
                self.assertEqual(first['bodily_withheld_processes'][0]['entry_body_reason'],'MOTOR_CAPABILITY')
                self.assertEqual(first['processes'],[])
                self.assertEqual(first['qualified_aggregate_practice_refs'],[])
                self.assertEqual(rt.snapshot('nadia')['practice_exposures'],[])
                self.assertEqual(rt.snapshot('nadia')['power_exercises'],[])
                self.assertEqual(rt.snapshot('nadia')['age_days'],160)
                self.assertTrue(eligible(rt.snapshot('nadia')['body'],'SING')[0])
                second=rt.background(10,processes=[process])['period']
                self.assertNotIn('bodily_withheld_processes',second)
                self.assertEqual(len(second['qualified_aggregate_practice_refs']),1)
                self.assertEqual(len(rt.snapshot('nadia')['practice_exposures']),1)
                self.assertEqual(rt.snapshot('nadia')['power_exercises'],[])
                self.assertEqual(rt.snapshot('nadia')['memories'],[])
                self.assertEqual(rt.snapshot('nadia')['body']['language'],0)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
