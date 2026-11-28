"""Actual work and purchase can become means of another's material care."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from test_labor_dependency_r19 import employment_spec

class ProvisioningPurpose(unittest.TestCase):
    def arm(self,db,adopt,forge=False):
        stage={'name':'feed'}
        offered=[]
        def cb(task,p):
            if task=='expression':return {'task':task,'surface':'Ordinary activity.'}
            if task=='actor_attempt':
                op='FEED' if stage['name']=='feed' else 'WORK'
                rows=[x for x in p['practical_options'] if x.get('project_id')=='care'
                      and x['operation']==op]
                if rows:return {'task':task,'practical_option_id':rows[0]['option_id']}
                return {'task':task,'action':'WAIT'}
            if task=='development':
                q=p.get('historically_possible_provisioning_reorganizations',[])
                if p['actor']['id']=='mother' and q:
                    offered.extend(deepcopy(q))
                    if adopt:
                        v=deepcopy(q[0])
                        if forge:v['provisioning_means_basis']['work_event_ref']='foreign'
                        return {'task':task,'candidates':[v]}
                return {'task':task,'candidates':[]}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            mother=adult('mother','Mother')
            mother['projects']=[{'id':'care','object':'provide food for Nadia','means':['FEED'],
                'status':'active','priority':.6,'addressed_party_ref':'nadia'}]
            world=blank_world();world['sites']['workshop']['food_price']=.25
            world['accounts']['mother']=0
            rt.ledger.initialize(world,[mother,adult('father','Father'),newborn('nadia','Nadia')])
            spec=rt.register_sourcefree_work_regime(employment_spec())
            rt.step('mother',requested_action='MOVE',object_ref='workshop')
            rt.step('mother',requested_action='INSPECT',object_ref=spec['terms_notice_ref'])
            rt.step('mother',requested_action='ACCEPT_WORK_TERMS')
            rt.step('mother',requested_action='REST')
            self.assertEqual(rt.step('mother',requested_action='WORK')['status'],'PERFORMED')
            self.assertEqual(rt.ledger.world()[1]['accounts']['mother'],.25)
            self.assertEqual(rt.step('mother',requested_action='BUY_FOOD')['status'],'PERFORMED')
            self.assertEqual(rt.ledger.world()[1]['accounts']['mother'],0)
            rt.step('mother',requested_action='MOVE',object_ref='home')
            rt.step('mother',requested_action='REST')
            before=deepcopy(rt.ledger.world()); child=deepcopy(rt.snapshot('nadia'))
            m=deepcopy(rt.snapshot('mother'))
            if forge:
                with self.assertRaises(InvalidDevelopment):rt.step('mother')
                self.assertEqual(rt.ledger.world(),before)
                self.assertEqual(rt.snapshot('nadia'),child)
                self.assertEqual(rt.snapshot('mother'),m)
                return
            self.assertEqual(rt.step('mother')['status'],'PERFORMED')
            self.assertEqual(len(offered),1)
            after=rt.snapshot('nadia')
            self.assertGreater(after['body']['nutrition'],child['body']['nutrition'])
            self.assertFalse(any(x.get('own_provisioning_receipt_analytic_only') for x in after['evidence_paths']))
            self.assertEqual(rt.ledger.world()[1]['material_feeding_events'][-1]['food_source'],'GIVER_HELD_FOOD')
            project=rt.snapshot('mother')['projects'][0]
            self.assertEqual(project['means'],['FEED','WORK','BUY_FOOD'] if adopt else ['FEED'])
            self.assertEqual(project['object'],'provide food for Nadia')
            self.assertTrue(rt.verify()['valid'])
            rt.step('mother',requested_action='MOVE',object_ref='workshop')
            rt.step('mother',requested_action='REST')
        finally:rt.close()
        cold=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            stage['name']='work'
            result=cold.step('mother')
            self.assertEqual(result['attempt'],'WORK' if adopt else 'WAIT')
            if adopt:self.assertEqual(result['status'],'PERFORMED')
            self.assertTrue(cold.verify()['valid'])
        finally:cold.close()
    def test_reproductive_activity_acquires_wage_and_purchase_as_means(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'adopt.sqlite',True)
            self.arm(Path(d)/'abstain.sqlite',False)
    def test_forged_work_source_rejects_whole_feeding_event(self):
        with tempfile.TemporaryDirectory() as d:
            self.arm(Path(d)/'forge.sqlite',True,True)
