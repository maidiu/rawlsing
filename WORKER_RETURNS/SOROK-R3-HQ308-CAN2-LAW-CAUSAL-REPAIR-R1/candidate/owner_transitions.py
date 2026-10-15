"""Bounded candidate owner working views, not accepted destination authority.

No-context calls can describe proposals, never applied memory/epistemic state.
A FixtureOwnerState explicitly binds an admitted full event, rule, actor, exact
pre-state, canonical claim and source features. It persists candidate state only.
Production owner/public standing remain HOLD; no registry/semantic issuance.
"""
import hashlib
from dataclasses import asdict,replace
from copy import deepcopy
from .adopted_contract import *
from .candidate_registry_fixture import digest,canon,validate_event,parse_time
ADP016_RULE_ID='CAND_ADP016_TRACE_COMMIT'
ADP016_RULE_VERSION='2.0.0-candidate'
ADP017_RULE_ID='CAND_ADP017_EPISTEMIC_UPDATE'
ADP017_RULE_VERSION='2.0.0-candidate'

class OwnerTransitionError(Exception):
    def __init__(self,code,detail=''):
        self.code=code;self.detail=detail;super().__init__(code+':'+detail)

def fail(code,detail=''):raise OwnerTransitionError(code,detail)

def _rule_ok(rule_id,version,content_hash):
    from .can008_candidate_rule import build_default_binding
    b=build_default_binding()
    return (rule_id,version,content_hash)==(b.rule_id,b.rule_version,b.rule_content_hash)

def memory_semantic_hash(data):
    # Identity pointers are derived from the causal transition core. Exclude them
    # from the post-feature digest to avoid a self-referential hash cycle. The
    # enclosing store separately hashes the entire memory and transition record.
    return digest({k:v for k,v in data.items() if k not in ('current_state_hash','formation_transition_id','last_transition_id')})

def canonical_claim(subject_ref,predicate_ref,object_or_value,temporal_scope,subject_scope,referent_refs=(),polarity='POSITIVE'):
    content=dict(subject_ref=subject_ref,predicate_ref=predicate_ref,object_or_value=object_or_value,polarity=polarity,temporal_scope=temporal_scope,subject_scope=subject_scope,referent_refs=list(referent_refs))
    h=digest(content)
    return dict(claim_id=hashlib.sha256(('V3_CANONICAL_CLAIM'+'1'+canon(content)).encode()).hexdigest(),claim_schema_version='1',**content,canonical_content_hash=h,integrity_state='INTACT')

def verify_claim(c):
    try:
        expected=canonical_claim(**{k:c[k] for k in ('subject_ref','predicate_ref','object_or_value','temporal_scope','subject_scope','referent_refs','polarity')})
        return c==expected and bool(c['subject_ref']) and bool(c['predicate_ref'])
    except (KeyError,TypeError):return False

