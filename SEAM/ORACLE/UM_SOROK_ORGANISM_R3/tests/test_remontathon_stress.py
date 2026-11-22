"""Multi-episode conservation at local sourcefree research grade."""
import tempfile, unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.organism import eligible
from um_sorok_organism.semantics import ValidatingSemanticService, HeuristicSemanticProvider, CallbackLLMProvider

SEED={'source_ref':'stress_fixture','answers':{'shift':'often','kinship':'mixed'},
      'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE','cues':['home','sing'],'enables':['SING','ORIENT']}],
                        'projects':[{'object':'care for shared environment','means':['CARE','WORK','REPAIR'],
                                     'priority':.5,'cue_terms':['home','workshop']}]}}

class IntegratedStress(unittest.TestCase):
    def test_120_causally_ordered_real_steps_plus_cold_reopen_keep_world_and_actor_chain(self):
        with tempfile.TemporaryDirectory() as folder:
            path=str(Path(folder)/'long_life.db')
            rt=ConstitutiveRuntime(path)
            try:
                rt.initialize([('m','M',SEED),('s','S',SEED)])
                for i in range(120):
                    actor='m' if i%2==0 else 's'
                    action=('ORIENT','SING','REST','WAIT','SIGNAL','PRACTICE')[i%6]
                    if not eligible(rt.ledger.actor(actor)[1]['body'],action)[0]:
                        action='REST'
                    rt.step(actor,requested_action=action)
                    if i%19==0:rt.background(3)
                    if i%13==0:self.assertTrue(rt.verify()['valid'])
                self.assertEqual(rt.verify()['source_seals_verified'],2)
                before=rt.verify()
            finally:rt.close()
            reopened=ConstitutiveRuntime(path)
            try:
                self.assertEqual(reopened.verify(),before)
                self.assertEqual(len(reopened.ledger.actors()),3)
                self.assertTrue(reopened.snapshot('m')['forms'])
            finally:reopened.close()

    def test_bad_second_model_effect_leaves_no_world_or_actor_event(self):
        h=HeuristicSemanticProvider()
        def provider(task,packet):
            if task!='development':return h.propose(task,packet)
            return {'task':'development','candidates':[
                {'kind':'TRACE','content':'temporary actor hypothesis','cue_terms':['signal']},
                {'kind':'ADD_PROJECT','project':{'object':'impossible','means':['TELEPORT']}}
            ]}
        with tempfile.TemporaryDirectory() as folder:
            rt=ConstitutiveRuntime(str(Path(folder)/'failure.db'),
                                    ValidatingSemanticService(CallbackLLMProvider(provider)))
            try:
                rt.initialize([('m','M',SEED)])
                initial=rt.verify();before=rt.ledger.actor('m')[1]
                world_before=rt.ledger.world()[1]
                with self.assertRaisesRegex(ValueError,'UNSUPPORTED_ACTIVITY_MEANS'):
                    rt.step('m',requested_action='ORIENT')
                self.assertEqual(rt.verify(),initial)
                self.assertEqual(rt.ledger.actor('m')[1],before)
                self.assertEqual(rt.ledger.world()[1],world_before)
            finally:rt.close()
