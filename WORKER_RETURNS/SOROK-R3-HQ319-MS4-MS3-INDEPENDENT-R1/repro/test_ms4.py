"""Fresh MS4 hostile court. Frozen before first collection or execution.
No author-test helpers, no native revisions, no success substitutes.
"""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace, asdict
from unittest.mock import patch
import json, os, sys
import pytest
R=Path(__file__).resolve().parents[1]
RT=R/'staging/ms3/staging/ms2/staging/ms1/runtime'
sys.path.insert(0,str(RT))
import ms1_serial as M
from candidate import owner_transitions as N, can008_candidate_rule as C
from candidate.candidate_registry_fixture import CandidateRegistryFixture, digest, canon, event_digest
OBS=[]
@pytest.fixture(autouse=True)
def observed(request):
    OBS.clear()
    yield
    p=R/'evidence'/os.environ.get('MS4_PHASE','hostile')/'observations'
    p.mkdir(parents=True,exist_ok=True)
    name=request.node.name.replace('/','_')
    (p/(name+'.json')).write_text(json.dumps(dict(case=request.node.nodeid,observations=OBS),indent=2,default=str)+'\n')
def remember(**kw):OBS.append(deepcopy(kw))
def seed(content='AVAILABLE_SOURCE_BOUND',late=False):
    r=CandidateRegistryFixture(); assert C.register_default_rule(r)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE'
    b=C.build_default_binding(); c=N.FixtureOwnerState(r); e=M.fixed_e1(); assert C.occurrence_gate(e,r)['status']=='ADMITTED_OCCURRENCE'
    claim=N.canonical_claim(M.ACTOR,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',M.T_E1,M.ACTOR,[e.event_id])
    q=c.bind_claim(claim,e) if late else None
    p=m=None
    if content is not None:
        p,m=M.form_and_commit_memory(r,c,e,b,content); assert p is not None
    if q is None:q=c.bind_claim(claim,e)
    return dict(r=r,c=c,b=b,e=e,q=q,m=m,p=p)
def snap(a):return dict(owner=a['c'].checkpoint(),registry=a['r'].checkpoint())
def call(a,entry='consume',**kw):
    if entry=='consume':
        args=dict(ctx=a['c'],reg=a['r'],binding=a['b'],e2=M.fixed_e2(),claim_id=a['q']);args.update(kw);return M.consume(**args)
    args=dict(ctx=a['c'],reg=a['r'],binding=a['b'],e1=a['e'],claim_id=a['q'],memory=a['m']);args.update(kw)
    return (M.mediate if entry=='mediate' else M.withdraw_mediator)(**args)
def native(a,access='CLAIM_ACCESSIBLE',op='ADD',target=None):
    return N.adp017_apply_epistemic_effect(actor_id=M.ACTOR,claim_ref=a['q'],stance_kind='BELIEF',stance_operation=op,target_record_ref=target,causal_parent_refs=[a['e'].event_id],actor_facing_basis_refs=[a['e'].event_id+':'+a['e'].event_hash],memory_basis_refs=[a['m']['memory_id']] if a['m'] else [],owning_rule_id=a['b'].rule_id,owning_rule_version=a['b'].rule_version,owning_rule_hash=a['b'].rule_content_hash,effective_causal_time=M.T_E1,claim_accessibility=access,context=a['c'],pre_state_hash=a['c'].state_hash)
def applied(out):assert out['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
def rejected(a,entry='consume',**kw):
    before=snap(a); out=call(a,entry,**kw);after=snap(a); remember(before=before,result=out,after=after)
    assert out['decision_state'] not in ('RESPONSE_EFFECTS_PRODUCED','RESPONSE_INPUTS_VALID_EMPTY','APPLIED_EPISTEMIC_TRANSITION')
    assert after==before
    assert not out.get('committed',False)
    return out
def reseal_memory(a):
    c=a['c'];m=next(iter(c.memories.values()));m['current_state_hash']=N.memory_semantic_hash(m);c._seal();a['m']=deepcopy(m)
def relink_transition(a):
    c=a['c'];m=next(iter(c.memories.values()));old=m['formation_transition_id'];t=c.memory_transitions.pop(old)
    t['memory_transition_id']=digest({k:v for k,v in t.items() if k!='memory_transition_id'})
    c.memory_transitions[t['memory_transition_id']]=t;m['formation_transition_id']=m['last_transition_id']=t['memory_transition_id'];reseal_memory(a)

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('attack',['posthash_relinked','featurehash_relinked','predecessor_cycle','orphan_transition','duplicate_transition','memory_without_formation','content_pair_swap','source_feature_permutation','foreign_actor_coherent','source_ref_swap'])
def test_formation_ancestry(entry,attack):
    a=seed('AVAILABLE_UNCERTAIN'); c=a['c']
    if entry=='consume':applied(call(a,'mediate'))
    m=next(iter(c.memories.values()));t=c.memory_transitions[m['formation_transition_id']]
    if attack=='posthash_relinked':t['post_state_hash']='0'*64;relink_transition(a)
    elif attack=='featurehash_relinked':t['feature_state_after_hash']=digest(['plausible substitute']);relink_transition(a)
    elif attack=='predecessor_cycle':t['pre_state_hash']=c.state_hash;relink_transition(a)
    elif attack=='orphan_transition':c.memory_transitions['orphan']=deepcopy(t)
    elif attack=='duplicate_transition':c.memory_transitions[t['memory_transition_id']+'duplicate']=deepcopy(t)
    elif attack=='memory_without_formation':c.memory_transitions.clear()
    elif attack=='content_pair_swap':
        m['source_feature_bindings']=tuple(canon(dict(json.loads(x),state='AVAILABLE_SOURCE_BOUND')) for x in m['source_feature_bindings']);m['uncertainty_state']='CERTAIN'
    elif attack=='source_feature_permutation':m['source_feature_bindings']=tuple(reversed(m['source_feature_bindings']))
    elif attack=='foreign_actor_coherent':m['actor_id']=t['actor_id']='FOREIGN_ACTOR';relink_transition(a)
    else:
        m['objective_source_event_refs']=('FOREIGN_SOURCE:'+a['e'].event_hash,);t['objective_source_event_refs']=list(m['objective_source_event_refs']);relink_transition(a)
    reseal_memory(a); assert c.verify();rejected(a,entry)

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('operation',['WITHDRAW','SUPERSEDE_EXACT_RECORD'])
@pytest.mark.parametrize('access',['CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'])
def test_terminal_permission_cannot_resurrect_prior_permit(entry,operation,access):
    a=seed();applied(call(a,'mediate'));old=deepcopy(a['c'].permissions[a['q']]);target=next(iter(a['c'].stances))
    applied(native(a,access,operation,target));c=a['c']; c.permissions[a['q']]=old
    c.permissions[a['q']]['epistemic_state_hash']=c.state_sets[a['q']]['current_state_hash'];c._seal()
    rejected(a,entry)

@pytest.mark.parametrize('entry',['mediate','consume','withdraw'])
@pytest.mark.parametrize('selector',['OMITTED',None,'','UNKNOWN','FOREIGN_BOUND'])
def test_claim_selector_does_not_become_genuine_none(entry,selector):
    a=seed();applied(call(a,'mediate'));target=next(iter(a['c'].stances))
    if selector=='FOREIGN_BOUND':
        e=replace(a['e'],event_id='MS4_OTHER_VALID_EVENT',event_hash=''); e=replace(e,event_hash=event_digest(e));assert C.occurrence_gate(e,a['r'])['status']=='ADMITTED_OCCURRENCE'
        q=N.canonical_claim(M.ACTOR,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',M.T_E1,M.ACTOR,[e.event_id]);selector=a['c'].bind_claim(q,e)
    kw=dict(target_effect_id=target) if entry=='withdraw' else {}
    if selector=='OMITTED':
        before=snap(a)
        with pytest.raises(TypeError):
            if entry=='consume':M.consume(a['c'],a['r'],a['b'],M.fixed_e2())
            else:
                f=M.mediate if entry=='mediate' else M.withdraw_mediator
                f(ctx=a['c'],reg=a['r'],binding=a['b'],e1=a['e'],memory=a['m'],**kw)
        remember(missing_selector_typeerror=True,before=before,after=snap(a));assert snap(a)==before
    else:rejected(a,entry,claim_id=selector,**kw)

@pytest.mark.parametrize('field,value',[('actor_scope','OTHER'),('world_ref','OTHER_WORLD'),('world_as_of','1998-10-02T16:00:00Z'),('effective_causal_time',M.T_E1),('effective_causal_time','1998-10-03T15:59:59Z'),('effective_causal_time','NOT_A_TIME'),('public_features',('alien_feature',)),('event_hash','0'*64)])
def test_second_event_actor_world_time_and_source(field,value):
    a=seed();applied(call(a,'mediate'));e=replace(M.fixed_e2(),**{field:value})
    if field!='event_hash':e=replace(e,event_hash=event_digest(e))
    rejected(a,e2=e)

@pytest.mark.parametrize('entry',['mediate','consume'])
@pytest.mark.parametrize('attack',['source_removed','source_rehashed_other_world','claim_polarity','claim_time','emission_event'])
def test_source_registry_and_claim_identity(entry,attack):
    a=seed();
    if entry=='consume':applied(call(a,'mediate'))
    c=a['c'];r=a['r']
    if attack=='source_removed':del r._events[a['e'].event_id];r._seal()
    elif attack=='source_rehashed_other_world':
        e=replace(a['e'],world_ref='COHERENT_FOREIGN_WORLD',event_hash='');e=replace(e,event_hash=event_digest(e));r._events[e.event_id]=asdict(e);r._seal()
    elif attack=='claim_polarity':c.claims[a['q']]['polarity']='NEGATIVE';c.claims[a['q']]['canonical_content_hash']=digest({k:v for k,v in c.claims[a['q']].items() if k in ('subject_ref','predicate_ref','object_or_value','polarity','temporal_scope','subject_scope','referent_refs')})
    elif attack=='claim_time':c.claims[a['q']]['temporal_scope']='1998-10-04T16:00:00Z'
    else:c.emissions[a['q']]['event_id']='FOREIGN_EVENT'
    c._seal();rejected(a,entry)

@pytest.mark.parametrize('content',[None,'AVAILABLE_SOURCE_BOUND','AVAILABLE_UNCERTAIN'])
@pytest.mark.parametrize('late',[False,True])
def test_genuine_bound_none_does_not_infer_nonknowledge(content,late):
    a=seed(content,late);before=snap(a);o=call(a);remember(before=before,result=o,after=snap(a))
    assert o['decision_state']=='RESPONSE_INPUTS_VALID_EMPTY' and not o['committed']
    assert a['q'] not in a['c'].state_sets and not a['c'].stances and snap(a)==before

@pytest.mark.parametrize('content',['AVAILABLE_SOURCE_BOUND','AVAILABLE_UNCERTAIN'])
@pytest.mark.parametrize('access,effect',[('CLAIM_ACCESSIBLE','REROUTE'),('CLAIM_INACCESSIBLE','BLOCK'),('CLAIM_ACCESS_UNKNOWN',None)])
@pytest.mark.parametrize('operation',['WITHDRAW','SUPERSEDE_EXACT_RECORD'])
def test_valid_terminal_sequence_replay(content,access,effect,operation):
    a=seed(content,late=True);first=native(a);applied(first);applied(native(a,access,operation,first['effect']['effect_id']))
    if operation=='WITHDRAW':applied(native(a,access))
    before=snap(a);o=call(a);remember(before=before,result=o,after=snap(a));assert o.get('effect_kind')==effect and not o['committed']
    assert o['decision_state']==('DEFER_MISSING_AUTHORITY' if effect is None else 'RESPONSE_EFFECTS_PRODUCED')
    assert a['c'].checkpoint()==before['owner']
    clone=N.FixtureOwnerState(a['r']);clone.restore(before['owner']);replay=dict(a,c=clone);again=call(replay)
    assert (again['decision_state'],again.get('effect_kind'),again.get('receipt_hash'))==(o['decision_state'],o.get('effect_kind'),o.get('receipt_hash'))
    if effect is None:assert snap(a)==before

@pytest.mark.parametrize('stage',['withdraw_after_real_apply','second_read_after_real_receipt','formation_with_pending','mediate_with_pending'])
def test_transaction_rollback_preserves_real_mutations_and_pending(stage):
    a=seed(None) if stage=='formation_with_pending' else seed()
    if stage!='formation_with_pending':applied(call(a,'mediate'))
    ctx=a['c'];r=a['r'];b=a['b'];e=a['e']
    # Real pending proposal stored by native formation API, not an invented sentinel.
    pending=N.adp016_form_causal_trace(actor_id=M.ACTOR,basis_event=e,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state='AVAILABLE_UNCERTAIN',owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx)
    assert digest(pending) in ctx._pending_memory
    if stage=='withdraw_after_real_apply':
        obj=N;name='adp017_apply_epistemic_effect';fn=getattr(obj,name);invoke=lambda:call(a,'withdraw',target_effect_id=next(iter(ctx.stances)))
    elif stage=='second_read_after_real_receipt':
        first=call(a);assert first['decision_state']=='RESPONSE_EFFECTS_PRODUCED'
        obj=C;name='build_response_receipt';fn=getattr(obj,name);invoke=lambda:call(a)
    elif stage=='formation_with_pending':
        obj=ctx;name='commit_memory';fn=getattr(obj,name);invoke=lambda:M.form_and_commit_memory(r,ctx,e,b,'AVAILABLE_SOURCE_BOUND')
    else:obj=N;name='adp017_apply_epistemic_effect';fn=getattr(obj,name);invoke=lambda:call(a,'mediate')
    before=snap(a);calls=[]
    def after_real(*args,**kwargs):
        result=fn(*args,**kwargs);calls.append(result);raise RuntimeError('MS4_AFTER_REAL_OPERATION')
    with patch.object(obj,name,after_real):out=invoke()
    remember(before=before,real_native_results=calls,result=out,after=snap(a));assert calls and snap(a)==before
    result=out[1] if isinstance(out,tuple) else out
    assert result['decision_state'] not in ('RESPONSE_EFFECTS_PRODUCED','APPLIED_EPISTEMIC_TRANSITION')
    retry=invoke();remember(retry=retry)
    if stage=='withdraw_after_real_apply':applied(retry)
    elif stage=='second_read_after_real_receipt':assert retry['decision_state']=='RESPONSE_EFFECTS_PRODUCED'
    elif stage=='mediate_with_pending':applied(retry)
    else:
        assert retry[0] is not None
        frozen=snap(a);duplicate=M.form_and_commit_memory(r,ctx,e,b,'AVAILABLE_SOURCE_BOUND')
        remember(duplicate=duplicate);assert duplicate[0] is None and snap(a)==frozen

@pytest.mark.parametrize('content,expected',[('AVAILABLE_SOURCE_BOUND','REROUTE'),('AVAILABLE_UNCERTAIN',None)])
def test_hypothetical_content_contrast_and_native_trace_firewall(content,expected):
    a=seed(content);applied(call(a,'mediate'));o=call(a)
    fp=N.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE',a['m']['representation_kind'],a['m']['memory_accessibility_state'],context=a['c'],claim_ref=a['q'],state_hash=a['c'].state_sets[a['q']]['current_state_hash'])
    remember(result=o,trace_permission=fp);assert o.get('effect_kind')==expected
    assert fp['first_person_permission']=='DENY_FIRST_PERSON_CLAIM' and not o['committed']
