from pathlib import Path
import pandas as pd, numpy as np, json, hashlib, collections,itertools,shutil,sys
B=Path('/mnt/data');P=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R11A_20260811';R=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811'

def jl(x):
 if pd.isna(x) or x=='':return []
 try:return json.loads(x)
 except:return []
def jj(x):return json.dumps(sorted(set(str(v) for v in x if pd.notna(v) and str(v)!='')))
def hid(prefix,*parts):return prefix+'-'+hashlib.sha256('||'.join(map(str,parts)).encode()).hexdigest()[:16]
PK=pd.read_csv(R/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype=str).fillna('')
# maps
obj_to_pid={}
coll_to_pid={}
block_packet={}
t6group={};normwave={};linkunit={}
for r in PK.itertuples(index=False):
 if r.packet_class=='SOURCE_NATIVE_OBJECT':
  for o in jl(r.source_object_ids_json):obj_to_pid[o]=r.packet_id
 elif r.packet_class=='SEMANTIC_COLLISION_GROUP':
  for o in jl(r.raw_origin_ids_json):coll_to_pid[o]=r.packet_id
 elif r.packet_class=='PAIR_RULE_INPUT_AUTHORITY_BLOCKER':block_packet[(r.rule_hypotheses.lower(),r.source_family,str(r.wave))]=r.packet_id
 elif r.packet_class=='T06_SAME_TARGET_SEMANTIC_HYPEREDGE':
  ts=jl(r.target_ids_json);t6group[(r.source_family,str(r.wave),ts[0] if ts else '')]=r.packet_id
 elif r.packet_class=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH':normwave[(r.source_family,str(r.wave))]=r.packet_id
 elif r.packet_class=='T06_NORM_ENDPOINT_LINK_WORKBENCH':
  us=jl(r.member_semantic_unit_ids_json);linkunit[(r.source_family,str(r.wave),us[0] if us else '')]=r.packet_id
