"""Finite TEST_ONLY native reconstruction, not an issuer or protected attestation.

Reexecute the pinned CAN2 fixture APIs in isolated owner objects. This proves a
native path consistent with the retained whole checkpoint, not external custody.
MS1 uses the default native memory identity; noninvertible overrides are not
invented here. Existing native owners and accepted authorities remain unchanged.
"""
from copy import deepcopy
from dataclasses import asdict
import json
from candidate import owner_transitions as owner, can008_candidate_rule as rule
from candidate.candidate_registry_fixture import canon,digest,parse_time,validate_event

class NativeProofError(Exception):
    pass

def need(ok,code):
    if not ok:raise NativeProofError(code)

def event(reg,event_id,event_type):
    raw=reg.event(event_id);need(isinstance(raw,dict),'MS3_SOURCE_EVENT_MISSING')
    e=event_type(**raw)
    need(validate_event(e) is None and reg.verify_event(e),'MS3_SOURCE_EVENT_INVALID')
    return e

def source_contract(ctx,reg,binding,e1):
    need(ctx.registry is reg and ctx.verify() and reg.verify(),'MS3_OWNER_REGISTRY_INTEGRITY')
    need(binding==rule.build_default_binding(),'MS3_EXACT_RULE_BINDING')
    need(ctx.actor_id==e1.actor_scope and reg.verify_event(e1) and validate_event(e1) is None,'MS3_SOURCE_EVENT_BINDING')

def selected(ctx,reg,binding,e1,ref,at=None):
    source_contract(ctx,reg,binding,e1)
    claim=owner.canonical_claim(e1.actor_scope,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e1.effective_causal_time,e1.actor_scope,[e1.event_id])
    need(ref==claim['claim_id'],'MS3_UNKNOWN_SELECTED_CLAIM')
    need(ctx.claims.get(ref)==claim and owner.verify_claim(claim),'MS3_CANONICAL_CLAIM_BINDING')
    expected=dict(event_id=e1.event_id,event_hash=e1.event_hash,rule_hash=binding.rule_content_hash,stance_kind='BELIEF',operations=['ADD','WITHDRAW','SUPERSEDE_EXACT_RECORD','NO_CHANGE'])
    need(ctx.emissions.get(ref)==expected,'MS3_CLAIM_SOURCE_EMISSION')
    if at is not None:
        cut=parse_time(at);need(parse_time(e1.effective_causal_time)<cut,'MS3_RESPONSE_CAUSAL_CUT')
        for t in ctx.epistemic_transitions:
            if t['effect']['claim_ref']==ref:need(parse_time(t['effect']['effective_causal_time'])<=cut,'MS3_SELECTED_EFFECT_AFTER_RESPONSE')
    return ref

def copy_owner(reg,state):
    nxt=owner.FixtureOwnerState(reg);nxt.restore(dict(state=state,pending={}));return nxt

