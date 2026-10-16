from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];REPO=R.parents[1]
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=REPO)
manifest=[]
def put(c,p,d):
 b=git('show',c+':'+p);blob=git('rev-parse',c+':'+p).decode().strip()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
 dst=R/d;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
 manifest.append(dict(commit=c,path=p,local=d,git_blob=blob,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
pins=[('E05S','f524f60781e2e7e72278d04d6377fb1da877698a','PYAT-USERDIRECT-20261016-R14-E05S-INDEPENDENT-SELECTED-WORLD-R1'),('E05R','84485d32c0088995f8dc664dc0517b2d27f2563d','PYAT-USERDIRECT-20261015-R13-E05R-SELECTED-WORLD-REPAIR-R1')]
for label,c,name in pins:
 prefix='WORKER_RETURNS/'+name+'/'
 for p in git('ls-tree','-r','--name-only',c,prefix).decode().splitlines():put(c,p,'inputs/'+label+'/'+p[len(prefix):])
for label,c,p in [('E05I','a56f5c9c3d13081677586510a83351bcdeda2d3c','WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E05I-INDEPENDENT-WORLD-ADAPTER-R1/00_INDEPENDENT_VERDICT.md'),('E04N','644a68b76042309be71f0eb65fabc4a6903f15b8','WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-E04N-FULL-NATIVE-INDEPENDENT-R1/00_FULL_NATIVE_VERDICT.md'),('E04S','6549105c5757d38e15e5f52202a03e1ecad389e8','WORKER_RETURNS/PYAT-USERDIRECT-20261016-R14-E04S-INDEPENDENT-NATIVE-CACHE-R1/00_INDEPENDENT_VERDICT.md')]:put(c,p,'inputs/'+label+'/'+p.rsplit('/',1)[1])
paths=['PYAT_CONTROL_ROOM/00_READ_ME_FIRST.md','PYAT_CONTROL_ROOM/00D_WARM_EXECUTION_PASSPORT_AND_MONEY_FIRST_AGENT_DISPENSATION_R1.md','PYAT_CONTROL_ROOM/26_HQD216_PRODUCTIVE_ADEQUACY_AND_PREV3_EMPIRICAL_GATE_LAW.md','PYAT_CONTROL_ROOM/00_INCOMING_HQ_VALIDITY_AND_PERSONA_END_PRODUCT_GATE_R1.md','CROSS_HQ_CONTROL_ROOM/HQ_GROK_AND_PROGRESS_PROTOCOL_R1.md','PYAT_CONTROL_ROOM/CURRENT_PROGRESS.json','PYAT_CONTROL_ROOM/CURRENT_PROGRESS.md','SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json','SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md','HQ_HANDOFF/LATEST.json','PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md']
for label,c in [('startup','c44367ee7734160b7387d3f3956158a3c4a00e12'),('canonical','0d551d36ff19dc9806e0ad490ff33a1e4c25e381')]:
 for p in paths:put(c,p,'authority/'+label+'/'+p)
(R/'input_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Pinned evidence/authority objects',len(manifest))
