"""Rehydrate exact pinned code only inside this reviewer's IGNORED workspace."""
from pathlib import Path
import subprocess,hashlib,json,ast
RET=Path(__file__).resolve().parents[1]
ROOT=RET/'runtime_root/source'
REV='189da3b54307d8731132c9a7f7baf578fee8bc96'
CAN='WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1'
TESTS=['test_wsc_gt0_protocol','test_wsc_gt0_end_to_end_integrated','test_wsc_gt0_prev3_bridge','test_psepf_zero_positive_guard','test_sdtf_r4_world_response_redrive','test_sdtf_r4_mechanism_rule_authority_binding','test_sdtf_r4_r2_current_rule_admission_seam','test_sdtf_r4_witness_currentness','test_sdtf_r4_d1_hosting_replay','test_m6_actor_safe_expression']
seen=set();rows=[]
def put(path,rev=REV):
    key=(rev,path)
    if key in seen:return
    seen.add(key)
    blob=subprocess.check_output(['git','rev-parse',rev+':'+path]).decode().strip()
    b=subprocess.check_output(['git','cat-file','blob',blob])
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
    f=ROOT/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    rows.append(dict(commit=rev,path=path,blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),local=str(f.relative_to(RET))))
    return f
for path in subprocess.check_output(['git','ls-tree','-r','--name-only',REV,CAN]).decode().splitlines():put(path)
modules=['rawlsing_next.tests.'+n for n in TESTS]
modules+=['rawlsing_next.'+n for n in ['wsc_gt0_protocol','wsc_gt0_end_to_end','wsc_gt0_v3_runtime','wsc_gt0_prev3_bridge','wsc_gt0_field_forge_ingress','wsc_gt0_source_preff','wsc_gt0_v2_mediation','v3_psepf_zero_positive_guard','m6_actor_safe_expression','sdtf_r4_world_response_redrive','sdtf_r4_mechanism_rule_authority_binding','sdtf_r4_witness_currentness','sdtf_r4_d1_hosting_replay']]
visited=set()
while modules:
    name=modules.pop(0)
    if name in visited:continue
    visited.add(name);path=name.replace('.','/')+'.py'
    exists=subprocess.run(['git','cat-file','-e',REV+':'+path],capture_output=True).returncode==0
    if not exists:continue
    f=put(path)
    if f is None:f=ROOT/path
    for n in ast.walk(ast.parse(f.read_text())):
        if isinstance(n,ast.Import):modules.extend(a.name for a in n.names if a.name.startswith('rawlsing_next.'))
        elif isinstance(n,ast.ImportFrom) and n.module:
            if n.module=='rawlsing_next':modules.extend(n.module+'.'+a.name for a in n.names)
            elif n.module.startswith('rawlsing_next.'):modules.append(n.module)
# The source-adoption pointer explicitly identifies the immutable CAN008 R2 blob.
adopt=[x for x in subprocess.check_output(['git','ls-tree','-r','--name-only',REV]).decode().splitlines() if x.endswith('CAN008_R2_AUTHORITY_CANDIDATE_R1/02_HQ_CAN008_R2_ADOPTION_R1.md')]
for path in adopt:put(path)
(RET/'source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
law_rows=[]
for name,blob in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
    b=subprocess.check_output(['git','cat-file','blob',blob])
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==blob
    path=RET/'runtime_root/law'/(name+'.txt');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
    law_rows.append(dict(name=name,blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),local=str(path.relative_to(RET))))
(RET/'law_blob_manifest.json').write_text(json.dumps(law_rows,indent=2)+'\n')
print('Exact staged candidate/owner files',len(rows),'all confined to ignored runtime_root')
if __name__=='__main__':pass
