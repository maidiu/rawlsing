"""Independent MS2 causal interventions. Freeze before collection/import/execution."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict
import sys,json,inspect,itertools
import pytest
R=Path(__file__).resolve().parents[1];RT=R/'staging/ms1/runtime';sys.path.insert(0,str(RT))
import ms1_serial as M
from candidate import owner_transitions as N,can008_candidate_rule as C,positive_chain as P
from candidate.candidate_registry_fixture import CandidateRegistryFixture,digest,canon
OUT=R/'evidence/new/observations'
CERTAIN='AVAILABLE_SOURCE_BOUND';UNCERTAIN='AVAILABLE_UNCERTAIN'
ACCESS=['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN']
CELLS=[('C1',CERTAIN,'ACTIVE','CONTENT_SENSITIVE',True,None),('C2',UNCERTAIN,'ACTIVE','CONTENT_SENSITIVE',True,None),('C3',CERTAIN,'WITHDRAWN','CONTENT_SENSITIVE',True,None),('C4',UNCERTAIN,'WITHDRAWN','CONTENT_SENSITIVE',True,None),('C4b',UNCERTAIN,'WITHDRAWN','CONTENT_SENSITIVE',True,'CLAIM_ACCESSIBLE'),('C5',CERTAIN,'INHIBITED','CONTENT_SENSITIVE',True,None),('C6',UNCERTAIN,'INHIBITED','CONTENT_SENSITIVE',True,None),('C7',CERTAIN,'ACTIVE','CLAMP',True,None),('C8',UNCERTAIN,'ACTIVE','CLAMP',True,None),('C9',CERTAIN,'ACTIVE','CONTENT_SENSITIVE',False,None),('C10',CERTAIN,'ACTIVE','REFERENCE_ONLY',True,None)]
EXPECTED={'C1':('RESPONSE_EFFECTS_PRODUCED','REROUTE'),'C2':('DEFER_MISSING_AUTHORITY',None),'C3':('RESPONSE_EFFECTS_PRODUCED','BLOCK'),'C4':('DEFER_MISSING_AUTHORITY',None),'C4b':('RESPONSE_EFFECTS_PRODUCED','BLOCK'),'C5':('RESPONSE_INPUTS_VALID_EMPTY',None),'C6':('RESPONSE_INPUTS_VALID_EMPTY',None),'C7':('RESPONSE_EFFECTS_PRODUCED','BLOCK'),'C8':('RESPONSE_EFFECTS_PRODUCED','BLOCK'),'C9':('RESPONSE_EFFECTS_PRODUCED','REROUTE'),'C10':('RESPONSE_EFFECTS_PRODUCED','REROUTE')}
def emit(case,**data):
    OUT.mkdir(parents=True,exist_ok=True);(OUT/(case+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')
def outcome(x):return (x['decision_state'],x.get('effect_kind'))
def armed(content=CERTAIN):
    reg=CandidateRegistryFixture();assert C.register_default_rule(reg)['status']=='CANDIDATE_REGISTERED_IN_FIXTURE'
    b=C.build_default_binding();ctx=N.FixtureOwnerState(reg,M.ACTOR);e1=M.fixed_e1();e2=M.fixed_e2()
    assert C.occurrence_gate(e1,reg)['status']=='ADMITTED_OCCURRENCE'
    initial=ctx.checkpoint()
    proposal=N.adp016_form_causal_trace(actor_id=M.ACTOR,basis_event=e1,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state=content,owning_rule_id=b.rule_id,owning_rule_version=b.rule_version,owning_rule_hash=b.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx)
    commit=ctx.commit_memory(proposal);assert commit['status']=='ADP016_TRACE_COMMITTED_IN_FIXTURE'
    memory=deepcopy(ctx.memories[proposal['memory']['memory_id']]);assert memory==proposal['memory']
    claim=N.canonical_claim(M.ACTOR,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',M.T_E1,M.ACTOR,[e1.event_id]);ref=ctx.bind_claim(claim,e1)
    return dict(reg=reg,ctx=ctx,b=b,e1=e1,e2=e2,memory=memory,claim=ref,formation=proposal,commit=commit,initial=initial)
def med(a,mode='CONTENT_SENSITIVE',**kw):
    return M.mediate(ctx=a['ctx'],reg=a['reg'],binding=a['b'],e1=a['e1'],claim_id=a['claim'],memory=a['memory'],mode=mode,**kw)
def native(a,access,operation='ADD',target=None,**overrides):
    args=dict(actor_id=M.ACTOR,claim_ref=a['claim'],stance_kind='BELIEF',stance_operation=operation,causal_parent_refs=[a['e1'].event_id],actor_facing_basis_refs=[a['e1'].event_id+':'+a['e1'].event_hash],memory_basis_refs=[a['memory']['memory_id']],owning_rule_id=a['b'].rule_id,owning_rule_version=a['b'].rule_version,owning_rule_hash=a['b'].rule_content_hash,effective_causal_time=M.T_E1,claim_accessibility=access,context=a['ctx'],pre_state_hash=a['ctx'].state_hash,target_record_ref=target)
    args.update(overrides);return N.adp017_apply_epistemic_effect(**args)
def consume(a,history=(),**kw):
    args=dict(ctx=a['ctx'],reg=a['reg'],binding=a['b'],e2=a['e2'],claim_id=a['claim'],prior_history=history);args.update(kw)
    return M.consume(**args)
def snapshot(a):
    return dict(owner=a['ctx'].checkpoint(),owner_hash=a['ctx'].state_hash,registry=a['reg'].checkpoint(),formation=a['formation'],memory=a['memory'],claim=a['claim'],events=[asdict(a['e1']),asdict(a['e2'])])
def run_independent(row):
    cid,content,mediator,mode,history,withdraw_access=row;a=armed(content);before=snapshot(a);steps=[]
    if mediator!='INHIBITED':
        m=med(a,mode);assert m['decision_state']=='APPLIED_EPISTEMIC_TRANSITION';steps.append(m)
        if mediator=='WITHDRAWN':
            access=withdraw_access or a['ctx'].state_sets[a['claim']]['current_claim_accessibility']
            w=native(a,access,'WITHDRAW',m['effect']['effect_id']);assert w['decision_state']=='APPLIED_EPISTEMIC_TRANSITION';steps.append(w)
    pre_read=snapshot(a);out=consume(a,('PRIOR',) if history else ());after=snapshot(a)
    assert pre_read['owner']==after['owner']
    return dict(cell=cid,content=content,before=before,steps=steps,pre_read=pre_read,response=out,after=after)

@pytest.mark.parametrize('row',CELLS,ids=[x[0] for x in CELLS])
def test_reconstruct_actual_cells_without_author_run_cell(row):
    rec=run_independent(row);cid=row[0];emit('cell_'+cid,**rec)
    assert outcome(rec['response'])==EXPECTED[cid]
    assert rec['response']['owner_state_hash_read']==rec['pre_read']['owner_hash']
    assert not rec['response']['committed'] and not rec['response']['production_owner_commit']
    state=rec['pre_read']['owner']['state'];assert all(x['stance_kind']=='BELIEF' for x in state['stances'].values())
    if row[2]=='WITHDRAWN':assert rec['steps'][0]['effect']['effect_id'] not in state['stances']

@pytest.mark.parametrize('access',ACCESS)
@pytest.mark.parametrize('withdraw',[False,True])
def test_fixed_epistemic_channel_blocks_memory_content_effect_on_outcome_choice(access,withdraw):
    observations=[]
    for content in [CERTAIN,UNCERTAIN]:
        a=armed(content);x=native(a,access);assert x['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        if withdraw:assert native(a,access,'WITHDRAW',x['effect']['effect_id'])['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        before=snapshot(a);out=consume(a);assert a['ctx'].checkpoint()==before['owner'];observations.append(dict(content=content,before=before,response=out))
    expected=('DEFER_MISSING_AUTHORITY',None) if access=='CLAIM_ACCESS_UNKNOWN' else ('RESPONSE_EFFECTS_PRODUCED','REROUTE' if access=='CLAIM_ACCESSIBLE' and not withdraw else 'BLOCK')
    assert [outcome(o['response']) for o in observations]==[expected,expected]
    # Choice invariance is not equality of complete provenance-bearing responses.
    assert observations[0]['response']['owner_state_hash_read']!=observations[1]['response']['owner_state_hash_read']
    emit('clamp_'+access+'_'+str(withdraw),observations=observations,estimand='decision/effect only; owner hashes differ')

@pytest.mark.parametrize('content',[CERTAIN,UNCERTAIN])
@pytest.mark.parametrize('access',ACCESS)
def test_native_supersession_withdrawal_readdition_at_fixed_memory(content,access):
    a=armed(content);original_memory=deepcopy(a['ctx'].memories);first=med(a);target=first['effect']['effect_id']
    second=native(a,access,'SUPERSEDE_EXACT_RECORD',target);assert second['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    # Fresh E2 admission for each read while preserving the same native owner.
    replies=[];states=[]
    for index,operation in enumerate(['ACTIVE','WITHDRAW','READD']):
        if operation=='WITHDRAW':assert native(a,access,'WITHDRAW',second['effect']['effect_id'])['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        elif operation=='READD':assert native(a,access)['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        d=asdict(a['e2']);d.update(event_id='MS2_SEQUENCE_'+str(index));d.pop('event_hash');event=P.seal_event(**d)
        before=snapshot(a);reply=consume(a,e2=event);assert a['ctx'].checkpoint()==before['owner']
        replies.append(reply);states.append(before)
    expected=[('DEFER_MISSING_AUTHORITY',None)]*3 if access=='CLAIM_ACCESS_UNKNOWN' else [('RESPONSE_EFFECTS_PRODUCED','BLOCK')]*3 if access=='CLAIM_INACCESSIBLE' else [('RESPONSE_EFFECTS_PRODUCED','REROUTE'),('RESPONSE_EFFECTS_PRODUCED','BLOCK'),('RESPONSE_EFFECTS_PRODUCED','REROUTE')]
    assert list(map(outcome,replies))==expected and a['ctx'].memories==original_memory
    emit('sequence_'+content+'_'+access,states=states,responses=replies)

@pytest.mark.parametrize('access',ACCESS)
def test_native_memory_reference_does_not_compute_content_to_accessibility(access):
    results=[]
    for content in [CERTAIN,UNCERTAIN]:
        a=armed(content);before=snapshot(a);result=native(a,access);assert result['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        results.append(dict(before=before,transition=result,permission=a['ctx'].permissions[a['claim']],state=a['ctx'].data()))
    assert results[0]['permission']['permission']==results[1]['permission']['permission']
    assert results[0]['state']['state_sets'][results[0]['before']['claim']]['current_claim_accessibility']==access
    assert results[1]['state']['state_sets'][results[1]['before']['claim']]['current_claim_accessibility']==access
    emit('native_content_placebo_'+access,results=results)

@pytest.mark.parametrize('history',[False,True])
def test_reference_only_pair_loses_the_content_contrast(history):
    values=[]
    for content in [CERTAIN,UNCERTAIN]:
        a=armed(content);assert med(a,'REFERENCE_ONLY')['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
        before=snapshot(a);reply=consume(a,('PRIOR',) if history else ());values.append(dict(before=before,response=reply))
    assert [outcome(x['response']) for x in values]==[('RESPONSE_EFFECTS_PRODUCED','REROUTE')]*2
    emit('reference_pair_'+str(history),values=values)

@pytest.mark.parametrize('field',['uncertainty_state','source_feature_bindings','memory_id','actor_id'])
def test_uncommitted_forged_memory_argument_refuses_without_owner_mutation(field):
    a=armed(UNCERTAIN);before=snapshot(a);memory=deepcopy(a['memory']);memory[field]='MS2_FORGED'
    out=M.mediate(ctx=a['ctx'],reg=a['reg'],binding=a['b'],e1=a['e1'],claim_id=a['claim'],memory=memory)
    emit('raw_forgery_'+field,before=before,forged=memory,response=out,after=snapshot(a))
    assert out['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and a['ctx'].checkpoint()==before['owner']

@pytest.mark.parametrize('mutation',['uncertainty_only','content_and_uncertainty','formation_post_hash','empty_source_refs'])
def test_rehashed_owner_memory_cannot_contradict_original_native_formation(mutation):
    a=armed(UNCERTAIN);ctx=a['ctx'];original=snapshot(a);mid=a['memory']['memory_id'];m=ctx.memories[mid]
    if mutation=='uncertainty_only':m['uncertainty_state']='CERTAIN'
    elif mutation=='content_and_uncertainty':
        m['uncertainty_state']='CERTAIN';m['source_feature_bindings']=tuple(canon(dict(json.loads(x),state=CERTAIN)) for x in m['source_feature_bindings'])
    elif mutation=='formation_post_hash':ctx.memory_transitions[m['formation_transition_id']]['post_state_hash']='MS2_WRONG_FORMATION_POSTSTATE'
    else:m['objective_source_event_refs']=()
    m['current_state_hash']=N.memory_semantic_hash(m);ctx._seal();a['memory']=deepcopy(m);before=snapshot(a)
    result=med(a);after=snapshot(a);reply=consume(a)
    emit('coherent_forgery_'+mutation,original=original,forged_before=before,transition=result,after=after,later_response=reply)
    assert result['decision_state']!='APPLIED_EPISTEMIC_TRANSITION','Contradictory original formation receipt accepted by mediator'
    assert after['owner']==before['owner']

@pytest.mark.parametrize('terminal',['WITHDRAW','INACCESSIBLE','UNKNOWN'])
def test_stale_permission_cannot_override_native_terminal_state(terminal):
    a=armed(CERTAIN);first=med(a);access='CLAIM_ACCESSIBLE' if terminal=='WITHDRAW' else 'CLAIM_INACCESSIBLE' if terminal=='INACCESSIBLE' else 'CLAIM_ACCESS_UNKNOWN'
    last=native(a,access,'WITHDRAW' if terminal=='WITHDRAW' else 'SUPERSEDE_EXACT_RECORD',first['effect']['effect_id']);assert last['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    valid=snapshot(a);p=a['ctx'].permissions[a['claim']];p['permission']='PERMIT_FIRST_PERSON_BELIEF';a['ctx']._seal();before=snapshot(a);out=consume(a)
    emit('stale_permission_'+terminal,valid_terminal=valid,forged_before=before,response=out,after=snapshot(a))
    assert out['decision_state']!='RESPONSE_EFFECTS_PRODUCED','Retained native terminal state was overridden by a forged stale permit'
    assert a['ctx'].checkpoint()==before['owner']

@pytest.mark.parametrize('field',['actor','time','claim','memory','rule_hash','basis'])
def test_native_wrong_actor_time_claim_or_basis_refuses_atomically(field):
    a=armed();before=snapshot(a);changes={'actor':dict(actor_id='MS2_OTHER'),'time':dict(effective_causal_time='1999-01-01T00:00:00Z'),'claim':dict(claim_ref='MS2_UNKNOWN_CLAIM'),'memory':dict(memory_basis_refs=['MS2_UNKNOWN_MEMORY']),'rule_hash':dict(owning_rule_hash='MS2_FALSE_HASH'),'basis':dict(actor_facing_basis_refs=['MS2_FALSE_BASIS'])}[field]
    out=native(a,'CLAIM_ACCESSIBLE',**changes);emit('native_wrong_'+field,before=before,response=out,after=snapshot(a))
    assert out['decision_state']!='APPLIED_EPISTEMIC_TRANSITION' and a['ctx'].checkpoint()==before['owner']

@pytest.mark.parametrize('field',['actor','world','time'])
def test_consumer_wrong_event_scope_refuses_atomically(field):
    a=armed();med(a);before=snapshot(a);d=asdict(a['e2']);d.pop('event_hash')
    d.update({'actor':dict(actor_scope='MS2_OTHER'),'world':dict(world_ref='MS2_OTHER_WORLD'),'time':dict(effective_causal_time=M.T_E1)}[field]);out=consume(a,e2=P.seal_event(**d))
    emit('consumer_wrong_'+field,before=before,response=out,after=snapshot(a));assert out['decision_state']!='RESPONSE_EFFECTS_PRODUCED' and a['ctx'].checkpoint()==before['owner']

def test_unknown_consumer_claim_cannot_be_misreported_as_bound_absence():
    a=armed();med(a);before=snapshot(a);out=consume(a,claim_id='MS2_UNKNOWN_SELECTED_CLAIM')
    emit('unknown_selected_claim',before=before,response=out,after=snapshot(a))
    assert out['decision_state'] not in ('RESPONSE_INPUTS_VALID_EMPTY','RESPONSE_EFFECTS_PRODUCED'),'Unknown selector erased a real applied BELIEF into apparently valid emptiness'
    assert a['ctx'].checkpoint()==before['owner']

def test_history_input_changes_provenance_but_not_choice_and_can3_comparator_stays_distinct():
    observed=[]
    for history in [(),('PRIOR',),('DIFFERENT','HISTORY','CONTENTS')]:
        a=armed();med(a);out=consume(a,history);observed.append(dict(history=history,state=snapshot(a),response=out))
    assert [outcome(x['response']) for x in observed]==[('RESPONSE_EFFECTS_PRODUCED','REROUTE')]*3
    assert len({x['response']['coupling']['prestate_hash'] for x in observed})==3
    left=P.run_positive_chain(_comparison=False);right=P.run_positive_chain(_comparison=False,omit_first_effect=True,later_event_requires_prior_effect=False)
    assert left['state']==right['state'] and left['later_event_response']['effect_kind']=='DEFLECT' and right['later_event_response']['effect_kind']=='AMPLIFY'
    emit('history_and_CAN3',observed=observed,comparator=dict(stored=left,omitted=right))

def test_causal_counterfactuals_preserve_original_falsification_and_authored_exclusion():
    cells={row[0]:run_independent(row) for row in CELLS};values={k:outcome(v['response']) for k,v in cells.items()}
    assert values['C1']!=values['C2'] and values['C1']!=values['C3'] and values['C1']!=values['C5']
    assert values['C2']==values['C4']==('DEFER_MISSING_AUTHORITY',None)
    assert values['C2']!=values['C6'] # typed refusal contrast; neither is productive
    assert values['C4b']!=values['C4'] and values['C7']==values['C8']
    assert values['C1']==values['C9']==values['C10']
    assert len({x['before']['memory']['memory_id'] for x in cells.values()})==1
    assert len({digest(x['before']['events']) for x in cells.values()})==1
    sig=inspect.signature(M.consume);assert 'memory' not in sig.parameters and 'ctx' in sig.parameters
    # Full ctx exposes memory and is hashed; no typed encapsulation prevents reading it.
    assert 'tuple(sorted(ctx.memories))' in inspect.getsource(M.consume)
    emit('causal_adjudication',outcomes=values,original_P3b='FALSIFIED',original_F_B='FIRED',original_top_gate_satisfied=False,unknown_identifying_contrast='No productive active/withdrawal contrast at fixed UNKNOWN; absence changes typed refusal only; C4b jointly changes access',direct_path='Choice map intentionally reads permission; full context and provenance hashes still depend on memory; exclusion limited to this source and choice estimand',rules='UNISSUED')
