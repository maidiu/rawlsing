from pathlib import Path
import json,csv,hashlib,shutil,zipfile,os
R9A=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9A_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9B_20260811')
if OUT.exists():shutil.rmtree(OUT)
for s in ['AUDIT','VALIDATION','CODE']:(OUT/s).mkdir(parents=True,exist_ok=True)
a=json.load(open(R9A/'AUDIT/R9A_CANARY_COVERAGE_CORRECTION.json'))
# Correct stale narrative literal in copied machine summary interpretation.
a['interpretation']=a['interpretation'].replace('Twenty sealed','Nineteen sealed')
json.dump(a,open(OUT/'AUDIT/R9B_CANARY_COVERAGE_CORRECTION.json','w'),indent=2)
report=(R9A/'R9A_COMPOSITE_DENOMINATOR_REPORT.md').read_text().replace('By rule, the 20 gaps are','By rule, the 19 gaps are')
open(OUT/'R9B_COMPOSITE_DENOMINATOR_REPORT.md','w').write(report)
status=json.load(open(R9A/'CURRENT_STATUS_R9A.json'))
status.update(checkpoint='Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9B_20260811',status='CORRECTIVE_HOSTILE_QA_COMPOSITE_DENOMINATOR_REQUIRED__NARRATIVE_CONSISTENCY_REPAIRED',supersedes='R9A narrative count wording only; preserves all R9A machine counts, R9 pair census, and R8 dispatch revocation')
json.dump(status,open(OUT/'CURRENT_STATUS_R9B.json','w'),indent=2)
readme='''# README FIRST — R9B\n\nR9B is a narrow append-only consistency correction to R9A. No semantic or denominator count changes.\n\nGoverning counts: **117** sealed R6 T03–T11 relations = **98 pair-addressable + 19 non-pair/non-relational-lane**. The 19 contain **210** implementation rows: 150 context, 50 topology, 10 non-scalar evidence.\n\nR8 W01–W04 remain DO NOT EXECUTE. Job 3 remains blocked.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
pointer='''# ACTIVE EXECUTION POINTER — R9B\n\nCurrent: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / R9B COMPOSITE DENOMINATOR CORRECTION`.\n\n- R8 66/53/13 denominator: REVOKED FOR DISPATCH.\n- R8 W01–W04: DO NOT EXECUTE.\n- R8C: preserve provisional decisions.\n- R9 364,094 pair census: valid and complete within current 3,324 relational-semantic-unit pair jurisdiction.\n- R6 T03–T11 canaries: 117 total = 98 pair-addressable + 19 requiring non-pair/non-relational-lane integration.\n- Unified 18,276-spine composite denominator required before item #14 can close.\n- Job 3: NOT AUTHORIZED.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER_R9B.md','w').write(pointer)
nextmd=(R9A/'NEXT_EXECUTION_STEPS.md').read_text()
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write(nextmd)
val='''from pathlib import Path\nimport json,sys,re\nR=Path(__file__).resolve().parents[1];errs=[];checks=[]\ndef ck(n,x,d=None):checks.append({'check':n,'pass':bool(x),'detail':d});errs.append(n) if not x else None\na=json.load(open(R/'AUDIT/R9B_CANARY_COVERAGE_CORRECTION.json'));ck('math',a['pair_census_addressable_relations']+a['nonpair_or_nonrelational_lane_relations']==a['r6_t03_t11_total_relations']);ck('98',a['pair_census_addressable_relations']==98);ck('19',a['nonpair_or_nonrelational_lane_relations']==19);ck('210',a['nonpair_member_implementation_count']==210);ck('interpretation_nineteen','Nineteen sealed' in a['interpretation']);ck('interpretation_no_twenty','Twenty sealed' not in a['interpretation'])\nr=(R/'R9B_COMPOSITE_DENOMINATOR_REPORT.md').read_text();ck('report_19','By rule, the 19 gaps are' in r);ck('report_no_20','By rule, the 20 gaps are' not in r);ck('report_98_117','98 / 117' in r);ck('report_19_117','19 / 117' in r)\ns=json.load(open(R/'CURRENT_STATUS_R9B.json'));ck('job3_false',s['job3_authorized'] is False);ck('packs_poisoned',s['r8_worker_packs']=='DO_NOT_EXECUTE')\nres={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9B.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}));sys.exit(0 if not errs else 1)\n'''
open(OUT/'VALIDATION/validate_r9b.py','w').write(val)
shutil.copy2('/mnt/data/build_r9b.py',OUT/'CODE/build_r9b.py')
os.system(f"python3 '{OUT/'VALIDATION/validate_r9b.py'}'")
# manifest + zip
man=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='SHA256_MANIFEST_R9B.csv':man.append((str(p.relative_to(OUT)),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size))
with open(OUT/'SHA256_MANIFEST_R9B.csv','w',newline='') as f:w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes']);w.writerows(man)
zp=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9B_20260811.zip')
if zp.exists():zp.unlink()
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(OUT)))
sha=hashlib.sha256(zp.read_bytes()).hexdigest();open(str(zp)+'.sha256','w').write(f'{sha}  {zp.name}\n')
print(json.dumps({'sha':sha,'manifest':len(man)},indent=2))
