from pathlib import Path
import sys,os,subprocess,json,time
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';mode=sys.argv[1]
(RT/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'candidate/repro',R/'repro'])),PV_RETURN=str(RT/'prior_PV'),PV2_RUNTIME_ROOT=str(RT),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
tests={'pv2_33':[str(RT/'candidate/tests/test_pv2_original_scope_binding.py')],'v2k_24':['rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py'],'pv_21':['rawlsing_next/tests/test_postastra_pv_v2k_independent.py'],'owners_111':['rawlsing_next/tests/'+x+'.py' for x in ['test_pre553_v2_durable_consumer_integration_candidate','test_pre553_original_workload_v2_mutation_hostiles_candidate','test_pre553_route_b_production','test_pre553_empirical_query','test_pre553_discovery_exact']],'independent':[str(R/'tests')]}
cmd=[sys.executable,'-m','pytest',*tests[mode],'-vv','--tb=short','--assert=plain','--import-mode=importlib','-p','no:cacheprovider',f'--basetemp={RT}/tmp/{mode}',f'--junitxml={R}/observations/{mode}.xml'] if mode in tests else [sys.executable,str(R/'repro'/(mode+'.py')),*sys.argv[2:]]
if mode=='owners_111':env['PV2I_AUDIT_DIR']=str(R/'observations/owners_111_child_audits')
t=time.time();p=subprocess.run(cmd,cwd=RT,env=env,capture_output=True,text=True)
(R/f'observations/{mode}.stdout').write_text(p.stdout+p.stderr);(R/f'observations/{mode}.terminal.json').write_text(json.dumps({'argv':cmd,'cwd':str(RT),'PYTHONPATH':env['PYTHONPATH'],'exit':p.returncode,'seconds':time.time()-t},indent=2)+'\n');print(mode,'EXIT',p.returncode);print('\n'.join((p.stdout+p.stderr).splitlines()[-8:]));sys.exit(p.returncode)
