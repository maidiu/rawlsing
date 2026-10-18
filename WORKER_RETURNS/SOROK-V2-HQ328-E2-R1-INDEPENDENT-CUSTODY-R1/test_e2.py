"""Fresh independent hostile court; imports only the exact candidate and E2 helpers."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json, os, select, sqlite3, subprocess, sys
import pytest
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
from probe_e2 import tables

HERE=Path(__file__).resolve().parent

def save(name, **data):
    out=Path(os.environ['E2_EVIDENCE']);out.mkdir(parents=True,exist_ok=True)
    (out/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')

def setup(path):
    b=m.Bridge(path/'state.sqlite',m.b1.initialize(m.b1.prehistory()))
    packet,context,policy=m.input_pair(b.store.state())
    witness=m.occurrence_witness(b.store.state(),packet,context)
    cap,registry=m.capability_fixture()
    v=dict(packet=packet,context=context,policy=policy,witness=witness,cap=cap,registry=registry)
    return b,v

def reseal(v):
    v['witness']=m.b1.sealed({k:x for k,x in v['witness'].items() if k!='hash'})
    return v

def advance(b,v,*,register=True,**kwargs):
    if register:b.witnesses[v['witness']['hash']]=deepcopy(v['witness'])
    b.capability_witnesses=deepcopy(v['registry'])
    return b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],**kwargs)

@pytest.mark.parametrize('field,value',[
    ('issuer','MODEL_SELF_ISSUED'),('source','FORGED_SOURCE'),('actor','peer'),
    ('time','2026-10-19T10:00:00Z'),('place','other-place'),
    ('objective_occurrence','E2_CONFLICT'),('parent_fact_hash','f'*64),
    ('readset',{'unseen':'other'}),('observed_interpretations',[]),
    ('registration_policy','NEW_POLICY'),('world_ref','world:other'),
    ('other_actions',[]),('number',100),('project','other-project')])
def test_exact_identity_full_content_refusal_after_response_rollback(tmp_path,field,value):
    b,v=setup(tmp_path)
    assert advance(b,v,grant=False)['status']=='TRANSACTION_ABORTED_ROLLBACK'
    before=tables(b.store.db)
    changed=deepcopy(v);changed['witness'][field]=value;reseal(changed)
    r=advance(b,changed,grant=False)
    after=tables(b.store.db)
    save('collision_'+field,inputs=changed,before=before,after=after,receipt=r)
    assert r['reason']=='EVENT_IDENTITY_CONFLICT' and r['event_admission']=='NOT_PERFORMED'
    assert not r['b1_invoked'] and after==before and not b.store.db.in_transaction
    b.close()

@pytest.mark.parametrize('part',['packet','context','policy'])
def test_full_readset_byte_binding(tmp_path,part):
    b,v=setup(tmp_path);advance(b,v,grant=False);before=tables(b.store.db)
    changed=deepcopy(v);changed[part]['e2_new_readset']=['new-parent']
    key={'packet':'proposal_hash','context':'context_hash','policy':'policy_hash'}[part]
    changed[part]=m.rehash(changed[part],key)
    if part!='policy':changed['witness'][key]=changed[part][key]
    reseal(changed)
    r=advance(b,changed,grant=False)
    save('readset_'+part,receipt=r,before=before,after=tables(b.store.db))
    assert r['event_admission']=='NOT_PERFORMED' and tables(b.store.db)==before
    b.close()

@pytest.mark.parametrize('state',['unregistered','revoked','body_substitution'])
def test_registered_provenance_is_required_even_for_replay(tmp_path,state):
    b,v=setup(tmp_path)
    if state!='unregistered':advance(b,v,grant=False)
    before=tables(b.store.db)
    if state=='body_substitution':
        b.witnesses[v['witness']['hash']]={'hash':v['witness']['hash'],'forged':True}
    else:b.witnesses.clear()
    r=advance(b,v,register=False)
    assert r['reason']=='INDEPENDENT_OCCURRENCE_WITNESS_REQUIRED' and tables(b.store.db)==before
    save('registrar_'+state,receipt=r,tables=before)
    b.close()

@pytest.mark.parametrize('kwargs',[{'grant':False},{'fault':'after_checkpoint'},{}])
def test_idempotence_before_and_after_checkpoint_change(tmp_path,kwargs):
    b,v=setup(tmp_path);first=advance(b,v,**kwargs);before=tables(b.store.db)
    second=advance(b,v,**kwargs)
    assert tables(b.store.db)==before
    assert first['admitted_event']==second['admitted_event'] and len(before['occurrence'])==1
    if not kwargs:
        assert second['status']=='ALREADY_ADMITTED' and not second['b1_invoked']
        assert len(b.store.state()['middle'])==len(b.store.state()['responses'])==1
    else:
        assert b.store.state()['responses']==[] and b.store.state()['middle']==[]
        assert before['joint_receipt']==[]
    save('replay_'+('success' if not kwargs else next(iter(kwargs))),first=first,second=second,tables=before)
    b.close()

def test_distinct_legal_ids_and_no_checkpoint_damage(tmp_path):
    b,v=setup(tmp_path);initial=b.store.state();receipts=[]
    for i in range(6):
        other=deepcopy(v);other['witness']['event_id']='E2-ID-'+str(i);reseal(other)
        other['cap'],other['registry']=m.capability_fixture(other['witness']['event_id'])
        receipts.append(advance(b,other,grant=False))
    assert all(isinstance(r['event_admission'],dict) for r in receipts)
    assert len(tables(b.store.db)['occurrence'])==6 and b.store.state()==initial
    save('distinct_ids',receipts=receipts,tables=tables(b.store.db));b.close()

@pytest.mark.parametrize('defect',['occurrence','b2_ingress','b2_event_identity','event_ref','ingress_ref','binding'])
def test_missing_or_partial_ledger_fails_without_new_admission(tmp_path,defect):
    b,v=setup(tmp_path);advance(b,v);sql=b.store.db
    if defect in ('occurrence','b2_ingress','b2_event_identity'):sql.execute('DELETE FROM '+defect)
    else:sql.execute('UPDATE b2_event_identity SET '+defect+'=?',('missing',))
    before=tables(sql);b.close()
    b=m.Bridge(tmp_path/'state.sqlite');r=advance(b,v)
    assert r['event_admission']=='NOT_PERFORMED' and not r['b1_invoked']
    assert tables(b.store.db)==before
    save('partial_'+defect,receipt=r,tables=before);b.close()

def test_legacy_before_wrapper_fails_closed(tmp_path):
    b,v=setup(tmp_path);b.store.admit_fixture(m.b1.episode(label='E2_DIRECT_OLD_B1'))
    before=tables(b.store.db);r=advance(b,v)
    assert r['reason']=='EVENT_IDENTITY_UNBOUND_LEGACY' and tables(b.store.db)==before
    save('legacy_before',receipt=r,tables=before);b.close()

@pytest.mark.parametrize('committed',[False,True])
def test_direct_b1_after_wrapper_limit_is_measured(tmp_path,committed):
    """Boundary characterization, not an assertion of global ledger security."""
    b,v=setup(tmp_path);advance(b,v,grant=committed)
    b.store.admit_fixture(m.b1.episode(label='E2_DIRECT_BYPASS_AFTER_MAPPING'))
    before=tables(b.store.db);r=advance(b,v,grant=False)
    assert len(before['occurrence'])==2
    assert tables(b.store.db)==before
    # Existing mapping does not scan for independently inserted competing B1 rows.
    assert isinstance(r['event_admission'],dict)
    assert r['status']==('ALREADY_ADMITTED' if committed else 'TRANSACTION_ABORTED_ROLLBACK')
    save('legacy_after_'+str(committed),receipt=r,tables=before,grade='OUTSIDE_B2_INGRESS_BYPASS_REMAINS')
    b.close()

@pytest.mark.parametrize('committed',[False,True])
def test_legacy_after_mapping_must_fail_closed_at_b2_reentry(tmp_path,committed):
    """Strict commission gate: both insertion orders, without requiring B1 changes.

    B1 can bypass the wrapper, as disclosed. On subsequent B2 reentry the
    ambiguous ledger must be detected instead of issuing an admitted receipt.
    This is a B2 pre-existing-state integrity check, not a B1 writer lockdown.
    """
    b,v=setup(tmp_path);advance(b,v,grant=committed)
    b.store.admit_fixture(m.b1.episode(label='E2_CONFLICTING_LEGACY_OCCURRENCE'))
    before=tables(b.store.db)
    r=advance(b,v,grant=False)
    save('strict_legacy_after_'+str(committed),receipt=r,before=before,after=tables(b.store.db),
         required='DENIED with NOT_PERFORMED on ambiguous same-ID ledger at B2 reentry')
    assert tables(b.store.db)==before
    b.close()
    assert r['event_admission']=='NOT_PERFORMED', 'B2 reentry certifies mapped occurrence despite conflicting legacy row'
    assert r['status']=='DENIED' and not r['b1_invoked']

def start(tmp_path,v,index):
    path=tmp_path/('input_'+str(index)+'.json');path.write_text(json.dumps(v))
    p=subprocess.Popen([sys.executable,str(HERE/'process_e2.py'),str(path),str(tmp_path/'state.sqlite')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    assert select.select([p.stdout],[],[],10)[0], 'writer did not become ready'
    ready=json.loads(p.stdout.readline());assert ready['ready'] and ready['isolation_level'] is None
    return p

def release(p):p.stdin.write('GO\n');p.stdin.flush()

def finish(p):
    stdout,stderr=p.communicate(timeout=30)
    assert p.returncode==0,stderr
    return json.loads(stdout)

@pytest.mark.parametrize('terrain',['same','conflicting','distinct','commit'])
def test_independent_simultaneous_processes(tmp_path,terrain):
    b,v=setup(tmp_path);initial=b.store.state();b.close();values=[]
    for i in range(6):
        other=deepcopy(v);other['kwargs']={} if terrain=='commit' else {'grant':False}
        if terrain=='conflicting':other['witness']['objective_occurrence']='E2-MATERIAL-'+str(i%3)
        if terrain=='distinct':
            other['witness']['event_id']='E2-EVENT-'+str(i)
            other['cap'],other['registry']=m.capability_fixture(other['witness']['event_id'])
        reseal(other);values.append(other)
    ps=[start(tmp_path,v,i) for i,v in enumerate(values)]
    for p in ps:release(p)
    results=[finish(p) for p in ps]
    b=m.Bridge(tmp_path/'state.sqlite');snapshot=tables(b.store.db)
    expected=6 if terrain=='distinct' else 1
    assert len({p.pid for p in ps})==6
    assert all(len(snapshot[t])==expected for t in ('occurrence','b2_ingress','b2_event_identity'))
    if terrain=='conflicting':assert sum(r['receipt'].get('reason')=='EVENT_IDENTITY_CONFLICT' for r in results)==4
    if terrain=='commit':
        assert sum(r['receipt']['status']=='COMMITTED' for r in results)==1
        assert len(b.store.state()['responses'])==len(b.store.state()['middle'])==len(snapshot['joint_receipt'])==1
    else:assert b.store.state()==initial and snapshot['joint_receipt']==[]
    assert b.store.db.execute('PRAGMA integrity_check').fetchone()==('ok',)
    save('processes_'+terrain,process_ids=[p.pid for p in ps],inputs=values,results=results,tables=snapshot)
    b.close()

@pytest.mark.parametrize('boundary',['occurrence','ingress','identity'])
def test_sigkill_uncommitted_rows_are_atomically_absent(tmp_path,boundary):
    b,v=setup(tmp_path);before=tables(b.store.db);v['pause']=boundary
    p=start(tmp_path,v,'killed');release(p)
    assert select.select([p.stdout],[],[],10)[0]
    paused=json.loads(p.stdout.readline())
    assert paused['in_transaction'] and len(paused['local']['occurrence'])==1
    if boundary in ('ingress','identity'):assert len(paused['local']['b2_ingress'])==1
    if boundary=='identity':assert len(paused['local']['b2_event_identity'])==1
    assert tables(b.store.db)==before
    p.kill();out,err=p.communicate(timeout=10);assert p.returncode==-9
    b.close();b=m.Bridge(tmp_path/'state.sqlite')
    recovered=tables(b.store.db);assert recovered==before
    assert b.store.db.execute('PRAGMA integrity_check').fetchone()==('ok',)
    receipt=advance(b,v);assert receipt['status']=='COMMITTED'
    save('sigkill_'+boundary,process_id=p.pid,returncode=p.returncode,paused=paused,external_before=before,recovered=recovered,retry=receipt,final=tables(b.store.db))
    b.close()

def test_checkpoint_read_is_after_lock_acquisition(tmp_path):
    b,v=setup(tmp_path);v['observe_lock']=True;p=start(tmp_path,v,'lock')
    b.store.db.execute('BEGIN IMMEDIATE')
    before=tables(b.store.db);state=b.store.state();state['e2_owner_checkpoint']='advanced'
    b.store.db.execute('UPDATE checkpoint SET body=? WHERE id=1',(m.b1.canonical(state),))
    release(p)
    assert select.select([p.stdout],[],[],10)[0]
    assert p.stdout.readline().strip()=='BEGIN_REQUESTED'
    assert not select.select([p.stdout],[],[],0.2)[0], 'writer passed the held lock'
    b.store.db.execute('COMMIT');r=finish(p)
    assert r['receipt']['reason']=='WITNESS_BINDING_OR_STALE_STATE'
    assert tables(b.store.db)['occurrence']==[] and b.store.state()==state
    save('checkpoint_lock',before=before,committed_checkpoint=state,result=r)
    b.close()

def test_cold_process_replay_and_later_event_persistence(tmp_path):
    b,v=setup(tmp_path);assert advance(b,v)['status']=='COMMITTED'
    state=b.store.state();packet,context,policy=m.input_pair(state,2)
    witness=m.occurrence_witness(state,packet,context,number=2)
    cap,registry=m.capability_fixture(witness['event_id'],witness['time'][:10])
    later=dict(packet=packet,context=context,policy=policy,witness=witness,cap=cap,registry=registry)
    assert advance(b,later)['status']=='COMMITTED'
    before=tables(b.store.db);b.close()
    p=start(tmp_path,v,'cold');release(p);r=finish(p)
    assert r['receipt']['status']=='ALREADY_ADMITTED' and not r['receipt']['b1_invoked']
    b=m.Bridge(tmp_path/'state.sqlite');assert tables(b.store.db)==before
    assert b.store.state()['responses'][-1]['practical_activity']==['joint_check:caretaker']
    save('cold_after_later',result=r,tables=before);b.close()
