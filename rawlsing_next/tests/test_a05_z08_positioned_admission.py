import hashlib
import pytest
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.source_backed_positioned_subject_possibility import (
    EPISTEMIC_CEILING, MODEL_ALGORITHM_ID, ConditionerBinding, PossibilitySliceEvidence,
    PositionedSubjectPossibilityError, PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery, SpecificityWalkbackStep,
    evaluate_positioned_subject_possibility,
)

def h(v): return hashlib.sha256(v.encode()).hexdigest()
def ref(kind, tag): return ExactRef(kind, f'urn:test:a05:{kind.lower()}:{tag}', h(f'{kind}:{tag}'))
def auth(tag): return AuthorityRef(f'A05-{tag}', '1.0.0', h(f'authority:{tag}'))
U=ref('EmpiricalUniverse@1.0.0','u'); R=ref('C11LogicalRelease','r'); T=ref('TARGET','t')

def binding(i): return ConditionerBinding(i,ref('GENERATED_SUBJECT_FACT',i),ref('EMPIRICAL_COORDINATE',i),auth(f'cmp-{i}'),U,R,'2026-R1')
def query(purpose='EMPIRICAL_POSSIBILITY_ONLY'):
    return PositionedSubjectPossibilityQuery('q-a05',ref('GENERATED_SUBJECT','s'),T,U,R,(binding('country'),binding('education'),binding('age')),{'kind':'JOINT_DISTRIBUTION'},purpose=purpose)
def evidence(ids,state='SUPPORTED',tag='e',geometry=None,n=100):
    if geometry is None and state=='SUPPORTED': geometry={'modes':{'A':60,'B':40}}
    return PossibilitySliceEvidence(ref('EmpiricalFact@1.0.0',tag),U,R,T,tuple(ids),state,geometry,n,'GOVERNED_UPSTREAM_STATE',(ref('PROVENANCE',tag),),(auth(f'evidence-{tag}'),))
def step(): return SpecificityWalkbackStep('drop-age',('country','education'),auth('proxy-drop-age'),U,R,'authority-declared specificity loss')
def rule(step_obj=None,**overrides):
    steps=() if step_obj is None else (step_obj,); positive=() if step_obj is None else (step_obj.proxy_authority_ref,)
    return PositionedSubjectPossibilityModelRule(auth('model'),auth('walkback'),(U,),steps,positive,**overrides)

def test_a05_actor_or_prediction_purpose_is_rejected_and_rule_is_inert():
    with pytest.raises(PositionedSubjectPossibilityError,match='actor/prediction jurisdiction forbidden'): query('ACTOR_BELIEF')
    material=rule().material()
    assert material['actor_inference_allowed'] is False
    assert material['proxy_can_satisfy_exact_request'] is False
    assert material['cross_source_proxy']=='FORBIDDEN_IN_V1'
    assert 'PROXY != EXACT FACT != ACTOR BELIEF' in EPISTEMIC_CEILING

def test_a05_smoothing_nearest_neighbor_or_extrapolation_rule_is_not_admissible():
    assert MODEL_ALGORITHM_ID=='EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION'
    for forbidden in ('NEAREST_NEIGHBOR','SMOOTHED_KERNEL','EXTRAPOLATED_MODEL'):
        with pytest.raises(PositionedSubjectPossibilityError,match='unrecognized or smoothing/interpolation model rule'): rule(algorithm_id=forbidden)

def test_a05_proxy_remains_separate_from_exact_lane_and_actor_belief():
    q=query(); ex=evidence(q.conditioner_ids,'UNDERPOWERED','exact-under',geometry=None,n=8); broad=evidence(('country','education'),tag='broad'); s=step()
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(s),evidence=(ex,broad))
    assert out.result_state=='EXACT_UNRESOLVED_PROXY_AVAILABLE'
    assert out.exact_disposition=='UNRESOLVED'
    assert out.exact_reason=='EXACT_UNDERPOWERED'
    assert out.proxy is not None
    proxy=out.proxy.material()
    assert proxy['projection_kind']=='EXPLICIT_LOWER_SPECIFICITY_PROXY'
    assert proxy['is_exact_fact'] is False
    assert proxy['is_actor_belief'] is False
    assert proxy['specificity_loss']['dropped_conditioner_ids']==['age']
    assert out.material()['exact_lane']['disposition']=='UNRESOLVED'
