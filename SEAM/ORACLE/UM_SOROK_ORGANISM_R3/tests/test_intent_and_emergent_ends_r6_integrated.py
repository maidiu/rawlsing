"""R6 purpose/possible-end behavioral contract ported from ba9c933.

Integration repairs upstream R6 fixture defect: a source-less pseudo-respondent
with answers={} must NOT bypass PSEUDO_RESPONDENT_REQUIRED. Instead a
nonempty explicitly synthetic answer makes this test source-qualified.
Likewise, activity_history is private actor-ledger state, not public snapshot.
These 19 checks are ported, not a byte-identical upstream test file.
"""
import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from um_sorok_organism.activity import record_activity_afterlife
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.types import adult,copy,stable_id
from um_sorok_organism.plans import propose_compositions

PARENT={'source_ref':'fictional_intention_test_source',
 'answers':{'SOURCEFREE_FIXTURE_INSTRUMENT':'UNDETERMINED_NOT_AN_EMPIRICAL_ANSWER'},
 'fictional_seed':{'projects':[
   {'object':'comfort my child through song','means':['SING'],'priority':.93,'cue_terms':['sing']},
   {'object':'experiment with changing a rhythm','means':['SING'],'priority':.81,'cue_terms':['sing']}]}}

def experience(actor='mother',ref='actor:experienced:1',action='SING',cue='world:perceived_song'):
    return {'actor':actor,'ref':ref,'own_action':action,
      'status':'PERFORMED','participated':True,
      'felt_enactment':{'attempted_operation':action,'objective_result_not_inferred':True},
      'perceived_cues':[{'id':cue,'tags':['sing','rhythm']}],
      'actor_access_grade':'SOURCEFREE'}

