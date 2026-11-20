"""REMONT R14 P004: actor-selected purpose cannot disagree with audited operation."""
import unittest
from um_sorok_organism.types import adult
from um_sorok_organism.activity import record_activity_afterlife


def person():
    a=adult('ann','Ann')
    a['projects']=[{'id':'care','object':'kin care','means':['SING'],'status':'active'},
                   {'id':'study','object':'study a song','means':['SING'],'status':'active'}]
    return a

class ActivityPurposeSelectionP004(unittest.TestCase):
    def test_external_injection_cannot_claim_project_course_by_legacy_basis(self):
        a=person()
        with self.assertRaisesRegex(ValueError,'ACTIVITY_PURPOSE_BASIS_CONTRADICTION'):
            record_activity_afterlife(a,'SING','PERFORMED','SANG',
                 ['project:care'],'event:1',purpose_selection={
                    'status':'EXTERNALLY_INJECTED_NO_ATTESTED_ACTOR_PURPOSE',
                    'project_id':None,'project_ids':[]})
        self.assertEqual(a.get('activity_history',[]),[])
        self.assertNotIn('operational_history',a['projects'][0])

    def test_unselected_extra_project_cannot_be_recorded_as_intent(self):
        a=person()
        with self.assertRaisesRegex(ValueError,'ACTIVITY_PURPOSE_BASIS_CONTRADICTION'):
            record_activity_afterlife(a,'SING','PERFORMED','SANG',
                ['project:care','project:study'],'event:2',purpose_selection={
                    'status':'ACTOR_POLICY_SELECTED_PROJECT_COURSE',
                    'project_id':'care','project_ids':['care']})
        self.assertEqual(a.get('activity_history',[]),[])

    def test_valid_selected_multiple_projects_remains_distinct(self):
        a=person()
        receipts=record_activity_afterlife(a,'SING','PERFORMED','SANG',
            ['project:care','project:study'],'event:3',purpose_selection={
                'status':'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES',
                'project_id':None,'project_ids':['care','study']})
        self.assertEqual({x['project'] for x in receipts},{'care','study'})
        self.assertEqual({x['intent_attribution'] for x in receipts},{'ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES'})

    def test_no_selected_purpose_does_not_create_activity_history(self):
        a=person()
        receipts=record_activity_afterlife(a,'SING','PERFORMED','SANG',
            ['organism'],'event:4',purpose_selection={
                'status':'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE',
                'project_id':None,'project_ids':[]})
        self.assertEqual(receipts,[])
        self.assertEqual(a.get('activity_history',[]),[])

    def test_selected_purpose_cannot_be_omitted_from_basis(self):
        a=person()
        with self.assertRaisesRegex(ValueError,'ACTIVITY_PURPOSE_BASIS_CONTRADICTION'):
            record_activity_afterlife(a,'SING','PERFORMED','SANG',
                ['organism'],'event:5',purpose_selection={
                    'status':'ACTOR_POLICY_SELECTED_PROJECT_COURSE',
                    'project_id':'care','project_ids':['care']})
        self.assertEqual(a.get('activity_history',[]),[])

if __name__=='__main__':unittest.main()
