"""Direct sourcefree checks for the new historically acquired reflective form."""
import unittest
from copy import deepcopy
from um_sorok_organism.reflective_regulation import acquire_reflective_regulation

ACTIONS={'ORIENT','SIGNAL','WAIT','REST','REFUSE','SPEAK'}

def actor(lang=.8, regulation=.6):
    return {'id':'nadia', 'location':'home',
            'body':{'language':lang,'regulation':regulation},
            'forms':{'f_practice':{'id':'f_practice','kind':'PRACTICE'}},
            'projects':[]}

def experience(actor_id='nadia',cue_ref='c2'):
    return {'actor':actor_id,'ref':'experience_2','participated':True,
            'status':'PERFORMED', 'own_action':'SPEAK',
            'felt_enactment':{'attempted_operation':'SPEAK'},
            'perceived_cues':[{'id':cue_ref,'tags':['public_reprimand'],'modality':'auditory'}]}

def proposal(**kwargs):
    return {'historical_source_ref':'f_practice',
            'future_operation':'SPEAK',
            'recruitment_polarity':'WITHHOLD',
            'perceived_cue_ref':'c2',**kwargs}

class ReflectiveRegulationR8(unittest.TestCase):
    def test_not_installed_in_infant_as_adult_will(self):
        a=actor(lang=0.0)
        with self.assertRaisesRegex(ValueError,'CAPACITY'):
            acquire_reflective_regulation(a,experience(),'event2',proposal(),ACTIONS)
    def test_inherited_practice_can_reorganize_future_conduct(self):
        a=actor()
        rec=acquire_reflective_regulation(a,experience(),'event2',proposal(),ACTIONS)
        f=a['forms'][rec['form']]
        self.assertEqual(f['tendencies'][0]['polarity'],'WITHHOLD')
        self.assertEqual(f['tendencies'][0]['action'],'SPEAK')
        self.assertEqual(f['enables'],[])
        self.assertEqual(f['historical_source_ref'],'f_practice')
        self.assertTrue(rec['not_sovereign_agency'])
    def test_cannot_invent_existing_expertise_or_history(self):
        a=actor()
        with self.assertRaisesRegex(ValueError,'UNOWNED'):
            acquire_reflective_regulation(a,experience(),'event2',
                            proposal(historical_source_ref='not_mine'),ACTIONS)
    def test_cannot_exercise_unearned_world_action(self):
        with self.assertRaisesRegex(ValueError,'UNLICENSED'):
            acquire_reflective_regulation(actor(),experience(),'event2',
                           proposal(future_operation='ELEVATE_SOCIAL_CLASS'),ACTIONS)
    def test_no_nonparticipatory_intention_from_observation(self):
        e=experience();e['felt_enactment']=None;e['participated']=False
        with self.assertRaisesRegex(ValueError,'NO_ENACTED'):
            acquire_reflective_regulation(actor(),e,'event2',proposal(),ACTIONS)
    def test_unseen_sign_cannot_motivate_the_new_practice(self):
        with self.assertRaisesRegex(ValueError,'UNEXPERIENCED'):
            acquire_reflective_regulation(actor(),experience(),'event2',
                               proposal(perceived_cue_ref='unseen'),ACTIONS)
    def test_duplicate_form_not_silently_minted(self):
        a=actor();p=proposal();e=experience()
        acquire_reflective_regulation(a,e,'event2',p,ACTIONS)
        old=deepcopy(a)
        with self.assertRaisesRegex(ValueError,'DUPLICATE'):
            acquire_reflective_regulation(a,e,'event2',p,ACTIONS)
        self.assertEqual(a,old)
    def test_wrong_actor_no_cross_actor_psychology(self):
        with self.assertRaisesRegex(ValueError,'IDENTITY'):
            acquire_reflective_regulation(actor(),experience('father'),
                                         'event2',proposal(),ACTIONS)
if __name__=='__main__':unittest.main()