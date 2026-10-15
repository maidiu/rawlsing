"""Execute exact suites, preserving real exit status and complete diagnostics."""
import datetime, hashlib, json, os, pathlib, shutil, subprocess, sys
RET=pathlib.Path(__file__).resolve().parents[1]
RT=RET/'runtime_root'
CP=RT/'WORKER_RETURNS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1'
NS=CP/'staging/ns'
SUITES={
 'smoke':['port/test_connection.py::test_adapter_run_calls_pinned_pe_c1_n10e'],
 'baseline_rc0':[str(RT/'baseline/test_rc0_hostile.py')],
 'rc0':['staging/rc0/test_rc0_hostile.py'],
 'k9_k10':['port/test_k9_provider_swap.py','port/test_k10_structural_conservation.py'],
 'original_k9_k10':['original_tests/test_k9_provider_swap.py','original_tests/test_k10_structural_conservation.py'],
 'connection':['port/test_connection.py'],
 'n10e_c1':['staging/ns/rawlsing_next/tests/test_pre553_empirical_possibility_provider.py','staging/ns/rawlsing_next/tests/test_pre553_analytical_composition.py'],
 'pe':['staging/ns/rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py'],
 'hostile':[str(RET/'reviewer_tests/test_rsc0_hostile.py')],
}
def environment(suite):
 env=os.environ.copy()
 env.update(PYTHONPATH=os.pathsep.join(map(str,[RT,CP,NS,NS/'rawlsing_next/tests',RT/'rawlsing_next/tests'])),
  RC0_RETURN=str(RET),RSC0_RETURN=str(RET),RSC0_RUNTIME=str(RT),RSC0_SUITE=suite,PYTHONDONTWRITEBYTECODE='1')
 if suite=='baseline_rc0':env['PYTHONPATH']=os.pathsep.join(map(str,[RT,RT/'baseline',NS,NS/'rawlsing_next/tests',RT/'rawlsing_next/tests']))
 if suite in ('baseline_rc0','rc0'):
  case=RT/'case_runs'/suite
  (case/'repro').mkdir(parents=True,exist_ok=True)
  link=case/'runtime_root'
  if not link.exists():link.symlink_to(RT,target_is_directory=True)
  env['RC0_RETURN']=str(case)
 return env
def sanitize(s):
 return s.replace(str(RT),'$RSC0_RUNTIME').replace(str(RET),'$RSC0_RETURN').replace(str(RET.parents[1]),'$REVIEW_WORKTREE')
def main():
 suite=sys.argv[1]
 if suite in ('probe','reverse_probe'): cmd=[sys.executable,str(RET/'repro'/('probe.py' if suite=='probe' else 'reverse_probe.py'))]
 else: cmd=[sys.executable,'-m','pytest',*SUITES[suite],'-q','-p','no:cacheprovider','--junitxml='+str(RET/'repro'/f'{suite}.xml')]
 started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 p=subprocess.run(cmd,cwd=RT/'baseline' if suite=='baseline_rc0' else CP,env=environment(suite),stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if suite in ('baseline_rc0','rc0'):
  source=RT/'case_runs'/suite/'repro/observations'
  if source.exists():shutil.copytree(source,RET/'repro/observations_by_suite'/suite,dirs_exist_ok=True)
 out=sanitize(p.stdout.decode(errors='replace'))
 (RET/'repro'/f'{suite}.log').write_text(out)
 xml=RET/'repro'/f'{suite}.xml'
 if xml.exists(): xml.write_text(sanitize(xml.read_text()))
 receipt=dict(suite=suite,started_at=started,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=[sanitize(x) for x in cmd],cwd=sanitize(str(RT/'baseline' if suite=='baseline_rc0' else CP)),exit_code=p.returncode,raw_stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),sanitization='runtime/return/worktree paths only',log=f'repro/{suite}.log',junit=f'repro/{suite}.xml' if xml.exists() else None)
 (RET/'repro'/f'{suite}_execution.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(out[-5000:]);print('ACTUAL_EXIT',p.returncode)
 return p.returncode
if __name__=='__main__': raise SystemExit(main())
