"""Prospective X3 assertions against unchanged pinned B3. REDs remain literal."""
import os, sys, json
from pathlib import Path
from copy import deepcopy
from dataclasses import replace, asdict
import pytest

B3 = Path(os.environ['X3_B3_ROOT'])
sys.path.insert(0, str(B3))
from integration import Integration, digest, seal, Refusal
from fixture_authority import FixtureAuthority
from developmental_loop import World, permission_for
from f2_adapter import inputs, run_case
from sources import m2
import source_guard, target_owner

OUT = Path(os.environ['X3_EVIDENCE'])
OUT.mkdir(parents=True, exist_ok=True)
CASES = json.loads((B3/'.runtime/f2/cases.json').read_text())['cases']

def frame_at(t=7):
    w = World()
    for i in range(1,t+1): w.tick(i)
    return w.frame()

def receipt(name, e, before, result):
    (OUT/(name+'.json')).write_text(json.dumps(dict(before=before, after=e.snapshot(), result=result,sql_trace=getattr(e,'_x3_trace',[])), indent=2)+'\n')

def engine(tmp_path, f):
    a=FixtureAuthority(); a.register_observed(f)
    e=Integration(tmp_path/'court.sqlite',a);e._x3_trace=[]
    e.db.set_trace_callback(lambda sql:e._x3_trace.append(sql) if sql.lstrip().split()[0].upper() in ('INSERT','UPDATE','DELETE','BEGIN','COMMIT','ROLLBACK') else None)
    return e,a

def rehash(x):
    x['hash']=digest({k:v for k,v in x.items() if k!='hash'})

def test_missing_origin_refusal_is_atomic(tmp_path):
    f=frame_at();f['origin_event_id']='NEVER_ADMITTED_PARENT'
    e,a=engine(tmp_path,f);before=e.snapshot()
    try:
        try:r=e.run(f)
        except Exception as exc:r={'exception':type(exc).__name__,'code':str(exc)}
        receipt('missing_origin',e,before,r)
        assert e.snapshot()==before, 'refused missing origin left durable admission/source rows'
        assert r['status']=='REFUSED'
    finally:e.close()

def test_duplicate_physical_check_cannot_form_practice(tmp_path):
    f=frame_at(); f['evidence']=[x for x in f['evidence'] if x['id']!='check:2']
    x=deepcopy(next(x for x in f['evidence'] if x['id']=='check:7'))
    x['id']='same-check-second-id';rehash(x);f['evidence'].append(x)
    # Both records now describe the same clock, actor, observer, object and result.
    f['readset']=[x['id'] for x in f['evidence'] if x['actor']=='child']+[s['witness'] for s in f['utterances']]
    e,a=engine(tmp_path,f);before=e.snapshot();p=permission_for([],f)
    try:
        r=e.run(f,owner_permission=p,registered_permissions=(p,));receipt('duplicate_activity',e,before,r)
        assert not r['owner_effect_committed'], 'two IDs of one witnessed activity counted as repetition'
    finally:e.close()

@pytest.mark.parametrize('change',['missing_observer','wrong_result','future','one_check','unregistered_permission','stale_permission'])
def test_practice_negative_controls(tmp_path,change):
    f=frame_at()
    if change=='one_check':f['evidence']=[x for x in f['evidence'] if x['id']!='check:2'];f['readset'].remove('check:2')
    for x in f['evidence']:
        if x['id']=='check:7':
            if change=='missing_observer':x.pop('observer')
            if change=='wrong_result':x['result']='JOURNAL_ONLY'
            if change=='future':x['time']=99
            rehash(x)
    e,a=engine(tmp_path,f);before=e.snapshot();p=permission_for([],f)
    if change=='stale_permission':p='old-unbound-permission'
    try:
        r=e.run(f,owner_permission=p,registered_permissions=() if change=='unregistered_permission' else (p,))
        receipt(change,e,before,r)
        assert not r['owner_effect_committed'] and e.middle()==[]
    finally:e.close()

