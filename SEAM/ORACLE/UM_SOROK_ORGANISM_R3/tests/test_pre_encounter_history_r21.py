"""R21 mulch first consumer: lived history exists before user contact.

The childhood model is an upstream generative history, not user-played
dialogue with Nadia's father. Exact code is SOURCEFREE, not adult-person
scientific calibration or a claim that the user sees private memories.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.joined_longitudinal_demo import run_counterfactual


PARENT = {
    'source_ref': 'r21_fictional_parent_source',
    'source_grade': 'SOURCEFREE_TEST_NOT_A_PYAT_RESPONDENT',
    'answers': {'R21_FICTIONAL_INSTRUMENT': 'NOT_A_REAL_PERSON_ANSWER'},
    'fictional_seed': {'projects': []},
}


class PreEncounterHistoryR21(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = Path(self.tmp.name)/'r21.sqlite3'
        self.rt = ConstitutiveRuntime(str(self.db))
        self.rt.initialize([
            ('father', 'Father', PARENT),
            ('mother', 'Mother', PARENT),
        ])

    def tearDown(self):
        self.rt.close()
        self.tmp.cleanup()

    def test_child_history_is_offscreen_before_any_meeting(self):
        operations = []
        source_step = self.rt.step

        def spy(actor_id, *args, **kwargs):
            operations.append((actor_id, args, kwargs))
            return source_step(actor_id, *args, **kwargs)

        self.rt.step = spy
        receipt = self.rt.construct_pre_encounter_history(
            'nadia', 8, horizon_days=3,
            autonomous_beats=1, max_segments=32)
        self.assertEqual(receipt['status'], 'HISTORICAL_AGE_CUT_REACHED')
        self.assertEqual(receipt['last_modeled_age_days'], 8)
        self.assertEqual(self.rt.snapshot('nadia')['age_days'], 8)
        self.assertEqual(receipt['autonomous_beats_committed'],
                         sum(len(x['autonomous_event_receipts'])
                             for x in receipt['historical_receipts']))
        self.assertGreaterEqual(receipt['autonomous_beats_committed'], 1)
        self.assertTrue(receipt['no_user_action_or_other_person_consent_injected'])
        self.assertFalse(receipt['user_visible_childhood_scenes'])
        self.assertFalse(receipt['public_first_encounter_not_issued'] is False)
        self.assertEqual(receipt['continuing_actor_role_not_reclassified'],
                         'child')
        self.assertTrue(all(args == () and kwargs == {}
                            for _, args, kwargs in operations))
        self.assertNotIn('forms', receipt)
        self.assertNotIn('memories', receipt)
        self.assertNotIn('self_model', receipt)
        self.assertNotIn('fictional_seed', str(receipt))
        self.assertTrue(self.rt.verify()['valid'])

    def test_reopen_persists_actual_offscreen_history_without_private_render(self):
        receipt = self.rt.construct_pre_encounter_history(
            'nadia', 6, horizon_days=2,
            autonomous_beats=0, max_segments=16)
        end = self.rt.snapshot('nadia')
        self.assertEqual(receipt['last_modeled_age_days'], 6)
        self.assertTrue(self.rt.verify()['valid'])
        cold = ConstitutiveRuntime(str(self.db))
        try:
            self.assertTrue(cold.verify()['valid'])
            self.assertEqual(cold.snapshot('nadia'), end)
        finally:
            cold.close()

    def test_held_due_obligation_cannot_be_silently_aged_past(self):
        from um_sorok_organism.continuity_clock import continue_pre_encounter

        class Ledger:
            def __init__(self):
                self.actor_state = {
                    'id':'nadia', 'age_days':5, 'role':'child'}
                self.world_state = {'clock':5}

            def actors(self):
                return {'nadia':self.actor_state}

            def actor(self, actor):
                return (1, self.actor_state)

            def world(self, world_id):
                return (1, self.world_state)

        class Owner:
            world_id = 'w1'

            def __init__(self):
                self.ledger = Ledger()
                self.advance_calls = 0

            def advance_to_discontinuity(self, horizon):
                self.advance_calls += 1
                self.ledger.world_state['clock'] += 1
                return {
                    'historical_discontinuity': {
                        'kind':'OBLIGATION_DUE', 'actor':'father',
                        'source_ref':'unsettled_source'},
                    'ordinary_interval_receipt':None,
                    'high_resolution_actor_event':'performed_actual_turn',
                }

            def continue_without_user(self, beats):
                raise AssertionError('Cannot skip unresolved material source')

        owner = Owner()
        result = continue_pre_encounter(
            owner, 'nadia', 8, horizon_days=1, autonomous_beats=3)
        self.assertEqual(result['status'],
                         'HELD_AT_UNRESOLVED_MATERIAL_DISCONTINUITY')
        self.assertEqual(result['last_modeled_age_days'], 5)
        self.assertEqual(result['historical_receipts'][0]
                         ['independently_resolved_event'], 'performed_actual_turn')
        self.assertTrue(result['partial_historical_commits_not_rolled_back'])
        self.assertEqual(owner.advance_calls, 1)

    def test_invalid_age_or_budget_rejected_before_any_ledger_append(self):
        original = self.rt.verify()['events']
        bad = [
            (False,3,1,4), (None,3,1,4),
            (6,0,1,4), (6,3,25,4),
            (6,3,1,0), (600,3,1,4),
            (0,3,1,4),
        ]
        for target,horizon,beats,segments in bad:
            with self.subTest(target=target, horizon=horizon,
                              beats=beats,segments=segments):
                with self.assertRaises(ValueError):
                    self.rt.construct_pre_encounter_history(
                        'nadia', target, horizon_days=horizon,
                        autonomous_beats=beats,max_segments=segments)
                self.assertEqual(self.rt.verify()['events'], original)
        with self.assertRaises(TypeError):
            self.rt.construct_pre_encounter_history(
                'nadia', 6, requested_action='SPEAK')
        self.assertEqual(self.rt.verify()['events'],original)

    def test_reuses_distinct_historical_nadia_lives_without_rewriting_parent(self):
        with tempfile.TemporaryDirectory() as out:
            run_counterfactual(Path(out)/'causal',days=4,beats=2)
            preserved = []
            for filename in ('speaking.sqlite3','silent.sqlite3'):
                rt = ConstitutiveRuntime(
                    str(Path(out)/'causal'/filename))
                try:
                    before = rt.snapshot('nadia')
                    target = before['age_days']+6
                    receipt = rt.construct_pre_encounter_history(
                        'nadia',target,horizon_days=3,
                        autonomous_beats=1,max_segments=32)
                    self.assertEqual(receipt['status'],
                                     'HISTORICAL_AGE_CUT_REACHED')
                    after = rt.snapshot('nadia')
                    initial = {x['id'] for x in
                               before['cultural_reference_practices']}
                    later = {x['id'] for x in
                             after['cultural_reference_practices']}
                    self.assertTrue(initial.issubset(later))
                    preserved.append(before['cultural_reference_practices'])
                    self.assertTrue(rt.verify()['valid'])
                finally:
                    rt.close()
            self.assertNotEqual(preserved[0],preserved[1])


if __name__ == '__main__':
    unittest.main()
