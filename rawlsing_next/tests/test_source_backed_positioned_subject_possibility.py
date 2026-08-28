import hashlib
import pytest
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding, PossibilitySliceEvidence, PositionedSubjectPossibilityError,
    PositionedSubjectPossibilityModelRule, PositionedSubjectPossibilityQuery,
    SpecificityWalkbackStep, evaluate_positioned_subject_possibility,
    verify_positioned_subject_possibility_replay,
)

def h(x): return hashlib.sha256(x.encode()).hexdigest()
def ref(kind, tag): return ExactRef(kind, f'urn:test:z08:{kind.lower()}:{tag}', h(f'{kind}:{tag}'))
def auth(tag): return AuthorityRef(f'Z08-{tag}', '1.0.0', h(f'auth:{tag}'))

U=ref('EmpiricalUniverse@1.0.0','u'); U2=ref('EmpiricalUniverse@1.0.0','u2')
R=ref('C11LogicalRelease','r'); R2=ref('C11LogicalRelease','r2'); T=ref('TARGET','t')

def binding(i):
    return ConditionerBinding(i, ref('GENERATED_SUBJECT_FACT',i), ref('EMPIRICAL_COORDINATE',i), auth(f'cmp-{i}'), U, R, '2026-R1')

def query():
    return PositionedSubjectPossibilityQuery('q1', ref('GENERATED_SUBJECT','s'), T, U, R, (binding('country'),binding('education'),binding('age')), {'kind':'JOINT_DISTRIBUTION'})

def evidence(ids, state='SUPPORTED', tag='e', *, universe=U, release=R, geometry=None, n=100):
    return PossibilitySliceEvidence(ref('EmpiricalFact@1.0.0',tag), universe, release, T, tuple(ids), state,
        {'modes':{'A':60,'B':40}} if geometry is None and state=='SUPPORTED' else geometry,
        n, 'GOVERNED_UPSTREAM_STATE', (ref('PROVENANCE',tag),), (auth(f'evidence-{tag}'),))

def rule(*steps):
    return PositionedSubjectPossibilityModelRule(auth('model'),auth('walkback'),(U,),tuple(steps),tuple(s.proxy_authority_ref for s in steps))

def step(tag, ids, *, universe=U, release=R):
    return SpecificityWalkbackStep(tag,tuple(ids),auth(f'proxy-{tag}'),universe,release,f'authorized loss {tag}')

def test_exact_supported_positioned_subject():
    q=query(); ex=evidence(q.conditioner_ids,tag='exact')
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(),evidence=(ex,))
    assert out.result_state=='EXACT_SUPPORTED'
    assert out.exact_disposition=='SUPPORTED'
    assert out.proxy is None
    assert out.exact_evidence_ref==ex.evidence_ref

def test_exact_underpowered_remains_unresolved_and_proxy_is_explicit():
    q=query(); ex=evidence(q.conditioner_ids,'UNDERPOWERED','exact-under',geometry=None,n=8)
    broad=evidence(('country','education'),tag='broad')
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(step('drop-age',('country','education'))),evidence=(ex,broad))
    assert out.result_state=='EXACT_UNRESOLVED_PROXY_AVAILABLE'
    assert out.exact_disposition=='UNRESOLVED'
    assert out.exact_reason=='EXACT_UNDERPOWERED'
    assert out.proxy is not None and out.proxy.evidence_ref==broad.evidence_ref
    assert out.proxy.specificity_loss.dropped_conditioner_ids==('age',)
    assert out.proxy.material()['is_exact_fact'] is False
    assert out.proxy.material()['is_actor_belief'] is False

def test_absent_exact_stratum_walks_authorized_ladder_and_replays_path():
    q=query(); mid=evidence(('country','education'),'UNDERPOWERED','mid',geometry=None,n=9); broad=evidence(('country',),tag='country-only')
    r=rule(step('drop-age',('country','education')),step('drop-age-education',('country',)))
    out=evaluate_positioned_subject_possibility(query=q,rule=r,evidence=(mid,broad))
    assert out.exact_reason=='EXACT_POSITIONED_STRATUM_ABSENT'
    assert [a.state for a in out.fallback_path]==['PROXY_EVIDENCE_UNDERPOWERED','AUTHORIZED_PROXY_SELECTED']
    assert out.proxy.specificity_loss.dropped_conditioner_ids==('age','education')
    replay=verify_positioned_subject_possibility_replay(out,query=q,rule=r,evidence=(broad,mid))
    assert replay.result_hash==out.result_hash
    assert replay.replay_identity==out.replay_identity

