"""R1 expected-refusal regressions; X2 frozen oracle remains byte unchanged."""
from copy import deepcopy
import json, os, sqlite3, subprocess, sys
from pathlib import Path
import pytest
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
HERE=Path(__file__).resolve().parent

def setup(tmp_path):
    initial=m.b1.initialize(m.b1.prehistory())
    b=m.Bridge(tmp_path/'state.sqlite',initial)
    packet,context,policy=m.input_pair(initial)
    witness=m.occurrence_witness(initial,packet,context)
    cap,registry=m.capability_fixture();b.capability_witnesses=registry
    b.witnesses={witness['hash']:witness}
    return b,dict(packet=packet,context=context,policy=policy,witness=witness,cap=cap,registry=registry)

def advance(b,v,**kw):
    b.witnesses[v['witness']['hash']]=v['witness']
    return b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],**kw)

def seal(v):
    v['witness']=m.b1.sealed({k:x for k,x in v['witness'].items() if k!='hash'})
    return v

def snapshot(b):
    return {t:b.store.db.execute('SELECT * FROM '+t+' ORDER BY 1').fetchall()
            for t in ('checkpoint','occurrence','b2_ingress','b2_event_identity','joint_receipt')}

@pytest.mark.parametrize('field,value',[
    ('objective_occurrence','DIFFERENT_OBJECTIVE_EVENT'),('actor','peer'),
    ('time','2026-10-18T10:00:00Z'),('number',2),('world_ref','other-world'),
    ('issuer','OTHER_ISSUER'),('parent_fact_hash','0'*64),
    ('expected_actor_state_hash','0'*64),('context_hash','0'*64),
    ('proposal_hash','0'*64),('candidate_hash','0'*64),
    ('project','other-project'),('participants',['PEER-1']),
    ('observed_interpretations',[]),('other_actions',[]),
    ('world_facts',{'known_thief':'invented'}),('interrupted',False),
    ('outcome','NONOCCURRENCE'),('place','other-place'),('extra_readset',['new'])])
def test_collision_refuses_before_any_write(tmp_path,field,value):
    b,v=setup(tmp_path)
    assert advance(b,v,grant=False)['event_admission']['status']=='ADMITTED_SYNTHETIC_FIXTURE_ONLY'
    before=snapshot(b)
    changed=deepcopy(v);changed['witness'][field]=value;seal(changed)
    r=advance(b,changed,grant=False)
    assert r['reason']=='EVENT_IDENTITY_CONFLICT'
    assert r['event_admission']=='NOT_PERFORMED' and not r['b1_invoked']
    assert snapshot(b)==before
    b.close()

@pytest.mark.parametrize('field',['packet','context','policy'])
def test_complete_readset_reuse_refused(tmp_path,field):
    b,v=setup(tmp_path);advance(b,v,grant=False);before=snapshot(b)
    changed=deepcopy(v);changed[field]['extra_readset']='new'
    # Rehash valid source objects, then bind the newly registered witness.
    hashfield={'packet':'proposal_hash','context':'context_hash','policy':'policy_hash'}[field]
    changed[field]=m.rehash(changed[field],hashfield)
    if field!='policy':changed['witness'][hashfield]=changed[field][hashfield]
    seal(changed)
    r=advance(b,changed,grant=False)
    assert r['status'] in ('DENIED','DEFERRED') and not r['b1_invoked']
    assert snapshot(b)==before;b.close()

@pytest.mark.parametrize('kwargs',[{}, {'grant':False}, {'fault':'after_checkpoint'}])
def test_exact_replay_idempotent_after_success_or_rollback(tmp_path,kwargs):
    b,v=setup(tmp_path);first=advance(b,v,**kwargs);before=snapshot(b)
    second=advance(b,v,**kwargs)
    assert snapshot(b)==before
    assert first['admitted_event']==second['admitted_event']
    assert first['event_admission']==second['event_admission']
    if not kwargs:assert second['status']=='ALREADY_ADMITTED' and not second['b1_invoked']
    b.close()