@pytest.mark.parametrize('kind',['speech','history','affect'])
def test_cold_renewed_attestation_is_blocked(tmp_path,kind):
    f=frame_at()
    if kind=='affect':f['evidence'].append(seal(dict(id='affect-source',actor='child',owner='child',act='BIKE_CARE',time=2,source='WORLD',object='bike-child',note='distress')))
    e,a=engine(tmp_path,f);r=e.run(f);assert r['status']=='ELIGIBLE_NONCAUSAL';e.close()
    e=Integration(tmp_path/'court.sqlite',a);before=e.snapshot();bad=deepcopy(f);bad['as_of']=8
    if kind=='speech':bad['utterances'][0]['claim']='replacement words'
    else:
        x=next(x for x in bad['evidence'] if x['id']==('affect-source' if kind=='affect' else 'check:2'))
        x['note']='opposite historical source';rehash(x)
    # Renew every source binding the fixture registrar can provide.
    for z in bad['exposures']:
        z['source_hash']=next(x['hash'] for x in bad['evidence'] if x['id']==z['speech_witness'])
    a.register_observed(bad)
    try:
        r=e.run(bad);receipt('cold_'+kind,e,before,r)
        assert r['code']=='SOURCE_PREIMAGE_IDENTITY_COLLISION' and e.snapshot()==before
    finally:e.close()

def test_guard_rejects_missing_previously_used_sources():
    s=m2.seed_scene();old=source_guard.preimages(s)
    removed=replace(s,speech=(),speech_actions=(),exposures=())
    # The helper's claimed immutable continuation should not drop its readset.
    with pytest.raises(m2.Refusal):source_guard.check(old,removed)

@pytest.mark.parametrize('attack',['unheard','never_spoke','future_action','objective_claim','event_collision'])
def test_event_and_hearing_negatives(tmp_path,attack):
    f=inputs(CASES[6]);e,a=engine(tmp_path,f)
    if attack=='event_collision':assert e.run(f)['status']=='ELIGIBLE_NONCAUSAL'
    before=e.snapshot();bad=deepcopy(f)
    if attack=='unheard':bad['exposures']=[]
    if attack=='never_spoke':
        x=next(x for x in bad['evidence'] if x['id']==bad['utterances'][0]['witness']);x['act']='BIKE_CARE';rehash(x)
    if attack=='future_action':
        x=next(x for x in bad['evidence'] if x['id']==bad['utterances'][0]['witness']);x['time']=1000;rehash(x)
    if attack=='objective_claim':bad['utterances'][0]['epistemic']='OBJECTIVE_FACT'
    if attack=='event_collision':bad['event']['content']['object']='replacement';bad['event']['content_hash']=digest(bad['event']['content'])
    a.register_observed(bad)
    try:
        r=e.run(bad);receipt(attack,e,before,r)
        assert r['status']=='REFUSED' and e.snapshot()==before
    finally:e.close()

def test_poison_all_analyst_metadata_and_no_effect(monkeypatch):
    original=deepcopy(CASES[6]);bad=deepcopy(original)
    bad.update(id='X3-UNSEEN-ID',expected={'status':'POISON'},group='POISON')
    bad['actor'].update(history_label='POISON',SES='POISON',sect='POISON',age=-999)
    def forbidden(*a,**k):raise AssertionError('durable M2 append must stay quarantined')
    monkeypatch.setattr(m2,'append_test_only',forbidden);monkeypatch.setattr(m2,'fixture_grant',forbidden)
    a,b=run_case(original),run_case(bad)
    for r in (a,b):r.pop('case_id',None)
    assert a==b
    assert not b['owner_effect_committed'] and b['CAN011_transition']['status']=='VALID_EMPTY'
    assert b['CAN008_response']['selected_belief'] is None and b['selected_affect'] is None

def test_private_affect_does_not_select_practice(tmp_path):
    results=[]
    for i,affect in enumerate(([],['rage'],['joy'])):
        f=frame_at();f['actor']['epistemic']['affect']=affect
        p=tmp_path/str(i);p.mkdir();e,a=engine(p,f);permission=permission_for([],f)
        r=e.run(f,owner_permission=permission,registered_permissions=(permission,));results.append((e.middle(),r['CAN008_response']));e.close()
    assert results[0]==results[1]==results[2]

def test_before_and_after_loss_practice_requires_pre_loss_act(tmp_path):
    f=frame_at()
    x=next(x for x in f['evidence'] if x['id']=='check:2');x['time']=6;rehash(x)
    e,a=engine(tmp_path,f);before=e.snapshot();p=permission_for([],f)
    try:
        r=e.run(f,owner_permission=p,registered_permissions=(p,));receipt('no_pre_loss_act',e,before,r)
        assert not r['owner_effect_committed'], 'both checks occurred after loss; pre-loss activity absent'
    finally:e.close()

