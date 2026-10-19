"""Independent prospective transaction assertions. All failures stay literal."""
from pathlib import Path
from copy import deepcopy
import os,sys,json,sqlite3,subprocess,select,signal,hashlib
import pytest
ROOT=Path(__file__).resolve().parent
B3=Path(os.environ['REVIEW_B3_ROOT']);sys.path.insert(0,str(B3))
from integration import Integration,Refusal,digest
from fixture_authority import FixtureAuthority
from developmental_loop import World,permission_for
from custody import prepare,admit,participant_from_records
OUT=Path(os.environ['REVIEW_EVIDENCE']);OUT.mkdir(parents=True,exist_ok=True)
WORKER=ROOT/'reviewer_worker.py'
def frame():
 w=World()
 for t in range(1,8):w.tick(t)
 return w.frame()
def cold(path):
 p=subprocess.run([sys.executable,str(WORKER),'inspect',str(path)],capture_output=True,text=True,check=True)
 r=json.loads(p.stdout);assert r['pid']!=os.getpid() and r['integrity']=='ok';return r

def stable(r):return {k:r[k] for k in ('schema','tables','integrity')}
def save(name,**kw):(OUT/(name+'.json')).write_text(json.dumps(kw,indent=2)+'\n')
def setup(tmp_path,seeded=False):
 f=frame();a=FixtureAuthority();a.register_observed(f);path=tmp_path/'public.sqlite';e=Integration(path,a)
 if seeded:
  other=deepcopy(f['event']);other['id']='I2-independent-before-request'
  bundle,_=prepare(e.bridge.store.state(),other,participant=participant_from_records(f['evidence'],other['time']))
  assert isinstance(admit(e.bridge,bundle)['event_admission'],dict)
 return f,a,e,path

def test_schema_only_race_is_rejected(tmp_path):
 f,a,e,path=setup(tmp_path);before=cold(path);fired=[]
 def fault(stage):
  if stage=='after_target_effect_before_commit':
   with sqlite3.connect(path) as other:other.execute('CREATE INDEX i2_external_index ON b3_source(body)')
   fired.append(stage)
 e.fault=fault;r=e.run(f);after=cold(path);e.close();save('schema_only_race',before=before,result=r,after=after,fired=fired)
 assert fired and before['schema']!=after['schema']
 assert r['status']=='REFUSED','schema-only concurrent mutation escaped claimed full publication readset'
 assert r['no_mutation'] is False
 assert after['tables']==before['tables']

@pytest.mark.parametrize('kind',['row','table'])
def test_external_change_survives_refusal_with_truthful_flag(tmp_path,kind):
 f,a,e,path=setup(tmp_path,True);before=cold(path);external={}
 def fault(stage):
  if stage!='after_target_effect_before_commit':return
  if kind=='row':
   other=deepcopy(f);other['event']['id']='I2-concurrent-B2-objective';fp=tmp_path/'other.json';fp.write_text(json.dumps(other))
   proc=subprocess.run([sys.executable,str(WORKER),'admit',str(path),str(fp)],capture_output=True,text=True,check=True)
   external.update(json.loads(proc.stdout));assert isinstance(external['result']['event_admission'],dict) and external['pid']!=os.getpid()
  else:
   with sqlite3.connect(path) as db:db.execute('CREATE TABLE i2_external_table (id TEXT PRIMARY KEY)')
  external['snapshot']=cold(path)
 e.fault=fault;r=e.run(f);after=cold(path);e.close();save('external_'+kind,before=before,result=r,external=external,after=after)
 assert r['status']=='REFUSED' and r['code']=='PUBLICATION_READSET_CHANGED' and r['no_mutation'] is False
 assert stable(after)==stable(external['snapshot'])
 for table,rows in before['tables'].items():assert set(map(tuple,rows))<=set(map(tuple,after['tables'][table]))
 assert not after['tables']['b3_source'] and not after['tables']['b3_transition']

@pytest.mark.parametrize('seeded',[False,True])
def test_refusal_after_validated_target_has_no_partial_public_effect(tmp_path,seeded):
 f,a,e,path=setup(tmp_path,seeded);before=cold(path);p=permission_for([],f);hit=[]
 def fault(stage):
  if stage=='after_target_effect_before_commit':hit.append(stage);raise Refusal('I2_AFTER_TARGET_VALIDATION')
 e.fault=fault;r=e.run(f,owner_permission=p,registered_permissions=(p,));after=cold(path)
 assert hit and r['status']=='REFUSED' and r['no_mutation'] and not r['owner_effect_committed'] and 'independent_owner_receipt' not in r
 assert stable(after)==stable(before)
 e.fault=lambda at:None;success=e.run(f);e.close();reopened=Integration(path,a);replay=reopened.run(f);final=cold(path);reopened.close()
 save('late_target_'+str(seeded),before=before,result=r,after=after,success=success,replay=replay,final=final)
 assert replay['exact_replay'] and not replay['owner_effect_committed'] and not final['tables']['b3_transition']

