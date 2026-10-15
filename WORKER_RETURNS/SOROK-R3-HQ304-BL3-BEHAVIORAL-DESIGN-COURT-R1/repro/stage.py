"""Independently stage exact original source; never execute author staging code."""
import datetime,hashlib,json,pathlib,subprocess,uuid
RET=pathlib.Path(__file__).resolve().parents[1];ROOT=RET.parents[1];RT=RET/'runtime_root'
RBA='1e1546f9e6e1520ab48eb9a9cf5da8ded4f00599';BP='WORKER_RETURNS/SOROK-R3-HQ301-RBA-BEHAVIORAL-R2-VALIDITY-R1'
R2='a7d2be9894bf92f81356adf14141136666e63bd1';R2P='WORKER_RETURNS/SOROK-R3-HQ300-BEHAVIORAL-ASSAY-R2-RECONSTRUCTION-R1'
if (RT/'runtime_marker.json').exists():raise SystemExit('EXISTING_VERIFIED_RUNTIME_REFUSE_OVERWRITE')
RT.mkdir(exist_ok=True);rows=[]
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def put(c,p,d,expected=None):
 b=git('show',c+':'+p);blob=git('rev-parse',c+':'+p).decode().strip()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()==blob
 assert expected is None or blob==expected
 out=RT/d;out.parent.mkdir(parents=True,exist_ok=True)
 if out.exists():assert out.read_bytes()==b,('PARTIAL_STAGE_DIFFERS',d)
 else:out.write_bytes(b)
 rows.append(dict(commit=c,source_path=p,staging_path=d,git_blob_sha1=blob,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
 return b
manifest=json.loads(git('show',RBA+':'+BP+'/staging/staging_manifest.json'))
assert len(manifest['entries'])==49
for e in manifest['entries']:
 raw=put(e['source_rev'],e['repo_path'],'rba/exec/'+e['staged_path'],e['git_blob_sha1'])
 assert raw==git('show',RBA+':'+BP+'/staging/'+e['staged_path'])
for p in ['hostile/test_hostile_rba.py','hostile/recompute_paired.py','00_RETURN.md','01_reviewer_expectations.json','02_verdict_matrix.json','outputs/paired_recompute.json','exec/r2/receipts/rba_review_run1/summary.json','exec/r2/receipts/rba_review_run1/raw_capture_audit.json']:
 put(RBA,BP+'/'+p,'rba/'+p if p.startswith('hostile/') else 'retained_rba/'+p)
for p in ['00_RETURN.md','01_DESIGN.md']:
 put(R2,R2P+'/'+p,'retained_r2/'+p)
# Original frozen reports are documentary inputs, not recomputed results.
for c,p,d in [
 ('d7cc7ebf0c06303ffe5637aa4d14c3c1fc228e09','WORKER_RETURNS/SOROK-S-M-LAB1-WORLD-ORG-RESPONSE-CAUSAL-COURT-R1/00_RETURN.md','reports/LAB1.md'),
 ('bf5fda102f4bced41a0f18f71c4c380d5d099462','WORKER_RETURNS/SOROK-R3-HQ298-SM-LAB2-BEHAVIORAL-R1/00_RETURN.md','reports/LAB2.md'),
 ('bf7518cff877ce108ef9c07f2e2eeaf990171d08','WORKER_RETURNS/SOROK-R3-HQ299-RMB-BEHAVIORAL-HARNESS-INDEPENDENT-R1/00_RETURN.md','reports/RMB.md')]:put(c,p,d)
# RMB original test expects imports/LAB2; this is a byte-identical local layout.
for row in list(rows):
 if row['staging_path'].startswith('rba/exec/lab2/lab2/') or row['staging_path']=='rba/exec/lab2/01_PREREGISTRATION_FROZEN.json':
  suffix=row['staging_path'].removeprefix('rba/exec/lab2/')
  put(row['commit'],row['source_path'],'rba/exec/rmb/imports/LAB2/'+suffix,row['git_blob_sha1'])
fz=RT/'rba/exec/r2/freezes/v6.json';r1=RT/'rba/exec/r2/original_R1_preregistration.json'
assert hashlib.sha256(fz.read_bytes()).hexdigest()=='9a05efd9cc4060a7ae9b496f6fe71a5193912b228ac0d2e04577f80902384823'
assert hashlib.sha256(r1.read_bytes()).hexdigest()=='880fbde407654cf847e72f9cc58f7884470973072e99c0964b8d33e17e0bb330'
marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_permission='SYNTHETIC_ONLY_ZERO_EXTERNAL_EXPERIMENTAL_CALLS',role='BL3_SOURCEFREE_DESIGN')
(RT/'runtime_marker.json').write_text(json.dumps(marker,indent=2)+'\n')
(RET/'source_selector.json').write_text(json.dumps(dict(schema='BL3_GENUINE_GIT_SOURCE_CUSTODY@1',original_pin_count=49,actual_NUL_verified=True,files=rows),indent=2)+'\n')
print('VERIFIED49_ORIGINAL_PINS_AND_TOTAL',len(rows),'EPOCH',marker['epoch_id'])
