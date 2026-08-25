from pathlib import Path
import pandas as pd, json, hashlib, os, shutil, gzip, csv, collections, re, subprocess, sys
BASE=Path('/mnt/data')
R10=BASE/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811'
OUT=BASE/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811'
if OUT.exists(): shutil.rmtree(OUT)
for d in ['SPINE','R14','AUDIT','VALIDATION','CODE','PROVENANCE','COVERAGE','ANCESTRY']: (OUT/d).mkdir(parents=True,exist_ok=True)
R14P=BASE/'live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json'
SP10=R10/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz'
CW=BASE/'R14_COMPREHENSIVE_OBJECT_CROSSWALK_R10A.csv'; MW=BASE/'R14_COMPREHENSIVE_MEMBER_CROSSWALK_R10A.csv'

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def jl(x):
 if pd.isna(x) or x=='': return []
 try:return json.loads(x)
 except:return []
def jd(xs):return json.dumps(sorted(set(str(x) for x in xs if pd.notna(x) and str(x) not in {'','nan','None'})))

reg=pd.read_csv(SP10,dtype=str,low_memory=False)
orig_cols=list(reg.columns)
cw=pd.read_csv(CW,dtype=str).fillna(''); mw=pd.read_csv(MW,dtype=str).fillna('')
# status on objects
cw['mapping_status']=cw.apply(lambda r: 'FULL_CURRENT_IMPLEMENTATION_CROSSWALK' if int(r.unresolved_member_code_count)==0 and int(r.mapped_implementation_count)>0 else ('PARTIAL_CURRENT_IMPLEMENTATION_CROSSWALK' if int(r.mapped_implementation_count)>0 else 'NO_CURRENT_IMPLEMENTATION_CROSSWALK__SOURCE_OBJECT_RETAINED'),axis=1)
cw.to_csv(OUT/'R14/R14_COMPREHENSIVE_SOURCE_OBJECT_CROSSWALK_R10A.csv',index=False)
mw.to_csv(OUT/'R14/R14_COMPREHENSIVE_SOURCE_MEMBER_CROSSWALK_R10A.csv',index=False)
obj=cw.set_index('object_id').to_dict('index')
# implementation -> corrected object ids
impl_objs=collections.defaultdict(list)
for _,r in cw.iterrows():
 for iid in jl(r.mapped_implementation_ids_json): impl_objs[iid].append(r.object_id)
ids=reg.question_implementation_id.astype(str)
reg['r14c_object_ids_json']=ids.map(lambda x:jd(impl_objs.get(x,[])))
reg['r14c_object_count']=reg.r14c_object_ids_json.map(lambda x:len(jl(x))).astype(str)
for col,key in [
 ('r14c_source_structure_labels_json','source_structure_label'),('r14c_states_json','state'),('r14c_evidence_classes_json','evidence_class'),('r14c_mapping_statuses_json','mapping_status'),('r14c_native_parent_identifiers_json','native_parent_identifier'),('r14c_printed_parent_ids_json','printed_parent_id'),('r14c_source_obligation_ids_json','source_obligation_id')]:
 reg[col]=reg.r14c_object_ids_json.map(lambda x:jd(obj[o].get(key,'') for o in jl(x) if o in obj))
reg['r14c_unresolved_source_member_code_count_sum']=reg.r14c_object_ids_json.map(lambda x:str(sum(int(obj[o].get('unresolved_member_code_count') or 0) for o in jl(x) if o in obj)))
reg['r14c_supersession_law']='R10 r14_* columns are preserved ancestry from first-schema join; r14c_* is the governing comprehensive R14/R15 heterogeneous-schema crosswalk for R10A successors.'
# corrected composite shores: preserve all existing, replace/add corrected R14 shore signal

def corrected_shores(r):
 z=set(jl(r.s14_composite_shores_json))
 if 'R14_SOURCE_NATIVE_STRUCTURE_MEMBER' in z: z.remove('R14_SOURCE_NATIVE_STRUCTURE_MEMBER')
 if int(r.r14c_object_count)>0: z.add('R14_SOURCE_NATIVE_STRUCTURE_MEMBER')
 return jd(z)
reg['s14c_composite_shores_json']=reg.apply(corrected_shores,axis=1)
reg['s14c_composite_shore_count']=reg.s14c_composite_shores_json.map(lambda x:str(len(jl(x))))
# exact preservation of all R10 columns
base=pd.read_csv(SP10,dtype=str,low_memory=False)
assert list(reg.columns[:len(orig_cols)])==orig_cols
for c in orig_cols:
 if not base[c].fillna('__NA__').astype(str).equals(reg[c].fillna('__NA__').astype(str)):
  raise AssertionError(f'R10 parent mutated {c}')
