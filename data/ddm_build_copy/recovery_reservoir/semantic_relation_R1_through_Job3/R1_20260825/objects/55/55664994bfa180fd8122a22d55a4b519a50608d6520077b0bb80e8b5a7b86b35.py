from pathlib import Path
import pandas as pd, json, hashlib, os, collections, shutil

ROOT=Path('/mnt/data/live_parents/o12'); O12=next(ROOT.iterdir()); P=O12/'PARENTS'
R4=Path('/mnt/data/r4_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811')
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811')
if OUT.exists(): shutil.rmtree(OUT)
for d in ['SPINE','INDEX','AUDIT','PROVENANCE','VALIDATION','CODE','COMPOSITE_BASE']:(OUT/d).mkdir(parents=True,exist_ok=True)

def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def jl(x):
 if x is None or (isinstance(x,float) and pd.isna(x)) or x=='':return []
 if isinstance(x,list):return x
 try:
  v=json.loads(x); return v if isinstance(v,list) else [v]
 except:return []
def jd(x):return json.dumps(sorted(set(str(v) for v in x if v is not None and str(v) not in {'','nan'})),separators=(',',':'))

files=['CANONICAL_IMPLEMENTATION_REGISTRY.csv','INTER_QUESTION_RELATION_AUTHORITY_R2.csv','P2_GLOBAL_SEMANTIC_PRIORITY_PAIR_AUTHORITY_18831.csv','P3C_PAIR_RESOLUTION_AUTHORITY.csv','P3C_STRONGER_BOUNDARY_AUTHORITY.csv','R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json','S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv']
pp={n:P/n for n in files}; hashes={n:sha(p) for n,p in pp.items()}
assert hashes['CANONICAL_IMPLEMENTATION_REGISTRY.csv']=='3b53b16cc6d3a3cb2d98a1db197b9b23676f2cd4b1935a3e4fa9dd849b01ac8a'
assert hashes['INTER_QUESTION_RELATION_AUTHORITY_R2.csv']=='dfdc1004d23b31a0461eca412dd06346e30ace37feccec009688ba00ec781e2c'
assert hashes['R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json']=='0f16c23042fc90e8037ac025bac13b3e52695323bd05fc3f6fa76ab45c73cdd8'
reg=pd.read_csv(pp['CANONICAL_IMPLEMENTATION_REGISTRY.csv'],low_memory=False); orig_cols=list(reg.columns); assert len(reg)==18276 and reg.question_implementation_id.nunique()==18276
r6=pd.read_csv(pp['INTER_QUESTION_RELATION_AUTHORITY_R2.csv'],low_memory=False);p2=pd.read_csv(pp['P2_GLOBAL_SEMANTIC_PRIORITY_PAIR_AUTHORITY_18831.csv'],low_memory=False);p3=pd.read_csv(pp['P3C_PAIR_RESOLUTION_AUTHORITY.csv'],low_memory=False);p3b=pd.read_csv(pp['P3C_STRONGER_BOUNDARY_AUTHORITY.csv'],low_memory=False);s16=pd.read_csv(pp['S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS.csv'],low_memory=False);r14=json.load(open(pp['R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json']))
qmeta=reg.set_index('question_implementation_id')[['source_family','wave','source_variable_code']].to_dict('index')
# R6 maps
maps={k:collections.defaultdict(list) for k in ['ids','types','roles','construct','structs']}; cross=[]
for _,r in r6.iterrows():
 mids=jl(r.member_question_implementation_ids);roles=jl(r.member_roles);structs=jl(r.source_structure_ids);active=[]
 for i,m in enumerate(mids):
  if m in qmeta:
   z=qmeta[m];active.append({'question_implementation_id':m,'active_source_family':z['source_family'],'active_wave':str(z['wave']),'source_variable_code':z['source_variable_code'],'member_role':roles[i] if i<len(roles) else None})
   maps['ids'][m].append(r.relation_authority_id);maps['types'][m].append(r.relation_type);maps['construct'][m].append(r.edge_construction_class);maps['structs'][m]+=structs
   if i<len(roles):maps['roles'][m].append(roles[i])
 cross.append({'relation_authority_id':r.relation_authority_id,'relation_type':r.relation_type,'historical_source_family':r.source_family,'historical_wave':str(r.wave),'edge_construction_class':r.edge_construction_class,'active_member_crosswalk_json':json.dumps(active,separators=(',',':')),'active_source_wave_set_json':jd(f"{x['active_source_family']}::{x['active_wave']}" for x in active),'member_count':len(mids),'active_member_count':len(active),'source_structure_ids_json':jd(structs)})
