"""Source-qualified hostile RED probes for SORACLE R10 d77cbf67.

These tests are authored to run in the R3 package checkout at the exact PR
#1188 HEAD. They are NOT represented as executed on that branch. Expected
before repair: RED. Do not treat intentional RED as a green production grade.
"""
import copy
import unittest

from um_sorok_organism.development import InvalidDevelopment, admit
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.types import adult


class TrialIssuanceRemont(unittest.TestCase):
    def test_r10_valid_trial_only_llm_choice_must_reach_runtime_issuer(self):
        """An issued trial ID is sufficient to identify its operation in runtime.

        ValidatingSemanticService currently checks only action and
        practical_option_id; it rejects this permitted R10 response before
        the runtime can verify trial identity and embodied eligibility.
        """
        service = ValidatingSemanticService(CallbackLLMProvider(
            lambda task, packet: {
                'task': task,
                'possible_end_trial_id': 'end_trial_issued_example',
            }))
        chosen = service.proposal('actor_attempt', {'options': []})
        self.assertEqual(chosen['possible_end_trial_id'], 'end_trial_issued_example')

    @staticmethod
    def _unissued_trial_fixture():
        person = adult('person_a', 'A')
        person['possible_ends'].append({
            'id': 'noticed_end_1',
            'origin_event': 'objective_prior',
            'status': 'POSSIBLE_NOT_ACQUIRED_MOTIVE',
            'possible_means': ['SING'],
            'trial_history': [],
        })
        experienced = {
            'actor': 'person_a',
            'ref': 'experience_real_current',
            'own_action': 'SING',
            'participated': True,
            'felt_enactment': {'attempted_operation': 'SING'},
            'perceived_cues': [],
            'status': 'PERFORMED',
        }
        # The actor policy NEVER selected, froze, or issued this ticket.
        forged = {
            'trial_id': 'model_invented_after_world_settlement',
            'actor': 'person_a',
            'operation': 'SING',
            'possible_end_ref': 'noticed_end_1',
            'origin_event': 'objective_prior',
            'actor_project_ref': None,
        }
        return person, experienced, forged

    def test_r10_semantic_candidate_cannot_mint_trial_after_world_settlement(self):
        """An actual SING does NOT authorize retrospective trial purpose.

        `admit` presently checks action, actor, end and experience, but not
        that trial_ID was frozen by runtime._actor_plan before resolution.
        """
        person, experienced, forged = self._unissued_trial_fixture()
        original = copy.deepcopy(person)
        with self.assertRaisesRegex(InvalidDevelopment,
                                    'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(person, experienced, 'objective_current', [
                {'kind': 'RECORD_POSSIBLE_END_TRIAL', 'trial': forged},
            ])
        self.assertEqual(person, original)

    def test_r10_one_world_event_cannot_be_forged_as_two_trial_selections(self):
        """Without a frozen one-ticket proof, two forged options both enter.

        Their different trial IDs produce different deterministic history IDs
        even though the performer only undertook one real physical SING.
        """
        person, experienced, forged = self._unissued_trial_fixture()
        original = copy.deepcopy(person)
        other = {**forged, 'trial_id': 'another_unissued_trial_for_same_event'}
        with self.assertRaisesRegex(InvalidDevelopment,
                                    'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(person, experienced, 'objective_current', [
                {'kind': 'RECORD_POSSIBLE_END_TRIAL', 'trial': forged},
                {'kind': 'RECORD_POSSIBLE_END_TRIAL', 'trial': other},
            ])
        self.assertEqual(person, original)


if __name__ == '__main__':
    unittest.main()
