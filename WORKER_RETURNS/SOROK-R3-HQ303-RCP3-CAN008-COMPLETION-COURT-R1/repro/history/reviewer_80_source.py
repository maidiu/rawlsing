"""RCP3 source-aware hostile predicates from adopted law, not author expected values.

Original RCP2 prereg stays byte-identical. These are later reviewer tests; failures
are retained as scientific REDs, never xfailed or inverted into acceptance.
"""
from pathlib import Path
from dataclasses import replace
import copy,json,hashlib,re
import pytest
from causal_probe import observe,RET
from candidate.adopted_contract import AdmittedEvent,GeneratedMemoryState
from candidate import can008_candidate_rule as rule
from candidate import owner_transitions as owner
from candidate.candidate_registry_fixture import CandidateRegistryFixture
from candidate.positive_chain import ChainEventLedger


def record(name,**data):
    p=RET/'repro/observations';p.mkdir(exist_ok=True)
    (p/(name+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')


def event(**kw):
    data=dict(event_id='REVIEW_EVENT_A',event_hash=hashlib.sha256(b'reviewer synthetic event A').hexdigest(),
              issuer_authority_id='ISSUER_AUTH_WORLD_SCHED',issuer_authority_version='1',event_kind='EXTERNAL_RUNTIME_EVENT',
              effective_causal_time='1998-10-03T16:00:00Z',actor_scope='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',
              world_as_of='1998-10-03T16:00:00Z',admission_state='ADMITTED',public_features=('reviewer_public_fixture',))
    data.update(kw);return AdmittedEvent(**data)


def prestate(**kw):
    data=dict(actor_id='ACTOR_SYNTH_1',world_ref='W_SYNTH_1998',world_as_of='1998-10-03T16:00:00Z',
              can010_strivings=('KEEP_STABLE_SHIFT',),can011_practices=('ASK_CLARIFICATION',))
    data.update(kw);return rule.OwnerPrestate(**data)


def registry():
    reg=CandidateRegistryFixture();rule.register_default_rule(reg);return reg


def trace(**kw):
    data=dict(actor_id='ACTOR_SYNTH_1',basis_event=event(),trace_key='REVIEW_TRACE',content_state='AVAILABLE_SOURCE_BOUND',
              owning_rule_id=rule.RULE_ID,owning_rule_version=rule.RULE_VERSION,owning_rule_hash=rule.build_default_binding().rule_content_hash,
              authority_id='WORKER_CANDIDATE_FIXTURE',authority_version='1')
    data.update(kw);return owner.adp016_form_causal_trace(**data)


def epistemic(**kw):
    data=dict(actor_id='ACTOR_SYNTH_1',claim_ref='REVIEW_CANONICAL_CLAIM',stance_kind='BELIEF',stance_operation='ADD',
              causal_parent_refs=('REVIEW_EVENT_A',),actor_facing_basis_refs=('REVIEW_EVENT_A:public',),memory_basis_refs=(),
              owning_rule_id=rule.RULE_ID,owning_rule_version=rule.RULE_VERSION,owning_rule_hash=rule.build_default_binding().rule_content_hash,
              effective_causal_time='1998-10-03T16:00:00Z',claim_objective_relation='OBJECTIVE_SUPPORTED')
    data.update(kw);return owner.adp017_apply_epistemic_effect(**data)


def rejected(out):
    return out.get('status')=='REFUSED' or out.get('committed') is False and out.get('decision_state')!='COUPLING_EVALUATED' or out.get('decision_state','').startswith(('DENIED_','DEFERRED_','BLOCKED_'))


def test_inherited_prereg_exact_and_not_replaced():
    raw=(RET/'00_INHERITED_FROZEN_PREREG.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()=='056ebe78a4240a6123abcf4f1b390d90d1cf31c077e9085ddf9d0904dc473700'


def test_actual_two_event_read_ablation_and_replay():
    base=observe();absent=observe('actual_absent_effect');again=observe()
    assert base['result']['later_event_response']['effect_kind']=='DEFLECT'
    assert absent['result']['later_event_response']['effect_kind']=='AMPLIFY'
    assert again['result']['full_replay_digest']==base['result']['full_replay_digest']
    reads=[c for c in base['calls'] if c['function']=='ChainEventLedger.read_effects']
    assert reads and reads[0]['stored'] and reads[0]['returned']
    absent_reads=[c for c in absent['calls'] if c['function']=='ChainEventLedger.read_effects']
    assert absent_reads[0]['returned']==[]
    record('actual_read_ablation',baseline=base,absent=absent)


def test_published_control_actually_has_no_prior_effect():
    b=observe('published_control');record('published_control',actual=b)
    reads=[c for c in b['calls'] if c['function']=='ChainEventLedger.read_effects']
    assert reads[0]['returned']==[], 'Named absent-effect control still reads BUFFER'


def test_later_response_consumes_durable_target_owner_state():
    b=observe();calls=[c for c in b['calls'] if c['function']=='coupline_evaluate']
    record('durable_owner_chain',actual=b)
    assert calls[1]['args'][1]['adp016_memory_refs'] or calls[1]['args'][1]['adp017_claim_refs'], 'Later prestate contains neither committed memory nor epistemic state'


def test_target_owner_validation_precedes_committed_effect():
    b=observe();response=[c for c in b['calls'] if c['function']=='response_rule_apply'][0]['returned']
    record('target_validation',response=response,ledger=b['ledger_entries'])
    assert all(x['validated'] and x['committed'] for x in response['target_owner_effect_requests']), 'Only unvalidated/uncommitted owner requests accompany reported target commit'


@pytest.mark.parametrize('mode',['forged_issuer','unadmitted','fake_event_hash'])
def test_invalid_first_event_is_failure_atomic(mode):
    b=observe(mode);record('atomic_'+mode,actual=b)
    assert b['ledger_entries'][0]==[], 'Invalid first event left a committed CAN008 effect before failure/continued completion'


def test_corrupted_persisted_effect_is_refused_on_actual_read():
    b=observe('corrupt_stored_effect');record('corrupt_persisted_effect',actual=b)
    assert b['result']['terminal']!='CHAIN_COMPLETE', 'Stale entry hash does not block later response/commit'


def test_ledger_payload_cannot_mutate_after_commit():
    l=ChainEventLedger();payload={'effect_kind':'BUFFER'};l.commit('EFFECT',payload,'1998',[])
    before=copy.deepcopy(l.entries);payload['effect_kind']='AMPLIFY';record('payload_alias',before=before,after=l.entries)
    assert l.entries==before,'Ledger stores caller mutable payload by reference'


def test_hash_chain_binds_predecessor():
    l=ChainEventLedger();l.commit('A',{},'1998',[]);l.commit('B',{},'1999',['A'])
    row=l.entries[1];content={k:v for k,v in row.items() if k!='entry_hash'}
    wanted=hashlib.sha256(json.dumps(content,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
    record('hash_chain',entry=row,independently_recomputed=wanted)
    assert row['entry_hash']==wanted,'Entry was hashed before prev_entry_hash was added'


@pytest.mark.parametrize('change',[
 {'admission_state':'REJECTED'},{'issuer_authority_id':'FORGED'},
 {'world_as_of':'1990'},{'actor_scope':'OTHER_ACTOR'},
 {'derived_from_future_partition':True},{'event_kind':'DRAFT_RESPONSE'},
 {'causal_parent_event_ids':('FUTURE',),'reverse_chronology_flag':True}])
def test_basic_occurrence_guards(change):
    out=rule.coupline_evaluate(event(**change),prestate(),rule.build_default_binding(),registry())
    record('basic_'+hashlib.sha256(str(change).encode()).hexdigest()[:10],input=change,output=out)
    assert rejected(out)


def test_duplicate_event_refuses():
    reg=registry();e=event();rule.coupline_evaluate(e,prestate(),rule.build_default_binding(),reg)
    assert rejected(rule.coupline_evaluate(e,prestate(),rule.build_default_binding(),reg))


def test_unregistered_rule_cannot_evaluate_positive():
    out=rule.coupline_evaluate(event(),prestate(),rule.build_default_binding(),CandidateRegistryFixture())
    record('unregistered_rule',output=out);assert rejected(out)


def test_foreign_rule_identity_cannot_evaluate_positive():
    binding=replace(rule.build_default_binding(),rule_id='FORGED_RULE',rule_content_hash='FORGED_HASH')
    out=rule.coupline_evaluate(event(),prestate(),binding,registry())
    record('foreign_rule',binding=vars(binding),output=out);assert rejected(out)


def test_registered_actor_scope_cannot_be_rewritten():
    binding=replace(rule.build_default_binding(),actor_scope='OTHER_ACTOR')
    out=rule.coupline_evaluate(event(actor_scope='OTHER_ACTOR'),prestate(actor_id='OTHER_ACTOR'),binding,registry())
    record('registry_scope',binding=vars(binding),output=out);assert rejected(out)


def test_borrowed_prestate_actor_refuses():
    out=rule.coupline_evaluate(event(),prestate(actor_id='OTHER_ACTOR'),rule.build_default_binding(),registry())
    record('borrowed_actor',output=out);assert rejected(out)


def test_temporal_scope_actually_enforced_without_flag():
    out=rule.coupline_evaluate(event(effective_causal_time='2099-01-01T00:00:00Z'),prestate(),rule.build_default_binding(),registry())
    record('future_scope',output=out);assert rejected(out)


def test_unreceivable_event_does_not_become_positive_response():
    b=rule.build_default_binding();s=prestate();c=rule.coupline_evaluate(event(public_features=()),s,b,registry())
    out=rule.response_rule_apply(c,s,b,'BUFFER');record('unreceivable',coupling=c,response=out)
    assert out.get('decision_state')!='RESPONSE_EFFECTS_PRODUCED'


# §16 text is independently read from the adopted blob. This is an active-path
# omission challenge, not the author's presence-only validate_complete helper.
BINDINGS=[('rule_id', ''),('eligible_event_authority_signatures',()),('actor_scope',''),
 ('receivability_semantics',''),('eligible_conditioning_owner_signatures',()),
 ('conditioning_causal_use_roles',()),('counterpart_scoping',''),('modality_evidence_authorities',()),
 ('uptake_appraisal_semantics',''),('recruitment_semantics',''),('multiplicity_handling',''),
 ('co_determination_closure',''),('prior_response_history_predicates',''),('current_condition_effort_role',''),
 ('effect_kinds',()),('target_validation',''),('pff_current_consequence_projection',''),('valid_empty_behavior',''),
 ('missing_deferred_ambiguous_behavior',''),('quantitative_contract',''),('adp020_binding',''),
 ('atomic_commit_behavior',''),('provenance_replay_requirements','')]
@pytest.mark.parametrize('ordinal,field,value',[(i+1,n,v) for i,(n,v) in enumerate(BINDINGS)])
def test_all_23_binding_omissions_on_active_path(ordinal,field,value):
    b=replace(rule.build_default_binding(),**{field:value});s=prestate()
    c=rule.coupline_evaluate(event(),s,b,registry());r=rule.response_rule_apply(c,s,b,'BUFFER')
    record('binding_%02d'%ordinal,field=field,coupling=c,response=r,helper_validation=b.validate_complete())
    if ordinal in (7,8,14,20,21):
        # No counterpart/modality/effort/numeric/stochastic input is used in this
        # cell. Law says "where applicable"; do not manufacture five defects by
        # demanding a positive implementation of an unused conditional feature.
        record('binding_%02d'%ordinal,field=field,applicability='NOT_USED_IN_THIS_CELL',coupling=c,response=r)
        assert r.get('decision_state') in ('RESPONSE_EFFECTS_PRODUCED','RESPONSE_COUPLING_RULE_MISSING')
        return
    assert c.get('decision_state')!='COUPLING_EVALUATED' or r.get('decision_state')!='RESPONSE_EFFECTS_PRODUCED', 'Active path accepted missing binding '+field


@pytest.mark.parametrize('content',['V2_TRANSCRIPT','RENDERED_DIALOGUE','STRUCTURAL_OBJECT','ANALYST_ANNOTATION','MEMORY_DISTILLATION_PROSE'])
def test_memory_noncausal_source_refusals(content):
    with pytest.raises(owner.OwnerTransitionError):trace(content_state=content)


def test_memory_causal_trace_and_complete_transition_schema():
    b=trace();law=json.loads((RET/'runtime_root/law/ADP016.txt').read_text())
    assert set(law['transition_record']['required_fields'])<=set(b['transition'])
    assert set(law['memory_model']['required_fields'])<=set(b['memory'])
    assert b['memory']['representation_kind']=='CAUSAL_TRACE_MEMORY'
    assert b['first_person_origin_claimable'] is False


def test_memory_rejects_missing_prestate_integrity():
    try:r=trace(parent_state_hash='')
    except owner.OwnerTransitionError:return
    record('memory_empty_prestate',output=r);pytest.fail('Formation committed with empty pre-state hash')


def test_memory_refuses_fake_rule_and_authority():
    try:r=trace(owning_rule_id='FORGED',owning_rule_hash='FORGED',authority_id='FORGED',authority_version='')
    except owner.OwnerTransitionError:return
    record('memory_forged_authority',output=r);pytest.fail('Presence of forged rule strings authorized formation')


def test_memory_transition_identity_binds_prestate():
    a=trace(parent_state_hash='PRE_A');b=trace(parent_state_hash='PRE_B')
    record('memory_transition_collision',a=a,b=b)
    assert a['transition']['memory_transition_id']!=b['transition']['memory_transition_id']


def test_memory_transition_requires_exact_parent():
    m=GeneratedMemoryState(**trace()['memory'])
    try:r=owner.adp016_attempt_transition(m,'DEGRADE')
    except owner.OwnerTransitionError:return
    record('memory_no_parent',output=r);pytest.fail('Transition accepted without parent/prestate verification')


@pytest.mark.parametrize('bad,code',[('parent','PARENT_EVENT_HASH_MISMATCH'),('state','PRE_STATE_HASH_MISMATCH')])
def test_memory_explicit_mismatches_are_typed(bad,code):
    m=GeneratedMemoryState(**trace()['memory'])
    with pytest.raises(owner.OwnerTransitionError) as err:
        owner.adp016_attempt_transition(m,'DEGRADE',parent_event=event(),declared_parent_hash='FORGED' if bad=='parent' else event().event_hash,pre_state_hash='FORGED' if bad=='state' else m.current_state_hash)
    assert err.value.code==code


def test_k3_trace_recall_and_first_person_are_denied():
    m=GeneratedMemoryState(**trace()['memory'])
    with pytest.raises(owner.OwnerTransitionError):owner.adp016_attempt_transition(m,'RECALL',parent_event=event())
    assert owner.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE','CAUSAL_TRACE_MEMORY')['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'


def test_k3_sole_trace_cannot_be_first_person_basis():
    m=GeneratedMemoryState(**trace()['memory'])
    out=owner.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESSIBLE',m)
    record('sole_trace_access',output=out);assert out['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'


@pytest.mark.parametrize('retention,access',[('CONTENT_UNAVAILABLE','INACCESSIBLE'),('RETAINED','INACCESSIBLE')])
def test_k3_dead_basis_denies_without_erasing_stance(retention,access):
    m=replace(GeneratedMemoryState(**trace()['memory']),retention_state=retention,memory_accessibility_state=access)
    out=owner.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESSIBLE',m)
    assert out['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'
    assert out['memory_inaccessibility_auto_erases_stance'] is False


def test_access_unknown_does_not_become_known_denial():
    m=replace(GeneratedMemoryState(**trace()['memory']),memory_accessibility_state='ACCESS_UNKNOWN')
    out=owner.adp017_sole_memory_basis_failclosed('BELIEF','CLAIM_ACCESS_UNKNOWN',m)
    record('access_unknown',output=out);assert out['first_person_permission']=='DEFER_MISSING_AUTHORITY'


def test_epistemic_12_fields_and_all_operations():
    law=json.loads((RET/'runtime_root/law/ADP017.txt').read_text())
    for op in law['epistemic_effect']['stance_operation']:
        out=epistemic(stance_operation=op)
        assert set(law['epistemic_effect']['required_fields'])<=set(out['effect'])


def test_k5_objective_relation_does_not_automatically_edit_private_belief():
    a=epistemic(claim_objective_relation='OBJECTIVE_SUPPORTED');b=epistemic(claim_objective_relation='OBJECTIVE_CONTRADICTED')
    assert a['effect']==b['effect']
    assert a['effect']['stance_kind']=='BELIEF'


def test_knowledge_requires_actual_actor_basis_and_truth():
    assert rejected(epistemic(stance_kind='KNOWLEDGE',actor_facing_basis_refs=()))
    assert rejected(epistemic(stance_kind='KNOWLEDGE',claim_objective_relation='OBJECTIVE_CONTRADICTED'))


def test_forged_actor_basis_is_not_verified_knowledge():
    out=epistemic(stance_kind='KNOWLEDGE',actor_facing_basis_refs=('FORGED_NONADMITTED',),causal_parent_refs=('FORGED_PARENT',),owning_rule_id='FORGED',owning_rule_hash='FORGED')
    record('forged_knowledge',output=out);assert rejected(out)


def test_empty_belief_claim_rule_and_parent_are_not_positive():
    out=epistemic(claim_ref='',causal_parent_refs=(),owning_rule_id='',owning_rule_version='',owning_rule_hash='')
    record('empty_belief',output=out);assert rejected(out)


def test_epistemic_effect_identity_binds_rule_and_parents():
    a=epistemic();b=epistemic(owning_rule_hash='DIFFERENT_RULE',causal_parent_refs=('DIFFERENT_PARENT',))
    record('epistemic_identity_collision',a=a,b=b);assert a['effect']['effect_id']!=b['effect']['effect_id']


def test_no_stance_is_not_nonknowledge_and_trace_cannot_be_exported():
    assert owner.adp017_first_person_check(None,'CLAIM_ACCESSIBLE')['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'
    assert owner.adp017_first_person_check('BELIEF','CLAIM_ACCESS_UNKNOWN')['first_person_permission']=='DEFER_MISSING_AUTHORITY'


def test_production_registry_stays_zero_positive_and_exact():
    import rawlsing_next.v3_psepf_zero_positive_guard as guard
    from types import MappingProxyType
    p=Path(guard.__file__);raw=p.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='e0528d65215cb431196570c38bac4eae94217a1b'
    assert isinstance(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES,MappingProxyType)
    before=dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)
    registry();observe()
    assert dict(guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES)==before=={}
    with pytest.raises(TypeError):guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES['FORGED']='x'


def test_fake_effect_kind_is_refused():
    b=rule.build_default_binding();s=prestate()
    c=rule.coupline_evaluate(event(),s,b,registry())
    assert rule.response_rule_apply(c,s,b,'FORGED_RESPONSE_KIND')['decision_state']=='RESPONSE_COUPLING_RULE_MISSING'


def test_fake_coupling_dictionary_is_not_admitted_causality():
    out=rule.response_rule_apply({'decision_state':'COUPLING_EVALUATED'},prestate(),rule.build_default_binding(),'BUFFER')
    record('fake_coupling',output=out)
    assert out['decision_state']!='RESPONSE_EFFECTS_PRODUCED'


def test_memory_missing_basis_is_typed_owner_refusal():
    try:out=trace(basis_event=None)
    except Exception as e:
        record('missing_basis_type',exception_type=type(e).__name__,message=str(e))
        assert isinstance(e,owner.OwnerTransitionError)
        return
    record('missing_basis_type',output=out);pytest.fail('Missing basis accepted')


def test_memory_integrity_marker_is_enforced():
    m=replace(GeneratedMemoryState(**trace()['memory']),integrity_state='CORRUPT')
    try:out=owner.adp016_attempt_transition(m,'DEGRADE',parent_event=event(),pre_state_hash=m.current_state_hash)
    except owner.OwnerTransitionError as e:
        assert e.code=='INTEGRITY_FAILURE';return
    record('corrupt_memory_state',output=out);pytest.fail('Corrupt memory accepted for commit')


def test_memory_id_collision_does_not_alias_distinct_sources():
    a=trace(memory_id_override='REVIEW_COLLISION',basis_event=event())
    try:b=trace(memory_id_override='REVIEW_COLLISION',basis_event=event(event_id='OTHER_EVENT',event_hash=hashlib.sha256(b'other event').hexdigest()))
    except owner.OwnerTransitionError:return
    record('memory_collision',a=a,b=b)
    assert a['memory']['memory_id']!=b['memory']['memory_id'],'Same memory/state identity accepted for different source events'


def test_empty_rule_version_is_refused():
    with pytest.raises(owner.OwnerTransitionError):trace(owning_rule_version='')


def test_known_inaccessible_event_memory_cannot_permit_first_person():
    out=owner.adp017_first_person_check('BELIEF','CLAIM_ACCESSIBLE','EVENT_REFERENTIAL_MEMORY','INACCESSIBLE')
    record('inaccessible_memory_permission',output=out)
    assert out['first_person_permission']=='DENY_FIRST_PERSON_CLAIM'
