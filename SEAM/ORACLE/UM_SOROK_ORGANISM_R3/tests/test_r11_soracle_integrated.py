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
        # The current owner first refuses the unowned/non-situated project
        # identity, before an otherwise valid provisional trial can be
        # interpreted as an attained project. Both are rejection, not success.
        with self.assertRaisesRegex(ValueError,'MODEL_SELECTED_PURPOSE_NOT_SITUATED_ELIGIBLE'):
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


class DissimilarMeansR34(unittest.TestCase):
    def test_new_means_is_lived_local_one_use_and_changes_future(self):
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        from um_sorok_organism.functional_correspondence import (
            propose_actor_lived_correspondences)
        parent={'source_ref':'r34_fictional_parent',
                'source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
                'answers':{'R34':'not a respondent'},'fictional_seed':{'projects':[]}}
        with tempfile.TemporaryDirectory() as d:
            outcomes={}
            for nominate in (True,False):
                offered=[]
                def callback(task,packet):
                    if task=='adult_constructor':
                        return HeuristicSemanticProvider().propose(task,packet)
                    if task=='expression':
                        return {'task':task,'surface':'Ordinary life.'}
                    if task=='actor_attempt':
                        trials=packet.get('possible_end_trials',[])
                        pick=next((x for x in trials if x['operation']=='EAT'),None)
                        if pick is None:
                            pick=next((x for x in trials if x['operation']=='REST'),None)
                        if pick:
                            return {'task':task,'possible_end_trial_id':pick['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task!='development':raise AssertionError(task)
                    if packet['actor']['id']!='mother':
                        return {'task':task,'candidates':[]}
                    e=packet['experience']
                    if e.get('own_action')=='REST' and not packet.get('actor_possible_ends'):
                        sign=next(c for c in e['perceived_cues'] if c['kind']=='performed_rest')
                        return {'task':task,'candidates':[
                            {'kind':'ADD_FORM','form':{'id':'r34_eat','kind':'PRACTICE',
                              'cues':['eat'],'enables':['EAT'],'always_recruitable':True,'scope':{}}},
                            {'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':sign['id'],
                             'possible_object':'seek a respite from bodily strain',
                             'possible_means':['REST'],'cue_terms':['rest']}]}
                    gs=[g for g in packet.get('historically_proposed_functional',[])
                        if g.get('dissimilar_means_basis')]
                    offered.extend(copy.deepcopy(gs))
                    return {'task':task,'candidates':gs if nominate and len(offered)==len(gs) else []}
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                db=str(Path(d)/('admit.db' if nominate else 'abstain.db'))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.initialize([('mother','Mother',parent)])
                    rt.step('mother',requested_action='MOVE',object_ref='workshop')
                    rt.step('mother',requested_action='REST')
                    self.assertEqual(rt.step('mother')['attempt'],'REST')
                    prior=rt.snapshot('mother')['possible_ends'][0]
                    self.assertEqual(len(prior['trial_history']),1)
                    rt.step('mother',requested_action='MOVE',object_ref='home')
                    self.assertEqual(rt.step('mother',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    basis=offered[0]['dissimilar_means_basis']
                    self.assertEqual((basis['earlier_operation'],basis['later_operation']),('REST','EAT'))
                    self.assertIn('comfort',basis['shared_lived_relief_axes'])
                    after=rt.snapshot('mother')
                    self.assertEqual(after['possible_ends'][0],prior)
                    bindings=[b for b in after['functional_bindings'] if b.get('dissimilar_means_basis')]
                    self.assertEqual(len(bindings),int(nominate))
                    if not nominate:
                        actor=rt.ledger.actor('mother')[1]
                        episode=next(x for x in actor['lived_genesis_episodes'] if x['id']==basis['later_episode_ref'])
                        sign=next(c for c in rt.see('mother')['cues'] if c['id']==offered[0]['perceived_cue_ref'])
                        experience={'actor':'mother','ref':episode['experience_ref'],
                            'clock':episode['clock'],'location':'home','own_action':'EAT',
                            'participated':True,'felt_enactment':{'attempted_operation':'EAT'},
                            'perceived_cues':[sign]}
                        bad=copy.deepcopy(offered[0]);bad['dissimilar_means_basis']['shared_lived_relief_axes']=['fabricated']
                        old=copy.deepcopy(actor)
                        with self.assertRaises(InvalidDevelopment):
                            admit(actor,experience,episode['event_ref'],[bad])
                        self.assertEqual(actor,old)
                        self.assertEqual(len(propose_actor_lived_correspondences(actor,experience,episode['event_ref'])),1)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.snapshot('mother')['functional_bindings'],after['functional_bindings'])
                    result=cold.step('mother')
                    outcomes[nominate]=result['attempt']
                    end=cold.snapshot('mother')['possible_ends'][0]
                    self.assertEqual(end['possible_means'],['REST'])
                    self.assertEqual(len(end['trial_history']),1+int(nominate))
                    if nominate:
                        self.assertEqual(end['trial_history'][-1]['operation'],'EAT')
                        self.assertEqual(end['trial_history'][-1]['functional_bridge_ref'],bindings[0]['id'])
                        self.assertFalse(any(t.get('functional_bridge_ref')==bindings[0]['id']
                            for o in cold.situated('mother')['candidate_actions']
                            for t in o.get('possible_end_trials',[])))
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(outcomes,{True:'EAT',False:'WAIT'})

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
        with tempfile.TemporaryDirectory() as directory:
            rt=ConstitutiveRuntime(str(Path(directory)/'r11_option_ingress.sqlite3'))
            try:
                rt.initialize()
                rt.semantic=callback
                before=rt.verify()['events']
                with self.assertRaisesRegex(
                        ValueError,'UNKNOWN_OR_AMBIGUOUS_PRACTICAL_OPTION_ID'):
                    rt.step('nadia')
                self.assertEqual(rt.verify()['events'],before)
            finally:
                rt.close()

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


class FunctionalAfterlifeR35(unittest.TestCase):
    def test_consumed_bridge_can_consolidate_then_be_suspended_without_erasure(self):
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        parent={'source_ref':'r35_fictional_parent',
                'source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
                'answers':{'R35':'not a respondent'},'fictional_seed':{'projects':[]}}
        with tempfile.TemporaryDirectory() as d:
            outcomes={}
            for consolidate in (True,False):
                acquired=[]; revisions=[]
                def callback(task,packet):
                    if task=='adult_constructor':
                        return HeuristicSemanticProvider().propose(task,packet)
                    if task=='expression':
                        return {'task':task,'surface':'Ordinary life.'}
                    if task=='actor_attempt':
                        trials=packet.get('possible_end_trials',[])
                        pick=next((x for x in trials if x['operation']=='EAT'),None)
                        if pick is None:
                            pick=next((x for x in trials if x['operation']=='REST'),None)
                        if pick:
                            return {'task':task,'possible_end_trial_id':pick['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task!='development':raise AssertionError(task)
                    if packet['actor']['id']!='mother':
                        return {'task':task,'candidates':[]}
                    e=packet['experience']
                    if e.get('own_action')=='REST' and not packet.get('actor_possible_ends'):
                        sign=next(c for c in e['perceived_cues'] if c['kind']=='performed_rest')
                        return {'task':task,'candidates':[
                            {'kind':'ADD_FORM','form':{'id':'r35_eat','kind':'PRACTICE',
                              'cues':['eat'],'enables':['EAT'],'always_recruitable':True,'scope':{}}},
                            {'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':sign['id'],
                             'possible_object':'seek a respite from bodily strain',
                             'possible_means':['REST'],'cue_terms':['rest']}]}
                    gs=[g for g in packet.get('historically_proposed_functional',[])
                        if g.get('dissimilar_means_basis')]
                    if gs and not acquired:
                        acquired.extend(copy.deepcopy(gs))
                        return {'task':task,'candidates':gs}
                    rs=packet.get('historically_possible_functional_revisions',[])
                    revisions.extend(copy.deepcopy(rs))
                    return {'task':task,'candidates':rs if consolidate else []}
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                db=str(Path(d)/('consolidate.db' if consolidate else 'abstain.db'))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.initialize([('mother','Mother',parent)])
                    rt.step('mother',requested_action='MOVE',object_ref='workshop')
                    rt.step('mother',requested_action='REST')
                    self.assertEqual(rt.step('mother')['attempt'],'REST')
                    rt.step('mother',requested_action='MOVE',object_ref='home')
                    self.assertEqual(rt.step('mother',requested_action='EAT')['status'],'PERFORMED')
                    bridge=next(b for b in rt.snapshot('mother')['functional_bindings']
                                if b.get('dissimilar_means_basis'))
                    self.assertEqual(rt.step('mother')['attempt'],'EAT')
                    self.assertEqual(revisions,[])
                    end=rt.snapshot('mother')['possible_ends'][0]
                    self.assertEqual(len(end['trial_history']),2)
                    self.assertFalse(any(t.get('functional_bridge_ref')==bridge['id']
                        for o in rt.situated('mother')['candidate_actions']
                        for t in o.get('possible_end_trials',[])))
                    # Real intervening activity lowers comfort; do not write
                    # a fabricated favorable body state or historical episode.
                    for _ in range(10):rt.step('mother',requested_action='WAIT')
                    self.assertEqual(rt.step('mother',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(revisions),1)
                    self.assertEqual(revisions[0]['mode'],'CONSOLIDATE')
                    self.assertIn('comfort',revisions[0]['revision_basis']['reproduced_relief_axes'])
                    before=rt.snapshot('mother')
                    b=next(b for b in before['functional_bindings'] if b['id']==bridge['id'])
                    self.assertEqual(b['status'],'ACQUIRED_CONDITIONAL_FUNCTIONAL_MEANS'
                                     if consolidate else 'POSSIBLE_FUNCTIONAL_SIMILARITY_NOT_BELIEF')
                    self.assertEqual(before['possible_ends'][0],end)
                    self.assertEqual(b['dissimilar_means_basis'],bridge['dissimilar_means_basis'])
                    if not consolidate:
                        actor=rt.ledger.actor('mother')[1]
                        rev=revisions[0]
                        row=next(x for x in actor['lived_genesis_episodes']
                                 if x['id']==rev['revision_basis']['later_episode_ref'])
                        sign=next(c for c in rt.see('mother')['cues']
                                  if c['id']==rev['revision_basis']['later_received_sign_ref'])
                        exp={'actor':'mother','ref':row['experience_ref'],'clock':row['clock'],
                             'location':'home','own_action':'EAT','participated':True,
                             'status':'PERFORMED','felt_enactment':{'attempted_operation':'EAT'},
                             'perceived_cues':[sign]}
                        forged=copy.deepcopy(rev)
                        forged['revision_basis']['first_bridge_trial_ref']='invented'
                        old=copy.deepcopy(actor)
                        with self.assertRaisesRegex(InvalidDevelopment,'FUNCTIONAL_REVISION_NO_LIVED_BASIS'):
                            admit(actor,exp,row['event_ref'],[forged])
                        self.assertEqual(actor,old)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.snapshot('mother')['functional_bindings'],before['functional_bindings'])
                    outcomes[consolidate]=cold.step('mother')['attempt']
                    if consolidate:
                        revision_ref=b['revision_history'][0]['id']
                        self.assertEqual(cold.snapshot('mother')['possible_ends'][0]['trial_history'][-1]
                                         ['conditional_means_revision_ref'],revision_ref)
                        self.assertEqual(cold.step('mother')['attempt'],'EAT')
                        # Consume actual finite household stock until the
                        # material world blocks an attempted course.
                        for _ in range(15):
                            result=cold.step('mother',requested_action='EAT')
                            if result['status']=='BLOCKED':break
                        self.assertEqual(result['status'],'BLOCKED')
                        self.assertEqual(revisions[-1]['mode'],'SUSPEND')
                        final=next(x for x in cold.snapshot('mother')['functional_bindings']
                                   if x['id']==bridge['id'])
                        self.assertEqual(final['status'],'SUSPENDED_CONDITIONAL_FUNCTIONAL_MEANS')
                        self.assertEqual([h['mode'] for h in final['revision_history']],
                                         ['CONSOLIDATE','SUSPEND'])
                        self.assertEqual(final['revision_history'][0],b['revision_history'][0])
                        self.assertEqual(final['dissimilar_means_basis'],bridge['dissimilar_means_basis'])
                        self.assertEqual(cold.snapshot('mother')['possible_ends'][0]['possible_means'],['REST'])
                        self.assertEqual(cold.step('mother')['attempt'],'WAIT')
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(outcomes,{True:'EAT',False:'WAIT'})



class UpstreamElasticEntranceR36(unittest.TestCase):
    def packet(self,kind='AUTHORED_WORLD_HISTORY'):
        return {'input_kind':kind,'source_ref':'fictional:life',
                'source_grade':'EXPLICIT_FICTIONAL_HISTORICAL_INPUT',
                'biographical_context':{'occupation':'weaver','history':'household and workshop'},
                'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE',
                    'content':'familiar household provisioning',
                    'cues':['food'],'enables':['EAT']}],
                    'projects':[{'object':'sustain household','means':['EAT']}]}}
    
    def test_same_runtime_without_survey_and_with_survey(self):
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        seen=[]
        def callback(task,packet):
            if task=='adult_constructor':seen.append(copy.deepcopy(packet))
            return HeuristicSemanticProvider().propose(task,packet)
        with tempfile.TemporaryDirectory() as d:
            for i,kind in enumerate(('THIN_BIOGRAPHY','AUTHORED_WORLD_HISTORY',
                                     'SUPPLIED_SURVEY_CONFIGURATION','SAMPLED_SURVEY_CONFIGURATION')):
                p=self.packet(kind)
                if kind.endswith('SURVEY_CONFIGURATION'):
                    p['answers']={'survey_q':'a'}
                    p['source_grade']='SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL'
                # Thin biography alone, no authored operative forms.
                if kind=='THIN_BIOGRAPHY':p.pop('fictional_seed')
                db=str(Path(d)/str(i))
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.initialize([('mother','Mother',p)])
                    a=rt.ledger.actor('mother')[1]
                    self.assertEqual(a['initialization']['input_kind'],kind)
                    self.assertEqual(a['initialization']['observed_question_count'],
                                     len(p.get('answers',{})))
                    self.assertTrue(a['projects'] or a['forms'])
                    self.assertEqual(rt.ledger.source('fictional_source:mother')['content'],p)
                    if not p.get('answers'):
                        self.assertFalse(any('asserted_answer' in f for f in a['forms'].values()))
                    self.assertEqual(rt.step('mother',requested_action='REST')['status'],'PERFORMED')
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                cold=ConstitutiveRuntime(db)
                try:
                    self.assertEqual(cold.ledger.actor('mother')[1]['initialization']['input_kind'],kind)
                    self.assertEqual(cold.ledger.source('fictional_source:mother')['content'],p)
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual([p['input_kind'] for p in seen],
                 ['THIN_BIOGRAPHY','AUTHORED_WORLD_HISTORY','SUPPLIED_SURVEY_CONFIGURATION','SAMPLED_SURVEY_CONFIGURATION'])
    
    def structural(self,value):
        return {'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY','source_ref':'fictional:world',
          'positions':[{'id':'position0','actor':'mother','field':'ration_access','value':'admitted',
                        'source_ref':'fictional:initial','effective_from':0,'effective_until':0},
                       {'id':'position1','actor':'mother','field':'ration_access','value':value,
                        'source_ref':'fictional:changed','effective_from':1,'effective_until':1}],
          'rules':[{'id':'ration_rule','operation':'EAT','location':'home',
                    'source_ref':'fictional:rule','effective_from':0,'effective_until':1,
                    'all_of':[{'kind':'RECORDED_POSITION','field':'ration_access','equals':'admitted'}]}]}
    
    def test_independent_temporal_structure_changes_actual_course_not_initial_psyche(self):
        with tempfile.TemporaryDirectory() as d:
            initial=[];courses={};states={}
            p=self.packet()
            for value in ('admitted','excluded'):
                db=str(Path(d)/value)
                spec=self.structural(value)
                rt=ConstitutiveRuntime(db)
                try:
                    rt.initialize([('mother','Mother',p)],authored_structural_history=spec)
                    initial.append(rt.ledger.actor('mother')[1])
                    self.assertEqual(rt.ledger.source('authored_structural_history')['content'],spec)
                    self.assertEqual(rt.step('mother',requested_action='EAT')['status'],'PERFORMED')
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                cold=ConstitutiveRuntime(db)
                try:
                    second=cold.step('mother',requested_action='EAT')
                    courses[value]=second['status']
                    states[value]=cold.ledger.actor('mother')[1]['body']
                    self.assertEqual(cold.ledger.world()[1]['material_gate_audit'][-1]
                         ['objective_rule_evaluation']['readset'],['fictional:rule'])
                    # At clock 2 the rule expires, not a psychological conversion.
                    self.assertEqual(cold.step('mother',requested_action='EAT')['status'],'PERFORMED')
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(initial[0],initial[1])
            self.assertEqual(courses,{'admitted':'PERFORMED','excluded':'BLOCKED'})
            self.assertNotEqual(states['admitted'],states['excluded'])
    
    def test_ambiguous_or_unqualified_inputs_refused_before_genesis(self):
        from um_sorok_organism.historical_parent_bridge import historically_conditioned_entrances
        p=self.packet()
        for bad in ({**p,'answers':{'fake':'a'}},
                    {**p,'source_grade':'NATIVE_PYAT'},
                    {**p,'biographical_context':{}},
                    {**p,'historically_supported_alternatives':[{}]*25}):
            with self.assertRaises(ValueError):historically_conditioned_entrances(bad)
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'invalid')
            rt=ConstitutiveRuntime(db)
            try:
                spec=self.structural('excluded')
                spec['positions'][1]['actor']='unknown'
                with self.assertRaisesRegex(ValueError,'STRUCTURAL_HISTORY_INVALID_POSITION'):
                    rt.initialize([('mother','Mother',p)],authored_structural_history=spec)
                self.assertEqual(rt.ledger.actors(),{})
                rt.initialize([('mother','Mother',p)])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()


class DependencyContrastR37(unittest.TestCase):
    def test_interrupted_learned_support_generates_new_prospective_means(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        with tempfile.TemporaryDirectory() as d:
            outcomes={}
            for nominate in (True,False):
                stage='first'
                offered=[]
                def callback(task,packet):
                    if task=='expression':
                        return {'task':task,'surface':'Ordinary activity.'}
                    if task=='actor_attempt':
                        if packet['actor']['id']=='mother':
                            return {'task':task,'action':'FEED' if stage=='supported' else 'REFUSE'}
                        if stage=='interrupted':
                            choices=[o for o in packet['practical_options']
                                     if o['operation']=='SIGNAL'
                                     and o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                                     and o['world_request']['addressed_party_ref']=='mother']
                            self.assertEqual(len(choices),1)
                            return {'task':task,'action':'SIGNAL','practical_option_id':choices[0]['option_id']}
                        if stage=='future':
                            ts=[t for t in packet.get('possible_end_trials',[])
                                if t['operation']=='EAT']
                            if ts:
                                return {'task':task,'possible_end_trial_id':ts[0]['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        if stage=='supported':
                            return {'task':task,'candidates':packet.get('historically_possible_joint_practices',[])}
                        gs=[g for g in packet.get('historically_possible_genetic_ends',[])
                            if g.get('dependency_loss_basis')]
                        offered.extend(copy.deepcopy(gs))
                        return {'task':task,'candidates':gs if nominate else []}
                    return HeuristicSemanticProvider().propose(task,packet)
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                db=str(Path(d)/str(nominate))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    a=adult('worker','Mara')
                    a['body']['nutrition']=.30
                    a['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
                        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
                        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
                        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}
                    mother=adult('mother','Mother')
                    mother['projects']=[{'id':'care','object':'ordinary care',
                                        'means':['FEED'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a,mother])
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PARTIAL')
                    stage='supported'
                    result=rt.step('worker',requested_action='SIGNAL',target='mother')
                    self.assertEqual(result['status'],'PERFORMED')
                    acquired=rt.ledger.actor('worker')[1]['joint_practices']
                    self.assertEqual(len(acquired),1)
                    self.assertEqual(len(rt.ledger.world()[1]['material_feeding_events']),1)
                    stage='interrupted'
                    result=rt.step('worker')
                    self.assertEqual((result['attempt'],result['status']),('SIGNAL','PARTIAL'))
                    self.assertEqual(len(rt.ledger.world()[1]['material_feeding_events']),1)
                    stage='independent'
                    self.assertEqual(rt.step('worker',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    basis=offered[0]['dependency_loss_basis']
                    self.assertEqual(basis['practice_ref'],acquired[0]['id'])
                    before=rt.ledger.actor('worker')[1]
                    self.assertEqual(before['joint_practices'],acquired)
                    ends=[e for e in before['possible_ends'] if e.get('dependency_loss_basis')]
                    self.assertEqual(len(ends),int(nominate))
                    if nominate:
                        self.assertEqual(ends[0]['possible_means'],['EAT'])
                        self.assertIsNone(ends[0]['addressed_party_ref'])
                        self.assertEqual(len(ends[0]['actual_contrasted_episode_refs']),3)
                    else:
                        episode=next(x for x in before['lived_genesis_episodes']
                                     if x['id']==basis['independent_episode_ref'])
                        sign=next(c for c in rt.see('worker')['cues']
                                  if c['id']==offered[0]['later_perceived_cue_ref'])
                        exp={'actor':'worker','ref':episode['experience_ref'],'clock':episode['clock'],
                             'location':'home','own_action':'EAT','participated':True,'status':'PERFORMED',
                             'felt_enactment':{'attempted_operation':'EAT'},'perceived_cues':[sign]}
                        forged=copy.deepcopy(offered[0])
                        forged['dependency_loss_basis']['historical_counterpart_ref']='invented'
                        old=copy.deepcopy(before)
                        with self.assertRaisesRegex(InvalidDevelopment,'GENESIS_DEPENDENCY_HISTORY_FORGERY'):
                            admit(before,exp,episode['event_ref'],[forged])
                        self.assertEqual(before,old)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                stage='future'
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    outcomes[nominate]=cold.step('worker')['attempt']
                    self.assertEqual(cold.ledger.actor('worker')[1]['joint_practices'],acquired)
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(outcomes,{True:'EAT',False:'WAIT'})



class DependencyProjectR38(unittest.TestCase):
    def test_later_independent_course_can_form_undertaking_without_owning_other(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        with tempfile.TemporaryDirectory() as d:
            final={}
            for takeup in (True,False):
                stage='first'; offered=[]
                def callback(task,packet):
                    if task=='actor_attempt':
                        if packet['actor']['id']=='mother':
                            return {'task':task,'action':'FEED' if stage=='supported' else 'REFUSE'}
                        if stage=='interrupted':
                            choices=[o for o in packet['practical_options']
                                     if o['operation']=='SIGNAL'
                                     and o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                                     and o['world_request']['addressed_party_ref']=='mother']
                            self.assertEqual(len(choices),1)
                            return {'task':task,'action':'SIGNAL','practical_option_id':choices[0]['option_id']}
                        if stage=='trial':
                            trials=[x for x in packet['possible_end_trials'] if x['operation']=='EAT']
                            self.assertEqual(len(trials),1)
                            return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
                        if stage=='revisit':
                            return {'task':task,'action':'EAT'}
                        if stage=='project':
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='EAT' and x.get('project_id') is not None]
                            if choices:
                                return {'task':task,'action':'EAT','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        if stage=='supported':
                            return {'task':task,'candidates':packet['historically_possible_joint_practices']}
                        if stage=='independent':
                            return {'task':task,'candidates':[g for g in packet['historically_possible_genetic_ends']
                                                               if g.get('dependency_loss_basis')]}
                        cs=packet.get('historically_possible_dependency_takeups',[])
                        if cs:offered.append((copy.deepcopy(cs),copy.deepcopy(packet['experience'])))
                        return {'task':task,'candidates':cs if takeup else []}
                    return HeuristicSemanticProvider().propose(task,packet)
                db=str(Path(d)/str(takeup)); service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    a=adult('worker','Mara');a['body']['nutrition']=.30
                    a['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
                        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
                        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
                        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}
                    mother=adult('mother','Mother')
                    mother['projects']=[{'id':'care','object':'ordinary care',
                                        'means':['FEED'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a,mother])
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PARTIAL')
                    stage='supported'
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PERFORMED')
                    practice=copy.deepcopy(rt.ledger.actor('worker')[1]['joint_practices'])
                    self.assertEqual(len(practice),1)
                    stage='interrupted'
                    self.assertEqual(rt.step('worker')['status'],'PARTIAL')
                    stage='independent'
                    self.assertEqual(rt.step('worker',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(rt.ledger.actor('worker')[1]['possible_ends']),1)
                    stage='trial'
                    self.assertEqual(rt.step('worker')['attempt'],'EAT')
                    self.assertEqual(offered,[])
                    trial_state=rt.ledger.actor('worker')[1]
                    self.assertEqual(trial_state['projects'],[])
                    self.assertEqual(len(trial_state['possible_ends'][0]['trial_history']),1)
                    stage='wait'
                    for _ in range(8):rt.step('worker')
                    self.assertEqual(offered,[])
                    stage='revisit'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    cs,exp=offered[0];self.assertEqual(len(cs),1)
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),int(takeup))
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(cs[0]['dependency_takeup_basis']['earlier_lived_trial_ref'],
                        trial_state['possible_ends'][0]['trial_history'][0]['id'])
                    if takeup:
                        p=a['projects'][0]
                        self.assertEqual(p['takeup_evidence']['dependency_takeup_basis'],cs[0]['dependency_takeup_basis'])
                        self.assertEqual(a['possible_ends'][0]['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
                        self.assertIsNone(p.get('addressed_party_ref'))
                    else:
                        bad=copy.deepcopy(cs[0])
                        bad['dependency_takeup_basis']['earlier_lived_trial_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=cs[0]['dependency_takeup_basis']['source_event_refs'][-1]
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_TAKEUP_NO_QUALIFIED_LATER_COURSE'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                stage='project'
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    final[takeup]=cold.step('worker')['attempt']
                    a=cold.ledger.actor('worker')[1]
                    if takeup:
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['operation'],'EAT')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['motive_realized'],
                                         'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                        # Exhaust actual shared food; the undertaking persists.
                        for _ in range(14):
                            out=cold.step('worker')
                            if out['status']=='BLOCKED':break
                        self.assertEqual(out['status'],'BLOCKED')
                        a=cold.ledger.actor('worker')[1]
                        self.assertEqual(a['projects'][0]['status'],'active')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['performed_status'],'BLOCKED')
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(final,{True:'EAT',False:'WAIT'})

class DependencyProjectReorganizationR39(unittest.TestCase):
    def test_obstructed_project_can_reorganize_around_renewed_conditional_cooperation(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        with tempfile.TemporaryDirectory() as d:
            final={}
            for reorganize in (True,False):
                takeup=True
                stage='first'; offered=[]; revisions=[]
                def callback(task,packet):
                    if task=='actor_attempt':
                        if packet['actor']['id']=='mother':
                            return {'task':task,'action':'FEED' if stage in ('supported','renewed','project_signal') else 'REFUSE'}
                        if stage in ('interrupted','renewed'):
                            choices=[o for o in packet['practical_options']
                                     if o['operation']=='SIGNAL'
                                     and o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                                     and o['world_request']['addressed_party_ref']=='mother']
                            self.assertEqual(len(choices),1)
                            return {'task':task,'action':'SIGNAL','practical_option_id':choices[0]['option_id']}
                        if stage in ('project_signal','project_refused'):
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='SIGNAL' and x.get('project_id') is not None
                                     and x.get('dependency_conditional_means_ref')]
                            if choices:
                                self.assertEqual(len(choices),1)
                                self.assertEqual(choices[0]['world_request']['addressed_party_ref'],'mother')
                                return {'task':task,'action':'SIGNAL','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                            return {'task':task,'action':'WAIT'}
                        if stage=='trial':
                            trials=[x for x in packet['possible_end_trials'] if x['operation']=='EAT']
                            self.assertEqual(len(trials),1)
                            return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
                        if stage=='revisit':
                            return {'task':task,'action':'EAT'}
                        if stage=='project':
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='EAT' and x.get('project_id') is not None]
                            if choices:
                                return {'task':task,'action':'EAT','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        if stage=='supported':
                            return {'task':task,'candidates':packet['historically_possible_joint_practices']}
                        if stage=='independent':
                            return {'task':task,'candidates':[g for g in packet['historically_possible_genetic_ends']
                                                               if g.get('dependency_loss_basis')]}
                        rs=packet.get('historically_possible_dependency_project_reorganizations',[])
                        if rs:revisions.append((copy.deepcopy(rs),copy.deepcopy(packet['experience'])))
                        if stage=='renewed':return {'task':task,'candidates':rs if reorganize else []}
                        cs=packet.get('historically_possible_dependency_takeups',[])
                        if cs:offered.append((copy.deepcopy(cs),copy.deepcopy(packet['experience'])))
                        return {'task':task,'candidates':cs if takeup else []}
                    return HeuristicSemanticProvider().propose(task,packet)
                db=str(Path(d)/str(reorganize)); service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    w['holdings']={'mother':{'food':3}}
                    a=adult('worker','Mara');a['body']['nutrition']=.30
                    a['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
                        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
                        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
                        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}
                    mother=adult('mother','Mother')
                    mother['projects']=[{'id':'care','object':'ordinary care',
                                        'means':['FEED'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a,mother])
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PARTIAL')
                    stage='supported'
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PERFORMED')
                    practice=copy.deepcopy(rt.ledger.actor('worker')[1]['joint_practices'])
                    self.assertEqual(len(practice),1)
                    stage='interrupted'
                    self.assertEqual(rt.step('worker')['status'],'PARTIAL')
                    stage='independent'
                    self.assertEqual(rt.step('worker',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(rt.ledger.actor('worker')[1]['possible_ends']),1)
                    stage='trial'
                    self.assertEqual(rt.step('worker')['attempt'],'EAT')
                    self.assertEqual(offered,[])
                    trial_state=rt.ledger.actor('worker')[1]
                    self.assertEqual(trial_state['projects'],[])
                    self.assertEqual(len(trial_state['possible_ends'][0]['trial_history']),1)
                    stage='wait'
                    for _ in range(8):rt.step('worker')
                    self.assertEqual(offered,[])
                    stage='revisit'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    cs,exp=offered[0];self.assertEqual(len(cs),1)
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),int(takeup))
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(cs[0]['dependency_takeup_basis']['earlier_lived_trial_ref'],
                        trial_state['possible_ends'][0]['trial_history'][0]['id'])
                    if takeup:
                        p=a['projects'][0]
                        self.assertEqual(p['takeup_evidence']['dependency_takeup_basis'],cs[0]['dependency_takeup_basis'])
                        self.assertEqual(a['possible_ends'][0]['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
                        self.assertIsNone(p.get('addressed_party_ref'))
                    else:
                        bad=copy.deepcopy(cs[0])
                        bad['dependency_takeup_basis']['earlier_lived_trial_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=cs[0]['dependency_takeup_basis']['source_event_refs'][-1]
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_TAKEUP_NO_QUALIFIED_LATER_COURSE'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                stage='project'
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.step('worker')['attempt'],'EAT')
                    a=cold.ledger.actor('worker')[1]
                    if takeup:
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['operation'],'EAT')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['motive_realized'],
                                         'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                        # Exhaust actual shared food; the undertaking persists.
                        for _ in range(14):
                            out=cold.step('worker')
                            if out['status']=='BLOCKED':break
                        self.assertEqual(out['status'],'BLOCKED')
                        a=cold.ledger.actor('worker')[1]
                        self.assertEqual(a['projects'][0]['status'],'active')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['performed_status'],'BLOCKED')
                        old_project=copy.deepcopy(a['projects'][0])
                    stage='wait'
                    for _ in range(12):cold.step('worker')
                    self.assertEqual(revisions,[])
                    stage='renewed'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(revisions),1)
                    rs,exp=revisions[0];self.assertEqual(len(rs),1)
                    a=cold.ledger.actor('worker')[1]
                    project=a['projects'][0]
                    self.assertEqual(project['id'],old_project['id'])
                    self.assertEqual(project['origin'],old_project['origin'])
                    self.assertEqual(project['means'],['EAT','SIGNAL'] if reorganize else ['EAT'])
                    self.assertEqual(project['operational_history'],old_project['operational_history'])
                    if reorganize:
                        self.assertEqual(project['dependency_reorganization_history'][0]['previous']['object'],old_project['object'])
                        self.assertEqual(project['dependency_conditional_means']['SIGNAL']['counterpart_ref'],'mother')
                    else:
                        bad=copy.deepcopy(rs[0])
                        bad['dependency_reorganization_basis']['counterpart_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=rs[0]['dependency_reorganization_basis']['renewed_event_ref']
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_PROJECT_REORGANIZATION_UNQUALIFIED'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertTrue(cold.verify()['valid'])
                    # Long actual history has depleted bodily rest. Keep that
                    # constraint operative; real restorative activity precedes
                    # the next independently solicited course.
                    from um_sorok_organism.organism import eligible
                    self.assertEqual(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL'),(False,'FATIGUE'))
                    stage='wait'
                    self.assertEqual(cold.step('worker',requested_action='REST')['status'],'PERFORMED')
                    self.assertTrue(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL')[0])
                    cold.close()
                    stage='project_refused'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    if reorganize:
                        plan=cold.plan('worker')
                        self.assertEqual((plan.action,plan.target),('SIGNAL','mother'),
                            str({'plan':plan,'signal':[x for x in cold.situated('worker')['candidate_actions'] if x['action']=='SIGNAL'],
                                 'cues':cold.see('worker')['cues']}))
                    result=cold.step('worker')
                    final[reorganize]=result['attempt']
                    if reorganize:
                        self.assertEqual(result['status'],'PARTIAL')
                        self.assertEqual(cold.ledger.actor('worker')[1]['projects'][0]['operational_history'][-1]['operation'],'SIGNAL')
                        stage='project_signal'
                        self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                        self.assertEqual(cold.ledger.actor('worker')[1]['projects'][0]['operational_history'][-1]['operation'],'SIGNAL')
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(final,{True:'SIGNAL',False:'WAIT'})

class DependencyMeansHistoryR40(unittest.TestCase):
    def test_repeated_interruption_and_renewal_revise_same_project_means_without_erasure(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        with tempfile.TemporaryDirectory() as d:
            final={}
            for reopen in (True,False):
                reorganize=True
                takeup=True
                stage='first'; offered=[]; revisions=[]; means_revisions=[]
                def callback(task,packet):
                    if task=='actor_attempt':
                        if packet['actor']['id']=='mother':
                            return {'task':task,'action':('REST' if stage=='restore_mother' else 'FEED' if stage in ('supported','renewed','project_signal','renew_means') else 'REFUSE')}
                        if stage in ('interrupted','renewed','renew_means'):
                            choices=[o for o in packet['practical_options']
                                     if o['operation']=='SIGNAL'
                                     and o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                                     and o['world_request']['addressed_party_ref']=='mother']
                            self.assertEqual(len(choices),1)
                            return {'task':task,'action':'SIGNAL','practical_option_id':choices[0]['option_id']}
                        if stage in ('project_signal','project_refused'):
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='SIGNAL' and x.get('project_id') is not None
                                     and x.get('dependency_conditional_means_ref')]
                            if choices:
                                self.assertEqual(len(choices),1)
                                self.assertEqual(choices[0]['world_request']['addressed_party_ref'],'mother')
                                return {'task':task,'action':'SIGNAL','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                            return {'task':task,'action':'WAIT'}
                        if stage=='trial':
                            trials=[x for x in packet['possible_end_trials'] if x['operation']=='EAT']
                            self.assertEqual(len(trials),1)
                            return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
                        if stage=='revisit':
                            return {'task':task,'action':'EAT'}
                        if stage=='project':
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='EAT' and x.get('project_id') is not None]
                            if choices:
                                return {'task':task,'action':'EAT','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        if stage=='supported':
                            return {'task':task,'candidates':packet['historically_possible_joint_practices']}
                        if stage=='independent':
                            return {'task':task,'candidates':[g for g in packet['historically_possible_genetic_ends']
                                                               if g.get('dependency_loss_basis')]}
                        rs=packet.get('historically_possible_dependency_project_reorganizations',[])
                        if rs:revisions.append((copy.deepcopy(rs),copy.deepcopy(packet['experience'])))
                        if stage=='renewed':return {'task':task,'candidates':rs if reorganize else []}
                        ms=packet.get('historically_possible_dependency_means_revisions',[])
                        if ms:
                            means_revisions.append((copy.deepcopy(ms),copy.deepcopy(packet['experience'])))
                            return {'task':task,'candidates':ms if ms[0]['dependency_means_revision_basis']['mode']=='SUSPEND' or reopen else []}
                        cs=packet.get('historically_possible_dependency_takeups',[])
                        if cs:offered.append((copy.deepcopy(cs),copy.deepcopy(packet['experience'])))
                        return {'task':task,'candidates':cs if takeup else []}
                    return HeuristicSemanticProvider().propose(task,packet)
                db=str(Path(d)/str(reopen)); service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    w['holdings']={'mother':{'food':6}}
                    a=adult('worker','Mara');a['body']['nutrition']=.30
                    a['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
                        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
                        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
                        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}
                    mother=adult('mother','Mother')
                    mother['projects']=[{'id':'care','object':'ordinary care',
                                        'means':['FEED'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a,mother])
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PARTIAL')
                    stage='supported'
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PERFORMED')
                    practice=copy.deepcopy(rt.ledger.actor('worker')[1]['joint_practices'])
                    self.assertEqual(len(practice),1)
                    stage='interrupted'
                    self.assertEqual(rt.step('worker')['status'],'PARTIAL')
                    stage='independent'
                    self.assertEqual(rt.step('worker',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(rt.ledger.actor('worker')[1]['possible_ends']),1)
                    stage='trial'
                    self.assertEqual(rt.step('worker')['attempt'],'EAT')
                    self.assertEqual(offered,[])
                    trial_state=rt.ledger.actor('worker')[1]
                    self.assertEqual(trial_state['projects'],[])
                    self.assertEqual(len(trial_state['possible_ends'][0]['trial_history']),1)
                    stage='wait'
                    for _ in range(8):rt.step('worker')
                    self.assertEqual(offered,[])
                    stage='revisit'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    cs,exp=offered[0];self.assertEqual(len(cs),1)
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),int(takeup))
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(cs[0]['dependency_takeup_basis']['earlier_lived_trial_ref'],
                        trial_state['possible_ends'][0]['trial_history'][0]['id'])
                    if takeup:
                        p=a['projects'][0]
                        self.assertEqual(p['takeup_evidence']['dependency_takeup_basis'],cs[0]['dependency_takeup_basis'])
                        self.assertEqual(a['possible_ends'][0]['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
                        self.assertIsNone(p.get('addressed_party_ref'))
                    else:
                        bad=copy.deepcopy(cs[0])
                        bad['dependency_takeup_basis']['earlier_lived_trial_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=cs[0]['dependency_takeup_basis']['source_event_refs'][-1]
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_TAKEUP_NO_QUALIFIED_LATER_COURSE'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                stage='project'
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.step('worker')['attempt'],'EAT')
                    a=cold.ledger.actor('worker')[1]
                    if takeup:
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['operation'],'EAT')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['motive_realized'],
                                         'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                        # Exhaust actual shared food; the undertaking persists.
                        for _ in range(14):
                            out=cold.step('worker')
                            if out['status']=='BLOCKED':break
                        self.assertEqual(out['status'],'BLOCKED')
                        a=cold.ledger.actor('worker')[1]
                        self.assertEqual(a['projects'][0]['status'],'active')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['performed_status'],'BLOCKED')
                        old_project=copy.deepcopy(a['projects'][0])
                    stage='wait'
                    for _ in range(12):cold.step('worker')
                    self.assertEqual(revisions,[])
                    stage='renewed'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(revisions),1)
                    rs,exp=revisions[0];self.assertEqual(len(rs),1)
                    a=cold.ledger.actor('worker')[1]
                    project=a['projects'][0]
                    self.assertEqual(project['id'],old_project['id'])
                    self.assertEqual(project['origin'],old_project['origin'])
                    self.assertEqual(project['means'],['EAT','SIGNAL'] if reorganize else ['EAT'])
                    self.assertEqual(project['operational_history'],old_project['operational_history'])
                    if reorganize:
                        self.assertEqual(project['dependency_reorganization_history'][0]['previous']['object'],old_project['object'])
                        self.assertEqual(project['dependency_conditional_means']['SIGNAL']['counterpart_ref'],'mother')
                    else:
                        bad=copy.deepcopy(rs[0])
                        bad['dependency_reorganization_basis']['counterpart_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=rs[0]['dependency_reorganization_basis']['renewed_event_ref']
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_PROJECT_REORGANIZATION_UNQUALIFIED'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertTrue(cold.verify()['valid'])
                    # Long actual history has depleted bodily rest. Keep that
                    # constraint operative; real restorative activity precedes
                    # the next independently solicited course.
                    from um_sorok_organism.organism import eligible
                    self.assertEqual(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL'),(False,'FATIGUE'))
                    stage='wait'
                    self.assertEqual(cold.step('worker',requested_action='REST')['status'],'PERFORMED')
                    self.assertTrue(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL')[0])
                    cold.close()
                    stage='project_refused'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    if reorganize:
                        plan=cold.plan('worker')
                        self.assertEqual((plan.action,plan.target),('SIGNAL','mother'),
                            str({'plan':plan,'signal':[x for x in cold.situated('worker')['candidate_actions'] if x['action']=='SIGNAL'],
                                 'cues':cold.see('worker')['cues']}))
                    result=cold.step('worker')
                    self.assertEqual(result['status'],'PARTIAL')
                    self.assertEqual(means_revisions,[])
                    self.assertEqual(cold.step('worker')['status'],'PARTIAL')
                    self.assertEqual(len(means_revisions),1)
                    suspended=cold.ledger.actor('worker')[1]
                    p=suspended['projects'][0]
                    binding=p['dependency_conditional_means']['SIGNAL']
                    self.assertEqual(binding['status'],'SUSPENDED')
                    self.assertEqual(binding['revision_history'][0]['basis']['mode'],'SUSPEND')
                    self.assertEqual(p['means'],['EAT','SIGNAL'])
                    self.assertEqual(p['id'],old_project['id'])
                    self.assertEqual(suspended['joint_practices'],practice)
                    self.assertEqual(p['status'],'active')
                    # Stored SIGNAL no longer recruits the project; the
                    # actor can still seek assistance for other reasons.
                    self.assertFalse(any(x.get('project_id')==p['id'] for a in cold.situated('worker')['candidate_actions']
                        if a['action']=='SIGNAL' for x in a.get('practical_alternatives',[])))
                    self.assertEqual(cold.plan('worker').action,'WAIT')
                    self.assertTrue(cold.verify()['valid'])
                    cold.close()
                    cold=ConstitutiveRuntime(db,semantic=service)
                    # Actual rest and independent support, not injected
                    # relief receipts or bypassed physiological constraints.
                    stage='wait'
                    cold.step('worker',requested_action='REST')
                    cold.step('mother',requested_action='REST')
                    stage='renew_means'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(means_revisions),1)
                    self.assertEqual(cold.ledger.actor('worker')[1]['projects'][0]
                        ['dependency_conditional_means']['SIGNAL']['status'],'SUSPENDED')
                    # Success at bodily saturation is not another lived
                    # nutritional differential. Let ordinary need recur.
                    stage='wait'
                    cold.step('worker',requested_action='REST')
                    for _ in range(10):cold.step('worker')
                    stage='renew_means'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(means_revisions),2,
                        str(cold.ledger.actor('worker')[1]['lived_genesis_episodes'][-14:]))
                    cs,exp=means_revisions[-1]
                    self.assertEqual(cs[0]['dependency_means_revision_basis']['mode'],'REOPEN')
                    a=cold.ledger.actor('worker')[1]
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(a['projects'][0]['id'],p['id'])
                    b=a['projects'][0]['dependency_conditional_means']['SIGNAL']
                    self.assertEqual(b['status'],'ACTIVE' if reopen else 'SUSPENDED')
                    self.assertEqual(len(b['revision_history']),2 if reopen else 1)
                    if not reopen:
                        forged=copy.deepcopy(cs[0])
                        forged['dependency_means_revision_basis']['episode_refs'][0]='invented'
                        before=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_MEANS_REVISION_UNQUALIFIED'):
                            admit(a,exp,cs[0]['dependency_means_revision_basis']['event_refs'][-1],[forged])
                        self.assertEqual(a,before)
                    cold.close()
                    stage='project_refused'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    result=cold.step('worker')
                    final[reopen]=result['attempt']
                    if reopen:
                        self.assertEqual(result['status'],'PARTIAL')
                        self.assertEqual(cold.ledger.actor('worker')[1]['projects'][0]
                             ['dependency_conditional_means']['SIGNAL']['status'],'ACTIVE')
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(final,{True:'SIGNAL',False:'WAIT'})

class DependencyCourseAmbivalenceR41(unittest.TestCase):
    def test_available_course_can_carry_opposed_historical_currents_without_global_veto(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        with tempfile.TemporaryDirectory() as d:
            final={}
            for nominate in (True,False):
                reopen=True
                reorganize=True
                takeup=True
                stage='first'; offered=[]; revisions=[]; means_revisions=[]; ambivalence=[]
                def callback(task,packet):
                    if task=='actor_attempt':
                        if packet['actor']['id']=='mother':
                            return {'task':task,'action':('REST' if stage=='restore_mother' else 'FEED' if stage in ('supported','renewed','project_signal','renew_means') else 'REFUSE')}
                        if stage in ('interrupted','renewed','renew_means'):
                            choices=[o for o in packet['practical_options']
                                     if o['operation']=='SIGNAL'
                                     and o.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                                     and o['world_request']['addressed_party_ref']=='mother']
                            self.assertEqual(len(choices),1)
                            return {'task':task,'action':'SIGNAL','practical_option_id':choices[0]['option_id']}
                        if stage in ('project_signal','project_refused','later_course'):
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='SIGNAL' and x.get('project_id') is not None
                                     and x.get('dependency_conditional_means_ref')]
                            if choices:
                                self.assertEqual(len(choices),1)
                                self.assertEqual(choices[0]['world_request']['addressed_party_ref'],'mother')
                                if stage=='later_course' and choices[0].get('course_psychodynamic_status')=='UNRESOLVED_CONTRADICTION':
                                    return {'task':task,'action':'WAIT'}
                                return {'task':task,'action':'SIGNAL','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                            return {'task':task,'action':'WAIT'}
                        if stage=='trial':
                            trials=[x for x in packet['possible_end_trials'] if x['operation']=='EAT']
                            self.assertEqual(len(trials),1)
                            return {'task':task,'possible_end_trial_id':trials[0]['trial_id']}
                        if stage=='revisit':
                            return {'task':task,'action':'EAT'}
                        if stage=='project':
                            choices=[x for x in packet['practical_options']
                                     if x['operation']=='EAT' and x.get('project_id') is not None]
                            if choices:
                                return {'task':task,'action':'EAT','project_id':choices[0]['project_id'],
                                        'practical_option_id':choices[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        if stage=='supported':
                            return {'task':task,'candidates':packet['historically_possible_joint_practices']}
                        if stage=='independent':
                            return {'task':task,'candidates':[g for g in packet['historically_possible_genetic_ends']
                                                               if g.get('dependency_loss_basis')]}
                        rs=packet.get('historically_possible_dependency_project_reorganizations',[])
                        if rs:revisions.append((copy.deepcopy(rs),copy.deepcopy(packet['experience'])))
                        if stage=='renewed':return {'task':task,'candidates':rs if reorganize else []}
                        amb=packet.get('historically_possible_dependency_ambivalence',[])
                        if amb:
                            ambivalence.append((copy.deepcopy(amb),copy.deepcopy(packet['experience'])))
                            return {'task':task,'candidates':amb if nominate else []}
                        ms=packet.get('historically_possible_dependency_means_revisions',[])
                        if ms:
                            means_revisions.append((copy.deepcopy(ms),copy.deepcopy(packet['experience'])))
                            return {'task':task,'candidates':ms if ms[0]['dependency_means_revision_basis']['mode']=='SUSPEND' or reopen else []}
                        cs=packet.get('historically_possible_dependency_takeups',[])
                        if cs:offered.append((copy.deepcopy(cs),copy.deepcopy(packet['experience'])))
                        return {'task':task,'candidates':cs if takeup else []}
                    return HeuristicSemanticProvider().propose(task,packet)
                db=str(Path(d)/str(nominate)); service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    w['holdings']={'mother':{'food':6}}
                    a=adult('worker','Mara');a['body']['nutrition']=.30
                    a['forms']['eating']={'id':'eating','kind':'PRACTICE','actor':'worker',
                        'origin':['fictional_init:worker'],'grade':'FICTIONAL_ABDUCTIVE_INITIALIZATION',
                        'content':'ordinary eating','cues':['eat'],'enables':['EAT'],
                        'scope':{},'always_recruitable':True,'lifecycle':'ACTIVE'}
                    mother=adult('mother','Mother')
                    mother['projects']=[{'id':'care','object':'ordinary care',
                                        'means':['FEED'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a,mother])
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PARTIAL')
                    stage='supported'
                    self.assertEqual(rt.step('worker',requested_action='SIGNAL',target='mother')['status'],'PERFORMED')
                    practice=copy.deepcopy(rt.ledger.actor('worker')[1]['joint_practices'])
                    self.assertEqual(len(practice),1)
                    stage='interrupted'
                    self.assertEqual(rt.step('worker')['status'],'PARTIAL')
                    stage='independent'
                    self.assertEqual(rt.step('worker',requested_action='EAT')['status'],'PERFORMED')
                    self.assertEqual(len(rt.ledger.actor('worker')[1]['possible_ends']),1)
                    stage='trial'
                    self.assertEqual(rt.step('worker')['attempt'],'EAT')
                    self.assertEqual(offered,[])
                    trial_state=rt.ledger.actor('worker')[1]
                    self.assertEqual(trial_state['projects'],[])
                    self.assertEqual(len(trial_state['possible_ends'][0]['trial_history']),1)
                    stage='wait'
                    for _ in range(8):rt.step('worker')
                    self.assertEqual(offered,[])
                    stage='revisit'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    cs,exp=offered[0];self.assertEqual(len(cs),1)
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),int(takeup))
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(cs[0]['dependency_takeup_basis']['earlier_lived_trial_ref'],
                        trial_state['possible_ends'][0]['trial_history'][0]['id'])
                    if takeup:
                        p=a['projects'][0]
                        self.assertEqual(p['takeup_evidence']['dependency_takeup_basis'],cs[0]['dependency_takeup_basis'])
                        self.assertEqual(a['possible_ends'][0]['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
                        self.assertIsNone(p.get('addressed_party_ref'))
                    else:
                        bad=copy.deepcopy(cs[0])
                        bad['dependency_takeup_basis']['earlier_lived_trial_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=cs[0]['dependency_takeup_basis']['source_event_refs'][-1]
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_TAKEUP_NO_QUALIFIED_LATER_COURSE'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                stage='project'
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.step('worker')['attempt'],'EAT')
                    a=cold.ledger.actor('worker')[1]
                    if takeup:
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['operation'],'EAT')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['motive_realized'],
                                         'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                        # Exhaust actual shared food; the undertaking persists.
                        for _ in range(14):
                            out=cold.step('worker')
                            if out['status']=='BLOCKED':break
                        self.assertEqual(out['status'],'BLOCKED')
                        a=cold.ledger.actor('worker')[1]
                        self.assertEqual(a['projects'][0]['status'],'active')
                        self.assertEqual(a['projects'][0]['operational_history'][-1]['performed_status'],'BLOCKED')
                        old_project=copy.deepcopy(a['projects'][0])
                    stage='wait'
                    for _ in range(12):cold.step('worker')
                    self.assertEqual(revisions,[])
                    stage='renewed'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(revisions),1)
                    rs,exp=revisions[0];self.assertEqual(len(rs),1)
                    a=cold.ledger.actor('worker')[1]
                    project=a['projects'][0]
                    self.assertEqual(project['id'],old_project['id'])
                    self.assertEqual(project['origin'],old_project['origin'])
                    self.assertEqual(project['means'],['EAT','SIGNAL'] if reorganize else ['EAT'])
                    self.assertEqual(project['operational_history'],old_project['operational_history'])
                    if reorganize:
                        self.assertEqual(project['dependency_reorganization_history'][0]['previous']['object'],old_project['object'])
                        self.assertEqual(project['dependency_conditional_means']['SIGNAL']['counterpart_ref'],'mother')
                    else:
                        bad=copy.deepcopy(rs[0])
                        bad['dependency_reorganization_basis']['counterpart_ref']='forged'
                        saved=copy.deepcopy(a)
                        ref=rs[0]['dependency_reorganization_basis']['renewed_event_ref']
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_PROJECT_REORGANIZATION_UNQUALIFIED'):
                            admit(a,exp,ref,[bad])
                        self.assertEqual(a,saved)
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertTrue(cold.verify()['valid'])
                    # Long actual history has depleted bodily rest. Keep that
                    # constraint operative; real restorative activity precedes
                    # the next independently solicited course.
                    from um_sorok_organism.organism import eligible
                    self.assertEqual(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL'),(False,'FATIGUE'))
                    stage='wait'
                    self.assertEqual(cold.step('worker',requested_action='REST')['status'],'PERFORMED')
                    self.assertTrue(eligible(cold.ledger.actor('worker')[1]['body'],'SIGNAL')[0])
                    cold.close()
                    stage='project_refused'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    if reorganize:
                        plan=cold.plan('worker')
                        self.assertEqual((plan.action,plan.target),('SIGNAL','mother'),
                            str({'plan':plan,'signal':[x for x in cold.situated('worker')['candidate_actions'] if x['action']=='SIGNAL'],
                                 'cues':cold.see('worker')['cues']}))
                    result=cold.step('worker')
                    self.assertEqual(result['status'],'PARTIAL')
                    self.assertEqual(means_revisions,[])
                    self.assertEqual(cold.step('worker')['status'],'PARTIAL')
                    self.assertEqual(len(means_revisions),1)
                    suspended=cold.ledger.actor('worker')[1]
                    p=suspended['projects'][0]
                    binding=p['dependency_conditional_means']['SIGNAL']
                    self.assertEqual(binding['status'],'SUSPENDED')
                    self.assertEqual(binding['revision_history'][0]['basis']['mode'],'SUSPEND')
                    self.assertEqual(p['means'],['EAT','SIGNAL'])
                    self.assertEqual(p['id'],old_project['id'])
                    self.assertEqual(suspended['joint_practices'],practice)
                    self.assertEqual(p['status'],'active')
                    # Stored SIGNAL no longer recruits the project; the
                    # actor can still seek assistance for other reasons.
                    self.assertFalse(any(x.get('project_id')==p['id'] for a in cold.situated('worker')['candidate_actions']
                        if a['action']=='SIGNAL' for x in a.get('practical_alternatives',[])))
                    self.assertEqual(cold.plan('worker').action,'WAIT')
                    self.assertTrue(cold.verify()['valid'])
                    cold.close()
                    cold=ConstitutiveRuntime(db,semantic=service)
                    # Actual rest and independent support, not injected
                    # relief receipts or bypassed physiological constraints.
                    stage='wait'
                    cold.step('worker',requested_action='REST')
                    cold.step('mother',requested_action='REST')
                    stage='renew_means'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(means_revisions),1)
                    self.assertEqual(cold.ledger.actor('worker')[1]['projects'][0]
                        ['dependency_conditional_means']['SIGNAL']['status'],'SUSPENDED')
                    # Success at bodily saturation is not another lived
                    # nutritional differential. Let ordinary need recur.
                    stage='wait'
                    cold.step('worker',requested_action='REST')
                    for _ in range(10):cold.step('worker')
                    stage='renew_means'
                    self.assertEqual(cold.step('worker')['status'],'PERFORMED')
                    self.assertEqual(len(means_revisions),2,
                        str(cold.ledger.actor('worker')[1]['lived_genesis_episodes'][-14:]))
                    cs,exp=means_revisions[-1]
                    self.assertEqual(cs[0]['dependency_means_revision_basis']['mode'],'REOPEN')
                    a=cold.ledger.actor('worker')[1]
                    self.assertEqual(a['joint_practices'],practice)
                    self.assertEqual(a['projects'][0]['id'],p['id'])
                    b=a['projects'][0]['dependency_conditional_means']['SIGNAL']
                    self.assertEqual(b['status'],'ACTIVE' if reopen else 'SUSPENDED')
                    self.assertEqual(len(b['revision_history']),2 if reopen else 1)
                    if not reopen:
                        forged=copy.deepcopy(cs[0])
                        forged['dependency_means_revision_basis']['episode_refs'][0]='invented'
                        before=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_MEANS_REVISION_UNQUALIFIED'):
                            admit(a,exp,cs[0]['dependency_means_revision_basis']['event_refs'][-1],[forged])
                        self.assertEqual(a,before)
                    cold.close()
                    stage='project_refused'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    result=cold.step('worker')
                    self.assertEqual(result['status'],'PARTIAL')
                    self.assertEqual(len(ambivalence),1)
                    cs,exp=ambivalence[0];self.assertEqual(len(cs),1)
                    a=cold.ledger.actor('worker')[1]
                    p=a['projects'][0]
                    self.assertEqual(p['dependency_conditional_means']['SIGNAL']['status'],'ACTIVE')
                    self.assertEqual(a['joint_practices'],practice)
                    rows=[x for x in a['historical_orientations'] if x.get('dependency_ambivalence_basis')]
                    self.assertEqual(len(rows),int(nominate))
                    if nominate:
                        self.assertEqual(rows[0]['orientation_mode'],'AMBIVALENT')
                        self.assertEqual(rows[0]['dependency_ambivalence_basis'],cs[0]['dependency_ambivalence_basis'])
                    else:
                        bad=copy.deepcopy(cs[0]);bad['dependency_ambivalence_basis']['approach_episode_refs'][0]='invented'
                        old=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'DEPENDENCY_AMBIVALENCE_UNQUALIFIED'):
                            admit(a,exp,cs[0]['dependency_ambivalence_basis']['latest_event_ref'],[bad])
                        self.assertEqual(a,old)
                    self.assertTrue(cold.verify()['valid'])
                    cold.close()
                    stage='later_course'
                    cold=ConstitutiveRuntime(db,semantic=service)
                    options=cold.situated('worker')['candidate_actions']
                    signal=next(x for x in options if x['action']=='SIGNAL')
                    self.assertNotEqual(signal.get('psychodynamic_status'),'UNRESOLVED_CONTRADICTION')
                    bound=[x for x in signal['practical_alternatives'] if x.get('dependency_conditional_means_ref')]
                    self.assertEqual(len(bound),1)
                    self.assertEqual(bound[0].get('course_psychodynamic_status'),
                        'UNRESOLVED_CONTRADICTION' if nominate else None)
                    self.assertEqual({x['polarity'] for x in bound[0].get('course_historical_currents',[])},
                        {'APPROACH','WITHHOLD'} if nominate else set())
                    self.assertTrue(any(x.get('grounds_status')=='HISTORICALLY_ACQUIRED_CONDITIONAL_JOINT_PRACTICE'
                        and not x.get('course_historical_currents') for x in signal['practical_alternatives']))
                    self.assertFalse(any(x.get('course_historical_currents') for x in options
                        if x['action']=='EAT' for x in x.get('practical_alternatives',[])))
                    result=cold.step('worker')
                    final[nominate]=result['attempt']
                    self.assertTrue(cold.verify()['valid'])
                finally:cold.close()
            self.assertEqual(final,{True:'WAIT',False:'SIGNAL'})


class PluralActivityAffectR42(unittest.TestCase):
    """Same material act, different projects, different subsequent meaning."""
    def test_plural_activity_compound_affect_and_cold_actual_selection(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        final={}
        with tempfile.TemporaryDirectory() as d:
            for compound in (True,False):
                stage='start'; admitted=[]; compound_offers=[]; packet_log=[]
                def callback(task,packet):
                    if task=='actor_attempt':
                        if stage=='start':
                            return {'task':task,'action':'REST','project_ids':['restore','duty']}
                        if stage=='later':
                            alts=[a for a in packet['practical_options']
                                  if a.get('project_id')=='duty' and a['operation']=='REST']
                            self.assertEqual(len(alts),1)
                            row=alts[0]
                            if any(a['basis']['object_affect_ref'] is not None
                                   for a in row.get('course_affective_organizations',[])):
                                return {'task':task,'action':'WAIT'}
                            return {'task':task,'practical_option_id':row['option_id']}
                        return {'task':task,'action':('REST' if stage in ('wait','hidden') else 'WAIT')}
                    if task=='development':
                        if stage=='appraisal':
                            projects={e['id']:e['project_id'] for e in packet['actor_expectations_analyst_only']}
                            rows=packet['historically_possible_delayed_appraisals']
                            self.assertEqual({projects[x['expectation_ref']] for x in rows},{'restore','duty'})
                            picked={}
                            for x in rows:picked.setdefault(x['expectation_ref'],x)
                            return {'task':task,'candidates':[
                                {'kind':'APPRAISE_EXPECTED_DIFFERENCE','expectation_ref':x['expectation_ref'],
                                 'perceived_cue_ref':x['source_perceived_cue_ref'],
                                 'appraisal':('ACTOR_INTERPRETS_SUPPORTED' if projects[x['expectation_ref']]=='restore'
                                              else 'ACTOR_INTERPRETS_DISAPPOINTED')}
                                for x in picked.values()]}
                        offers=packet.get('historically_possible_activity_affects',[])
                        if stage=='hidden':
                            self.assertEqual(offers,[])
                        if stage=='affect':
                            by_project={}
                            for x in offers:
                                if x['object_affect_ref'] is None:by_project.setdefault(x['project_ref'],x)
                            self.assertEqual(set(by_project),{'restore','duty'})
                            cs=[{'kind':'ACQUIRE_ACTIVITY_AFFECT','basis':b,
                                 'affect_name':'relief' if p=='restore' else 'unease',
                                 'personal_sense':('the quiet interval feels restorative' if p=='restore'
                                                   else 'rest conflicts with a continuing obligation'),
                                 'course_orientation':'APPROACH' if p=='restore' else 'NO_DIRECT_TENDENCY'}
                                for p,b in by_project.items()]
                            admitted.extend(copy.deepcopy(cs))
                            return {'task':task,'candidates':cs}
                        if stage=='compound':
                            es=packet['actor_expectations_analyst_only']
                            relief=next(a['id'] for e in es for a in e.get('affective_organizations',[])
                                        if a['affect_name']=='relief')
                            rows=[x for x in offers if x['project_ref']=='duty' and x['object_affect_ref']==relief]
                            self.assertTrue(rows)
                            c={'kind':'ACQUIRE_ACTIVITY_AFFECT','basis':rows[0],
                               'affect_name':'shame about relief',
                               'personal_sense':'the relief itself has become troubling in relation to duty',
                               'course_orientation':'WITHHOLD'}
                            compound_offers.append((copy.deepcopy(c),copy.deepcopy(packet['experience'])))
                            return {'task':task,'candidates':[c] if compound else []}
                        return {'task':task,'candidates':[]}
                    return HeuristicSemanticProvider().propose(task,packet)
                db=str(Path(d)/str(compound));service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    a=adult('worker','Mara')
                    a['projects']=[
                        {'id':p,'object':obj,'means':['REST'],'status':'active','priority':.5,
                         'expected_difference':{'feature':obj,'direction':'PRESERVE','sign_tags':['wait']}}
                        for p,obj in [('restore','recover strength'),('duty','sustain availability to family'),
                                      ('unselected','ordinary leisure')]]
                    rt.ledger.initialize(blank_world(),[a])
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    x=rt.ledger.actor('worker')[1]
                    es=x['expectations'];self.assertEqual({e['project_id'] for e in es},{'restore','duty'})
                    self.assertEqual(len({e['origin_event'] for e in es}),1)
                    self.assertEqual(len({e['practical_option_id'] for e in es}),2)
                    self.assertEqual(len({e['shared_selected_operation_ref'] for e in es}),1)
                    self.assertEqual(len(x['activity_history']),2)
                    self.assertTrue(all(e['motive_realized']=='UNDETERMINED_BY_TECHNICAL_OUTCOME'
                                        for e in x['activity_history']))
                    # A personally performed WAIT supplies the qualified quiet sign;
                    # a fixture cue may be situationally visible but is not an
                    # actor-experience receipt merely because it was accessible.
                    stage='appraisal'
                    rt.step('worker')
                    x=rt.ledger.actor('worker')[1]
                    self.assertEqual({e['project_id']:e['state'] for e in x['expectations']},
                        {'restore':'ACTOR_INTERPRETS_SUPPORTED','duty':'ACTOR_INTERPRETS_DISAPPOINTED'})
                    self.assertFalse(any(e.get('affective_organizations') for e in x['expectations']))
                    # A fresh cue only outside actor's finite sensory access
                    # cannot form an acquired meaning.
                    stage='wait'
                    for _ in range(4):rt.step('worker')
                    stage='hidden'
                    rt.cue(kind='private_quiet',tags=['wait'],private_to='other',lasting_ticks=2)
                    rt.step('worker')
                    stage='affect'
                    rt.step('worker')
                    x=rt.ledger.actor('worker')[1]
                    es=x['expectations'];first={e['project_id']:e['affective_organizations'][0] for e in es}
                    self.assertEqual({a['affect_name'] for a in first.values()},{'relief','unease'})
                    self.assertTrue(all(a['depth']==1 for a in first.values()))
                    stage='wait'
                    for _ in range(4):rt.step('worker')
                    stage='compound'
                    rt.step('worker')
                    self.assertEqual(len(compound_offers),1)
                    x=rt.ledger.actor('worker')[1]
                    duty=next(e for e in x['expectations'] if e['project_id']=='duty')
                    self.assertEqual(len(duty['affective_organizations']),2 if compound else 1)
                    self.assertEqual(duty['affective_organizations'][0],first['duty'])
                    if compound:
                        self.assertEqual(duty['affective_organizations'][1]['basis']['object_affect_ref'],first['restore']['id'])
                    else:
                        c,exp=compound_offers[0]
                        bad=copy.deepcopy(c);bad['basis']['object_affect_ref']='unowned-affect'
                        original=copy.deepcopy(x)
                        # Even a valid first mutation cannot leak when the
                        # second proposed mutation has fabricated ancestry.
                        with self.assertRaisesRegex(InvalidDevelopment,'ACTIVITY_AFFECT_UNQUALIFIED_HISTORY'):
                            admit(x,exp,c['basis']['current_event_ref'],[c,bad])
                        self.assertEqual(x,original)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    stage='wait'
                    for _ in range(4):rt.step('worker')
                    def courses():
                        return {z['project_id']:z for o in rt.situated('worker')['candidate_actions']
                                if o['action']=='REST' for z in o['practical_alternatives']}
                    self.assertFalse(any(v.get('course_affective_organizations') for v in courses().values()))
                    rt.cue(kind='quiet_return',tags=['wait'],lasting_ticks=3)
                    stage='later'
                    rows=courses()
                    self.assertEqual(len(rows['restore']['course_affective_organizations']),1)
                    self.assertEqual(len(rows['duty']['course_affective_organizations']),2 if compound else 1)
                    self.assertNotIn('course_affective_organizations',rows['unselected'])
                    self.assertNotIn('course_affective_organizations',rows[None])
                    result=rt.step('worker')
                    final[compound]=result['attempt']
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
            self.assertEqual(final,{True:'WAIT',False:'REST'})

    def test_forged_plural_expectation_course_cannot_partially_write(self):
        from um_sorok_organism.practical_difference import start_selected_expectations
        a=adult('worker','Mara')
        a['projects']=[{'id':p,'object':p,'means':['REST'],
                        'expected_difference':{'feature':p}} for p in ('a','b')]
        courses=[]
        for p in a['projects']:
            expected=p['expected_difference']
            ident=stable_id('practical_option',{'actor':'worker','clock':1,'action':'REST',
                'project_ref':p['id'],'expected_difference':expected,'addressed_party_ref':None})
            courses.append({'project_id':p['id'],'option_id':ident,'anticipated_difference':expected})
        courses[1]['option_id']='invented'
        sel={'actor':'worker','status':'ACTOR_POLICY_PRACTICAL_ATTEMPT','as_of_clock':1,
             'selected_project_refs':['a','b'],'selected_expectation_courses':courses,
             'world_request':{'operation':'REST','addressed_party_ref':None,'material_object_ref':None}}
        exp={'actor':'worker','own_action':'REST','ref':'experienced',
             'own_practical_selection':sel}
        before=copy.deepcopy(a)
        with self.assertRaisesRegex(ValueError,'PLURAL_EXPECTATION_OPTION_CONTRADICTION'):
            start_selected_expectations(a,sel,exp,'event')
        self.assertEqual(a,before)


class PrivateRehearsalR43(unittest.TestCase):
    def test_private_rehearsal_of_acquired_affect_changes_actual_future_course(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.reflective_regulation import offer_private_rehearsals
        secret='Perhaps I could make room for quiet without earning it first.'
        with tempfile.TemporaryDirectory() as d:
            final={}
            for choose in (True,False):
                stage='start'; private_receipts=[]; exposed=[]
                def callback(task,packet):
                    if task=='expression':
                        self.assertNotIn(secret,str(packet))
                        return {'task':task,'surface':'An ordinary interval.'}
                    if packet.get('actor',{}).get('id')!='worker':
                        if task=='actor_attempt':
                            self.assertNotIn(secret,str(packet))
                            return {'task':task,'action':'WAIT'}
                        if task=='development':
                            self.assertNotIn(secret,str(packet))
                            return {'task':task,'candidates':[]}
                    if task=='actor_attempt':
                        if stage=='start':
                            return {'task':task,'action':'REST','project_id':'duty'}
                        if stage=='rehearse':
                            opts=packet['private_rehearsal_options']
                            linked=[o for o in opts if o['affective_object'] is not None]
                            self.assertEqual(len(linked),1)
                            self.assertEqual(linked[0]['affective_object']['affect_name'],'unease')
                            self.assertTrue(any(o['affect_ref'] is None for o in opts))
                            if choose:
                                return {'task':task,'action':'WAIT',
                                    'private_rehearsal_id':linked[0]['rehearsal_id'],
                                    'private_rehearsal_content':secret}
                        if stage=='trial':
                            opts=[t for t in packet['possible_end_trials']
                                  if t.get('private_rehearsal_ref')]
                            if opts:
                                self.assertEqual(len(opts),1)
                                self.assertEqual(opts[0]['matching_present_terms'],[])
                                return {'task':task,'possible_end_trial_id':opts[0]['trial_id']}
                        if stage=='later':
                            return {'task':task,'action':'REST'}
                        if stage=='project':
                            rows=[x for x in packet['practical_options']
                                  if x.get('project_id') not in (None,'duty')
                                  and x['operation']=='REST']
                            if rows:return {'task':task,'practical_option_id':rows[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        exp=packet['experience']
                        if stage=='appraise':
                            rows=packet['historically_possible_delayed_appraisals']
                            self.assertTrue(rows)
                            return {'task':task,'candidates':[{'kind':'APPRAISE_EXPECTED_DIFFERENCE',
                                    'expectation_ref':rows[0]['expectation_ref'],
                                    'perceived_cue_ref':rows[0]['source_perceived_cue_ref'],
                                    'appraisal':'ACTOR_INTERPRETS_DISAPPOINTED'}]}
                        if stage=='affect':
                            rows=packet['historically_possible_activity_affects']
                            self.assertTrue(rows)
                            return {'task':task,'candidates':[
                                {'kind':'ACQUIRE_ACTIVITY_AFFECT','basis':rows[0],
                                 'affect_name':'unease','personal_sense':'quiet conflicts with duty',
                                 'course_orientation':'WITHHOLD'},
                                {'kind':'MEMORY','cue_terms':['wait'],
                                 'content':'An uneasy quiet interval'}]}
                        receipt=packet.get('actual_private_rehearsal_analyst_only')
                        if receipt:
                            private_receipts.append(copy.deepcopy(receipt))
                            exposed.append(copy.deepcopy(exp))
                            return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                                'rehearsal_ref':receipt['id'],'possible_object':'make room for quiet',
                                'possible_means':['REST']}]}
                        if stage=='later' and choose:
                            end=next(e for e in packet['actor_possible_ends']
                                     if e.get('private_rehearsal_ref'))
                            return {'task':task,'candidates':[{'kind':'TAKE_UP_POSSIBLE_END',
                                    'possible_end_ref':end['id'],'means':['REST']}]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                db=str(Path(d)/str(choose));service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    a=adult('worker','Mara')
                    a['projects']=[{'id':'duty','object':'sustain availability',
                        'means':['REST'],'status':'active','priority':.5,
                        'expected_difference':{'feature':'availability','direction':'PRESERVE',
                                               'sign_tags':['wait']}}]
                    rt.ledger.initialize(blank_world(),[a,adult('other','Other')])
                    rt.step('worker')
                    stage='appraise';rt.step('worker')
                    stage='affect';rt.step('worker')
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['memories']),1)
                    self.assertEqual(len(a['expectations'][0]['affective_organizations']),1)
                    stage='rehearse'
                    # An externally requested WAIT cannot fabricate the
                    # private act, even when the same private option exists.
                    rt.step('worker',requested_action='WAIT')
                    self.assertEqual(private_receipts,[])
                    before=rt.ledger.world()[1]
                    rt.step('worker')
                    after=rt.ledger.world()[1]
                    self.assertEqual(after['clock'],before['clock']+1)
                    self.assertEqual(after['sites'],before['sites'])
                    self.assertNotIn(secret,str(after))
                    self.assertNotIn(secret,str(rt.ledger.actor('other')[1]))
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(private_receipts),int(choose))
                    self.assertEqual(len(a['possible_ends']),int(choose))
                    self.assertEqual(len(a['memories'][0].get('private_rehearsals',[])),int(choose))
                    self.assertEqual(len(a['projects']),1)
                    if choose:
                        end=a['possible_ends'][0];rec=private_receipts[0]
                        self.assertEqual(end['private_rehearsal_ref'],rec['id'])
                        self.assertIsNone(end['actor_perceived_cue_ref'])
                        self.assertEqual(end['cue_terms'],[])
                        self.assertEqual(rec['affect_ref'],a['expectations'][0]['affective_organizations'][0]['id'])
                        bad={'kind':'NOTICE_PRIVATE_POSSIBLE_END','rehearsal_ref':'forged',
                             'possible_object':'fake','possible_means':['REST']}
                        saved=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'PRIVATE_END_NO_ACTUAL_REHEARSAL'):
                            admit(a,exposed[0],rec['event_ref'],[bad])
                        self.assertEqual(saved,a)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    stage='trial'
                    res=rt.step('worker')
                    final[choose]=res['attempt']
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),1)
                    if choose:
                        self.assertEqual(len(a['possible_ends'][0]['trial_history']),1)
                        self.assertEqual(a['possible_ends'][0]['trial_history'][0]['private_rehearsal_ref'],
                                         private_receipts[0]['id'])
                    stage='later';rt.step('worker')
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['projects']),2 if choose else 1)
                    if choose:
                        self.assertEqual(a['projects'][1]['takeup_evidence']['private_takeup_basis']
                                         ['rehearsal_ref'],private_receipts[0]['id'])
                    stage='project'
                    self.assertEqual(rt.step('worker')['attempt'],'REST' if choose else 'WAIT')
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
            self.assertEqual(final,{True:'REST',False:'WAIT'})

    def test_private_rehearsal_cannot_use_unowned_or_preverbal_source(self):
        from um_sorok_organism.reflective_regulation import offer_private_rehearsals
        from um_sorok_organism.types import blank_world
        child=newborn('child','Child')
        self.assertEqual(offer_private_rehearsals(child,0,'home',['WAIT','REST']),[])
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'db'),semantic=ValidatingSemanticService(
                CallbackLLMProvider(lambda task,p: {'task':task,'action':'WAIT',
                    'private_rehearsal_id':'forged','private_rehearsal_content':'invented'})))
            try:
                rt.ledger.initialize(blank_world(),[adult('worker','Mara')])
                before=rt.ledger.world()[1]
                with self.assertRaisesRegex(ValueError,'PRIVATE_REHEARSAL_UNISSUED'):
                    rt.step('worker')
                self.assertEqual(rt.ledger.world()[1],before)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()


class UndertakingAttentionR45(unittest.TestCase):
    def test_actual_outward_undertaking_deliberate_reception_memory_private_trial(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.attention_field import offer_undertaking_attention
        outcomes={}
        with tempfile.TemporaryDirectory() as d:
            for attend in (True,False):
                stage='pledge';receipts=[];rehearsals=[]
                def callback(task,packet):
                    if task=='expression':
                        self.assertNotIn('undertaking_attention_receipt',packet['actor_accessible'])
                        return {'task':task,'surface':'An ordinary interval.'}
                    if task=='actor_attempt':
                        if packet['actor']['id']!='worker':
                            return {'task':task,'action':'WAIT'}
                        if stage=='attend':
                            rows=packet['undertaking_attention_options']
                            self.assertEqual(len(rows),1)
                            self.assertEqual(rows[0]['source_kind'],'INDEPENDENT_COMPUTATIONAL_ACTOR')
                            self.assertEqual(rows[0]['counterpart_ref'],'mother')
                            self.assertNotIn('status',rows[0])
                            if attend:return {'task':task,'action':'ORIENT',
                                'undertaking_attention_id':rows[0]['attention_id']}
                            return {'task':task,'action':'ORIENT'}
                        if stage=='rehearse':
                            rows=[x for x in packet['private_rehearsal_options']
                                  if x.get('undertaking_attention')]
                            self.assertEqual(len(rows),int(attend))
                            if rows:return {'task':task,'action':'WAIT',
                                'private_rehearsal_id':rows[0]['rehearsal_id'],
                                'private_rehearsal_content':'Perhaps rest need not wait for her return.'}
                        if stage=='trial':
                            rows=[x for x in packet['possible_end_trials']
                                  if x.get('private_rehearsal_ref')]
                            if rows:return {'task':task,'possible_end_trial_id':rows[0]['trial_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if packet['actor']['id']!='worker':return {'task':task,'candidates':[]}
                        rec=packet.get('actual_undertaking_attention_analyst_only')
                        if rec:
                            receipts.append((copy.deepcopy(rec),copy.deepcopy(packet['experience']),
                                             packet['evidence_path']['event']))
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'undertaking_attention_ref':rec['attention_id'],
                                'cue_terms':['pledge_care'],'content':'She said she would care later.'}]}
                        rec=packet.get('actual_private_rehearsal_analyst_only')
                        if rec:
                            rehearsals.append(copy.deepcopy(rec))
                            return {'task':task,'candidates':[{'kind':'NOTICE_PRIVATE_POSSIBLE_END',
                                'rehearsal_ref':rec['id'],'possible_object':'rest without awaiting care',
                                'possible_means':['REST']}]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                db=str(Path(d)/str(attend))
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.ledger.initialize(blank_world(),[adult('worker','Mara'),
                        adult('mother','Mother'),adult('bystander','Bystander')])
                    # Actual sourcefree injected outward act by a distinct
                    # computational actor; no claim of native choice of pledge.
                    self.assertEqual(rt.step('mother',requested_action='PLEDGE_CARE',
                                             target='worker')['status'],'PERFORMED')
                    a=rt.ledger.actor('worker')[1];world=rt.ledger.world()[1]
                    b=rt.ledger.actor('bystander')[1]
                    access=actor_access(b,world)
                    self.assertEqual(offer_undertaking_attention(b,world,access,
                        [c['id'] for c in access.cues]),[])
                    self.assertEqual(a['memories'],[])
                    stage='attend'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(receipts),int(attend))
                    self.assertEqual(len(a['memories']),int(attend))
                    self.assertEqual(a['possible_ends'],[])
                    if attend:
                        rec,exp,event=receipts[0]
                        self.assertEqual(a['memories'][0]['undertaking_attention'],rec)
                        self.assertEqual(rec['commitment_ref'],world['scheduled_obligations'][0]['id'])
                        self.assertIn(rec['cue_ref'],a['evidence_paths'][-1]['received_cue_refs'])
                        bad={'kind':'MEMORY','undertaking_attention_ref':'forged',
                             'content':'not my receipt'}
                        old=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'UNDERTAKING_MEMORY_UNQUALIFIED'):
                            admit(a,exp,event,[bad])
                        self.assertEqual(a,old)
                    # Ordinary world time passes independently; no deadline
                    # appraisal, automatic recollection or imposed response.
                    rt.background(5)
                    self.assertEqual(rt.ledger.actor('worker')[1]['memories'],a['memories'])
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    stage='rehearse';rt.step('worker')
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(rehearsals),int(attend))
                    self.assertEqual(len(a['possible_ends']),int(attend))
                    if attend:
                        end=a['possible_ends'][0]
                        self.assertEqual(end['private_undertaking_attention'],receipts[0][0])
                        self.assertIsNone(end['actor_perceived_cue_ref'])
                    stage='trial';outcomes[attend]=rt.step('worker')['attempt']
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
            self.assertEqual(outcomes,{True:'REST',False:'WAIT'})

    def test_injected_orient_does_not_retain_deliberate_undertaking(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.attention_field import offer_undertaking_attention
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'db'),semantic=ValidatingSemanticService(
                CallbackLLMProvider(lambda task,p: {'task':task,'candidates':[]} if task=='development'
                    else {'task':task,'surface':'ordinary'} if task=='expression'
                    else {'task':task,'action':'WAIT'})))
            try:
                rt.ledger.initialize(blank_world(),[adult('worker','Mara'),adult('mother','Mother')])
                rt.step('mother',requested_action='PLEDGE_CARE',target='worker')
                a=rt.ledger.actor('worker')[1];w=rt.ledger.world()[1];e=actor_access(a,w)
                self.assertEqual(len(offer_undertaking_attention(a,w,e,[c['id'] for c in e.cues])),1)
                # A source candidate without its actual authored row cannot
                # become a deliberate reception option.
                forged=copy.deepcopy(w);forged['scheduled_obligations']=[]
                self.assertEqual(offer_undertaking_attention(a,forged,e,[c['id'] for c in e.cues]),[])
                rt.step('worker',requested_action='ORIENT')
                self.assertFalse(any(x.get('undertaking_attention') for x in
                                     rt.ledger.actor('worker')[1]['evidence_paths']))
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()


class AcquiredRepairFacilityR46(unittest.TestCase):
    def test_structurally_qualified_ordinary_practice_and_actual_repairs_change_later_material_result(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.material_conjunction import admit_authored_structural_history
        from um_sorok_organism.practical_powers import active_repair_technique
        results={}
        with tempfile.TemporaryDirectory() as d:
            for allowed,nominate in ((True,True),(True,False),(False,True)):
                target=None;offered=[];phase='ordinary'
                def callback(task,packet):
                    if task=='expression':return {'task':task,'surface':'Ordinary work.'}
                    if task=='actor_attempt':
                        if phase=='repair':
                            choices=[x for x in packet['practical_options']
                                if x['operation']=='REPAIR'
                                and x.get('world_request',{}).get('material_object_ref')==target
                                and x.get('project_id') is None]
                            self.assertTrue(choices)
                            return {'task':task,'practical_option_id':choices[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        cs=packet.get('historically_possible_repair_techniques',[])
                        if cs:offered.append((copy.deepcopy(cs[0]),copy.deepcopy(packet['experience']),
                                             packet['evidence_path']['event']))
                        return {'task':task,'candidates':cs if nominate else []}
                    raise AssertionError(task)
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                db=str(Path(d)/str((allowed,nominate)))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world();w['sites']['home']['stock']=20
                    a=adult('worker','Mara')
                    a['projects']=[{'id':'repair_training','object':'practice repair',
                        'means':['REPAIR'],'priority':.5,'status':'active'}]
                    spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY',
                          'source_ref':'fictional:repair_training',
                          'positions':[{'id':'training','actor':'worker','field':'training_access',
                            'value':'admitted' if allowed else 'excluded','source_ref':'fictional:training',
                            'effective_from':0,'effective_until':6}],
                          'rules':[{'id':'training_gate','operation':'REPAIR','location':'home',
                            'source_ref':'fictional:training_gate','effective_from':0,'effective_until':6,
                            'all_of':[{'kind':'RECORDED_POSITION','field':'training_access','equals':'admitted'}]}]}
                    admit_authored_structural_history(w,{'worker'},spec)
                    rt.ledger.initialize(w,[a],source_seals=[
                        ('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
                    source=rt.register_historical_routine_source({
                        'kind':'QUALIFIED_ROUTINE_PRACTICE','actor':'worker','location':'home',
                        'start_clock':0,'end_clock':7,'max_hours_per_active_day':3,
                        'description':'bounded modeled component practice'})
                    rt.background(7,processes=[{'kind':'QUALIFIED_ROUTINE_PRACTICE',
                        'actor':'worker','location':'home','source_ref':source['source_ref'],
                        'hours_per_active_day':3,'provisional_exposure_fraction':1.,
                        'operation':'REPAIR','mode':'SOLO_COMPONENT_PRACTICE'}])
                    a=rt.ledger.actor('worker')[1]
                    self.assertEqual(len(a['practice_exposures']),int(allowed))
                    self.assertEqual(a['power_exercises'],[])
                    self.assertEqual(a['memories'],[])
                    # Three distinct materially produced artifacts, not
                    # injected success or simulated technical measurements.
                    refs=[]
                    for _ in range(3):
                        phase='ordinary';rt.step('worker',requested_action='REST')
                        before=set(rt.ledger.world()[1]['material_objects'])
                        self.assertEqual(rt.step('worker',requested_action='MAKE_OBJECT')['status'],'PERFORMED')
                        created=set(rt.ledger.world()[1]['material_objects'])-before
                        self.assertEqual(len(created),1)
                        refs.append(created.pop())
                    for target in refs[:2]:
                        phase='ordinary';rt.step('worker',requested_action='REST')
                        phase='repair';self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                        self.assertEqual(rt.ledger.world()[1]['material_objects'][target]['condition'],.8)
                    self.assertEqual(len(offered),int(allowed))
                    a=rt.ledger.actor('worker')[1]
                    technique=active_repair_technique(a,'home')
                    self.assertEqual(bool(technique),allowed and nominate)
                    self.assertIsNone(active_repair_technique(a,'workshop'))
                    if allowed and not nominate:
                        c,exp,event=offered[0];bad=copy.deepcopy(c)
                        bad['basis']['distinct_worked_objects'][0]='invented'
                        old=copy.deepcopy(a)
                        with self.assertRaisesRegex(InvalidDevelopment,'REPAIR_TECHNIQUE_UNQUALIFIED'):
                            admit(a,exp,event,[bad])
                        self.assertEqual(a,old)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    phase='ordinary';rt.step('worker',requested_action='REST')
                    target=refs[2];phase='repair'
                    self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    obj=rt.ledger.world()[1]['material_objects'][target]
                    results[(allowed,nominate)]=obj['condition']
                    self.assertEqual(obj['owner'],'worker')
                    row=obj['objective_labor_history'][-1]
                    self.assertEqual(row['material_stock_units'],1)
                    self.assertEqual(bool(row.get('acquired_component_technique_ref')),allowed and nominate)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
            self.assertEqual(results,{(True,True):.9,(True,False):.8,(False,True):.8})


class AcquiredExpressiveBodyR47(unittest.TestCase):
    def test_same_affect_different_acquired_vocal_manner_and_differential_receipt(self):
        from um_sorok_organism.types import blank_world
        outputs={}
        with tempfile.TemporaryDirectory() as d:
            for learn in (True,False):
                stage='start'; offers=[]; final_receipts={}
                def policy(task,packet):
                    if task=='actor_attempt':
                        if packet['actor']['id']!='worker':return {'task':task,'action':'WAIT'}
                        if stage=='start':return {'task':task,'action':'REST','project_id':'duty'}
                        if stage in ('speech','final'):
                            rows=[x for x in packet['practical_options']
                                  if x.get('project_id')=='duty' and x['operation']=='SPEAK']
                            self.assertEqual(len(rows),1)
                            self.assertTrue(rows[0].get('course_affective_organizations'))
                            return {'task':task,'practical_option_id':rows[0]['option_id']}
                        return {'task':task,'action':'WAIT'}
                    if task=='expression':
                        self.assertNotIn('selected_course_affects_analytic_only',
                            (packet['actor_accessible'].get('own_practical_selection') or {}))
                        return {'task':task,'surface':'Ordinary speech.'}
                    if task=='development':
                        aid=packet['actor']['id'];exp=packet['experience']
                        if stage=='final':
                            final_receipts[aid]=copy.deepcopy(exp)
                        if aid!='worker':return {'task':task,'candidates':[]}
                        if stage=='appraise':
                            row=packet['historically_possible_delayed_appraisals'][0]
                            return {'task':task,'candidates':[{'kind':'APPRAISE_EXPECTED_DIFFERENCE',
                                'expectation_ref':row['expectation_ref'],
                                'perceived_cue_ref':row['source_perceived_cue_ref'],
                                'appraisal':'ACTOR_INTERPRETS_DISAPPOINTED'}]}
                        if stage=='affect':
                            row=packet['historically_possible_activity_affects'][0]
                            return {'task':task,'candidates':[{'kind':'ACQUIRE_ACTIVITY_AFFECT',
                                'basis':row,'affect_name':'private unease',
                                'personal_sense':'quiet conflicts with duty',
                                'course_orientation':'NO_DIRECT_TENDENCY'}]}
                        if stage=='speech':
                            rows=packet['historically_possible_expressive_practices']
                            if rows:
                                candidate={'kind':'ACQUIRE_EXPRESSIVE_PRACTICE',
                                           'basis':rows[0]['basis'],'cadence':'HALTING'}
                                offers.append((copy.deepcopy(candidate),copy.deepcopy(exp),
                                               packet['evidence_path']['event']))
                                return {'task':task,'candidates':[candidate] if learn else []}
                        if stage=='final' and learn:
                            return {'task':task,'candidates':[{'kind':'MEMORY',
                                'cue_terms':['vocal_cadence:halting'],
                                'content':'I heard my own speech pause.'}]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                service=ValidatingSemanticService(CallbackLLMProvider(policy))
                db=str(Path(d)/str(learn));rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    a=adult('worker','Mara')
                    a['projects']=[{'id':'duty','object':'sustain availability',
                        'means':['REST','SPEAK'],'status':'active','priority':.5,
                        'expected_difference':{'feature':'availability','direction':'PRESERVE',
                                               'sign_tags':['wait']}}]
                    rt.ledger.initialize(blank_world(),[a,adult('hearer','Hearer'),
                        adult('blocked','Blocked')])
                    rt.register_sourcefree_recursive_encounter_paths({
                        'grade':'SOURCEFREE_TEST_ONLY','source_ref':'R47_SOUND',
                        'paths':[{'observer':aid,'source_actor':'worker','location':'home',
                            'from_clock':0,'through_clock':30,'hearing':audible,
                            'sound_path':'audible' if audible else 'blocked',
                            'visual':True,'light':'lit','sightline':'unobstructed','facing':'away'}
                            for aid,audible in [('hearer',True),('blocked',False)]]})
                    rt.step('worker')
                    stage='appraise';rt.step('worker')
                    stage='affect';rt.step('worker')
                    for _ in range(2):
                        stage='quiet';rt.step('worker')
                        stage='speech';self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                        self.assertNotIn('vocal_cadence',rt.ledger.world()[1]['cues'][-1])
                    self.assertEqual(len(offers),1)
                    actor=rt.ledger.actor('worker')[1]
                    aff=actor['expectations'][0]['affective_organizations'][0]
                    self.assertEqual(bool(aff.get('expressive_practice')),learn)
                    if not learn:
                        c,exp,event=offers[0];c['basis']['earlier_cue_ref']='invented'
                        saved=copy.deepcopy(actor)
                        with self.assertRaisesRegex(InvalidDevelopment,'EXPRESSIVE_PRACTICE_UNQUALIFIED'):
                            admit(actor,exp,event,[c])
                        self.assertEqual(actor,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    stage='quiet';rt.step('worker')
                    stage='final';self.assertEqual(rt.step('worker')['status'],'PERFORMED')
                    cue=rt.ledger.world()[1]['cues'][-1]
                    self.assertEqual(cue.get('vocal_cadence'),'HALTING' if learn else None)
                    self.assertNotIn('private unease',str(cue))
                    self.assertNotIn('sustain availability',str(cue))
                    hear=next(c for c in final_receipts['hearer']['perceived_cues'] if c['id']==cue['id'])
                    self.assertIsNone(hear['source_actor'])
                    self.assertEqual(hear.get('vocal_cadence'),'HALTING' if learn else None)
                    self.assertNotIn('blocked',final_receipts)
                    own=rt.snapshot('worker')['evidence_paths'][-1]['own_vocal_reception']
                    self.assertEqual(own['cadence_as_sensed'],'HALTING' if learn else 'NOT_DIFFERENTIATED')
                    self.assertEqual(len(rt.snapshot('worker')['memories']),int(learn))
                    self.assertTrue(rt.verify()['valid'])
                    outputs[learn]=cue.get('vocal_cadence')
                finally:rt.close()
            self.assertEqual(outputs,{True:'HALTING',False:None})


class FallibleInstitutionalExpectationR48(unittest.TestCase):
    def test_same_public_account_and_actual_gate_different_actor_afterlife(self):
        from um_sorok_organism.types import blank_world
        from um_sorok_organism.material_conjunction import admit_authored_structural_history
        results={}
        with tempfile.TemporaryDirectory() as d:
            for revise in (True,False):
                stage='read';offered=[];revision_offers=[]
                def policy(task,packet):
                    if task=='expression':
                        self.assertNotIn('notice_expectation',
                            (packet['actor_accessible'].get('own_practical_selection') or {}))
                        return {'task':task,'surface':'Ordinary activity.'}
                    if task=='actor_attempt':
                        rows=[x for o in packet['options'] if o['action']=='EAT'
                              for x in o.get('fallible_notice_expectations',[])]
                        if stage in ('attempt','later'):
                            self.assertEqual(len(rows),1)
                            if rows[0]['anticipated_availability']=='AVAILABLE':
                                return {'task':task,'action':'EAT','project_id':'food',
                                        'notice_expectation_ref':rows[0]['expectation_ref']}
                        return {'task':task,'action':'WAIT'}
                    if task=='development':
                        if stage=='read':
                            rows=packet['historically_possible_notice_expectations']
                            self.assertEqual(len(rows),1)
                            c={'kind':'ACQUIRE_NOTICE_EXPECTATION','basis':rows[0],
                               'anticipated_availability':'AVAILABLE'}
                            offered.append(copy.deepcopy(c))
                            return {'task':task,'candidates':[c]}
                        if stage=='attempt':
                            rows=packet['historically_possible_notice_revisions']
                            self.assertEqual(len(rows),1)
                            self.assertEqual(rows[0]['own_course'],'INCOMPLETE')
                            self.assertEqual(rows[0]['actual_hidden_cause'],'NOT_KNOWN')
                            c={'kind':'REVISE_NOTICE_EXPECTATION','basis':rows[0],
                               'revision':'UNAVAILABLE' if revise else 'RETAIN'}
                            revision_offers.append((copy.deepcopy(c),copy.deepcopy(packet['experience']),
                                                    packet['evidence_path']['event']))
                            return {'task':task,'candidates':[c]}
                        return {'task':task,'candidates':[]}
                    raise AssertionError(task)
                db=str(Path(d)/str(revise));service=ValidatingSemanticService(CallbackLLMProvider(policy))
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    w=blank_world()
                    w['public_notices']=[{'id':'food_notice','public':True,'location':'home',
                        'public_terms':['eat','available'],'public_text':'Food is available here.',
                        'effective_from':0,'effective_until':20}]
                    spec={'grade':'EXPLICIT_SOURCEFREE_STRUCTURAL_HISTORY','source_ref':'fictional:gate',
                          'positions':[{'id':'position','actor':'worker','field':'food_access',
                            'value':'excluded','source_ref':'fictional:position','effective_from':0,
                            'effective_until':1}],
                          'rules':[{'id':'gate','operation':'EAT','location':'home',
                            'source_ref':'fictional:gate','effective_from':0,'effective_until':1,
                            'all_of':[{'kind':'RECORDED_POSITION','field':'food_access','equals':'admitted'}]}]}
                    admit_authored_structural_history(w,{'worker'},spec)
                    a=adult('worker','Mara');a['projects']=[{'id':'food','object':'sustain nutrition',
                         'means':['EAT'],'priority':.5,'status':'active'}]
                    rt.ledger.initialize(w,[a],source_seals=[
                        ('authored_structural_history','FICTIONAL_WORLD_CONDITIONING',spec)])
                    self.assertEqual(rt.step('worker',requested_action='INSPECT',
                                             object_ref='food_notice')['status'],'PERFORMED')
                    self.assertEqual(len(offered),1)
                    a=rt.ledger.actor('worker')[1];x=a['institutional_expectations'][0]
                    self.assertEqual(x['anticipated_availability'],'AVAILABLE')
                    stage='attempt'
                    before=rt.ledger.world()[1]['sites']['home']['food']
                    self.assertEqual(rt.step('worker')['status'],'BLOCKED')
                    self.assertEqual(rt.ledger.world()[1]['sites']['home']['food'],before)
                    a=rt.ledger.actor('worker')[1];x=a['institutional_expectations'][0]
                    self.assertEqual(x['anticipated_availability'],'UNAVAILABLE' if revise else 'AVAILABLE')
                    self.assertEqual(x['revisions'][0]['own_course'],'INCOMPLETE')
                    c,exp,event=revision_offers[0]
                    bad=copy.deepcopy(c);bad['basis']['received_sign_ref']='invented'
                    saved=copy.deepcopy(a)
                    with self.assertRaisesRegex(InvalidDevelopment,'NOTICE_REVISION_UNQUALIFIED'):
                        admit(a,exp,event,[bad])
                    self.assertEqual(a,saved)
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    stage='later'
                    before=rt.ledger.world()[1]['sites']['home']['food']
                    result=rt.step('worker')
                    results[revise]=(result['attempt'],rt.ledger.world()[1]['sites']['home']['food']-before)
                    self.assertEqual(rt.ledger.world()[1]['public_notices'][0]['public_text'],
                                     'Food is available here.')
                    self.assertTrue(rt.verify()['valid'])
                finally:rt.close()
            self.assertEqual(results,{True:('WAIT',0),False:('EAT',-1)})


class StagedFamilyGenesisR49(unittest.TestCase):
    def packet(self,who,purpose):
        return {'input_kind':'THIN_BIOGRAPHY','source_grade':'EXPLICIT_FICTIONAL_HISTORICAL_INPUT',
                'source_ref':'fictional:'+who,'biographical_context':{'ordinary_life':purpose},
                'fictional_seed':{'projects':[{'object':purpose,'means':['REST'],'priority':.5}]}}

    def test_actual_maternal_life_selects_distinct_counterpart_and_child_birth_cold(self):
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        from um_sorok_organism.storage import Conflict
        outcomes={}
        with tempfile.TemporaryDirectory() as d:
            for first in ('REST','WAIT'):
                chosen=[];constructed=[]
                fallback=HeuristicSemanticProvider()
                def callback(task,packet):
                    if task=='adult_constructor':
                        constructed.append(packet['actor_id'])
                    if task=='family_pathway_selection':
                        self.assertEqual(len(packet['eligible_pathways']),2)
                        self.assertNotIn('counterpart_packet',str(packet['eligible_pathways']))
                        self.assertEqual(packet['mother']['lived_genesis_episodes'][-1]['actor_felt_attempt'],first)
                        pid='path-rest' if first=='REST' else 'path-wait'
                        chosen.append(pid)
                        return {'task':task,'pathway_id':pid}
                    if task=='actor_attempt':
                        return {'task':task,'action':first if packet['actor']['id']=='mother' else 'WAIT'}
                    if task=='development':return {'task':task,'candidates':[]}
                    return fallback.propose(task,packet)
                service=ValidatingSemanticService(CallbackLLMProvider(callback))
                db=str(Path(d)/first)
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    rt.initialize_antecedent_adult('mother','Mother',self.packet('mother','ordinary embodied life'))
                    self.assertEqual(set(rt.ledger.actors()),{'mother'})
                    rows=[{'id':'path-'+suffix,'source_ref':'fictional:path:'+suffix,
                           'intersection_clock':1,'intersection_site':'home',
                           'conception_clock':2,'birth_clock':5,
                           'counterpart_id':'father-'+suffix,'counterpart_name':'Father '+suffix,
                           'counterpart_packet':self.packet('father-'+suffix,'independent life '+suffix),
                           'child_id':'nadia','child_name':'Nadia',
                           'prior_shared_effects':'UNMODELED_NO_RETROACTIVE_WRITE'}
                          for suffix in ('rest','wait')]
                    sid=rt.register_family_pathways('mother',rows)['source_seal_id']
                    with self.assertRaisesRegex(ValueError,'FAMILY_NO_SITUATED_PATHWAY'):
                        rt.select_family_intersection(sid)
                    self.assertEqual(constructed,['mother'])
                    rt.step('mother')
                    maternal=copy.deepcopy(rt.ledger.actor('mother')[1])
                    earlier_events=copy.deepcopy(rt.ledger.events())
                    entered=rt.select_family_intersection(sid)
                    father=entered['actor'];self.assertEqual(father,'father-'+first.lower())
                    self.assertEqual(constructed,['mother',father])
                    self.assertEqual(rt.ledger.actor('mother')[1],maternal)
                    self.assertEqual(rt.ledger.events()[:len(earlier_events)],earlier_events)
                    world=rt.ledger.world()[1];family=world['family_genesis']
                    self.assertNotEqual(family['selected_pathway']['maternal_proposal_state_digest'],
                                        family['selected_pathway']['maternal_selection_state_digest'])
                    self.assertEqual(world['relations'],{})
                    self.assertEqual(set(rt.ledger.actors()),{'mother',father})
                    self.assertEqual(rt.ledger.actor(father)[1]['projects'][0]['object'],
                                     'independent life '+first.lower())
                    with self.assertRaisesRegex(ValueError,'FAMILY_CONCEPTION_WRONG_SOURCE_OR_CLOCK'):
                        rt.admit_family_conception()
                    self.assertEqual(rt.step(father,requested_action='CARE',target='mother')['status'],'PERFORMED')
                    rt.admit_family_conception()
                    self.assertNotIn('nadia',rt.ledger.actors())
                    v,original=rt.ledger.world()
                    forged=copy.deepcopy(original)
                    forged['family_genesis']['stage']='CHILD_BORN'
                    with self.assertRaisesRegex(Conflict,'FAMILY_TRANSITION_REQUIRES_QUALIFIED_EVENT'):
                        rt.ledger.commit(rt.world_id,v,forged,{}, {},'ORDINARY_WORLD_EVENT',None,{})
                    self.assertEqual(rt.ledger.world()[1],original)
                    w=rt.ledger.world()[1];actors=rt.ledger.actors();count=rt.verify()['events']
                    with self.assertRaisesRegex(Conflict,'FAMILY_BIRTH_BOUNDARY'):
                        rt.background(4)
                    self.assertEqual(rt.ledger.world()[1],w)
                    self.assertEqual(rt.ledger.actors(),actors)
                    self.assertEqual(rt.verify()['events'],count)
                finally:rt.close()
                rt=ConstitutiveRuntime(db,semantic=service)
                try:
                    for _ in range(4):
                        if 'nadia' in rt.ledger.actors():break
                        rt.advance_to_discontinuity(horizon=5-rt.ledger.world()[1]['clock'] or 1)
                    self.assertEqual(rt.ledger.world()[1]['clock'],5)
                    self.assertEqual(rt.ledger.actor('nadia')[1],newborn('nadia','Nadia'))
                    self.assertEqual(rt.ledger.world()[1]['family_genesis']['birth']['biological_lineage_refs'],
                                     ['mother',father])
                    self.assertEqual(rt.ledger.world()[1]['family_genesis']['stage'],'CHILD_BORN')
                    self.assertFalse(any('nadia' in x['participants'] for x in
                                         rt.ledger.world()[1]['relations'].values()))
                    self.assertEqual(rt.step('mother',requested_action='CARE',target='nadia')['status'],'PERFORMED')
                    child=rt.ledger.actor('nadia')[1]
                    self.assertGreater(child['body']['comfort'],.66)
                    self.assertTrue(child['experienced_care_events'])
                    self.assertTrue(rt.verify()['valid'])
                    outcomes[first]=(father,child['body']['comfort'])
                finally:rt.close()
            self.assertNotEqual(outcomes['REST'][0],outcomes['WAIT'][0])

    def test_no_lived_history_or_impossible_location_cannot_admit_counterpart(self):
        from um_sorok_organism.storage import Conflict
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'db'))
            try:
                rt.initialize_antecedent_adult('mother','Mother',self.packet('mother','ordinary life'))
                row={'id':'path','source_ref':'fictional:path','intersection_clock':1,
                     'intersection_site':'workshop','conception_clock':2,'birth_clock':5,
                     'counterpart_id':'father','counterpart_name':'Father',
                     'counterpart_packet':self.packet('father','independent life'),
                     'child_id':'nadia','child_name':'Nadia',
                     'prior_shared_effects':'UNMODELED_NO_RETROACTIVE_WRITE'}
                bad=copy.deepcopy(row);bad['counterpart_id']='workshop_steward'
                with self.assertRaisesRegex(ValueError,'FAMILY_PATHWAY_OVERLAP_OR_IDENTITY'):
                    rt.register_family_pathways('mother',[bad])
                sid=rt.register_family_pathways('mother',[row])['source_seal_id']
                rt.background(1)
                before=rt.ledger.world()[1]
                with self.assertRaisesRegex(ValueError,'FAMILY_NO_SITUATED_PATHWAY'):
                    rt.select_family_intersection(sid)
                self.assertEqual(rt.ledger.world()[1],before)
                self.assertEqual(set(rt.ledger.actors()),{'mother'})
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
