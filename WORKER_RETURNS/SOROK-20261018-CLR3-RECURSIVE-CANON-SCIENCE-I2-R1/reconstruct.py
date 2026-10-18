"""Exact-object reconstruction; all materialization stays in this return."""
import hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
WT = ROOT.parent.parent
TARGET = '4076dcc7c944723b8eea449c0753e535b79d1aa5'
PRIOR = 'a1c5b1b09b825184e80e84a1789c393b97ea9ae2'
START = '60acc908213d2ed6c310909016703c16d69dae47'
CLR = 'WORKER_RETURNS/SOROK-20261018-CLR3-RECURSIVE-FORMATION-CANON-COURT-R1/'
R1 = 'WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R1/'
R2 = 'WORKER_RETURNS/SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R2_REASSESSMENT/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(WT), *args])

def materialize(ref, prefix, dest):
    entries = git('ls-tree', '-r', ref, '--', prefix).decode().splitlines()
    rows=[]
    for entry in entries:
        meta,path=entry.split('\t',1)
        mode,kind,blob=meta.split()
        assert kind=='blob'
        data=git('cat-file','blob',blob)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
        out=ROOT/dest/path.removeprefix(prefix)
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_bytes(data)
        rows.append(dict(commit=ref,path=path,blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),local_path=str(out.relative_to(ROOT))))
    return rows

if __name__=='__main__':
    rows=[]
    for ref,prefix,dest in [(TARGET,CLR,'reconstructed/clr3'),(PRIOR,R1,'reconstructed/r1'),(PRIOR,R2,'reconstructed/r2')]:
        rows+=materialize(ref,prefix,dest)
    for path in ['SOROK_PRODUCT_CONTROL_ROOM/00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md','SOROK_PRODUCT_CONTROL_ROOM/00D_WARM_ENVIRONMENT_PASSPORT_AND_COST_AWARE_AGENT_DISPENSATION_R1.md']:
        rows+=materialize(START,path,'governance/'+path.split('/')[-1])
    (ROOT/'evidence').mkdir(exist_ok=True)
    (ROOT/'evidence/reconstruction_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({'verified_exact_git_blobs':len(rows),'commits':[TARGET,PRIOR,START]}))