class PurposeAndGenesisR6Integrated(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(str(Path(self.tmp.name)/'person.db'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([('mother','Mother',copy(PARENT))])
    def private_actor(self,ident='mother'):
        return self.rt.ledger.actor(ident)[1]
    def provider(self,choice='comfort my child through song',include_purpose=True,record=None):
        def callback(task,packet):
            if task=='actor_attempt':
                selected=next(o for o in packet['options'] if o['action']=='SING')
                projects=selected.get('project_courses',[])
                self.assertEqual(len(projects),2)
                project=next(p for p in projects if p['object']==choice)
                ans={'task':task,'action':'SING'}
                if include_purpose:ans['project_id']=project['project_id']
                return ans
            if task in ('development','expression'):
                if record is not None:record.append((task,copy(packet)))
                return {'task':task,'candidates':[]} if task=='development' else {'task':task,'surface':'heard a song'}
            self.fail('unexpected task '+task)
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
    def test_two_available_project_courses_do_not_both_become_attempts(self):
        self.provider()
        sing=next(o for o in self.rt.situated('mother')['candidate_actions'] if o['action']=='SING')
        self.assertEqual({c['object'] for c in sing['project_courses']},
            {'comfort my child through song','experiment with changing a rhythm'})
        self.rt.step('mother');a=self.private_actor()
        self.assertEqual(len(a['activity_history']),1)
        self.assertEqual(a['activity_history'][0]['practical_object'],'comfort my child through song')
        self.assertEqual(a['activity_history'][0]['intent_attribution'],'ACTOR_POLICY_SELECTED_PROJECT_COURSE')
        self.assertEqual(a['activity_history'][0]['object_fulfillment'],'NOT_INFERRED_FROM_OPERATION')
        self.assertEqual(next(p for p in a['projects'] if p['object']=='experiment with changing a rhythm').get('operational_history',[]),[])
        self.assertTrue(self.rt.verify()['valid'])
    def test_explicitly_multiple_projects_can_both_be_undertaken_without_pooling(self):
        def callback(task,packet):
            if task=='actor_attempt':
                option=next(o for o in packet['options'] if o['action']=='SING')
                selected=[c['project_id'] for c in option['project_courses']]
                self.assertEqual(len(selected),2)
                return {'task':task,'action':'SING','project_ids':selected}
            if task=='development':return {'task':task,'candidates':[]}
            return {'task':task,'surface':'song perceived'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        self.rt.step('mother');a=self.private_actor()
        self.assertEqual(len(a['activity_history']),2)
        self.assertEqual({x['practical_object'] for x in a['activity_history']},
            {'comfort my child through song','experiment with changing a rhythm'})
        self.assertTrue(all(x['intent_attribution']=='ACTOR_POLICY_SELECTED_MULTIPLE_PROJECT_COURSES' for x in a['activity_history']))
        self.assertEqual(len(self.rt.snapshot('mother')['evidence_paths'][-1]['selected_project_refs']),2)
    def test_no_model_project_choice_means_unattributed_exploration(self):
        self.provider(include_purpose=False);self.rt.step('mother');a=self.private_actor()
        self.assertEqual(a['activity_history'],[])
        evidence=self.rt.snapshot('mother')['evidence_paths'][-1]
        self.assertEqual(evidence['purpose_status'],'ACTOR_POLICY_NO_ATTESTED_PROJECT_PURPOSE')
        self.assertIsNone(evidence['selected_project_ref'])
        self.assertEqual(evidence['unencountered_alternatives'],'UNKNOWN_NOT_OBSERVED')
    def test_wrong_project_ownership_cannot_be_forged_by_model(self):
        def callback(task,packet):return {'task':task,'action':'SING','project_id':'invented_project'}
        self.rt.semantic=ValidatingSemanticService(CallbackLLMProvider(callback))
        before=self.rt.ledger.world()[1]['clock']
        with self.assertRaisesRegex(ValueError,'MODEL_SELECTED_PURPOSE_NOT_SITUATED_ELIGIBLE'):
            self.rt.step('mother')
        self.assertEqual(self.rt.ledger.world()[1]['clock'],before)
        self.assertEqual(self.private_actor()['activity_history'],[])
    def test_external_action_injection_does_not_assign_a_project(self):
        self.rt.step('mother',requested_action='SING')
        self.assertEqual(self.private_actor()['activity_history'],[])
        self.assertEqual(self.rt.snapshot('mother')['evidence_paths'][-1]['purpose_status'],
                         'EXTERNALLY_INJECTED_NO_ATTESTED_ACTOR_PURPOSE')
    def test_heuristic_must_choose_single_explicit_course(self):
        attempt=self.rt.plan('mother')
        if attempt.action=='SING':
            self.assertEqual(attempt.purpose_selection['status'],'ACTOR_POLICY_SELECTED_PROJECT_COURSE')
            self.assertEqual(attempt.purpose_selection['practical_object'],'comfort my child through song')
            self.assertEqual(len([b for b in attempt.basis if b.startswith('project:')]),1)
    def test_selected_purpose_remains_private_to_analytic_model_not_renderer(self):
        packets=[];self.provider(record=packets);self.rt.step('mother')
        dev=[v for task,v in packets if task=='development' and v.get('actor',{}).get('id')=='mother'];ex=[v for task,v in packets if task=='expression']
        self.assertEqual(len(dev),1);self.assertEqual(len(ex),1)
        self.assertIn('selected_purpose_analytic_only',dev[0])
        self.assertNotIn('selected_purpose_analytic_only',ex[0])
        self.assertNotIn('motive_hypothesis',str(ex[0]))
        self.assertNotIn('possible_ends',str(ex[0]))
    def test_possible_end_is_not_immediate_project_or_original_intention(self):
        a=adult('mother','Mother')
        r=admit(a,experience(),'objective:first_song',[{'kind':'NOTICE_POSSIBLE_END',
            'perceived_cue_ref':'world:perceived_song','possible_object':'continue rhythms with another',
            'possible_means':['SING','PRACTICE'],'cue_terms':['sing','rhythm']}])
        self.assertEqual(len(a['projects']),0);self.assertEqual(len(a['possible_ends']),1)
        self.assertEqual(a['possible_ends'][0]['status'],'POSSIBLE_NOT_ACQUIRED_MOTIVE')
        self.assertTrue(a['possible_ends'][0]['initial_event_intent_not_rewritten'])
        self.assertEqual(r[0]['status'],'ADMITTED_PROVISIONAL_END_NOT_YET_MOTIVE')
    def test_later_experience_can_take_up_possible_end_as_distinct_end(self):
        a=adult('mother','Mother');admit(a,experience(),'objective:first_song',[{
            'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':'world:perceived_song',
            'possible_object':'continue rhythms with another','possible_means':['SING','PRACTICE'],
            'cue_terms':['rhythm']}]);ref=a['possible_ends'][0]['id']
        later=experience(ref='lived:later',action='PRACTICE',cue='world:later_rhythm')
        r=admit(a,later,'objective:later_episode',[{'kind':'TAKE_UP_POSSIBLE_END',
            'possible_end_ref':ref,'means':['SING'],'priority':.4}])
        self.assertEqual(r[0]['status'],'ADMITTED_FICTIONAL_LATER_END_TAKEUP')
        self.assertEqual(len(a['projects']),1)
        self.assertEqual(a['projects'][0]['origin'],['objective:first_song','objective:later_episode'])
        self.assertEqual(a['possible_ends'][0]['status'],'TAKEN_UP_AS_PRACTICAL_PROJECT')
        self.assertTrue(a['projects'][0]['original_attempt_purpose_not_rewritten'])
        self.assertTrue(a['projects'][0]['skill_mastery_not_inferred'])
    def test_later_takeup_cannot_cite_an_unreceived_cue(self):
        a=adult('mother','Mother');admit(a,experience(),'objective:one',[{
            'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':'world:perceived_song',
            'possible_object':'pursue shared rhythm','possible_means':['SING'],'cue_terms':['sing']}]);before=copy(a)
        with self.assertRaisesRegex(InvalidDevelopment,'TAKEUP_SIGN_NOT_ACTOR_RECEIVED'):
            admit(a,experience(ref='lived:two',cue='world:real_later'),'objective:two',[{
                'kind':'TAKE_UP_POSSIBLE_END','possible_end_ref':a['possible_ends'][0]['id'],
                'later_perceived_cue_ref':'world:invented','means':['SING']}])
        self.assertEqual(a,before)
    def test_takeup_persists_actual_later_sign_without_motive_certainty(self):
        a=adult('mother','Mother');admit(a,experience(),'objective:one',[{
            'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':'world:perceived_song',
            'possible_object':'explore rhythm','possible_means':['SING'],'cue_terms':['rhythm']}])
        initial=copy(a['possible_ends'][0]);later=experience(ref='lived:two',cue='world:heard_again')
        admit(a,later,'objective:two',[{'kind':'TAKE_UP_POSSIBLE_END',
            'possible_end_ref':initial['id'],'later_perceived_cue_ref':'world:heard_again','means':['SING']}])
        evidence=a['projects'][0]['takeup_evidence']
        self.assertEqual(evidence['later_received_sign_ref'],'world:heard_again')
        self.assertEqual(evidence['actual_received_sign_refs'],['world:heard_again'])
        self.assertEqual(evidence['sign_selection_grade'],'LLM_PROPOSED_ACTOR_RECEIVED_SIGN')
        self.assertTrue(evidence['not_a_proven_causal_significance'])
        self.assertEqual(a['projects'][0]['origin'],['objective:one','objective:two'])
        self.assertTrue(a['projects'][0]['original_attempt_purpose_not_rewritten'])
    def test_same_event_cannot_retroactively_become_own_purpose(self):
        a=adult('mother','Mother');one={'kind':'NOTICE_POSSIBLE_END',
           'perceived_cue_ref':'world:perceived_song','possible_object':'value surprising sound',
           'possible_means':['SING']}
        ref=stable_id('possible_end',{'actor':'mother','event':'objective:first',
                'cue':'world:perceived_song','index':0,'object':'value surprising sound'})
        with self.assertRaisesRegex(InvalidDevelopment,'POSSIBLE_END_CANNOT_RETROACTIVELY_BECOME_INTENT'):
            admit(a,experience(),'objective:first',[one,{'kind':'TAKE_UP_POSSIBLE_END',
                'possible_end_ref':ref}])
        self.assertEqual(a['possible_ends'],[]);self.assertEqual(a['projects'],[])
    def test_hidden_or_invented_cue_cannot_justify_possible_end(self):
        a=adult('mother','Mother')
        with self.assertRaisesRegex(InvalidDevelopment,'POSSIBLE_END_MUST_DERIVE_FROM_ACTOR_RECEIVED_SIGN'):
            admit(a,experience(),'objective:first',[{'kind':'NOTICE_POSSIBLE_END',
                'perceived_cue_ref':'secret_unseen_cue','possible_object':'invent memory',
                'possible_means':['SING']}])
        self.assertEqual(a['possible_ends'],[])
    def test_new_undertaking_may_not_mint_an_unavailable_operation(self):
        a=adult('mother','Mother');admit(a,experience(),'objective:first',[{
            'kind':'NOTICE_POSSIBLE_END','perceived_cue_ref':'world:perceived_song',
            'possible_object':'try melody','possible_means':['SING']}]);old=copy(a)
        with self.assertRaisesRegex(InvalidDevelopment,'UNLICENSED_TAKEUP_MEANS'):
            admit(a,experience(ref='lived:second'),'objective:second',[{
                'kind':'TAKE_UP_POSSIBLE_END','possible_end_ref':a['possible_ends'][0]['id'],
                'means':['WORK']}])
        self.assertEqual(a,old)
    def test_actual_nadia_development_distinguishes_first_and_later_song(self):
        self.rt.background(240);self.rt.step('nadia',requested_action='SING')
        first=self.rt.snapshot('nadia')
        self.assertTrue(any(e['status']=='POSSIBLE_NOT_ACQUIRED_MOTIVE' for e in first['possible_ends']))
        self.assertFalse(any('rhythm' in p['object'] for p in first['projects']))
        self.rt.step('nadia',requested_action='SING');later=self.rt.snapshot('nadia')
        self.assertTrue(any(e['status']=='TAKEN_UP_AS_PRACTICAL_PROJECT' for e in later['possible_ends']))
        self.assertTrue(any('rhythm' in p['object'] for p in later['projects']))
        self.assertTrue(self.rt.verify()['valid'])
    def test_two_composed_projects_same_object_stay_separate_by_project_origin(self):
        common={'object':'make a shared sound','means':['PRACTICE','SING'],'kind':'ONGOING_ACTIVITY'}
        view=SimpleNamespace(actor='mother',currents=[dict(common,ref='first'),dict(common,ref='second')],
            candidate_actions=[{'action':'PRACTICE','basis':['project:first','project:second']},
                               {'action':'SING','basis':['project:first','project:second']}],learned_compositions=[])
        plans=propose_compositions(view)
        self.assertEqual(len(plans),2)
        self.assertEqual({p.project_ref for p in plans},{'first','second'})
        self.assertEqual(len({p.id for p in plans}),2)
        self.assertTrue(all(p.purpose_claim=='HYPOTHESIZED_PLAN_OBJECT_NOT_PERFORMER_INTENT' for p in plans))
    def test_first_new_end_and_actual_signal_path_are_relevant_without_being_motives(self):
        self.rt.background(240);self.rt.step('nadia',requested_action='SING')
        cur=self.rt.situated('nadia');kinds={x['kind'] for x in cur['currents']}
        self.assertIn('HISTORICALLY_NOTICED_POSSIBLE_END',kinds)
        self.assertIn('HISTORICAL_SIGNAL_PATH_REENCOUNTERED',kinds)
        signal=next(x for x in cur['currents'] if x['kind']=='HISTORICAL_SIGNAL_PATH_REENCOUNTERED')
        self.assertTrue(signal['not_imputed_counterfactual'])
        self.assertTrue(signal['no_automatic_belief_update'])
        end=next(x for x in cur['currents'] if x['kind']=='HISTORICALLY_NOTICED_POSSIBLE_END')
        self.assertTrue(end['not_automatically_an_active_motive'])
        self.assertFalse(any('rhythm' in p['object'] for p in self.rt.snapshot('nadia')['projects']))
    def test_unobserved_interval_does_not_fake_same_signal_as_current(self):
        self.rt.background(240);self.rt.step('nadia',requested_action='SING')
        self.rt.background(1);cur=self.rt.situated('nadia')
        self.assertFalse(any(x['kind']=='HISTORICAL_SIGNAL_PATH_REENCOUNTERED' for x in cur['currents']))
        self.assertTrue(self.rt.snapshot('nadia')['evidence_paths'])
    def test_legacy_explicit_multi_project_call_stays_distinct_from_auto_pool(self):
        a=adult('mother','Mother');a['projects']=[
             {'id':'care','object':'offer care','means':['SING'],'status':'active'},
             {'id':'play','object':'explore play','means':['SING'],'status':'active'}]
        histories=record_activity_afterlife(a,'SING','PERFORMED','SOLO_PRACTICE',
            ['project:care','project:play'],'objective:one')
        self.assertEqual(len(histories),2)
        self.assertTrue(all(h['intent_attribution']=='EXPLICIT_LEGACY_PROJECT_BASIS_ASSERTION' for h in histories))
