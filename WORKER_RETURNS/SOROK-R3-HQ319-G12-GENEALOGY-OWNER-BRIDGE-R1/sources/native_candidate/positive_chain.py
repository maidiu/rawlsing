"""Atomic sourcefree candidate experiment, with explicit production owner HOLD.

The demonstrated response contrast uses exact prior CAN008 current history.
ADP016/017 state is applied/reloaded in a finite local fixture, never described
as an accepted destination-owner operation or public-standing ratification.
"""
import hashlib,json,time
from copy import deepcopy
from dataclasses import asdict,replace
from .adopted_contract import AdmittedEvent,GeneratedMemoryState
from .candidate_registry_fixture import CandidateRegistryFixture,digest,event_digest,parse_time
from .can008_candidate_rule import build_default_binding,coupline_evaluate,response_rule_apply,build_response_receipt,register_default_rule,OwnerPrestate,RULE_ID,RULE_VERSION
from .owner_transitions import adp016_form_causal_trace,adp017_apply_epistemic_effect,FixtureOwnerState,canonical_claim,OwnerTransitionError
CHAIN_VERSION='CAN2_SOURCEFREE_CHAIN@2'
CHAIN_GRAIN='SOURCEFREE_CANDIDATE_CHAIN__NOT_ADOPTED__NOT_V3_OPERATION'

class LedgerIntegrityError(Exception):pass

class ChainEventLedger:
    def __init__(self):self.entries=[];self._sealed_digest=digest([])
    def verify(self):
        if digest(self.entries)!=self._sealed_digest:raise LedgerIntegrityError('LEDGER_CONTENT_MUTATED')
        prev=None
        for i,e in enumerate(self.entries):
            if e['seq']!=i or e['prev_entry_hash']!=prev or e['entry_hash']!=digest({k:v for k,v in e.items() if k!='entry_hash'}):raise LedgerIntegrityError('LEDGER_CHAIN_INTEGRITY')
            prev=e['entry_hash']
        return True
    def commit(self,kind,payload,effective_causal_time,causal_parent_refs):
        self.verify()
        try:t=parse_time(effective_causal_time)
        except (ValueError,TypeError,AttributeError):
            # Support legacy year-only standalone causal-order fixtures.
            try:t=parse_time(effective_causal_time+'-01-01T00:00:00Z')
            except Exception:return dict(status='REFUSED',code='INVALID_CAUSAL_TIME')
        if self.entries:
            last=self.entries[-1]['effective_causal_time'];last=last+'-01-01T00:00:00Z' if len(last)==4 else last
            if t<parse_time(last):return dict(status='REFUSED',code='BLOCK_REVERSE_CHRONOLOGY_CAUSAL_PARENT')
        e=dict(seq=len(self.entries),kind=kind,payload=deepcopy(payload),effective_causal_time=effective_causal_time,causal_parent_refs=list(causal_parent_refs),prev_entry_hash=self.entries[-1]['entry_hash'] if self.entries else None)
        e['entry_hash']=digest(e);self.entries.append(e);self._sealed_digest=digest(self.entries)
        return dict(status='COMMITTED_IN_CAUSAL_ORDER',entry=deepcopy(e))
    def read_effects(self,kind=None):
        self.verify();return deepcopy([e for e in self.entries if kind is None or e['kind']==kind])
    def ledger_hash(self):self.verify();return digest(self.entries)
    def checkpoint(self):self.verify();return deepcopy(self.entries),self._sealed_digest
    def restore(self,s):self.entries,self._sealed_digest=deepcopy(s)


def seal_event(**kwargs):
    # Constructor is intentionally a visible test seam for the inherited hostile
    # instrumentation. Verify the returned object's full bytes, not input labels.
    data=dict(public_features=(),causal_parent_event_ids=(),derived_from_future_partition=False,reverse_chronology_flag=False);data.update(kwargs)
    return AdmittedEvent(event_hash=digest(data),**data)


