import unittest
from operative_witness import freeze_operative_witness as bind, NONPROJECT_APPROACH as A, NONPROJECT_DEFERRAL as D

H='SOURCEFREE_RULE_BASED_PLACEHOLDER_NO_LLM'


def option(action, mode=None, refs=None):
    o={'action':action,'project_courses':[]}
    if mode:o['preproject_recruitment']={'status':mode,'ground_refs':refs or []}
    return o


class OperativeWitnessTests(unittest.TestCase):
    def test_lived_ground_frozen_before_outcome(self):
        out=bind('nadia',4,[option('ORIENT','ACQUIRED_NONPROJECT_APPROACH',['event-care-1']),option('WAIT')],
                 'ORIENT',{'purpose_selection_grade':A},H,[])
        self.assertEqual(out['policy_path'],'OFFLINE_HISTORICALLY_RECRUITED_ORIENTATION')
        self.assertEqual(out['recruited_ground_refs_at_choice'],['event-care-1'])
        self.assertTrue(out['not_actor_self_knowledge'])
        self.assertTrue(out['not_objective_world_cause'])
        self.assertNotIn('world_outcome',out)

    def test_duplicate_representations_not_extra_votes(self):
        with self.assertRaises(ValueError):
            bind('nadia',4,[option('ORIENT','ACQUIRED_NONPROJECT_APPROACH',['event-1','event-1'])],
                 'ORIENT',{'purpose_selection_grade':A},H,[])

    def test_two_real_distinct_grounds_retained_not_summed(self):
        out=bind('nadia',6,[option('ORIENT','ACQUIRED_NONPROJECT_APPROACH',['event-1','event-2'])],
                 'ORIENT',{'purpose_selection_grade':A},H,[])
        self.assertEqual(out['recruited_ground_refs_at_choice'],['event-1','event-2'])
        self.assertNotIn('strength',out)

    def test_deferral_witness_sources_are_opposed_options_not_wait(self):
        out=bind('nadia',9,[option('ORIENT','ACQUIRED_NONPROJECT_WITHHOLD',['event-strain']),option('WAIT')],
                 'WAIT',{'purpose_selection_grade':D},H,[])
        self.assertEqual(out['affected_option_refs'],['ORIENT'])
        self.assertEqual(out['recruited_ground_refs_at_choice'],['event-strain'])

    def test_conflict_cannot_be_misclassified_as_one_polarity(self):
        with self.assertRaisesRegex(ValueError,'FALSE_PREPROJECT'):
            bind('nadia',5,[option('ORIENT','UNRESOLVED_PREPROJECT_CONTRADICTION',['e1','e2'])],
                 'ORIENT',{'purpose_selection_grade':A},H,[])

    def test_lingual_model_mimic_cannot_claim_offline_policy(self):
        out=bind('nadia',5,[option('ORIENT','ACQUIRED_NONPROJECT_APPROACH',['history'])],
                 'ORIENT',{'purpose_selection_grade':A},'INJECTED_EXTERNAL_PROVIDER',[])
        self.assertEqual(out['policy_path'],'INDETERMINATE_SEMANTIC_CHOICE')
        self.assertEqual(out['recruited_ground_refs_at_choice'],[])

    def test_external_model_choice_not_washed_into_motive(self):
        out=bind('mother',55,[option('SING')], 'SING',{'project_id':'p1'}, 'LLM', ['p1'])
        self.assertEqual(out['selected_project_refs'],['p1'])
        self.assertNotIn('motivation',out)

    def test_deferral_requires_actual_opposition(self):
        with self.assertRaisesRegex(ValueError,'UNGROUNDED_DEFERRAL'):
            bind('nadia',3,[option('REST'),option('WAIT')],'WAIT',{'purpose_selection_grade':D},H,[])

    def test_selection_requires_single_actually_issued_option(self):
        with self.assertRaisesRegex(ValueError,'NOT_SINGULARLY_ISSUED'):
            bind('nadia',3,[option('ORIENT'),option('ORIENT')],'ORIENT',{},H,[])

    def test_external_model_conflict_no_retrospective_history(self):
        out=bind('nadia',3,[option('ORIENT','UNRESOLVED_PREPROJECT_CONTRADICTION',['e1','e2'])],
                 'ORIENT',{},'LLM',[])
        self.assertEqual(out['policy_path'],'INDETERMINATE_SEMANTIC_CHOICE')

    def test_injected_choice_not_eligible_as_actor_witness(self):
        out=bind('mother',30,[option('SING')],'SING',{},'EXTERNAL_RESEARCH_ACTION_INJECTION',[])
        self.assertEqual(out['policy_path'],'INDETERMINATE_SEMANTIC_CHOICE')

if __name__=='__main__':unittest.main()