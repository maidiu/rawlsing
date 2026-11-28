"""R008: detailed and compressed preproject child activity, one causal life.
Sourcefree controlled exercise; no measured childhood learning law.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import newborn, blank_world
from um_sorok_organism.organism import eligible, conserved_motor_exercise
from um_sorok_organism.mediated_efficacy import preproject_motor_readiness
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService


class EarlyOrdinaryPractice(unittest.TestCase):
    def runtime(self, db, stage):
        def model(task, packet):
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='actor_attempt':
                names={x['action'] for x in packet['options']}
                action=stage['action']
                if action=='LATER':action='SING' if 'SING' in names else 'WAIT'
                self.assertIn(action,names)
                return {'task':task,'action':action}
            raise AssertionError(task)
        return ConstitutiveRuntime(str(db),semantic=ValidatingSemanticService(CallbackLLMProvider(model)))

    def child(self, rt):
        return rt.ledger.actor('nadia')[1]

    def source(self, rt, operation, ref, days):
        w=rt.ledger.world()[1]
        source=rt.register_historical_routine_source({
            'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
            'start_clock':w['clock'],'end_clock':w['clock']+days,
            'max_hours_per_active_day':1,'description':'bounded ordinary bodily exploration',
            'operation':operation,'preproject_exercise_ref':ref})
        return {'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'nadia','location':'home',
                'source_ref':source['source_ref'],'hours_per_active_day':1,
                'provisional_exposure_fraction':1.,'operation':operation,
                'mode':'SOLO_COMPONENT_PRACTICE','preproject_exercise_ref':ref}

    def anchor(self, rt, operation):
        rows=[r for r in self.child(rt)['power_exercises']
              if r['operation']==operation and r.get('actor_selected_preproject_exercise')]
        self.assertEqual(len(rows),1)
        return rows[0]['id']

    def arm(self, db, aggregate, split=False):
        stage={'action':'SIGNAL'}
        rt=self.runtime(db,stage)
        try:
            rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia')])
            self.assertEqual(rt.step('nadia')['attempt'],'SIGNAL')
            signal_ref=self.anchor(rt,'SIGNAL')
            proc=self.source(rt,'SIGNAL',signal_ref,100)
            before=rt.verify()['events']
            prior=self.child(rt)
            for wrong,code in [
                (dict(proc,operation='PRACTICE'),'PREPROJECT_ROUTINE_SOURCE_SCOPE_MISMATCH'),
                (dict(proc,preproject_exercise_ref='forged'),'PREPROJECT_ROUTINE_SOURCE_SCOPE_MISMATCH')]:
                with self.assertRaisesRegex(ValueError,code):rt.background(10,[wrong])
                self.assertEqual(rt.verify()['events'],before)
                self.assertEqual(self.child(rt),prior)
            period=rt.background(100-self.child(rt)['age_days'],[proc])['period']
            self.assertEqual(len(period['qualified_aggregate_practice_refs']),1)
            self.assertEqual(len(period['preproject_practice_loads']),1)
            self.assertEqual(self.child(rt)['projects'],[])
            self.assertEqual(self.child(rt)['forms'],{})
            options=rt.situated('nadia')['candidate_actions']
            practice=next(o for o in options if o['action']=='PRACTICE')
            self.assertIn('RUDIMENTARY_EXPLORATORY_OPPORTUNITY_NOT_ACQUIRED_MEANS',
                          practice['historical_support_statuses'])
            self.assertEqual(practice['practical_aggregate_sources'],
                             period['qualified_aggregate_practice_refs'])
            stage['action']='PRACTICE'
            self.assertEqual(rt.step('nadia')['status'],'PERFORMED')
            practice_ref=self.anchor(rt,'PRACTICE')
            self.assertEqual(conserved_motor_exercise(self.child(rt)),.008)
            span=125-self.child(rt)['age_days']
            proc=self.source(rt,'PRACTICE',practice_ref,span)
            before=rt.verify()['events']
            with self.assertRaisesRegex(ValueError,'PREPROJECT_ROUTINE_DUPLICATE_COMPONENT_WINDOW'):
                rt.background(1,[proc,proc])
            self.assertEqual(rt.verify()['events'],before)
            if split:
                rt.background(10,[proc] if aggregate else [])
                rt.background(span-10,[proc] if aggregate else [])
            else:rt.background(span,[proc] if aggregate else [])
            child=self.child(rt)
            self.assertEqual(child['age_days'],125)
            self.assertEqual(child['projects'],[])
            self.assertEqual(child['forms'],{})
            self.assertEqual(child['memories'],[])
            self.assertEqual(child['body']['language'],0)
            self.assertEqual(conserved_motor_exercise(child),.008)
            self.assertEqual(preproject_motor_readiness(child)>0,aggregate)
            self.assertEqual(eligible(child['body'],'SING')[0],aggregate)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        cold=self.runtime(db,stage)
        try:
            self.assertEqual(self.child(cold),child)
            stage['action']='LATER'
            actual=cold.step('nadia')
            self.assertEqual(actual['attempt'],'SING' if aggregate else 'WAIT')
            self.assertEqual(actual['status'],'PERFORMED')
            self.assertTrue(cold.verify()['valid'])
            return child
        finally:cold.close()

    def test_matched_life_and_partitioned_dose(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            whole=self.arm(p/'whole.db',True)
            split=self.arm(p/'split.db',True,True)
            absent=self.arm(p/'absent.db',False)
            self.assertEqual(preproject_motor_readiness(whole),preproject_motor_readiness(split))
            self.assertEqual(whole['body']['motor'],split['body']['motor'])
            self.assertGreater(whole['body']['motor'],absent['body']['motor'])
            self.assertLess(whole['body']['rest'],absent['body']['rest'])

    def test_injected_or_unlived_exercise_cannot_license_ordinary_dose(self):
        with tempfile.TemporaryDirectory() as d:
            rt=self.runtime(Path(d)/'negative.db',{'action':'WAIT'})
            try:
                rt.ledger.initialize(blank_world(),[newborn('nadia','Nadia')])
                rt.step('nadia',requested_action='SIGNAL')
                ref=self.child(rt)['power_exercises'][-1]['id']
                before=rt.verify()['events']
                for bad in (ref,'unlived'):
                    with self.assertRaisesRegex(ValueError,'PREPROJECT_SOURCE_NO_ACTUAL_OWN_EXERCISE'):
                        self.source(rt,'SIGNAL',bad,10)
                    self.assertEqual(rt.verify()['events'],before)
                self.assertEqual(self.child(rt)['practice_exposures'],[])
            finally:rt.close()
