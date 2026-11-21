"""REMONT R11 real trial before motive, no retrospective model authority."""
import copy
import tempfile
import unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider, ValidatingSemanticService
from um_sorok_organism.types import adult, newborn, stable_id
from um_sorok_organism.constitution import materialize, actor_access, compose
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.prospective_horizon import project_trial_horizons


class R11ProspectiveRuntime(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.db=str(Path(self.tmp.name)/'organism.db')
        self.rt=ConstitutiveRuntime(self.db)
        self.addCleanup(self.rt.close)
        self.rt.initialize()

    def initial_end(self):
        self.rt.background(280)
        self.rt.step('nadia',requested_action='SING')
        possible=self.rt.snapshot('nadia')['possible_ends']
        self.assertEqual(len(possible),1)
        self.assertEqual(possible[0]['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertEqual(len([p for p in self.rt.snapshot('nadia')['projects'] if 'rhythm' in p['object']]),0)
        return possible[0]

    def trial_callback(self,task,packet):
        if task=='actor_attempt':
            candidates=packet['possible_end_trials']
            self.assertTrue(candidates)
            picked=next((t for t in candidates if t['operation']=='SING'),candidates[0])
            return {'task':task,'possible_end_trial_id':picked['trial_id']}
        if task=='development':
            return {'task':task,'candidates':[]}
        return {'task':task,'surface':'no privileged knowledge'}

    def test_real_world_trial_event_and_cold_reopen(self):
        first=self.initial_end()
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(self.trial_callback))
        before=self.rt.ledger.world()[1]['clock']
        plan=self.rt.plan('nadia')
        ticket=plan.practical_selection['possible_end_trial']
        self.assertEqual(ticket['actor'],'nadia')
        self.assertEqual(ticket['possible_end_ref'],first['id'])
        self.assertEqual(ticket['as_of_clock'],before)
        self.assertEqual(plan.purpose_selection['status'],
                         'ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE')
        answer=self.rt.step('nadia')
        later=self.rt.snapshot('nadia')
        end=next(e for e in later['possible_ends'] if e['id']==first['id'])
        self.assertEqual(len(end['trial_history']),1)
        record=end['trial_history'][0]
        self.assertEqual(record['original_situated_trial_ref'],ticket['trial_id'])
        self.assertEqual(record['operation'],'SING')
        self.assertEqual(record['world_success_or_motive_fulfillment'],'NOT_INFERRED')
        self.assertEqual(end['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertFalse(any('rhythm' in p['object'] for p in later['projects']))
        self.assertTrue(self.rt.verify()['valid'])
        self.rt.close()
        reopened=ConstitutiveRuntime(self.db)
        self.assertTrue(reopened.verify()['valid'])
        self.assertEqual(reopened.snapshot('nadia')['possible_ends'][0]['trial_history'],
                         end['trial_history'])
        reopened.close()

    def test_external_injection_never_issues_trial_even_if_eligible(self):
        first=self.initial_end()
        self.rt.step('nadia',requested_action='SING')
        # The historical fallback may separately take up an end; it never
        # rewrites the injected operation into a prospective actor choice.
        end=next(e for e in self.rt.snapshot('nadia')['possible_ends'] if e['id']==first['id'])
        self.assertEqual(end.get('trial_history',[]),[])

    def test_model_can_select_valid_trial_by_id_but_not_unknown(self):
        self.initial_end()
        def callback(task,packet):
            if task=='actor_attempt':return {'task':task,'possible_end_trial_id':'invented_999'}
            return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'ok'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        start=self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(ValueError,'UNISSUED_OR_AMBIGUOUS_POSSIBLE_END_TRIAL'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],start)

    def test_model_selected_established_project_cannot_coincide_with_trial(self):
        self.initial_end()
        def callback(task,packet):
            if task=='actor_attempt':
                ticket=packet['possible_end_trials'][0]
                return {'task':task,'action':ticket['operation'],
                        'possible_end_trial_id':ticket['trial_id'],
                        'project_id':'project:ordinary_life'}
            return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'ok'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        start=self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(ValueError,'PROVISIONAL_TRIAL_CANNOT_ASSERT_ESTABLISHED_PROJECT'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],start)

    def test_mismatched_operation_from_trial_is_refused(self):
        self.initial_end()
        def callback(task,packet):
            if task=='actor_attempt':
                ticket=packet['possible_end_trials'][0]
                return {'task':task,'possible_end_trial_id':ticket['trial_id'],'action':'REST'}
            return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'ok'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        with self.assertRaisesRegex(ValueError,'POSSIBLE_END_TRIAL_OPERATION_CONFLICT'):
            self.rt.step('nadia')

    def test_two_actor_turns_after_initial_history_have_no_extra_issuer(self):
        self.initial_end()
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(self.trial_callback))
        self.rt.step('nadia')
        end=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(len(end['trial_history']),1)
        self.rt.step('nadia')
        after=self.rt.snapshot('nadia')['possible_ends'][0]
        self.assertEqual(len(after['trial_history']),2)
        self.assertNotEqual(after['trial_history'][0]['event_ref'],after['trial_history'][1]['event_ref'])
        self.assertTrue(self.rt.verify()['valid'])


class R11ProspectiveComposition(unittest.TestCase):
    def fixture(self):
        actor=adult('a','Actor')
        actor['possible_ends']=[{'id':'end_a','status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
            'origin_event':'old_event_a','experience_ref':'old_exp_a',
            'actor_perceived_cue_ref':'old_cue_a','possible_means':['SING','PRACTICE'],
            'cue_terms':['sing'],'possible_object':'possible rhythm'}]
        from um_sorok_organism.types import blank_world
        w=blank_world();w['positions']={'a':'home'};w['clock']=5
        w['cues']=[{'id':'visible','clock':5,'last_access_clock':5,
            'kind':'performed_sing','tags':['sing'],'location':'home',
            'modality':'auditory','threshold':.05,'private_to':None}]
        actor['forms']['sing_skill']={'id':'sing_skill','kind':'PRACTICE','lifecycle':'ACTIVE',
            'cues':['sing'],'enables':['SING','PRACTICE'],'strength':.8,'body_min':.1,'scope':{}}
        return actor,w

    def test_eligible_operations_only_and_clock_actor_bound(self):
        actor,w=self.fixture();s=compose(materialize(actor,w),actor_access(actor,w))
        for o in s.candidate_actions:
            for t in o.get('possible_end_trials',[]):
                self.assertEqual(t['actor'],'a');self.assertEqual(t['as_of_clock'],5)
                self.assertEqual(t['operation'],o['action'])
        offered=[t for o in s.candidate_actions for t in o.get('possible_end_trials',[])]
        self.assertEqual({t['operation'] for t in offered},{'SING','PRACTICE'})
        self.assertTrue(any(c['kind']=='POSSIBLE_END_RECRUITS_PROSPECTIVE_TRIALS' for c in s.currents))

    def test_unobserved_sign_or_wrong_actor_cannot_project_trial(self):
        actor,w=self.fixture();w['cues']=[]
        s=compose(materialize(actor,w),actor_access(actor,w))
        self.assertFalse(any(o.get('possible_end_trials') for o in s.candidate_actions))
        self.assertFalse(any(c['kind']=='POSSIBLE_END_RECRUITS_PROSPECTIVE_TRIALS' for c in s.currents))
        from um_sorok_organism.types import AccessibleEncounter
        other=AccessibleEncounter('not_actor',w['clock'],'home',[],[],[])
        with self.assertRaisesRegex(ValueError,'PROSPECTIVE_ACTOR_IDENTITY_MISMATCH'):
            project_trial_horizons(materialize(actor,w),other,[])

    def test_repeated_history_makes_untried_means_distinguishable(self):
        actor,w=self.fixture()
        actor['possible_ends'][0]['trial_history']=[{'id':'prior_attempt','operation':'SING',
            'event_ref':'later_actual_event'}]
        s=compose(materialize(actor,w),actor_access(actor,w))
        trial={t['operation']:t for o in s.candidate_actions for t in o.get('possible_end_trials',[])}
        self.assertTrue(trial['SING']['prior_mean_attempted'])
        self.assertTrue(trial['PRACTICE']['recognized_open_means_contrast'])
        self.assertEqual(trial['PRACTICE']['actual_prior_trial_history_refs'],['prior_attempt'])

    def test_unissued_model_trial_rejected_atomically_even_in_batch(self):
        actor,_=self.fixture();old=copy.deepcopy(actor)
        experienced={'actor':'a','ref':'exp','own_action':'SING','participated':True,
           'felt_enactment':{'attempted_operation':'SING'},'perceived_cues':[], 'status':'PERFORMED'}
        with self.assertRaisesRegex(InvalidDevelopment,'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(actor,experienced,'new_event',[
                {'kind':'NO_CHANGE'},
                {'kind':'RECORD_POSSIBLE_END_TRIAL','trial':{
                  'actor':'a','possible_end_ref':'end_a','operation':'SING'}}])
        self.assertEqual(actor,old)

    def test_no_two_trials_same_event_even_if_different_ends(self):
        actor,_=self.fixture();actor['possible_ends'].append({
            **actor['possible_ends'][0],'id':'end_b','origin_event':'old_event_b',
            'experience_ref':'old_exp_b'})
        actor['possible_ends'][0]['trial_history']=[{'id':'registered','event_ref':'event_now',
                                                   'operation':'PRACTICE'}]
        before=copy.deepcopy(actor)
        experience={'actor':'a','ref':'exp-now','own_action':'SING','participated':True,
          'felt_enactment':{'attempted_operation':'SING'},'perceived_cues':[], 'status':'PERFORMED'}
        ticket={'actor':'a','trial_id':stable_id('end_trial', {
                'actor':'a','clock':5,'end':'end_b','operation':'SING'}),
            'as_of_clock':5,'operation':'SING',
            'possible_end_ref':'end_b','origin_event':'old_event_b',
            'origin_experience_ref':'old_exp_b','actor_project_ref':None}
        with self.assertRaisesRegex(InvalidDevelopment,'POSSIBLE_END_TRIAL_EVENT_ALREADY_CONSUMED'):
            admit(actor,experience,'event_now',[],issued_trial=ticket)
        self.assertEqual(actor,before)