class FixtureOwnerState:
    """Single-process candidate store with explicit finite rule emission grants.

    Permissions are TEST_ONLY setup. No statement about a production owner,
    psychological truth, public ratification or durable external storage follows.
    """
    def __init__(self,registry,actor_id='ACTOR_SYNTH_1'):
        self.registry=registry;self.actor_id=actor_id;self.memories={};self.memory_transitions={};self.claims={};self.emissions={};self.stances={};self.epistemic_transitions=[];self.state_sets={};self.permissions={};self._pending_memory={};self._seal()
    def data(self):return deepcopy(dict(actor_id=self.actor_id,memories=self.memories,memory_transitions=self.memory_transitions,claims=self.claims,emissions=self.emissions,stances=self.stances,epistemic_transitions=self.epistemic_transitions,state_sets=self.state_sets,permissions=self.permissions))
    def _seal(self):self.state_hash=digest(self.data())
    def verify(self):
        from .can008_candidate_rule import build_default_binding
        b=build_default_binding();reg=self.registry.lookup(b.rule_id,b.rule_version)
        return reg is not None and reg.rule_content_hash==b.rule_content_hash and self.actor_id==b.actor_scope and self.state_hash==digest(self.data())
    def checkpoint(self):
        if not self.verify():fail('INTEGRITY_FAILURE')
        return dict(state=deepcopy(self.data()),pending=deepcopy(self._pending_memory))
    def restore(self,d):
        for k,v in deepcopy(d['state']).items():setattr(self,k,v)
        self._pending_memory=deepcopy(d['pending'])
        self._seal()
    def matches_prestate(self,p):
        return self.verify() and p.actor_id==self.actor_id and tuple(sorted(self.memories))==p.adp016_memory_refs and tuple(sorted(self.stances))==p.adp017_claim_refs
    def bind_claim(self,claim,event,stance_kind='BELIEF'):
        from .can008_candidate_rule import build_default_binding
        b=build_default_binding()
        if not self.verify() or not verify_claim(claim) or not self.registry.verify_event(event) or event.actor_scope!=self.actor_id:fail('INTEGRITY_FAILURE','claim/event custody')
        if tuple(event.public_features)!=('shift_feedback_window_open','supervisor_solicits_comment'):fail('UNAUTHORIZED_TRANSITION','Rule does not emit belief for these public features')
        if claim['subject_scope']!=self.actor_id or claim['subject_ref']!=self.actor_id or claim['temporal_scope']!=event.effective_causal_time or claim['referent_refs']!=[event.event_id]:fail('INTEGRITY_FAILURE','claim actor/time')
        # This rule has no knowledge-acquisition or public-ratification authority.
        if stance_kind!='BELIEF' or claim['predicate_ref']!='FIXTURE_PRIVATE_FEEDBACK_APPRAISAL' or claim['object_or_value']!='RESPECTED' or claim['polarity']!='POSITIVE':fail('UNAUTHORIZED_TRANSITION','outside finite belief rule')
        self.claims[claim['claim_id']]=deepcopy(claim)
        self.emissions[claim['claim_id']]=dict(event_id=event.event_id,event_hash=event.event_hash,rule_hash=b.rule_content_hash,stance_kind=stance_kind,operations=['ADD','WITHDRAW','SUPERSEDE_EXACT_RECORD','NO_CHANGE'])
        self._seal();return claim['claim_id']
    def commit_memory(self,proposal):
        if not self.verify():fail('INTEGRITY_FAILURE')
        if proposal.get('status')!='ADP016_FORMATION_VALIDATED_IN_FIXTURE':fail('DEFERRED_MISSING_MEMORY_BASIS')
        existing=self.memory_transitions.get(proposal.get('transition',{}).get('memory_transition_id'))
        if existing is not None:
            if digest(proposal) in self._pending_memory and existing==proposal['transition'] and self.memories.get(proposal['memory']['memory_id'])==proposal['memory']:
                return dict(status='IDEMPOTENT_REPLAY',memory_id=proposal['memory']['memory_id'],state_hash=self.state_hash,production_owner_commit=False)
            fail('MEMORY_ID_COLLISION')
        if proposal.get('pre_state_hash')!=self.state_hash:fail('PRE_STATE_HASH_MISMATCH')
        if digest(proposal) not in self._pending_memory:fail('INTEGRITY_FAILURE','Unvalidated/changed memory proposal')
        m=proposal['memory'];t=proposal['transition'];e=self.registry.event(t['causal_parent_event_refs'][0]) if t['causal_parent_event_refs'] else None
        if not e or m['objective_source_event_refs']!=[e['event_id']+':'+e['event_hash']] and tuple(m['objective_source_event_refs'])!=(e['event_id']+':'+e['event_hash'],):fail('MISSING_PARENT_EVENT')
        if m['current_state_hash']!=memory_semantic_hash(m) or t['post_state_hash']!=m['current_state_hash']:fail('INTEGRITY_FAILURE')
        if m['memory_id'] in self.memories:fail('MEMORY_ID_COLLISION')
        self.memories[m['memory_id']]=deepcopy(m);self.memory_transitions[t['memory_transition_id']]=deepcopy(t);self._seal()
        return dict(status='ADP016_TRACE_COMMITTED_IN_FIXTURE',memory_id=m['memory_id'],state_hash=self.state_hash,production_owner_commit=False)


