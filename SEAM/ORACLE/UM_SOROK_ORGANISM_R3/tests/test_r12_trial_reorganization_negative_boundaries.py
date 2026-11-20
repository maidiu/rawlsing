"""R12 author supplementary first-fault regression, kept distinct from prior hostile review."""
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment

class R12ProjectReorganizationBoundaries(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory(); self.addCleanup(self.t.cleanup)
        self.rt = ConstitutiveRuntime(str(Path(self.t.name) / 'actor.sqlite'))
        self.addCleanup(self.rt.close)
        self.rt.initialize(); self.rt.background(280)
        initial_semantic=self.rt.semantic
        def seed(task, packet):
            if task == 'development':
                return {'task': task, 'candidates': [{'kind':'ADD_PROJECT',
                    'project': {'object':'repair a family bicycle', 'means':['WAIT','SING'],
                    'motive':'keep transport working', 'priority':.2, 'cue_terms':['home']}}]}
            return {'task':task,'surface':'ok'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(seed))
        self.rt.step('nadia',requested_action='WAIT')
        self.rt.semantic = initial_semantic
        self.rt.step('nadia',requested_action='SING')
        self.project = deepcopy(self.rt.snapshot('nadia')['projects'][0])
        self.end = deepcopy(self.rt.snapshot('nadia')['possible_ends'][0])

    def _provider(self,candidates):
        def fn(task, packet):
            if task == 'actor_attempt':
                issued = next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':issued['trial_id']}
            if task == 'development':return {'task':task,'candidates':candidates}
            return {'task':task,'surface':'ok'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(fn))

    def _must_rollback(self,candidates):
        self._provider(candidates)
        before_clock=self.rt.ledger.world()[1]['clock']
        before_actor=deepcopy(self.rt.ledger.actors()['nadia'])
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before_clock)
        self.assertEqual(self.rt.ledger.actors()['nadia'],before_actor)
        self.assertTrue(self.rt.verify()['valid'])

    def test_object_only_rewrite_refused_without_effect(self):
        self._must_rollback([{'kind':'REORGANIZE_PROJECT', 'project_id':self.project['id'],
                              'object':'singing as a fully acquired vocation'}])

    def test_motive_only_rewrite_refused_even_with_existing_object(self):
        self._must_rollback([{'kind':'REORGANIZE_PROJECT', 'project_id':self.project['id'],
                              'motive':'MATURE_HISTORICAL_MOTIVE_FROM_CURRENT_TRIAL'}])

    def test_mixed_trace_then_motive_rewrite_rolls_back_everything(self):
        self._must_rollback([{'kind':'TRACE', 'cue_terms':['home'],
                              'content':'tentative actor sensation'},
                             {'kind':'REORGANIZE_PROJECT', 'project_id':self.project['id'],
                              'motive':'ANACHRONISTIC_RETROACTIVE_PURPOSE'}])

    def test_current_trial_nonpurpose_project_scope_update_remains_available(self):
        self._provider([{'kind':'REORGANIZE_PROJECT', 'project_id':self.project['id'],
                         'priority':.23,'cue_terms':['home','practice']}])
        self.rt.step('nadia')
        now=next(x for x in self.rt.snapshot('nadia')['projects'] if x['id']==self.project['id'])
        self.assertEqual(now['object'],self.project['object'])
        self.assertEqual(now['motive'],self.project['motive'])
        self.assertEqual(now['priority'],.23)
        self.assertEqual(now['cue_terms'],['home','practice'])
        self.assertEqual(self.rt.snapshot('nadia')['possible_ends'][0]['status'],
                         'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertEqual(len(self.rt.snapshot('nadia')['possible_ends'][0]['trial_history']),1)
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':unittest.main()
