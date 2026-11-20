"""R8 joined sourcefree default-runtime witness; verify at exact GitHub HEAD.

Unlike the earlier callback-injected R8 witness, this test requires no analyst
hand-inserted ACQUIRE_PREPROJECT_ANTICIPATION proposal. The actual changed body
and personally received event must generate it through the ordinary fallback.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService

PARENT = {'source_ref': 'synthetic_CARE_genesis_witness', 'answers': {},
          'fictional_seed': {'projects': []}}


class ChildLivedGenesisRuntimeR8(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt = ConstitutiveRuntime(str(Path(self.tmp.name) / 'genesis.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([('mother', 'Mother', PARENT),
                            ('father', 'Father', PARENT)])

    def test_actual_care_changes_body_then_proposes_preproject_without_injected_model(self):
        old = self.rt.snapshot('nadia')
        self.assertEqual(old['projects'], [])
        self.assertEqual(old['expectations'], [])
        actual = self.rt.step('mother', requested_action='CARE', target='nadia')
        self.assertEqual(actual['status'], 'PERFORMED')
        child = self.rt.snapshot('nadia')
        self.assertGreater(child['body']['comfort'], old['body']['comfort'])
        self.assertEqual(child['projects'], [])
        acquired = [e for e in child['expectations']
                    if e.get('acquisition') == 'PREPROJECT_ORIENTING_CONTINGENCY']
        self.assertEqual(len(acquired), 1)
        self.assertEqual(acquired[0]['possible_operation'], 'ORIENT')
        self.assertEqual(acquired[0]['orientation_mode'], 'APPROACH')
        self.assertEqual(acquired[0]['discriminant_tags'], ['sensory:visual'])
        self.assertEqual(acquired[0]['world_consequence'], 'NOT_INFERRED')
        self.assertEqual(self.rt.plan('nadia').action, 'ORIENT')
        # Acquired initiative is not a continuing conscious project or goal.
        self.assertEqual(self.rt.snapshot('nadia')['projects'], [])
        self.assertTrue(self.rt.verify()['valid'])

    def test_witnessed_other_person_care_does_not_fabricate_my_bodily_relief(self):
        self.rt.step('mother', requested_action='CARE', target='father')
        self.assertEqual(self.rt.snapshot('nadia')['expectations'], [])
        self.assertTrue(self.rt.verify()['valid'])

    def test_semantic_service_may_decline_qualified_candidate_without_retcon(self):
        def no_formation(task, packet):
            if task == 'development':
                if packet['actor']['id'] == 'nadia':
                    self.assertEqual(len(packet.get('historically_proposed_preproject', [])), 1)
                return {'task':task, 'candidates':[]}
            if task == 'expression':
                self.assertNotIn('bodily_before_actor_analyst_only', packet)
                return {'task':task, 'surface':'a caregiver acts'}
            raise AssertionError('unexpected semantic invocation: '+task)
        self.rt.semantic = ValidatingSemanticService(CallbackLLMProvider(no_formation))
        self.rt.step('mother',requested_action='CARE',target='nadia')
        self.assertEqual(self.rt.snapshot('nadia')['expectations'], [])
        self.assertTrue(self.rt.verify()['valid'])

if __name__ == '__main__': unittest.main()