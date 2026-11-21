"""Independent R12 receiving -- adversarial first-consumer test, not author tests.

Freeze: maidiu/rawlsing #1199 HEAD 9db0e6f64bf568409e638ff2215af8b8a414487f
Original source unmodified; review-only module added after exact 42-file verification.
"""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.storage import ResearchLedger
from um_sorok_organism.types import adult, blank_world, canonical
from um_sorok_organism.constitution import actor_access


class TrialProjectAuthority(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.rt = ConstitutiveRuntime(str(Path(self.directory.name) / 'life.sqlite'))
        self.addCleanup(self.rt.close)
        self.rt.initialize()
        self.rt.background(280)
        original_provider = self.rt.semantic
        # First acquire a fully separate project in an earlier, real nontrial event.
        def create_prior_project(task, packet):
            if task == 'development':
                return {'task': task, 'candidates': [{'kind': 'ADD_PROJECT', 'project': {
                    'object': 'keep familiar household rhythm',
                    'means': ['WAIT', 'SING'],
                    'motive': 'maintain family continuity',
                    'cue_terms': ['home', 'sing'],
                    'priority': .1}}]}
            return {'task': task, 'surface': 'ok'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(create_prior_project))
        self.rt.step('nadia', requested_action='WAIT')
        self.rt.semantic = original_provider
        self.project = self.rt.snapshot('nadia')['projects'][0]
        # Different objective event produces a tentative possible end.
        self.rt.step('nadia', requested_action='SING')
        self.end = self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(self.end['status'], 'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertTrue(self.rt.verify()['valid'])

    def _choose_trial(self, development_candidates):
        def semantic(task, packet):
            if task == 'actor_attempt':
                trials = [t for t in packet['possible_end_trials'] if t['operation'] == 'SING']
                self.assertEqual(len(trials), 1, 'An actually issued SING trial is essential')
                return {'task': task, 'possible_end_trial_id': trials[0]['trial_id']}
            if task == 'development':
                return {'task': task, 'candidates': development_candidates}
            return {'task': task, 'surface': 'ok'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(semantic))

    def test_negative_same_event_trial_rewrite_of_existing_project_must_refuse(self):
        """RED: R12 bans ADD_PROJECT but permits motive rewrite via REORGANIZE_PROJECT."""
        self._choose_trial([{'kind': 'REORGANIZE_PROJECT',
            'project_id': self.project['id'],
            'object': self.end['possible_object'],
            'motive': 'MATURE_END_FROM_THIS_TRIAL',
            'priority': 15.0}])
        before_clock = self.rt.ledger.world()[1]['clock']
        before_projects = deepcopy(self.rt.snapshot('nadia')['projects'])
        with self.assertRaisesRegex(InvalidDevelopment,
                'CURRENT_TRIAL|MOTIVE|DURABLE_PROJECT'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'], before_clock)
        self.assertEqual(self.rt.snapshot('nadia')['projects'], before_projects)
        self.assertTrue(self.rt.verify()['valid'])

    def test_positive_current_trial_ADD_PROJECT_rejected_atomically(self):
        self._choose_trial([{'kind': 'ADD_PROJECT', 'project': {
            'object': self.end['possible_object'],
            'motive': 'MATURE_END_FROM_THIS_TRIAL',
            'means': ['SING']}}])
        clock = self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(InvalidDevelopment,
                'CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'], clock)
        self.assertTrue(self.rt.verify()['valid'])

    def test_positive_actual_trial_does_not_promote_possible_end_without_proposal(self):
        self._choose_trial([])
        self.rt.step('nadia')
        state = self.rt.snapshot('nadia')
        self.assertEqual(state['possible_ends'][0]['status'], 'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertEqual(len(state['possible_ends'][0]['trial_history']), 1)
        self.assertEqual(state['projects'][0]['motive'], self.project['motive'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_positive_nontrial_reorganization_remains_usable(self):
        def semantic(task,packet):
            if task == 'development':return {'task':task,'candidates': [
                {'kind':'REORGANIZE_PROJECT','project_id':self.project['id'],
                 'object':'care with renewed household resources',
                 'motive':'REVISED_AFTER_INDEPENDENT_NONTRIAL_EVENT'}]}
            return {'task':task,'surface':'ok'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(semantic))
        self.rt.step('nadia', requested_action='WAIT')
        self.assertEqual(self.rt.snapshot('nadia')['projects'][0]['motive'],
            'REVISED_AFTER_INDEPENDENT_NONTRIAL_EVENT')
        self.assertTrue(self.rt.verify()['valid'])

class SourceIntegrityAdversarial(unittest.TestCase):
    def test_p070_separate_snapshot_canonical_and_world_roster_fail_closed(self):
        for target in ('worlds','actors','world_roster'):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as d:
                l = ResearchLedger(str(Path(d)/'data.sqlite'))
                try:
                    l.initialize(blank_world(), [adult('ann','Ann')])
                    if target == 'world_roster':
                        l.conn.execute('INSERT INTO worlds(id,version,body) VALUES(?,?,?)',
                            ('w2',0,canonical(blank_world('w2'))))
                    else:
                        raw = l.conn.execute(f'SELECT body FROM {target} LIMIT 1').fetchone()[0]
                        l.conn.execute(f'UPDATE {target} SET body=?', (' '+raw,))
                    with self.assertRaisesRegex(AssertionError,'NONCANONICAL|UNCOMMITTED_WORLD_ROSTER'):
                        l.verify_chain()
                finally:
                    l.close()

    def test_p071_invalid_float_sensor_nan_and_inf_fail_closed(self):
        for invalid in (float('nan'),float('inf'),float('-inf')):
            with self.subTest(value=str(invalid)):
                a = adult('ann','Ann')
                a['body']['sensor'] = invalid
                w = blank_world()
                with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE:sensor'):
                    actor_access(a,w)

if __name__ == '__main__':
    unittest.main()
