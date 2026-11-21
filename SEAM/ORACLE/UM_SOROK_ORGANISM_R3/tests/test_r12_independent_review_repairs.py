"""REMONT R12: reviewer first-fault repairs plus positive nontrial genesis."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.types import adult


class TrialPurposeAuthorityR12(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
        self.runtime=ConstitutiveRuntime(str(Path(self.t.name)/'world.sqlite'))
        self.addCleanup(self.runtime.close)
        self.runtime.initialize()
        self.runtime.background(280)
        self.runtime.step('nadia',requested_action='SING')
        self.earlier_end=self.runtime.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(self.earlier_end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')

    def provider(self, *, project_object, project_motive, append_other_effect=False):
        end=self.earlier_end
        def callback(task,packet):
            if task=='actor_attempt':
                ticket=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':ticket['trial_id']}
            if task=='development':
                candidates=[{'kind':'ADD_PROJECT','project':{
                    'object':project_object,'means':['SING'],'motive':project_motive,
                    'cue_terms':['sing'],'priority':.8}}]
                if append_other_effect:
                    candidates.insert(0,{'kind':'TRACE','content':'unrelated provisional response',
                                          'cue_terms':['sing']})
                return {'task':task,'candidates':candidates}
            return {'task':task,'surface':'public only'}
        return ValidatingSemanticService(CallbackLLMProvider(callback))

    def test_same_trial_relabel_as_exact_possible_object_rejected_atomically(self):
        rt=self.runtime
        rt.semantic=self.provider(project_object=self.earlier_end['possible_object'],
                                  project_motive='MATURE_RHYTHM_MOTIVE')
        pre_clock=rt.ledger.world()[1]['clock']
        pre_ends=deepcopy(rt.snapshot('nadia')['possible_ends'])
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT'):
            rt.step('nadia')
        self.assertEqual(rt.ledger.world()[1]['clock'],pre_clock)
        self.assertEqual(rt.snapshot('nadia')['possible_ends'],pre_ends)
        self.assertTrue(rt.verify()['valid'])

    def test_same_trial_cannot_relabel_object_to_avoid_guard(self):
        rt=self.runtime
        rt.semantic=self.provider(project_object='become a lifelong singer',
                                  project_motive='MATURE_UNRELATED_LABEL_FOR_SAME_TRIAL')
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT'):
            rt.step('nadia')
        self.assertFalse(any(p.get('motive')=='MATURE_UNRELATED_LABEL_FOR_SAME_TRIAL'
                             for p in rt.snapshot('nadia')['projects']))

    def test_earlier_trace_candidate_does_not_survive_rejected_later_project(self):
        rt=self.runtime
        rt.semantic=self.provider(project_object='rename the current trial as future life',
                                  project_motive='UNISSUED_MOTIVE',append_other_effect=True)
        pre=deepcopy(rt.snapshot('nadia'))
        with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT'):
            rt.step('nadia')
        after=rt.snapshot('nadia')
        self.assertEqual(after['traces'],pre['traces'])
        self.assertEqual(after['possible_ends'],pre['possible_ends'])

    def test_other_nontrial_event_may_admit_actor_specific_new_project(self):
        # No issued trial ticket; an independently experienced later event
        # may still support a *provisional* project through existing admission.
        actor=adult('ann','Ann')
        exp={'actor':'ann','ref':'experience_event2','participated':True,
             'own_action':'SING','status':'PERFORMED','perceived_cues':[]}
        r=admit(actor,exp,'different_event_from_prior_experience',[
             {'kind':'ADD_PROJECT','project':{'object':'care at home',
                         'means':['CARE'],'motive':'TENTATIVE_CARE_INTEREST'}}])
        self.assertEqual(len(r),1)
        self.assertEqual(actor['projects'][-1]['motive'],'TENTATIVE_CARE_INTEREST')
        self.assertEqual(actor['projects'][-1]['origin'],['different_event_from_prior_experience'])

    def test_subsequent_tried_means_do_not_prove_motive_on_success(self):
        rt=self.runtime
        def callback(task,packet):
            if task=='actor_attempt':
                ticket=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                return {'task':task,'possible_end_trial_id':ticket['trial_id']}
            if task=='development':return {'task':task,'candidates':[]}
            return {'task':task,'surface':'ok'}
        rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        rt.step('nadia')
        end=rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(len(end['trial_history']),1)
        self.assertEqual(end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertFalse(any('rhythm' in p.get('object','') for p in rt.snapshot('nadia')['projects']))
        self.assertTrue(rt.verify()['valid'])

if __name__=='__main__': unittest.main()