def reconstruct(ctx,reg,binding,e1):
    """Return exact native step receipts only if the complete target reproduces."""
    source_contract(ctx,reg,binding,e1)
    target=ctx.data();root=owner.FixtureOwnerState(reg).data()
    need(set(target)==set(root) and target['actor_id']==root['actor_id'],'MS3_NATIVE_STATE_SCHEMA')
    need(set(target['emissions'])==set(target['claims']),'MS3_NATIVE_EMISSION_COVERAGE')
    visited=set()
    def walk(current,claims,memories):
        key=current.state_hash
        if key in visited:return None
        visited.add(key);index=len(current.epistemic_transitions)
        if not claims and not memories and index==len(target['epistemic_transitions']):
            return [] if canon(current.data())==canon(target) else None
        candidates=[]
        if index<len(target['epistemic_transitions']):
            t=target['epistemic_transitions'][index]
            if t['pre_state_hash']==current.state_hash:
                for access in ['CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN']:
                    nxt=copy_owner(reg,current.data());args=deepcopy({k:v for k,v in t['effect'].items() if k!='effect_id'})
                    args.update(context=nxt,pre_state_hash=current.state_hash,target_record_ref=t['target_record_ref'],claim_accessibility=access)
                    result=owner.adp017_apply_epistemic_effect(**args)
                    if result['decision_state']=='APPLIED_EPISTEMIC_TRANSITION' and canon(result['transition'])==canon(t):
                        candidates.append((nxt,claims,memories,dict(kind='ADP017',pre_state_hash=current.state_hash,post_state_hash=nxt.state_hash,transition_id=t['transition_id'],native_result=result)))
        for mid in memories:
            m=target['memories'][mid];tid=m.get('formation_transition_id');t=target['memory_transitions'].get(tid)
            if not isinstance(t,dict) or t.get('pre_state_hash')!=current.state_hash:continue
            # No defaulting empty sources or trusting a self-rehashed memory.
            if tuple(m.get('objective_source_event_refs',()))!=(e1.event_id+':'+e1.event_hash,):continue
            if tuple(t.get('causal_parent_event_refs',()))!=(e1.event_id,):continue
            bindings=[json.loads(x) for x in m.get('source_feature_bindings',())]
            if len(bindings)!=len(e1.public_features):continue
            values={x['state'] for x in bindings}
            if len(values)!=1:continue
            value=next(iter(values));nxt=copy_owner(reg,current.data())
            try:
                proposal=owner.adp016_form_causal_trace(actor_id=ctx.actor_id,basis_event=e1,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state=value,owning_rule_id=binding.rule_id,owning_rule_version=binding.rule_version,owning_rule_hash=binding.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=current.state_hash,context=nxt)
                if canon(proposal['memory'])!=canon(m) or canon(proposal['transition'])!=canon(t):continue
                result=nxt.commit_memory(proposal)
            except owner.OwnerTransitionError:continue
            if result['status']!='ADP016_TRACE_COMMITTED_IN_FIXTURE':continue
            candidates.append((nxt,claims,tuple(x for x in memories if x!=mid),dict(kind='ADP016',pre_state_hash=current.state_hash,post_state_hash=nxt.state_hash,transition_id=tid,native_proposal=proposal,native_result=result)))
        for ref in claims:
            claim=target['claims'][ref];emission=target['emissions'][ref];nxt=copy_owner(reg,current.data())
            try:
                e=event(reg,emission['event_id'],type(e1));actual=nxt.bind_claim(claim,e,stance_kind=emission['stance_kind'])
            except (owner.OwnerTransitionError,NativeProofError):continue
            if actual!=ref or canon(nxt.emissions[ref])!=canon(emission):continue
            candidates.append((nxt,tuple(x for x in claims if x!=ref),memories,dict(kind='CANONICAL_CLAIM_BIND',pre_state_hash=current.state_hash,post_state_hash=nxt.state_hash,claim_ref=ref,event_id=e.event_id,event_hash=e.event_hash)))
        for nxt,pc,pm,step in candidates:
            suffix=walk(nxt,pc,pm)
            if suffix is not None:return [step]+suffix
        return None
    steps=walk(copy_owner(reg,root),tuple(sorted(target['claims'])),tuple(sorted(target['memories'])))
    need(steps is not None,'MS3_NATIVE_TIMELINE_INVALID')
    terminal={}
    for t in target['epistemic_transitions']:terminal[t['effect']['claim_ref']]=t['transition_id']
    for ref,tid in terminal.items():need(target['state_sets'][ref]['last_transition_ref']==tid,'MS3_NATIVE_TERMINAL_MISMATCH')
    return dict(schema='MS3_SOURCEFREE_NATIVE_TRAJECTORY@1',root_state_hash=digest(root),current_owner_state_hash=ctx.state_hash,steps=steps,terminal_transition_refs=terminal,scope='FINITE_NATIVE_REEXECUTION; NOT_PROTECTED_EXTERNAL_ATTESTATION')

def validate(ctx,reg,binding,e1,ref=None,at=None):
    if ref is not None:selected(ctx,reg,binding,e1,ref,at)
    proof=reconstruct(ctx,reg,binding,e1)
    if ref is not None:
        snapshot=ctx.state_sets.get(ref);permission=ctx.permissions.get(ref)
        if snapshot is None:need(permission is None and not any(x['claim_ref']==ref for x in ctx.stances.values()),'MS3_BOUND_NONE_INVALID')
        else:
            active=snapshot['active_stance_records'];expected=owner.first_person_permission('BELIEF' if active else None,snapshot['current_claim_accessibility'])
            need(permission['permission']==expected,'MS3_NATIVE_PERMISSION_VALUE')
            need(permission['epistemic_state_hash']==snapshot['current_state_hash'],'MS3_NATIVE_PERMISSION_SNAPSHOT')
    return proof