pd.DataFrame(cross).to_csv(OUT/'INDEX/R6_RELATION_ACTIVE_WAVE_CROSSWALK_R10.csv',index=False)
# Pair authority maps
p2m={k:collections.defaultdict(list) for k in ['ids','types','statuses','counter']};nested=collections.Counter();targetrel=collections.Counter();p3m={k:collections.defaultdict(list) for k in ['ids','types','statuses','counter']};p3bm={k:collections.defaultdict(list) for k in ['ids','types','statuses']};pairrows=[]
for _,r in p2.iterrows():
 l,rgt=str(r.left_lineage_id),str(r.right_lineage_id);aid=str(r.global_semantic_authority_id);typ=str(r.original_relation_type);st=str(r.authority_status);pairrows.append({'authority_source':'P2','pair_authority_id':aid,'left_lineage_id':l,'right_lineage_id':rgt,'relation_or_obligation_type':typ,'authority_or_resolution_status':st})
 for a,b in [(l,rgt),(rgt,l)]:
  p2m['ids'][a].append(aid);p2m['types'][a].append(typ);p2m['statuses'][a].append(st);p2m['counter'][a].append(b)
  if typ=='NESTED_TARGET_RELATION_NOT_EQUIVALENT':nested[a]+=1
  if typ in {'NESTED_TARGET_RELATION_NOT_EQUIVALENT','TARGET_RELATION_COORDINATE_ONLY'}:targetrel[a]+=1
for _,r in p3.iterrows():
 l,rgt=str(r.left_object_id),str(r.right_object_id);aid=str(r.adjudication_id);typ=str(r.obligation_type);st=str(r.resolution_status);pairrows.append({'authority_source':'P3C','pair_authority_id':aid,'left_lineage_id':l,'right_lineage_id':rgt,'relation_or_obligation_type':typ,'authority_or_resolution_status':st})
 for a,b in [(l,rgt),(rgt,l)]:p3m['ids'][a].append(aid);p3m['types'][a].append(typ);p3m['statuses'][a].append(st);p3m['counter'][a].append(b)
for _,r in p3b.iterrows():
 l,rgt=str(r.left_object_id),str(r.right_object_id);aid=str(r.adjudication_id);typ=str(r.boundary_kind);st=str(r.disposition);pairrows.append({'authority_source':'P3C_STRONGER_BOUNDARY','pair_authority_id':aid,'left_lineage_id':l,'right_lineage_id':rgt,'relation_or_obligation_type':typ,'authority_or_resolution_status':st})
 for a in [l,rgt]:p3bm['ids'][a].append(aid);p3bm['types'][a].append(typ);p3bm['statuses'][a].append(st)
