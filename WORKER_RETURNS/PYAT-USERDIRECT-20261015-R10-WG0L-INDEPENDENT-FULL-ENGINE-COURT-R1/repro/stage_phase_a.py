"""Exact historical sources only. Never resolves or reads WG0P4 candidate."""
from pathlib import Path
import subprocess,ast,hashlib,json,uuid,datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];RT=R/'runtime_root';RT.mkdir(exist_ok=False)
C='56098540bd36f22aef66db24913722aec808e3e9';rows=[];mapped={}
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def put(c,p,d):
 data=git('show',c+':'+p);expected=git('rev-parse',c+':'+p).decode().strip();physical=subprocess.check_output(['git','hash-object','--stdin'],input=data).decode().strip();assert expected==physical
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==expected
 out=RT/d;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
 r={'commit':c,'source_path':p,'staged_path':d,'git_blob_sha1':expected,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)};rows.append(r);mapped[d]=r
 return data
sources=[('b62b02702b08f71adcba25e214fbddcb6ccec566','WORKER_RETURNS/PYAT-USERDIRECT-20261014-R6-WG0J-INDEPENDENT-WORKLOAD-COURT-R1','WG0J'),('c506293e31ea8f9e490de0369169005f52f81033','WORKER_RETURNS/PYAT-USERDIRECT-20261015-R8-WG0K-INDEPENDENT-CUSTODY-COURT-R1','WG0K'),('16584e2f5b6ab43652063797d30c59465b1f66bb','WORKER_RETURNS/PYAT-USERDIRECT-20261015-R7-WG0P3-IDENTITY-FRONTIER-COLD-REPAIR-R1','WG0P3'),(C,'WORKER_RETURNS/PYAT-USERDIRECT-20261014-R5-WG0P2-WORKLOAD-PRODUCTIVE-REPAIR-R1','WG0P2')]
# Discover exact predecessor prefix if capitalization differs; fixed scientific role, no candidate search.
for c,prefix,dest in sources:
 found=git('ls-tree','-r','--name-only',c,prefix).decode().splitlines()
 if not found:
  key='WG0P3' if dest=='WG0P3' else dest
  allpaths=git('ls-tree','-r','--name-only',c,'WORKER_RETURNS').decode().splitlines()
  candidates=sorted({p.split('/')[1] for p in allpaths if key in p.split('/')[1]});assert len(candidates)==1,candidates
  prefix='WORKER_RETURNS/'+candidates[0];found=[p for p in allpaths if p.startswith(prefix+'/')]
 # reports/oracles/tests/runtime helpers, not verbose historic observation payloads
 for p in found:
  rel=p.removeprefix(prefix+'/')
  if rel.startswith(('observations/','runtime_root/')):continue
  put(c,p,dest+'/'+rel)
commission='WORKER_COMMISSIONS/PYAT-USERDIRECT-20261015-R9-WG0P4-EXACT-FRONTIER-COLD-REPAIR-R1/00_COMMISSION.md'
put('c1e88fb26f3ef757f13bad7cf901cd6529a368c8',commission,'WG0P4_COMMISSION.md')
required={'pre553_c11_repository':'67c6eb6494522cd11aab1b93d0e73f9cef6036f3','pre553_c11_ingest':'37cd35fa2e3420a3eea272a2902e96ab9ba38aba','pre553_empirical_query':'03facecf70890bfd13b80418620d274cbcd69d02','pre553_batch_runner':'2d291600b9a10c56d9c6f6de7f7d619f6c52e829','pre553_empirical_objects':'a61365b994e5c3c50de0f598fcf40e90abf757b6','pre553_c11_integrity':'7c59aa13a2b7c8e3ab0dc90a1400df645b0b4bbd'}
for name,pin in required.items():
 p='rawlsing_next/'+name+'.py';put(C,p,p);assert mapped[p]['git_blob_sha1']==pin
queue=list(rows);seen=set()
def module(name):
 if not name.startswith('rawlsing_next.'):return
 p=name.replace('.','/')+'.py'
 if p in mapped:return
 if subprocess.run(['git','-C',str(ROOT),'cat-file','-e',C+':'+p],capture_output=True).returncode:return
 put(C,p,p);queue.append(mapped[p])
while queue:
 r=queue.pop();rel=r['staged_path']
 if not rel.endswith('.py') or rel in seen:continue
 seen.add(rel)
 for n in ast.walk(ast.parse((RT/rel).read_text())):
  if isinstance(n,ast.Import):
   for x in n.names:module(x.name)
  elif isinstance(n,ast.ImportFrom) and n.module:
   name=n.module if not n.level else '.'.join(rel[:-3].split('/')[:-n.level])+'.'+n.module
   module(name)
   for x in n.names:module(name+'.'+x.name)
(R/'source_selector_phase_a.json').write_text(json.dumps({'phase':'A','no_WG0P4_candidate_read':True,'files':rows},indent=2)+'\n')
(R/'observations/runtime_marker.json').write_text(json.dumps({'environment_id':str(uuid.uuid4()),'epoch_id':str(uuid.uuid4()),'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'permission':'Read historical sourcefree code, run local synthetic tests; no original source or issuance'},indent=2)+'\n')
print('EXACT_STAGED',len(rows))
