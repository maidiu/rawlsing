"""Joined R8 sourcefree witness. Run ONLY in exact R8 package checkout.

One real world SIGNAL event -> personally perceived cue -> owner admission
-> next actor-selected ORIENT without adult project -> objective world step.
These tests are committed candidates until an actual package runner executes.
"""
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (CallbackLLMProvider, HeuristicSemanticProvider,
                                        ValidatingSemanticService)


class PreprojectRuntimeR8(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.rt = ConstitutiveRuntime(str(Path(self.temp.name) / 'r8.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize()
        self.emitted = False

        def callback(task, packet):
            if task == 'actor_attempt':
                return HeuristicSemanticProvider().propose(task, packet)
            if task == 'development':
                experience = packet['experience']
                if (packet['actor']['id'] == 'nadia' and
                        experience.get('own_action') == 'SIGNAL' and
                        experience.get('perceived_cues') and not self.emitted):
                    self.emitted = True
                    return {'task': task, 'candidates': [
                        {'kind': 'ACQUIRE_PREPROJECT_ANTICIPATION',
                         'perceived_cue_ref': experience['perceived_cues'][0]['id'],
                         'possible_operation': 'ORIENT',
                         'orientation_mode': 'APPROACH'}]}
                return {'task': task, 'candidates': []}
            if task == 'expression':
                # Never put private anticipation into public speech.
                self.assertNotIn('actor_expectations_analyst_only', packet)
                return {'task': task, 'surface': 'a child turns toward a sound'}
            raise ValueError('UNKNOWN_MODEL_TASK:' + task)
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(callback))

    def test_one_world_event_creates_nonproject_future_operation(self):
        first = self.rt.step('nadia', requested_action='SIGNAL')
        self.assertEqual(first['attempt'], 'SIGNAL')
        child = self.rt.snapshot('nadia')
        self.assertEqual(child['projects'], [])
        self.assertEqual(len(child['expectations']), 1)
        self.assertIsNone(child['expectations'][0]['project_id'])
        self.assertEqual(child['expectations'][0]['conceptual_access'],
                         'NONDECLARATIVE_NOT_ACTOR_PROPOSITION')
        situated = self.rt.situated('nadia')
        self.assertIn('HISTORICALLY_ACQUIRED_PREPROJECT_SOLICITATION',
                      [c.get('kind') for c in situated['currents']])
        next_attempt = self.rt.plan('nadia')
        self.assertEqual(next_attempt.action, 'ORIENT')
        self.assertIsNone(next_attempt.purpose_selection.get('project_id'))
        second = self.rt.step('nadia')
        self.assertEqual(second['attempt'], 'ORIENT')
        self.assertTrue(self.rt.verify()['valid'])
        child = self.rt.snapshot('nadia')
        self.assertEqual(child['projects'], [])

    def test_no_forged_sensory_input_rolls_back_real_world(self):
        def invalid(task, packet):
            if task == 'development':
                return {'task': task, 'candidates': [
                    {'kind': 'ACQUIRE_PREPROJECT_ANTICIPATION',
                     'perceived_cue_ref': 'unexperienced_invented_sign',
                     'possible_operation': 'ORIENT',
                     'orientation_mode': 'APPROACH'}]}
            if task == 'expression':
                return {'task': task, 'surface': 'irrelevant'}
            return HeuristicSemanticProvider().propose(task, packet)
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(invalid))
        before = self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(ValueError, 'UNEXPERIENCED'):
            self.rt.step('nadia', requested_action='SIGNAL')
        self.assertEqual(self.rt.ledger.world()[1]['clock'], before)
        self.assertEqual(self.rt.snapshot('nadia')['expectations'], [])


if __name__ == '__main__':
    unittest.main()