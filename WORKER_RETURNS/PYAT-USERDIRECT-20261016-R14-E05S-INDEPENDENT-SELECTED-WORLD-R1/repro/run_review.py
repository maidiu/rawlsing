"""Full portable R14 execution, preserving independent and author suite labels."""
import sys,os,pathlib,subprocess,json,time
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations';O.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro'])))
commands=[('stage',[sys.executable,'repro/stage.py']),('activate',[sys.executable,'repro/activate_candidate.py']),('original271',[sys.executable,'repro/run_suites.py']),('frozen55',[sys.executable,'-m','pytest','-q','tests/test_independent_court.py','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/frozen55.xml']),('reviewer45',[sys.executable,'-m','pytest','-q','tests/test_r14_independent.py','--noconftest','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/reviewer45.xml']),('author32',[sys.executable,'-m','pytest','-q','tests/test_e05r_repair.py','--noconftest','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/author_additional.xml']),('native_probe',[sys.executable,'repro/r14_native_probe.py']),('C11_reconstruction',[sys.executable,'repro/r14_reconstruct.py']),('cold_replay',[sys.executable,'repro/run_cold.py']),('cold_prepare',[sys.executable,'repro/r14_cold.py','prepare']),('cold_restart',[sys.executable,'repro/r14_cold.py','restart'])]
results=[]
for label,cmd in commands:
 t=time.monotonic();p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True)
 (O/(label+'_runner.log')).write_text(p.stdout+'\n'+p.stderr);results.append(dict(label=label,command=cmd,cwd=str(R),exit=p.returncode,elapsed_seconds=time.monotonic()-t));print(label,p.returncode,flush=True)
 (R/'reproduction_process_exits.json').write_text(json.dumps(results,indent=2)+'\n')
 if p.returncode:raise SystemExit(p.returncode)
