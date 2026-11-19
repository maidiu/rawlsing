"""R4 sourcefree feature checks; construction scope, NOT REMONT receiving.

These examples check activity-specific recruitment and independently
selected acquired methods. They do not validate human motive formation,
correct any SR-P004/P005 defect, or accredit native SOROK psychology.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.constitution import materialize, actor_access, compose
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import (
    CallbackLLMProvider, HeuristicSemanticProvider, ValidatingSemanticService,
)


def packet():
    return {
        'source_ref': 'R4_FICTIONAL_ONLY',
        'answers': {'role': 'uncertain'},
        'fictional_seed': {
            'acquired_forms': [
                {'kind': 'PRACTICE', 'content': 'sing in familiar places',
                 'cues': ['coactor', 'home'], 'enables': ['SING'],
                 'scope': {'locations': ['home']}},
                {'kind': 'PRACTICE', 'content': 'care through ordinary action',
                 'cues': ['coactor', 'home'], 'enables': ['CARE'],
                 'scope': {'locations': ['home']}},
                {'kind': 'TENSION', 'content': 'withhold public singing',
                 'cues': ['coactor', 'home'], 'enables': [],
                 'scope': {'locations': ['home']},
                 'tendencies': [
                     {'action': 'SING', 'object': 'public singing',
                      'polarity': 'WITHHOLD'}]},
            ],
            'projects': [
                {'object': 'public singing', 'means': ['SING'],
                 'priority': .8, 'cue_terms': ['coactor']},
                {'object': 'private singing', 'means': ['SING'],
                 'priority': .7, 'cue_terms': ['coactor']},
            ],
        },
    }


class ActivityQualifiedFormation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name) / 'r4.sqlite')

    def tearDown(self):
        self.tmp.cleanup()

    def test_one_action_different_activity_not_globally_inhibited(self):
        r = ConstitutiveRuntime(self.db)
        try:
            r.initialize([('mother', 'Mother', packet())])
            _, world = r.ledger.world()
            _, actor = r.ledger.actor('mother')
            situated = compose(materialize(actor, world), actor_access(actor, world))
            self.assertTrue(any(
                s.get('practical_object') == 'public singing'
                for s in situated.suspended_actions
            ))
            self.assertTrue(any(
                a['action'] == 'SING' and a.get('practical_object') == 'private singing'
                for a in situated.candidate_actions
            ))
            self.assertTrue(any(
                a['action'] == 'SING' and not a.get('activity_ref')
                for a in situated.candidate_actions
            ))
        finally:
            r.close()

    def test_actor_policy_can_select_currently_acquired_method(self):
        fallback = HeuristicSemanticProvider()

        def provider(task, input_):
            if task == 'adult_constructor':
                return fallback.propose(task, input_)
            if task == 'development' and input_['actor']['id'] == 'mother':
                exp = input_['experience']
                if exp.get('own_action') == 'CARE' and exp.get('status') == 'PERFORMED':
                    forms = input_['actor_forms']
                    singer = next(fid for fid, f in forms.items()
                                  if 'SING' in f.get('enables', []))
                    carer = next(fid for fid, f in forms.items()
                                 if 'CARE' in f.get('enables', []))
                    return {'task': task, 'candidates': [
                        {'kind': 'ACQUIRE_COMPOSITION_METHOD',
                         'source_forms': [carer, singer],
                         'operations': ['CARE', 'SING'],
                         'hypothesized_end': 'care and familiar rhythm',
                         'locations': ['home']}
                    ]}
                return {'task': task, 'candidates': []}
            if task == 'composition_choice':
                return {'task': task,
                        'method_id': input_['available_methods'][0]['id']}
            if task == 'actor_attempt':
                return {'task': task, 'action': 'WAIT'}
            if task == 'expression':
                return {'task': task, 'surface': 'opaque'}
            raise ValueError(task)

        r = ConstitutiveRuntime(
            self.db, ValidatingSemanticService(CallbackLLMProvider(provider))
        )
        try:
            r.initialize([('mother', 'Mother', packet())])
            r.step('mother', requested_action='CARE', target='nadia')
            learned = r.situated('mother')['learned_compositions']
            self.assertTrue(learned)
            returned = r.act_on_acquired_method('mother')
            self.assertEqual(returned['status'],
                             'SOURCEFREE_ACTOR_POLICY_SELECTED_COMPOSITION')
            self.assertEqual(returned['method_id'], learned[0]['id'])
            self.assertTrue(returned['attempts'])
            self.assertEqual(
                returned['attempts'][0]['selection_grade'],
                'ACTOR_POLICY_SELECTED_ACQUIRED_METHOD_SOURCEFREE'
            )
            self.assertTrue(r.verify()['valid'])
        finally:
            r.close()


if __name__ == '__main__':
    unittest.main()
