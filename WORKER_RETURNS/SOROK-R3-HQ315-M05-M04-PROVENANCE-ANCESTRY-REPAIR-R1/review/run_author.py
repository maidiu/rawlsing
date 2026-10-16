from pathlib import Path
import subprocess,sys,os,json,hashlib
R=Path(__file__).resolve().parents[1];freeze=json.loads((R/'03_AUTHOR_FREEZE.json').read_text())
for p,h in freeze['files'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
out=R/'evidence/m05_author';out.mkdir(exist_ok=True)
cmd=[sys.executable,'-m','pytest',str(R/'review/test_m05_author.py'),'-vv','--tb=short','--noconftest','-p','no:cacheprovider','--import-mode=importlib','--rootdir='+str(R),'--confcutdir='+str(R),'--junitxml='+str(out/'junit.xml')]
p=subprocess.run(cmd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
(out/'stdout.log').write_text(p.stdout+p.stderr);(out/'execution.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode),indent=2)+'\n');print('\n'.join((p.stdout+p.stderr).splitlines()[-6:]));raise SystemExit(p.returncode)
