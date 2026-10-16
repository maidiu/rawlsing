"""Independent exact-object staging; no author runtime or Desktop-source copy."""
from pathlib import Path
import subprocess,json,hashlib,shutil
R=Path(__file__).resolve().parents[1];REPO=R.parents[1];RT=R/'runtime_root';RT.mkdir(exist_ok=False)
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=REPO)
rows=[]
def put(c,p,d,blob=None):
 b=git('show',c+':'+p);expected=git('rev-parse',c+':'+p).decode().strip()
 actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert actual==expected and (blob is None or blob==expected)
 dst=RT/d;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
 row=dict(commit=c,path=p,local=d,git_blob=actual,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b));rows.append(row)
selector=json.loads((R/'inputs/E04N/source_selector.json').read_text())
assert len(selector['files'])==94
for x in selector['files']:put(x['commit'],x['source_path'],x['staged_path'],x['git_blob_sha1'])
P='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R13-E04R-NATIVE-CACHE-INTEGRITY-REPAIR-R1/'
for p in git('ls-tree','-r','--name-only','97254d0b215b5dd45580dd94608a8ec95ff8b76f',P+'product').decode().splitlines():
 put('97254d0b215b5dd45580dd94608a8ec95ff8b76f',p,'repaired/'+p[len(P):])
(R/'source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
(R/'tests').mkdir(exist_ok=True);(R/'observations').mkdir(exist_ok=True)
for src,dst in [('inputs/E04N/tests/test_full_native_independent.py','tests/test_full_native_independent.py'),('inputs/E04N/repro/common.py','repro/common.py')]:
 shutil.copyfile(R/src,R/dst)
print('Staged exact original/native files',len(rows),'including 51 native manifest entries, six repaired product files')
