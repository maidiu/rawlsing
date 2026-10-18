"""Real derived-index migration and every-writer maintenance regressions."""
from pathlib import Path
from dataclasses import replace
from copy import deepcopy
import os,sys,json,sqlite3,time,statistics
import pytest
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m

def setup(path):
 b=m.Bridge(path/'state.sqlite',None if (path/'state.sqlite').exists() else m.b1.initialize(m.b1.prehistory()))
 packet,context,policy=m.input_pair(b.store.state());w=m.occurrence_witness(b.store.state(),packet,context);cap,reg=m.capability_fixture()
 b.witnesses={w['hash']:w};b.capability_witnesses=reg
 return b,(packet,context,policy,w,cap)
def snapshot(b):return {n:b.store.db.execute('SELECT * FROM '+n+' ORDER BY 1').fetchall() for n in ('occurrence','checkpoint','b2_ingress','b2_event_identity','joint_receipt')}
def save(name,**v):
 out=Path(os.environ['E3_EVIDENCE']);(out/('indexed_'+name+'.json')).write_text(json.dumps(v,indent=2)+'\n')

@pytest.mark.parametrize('polluted',[False,True])
def test_existing_ledger_is_indexed_without_fact_changes(tmp_path,polluted):
 path=tmp_path/'state.sqlite';s=m.b1.Store(path,m.b1.initialize(m.b1.prehistory()))
 s.admit_fixture(m.b1.episode())
 if polluted:s.admit_fixture(m.b1.episode(label='LEGACY-CONFLICT'))
 before=s.db.execute('SELECT * FROM occurrence ORDER BY 1').fetchall();s.close()
 b,args=setup(tmp_path);r=b.advance(*args,grant=False)
 assert r['reason']=='EVENT_IDENTITY_UNBOUND_LEGACY'
 assert b.store.db.execute('SELECT * FROM occurrence ORDER BY 1').fetchall()==before
 plan=b.store.db.execute("EXPLAIN QUERY PLAN SELECT hash,body FROM occurrence WHERE json_extract(body,'$.event_id')=? LIMIT 2",('event1',)).fetchall()
 assert any('b2_occurrence_event_id' in row[-1] and 'SEARCH' in row[-1] for row in plan)
 save('migration_'+str(polluted),plan=plan,receipt=r,occurrence=before);b.close()

@pytest.mark.parametrize('kind',['insert','update'])
def test_separate_raw_sql_writer_updates_derived_lookup(tmp_path,kind):
 b,args=setup(tmp_path);b.advance(*args,grant=False)
 foreign=m.b1.sealed(m.b1.asdict(replace(m.b1.episode(label='RAW-CONFLICT'),event_id='OTHER' if kind=='update' else 'event1')))
 con=sqlite3.connect(tmp_path/'state.sqlite',isolation_level=None)
 con.execute('INSERT INTO occurrence VALUES (?,?)',(foreign['hash'],m.b1.canonical(foreign)))
 if kind=='update':
  event=deepcopy(foreign);event['event_id']='event1';event.pop('hash');event=m.b1.sealed(event)
  con.execute('UPDATE occurrence SET hash=?,body=? WHERE hash=?',(event['hash'],m.b1.canonical(event),foreign['hash']))
 con.close();before=snapshot(b);r=b.advance(*args,grant=False)
 assert r['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE' and r['event_admission']=='NOT_PERFORMED' and not r['b1_invoked']
 assert snapshot(b)==before
 save('raw_'+kind,receipt=r,tables=before);b.close()

def test_many_conflicts_need_only_two_lookup_rows(tmp_path):
 b,args=setup(tmp_path);b.advance(*args,grant=False)
 for i in range(20):b.store.admit_fixture(m.b1.episode(label='CONFLICT-'+str(i)))
 rows=b.store.db.execute("SELECT hash FROM occurrence WHERE json_extract(body,'$.event_id')=? LIMIT 2",('event1',)).fetchall()
 before=snapshot(b);r=b.advance(*args,grant=False)
 assert len(rows)==2 and r['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE' and snapshot(b)==before
 save('many_conflicts',receipt=r,lookup_rows=rows,occurrence_count=len(before['occurrence']));b.close()

def test_unrelated_ledger_size_does_not_expand_reentry_query_work(tmp_path):
 b,args=setup(tmp_path);b.advance(*args,grant=False);stats=[]
 for count in (0,100,10000):
  current=b.store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0]-1
  b.store.db.execute('BEGIN IMMEDIATE')
  for i in range(current,count):b.store.admit_fixture(replace(m.b1.episode(),event_id='SCALE-'+str(i)))
  b.store.db.execute('COMMIT')
  work=[]
  for _ in range(5):
   calls=[0]
   def progress():calls[0]+=1;return 0
   b.store.db.set_progress_handler(progress,1);start=time.perf_counter()
   rows=b.store.db.execute("SELECT hash,body FROM occurrence WHERE json_extract(body,'$.event_id')=? LIMIT 2",('event1',)).fetchall()
   elapsed=time.perf_counter()-start;b.store.db.set_progress_handler(None,0)
   assert len(rows)==1;work.append(dict(vm_instructions=calls[0],seconds=elapsed))
  stats.append(dict(unrelated_rows=count,measurements=work))
 assert max(r['vm_instructions'] for sample in stats for r in sample['measurements'])<100
 assert max(r['vm_instructions'] for r in stats[-1]['measurements'])==max(r['vm_instructions'] for r in stats[0]['measurements'])
 r=b.advance(*args,grant=False);assert isinstance(r['event_admission'],dict)
 save('scale',stats=stats,receipt=r);b.close()

def test_reopening_and_idempotent_index_creation_preserve_state(tmp_path):
 b,args=setup(tmp_path);b.advance(*args,grant=True);before=snapshot(b);b.close()
 for _ in range(3):
  b=m.Bridge(tmp_path/'state.sqlite');assert snapshot(b)==before
  assert b.store.db.execute('PRAGMA integrity_check').fetchone()==('ok',);b.close()
