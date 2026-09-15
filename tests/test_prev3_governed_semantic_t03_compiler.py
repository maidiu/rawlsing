from __future__ import annotations
import pytest
from rawlsing_next.pre553_empirical_objects import AuthorityRef,ExactRef,semantic_hash
from rawlsing_next._prev3_structural_batch_base import CandidateKind,CandidateOutcome
from rawlsing_next.prev3_governed_semantic_t03_compiler import (
    CarrierKind,CurrentnessBlockedError,CurrentnessState,EpistemicClass,
    EquivalenceAuthority,EquivalenceDecision,FixtureSchemaError,
    GovernedSemanticCapitalRecord,SemanticAuthorityState,SemanticJurisdiction,
    FINAL_RELEASE_HOLD,adapt_fqra_fixture,adapt_negative_block_fixture,
    adapt_qsmv2_fixture,adapt_response_semantics_fixture,adapt_typed_relation_fixture,
    compile_governed_semantic_batch,compile_governed_semantic_capital,
)

def h(x): return semantic_hash({'fixture':x})
def r(kind,obj): return ExactRef(kind,obj,h(f'{kind}:{obj}'))
def a(name='AUTH',version='R1'): return AuthorityRef(name,version,h(f'{name}:{version}'))
def eq(decision=EquivalenceDecision.AUTHORIZED,tag='eq'):
    return EquivalenceAuthority(r('REL',tag),decision,r('REL_DECISION',f'{tag}:{decision.value}'),a('EQAUTH'))
def rec(*, carrier=CarrierKind.FQRA,state=SemanticAuthorityState.POSITIVE,current=CurrentnessState.CURRENT,core=None,jur=SemanticJurisdiction.SOURCE_SEMANTIC,epi=EpistemicClass.MANUAL_ADJUDICATED,tag='x',equivs=()):
    return GovernedSemanticCapitalRecord(
        carrier_kind=carrier,carrier_locator_ref=r('CARRIER',carrier.value),carrier_row_ref=r('ROW',tag),source_family_ref=r('FAMILY','fam'),source_release_ref=r('RELEASE','rel'),source_question_ref=r('QUESTION',f'q-{tag}'),implementation_ref_or_exact_na=r('IMPL',f'i-{tag}'),authority_ref=a(f'AUTH-{tag}'),authority_snapshot_ref=r('AUTH_SNAPSHOT',tag),epistemic_class=epi,jurisdiction=jur,authority_state=state,currentness_state=current,currentness_ref=None if current is CurrentnessState.MISSING else r('CURRENTNESS',f'{tag}:{current.value}'),noncurrent_disposition_ref=r('NONCURRENT',tag) if current is CurrentnessState.HISTORICAL_NONCURRENT else None,response_category_semantics_ref=r('RESPONSE',tag),routing_applicability_ref=r('ROUTING',tag),structural_use_ceiling_ref=r('CEILING',tag),semantic_core_ref=core or r('CORE',tag),semantic_schema_ref=r('SCHEMA','s1'),negative_ceiling_ref=r('NEG_CEILING','n1'),type_class_ceiling_ref=r('TYPE_CEILING','t1'),evidence_admission_refs=(r('EVIDENCE',tag),),provenance_refs=(r('PROVENANCE',tag),),equivalence_authorities=tuple(equivs),candidate_kind=CandidateKind.STRUCTURAL_POSITION)
def fixture_material(x):
    return {'carrier_locator_ref':x.carrier_locator_ref.as_dict(),'carrier_row_ref':x.carrier_row_ref.as_dict(),'source_family_ref':x.source_family_ref.as_dict(),'source_release_ref':x.source_release_ref.as_dict(),'source_question_ref':x.source_question_ref.as_dict(),'implementation_ref_or_exact_na':x.implementation_ref_or_exact_na.as_dict(),'authority_ref':x.authority_ref.as_dict(),'authority_snapshot_ref':x.authority_snapshot_ref.as_dict(),'epistemic_class':x.epistemic_class.value,'jurisdiction':x.jurisdiction.value,'authority_state':x.authority_state.value,'currentness_state':x.currentness_state.value,'currentness_ref':None if x.currentness_ref is None else x.currentness_ref.as_dict(),'noncurrent_disposition_ref':None if x.noncurrent_disposition_ref is None else x.noncurrent_disposition_ref.as_dict(),'response_category_semantics_ref':x.response_category_semantics_ref.as_dict(),'routing_applicability_ref':x.routing_applicability_ref.as_dict(),'structural_use_ceiling_ref':x.structural_use_ceiling_ref.as_dict(),'semantic_core_ref':x.semantic_core_ref.as_dict(),'semantic_schema_ref':x.semantic_schema_ref.as_dict(),'negative_ceiling_ref':x.negative_ceiling_ref.as_dict(),'type_class_ceiling_ref':x.type_class_ceiling_ref.as_dict(),'evidence_admission_refs':[z.as_dict() for z in x.evidence_admission_refs],'provenance_refs':[z.as_dict() for z in x.provenance_refs],'equivalence_authorities':[{'relation_ref':z.relation_ref.as_dict(),'decision':z.decision.value,'decision_ref':z.decision_ref.as_dict(),'authority_ref':z.authority_ref.as_dict()} for z in x.equivalence_authorities],'candidate_kind':x.candidate_kind.value}

