"""Preregistered required boundary assertions. RED is retained evidence, not xfail."""
import json
from dataclasses import replace
import pytest
from support import *
from candidate.events import GRADE_NATIVE
from candidate.later_action import read_target_for_later_action

@pytest.fixture
def store(tmp_path):
 with CandidateStore(tmp_path/'review.sqlite') as s:yield s

def assert_no_effect(result):
 assert result.decision is None or result.decision.branch is not TargetBranch.CREATE

def test_forged_actor_original_source_refused():
 forged=reseal(actor(),source_ref='ADP007:INVENTED',source_hash='not-an-authentic-source')
 assert not ingress_actor(forged,as_of=20).admitted

def test_wrong_actor_event_refused(store):
 assert_no_effect(run(store,event_raw=event(actor_role='TEST_ONLY_OTHER_ACTOR',content={'participants':['OTHER'],'scene':'elsewhere'})))

def test_forged_native_receipt_refused():
 e=event(admission_grade=GRADE_NATIVE,owner_ref='ADP019:FICTIONAL',owner_receipt_ref='no-such-owner-receipt')
 assert not ingress_event(e,as_of=20,last_time=0,prior_event_hashes=frozenset()).admitted

def test_foreign_conditioning_subject_refused(store):
 s=reseal(sources()[0],subject='OTHER')
 r=run(store,conditioning_sources=[s]);assert not r.committed
 assert not store.committed_event_hashes()

@pytest.mark.parametrize('body',[{'as_of':999,'scene':'garage','access':'granted'},{'as_of':15,'scene':'other-world','access':'granted'},{'as_of':15,'scene':'garage','access':'denied'}],ids=['future','wrong-scene','denied-material-access'])
def test_ineligible_world_does_not_create(store,body):
 s=make_conditioning_source(source_ref='TEST_ONLY_REVIEW_GARAGE',source_class='ResolvedStructuralContext',subject=A,body=body)
 assert_no_effect(run(store,conditioning_sources=[s]))

def test_rehashed_source_false_identity_refused():
 s=reseal(sources()[0],content={'access':'denied'},source_hash='unchanged-false-digest')
 assert not bind_conditioning(subject=A,sources=[s],as_of=20).bound

def test_observer_privileged_truth_not_actor_practice(store):
 s=make_conditioning_source(source_ref='TEST_ONLY_PRIVATE_P_BELIEF',source_class='OBSERVER_TRUTH',subject=A,body={'P_private_plan':'leave','actor_observed':False})
 assert_no_effect(run(store,conditioning_sources=[s]))

def test_unissued_rule_not_adopted_by_r2_label():
 r=replace(rule(),authority_id='CAN008_R2_ADOPTED',authority_version='R2',grade='CURRENT_ACCEPTED',issuer_ref='LOCAL_CALLER')
 reg=ResponseRuleRegistry('FORGED_CURRENT_REGISTRY','R2','CURRENT_ACCEPTED',{r.registry_key():r.as_dict()})
 found=lookup_rule(reg,authority_id=r.authority_id,rule_version=r.rule_version,rule_content_hash=r.rule_content_hash,subject=A)
 assert not found.found

def test_rule_content_rehash_not_authenticated():
 r=rule();entry=r.as_dict();entry['predicates']=['anything'];entry['rule_content_hash']='forged-rehash'
 reg=ResponseRuleRegistry('LOCAL','1','CURRENT_ACCEPTED',{(r.authority_id,'1','forged-rehash'):entry})
 assert not lookup_rule(reg,authority_id=r.authority_id,rule_version='1',rule_content_hash='forged-rehash',subject=A).found

def test_locally_minted_target_registry_and_grant_refused(store):
 r=rule();t=replace(target(r),issuer_ref='LOCAL_FORGER',grade='CURRENT_ACCEPTED')
 reg=TargetRuleRegistry('FORGED_CURRENT','1','CURRENT_ACCEPTED',{t.registry_key():t.as_dict()})
 p=make_target_permission(grant_id='FORGED',issuer_ref='LOCAL_FORGER',actor_id=A,rule_content_hash=r.rule_content_hash,before_target_hash=store.target_state_hash(),response_hash='not-response',issued_at=10,grade='CURRENT_ACCEPTED')
 _,_,d=decide(store,target_registry=reg,target_permission=p,permitted_issuer_refs=frozenset({'LOCAL_FORGER'}))
 assert d.branch is not TargetBranch.CREATE

@pytest.mark.parametrize('field,value',[('response_hash','WRONG_RESPONSE'),('issued_at',999),('issuer_scope','REVOKED_SCOPE')])
def test_target_grant_exact_binding(store,field,value):
 p=reseal(params(store)['target_permission'],**{field:value})
 assert_no_effect(run(store,target_permission=p))

@pytest.mark.parametrize('hist',[('OUTCOME_LABEL_ONLY',),('TEST_ONLY_DUP','TEST_ONLY_DUP'),('FUTURE_H999','OTHER_ACTOR_H999')],ids=['single-invented','duplicate','future-foreign'])
def test_unwitnessed_history_not_practice(store,hist):
 assert_no_effect(run(store,enacted_history_refs=hist))

def test_own_offer_not_independent_p_action(store):
 assert_no_effect(run(store,other_person_offer_ref=A+':I_IMAGINED_AN_OFFER'))

