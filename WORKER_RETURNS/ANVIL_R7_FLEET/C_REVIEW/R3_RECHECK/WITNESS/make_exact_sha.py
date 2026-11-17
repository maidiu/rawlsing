#!/usr/bin/env python3
"""R3 exact-SHA inventory."""
import hashlib,json,pathlib,subprocess
R3=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R3_RECHECK')
NEW=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION')
TS=(R3/'LOGS/STAMP').read_text().strip(); PKG=R3/f'COLD/FRESH_{TS}/ANVIL_R7'
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def rec(p):
 q=pathlib.Path(p).resolve()
 try:l=str(q.relative_to(R3))
 except ValueError:l=str(q)
 return {'path':l,'bytes':q.stat().st_size,'sha256':sha(q)}
out={'target_commit':subprocess.run(['git','-C',str(NEW),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()}
out['input_zip']=rec(R3/'INPUT/REPAIRED_PACKAGE_R3.zip')
out['original_zip']=rec('/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip')
out['target_manifest']=rec(NEW/'MANIFEST.json')
out['source_authentication']=rec(NEW/'SOURCE_AUTHENTICATION.json')
out['inventory']=rec(PKG/'EVIDENCE/SOURCE_IDENTITY_INVENTORY.json')
out['frame']=rec(PKG/'EVIDENCE/FRAME.json');out['decision']=rec(PKG/'EVIDENCE/DECISION.json');out['c_packet']=rec(PKG/'EVIDENCE/C.json')
out['package_tools']={n:rec(PKG/'tools'/n) for n in ('r7_integrated.py','r7_inventory.py','r7_build.py','r7_contract.py','test_integrated_strict.py','test_r7_integrated.py')}
out['docs']={n:rec(R3/n) for n in ('VERDICT.md','GROK_DELTA.md','REVIEW_VERDICT.json','RAW_COMMANDS.md','TEST_TRANSCRIPT.json') if (R3/n).exists()}
w={}
for p in sorted((R3/'LOGS').glob('*')):
 if p.name in ('make_exact_sha.log','STAMP'):continue
 w[str(p.relative_to(R3))]=rec(p)
for p in sorted((R3/'WITNESS').glob('*')):
 if p.is_file():w[str(p.relative_to(R3))]=rec(p)
 elif p.is_dir():
  for q in sorted(p.glob('*')):
   if q.is_file():w[str(q.relative_to(R3))]=rec(q)
out['witness_and_logs']=w
(R3/'EXACT_SHA256.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'target':out['target_commit'],'input':out['input_zip'],'manifest':out['target_manifest'],'witness_logs':len(w)},indent=2))
