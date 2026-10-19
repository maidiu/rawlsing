"""Independent preregistered falsifiers. Candidate and frozen tests stay unchanged."""
from copy import deepcopy
from unittest.mock import patch
import pytest
import recursive_court as c

@pytest.fixture(scope='module')
def runs():
    return {w:c.run_trajectory(w) for w in c.r1_world.WORK_OUTCOMES}

def source(runs,work='ROUTINE',identity='fresh'):
    f=deepcopy(runs[work]['source_preimages']['episode-theft']);f['id']=identity
    return f

def snapshot(ledger):return deepcopy((ledger.entries,ledger._sources))

@pytest.mark.parametrize('slots',[('hall_drawer','garage_shelf'),('garage_shelf','hall_drawer')])
def test_N01_conflict_atomicity_retry(runs,slots):
    l=c.CanonLedger();a=source(runs,identity='a');b=source(runs,identity='b')
    e=l.admit(a,c.propose_realization(a,slots[0]));l.append_unrelated(clock=24)
    before=snapshot(l)
    with pytest.raises(ValueError,match='CANON_OBJECT_LOCATION_CONFLICT'):l.admit(b,c.propose_realization(b,slots[1]))
    assert snapshot(l)==before and l.verify()
    retry=l.admit(b,c.propose_realization(b,slots[0],'alternate'))
    assert retry['id']=='canon:2' and l.later_consume(e['id'])['target_location']==slots[0]

@pytest.mark.parametrize('order',[('ROUTINE','RAISE_WITH_OVERTIME'),('RAISE_WITH_OVERTIME','ROUTINE')])
def test_N02_individually_consistent_presence_conflict(runs,order):
    l=c.CanonLedger();a=source(runs,order[0],'a');b=source(runs,order[1],'b')
    l.admit(a,c.propose_realization(a));l.append_unrelated(clock=24);before=snapshot(l)
    with pytest.raises(ValueError,match='CANON_ACTOR_FACT_CONFLICT'):l.admit(b,c.propose_realization(b))
    assert snapshot(l)==before and 'b' not in l._sources

@pytest.mark.parametrize('optional',[True,False])
@pytest.mark.parametrize('defect',['missing','duplicate','kind','care','absent_extra'])
def test_N03_typed_producer_inconsistency_atomic_retry(runs,optional,defect):
    work='RAISE_WITH_OVERTIME' if defect=='absent_extra' else 'ROUTINE'
    f=source(runs,work);good=deepcopy(f)
    if not optional:
        f['resolved'].pop('father_response');good['resolved'].pop('father_response')
    ev=f['effect']['selected_events']
    attention=deepcopy(next(e for e in runs['ROUTINE']['immediate']['selected_events'] if e['id']=='actual-shared-attention'))
    if defect=='missing':ev[:]=[e for e in ev if e['id']!='actual-shared-attention']
    elif defect=='duplicate':ev.append(attention)
    elif defect=='kind':next(e for e in ev if e['id']==attention['id'])['kind']='practice'
    elif defect=='care':next(e for e in ev if e['id']==attention['id'])['magnets']['offers']=['attention']
    else:ev.append(attention)
    l=c.CanonLedger()
    with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):l.admit(f,c.propose_realization(f))
    assert snapshot(l)==([],{});l.admit(good,c.propose_realization(good));assert l.verify()

@pytest.mark.parametrize('work',['ROUTINE','RAISE_WITH_OVERTIME'])
def test_N04_optional_material_record_absent(runs,work):
    f=source(runs,work);f['resolved'].pop('father_response')
    l=c.CanonLedger();l.admit(f,c.propose_realization(f));assert l.verify()

@pytest.mark.parametrize('work,minutes,accept',[('ROUTINE',9,False),('ROUTINE',10,True),('RAISE_WITH_OVERTIME',9,True),('RAISE_WITH_OVERTIME',10,False)])
def test_N04_existing_material_boundary(runs,work,minutes,accept):
    f=source(runs,work);f['resolved']['father_response']['available_minutes']=minutes
    l=c.CanonLedger()
    if accept:l.admit(f,c.propose_realization(f));assert l.verify()
    else:
        with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):l.admit(f,c.propose_realization(f))
        assert snapshot(l)==([],{})

@pytest.mark.parametrize('value',[0,1,'false',None])
def test_N04_presence_is_boolean(runs,value):
    f=source(runs);f['resolved']['father_present']=value;l=c.CanonLedger()
    with pytest.raises(ValueError,match='SOURCE_ENCOUNTER_MISMATCH'):l.admit(f,c.propose_realization(f))
    assert snapshot(l)==([],{})

def test_N05_source_identity_and_post_admission_tamper(runs):
    f=source(runs);l=c.CanonLedger();e=l.admit(f,c.propose_realization(f));before=snapshot(l)
    replacement=deepcopy(f);replacement['proposal']['confidence']='OTHER'
    with pytest.raises(ValueError,match='SOURCE_ID_REUSE'):l.admit(replacement,c.propose_realization(replacement))
    assert snapshot(l)==before
    l._sources[f['id']]['resolved']['child_at_home']=False
    for operation in (l.verify,lambda:l.later_consume(e['id']),lambda:l.append_unrelated()):
        with pytest.raises(ValueError,match='SOURCE_PREIMAGE_REWRITE'):operation()
    assert l.entries==before[0]

