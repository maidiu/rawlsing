from pathlib import Path
import pandas as pd,json,hashlib,gzip,sys,os
R=Path(__file__).resolve().parents[1]
P=Path('/mnt/data/live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS')
errs=[]; checks=[]
def ck(n,c,d=None):
    checks.append({'check':n,'pass':bool(c),'detail':d});
    if not c: errs.append(n)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
sp_path=R/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz'
try:
 with gzip.open(sp_path,'rb') as f:
  while f.read(1024*1024): pass
 ck('gzip_integrity',True)
except Exception as e: ck('gzip_integrity',False,str(e))
sp=pd.read_csv(sp_path,low_memory=False); parent=pd.read_csv(P/'CANONICAL_IMPLEMENTATION_REGISTRY.csv',low_memory=False)
ck('spine_18276',len(sp)==18276,len(sp)); ck('spine_unique_ids',sp.question_implementation_id.nunique()==18276,sp.question_implementation_id.nunique())
ck('parent_18276',len(parent)==18276,len(parent)); ck('parent_cols_182',len(parent.columns)==182,len(parent.columns)); ck('successor_cols_216',len(sp.columns)==216,len(sp.columns))
ck('first_182_column_names_exact',sp.columns[:182].tolist()==parent.columns.tolist())
# compare all parent fields row-keyed, normalized NA
s=sp.set_index('question_implementation_id'); p=parent.set_index('question_implementation_id'); ck('same_id_set',set(s.index)==set(p.index))
mut=0
for c in parent.columns:
 if c=='question_implementation_id': continue
 a=s.loc[p.index,c].fillna('<NA>').astype(str); b=p[c].fillna('<NA>').astype(str)
 mut += int((a.values!=b.values).sum())
ck('parent_value_mutations_zero',mut==0,mut)
ck('semantic_membership_rows_4575',int(sp.sem__audit_unit_id.notna().sum())==4575,int(sp.sem__audit_unit_id.notna().sum()))
ck('semantic_units_3324',sp.sem__audit_unit_id.dropna().nunique()==3324,sp.sem__audit_unit_id.dropna().nunique())
ck('source_wave_groups_35',sp.groupby(['source_family','wave']).ngroups==35,sp.groupby(['source_family','wave']).ngroups)
ck('o04_accept_2113',int(sp.o04__central_s2b_disposition.fillna('').eq('ACCEPT_ENDPOINT').sum())==2113,int(sp.o04__central_s2b_disposition.fillna('').eq('ACCEPT_ENDPOINT').sum()))
ck('r14_member_rows_2456',int((sp.r14_object_count.fillna(0)>0).sum())==2456,int((sp.r14_object_count.fillna(0)>0).sum()))
# parent hashes
known={'CANONICAL_IMPLEMENTATION_REGISTRY.csv':'3b53b16cc6d3a3cb2d98a1db197b9b23676f2cd4b1935a3e4fa9dd849b01ac8a','INTER_QUESTION_RELATION_AUTHORITY_R2.csv':'dfdc1004d23b31a0461eca412dd06346e30ace37feccec009688ba00ec781e2c','P2_GLOBAL_SEMANTIC_PRIORITY_PAIR_AUTHORITY_18831.csv':'f70a84646a232153164f73fa912cb80b64b3ecebbb713cfeac9de175601e5c38','P3C_PAIR_RESOLUTION_AUTHORITY.csv':'ace058e91fbacae8cc18e4b35a1178c785b48558d7e100f7218e325496097237','R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json':'0f16c23042fc90e8037ac025bac13b3e52695323bd05fc3f6fa76ab45c73cdd8'}
for fn,h in known.items(): ck('parent_hash_'+fn,sha(P/fn)==h,sha(P/fn))
# independent R6 canary reconstruction from parent R6 IDs directly to current spine
r6=pd.read_csv(P/'INTER_QUESTION_RELATION_AUTHORITY_R2.csv',low_memory=False)
types={'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE'}
rr=r6[r6.relation_type.isin(types)]
ck('r6_t03_t11_relations_117',len(rr)==117,len(rr))
spids=set(sp.question_implementation_id.astype(str)); missing=[]
for _,r in rr.iterrows():
 try: ids=[str(x) for x in json.loads(r.member_question_implementation_ids)]
 except: ids=[]
 miss=[x for x in ids if x and x not in spids]
 if miss: missing.append((r.relation_authority_id,miss))