def adp016_form_causal_trace(*,actor_id,basis_event,trace_key,content_state,owning_rule_id,owning_rule_version,owning_rule_hash,authority_id,authority_version,parent_state_hash='PRE_ROOT',memory_id_override=None,context=None,stochastic=False):
    if basis_event is None:fail('MISSING_PARENT_EVENT')
    if basis_event.admission_state!='ADMITTED' or basis_event.derived_from_future_partition or basis_event.event_kind!='EXTERNAL_RUNTIME_EVENT':fail('INELIGIBLE_NONCAUSAL_SOURCE')
    if not basis_event.event_id or not basis_event.event_hash:fail('MISSING_PARENT_EVENT')
    if content_state not in ADP016_SOURCE_FEATURE_STATE:fail('INELIGIBLE_NONCAUSAL_SOURCE')
    if not owning_rule_version:fail('MISSING_RULE_VERSION')
    if not _rule_ok(owning_rule_id,owning_rule_version,owning_rule_hash) or (authority_id,authority_version)!=('WORKER_CANDIDATE_FIXTURE','1'):fail('UNAUTHORIZED_TRANSITION','exact candidate rule/authority required')
    if not trace_key or actor_id!=basis_event.actor_scope:fail('DEFERRED_MISSING_MEMORY_BASIS')
    if not parent_state_hash:fail('PRE_STATE_HASH_MISMATCH')
    if stochastic:fail('MISSING_RNG_AUTHORITY')
    if context is not None:
        if not context.verify():fail('INTEGRITY_FAILURE')
        if not context.registry.verify_event(basis_event):fail('PARENT_EVENT_HASH_MISMATCH')
        if context.actor_id!=actor_id:fail('UNAUTHORIZED_TRANSITION')
        if trace_key!='TRACE_FEEDBACK_WINDOW_EXPERIENCE' or tuple(basis_event.public_features)!=('shift_feedback_window_open','supervisor_solicits_comment'):fail('UNAUTHORIZED_TRANSITION','No exact formation request in this rule cell')
        if parent_state_hash!=context.state_hash:fail('PRE_STATE_HASH_MISMATCH')
    # Non-context output is a draft schema only. It cannot establish an admitted
    # source, grant, transition or store mutation; the status says DEFERRED.
    src=basis_event.event_id+':'+basis_event.event_hash
    mid=digest(['V3_MEMORY',authority_id,authority_version,actor_id,src,trace_key,memory_id_override,owning_rule_id,owning_rule_version,owning_rule_hash])
    data=dict(memory_id=mid,actor_id=actor_id,representation_kind='CAUSAL_TRACE_MEMORY',formation_transition_id='',objective_source_event_refs=(src,),source_feature_bindings=tuple(canon(dict(source_event=src,feature=x,state=content_state)) for x in basis_event.public_features),retention_state='RETAINED',memory_accessibility_state='NOT_APPLICABLE_CAUSAL_TRACE',uncertainty_state='UNCERTAIN' if content_state=='AVAILABLE_UNCERTAIN' else 'CERTAIN',last_transition_id='',last_transition_effective_time=basis_event.effective_causal_time,current_state_hash='',integrity_state='INTACT')
    post=memory_semantic_hash(data)
    t=dict(memory_transition_id='',memory_id=mid,actor_id=actor_id,transition_kind='FORMATION',effective_causal_time=basis_event.effective_causal_time,authority_id=authority_id,authority_version=authority_version,authority_or_rule_hash=owning_rule_hash,memory_rule_id=ADP016_RULE_ID,memory_rule_version=ADP016_RULE_VERSION,memory_rule_hash=digest([ADP016_RULE_ID,ADP016_RULE_VERSION,PINS['ADP016_JSON']]),objective_source_event_refs=[src],causal_parent_event_refs=[basis_event.event_id],cue_or_trigger_refs=[],pre_state_hash=parent_state_hash,post_state_hash=post,feature_state_before_hash=digest(['EMPTY_FEATURE',parent_state_hash]),feature_state_after_hash=digest(data['source_feature_bindings']),decision_state='FORMATION_VALIDATED_IN_FIXTURE' if context else 'DEFERRED_MISSING_MEMORY_BASIS',integrity_state='INTACT')
    tid=digest({k:v for k,v in t.items() if k!='memory_transition_id'});t['memory_transition_id']=tid;data.update(formation_transition_id=tid,last_transition_id=tid,current_state_hash=post)
    proposal=dict(status='ADP016_FORMATION_VALIDATED_IN_FIXTURE' if context else 'DEFERRED_MISSING_MEMORY_BASIS',memory=data,transition=t,pre_state_hash=parent_state_hash,exports_to_adp017_only=True,must_not_output=list(ADP016_MUST_NOT_OUTPUT),first_person_origin_claimable=False,production_owner_commit=False,hold='NO_ACCEPTED_DESTINATION_OWNER_AUTHORITY',committed=False)
    if context is not None:context._pending_memory[digest(proposal)]=True
    return proposal


