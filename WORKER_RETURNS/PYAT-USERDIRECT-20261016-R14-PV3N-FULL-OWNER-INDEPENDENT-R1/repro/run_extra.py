from pathlib import Path
import subprocess,sys,os,json
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root';E=R/'evidence/extra';E.mkdir(exist_ok=True)
cmd=[sys.executable,'-m','pytest',str(R/'repro/test_extra.py'),'-vv','--tb=short','--import-mode=importlib','-p','no:cacheprovider','--basetemp='+str(R/'runtime/extra_tmp'),'--junitxml='+str(E/'junit.xml')]
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[R/'repro',C/'repro',RT,RT/'candidate/repro',C/'frozen_pv2i/repro'])),PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1')
p=subprocess.run(cmd,env=env,capture_output=True,text=True,cwd=RT);(E/'stdout.log').write_text(p.stdout+p.stderr);(E/'execution.json').write_text(json.dumps(dict(argv=cmd,exit=p.returncode),indent=2)+'\n');print(p.stdout[-5000:]+p.stderr);raise SystemExit(p.returncode)
