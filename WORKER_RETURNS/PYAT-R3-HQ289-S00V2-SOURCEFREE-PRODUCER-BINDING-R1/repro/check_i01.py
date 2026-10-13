"""Compatibility evidence only; an implementer cannot independently adopt."""
import hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=pathlib.Path(__file__).resolve().parent
ACCEPTED=pathlib.Path('/Users/matthewsmith/.codex/worktrees/hq288-i01r-independent/Rawlsing')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ACCEPTED,text=True).strip()=='473b7997d1b446c54a2d8688f94053b6c8670881'
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(OUT/'i01_overlay')+os.pathsep+str(ACCEPTED),'S00V2_SEAM_PATH':str(ROOT/'rawlsing_next/r3_s02_seam_witness.py'),'S00V2_I01_ROOT':str(ACCEPTED)}
records=[]
for label,test in [('i01_author_compatibility','test_hq287_i01_sourcefree_world_lifecycle.py'),('i01_independent_previous_court','test_hq288_i01r_independent_product.py')]:
 cmd=[sys.executable,'-m','pytest',str(ACCEPTED/'rawlsing_next/tests'/test),'-q','-p','no:cacheprovider','--junitxml='+str(OUT/(label+'.xml'))]
 p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(OUT/(label+'.log')).write_text(p.stdout)
 records.append(dict(label=label,argv=cmd,cwd=str(ROOT),environment={k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','PYTHONPATH','S00V2_SEAM_PATH','S00V2_I01_ROOT')},exit=p.returncode));print(label,p.returncode,p.stdout.splitlines()[-1],flush=True)
cmd=[sys.executable,str(ACCEPTED/'WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1/repro/emit_product.py'),str(OUT/'i01_product')]
p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(OUT/'i01_product.log').write_text(p.stdout)
records.append(dict(label='i01_product',argv=cmd,cwd=str(ROOT),exit=p.returncode,environment={k:env[k] for k in ('PYTHONDONTWRITEBYTECODE','PYTHONPATH','S00V2_SEAM_PATH','S00V2_I01_ROOT')}));print('i01_product',p.returncode,p.stdout,flush=True)
(OUT/'i01_commands.json').write_text(json.dumps(records,indent=2)+'\n')