@pytest.mark.parametrize('adapter,kind',[(adapt_fqra_fixture,CarrierKind.FQRA),(adapt_qsmv2_fixture,CarrierKind.QSMV2),(adapt_negative_block_fixture,CarrierKind.NEGATIVE_BLOCK),(adapt_response_semantics_fixture,CarrierKind.RESPONSE_SEMANTICS),(adapt_typed_relation_fixture,CarrierKind.TYPED_RELATION)])
def test_five_bounded_carrier_adapters_preserve_exact_material(adapter,kind):
    original=rec(carrier=kind,tag=kind.value); adapted=adapter(fixture_material(original))
    assert adapted.carrier_kind is kind and adapted.authority_ref == original.authority_ref and adapted.semantic_core_ref == original.semantic_core_ref
    assert adapted.response_category_semantics_ref == original.response_category_semantics_ref and adapted.routing_applicability_ref == original.routing_applicability_ref and adapted.structural_use_ceiling_ref == original.structural_use_ceiling_ref

@pytest.mark.parametrize('state,outcome',[(SemanticAuthorityState.POSITIVE,CandidateOutcome.CANDIDATE_ONLY),(SemanticAuthorityState.NEGATIVE_FORBIDDEN,CandidateOutcome.CANDIDATE_ONLY),(SemanticAuthorityState.BLOCKED,CandidateOutcome.BLOCKED),(SemanticAuthorityState.REVIEW_REQUIRED,CandidateOutcome.BLOCKED)])
def test_authority_states_conserved_without_laundering(state,outcome):
    out=compile_governed_semantic_capital(rec(state=state,tag=state.value)); assert out.authority_state is state and out.status.outcome is outcome
    assert (out.blocker is not None) is (outcome is CandidateOutcome.BLOCKED)
def test_superseded_is_historical_noncurrent_not_current():
    out=compile_governed_semantic_capital(rec(state=SemanticAuthorityState.SUPERSEDED,current=CurrentnessState.HISTORICAL_NONCURRENT,tag='old'))
    assert out.authority_state is SemanticAuthorityState.SUPERSEDED and out.currentness_state is CurrentnessState.HISTORICAL_NONCURRENT and out.status.outcome is CandidateOutcome.HISTORICAL_NONCURRENT and out.status.noncurrent_disposition_refs
@pytest.mark.parametrize('jur',list(SemanticJurisdiction))
def test_jurisdiction_conserved(jur): assert compile_governed_semantic_capital(rec(jur=jur,tag=jur.value)).jurisdiction is jur
@pytest.mark.parametrize('epi',list(EpistemicClass))
def test_epistemic_class_conserved(epi): assert compile_governed_semantic_capital(rec(epi=epi,tag=epi.value)).epistemic_class is epi
def test_exact_provenance_authority_response_routing_and_ceiling_retained():
    x=rec(tag='prov'); out=compile_governed_semantic_capital(x); pkeys={z.key for z in out.semantic_candidate.provenance_refs}
    assert x.provenance_refs[0].key in pkeys and x.carrier_locator_ref.key in pkeys and x.carrier_row_ref.key in pkeys and x.authority_snapshot_ref.key in pkeys
    assert x.source_family_ref.key in pkeys and x.source_release_ref.key in pkeys and x.source_question_ref.key in pkeys and x.implementation_ref_or_exact_na.key in pkeys
    assert out.authority_ref == x.authority_ref and out.response_category_semantics_ref == x.response_category_semantics_ref and out.routing_applicability_ref == x.routing_applicability_ref and out.structural_use_ceiling_ref == x.structural_use_ceiling_ref
