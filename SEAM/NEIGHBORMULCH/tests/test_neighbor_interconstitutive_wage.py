"""Coarse paid work is real money, not invented daily episodes or collective will."""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.organism import mature
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.labor_dependency import _uncommitted_paid_wage

class InterconstitutiveWage(unittest.TestCase):
    def course(self,db,reverse,initial_cash,contract_b=True):
        phase={'op':'WAIT'}
        def policy(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='actor_attempt':
                if p.get('requesting_actor'):return {'task':task,'action':'REFUSE'}
                return {'task':task,'action':phase['op']}
            raise AssertionError(task)
        service=ValidatingSemanticService(CallbackLLMProvider(policy))
        rt=ConstitutiveRuntime(str(db),semantic=service)
        w=blank_world()
        w['accounts']['workshop_steward']=initial_cash
        w['sites']['workshop']['food_price']=1.25
        w['sites']['workshop']['food']=10
        a=adult('a','A','workshop');b=adult('b','B','workshop')
        c=newborn('child','Child');mature(c,365);c['location']='workshop'
        c['body']['nutrition']=.2
        for x in (a,b):
            x['projects']=[{'id':x['id']+'-work','object':'earn a living',
                        'means':['WORK'],'priority':.7,'status':'active'}]
        a['projects'].append({'id':'care','object':'feed child','means':['CARE','FEED'],
                    'addressed_party_ref':'child','priority':.7,'status':'active'})
        rt.ledger.initialize(w,[a,b,c])
        def world():return rt.ledger.world()[1]
        def actor(aid):return rt.ledger.actor(aid)[1]
        def beat(aid,op):
            phase['op']=op
            result=rt.step(aid)
            self.assertEqual((result['attempt'],result['status']),(op,'PERFORMED'))
            self.assertNotEqual(result['selection_grade'],'INJECTED_NOT_NATIVE_ACTOR_CHOICE')
            return result
        try:
            reg=rt.register_sourcefree_work_regime({
                'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO',
                'source_ref':'declared-work-relation','site':'workshop',
                'controller':'workshop_steward','eligible_workers':['a','b'],
                'delegates':['b']})
            for aid in ('a','b'):
                self.assertEqual(rt.step(aid,requested_action='INSPECT',
                                object_ref=reg['terms_notice_ref'])['status'],'PERFORMED')
                if aid=='a' or contract_b:
                    self.assertEqual(rt.step(aid,requested_action='ACCEPT_WORK_TERMS')['status'],'PERFORMED')
            start=world()['clock']
            processes=[]
            for aid,hours in [('a',4.),('b',8.)]:
                src=rt.register_historical_routine_source({
                    'kind':'QUALIFIED_WAGE_LABOR','actor':aid,'location':'workshop',
                    'start_clock':start,'end_clock':start+8,
                    'max_hours_per_active_day':hours,'description':'Explicit ordinary work premise'})
                processes.append({'kind':'QUALIFIED_WAGE_LABOR','actor':aid,'location':'workshop',
                    'source_ref':src['source_ref'],'hours_per_active_day':hours,
                    'provisional_exposure_fraction':1.})
            if reverse:processes.reverse()
            prior=deepcopy(world()['material_claims'])
            phase['op']='WAIT'
            rt.continue_mixed_history(start+8,cadence_origin=start,ordinary_span=8,
                                      period_processes=processes)
            result=world()
            rows=result['wage_labor_periods']
            paid={aid:round(sum(x['actual_paid_model'] for x in rows if x['worker']==aid),5)
                   for aid in ('a','b')}
            due={aid:round(sum(x['wage_due_sourcefree_model'] for x in rows if x['worker']==aid),5)
                   for aid in ('a','b')}
            self.assertEqual(due,{'a':1.,'b':2. if contract_b else 0.})
            self.assertEqual(round(sum(paid.values()),5),min(sum(due.values()),initial_cash))
            self.assertEqual(result['material_claims'],prior)
            self.assertTrue(all(x['work_regime_ref']==reg['regime_ref'] for x in rows))
            self.assertEqual(result['accounts']['workshop_steward'],max(0.,initial_cash-sum(due.values())))
            self.assertEqual({aid:round(_uncommitted_paid_wage(result,
                 result['work_regimes']['workshop'],aid,'workshop'),5) for aid in ('a','b')},paid)
            # A qualified receipt cannot be duplicated or detached from its allocation.
            forged=deepcopy(result);forged['wage_labor_periods'].append(deepcopy(rows[0]))
            with self.assertRaisesRegex(ValueError,'R19_UNQUALIFIED_AGGREGATE_WAGE_PROVENANCE'):
                _uncommitted_paid_wage(forged,forged['work_regimes']['workshop'],rows[0]['worker'],'workshop')
            rt.close();rt=ConstitutiveRuntime(str(db),semantic=service)
            self.assertTrue(rt.verify()['valid'])
            if paid['b']>=.25:
                before=world()['accounts']['b']
                beat('b','CONTRIBUTE_WAGE_RELIEF')
                self.assertEqual(world()['accounts']['b'],round(before-.25,5))
                self.assertEqual(world()['accounts'][reg['relief_pool_ref']],.25)
                current=world()
                self.assertEqual(_uncommitted_paid_wage(current,current['work_regimes']['workshop'],
                                                        'b','workshop'),round(paid['b']-.25,5))
            if initial_cash>=4. and contract_b:
                self.assertEqual(rt.step('b',requested_action='SUSPEND_WAGE_WORK',
                                   target='a')['status'],'PERFORMED')
                self.assertEqual(rt.step('a',requested_action='WORK')['status'],'BLOCKED')
                self.assertEqual(rt.step('a',requested_action='BUY_FOOD')['status'],'BLOCKED')
                beat('a','DRAW_WAGE_RELIEF')
                self.assertEqual(world()['accounts'][reg['relief_pool_ref']],0.)
                self.assertEqual(rt.step('a',requested_action='BUY_FOOD')['status'],'PERFORMED')
                before_child=actor('child')['body']['nutrition']
                self.assertEqual(rt.step('a',requested_action='FEED',target='child')['status'],'PERFORMED')
                self.assertGreater(actor('child')['body']['nutrition'],before_child)
                self.assertTrue(world()['material_feeding_events'])
                self.assertFalse(actor('child')['labor_dependency_encounters'])
            self.assertTrue(rt.verify()['valid'])
            print('INTERCONSTITUTIVE_WAGE',initial_cash,reverse,contract_b,due,paid)
            return paid
        finally:rt.close()

    def test_paid_coarse_work_reenters_independent_collective_support(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.course(Path(d)/'full.sqlite',False,4.),{'a':1.,'b':2.})

    def test_simultaneous_cash_shortage_is_not_input_order_or_unpaid_income(self):
        with tempfile.TemporaryDirectory() as d:
            a=self.course(Path(d)/'first.sqlite',False,1.5)
            b=self.course(Path(d)/'second.sqlite',True,1.5)
            self.assertEqual(a,b)
            self.assertEqual(a,{'a':.5,'b':1.})

    def test_ordinary_premise_does_not_forge_worker_contract(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(self.course(Path(d)/'denied.sqlite',False,4.,False),{'a':1.,'b':0.})

if __name__=='__main__':unittest.main()