@pytest.mark.parametrize('attack',['origin_binding','missing_origin','clock','source_parent'])
def test_exact_lineage_clock_and_source_replay(tmp_path,attack):
 f,a,e,path=setup(tmp_path);first=e.run(f);assert first['status']=='ELIGIBLE_NONCAUSAL';e.close();e=Integration(path,a);before=cold(path);bad=deepcopy(f)
 expected={'origin_binding':'SYNTHETIC_SOURCE_ISSUER_NOT_REGISTERED','missing_origin':'ORIGINAL_EVENT_NOT_ADMITTED','clock':'B3_TIME_REVERSED','source_parent':'SOURCE_PREIMAGE_IDENTITY_COLLISION'}[attack]
 if attack in ('origin_binding','missing_origin'):bad['origin_event_id']='I2-never-admitted'
 elif attack=='clock':bad['as_of']=6;bad['evidence']=[x for x in bad['evidence'] if x['time']<=6];bad['readset']=[x for x in bad['readset'] if x in {z['id'] for z in bad['evidence']}]
 else:
  x=bad['evidence'][0];x['note']='I2 replacement historical material';x['hash']=digest({k:v for k,v in x.items() if k!='hash'})
 if attack!='origin_binding':a.register_observed(bad)
 r=e.run(bad);after=cold(path);replay=e.run(f);e.close();save('tamper_'+attack,before=before,result=r,after=after,replay=replay)
 assert r['status']=='REFUSED' and r['code']==expected and r['no_mutation'] and stable(after)==stable(before)
 assert replay['status']=='ELIGIBLE_NONCAUSAL' and replay['exact_replay']

@pytest.mark.parametrize('stage',['before_first_b2_admission','after_first_source_admission','after_target_effect_before_commit','after_publication_before_commit','after_successful_return'])
@pytest.mark.parametrize('seeded',[False,True])
def test_real_process_kill_and_cold_reentry(tmp_path,stage,seeded):
 f,a,e,path=setup(tmp_path,seeded);e.close();before=cold(path);fp=tmp_path/'frame.json';fp.write_text(json.dumps(f))
 proc=subprocess.Popen([sys.executable,str(WORKER),'kill',str(path),str(fp),stage],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  assert select.select([proc.stdout],[],[],25)[0],'worker never reached selected boundary'
  ready=json.loads(proc.stdout.readline());assert ready['pid']==proc.pid and proc.poll() is None
  os.kill(proc.pid,signal.SIGKILL);out,err=proc.communicate(timeout=15);assert proc.returncode==-signal.SIGKILL
 finally:
  if proc.poll() is None:proc.kill();proc.wait()
 after=cold(path);e=Integration(path,a);replay=e.run(f);middle=e.middle();e.close();save('kill_'+stage+'_'+str(seeded),before=before,ready=ready,exit=proc.returncode,after=after,replay=replay,middle=middle)
 if stage=='after_successful_return':
  assert after['tables']['b3_transition'] and replay['exact_replay']
  for table,rows in before['tables'].items():assert set(map(tuple,rows))<=set(map(tuple,after['tables'][table]))
 else:assert stable(after)==stable(before) and not middle and not replay['owner_effect_committed']


def test_schema_change_on_refusal_sets_no_mutation_false(tmp_path):
 f,a,e,path=setup(tmp_path);before=cold(path)
 def fault(stage):
  if stage=='after_target_effect_before_commit':
   with sqlite3.connect(path) as db:db.execute('CREATE INDEX i2_refused_schema ON b3_source(body)')
   raise Refusal('I2_REFUSAL_WITH_EXTERNAL_SCHEMA_CHANGE')
 e.fault=fault;r=e.run(f);after=cold(path);e.close();save('schema_refusal_flag',before=before,result=r,after=after)
 assert r['status']=='REFUSED' and after['tables']==before['tables'] and after['schema']!=before['schema']
 assert r['no_mutation'] is False,'schema mutation incorrectly reported as no public mutation'
