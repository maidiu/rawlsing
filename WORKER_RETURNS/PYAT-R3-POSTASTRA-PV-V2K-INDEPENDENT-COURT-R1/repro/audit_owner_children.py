import pathlib,json,os,subprocess,sys,shutil,time
RET=pathlib.Path(__file__).resolve().parents[1];sel=json.loads((RET/'02_EXACT_COMPOSITE_SOURCE_SELECTOR.json').read_text());runtime=pathlib.Path(sel['runtime'])
(runtime/'sitecustomize.py').write_bytes((RET/'repro/pv_child_audit.py').read_bytes())
for suffix in ['.log','.xml','_imports.json','_executed_sources.json']:
 p=RET/'repro'/('owners'+suffix)
 if p.exists():shutil.copyfile(p,p.with_name('pre_child_'+p.name))
tests=['rawlsing_next/tests/'+p for p in ['test_pre553_v2_durable_consumer_integration_candidate.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py','test_pre553_route_b_production.py','test_pre553_empirical_query.py','test_pre553_discovery_exact.py']]
cmd=[sys.executable,str(runtime/'pv_pytest.py'),'-q',*tests,'--import-mode=importlib','--junitxml='+str(RET/'repro/owners.xml')];t=time.time()
with (RET/'repro/owners.log').open('w') as f:r=subprocess.run(cmd,cwd=runtime,env=dict(os.environ,PYTHONPATH=str(runtime),PV_RUNTIME=str(runtime),PV_RETURN=str(RET),PV_SUITE='owners',PYTHONDONTWRITEBYTECODE='1'),stdout=f,stderr=subprocess.STDOUT)
(RET/'repro/child_execution.json').write_text(json.dumps([dict(suite='owners_child_import_audit',command=cmd,cwd=str(runtime),exit_code=r.returncode,seconds=time.time()-t)],indent=2))
print((RET/'repro/owners.log').read_text())
