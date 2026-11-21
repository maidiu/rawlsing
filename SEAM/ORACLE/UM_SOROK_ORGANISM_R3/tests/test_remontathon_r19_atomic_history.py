"""R19: P004 all-selected-project duplicate-event history must be atomic.

Small, sourcefree first-owner court. This must not imply a psychological
purpose was achieved or replace native science/actor source authority.
"""
from copy import deepcopy
import unittest
from um_sorok_organism.activity import record_activity_afterlife


def project(pid, existing=False):
    result = {'id': pid, 'means': ['INSPECT'], 'object': 'object-' + pid,
              'motive': 'UNDISCLOSED'}
    if existing:
        result['operational_history'] = [
            {'event': 'evt_1', 'operation': 'INSPECT', 'project': pid}]
    return result


def selected(ids):
    return {
        'project_id': ids[0] if len(ids) == 1 else None,
        'project_ids': ids,
        'status': ('ACTOR_POLICY_SELECTED_PROJECT_COURSE' if len(ids) == 1
                   else 'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES' if ids
                   else 'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE'),
    }


class AtomicSelectionR19(unittest.TestCase):
    def test_later_duplicate_refuses_before_any_project_history_write(self):
        actor = {'id': 'nadia', 'projects': [project('a'), project('b', True)]}
        before = deepcopy(actor)
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(
                actor, 'INSPECT', 'PERFORMED', {}, ['project:a', 'project:b'],
                'evt_1', purpose_selection=selected(['a', 'b']))
        self.assertEqual(actor, before)

    def test_earlier_duplicate_also_refuses_without_mutation(self):
        actor = {'id': 'nadia', 'projects': [project('a', True), project('b')]}
        before = deepcopy(actor)
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(
                actor, 'INSPECT', 'PARTIAL', {}, ['project:a', 'project:b'],
                'evt_1', purpose_selection=selected(['a', 'b']))
        self.assertEqual(actor, before)

    def test_valid_multi_project_occurrence_preserved(self):
        actor = {'id': 'nadia', 'projects': [project('a'), project('b')]}
        receipts = record_activity_afterlife(
            actor, 'INSPECT', 'PERFORMED', {'object': 'seen'},
            ['project:a', 'project:b'], 'evt_2',
            purpose_selection=selected(['a', 'b']))
        self.assertEqual([x['project'] for x in receipts], ['a', 'b'])
        self.assertEqual(len(actor['activity_history']), 2)
        self.assertTrue(all(x['motive_realized'] == 'UNDETERMINED_BY_TECHNICAL_OUTCOME'
                            for x in receipts))

    def test_incompatible_selected_means_refuses_without_mutation(self):
        actor = {'id': 'nadia', 'projects': [project('a'), project('b')]}
        actor['projects'][1]['means'] = ['REST']
        before = deepcopy(actor)
        with self.assertRaisesRegex(ValueError, 'ACTIVITY_SELECTED_MEANS_CONTRADICTION'):
            record_activity_afterlife(
                actor, 'INSPECT', 'PERFORMED', {}, ['project:a', 'project:b'],
                'evt_3', purpose_selection=selected(['a', 'b']))
        self.assertEqual(actor, before)

    def test_legacy_explicit_assertion_preserved(self):
        actor = {'id': 'nadia', 'projects': [project('a')]}
        receipt = record_activity_afterlife(
            actor, 'INSPECT', 'BLOCKED', {}, ['project:a'], 'evt_4')
        self.assertEqual(receipt[0]['intent_attribution'],
                         'EXPLICIT_LEGACY_PROJECT_BASIS_ASSERTION')

    def test_actor_prior_history_untouched_after_duplicate(self):
        actor = {'id': 'nadia', 'projects': [project('a'), project('b', True)],
                 'activity_history': [{'event': 'earlier', 'project': 'a'}]}
        before = deepcopy(actor)
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(
                actor, 'INSPECT', 'PERFORMED', {},
                ['project:a', 'project:b'], 'evt_1',
                purpose_selection=selected(['a', 'b']))
        self.assertEqual(actor, before)

    def test_legacy_multi_basis_duplicate_also_atomic(self):
        actor = {'id': 'nadia', 'projects': [project('a'), project('b', True)]}
        before = deepcopy(actor)
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(
                actor, 'INSPECT', 'PERFORMED', {},
                ['project:a', 'project:b'], 'evt_1')
        self.assertEqual(actor, before)

    def test_projectless_action_remains_projectless(self):
        actor = {'id': 'nadia', 'projects': [project('a')]}
        receipt = record_activity_afterlife(
            actor, 'INSPECT', 'BLOCKED', {}, [], 'evt_6',
            purpose_selection=selected([]))
        self.assertEqual(receipt, [])
        self.assertEqual(actor['projects'][0].get('operational_history', []), [])
