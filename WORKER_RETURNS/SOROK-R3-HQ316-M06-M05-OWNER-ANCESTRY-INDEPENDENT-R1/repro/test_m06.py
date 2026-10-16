"""M06 independent expectations: freeze this file before executing or collecting it."""
from pathlib import Path
from copy import deepcopy
from dataclasses import asdict, replace
import sys, json, hashlib, itertools
import pytest
R=Path(__file__).resolve().parents[1]
M1=R/'runtime/m05/runtime/m02/runtime/m01'
sys.path.insert(0,str(M1/'repro'))
import bootstrap, cell, claim_provenance
from cell import Cell, Refusal, owner, digest
from candidate.candidate_registry_fixture import canon
from candidate.positive_chain import seal_event, run_positive_chain
O=R/'evidence/new/observations'

def write(case, **data):
    O.mkdir(parents=True,exist_ok=True)
    (O/(case+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')

def fresh(memory='UNCERTAIN',epistemic='BELIEF',history='STORED'):
    c=Cell();c.prepare(memory,epistemic,history);return c

def revise(c, access='CLAIM_ACCESSIBLE', operation='ADD', target=None, claim=None, event=None):
    e=event or c.e1
    args=c.epi_args(access)
    args.update(claim_ref=claim or c.claim_id,stance_operation=operation,target_record_ref=target,
                causal_parent_refs=[e.event_id],actor_facing_basis_refs=[e.event_id+':'+e.event_hash],effective_causal_time=e.effective_causal_time)
    result=owner.adp017_apply_epistemic_effect(**args)
    assert result['decision_state']=='APPLIED_EPISTEMIC_TRANSITION'
    return result

def extra_claim(c, suffix, at='1998-10-15T12:00:00Z'):
    d=asdict(c.e1);d.update(event_id='M06_EXTRA_'+suffix,effective_causal_time=at,causal_parent_event_ids=(c.e1.event_id,) if at>c.e1.effective_causal_time else ());d.pop('event_hash')
    e=seal_event(**d);assert c.reg.admit_event(e)['status']=='EVENT_IDENTITY_ADMITTED_IN_FIXTURE'
    claim=owner.canonical_claim(c.ctx.actor_id,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',at,c.ctx.actor_id,[e.event_id])
    ref=c.ctx.bind_claim(claim,e);revise(c,claim=ref,event=e)
    return e,ref

def exact_target(c,ref=None):
    return next(k for k,v in c.ctx.stances.items() if v['claim_ref']==(ref or c.claim_id))

def rejected(c, packet, case, route):
    initial=c.checkpoint();out=None;reason=None;phase='restore'
    if route=='restore':
        try:c.restore(packet)
        except Refusal as exc:
            reason=str(exc)
            write(case,route=route,phase=phase,refusal=reason,before=initial,packet=packet,after=c.checkpoint())
            assert c.checkpoint()==initial
            return
    else:
        c._restore_parts(packet)
    before=c.checkpoint();phase='direct_read' if route=='direct' else 'later'
    try:
        out=c.read_owner(c.ctx.state_hash,c.e2.effective_causal_time) if route=='direct' else c.later(c.ctx.state_hash)
    except Refusal as exc:reason=str(exc)
    after=c.checkpoint()
    write(case,route=route,phase=phase,refusal=reason,before=before,packet=packet,observed=out,after=after)
    assert reason is not None, 'Invalid provenance produced response: '+str(out and out['streams'])
    assert after==before, 'Refusal changed owner, registry, reads, witnesses or journals'

def rehash_journal(packet):
    rows=packet['journal'][0];previous=None
    for row in rows:
        row['prev_entry_hash']=previous;row['entry_hash']=digest({k:v for k,v in row.items() if k!='entry_hash'});previous=row['entry_hash']
    packet['journal']=(rows,digest(rows))
    b=json.loads(packet['claim_selection_binding']);first=next(x for x in rows if x['kind']=='FIRST_EVENT_COMPLETE')
    b['first_event_entry_hash']=first['entry_hash'];packet['claim_selection_binding']=canon(b)

def rehash_terminal(s,t):
    effect=t['effect'];old=effect['effect_id']
    effect['effect_id']=digest(['EPISTEMIC_EFFECT',{k:v for k,v in effect.items() if k!='effect_id'},t['pre_state_hash'],t['target_record_ref']])
    if old in s['stances']:
        del s['stances'][old];s['stances'][effect['effect_id']]=deepcopy(effect)
    t['post_stance_set_hash']=digest(s['stances'])
    t['transition_id']=digest({k:v for k,v in t.items() if k not in ('transition_id','post_state_set_hash')})
    ref=effect['claim_ref'];snap=s['state_sets'][ref]
    snap['active_stance_records']=[deepcopy(v) for k,v in sorted(s['stances'].items()) if v['claim_ref']==ref]
    snap['last_transition_ref']=t['transition_id'];snap['current_state_hash']=digest({k:v for k,v in snap.items() if k!='current_state_hash'})
    t['post_state_set_hash']=snap['current_state_hash'];s['permissions'][ref]['epistemic_state_hash']=snap['current_state_hash']

@pytest.mark.parametrize('memory,epistemic',list(itertools.product(['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'],['NONE','BELIEF','INACCESSIBLE'])))
@pytest.mark.parametrize('route',['restore','direct','later'])
def test_wrong_cell_full_owner_plus_witness_splice(memory,epistemic,route):
    c=fresh('CERTAIN','BELIEF');donor=fresh(memory,epistemic)
    # An exactly equal same-contract owner is lawful replay, tested separately.
    if memory=='CERTAIN' and epistemic=='BELIEF':
        p=donor.checkpoint();c.restore(p);assert c.later(c.ctx.state_hash)['streams']=={'memory':'BUFFER','epistemic':'REROUTE'};return
    p=c.checkpoint();p['ctx']=donor.checkpoint()['ctx'];p['native_formation_inputs']=donor.checkpoint()['native_formation_inputs']
    rejected(c,p,'splice_'+memory+'_'+epistemic+'_'+route,route)

@pytest.mark.parametrize('mode',['borrowed_prestate','native_empty_root','different_claim_prestate'])
@pytest.mark.parametrize('route',['restore','direct','later'])
def test_coherently_rehashed_suffix_cannot_invent_native_predecessor(mode,route):
    c=fresh();revise(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',exact_target(c));revise(c,'CLAIM_ACCESSIBLE','SUPERSEDE_EXACT_RECORD',exact_target(c))
    p=c.checkpoint();s=p['ctx']['state'];t=s['epistemic_transitions'][-1]
    if mode=='borrowed_prestate':value=fresh('NONE','BELIEF').ctx.state_hash
    elif mode=='native_empty_root':value=c.initial
    else:
        donor=fresh();extra_claim(donor,'FALSE_PREDECESSOR');value=donor.ctx.state_hash
    assert value!=t['pre_state_hash'];t['pre_state_hash']=value;rehash_terminal(s,t)
    rejected(c,p,'false_predecessor_'+mode+'_'+route,route)

@pytest.mark.parametrize('mode',['prefix_permission','cross_claim_terminal','reverse_interleaved','drop_middle','duplicate_suffix','foreign_target'])
@pytest.mark.parametrize('route',['restore','direct','later'])
def test_interleaved_claim_terminal_authority_and_retained_history(mode,route):
    c=fresh();old=c.ctx.data();e,ref=extra_claim(c,'INTERLEAVED')
    revise(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',exact_target(c))
    revise(c,operation='WITHDRAW',target=exact_target(c,ref),claim=ref,event=e)
    p=c.checkpoint();s=p['ctx']['state']
    if mode=='prefix_permission':
        for family in ['stances','state_sets','permissions']:
            if family=='stances':
                s[family]={k:v for k,v in s[family].items() if v['claim_ref']!=c.claim_id};s[family].update(old[family])
            else:s[family][c.claim_id]=deepcopy(old[family][c.claim_id])
    elif mode=='cross_claim_terminal':s['state_sets'][c.claim_id]['last_transition_ref']=s['epistemic_transitions'][-1]['transition_id']
    elif mode=='reverse_interleaved':s['epistemic_transitions'][1:]=reversed(s['epistemic_transitions'][1:])
    elif mode=='drop_middle':del s['epistemic_transitions'][1]
    elif mode=='duplicate_suffix':s['epistemic_transitions'].append(deepcopy(s['epistemic_transitions'][-1]))
    else:
        t=s['epistemic_transitions'][-1];t['target_record_ref']=next(iter(old['stances']));rehash_terminal(s,t)
    rejected(c,p,'interleaved_'+mode+'_'+route,route)

@pytest.mark.parametrize('field',['parent_state_hash','memory_id_override','owning_rule_version','owning_rule_hash','authority_version','actor_id','basis_event'])
@pytest.mark.parametrize('route',['restore','direct'])
def test_noninvertible_formation_witness_cannot_authorize_different_actual_input(field,route):
    c=fresh();p=c.checkpoint();w=next(iter(p['native_formation_inputs'].values()))
    if field=='basis_event':w[field]['event_hash']='M06_REHASHED_FOREIGN_EVENT'
    elif field=='parent_state_hash':w[field]=fresh('NONE','NONE').ctx.state_hash
    else:w[field]='M06_FALSE_INPUT'
    rejected(c,p,'witness_'+field+'_'+route,route)

@pytest.mark.parametrize('mutation',['delete_memory_row','delete_epistemic_row','wrong_memory_before','wrong_memory_after','wrong_epistemic_result','duplicate_native_row'])
def test_fully_rehashed_e1_journal_cannot_replace_native_formation_receipts(mutation):
    c=fresh();p=c.checkpoint();rows=p['journal'][0];m=next(x for x in rows if x['kind']=='ADP016_COMMIT');e=next(x for x in rows if x['kind']=='ADP017_COMMIT')
    if mutation=='delete_memory_row':rows.remove(m)
    elif mutation=='delete_epistemic_row':rows.remove(e)
    elif mutation=='wrong_memory_before':m['payload']['before']=c.initial+'0'
    elif mutation=='wrong_memory_after':m['payload']['after']=c.ctx.state_hash
    elif mutation=='wrong_epistemic_result':e['payload']['result']['production_owner_commit']=True
    else:rows.insert(0,deepcopy(m))
    for i,row in enumerate(rows):row['seq']=i+1
    rehash_journal(p);rejected(c,p,'journal_'+mutation,'restore')

@pytest.mark.parametrize('access',['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'])
@pytest.mark.parametrize('history',['STORED','OMITTED','WITHHELD'])
def test_native_interleaving_no_change_withdraw_readd_and_full_replay(access,history):
    c=fresh('UNCERTAIN','NONE',history);e,ref=extra_claim(c,'VALID_INTERLEAVE')
    for unused in range(2):
        revise(c);revise(c,'CLAIM_INACCESSIBLE','SUPERSEDE_EXACT_RECORD',exact_target(c));revise(c,operation='WITHDRAW',target=exact_target(c))
    revise(c,access)
    before=c.checkpoint();a=c.epi_args(access);a['stance_operation']='NO_CHANGE'
    assert owner.adp017_apply_epistemic_effect(**a)['decision_state']=='NO_EPISTEMIC_TRANSITION';assert c.checkpoint()==before
    clone=Cell();clone.restore(before);assert clone.checkpoint()==before
    if access=='CLAIM_ACCESS_UNKNOWN':
        with pytest.raises(Refusal):clone.later(clone.ctx.state_hash)
        assert clone.checkpoint()==before
    else:
        result=clone.later(clone.ctx.state_hash,history_access=history!='WITHHELD')
        assert result['streams']=={'memory':'DEFLECT','epistemic':'REROUTE' if access=='CLAIM_ACCESSIBLE' else 'BLOCK'}
        proof=result['read']['claim_selection_provenance']['native_owner_ancestry']
        assert proof['terminal_transition_refs'][ref]!=proof['terminal_transition_refs'][c.claim_id]
        assert clone.ctx.data()==before['ctx']['state'];write('lawful_'+access+'_'+history,checkpoint=before,result=result)

@pytest.mark.parametrize('tag',['M06_ALPHA',{'stable':'M06_STRUCTURED'},['M06','COMPOSITE']])
@pytest.mark.parametrize('access',['NONE','BELIEF','INACCESSIBLE'])
def test_valid_alternate_memory_identity_preserves_native_content_and_permissions(tag,access):
    c=fresh('NONE',access);proposal=c.form('AVAILABLE_UNCERTAIN',memory_id_override=tag)
    assert c.ctx.commit_memory(proposal)['status']=='ADP016_TRACE_COMMITTED_IN_FIXTURE'
    clone=Cell();clone.restore(c.checkpoint());result=clone.later(clone.ctx.state_hash)
    assert result['streams']=={'memory':'DEFLECT','epistemic':{'NONE':'AMPLIFY','BELIEF':'REROUTE','INACCESSIBLE':'BLOCK'}[access]}
    write('identity_'+digest(tag)[:8]+'_'+access,formation=proposal,result=result)

@pytest.mark.parametrize('at',['1998-10-03T16:00:00.000001Z','1999-03-01T10:00:00Z','2000-12-31T23:59:59.999999Z'])
def test_earlier_and_future_unselected_claims_do_not_select_the_wrong_terminal(at):
    c=fresh('NONE','NONE');extra_claim(c,'PAST','1998-09-01T00:00:00Z');extra_claim(c,'FUTURE','2000-01-01T00:00:00Z')
    d=asdict(c.e2);d.update(event_id='M06_CUT_'+at,effective_causal_time=at);d.pop('event_hash');e=seal_event(**d)
    result=c.later(c.ctx.state_hash,event=e)
    assert result['streams']=={'memory':'AMPLIFY','epistemic':'AMPLIFY'}
    assert result['read']['claim_selection_provenance']['selected_claim_ref']==c.claim_id
    write('cut_'+digest(at)[:8],result=result)

@pytest.mark.parametrize('stage',['later_admission','later_read','later_emission'])
def test_revised_multiclaim_state_exception_and_retry_are_transactional(stage):
    c=fresh();extra_claim(c,'FAULT');revise(c,operation='WITHDRAW',target=exact_target(c));revise(c)
    before=c.checkpoint()
    with pytest.raises(Refusal,match='TEST_FAULT'):c.later(c.ctx.state_hash,failure=stage)
    assert c.checkpoint()==before and c.reg.event(c.e2.event_id) is None
    out=c.later(c.ctx.state_hash);assert len(c.reads)==1
    assert len(c.journal.read_effects('M01_CAN008_CURRENT_RESPONSE_GRAPH'))==1
    saved=c.checkpoint()
    with pytest.raises(Refusal):c.later(c.ctx.state_hash)
    assert c.checkpoint()==saved;write('atomic_'+stage,before=before,result=out,after=saved)

@pytest.mark.parametrize('module',['claim_provenance','cell'])
def test_changed_actual_source_body_invalidates_stale_grant_atomically(module):
    c=fresh();before=c.checkpoint();p=Path(sys.modules[module].__file__);original=p.read_bytes()
    try:
        p.write_bytes(original+b'\n# M06 independently frozen actual-body mutation\n')
        with pytest.raises(Refusal,match='UNAUTHORIZED_RULE_OR_SOURCE'):c.later(c.ctx.state_hash)
        assert c.checkpoint()==before
    finally:p.write_bytes(original)
    assert c.later(c.ctx.state_hash)['status']=='COMMITTED_TEST_ONLY'

@pytest.mark.parametrize('family',['formation','epistemic','first_receipt'])
def test_detached_outer_diagnostics_cannot_override_actual_owner_read(family):
    c=fresh();p=c.checkpoint()
    if family=='first_receipt':
        p[family]['rule_version']='M06_STALE_RULE';p[family]['receipt_hash']=cell.old._sha(cell.old._canon({k:v for k,v in p[family].items() if k!='receipt_hash'}))
        rejected(c,p,'diagnostic_'+family,'restore')
    else:
        # These diagnostic copies are not authority. Changing them must not select effects.
        p[family]={'M06_UNTRUSTED_DIAGNOSTIC':True};c.restore(p)
        out=c.later(c.ctx.state_hash);assert out['streams']=={'memory':'DEFLECT','epistemic':'REROUTE'}
        write('diagnostic_'+family,result=out)

def test_consumed_checkpoint_replays_with_distinct_later_event_and_same_owner():
    a=fresh();first=a.later(a.ctx.state_hash);b=Cell();b.restore(a.checkpoint())
    d=asdict(a.e2);d.update(event_id='M06_THIRD_EVENT',effective_causal_time='1999-07-01T00:00:00Z');d.pop('event_hash');e=seal_event(**d)
    left=a.later(a.ctx.state_hash,event=e);right=b.later(b.ctx.state_hash,event=e)
    assert left==right and a.checkpoint()==b.checkpoint() and left['streams']==first['streams']
    write('consumed_replay',result=left)

def test_independent_factorial_and_counterfactual_parallel_dag():
    arms={}
    for memory,epistemic,history in itertools.product(['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'],['NONE','BELIEF','INACCESSIBLE'],['STORED','OMITTED','WITHHELD']):
        c=fresh(memory,epistemic,history);before=c.export();out=c.later(c.ctx.state_hash,history_access=history!='WITHHELD')
        assert before['owner_state']==out['read']['actual_state']==c.ctx.data()
        assert out['streams']=={'memory':{'NONE':'AMPLIFY','CERTAIN':'BUFFER','UNCERTAIN':'DEFLECT','UNAVAILABLE':'AMPLIFY'}[memory],'epistemic':{'NONE':'AMPLIFY','BELIEF':'REROUTE','INACCESSIBLE':'BLOCK'}[epistemic]}
        assert all(not x['memory_basis_refs'] and x['actor_facing_basis_refs']==(c.e1.event_id+':'+c.e1.event_hash,) for x in c.ctx.stances.values())
        assert out['read']['actor']==c.e1.actor_scope==c.e2.actor_scope
        assert out['read']['state_hash']==c.ctx.state_hash
        assert c.reg.verify_event(c.e1) and c.reg.verify_event(c.e2)
        assert out['receipt']['payload']['public_standing']=='HOLD_NO_PUBLIC_RATIFICATION_OWNER'
        arms[(memory,epistemic,history)]=(before,out,c.export())
        write('factorial_'+'_'.join((memory,epistemic,history)),before=before,result=out,after=c.export())
    contrasts=[]
    for e,h in itertools.product(['NONE','BELIEF','INACCESSIBLE'],['STORED','OMITTED','WITHHELD']):
        a,ao,_=arms[('CERTAIN',e,h)];b,bo,_=arms[('UNCERTAIN',e,h)]
        assert a['history']==b['history'] and set(a['owner_state']['memories'])==set(b['owner_state']['memories'])
        assert ao['streams']['memory']!=bo['streams']['memory'] and ao['streams']['epistemic']==bo['streams']['epistemic']
        contrasts.append(dict(fixed_epistemic=e,history=h,left=ao['streams'],right=bo['streams']))
    for m,h in itertools.product(['NONE','CERTAIN','UNCERTAIN','UNAVAILABLE'],['STORED','OMITTED','WITHHELD']):
        a,ao,_=arms[(m,'NONE',h)];b,bo,_=arms[(m,'BELIEF',h)]
        assert a['owner_state']['memories']==b['owner_state']['memories'] and a['history']==b['history']
        assert ao['streams']['memory']==bo['streams']['memory'] and ao['streams']['epistemic']!=bo['streams']['epistemic']
    left=run_positive_chain(_comparison=False);right=run_positive_chain(_comparison=False,omit_first_effect=True,later_event_requires_prior_effect=False)
    assert left['state']==right['state'] and left['later_event_response']['effect_kind']=='DEFLECT' and right['later_event_response']['effect_kind']=='AMPLIFY'
    write('independent_causal_contrasts',memory_contrasts=contrasts,history_comparator=dict(stored=left,omitted=right),serial_edge='UNPROVED; direct actor-facing basis, empty memory_basis_refs')
