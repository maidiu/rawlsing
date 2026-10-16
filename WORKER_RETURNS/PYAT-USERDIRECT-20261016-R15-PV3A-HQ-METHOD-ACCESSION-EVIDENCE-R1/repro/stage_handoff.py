"""Minimal Git-object reconstruction of PV3N-accepted owners and handoff controls.
Never executes the completed PV3N acceptance suites.
"""
import pathlib,subprocess,json,hashlib,shutil
R=pathlib.Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root'
manifest=[]
def git(*args):return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=R)
def stage(commit,path,dest,expected_blob=None,expected_sha=None):
 b=git('show',commit+':'+path);blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert blob==(expected_blob or git('rev-parse',commit+':'+path).decode().strip())
 sha=hashlib.sha256(b).hexdigest()
 if expected_sha:assert sha==expected_sha
 if dest.exists():assert dest.read_bytes()==b
 else:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 manifest.append(dict(commit=commit,path=path,local=str(dest.relative_to(R)),git_blob=blob,sha256=sha,bytes=len(b)))
for row in json.loads((R/'native_74_source_manifest.json').read_text())['files']:
 stage(row['commit'],row['source_path'],RT/row['staged_path'],row['git_blob_sha1'],row['sha256'])
rev='5c70c7d347998907c1c8a865f833dad581777a0e';prefix='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R12-PV3-INDEPENDENT-ROOT-CUSTODY-REPAIR-R1/'
for path in git('ls-tree','--full-tree','-r','--name-only',rev,prefix+'repro',prefix+'authority').decode().splitlines():stage(rev,path,C/path[len(prefix):])
rev='1de1c9c57bffa8bb663edd44af744379b028f698';prefix='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R11-PV2I-INDEPENDENT-ORIGINAL-SCOPE-R1/'
for path in git('ls-tree','--full-tree','-r','--name-only',rev,prefix+'repro',prefix+'tests',prefix+'01_FROZEN_ORIGINAL_EXPECTED_SET.json').decode().splitlines():stage(rev,path,C/'frozen_pv2i'/path[len(prefix):])
(R/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'evidence').mkdir(exist_ok=True)
print('Pinned original native74 plus exact PV3 install/API and PV2I input controls staged:',len(manifest))