def test_only_positive_equivalence_enters_admission_but_all_decisions_remain_provenance():
    allow=eq(EquivalenceDecision.AUTHORIZED,'allow'); deny=eq(EquivalenceDecision.DENIED,'deny'); unknown=eq(EquivalenceDecision.UNKNOWN_AUTHORITY,'unknown'); out=compile_governed_semantic_capital(rec(tag='eqs',equivs=(allow,deny,unknown)))
    ekeys={z.key for z in out.semantic_candidate.evidence_admission_refs}; pkeys={z.key for z in out.semantic_candidate.provenance_refs}
    assert allow.relation_ref.key in ekeys and deny.relation_ref.key not in ekeys and unknown.relation_ref.key not in ekeys
    for item in (allow,deny,unknown): assert item.relation_ref.key in pkeys and item.decision_ref.key in pkeys
    assert out.positive_equivalence_refs == (allow.relation_ref,)
def test_exact_equal_core_dedup_retains_all_candidate_evidence_and_provenance():
    core=r('CORE','shared'); one=rec(core=core,tag='one'); two=rec(core=core,tag='two'); batch=compile_governed_semantic_batch((one,two)); assert batch.final_release_hold == FINAL_RELEASE_HOLD and len(batch.reduction.aggregates)==1
    ag=batch.reduction.aggregates[0]; ekeys={z.key for z in ag.evidence_admission_refs}; pkeys={z.key for z in ag.provenance_refs}
    assert len(ag.candidate_refs)==2 and one.evidence_admission_refs[0].key in ekeys and two.evidence_admission_refs[0].key in ekeys and one.provenance_refs[0].key in pkeys and two.provenance_refs[0].key in pkeys
def test_deterministic_replay_and_order_independent_batch_reduction():
    core=r('CORE','shared-replay'); one=rec(core=core,tag='r1'); two=rec(core=core,tag='r2'); a1=compile_governed_semantic_capital(one); a2=compile_governed_semantic_capital(one)
    assert a1.ref==a2.ref and a1.semantic_candidate.ref==a2.semantic_candidate.ref and a1.source_local_intake.ref==a2.source_local_intake.ref
    b1=compile_governed_semantic_batch((one,two)); b2=compile_governed_semantic_batch((two,one)); assert [x.ref for x in b1.reduction.aggregates]==[x.ref for x in b2.reduction.aggregates]
@pytest.mark.parametrize('cur',[CurrentnessState.MISSING,CurrentnessState.AMBIGUOUS])
def test_missing_or_ambiguous_currentness_fails_closed(cur):
    x=rec(current=cur,tag=cur.value)
    if cur is CurrentnessState.AMBIGUOUS: object.__setattr__(x,'currentness_ref',r('CURRENTNESS','ambiguous'))
    with pytest.raises(CurrentnessBlockedError): compile_governed_semantic_capital(x)
def test_missing_currentness_ref_fails_closed_even_when_state_says_current():
    x=rec(tag='no-ref'); object.__setattr__(x,'currentness_ref',None)
    with pytest.raises(CurrentnessBlockedError): compile_governed_semantic_capital(x)
def test_superseded_current_contradiction_fails_closed():
    with pytest.raises(CurrentnessBlockedError): compile_governed_semantic_capital(rec(state=SemanticAuthorityState.SUPERSEDED,current=CurrentnessState.CURRENT,tag='bad'))
def test_historical_without_noncurrent_disposition_fails_closed():
    x=rec(current=CurrentnessState.HISTORICAL_NONCURRENT,tag='missing-disp'); object.__setattr__(x,'noncurrent_disposition_ref',None)
    with pytest.raises(CurrentnessBlockedError): compile_governed_semantic_capital(x)
def test_fixture_adapter_rejects_free_text_or_inferred_semantics_fields():
    m=fixture_material(rec(tag='strict')); m['question_text']='infer me'; m.pop('semantic_core_ref')
    with pytest.raises(FixtureSchemaError) as exc: adapt_fqra_fixture(m)
    assert 'semantic_core_ref' in str(exc.value) and 'question_text' in str(exc.value)
def test_negative_forbidden_remains_negative_state_and_does_not_become_empirical_negative():
    x=rec(state=SemanticAuthorityState.NEGATIVE_FORBIDDEN,tag='neg'); out=compile_governed_semantic_capital(x)
    assert out.authority_state is SemanticAuthorityState.NEGATIVE_FORBIDDEN and out.semantic_candidate.negative_ceiling_ref == x.negative_ceiling_ref and out.status.outcome is CandidateOutcome.CANDIDATE_ONLY
def test_compiler_never_emits_current_t03_outcome():
    out=compile_governed_semantic_capital(rec(tag='not-selector')); assert out.status.outcome is CandidateOutcome.CANDIDATE_ONLY and out.status.current_selection_refs and out.status.outcome is not CandidateOutcome.CURRENT