def test_no_admissible_surrogate_is_unresolved():
    q=query(); r=rule(step('drop-age',('country','education')),step('drop-age-education',('country',)))
    out=evaluate_positioned_subject_possibility(query=q,rule=r,evidence=())
    assert out.result_state=='UNRESOLVED'
    assert out.exact_disposition=='UNRESOLVED'
    assert out.proxy is None
    assert len(out.fallback_path)==2

def test_mixed_source_proxy_fails_closed():
    q=query(); wrong=step('wrong-source',('country','education'),universe=U2)
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(wrong),evidence=())
    assert out.result_state=='FAIL_CLOSED'
    assert out.proxy is None
    assert out.fallback_path[-1].state=='FAIL_CLOSED_UNAUTHORIZED_PROXY_SOURCE'

def test_release_crossing_proxy_fails_closed():
    q=query(); wrong=step('wrong-release',('country','education'),release=R2)
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(wrong),evidence=())
    assert out.result_state=='FAIL_CLOSED'
    assert out.proxy is None

def test_walkback_must_strictly_lose_specificity_and_cannot_reorder_back_up():
    q=query(); bad=rule(step('drop-age',('country','education')),step('widen-back',('country','education','age')))
    with pytest.raises(PositionedSubjectPossibilityError):
        evaluate_positioned_subject_possibility(query=q,rule=bad,evidence=())

def test_proxy_specificity_is_not_hidden_by_result_identity():
    q=query(); a=evidence(('country','education'),tag='a'); b=evidence(('country',),tag='b')
    out1=evaluate_positioned_subject_possibility(query=q,rule=rule(step('a',('country','education'))),evidence=(a,))
    out2=evaluate_positioned_subject_possibility(query=q,rule=rule(step('b',('country',))),evidence=(b,))
    assert out1.result_hash != out2.result_hash
    assert out1.proxy.specificity_loss.loss_count==1
    assert out2.proxy.specificity_loss.loss_count==2

def test_valid_empty_remains_exact_typed_state_and_is_not_broadened():
    q=query(); ex=evidence(q.conditioner_ids,'VALID_EMPTY','empty',geometry=None,n=0); broad=evidence(('country',),tag='broad')
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(step('drop',('country',))),evidence=(ex,broad))
    assert out.result_state=='VALID_EMPTY'
    assert out.exact_disposition=='VALID_EMPTY'
    assert out.proxy is None

def test_noncomparable_exact_state_blocks_proxy_walkback():
    q=query(); ex=evidence(q.conditioner_ids,'NONCOMPARABLE','nc',geometry=None,n=None); broad=evidence(('country',),tag='broad')
    out=evaluate_positioned_subject_possibility(query=q,rule=rule(step('drop',('country',))),evidence=(ex,broad))
    assert out.result_state=='NONCOMPARABLE'
    assert out.proxy is None

def test_conditioner_binding_cannot_cross_exact_query_source():
    bad=ConditionerBinding('country',ref('GENERATED_SUBJECT_FACT','x'),ref('EMPIRICAL_COORDINATE','x'),auth('cmp-x'),U2,R,'2026-R1')
    with pytest.raises(PositionedSubjectPossibilityError):
        PositionedSubjectPossibilityQuery('q',ref('SUBJECT','s'),T,U,R,(bad,),{'kind':'JOINT'})

def test_unlisted_proxy_authority_is_rejected():
    s=step('drop-age',('country','education'))
    with pytest.raises(PositionedSubjectPossibilityError):
        PositionedSubjectPossibilityModelRule(auth('model'),auth('walkback'),(U,),(s,),())

def test_irrelevant_unconsumed_evidence_does_not_change_replay_identity():
    q=query(); broad=evidence(('country','education'),tag='broad'); irrelevant=evidence((),tag='irrelevant')
    r=rule(step('drop-age',('country','education')))
    first=evaluate_positioned_subject_possibility(query=q,rule=r,evidence=(broad,))
    second=evaluate_positioned_subject_possibility(query=q,rule=r,evidence=(irrelevant,broad))
    assert first.result_hash==second.result_hash
    assert first.replay_identity==second.replay_identity
