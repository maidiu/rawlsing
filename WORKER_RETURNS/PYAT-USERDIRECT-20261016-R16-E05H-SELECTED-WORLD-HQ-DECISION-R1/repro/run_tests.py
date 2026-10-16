from bootstrap import ROOT
import subprocess,sys,os,json,time
args=[sys.executable,'-m','pytest','-q','tests/test_preview.py','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/preview.xml']
t=time.monotonic();p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'))
text=(p.stdout+'\n'+p.stderr).replace(str(ROOT),'<RETURN>')
(ROOT/'observations/preview.stdout').write_text(text)
(ROOT/'observations/preview.terminal.json').write_text(json.dumps(dict(argv=['python3',*args[1:]],cwd='RETURN',exit=p.returncode,seconds=time.monotonic()-t,scope='E05H_INCREMENTAL_PREVIEW_ONLY__403_NOT_RERUN'),indent=2)+'\n')
print(text);raise SystemExit(p.returncode)
