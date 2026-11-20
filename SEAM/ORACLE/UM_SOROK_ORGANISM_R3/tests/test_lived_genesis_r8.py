import unittest
from copy import deepcopy
from um_sorok_organism.lived_genesis import proposals_from_bodily_history
from um_sorok_organism.preproject_agency import admit_preproject_anticipation


def actor():
    return {'id':'nadia','body':{'language':0.0,'sensor':0.4},'expectations':[],'projects':[]}

def exp(participated=True,felt_effect='SOMATIC_CARE_CANDIDATE',
        modality='visual',cue_id='c1'):
    return {'actor':'nadia','ref':'x1','participated':participated,
            'felt_effect':felt_effect,'perceived_cues':[
                {'id':cue_id,'modality':modality,'tags':['adult_analyst_label']}]}

def body(comfort=.5,pain=0):return {'comfort':comfort,'pain':pain}

class LivedGenesisR8(unittest.TestCase):
    def test_actual_bodily_relief_and_sensed_cue_proposes_not_installs(self):
        a=actor(); p=proposals_from_bodily_history(a,exp(),body(.4),body(.6))
        self.assertEqual(len(p),1)
        self.assertEqual(p[0]['orientation_mode'],'APPROACH')
        self.assertEqual(a['expectations'],[])
        self.assertEqual(a['projects'],[])
        admit_preproject_anticipation(a,exp(),'e1',p[0]);self.assertEqual(len(a['expectations']),1)
        self.assertEqual(a['expectations'][0]['discriminant_tags'],['sensory:visual'])
    def test_no_arbitrary_cause_from_world_event_without_bodily_change(self):
        self.assertEqual(proposals_from_bodily_history(actor(),exp(),body(.4),body(.405)),[])
    def test_coobserved_alien_effect_does_not_prove_my_relief(self):
        self.assertEqual(proposals_from_bodily_history(actor(),exp(felt_effect=None),body(.4),body(.6)),[])
    def test_actual_discomfort_may_propose_inhibition_without_compliance_law(self):
        p=proposals_from_bodily_history(actor(),exp(),body(.7),body(.5))
        self.assertEqual(p[0]['orientation_mode'],'WITHHOLD')
        self.assertEqual(p[0]['possible_operation'],'ORIENT')
    def test_infant_has_no_analyst_semantic_identity(self):
        p=proposals_from_bodily_history(actor(),exp(),body(.3),body(.6))
        a=actor();admit_preproject_anticipation(a,exp(),'e1',p[0]);rec=a['expectations'][0]
        self.assertNotIn('adult_analyst_label',rec['discriminant_tags'])
    def test_existing_acquired_band_is_not_replaced_by_deterministic_valence(self):
        a=actor();received=exp();prior=proposals_from_bodily_history(a,received,body(.3),body(.6))[0]
        admit_preproject_anticipation(a,received,'e1',prior)
        self.assertEqual(proposals_from_bodily_history(a,exp(cue_id='c2'),body(.8),body(.2)),[])
        self.assertEqual(a['expectations'][0]['orientation_mode'],'APPROACH')
    def test_low_sensor_cannot_gain_arbitrary_discrimination(self):
        a=actor();a['body']['sensor']=0.03
        self.assertEqual(proposals_from_bodily_history(a,exp(),body(.3),body(.6)),[])
    def test_adult_body_does_not_get_baby_fallback(self):
        a=actor();a['body']['language']=.9
        self.assertEqual(proposals_from_bodily_history(a,exp(),body(.3),body(.6)),[])
    def test_invalid_body_grades_rejected(self):
        with self.assertRaisesRegex(ValueError,'INVALID_BODY'):
            proposals_from_bodily_history(actor(),exp(),body(.2),body(float('nan')))
    def test_unseen_modality_not_assigned_as_an_infant_discrimination(self):
        self.assertEqual(proposals_from_bodily_history(actor(),exp(modality='unknown'),body(.2),body(.6)),[])

if __name__=='__main__':unittest.main()