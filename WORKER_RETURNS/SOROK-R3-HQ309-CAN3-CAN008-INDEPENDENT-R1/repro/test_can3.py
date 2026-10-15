"""CAN3 independently authored sealed controls. No production authorization."""
import copy,json,hashlib
from pathlib import Path
from dataclasses import replace,asdict
from unittest.mock import patch
import pytest
from candidate import can008_candidate_rule as r,positive_chain as pc,owner_transitions as o
from candidate.candidate_registry_fixture import CandidateRegistryFixture,event_digest,digest,CandidateRuleRegistration
from candidate.adopted_contract import GeneratedMemoryState,ADP016_FAIL_CLOSED_STATES
R=Path(__file__).resolve().parents[1]
def save(name,value):
 p=R/'evidence/independent/observations';p.mkdir(parents=True,exist_ok=True);(p/(name+'.json')).write_text(json.dumps(value,indent=2,default=str)+'\n')
def fixture(admit=False):
 reg=CandidateRegistryFixture();assert r.register_default_rule(reg)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE';b=r.build_default_binding()
 e=pc.seal_event(event_id='CAN3_SEALED_EVENT',issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',effective_causal_time='1998-10-03T16:00:00Z',actor_scope='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',admission_state='ADMITTED',public_features=('shift_feedback_window_open','supervisor_solicits_comment'))
 p=r.OwnerPrestate(actor_id=e.actor_scope,world_ref=e.world_ref,world_as_of=e.world_as_of)
 if admit:assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED'
 return reg,e,p,b,o.FixtureOwnerState(reg)
def form(ctx,e,b,**kw):
 args=dict(actor_id=e.actor_scope,basis_event=e,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state='AVAILABLE_SOURCE_BOUND',owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx);args.update(kw);return o.adp016_form_causal_trace(**args)
def epi():
 reg,e,p,b,ctx=fixture(True);m=form(ctx,e,b);ctx.commit_memory(m)
 claim=o.canonical_claim(e.actor_scope,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e.effective_causal_time,e.actor_scope,[e.event_id]);cid=ctx.bind_claim(claim,e)
 args=dict(actor_id=e.actor_scope,claim_ref=cid,stance_kind='BELIEF',stance_operation='ADD',causal_parent_refs=[e.event_id],actor_facing_basis_refs=[e.event_id+':'+e.event_hash],memory_basis_refs=[m['memory']['memory_id']],owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,effective_causal_time=e.effective_causal_time,context=ctx,pre_state_hash=ctx.state_hash)
 return ctx,args

def test_independent_productive_effect_calls_and_precommit_chronology():
 seen=[];instances=[];base=pc.ChainEventLedger;apply=pc.response_rule_apply
 class Observe(base):
  def __init__(self):super().__init__();instances.append(self)
  def commit(self,*a):
   out=super().commit(*a);seen.append(dict(phase='commit',kind=a[0],payload=copy.deepcopy(a[1]),out=copy.deepcopy(out)));return out
 def wrapped(*a):
  out=apply(*a);seen.append(dict(phase='precommit',response=copy.deepcopy(out)));return out
 with patch.object(pc,'ChainEventLedger',Observe),patch.object(pc,'response_rule_apply',wrapped):out=pc.run_positive_chain(_comparison=False)
 assert out['terminal']=='CHAIN_COMPLETE' and out['target_owner_effect_committed'] is True
 pre=[x for x in seen if x['phase']=='precommit'];assert len(pre)==2
 assert all(z['validated'] and not z['committed'] for x in pre for z in x['response']['target_owner_effect_requests'])
 effects=instances[0].read_effects('CAN008_CURRENT_RESPONSE_EFFECT');assert [x['payload']['effect_kind'] for x in effects]==['BUFFER','DEFLECT']
 for x in effects:
  p=x['payload'];rc=p['response_receipt'];assert p['receipt_hash']==rc['receipt_hash'];assert p['event_hash']==rc['precipitating_event']['event_hash'];assert rc['effect_kind']==p['effect_kind']
 assert effects[1]['payload']['prior_effect_refs']==[effects[0]['entry_hash']]
 assert out['production_owner_hold']=='HOLD_NO_ACCEPTED_DESTINATION_OWNER_AUTHORITY'
 save('chronology',dict(calls=seen,result=out,actual_ledger=instances[0].entries))

@pytest.mark.parametrize('field,value,code',[
 ('issuer_authority_id','CAN3_FORGED','BLOCK_FORGED_OR_MISMATCHED_ISSUER'),('issuer_authority_version','9','BLOCK_FORGED_OR_MISMATCHED_ISSUER'),('actor_scope','OTHER','BLOCK_WRONG_ACTOR_SCOPE'),('world_ref','OTHER','BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF'),('world_as_of','1998-10-04T00:00:00Z','BLOCK_STALE_OR_MISMATCHED_WORLD_ASOF'),('effective_causal_time','1997-12-31T23:59:59Z','BLOCK_TIME_OUTSIDE_RULE_SCOPE'),('effective_causal_time','2001-01-01T00:00:00Z','BLOCK_TIME_OUTSIDE_RULE_SCOPE'),('effective_causal_time','1999-01-01','BLOCK_TIME_OUTSIDE_RULE_SCOPE'),('admission_state','REJECTED','BLOCK_UNADMITTED_EVENT'),('event_kind','DRAFT_RESPONSE','BLOCK_NON_OCCURRENCE_KIND'),('event_kind','STATIC_STATE_RECORD','BLOCK_NON_OCCURRENCE_KIND'),('derived_from_future_partition',True,'BLOCK_HIDDEN_FUTURE_LEAK')])
def test_resealed_invalid_scope_is_refused_without_mutation(field,value,code):
 reg,e,p,b,ctx=fixture();bad=replace(e,**{field:value});bad=replace(bad,event_hash=event_digest(bad));before=reg.checkpoint()
 assert r.coupline_evaluate(bad,p,b,reg)['code']==code;assert reg.checkpoint()==before
 # Positive control in same registry ensures no broad refusal masquerades as gate.
 assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED'

@pytest.mark.parametrize('time',['1998-01-01T00:00:00Z','2000-12-31T23:59:59Z'])
def test_temporal_boundary_positive(time):
 reg,e,p,b,ctx=fixture();e=replace(e,effective_causal_time=time);e=replace(e,event_hash=event_digest(e));assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED'

@pytest.mark.parametrize('field,value',[('rule_version','UNISSUED'),('rule_content_hash','forged'),('eligible_conditioning_owner_signatures',('FORGED',)),('target_authority_kind','PUBLIC_STANDING'),('atomic_commit_behavior','partial'),('adp020_binding','unissued')])
def test_rule_mutation_fails_before_admission(field,value):
 reg,e,p,b,ctx=fixture();bad=replace(b,**{field:value});before=reg.checkpoint();assert r.coupline_evaluate(e,p,bad,reg)['code']=='RESPONSE_COUPLING_RULE_MISSING';assert reg.checkpoint()==before

@pytest.mark.parametrize('stage',['after_coupling','after_trace_validation','after_epistemic','after_current_commit','after_owner_journal'])
def test_all_five_transaction_boundaries_restore_every_state_set(stage):
 reg=CandidateRegistryFixture();out=pc.run_positive_chain(registry=reg,failure_at=stage,_comparison=False)
 assert out['terminal']=='FIRST_EVENT_REFUSED' and not out['ledger_entries']
 assert all(out['state'][k] in ({},[]) for k in ['memories','memory_transitions','claims','emissions','stances','epistemic_transitions','state_sets','permissions'])
 assert reg.verify() and reg._events=={} and reg._evaluations=={}
 assert len(reg._rules)==1  # Setup registration survives; event transaction does not.
 save('rollback_'+stage,out)

def test_later_rollback_exact_first_snapshot():
 a=pc.run_positive_chain(include_later_event=False,_comparison=False);b=pc.run_positive_chain(failure_at='later_after_coupling',_comparison=False)
 assert b['terminal']=='LATER_EVENT_REFUSED' and b['state']==a['state'] and b['n_ledger_entries']==3

@pytest.mark.parametrize('mode',['memory_refs','epistemic_refs','both_refs','withheld_history','absent_history','both_refs_and_history'])
def test_genuine_state_and_history_ablation(mode):
 before=[];after=[];reads=[];orig=pc.coupline_evaluate;base=pc.ChainEventLedger
 def evaluate(e,p,b,reg):
  if e.event_id.startswith('EV2'):
   before.append(asdict(p))
   if mode in ('memory_refs','both_refs','both_refs_and_history'):p.adp016_memory_refs=()
   if mode in ('epistemic_refs','both_refs','both_refs_and_history'):p.adp017_claim_refs=()
   after.append(asdict(p))
  return orig(e,p,b,reg)
 class Ledger(base):
  def read_effects(self,kind=None):
   actual=super().read_effects(kind);ret=[] if mode in ('withheld_history','both_refs_and_history') else actual
   reads.append(dict(actual=copy.deepcopy(actual),returned=copy.deepcopy(ret)));return ret
 with patch.object(pc,'coupline_evaluate',evaluate),patch.object(pc,'ChainEventLedger',Ledger):
  out=pc.run_positive_chain(_comparison=False,later_event_requires_prior_effect=False,omit_first_effect=mode=='absent_history')
 assert before[0]['adp016_memory_refs'] and before[0]['adp017_claim_refs']
 save('ablation_'+mode,dict(before=before,after=after,reads=reads,result=out))
 if mode in ('memory_refs','epistemic_refs'):
  assert out['terminal']=='LATER_EVENT_REFUSED' and out['code']=='RESPONSE_CONDITIONING_OWNER_UNBOUND'
  assert out['n_ledger_entries']==3
  return
 assert out['terminal']=='CHAIN_COMPLETE';expected='AMPLIFY' if mode in ('withheld_history','absent_history','both_refs_and_history') else 'DEFLECT'
 assert out['later_event_response']['effect_kind']==expected
 assert out['later_event_response']['prior_effect_read']==(expected=='DEFLECT')
 assert bool(reads[0]['returned'])==(expected=='DEFLECT')
 if mode=='withheld_history':assert reads[0]['actual'] and reads[0]['returned']==[]
 if mode=='absent_history':assert reads[0]['actual']==[]
 save('ablation_'+mode,dict(before=before,after=after,reads=reads,result=out))

@pytest.mark.parametrize('change',['alias','truncate','rehash','reorder','payload'])
def test_immutable_ledger(change):
 l=pc.ChainEventLedger();payload={'nested':['source']};out=l.commit('A',payload,'1998',[]);l.commit('B',{},'1999',['A'])
 if change=='alias':
  payload['nested'].append('external');out['entry']['payload']['nested'].append('return alias');read=l.read_effects();read[0]['payload']['nested'].append('read alias');assert l.read_effects()[0]['payload']=={'nested':['source']};return
 if change=='truncate':l.entries.pop()
 elif change=='reorder':l.entries.reverse()
 else:
  l.entries[0]['payload']['nested'].append('corrupt')
  if change=='rehash':l.entries[0]['entry_hash']=digest({k:v for k,v in l.entries[0].items() if k!='entry_hash'})
 with pytest.raises(pc.LedgerIntegrityError):l.read_effects()


def test_corruption_of_real_prior_read_refuses_later_transaction():
 base=pc.ChainEventLedger
 class Corrupt(base):
  def read_effects(self,kind=None):self.entries[0]['payload']['effect_kind']='AMPLIFY';return super().read_effects(kind)
 with patch.object(pc,'ChainEventLedger',Corrupt):out=pc.run_positive_chain(_comparison=False)
 assert out['terminal']=='LATER_EVENT_REFUSED' and out['code']=='LEDGER_CONTENT_MUTATED'
 save('corrupt_read',out)


def test_valid_duplicate_event_and_historical_property_request():
 reg,e,p,b,ctx=fixture();c=r.coupline_evaluate(e,p,b,reg);response=r.response_rule_apply(c,p,b,'BUFFER')
 assert response['target_owner_effect_requests']==[dict(target_owner_kind='CAN008_CURRENT',validated=True,committed=False,request_kind='CANDIDATE_CURRENT_HISTORY_ONLY')]
 assert response['destination_owner_hold']=='HOLD_NO_ACCEPTED_ADP016_ADP017_POSITIVE_AUTHORITY'
 assert r.coupline_evaluate(e,p,b,reg)['code']=='BLOCK_DUPLICATE_EVENT_IDENTITY'


def test_valid_memory_historical_k3_recall_delete_rehydration_hashes():
 reg,e,p,b,ctx=fixture(True);proposal=form(ctx,e,b);ctx.commit_memory(proposal);m=GeneratedMemoryState(**proposal['memory']);assert ctx.verify()
 assert proposal['first_person_origin_claimable'] is False and set(proposal['must_not_output'])=={'actor_knows','actor_believes','may_claim_first_person','V2_may_render_as_fact'}
 for kind,args,code in [('RECALL',{},'UNAUTHORIZED_RECALL_CUE'),('DELETE_MEMORY',{},'UNAUTHORIZED_TRANSITION'),('REACTIVATE',{'declared_parent_hash':'wrong'},'PARENT_EVENT_HASH_MISMATCH'),('REACTIVATE',{'pre_state_hash':'wrong'},'PRE_STATE_HASH_MISMATCH')]:
  kw=dict(parent_event=e,pre_state_hash=m.current_state_hash,context=ctx);kw.update(args);before=ctx.checkpoint()
  with pytest.raises(o.OwnerTransitionError) as err:o.adp016_attempt_transition(m,kind,**kw)
  assert err.value.code==code and ctx.checkpoint()==before
 with pytest.raises(o.OwnerTransitionError) as err:o.adp016_rehydration_refused(m,'source analyst content')
 assert err.value.code=='UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION'
 assert o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',m.representation_kind,m.memory_accessibility_state)['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'
 dead=replace(m,memory_accessibility_state='INACCESSIBLE',retention_state='CONTENT_UNAVAILABLE')
 assert o.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESSIBLE',dead)['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'

@pytest.mark.parametrize('field,value,code',[('basis_event',None,'MISSING_PARENT_EVENT'),('trace_key','FAKE_MEMORY','UNAUTHORIZED_TRANSITION'),('content_state','V2_TRANSCRIPT','INELIGIBLE_NONCAUSAL_SOURCE'),('owning_rule_version','','MISSING_RULE_VERSION'),('owning_rule_hash','h','UNAUTHORIZED_TRANSITION'),('parent_state_hash','STALE','PRE_STATE_HASH_MISMATCH'),('stochastic',True,'MISSING_RNG_AUTHORITY'),('actor_id','OTHER','DEFERRED_MISSING_MEMORY_BASIS')])
def test_memory_formation_gates(field,value,code):
 reg,e,p,b,ctx=fixture(True);before=ctx.checkpoint()
 with pytest.raises(o.OwnerTransitionError) as err:form(ctx,e,b,**{field:value})
 assert err.value.code==code and ctx.checkpoint()==before

@pytest.mark.parametrize('field,value',[('actor_id','OTHER'),('claim_ref','unknown'),('stance_kind','KNOWLEDGE'),('actor_facing_basis_refs',[]),('causal_parent_refs',['OTHER']),('memory_basis_refs',['UNKNOWN']),('owning_rule_hash','forged'),('effective_causal_time','1999-01-01T00:00:00Z'),('pre_state_hash','STALE')])
def test_epistemic_exact_provenance_and_no_knowledge(field,value):
 ctx,args=epi();before=ctx.checkpoint();args[field]=value;out=o.adp017_apply_epistemic_effect(**args)
 assert out['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and ctx.checkpoint()==before


def test_k5_belief_unaffected_by_objective_labels_and_public_owner_held():
 outs=[]
 for relation in ['OBJECTIVE_SUPPORTED','OBJECTIVE_CONTRADICTED','OBJECTIVE_UNRESOLVED']:
  ctx,args=epi();args['claim_objective_relation']=relation;out=o.adp017_apply_epistemic_effect(**args);outs.append(ctx.data())
  assert out['public_ratification']=='HOLD_NO_PUBLIC_STANDING_OWNER';assert out['production_owner_commit'] is False
  cid=args['claim_ref'];h=ctx.state_sets[cid]['current_state_hash'];check=o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',context=ctx,claim_ref=cid,state_hash=h)
  assert check['first_person_permission']=='PERMIT_FIRST_PERSON_BELIEF' and check['self_explanation_of_hidden_origin']=='BLOCKED'
  assert o.adp017_first_person_check('KNOWLEDGE','CLAIM_ACCESSIBLE',context=ctx,claim_ref=cid,state_hash=h)['first_person_permission']=='DEFER_MISSING_AUTHORITY'
 assert outs[0]==outs[1]==outs[2]

@pytest.mark.parametrize('unknown',['RETENTION_UNKNOWN','ACCESS_UNKNOWN'])
def test_unknown_memory_remains_unknown(unknown):
 reg,e,p,b,ctx=fixture(True);m=GeneratedMemoryState(**form(ctx,e,b)['memory']);kw={'retention_state':unknown} if unknown=='RETENTION_UNKNOWN' else {'memory_accessibility_state':unknown};m=replace(m,**kw)
 assert o.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESS_UNKNOWN',m)['first_person_permission']=='DEFER_MISSING_AUTHORITY';assert all(getattr(m,k)==v for k,v in kw.items())


def test_exact_replay_and_17_states_law_not_legacy_16():
 a=pc.run_positive_chain(_comparison=False);b=pc.run_positive_chain(_comparison=False);assert a['full_replay_digest']==b['full_replay_digest'] and a['ledger_hash']==b['ledger_hash'] and a['state']==b['state']
 law=json.loads((R/'runtime/law/ADP016.txt').read_text());assert {x['state'] for x in law['fail_closed_states']}==set(ADP016_FAIL_CLOSED_STATES) and len(ADP016_FAIL_CLOSED_STATES)==17


def test_actual_changed_source_body_is_refused_on_evaluation():
 import shutil,subprocess,sys,os
 target=R/'runtime/can3_body_probe';target.mkdir(exist_ok=True)
 shutil.copytree(Path(r.__file__).parent,target/'candidate',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
 script='''
from pathlib import Path
from candidate import can008_candidate_rule as r,positive_chain as pc
from candidate.candidate_registry_fixture import CandidateRegistryFixture
reg=CandidateRegistryFixture();r.register_default_rule(reg);b=r.build_default_binding()
e=pc.seal_event(event_id='BODY_PROBE',issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',effective_causal_time='1998-10-03T16:00:00Z',actor_scope='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',admission_state='ADMITTED',public_features=('valid',))
p=r.OwnerPrestate(actor_id=e.actor_scope,world_ref=e.world_ref,world_as_of=e.world_as_of)
f=Path(pc.__file__);f.write_bytes(f.read_bytes()+b'\\n# CAN3 independent source mutation\\n')
assert r.binding_digest(b)!=b.rule_content_hash
out=r.coupline_evaluate(e,p,b,reg);assert out['code']=='RESPONSE_COUPLING_RULE_MISSING';assert reg.event(e.event_id) is None
print(out)
'''
 out=subprocess.run([sys.executable,'-c',script],cwd=target,capture_output=True,text=True,env={'PATH':os.environ['PATH'],'PYTHONPATH':str(target)})
 save('body_mutation',dict(returncode=out.returncode,stdout=out.stdout,stderr=out.stderr));assert out.returncode==0

@pytest.mark.parametrize('mode',['unadmitted_parent','changed_parent','actor','features','prestate','rng','rule'])
def test_all_seven_adp016_gates_with_valid_formation_control(mode):
 reg,e,p,b,ctx=fixture(True);positive=form(ctx,e,b);assert positive['status']=='ADP016_FORMATION_VALIDATED_IN_FIXTURE'
 before=ctx.checkpoint();kw={}
 if mode=='unadmitted_parent':kw['basis_event']=replace(e,admission_state='PROPOSED')
 if mode=='changed_parent':kw['basis_event']=replace(e,event_hash='FAKE')
 if mode=='actor':kw['actor_id']='OTHER'
 if mode=='features':kw['basis_event']=replace(e,public_features=('invented',))
 if mode=='prestate':kw['parent_state_hash']='STALE'
 if mode=='rng':kw['stochastic']=True
 if mode=='rule':kw['owning_rule_hash']='UNISSUED'
 with pytest.raises(o.OwnerTransitionError):form(ctx,e,b,**kw)
 assert ctx.checkpoint()==before

@pytest.mark.parametrize('state',ADP016_FAIL_CLOSED_STATES)
def test_17_adopted_negative_or_unknown_behaviors(state):
 reg,e,p,b,ctx=fixture(True);proposal=form(ctx,e,b);ctx.commit_memory(proposal);m=GeneratedMemoryState(**proposal['memory']);before=ctx.checkpoint()
 # API has no session/confabulation promotion operation: rejection behavior is
 # tested without claiming those exact state labels are emitted by this fixture.
 if state in ('RETENTION_UNKNOWN','ACCESS_UNKNOWN'):
  changed=replace(m,**({'retention_state':state} if state=='RETENTION_UNKNOWN' else {'memory_accessibility_state':state}))
  assert o.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESS_UNKNOWN',changed)['first_person_permission']=='DEFER_MISSING_AUTHORITY'
 elif state=='DEFERRED_MISSING_MEMORY_BASIS':
  assert form(ctx,e,b,context=None)['status']==state
 elif state=='MEMORY_ID_COLLISION':
  # Formation stages a proposal by design; measure COMMIT refusal from its
  # immediate prestate, rather than conflating staging with a failed commit.
  duplicate=form(ctx,e,b);before=ctx.checkpoint()
  with pytest.raises(o.OwnerTransitionError):ctx.commit_memory(duplicate)
 elif state=='UNKNOWN_MEMORY_ID':
  ghost=replace(m,memory_id='UNKNOWN');ghost=replace(ghost,current_state_hash=o.memory_semantic_hash(asdict(ghost)))
  with pytest.raises(o.OwnerTransitionError) as err:o.adp016_attempt_transition(ghost,'DEGRADE',parent_event=e,pre_state_hash=ghost.current_state_hash,context=ctx)
  assert err.value.code==state
 elif state=='UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION':
  with pytest.raises(o.OwnerTransitionError) as err:o.adp016_rehydration_refused(m,'objective analyst event')
  assert err.value.code==state
 else:
  kind='DEGRADE';kw=dict(parent_event=e,pre_state_hash=m.current_state_hash,context=ctx);target=m
  if state=='INELIGIBLE_NONCAUSAL_SOURCE':
   with pytest.raises(o.OwnerTransitionError) as err:form(ctx,e,b,content_state='V2_TRANSCRIPT')
   assert err.value.code==state;return
  if state=='MISSING_RULE_VERSION':
   with pytest.raises(o.OwnerTransitionError) as err:form(ctx,e,b,owning_rule_version='')
   assert err.value.code==state;return
  if state=='MISSING_PARENT_EVENT':kw['parent_event']=None
  if state=='PARENT_EVENT_HASH_MISMATCH':kw['declared_parent_hash']='FAKE'
  if state=='PRE_STATE_HASH_MISMATCH':kw['pre_state_hash']='STALE'
  if state=='UNAUTHORIZED_TRANSITION':kind='DELETE_MEMORY'
  if state=='UNAUTHORIZED_RECALL_CUE':kind='RECALL'
  if state=='UNAUTHORIZED_V2_SESSION_PROMOTION':kind='PROMOTE_V2_SESSION'
  if state=='UNSUPPORTED_CONFABULATION':kind='CONFABULATE'
  if state=='MISSING_RNG_AUTHORITY':kw['stochastic']=True
  if state=='INTEGRITY_FAILURE':target=replace(m,current_state_hash='CORRUPTED')
  with pytest.raises(o.OwnerTransitionError) as err:o.adp016_attempt_transition(target,kind,**kw)
  if state not in ('UNSUPPORTED_CONFABULATION','UNAUTHORIZED_V2_SESSION_PROMOTION'):assert err.value.code==state
 assert ctx.checkpoint()==before

@pytest.mark.parametrize('field,value',[('issuer_authority_id','UNISSUED'),('issuer_authority_version','2'),('actor_scope','OTHER'),('temporal_scope','ALL_TIME'),('target_owner_kind','ADP017'),('rule_version','NEW')])
def test_fixture_registration_cannot_mint_other_issuer_or_scope(field,value):
 reg,e,p,b,ctx=fixture();good=reg.lookup(b.rule_id,b.rule_version);fresh=CandidateRegistryFixture();bad=replace(good,**{field:value})
 assert fresh.register(bad)['code']=='REGISTRATION_BINDING_MISMATCH';assert fresh.verify() and fresh.ledger()==[]
 assert fresh.register(good)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE'

@pytest.mark.parametrize('time',['1998-10-03T16:00:00Z','1998-01-01T00:00:00Z'])
def test_actual_parent_chronology_without_reverse_flag(time):
 reg,e,p,b,ctx=fixture(True);child=replace(e,event_id='CAN3_CHILD',effective_causal_time=time,causal_parent_event_ids=(e.event_id,));child=replace(child,event_hash=event_digest(child));before=reg.checkpoint()
 assert r.coupline_evaluate(child,p,b,reg)['code']=='BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT';assert reg.checkpoint()==before


def test_lawful_memory_commit_idempotence_alias_and_conflicting_duplicate():
 reg,e,p,b,ctx=fixture(True);proposal=form(ctx,e,b);ctx.commit_memory(proposal);before=ctx.checkpoint()
 assert ctx.commit_memory(proposal)['status']=='IDEMPOTENT_REPLAY' and ctx.checkpoint()==before
 changed=copy.deepcopy(proposal);changed['memory']['source_feature_bindings']=('unissued replacement',)
 with pytest.raises(o.OwnerTransitionError):ctx.commit_memory(changed)
 assert ctx.checkpoint()==before
 exported=ctx.data();exported['memories'].clear();assert ctx.verify() and ctx.memories


def test_epistemic_exact_replay_is_failclosed_and_never_duplicates_state():
 ctx,args=epi();first=o.adp017_apply_epistemic_effect(**args);before=ctx.checkpoint();second=o.adp017_apply_epistemic_effect(**args)
 # Current API regenerates effects and requires exact prestate. It rejects old
 # prestate, rather than furnishing an idempotent replay receipt. This is a
 # documented replay-API limitation, not proof of full ADP017 H28 implementation.
 assert second['decision_state']=='BLOCKED_INTEGRITY_FAILURE' and ctx.checkpoint()==before
 assert len(ctx.stances)==1 and len(ctx.epistemic_transitions)==1
 save('epistemic_replay_ceiling',dict(first=first,second=second,state=ctx.data(),limitation='No idempotent ADP017 effect-replay receipt; exact stale call safely refused'))
