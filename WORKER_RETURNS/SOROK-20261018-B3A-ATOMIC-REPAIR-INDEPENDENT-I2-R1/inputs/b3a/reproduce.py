"""Bounded one-store reproduction. Existing frozen files are never overwritten.

Usage: python3 reproduce.py [--reuse-baseline]
Expected historical REDs remain pytest failures in raw XML/logs.
"""
from pathlib import Path
import os,sys,json,subprocess,shutil,tempfile
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent;E=ROOT/'evidence'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO).decode().strip()
def run(label,args,cwd,env,expected=0):
 p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
 (E/(label+'.log')).write_text(p.stdout+p.stderr)
 rows=json.loads((E/'reproduction_commands.json').read_text()) if (E/'reproduction_commands.json').exists() else []
 rows.append(dict(label=label,args=list(map(str,args)),cwd=str(cwd),exit=p.returncode,expected=expected));(E/'reproduction_commands.json').write_text(json.dumps(rows,indent=2)+'\n')
 assert p.returncode==expected,(label,p.returncode,p.stdout[-2000:],p.stderr[-2000:])
def main():
 E.mkdir(exist_ok=True);env=dict(os.environ,GIT_DIR=git('rev-parse','--path-format=absolute','--git-common-dir'),PYTHONDONTWRITEBYTECODE='1')
 if '--audit-only' in sys.argv:
  run('final_audit',[sys.executable,str(ROOT/'audit_return.py')],ROOT,env)
  return
 # Original materializer resolves ROOT.parent.parent. Keep staging outside the repo
 # so Git pathspecs cannot become relative to an unrelated nested source subtree.
 with tempfile.TemporaryDirectory(prefix='sorok-atomic-reproduction-') as d:
  frozen=Path(d)/'WORKER_RETURNS/B3';shutil.copytree(ROOT/'frozen_b3',frozen)
  if '--reuse-baseline' not in sys.argv:
   run('frozen_full',[sys.executable,'run_all.py'],frozen,env,1)
   text=(E/'frozen_full.log').read_text();assert "assert branch=='agent/rabochii" in text
   shutil.copytree(frozen/'evidence',E/'baseline',dirs_exist_ok=True)
  else:
   run('frozen_materialize',[sys.executable,'materialize.py'],frozen,env)
  candidate=ROOT/'candidate'
  if not (candidate/'.runtime').exists():
   shutil.copytree(frozen/'.runtime',candidate/'.runtime')
   shutil.copyfile(frozen/'source_manifest.json',candidate/'source_manifest.json')
  (candidate/'evidence').mkdir(exist_ok=True)
  for label,base in (('frozen_x3',frozen),('candidate_x3',candidate)):
   xenv=dict(env,X3_B3_ROOT=str(base),X3_EVIDENCE=str(E/(label+'_sql')))
   run(label,[sys.executable,'-m','pytest','-q',str(ROOT/'frozen_x3/test_independent.py'),'--junitxml='+str(E/(label+'.xml'))],ROOT,xenv,1)
  (E/'e3_sql').mkdir(exist_ok=True)
  run('e3',[sys.executable,'-m','pytest','-q',str(candidate/'.runtime/e3/test_independent.py'),'--junitxml='+str(E/'e3.xml')],ROOT,dict(env,B2_REVIEW_ROOT=str(candidate/'.runtime/b2'),E3_EVIDENCE=str(E/'e3_sql')))
  run('candidate_b3',[sys.executable,'-m','pytest','-q','test_integration_b3.py','--junitxml='+str(E/'candidate_b3.xml')],candidate,env)
  run('atomic',[sys.executable,'-m','pytest','-q',str(ROOT/'test_atomic.py'),str(ROOT/'test_projected_atomic.py'),'--junitxml='+str(E/'atomic.xml')],ROOT,env)
  run('blinded_f2',[sys.executable,str(ROOT/'frozen_x3/audit_f2.py')],ROOT,dict(env,X3_B3_ROOT=str(candidate),X3_EVIDENCE=str(E/'f2_blinded')))
  for label,script,args in [('candidate_f2','run_f2.py',[]),('candidate_mutation','mutation_audit_b3.py',[]),('candidate_loop','developmental_loop.py',['evidence/loop'])]:
   run(label,[sys.executable,script,*args],candidate,env)
  for label in ('positive','permission_absent'):
   db=candidate/'evidence/loop'/(label+'_cold.sqlite');db.unlink(missing_ok=True)
   run(label+'_cold',[sys.executable,'developmental_loop.py','replay','evidence/loop/'+label+'.json',str(db)],candidate,env)
   live=json.loads((candidate/'evidence/loop'/(label+'.json')).read_text());cold=json.loads((E/(label+'_cold.log')).read_text())
   assert cold['snapshot_hash']==live['snapshot_hash'] and cold['receipts']==[e['receipt'] for e in live['episodes']]
  shutil.copytree(candidate/'evidence',E/'candidate',dirs_exist_ok=True)
  # The source manifest uses relative paths independent of the ephemeral runtime.
  shutil.copyfile(frozen/'source_manifest.json',ROOT/'import_manifest.json')
 run('final_audit',[sys.executable,str(ROOT/'audit_return.py')],ROOT,env)
if __name__=='__main__':main()