def run_positive_chain(*,world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',actor_id='ACTOR_SYNTH_1',effect_kind='BUFFER',registry=None,include_later_event=True,later_event_requires_prior_effect=True,omit_first_effect=False,_comparison=True,failure_at=None):
    reg=registry if registry is not None else CandidateRegistryFixture();ledger=ChainEventLedger();start=time.perf_counter()
    registration=register_default_rule(reg)
    if registration.get('status')!='CANDIDATE_REGISTERED_IN_FIXTURE':return dict(terminal='RULE_REGISTRATION_REFUSED',detail=registration,n_ledger_entries=0)
    binding=build_default_binding();ctx=FixtureOwnerState(reg,actor_id)
    pre=OwnerPrestate(actor_id=actor_id,can010_strivings=('KEEP_STABLE_SHIFT',),can011_practices=('ASK_CLARIFICATION',),world_ref=world_ref,world_as_of=world_as_of)
    # Failed event transactions restore ALL fixture event admissions, ledger,
    # memory and epistemic sets. A later refusal retains the earlier valid event.
    snapshots=[]
    def checkpoint():return ledger.checkpoint(),reg.checkpoint(),ctx.checkpoint()
    def rollback(s):ledger.restore(s[0]);reg.restore(s[1]);ctx.restore(s[2])
    def ensure(ok,code):
        if not ok:raise OwnerTransitionError(code)
    def event(n):
        return seal_event(event_id='EV1_FEEDBACK_WINDOW_ENCOUNTER' if n==1 else 'EV2_LATER_SHIFT_CHANGE_REQUEST',issuer_authority_id='ISSUER_AUTH_WORLD_SCHED' if n==1 else 'ISSUER_AUTH_INSTITUTION',issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',effective_causal_time='1998-10-03T16:00:00Z' if n==1 else '1998-11-20T09:00:00Z',actor_scope=actor_id,world_ref=world_ref,world_as_of=world_as_of,admission_state='ADMITTED',public_features=('shift_feedback_window_open','supervisor_solicits_comment') if n==1 else ('shift_change_request_window',))
    def commit_response(e,c,r,receipt,prior=()):
        ensure(r.get('decision_state')=='RESPONSE_EFFECTS_PRODUCED',r.get('decision_state','RESPONSE_REFUSED'))
        ensure(all(x['validated'] for x in r['target_owner_effect_requests']),'TARGET_PRECHECK_REFUSED')
        payload=dict(effect_kind=r['current_response_consequence']['effect_kind'],receipt_hash=receipt['receipt_hash'],actor_id=e.actor_scope,world_ref=e.world_ref,world_as_of=e.world_as_of,event_id=e.event_id,event_hash=e.event_hash,rule_hash=binding.rule_content_hash,prior_effect_refs=[x['entry_hash'] for x in prior],response_receipt=deepcopy(receipt))
        out=ledger.commit('CAN008_CURRENT_RESPONSE_EFFECT',payload,e.effective_causal_time,[e.event_id]+[x['payload']['event_id'] for x in prior])
        if out['status']=='NOT_COMMITTED_REVIEWER_ABLATION':return out
        ensure(out['status']=='COMMITTED_IN_CAUSAL_ORDER',out.get('code','COMMIT_REFUSED'))
        for x in r['target_owner_effect_requests']:x['committed']=True
        return out
    first_checkpoint=checkpoint()
    try:
        e1=event(1);c=coupline_evaluate(e1,pre,binding,reg);r=response_rule_apply(c,pre,binding,effect_kind);receipt=build_response_receipt(e1,pre,binding,c,r)
        ensure(c.get('decision_state')=='COUPLING_EVALUATED',c.get('code',c.get('decision_state','COUPLING_REFUSED')))
        if failure_at=='after_coupling':raise OwnerTransitionError('TEST_FAULT_AFTER_COUPLING')
        # Prevalidate all memory and epistemic material before publishing event.
        trace=adp016_form_causal_trace(actor_id=actor_id,basis_event=e1,trace_key='TRACE_FEEDBACK_WINDOW_EXPERIENCE',content_state='AVAILABLE_SOURCE_BOUND',owning_rule_id=RULE_ID,owning_rule_version=RULE_VERSION,owning_rule_hash=binding.rule_content_hash,authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1',parent_state_hash=ctx.state_hash,context=ctx)
        if failure_at=='after_trace_validation':raise OwnerTransitionError('TEST_FAULT_AFTER_TRACE')
        memory_commit=ctx.commit_memory(trace)
        claim=canonical_claim(actor_id,'FIXTURE_PRIVATE_FEEDBACK_APPRAISAL','RESPECTED',e1.effective_causal_time,actor_id,[e1.event_id])
        claim_id=ctx.bind_claim(claim,e1)
        epi=adp017_apply_epistemic_effect(actor_id=actor_id,claim_ref=claim_id,stance_kind='BELIEF',stance_operation='ADD',causal_parent_refs=[e1.event_id],actor_facing_basis_refs=[e1.event_id+':'+e1.event_hash],memory_basis_refs=[trace['memory']['memory_id']],owning_rule_id=RULE_ID,owning_rule_version=RULE_VERSION,owning_rule_hash=binding.rule_content_hash,effective_causal_time=e1.effective_causal_time,context=ctx,pre_state_hash=ctx.state_hash)
        ensure(epi['decision_state']=='APPLIED_EPISTEMIC_TRANSITION',epi['decision_state'])
        if failure_at=='after_epistemic':raise OwnerTransitionError('TEST_FAULT_AFTER_EPISTEMIC')
        first_commit=dict(status='CONTROL_OMITTED_FIRST_EFFECT') if omit_first_effect else commit_response(e1,c,r,receipt)
        if failure_at=='after_current_commit':raise OwnerTransitionError('TEST_FAULT_AFTER_CURRENT')
        for kind,payload in [('ADP016_TRACE_COMMIT',dict(memory=trace['memory'],transition=trace['transition'],fixture_state_hash=ctx.state_hash)),('ADP017_EPISTEMIC_UPDATE',dict(effect=epi['effect'],transition=epi['transition'],fixture_state_hash=ctx.state_hash))]:
            result=ledger.commit(kind,payload,e1.effective_causal_time,[e1.event_id]);ensure(result['status']=='COMMITTED_IN_CAUSAL_ORDER',result.get('code','DESTINATION_FIXTURE_REFUSED'))
        if failure_at=='after_owner_journal':raise OwnerTransitionError('TEST_FAULT_AFTER_OWNER_JOURNAL')
        snapshots.append(dict(event=e1.event_id,state_hash=ctx.state_hash,ledger_hash=ledger.ledger_hash(),candidate_only=True))
    except (OwnerTransitionError,LedgerIntegrityError,ValueError) as exc:
        rollback(first_checkpoint)
        return dict(chain_version=CHAIN_VERSION,terminal='FIRST_EVENT_REFUSED',code=getattr(exc,'code',str(exc)),n_ledger_entries=len(ledger.entries),state=ctx.data(),ledger_entries=deepcopy(ledger.entries),registry=reg.as_dict(),production_owner_hold=True)
    later=None;difference=None
    if include_later_event:
        s=checkpoint()
        try:
            e2=event(2);prior=ledger.read_effects('CAN008_CURRENT_RESPONSE_EFFECT')
            # The exact rule predicate validates every history row before use.
            for row in prior:
                p=row['payload'];record=reg.event(p.get('event_id',''))
                ensure(record is not None and p.get('event_hash')==record['event_hash'] and p.get('actor_id')==actor_id and p.get('world_ref')==world_ref and p.get('world_as_of')==world_as_of and p.get('rule_hash')==binding.rule_content_hash and parse_time(row['effective_causal_time'])<parse_time(e2.effective_causal_time),'PRIOR_HISTORY_BINDING_INVALID')
                rcpt=p.get('response_receipt',{});ensure(rcpt.get('effect_kind')==p.get('effect_kind') and rcpt.get('rule_content_hash')==binding.rule_content_hash and rcpt.get('decision_state')=='RESPONSE_EFFECTS_PRODUCED' and rcpt.get('precipitating_event',{}).get('event_hash')==record['event_hash'] and rcpt.get('precipitating_event',{}).get('issuer_authority_version')==record['issuer_authority_version'] and rcpt.get('precipitating_event',{}).get('actor_scope')==actor_id and rcpt.get('current_response_consequence',{}).get('effect_kind')==p.get('effect_kind'),'PRIOR_RECEIPT_BINDING_INVALID');ensure(p.get('receipt_hash')==rcpt.get('receipt_hash')==hashlib.sha256(json.dumps({k:v for k,v in rcpt.items() if k!='receipt_hash'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),'PRIOR_RECEIPT_INTEGRITY_FAILURE')
            if later_event_requires_prior_effect and not prior:raise OwnerTransitionError('BLOCK_MISSING_PRIOR_OWNER_EFFECT')
            pre2=replace(pre,adp016_memory_refs=tuple(sorted(ctx.memories)),adp017_claim_refs=tuple(sorted(ctx.stances)),prior_can008_response_count=len(prior));pre2._context=ctx
            c2=coupline_evaluate(e2,pre2,binding,reg)
            chosen='DEFLECT' if any(x['payload']['effect_kind']=='BUFFER' for x in prior) else 'AMPLIFY'
            r2=response_rule_apply(c2,pre2,binding,chosen);receipt2=build_response_receipt(e2,pre2,binding,c2,r2)
            ensure(c2.get('decision_state')=='COUPLING_EVALUATED',c2.get('code','LATER_COUPLING_REFUSED'))
            if failure_at=='later_after_coupling':raise OwnerTransitionError('TEST_FAULT_LATER')
            committed=commit_response(e2,c2,r2,receipt2,prior)
            later=dict(event2_id=e2.event_id,effect_kind=chosen,prior_effect_read=bool(prior),prior_effect_refs=[x['entry_hash'] for x in prior],candidate_state_read_hash=ctx.state_hash,commit=committed['status'],receipt2_hash=receipt2['receipt_hash'])
        except (OwnerTransitionError,LedgerIntegrityError,ValueError) as exc:
            rollback(s)
            return dict(chain_version=CHAIN_VERSION,terminal='LATER_EVENT_REFUSED',code=getattr(exc,'code',str(exc)),n_ledger_entries=len(ledger.entries),state=ctx.data(),ledger_entries=deepcopy(ledger.entries),production_owner_hold=True)
        if _comparison:
            control=run_control_without_prior_effect(_comparison=False)
            actual=control['later_event_response']['effect_kind']
            difference=dict(with_prior_effect=chosen,control_without_prior_effect=actual,typed_difference=chosen!=actual,control_executed=True,control_digest=control['full_replay_digest'])
    result=dict(chain_version=CHAIN_VERSION,chain_grain=CHAIN_GRAIN,terminal='CHAIN_COMPLETE',rule_registration=registration,occurrence_gate=c['gate'],coupling_decision_state=c['decision_state'],receivability=c['receivability'],uptake_appraisal_projection=c['uptake_appraisal_projection'],situated_recruitment=c['situated_recruitment'],response_effect_kind=r['current_response_consequence']['effect_kind'],response_durability=r['current_response_consequence']['durability'],response_receipt_hash=receipt['receipt_hash'],target_owner_effect_committed=first_commit['status']=='COMMITTED_IN_CAUSAL_ORDER',target_commit_scope='CAN008_CURRENT_HISTORY_ONLY; fixture ADP state is separate',production_owner_hold='HOLD_NO_ACCEPTED_DESTINATION_OWNER_AUTHORITY',public_standing_hold='HOLD_NO_PUBLIC_RATIFICATION_OWNER',causal_order_enforced=True,adp016_trace=dict(status=memory_commit['status'],memory_id=trace['memory']['memory_id'],representation_kind='CAUSAL_TRACE_MEMORY',retention_state='RETAINED',memory_accessibility_state='NOT_APPLICABLE_CAUSAL_TRACE',content_first_person_readable=False,must_not_output=list(trace['must_not_output'])),adp017_epistemic=dict(decision_state=epi['decision_state'],stance_kind='BELIEF',stance_operation='ADD',accessible_memory_auto_creates_stance=False,grade='TEST_ONLY_CANDIDATE_STATE'),later_event_response=later,later_response_typed_difference=difference,ledger_hash=ledger.ledger_hash(),n_ledger_entries=len(ledger.entries),state=ctx.data(),state_hash=ctx.state_hash,event_snapshots=snapshots)
    result['full_replay_digest']=digest(dict(receipt=receipt,trace=trace,epi=epi,later=later,ledger=ledger.entries,state=ctx.data()))
    result['wall_seconds']=round(time.perf_counter()-start,6)
    return result


def run_control_without_prior_effect(**kwargs):
    kwargs.update(include_later_event=True,later_event_requires_prior_effect=False,omit_first_effect=True)
    return run_positive_chain(**kwargs)
