"""Execute unchanged original courts in fresh processes and preserve phase evidence."""
from pathlib import Path
import subprocess,sys,os,shutil,json,xml.etree.ElementTree as E,time
R=Path(__file__).resolve().parents[1];M2=R/'runtime/m02';M1=M2/'runtime/m01';phase=sys.argv[1];assert phase in ['before','after']
O=R/'evidence'/phase;O.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONPATH=str(M2/'repro'),TMPDIR=str(R/'runtime/tmp'))
commands=[('inherited413',[sys.executable,str(M1/'repro/run.py')],M1/'evidence'),('m02_100',[sys.executable,str(M2/'repro/run_independent.py')],M2/'evidence/independent'),('m03_74',[sys.executable,str(R/'repro/run_author.py')],R/'evidence/author'),('m04_51',[sys.executable,'-m','pytest',str(R/'review/test_falsifiers.py'),'-vv','--tb=short','--import-mode=importlib','-p','no:cacheprovider','--rootdir='+str(R),'--confcutdir='+str(R),'--basetemp='+str(R/'runtime/tmp'/('m04_'+phase)),'--junitxml='+str(R/'evidence/fresh/junit.xml')],R/'evidence/fresh')]
(R/'evidence/fresh').mkdir(exist_ok=True)
results=[]
for name,cmd,source in commands:
 t=time.monotonic();p=subprocess.run(cmd,cwd=R.parents[1],env=env,capture_output=True,text=True);dest=O/name
 shutil.copytree(source,dest,dirs_exist_ok=True)
 (dest/'launcher.stdout').write_text(p.stdout+p.stderr)
 counts={k:0 for k in ['tests','failures','errors','skipped']}
 for f in dest.rglob('junit.xml'):
  for ts in E.parse(f).getroot().iter('testsuite'):
   for k in counts:counts[k]+=int(ts.get(k,0))
 row=dict(suite=name,command=cmd,exit=p.returncode,seconds=time.monotonic()-t,counts=counts);results.append(row);print(name,p.returncode,counts,flush=True)
 expected=10 if phase=='before' and name=='m04_51' else 0
 assert counts==dict(tests={'inherited413':413,'m02_100':100,'m03_74':74,'m04_51':51}[name],failures=expected,errors=0,skipped=0)
 assert p.returncode==(1 if expected else 0)
(O/'execution.json').write_text(json.dumps(results,indent=2)+'\n')
