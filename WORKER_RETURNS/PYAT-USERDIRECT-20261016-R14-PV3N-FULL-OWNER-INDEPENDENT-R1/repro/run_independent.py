from pathlib import Path
import subprocess,os,sys,json
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root';E=R/'evidence/independent';E.mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[R/'repro',C/'repro',RT,RT/'candidate/repro',C/'frozen_pv2i/repro'])),PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PV2_RUNTIME_ROOT=str(RT),PV_RETURN=str(RT/'prior_PV'))
cmd=[sys.executable,'-m','pytest',str(R/'repro/test_independent.py'),'-vv','--tb=short','--import-mode=importlib','-p','no:cacheprovider','--basetemp='+str(R/'runtime/independent_tmp'),'--junitxml='+str(E/'junit.xml')]
p=subprocess.run(cmd,env=env,cwd=RT,capture_output=True,text=True)
(E/'stdout.log').write_text(p.stdout+p.stderr);(E/'execution.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode),indent=2)+'\n');print(p.stdout[-5000:]+p.stderr);raise SystemExit(p.returncode)
