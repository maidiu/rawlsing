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

if __name__=='__main__':unittest.main()
