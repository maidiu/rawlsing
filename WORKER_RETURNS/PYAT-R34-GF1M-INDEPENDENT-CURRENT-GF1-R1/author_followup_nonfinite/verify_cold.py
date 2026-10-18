import os,sys,subprocess,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;O=R/'evidence';V=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';S=V/'stage'
E=S/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1';G=S/'WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1'
seat=E/'court/runtime_root/gf1_pair_support_consumer.py';saved=seat.read_bytes();new=(R/'gf1_pair_support_consumer.py').read_bytes()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1G_COURT=str(E),GF1G_ORACLE=str(G/'01_FROZEN_ORACLE.json'),GF1J_GF1G_TEST=str(G/'phase_a/test_gf1g_precommitted.py'),GF1M_HISTORICAL_HELPER=str(V/'phase_a/test_gf1l_executable_v2.py'),GF1M_ORIGINAL_PHASE_A=str(P/'03_REAL_JUNIT_282_NESTED44_COLD_AND_NEW_ADVERSARIALS/test_independent_domains.py'))
receipts=[]
try:
 seat.write_bytes(new)
 for i in (0,1):
  proc=subprocess.run([sys.executable,str(R/'cold_refusals.py')],cwd=E/'court/repro',env=env,text=True,capture_output=True)
  (O/f'cold_refusal_{i}.json').write_text(proc.stdout);(O/f'cold_refusal_{i}.stderr').write_text(proc.stderr)
  assert proc.returncode==0,proc.stderr
  data=json.loads(proc.stdout);receipts.append(data)
  assert data['consumer_sha256']==hashlib.sha256(new).hexdigest() and data['reattested']==74
  assert Path(data['consumer_file']).resolve()==seat.resolve() and len(data['cases'])==12
 a,b=[dict(x) for x in receipts];assert a.pop('pid')!=b.pop('pid') and a==b
 print('12 nonfinite typed refusals identical in two cold processes:',[x['pid'] for x in receipts])
finally:seat.write_bytes(saved)
