from bootstrap import ROOT
import subprocess,sys,os,json,time
args=[sys.executable,'-m','pytest','-q','tests/test_bridge.py','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/bridge.xml']
t=time.monotonic();p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'))
output=(p.stdout+'\n'+p.stderr).replace(str(ROOT),'<RETURN>')
(ROOT/'observations/bridge.stdout').write_text(output)
(ROOT/'observations/bridge.terminal.json').write_text(json.dumps(dict(argv=['python3',*args[1:]],cwd='RETURN',exit=p.returncode,seconds=time.monotonic()-t,scope='E06_NEW_INTEGRATION_CASES_ONLY__494_AND_403_NOT_RERUN'),indent=2)+'\n')
print(output);raise SystemExit(p.returncode)