def test_exact_old_event_after_later_committed_event(tmp_path):
    b,v=setup(tmp_path);advance(b,v)
    state=b.store.state();packet,context,policy=m.input_pair(state,2)
    witness=m.occurrence_witness(state,packet,context,number=2)
    cap,registry=m.capability_fixture(witness['event_id'],witness['time'][:10])
    b.capability_witnesses=registry
    assert advance(b,dict(packet=packet,context=context,policy=policy,witness=witness,cap=cap))['status']=='COMMITTED'
    before=snapshot(b)
    assert advance(b,v)['status']=='ALREADY_ADMITTED'
    assert snapshot(b)==before;b.close()

def test_legacy_unmapped_occurrence_fails_closed(tmp_path):
    b,v=setup(tmp_path);b.store.admit_fixture(m.b1.episode());before=snapshot(b)
    assert advance(b,v)['reason']=='EVENT_IDENTITY_UNBOUND_LEGACY'
    assert snapshot(b)==before;b.close()

@pytest.mark.parametrize('table',['occurrence','b2_ingress','b2_event_identity'])
def test_storage_fault_rolls_back_entire_admission(tmp_path,table):
    b,v=setup(tmp_path);before=snapshot(b)
    b.store.db.execute('CREATE TRIGGER fail BEFORE INSERT ON '+table+" BEGIN SELECT RAISE(ABORT,'injected'); END")
    assert advance(b,v)['reason']=='SYNTHETIC_INGRESS_STORAGE_FAILURE'
    assert snapshot(b)==before and not b.store.db.in_transaction
    b.close()

def start(tmp_path,v,name):
    path=tmp_path/(name+'.json');path.write_text(json.dumps(v))
    proc=subprocess.Popen([sys.executable,str(HERE/'worker.py'),str(path),str(tmp_path/'state.sqlite')],
        stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    assert proc.stdout.readline().strip()=='READY'
    return proc

def finish(proc):
    stdout,stderr=proc.communicate(timeout=20)
    assert proc.returncode==0,stderr
    return json.loads(stdout)

@pytest.mark.parametrize('mode',['exact','payload','issuer','clock','actor','readset','utterance','distinct'])
def test_simultaneous_fresh_process_writers(tmp_path,mode):
    b,v=setup(tmp_path);initial=b.store.state();b.close();v['kwargs']={'grant':False}
    changed=deepcopy(v)
    if mode=='distinct':changed['witness']['event_id']='event-other'
    elif mode=='payload':changed['witness']['objective_occurrence']='CONFLICT'
    elif mode=='issuer':changed['witness']['issuer']='OTHER_ISSUER'
    elif mode=='clock':changed['witness']['time']='2026-10-18T10:00:00Z'
    elif mode=='actor':changed['witness']['actor']='other'
    elif mode=='readset':changed['witness']['extra_readset']='other'
    elif mode=='utterance':changed['witness']['observed_interpretations']=[]
    seal(changed)
    # All connections exist before release; actual independent OS processes.
    procs=[start(tmp_path,x,str(i)) for i,x in enumerate([v,changed,v,changed])]
    for p in procs:p.stdin.write('GO\n');p.stdin.flush()
    results=[finish(p) for p in procs]
    b=m.Bridge(tmp_path/'state.sqlite');rows=b.store.db.execute('SELECT body FROM occurrence').fetchall()
    assert len(rows)==(2 if mode=='distinct' else 1)
    assert len({json.loads(r[0])['event_id'] for r in rows})==len(rows)
    assert b.store.state()==initial
    assert b.store.db.execute('SELECT count(*) FROM b2_event_identity').fetchone()[0]==len(rows)
    assert b.store.db.execute('SELECT count(*) FROM b2_ingress').fetchone()[0]==len(rows)
    if mode in ('payload','actor','readset'):
        assert sum(r.get('reason')=='EVENT_IDENTITY_CONFLICT' for r in results)==2
    if mode=='exact':assert all(isinstance(r['event_admission'],dict) for r in results)
    if os.environ.get('R1_EVIDENCE'):
        Path(os.environ['R1_EVIDENCE'],mode+'.json').write_text(json.dumps(dict(
            process_ids=[p.pid for p in procs],results=results,
            occurrence_rows=[r[0] for r in rows],tables=snapshot(b)),indent=2)+'\n')
    b.close()

def test_fresh_process_exact_replay_after_committed_response(tmp_path):
    b,v=setup(tmp_path);advance(b,v);before=snapshot(b);b.close()
    p=start(tmp_path,v,'replay');p.stdin.write('GO\n');p.stdin.flush()
    assert finish(p)['status']=='ALREADY_ADMITTED'
    b=m.Bridge(tmp_path/'state.sqlite');assert snapshot(b)==before;b.close()

def test_prestate_checked_under_actual_sqlite_lock(tmp_path):
    b,v=setup(tmp_path);v['lock_probe']=True;p=start(tmp_path,v,'stale')
    b.store.db.execute('BEGIN IMMEDIATE')
    changed=deepcopy(b.store.state());changed['middle'].append({'separate_owner_change':True})
    b.store.db.execute('UPDATE checkpoint SET body=? WHERE id=1',(m.b1.canonical(changed),))
    p.stdin.write('GO\n');p.stdin.flush()
    assert p.stdout.readline().strip()=='LOCK_REQUESTED'
    # A pipe command is released while the writer lock is held. The worker must
    # read the committed prestate after acquisition, never its old cached state.
    b.store.db.execute('COMMIT')
    r=finish(p)
    assert r['reason']=='WITNESS_BINDING_OR_STALE_STATE'
    assert b.store.state()==changed
    assert b.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]==0
    b.close()

