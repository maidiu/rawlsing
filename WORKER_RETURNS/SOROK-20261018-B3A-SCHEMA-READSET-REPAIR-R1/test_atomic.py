"""Prospective public-boundary atomicity court, no frozen expectation edits."""
from pathlib import Path
from copy import deepcopy
import sys,json,subprocess,os,select,sqlite3
import pytest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'candidate'))
from integration import Integration,Refusal,digest
from fixture_authority import FixtureAuthority
from developmental_loop import World,permission_for
from custody import prepare,admit
import integration
OUT=ROOT/'evidence/atomic_sql';OUT.mkdir(parents=True,exist_ok=True)
STAGES=('before_first_b2_admission','after_first_source_admission','after_b3_source_insert','after_b3_preimage_insert','after_target_effect_before_commit','after_publication_before_commit')
def frame(t=7):
 w=World()
 for i in range(1,t+1):w.tick(i)
 return w.frame()
def cold(path):
 p=subprocess.run([sys.executable,str(ROOT/'atomic_worker.py'),str(path),'inspect'],capture_output=True,text=True,check=True)
 r=json.loads(p.stdout);assert r['pid']!=os.getpid() and r['integrity']=='ok';return r
def seed(e,f,same=False):
 external=deepcopy(f['event'])
 if not same:external['id']='independent-objective-fact'
 bundle,_=prepare(e.bridge.store.state(),external,participant=integration.participant_from_records(f['evidence'],external['time']))
 r=admit(e.bridge,bundle);assert isinstance(r['event_admission'],dict)
 return bundle
def setup(tmp_path,independent=False):
 f=frame();a=FixtureAuthority();a.register_observed(f);path=tmp_path/'public.sqlite';e=Integration(path,a)
 if independent:seed(e,f)
 return f,a,e,path
def snap(e):return json.loads(json.dumps(e.snapshot()))
def save(name,**data):(OUT/(name+'.json')).write_text(json.dumps(data,indent=2)+'\n')
def replay_no_ghost(e,a):
 f=frame();r=e.run(f);assert r['status']=='ELIGIBLE_NONCAUSAL' and not r['owner_effect_committed'] and e.middle()==[]
 later=frame(9);a.register_observed(later);r=e.run(later)
 assert r['status']=='ELIGIBLE_NONCAUSAL' and not r['CAN008_response']['recruited'] and not r['CAN008_response']['practical_actions']
 return r
@pytest.mark.parametrize('stage',STAGES)
@pytest.mark.parametrize('independent',[False,True])
@pytest.mark.parametrize('failure',['refusal','unexpected','storage'])
def test_injected_failure_all_tables_cold_replay(tmp_path,stage,independent,failure):
 f,a,e,path=setup(tmp_path,independent);before=snap(e);hit=[];p=permission_for([],f)
 def fault(at):
  if at==stage:
   hit.append(at)
   if failure=='refusal':raise Refusal('INJECTED_'+at)
   if failure=='storage':raise sqlite3.OperationalError('INJECTED_STORAGE_'+at)
   raise RuntimeError('INJECTED_'+at)
 e.fault=fault
 if failure=='refusal':
  result=e.run(f,owner_permission=p,registered_permissions=(p,));assert result['status']=='REFUSED' and result['no_mutation'] and not result['owner_effect_committed'] and 'independent_owner_receipt' not in result and 'CAN011_transition' not in result and 'admission' not in result
 else:
  with pytest.raises(sqlite3.OperationalError if failure=='storage' else RuntimeError):e.run(f,owner_permission=p,registered_permissions=(p,))
  result={'exception':failure}
 assert hit==[stage] and snap(e)==before
 e.close();c=cold(path);assert c['snapshot']==before
 e=Integration(path,a);later=replay_no_ghost(e,a);after=snap(e);e.close()
 save(f'{stage}_{independent}_{failure}',before=before,cold=c,result=result,later=later,after=after)
