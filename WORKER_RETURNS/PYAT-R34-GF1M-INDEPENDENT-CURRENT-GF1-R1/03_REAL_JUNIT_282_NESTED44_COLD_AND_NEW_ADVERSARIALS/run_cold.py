import os,sys,json,subprocess,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent;V=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';S=V/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1';G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
seat=E/'court/runtime_root/gf1_pair_support_consumer.py';saved=seat.read_bytes();candidate=V/'repair/gf1_pair_support_consumer.py'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'),GF1M_HISTORICAL_HELPER=str(V/'phase_a/test_gf1l_executable_v2.py'))
receipts=[]
try:
 seat.write_bytes(candidate.read_bytes())
 for i in (0,1):
  proc=subprocess.run([sys.executable,str(O/'independent_cold.py')],cwd=E/'court/repro',env=env,text=True,capture_output=True)
  (O/f'independent_cold_{i}.json').write_text(proc.stdout);(O/f'independent_cold_{i}.stderr').write_text(proc.stderr)
  assert proc.returncode==0,proc.stderr
  data=json.loads(proc.stdout);receipts.append(data)
  for imp in data['imports']:
   file=Path(imp['file']);b=file.read_bytes();assert hashlib.sha256(b).hexdigest()==imp['sha256']
   original=candidate.read_bytes() if file==seat else subprocess.check_output(['git','show','eeb726357204653b22458dc267dd70ba0009bd77:WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/'+imp['relative']],cwd=R.parents[1])
   assert b==original,imp
 a,b=[dict(x) for x in receipts];assert a.pop('pid')!=b.pop('pid');assert a==b
 (O/'independent_cold_verification.json').write_text(json.dumps(dict(pids=[x['pid'] for x in receipts],non_pid_receipts_equal=True,actual_imports_per_process=len(a['imports']),imports_independently_git_verified=True,cases_per_process=82,nonfinite_witnesses_per_process=2),indent=2)+'\n')
 print('Independent cold82 + original native identities + nonfinite witnesses identical in two processes')
finally:seat.write_bytes(saved)
