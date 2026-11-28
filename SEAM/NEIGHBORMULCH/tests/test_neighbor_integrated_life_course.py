"""Whole candidate organism: actual family genesis, mixed life and finite encounter."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
import test_neighbor_material_support_r17 as inherited
from constitutive_life_campaign import run_integrated_life_course
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,blank_world
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService

class IntegratedLifeCourse(unittest.TestCase):
    def test_same_actual_life_after_bounded_cold_resume(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            a=run_integrated_life_course(root/'cold.sqlite',resume=True,acquire=True)
            b=run_integrated_life_course(root/'direct.sqlite',resume=False,acquire=True)
            self.assertEqual(a['state_digest'],b['state_digest'])
            self.assertEqual(a['child_address_operation'],'SIGNAL')
            self.assertEqual(a['child_address_status'],'PARTIAL')
            self.assertGreater(a['age_after_absence'],a['previsit']['age'])
            self.assertGreaterEqual(a['previsit']['detailed_beats'],12)
            self.assertEqual(a['present_beats'],6)
            self.assertEqual(a['constructor_calls'],['mother','father'])
            null=run_integrated_life_course(root/'null.sqlite',resume=True,acquire=False)
            self.assertEqual(null['child_address_operation'],'ORIENT')
            self.assertEqual(null['constructor_calls'],['mother','father'])
            self.assertNotEqual(a['state_digest'],null['state_digest'])
            print('INTEGRATED_LIFE_RECEIPT', {k:a[k] for k in (
                'clock','events','previsit','age_after_absence','child_address_operation',
                'present_beats','absence_beats','constructor_calls')})

    def test_explicit_routine_withheld_when_actual_location_changes_and_requalified(self):
        def policy(task,p):
            if task=='actor_attempt':return {'task':task,'action':'WAIT'}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            raise AssertionError(task)
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'conditional.sqlite'),
                semantic=ValidatingSemanticService(CallbackLLMProvider(policy)))
            try:
                a=adult('a','A');b=adult('b','B')
                a['projects']=[{'id':'care','object':'care for B','means':['CARE'],
                                'addressed_party_ref':'b','priority':.6,'status':'active'}]
                rt.ledger.initialize(blank_world(),[a,b])
                src=rt.register_historical_routine_source({
                    'kind':'QUALIFIED_REPRODUCTIVE_CARE','actor':'a','location':'home',
                    'start_clock':2,'end_clock':12,'max_hours_per_active_day':2,
                    'description':'Conditional fictional care arrangement'})
                p={'kind':'QUALIFIED_REPRODUCTIVE_CARE','actor':'a','location':'home',
                    'recipient':'b','source_ref':src['source_ref'],
                    'hours_per_active_day':1.,'provisional_exposure_fraction':.5}
                # Explicit location fixture action, not credited as native choice.
                self.assertEqual(rt.step('a',requested_action='MOVE',object_ref='workshop')['status'],'PERFORMED')
                before=deepcopy(rt.ledger.world())
                with self.assertRaisesRegex(ValueError,'HISTORICAL_PROCESS_UNREGISTERED_SOURCE_ENVELOPE'):
                    rt.continue_mixed_history(6,period_processes=[{**p,'source_ref':'forged'}])
                self.assertEqual(rt.ledger.world(),before)
                out=rt.continue_mixed_history(6,ordinary_span=20,detail_beats=3,period_processes=[p])
                self.assertEqual(out['status'],'MODELED_HISTORY_CUT_REACHED')
                w=rt.ledger.world()[1]
                held=[x for period in w['historical_periods'] for x in period.get('situationally_withheld_processes',[])]
                self.assertTrue(held)
                self.assertTrue(all(x['reason']=='ACTOR_ELSEWHERE' for x in held))
                self.assertFalse(w['social_reproductive_labor'])
                self.assertEqual(rt.step('a',requested_action='MOVE',object_ref='home')['status'],'PERFORMED')
                out=rt.continue_mixed_history(15,ordinary_span=20,detail_beats=3,period_processes=[p])
                self.assertEqual(out['status'],'MODELED_HISTORY_CUT_REACHED')
                w=rt.ledger.world()[1]
                self.assertTrue(w['social_reproductive_labor'])
                for period in w['historical_periods']:
                    if period['processes']:
                        self.assertGreaterEqual(period['start'],2)
                        self.assertLessEqual(period['end'],12)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

if __name__=='__main__':unittest.main()
