import hashlib,io,json,os,pathlib,platform,subprocess,sys,tarfile,tempfile,time,shutil
ROOT=pathlib.Path(__file__).resolve().parents[3];RET=ROOT/'WORKER_RETURNS/PYAT-R3-HQ297-V2-ROLE-QUERY-SEMANTIC-BINDING-R1'
PV='WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1'
OWNER='3f91dc22d2eb863bc1d2facccfd33e6c05349503';CAND='d1283fb53b543471fe825e78d64bf5bd19efbf11';PARENT='694fb45085cd5e4891949921a44edb77c3f603f2'
stage=sys.argv[1];runtime=pathlib.Path(tempfile.mkdtemp(prefix='hq297-v2r-'+stage+'-')).resolve()
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
with tarfile.open(fileobj=io.BytesIO(git('archive',OWNER,'rawlsing_next','WORKER_RETURNS/PYAT-HQ282-P01-V2-DURABLE-CONSUMER-INTEGRATION-R1'))) as tf:tf.extractall(runtime)
origins={p.relative_to(runtime).as_posix():OWNER for p in runtime.rglob('*') if p.is_file()}
for commit,paths in [(CAND,['rawlsing_next/pre553_original_identity_v2k_successor_candidate.py','rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py']), (PARENT,['rawlsing_next/tests/test_postastra_pv_v2k_independent.py',PV+'/01_FROZEN_ORIGINAL_IDENTITY_ORACLES.json'])]:
 for rel in paths:
  p=runtime/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('show',commit+':'+rel));origins[rel]=commit
for p in (ROOT/'rawlsing_next').glob('pre553_hq297_v2r_*.py'):
 rel=p.relative_to(ROOT).as_posix();(runtime/rel).write_bytes(p.read_bytes());origins[rel]=None
rel='rawlsing_next/tests/test_hq297_v2r_role_query_binding.py';(runtime/rel).write_bytes((ROOT/rel).read_bytes());origins[rel]=None
scratch=runtime/PV;(scratch/'repro').mkdir(parents=True)
manifest=[]
for rel,c in sorted(origins.items()):
 raw=(runtime/rel).read_bytes();blob=git('rev-parse',c+':'+rel).decode().strip() if c else None
 if c:assert raw==git('show',c+':'+rel)
 manifest.append(dict(path=rel,commit=c,git_blob=blob,sha256=hashlib.sha256(raw).hexdigest(),byte_verified=True))
selector=dict(stage=stage,runtime=str(runtime),sealed_start='7ac4d464049d8451876732680d00d529be90fb89',owner=OWNER,candidate=CAND,PV=PARENT,files=manifest)
(scratch/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').write_text(json.dumps(selector,indent=2));(RET/'repro'/('selector_'+stage+'.json')).write_text(json.dumps(selector,indent=2))
# Inherited read-only exec/import auditing; actual helper subprocesses inherit it.
(runtime/'sitecustomize.py').write_bytes(git('show',PARENT+':'+PV+'/repro/pv_child_audit.py'))
cmd=[sys.executable,'-m','pytest','-q','--import-mode=importlib']
if stage=='red':cmd+=['rawlsing_next/tests/test_hq297_v2r_role_query_binding.py']
elif stage=='green':cmd+=['rawlsing_next/tests/test_hq297_v2r_role_query_binding.py']
elif stage=='regressions':cmd+=['rawlsing_next/tests/'+n for n in ['test_postastra_pv_v2k_independent.py','test_hq295_v2k_original_identity_successor.py','test_pre553_v2_durable_consumer_integration_candidate.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py','test_pre553_route_b_production.py','test_pre553_empirical_query.py','test_pre553_discovery_exact.py']]
else:raise ValueError(stage)
cmd+=['--junitxml='+str(RET/'repro'/f'{stage}.xml')]
env=dict(os.environ,PYTHONPATH=str(runtime),PV_RUNTIME=str(runtime),PV_RETURN=str(scratch),PV_SUITE=stage,V2R_STAGE='red' if stage=='red' else 'green',V2R_RETURN=str(RET),PYTHONDONTWRITEBYTECODE='1')
t=time.time()
with (RET/'repro'/f'{stage}.log').open('w') as f:run=subprocess.run(cmd,cwd=runtime,env=env,stdout=f,stderr=subprocess.STDOUT)
shutil.copytree(scratch/'repro',RET/'repro'/('audit_'+stage),dirs_exist_ok=True)
result=dict(stage=stage,command=cmd,cwd=str(runtime),environment={k:env[k] for k in ['PYTHONPATH','PV_RUNTIME','PV_RETURN','PV_SUITE','V2R_STAGE','V2R_RETURN']},exit_code=run.returncode,seconds=time.time()-t,python=sys.version,executable=sys.executable,host=platform.node())
(RET/'repro'/f'{stage}_execution.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print((RET/'repro'/f'{stage}.log').read_text()[-2500:])

if stage!='red' and run.returncode:sys.exit(run.returncode)