def test_simultaneous_successful_replay_commits_one_response(tmp_path):
    b,v=setup(tmp_path);b.close()
    procs=[start(tmp_path,v,'commit'+str(i)) for i in range(4)]
    for p in procs:p.stdin.write('GO\n');p.stdin.flush()
    results=[finish(p) for p in procs]
    b=m.Bridge(tmp_path/'state.sqlite')
    assert sum(r['status']=='COMMITTED' for r in results)==1
    assert len(b.store.state()['responses'])==1
    assert len(b.store.state()['middle'])==1
    assert b.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]==1
    assert b.store.db.execute('SELECT count(*) FROM joint_receipt').fetchone()[0]==1
    if os.environ.get('R1_EVIDENCE'):
        Path(os.environ['R1_EVIDENCE'],'concurrent_commit.json').write_text(json.dumps(dict(
            process_ids=[p.pid for p in procs],results=results,tables=snapshot(b)),indent=2)+'\n')
    b.close()

@pytest.mark.parametrize('table',['occurrence','b2_ingress'])
def test_replay_detects_missing_ledger_row(tmp_path,table):
    b,v=setup(tmp_path);advance(b,v);b.store.db.execute('DELETE FROM '+table)
    before=snapshot(b)
    assert advance(b,v)['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE'
    assert snapshot(b)==before;b.close()

def test_terminated_writer_rolls_back_uncommitted_admission(tmp_path):
    b,v=setup(tmp_path);before=snapshot(b);v['admission_pause']=True
    p=start(tmp_path,v,'crash');p.stdin.write('GO\n');p.stdin.flush()
    assert p.stdout.readline().strip()=='UNCOMMITTED_OCCURRENCE'
    # Another connection cannot see the occurrence before the registrar commit.
    assert snapshot(b)==before
    p.kill();stdout,stderr=p.communicate(timeout=10)
    assert p.returncode!=0
    b.close();b=m.Bridge(tmp_path/'state.sqlite')
    assert snapshot(b)==before
    # Re-register the independent downstream capability witness after reopening.
    b.capability_witnesses=v['registry']
    # A genuinely new attempt remains admissible after process death.
    assert advance(b,v)['status']=='COMMITTED';b.close()
