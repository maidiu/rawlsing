import pathlib,json,os,sys,subprocess,time,hashlib
RET=pathlib.Path(__file__).resolve().parents[1];ROOT=RET.parents[1];RT=RET/'runtime_root';CP='WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1';CAND=RT/CP
stage=sys.argv[1]
if stage=='independent':
    p=RT/'independent/test_rc0_hostile.py';p.parent.mkdir(exist_ok=True);p.write_bytes((RET/'reviewer_tests/test_rc0_hostile.py').read_bytes())
if (RT/'sitecustomize.py').read_bytes()!=(RET/'repro/sitecustomize.py').read_bytes():
    (RT/'sitecustomize.py').write_bytes((RET/'repro/sitecustomize.py').read_bytes())
suites={'smoke':[CP+'/port/test_k9_provider_swap.py::test_k9_01_two_providers_same_meaning',CP+'/port/test_k10_structural_conservation.py::test_k10_03_dyadize_nary'],
'k9':[CP+'/port/test_k9_provider_swap.py'],'k10':[CP+'/port/test_k10_structural_conservation.py'],
'n10e_c1':[CP+'/staging/ns/rawlsing_next/tests/test_pre553_empirical_possibility_provider.py',CP+'/staging/ns/rawlsing_next/tests/test_pre553_analytical_composition.py'],
'pe':[CP+'/staging/ns/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py'],
'hq297':[CP+'/staging/ns/rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py'],
'independent':['independent/test_rc0_hostile.py']}
paths=[RT,CAND,CAND/'staging/ns',CAND/'staging/ns/rawlsing_next/tests',RT/'rawlsing_next/tests']
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,paths)),PYTHONDONTWRITEBYTECODE='1',RC0_RUNTIME=str(RT),RC0_RETURN=str(RET),RC0_SUITE=stage,HQ297_EXACT_PE_ROOT=str(CAND/'staging/ns'))
cmd=[sys.executable,'-m','pytest',*suites[stage],'-q','-p','no:cacheprovider','--junitxml='+str(RET/'repro'/f'{stage}.xml')]
t=time.time()
with (RET/'repro'/f'{stage}.raw.log').open('w') as f:r=subprocess.run(cmd,cwd=RT,env=env,stdout=f,stderr=subprocess.STDOUT)
log=(RET/'repro'/f'{stage}.raw.log').read_text();san=lambda s:str(s).replace(str(RT),'$RC0_RUNTIME').replace(str(RET),'$RC0_RETURN').replace(str(ROOT),'$WORKTREE')
(RET/'repro'/f'{stage}.log').write_text(san(log));(RET/'repro'/f'{stage}.raw.log').unlink()
# JUnit portability: keep actual assertions/case counts; normalize only absolute terrain aliases.
x=RET/'repro'/f'{stage}.xml'
if x.exists():x.write_text(san(x.read_text()))
result=dict(suite=stage,command=[san(v) for v in cmd],cwd='$RC0_RUNTIME',exit_code=r.returncode,seconds=time.time()-t,python=sys.version,pytest='9.0.2',raw_stdout_sha256=hashlib.sha256(log.encode()).hexdigest(),stdout_path=f'repro/{stage}.log',junit_path=f'repro/{stage}.xml',path_normalization_only=True)
(RET/'repro'/f'{stage}_execution.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));print(san(log[-3000:]))
