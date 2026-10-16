from bootstrap import ROOT,RT
import subprocess,sys,time,json,os
O=ROOT/'observations';O.mkdir(exist_ok=True)
args=[sys.executable,'-m','pytest','-q','tests/test_method_handoff.py','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/handoff.xml']
t=time.monotonic();p=subprocess.run(args,cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'),capture_output=True,text=True)
# Full raw process output stays local/ignored; public receipts use relative
# aliases so environment passports/logs disclose no personal filesystem root.
(RT/'pytest_raw.stdout').write_text(p.stdout+'\n'+p.stderr)
public=(p.stdout+'\n'+p.stderr).replace(str(ROOT),'<RETURN>').replace(str(sys.executable),'<PYTHON>')
(O/'handoff.stdout').write_text(public)
(O/'handoff.terminal.json').write_text(json.dumps(dict(argv=['python3',*args[1:]],cwd='RETURN',exit=p.returncode,seconds=time.monotonic()-t,sourcefree=True,scope='FRESH_E05A_HANDOFF_ONLY__E05S_403_NOT_RERUN'),indent=2)+'\n')
print(public);raise SystemExit(p.returncode)