def test_N06_alternative_wording_and_copy_isolation(runs):
    l=c.CanonLedger();a=source(runs,identity='a');b=source(runs,identity='b')
    first=l.admit(a,c.propose_realization(a));second=l.admit(b,c.propose_realization(b,variant='alternate'))
    assert first['facts']==second['facts'] and first['text']!=second['text']
    a['effect']['before'].clear();b['world'].clear();second['facts']['lock_location']='elsewhere'
    assert l.verify() and l.entries[0]==first
    assert l.later_consume(second['id'])['target_location']=='hall_drawer'

def test_N07_actual_consumer_call_and_feedback_parent():
    original=c.CanonLedger.later_consume;calls=[]
    def observed(ledger,identity,*args,**kwargs):
        result=original(ledger,identity,*args,**kwargs)
        calls.append((deepcopy(ledger.entries),identity,deepcopy(result)))
        return result
    with patch.object(c.CanonLedger,'later_consume',observed):
        a=c.run_trajectory(location='hall_drawer');b=c.run_trajectory(location='garage_shelf',variant='alternate')
    assert len(calls)==2
    for r,(entries,identity,result) in zip((a,b),calls):
        assert r['later']==result==r['delayed_feedback']['actual_activity_source']
        stored=next(e for e in entries if e['id']==identity)
        assert result['target_location']==stored['facts']['lock_location']
        assert result['canon_read']['hash']==stored['hash']
        assert r['ticks'][3]['before']==r['delayed_feedback']['after']
    assert a['later']['target_location']!=b['later']['target_location']
    assert a['immediate']==b['immediate'] and a['final_state']==b['final_state']

def test_N08_neutral_append_and_material_convergence(runs):
    state=c.initial_state();cfg,order=c.config_and_order();c.apply_existing_events(state,[],cfg,0)
    neutral=c.apply_existing_events(state,[],cfg,23);assert neutral['before']==neutral['after']
    f=source(runs,'RAISE_WITH_OVERTIME');f['effect']=neutral;f['resolved'].pop('father_response')
    l=c.CanonLedger();e=l.admit(f,c.propose_realization(f));assert e['prestate_hash']==e['poststate_hash']
    tick=c.advance(state,cfg,order,30,'fresh-ordinary')
    assert tick['numeric_changes'] and any(tick['before'][k]==tick['after'][k] for k in tick['before'])
    assert runs['HOURS_CUT']['final_state']==runs['ROUTINE']['final_state']
    assert runs['ROUTINE']['final_state']!=runs['RAISE_WITH_OVERTIME']['final_state']

def test_N09_separate_worlds_cross_clock_and_access_boundaries(runs):
    f=source(runs);l=c.CanonLedger();first=l.admit(f,c.propose_realization(f));g=source(runs,identity='later')
    cand=c.propose_realization(g,'garage_shelf');cand['clock']=26;second=l.admit(g,cand)
    assert l.later_consume(first['id'])['target_location']=='hall_drawer'
    assert l.later_consume(second['id'])['target_location']=='garage_shelf'
    other=c.CanonLedger();other.admit(g,c.propose_realization(g,'garage_shelf'));assert other.verify()
    for operation,code in [(lambda:l.later_consume(first['id'],actor='father'),'HISTORY_ACCESS_DENIED'),(lambda:l.later_consume(second['id'],clock=25),'FUTURE_CANON_READ')]:
        with pytest.raises(ValueError,match=code):operation()
    future=source(runs,identity='future');candidate=c.propose_realization(future);candidate['clock']=22
    with pytest.raises(ValueError,match='FUTURE_SOURCE'):l.admit(future,candidate)

def test_N10_consistent_untrusted_fabrication_still_requires_producer_authority(runs):
    # Observational boundary control, NOT an expectation that local repair authenticates inputs.
    f=source(runs);f['resolved']['father_present']=False
    f['resolved']['father_response']['available_minutes']=3
    f['effect']['selected_events']=[e for e in f['effect']['selected_events'] if e['id']!='actual-shared-attention']
    # Retain the original care-including numerical snapshot: ledger cannot certify causality.
    assert f['effect']['after']==runs['ROUTINE']['immediate']['after']
    l=c.CanonLedger();l.admit(f,c.propose_realization(f));assert l.verify()

def test_N11_verify_rechecks_cross_entry_consistency(runs):
    l=c.CanonLedger();a=source(runs,identity='a');b=source(runs,identity='b')
    l.admit(a,c.propose_realization(a));l.admit(b,c.propose_realization(b))
    forged=l._entries[1];forged['facts']['lock_location']='garage_shelf'
    forged['text']=c.render_text(forged['facts'],'plain')
    forged['hash']=c.digest({k:v for k,v in forged.items() if k!='hash'})
    with pytest.raises(ValueError,match='CANON_OBJECT_LOCATION_CONFLICT'):l.verify()

@pytest.mark.parametrize('defect',['events_none','offers_none','response_empty'])
def test_N13_malformed_input_never_partial_admits(runs,defect):
    f=source(runs)
    if defect=='events_none':f['effect']['selected_events']=None
    elif defect=='offers_none':f['effect']['selected_events'][1]['magnets']['offers']=None
    else:f['resolved']['father_response']={}
    l=c.CanonLedger()
    # A diagnostic of exception typing, not a new well-typed fixture safety claim.
    with pytest.raises((ValueError,TypeError,KeyError)):l.admit(f,c.propose_realization(f))
    assert snapshot(l)==([],{})