def adp016_attempt_transition(memory,transition_kind,*,parent_event=None,pre_state_hash=None,declared_parent_hash=None,context=None,stochastic=False):
    if transition_kind in ADP016_FORBIDDEN_TRANSITION_KIND or transition_kind not in ADP016_TRANSITION_KIND:fail('UNAUTHORIZED_TRANSITION')
    if memory.integrity_state!='INTACT' or validate_memory_state(memory) or memory.current_state_hash!=memory_semantic_hash(asdict(memory)):fail('INTEGRITY_FAILURE')
    if declared_parent_hash is not None and (parent_event is None or declared_parent_hash!=parent_event.event_hash):fail('PARENT_EVENT_HASH_MISMATCH')
    if pre_state_hash is not None and pre_state_hash!=memory.current_state_hash:fail('PRE_STATE_HASH_MISMATCH')
    if parent_event is None or parent_event.admission_state!='ADMITTED':fail('MISSING_PARENT_EVENT')
    if not pre_state_hash:fail('PRE_STATE_HASH_MISMATCH')
    if stochastic:fail('MISSING_RNG_AUTHORITY')
    if transition_kind=='RECALL' and memory.representation_kind=='CAUSAL_TRACE_MEMORY':fail('UNAUTHORIZED_RECALL_CUE')
    if context is None:fail('DEFERRED_MISSING_MEMORY_BASIS','No admitted owner state')
    if not context.verify() or not context.registry.verify_event(parent_event):fail('INTEGRITY_FAILURE')
    if memory.memory_id not in context.memories:fail('UNKNOWN_MEMORY_ID')
    if context.memories[memory.memory_id]!=asdict(memory):fail('INTEGRITY_FAILURE')
    # Formation is implemented. Other transition semantics require separate
    # exact rule/cue grants; never invent a degradation/recall operation here.
    fail('UNAUTHORIZED_TRANSITION','No registered transition/cue rule for '+transition_kind)


def adp016_rehydration_refused(memory,analyst_ledger_content):fail('UNAUTHORIZED_OBJECTIVE_HISTORY_REHYDRATION')


