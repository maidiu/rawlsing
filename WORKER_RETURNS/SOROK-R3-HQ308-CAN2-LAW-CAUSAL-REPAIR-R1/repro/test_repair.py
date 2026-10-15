"""Sourcefree repair controls using fully admitted/sealed positive fixtures.

These are author tests after inherited freeze, not independent acceptance.
Mutations must reach valid paths, not pass because every request is refused.
"""
import copy,hashlib,json,sys
from pathlib import Path
from dataclasses import replace,asdict
from unittest.mock import patch
import pytest
RET=Path(__file__).resolve().parents[1];sys.path.insert(0,str(RET))
from candidate import can008_candidate_rule as r,positive_chain as pc,owner_transitions as o
from candidate.candidate_registry_fixture import CandidateRegistryFixture,digest,event_digest
from candidate.adopted_contract import GeneratedMemoryState


def fixture():
    reg=CandidateRegistryFixture();assert r.register_default_rule(reg)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE'
    e=pc.seal_event(event_id='CONTROL_EVENT',issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',effective_causal_time='1998-10-03T16:00:00Z',actor_scope='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',admission_state='ADMITTED',public_features=('shift_feedback_window_open','supervisor_solicits_comment'))
    p=r.OwnerPrestate(actor_id=e.actor_scope,world_ref=e.world_ref,world_as_of=e.world_as_of)
    b=r.build_default_binding();return reg,e,p,b

def admitted():
    reg,e,p,b=fixture();assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED'
    ctx=o.FixtureOwnerState(reg);return reg,e,p,b,ctx

def memory(ctx,e,b,**kw):
    args=dict(actor_id=e.actor_scope,basis_event=e,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state='AVAILABLE_SOURCE_BOUND',owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx);args.update(kw)
    return o.adp016_form_causal_trace(**args)

def epistemic_setup():
    reg,e,p,b,ctx=admitted();m=memory(ctx,e,b);ctx.commit_memory(m)
    claim=o.canonical_claim(e.actor_scope,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e.effective_causal_time,e.actor_scope,[e.event_id]);cid=ctx.bind_claim(claim,e)
    args=dict(actor_id=e.actor_scope,claim_ref=cid,stance_kind='BELIEF',stance_operation='ADD',causal_parent_refs=[e.event_id],actor_facing_basis_refs=[e.event_id+':'+e.event_hash],memory_basis_refs=[m['memory']['memory_id']],owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,effective_causal_time=e.effective_causal_time,context=ctx,pre_state_hash=ctx.state_hash)
    return ctx,args


def test_positive_path_and_exact_replay_and_real_control():
    a=pc.run_positive_chain();b=pc.run_positive_chain();c=pc.run_control_without_prior_effect()
    assert a['terminal']==b['terminal']==c['terminal']=='CHAIN_COMPLETE'
    assert a['full_replay_digest']==b['full_replay_digest']
    assert a['later_event_response']['effect_kind']=='DEFLECT' and c['later_event_response']['effect_kind']=='AMPLIFY'
    assert a['later_event_response']['prior_effect_read'] is True and c['later_event_response']['prior_effect_read'] is False
    assert a['later_response_typed_difference']['control_executed'] is True
    assert a['n_ledger_entries']==4 and c['n_ledger_entries']==3
    assert a['production_owner_hold']=='HOLD_NO_ACCEPTED_DESTINATION_OWNER_AUTHORITY'
    assert a['public_standing_hold']=='HOLD_NO_PUBLIC_RATIFICATION_OWNER'
    state=a['state'];assert state['memories'] and state['stances'] and state['state_sets'] and state['permissions']
    assert a['later_event_response']['candidate_state_read_hash']==a['state_hash']


@pytest.mark.parametrize('stage',['after_coupling','after_trace_validation','after_epistemic','after_current_commit','after_owner_journal'])
def test_all_first_event_transaction_boundaries_rollback(stage):
    result=pc.run_positive_chain(failure_at=stage)
    assert result['terminal']=='FIRST_EVENT_REFUSED'
    assert result['ledger_entries']==[] and result['state']['memories']==result['state']['stances']=={}
    assert not any(x.get('kind')=='EVENT_IDENTITY' for x in result['registry']['ledger'])


def test_later_failure_retains_exact_first_committed_event():
    a=pc.run_positive_chain(include_later_event=False);b=pc.run_positive_chain(failure_at='later_after_coupling')
    assert b['terminal']=='LATER_EVENT_REFUSED' and b['n_ledger_entries']==3
    assert b['state']==a['state']


@pytest.mark.parametrize('field,value',[('issuer_authority_id','FORGED'),('issuer_authority_version','2'),('actor_scope','OTHER'),('effective_causal_time','2099-01-01T00:00:00Z'),('world_as_of','1999'),('event_hash',''),('admission_state','PROPOSED'),('derived_from_future_partition',True),('event_kind','STATIC_STATE_RECORD')])
def test_invalid_sealed_event_never_admits_or_mutates(field,value):
    reg,e,p,b=fixture();bad=replace(e,**{field:value});before=reg.ledger()
    out=r.coupline_evaluate(bad,p,b,reg)
    assert out['committed'] is False and out['decision_state']!='COUPLING_EVALUATED';assert reg.ledger()==before


FIELDS=['rule_id','eligible_event_authority_signatures','actor_scope','receivability_semantics','eligible_conditioning_owner_signatures','conditioning_causal_use_roles','counterpart_scoping','modality_evidence_authorities','uptake_appraisal_semantics','recruitment_semantics','multiplicity_handling','co_determination_closure','prior_response_history_predicates','current_condition_effort_role','effect_kinds','target_validation','pff_current_consequence_projection','valid_empty_behavior','missing_deferred_ambiguous_behavior','quantitative_contract','adp020_binding','atomic_commit_behavior','provenance_replay_requirements']
@pytest.mark.parametrize('field',FIELDS)
def test_binding_mutation_enters_valid_event_path_and_refuses(field):
    reg,e,p,b=fixture();v=getattr(b,field);bad=replace(b,**{field:() if isinstance(v,tuple) else ''})
    out=r.coupline_evaluate(e,p,bad,reg)
    assert out['decision_state']=='RESPONSE_COUPLING_RULE_MISSING'
    # The unchanged valid event/registry IS productive. Five unused conditional
    # descriptors stay N/A scientifically; refusal here is immutable rule custody.
    good=r.coupline_evaluate(e,p,b,reg);assert good['decision_state']=='COUPLING_EVALUATED'
    assert r.response_rule_apply(good,p,b,'BUFFER')['decision_state']=='RESPONSE_EFFECTS_PRODUCED'


def test_rule_body_digest_and_registry_tamper_enforcement():
    reg,e,p,b=fixture();assert len(b.rule_content_hash)==64
    reg._rules.clear()
    assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='RESPONSE_COUPLING_RULE_MISSING'
    assert r.response_rule_apply({'decision_state':'COUPLING_EVALUATED'},p,b,'BUFFER')['decision_state']!='RESPONSE_EFFECTS_PRODUCED'


def test_complete_event_hash_detects_content_change_and_unknown_parent():
    reg,e,p,b=fixture();bad=replace(e,public_features=('changed',))
    assert r.coupline_evaluate(bad,p,b,reg)['code']=='PARENT_EVENT_HASH_MISMATCH'
    bad=replace(e,causal_parent_event_ids=('UNKNOWN',));bad=replace(bad,event_hash=event_digest(bad))
    assert r.coupline_evaluate(bad,p,b,reg)['code']=='MISSING_PARENT_EVENT'


def test_parent_time_is_checked_without_caller_flag():
    reg,e,p,b=fixture();assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED'
    child=replace(e,event_id='BACKWARD',effective_causal_time='1998-01-01T00:00:00Z',causal_parent_event_ids=(e.event_id,));child=replace(child,event_hash=event_digest(child))
    assert r.coupline_evaluate(child,p,b,reg)['code']=='BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT'


@pytest.mark.parametrize('change',['content','truncate','reorder','rehash','alias'])
def test_history_integrity_and_aliases(change):
    l=pc.ChainEventLedger();payload={'x':['original']};ret=l.commit('A',payload,'1998',[]);l.commit('B',{},'1999',['A'])
    if change=='alias':
        payload['x'].append('caller');ret['entry']['payload']['x'].append('returned');assert l.read_effects()[0]['payload']=={'x':['original']};return
    if change=='content':l.entries[0]['payload']['x']=['corrupt']
    if change=='truncate':l.entries.pop()
    if change=='reorder':l.entries.reverse()
    if change=='rehash':l.entries[0]['payload']['x']=['corrupt'];l.entries[0]['entry_hash']=digest({k:v for k,v in l.entries[0].items() if k!='entry_hash'})
    with pytest.raises(pc.LedgerIntegrityError):l.read_effects()
    with pytest.raises(pc.LedgerIntegrityError):l.commit('C',{},'2000',[])


def test_memory_actual_commit_source_bindings_and_idempotence():
    reg,e,p,b,ctx=admitted();before=ctx.state_hash;proposal=memory(ctx,e,b)
    assert ctx.state_hash==before
    for binding in proposal['memory']['source_feature_bindings']:
        record=json.loads(binding);assert record['feature'] in e.public_features and record['source_event']==e.event_id+':'+e.event_hash
    commit=ctx.commit_memory(proposal);assert commit['production_owner_commit'] is False
    after=ctx.state_hash;assert after!=before
    assert ctx.commit_memory(proposal)['status']=='IDEMPOTENT_REPLAY' and ctx.state_hash==after
    proposal['memory']['source_feature_bindings']=('injected',);assert ctx.verify()
    assert ctx.memories[commit['memory_id']]['source_feature_bindings']!=('injected',)


@pytest.mark.parametrize('change',['parent','actor','feature','authority','prestate','rule','version','rng','missing','noncausal'])
def test_memory_gate_refusals_are_neutral(change):
    reg,e,p,b,ctx=admitted();kw={}
    if change=='parent':kw['basis_event']=replace(e,event_hash='FORGED')
    if change=='actor':kw['actor_id']='OTHER'
    if change=='feature':kw['trace_key']='INVENTED_CHILDHOOD'
    if change=='authority':kw['authority_id']='A'
    if change=='prestate':kw['parent_state_hash']=''
    if change=='rule':kw['owning_rule_hash']='h'
    if change=='version':kw['owning_rule_version']=''
    if change=='rng':kw['stochastic']=True
    if change=='missing':kw['basis_event']=None
    if change=='noncausal':kw['content_state']='V2_TRANSCRIPT'
    before=ctx.checkpoint()
    with pytest.raises(o.OwnerTransitionError):memory(ctx,e,b,**kw)
    assert ctx.checkpoint()==before


def test_memory_proposal_tampering_cannot_commit():
    reg,e,p,b,ctx=admitted();proposal=memory(ctx,e,b);before=ctx.state_hash
    proposal['memory']['actor_id']='OTHER';proposal['memory']['current_state_hash']=o.memory_semantic_hash(proposal['memory']);proposal['transition']['post_state_hash']=proposal['memory']['current_state_hash']
    with pytest.raises(o.OwnerTransitionError):ctx.commit_memory(proposal)
    assert ctx.state_hash==before


def test_no_context_is_deferred_and_no_unbound_proposal_applies():
    reg,e,p,b,ctx=admitted();proposal=memory(ctx,e,b,context=None)
    assert proposal['status']=='DEFERRED_MISSING_MEMORY_BASIS' and proposal['committed'] is False
    with pytest.raises(o.OwnerTransitionError):ctx.commit_memory(proposal)
    c,args=epistemic_setup();args['context']=None
    out=o.adp017_apply_epistemic_effect(**args);assert out['decision_state']=='DEFERRED_MISSING_EPISTEMIC_BASIS' and out['stance_persisted'] is False


def test_memory_collision_and_no_unauthorized_transition():
    reg,e,p,b,ctx=admitted();proposal=memory(ctx,e,b);ctx.commit_memory(proposal)
    another=memory(ctx,e,b)
    with pytest.raises(o.OwnerTransitionError) as err:ctx.commit_memory(another)
    assert err.value.code=='MEMORY_ID_COLLISION'
    mem=GeneratedMemoryState(**proposal['memory'])
    for kind in ('DELETE_MEMORY','RECALL','DEGRADE','ACCESS_INCREASE'):
        with pytest.raises(o.OwnerTransitionError):o.adp016_attempt_transition(mem,kind,parent_event=e,pre_state_hash=mem.current_state_hash,declared_parent_hash=e.event_hash,context=ctx)


@pytest.mark.parametrize('mutation',['claim','basis','parent','rule','actor','time','prestate','knowledge'])
def test_epistemic_gates_with_real_canonical_positive_control(mutation):
    ctx,args=epistemic_setup();before=ctx.checkpoint();bad=copy.copy(args)
    if mutation=='claim':bad['claim_ref']='FREE_TEXT_CLAIM'
    if mutation=='basis':bad['actor_facing_basis_refs']=['FORGED']
    if mutation=='parent':bad['causal_parent_refs']=['FORGED']
    if mutation=='rule':bad['owning_rule_hash']='h'
    if mutation=='actor':bad['actor_id']='OTHER'
    if mutation=='time':bad['effective_causal_time']='2099-01-01T00:00:00Z'
    if mutation=='prestate':bad['pre_state_hash']='STALE'
    if mutation=='knowledge':bad['stance_kind']='KNOWLEDGE';bad['claim_objective_relation']='OBJECTIVE_SUPPORTED'
    out=o.adp017_apply_epistemic_effect(**bad)
    assert out['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and ctx.checkpoint()==before
    assert o.adp017_apply_epistemic_effect(**args)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'


def test_canonical_claim_tampering_and_foreign_feature_emission_refuse():
    reg,e,p,b,ctx=admitted();c=o.canonical_claim(e.actor_scope,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e.effective_causal_time,e.actor_scope,[e.event_id]);c['object_or_value']='INVENTED'
    with pytest.raises(o.OwnerTransitionError):ctx.bind_claim(c,e)
    before=ctx.state_hash;ctx.claims['FAKE']=c;assert not ctx.verify()
    assert ctx.state_hash==before


def test_epistemic_operations_change_only_exact_record_and_permission_snapshot():
    ctx,args=epistemic_setup();out=o.adp017_apply_epistemic_effect(**args);eid=out['effect']['effect_id'];cid=args['claim_ref'];state=ctx.state_sets[cid]
    law=json.loads((RET/'runtime_root/law/ADP017.txt').read_text())
    assert set(law['epistemic_state_model']['required_fields'])<=set(state)
    assert ctx.permissions[cid]['epistemic_state_hash']==state['current_state_hash']
    # NO_CHANGE must leave every state and transition byte unchanged.
    args.update(pre_state_hash=ctx.state_hash,stance_operation='NO_CHANGE');before=ctx.checkpoint()
    assert o.adp017_apply_epistemic_effect(**args)['decision_state']=='NO_EPISTEMIC_TRANSITION';assert ctx.checkpoint()==before
    args.update(stance_operation='WITHDRAW');out=o.adp017_apply_epistemic_effect(**args);assert out['decision_state']=='DEFERRED_MISSING_EPISTEMIC_BASIS'
    args['target_record_ref']=eid;out=o.adp017_apply_epistemic_effect(**args);assert out['decision_state']=='APPLIED_EPISTEMIC_TRANSITION' and not ctx.stances
    assert ctx.permissions[cid]['permission']=='DENY_FIRST_PERSON_CLAIM'


def test_k5_truth_cannot_create_or_edit_belief_or_public_standing():
    a,x=epistemic_setup();b,y=epistemic_setup();x['claim_objective_relation']='OBJECTIVE_SUPPORTED';y['claim_objective_relation']='OBJECTIVE_CONTRADICTED'
    ra=o.adp017_apply_epistemic_effect(**x);rb=o.adp017_apply_epistemic_effect(**y)
    assert ra['effect']==rb['effect'] and a.data()==b.data()
    assert ra['public_ratification']=='HOLD_NO_PUBLIC_STANDING_OWNER'


@pytest.mark.parametrize('kind,access,retention,wanted',[('CAUSAL_TRACE_MEMORY','NOT_APPLICABLE_CAUSAL_TRACE','RETAINED','DENY_FIRST_PERSON_CLAIM'),('EVENT_REFERENTIAL_MEMORY','INACCESSIBLE','RETAINED','DENY_FIRST_PERSON_CLAIM'),('EVENT_REFERENTIAL_MEMORY','ACCESS_UNKNOWN','RETENTION_UNKNOWN','DEFER_MISSING_AUTHORITY')])
def test_k3_permissions_do_not_promote_trace_or_unknown(kind,access,retention,wanted):
    reg,e,p,b,ctx=admitted();m=GeneratedMemoryState(**memory(ctx,e,b)['memory']);m=replace(m,representation_kind=kind,memory_accessibility_state=access,retention_state=retention)
    out=o.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESSIBLE',m)
    assert out['first_person_permission']==wanted and out['memory_inaccessibility_auto_erases_stance'] is False


def test_guard_empty_exact_before_and_after_every_positive_fixture():
    sys.path.insert(0,str(RET/'runtime_root/original'))
    from rawlsing_next import v3_psepf_zero_positive_guard as g
    raw=Path(g.__file__).read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='e0528d65215cb431196570c38bac4eae94217a1b'
    assert dict(g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)=={}
    assert pc.run_positive_chain()['terminal']=='CHAIN_COMPLETE'
    assert dict(g.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)=={}


def test_law_17_negative_classes_keep_unknown_distinct_from_unauthorized():
    law=json.loads((RET/'runtime_root/law/ADP016.txt').read_text());rows={x['state']:x['behavior'] for x in law['fail_closed_states']}
    assert set(rows)==set(o.ADP016_FAIL_CLOSED_STATES) and len(rows)==17
    # UNKNOWN is observed through the permission boundary; neither is a positive
    # transition/default. Unsupported promotion/confabulation/cue APIs are not
    # present: generic attempted kinds are refused without state mutation.
    reg,e,p,b,ctx=admitted();m=GeneratedMemoryState(**memory(ctx,e,b)['memory']);before=ctx.checkpoint()
    for kind in ('DELETE_MEMORY','PROMOTE_V2_SESSION','CONFABULATE','RESTORE_ANALYST_CONTENT'):
        with pytest.raises(o.OwnerTransitionError):o.adp016_attempt_transition(m,kind,parent_event=e,pre_state_hash=m.current_state_hash,context=ctx)
    assert ctx.checkpoint()==before
    for state in ('RETENTION_UNKNOWN','ACCESS_UNKNOWN'):
        changed=replace(m,**({'retention_state':state} if state=='RETENTION_UNKNOWN' else {'memory_accessibility_state':state}))
        out=o.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESS_UNKNOWN',changed)
        assert out['first_person_permission']=='DEFER_MISSING_AUTHORITY'
        assert getattr(changed,'retention_state' if state=='RETENTION_UNKNOWN' else 'memory_accessibility_state')==state


def test_partial_owner_journal_commit_refusal_rolls_back_all():
    base=pc.ChainEventLedger
    class Failing(base):
        def commit(self,kind,*args):
            if kind=='ADP017_EPISTEMIC_UPDATE':return dict(status='REFUSED',code='INJECTED_DESTINATION_REFUSAL')
            return super().commit(kind,*args)
    with patch.object(pc,'ChainEventLedger',Failing):out=pc.run_positive_chain()
    assert out['terminal']=='FIRST_EVENT_REFUSED' and out['n_ledger_entries']==0
    assert out['state']['memories']==out['state']['stances']=={}


def test_post_commit_wrong_payload_with_valid_chain_hash_is_not_a_legal_history():
    base=pc.ChainEventLedger
    class Forged(base):
        def commit(self,kind,payload,*args):
            if kind=='CAN008_CURRENT_RESPONSE_EFFECT':payload=copy.deepcopy(payload);payload['effect_kind']='AMPLIFY'
            return super().commit(kind,payload,*args)
    with patch.object(pc,'ChainEventLedger',Forged):out=pc.run_positive_chain(_comparison=False)
    assert out['terminal']=='LATER_EVENT_REFUSED' and out['code']=='PRIOR_RECEIPT_BINDING_INVALID'


def test_source_and_memory_records_cannot_silently_mutate_candidate_state():
    reg,e,p,b,ctx=admitted();m=memory(ctx,e,b);ctx.commit_memory(m);before=ctx.state_hash
    ctx.memories[m['memory']['memory_id']]['retention_state']='CONTENT_UNAVAILABLE'
    assert not ctx.verify() and ctx.state_hash==before
    with pytest.raises(o.OwnerTransitionError):memory(ctx,e,b)


def test_withdraw_foreign_record_and_supersede_exact_record():
    ctx,args=epistemic_setup();first=o.adp017_apply_epistemic_effect(**args);eid=first['effect']['effect_id']
    args.update(pre_state_hash=ctx.state_hash,stance_operation='SUPERSEDE_EXACT_RECORD',target_record_ref='FORGED');before=ctx.checkpoint()
    assert o.adp017_apply_epistemic_effect(**args)['decision_state']=='DEFERRED_MISSING_EPISTEMIC_BASIS';assert ctx.checkpoint()==before
    args['target_record_ref']=eid;second=o.adp017_apply_epistemic_effect(**args)
    assert second['decision_state']=='APPLIED_EPISTEMIC_TRANSITION' and eid not in ctx.stances and len(ctx.stances)==1
    assert second['effect']['effect_id']!=eid


def test_first_person_permission_requires_exact_live_state_snapshot():
    assert o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE')['first_person_permission']=='DEFER_MISSING_AUTHORITY'
    ctx,args=epistemic_setup();o.adp017_apply_epistemic_effect(**args);cid=args['claim_ref'];h=ctx.state_sets[cid]['current_state_hash']
    kw=dict(context=ctx,claim_ref=cid,state_hash=h)
    assert o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',**kw)['first_person_permission']=='PERMIT_FIRST_PERSON_BELIEF'
    kw['state_hash']='STALE';assert o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',**kw)['first_person_permission']=='DEFER_MISSING_AUTHORITY'
    assert o.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',context=ctx,claim_ref=cid,state_hash=h)['self_explanation_of_hidden_origin']=='BLOCKED'


def test_owner_fixture_cannot_bypass_absent_registered_rule():
    reg,e,p,b=fixture();reg2=CandidateRegistryFixture();assert reg2.admit_event(e)['status']=='EVENT_IDENTITY_ADMITTED_IN_FIXTURE'
    ctx=o.FixtureOwnerState(reg2)
    with pytest.raises(o.OwnerTransitionError):memory(ctx,e,b)
    c=o.canonical_claim(e.actor_scope,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e.effective_causal_time,e.actor_scope,[e.event_id])
    with pytest.raises(o.OwnerTransitionError):ctx.bind_claim(c,e)


def test_duplicate_valid_event_and_borrowed_prestate_refuse():
    reg,e,p,b=fixture();assert r.coupline_evaluate(e,p,b,reg)['decision_state']=='COUPLING_EVALUATED';before=reg.ledger()
    assert r.coupline_evaluate(e,p,b,reg)['code']=='BLOCK_DUPLICATE_EVENT_IDENTITY' and reg.ledger()==before
    reg,e,p,b=fixture();assert r.coupline_evaluate(e,replace(p,actor_id='OTHER'),b,reg)['code']=='BLOCK_WRONG_ACTOR_SCOPE'


def test_valid_memory_parent_prestate_and_rehydration_firewalls():
    reg,e,p,b,ctx=admitted();m=GeneratedMemoryState(**memory(ctx,e,b)['memory'])
    for args,code in [({'declared_parent_hash':'FORGED','pre_state_hash':m.current_state_hash},'PARENT_EVENT_HASH_MISMATCH'),({'declared_parent_hash':e.event_hash,'pre_state_hash':'FORGED'},'PRE_STATE_HASH_MISMATCH')]:
        with pytest.raises(o.OwnerTransitionError) as err:o.adp016_attempt_transition(m,'DEGRADE',parent_event=e,context=ctx,**args)
        assert err.value.code==code
    with pytest.raises(o.OwnerTransitionError) as err:o.adp016_rehydration_refused(m,'analyst-only invented content')
    assert err.value.code=='UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION'


def test_actual_module_byte_change_invalidates_registered_body():
    import shutil,subprocess
    target=RET/'runtime_root/body_change_probe';target.mkdir(exist_ok=True)
    shutil.copytree(RET/'candidate',target/'candidate',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    script="""
from pathlib import Path
from candidate import can008_candidate_rule as r
from candidate.candidate_registry_fixture import CandidateRegistryFixture
reg=CandidateRegistryFixture();assert r.register_default_rule(reg)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE'
before=r.build_default_binding().rule_content_hash
p=Path(r.__file__).with_name('positive_chain.py');p.write_bytes(p.read_bytes()+b'\\n# actual source-byte mutation\\n')
after=r.build_default_binding().rule_content_hash
assert before!=after
assert reg.lookup(r.RULE_ID,r.RULE_VERSION).rule_content_hash!=after
print('BODY_CHANGE_REFUSED; original and changed digests distinct')
"""
    result=subprocess.run([sys.executable,'-c',script],cwd=target,env={'PATH':__import__('os').environ['PATH'],'PYTHONPATH':str(target.resolve())},text=True,capture_output=True)
    assert result.returncode==0,(result.stdout,result.stderr)
