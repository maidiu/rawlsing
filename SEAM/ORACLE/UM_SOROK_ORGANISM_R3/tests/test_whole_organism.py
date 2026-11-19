"""Integration-level checks of the sourcefree fictional organism.
These tests are software correctness probes, never native CAN/ADP accreditation.
"""
import json,sqlite3, tempfile,unittest
from pathlib import Path
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.world import resolve as direct_resolve
from um_sorok_organism.types import Attempt
from um_sorok_organism.development import admit,InvalidDevelopment
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService

MARA={'source_ref':'fixture_a','answers':{'practice':'frequent','identity':'nonreligious'},
      'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE',
             'content':'retain group sound patterns','cues':['sing','song'],
             'enables':['SING'],'object':'joint rhythm'}],
           'projects':[{'object':'make music together','means':['SING','CARE'],
                        'cue_terms':['sing','home'],'priority':.91}]}}
SAM={'source_ref':'fixture_b','answers':{'practice':'rare','identity':'religious'},
     'fictional_seed':{'acquired_forms':[{'kind':'PRACTICE',
             'content':'join an available rhythm','cues':['sing','join'],
             'enables':['JOIN'],'object':'response rhythm'}],
           'projects':[{'object':'respond to household joint activity',
                        'means':['JOIN'],'cue_terms':['home','join'],'priority':.91}]}}

