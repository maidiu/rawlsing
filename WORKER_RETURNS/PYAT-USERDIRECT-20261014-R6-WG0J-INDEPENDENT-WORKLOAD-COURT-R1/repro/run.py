"""Exact-source subprocess harness; no substitutes or owner patches."""
from pathlib import Path
import os,sys,subprocess,json,time
R=Path(__file__).resolve().parents[1]; RT=R/'runtime_root'
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'candidate/repro',R/'repro'])),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
name=sys.argv[1]
commands={'author':[sys.executable,'-m','pytest',str(RT/'candidate/repro/test_wg0p2_repair.py'),'-vv','--tb=short','--assert=plain',f'--junitxml={R}/observations/author.xml'], 'independent':[sys.executable,'-m','pytest',str(R/'tests'),'-vv','--tb=short','--assert=plain',f'--junitxml={R}/observations/independent.xml'], 'experiments':[sys.executable,str(R/'repro/experiments.py')], 'probe':[sys.executable,str(R/'repro/probe.py')], 'cold':[sys.executable,str(R/'repro/cold.py'),*sys.argv[2:]]}
t=time.time(); p=subprocess.run(commands[name],cwd=RT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
(R/'observations'/f'{name}.stdout').write_text(p.stdout)
(R/'observations'/f'{name}.terminal.json').write_text(json.dumps({'argv':commands[name],'cwd':str(RT),'PYTHONPATH':env['PYTHONPATH'],'exit':p.returncode,'seconds':time.time()-t},indent=2)+'\n')
print(p.stdout);print('TERMINAL_EXIT',p.returncode);sys.exit(p.returncode)