if __name__=='__main__':unittest.main()

class R11NoMotiveFromCurrentTrial(unittest.TestCase):
    def test_heuristic_does_not_upgrade_current_trial_to_mature_project(self):
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/'trial.sqlite'))
            try:
                rt.initialize();rt.background(280)
                rt.step('nadia',requested_action='SING')
                from um_sorok_organism.semantics import HeuristicSemanticProvider
                heuristic=HeuristicSemanticProvider()
                def cb(task,packet):
                    if task=='actor_attempt':
                        trial=next(t for t in packet['possible_end_trials'] if t['operation']=='SING')
                        return {'task':task,'possible_end_trial_id':trial['trial_id']}
                    return heuristic.propose(task,packet)
                rt.semantic=ValidatingSemanticService(CallbackLLMProvider(cb))
                rt.step('nadia')
                state=rt.snapshot('nadia')
                self.assertEqual(state['possible_ends'][0]['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
                self.assertEqual(len(state['possible_ends'][0]['trial_history']),1)
                self.assertFalse(any('rhythm' in p['object'] for p in state['projects']))
            finally:rt.close()

class R11MotiveSpoofGuard(unittest.TestCase):
    def test_llm_cannot_promote_same_end_during_current_trial(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'x.sqlite'))
            try:
                rt.initialize();rt.background(280)
                rt.step('nadia',requested_action='SING')
                start=rt.ledger.world()[1]['clock']
                initial=rt.snapshot('nadia')['possible_ends'][0]
                def malicious(task,packet):
                    if task=='actor_attempt':
                        t=next(x for x in packet['possible_end_trials'] if x['operation']=='SING')
                        return {'task':task,'possible_end_trial_id':t['trial_id']}
                    if task=='development':
                        return {'task':task,'candidates':[{
                           'kind':'TAKE_UP_POSSIBLE_END','possible_end_ref':initial['id'],
                           'means':['SING'],'priority':.5}]}
                    return {'task':task,'surface':'undetermined'}
                rt.semantic=ValidatingSemanticService(CallbackLLMProvider(malicious))
                with self.assertRaisesRegex(InvalidDevelopment,'CURRENT_TRIAL_NOT_MATURE_MOTIVE'):
                    rt.step('nadia')
                self.assertEqual(rt.ledger.world()[1]['clock'],start)
                self.assertEqual(rt.snapshot('nadia')['possible_ends'][0],initial)
            finally:rt.close()

class R11IngressContract(unittest.TestCase):
    def test_practical_option_id_only_selects_operation_but_unissued_id_is_refused(self):
        # R3 deliberately implemented typed practical-option issuance after R11.
        # The old R11 service-level rejection is now a superseded interface,
        # not permission to forge a practical option in the runtime.
        callback=ValidatingSemanticService(CallbackLLMProvider(
            lambda task,packet:{'task':task,'practical_option_id':'fictionally_named'}))
        proposal=callback.proposal('actor_attempt',{'options':[]})
        self.assertEqual(proposal['practical_option_id'],'fictionally_named')
        self.rt.semantic=callback
        before=self.rt.verify()['events']
        with self.assertRaisesRegex(ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
            self.rt.step('nadia')
        self.assertEqual(self.rt.verify()['events'],before)

    def test_direct_forged_trial_kwarg_rejected_without_issued_identity(self):
        a=adult('a','A')
        a['possible_ends']=[{'id':'end1','origin_event':'old',
           'experience_ref':'exp:old','possible_means':['SING'],
           'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE'}]
        original=copy.deepcopy(a)
        exp={'actor':'a','ref':'exp:new','own_action':'SING','participated':True,
             'status':'PERFORMED','perceived_cues':[],
             'felt_enactment':{'attempted_operation':'SING'}}
        with self.assertRaisesRegex(InvalidDevelopment,'UNISSUED_POSSIBLE_END_TRIAL'):
            admit(a,exp,'objective-new',[],issued_trial={'actor':'a',
                'trial_id':'forged_after_event','as_of_clock':4,'operation':'SING',
                'possible_end_ref':'end1','origin_event':'old',
                'origin_experience_ref':'exp:old'})
        self.assertEqual(a,original)

class R11ConflictingOption(unittest.TestCase):
    def test_trial_and_unimplemented_practical_option_cannot_be_pooled(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'selection.sqlite'))
            try:
                rt.initialize();rt.background(280)
                rt.step('nadia',requested_action='SING')
                before=rt.ledger.world()[1]['clock']
                def cb(task,packet):
                    if task=='actor_attempt':
                        trial=packet['possible_end_trials'][0]
                        return {'task':task,'possible_end_trial_id':trial['trial_id'],
                                'practical_option_id':'fabricated_dual_selection'}
                    return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'none'}
                rt.semantic=ValidatingSemanticService(CallbackLLMProvider(cb))
                with self.assertRaisesRegex(ValueError,'POSSIBLE_END_TRIAL_SELECTION_CONFLICT'):
                    rt.step('nadia')
                self.assertEqual(rt.ledger.world()[1]['clock'],before)
            finally:rt.close()
