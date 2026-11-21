"""R18 independent R14 P004 follow-on: selected actor purpose must admit performed means."""
import copy
import unittest

from um_sorok_organism.activity import record_activity_afterlife
from um_sorok_organism.types import adult


class SelectedActivityMeansR18(unittest.TestCase):
    def setUp(self):
        self.actor=adult('amy', 'Amy')
        self.actor['projects']=[
            {'id':'repair','object':'repair a chair','motive':'care for household',
             'status':'active','means':['REPAIR'],'priority':.4},
            {'id':'sing','object':'family singing','motive':'make music together',
             'status':'active','means':['SING'],'priority':.4},
            {'id':'shared','object':'second music course','motive':'practice rhythm',
             'status':'active','means':['SING','WAIT'],'priority':.4}]

    def record(self, operation, ids, *, status='PERFORMED', basis=None, event='event-r18', grade=None):
        if grade is None:
            grade=('ACTOR_POLICY_SELECTED_PROJECT_COURSE' if len(ids)==1 else
                   'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES' if ids else
                   'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE')
        receipt={'project_ids':ids,'project_id':ids[0] if len(ids)==1 else None,
                 'status':grade}
        if basis is None:
            basis=['project:'+id for id in ids]
        return record_activity_afterlife(self.actor,operation,status,'CONSEQUENCE',basis,
                                         event,purpose_selection=receipt)

    def assert_no_change(self, old):
        self.assertEqual(self.actor,old,'partial committed actor history on rejected actor-purpose mismatch')

    def test_selected_project_excludes_operation_refuses_before_history(self):
        old=copy.deepcopy(self.actor)
        with self.assertRaisesRegex(ValueError,'ACTIVITY_SELECTED_MEANS_CONTRADICTION'):
            self.record('SING',['repair'])
        self.assert_no_change(old)

    def test_mixed_purposes_one_incompatible_refuses_atomically(self):
        old=copy.deepcopy(self.actor)
        with self.assertRaisesRegex(ValueError,'ACTIVITY_SELECTED_MEANS_CONTRADICTION'):
            self.record('SING',['sing','repair'])
        self.assert_no_change(old)

    def test_unknown_selected_project_refuses_without_silent_drop(self):
        old=copy.deepcopy(self.actor)
        with self.assertRaisesRegex(ValueError,'ACTIVITY_SELECTED_MEANS_CONTRADICTION'):
            self.record('SING',['missing'])
        self.assert_no_change(old)

    def test_selected_project_allows_exact_exercised_mean(self):
        result=self.record('REPAIR',['repair'])
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['project'],'repair')
        self.assertEqual(result[0]['intent_attribution'],'ACTOR_POLICY_SELECTED_PROJECT_COURSE')
        self.assertEqual(len(self.actor['activity_history']),1)

    def test_multiple_genuine_courses_survive(self):
        result=self.record('SING',['sing','shared'])
        self.assertEqual({x['project'] for x in result},{'sing','shared'})
        self.assertEqual(len(self.actor['activity_history']),2)

    def test_blocked_attempt_preserves_selected_historical_course(self):
        result=self.record('SING',['sing'],status='BLOCKED')
        self.assertEqual(result[0]['operation_course'],'INTERRUPTED_ATTEMPT')
        self.assertEqual(result[0]['motive_realized'],'UNDETERMINED_BY_TECHNICAL_OUTCOME')

    def test_projectless_policy_selection_remains_projectless(self):
        result=self.record('WAIT',[],basis=['organism'])
        self.assertEqual(result,[])
        self.assertEqual(self.actor['activity_history'],[])

    def test_disclosed_legacy_direct_helper_does_not_claim_policy_selection(self):
        result=record_activity_afterlife(self.actor,'SING','PERFORMED','CONSEQUENCE',
                          ['project:sing'],'legacy-event',purpose_selection=None)
        self.assertEqual(len(result),1)
        self.assertEqual(result[0]['intent_attribution'],'EXPLICIT_LEGACY_PROJECT_BASIS_ASSERTION')

if __name__=='__main__':
    unittest.main()
