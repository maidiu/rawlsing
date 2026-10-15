from pathlib import Path
import sys,os,subprocess,json,time
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root'
mode=sys.argv[1]
paths={'author29':[RT/'WG0P2/repro/test_wg0p2_repair.py'],'author36':[RT/'WG0P3/tests/test_wg0p3_repair.py'],'wg0k_full_historical':[RT/'WG0K/repro/test_wg0k_full_module_hostiles.py'],'phase_a':[R/'tests/test_phase_a_environment.py']}
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'WG0P2/repro',RT/'WG0P3/repro',R/'repro'])),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
cmd=[sys.executable,'-m','pytest',*map(str,paths[mode]),'-vv','--tb=short','--assert=plain',f'--junitxml={R}/observations/{mode}.xml']
t=time.time();p=subprocess.run(cmd,cwd=RT,env=env,capture_output=True,text=True)
(R/f'observations/{mode}.stdout').write_text(p.stdout+p.stderr)
(R/f'observations/{mode}.terminal.json').write_text(json.dumps({'qualification':'PHASE_A_HISTORICAL_OWNER_OR_ENVIRONMENT_ONLY_NOT_WG0P4','argv':cmd,'cwd':str(RT),'PYTHONPATH':env['PYTHONPATH'],'exit':p.returncode,'elapsed':time.time()-t},indent=2)+'\n')
print(mode,'EXIT',p.returncode);print('\n'.join(p.stdout.splitlines()[-4:]));sys.exit(p.returncode)
