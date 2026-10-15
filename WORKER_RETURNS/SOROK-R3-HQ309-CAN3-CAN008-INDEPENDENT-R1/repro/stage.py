"""Reconstruct only exact authorized Git objects; verify native blob bytes."""
from pathlib import Path
import subprocess,json,hashlib,shutil
R=Path(__file__).resolve().parents[1]; A=R/'runtime/author'
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
# Bootstrap the reviewed packet from native Git, so no ignored runtime state is required.
rev='ee6a48b40247b113c614fe2099d4c443e8dd7bb7';base='WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1'
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',rev,base],text=True).splitlines()
for path in paths:
 rel=path[len(base)+1:]
 if rel.startswith(('candidate/','repro/','inherited/','lineage/')) or rel=='00_INHERITED_FROZEN_PREREG.json':
  raw=subprocess.check_output(['git','show',rev+':'+path]);assert blob(raw)==subprocess.check_output(['git','rev-parse',rev+':'+path],text=True).strip()
  dest=A/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
for name,ref in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
 raw=subprocess.check_output(['git','cat-file','blob',ref]);assert blob(raw)==ref
 dest=R/'runtime/law'/(name+'.txt');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
rows=json.loads((A/'lineage/00_ORIGINAL_SOURCE_MANIFEST.json').read_text()); receipts=[]
for row in rows:
 b=subprocess.check_output(['git','show',row['commit']+':'+row['path']]);assert blob(b)==row['blob_sha1'];assert hashlib.sha256(b).hexdigest()==row['sha256']
 rel=Path(row['local']).relative_to('runtime_root/source');d=A/'runtime_root/original'/rel;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
 receipts.append(dict(commit=row['commit'],path=row['path'],blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
# Original owner/original candidate test paths retained. Only six repaired modules overlay.
S=A/'runtime_root/court_repaired/runtime_root/source';shutil.copytree(A/'runtime_root/original',S,dirs_exist_ok=True)
C=S/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1/candidate'
rev='ee6a48b40247b113c614fe2099d4c443e8dd7bb7';base='WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1'
for f in (A/'candidate').glob('*.py'):
 b=subprocess.check_output(['git','show',rev+':'+base+'/candidate/'+f.name]);assert b==f.read_bytes();(C/f.name).write_bytes(b)
 receipts.append(dict(commit=rev,path=base+'/candidate/'+f.name,blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
# Check repair code seal equals final candidate; don't silently follow changed source.
for f in (A/'candidate').glob('*.py'):assert f.read_bytes()==subprocess.check_output(['git','show','f9ff05197fb2837c733f8b453c678043e90c77d8:'+base+'/candidate/'+f.name])
(R/'01_SOURCE_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('Verified',len(rows),'original objects and',len(list((A/'candidate').glob('*.py'))),'repaired modules')

for dest in [A/'runtime_root/law',A/'runtime_root/court_repaired/runtime_root/law']:
 shutil.copytree(R/'runtime/law',dest,dirs_exist_ok=True)
(A/'evidence').mkdir(exist_ok=True)
# RCP3 test and instrument bytes are checked against their independent source commit.
for n in ['test_independent.py','causal_probe.py']:
 original=subprocess.check_output(['git','show','a11982e6cf135a8ecc72b6152ec796b4a4707093:WORKER_RETURNS/SOROK-R3-HQ303-RCP3-CAN008-COMPLETION-COURT-R1/repro/'+n])
 assert original==(A/'inherited/repro'/n).read_bytes()
