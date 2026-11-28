"""R59: aggregate work expenditure becomes another person's conditions of life.

Explicit fictional research histories, not observed microevents or fatigue science.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult, newborn, blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.organism import eligible
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService

class ReproductiveWorkload(unittest.TestCase):
    def arm(self, db, work, cash=12.):
        stage={'run':False}
        def cb(task,p):
            if task=='actor_attempt':
                if p['actor']['id']=='mother' and stage['run']:
                    options=[o for o in p.get('practical_options',[])
                             if o['operation']=='CARE'
                             and o.get('world_request',{}).get('addressed_party_ref')=='nadia']
                    if options:return {'task':task,'practical_option_id':options[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':return {'task':task,'surface':'Ordinary life continues.'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            w=blank_world();w['accounts']['workshop_steward']=cash
            a=adult('mother','Mother');b=newborn('nadia','Nadia')
            for x in (a,b):
                x['location']='workshop'
            # Explicit matched initial bodily condition. No past events fabricated.
            a['body']['rest']=.22
            b['body']['comfort']=.3
            a['projects']=[{'id':'livelihood','object':'subsistence','means':['WORK'],
                            'status':'active','priority':.5},
                           {'id':'care','object':'care for Nadia','means':['CARE'],
                            'addressed_party_ref':'nadia','status':'active','priority':.6}]
            rt.ledger.initialize(w,[a,b])
            processes=[]
            if work:
                source=rt.register_historical_routine_source({
                    'kind':'QUALIFIED_WAGE_LABOR','actor':'mother','location':'workshop',
                    'start_clock':0,'end_clock':100,'max_hours_per_active_day':8,
                    'description':'fictional aggregate labor claim, not observed daily events'})
                processes=[{'kind':'QUALIFIED_WAGE_LABOR','actor':'mother','location':'workshop',
                    'source_ref':source['source_ref'],'hours_per_active_day':8,
                    'provisional_exposure_fraction':1.0}]
            rt.background(100,processes)
            state=rt.snapshot('mother');child=rt.snapshot('nadia')
            self.assertEqual(state['age_days'],a['age_days']+100)
            self.assertEqual(child['age_days'],100)
            self.assertEqual(state['body']['rest'],.089 if work else .185)
            self.assertEqual(eligible(state['body'],'CARE')[0],not work)
            self.assertEqual(child['memories'],[])
            self.assertEqual(child['experienced_care_events'],[])
            world=rt.ledger.world('w1')[1]
            row=None
            if work:
                row=world['wage_labor_periods'][0]
                self.assertEqual(row['modeled_labor_hours'],800)
                self.assertEqual(row['worker_rest_expenditure_model'],.096)
                self.assertEqual(row['actual_paid_model'],cash)
                self.assertEqual(row['wage_arrears'],25-cash)
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            stage['run']=True
            before=rt.snapshot('nadia')['body']['comfort']
            result=rt.step('mother')
            self.assertEqual(result['attempt'],'WAIT' if work else 'CARE')
            child=rt.snapshot('nadia')
            self.assertEqual(len(child['experienced_care_events']),0 if work else 1)
            self.assertEqual(child['memories'],[])
            if not work:self.assertGreater(child['body']['comfort'],before)
            else:
                self.assertLessEqual(child['body']['comfort'],before)
                # Actual rest, not inferred from elapsed hours, recovers the
                # capacity; no new acquired technique or changed authority.
                rt.step('mother',requested_action='REST')
                self.assertTrue(eligible(rt.snapshot('mother')['body'],'CARE')[0])
                self.assertEqual(rt.step('mother')['attempt'],'CARE')
                self.assertEqual(len(rt.snapshot('nadia')['experienced_care_events']),1)
            self.assertTrue(rt.verify()['valid'])
            return row
        finally:rt.close()

    def test_same_age_different_workload_changes_another_life(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'unmodeled.sqlite',False)
            paid=self.arm(Path(d)/'paid.sqlite',True,12.)
            unpaid=self.arm(Path(d)/'unpaid.sqlite',True,0.)
            self.assertEqual(paid['worker_rest_expenditure_model'],unpaid['worker_rest_expenditure_model'])
            self.assertNotEqual(paid['actual_paid_model'],unpaid['actual_paid_model'])

    def test_saturated_rest_cannot_be_credited_by_work(self):
        from um_sorok_organism.historical_social_reproduction import _work,_plan_wages
        a=adult('worker','Worker');w=blank_world()
        a['body']['rest']=.001
        proc={'kind':'QUALIFIED_WAGE_LABOR','actor':'worker','location':'workshop',
            'source_ref':'direct_settlement_fixture','hours_per_active_day':8,
            'provisional_exposure_fraction':1.0}
        row=_work(w,{'worker':a},proc,0,100,_plan_wages(w,[proc],0,100))
        self.assertEqual(a['body']['rest'],0.)
        self.assertEqual(row['worker_rest_expenditure_model'],.001)
