"""Exact Git-object-only staging, no author runtime or Desktop source copies."""
import subprocess, pathlib, json, hashlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]; REPO=ROOT.parents[1]
RT=ROOT/'runtime'; RT.mkdir(exist_ok=True)
START='e2f1b96a860d1555e072f1538eea5d913eef3b37'; E05='257dfaf41be7d2a88c11741851e9dc89363b5386'; E04='9c96f201f3530d2dae321201e9a913bb7a61800f';N9='9ab4a0192b7c951bb0b387637e6c74333246766c';E03='0e0ed50dbce2dd1434d3a3c84b937b9a956adba9'
P05='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R11-E05-SELECTED-WORLD-INSTALLATION-R1/';P04='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1/'
def git(*a):return subprocess.check_output(['git',*a],cwd=REPO)
manifest=[]
def stage(c,p,d):
 b=git('show',c+':'+p); out=RT/d;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 expected=git('rev-parse',c+':'+p).decode().strip();actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert expected==actual
 manifest.append(dict(commit=c,path=p,local=d,git_blob=expected,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
def paths(c,*p):return git('ls-tree','-r','--name-only',c,*p).decode().splitlines()
for p in paths(START,'rawlsing_next','tests'):stage(START,p,p)
for prefix in ['PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1','PYAT-C1-00-CONTRACT-CORRECTION-R2','PYAT-C1-00-CONTRACT-CORRECTION-R3','PYAT-C1-00-CONTRACT-CORRECTION-R8']:
 for p in paths(START,'WORKER_RETURNS/'+prefix):
  if p.endswith('.json'):stage(START,p,p)
for p in ['rawlsing_next/pre553_n9_n10w_progressive_candidate.py','rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py']:stage(E03,p,p)
for p in ['rawlsing_next/pre553_hq297_n9c_two_field_reader.py','tests/test_hq297_n9c_two_field_reader.py','WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json']:stage(N9,p,p)
for p in paths(E04,P04+'product'):stage(E04,p,p[len(P04):])
stage(E04,P04+'repro/test_product.py','_e04-candidate/repro/test_product.py')
stg=RT/'_e04-candidate';(stg/'runtime_root/source').mkdir(parents=True,exist_ok=True)
for n in ['rawlsing_next','tests']:
 d=stg/'runtime_root/source'/n
 if not d.exists():d.symlink_to(RT/n)
if not (stg/'product').exists():(stg/'product').symlink_to(RT/'product')
for p in paths(E05,P05):stage(E05,p,'_e05/'+p[len(P05):])
stage(E05,P05+'repro/e05_n9_selected_world_adapter.py','e05_n9_selected_world_adapter.py')
(ROOT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# No candidate imports. Freeze complete original native identities before any execution.
fixture=RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
(ROOT/'01_FROZEN_NATIVE_DEPENDENCY_IDENTITIES.json').write_text(json.dumps({'source_commit':N9,'original_registry':json.loads(fixture.read_text()),'method':'Exact original test-only records frozen before candidate import; refs verified by native suite, hashes are integrity not signer authority'},indent=2)+'\n')
print('Exact staged files',len(manifest));print('runtime',RT)
