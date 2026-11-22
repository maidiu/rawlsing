"""REMONT R7: red-first independent coaction, objective grants, and invalid embodied recipient state."""
from copy import deepcopy
import unittest

from um_sorok_organism.types import Attempt, blank_world, adult
from um_sorok_organism.world import IndependentWorldAuthority, resolve


def scene():
    w=blank_world()
    w['positions'].update({'ann':'home','joann':'home'})
    a={'ann':adult('ann','Ann',location='home'), 'joann':adult('joann','Joann',location='home')}
    return w,a

class IndependentWorldR7(unittest.TestCase):
    def test_p058_malformed_hall_membership_string_does_not_authorize_substring_actor(self):
        w,a=scene()
        w['institutions']['hall_board']['members']='joann'
        initial=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_INSTITUTION_MEMBERSHIP'):
            resolve(w,a,Attempt('ann','OPEN_HALL'))
        self.assertEqual(initial,w)

    def test_p058_malformed_site_admission_string_cannot_authorize_move(self):
        w,a=scene()
        w['sites']['hall']['admitted']='joann'
        initial=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_SITE_ADMISSION'):
            resolve(w,a,Attempt('ann','MOVE',object_ref='hall'))
        self.assertEqual(initial,w)

    def test_p058_malformed_material_grants_string_cannot_authorize_repair(self):
        w,a=scene()
        w['positions']['ann']='workshop';a['ann']['location']='workshop'
        w['sites']['workshop']['material_use_grants']='joann'
        initial=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_MATERIAL_GRANT'):
            resolve(w,a,Attempt('ann','REPAIR'))
        self.assertEqual(initial,w)

    def test_p058_real_qualified_membership_grants_continue_to_work(self):
        w,a=scene()
        w['institutions']['hall_board']['members']=['ann']
        r=resolve(w,a,Attempt('ann','OPEN_HALL'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertEqual(w['sites']['hall']['access'],'public')
        w['sites']['hall']['access']='controlled'
        w['sites']['hall']['admitted']=['ann']
        self.assertEqual(resolve(w,a,Attempt('ann','MOVE',object_ref='hall')).status,'PERFORMED')
        w['positions']['ann']='workshop';a['ann']['location']='workshop'
        w['sites']['workshop']['material_use_grants']=['ann']
        self.assertEqual(resolve(w,a,Attempt('ann','REPAIR')).status,'PERFORMED')

    def test_p059_blocked_initiator_never_produces_partner_voluntary_completion(self):
        w,a=scene();a['ann']['body']['motor']=0.01
        invocations=[]
        def planner(principal,ww,aa):
            invocations.append(principal.action)
            return Attempt('joann','JOIN',target='ann')
        authority=IndependentWorldAuthority(planner)
        r,partner,policy=authority.resolve(w,a,Attempt('ann','SING',target='joann'))
        self.assertEqual(r.status,'BLOCKED')
        self.assertIsNone(partner)
        self.assertIsNone(policy)
        self.assertEqual(r.performed,[{'actor':'ann','action':'SING','status':'BLOCKED','as_willing':True}])
        self.assertEqual(invocations,[])
        self.assertFalse(w['relations'])

    def test_p059_qualified_joint_act_still_records_independent_respondent(self):
        w,a=scene()
        authority=IndependentWorldAuthority(lambda pr,ww,aa:Attempt('joann','SING',target='ann'))
        r,partner,policy=authority.resolve(w,a,Attempt('ann','SING',target='joann'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertIsNotNone(partner)
        self.assertEqual(r.objective_description,'JOINT_ACTIVITY_PERFORMED')
        self.assertIsNotNone(policy)

    def test_p060_other_policy_response_target_must_match_actual_initiator(self):
        w,a=scene()
        before=deepcopy(w)
        authority=IndependentWorldAuthority(lambda pr,ww,aa:Attempt('joann','JOIN',target='third_person'))
        with self.assertRaisesRegex(ValueError,'INDEPENDENT_COACTOR_TARGET_MISMATCH'):
            authority.resolve(w,a,Attempt('ann','SING',target='joann'))
        self.assertEqual(before,w)

    def test_p061_care_cannot_launder_nonfinite_target_body_without_validation(self):
        w,a=scene();a['joann']['body']['nutrition']=float('nan')
        before=deepcopy(w)
        with self.assertRaisesRegex(ValueError,'INVALID_BODY_STATE:nutrition'):
            resolve(w,a,Attempt('ann','CARE',target='joann'))
        self.assertEqual(before,w)

    def test_p061_valid_care_target_continues_to_receive_material_care(self):
        w,a=scene();before=a['joann']['body']['comfort']
        r=resolve(w,a,Attempt('ann','CARE',target='joann'))
        self.assertEqual(r.status,'PERFORMED')
        self.assertGreater(a['joann']['body']['comfort'],before)


class PsychicScopeTypeR7(unittest.TestCase):
    def test_p062_invalid_scope_location_string_refused_at_admission(self):
        from um_sorok_organism.psychodynamics import validate_tendencies
        with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_FORM_PARAMETERS'):
            validate_tendencies({'id':'x','scope':{'locations':'homeworkshop'}})

    def test_p062_invalid_scope_counterpart_type_refused(self):
        from um_sorok_organism.psychodynamics import validate_tendencies
        with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_FORM_PARAMETERS'):
            validate_tendencies({'id':'x','scope':{'counterpart':['ann']}})

    def test_p062_invalid_form_cue_string_refused(self):
        from um_sorok_organism.psychodynamics import validate_tendencies
        with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_FORM_PARAMETERS'):
            validate_tendencies({'id':'x','cues':'coactor'})

    def test_p062_world_access_reader_must_not_infer_admission_by_substring(self):
        from um_sorok_organism.constitution import actor_access
        w,a=scene();w['positions']['ann']='hall';a['ann']['location']='hall'
        w['sites']['hall']['admitted']='joann'
        with self.assertRaisesRegex(ValueError,'INVALID_SITE_ADMISSION'):
            actor_access(a['ann'],w)

    def test_p063_link_context_string_refused_before_acquired_relation_installed(self):
        from um_sorok_organism.development import admit, InvalidDevelopment
        a=adult('ann','Ann');a['forms']={'a':{'id':'a'},'b':{'id':'b'}}
        before=deepcopy(a)
        exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_LINK_CONTEXTS'):
            admit(a,exp,'objective_1',[{'kind':'LINK_FORMS','source':'a','target':'b',
                                      'relation':'RECRUITS','contexts':'homeworkshop'}])
        self.assertEqual(before,a)

    def test_p063_activity_link_context_string_refused(self):
        from um_sorok_organism.development import admit, InvalidDevelopment
        a=adult('ann','Ann');a['forms']={'a':{'id':'a'}}
        a['projects']=[{'id':'project1','object':'care','means':['CARE']}]
        exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_LINK_CONTEXTS'):
            admit(a,exp,'objective_1',[{'kind':'LINK_ACTIVITY','source':'a',
                 'target':'project1','contexts':'homeworkshop'}])

    def test_p063_project_cue_terms_must_not_be_string_misread_as_single_char_cues(self):
        from um_sorok_organism.development import admit, InvalidDevelopment
        a=adult('ann','Ann');exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_PROJECT_CUE_TERMS'):
            admit(a,exp,'objective_1',[{'kind':'ADD_PROJECT','project':{'object':'care',
                 'means':['CARE'],'cue_terms':'home'}}])

    def test_p063_trace_cue_terms_must_be_string_list(self):
        from um_sorok_organism.development import admit, InvalidDevelopment
        a=adult('ann','Ann');exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_TRACE_CUES'):
            admit(a,exp,'objective_1',[{'kind':'TRACE','cue_terms':'care','content':'tacit'}])

class R7PositiveAndAtomicBoundaries(unittest.TestCase):
    def test_p058_explicit_different_actor_in_real_roster_does_not_authorize(self):
        w,a=scene();w['institutions']['hall_board']['members']=['joann']
        result=resolve(w,a,Attempt('ann','OPEN_HALL'))
        self.assertEqual(result.status,'BLOCKED')
        self.assertEqual(w['sites']['hall']['access'],'controlled')

    def test_p062_scope_reorganization_string_refused_without_partial_psyche(self):
        from um_sorok_organism.development import admit
        a=adult('ann','Ann');a['forms']['form1']={'id':'form1','scope':{'locations':['home']}}
        exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        original=deepcopy(a)
        with self.assertRaisesRegex(ValueError,'INVALID_ACQUIRED_FORM_PARAMETERS'):
            admit(a,exp,'objective_1',[{'kind':'CHANGE_RECRUITMENT_SCOPE',
                            'form_id':'form1','new_scope':{'locations':'homeworkshop'}}])
        self.assertEqual(a,original)

    def test_p062_real_location_list_still_permits_acquired_form(self):
        from um_sorok_organism.psychodynamics import validate_tendencies
        validate_tendencies({'id':'form1','cues':['song'],'scope':{'locations':['home','hall'],'counterpart':'joann'}})

    def test_p063_reorganizing_project_with_bad_cues_cannot_mutate_prior_project(self):
        from um_sorok_organism.development import admit,InvalidDevelopment
        a=adult('ann','Ann');a['projects']=[{'id':'p1','object':'care','means':['CARE']}]
        exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        original=deepcopy(a)
        with self.assertRaisesRegex(InvalidDevelopment,'INVALID_PROJECT_CUE_TERMS'):
            admit(a,exp,'objective_1',[{'kind':'REORGANIZE_PROJECT',
                             'project_id':'p1','cue_terms':'home'}])
        self.assertEqual(a,original)

    def test_p063_typed_link_context_admitted_without_deleting_other_links(self):
        from um_sorok_organism.development import admit
        a=adult('ann','Ann');a['forms']={'a':{'id':'a'},'b':{'id':'b'}}
        exp={'actor':'ann','ref':'lived','participated':True,'perceived_cues':[]}
        receipt=admit(a,exp,'objective_1',[{'kind':'LINK_FORMS','source':'a','target':'b',
                                         'relation':'RECRUITS','contexts':['home','hall']}])
        self.assertEqual(a['links'][-1]['contexts'],['home','hall'])
        self.assertEqual(len(receipt),1)

if __name__=='__main__': unittest.main()
