"""MS3 prospective author controls. Commit before candidate implementation/execution."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict,replace
from unittest.mock import patch
import sys,json
import pytest
R=Path(__file__).resolve().parents[1];RT=R/'staging/ms2/staging/ms1/runtime';sys.path.insert(0,str(RT))
import ms1_serial as M
from candidate import owner_transitions as N,can008_candidate_rule as C,positive_chain as P
from candidate.candidate_registry_fixture import CandidateRegistryFixture,digest,canon
O=R/'evidence/author/observations'
def save(name,**d):
    O.mkdir(parents=True,exist_ok=True);(O/(name+'.json')).write_text(json.dumps(d,indent=2,default=str)+'\n')
def seed(content='AVAILABLE_SOURCE_BOUND',late=False):
    reg=CandidateRegistryFixture();C.register_default_rule(reg);b=C.build_default_binding();ctx=N.FixtureOwnerState(reg);e1=M.fixed_e1();C.occurrence_gate(e1,reg)
    claim=N.canonical_claim(M.ACTOR,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',M.T_E1,M.ACTOR,[e1.event_id])
    ref=ctx.bind_claim(claim,e1) if late else None
    proposal=memory=None
    if content is not None:
        proposal,memory=M.form_and_commit_memory(reg,ctx,e1,b,content);assert proposal is not None
    if ref is None:ref=ctx.bind_claim(claim,e1)
    return dict(reg=reg,ctx=ctx,b=b,e1=e1,e2=M.fixed_e2(),claim=ref,memory=memory,proposal=proposal)
def state(a):return dict(owner=a['ctx'].checkpoint(),registry=a['reg'].checkpoint())
def med(a,**kw):
    args=dict(ctx=a['ctx'],reg=a['reg'],binding=a['b'],e1=a['e1'],claim_id=a['claim'],memory=a['memory']);args.update(kw);return M.mediate(**args)
def consume(a,**kw):
    args=dict(ctx=a['ctx'],reg=a['reg'],binding=a['b'],e2=a['e2'],claim_id=a['claim']);args.update(kw);return M.consume(**args)
def native(a,access,op='ADD',target=None):
    return N.adp017_apply_epistemic_effect(actor_id=M.ACTOR,claim_ref=a['claim'],stance_kind='BELIEF',stance_operation=op,target_record_ref=target,causal_parent_refs=[a['e1'].event_id],actor_facing_basis_refs=[a['e1'].event_id+':'+a['e1'].event_hash],memory_basis_refs=[a['memory']['memory_id']] if a['memory'] else [],owning_rule_id=a['b'].rule_id,owning_rule_version=a['b'].rule_version,owning_rule_hash=a['b'].rule_content_hash,effective_causal_time=M.T_E1,claim_accessibility=access,context=a['ctx'],pre_state_hash=a['ctx'].state_hash)
def deny(a,entry,name,**kw):
    before=state(a);out=med(a,**kw) if entry=='mediate' else consume(a,**kw);after=state(a)
    save(name,before=before,response=out,after=after)
    assert out['decision_state'] not in ['APPLIED_EPISTEMIC_TRANSITION','RESPONSE_EFFECTS_PRODUCED','RESPONSE_INPUTS_VALID_EMPTY']
    assert after==before

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('mode',['false_prestate','feature_source','uncertainty_mismatch','missing_transition','authority_hash','wrong_source_time'])
def test_native_formation_receipt_cannot_be_replaced_by_rehashed_memory(mode,entry):
    a=seed('AVAILABLE_UNCERTAIN')
    if entry=='consume':assert med(a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    ctx=a['ctx'];m=next(iter(ctx.memories.values()));t=ctx.memory_transitions[m['formation_transition_id']]
    if mode=='false_prestate':t['pre_state_hash']=seed(None)['ctx'].state_hash
    elif mode=='feature_source':m['source_feature_bindings']=tuple(canon(dict(json.loads(x),source_event='MS3_FOREIGN_EVENT:hash')) for x in m['source_feature_bindings'])
    elif mode=='uncertainty_mismatch':m['uncertainty_state']='CERTAIN'
    elif mode=='missing_transition':ctx.memory_transitions.clear()
    elif mode=='authority_hash':t['authority_or_rule_hash']='MS3_FORGED_AUTHORITY'
    else:t['effective_causal_time']='1999-01-01T00:00:00Z'
    m['current_state_hash']=N.memory_semantic_hash(m);ctx._seal();a['memory']=deepcopy(m)
    deny(a,entry,'formation_'+mode+'_'+entry)

def rehash_last(ctx,field):
    t=ctx.epistemic_transitions[-1];e=t['effect'];old=e['effect_id']
    if field=='pre_state_hash':t[field]=N.FixtureOwnerState(ctx.registry).state_hash
    elif field=='authority_hash':t[field]='MS3_FALSE_AUTHORITY'
    elif field=='target_record_ref':t[field]='MS3_FALSE_TARGET'
    elif field=='owning_rule_hash':e[field]='MS3_FALSE_RULE'
    elif field=='effective_causal_time':e[field]='1999-01-01T00:00:00Z'
    else:e[field]=('MS3_WRONG_SOURCE:hash',)
    e['effect_id']=digest(['EPISTEMIC_EFFECT',{k:v for k,v in e.items() if k!='effect_id'},t['pre_state_hash'],t['target_record_ref']])
    if old in ctx.stances:del ctx.stances[old]
    ctx.stances[e['effect_id']]=deepcopy(e);t['post_stance_set_hash']=digest(ctx.stances)
    t['transition_id']=digest({k:v for k,v in t.items() if k not in ['transition_id','post_state_set_hash']})
    s=ctx.state_sets[e['claim_ref']];s['active_stance_records']=[deepcopy(v) for k,v in sorted(ctx.stances.items()) if v['claim_ref']==e['claim_ref']];s['last_transition_ref']=t['transition_id'];s['current_state_hash']=digest({k:v for k,v in s.items() if k!='current_state_hash'})
    t['post_state_set_hash']=s['current_state_hash'];ctx.permissions[e['claim_ref']]['epistemic_state_hash']=s['current_state_hash'];ctx._seal()

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('field',['pre_state_hash','authority_hash','target_record_ref','owning_rule_hash','effective_causal_time','actor_facing_basis_refs'])
def test_coherent_epistemic_hashes_do_not_create_native_predecessor_or_authority(field,entry):
    a=seed();first=med(a);assert first['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    assert native(a,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',first['effect']['effect_id'])['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    rehash_last(a['ctx'],field);deny(a,entry,'epistemic_'+field+'_'+entry)

@pytest.mark.parametrize('content',[None,'AVAILABLE_SOURCE_BOUND'])
@pytest.mark.parametrize('history',[False,True])
def test_genuine_bound_none_remains_valid_empty_and_atomic(content,history):
    a=seed(content);before=state(a);out=consume(a,prior_history=('PRIOR',) if history else ())
    assert out['decision_state']=='RESPONSE_INPUTS_VALID_EMPTY' and not out['committed']
    assert state(a)==before # nonproductive E2 admission/evaluation rolls back too
    save('none_'+str(content)+'_'+str(history),before=before,response=out,after=state(a))

@pytest.mark.parametrize('content',['AVAILABLE_SOURCE_BOUND','AVAILABLE_UNCERTAIN'])
@pytest.mark.parametrize('access',['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'])
def test_real_memory_formation_after_claim_and_native_terminal_sequences_remain_lawful(content,access):
    a=seed(content,late=True);before=deepcopy(a['ctx'].memories);first=native(a,access);assert first['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    assert native(a,access,'WITHDRAW',first['effect']['effect_id'])['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    assert native(a,access)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    pre=state(a);out=consume(a)
    assert (out['decision_state'],out.get('effect_kind'))==({'CLAIM_ACCESSIBLE':('RESPONSE_EFFECTS_PRODUCED','REROUTE'),'CLAIM_INACCESSIBLE':('RESPONSE_EFFECTS_PRODUCED','BLOCK'),'CLAIM_ACCESS_UNKNOWN':('DEFER_MISSING_AUTHORITY',None)}[access])
    assert a['ctx'].memories==before and a['ctx'].checkpoint()==pre['owner']
    if access=='CLAIM_ACCESS_UNKNOWN':assert state(a)==pre
    save('late_formation_'+content+'_'+access,before=pre,response=out,after=state(a))

@pytest.mark.parametrize('stage',['formation_commit','mediate_native','consumer_admission','consumer_effect','consumer_receipt'])
def test_real_operation_then_injected_exception_restores_all_live_state(stage):
    a=seed(None) if stage=='formation_commit' else seed();called=[]
    if stage=='formation_commit':target=a['ctx'];name='commit_memory';original=target.commit_memory;call=lambda:M.form_and_commit_memory(a['reg'],a['ctx'],a['e1'],a['b'],'AVAILABLE_SOURCE_BOUND')
    elif stage=='mediate_native':target=N;name='adp017_apply_epistemic_effect';original=getattr(target,name);call=lambda:med(a)
    else:
        assert med(a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        target=C;name={'consumer_admission':'coupline_evaluate','consumer_effect':'response_rule_apply','consumer_receipt':'build_response_receipt'}[stage];original=getattr(target,name);call=lambda:consume(a)
    before=state(a)
    def failing(*args,**kw):
        result=original(*args,**kw)
        if stage=='mediate_native' and kw.get('context') is not a['ctx']:return result
        called.append(result);raise RuntimeError('MS3_AFTER_REAL_NATIVE_OPERATION')
    with patch.object(target,name,failing):out=call()
    assert called and state(a)==before
    result=out[1] if stage=='formation_commit' else out
    assert result['decision_state'] not in ['APPLIED_EPISTEMIC_TRANSITION','RESPONSE_EFFECTS_PRODUCED']
    if stage=='formation_commit':assert call()[0] is not None
    elif stage=='mediate_native':assert med(a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    else:assert consume(a)['decision_state']=='RESPONSE_EFFECTS_PRODUCED'
    save('exception_'+stage,before=before,refusal=result,real_operation_receipts=called)

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('field',['binding','source_event','selected_claim'])
def test_entrypoint_rejects_wrong_rule_source_event_or_selector_without_admission(field,entry):
    a=seed();assert med(a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION';kw={}
    if field=='binding':kw['binding']=replace(a['b'],rule_content_hash='MS3_FORGED_HASH')
    elif field=='selected_claim':kw['claim_id']='MS3_UNKNOWN_CLAIM'
    else:a['reg']._events[a['e1'].event_id]['world_ref']='MS3_FOREIGN_WORLD';a['reg']._seal()
    deny(a,entry,'entry_'+field+'_'+entry,**kw)

def test_complete_native_checkpoint_clone_and_duplicate_e2_behavior():
    a=seed();assert med(a)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    reg=CandidateRegistryFixture();reg.restore(a['reg'].checkpoint());ctx=N.FixtureOwnerState(reg);ctx.restore(a['ctx'].checkpoint());b=dict(a,reg=reg,ctx=ctx)
    x=consume(a);y=consume(b);assert x==y and a['ctx'].data()==b['ctx'].data()
    before=state(b);again=consume(b);assert again['decision_state']=='BLOCK_DUPLICATE_EVENT_IDENTITY' and state(b)==before
    save('clone_and_duplicate',left=x,right=y,duplicate=again)

def test_original_p3b_gate_and_uncommitted_response_ceiling_are_preserved():
    certain=M.run_cell('MS3_CERTAIN',M.MEMORY_CONTENT_CERTAIN);active=M.run_cell('C2',M.MEMORY_CONTENT_UNCERTAIN);withdrawn=M.run_cell('C4',M.MEMORY_CONTENT_UNCERTAIN,mediator='WITHDRAWN')
    assert certain['response_effect_kind']=='REROUTE'
    assert (active['response_decision_state'],active['response_effect_kind'])==(withdrawn['response_decision_state'],withdrawn['response_effect_kind'])==('DEFER_MISSING_AUTHORITY',None)
    assert all(not r['response']['committed'] and not r['response']['production_owner_commit'] and 'UNISSUED' in r['rule_grain'] for r in [certain,active,withdrawn])
    save('original_falsification',certain=certain,C2=active,C4=withdrawn,P3b='FALSIFIED',F_B='FIRED',serial_identification='HOLD',independent_MS4='REQUIRED')