pd.DataFrame(pairrows).to_csv(OUT/'INDEX/P2_P3_LINEAGE_PAIR_AUTHORITY_INDEX_R10.csv',index=False)
# R14 index
obj={o['object_id']:o for o in r14['objects'] if o.get('object_id')}; accepted={'ACCEPTED_SOURCE_NATIVE_JOINT','ACCEPTED_SOURCE_NATIVE_SINGLETON','JOINT_SOURCE_NATIVE','TERMINAL_SOURCE_NATIVE_WITH_LOCALIZED_BLOCKERS','STANDALONE_SUBSTANTIVE'}
pd.DataFrame([{'object_id':oid,'family_raw':o.get('family'),'wave_raw':o.get('wave'),'state':o.get('state'),'printed_parent_id':o.get('printed_parent_id'),'printed_parent_text':o.get('printed_parent_text'),'evidence_class':o.get('evidence_class'),'member_count':len(o.get('members') or []),'members_json':jd(o.get('members') or []),'routing':o.get('routing'),'universe':o.get('universe'),'applicability':o.get('applicability'),'completion_rule':o.get('completion_rule')} for oid,o in obj.items()]).to_csv(OUT/'INDEX/R14_SOURCE_OBJECT_INDEX_R10.csv',index=False)
# map columns via dict -> Series
q=reg.question_implementation_id.astype(str); lin=reg.lineage_id.fillna('').astype(str)
for dst,src in [('r6_relation_ids_json','ids'),('r6_relation_types_json','types'),('r6_member_roles_json','roles'),('r6_edge_construction_classes_json','construct'),('r6_source_structure_ids_json','structs')]:reg[dst]=q.map(lambda x:jd(maps[src].get(x,[])))
reg['r6_relation_count']=q.map(lambda x:len(set(maps['ids'].get(x,[]))))
rare={'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE'}
reg['r6_t03_t11_relation_count']=q.map(lambda x:len(set(i for i,t in zip(maps['ids'].get(x,[]),maps['types'].get(x,[])) if t in rare)))
for dst,src in [('p2_pair_authority_ids_json','ids'),('p2_pair_relation_types_json','types'),('p2_pair_authority_statuses_json','statuses'),('p2_counterpart_lineage_ids_json','counter')]:reg[dst]=lin.map(lambda x:jd(p2m[src].get(x,[])))
reg['p2_pair_authority_count']=lin.map(lambda x:len(set(p2m['ids'].get(x,[]))));reg['p2_explicit_nested_target_relation_count']=lin.map(nested).fillna(0).astype(int);reg['p2_target_relation_terrain_count']=lin.map(targetrel).fillna(0).astype(int)
for dst,src in [('p3c_adjudication_ids_json','ids'),('p3c_obligation_types_json','types'),('p3c_resolution_statuses_json','statuses'),('p3c_counterpart_lineage_ids_json','counter')]:reg[dst]=lin.map(lambda x:jd(p3m[src].get(x,[])))
reg['p3c_pair_resolution_count']=lin.map(lambda x:len(set(p3m['ids'].get(x,[]))))
for dst,src in [('p3c_stronger_boundary_ids_json','ids'),('p3c_stronger_boundary_kinds_json','types'),('p3c_stronger_boundary_dispositions_json','statuses')]:reg[dst]=lin.map(lambda x:jd(p3bm[src].get(x,[])))
reg['p3c_stronger_boundary_count']=lin.map(lambda x:len(set(p3bm['ids'].get(x,[]))))
# T08 merge by semantic unit
t08p=R4/'NARROWING/T08_INSTITUTION_CLASS_MAPPING_R4.csv'; t08=pd.read_csv(t08p,low_memory=False); hashes['T08_INSTITUTION_CLASS_MAPPING_R4.csv']=sha(t08p)
t8=t08.set_index('sem__audit_unit_id')
for src,dst in [('institution_class','t08_institution_class'),('class_mapping_status','t08_class_mapping_status'),('class_mapping_basis','t08_class_mapping_basis'),('class_mapping_confidence','t08_class_mapping_confidence')]:reg[dst]=reg.sem__audit_unit_id.map(t8[src])
# R14 aggregate metadata from existing membership
r14ids=reg.r14_object_ids_json.map(jl)
reg['r14_object_count']=r14ids.map(lambda z:len(set(z)));reg['r14_accepted_or_terminal_object_count']=r14ids.map(lambda z:sum(1 for x in set(z) if x in obj and obj[x].get('state') in accepted));reg['r14_printed_parent_ids_json']=r14ids.map(lambda z:jd(obj[x].get('printed_parent_id') for x in z if x in obj));reg['r14_states_json']=r14ids.map(lambda z:jd(obj[x].get('state') for x in z if x in obj));reg['r14_evidence_classes_json']=r14ids.map(lambda z:jd(obj[x].get('evidence_class') for x in z if x in obj))
# shore flags
def shores(r):
 z=[]
 if pd.notna(r.sem__audit_unit_id):z.append('RELATIONAL_STRUCTURAL_SEMANTIC')
 if r.o04__central_s2b_disposition=='ACCEPT_ENDPOINT':z.append('O04_ACCEPTED_BEHAVIOR_EXPOSURE_ENDPOINT')
 if r.r14_object_count>0:z.append('R14_SOURCE_NATIVE_STRUCTURE_MEMBER')
 if r.p2_pair_authority_count>0 or r.p3c_pair_resolution_count>0 or r.p3c_stronger_boundary_count>0:z.append('P2_P3_PAIR_OR_BOUNDARY_AUTHORITY_MEMBER')
 if r.semantic_lane in {'non_scalar_evidence','topology','context','structural','substantive','subjective_evidence','relation','position'}:z.append('S14_RELEVANT_SEMANTIC_OR_STRUCTURAL_LANE')
 if pd.notna(r.t08_institution_class):z.append('T08_INSTITUTION_CLASS_MAPPED')
 if r.r6_relation_count>0:z.append('R6_EXISTING_RELATION_MEMBER')
 return jd(z)