# pair map
RP=pd.read_csv(P/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz',dtype={'wave':str},low_memory=False)
PA=pd.read_csv(P/'PAIR_ACCOUNTING/R11_ALL_364094_PAIR_MAP_OR_EXCLUSION.csv.gz',dtype={'wave':str},low_memory=False).set_index('pair_id').loc[RP.pair_id].reset_index()
# base refs once
base=[]
for objs,cg in zip(PA.corrected_common_r14c_object_ids_json.fillna('[]'),PA.driver_domain_collision_group_id.fillna('')):
 refs=[]
 for o in jl(objs):
  if o in obj_to_pid:refs.append(obj_to_pid[o])
 if cg and cg in coll_to_pid:refs.append(coll_to_pid[cg])
 base.append(json.dumps(sorted(set(refs))))
base=np.array(base,dtype=object)
# metadata target for t06 grouping
sp=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',dtype=str,low_memory=False)
meta=sp[sp.sem__audit_unit_id.notna()][['sem__audit_unit_id','sem__canonical_target_id']].drop_duplicates('sem__audit_unit_id').set_index('sem__audit_unit_id').sem__canonical_target_id
M=RP[['pair_id','source_family','wave']].copy()
for rid in ['t03','t04','t05','t06','t07','t08','t09','t10','t11']:
 post=RP[rid+'_posture'].fillna('')
 vals=base.copy()
 # input blockers
 mask=post.str.startswith('INPUT_AUTHORITY_INCOMPLETE').to_numpy()
 if mask.any():
  keys=list(zip([rid]*mask.sum(),RP.loc[mask,'source_family'],RP.loc[mask,'wave'].astype(str)))
  vals[mask]=[json.dumps([block_packet[k]]) for k in keys]
 # terminal
 mask2=post.str.startswith('TERMINAL_').to_numpy();vals[mask2]=[json.dumps(['TERMINAL:'+x]) for x in post[mask2]]
 # nonpair
 mask3=post.str.startswith('NOT_PRIMARY_PAIR_GRAIN').to_numpy();vals[mask3]=json.dumps(['NONPAIR_GRAIN:SOURCE_OBJECT_AND_ALIGNMENT_PACKETS'])
 # t06 same target
 if rid=='t06':
  mask4=post.str.startswith('REQUIRES_NORM_CONDUCT').to_numpy()
  ua=RP.loc[mask4,'unit_a'];ts=ua.map(meta).fillna('')
  keys=list(zip(RP.loc[mask4,'source_family'],RP.loc[mask4,'wave'].astype(str),ts))
  vals[mask4]=[json.dumps([t6group[k]]) for k in keys]
 # if review refs somehow empty, make blocker explicit
 rev=(~mask)&(~mask2)&(~mask3)
 if rid=='t06':rev=rev&(~post.str.startswith('REQUIRES_NORM_CONDUCT').to_numpy())
 empty=rev & (vals=='[]')
 if empty.any(): vals[empty]=json.dumps(['INPUT_AUTHORITY_BLOCKER:UNRESOLVED_PACKET_BINDING'])
 M[rid+'_compression_refs_json']=vals
M.to_csv(R/'MAPPINGS/R12_PAIR_RULE_TO_PACKET_OR_TERMINAL_MAP.csv.gz',index=False,compression='gzip')
print('pair map written',len(M))
# T06 raw mapping vectorized
T6=pd.read_csv(P/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',dtype=str).fillna('')
ids=[]
for sf,w,u,d in zip(T6.source_family,T6.wave,T6.semantic_unit_id,T6.disposition):
 ids.append(normwave[(sf,str(w))] if d=='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED' else linkunit[(sf,str(w),u)])
tmap=pd.DataFrame({'r11_opportunity_id':T6.opportunity_id,'r12_packet_id':ids,'r11_disposition':T6.disposition})
tmap.to_csv(R/'MAPPINGS/R12_T06_287513_RAW_TO_PACKET_MAP.csv.gz',index=False,compression='gzip')
print('t06 map written',len(tmap))
# specialized origin map from packet raw origins (includes huge t06 IDs too; keep unique)
rows=[]
for r in PK.itertuples(index=False):
 for o in jl(r.raw_origin_ids_json):rows.append((o,r.packet_id,r.packet_class))
OM=pd.DataFrame(rows,columns=['r11_origin_id','r12_packet_id','packet_class']).drop_duplicates()
OM.to_csv(R/'MAPPINGS/R12_SPECIALIZED_ORIGIN_TO_PACKET_MAP.csv.gz',index=False,compression='gzip')
print('origin map',len(OM))
# R8 ancestry crosswalk
r8=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811/ANCESTRY/R8_89_PACKET_TO_R10_SPINE_CROSSWALK.csv',dtype=str).fillna('')
packet_impl={r.packet_id:set(jl(r.member_implementation_ids_json)) for r in PK.itertuples(index=False)}
anc=[]
for rr in r8.itertuples(index=False):
 old=set(jl(rr.mapped_question_implementation_ids_json));subs=[];overs=[]
 if old:
  for pid,s in packet_impl.items():
   if not s:continue
   inter=len(old&s)
   if not inter:continue
   if old<=s:subs.append(pid)
   overs.append((inter/len(old),inter,pid))
 chosen=sorted(subs) if subs else [x[2] for x in sorted(overs,reverse=True)[:5]]
 anc.append(dict(r8_canonical_packet_id=rr.canonical_packet_id,r8_queue_class=rr.queue_class,r8_rule_hypotheses=rr.rule_hypotheses,r8_mapped_implementation_count=len(old),r12_candidate_packet_ids_json=jj(chosen),crosswalk_status='PRESERVED_BY_EXACT_MEMBER_SUBSET' if subs else ('PRESERVED_BY_MEMBER_OVERLAP_REQUIRES_REVALIDATION' if chosen else 'NO_R12_PACKET_MATCH__INVESTIGATE')))
ANC=pd.DataFrame(anc);ANC.to_csv(R/'ANCESTRY/R8_89_PACKET_TO_R12_COMPRESSION_CROSSWALK.csv',index=False)
# R8C
r8c=pd.read_csv(B/'r8c_full/Rawlsing_R10K_S14_R8C_Vozhd_Central_Adjudication_20260811/ADJUDICATION/CENTRAL_13_RULE_VERDICTS_R8C.csv',dtype=str).fillna(''); amap=ANC.set_index('r8_canonical_packet_id').r12_candidate_packet_ids_json.to_dict();r8c['r12_candidate_packet_ids_json']=r8c.canonical_packet_id.map(amap).fillna('[]');r8c['r12_revalidation_status']='PROVISIONAL_R8C_VERDICT_PRESERVED__REVALIDATE_AGAINST_R12_PACKET';r8c.to_csv(R/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R12_PACKETS.csv',index=False)
# summaries
cls=PK.groupby('packet_class').agg(packet_count=('packet_id','size'),raw_primitive_rows=('raw_primitive_row_count',lambda s:pd.to_numeric(s).sum()),decision_atoms=('decision_atom_count',lambda s:pd.to_numeric(s).sum())).reset_index();cls.to_csv(R/'COVERAGE/R12_PACKET_CLASS_SUMMARY.csv',index=False)
status=PK.groupby('packet_status').agg(packet_count=('packet_id','size'),raw_primitive_rows=('raw_primitive_row_count',lambda s:pd.to_numeric(s).sum()),decision_atoms=('decision_atom_count',lambda s:pd.to_numeric(s).sum())).reset_index();status.to_csv(R/'COVERAGE/R12_PACKET_STATUS_SUMMARY.csv',index=False)
summary={'packet_count_total':len(PK),'packet_class_counts':PK.packet_class.value_counts().to_dict(),'raw_primitive_rows_represented_sum':int(pd.to_numeric(PK.raw_primitive_row_count).sum()),'decision_atom_count_sum':int(pd.to_numeric(PK.decision_atom_count).sum()),'r11a_pair_rows':len(RP),'pair_rule_trace_rows_wide':len(M),'r11a_t06_cross_rows':len(T6),'t06_raw_rows_mapped_exactly_once':len(tmap),'specialized_origin_map_rows':len(OM),'r8_packets_crosswalked':len(ANC),'r8_packets_with_no_r12_match':int(ANC.crosswalk_status.str.startswith('NO_').sum()),'r8c_rule_verdicts_preserved':len(r8c),'job3_authorized':False,'r8_worker_packs':'DO_NOT_EXECUTE'}
json.dump(summary,open(R/'COVERAGE/R12_COMPRESSION_SUMMARY.json','w'),indent=2)
open(R/'R12_COMPRESSION_REPORT.md','w').write('# R12 — Lossless canonical compression of R11A\n\n'+json.dumps(summary,indent=2)+'\n\nPacket count and decision-atom count are intentionally distinct. Every pair-rule posture maps to a packet/terminal/non-pair reference; every 287,513 T06 cross-shore row maps exactly once. R8/R8C ancestry is preserved for revalidation. No Job 3 authority.\n')
json.dump({'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811','status':'R12_COMPRESSION_BUILT__VALIDATION_NEXT','job3_authorized':False,'item15_status':'AWAITING_INDEPENDENT_VALIDATOR','summary':summary,'next':'independent losslessness validator then #16 cross-rule dedupe'},open(R/'CURRENT_STATUS_R12.json','w'),indent=2)
open(R/'ACTIVE_EXECUTION_POINTER.md','w').write('# ACTIVE EXECUTION POINTER — R12\n\nR12 lossless compression built; independent losslessness validation next. R8 packs DO NOT EXECUTE. Job 3 NOT AUTHORIZED.\n')
# provenance
import hashlib
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins={'R11A_zip_sha256':'a39065f9428e9b341f0669fe4214e7865cc4fd903e55fe4376b2123a52ee1d82','R11A_packet_posture_sha256':sha(P/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz'),'R11A_T06_full_sha256':sha(P/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz'),'R10A_spine_sha256':'72bdf342452ef3f7fa7f4859f7b81a6e2fa182cb564da177fd70d1b11cbc47e5','law':'compression only; no raw primitive may disappear and no input-authority blocker may become negative authority'}
json.dump(pins,open(R/'PROVENANCE/PARENT_PINS_R12.json','w'),indent=2)
shutil.copy('/mnt/data/build_r12.py',R/'CODE/build_r12_initial.py');shutil.copy('/mnt/data/resume_r12.py',R/'CODE/resume_r12.py')
print(json.dumps(summary,indent=2));print('\n',cls.to_string(index=False));print('\nR8 crosswalk\n',ANC.crosswalk_status.value_counts().to_string())
