#!/usr/bin/env python3
"""Generate the R2 exact-SHA inventory for the review return."""
import hashlib, json, pathlib, subprocess

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
NEW = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def rec(p):
    q=pathlib.Path(p).resolve()
    try: label=str(q.relative_to(R2))
    except ValueError: label=str(q)
    return {'path':label,'bytes':q.stat().st_size,'sha256':sha(q)}
out={}
out['target_commit']=subprocess.run(['git','-C',str(NEW),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
out['target_branch']=subprocess.run(['git','-C',str(NEW),'branch','--show-current'],capture_output=True,text=True).stdout.strip()
out['target_worktree_clean_tracked']=subprocess.run(['git','-C',str(NEW),'status','--porcelain'],capture_output=True,text=True).stdout.strip()=='' or all(x.startswith('??') for x in subprocess.run(['git','-C',str(NEW),'status','--porcelain'],capture_output=True,text=True).stdout.splitlines() if x.strip())
out['input_zip']=rec(R2/'INPUT/REPAIRED_PACKAGE_R2.zip')
out['original_zip']=rec('/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip')
out['target_manifest']=rec(NEW/'MANIFEST.json')
out['source_authentication']=rec(NEW/'SOURCE_AUTHENTICATION.json')
out['inventory']=rec(PKG/'EVIDENCE/SOURCE_IDENTITY_INVENTORY.json')
out['frame']=rec(PKG/'EVIDENCE/FRAME.json')
out['decision']=rec(PKG/'EVIDENCE/DECISION.json')
out['c_packet']=rec(PKG/'EVIDENCE/C.json')
out['package_tools']={n:rec(PKG/'tools'/n) for n in ('r7_integrated.py','r7_inventory.py','r7_build.py','r7_stage.py','test_integrated_strict.py','test_r7_integrated.py')}
out['built']={n:rec(PKG/'BUILT'/n) for n in ('BOUNDARY_CONTRACT_MAP.json','TYPED_GRAPH.json','IDENTITY_DISPOSITIONS.tsv','EVIDENCE_INDEX.jsonl','BUILDER_HANDOFF.json','BUILDER_HANDOFF.jsonl','MANIFEST.json')}
out['docs']={n:rec(R2/n) for n in ('VERDICT.md','GROK_DELTA.md','REVIEW_VERDICT.json','RAW_COMMANDS.md','TEST_TRANSCRIPT.json') if (R2/n).exists()}
wl={}
for p in sorted((R2/'LOGS').glob('*')):
    if p.name in ('make_exact_sha.log','STAMP'): continue
    wl[str(p.relative_to(R2))]=rec(p)
for p in sorted((R2/'WITNESS').glob('*')):
    if p.is_file(): wl[str(p.relative_to(R2))]=rec(p)
    elif p.is_dir():
        for q in sorted(p.glob('*')):
            if q.is_file(): wl[str(q.relative_to(R2))]=rec(q)
out['witness_and_logs']=wl
(R2/'EXACT_SHA256.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'written':'R2_RECHECK/EXACT_SHA256.json','target':out['target_commit'],'manifest':out['target_manifest'],'input':out['input_zip'],'witness_logs':len(wl)},indent=2))