# write gzip
spout=OUT/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz'
reg.to_csv(spout,index=False,compression='gzip')
# object coverage summary
summary={
 'r10_parent_spine_sha256':sha(SP10),'r14_parent_sha256':sha(R14P),'rows':len(reg),'unique_implementation_ids':reg.question_implementation_id.nunique(),
 'r10_parent_column_count':len(orig_cols),'r10a_column_count':len(reg.columns),'appended_r10a_columns':len(reg.columns)-len(orig_cols),
 'r10_old_r14_member_rows':int((pd.to_numeric(reg.r14_object_count,errors='coerce').fillna(0)>0).sum()),
 'r10a_corrected_r14_member_rows':int((pd.to_numeric(reg.r14c_object_count,errors='coerce').fillna(0)>0).sum()),
 'r10_old_unique_r14_objects_mapped':len(set(o for x in reg.r14_object_ids_json.fillna('') for o in jl(x))),
 'r10a_unique_r14_objects_mapped':len(set(o for x in reg.r14c_object_ids_json.fillna('') for o in jl(x))),
 'r14_parent_object_count':len(cw),'r14_parent_member_code_count':int(pd.to_numeric(cw.member_code_count).sum()),
 'r14_mapped_member_occurrences':int(pd.to_numeric(cw.mapped_implementation_count).sum()),'r14_unique_current_implementations_mapped':len(impl_objs),
 'r14_unresolved_source_member_codes':int(pd.to_numeric(cw.unresolved_member_code_count).sum()),
 'r14_objects_full_current_crosswalk':int((cw.mapping_status=='FULL_CURRENT_IMPLEMENTATION_CROSSWALK').sum()),
 'r14_objects_partial_current_crosswalk':int((cw.mapping_status=='PARTIAL_CURRENT_IMPLEMENTATION_CROSSWALK').sum()),
 'r14_objects_no_current_crosswalk':int((cw.mapping_status=='NO_CURRENT_IMPLEMENTATION_CROSSWALK__SOURCE_OBJECT_RETAINED').sum()),
 'ordered_members_schema_objects':int(cw.extraction_methods.str.contains('ordered_members',na=False).sum()),
 'ordered_members_schema_objects_with_current_mapping':int((cw.extraction_methods.str.contains('ordered_members',na=False)&(pd.to_numeric(cw.mapped_implementation_count)>0)).sum()),
 'placeholder_members_mapped_by_structure_label':int((mw.mapping_basis=='STRUCTURE_LABEL_PLUS_ITEM_SUFFIX').sum()),
 'q833_exact_mapping':cw[cw.object_id=='LITS-IV-GROUP-Q833'].iloc[0].mapped_implementation_ids_json if (cw.object_id=='LITS-IV-GROUP-Q833').any() else 'MISSING'
}
json.dump(summary,open(OUT/'AUDIT/R14_HETEROGENEOUS_SCHEMA_CORRECTION_SUMMARY_R10A.json','w'),indent=2)
# all R6 source structure refs vs R14 object set
r6=pd.read_csv(BASE/'live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/INTER_QUESTION_RELATION_AUTHORITY_R2.csv',dtype=str).fillna('')
oids=set(cw.object_id); rr=[]
for _,r in r6.iterrows():
 for sid in jl(r.source_structure_ids):
  rr.append({'relation_authority_id':r.relation_authority_id,'relation_type':r.relation_type,'source_family':r.source_family,'wave':r.wave,'source_structure_id':sid,'present_in_r14_parent':sid in oids,'r14_mapping_status':obj.get(sid,{}).get('mapping_status','NOT_R14_OBJECT')})