reg['s14_composite_shores_json']=reg.apply(shores,axis=1);reg['s14_composite_shore_count']=reg.s14_composite_shores_json.map(lambda x:len(jl(x)))
# parent conservation exact values
base=pd.read_csv(pp['CANONICAL_IMPLEMENTATION_REGISTRY.csv'],low_memory=False);assert list(reg.columns[:len(orig_cols)])==orig_cols
for c in orig_cols:assert base[c].fillna('__NA__').astype(str).equals(reg[c].fillna('__NA__').astype(str)),c
# write uncompressed then gzip fast externally
spcsv=OUT/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv';reg.to_csv(spcsv,index=False)
# indices
sem=reg[reg.sem__audit_unit_id.notna()].copy(); sem['sw']=sem.source_family.astype(str)+'::'+sem.wave.astype(str)
sem.groupby('sem__audit_unit_id').agg(implementation_count=('question_implementation_id','nunique'),question_implementation_ids_json=('question_implementation_id',jd),active_source_waves_json=('sw',jd)).reset_index().to_csv(OUT/'INDEX/SEMANTIC_UNIT_TO_IMPLEMENTATIONS_R10.csv',index=False)
waves=reg.groupby(['source_family','wave'],dropna=False).agg(implementation_count=('question_implementation_id','size'),semantic_unit_membership_rows=('sem__audit_unit_id',lambda x:x.notna().sum()),unique_semantic_units=('sem__audit_unit_id',lambda x:x.dropna().nunique()),accepted_o04_endpoints=('o04__central_s2b_disposition',lambda x:(x=='ACCEPT_ENDPOINT').sum()),r14_member_rows=('r14_object_count',lambda x:(x>0).sum()),p2_p3_authority_member_rows=('p2_pair_authority_count',lambda x:(x>0).sum())).reset_index();waves.to_csv(OUT/'INDEX/SOURCE_WAVE_IMPLEMENTATION_SUMMARY_R10.csv',index=False)
objimpl=collections.defaultdict(list)
for qid,z in zip(reg.question_implementation_id,r14ids):
 for oid in z:objimpl[oid].append(qid)
pd.DataFrame([{'object_id':oid,'registry_mapped_implementation_count':len(set(objimpl.get(oid,[]))),'question_implementation_ids_json':jd(objimpl.get(oid,[])),'state':o.get('state'),'family_raw':o.get('family'),'wave_raw':o.get('wave'),'printed_parent_id':o.get('printed_parent_id')} for oid,o in obj.items()]).to_csv(OUT/'INDEX/R14_OBJECT_TO_IMPLEMENTATIONS_R10.csv',index=False)
sg=s16[s16.rule_id.isin([f'S14-T{x:02d}' for x in range(3,12)])].merge(waves,on=['source_family','wave'],how='left',validate='many_to_one');sg.to_csv(OUT/'INDEX/S16_T03_T11_GATE_WITH_SPINE_COUNTS_R10.csv',index=False)
summary={'spine_rows':len(reg),'unique_implementation_ids':reg.question_implementation_id.nunique(),'parent_column_count':len(orig_cols),'successor_column_count':len(reg.columns),'appended_column_count':len(reg.columns)-len(orig_cols),'semantic_unit_membership_rows':int(reg.sem__audit_unit_id.notna().sum()),'unique_semantic_units':int(reg.sem__audit_unit_id.dropna().nunique()),'accepted_o04_endpoints':int((reg.o04__central_s2b_disposition=='ACCEPT_ENDPOINT').sum()),'r14_member_rows':int((reg.r14_object_count>0).sum()),'p2_pair_authority_member_rows':int((reg.p2_pair_authority_count>0).sum()),'p3c_resolution_member_rows':int((reg.p3c_pair_resolution_count>0).sum()),'p3c_boundary_member_rows':int((reg.p3c_stronger_boundary_count>0).sum()),'r6_relation_member_rows':int((reg.r6_relation_count>0).sum()),'t08_class_mapped_rows':int(reg.t08_institution_class.notna().sum()),'source_wave_groups':int(reg[['source_family','wave']].drop_duplicates().shape[0])}
json.dump(summary,open(OUT/'AUDIT/SPINE_CONSERVATION_SUMMARY_R10.json','w'),indent=2);json.dump({'release_id':'S14-SPINE-R10-20260811','parent_authority_hashes':hashes,'laws':['All 18,276 exact implementation IDs conserved one-to-one.','Parent 182 columns preserved value-for-value; R10 appends authority membership/crosswalk fields only.','P2/P3/R6 membership fields are evidence/jurisdiction locators, not new S14 relation truth.','T08 class mapping is inherited R4 mapping substrate and remains non-final until S14 authority freeze.','Active wave identity follows exact implementation authority; historical display wave labels are ancestry only.']},open(OUT/'PROVENANCE/PARENT_AUTHORITY_HASHES_R10.json','w'),indent=2)
print(json.dumps(summary,indent=2))
