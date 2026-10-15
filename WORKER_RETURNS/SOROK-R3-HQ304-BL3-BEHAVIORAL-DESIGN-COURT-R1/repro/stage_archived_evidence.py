"""Exact archived synthetic captures for independent R2 audit; no rerun/resampling."""
import hashlib,json,pathlib,subprocess
RET=pathlib.Path(__file__).resolve().parents[1];ROOT=RET.parents[1];RT=RET/'runtime_root'
C='1e1546f9e6e1520ab48eb9a9cf5da8ded4f00599';CP='WORKER_RETURNS/SOROK-R3-HQ301-RBA-BEHAVIORAL-R2-VALIDITY-R1'
selector=RET/'source_selector.json';obj=json.loads(selector.read_text());known={r['staging_path'] for r in obj['files']}
def put(c,p,d):
 if d in known:return
 raw=subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),'show',c+':'+p]);blob=subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),'rev-parse',c+':'+p],text=True).strip()
 assert hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==blob
 out=RT/d;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==raw
 else:out.write_bytes(raw)
 obj['files'].append(dict(commit=c,source_path=p,staging_path=d,git_blob_sha1=blob,sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)));known.add(d)
for phase in ['complete_lawful','all_first_option','metadata_attack','budget_falsifier','origin_falsifier','belief_falsifier']:
 for name in ['ledger.jsonl.gz','coded_captures.json.gz','intervention_receipts.json.gz','summary.json']:
  rel='exec/r2/receipts/rba_review_run1/'+phase+'/'+name;put(C,CP+'/'+rel,'rba/'+rel)
put(C,CP+'/exec/r2/receipts/rba_review_run1/summary.json','rba/exec/r2/receipts/rba_review_run1/summary.json')
R2='a7d2be9894bf92f81356adf14141136666e63bd1';RP='WORKER_RETURNS/SOROK-R3-HQ300-BEHAVIORAL-ASSAY-R2-RECONSTRUCTION-R1'
for name in ['corpus.json','oracle.json','schedule.json']:put(R2,RP+'/data/'+name,'rba/staging/r2/data/'+name)
put('bf5fda102f4bced41a0f18f71c4c380d5d099462','WORKER_RETURNS/SOROK-R3-HQ298-SM-LAB2-BEHAVIORAL-R1/outputs/preregistration_freeze.json','rba/exec/lab2/outputs/preregistration_freeze.json')
put(C,CP+'/repro/rmb_review.xml','retained_rba/repro/rmb_review.xml')
selector.write_text(json.dumps(obj,indent=2)+'\n');print('ARCHIVED_R2_INPUTS_VERIFIED; TOTAL',len(obj['files']))