def adp017_apply_epistemic_effect(*,actor_id,claim_ref,stance_kind,stance_operation,causal_parent_refs,actor_facing_basis_refs,memory_basis_refs,owning_rule_id,owning_rule_version,owning_rule_hash,effective_causal_time,claim_objective_relation='OBJECTIVE_UNRESOLVED',claim_accessibility='CLAIM_ACCESSIBLE',context=None,pre_state_hash=None,target_record_ref=None):
    fields=dict(actor_id=actor_id,claim_ref=claim_ref,stance_kind=stance_kind,stance_operation=stance_operation,causal_parent_refs=tuple(causal_parent_refs or ()),actor_facing_basis_refs=tuple(actor_facing_basis_refs or ()),memory_basis_refs=tuple(memory_basis_refs or ()),owning_rule_id=owning_rule_id,owning_rule_version=owning_rule_version,owning_rule_hash=owning_rule_hash,effective_causal_time=effective_causal_time)
    effect=dict(effect_id=digest(['EPISTEMIC_EFFECT',fields,pre_state_hash,target_record_ref]),**fields)
    def no(code,reason):return dict(decision_state=code,detail=reason,effect=effect,stance_persisted=False,accessible_memory_auto_creates_stance=False,production_owner_commit=False)
    if not all(fields[k] for k in ('actor_id','claim_ref','owning_rule_id','owning_rule_version','owning_rule_hash','effective_causal_time','causal_parent_refs')) or stance_kind not in ADP017_STANCE_KIND or stance_operation not in ADP017_STANCE_OPERATION:return no('BLOCKED_INTEGRITY_FAILURE','Missing/invalid effect field')
    if not actor_facing_basis_refs:return no('DENIED_NON_ACTOR_SOURCE','Missing exact actor-facing basis')
    if not _rule_ok(owning_rule_id,owning_rule_version,owning_rule_hash):return no('DENIED_UNAUTHORIZED_PROMOTION','Unregistered exact rule')
    if context is None:return no('DEFERRED_MISSING_EPISTEMIC_BASIS','No canonical claim, admitted basis or owner state supplied; proposal only')
    if not context.verify() or pre_state_hash!=context.state_hash:return no('BLOCKED_INTEGRITY_FAILURE','Prestate/custody mismatch')
    claim=context.claims.get(claim_ref);grant=context.emissions.get(claim_ref)
    if not claim or not verify_claim(claim) or not grant:return no('DEFERRED_MISSING_EPISTEMIC_BASIS','Unknown canonical claim/rule emission')
    if claim['subject_scope']!=actor_id or actor_id!=context.actor_id or claim['temporal_scope']!=effective_causal_time:return no('BLOCKED_INTEGRITY_FAILURE','Actor/time mismatch')
    if (tuple(causal_parent_refs)!=(grant['event_id'],) or tuple(actor_facing_basis_refs)!=(grant['event_id']+':'+grant['event_hash'],) or grant['rule_hash']!=owning_rule_hash or grant['stance_kind']!=stance_kind):return no('DENIED_UNAUTHORIZED_PROMOTION','Exact acquisition/emission binding mismatch')
    ev=context.registry.event(grant['event_id'])
    if not ev or ev['event_hash']!=grant['event_hash'] or ev['effective_causal_time']!=effective_causal_time:return no('BLOCKED_INTEGRITY_FAILURE','Admitted parent mismatch')
    # Trace refs may condition a private update but never establish conscious
    # acquisition or a knowledge grant. This registered rule emits BELIEF only.
    if any(m not in context.memories for m in memory_basis_refs):return no('DENIED_NON_ACTOR_SOURCE','Unknown memory')
    if stance_kind=='KNOWLEDGE':return no('DEFERRED_MISSING_EPISTEMIC_BASIS','No accepted knowledge-acquisition rule in this candidate')
    if stance_operation in ('WITHDRAW','SUPERSEDE_EXACT_RECORD') and (target_record_ref is None or target_record_ref not in context.stances):return no('DEFERRED_MISSING_EPISTEMIC_BASIS','Exact target record required')
    if claim_accessibility not in ('CLAIM_ACCESSIBLE','CLAIM_INACCESSIBLE','CLAIM_ACCESS_UNKNOWN'):return no('BLOCKED_INTEGRITY_FAILURE','Unknown accessibility class')
    before=context.state_hash
    if stance_operation=='NO_CHANGE':return no('NO_EPISTEMIC_TRANSITION','No mutation')
    if target_record_ref is not None and stance_operation in ('WITHDRAW','SUPERSEDE_EXACT_RECORD'):
        target=context.stances[target_record_ref]
        if target['claim_ref']!=claim_ref or target['actor_id']!=actor_id:return no('BLOCKED_INTEGRITY_FAILURE','Foreign exact target')
        del context.stances[target_record_ref]
    if stance_operation in ('ADD','SUPERSEDE_EXACT_RECORD'):context.stances[effect['effect_id']]=deepcopy(effect)
    # State set supports coexisting records; no bulk coherence or auto truth edit.
    record=dict(actor_id=actor_id,effect=deepcopy(effect),pre_state_hash=before,post_stance_set_hash=digest(context.stances),target_record_ref=target_record_ref,causal_parent_refs=list(causal_parent_refs),authority_hash=PINS['ADP017_JSON'])
    record['transition_id']=digest(record)
    state=dict(actor_id=actor_id,claim_id=claim_ref,active_stance_records=[deepcopy(v) for k,v in sorted(context.stances.items()) if v['claim_ref']==claim_ref],current_claim_accessibility=claim_accessibility,accessibility_basis_refs=list(actor_facing_basis_refs),analyst_relation='OBJECTIVE_UNRESOLVED',objective_relation_authority='HOLD_NO_OBJECTIVE_TRUTH_OWNER',last_transition_ref=record['transition_id'],integrity_state='INTACT')
    state['current_state_hash']=digest(state);context.state_sets[claim_ref]=state
    permission=first_person_permission(stance_kind if state['active_stance_records'] else None,claim_accessibility)
    context.permissions[claim_ref]=dict(actor_id=actor_id,claim_id=claim_ref,permission=permission,epistemic_state_hash=state['current_state_hash'],basis_refs=list(actor_facing_basis_refs),permission_source='TEST_ONLY_CANDIDATE_STATE; NOT_ACCEPTED_OWNER',hidden_origin_claimable=False)
    record['post_state_set_hash']=state['current_state_hash'];record['authority_hash']=PINS['ADP017_JSON'];context.epistemic_transitions.append(record);context._seal()
    return dict(decision_state='APPLIED_EPISTEMIC_TRANSITION',effect=deepcopy(effect),transition=deepcopy(record),state_hash=context.state_hash,stance_persisted=stance_operation in ('ADD','SUPERSEDE_EXACT_RECORD'),accessible_memory_auto_creates_stance=False,production_owner_commit=False,grade='TEST_ONLY_CANDIDATE_STATE',public_ratification='HOLD_NO_PUBLIC_STANDING_OWNER')


