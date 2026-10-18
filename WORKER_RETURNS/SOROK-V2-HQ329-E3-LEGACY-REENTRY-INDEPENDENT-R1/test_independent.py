"""Independent E3 controls: objective ledger custody, held locks and cold reentry."""
import os,sys,json,subprocess,select,time,hashlib
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import pytest
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
HERE=Path(__file__).resolve().parent

def snapshot(b):
 names=[r[0] for r in b.store.db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
 return {n:b.store.db.execute('SELECT * FROM "'+n+'" ORDER BY 1').fetchall() for n in names}
def save(name,**data):
 Path(os.environ['E3_EVIDENCE'],name+'.json').write_text(json.dumps(data,indent=2)+'\n')
def make(path):
 b=m.Bridge(path/'state.sqlite',m.b1.initialize(m.b1.prehistory()))
 p,c,s=m.input_pair(b.store.state());w=m.occurrence_witness(b.store.state(),p,c);cap,reg=m.capability_fixture()
 return b,dict(packet=p,context=c,policy=s,witness=w,cap=cap,registry=reg,grant=False)
def advance(b,v):
 b.witnesses={v['witness']['hash']:deepcopy(v['witness'])};b.capability_witnesses=v['registry']
 return b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],grant=v['grant'])
def denied(r):
 assert r['status']=='DENIED' and r['event_admission']=='NOT_PERFORMED' and not r['b1_invoked']
