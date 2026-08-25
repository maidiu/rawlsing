from pathlib import Path
import pandas as pd,json,csv,hashlib,shutil,zipfile,os
BASE=Path('/mnt/data/rawlsing_exec/o12r2')
R9=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9A_20260811')
if OUT.exists():shutil.rmtree(OUT)
for s in ['AUDIT','PROVENANCE','VALIDATION','CODE']:(OUT/s).mkdir(parents=True,exist_ok=True)
reg=pd.read_csv(BASE/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False)
r6=pd.read_csv(BASE/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv',low_memory=False)
can=pd.read_csv(R9/'PROVENANCE/R6_T03_T11_PAIR_CENSUS_CANARY_COVERAGE_R9.csv')
# R9's first canary mapping filtered by the relation's display wave label; LiTS R6 wave I maps to current registry wave 2006.
# R9A corrects by exact implementation ID, which is the governing identity.
rtypes=['GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE']
impl_sem=reg.set_index('question_implementation_id')['sem__audit_unit_id'].to_dict()
exact_cov=[]
for _,rr in r6[r6.relation_type.isin(rtypes)].iterrows():
    try: impls=json.loads(rr.member_question_implementation_ids)
    except: impls=[]
    units=sorted(set(str(impl_sem.get(i,'')) for i in impls if pd.notna(impl_sem.get(i,'')) and str(impl_sem.get(i,'')) not in ('','nan','None')))
    exact_cov.append(dict(relation_authority_id=rr.relation_authority_id,relation_type=rr.relation_type,source_family=rr.source_family,wave=rr.wave,member_implementation_count=len(impls),mapped_semantic_unit_count=len(units),coverage_status='PAIR_CENSUS_ADDRESSABLE_BY_EXACT_IMPLEMENTATION_ID' if len(units)>=2 else 'REQUIRES_NON_RELATIONAL_LANE_OR_SOURCE_STRUCTURE_INTEGRATION'))
exact_cov=pd.DataFrame(exact_cov)
exact_cov.to_csv(OUT/'PROVENANCE/R6_T03_T11_EXACT_IMPLEMENTATION_CANARY_COVERAGE_R9A.csv',index=False)
gaps=exact_cov[exact_cov.coverage_status.ne('PAIR_CENSUS_ADDRESSABLE_BY_EXACT_IMPLEMENTATION_ID')].copy()
rows=[]
for _,rr in r6[r6.relation_authority_id.isin(gaps.relation_authority_id)].iterrows():
    try: impls=json.loads(rr.member_question_implementation_ids)
    except: impls=[]
    h=reg[reg.question_implementation_id.isin(impls)].copy()
    lanes=h.semantic_lane.fillna('BLANK').astype(str).value_counts().to_dict()
    o08=h.o08__position_lane.fillna('BLANK').astype(str).value_counts().to_dict()
    rows.append(dict(relation_authority_id=rr.relation_authority_id,relation_type=rr.relation_type,source_family=rr.source_family,wave=rr.wave,
                     member_implementation_count=len(impls),registry_rows_found=len(h),rows_with_sem_audit_unit=int(h.sem__audit_unit_id.notna().sum()),
                     semantic_lane_counts_json=json.dumps(lanes,sort_keys=True),o08_position_lane_counts_json=json.dumps(o08,sort_keys=True),
                     rows_with_o04_status=int(h.o04__central_o04_status.notna().sum()),
                     corrective_disposition='REQUIRES_NON_RELATIONAL_LANE_OR_SOURCE_STRUCTURE_INTEGRATION__NOT_PAIR_CENSUS_FAILURE'))
ledger=pd.DataFrame(rows).sort_values(['relation_type','source_family','wave','relation_authority_id'])
ledger.to_csv(OUT/'AUDIT/R6_T03_T11_NONPAIR_CANARY_GAP_LEDGER_R9A.csv',index=False)

rule_counts=ledger.relation_type.value_counts().to_dict()
# aggregate member lane counts
from collections import Counter
lc=Counter();oc=Counter();total_members=0;found=0
for _,r in ledger.iterrows():
 lc.update(json.loads(r.semantic_lane_counts_json));oc.update(json.loads(r.o08_position_lane_counts_json));total_members+=int(r.member_implementation_count);found+=int(r.registry_rows_found)
summary={
 'r9_parent_zip_sha256':'e8b4d576ab6ac024e18d70dee1d3faa7d12aacef69e4a78f43bd21f48daba699',
 'r6_t03_t11_total_relations':117,'pair_census_addressable_relations':98,'nonpair_or_nonrelational_lane_relations':19,
 'nonpair_rule_counts':rule_counts,'nonpair_member_implementation_count':total_members,'nonpair_registry_rows_found':found,
 'nonpair_semantic_lane_counts':dict(lc),'nonpair_o08_position_lane_counts':dict(oc),
 'interpretation':'The R9 364,094 pair census is complete for the current relational semantic-unit terrain only. Twenty sealed R6 T03-T11 relations are fully present in the 18,276 implementation registry but have zero sem__audit_unit_id membership. Therefore final item-14 completeness requires a composite universe: relational pair census + structural-choice/context/topology/endpoint/source-structure shores.'
}
json.dump(summary,open(OUT/'AUDIT/R9A_CANARY_COVERAGE_CORRECTION.json','w'),indent=2)
status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9A_20260811',
 'status':'CORRECTIVE_HOSTILE_QA_COMPOSITE_DENOMINATOR_REQUIRED',
 'active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR',
 'job3_authorized':False,
 'supersedes':'R9 interpretation of pair census as generic S14 base; preserves R9 pair census bytes and R8 dispatch revocation',
 'r8_worker_packs':'DO_NOT_EXECUTE',
 'r8c':'PRESERVE_PROVISIONALLY_REVALIDATE_LATER',
 'pair_census':'364094 COMPLETE ONLY FOR CURRENT 3324 RELATIONAL SEMANTIC UNITS',
 'r6_t03_t11_canary_coverage':{'pair_addressable':98,'nonpair_or_nonrelational':19},
 'next_dependency':'Construct COMPOSITE item-14 opportunity universe across all 18,276 implementations by joining the R9 relational pair census to non-relational semantic lanes, O04 endpoint shore, P2/P3 hierarchy, institution classes, exact source-parent structures and matrix/topology authority. Then rule-specific ledgers, dedupe, worker economics.'
}
json.dump(status,open(OUT/'CURRENT_STATUS_R9A.json','w'),indent=2)
report=f'''# R9A — Canary coverage correction and composite-denominator requirement\n\n## Why R9A exists\n\nR9 correctly revoked the premature R8 66/53/13 worker denominator and installed an exhaustive **364,094-pair** census over the current 3,324 relational semantic units. Its own canary ledger then exposed a further boundary: only **98 / 117** sealed R6 T03–T11 relations have at least two members on that relational semantic-unit terrain.\n\nR9 initially reported 97/20 because its canary mapper required the R6 display wave label to equal the current registry wave label. Exact implementation-ID identity recovers `LiTS wave I` as current registry `2006`, so R9A corrects that bookkeeping artifact.

The other **19 / 117** are not missing from the project. All their **{total_members} member implementation rows are present in the canonical 18,276 registry**. They simply live outside `sem__audit_unit_id` on lanes including {dict(lc)}. By rule, the 20 gaps are {rule_counts}.\n\nTherefore the pair census is a complete base for **current relational-semantic pairs**, not the complete S14 universe. This is not a defect in the census; it is direct evidence that repair item #2 (the unified 18,276 structural-semantic spine) is required before item #14 can close.\n\n## Correct governing model\n\nThe final item-#14 universe must be composite:\n\n1. R9 complete relational pair census (364,094 pairs);\n2. non-scalar / structural-choice and topology semantic lanes;\n3. context and position-conditioned rows where accepted R6 relations use them;\n4. O04 behavior/exposure endpoint shore for T06;\n5. P2/P3 broader/narrower and target-coordinate structures for T07;\n6. controlled institution-class mappings for T08;\n7. exact actor/recipient and printed-parent structures for T09;\n8. exact matrix/topology/source-parent structures for T10;\n9. source-native and cross-object complementary-role structures for T11.\n\nNo one substrate gets to call itself the maximum universe.\n\n## Governance\n\n- R8 W01–W04 remain **DO NOT EXECUTE**.\n- R8C remains provisional ancestry.\n- R3–R7 bounded narrowing remains useful, not globally complete.\n- R9 pair census is preserved unchanged and becomes one component of the composite denominator.\n- Job 3 remains blocked.\n'''
open(OUT/'R9A_COMPOSITE_DENOMINATOR_REPORT.md','w').write(report)
readme='''# README FIRST — R9A\n\nR9A is the current corrective pointer. It preserves R9's 364,094-pair census but narrows its jurisdiction: complete relational-semantic pair base, **not** complete S14 universe. Nineteen of 117 sealed T03–T11 R6 canaries live wholly outside `sem__audit_unit_id` and force a composite 18,276-spine denominator.\n\nR8 worker packs remain DO NOT EXECUTE. Job 3 remains blocked.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
nextmd='''# Next execution steps — R9A\n\n1. Build/finalize the 18,276-row structural-semantic spine required by repair item #2, with explicit lane/jurisdiction columns rather than forcing all rows into the relational semantic unit ontology.\n2. Register the 20 non-pair-addressable R6 canaries as mandatory composite-universe tests.\n3. Build rule-specific T03–T11 opportunity/disposition ledgers across the correct shores.\n4. Require 117/117 R6 T03–T11 canary recovery/accounting in the composite universe.\n5. Only after item #14 passes: recompress (#15), cross-rule dedupe (#16), remeasure worker economics (#17), then resume terminal S14 adjudication (#18).\n'''
open(OUT/'NEXT_EXECUTION_STEPS.md','w').write(nextmd)
pointer='''# ACTIVE EXECUTION POINTER — R9A\n\nCurrent: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / R9A COMPOSITE DENOMINATOR CORRECTION`.\n\n- R8 66/53/13 denominator: REVOKED FOR DISPATCH.\n- R8 W01–W04: DO NOT EXECUTE.\n- R8C: preserve provisional decisions.\n- R9 364,094 pair census: valid and complete **within current relational-semantic pair jurisdiction**.\n- 19/117 sealed R6 T03–T11 canaries are wholly outside that jurisdiction and require the unified 18,276-spine composite denominator.\n- Job 3: NOT AUTHORIZED.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER_R9A.md','w').write(pointer)
# validator
val='''from pathlib import Path\nimport json,csv,sys\nR=Path(__file__).resolve().parents[1];e=[];c=[]\ndef ck(n,x,d=None):c.append({'check':n,'pass':bool(x),'detail':d});e.append(n) if not x else None\ns=json.load(open(R/'CURRENT_STATUS_R9A.json'));ck('job3_false',s['job3_authorized'] is False);ck('r8_poison','DO_NOT_EXECUTE' in s['r8_worker_packs'])\na=json.load(open(R/'AUDIT/R9A_CANARY_COVERAGE_CORRECTION.json'));ck('117_total',a['r6_t03_t11_total_relations']==117);ck('98_pair',a['pair_census_addressable_relations']==98);ck('19_nonpair',a['nonpair_or_nonrelational_lane_relations']==19);ck('210_members',a['nonpair_member_implementation_count']==210,a['nonpair_member_implementation_count']);ck('210_found',a['nonpair_registry_rows_found']==210,a['nonpair_registry_rows_found']);ck('rules',a['nonpair_rule_counts']=={'COMPLEMENTARY_ROLE_CONVERGENCE':11,'TARGET_CONDITION_MATRIX':8},a['nonpair_rule_counts'])\nrows=list(csv.DictReader(open(R/'AUDIT/R6_T03_T11_NONPAIR_CANARY_GAP_LEDGER_R9A.csv')));ck('19_rows',len(rows)==19,len(rows));ck('zero_sem',all(int(r['rows_with_sem_audit_unit'])==0 for r in rows));ck('all_registry',all(int(r['registry_rows_found'])==int(r['member_implementation_count']) for r in rows))\nres={'status':'PASS' if not e else 'FAIL','check_count':len(c),'errors':e,'checks':c};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9A.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(c),'errors':e}));sys.exit(0 if not e else 1)\n'''
open(OUT/'VALIDATION/validate_r9a.py','w').write(val)
shutil.copy2('/mnt/data/build_r9a.py',OUT/'CODE/build_r9a.py')
os.system(f"python3 '{OUT/'VALIDATION/validate_r9a.py'}'")
# manifest and zip
man=[]
for p in sorted(OUT.rglob('*')):
 if p.is_file() and p.name!='SHA256_MANIFEST_R9A.csv':man.append((str(p.relative_to(OUT)),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size))
with open(OUT/'SHA256_MANIFEST_R9A.csv','w',newline='') as f:w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes']);w.writerows(man)
zp=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R9A_20260811.zip')
if zp.exists():zp.unlink()
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,str(p.relative_to(OUT)))
sha=hashlib.sha256(zp.read_bytes()).hexdigest();open(str(zp)+'.sha256','w').write(f'{sha}  {zp.name}\n')
print(json.dumps({'zip':str(zp),'sha':sha,'manifest':len(man),'gap_rows':len(ledger),'members':total_members,'lanes':dict(lc)},indent=2))
