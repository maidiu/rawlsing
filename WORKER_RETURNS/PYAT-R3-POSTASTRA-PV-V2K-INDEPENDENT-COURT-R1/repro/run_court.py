"""Exact Git composite; all suite failures retained; no owner code edits."""
import hashlib, importlib, json, os, pathlib, platform, subprocess, sys, tarfile, tempfile, time
ROOT=pathlib.Path(__file__).resolve().parents[3]
RET=ROOT/'WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1'
START='ce760f231cb5ae0678e39f9d12798997f8b6da27';CAND='d1283fb53b543471fe825e78d64bf5bd19efbf11';OWNER='3f91dc22d2eb863bc1d2facccfd33e6c05349503'
RUNTIME=pathlib.Path(tempfile.mkdtemp(prefix='postastra-pv-runtime-')).resolve()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
archive=git('archive',OWNER,'rawlsing_next','WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1')
import io
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(RUNTIME)
for p in ['rawlsing_next/pre553_original_identity_v2k_successor_candidate.py','rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py']:
    (RUNTIME/p).write_bytes(git('show',CAND+':'+p))
    assert git('show',START+':'+p)==(RUNTIME/p).read_bytes()
ind='rawlsing_next/tests/test_postastra_pv_v2k_independent.py'
(RUNTIME/ind).write_bytes((ROOT/ind).read_bytes())
manifest=[]
for p in sorted(RUNTIME.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(RUNTIME).as_posix();commit=CAND if rel in ['rawlsing_next/pre553_original_identity_v2k_successor_candidate.py','rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py'] else OWNER
    if rel==ind: commit=None;blob=None
    else:
        blob=git('rev-parse',commit+':'+rel).decode().strip()
        assert git('show',commit+':'+rel)==p.read_bytes()
    manifest.append(dict(path=rel,commit=commit,git_blob=blob,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),byte_verified=True))
selector=dict(schema='POSTASTRA_PV_EXACT_COMPOSITE@1',sealed_start=START,candidate_commit=CAND,owner_commit=OWNER,runtime=str(RUNTIME),files=manifest,policy='All original owners/tests from fixed owner archive; candidate and its test from fixed candidate blobs; independent test from owned reviewer terrain only.')
(RET/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').write_text(json.dumps(selector,indent=2)+'\n')
# This plugin records the actual modules that pytest loaded, including helpers.
plugin=RUNTIME/'pv_import_audit.py'
plugin.write_text('''import sys,pathlib,json,hashlib,os
class Audit:
 def __init__(self): self.executed=set()
 def trace(self,frame,event,arg):
  if event=='call' and frame.f_code.co_filename.startswith(os.environ['PV_RUNTIME']): self.executed.add(frame.f_code.co_filename)
 def pytest_sessionstart(self,session): sys.setprofile(self.trace)
 def pytest_sessionfinish(self,session,exitstatus):
  sys.setprofile(None)
  rows=[];base=pathlib.Path(os.environ['PV_RUNTIME']).resolve()
  selector=json.loads(pathlib.Path(os.environ['PV_RETURN'],'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text())
  pinned={r['path']:r for r in selector['files']}
  for name,m in sorted(sys.modules.items()):
   f=getattr(m,'__file__',None)
   if not f:continue
   p=pathlib.Path(f).resolve()
   if not p.is_relative_to(base):
    assert not name.startswith('rawlsing_next'),(name,p)
    continue
   rel=p.relative_to(base).as_posix()
   if rel not in pinned:continue
   sha=hashlib.sha256(p.read_bytes()).hexdigest();ref=pinned[rel]
   assert sha==ref['sha256'],(name,p)
   rows.append(dict(module=name,file=str(p),sha256=sha,git_blob=ref['git_blob'],commit=ref['commit'],match=True))
  pathlib.Path(os.environ['PV_RETURN'],'repro',os.environ['PV_SUITE']+'_imports.json').write_text(json.dumps(rows,indent=2))
  executed=[]
  for f in sorted(self.executed):
   p=pathlib.Path(f).resolve();rel=p.relative_to(base).as_posix()
   if rel not in pinned:continue
   ref=pinned[rel];sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==ref['sha256']
   executed.append(dict(file=str(p),path=rel,sha256=sha,git_blob=ref['git_blob'],commit=ref['commit'],match=True))
  pathlib.Path(os.environ['PV_RETURN'],'repro',os.environ['PV_SUITE']+'_executed_sources.json').write_text(json.dumps(executed,indent=2))
''')
runner=RUNTIME/'pv_pytest.py';runner.write_text('import pytest,sys\nfrom pv_import_audit import Audit\nsys.exit(pytest.main(sys.argv[1:],plugins=[Audit()]))\n')
(RUNTIME/'sitecustomize.py').write_bytes((RET/'repro/pv_child_audit.py').read_bytes())
env=dict(os.environ,PYTHONPATH=str(RUNTIME),PV_RUNTIME=str(RUNTIME),PV_RETURN=str(RET),PYTHONDONTWRITEBYTECODE='1')
suites=[('independent',[ind]),('candidate',['rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py']),('owners',['rawlsing_next/tests/'+p for p in ['test_pre553_v2_durable_consumer_integration_candidate.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py','test_pre553_route_b_production.py','test_pre553_empirical_query.py','test_pre553_discovery_exact.py']])]
results=[]
for name,tests in suites:
    cmd=[sys.executable,str(runner),'-q',*tests,'--import-mode=importlib','--junitxml='+str(RET/'repro'/f'{name}.xml')]
    t=time.time()
    with (RET/'repro'/f'{name}.log').open('w') as out:
        run=subprocess.run(cmd,cwd=RUNTIME,env=dict(env,PV_SUITE=name),stdout=out,stderr=subprocess.STDOUT)
    results.append(dict(suite=name,command=cmd,cwd=str(RUNTIME),exit_code=run.returncode,seconds=time.time()-t))
    print(name,run.returncode,(RET/'repro'/f'{name}.log').read_text()[-1800:],flush=True)
(RET/'repro/final_execution.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,host=platform.node(),suites=results),indent=2))
print('RUNTIME',RUNTIME)
