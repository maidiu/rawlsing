"""REMONTATHON R13: first-red trial motive laundering and cue provenance integrity."""
from copy import deepcopy
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.types import adult, stable_id


class TrialProjectReorganizationR13(unittest.TestCase):
    def setUp(self):
        self.actor=adult('ann','Ann')
        self.actor['projects']=[{'id':'existing','object':'care in household','means':['CARE'],
                                  'motive':'TENTATIVE_CARE','status':'dormant',
                                  'priority':.3,'cue_terms':['care']}]
        self.end={'id':'maybe_rhythm','status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
                  'origin_event':'origin_event1','experience_ref':'first_lived',
                  'possible_means':['SING'],'cue_terms':['sing'],
                  'possible_object':'rhythm in home'}
        self.actor['possible_ends']=[deepcopy(self.end)]
        self.ticket={'actor':'ann','as_of_clock':9,'possible_end_ref':'maybe_rhythm',
                     'operation':'SING','origin_event':'origin_event1',
                     'origin_experience_ref':'first_lived','actor_project_ref':None}
        self.ticket['trial_id']=stable_id('end_trial',{'actor':'ann','clock':9,
                                       'end':'maybe_rhythm','operation':'SING'})
        self.exp={'actor':'ann','ref':'second_lived','participated':True,
                  'own_action':'SING','status':'PERFORMED',
                  'felt_enactment':{'attempted_operation':'SING'},
                  'perceived_cues':[]}

    def test_r13_same_trial_cannot_relabel_existing_project_as_new_enduring_motive(self):
        pre=deepcopy(self.actor)
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_REORGANIZE_DURABLE_PROJECT'):
            admit(self.actor,self.exp,'distinct_event2',[{'kind':'REORGANIZE_PROJECT',
                    'project_id':'existing','motive':'MATURE_RHYTHM_FROM_ONE_TRIAL',
                    'object':'my lifelong singing','means':['SING'],'status':'active'}],
                  issued_trial=self.ticket)
        self.assertEqual(self.actor,pre)

    def test_r13_same_trial_cannot_enable_dormant_project_through_status(self):
        pre=deepcopy(self.actor)
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_REORGANIZE_DURABLE_PROJECT'):
            admit(self.actor,self.exp,'distinct_event2',[{'kind':'REORGANIZE_PROJECT',
                    'project_id':'existing','status':'active','priority':999}],
                  issued_trial=self.ticket)
        self.assertEqual(self.actor,pre)

    def test_r13_distinct_nontrial_event_can_still_reorganize_existing_project(self):
        result=admit(self.actor,self.exp,'distinct_nontrial_event',[{'kind':'REORGANIZE_PROJECT',
                     'project_id':'existing','motive':'REVISABLE_NEW_PROJECT_REASON',
                     'status':'active'}])
        self.assertEqual(len(result),1)
        self.assertEqual(self.actor['projects'][0]['motive'],'REVISABLE_NEW_PROJECT_REASON')
        self.assertEqual(self.actor['projects'][0]['status'],'active')

    def test_r13_current_trial_witness_with_no_durable_project_change_still_admitted(self):
        r=admit(self.actor,self.exp,'distinct_event2',[],issued_trial=self.ticket)
        self.assertEqual(r[0]['kind'],'RECORD_POSSIBLE_END_TRIAL')
        self.assertEqual(len(self.actor['possible_ends'][0]['trial_history']),1)
        self.assertEqual(self.actor['projects'][0]['status'],'dormant')

    def test_r13_runtime_trial_reorganization_rejected_without_partial_ledger_event(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'life.sqlite'))
            try:
                rt.initialize();rt.background(280);rt.step('nadia',requested_action='SING')
                # Explicit fixture: an EXISTING project unrelated to the end, not
                # an inferred project or a generated psychological motive.
                v,w=rt.ledger.world();actors=rt.ledger.actors()
                av={aid:rt.ledger.actor(aid)[0] for aid in actors}
                actors['nadia']['projects'].append(deepcopy(self.actor['projects'][0]))
                rt.ledger.commit(rt.world_id,v,w,actors,av,'EXPLICIT_R13_TEST_SETUP',None,
                         {'grade':'TEST_FIXTURE_NONSCIENTIFIC'})
                start=rt.verify()['events'];project_pre=deepcopy(rt.snapshot('nadia')['projects'])
                def f(task,packet):
                    if task=='actor_attempt':
                        t=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                        return {'task':task,'possible_end_trial_id':t['trial_id']}
                    if task=='development':
                        return {'task':task,'candidates':[{'kind':'REORGANIZE_PROJECT',
                          'project_id':'existing','object':'mature sung purpose',
                          'motive':'UNISSUED_FROM_CURRENT_TRIAL','means':['SING'],'status':'active'}]}
                    return {'task':task,'surface':'ok'}
                rt.semantic=ValidatingSemanticService(CallbackLLMProvider(f))
                with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_REORGANIZE_DURABLE_PROJECT'):
                    rt.step('nadia')
                self.assertEqual(rt.verify()['events'],start)
                self.assertEqual(rt.snapshot('nadia')['projects'],project_pre)
                self.assertFalse(rt.snapshot('nadia')['possible_ends'][0].get('trial_history'))
            finally:rt.close()


class CueInputR13(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.rt=ConstitutiveRuntime(str(Path(self.temp.name)/'life.sqlite'))
        self.addCleanup(self.rt.close)
        self.rt.initialize()

    def test_r13_false_tag_input_must_not_silently_become_cue_of_kind(self):
        before=self.rt.verify()['events']
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
            self.rt.cue('nadia',kind='secret_contact',tags=False)
        self.assertEqual(self.rt.verify()['events'],before)

    def test_r13_empty_string_tag_input_must_not_silently_become_cue_of_kind(self):
        before=self.rt.verify()['events']
        with self.assertRaisesRegex(ValueError,'INVALID_CUE_TAGS'):
            self.rt.cue('nadia',kind='signal',tags='')
        self.assertEqual(self.rt.verify()['events'],before)

    def test_r13_explicit_empty_tags_stay_empty_without_inventing_kind_tag(self):
        result=self.rt.cue('nadia',kind='signal',tags=[])
        self.assertEqual(result['cue']['tags'],[])
        self.assertTrue(self.rt.verify()['valid'])

    def test_r13_absent_tags_keeps_documented_default(self):
        result=self.rt.cue('nadia',kind='signal')
        self.assertEqual(result['cue']['tags'],['signal'])
        self.assertTrue(self.rt.verify()['valid'])

if __name__=='__main__':unittest.main()
