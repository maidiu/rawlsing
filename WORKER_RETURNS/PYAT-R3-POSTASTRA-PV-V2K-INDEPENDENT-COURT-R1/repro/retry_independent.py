import pathlib,json,shutil,hashlib,os,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[3];RET=ROOT/'WORKER_RETURNS/PYAT-R3-POSTASTRA-PV-V2K-INDEPENDENT-COURT-R1'
sel=json.loads((RET/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text());runtime=pathlib.Path(sel['runtime']);ind='rawlsing_next/tests/test_postastra_pv_v2k_independent.py'
for name in ['independent.log','independent.xml','independent_imports.json','independent_observations.jsonl']:
    p=RET/'repro'/name
    if p.exists():shutil.copyfile(p,p.with_name('initial_'+name))
(runtime/ind).write_bytes((ROOT/ind).read_bytes())
for row in sel['files']:
    if row['path']==ind:row['sha256']=hashlib.sha256((runtime/ind).read_bytes()).hexdigest()
(RET/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').write_text(json.dumps(sel,indent=2)+'\n')
(RET/'repro/independent_observations.jsonl').write_text('')
cmd=[sys.executable,str(runtime/'pv_pytest.py'),'-q',ind,'--import-mode=importlib','--junitxml='+str(RET/'repro/independent.xml')]
t=time.time()
with (RET/'repro/independent.log').open('w') as f:r=subprocess.run(cmd,cwd=runtime,env=dict(os.environ,PYTHONPATH=str(runtime),PV_RUNTIME=str(runtime),PV_RETURN=str(RET),PV_SUITE='independent',PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT)
e=json.loads((RET/'repro/execution.json').read_text());e['suites'].append(dict(suite='independent_corrected_fixture',command=cmd,cwd=str(runtime),exit_code=r.returncode,seconds=time.time()-t));(RET/'repro/execution.json').write_text(json.dumps(e,indent=2))
print((RET/'repro/independent.log').read_text())
