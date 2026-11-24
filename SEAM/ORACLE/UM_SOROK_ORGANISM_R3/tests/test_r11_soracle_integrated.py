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