@pytest.mark.parametrize('kw',[{'enacted_history_refs':()},{'other_person_offer_ref':''},{'material_opportunity_ref':''},{'target_permission':None},{'target_registry':TargetRuleRegistry.production()}],ids=['empty-history','absent-offer','absent-material','missing-permission','unissued-target'])
def test_valid_empty_and_denied_preserve_occurrence(store,kw):
 r=run(store,**kw);assert r.committed
 assert_no_effect(r);assert not store.committed_target_ids()
 assert event()['hash'] in store.committed_event_hashes()

def test_revocation_between_evaluation_and_commit_refused(store):
 args,resp,d=decide(store);assert d.branch is TargetBranch.CREATE
 args['target_permission'].update(reseal(args['target_permission'],revoked=True))
 store.admit_occurrence(args['event_raw'])
 receipt=store.commit(event=args['event_raw'],response=seal({'event_ref':args['event_raw']['hash'],'status':resp.status.value}),decision=d,readset_refs=d.readset_refs)
 assert not receipt.committed or not store.committed_target_ids()

def test_missing_original_source_not_read_at_commit(store):
 args,resp,d=decide(store)
 args['actor_raw']['source_hash']='REVOKED';args['conditioning_sources'].clear()
 store.admit_occurrence(args['event_raw'])
 receipt=store.commit(event=args['event_raw'],response=seal({'event_ref':args['event_raw']['hash']}),decision=d,readset_refs=d.readset_refs)
 assert not receipt.committed or not store.committed_target_ids()

@pytest.mark.parametrize('ddl',["CREATE TRIGGER stop_target BEFORE INSERT ON target_state BEGIN SELECT RAISE(ABORT,'blocked'); END",'ALTER TABLE receipt ADD COLUMN unexpected TEXT NOT NULL DEFAULT \'schema-interference\''],ids=['row-trigger','schema'])
def test_atomic_interference_cold_no_ghost(tmp_path,ddl):
 path=tmp_path/'atomic.sqlite'
 with CandidateStore(path) as s:
  e=event();s.admit_occurrence(e);s.db.execute(ddl);before=s.snapshot()
  r=run(s);assert r.receipt.no_mutation
  assert s.snapshot()==before
 with CandidateStore(path) as reopened:assert reopened.snapshot()==before

def test_later_omitted_mediator_refused(store):
 r=run(store)
 class Omit(LaterActionConsumer):
  def read_target(self,*args):return None,''
 read=read_target_for_later_action(store,consumer=Omit('TEST_ONLY_OMIT','target'),middle_state_id=r.decision.proposal_hash,as_of=30,commit_time=15)
 assert read.status is LaterActionStatus.STATE_ABSENT

def test_later_counterfeit_body_with_real_hash_refused(store):
 r=run(store)
 class Counterfeit(LaterActionConsumer):
  def read_target(self,s,key,as_of):
   real=s.read_target_state(key);return {'actor_id':'OTHER','invented_practice':True},digest(real)
 read=read_target_for_later_action(store,consumer=Counterfeit('TEST_ONLY_COUNTERFEIT','target'),middle_state_id=r.decision.proposal_hash,as_of=30,commit_time=15)
 assert read.status is LaterActionStatus.CONSUMER_READSET_MISMATCH

@pytest.mark.parametrize('state,time',[('WRONG_STATE',30),('state',1)],ids=['mismatched-target','pre-commit-time'])
def test_fictional_performed_receipt_not_admitted(state,time):
 p=make_performed_action_receipt(actor_id=A,act='inspect',actuator_ref='INVENTED',occurrence_ref='NEVER_PERFORMED',action_time=time,consumed_state_hash=state)
 r=admit_performed_action(owner_receipt=p,expected_actor_id=A,expected_act='inspect',consumed_state_hash='state',as_of=40)
 assert not getattr(r,'admitted',False)

def test_seven_default_holds_remain():
 gate=evaluate_release_gate();assert gate.held
 assert len(gate.holds)==7
 assert dict(__import__('rawlsing_next.v3_psepf_zero_positive_guard',fromlist=['x']).DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)=={}

def test_raw_caller_flag_cannot_clear_authenticated_hold():
 gate=evaluate_release_gate(rule_a_issuer_verified=True)
 assert any(h.hold_code.value=='CAN008_RULE_ISSUER_UNVERIFIED' for h in gate.holds)

def test_duplicate_event_id_different_content_refused(store):
 first=run(store);second=run(store,event_raw=event(time=16,content={'fact':'incompatible-new-fact'}),target_permission=None)
 assert not second.committed or len(store.committed_event_hashes())==1

def test_conditioning_view_rejects_mutation():
 v=bind_conditioning(subject=A,sources=sources(),as_of=20)
 original=v.sources[0]['source_ref']
 try:v.sources[0]['source_ref']='MUTATED'
 except TypeError:pass
 assert v.sources[0]['source_ref']==original

def test_guard_denial_does_not_prove_native_effect_guard(store):
 r=run(store)
 assert 'DENY_ZERO_EFFECT' in r.conditioning.guard_outcome
 # This is a TEST_ONLY observation of the actual path, never a native positive.
 assert r.decision.branch is TargetBranch.CREATE
 assert evaluate_release_gate().held
