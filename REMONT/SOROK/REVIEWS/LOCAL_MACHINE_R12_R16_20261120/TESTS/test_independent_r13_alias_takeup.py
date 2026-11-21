"""Independent exact-R13 negative receiving: same-event end-identity laundering.

Review-only adversarial tests. They are not a production repair or new R13 owner code.
"""
from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from um_sorok_organism.development import InvalidDevelopment, admit
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.types import adult, stable_id


class SameEventAliasTakeup(unittest.TestCase):
    def test_real_issued_trial_may_not_launder_identical_end_under_other_id(self):
        with tempfile.TemporaryDirectory() as temp:
            runtime=ConstitutiveRuntime(str(Path(temp)/'whole.sqlite'))
            try:
                runtime.initialize()
                runtime.background(280)
                runtime.step('nadia', requested_action='SING')
                first=runtime.snapshot('nadia')['possible_ends'][0]
                # A separate actual experience produces a second independent ID
                # for an equivalent provisional end, not a forged model history.
                def second_event(task,packet):
                    if task=='development' and packet['actor']['id']=='nadia':
                        seen=packet['experience']['perceived_cues']
                        self.assertTrue(seen)
                        return {'task':task,'candidates':[{
                            'kind':'NOTICE_POSSIBLE_END',
                            'perceived_cue_ref':seen[0]['id'],
                            'possible_object':first['possible_object'],
                            'possible_means':['SING'],
                            'cue_terms':first['cue_terms'],
                        }]}
                    return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'ok'}
                runtime.semantic=ValidatingSemanticService(CallbackLLMProvider(second_event))
                runtime.step('nadia',requested_action='SING')
                ends=runtime.snapshot('nadia')['possible_ends']
                self.assertEqual(len(ends),2)
                self.assertNotEqual(ends[0]['id'],ends[1]['id'])
                self.assertEqual(ends[0]['possible_object'],ends[1]['possible_object'])
                earlier_events=runtime.verify()['events']
                earlier_actor=deepcopy(runtime.snapshot('nadia'))
                def malicious(task,packet):
                    if task=='actor_attempt':
                        trial=next(t for t in packet['possible_end_trials']
                                   if t['possible_end_ref']==ends[0]['id'] and t['operation']=='SING')
                        return {'task':task,'possible_end_trial_id':trial['trial_id']}
                    if task=='development' and packet['actor']['id']=='nadia':
                        return {'task':task,'candidates':[{
                            'kind':'TAKE_UP_POSSIBLE_END',
                            'possible_end_ref':ends[1]['id'],
                            'means':['SING'],
                        }]}
                    return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'ok'}
                runtime.semantic=ValidatingSemanticService(CallbackLLMProvider(malicious))
                with self.assertRaises(InvalidDevelopment):
                    runtime.step('nadia')
                self.assertEqual(runtime.verify()['events'],earlier_events)
                self.assertEqual(runtime.snapshot('nadia'),earlier_actor)
                self.assertTrue(runtime.verify()['valid'])
            finally:
                runtime.close()

    def test_direct_owner_does_not_turn_current_issued_trial_into_other_durable_end(self):
        actor=adult('ann','Ann')
        actor['possible_ends']=[{
            'id':ref,'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
            'origin_event':f'earlier_{i}','experience_ref':f'lived_{i}',
            'actor_perceived_cue_ref':f'cue_{i}',
            'possible_object':'sing together','possible_means':['SING'],
            'cue_terms':['sing'],
        } for i,ref in enumerate(('end_a','end_b'))]
        ticket={'actor':'ann','as_of_clock':9,'possible_end_ref':'end_a',
                'operation':'SING','origin_event':'earlier_0',
                'origin_experience_ref':'lived_0','actor_project_ref':None}
        ticket['trial_id']=stable_id('end_trial',{'actor':'ann','clock':9,
                                'end':'end_a','operation':'SING'})
        experience={'actor':'ann','ref':'today_lived','participated':True,
                    'own_action':'SING','status':'PERFORMED',
                    'felt_enactment':{'attempted_operation':'SING'},
                    'perceived_cues':[]}
        before=deepcopy(actor)
        with self.assertRaises(InvalidDevelopment):
            admit(actor,experience,'today_event',[{'kind':'TAKE_UP_POSSIBLE_END',
                'possible_end_ref':'end_b','means':['SING']}],issued_trial=ticket)
        self.assertEqual(actor,before)

    def test_legitimate_later_nontrial_takeup_remains_available(self):
        actor=adult('ann','Ann')
        exp1={'actor':'ann','ref':'lived_one','participated':True,'own_action':'SING',
              'status':'PERFORMED','perceived_cues':[{'id':'sign_one'}]}
        admit(actor,exp1,'event_one',[{'kind':'NOTICE_POSSIBLE_END',
            'perceived_cue_ref':'sign_one','possible_object':'make music with someone',
            'possible_means':['SING'],'cue_terms':['song']}])
        ref=actor['possible_ends'][0]['id']
        exp2={'actor':'ann','ref':'lived_two','participated':True,'own_action':'SING',
              'status':'PERFORMED','perceived_cues':[{'id':'sign_two'}]}
        r=admit(actor,exp2,'event_two',[{'kind':'TAKE_UP_POSSIBLE_END',
            'possible_end_ref':ref,'later_perceived_cue_ref':'sign_two','means':['SING']}])
        self.assertEqual(r[0]['kind'],'TAKE_UP_POSSIBLE_END')
        self.assertEqual(actor['projects'][-1]['origin'],['event_one','event_two'])

    def test_r13_cue_provenance_invalid_false_does_not_commit(self):
        with tempfile.TemporaryDirectory() as temp:
            runtime=ConstitutiveRuntime(str(Path(temp)/'life.sqlite'))
            try:
                runtime.initialize()
                events=runtime.verify()['events']
                for invalid in (False,'',{},(),[None]):
                    with self.subTest(invalid=invalid):
                        with self.assertRaises(ValueError):
                            runtime.cue('nadia',kind='contact',tags=invalid)
                        self.assertEqual(runtime.verify()['events'],events)
            finally:
                runtime.close()

    def test_legitimate_current_trial_without_take_up_stays_provisional(self):
        actor=adult('ann','Ann')
        actor['possible_ends']=[{'id':'end_a','status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
                                'origin_event':'event_one','experience_ref':'lived_one',
                                'actor_perceived_cue_ref':'cue_one',
                                'possible_object':'keep singing','possible_means':['SING'],
                                'cue_terms':['sing']}]
        ticket={'actor':'ann','as_of_clock':9,'possible_end_ref':'end_a',
                'operation':'SING','origin_event':'event_one',
                'origin_experience_ref':'lived_one','actor_project_ref':None,
                'trial_id':stable_id('end_trial',{'actor':'ann','clock':9,
                                          'end':'end_a','operation':'SING'})}
        exp={'actor':'ann','ref':'lived_two','participated':True,'own_action':'SING',
             'status':'PERFORMED','felt_enactment':{'attempted_operation':'SING'},
             'perceived_cues':[]}
        r=admit(actor,exp,'event_two',[],issued_trial=ticket)
        self.assertEqual(r[0]['kind'],'RECORD_POSSIBLE_END_TRIAL')
        self.assertEqual(actor['possible_ends'][0]['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertEqual(actor['projects'],[])


if __name__=='__main__':unittest.main()