pd.DataFrame(rr).to_csv(OUT/'AUDIT/R6_SOURCE_STRUCTURE_REFERENCE_TO_R14_R10A.csv',index=False)
# report/status/checklist
report=f'''# R10A — Unified spine R14 heterogeneous-schema correction\n\n## Finding\nR10 correctly preserved the 18,276-row parent and most joined authorities, but its R14 join consumed only the earlier `members` schema. The sealed R14 parent also contains **296** later objects using `ordered_members` / `member_evidence` (including LiTS/R15 reconciliation). Those were absent from R10's R14 sidecar.\n\nR10A is append-only over R10: all **{len(orig_cols)} R10 columns are preserved byte-semantically**, and new `r14c_*` fields install the comprehensive heterogeneous-schema crosswalk. The old `r14_*` fields remain immutable ancestry and are superseded for future composite-denominator work.\n\n## Corrected coverage\n- R14 objects in sealed parent: **{len(cw)}**\n- ordered-members objects: **{summary['ordered_members_schema_objects']} / {summary['ordered_members_schema_objects_with_current_mapping']} mapped**\n- R10 R14-member implementation rows: **{summary['r10_old_r14_member_rows']}**\n- R10A corrected R14-member implementation rows: **{summary['r10a_corrected_r14_member_rows']}**\n- unique current implementations with R14/R15 source-object membership: **{summary['r14_unique_current_implementations_mapped']}**\n- source-member codes in parent: **{summary['r14_parent_member_code_count']}**; mapped membership occurrences **{summary['r14_mapped_member_occurrences']}**; unresolved source-code tokens **{summary['r14_unresolved_source_member_codes']}**. Unresolved tokens remain explicit source-object crosswalk obligations; no source object is deleted.\n- placeholder `itemN` members deterministically reconciled via source structure label: **{summary['placeholder_members_mapped_by_structure_label']}**.\n- LiTS IV Q833 now maps exactly to q833a/q833b/q833c.\n\n## Governance\nThis correction reopens R10 #2 only long enough to repair the missed R14/R15 membership shore. R10A re-closes #2 subject to independent validation. R11 candidate enumeration must use `r14c_*`, never the superseded R10 `r14_*` sidecar.\n'''
open(OUT/'R10A_R14_CROSSWALK_CORRECTION_REPORT.md','w').write(report)
status={'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811','status':'UNIFIED_SPINE_R14_HETEROGENEOUS_SCHEMA_CORRECTED','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / #14 OPPORTUNITY DENOMINATOR NEXT','job3_authorized':False,'r8_worker_packs':'DO_NOT_EXECUTE','r10_status':'SUPERSEDED_FOR_R14_SIDE_CROSSWALK_ONLY__ALL_OTHER_R10_FIELDS_PRESERVED','item_2_unified_18276_spine':'DONE_AFTER_R10A_CORRECTION','item_3_relation_role_ontology':'DONE_R10','item_14':'ACTIVE_NEXT','governing_r14_fields':'r14c_*','spine_sha256':sha(spout),'summary':summary}
json.dump(status,open(OUT/'CURRENT_STATUS_R10A.json','w'),indent=2)
repair={'done':[1,2,3,7,8],'partial':[4,5,6,9,10,11,12,13,15,16,18,23],'open':[14,17,19,20,21,22,24,25],'correction':'R10A repairs heterogeneous R14/R15 source-object membership crosswalk; #2 re-closed only after this correction.'}
json.dump(repair,open(OUT/'REPAIR_STACK_R10A.json','w'),indent=2)
pointer=f'''# ACTIVE EXECUTION POINTER — R10A\n\nCanonical active checkpoint: `/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R10A_20260811/`\n\nState: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / #14 COMPOSITE OPPORTUNITY DENOMINATOR`.\n\n- #2 unified 18,276 spine: **DONE after R10A heterogeneous R14/R15 crosswalk correction**.\n- #3 orthogonal relation-role ontology: **DONE at schema level**.\n- R10 `r14_*`: preserved superseded ancestry; use **R10A `r14c_*`** for all successor work.\n- R8 66/53/13: revoked for dispatch; W01–W04 **DO NOT EXECUTE**; R8C provisional.\n- Job 3: **NOT AUTHORIZED**.\n- Next: build named R11 S14 opportunity-rule release and denominator-complete T03–T11 ledgers using R10A spine + R9 pair audit + corrected R14/R15 source structures + O04/P2/P3/T08.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER.md','w').write(pointer)
# provenance
prov={'R10_spine':str(SP10),'R10_spine_sha256':sha(SP10),'R14_parent':str(R14P),'R14_parent_sha256':sha(R14P),'comprehensive_crosswalk_builder':'/mnt/data/build_r10a_r14_crosswalk.py','law':'R10A preserves all R10 columns and adds corrected heterogeneous-schema R14 crosswalk sidecar.'}
json.dump(prov,open(OUT/'PROVENANCE/PARENT_PINS_R10A.json','w'),indent=2)
# copy builder scripts
shutil.copy2('/mnt/data/build_r10a_r14_crosswalk.py',OUT/'CODE/build_r10a_r14_crosswalk.py');shutil.copy2('/mnt/data/build_r10a.py',OUT/'CODE/build_r10a.py')
print(json.dumps(summary,indent=2));print('spine sha',sha(spout))