@pytest.mark.parametrize('attack',['missing_parent','future_event','future_capability','history_collision'])
def test_late_refusal_does_not_partially_admit(tmp_path,attack):
    f=frame_at();e,a=engine(tmp_path,f)
    if attack=='history_collision':
        assert e.run(f)['status']=='ELIGIBLE_NONCAUSAL'
        # A newly admitted event plus a changed derived M2 history ID should still be atomic.
        f['as_of']=8
    before=e.snapshot();bad=deepcopy(f)
    if attack=='missing_parent':bad['origin_event_id']='unadmitted'
    if attack=='future_event':bad['event']['time']=99
    if attack=='future_capability':bad['capability']['witnesses'][0]['time']=99
    if attack=='history_collision':
        bad['event']['id']='new-current-event';bad['event']['time']=8
        # Raw source payloads stay identical; this targets derived event/history collision.
        bad['utterances'][0]['event_ref']='new-current-event'
    a.register_observed(bad)
    try:
        try:r=e.run(bad)
        except Exception as exc:r={'exception':type(exc).__name__,'code':str(exc)}
        receipt('atomic_'+attack,e,before,r)
        assert e.snapshot()==before, 'failed/refused operation changed persisted source/occurrence tables'
    finally:e.close()

def test_integrated_source_removal_cannot_bypass_guard(tmp_path):
    f=frame_at();e,a=engine(tmp_path,f);assert e.run(f)['status']=='ELIGIBLE_NONCAUSAL'
    e.close();e=Integration(tmp_path/'court.sqlite',a);before=e.snapshot()
    bad=deepcopy(f);bad['utterances']=[];bad['exposures']=[];bad['readset']=[x for x in bad['readset'] if x.startswith('check:') or x in ('cap','choice','loss_observed')]
    a.register_observed(bad)
    try:
        r=e.run(bad);receipt('integrated_source_removal',e,before,r)
        assert r['code']=='SOURCE_PREIMAGE_IDENTITY_COLLISION' and e.snapshot()==before
    finally:e.close()

def test_privileged_second_connection_between_guard_and_commit_is_detected_only_on_reentry(tmp_path,monkeypatch):
    import sqlite3
    f=frame_at();e,a=engine(tmp_path,f);before=e.snapshot();original=source_guard.check;fired=[]
    def race(old,scene):
        result=original(old,scene)
        if not fired:
            # Ignore B3's advisory file lock: this is an explicitly privileged SQL adversary.
            other=sqlite3.connect(e.path)
            key='check:2';bad=deepcopy(next(x for x in f['evidence'] if x['id']==key));bad['note']='SQL replacement after guard'
            other.execute('INSERT OR REPLACE INTO b3_preimage VALUES (?,?)',(key,m2.canonical(bad)));other.commit();other.close();fired.append(True)
        return result
    monkeypatch.setattr(source_guard,'check',race)
    try:
        r=e.run(f);receipt('privileged_guard_to_commit_race',e,before,r)
        assert r['status']=='ELIGIBLE_NONCAUSAL' and fired
        e.close();e=Integration(tmp_path/'court.sqlite',a);polluted=e.snapshot()
        r=e.run(f);receipt('privileged_guard_to_commit_cold_detection',e,polluted,r)
        assert r['code']=='SOURCE_PREIMAGE_IDENTITY_COLLISION' and e.snapshot()==polluted
    finally:e.close()

@pytest.mark.parametrize('kind',['missing_origin','future_event'])
def test_refusal_rows_persist_on_real_cold_connection(tmp_path,kind):
    f=frame_at()
    if kind=='missing_origin':f['origin_event_id']='never-existed'
    else:f['event']['time']=99
    e,a=engine(tmp_path,f);before=e.snapshot()
    try:r=e.run(f)
    except Exception as exc:r={'exception':type(exc).__name__,'code':str(exc)}
    e.close();e=Integration(tmp_path/'court.sqlite',a)
    try:
        receipt('cold_partial_'+kind,e,before,r)
        assert e.snapshot()==before, 'partial writes survived closing and reopening SQLite'
    finally:e.close()
