"""Run the frozen suites and additional regressions with declared process exits."""
import subprocess,sys,os,pathlib,json,time,xml.etree.ElementTree as ET,hashlib
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations';O.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro'])))
commands=[('original_271',[sys.executable,str(R/'repro/run_suites.py')]),('independent_55',[sys.executable,'-m','pytest','-q',str(R/'tests/test_independent_court.py'),'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/'repaired_independent.xml')]),('additional',[sys.executable,'-m','pytest','-q',str(R/'tests/test_e05r_repair.py'),'--noconftest','--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/'e05r_additional.xml')]),('cold',[sys.executable,str(R/'repro/run_cold.py')])]
results=[]
for name,cmd in commands:
 t=time.monotonic();p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True)
 (O/(name+'_runner.log')).write_text(p.stdout+'\n'+p.stderr)
 results.append(dict(name=name,argv=cmd,cwd=str(R),exit=p.returncode,elapsed_seconds=time.monotonic()-t))
 print(name,p.returncode,p.stdout[-600:],p.stderr[-600:],flush=True)
(R/'process_exits.json').write_text(json.dumps(dict(processes=results,adapter_sha256=hashlib.sha256((R/'candidate/e05r_selected_world_adapter.py').read_bytes()).hexdigest()),indent=2)+'\n')
if any(r['exit'] for r in results):
 raise SystemExit(1)
subprocess.run([sys.executable,str(R/'repro/verify_artifacts.py')],cwd=R,env=env,check=True)

# Verify terminal identities and counts after successful suite/cold execution.
