import json,pathlib,subprocess,sys,os,time,shutil
RET=pathlib.Path(__file__).resolve().parents[1];sel=json.loads((RET/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text());runtime=pathlib.Path(sel['runtime']);ledger=runtime/'cold-independent-ledger';results=[]
for phase in ['first','replay']:
 for suffix in ['.json','.log','_imports.json','_executed_sources.json']:
  p=RET/'repro'/('cold_'+phase+suffix)
  if p.exists():shutil.copyfile(p,p.with_name('pre_trace_'+p.name))
 cmd=[sys.executable,str(RET/'repro/cold_independent.py'),str(ledger),phase];t=time.time()
 with (RET/'repro'/('cold_'+phase+'.log')).open('w') as f:
  r=subprocess.run(cmd,cwd=runtime,env=dict(os.environ,PYTHONPATH=str(runtime),PV_RUNTIME=str(runtime),PV_RETURN=str(RET),PV_SUITE='cold_'+phase,PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT)
 results.append(dict(suite='cold_'+phase,command=cmd,cwd=str(runtime),exit_code=r.returncode,seconds=time.time()-t));print((RET/'repro'/('cold_'+phase+'.log')).read_text())
(RET/'repro/cold_execution.json').write_text(json.dumps(results,indent=2))