class WholeOrganism(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=str(Path(self.tmp.name)/'organism.db')
        self.rt=ConstitutiveRuntime(self.path)
        self.rt.initialize([('mara','Mara',MARA),('sam','Sam',SAM)])
    def tearDown(self):self.rt.close();self.tmp.cleanup()

    def test_newborn_is_not_prepsychologized(self):
        n=self.rt.snapshot('nadia')
        self.assertEqual(n['forms'],{})
        self.assertEqual(n['body']['language'],0)
        self.assertNotEqual(self.rt.snapshot('mara')['forms'],n['forms'])
    def test_child_cannot_sing_pre_capacity(self):
        with self.assertRaisesRegex(ValueError,'MOTOR_CAPABILITY'):
            self.rt.step('nadia',requested_action='SING')
        self.assertEqual(self.rt.verify()['events'],1)
    def test_parent_constitution_heterogeneous_and_abductive(self):
        m=self.rt.snapshot('mara');s=self.rt.snapshot('sam')
        self.assertNotEqual(m['forms'],s['forms'])
        a=self.rt.interview('mara',['practice','identity'])
        self.assertEqual(a['independent_whole_respondent_correspondence'],'NOT_DEMONSTRATED')
        self.assertTrue(all(v=='DIRECT_ANSWER_LEAKAGE_NOT_INDEPENDENT'
                          for v in a['evidence_quality'].values()))
    def test_body_world_and_qualified_acquisition(self):
        self.rt.step('nadia',requested_action='SIGNAL')
        self.rt.step('mara',requested_action='CARE',target='nadia')
        self.rt.background(240)
        before=self.rt.situated('nadia')
        self.assertNotIn('SING',{x['action'] for x in before['candidate_actions']})
        self.rt.step('nadia',requested_action='SING')
        after=self.rt.situated('nadia')
        self.assertIn('SING',{x['action'] for x in after['candidate_actions']})
        self.assertGreaterEqual(len(self.rt.snapshot('nadia')['forms']),1)
        # The next actor choice is selected from *acquired* organization.
        auto=self.rt.step('nadia')
        self.assertEqual(auto['selection_grade'],'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE')
        self.assertIn(auto['attempt'],('SING','PRACTICE'))
    def test_participation_is_independent_and_shared_field_world_owned(self):
        self.rt.step('mara',requested_action='SING',target='sam')
        self.rt.step('mara',requested_action='SING',target='sam')
        rels=self.rt.snapshot('mara')['relations']
        self.assertEqual(len(rels),1)
        self.assertEqual(rels[0]['participants'],['mara','sam'])
        self.assertEqual(len(rels[0]['history']),2)
        self.assertIn('REPEATED_JOINT_ACT_OBSERVED',rels[0]['observed_patterns'])
        self.assertEqual(rels[0]['joint_capabilities'],[])  # no automatic power
        self.assertEqual(self.rt.snapshot('sam')['relations'],rels)
        self.assertNotEqual(self.rt.snapshot('sam')['forms'],self.rt.snapshot('mara')['forms'])
    def test_shared_activity_yields_separately_owned_relational_afterlives(self):
        first=self.rt.step('mara',requested_action='SING',target='sam')
        self.assertEqual(first['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
        mother=self.rt.snapshot('mara');father=self.rt.snapshot('sam')
        self.assertIn('sam',mother['other_models'])
        self.assertIn('mara',father['other_models'])
        self.assertNotIn('sam',father['other_models'])
        self.assertFalse(any(f['kind']=='RELATIONAL_INVESTMENT' for f in mother['forms'].values()))
        self.assertFalse(any(f['kind']=='RELATIONAL_INVESTMENT' for f in father['forms'].values()))
        self.assertTrue(any(t['manifestation']=='joint_activity_contingency_possible'
                            for t in mother['traces']))
        self.assertTrue(any(t['manifestation']=='joint_activity_contingency_possible'
                            for t in father['traces']))
        self.assertEqual(mother['relations'],father['relations'])
        self.assertNotEqual(mother['other_models'],father['other_models'])

    def test_no_bool_partner_consent_bypass_public_runtime(self):
        with self.assertRaisesRegex(ValueError,'FORGED_COACTOR_OVERRIDE_REFUSED'):
            self.rt.step('mara',requested_action='SING',target='sam',coactor_override=True)
    def test_no_raw_other_attempt_bypass_world(self):
        _,world=self.rt.ledger.world();actors=self.rt.ledger.actors()
        with self.assertRaisesRegex(ValueError,'DIRECT_COACTOR_BYPASS_REFUSED'):
            direct_resolve(world,actors,Attempt('mara','SING','sam'),Attempt('sam','JOIN'))
        with self.assertRaises(TypeError):
            self.rt.authority.resolve(world,actors,Attempt('mara','SING','sam'),Attempt('sam','JOIN'))
    def test_independent_coactor_issuer_has_no_external_decision_parameter(self):
        _,world=self.rt.ledger.world();actors=self.rt.ledger.actors()
        principal=Attempt('mara','SING','sam')
        actual,coactor,policy=self.rt.authority.resolve(world,actors,principal)
        self.assertEqual(coactor.actor,'sam')
        self.assertEqual(coactor.action,'JOIN')
        self.assertIn('actor_state_hash',policy)
        self.assertEqual(actual.objective_description,'JOINT_ACTIVITY_PERFORMED')
        with self.assertRaises(TypeError):
            self.rt.authority.resolve(world,actors,principal,Attempt('sam','JOIN'))

    def test_institutional_access_is_objective(self):
        self.rt.background(365)
        denied=self.rt.step('sam',requested_action='MOVE',object_ref='hall')
        self.assertEqual(denied['objective_outcome'],'INSTITUTIONAL_ACCESS_DENIED')
        self.assertEqual(self.rt.snapshot('sam')['clock'],366)
        opened=self.rt.step('mara',requested_action='OPEN_HALL')
        self.assertEqual(opened['objective_outcome'],'HALL_OPENED')
        gained=self.rt.step('sam',requested_action='MOVE',object_ref='hall')
        self.assertEqual(gained['objective_outcome'],'MOVED')
        self.assertEqual(self.rt.see('sam')['location'],'hall')
    def test_imposition_not_consent(self):
        self.rt.step('mara',requested_action='IMPOSE',target='nadia')
        _,world=self.rt.ledger.world()
        self.assertEqual(world['public_history'][-1]['outcome'],'UNILATERAL_IMPOSITION_NOT_CONSENT')
        self.assertIsNone(self.rt.ledger.events()[-1]['envelope']['payload']['coactor_attempt'])
    def test_inaccessible_world_cue_not_memory(self):
        before=self.rt.snapshot('nadia')['memories']
        self.rt.cue('sam',kind='unseen_workplace',tags=['work'],location='workshop')
        seen=self.rt.see('nadia')
        self.assertFalse(any(x['kind']=='unseen_workplace' for x in seen['cues']))
        self.assertEqual(self.rt.snapshot('nadia')['memories'],before)
    def test_private_cue_not_seen_by_other(self):
        self.rt.cue('sam',kind='private_thought',tags=['private'],location='home',private_to='sam')
        self.assertFalse(any(x['kind']=='private_thought' for x in self.rt.see('nadia')['cues']))
        self.assertTrue(any(x['kind']=='private_thought' for x in self.rt.see('sam')['cues']))
    def test_compressed_life_is_not_micro_event_forgery(self):
        self.rt.background(120,[{'kind':'household','coverage':'AGGREGATE_MODELED'}])
        _,w=self.rt.ledger.world()
        self.assertEqual(len(w['historical_periods']),1)
        self.assertEqual(w['public_history'],[])
        self.assertEqual(w['historical_periods'][0]['resolution'],'AGGREGATE_MODELED')
        self.assertGreater(self.rt.ledger.actor('nadia')[1]['age_days'],0)
    def test_cross_context_recruitment_becomes_real_after_new_life(self):
        self.rt.background(365)
        self.rt.step('nadia',requested_action='PRACTICE')
        forms=self.rt.snapshot('nadia')['forms'];practice=next(f for f in forms.values() if 'PRACTICE' in f['enables'])
        self.assertEqual(practice['scope']['locations'],['home'])
        moved=self.rt.step('nadia',requested_action='MOVE',object_ref='workshop')
        self.assertEqual(moved['objective_outcome'],'MOVED')
        self.assertNotIn('PRACTICE',{x['action'] for x in self.rt.situated('nadia')['candidate_actions']})
        self.rt.step('nadia',requested_action='PRACTICE')
        forms2=self.rt.snapshot('nadia')['forms']
        self.assertEqual(len(forms2),len(forms))
        self.assertIn('workshop',forms2[practice['id']]['scope']['locations'])
        self.assertIn('PRACTICE',{x['action'] for x in self.rt.situated('nadia')['candidate_actions']})
    def test_composed_activity_generates_multiple_world_attempts(self):
        self.rt.background(365)
        self.rt.step('nadia',requested_action='PRACTICE')
        self.rt.step('nadia',requested_action='SING')
        options=self.rt.possible_composed_activities('nadia')
        self.assertTrue(options)
        result=self.rt.perform_composed_activity('nadia',options[0]['id'])
        self.assertGreaterEqual(len(result['attempts']),1)
        self.assertTrue(result['no_guaranteed_outcome'])
        self.assertTrue(self.rt.verify()['valid'])
    def test_lived_activity_rewires_recruitment_and_project_objects(self):
        self.rt.background(365)
        self.rt.step('nadia',requested_action='PRACTICE')
        self.rt.step('nadia',requested_action='SING')
        person=self.rt.snapshot('nadia')
        self.assertTrue(any(link['relation']=='SUPPORTS' for link in person['links']))
        self.assertTrue(any('rhythm' in p['object'] for p in person['projects']))
        # Persisted relation means one acquired practice can activate another.
        practice=next(f for f in person['forms'].values() if 'PRACTICE' in f['enables'])
        song=next(f for f in person['forms'].values() if 'SING' in f['enables'])
        self.assertTrue(any(e['source']==practice['id'] and e['target']==song['id'] for e in person['links']))
        self.assertGreaterEqual(len(person['history_refs']),2)

    def test_independent_partner_may_refuse_and_world_does_not_fake_joint_act(self):
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'other.db'))
            no_partner={'source_ref':'fixture_absent','answers':{'practice':'rare'},
                        'fictional_seed':{'projects':[{'object':'avoid coactivity',
                            'means':['REFUSE'],'priority':.98,'cue_terms':['sing']}]}}
            try:
                rt.initialize([('mara','Mara',MARA),('other','Other',no_partner)])
                result=rt.step('mara',requested_action='SING',target='other')
                self.assertEqual(result['coactor'],'REFUSE')
                self.assertEqual(result['status'],'PARTIAL')
                self.assertEqual(rt.snapshot('mara')['relations'],[])
            finally:rt.close()

    def test_hidden_world_details_not_sent_to_actor_policy(self):
        self.rt.cue('sam',kind='private_receipt',tags=['private'],location='home',private_to='sam')
        packets=[]
        def callback(task,packet):
            if task=='actor_attempt':
                packets.append(packet)
                return {'task':task,'action':'WAIT'}
            if task=='development':return {'task':task,'candidates':[]}
            return {'task':task,'surface':'silent'}
        rt=ConstitutiveRuntime(self.path,ValidatingSemanticService(CallbackLLMProvider(callback)))
        try:
            rt.step('nadia')
            self.assertEqual(len(packets),1)
            accessible=packets[0]['accessible']
            self.assertNotIn('inaccessible_count',accessible)
            self.assertFalse(any(c['kind']=='private_receipt' for c in accessible['cues']))
        finally:rt.close()

    def test_zero_positive_native_rights(self):
        from um_sorok_organism.adapters import P2_P3_P6_INTEGRATION_CONTRACT
        self.assertFalse(P2_P3_P6_INTEGRATION_CONTRACT['native_owner_writer_rights'])
        self.assertFalse(P2_P3_P6_INTEGRATION_CONTRACT['source_science_issued'])
    def test_unqualified_development_refused(self):
        actor=self.rt.ledger.actor('nadia')[1]
        with self.assertRaises(InvalidDevelopment):
            admit(actor,{'actor':'nadia','ref':'x','perceived_cues':[],'participated':False},
                  'obj_1',[{'kind':'ADD_FORM','form':{'kind':'PRACTICE','cues':['x'],'enables':['SING']}}])
    def test_broken_model_proposal_fails_without_commit(self):
        def callback(task,packet):
            if task=='actor_attempt':return {'task':task,'action':'MINT_IMPOSSIBLE_ACTION'}
            return {'task':task,'candidates':[]} if task=='development' else {'task':task}
        other=ConstitutiveRuntime(self.path,ValidatingSemanticService(CallbackLLMProvider(callback)))
        try:
            with self.assertRaisesRegex(ValueError,'MODEL_ATTEMPT_NOT_ACTOR_ELIGIBLE'):
                other.step('mara')
            self.assertEqual(other.verify()['events'],1)
        finally:other.close()
    def test_cold_reopen_same_actor_state(self):
        self.rt.step('nadia',requested_action='SIGNAL')
        one=self.rt.snapshot('nadia')
        v=self.rt.verify()
        reopened=ConstitutiveRuntime(self.path)
        try:
            self.assertEqual(one,reopened.snapshot('nadia'))
            self.assertEqual(v,reopened.verify())
        finally:reopened.close()
    def test_full_ledger_detects_outside_state_tampering(self):
        self.rt.step('nadia',requested_action='SIGNAL')
        _,world=self.rt.ledger.world()
        world['clock']=999
        # Deliberate direct SQLite tamper demonstrates detection, not normal mutation.
        from um_sorok_organism.types import canonical
        self.rt.ledger.conn.execute('UPDATE worlds SET body=? WHERE id=?',(canonical(world),'w1'))
        with self.assertRaisesRegex(AssertionError,'LAST_WORLD_STATE_CHANGED_OUTSIDE_LEDGER'):
            self.rt.verify()


    def test_historical_cue_expires_without_becoming_memory(self):
        self.rt.cue('sam',kind='momentary_song',tags=['song'],location='home')
        self.assertTrue(any(c['kind']=='momentary_song' for c in self.rt.see('nadia')['cues']))
        old_count=len(self.rt.snapshot('nadia')['memories'])
        self.rt.background(3)
        self.assertFalse(any(c['kind']=='momentary_song' for c in self.rt.see('nadia')['cues']))
        self.assertEqual(len(self.rt.snapshot('nadia')['memories']),old_count)
        self.assertEqual(len(self.rt.ledger.world()[1]['cues']),1)  # history remains

    def test_recruitment_link_cannot_break_target_scope(self):
        from um_sorok_organism.constitution import compose,materialize,actor_access
        _,world=self.rt.ledger.world();actor=self.rt.ledger.actor('nadia')[1]
        actor['body']['motor']=.8
        actor['forms']={
            'source':{'id':'source','kind':'PRACTICE','cues':['coactor'],
                      'enables':['PRACTICE'],'scope':{'locations':['home']},'strength':.7},
            'target':{'id':'target','kind':'PRACTICE','cues':['unseen_target'],
                      'enables':['SING'],'scope':{'locations':['workshop']},'strength':.7}}
        actor['links']=[{'source':'source','target':'target','relation':'RECRUITS','contexts':[]}]
        c=compose(materialize(actor,world),actor_access(actor,world))
        self.assertIn('source',{f['id'] for f in c.recruited})
        self.assertNotIn('target',{f['id'] for f in c.recruited})
        self.assertNotIn('SING',{a['action'] for a in c.candidate_actions})
        actor['forms']['target']['scope']={'locations':['home','workshop']}
        c2=compose(materialize(actor,world),actor_access(actor,world))
        self.assertIn('target',{f['id'] for f in c2.recruited})

    def test_unrecruited_project_does_not_summon_its_own_form(self):
        from um_sorok_organism.constitution import compose,materialize,actor_access
        _,world=self.rt.ledger.world();actor=self.rt.ledger.actor('nadia')[1]
        actor['body']['motor']=.8
        actor['forms']={'phantom':{'id':'phantom','kind':'PRACTICE','cues':['future_game'],
                       'enables':['SING'],'scope':{'locations':['home']},'strength':.9}}
        actor['projects']=[{'id':'future','object':'yet-unavailable collective game',
                'motive':'to be present with someone not currently accessible',
                'means':['SING'],'contextual_only':True,'cue_terms':['future_game'],
                'priority':.99,'status':'active'}]
        c=compose(materialize(actor,world),actor_access(actor,world))
        self.assertFalse(c.recruited)
        self.assertNotIn('SING',{a['action'] for a in c.candidate_actions})
        # A genuine present cue recruits it; the same stored psyche becomes
        # differently operative without creation of a new trait.
        from um_sorok_organism.world import add_cue
        add_cue(world,'offered_game',['future_game'],location='home')
        c2=compose(materialize(actor,world),actor_access(actor,world))
        self.assertIn('phantom',{f['id'] for f in c2.recruited})
        self.assertIn('SING',{a['action'] for a in c2.candidate_actions})

    def test_actor_somatic_feedback_not_equated_with_public_event_cue(self):
        self.rt.background(365)
        self.rt.step('nadia',requested_action='MOVE',object_ref='workshop')
        e=self.rt.ledger.events()[-1]['envelope']['payload']
        self.assertIn('nadia',e['subjective_experience_refs'])
        lived=e['private_actor_experience_receipts']['nadia']
        self.assertEqual(lived['felt_enactment']['attempted_operation'],'MOVE')
        self.assertTrue(lived['felt_enactment']['objective_result_not_inferred'])
        self.assertEqual(lived['perceived_cues'],[])  # event cue emitted at origin
        # Public speech does not falsely disclose the full psychological state;
        # the actor's self-movement does not require visual access to the
        # origin-point announcement after the actor moved away.
        self.assertEqual(self.rt.see('nadia')['location'],'workshop')
        self.assertTrue(self.rt.verify()['valid'])

    def test_objective_labor_and_wage_are_not_technical_fulfillment(self):
        self.rt.background(365)
        self.rt.step('mara',requested_action='MOVE',object_ref='workshop')
        _,before=self.rt.ledger.world();b=before['accounts']['mara']
        r=self.rt.step('mara',requested_action='WORK')
        _,after=self.rt.ledger.world()
        self.assertEqual(r['objective_outcome'],'PRODUCED_GOODS_CONTROLLED_BY_OTHER')
        self.assertGreater(after['accounts']['mara'],b)
        self.assertTrue(after['material_claims'][-1]['worker_control_of_output'] is False)
        self.assertEqual(after['material_claims'][-1]['controller'],'workshop_steward')
        self.assertIsNotNone(after['public_history'][-1]['material_claim_ref'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_one_operation_can_serve_competing_activities_without_motive_deduction(self):
        from um_sorok_organism.activity import record_activity_afterlife
        a=self.rt.ledger.actor('mara')[1]
        a['projects']=[
          {'id':'livelihood','object':'wage access','motive':'meet dependent needs','means':['WORK'], 'status':'active'},
          {'id':'duty','object':'perform socially necessary task','motive':'honor collective obligation','means':['WORK'], 'status':'active'}]
        record_activity_afterlife(a,'WORK','PERFORMED','PRODUCED_GOODS_CONTROLLED_BY_OTHER',
               ['project:livelihood','project:duty'],'evt_actual',{'material_claim_ref':1})
        self.assertEqual(len(a['activity_history']),2)
        self.assertEqual({h['motive_realized'] for h in a['activity_history']},
                         {'UNDETERMINED_BY_TECHNICAL_OUTCOME'})
        self.assertNotEqual(a['activity_history'][0]['practical_object'],a['activity_history'][1]['practical_object'])
        self.assertTrue(all(h['event']=='evt_actual' for h in a['activity_history']))

    def test_sr004_blocked_actor_activity_survives_cold_reopen_without_motive_inference(self):
        from copy import deepcopy
        packet=deepcopy(MARA)
        packet['fictional_seed']['acquired_forms']=[]
        packet['fictional_seed']['projects']=[{'object':'obtain food through the market',
            'means':['BUY_FOOD'],'priority':3,'cue_terms':['home'],
            'motive':'household provision remains a hypothesis'}]
        with tempfile.TemporaryDirectory() as directory:
            path=str(Path(directory)/'sr004.sqlite3')
            rt=ConstitutiveRuntime(path)
            rt.initialize([('worker','Worker',packet)])
            try:
                self.assertEqual(rt.situated('worker')['candidate_actions'][0]['action'],'BUY_FOOD')
                actual=rt.step('worker')
                self.assertEqual(actual['selection_grade'],'ACTOR_SITUATED_CANDIDATE_SELECTED_SOURCEFREE')
                self.assertEqual(actual['status'],'BLOCKED')
                self.assertEqual(actual['objective_outcome'],'INSUFFICIENT_CLAIM_ON_FOOD')
                original=rt.ledger.actor('worker')[1]
                self.assertEqual(len(original['activity_history']),1)
                episode=original['activity_history'][0]
                self.assertEqual(episode['performed_status'],'BLOCKED')
                self.assertEqual(episode['operation_course'],'INTERRUPTED_ATTEMPT')
                self.assertEqual(episode['object_fulfillment'],'NOT_INFERRED_FROM_OPERATION')
                self.assertEqual(episode['motive_realized'],'UNDETERMINED_BY_TECHNICAL_OUTCOME')
                self.assertEqual(len(original['lived_activity_history']),1)
                lived=original['lived_activity_history'][0]
                self.assertEqual(lived['objective_outcome'],'NOT_INFERRED')
                self.assertEqual(lived['felt'],'SOMATIC_ATTEMPT_ONLY')
                self.assertNotIn('INSUFFICIENT_CLAIM_ON_FOOD',str(lived))
                # The existing actor's next situated constitution now carries
                # the lived course, not a manufactured fulfilled purpose.
                ongoing=[c for c in rt.situated('worker')['currents']
                    if c['kind']=='ONGOING_ACTIVITY' and 'market' in c['object']]
                self.assertEqual(len(ongoing),1)
                self.assertEqual(ongoing[0]['latest_lived_attempt'],lived)
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()
            reopened=ConstitutiveRuntime(path)
            try:
                self.assertTrue(reopened.verify()['valid'])
                persisted=reopened.ledger.actor('worker')[1]
                self.assertEqual(persisted['activity_history'][0]['event'],episode['event'])
                self.assertEqual(persisted['lived_activity_history'][0],lived)
            finally:reopened.close()

    def test_sr004_externally_injected_action_does_not_steal_an_actor_motive(self):
        a=self.rt.ledger.actor('mara')[1]
        # An externally injected operation may coincide with an acquired means
        # without becoming the actor's own undertaking.
        self.rt.step('mara',requested_action='SING')
        after=self.rt.ledger.actor('mara')[1]
        self.assertEqual(after.get('activity_history',[]),a.get('activity_history',[]))
        self.assertEqual(after.get('lived_activity_history',[]),a.get('lived_activity_history',[]))
        self.assertTrue(self.rt.verify()['valid'])

    def test_sr004_partial_and_blocked_activity_not_erased_by_technical_status(self):
        from um_sorok_organism.activity import record_activity_afterlife
        a=self.rt.ledger.actor('mara')[1]
        a['projects']=[{'id':'needs','object':'secure food','means':['BUY_FOOD'],'status':'active'},
                       {'id':'relations','object':'participate in shared provisioning','means':['BUY_FOOD'],'status':'active'}]
        partial=record_activity_afterlife(a,'BUY_FOOD','PARTIAL','REQUEST_UNANSWERED',
            ['project:needs','project:relations'],'objective_one')
        blocked=record_activity_afterlife(a,'BUY_FOOD','BLOCKED','NO_ACCESSIBLE_FOOD',
            ['project:needs','project:relations'],'objective_two')
        self.assertEqual(len(partial),2)
        self.assertEqual(len(blocked),2)
        self.assertEqual({x['practical_object'] for x in blocked},{'secure food','participate in shared provisioning'})
        self.assertEqual({x['operation_course'] for x in partial},{'PARTIAL_ATTEMPT'})
        self.assertEqual({x['operation_course'] for x in blocked},{'INTERRUPTED_ATTEMPT'})
        self.assertTrue(all(x['object_fulfillment']=='NOT_INFERRED_FROM_OPERATION'
            for x in partial+blocked))
        self.assertTrue(all(len(p['operational_history'])==2 for p in a['projects']))
        with self.assertRaisesRegex(ValueError,'DUPLICATE_ACTIVITY_EVENT_FOR_PROJECT'):
            record_activity_afterlife(a,'BUY_FOOD','BLOCKED','NO_ACCESSIBLE_FOOD',
                ['project:needs'],'objective_two')

    def test_sr004_composed_plan_cannot_graft_unrelated_means_onto_object(self):
        from types import SimpleNamespace
        from um_sorok_organism.plans import propose_compositions
        options=[{'action':a,'score':1,'basis':basis} for a,basis in [
          ('WORK',['project:livelihood']),('REPAIR',['project:livelihood']),
          ('PRACTICE',['project:music','form:practice']),
          ('SING',['project:music','form:song'])]]
        currents=[{'kind':'ONGOING_ACTIVITY','ref':'music','object':'make music together',
                   'means':['PRACTICE','SING']},
                  {'kind':'ONGOING_ACTIVITY','ref':'livelihood','object':'repair the workshop',
                   'means':['WORK','REPAIR']}]
        results=propose_compositions(SimpleNamespace(actor='mara',currents=currents,
                                                      candidate_actions=options,learned_compositions=[]))
        self.assertEqual(len(results),2)
        by_object={x.object:x for x in results}
        self.assertEqual(by_object['make music together'].steps,('PRACTICE','SING'))
        self.assertEqual(by_object['repair the workshop'].steps,('WORK','REPAIR'))
        self.assertNotIn('project:livelihood',by_object['make music together'].basis)
        self.assertNotIn('project:music',by_object['repair the workshop'].basis)

    def test_sr004_global_operations_without_owner_basis_do_not_form_project_plan(self):
        from types import SimpleNamespace
        from um_sorok_organism.plans import propose_compositions
        fake=SimpleNamespace(actor='mara',currents=[{'kind':'ONGOING_ACTIVITY',
          'ref':'music','object':'music','means':['PRACTICE','SING']}],
          candidate_actions=[{'action':'PRACTICE','basis':['project:someone_else']},
                             {'action':'SING','basis':['form:sing']}],learned_compositions=[])
        self.assertEqual(propose_compositions(fake),[])

    def test_bodily_maturation_is_not_automatically_language_competence(self):
        self.rt.background(365*2)
        n=self.rt.snapshot('nadia')
        self.assertGreater(n['body']['language_ceiling'],.1)
        self.assertEqual(n['body']['language'],0)
        with self.assertRaisesRegex(ValueError,'LANGUAGE_CAPABILITY'):
            self.rt.step('nadia',requested_action='SPEAK')


    def test_mutual_care_has_world_field_bodily_effect_and_distinct_experience(self):
        from um_sorok_organism.runtime import ConstitutiveRuntime
        packet={'source_ref':'fictional_care_fixture','answers':{'care':'possible'},
                'fictional_seed':{'projects':[{'object':'respond to a dependent other',
                    'means':['CARE'],'priority':.98,'cue_terms':['signal','care']}]}}
        with tempfile.TemporaryDirectory() as d:
            rt=ConstitutiveRuntime(str(Path(d)/'joined.db'))
            try:
                rt.initialize([('mother','Mother',packet)])
                b=rt.snapshot('nadia')['body']['comfort']
                out=rt.step('nadia',requested_action='SIGNAL',target='mother')
                self.assertEqual(out['coactor'],'CARE')
                self.assertEqual(out['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
                rel=rt.snapshot('nadia')['relations'][0]
                self.assertEqual(rel['participants'],['mother','nadia'])
                self.assertEqual(rel['history'][0]['material_effects'][0]['kind'],
                                 'CONTINGENT_CARE_REGULATION')
                self.assertGreater(rt.snapshot('nadia')['body']['comfort'],b)
                env=rt.ledger.events()[-1]['envelope']['payload']
                experience=env['private_actor_experience_receipts']
                self.assertEqual(experience['nadia']['felt_enactment']['attempted_operation'],'SIGNAL')
                self.assertEqual(experience['mother']['felt_enactment']['attempted_operation'],'CARE')
                self.assertNotEqual(experience['nadia']['ref'],experience['mother']['ref'])
                self.assertTrue(rt.verify()['valid'])
            finally:rt.close()

    def test_private_experience_receipts_not_sent_to_public_expression(self):
        packets=[]
        def callback(task,packet):
            if task=='actor_attempt':return {'task':task,'action':'WAIT'}
            if task=='development':return {'task':task,'candidates':[]}
            if task=='expression':
                packets.append(packet)
                return {'task':task,'surface':'limited external tip'}
            return {'task':task}
        other=ConstitutiveRuntime(self.path,ValidatingSemanticService(CallbackLLMProvider(callback)))
        try:
            other.step('nadia',requested_action='SIGNAL')
            self.assertEqual(len(packets),1)
            self.assertNotIn('private_actor_experience_receipts',packets[0])
            self.assertEqual(packets[0]['restriction'],'NO_INNER_PSYCHIC_OMNISCIENCE')
        finally:other.close()


    def test_repetition_is_not_stable_relational_power_or_investment(self):
        self.rt.step('mara',requested_action='SING',target='sam')
        self.rt.step('mara',requested_action='SING',target='sam')
        rel=self.rt.snapshot('mara')['relations'][0]
        self.assertEqual(len(rel['history']),2)
        self.assertIn('REPEATED_JOINT_ACT_OBSERVED',rel['observed_patterns'])
        self.assertNotIn('RECURRENT_COORDINATION',rel['joint_capabilities'])
        for aid in ('mara','sam'):
            person=self.rt.snapshot(aid)
            self.assertFalse(any(f['kind']=='RELATIONAL_INVESTMENT' for f in person['forms'].values()))
            self.assertIn('joint_activity_contingency_possible',
                          [t['manifestation'] for t in person['traces']])

if __name__=='__main__':unittest.main()