ck('all_117_canaries_exact_members_on_spine',not missing,missing[:5])
# generated crosswalk agrees 366 relation rows, with only inherited explicit blank member deficit outside T03-T11
cw=pd.read_csv(R/'INDEX/R6_RELATION_ACTIVE_WAVE_CROSSWALK_R10.csv')
ck('r6_crosswalk_366',len(cw)==366,len(cw)); ck('r6_crosswalk_unique_366',cw.relation_authority_id.nunique()==366,cw.relation_authority_id.nunique())
gaps=cw[cw.member_count!=cw.active_member_count]
ck('r6_only_one_inherited_member_gap',len(gaps)==1 and gaps.iloc[0].relation_authority_id=='IQRA-R2-e3b15659c96d331d0bdf',gaps[['relation_authority_id','member_count','active_member_count']].to_dict('records'))
# ontology coverage
ont=pd.read_csv(R/'ONTOLOGY/RELATION_ROLE_ONTOLOGY_R10.csv'); ct=pd.read_csv(R/'COVERAGE/S14_T03_T11_INPUT_CONTRACT_STATUS_R10.csv')
ck('ontology_nonempty',len(ont)>=20,len(ont)); ck('contract_9_rules',len(ct)==9,len(ct)); ck('job3_not_authorized_contract',(~ct.job3_authorized.astype(bool)).all())
ck('no_final_absence_authorized',(~ct.candidate_generation_authorized_for_final_absence_claim.astype(bool)).all())
# composite shore census 35*9
shore=pd.read_csv(R/'COVERAGE/S14_T03_T11_COMPOSITE_SHORE_CENSUS_BY_WAVE_R10.csv')
ck('shore_cells_315',len(shore)==315,len(shore)); ck('shore_35_waves',shore.groupby(['source_family','wave']).ngroups==35,shore.groupby(['source_family','wave']).ngroups); ck('shore_9_rules',shore.rule_id.nunique()==9,shore.rule_id.nunique())
ck('all_shore_cells_fail_closed',shore.denominator_completion_status.eq('INPUT_AUTHORITY_INCOMPLETE__NO_FINAL_ABSENCE_CLAIM').all())
# ancestry no loss: 89 rows + 33 central verdict rows retained, even if packet surface cannot yield exact impl mapping
ac=pd.read_csv(R/'ANCESTRY/R8_89_PACKET_TO_R10_SPINE_CROSSWALK.csv'); av=pd.read_csv(R/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R10_SPINE_CROSSWALK.csv')
ck('r8_packet_rows_preserved_89',len(ac)==89,len(ac)); ck('r8_packet_ids_unique_89',ac.canonical_packet_id.nunique()==89,ac.canonical_packet_id.nunique()); ck('r8c_verdict_rows_preserved_33',len(av)==33,len(av))
# R9 pair base hash and scope
pp=json.load(open(R/'PROVENANCE/R9_PAIR_CENSUS_POINTER_R10.json')); ck('r9_pair_count_364094',pp['pair_count']==364094,pp['pair_count']); ck('r9_pair_hash',pp['local_sha256']=='51f8e5e6f345181a03f66c6073b22391fa9539c9a57c80a7e40bfa66c2e07138',pp['local_sha256'])
# R4 T08 unresolved status must stay visible
m=pd.read_csv(R/'COVERAGE/T08_CLASS_MAPPING_STATUS_CENSUS_R10.csv'); unresolved=int(m[m.class_mapping_status.astype(str).str.contains('REVIEW_REQUIRED',na=False)].semantic_unit_count.sum())
ck('t08_review_required_visible',unresolved==32,unresolved)
# status state
st=json.load(open(R/'CURRENT_STATUS_R10.json')); ck('job3_false',st['job3_authorized'] is False); ck('r8_packs_poisoned',st['r8_worker_packs']=='DO_NOT_EXECUTE'); ck('item14_open',st['repair_item_14_composite_denominator']=='ACTIVE_NOT_COMPLETE')
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R10.json','w'),indent=2)
print(json.dumps({'status':res['status'],'check_count':len(checks),'errors':errs},indent=2))
sys.exit(1 if errs else 0)
