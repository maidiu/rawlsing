"""Additional receiving probes: same-event trial cannot mint a durable motive by aliasing ingress."""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment


class SameEventMotiveRoutes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt = ConstitutiveRuntime(str(Path(self.tmp.name) / 'life.sqlite'))
        self.addCleanup(self.rt.close)
        self.rt.initialize()
        self.rt.background(280)
        self.rt.step('nadia', requested_action='SING')
        self.end = self.rt.snapshot('nadia')['possible_ends'][0]

    def _attempt(self, candidates):
        def provider(task, packet):
            if task == 'actor_attempt':
                issued = next(t for t in packet['possible_end_trials']
                              if t['operation'] == 'SING')
                return {'task': task, 'possible_end_trial_id': issued['trial_id']}
            if task == 'development':
                return {'task': task, 'candidates': candidates}
            return {'task': task, 'surface': 'public only'}
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(provider))
        before = self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(InvalidDevelopment, 'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'], before)
        self.assertFalse(self.rt.snapshot('nadia')['possible_ends'][0].get('trial_history'))
        self.assertTrue(self.rt.verify()['valid'])

    def test_alias_object_cannot_mint_same_event_project(self):
        self._attempt([{'kind': 'ADD_PROJECT', 'project': {
            'object': 'a deliberately renamed new ambition', 'means': ['SING'],
            'motive': 'MATURE_MOTIVE_DISGUISED', 'priority': .9}}])

    def test_a_previous_project_cannot_gain_same_event_new_motive(self):
        project = {'object': 'keep daily routines', 'means': ['REST'],
                   'motive': 'ORDINARY_CARE', 'priority': .4,
                   'status': 'active', 'cue_terms': []}

        def seed(task, packet):
            if task == 'development':
                return {'task': task, 'candidates': [
                    {'kind': 'ADD_PROJECT', 'project': project}]}
            return {'task': task, 'surface': 'public only'}

        # This previously established project is acquired at a separate,
        # genuine objective event rather than inserted into an actor copy.
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(seed))
        self.rt.step('nadia', requested_action='SIGNAL')
        old = next(p for p in self.rt.snapshot('nadia')['projects']
                   if p['object'] == project['object'])
        self.assertEqual(old['motive'], 'ORDINARY_CARE')
        self.rt.cue(kind='audible_song', tags=['sing', 'rhythm'])
        self._attempt([{'kind': 'REORGANIZE_PROJECT',
                        'project_id': old['id'],
                        'motive': 'MATURE_MOTIVE_DISGUISED'}])
        after = next(p for p in self.rt.snapshot('nadia')['projects']
                     if p['id'] == old['id'])
        self.assertEqual(after['motive'], 'ORDINARY_CARE')

    def test_atomicity_blocks_form_then_project_shortcut(self):
        self._attempt([{'kind': 'TRACE', 'cue_terms': ['rhythm'],
                        'content': 'tentative notice'},
                       {'kind': 'ADD_PROJECT', 'project': {
                           'object': self.end['possible_object'], 'means': ['SING'],
                           'motive': 'RETROACTIVE_MOTIVE'}}])


if __name__ == '__main__':
    unittest.main()
