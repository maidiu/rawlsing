"""REMONT negative contracts against latest ORACLE R3, sourcefree only."""
import tempfile,unittest
from pathlib import Path
from um_sorok_organism.psychodynamics import validate_tendencies
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService


class R3DefectRegressions(unittest.TestCase):
    def test_sr_p024_unexecutable_seed_tendency_rejected_without_actor_or_world(self):
        packet={'source_ref':'sourcefree_negative','answers':{'work':'yes'},
                'fictional_seed':{'acquired_forms':[{'kind':'TENSION','content':'fake mechanics',
                'cues':['home'],'enables':[],'tendencies':[{'action':'TELEPORT','polarity':'WITHHOLD'}]}]}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'negative.sqlite'))
            try:
                with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_TENDENCIES'):
                    rt.initialize([('adult','Adult',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_sr_p024_actual_supported_tendency_still_allowed(self):
        validate_tendencies({'tendencies':[{'action':'SING','polarity':'WITHHOLD'}]})

    def test_sr_p021_empty_external_provider_rejected_no_inert_adult(self):
        def blank(task,packet):
            if task=='adult_constructor': return {'task':task,'forms':[],'projects':[],'links':[]}
            return {'task':task,'candidates':[]}
        semantic=ValidatingSemanticService(CallbackLLMProvider(blank))
        packet={'source_ref':'sourcefree_negative','answers':{'work':'yes'}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'empty.sqlite'),semantic)
            try:
                with self.assertRaisesRegex(ValueError,'NO_OPERATIVE_FICTIONAL_PARENT_CONSTITUTION'):
                    rt.initialize([('empty','Empty',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_sr_p025_parent_seed_impossible_project_means_rejected_without_commit(self):
        packet={'source_ref':'sourcefree_negative','answers':{'work':'yes'},
           'fictional_seed':{'projects':[{'object':'walk through walls','means':['TELEPORT']}]}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'invalid_project.sqlite'))
            try:
                with self.assertRaisesRegex(ValueError,'UNSUPPORTED_ACTIVITY_MEANS'):
                    rt.initialize([('adult','A',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_sr_p025_parent_seed_impossible_form_enabler_rejected(self):
        packet={'source_ref':'sourcefree_negative','answers':{'work':'yes'},
           'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE',
            'content':'nonphysical skill','cues':['home'],'enables':['TELEPORT']}]}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'invalid_form.sqlite'))
            try:
                with self.assertRaisesRegex(ValueError,'UNSUPPORTED_ACQUIRED_OPERATION'):
                    rt.initialize([('adult','A',packet)])
                self.assertEqual(rt.ledger.events(),[])
            finally:rt.close()

    def test_sr_p025_invalid_new_and_reorganized_project_means_do_not_mutate(self):
        from copy import deepcopy
        from um_sorok_organism.types import adult
        from um_sorok_organism.development import admit,InvalidDevelopment
        actor=adult('actor','A')
        actor['projects']=[{'id':'p1','object':'repair available things','means':['REPAIR']}]
        before=deepcopy(actor)
        exp={'actor':'actor','ref':'lived1','participated':True,
             'status':'PERFORMED','perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'UNSUPPORTED_ACTIVITY_MEANS'):
            admit(actor,exp,'objective1',[{'kind':'ADD_PROJECT',
                'project':{'object':'ghost means','means':['TELEPORT']}}])
        self.assertEqual(actor,before)
        with self.assertRaisesRegex(InvalidDevelopment,'UNSUPPORTED_ACTIVITY_MEANS'):
            admit(actor,exp,'objective1',[{'kind':'REORGANIZE_PROJECT',
                'project_id':'p1','means':['REPAIR','TELEPORT']}])
        self.assertEqual(actor,before)
        with self.assertRaisesRegex(InvalidDevelopment,'UNSUPPORTED_ACQUIRED_OPERATION'):
            admit(actor,exp,'objective1',[{'kind':'ADD_FORM','form':{'kind':'PRACTICE',
                'cues':['home'],'enables':['TELEPORT']}}])
        self.assertEqual(actor,before)

    def test_sr_p026_no_production_or_food_transaction_at_missing_material_site(self):
        from copy import deepcopy
        from um_sorok_organism.types import adult,Attempt,blank_world
        from um_sorok_organism.world import resolve
        world=blank_world();world['positions']['worker']='nonexistent_site'
        actors={'worker':adult('worker','W',location='nonexistent_site')}
        before=deepcopy(world['sites'])
        for action in ('WORK','REPAIR','BUY_FOOD','EAT'):
            with self.subTest(action=action):
                response=resolve(world,actors,Attempt('worker',action))
                self.assertEqual(response.status,'BLOCKED')
                self.assertEqual(response.objective_description,'UNKNOWN_MATERIAL_SITE')
                self.assertEqual(world['sites'],before)
        self.assertEqual(world['material_claims'],[])

if __name__=='__main__':unittest.main()