def adp017_first_person_check(stance_kind,claim_accessibility,memory_representation_kind=None,memory_accessibility=None,*,context=None,claim_ref=None,state_hash=None):
    permission=first_person_permission(stance_kind,claim_accessibility) if stance_kind in ADP017_STANCE_KIND or stance_kind is None else 'DEFER_MISSING_AUTHORITY'
    if memory_accessibility=='ACCESS_UNKNOWN':permission='DEFER_MISSING_AUTHORITY'
    elif memory_representation_kind=='CAUSAL_TRACE_MEMORY' or memory_accessibility=='INACCESSIBLE':permission='DENY_FIRST_PERSON_CLAIM'
    elif permission.startswith('PERMIT_'):
        # Caller-supplied stance/access strings are not a current permission
        # record. Any actual permit must bind the exact verified state snapshot.
        snapshot=context.state_sets.get(claim_ref) if context is not None and context.verify() else None
        record=context.permissions.get(claim_ref) if snapshot is not None else None
        if (record is None or snapshot['current_state_hash']!=state_hash or record['epistemic_state_hash']!=state_hash or snapshot['current_claim_accessibility']!=claim_accessibility or not any(x['stance_kind']==stance_kind for x in snapshot['active_stance_records'])):
            permission='DEFER_MISSING_AUTHORITY'
        else:permission=record['permission']
    return dict(first_person_permission=permission,self_explanation_of_hidden_origin='BLOCKED',analyst_only_causal_trace_actor_claimable=False,grade='TEST_ONLY_CANDIDATE_PERMISSION; production owner HOLD')


def adp017_sole_memory_basis_failclosed(stance_kind,claim_accessibility,basis_memory_state):
    m=basis_memory_state
    if m.memory_accessibility_state=='INACCESSIBLE' or m.retention_state=='CONTENT_UNAVAILABLE':p='DENY_FIRST_PERSON_CLAIM'
    elif m.memory_accessibility_state=='ACCESS_UNKNOWN' or m.retention_state=='RETENTION_UNKNOWN':p='DEFER_MISSING_AUTHORITY'
    else:p=adp017_first_person_check(stance_kind,claim_accessibility,m.representation_kind,m.memory_accessibility_state)['first_person_permission']
    return dict(first_person_permission=p,decision_state='NO_EPISTEMIC_TRANSITION',memory_inaccessibility_auto_erases_stance=False)
