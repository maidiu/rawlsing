"""Bounded repair regression execution; prior independent acceptance is not reused."""
from pathlib import Path
import os,sys,subprocess,json,time,shutil
ROOT=Path(__file__).resolve().parent;E=ROOT/'evidence';C=ROOT/'candidate';E.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_DIR=subprocess.check_output(['git','rev-parse','--path-format=absolute','--git-common-dir'],cwd=ROOT).decode().strip())
def run(label,args,cwd=ROOT,expected=0,extra=None):
 start=time.time();p=subprocess.run(list(map(str,args)),cwd=cwd,env=dict(ENV,**(extra or {})),capture_output=True,text=True)
 (E/(label+'.log')).write_text(p.stdout+p.stderr);f=E/'commands.json';rows=json.loads(f.read_text()) if f.exists() else [];rows.append({'label':label,'command':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode,'expected':expected,'elapsed_seconds':time.time()-start});f.write_text(json.dumps(rows,indent=2)+'\n');print(label,p.returncode,flush=True)
 if p.returncode!=expected:print((p.stdout+p.stderr)[-2500:],flush=True);raise RuntimeError(label)
def main():
 if not (C/'.runtime').exists():run('materialize',[sys.executable,'materialize.py'],C)
 env={'REVIEW_B3_ROOT':str(C),'REVIEW_EVIDENCE':str(E/'schema_sql')}
 run('schema_repair',[sys.executable,'-m','pytest','-q',ROOT/'frozen_review/test_reviewer_hostiles.py',ROOT/'test_schema_repair.py','--junitxml='+str(E/'schema_repair.xml')],extra=env)
 if '--targeted' in sys.argv:return
 run('seeded_refusals',[sys.executable,'-m','pytest','-q',ROOT/'frozen_review/test_seeded_refusals.py','--junitxml='+str(E/'seeded_refusals.xml')],extra=dict(env,REVIEW_EVIDENCE=str(E/'seeded_sql')))
 (C/'evidence').mkdir(exist_ok=True)
 run('b3',[sys.executable,'-m','pytest','-q','test_integration_b3.py','--junitxml='+str(E/'b3.xml')],C)
 run('atomic',[sys.executable,'-m','pytest','-q',ROOT/'test_atomic.py',ROOT/'test_projected_atomic.py','--junitxml='+str(E/'atomic.xml')])
 matrix_input=(C/'F2_CASE_MATRIX.json').read_bytes()
 try:run('f2',[sys.executable,'run_f2.py'],C)
 finally:
  shutil.copyfile(C/'F2_CASE_MATRIX.json',E/'F2_CASE_MATRIX.actual.json')
  (C/'F2_CASE_MATRIX.json').write_bytes(matrix_input)
 run('x3',[sys.executable,'-m','pytest','-q',ROOT/'frozen_x3/test_independent.py','--junitxml='+str(E/'x3.xml')],expected=1,extra={'X3_B3_ROOT':str(C),'X3_EVIDENCE':str(E/'x3_sql')})
 run('f2_blinded',[sys.executable,ROOT/'frozen_x3/audit_f2.py'],extra={'X3_B3_ROOT':str(C),'X3_EVIDENCE':str(E/'f2_blinded')})
 run('loops',[sys.executable,'developmental_loop.py','evidence/loop'],C)
 for label in ('positive','permission_absent'):
  run(label+'_cold',[sys.executable,'developmental_loop.py','replay','evidence/loop/'+label+'.json','evidence/loop/'+label+'_cold.sqlite'],C)
  live=json.loads((C/'evidence/loop'/(label+'.json')).read_text());cold=json.loads((E/(label+'_cold.log')).read_text());assert cold['snapshot_hash']==live['snapshot_hash'] and cold['receipts']==[x['receipt'] for x in live['episodes']]
 shutil.copytree(C/'evidence',E/'candidate',dirs_exist_ok=True,ignore=shutil.ignore_patterns('*.sqlite','*.sqlite-*','*.b3lock'))
if __name__=='__main__':main()