@pytest.mark.parametrize('stage',STAGES)
@pytest.mark.parametrize('independent',[False,True])
def test_actual_sigkill_all_tables_and_no_recruitment(tmp_path,stage,independent):
 f,a,e,path=setup(tmp_path,independent);before=snap(e);e.close();fp=tmp_path/'frame.json';fp.write_text(json.dumps(f))
 p=subprocess.Popen([sys.executable,str(ROOT/'atomic_worker.py'),str(path),stage,str(fp)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try:
  assert select.select([p.stdout],[],[],30)[0]
  line=p.stdout.readline();assert line,(p.poll(),p.stderr.read())
  ready=json.loads(line);assert ready['stage']==stage and ready['pid']!=os.getpid()
  p.kill();out,err=p.communicate(timeout=15);assert p.returncode==-9
 finally:
  if p.poll() is None:p.kill();p.wait()
 c=cold(path);assert c['snapshot']==before
 e=Integration(path,a);later=replay_no_ghost(e,a);e.close()
 save(f'kill_{stage}_{independent}',before=before,ready=ready,exit_code=p.returncode,cold=c,later=later)
@pytest.mark.parametrize('attack',['missing_origin','future_event','unbound_origin','origin_after_event','derived_collision'])
def test_preflight_before_first_admission(tmp_path,monkeypatch,attack):
 f,a,e,path=setup(tmp_path);bad=deepcopy(f)
 if attack=='missing_origin':bad['origin_event_id']='never'
 if attack=='future_event':bad['event']['time']=99
 if attack=='unbound_origin':bad['origin_event_id']='unregistered'
 if attack in ('origin_after_event','derived_collision'):
  assert e.run(f)['status']=='ELIGIBLE_NONCAUSAL';bad['as_of']=8;bad['event']['id']='new-current-event';bad['event']['time']=8
  if attack=='origin_after_event':
   # Parent clock is 3; earlier current clock is refused before B2.
   bad['event']['time']=2;bad['origin_event_id']=f['event']['id']
  else:bad['utterances'][0]['event_ref']='new-current-event'
 if attack!='unbound_origin':a.register_observed(bad)
 before=snap(e);calls=[]
 def forbidden(*args,**kwargs):calls.append(True);raise AssertionError('B2 CALLED BEFORE PREFLIGHT')
 monkeypatch.setattr(integration,'admit',forbidden)
 r=e.run(bad);assert r['status']=='REFUSED' and not calls and snap(e)==before
 e.close();c=cold(path);assert c['snapshot']==before
 save('preflight_'+attack,before=before,result=r,cold=c,admission_calls=len(calls))
def test_independent_exact_event_and_denied_permission_are_retained(tmp_path):
 f,a,e,path=setup(tmp_path);seed(e,f,same=True);before=snap(e);p=permission_for([],f)
 r=e.run(f,owner_permission=p,registered_permissions=());assert r['status']=='ELIGIBLE_NONCAUSAL' and r['CAN011_transition']['status']=='DENIED'
 assert not r['owner_effect_committed'] and e.middle()==[]
 for table,rows in before.items():assert set(map(tuple,rows))<=set(map(tuple,snap(e)[table]))
 admitted=e.snapshot();e.close();c=cold(path);assert c['snapshot']==json.loads(json.dumps(admitted))
 save('independent_exact_then_permission_denied',before=before,result=r,cold=c)
def test_publication_readset_rejects_privileged_race_without_erasing_it(tmp_path):
 f,a,e,path=setup(tmp_path);before=snap(e);fired=[]
 def fault(stage):
  if stage=='after_target_effect_before_commit' and not fired:
   other=sqlite3.connect(path);other.execute('INSERT INTO b3_clock VALUES (1234)');other.commit();other.close();fired.append(True)
 e.fault=fault;r=e.run(f)
 assert r['status']=='REFUSED' and r['code']=='PUBLICATION_READSET_CHANGED' and not r['no_mutation']
 after=snap(e);assert after['b3_clock']==[[1234]]
 for table,rows in before.items():
  if table!='b3_clock':assert after[table]==rows
 e.close();save('privileged_race_preserved',before=before,result=r,cold=cold(path))

@pytest.mark.parametrize('stage',STAGES)
def test_boundary_sql_writes_are_tentative_until_publication(tmp_path,monkeypatch,stage):
 f,a,e,path=setup(tmp_path);before=snap(e);staged=[];public_trace=[];scratch_trace=[];observed={}
 e.db.set_trace_callback(public_trace.append)
 original=Integration._run
 def spy(self,*args,**kwargs):
  staged.append(self);self.db.set_trace_callback(scratch_trace.append)
  return original(self,*args,**kwargs)
 monkeypatch.setattr(Integration,'_run',spy)
 def fault(at):
  if at==stage:
   db=e if at=='after_publication_before_commit' else staged[0]
   observed.update(snapshot=snap(db),in_transaction=db.db.in_transaction)
   raise Refusal('SQL_BOUNDARY_'+at)
 e.fault=fault;p=permission_for([],f);r=e.run(f,owner_permission=p,registered_permissions=(p,))
 assert r['status']=='REFUSED' and snap(e)==before
 if stage=='before_first_b2_admission':assert observed['snapshot']==before
 else:assert len(observed['snapshot']['occurrence'])>=1
 if stage in ('after_target_effect_before_commit','after_publication_before_commit'):
  assert observed['snapshot']['b3_transition'] and observed['in_transaction']
 e.close();save('boundary_sql_'+stage,before=before,tentative=observed,result=r,public_trace=public_trace,scratch_trace=scratch_trace,cold=cold(path))