def seal(v):v['witness']=m.b1.sealed({k:x for k,x in v['witness'].items() if k!='hash'})
def start(path,v,i):
 source=path/('input'+str(i)+'.json');source.write_text(json.dumps(v))
 p=subprocess.Popen([sys.executable,str(HERE/'worker.py'),str(source),str(path/'state.sqlite')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 assert select.select([p.stdout],[],[],15)[0];ready=json.loads(p.stdout.readline());assert ready['ready'] and ready['isolation'] is None
 return p,ready
def release(p):p.stdin.write('GO\n');p.stdin.flush()
def finish(p):
 out,err=p.communicate(timeout=30);assert p.returncode==0,err
 lines=out.splitlines();assert lines[0]=='LOCK_REQUEST'
 return json.loads(lines[-1])

@pytest.mark.parametrize('committed',[False,True])
@pytest.mark.parametrize('order',['before','after'])
def test_same_id_conflict_committed_history_is_preserved(tmp_path,committed,order):
 b,v=make(tmp_path);v['grant']=committed
 if order=='after':advance(b,v)
 b.store.admit_fixture(m.b1.episode(label='E3_FOREIGN_MATERIAL_FACT'))
 before=snapshot(b);r=advance(b,v);denied(r)
 assert r['reason']==('EVENT_IDENTITY_UNBOUND_LEGACY' if order=='before' else 'EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE')
 assert snapshot(b)==before and not b.store.db.in_transaction
 save('polluted_'+order+'_'+str(committed),before=before,after=snapshot(b),receipt=r);b.close()

@pytest.mark.parametrize('committed',[False,True])
def test_exact_b1_duplicate_then_foreign_duplicate(tmp_path,committed):
 b,v=make(tmp_path);v['grant']=committed;first=advance(b,v)
 data=deepcopy(first['admitted_event']);data.pop('hash');before=snapshot(b)
 b.store.admit_fixture(m.b1.Event(**data));assert snapshot(b)==before
 r=advance(b,v);assert r['admitted_event']==first['admitted_event'] and snapshot(b)==before
 foreign=replace(m.b1.episode(label='E3_UNRELATED'),event_id='E3-UNRELATED')
 b.store.admit_fixture(foreign);once=snapshot(b);b.store.admit_fixture(foreign);assert snapshot(b)==once
 replay=advance(b,v);assert replay['admitted_event']==first['admitted_event'] and snapshot(b)==once
 save('duplicates_'+str(committed),first=first,replay=replay,before=once,after=snapshot(b));b.close()

@pytest.mark.parametrize('field',['issuer','world_ref','expected_actor_state_hash','other_actions'])
@pytest.mark.parametrize('mapped',[False,True])
def test_closed_registrar_rejects_forged_provenance(tmp_path,field,mapped):
 b,v=make(tmp_path)
 if mapped:advance(b,v)
 changed=deepcopy(v)
 if field=='other_actions':changed['witness'][field][0]['participant']['actor_id']='peer'
 else:changed['witness'][field]='E3-COUNTERFEIT'
 seal(changed);before=snapshot(b);r=advance(b,changed);denied(r)
 assert snapshot(b)==before
 save('forged_'+field+'_'+str(mapped),receipt=r,tables=before);b.close()

@pytest.mark.parametrize('part',['packet','context','policy'])
def test_replay_cannot_extend_complete_readset(tmp_path,part):
 b,v=make(tmp_path);advance(b,v);before=snapshot(b)
 v[part]['e3_added_readset']={'parent':'UNWITNESSED'}
 key={'packet':'proposal_hash','context':'context_hash','policy':'policy_hash'}[part];v[part]=m.rehash(v[part],key)
 r=advance(b,v)
 assert r['status'] in ('DENIED','DEFERRED') and r['event_admission']=='NOT_PERFORMED' and not r['b1_invoked']
 assert snapshot(b)==before
 save('readset_'+part,receipt=r,tables=before);b.close()

def test_unmapped_stale_checkpoint_cannot_create_occurrence(tmp_path):
 b,v=make(tmp_path);state=b.store.state();state['e3_owner_epoch']=3
 b.store.db.execute('UPDATE checkpoint SET body=? WHERE id=1',(m.b1.canonical(state),));before=snapshot(b)
 r=advance(b,v);denied(r);assert snapshot(b)==before
 save('stale_checkpoint',receipt=r,tables=before);b.close()

@pytest.mark.parametrize('committed',[False,True])
def test_two_cold_ingress_writers_wait_for_privileged_b1_commit(tmp_path,committed):
 b,v=make(tmp_path);v['grant']=committed;advance(b,v)
 ps=[start(tmp_path,v,i) for i in range(2)]
 b.store.db.execute('BEGIN IMMEDIATE');b.store.admit_fixture(m.b1.episode(label='E3_PRIVILEGED_B1_BYPASS'))
 pending=snapshot(b)
 for p,_ in ps:release(p)
 for p,_ in ps:
  assert select.select([p.stdout],[],[],15)[0];assert p.stdout.readline().strip()=='LOCK_REQUEST'
  assert not select.select([p.stdout],[],[],0.15)[0]
 b.store.db.execute('COMMIT')
 results=[]
 for p,ready in ps:
  out,err=p.communicate(timeout=30);assert p.returncode==0,err
  result=json.loads(out);denied(result['receipt']);assert result['receipt']['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE';results.append(dict(ready=ready,**result))
 assert snapshot(b)==pending and len(pending['occurrence'])==2
 assert len({r['pid'] for r in results})==2
 save('lock_conflict_'+str(committed),processes=results,committed=pending,after=snapshot(b));b.close()

def test_rolled_back_privileged_writer_does_not_poison_reentry(tmp_path):
 b,v=make(tmp_path);advance(b,v);before=snapshot(b);p,ready=start(tmp_path,v,0)
 b.store.db.execute('BEGIN IMMEDIATE');b.store.admit_fixture(m.b1.episode(label='E3_ABORTED_BYPASS'));release(p)
 assert select.select([p.stdout],[],[],15)[0];assert p.stdout.readline().strip()=='LOCK_REQUEST'
 assert not select.select([p.stdout],[],[],0.15)[0];b.store.db.execute('ROLLBACK')
 out,err=p.communicate(timeout=30);assert p.returncode==0,err;r=json.loads(out.splitlines()[-1])
 assert isinstance(r['receipt']['event_admission'],dict) and snapshot(b)==before
 save('lock_rollback',ready=ready,result=r,before=before,after=snapshot(b));b.close()

def test_cold_mapped_replay_refuses_pollution_without_rewriting_response(tmp_path):
 b,v=make(tmp_path);v['grant']=True;first=advance(b,v);assert first['status']=='COMMITTED'
 b.store.admit_fixture(m.b1.episode(label='E3_LATER_POLLUTION'));before=snapshot(b);b.close()
 p,ready=start(tmp_path,v,'cold');release(p);r=finish(p);denied(r['receipt'])
 b=m.Bridge(tmp_path/'state.sqlite');assert snapshot(b)==before and len(b.store.state()['responses'])==1
 save('cold_polluted',ready=ready,result=r,before=before,after=snapshot(b));b.close()

def test_scan_cost_and_query_plan_are_bounded_measurements(tmp_path):
 b,v=make(tmp_path);advance(b,v);samples=[]
 for count in (0,100,1000):
  current=b.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]-1
  b.store.db.execute('BEGIN IMMEDIATE')
  for i in range(current,count):b.store.admit_fixture(replace(m.b1.episode(),event_id='E3-SCALE-'+str(i)))
  b.store.db.execute('COMMIT');before=snapshot(b);times=[];traces=[]
  b.store.db.set_trace_callback(traces.append)
  for _ in range(3):
   t=time.perf_counter();r=advance(b,v);times.append(time.perf_counter()-t);assert isinstance(r['event_admission'],dict)
  b.store.db.set_trace_callback(None);assert snapshot(b)==before
  samples.append(dict(unrelated_rows=count,seconds=times,trace=traces,plan=b.store.db.execute('EXPLAIN QUERY PLAN SELECT hash,body FROM occurrence').fetchall()))
 save('scan_cost',samples=samples,limitation='Whole table JSON scan under writer lock; O(total occurrence rows), no production latency guarantee.');b.close()

@pytest.mark.parametrize('committed',[False,True])
def test_schema_valid_changed_policy_is_bound_even_on_replay(tmp_path,committed):
 b,v=make(tmp_path);v['grant']=committed;advance(b,v);before=snapshot(b)
 v['policy']['policy_id']='E3-DIFFERENT-VALID-POLICY';v['policy']=m.rehash(v['policy'],'policy_hash')
 r=advance(b,v);denied(r)
 assert r['reason']=='EVENT_IDENTITY_CONFLICT' and snapshot(b)==before
 save('valid_policy_'+str(committed),receipt=r,tables=before);b.close()

def test_exact_content_legacy_before_mapping_cannot_invent_provenance(tmp_path):
 origin=tmp_path/'origin';origin.mkdir();source,v=make(origin);first=advance(source,v);data=deepcopy(first['admitted_event']);data.pop('hash');source.close()
 b,v=make(tmp_path);b.store.admit_fixture(m.b1.Event(**data));before=snapshot(b)
 r=advance(b,v);denied(r)
 assert r['reason']=='EVENT_IDENTITY_UNBOUND_LEGACY' and snapshot(b)==before
 save('exact_content_unmapped',receipt=r,tables=before);b.close()
