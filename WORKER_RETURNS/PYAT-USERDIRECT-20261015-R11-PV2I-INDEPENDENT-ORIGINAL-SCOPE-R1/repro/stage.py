from pathlib import Path
import subprocess,hashlib,json,ast,uuid,datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];RT=R/'runtime_root';RT.mkdir(exist_ok=False)
C='c6ff1c3ec68d62fda478df8ceb2986b268b72dbf';BASE='3f91dc22d2eb863bc1d2facccfd33e6c05349503';CP='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-PV2-ORIGINAL-EXPECTED-SCOPE-BINDING-R1';PV='694fb45085cd5e4891949921a44edb77c3f603f2';PP='WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1';rows=[];mapped={}
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def put(c,p,d):
 data=git('show',c+':'+p);blob=git('rev-parse',c+':'+p).decode().strip();assert subprocess.check_output(['git','hash-object','--stdin'],input=data).decode().strip()==blob
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
 out=RT/d;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data);row=dict(commit=c,source_path=p,staged_path=d,git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data));rows.append(row);mapped[d]=row;return data
for p in git('ls-tree','-r','--name-only',C,CP).decode().splitlines():put(C,p,'candidate/'+p.removeprefix(CP+'/'))
passport=json.loads((RT/'candidate/environment_passport_delta.json').read_text())
for p,row in passport['blob_pinning'].items():
 put(row['source_commit'],p,p);assert mapped[p]['git_blob_sha1']==row['pinned']
for p in ['rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py','rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py']:put(BASE,p,p)
for rel in ['01_FROZEN_ORIGINAL_IDENTITY_ORACLES.json','00_INDEPENDENT_METHOD_COURT.md','04_SEMANTIC_OWNER_DECISION_REQUIRED.md']:put(PV,PP+'/'+rel,'prior_PV/'+rel)
(RT/'prior_PV/repro').mkdir(exist_ok=True)
queue=list(rows);seen=set()
def module(name):
 if not name.startswith('rawlsing_next.'):return
 p=name.replace('.','/')+'.py'
 if p in mapped:return
 if subprocess.run(['git','-c','gc.auto=0','-C',str(ROOT),'cat-file','-e',BASE+':'+p],capture_output=True).returncode:return
 put(BASE,p,p);queue.append(mapped[p])
while queue:
 row=queue.pop();rel=row['staged_path']
 if not rel.endswith('.py') or rel in seen:continue
 seen.add(rel)
 for n in ast.walk(ast.parse((RT/rel).read_text())):
  if isinstance(n,ast.Import):
   for x in n.names:module(x.name)
  elif isinstance(n,ast.ImportFrom):
   name=n.module or ''
   if n.level:name='.'.join(rel[:-3].split('/')[:-n.level])+('.'+name if name else '')
   module(name)
   for x in n.names:module(name+'.'+x.name)
# P01 loads its pinned retained join worker by physical path. It is already present via passport.
(R/'source_selector.json').write_text(json.dumps({'candidate':C,'accepted_base':BASE,'files':rows,'actual_git_hash_object_and_NUL_preimage':True},indent=2)+'\n')
(R/'observations/runtime_marker.json').write_text(json.dumps({'environment_id':str(uuid.uuid4()),'epoch_id':str(uuid.uuid4()),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'permission':'local original-sourcefree synthetic owner tests only'},indent=2)+'\n')
print('STAGED',len(rows))
