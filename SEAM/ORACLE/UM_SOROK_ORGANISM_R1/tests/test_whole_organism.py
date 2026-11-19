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
        self.assertIn('RECURRENT_COORDINATION',rels[0]['joint_capabilities'])
        self.assertEqual(self.rt.snapshot('sam')['relations'],rels)
        self.assertNotEqual(self.rt.snapshot('sam')['forms'],self.rt.snapshot('mara')['forms'])
    def test_shared_activity_yields_separately_owned_relational_afterlives(self):
        first=self.rt.step('mara',requested_action='SING',target='sam')
        self.assertEqual(first['objective_outcome'],'JOINT_ACTIVITY_PERFORMED')
        mother=self.rt.snapshot('mara');father=self.rt.snapshot('sam')
        self.assertIn('sam',mother['other_models'])
        self.assertIn('mara',father['other_models'])
        self.assertNotIn('sam',father['other_models'])
        self.assertTrue(any(f['kind']=='RELATIONAL_INVESTMENT' for f in mother['forms'].values()))
        self.assertTrue(any(f['kind']=='RELATIONAL_INVESTMENT' for f in father['forms'].values()))
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

if __name__=='__main__':unittest.main()
