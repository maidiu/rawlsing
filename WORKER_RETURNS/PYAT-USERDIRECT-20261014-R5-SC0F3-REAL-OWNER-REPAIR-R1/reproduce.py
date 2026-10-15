"""Reproduce pinned suites and candidate without overwriting any prior run."""
from pathlib import Path
import os,sys,subprocess,json,re,hashlib
RET=Path(__file__).resolve().parent
if len(sys.argv)!=2 or not re.fullmatch(r'[A-Za-z0-9_-]+',sys.argv[1]):
 raise SystemExit('Usage: python3 reproduce.py fresh_run_id')
tag=sys.argv[1]
manifest=json.loads((RET/'source_manifest.json').read_text())
for row in manifest:
 b=(RET/row['staged']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob_sha1']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
expected={'old_sc0f':0,'old_sc0i':0,'old_i2':1,'old_rc0':1,'k9':0,'k10':0,'n10e_c1':0,'pe_author':0,'pe_independent':1,'candidate':0}
for suite,wanted in expected.items():
 name=suite+'__'+tag
 log=RET/'repro'/(name+'.log')
 with log.open('x') as f:
  proc=subprocess.run([sys.executable,str(RET/'repro/run_suite.py'),name],stdout=f,stderr=subprocess.STDOUT,cwd=RET.parents[1])
 print(suite,proc.returncode,'expected',wanted,flush=True)
 if proc.returncode!=wanted:raise SystemExit('Unexpected suite disposition: '+suite)
subprocess.run([sys.executable,str(RET/'repro/prove.py'),tag],check=True,cwd=RET.parents[1])
print('Prior REDs preserved; fixture-only candidate reproduced. No scientific acceptance or original-source permission.')
