"""Minimal genuine Git closure; immutable original sources live ignored."""
import ast,datetime,hashlib,json,pathlib,subprocess,uuid
RET=pathlib.Path(__file__).resolve().parents[1];ROOT=RET.parents[1];RT=RET/'runtime_root'
C='56098540bd36f22aef66db24913722aec808e3e9';CP='WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-WG0P2-WORKLOAD-PRODUCTIVE-REPAIR-R1'
if RT.exists():raise SystemExit('EXISTING_RUNTIME_REFUSE_OVERWRITE')
RT.mkdir();rows=[];mapped={}
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def put(c,p,d,expected=None):
 b=git('show',c+':'+p);blob=git('rev-parse',c+':'+p).decode().strip();assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==blob
 assert expected is None or blob==expected,(p,expected,blob)
 out=RT/d;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 row=dict(commit=c,source_path=p,staging_path=d,git_blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b));rows.append(row);mapped[d]=row
 return b
for p in git('ls-tree','-r','--name-only',C,CP).decode().splitlines():put(C,p,'candidate/'+p.removeprefix(CP+'/'))
for c,prefix,dest in [('e1cc3016280d3714c485bf6ec7cecb360e4df3bc','WORKER_RETURNS/PYAT-USERDIRECT-20261014-R4-WG0I-INDEPENDENT-WORKLOAD-COURT-R1','previous_WG0I')]:
 for p in git('ls-tree','-r','--name-only',c,prefix).decode().splitlines():put(c,p,dest+'/'+p.removeprefix(prefix+'/'))
oracle=json.loads((RET/'01_FROZEN_ORACLE_AND_PINNED_OWNERS.json').read_text())
for p,blob in oracle['pinned_owner_blobs'].items():put(C,p,p,blob)
queue=[r for r in rows if r['staging_path'].endswith('.py')];seen=set()
def module(name):
 if not name.startswith('rawlsing_next.'):return
 rel=name.replace('.','/')+'.py'
 if rel in mapped:return
 if subprocess.run(['git','-c','gc.auto=0','-C',str(ROOT),'cat-file','-e',C+':'+rel],capture_output=True).returncode:return
 put(C,rel,rel);queue.append(mapped[rel])
while queue:
 row=queue.pop();rel=row['staging_path']
 if rel in seen:continue
 seen.add(rel);tree=ast.parse((RT/rel).read_text())
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):
   for a in n.names:module(a.name)
  elif isinstance(n,ast.ImportFrom) and n.module:
   name=n.module if not n.level else '.'.join(rel.removesuffix('.py').split('/')[:-n.level])+'.'+n.module
   module(name)
   for a in n.names:module(name+'.'+a.name)
marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),role='WG0J_INDEPENDENT',permissions='SYNTHETIC_ONLY_NO_ORIGINAL_SURVEY_ISSUER_OR_ACTOR')
(RT/'runtime_marker.json').write_text(json.dumps(marker,indent=2)+'\n')
(RET/'source_selector.json').write_text(json.dumps(dict(schema='WG0J_GENUINE_GIT_SOURCE_CUSTODY@1',candidate=C,files=rows,actual_NUL_verified=True),indent=2)+'\n');print('STAGED_EXACT_FILES',len(rows),'EPOCH',marker['epoch_id'])
