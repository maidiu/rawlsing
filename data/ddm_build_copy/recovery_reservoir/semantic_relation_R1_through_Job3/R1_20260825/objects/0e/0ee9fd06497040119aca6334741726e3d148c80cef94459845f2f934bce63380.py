from pathlib import Path
import json,csv,hashlib,shutil,zipfile,os
R9B=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9B_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9C_20260811')
if OUT.exists():shutil.rmtree(OUT)
for s in ['AUDIT','VALIDATION','CODE']:(OUT/s).mkdir(parents=True,exist_ok=True)
a=json.load(open(R9B/'AUDIT/R9B_CANARY_COVERAGE_CORRECTION.json'))
json.dump(a,open(OUT/'AUDIT/R9C_CANARY_COVERAGE_STATE.json','w'),indent=2)
r=(R9B/'R9B_COMPOSITE_DENOMINATOR_REPORT.md').read_text()
r=r.replace('# R9A — Canary coverage correction and composite-denominator requirement','# R9C — Hostile-QA stabilized composite-denominator state')
r=r.replace('## Why R9A exists','## Why this corrective state exists')
open(OUT/'R9C_COMPOSITE_DENOMINATOR_REPORT.md','w').write(r)
status=json.load(open(R9B/'CURRENT_STATUS_R9B.json'))
status.update(checkpoint='Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9C_20260811',status='HOSTILE_QA_STABILIZED__COMPOSITE_DENOMINATOR_REPAIR_ACTIVE',supersedes='R9B labeling/pointer stabilization only; semantic counts unchanged')
json.dump(status,open(OUT/'CURRENT_STATUS_R9C.json','w'),indent=2)
readme='''# README FIRST — R9C\n\nR9C is the stabilized hostile-QA checkpoint after review of R3–R8C. It changes no semantic counts from corrected R9B.\n\nGoverning state: R8 66/53/13 dispatch denominator revoked; R8 worker packs DO NOT EXECUTE; R8C provisional; R9 364,094 pair census valid only within current 3,324 relational-semantic-unit jurisdiction; 117 R6 T03–T11 canaries = 98 pair-addressable + 19 requiring non-pair/non-relational-lane integration; item #14 open; Job 3 blocked.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
pointer='''# ACTIVE EXECUTION POINTER\n\nCanonical active checkpoint: `/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R9C_20260811/`\n\nState: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / COMPOSITE DENOMINATOR REPAIR`.\n\n- R8 66/53/13 denominator: **REVOKED FOR DISPATCH**.\n- R8 W01–W04 packs: **DO NOT EXECUTE**.\n- R8C: preserve as provisional adjudication ancestry; revalidate after corrected denominator.\n- R9 pair census: **364,094 exhaustive same-source-wave pairs within the current 3,324 relational semantic units**.\n- R6 T03–T11 canaries: **117 total = 98 pair-addressable + 19 requiring non-pair/non-relational-lane integration**.\n- The final item-#14 universe must be composite over the unified 18,276 spine and all required rule-specific shores.\n- Job 3: **NOT AUTHORIZED**.\n\nNext: finalize the unified 18,276 structural-semantic spine/composite opportunity universe; build denominator-complete T03–T11 ledgers; then recompress, dedupe, remeasure worker economics, and only then issue successor adjudication packs.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER.md','w').write(pointer)
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write((R9B/'NEXT_EXECUTION_STEPS.md').read_text())
val='''from pathlib import Path\nimport json,sys\nR=Path(__file__).resolve().parents[1];checks=[];errs=[]\ndef ck(n,x,d=None):checks.append({'check':n,'pass':bool(x),'detail':d});errs.append(n) if not x else None\ns=json.load(open(R/'CURRENT_STATUS_R9C.json'));ck('job3_false',s['job3_authorized'] is False);ck('packs_poisoned',s['r8_worker_packs']=='DO_NOT_EXECUTE');ck('98_19',s['r6_t03_t11_canary_coverage']=={'pair_addressable':98,'nonpair_or_nonrelational':19});ck('pair_scope','3324' in s['pair_census'] and '364094' in s['pair_census'])\nr=(R/'R9C_COMPOSITE_DENOMINATOR_REPORT.md').read_text();ck('report_title',r.startswith('# R9C —'));ck('report_no_stale_20','20 gaps' not in r and 'Twenty sealed' not in r);ck('report_counts','98 / 117' in r and '19 / 117' in r and '210 member' in r)\np=(R/'ACTIVE_EXECUTION_POINTER.md').read_text();ck('pointer_r9c','CHECKPOINT_R9C_20260811' in p);ck('pointer_poison','DO NOT EXECUTE' in p);ck('pointer_job3','NOT AUTHORIZED' in p);ck('pointer_math','117 total = 98 pair-addressable + 19' in p)\na=json.load(open(R/'AUDIT/R9C_CANARY_COVERAGE_STATE.json'));ck('audit_math',a['pair_census_addressable_relations']+a['nonpair_or_nonrelational_lane_relations']==117)\nres={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9C.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}));sys.exit(0 if not errs else 1)\n'''
open(OUT/'VALIDATION/validate_r9c.py','w').write(val);shutil.copy2('/mnt/data/build_r9c.py',OUT/'CODE/build_r9c.py')
os.system(f"python3 '{OUT/'VALIDATION/validate_r9c.py'}'")
man=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='SHA256_MANIFEST_R9C.csv':man.append((str(p.relative_to(OUT)),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size))
with open(OUT/'SHA256_MANIFEST_R9C.csv','w',newline='') as f:w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes']);w.writerows(man)
zp=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9C_20260811.zip');
if zp.exists():zp.unlink()
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(OUT)))
sha=hashlib.sha256(zp.read_bytes()).hexdigest();open(str(zp)+'.sha256','w').write(f'{sha}  {zp.name}\n')
print(json.dumps({'sha':sha,'manifest':len(man)},indent=2))
