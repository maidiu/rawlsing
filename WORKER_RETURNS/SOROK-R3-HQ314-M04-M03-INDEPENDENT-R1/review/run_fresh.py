"""Run immutable independent tests, retaining pytest's real exit (including REDs)."""
from pathlib import Path
import json,hashlib,subprocess,sys,os
R=Path(__file__).resolve().parents[1]
freeze=json.loads((R/'03_FREEZE_MANIFEST.json').read_text())
for p,h in freeze['files'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h
out=R/'evidence/fresh';out.mkdir(parents=True,exist_ok=True)
cmd=[sys.executable,'-m','pytest',str(R/'review/test_falsifiers.py'),'-vv','--tb=short','--import-mode=importlib','-p','no:cacheprovider','--rootdir='+str(R),'--confcutdir='+str(R),'--basetemp='+str(R/'runtime/tmp/m04'),'--junitxml='+str(out/'junit.xml')]
(out/'command.json').write_text(json.dumps(dict(freeze_commit='3b529996ddd05c3c84225d2054428ff943091aef',command=cmd),indent=2)+'\n')
p=subprocess.run(cmd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
(out/'stdout.log').write_text(p.stdout+p.stderr)
(out/'execution.json').write_text(json.dumps(dict(pytest_exit=p.returncode,frozen_test_unchanged=hashlib.sha256((R/'review/test_falsifiers.py').read_bytes()).hexdigest()==freeze['files']['review/test_falsifiers.py']),indent=2)+'\n')
print('\n'.join((p.stdout+p.stderr).splitlines()[-14:]))
raise SystemExit(p.returncode)
