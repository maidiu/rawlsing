"""Fresh independent executions; never reads or reuses author execution state."""
from pathlib import Path
import os,sys,subprocess,shutil,json,time,hashlib
ROOT=Path(__file__).resolve().parent
RUN=ROOT/'.scratch/b3a';OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
COMMON=subprocess.check_output(['git','rev-parse','--path-format=absolute','--git-common-dir'],cwd=ROOT).decode().strip()
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_DIR=COMMON)
def run(label,args,cwd,expected=0,extra=None):
 env=dict(ENV,**(extra or {}));start=time.time();p=subprocess.run(list(map(str,args)),cwd=cwd,env=env,text=True,capture_output=True)
 (OUT/(label+'.log')).write_text(p.stdout+p.stderr)
 f=OUT/'commands.json';rows=json.loads(f.read_text()) if f.exists() else []
 rows.append(dict(label=label,args=list(map(str,args)),cwd=str(cwd),environment_overrides=extra or {},exit=p.returncode,expected=expected,elapsed_seconds=time.time()-start));f.write_text(json.dumps(rows,indent=2)+'\n')
 print(label,'exit',p.returncode,'expected',expected,flush=True)
 if p.returncode!=expected:print((p.stdout+p.stderr)[-2000:],flush=True);raise RuntimeError(label)
def main():
 candidate=RUN/'candidate';frozen=RUN/'frozen_b3'
 assert (candidate/'.runtime').is_dir() and (frozen/'.runtime').is_dir(),'Run prepare_review.py in a new checkout first'
 if '--seeded' in sys.argv:
  for label,base,expected in [('original_seeded',frozen,1),('candidate_seeded',candidate,0)]:
   run(label,[sys.executable,'-m','pytest','-q',ROOT/'test_seeded_refusals.py','--junitxml='+str(OUT/(label+'.xml'))],ROOT,expected,dict(REVIEW_B3_ROOT=str(base),REVIEW_EVIDENCE=str(OUT/(label+'_sql'))))
  return
 if '--hostiles' in sys.argv:
  run('reviewer_hostiles',[sys.executable,'-m','pytest','-q',ROOT/'test_reviewer_hostiles.py','--junitxml='+str(OUT/'reviewer_hostiles.xml')],ROOT,1,dict(REVIEW_B3_ROOT=str(candidate),REVIEW_EVIDENCE=str(OUT/'reviewer_sql')));return
 run('inherited',[sys.executable,'run_inherited.py'],frozen)
 shutil.copytree(frozen/'evidence/inherited',OUT/'inherited',dirs_exist_ok=True)
 for label,base in [('frozen_b3',frozen),('candidate_b3',candidate)]:
  (base/'evidence').mkdir(exist_ok=True)
  run(label,[sys.executable,'-m','pytest','-q','test_integration_b3.py','--junitxml='+str(OUT/(label+'.xml'))],base)
 for label,base in [('original_x3',frozen),('candidate_x3',candidate)]:
  run(label,[sys.executable,'-m','pytest','-q',RUN/'frozen_x3/test_independent.py','--junitxml='+str(OUT/(label+'.xml'))],ROOT,1,dict(X3_B3_ROOT=str(base),X3_EVIDENCE=str(OUT/(label+'_sql'))))
 run('atomic',[sys.executable,'-m','pytest','-q',RUN/'test_atomic.py',RUN/'test_projected_atomic.py','--junitxml='+str(OUT/'atomic.xml')],RUN)
 shutil.copytree(RUN/'evidence/atomic_sql',OUT/'atomic_sql',dirs_exist_ok=True)
 (OUT/'e3_sql').mkdir(exist_ok=True)
 run('e3',[sys.executable,'-m','pytest','-q',candidate/'.runtime/e3/test_independent.py','--junitxml='+str(OUT/'e3.xml')],ROOT,0,dict(B2_REVIEW_ROOT=str(candidate/'.runtime/b2'),E3_EVIDENCE=str(OUT/'e3_sql')))
 run('f2',[sys.executable,'run_f2.py'],candidate)
 run('f2_blinded',[sys.executable,RUN/'frozen_x3/audit_f2.py'],ROOT,0,dict(X3_B3_ROOT=str(candidate),X3_EVIDENCE=str(OUT/'f2_blinded')))
 run('b3_mutants',[sys.executable,'mutation_audit_b3.py'],candidate)
 for version,base in [('original',frozen),('candidate',candidate)]:
  run(version+'_loop',[sys.executable,'developmental_loop.py','evidence/loop'],base)
  for label in ('positive','permission_absent'):
   run(version+'_'+label+'_cold',[sys.executable,'developmental_loop.py','replay','evidence/loop/'+label+'.json','evidence/loop/'+label+'_cold.sqlite'],base)
   live=json.loads((base/'evidence/loop'/(label+'.json')).read_text());cold=json.loads((OUT/(version+'_'+label+'_cold.log')).read_text())
   assert live['snapshot_hash']==cold['snapshot_hash'] and cold['receipts']==[e['receipt'] for e in live['episodes']]
  shutil.copytree(base/'evidence',OUT/(version+'_execution'),dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.sqlite','*.sqlite-*','*.b3lock'))
if __name__=='__main__':main()
