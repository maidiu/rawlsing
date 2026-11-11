from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,sys
B=Path('/mnt/data'); here=Path(__file__).resolve()
R=(here.parents[1] if here.parent.name=='VALIDATION' else B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811')
P=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R11A_20260811'
checks=[];errs=[]
def ck(n,c,d=None):
    ok=bool(c); checks.append({'check':n,'pass':ok,'detail':d});
    if not ok: errs.append(n)
def jl(x):
    if x is None or (isinstance(x,float) and pd.isna(x)) or x=='': return []
    try:return json.loads(x)
    except:return []
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
prov=json.load(open(R/'PROVENANCE/PARENT_PINS_R12.json'))
ck('parent_R11A_pair_posture_hash',prov['R11A_pair_posture_sha256']==sha(P/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz'))
ck('parent_R11A_t06_hash',prov['R11A_T06_full_sha256']==sha(P/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz'))
# sealed parent surfaces
RP=pd.read_csv(P/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz',dtype=str,low_memory=False)
T6=pd.read_csv(P/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',dtype=str,low_memory=False)
SO=pd.read_csv(P/'SOURCE_OBJECTS/R11_SOURCE_NATIVE_OBJECT_OPPORTUNITY_LEDGER.csv',dtype=str).fillna('')
CG=pd.read_csv(P/'SEMANTIC_COLLISIONS/R11_DRIVER_DOMAIN_COLLISION_GROUPS.csv',dtype=str).fillna('')
T6S=pd.read_csv(P/'T06/R11_T06_SAME_TARGET_SEMANTIC_PAIR_OPPORTUNITIES.csv',dtype=str).fillna('')
T7=pd.read_csv(P/'T07/R11_T07_P2_TARGET_RELATION_79_ROW_ACCOUNTING.csv',dtype=str).fillna('')
T8=pd.read_csv(P/'T08/R11_T08_INSTITUTION_CLASS_GROUP_OPPORTUNITIES.csv',dtype=str).fillna('')
A=pd.read_csv(P/'T09_T10/R11_PARALLEL_SOURCE_OBJECT_EQUAL_SIZE_ALIGNMENT_OPPORTUNITIES.csv',dtype=str).fillna('')
T11=pd.read_csv(P/'T11/R11_T11_SAME_TARGET_MULTIROLE_GROUPS.csv',dtype=str).fillna('')
# independently reconstruct packet class counts
expected={'SOURCE_NATIVE_OBJECT':int((pd.to_numeric(SO.mapped_implementation_count)>=2).sum()),'SEMANTIC_COLLISION_GROUP':len(CG)}
sp=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',dtype=str,low_memory=False,usecols=['sem__audit_unit_id','sem__canonical_target_id'])
meta=sp[sp.sem__audit_unit_id.notna()].drop_duplicates('sem__audit_unit_id').set_index('sem__audit_unit_id').sem__canonical_target_id
_tt=T6S.copy(); _tt['target_id']=_tt.unit_a.map(meta)
expected['T06_SAME_TARGET_SEMANTIC_HYPEREDGE']=_tt.groupby(['source_family','wave','target_id']).ngroups
unknown=T6[T6.disposition=='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED']
rest=T6[T6.disposition!='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED']
expected['T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH']=unknown.groupby(['source_family','wave']).ngroups
expected['T06_NORM_ENDPOINT_LINK_WORKBENCH']=rest.groupby(['source_family','wave','semantic_unit_id']).ngroups
expected['T07_P2_TARGET_RELATION_CONCEPT']=len(T7)
expected['T08_INSTITUTION_CLASS_GROUP']=len(T8)
expected['T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT']=A.groupby(['source_family','wave','member_count_each']).ngroups
expected['T11_SAME_TARGET_MULTIROLE_GROUP']=len(T11)
expected['PAIR_RULE_INPUT_AUTHORITY_BLOCKER']=sum(RP.loc[RP[r+'_posture'].str.startswith('INPUT_AUTHORITY_INCOMPLETE',na=False)].groupby(['source_family','wave']).ngroups for r in ['t03','t04','t05','t07','t08','t09','t11'])
PK=pd.read_csv(R/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype=str).fillna('')
ck('packet_ids_unique',PK.packet_id.nunique()==len(PK),(len(PK),PK.packet_id.nunique()))
ck('packet_count_2846',len(PK)==2846,len(PK))
for cls,n in expected.items(): ck('class_'+cls,int((PK.packet_class==cls).sum())==n,(int((PK.packet_class==cls).sum()),n))
ck('expected_class_sum',sum(expected.values())==len(PK),(sum(expected.values()),len(PK)))
raw=pd.to_numeric(PK.raw_primitive_row_count)
ck('source_packet_raw_598',int(raw[PK.packet_class=='SOURCE_NATIVE_OBJECT'].sum())==598,int(raw[PK.packet_class=='SOURCE_NATIVE_OBJECT'].sum()))
ck('collision_raw_410',int(raw[PK.packet_class=='SEMANTIC_COLLISION_GROUP'].sum())==410,int(raw[PK.packet_class=='SEMANTIC_COLLISION_GROUP'].sum()))
ck('t06_same_target_raw_751',int(raw[PK.packet_class=='T06_SAME_TARGET_SEMANTIC_HYPEREDGE'].sum())==751,int(raw[PK.packet_class=='T06_SAME_TARGET_SEMANTIC_HYPEREDGE'].sum()))
ck('t06_norm_block_raw_209121',int(raw[PK.packet_class=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH'].sum())==len(unknown),(int(raw[PK.packet_class=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH'].sum()),len(unknown)))
ck('t06_link_raw_78392',int(raw[PK.packet_class=='T06_NORM_ENDPOINT_LINK_WORKBENCH'].sum())==len(rest),(int(raw[PK.packet_class=='T06_NORM_ENDPOINT_LINK_WORKBENCH'].sum()),len(rest)))
ck('align_raw_1718',int(raw[PK.packet_class=='T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT'].sum())==len(A),(int(raw[PK.packet_class=='T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT'].sum()),len(A)))
# pair trace exact coverage, same canonical row order as parent
M=pd.read_csv(R/'MAPPINGS/R12_PAIR_RULE_TO_PACKET_OR_TERMINAL_MAP.csv.gz',dtype=str,low_memory=False)
ck('pair_trace_rows_364094',len(M)==len(RP),(len(M),len(RP)))
ck('pair_trace_ids_exact',M.pair_id.nunique()==len(RP) and (M.pair_id.values==RP.pair_id.values).all(),(M.pair_id.nunique(),RP.pair_id.nunique()))
packet_ids=set(PK.packet_id); pclass=PK.set_index('packet_id').packet_class.to_dict()
# parse only unique compression refs, then vectorized map
for rid in ['t03','t04','t05','t06','t07','t08','t09','t10','t11']:
    c=rid+'_compression_refs_json'
    uniq=M[c].drop_duplicates()
    parsed={s:jl(s) for s in uniq}
    empty=sum(not v for v in parsed.values())
    bad=[]
    for refs in parsed.values():
        for ref in refs:
            if ref in packet_ids or ref.startswith('TERMINAL:') or ref.startswith('NONPAIR_GRAIN:'): continue
            bad.append(ref)
    ck(rid+'_refs_nonempty',empty==0,empty); ck(rid+'_refs_all_valid',not bad,bad[:10])
    first_map={s:(v[0] if v else '') for s,v in parsed.items()}
    first=M[c].map(first_map)
    mask=RP[rid+'_posture'].str.startswith('INPUT_AUTHORITY_INCOMPLETE',na=False)
    classes=first[mask].map(pclass)
    ck(rid+'_input_blockers_map_to_blocker_packet',classes.eq('PAIR_RULE_INPUT_AUTHORITY_BLOCKER').all() if mask.any() else True,int((classes!='PAIR_RULE_INPUT_AUTHORITY_BLOCKER').sum()) if mask.any() else 0)
# T06 raw exact map
TM=pd.read_csv(R/'MAPPINGS/R12_T06_287513_RAW_TO_PACKET_MAP.csv.gz',dtype=str,low_memory=False)
ck('t06_map_rows_287513',len(TM)==len(T6),(len(TM),len(T6)))
ck('t06_origin_ids_exact',TM.r11_opportunity_id.nunique()==len(T6) and set(TM.r11_opportunity_id)==set(T6.opportunity_id),(TM.r11_opportunity_id.nunique(),T6.opportunity_id.nunique()))
ck('t06_origin_unique',TM.r11_opportunity_id.nunique()==len(TM),TM.r11_opportunity_id.nunique())
disp=T6.set_index('opportunity_id').disposition; joined_disp=TM.r11_opportunity_id.map(disp); cls=TM.r12_packet_id.map(pclass)
want=np.where(joined_disp=='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED','T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH','T06_NORM_ENDPOINT_LINK_WORKBENCH')
ck('t06_map_packet_class_exact',(cls.values==want).all(),int((cls.values!=want).sum()))
# specialized raw origin map exact against packet-listed origins
OM=pd.read_csv(R/'MAPPINGS/R12_SPECIALIZED_ORIGIN_TO_PACKET_MAP.csv.gz',dtype=str,low_memory=False)
listed=[]
for rr in PK[['packet_id','raw_origin_ids_json']].itertuples(index=False):
    listed.extend((o,rr.packet_id) for o in jl(rr.raw_origin_ids_json))
exp=set(listed); got=set(zip(OM.r11_origin_id,OM.r12_packet_id))
ck('specialized_origin_map_exact',got==exp,(len(got),len(exp),len(exp-got),len(got-exp)))
# ancestry
ANC=pd.read_csv(R/'ANCESTRY/R8_89_PACKET_TO_R12_COMPRESSION_CROSSWALK.csv',dtype=str).fillna('')
ck('r8_89_accounted',len(ANC)==89,len(ANC)); ck('r8_zero_unmatched',int(ANC.crosswalk_status.str.startswith('NO_').sum())==0,int(ANC.crosswalk_status.str.startswith('NO_').sum()))
R8C=pd.read_csv(R/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R12_PACKETS.csv',dtype=str).fillna('')
ck('r8c_33_preserved',len(R8C)==33,len(R8C)); ck('r8c_all_revalidation_marked',R8C.r12_revalidation_status.str.contains('PROVISIONAL_R8C_VERDICT_PRESERVED').all())
# governance
st=json.load(open(R/'CURRENT_STATUS_R12.json')); ck('job3_false',st['job3_authorized'] is False)
ptr=open(R/'ACTIVE_EXECUTION_POINTER.md').read(); ck('pointer_job3_not_authorized','NOT AUTHORIZED' in ptr)
ck('r8_packs_do_not_execute',st['summary']['r8_worker_packs']=='DO_NOT_EXECUTE')
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R12.json','w'),indent=2); print(json.dumps(res,indent=2));sys.exit(1 if errs else 0)
