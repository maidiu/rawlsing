"""Run original suites and versioned BL3 code with true statuses/full outputs."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
RET=pathlib.Path(__file__).resolve().parents[1];RT=RET/'runtime_root';RBA=RT/'rba';R2=RBA/'exec/r2'
def env(suite):
 e=os.environ.copy();e.update(BL3_RETURN=str(RET),BL3_SUITE=suite,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=os.pathsep.join(map(str,[RT,RET,R2,RBA/'exec/lab1',RBA/'exec/lab2'])))
 return e
def clean(s):return s.replace(str(RT),'$BL3_RUNTIME').replace(str(RET),'$BL3_RETURN').replace(str(RET.parents[1]),'$BL3_WORKTREE')
def main():
 s=sys.argv[1]
 specs={'r2':([str(R2/'test_r2.py')],R2),'rba':([str(RBA/'hostile/test_hostile_rba.py')],RBA),'lab1':([str(RBA/'exec/lab1/lab/test_lab.py')],RBA/'exec/lab1'),'lab2':([str(RBA/'exec/lab2/lab2/test_lab2.py')],RBA/'exec/lab2'),'rmb':([str(RBA/'exec/rmb/test_independent.py')],RBA/'exec/rmb'),'r3':([str(RET/'tests/test_r3.py')],RET)}
 if s in specs:
  paths,cwd=specs[s];cmd=[sys.executable,'-m','pytest',*paths,'-q','-p','no:cacheprovider','--junitxml='+str(RET/'repro'/f'{s}.xml')]
 elif s=='r2_archive_audit':cwd=R2;cmd=[sys.executable,str(R2/'audit_outputs.py'),'rba_review_run1']
 elif s=='rba_recompute':cwd=RBA;cmd=[sys.executable,str(RBA/'hostile/recompute_paired.py')]
 elif s=='r3_audit':cwd=RET;cmd=[sys.executable,str(RET/'repro/audit_r3_captures.py')]
 elif s=='evidence':cwd=RET;cmd=[sys.executable,str(RET/'repro/build_evidence.py')]
 elif s=='mock':cwd=RET;cmd=[sys.executable,'-m','r3.experiment']
 elif s=='probe':cwd=RET;cmd=[sys.executable,str(RET/'repro/probe.py')]
 else:raise ValueError(s)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(cmd,cwd=cwd,env=env(s),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (RET/'repro'/f'{s}.log').write_text(clean(p.stdout.decode(errors='replace')))
 xml=RET/'repro'/f'{s}.xml'
 if xml.exists():xml.write_text(clean(xml.read_text()))
 receipt=dict(suite=s,started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=[clean(x) for x in cmd],cwd=clean(str(cwd)),exit_code=p.returncode,raw_stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stdout='repro/'+s+'.log',junit='repro/'+s+'.xml' if xml.exists() else None,sanitization='runtime/return/worktree path aliases only')
 (RET/'repro'/f'{s}_execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(clean(p.stdout.decode(errors='replace'))[-5000:]);print('ACTUAL_EXIT',p.returncode)
 return p.returncode
if __name__=='__main__':raise SystemExit(main())
