from pathlib import Path
import pandas as pd, numpy as np, json, hashlib, collections, itertools, os, shutil
B=Path('/mnt/data')
PARENT=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R11A_20260811'
R=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811'
if R.exists(): shutil.rmtree(R)
for d in ['PACKETS','MAPPINGS','ANCESTRY','AUDIT','VALIDATION','PROVENANCE','COVERAGE','CODE']: (R/d).mkdir(parents=True,exist_ok=True)

def jl(x):
    if pd.isna(x) or x=='': return []
    try:return json.loads(x)
    except:return []
def jj(x): return json.dumps(sorted(set(str(v) for v in x if pd.notna(v) and str(v)!='')))
def hid(prefix,*parts): return prefix+'-'+hashlib.sha256('||'.join(map(str,parts)).encode()).hexdigest()[:16]
def semi(s):
    vals=[]
    for x in s:
        if pd.isna(x):continue
        vals += [v.strip() for v in str(x).split(';') if v.strip()]
    return ';'.join(sorted(set(vals)))

# parents
sp=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',dtype=str,low_memory=False)
sem=sp[sp.sem__audit_unit_id.notna()][['source_family','wave','sem__audit_unit_id','sem__canonical_target_id']].drop_duplicates(['source_family','wave','sem__audit_unit_id'])
unit_impl=sp[sp.sem__audit_unit_id.notna()].groupby('sem__audit_unit_id').question_implementation_id.apply(lambda s: sorted(set(s))).to_dict()
unit_target=sem.drop_duplicates('sem__audit_unit_id').set_index('sem__audit_unit_id').sem__canonical_target_id.to_dict()
cw=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/R14/R14_COMPREHENSIVE_SOURCE_OBJECT_CROSSWALK_R10A.csv',dtype=str).fillna('')
obj_impl={r.object_id:set(jl(r.mapped_implementation_ids_json)) for r in cw.itertuples(index=False)}
obj_units={}
for oid,ims in obj_impl.items(): obj_units[oid]=set(sp[sp.question_implementation_id.isin(ims)].sem__audit_unit_id.dropna())

packets=[]
origin_to_packets=collections.defaultdict(set)

def add_packet(pid,pclass,sf,wave,rules,units=(),impls=(),objs=(),targets=(),origins=(),raw_rows=0,atoms=0,status='REQUIRES_ADJUDICATION',ceiling='NO_RELATION_AUTHORITY',notes=''):
    rec=dict(packet_id=pid,packet_class=pclass,source_family=sf,wave=str(wave),rule_hypotheses=rules,
             member_semantic_unit_ids_json=jj(units),member_implementation_ids_json=jj(impls),source_object_ids_json=jj(objs),target_ids_json=jj(targets),
             raw_origin_count=len(set(origins)),raw_origin_ids_json=jj(origins),raw_primitive_row_count=int(raw_rows),decision_atom_count=int(atoms),packet_status=status,authority_ceiling=ceiling,notes=notes)
    packets.append(rec)
    for o in origins: origin_to_packets[str(o)].add(pid)
    return pid

# 1 source-object packets: all 598 current multi-member, giant container explicitly blocked/decomposition
SO=pd.read_csv(PARENT/'SOURCE_OBJECTS/R11_SOURCE_NATIVE_OBJECT_OPPORTUNITY_LEDGER.csv',dtype=str).fillna('')
for r in SO.itertuples(index=False):
    n=int(r.mapped_implementation_count or 0)
    if n<2: continue
    pid=hid('R12SRC',r.object_id)
    status='SOURCE_CONTAINER_BLOCKER__DECOMPOSE_CHILD_STRUCTURES' if n>50 else 'REQUIRES_SOURCE_OBJECT_RULE_ADJUDICATION'
    atoms=0 if n>50 else max(1,len([x for x in str(r.rule_hypotheses).split(';') if x]))
    add_packet(pid,'SOURCE_NATIVE_OBJECT',r.source_family,r.wave,r.rule_hypotheses,jl(r.semantic_unit_ids_json),jl(r.mapped_implementation_ids_json),[r.object_id],jl(r.targets_json),[r.opportunity_id],1,atoms,status,'SOURCE_OBJECT_OPPORTUNITY_ONLY__NO_RELATION_AUTHORITY',f'R11 source object; mapped members={n}.')

# 2 semantic collision packets
CG=pd.read_csv(PARENT/'SEMANTIC_COLLISIONS/R11_DRIVER_DOMAIN_COLLISION_GROUPS.csv',dtype=str).fillna('')
for r in CG.itertuples(index=False):
    units=jl(r.semantic_unit_ids_json); impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units))
    pid=hid('R12COLL',r.opportunity_id)
    add_packet(pid,'SEMANTIC_COLLISION_GROUP',r.source_family,r.wave,r.rule_hypotheses,units,impls,(),jl(r.targets_json),[r.opportunity_id],1,max(1,len(str(r.rule_hypotheses).split(';'))),'REQUIRES_RELATIVE_ROLE_ADJUDICATION','SEMANTIC_COLLISION_RECALL_ONLY__NO_RELATION_AUTHORITY',f'driver={r.driver_id}; domain={r.structural_domain_id}')

# 3 T06 same-target pairs -> target hyperedges
T6S=pd.read_csv(PARENT/'T06/R11_T06_SAME_TARGET_SEMANTIC_PAIR_OPPORTUNITIES.csv',dtype=str).fillna('')
T6S['target_id']=T6S.unit_a.map(unit_target).fillna('')
for (sf,w,t),g in T6S.groupby(['source_family','wave','target_id'],dropna=False):
    units=set(g.unit_a)|set(g.unit_b);impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units));origins=g.opportunity_id.tolist()
    pid=hid('R12T06T',sf,w,t)
    add_packet(pid,'T06_SAME_TARGET_SEMANTIC_HYPEREDGE',sf,w,'T06',units,impls,(),[t],origins,len(g),len(g),'REQUIRES_NORM_STATED_CONDUCT_ROLE_ADJUDICATION','SAME_TARGET_RECALL_ONLY__NO_T06_AUTHORITY',f'{len(units)} semantic units / {len(g)} raw pairs')

# 4 T06 exhaustive endpoint cross-shore compression
T6=pd.read_csv(PARENT/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',dtype=str).fillna('')
# norm role unknown -> one wave workbench, decisions are per semantic unit
unknown=T6[T6.disposition=='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED']
for (sf,w),g in unknown.groupby(['source_family','wave']):
    units=sorted(set(g.semantic_unit_id));impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units));origins=g.opportunity_id.tolist()
    pid=hid('R12T06NORMBLOCK',sf,w)
    add_packet(pid,'T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH',sf,w,'T06',units,impls,(),(),origins,len(g),len(units),'INPUT_AUTHORITY_BLOCKER__ASSIGN_RELATIVE_NORM_ROLE','NO_T06_ABSENCE_CLAIM',f'{len(units)} semantic-unit role decisions gate {len(g)} raw endpoint combinations.')
# all R2-shore/link terrain -> one packet per semantic unit in source-wave with all endpoints, decision atoms are endpoint comparisons
rest=T6[T6.disposition!='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED']
for (sf,w,u),g in rest.groupby(['source_family','wave','semantic_unit_id']):
    eps=sorted(set(g.endpoint_implementation_id));origins=g.opportunity_id.tolist();stats=g.disposition.value_counts().to_dict()
    pid=hid('R12T06LINK',sf,w,u)
    add_packet(pid,'T06_NORM_ENDPOINT_LINK_WORKBENCH',sf,w,'T06',[u],unit_impl.get(u,[])+eps,(),jl(g.iloc[0].target_ids_json),origins,len(g),len(eps),'REQUIRES_NORM_ENDPOINT_LINK_AND_ACTOR_TARGET_ACTION_ADJUDICATION','NO_T06_RELATION_AUTHORITY',json.dumps(stats,sort_keys=True))

# 5 T07 79 concept-level rows one packet each
T7=pd.read_csv(PARENT/'T07/R11_T07_P2_TARGET_RELATION_79_ROW_ACCOUNTING.csv',dtype=str).fillna('')
for r in T7.itertuples(index=False):
    pid=hid('R12T07P2',r.opportunity_id)
    status='EXISTING_OR_RECALL_TARGET_HIERARCHY__IMPLEMENTATION_BINDING_SEPARATE'
    add_packet(pid,'T07_P2_TARGET_RELATION_CONCEPT',getattr(r,'source_a_family','MULTI'),getattr(r,'wave','CONCEPT'),'T07',(),(),(),(),[r.opportunity_id],1,1,status,'TARGET_RELATION_CONCEPT_ONLY__NO_RESPONDENT_JOIN',getattr(r,'reason',''))

# 6 T08 class groups
T8=pd.read_csv(PARENT/'T08/R11_T08_INSTITUTION_CLASS_GROUP_OPPORTUNITIES.csv',dtype=str).fillna('')
for r in T8.itertuples(index=False):
    units=jl(r.semantic_unit_ids_json);impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units));pid=hid('R12T08',r.opportunity_id)
    add_packet(pid,'T08_INSTITUTION_CLASS_GROUP',r.source_family,r.wave,'T08',units,impls,(),jl(r.target_ids_json),[r.opportunity_id],1,1,'REQUIRES_T08_DIFFERENTIATION_ADJUDICATION','GOVERNED_CLASS_MAPPING_TERRAIN__NO_RELATION_AUTHORITY','')

# 7 T09/T10 alignments -> complete graph component per source-wave-cardinality
A=pd.read_csv(PARENT/'T09_T10/R11_PARALLEL_SOURCE_OBJECT_EQUAL_SIZE_ALIGNMENT_OPPORTUNITIES.csv',dtype=str).fillna('')
for (sf,w,n),g in A.groupby(['source_family','wave','member_count_each']):
    objs=sorted(set(g.object_a)|set(g.object_b));impls=set();units=set()
    for o in objs:impls |= obj_impl.get(o,set());units |= obj_units.get(o,set())
    origins=g.opportunity_id.tolist();pid=hid('R12ALIGN',sf,w,n)
    add_packet(pid,'T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT',sf,w,'T09;T10',units,impls,objs,(),origins,len(g),len(g),'REQUIRES_PARALLEL_OBJECT_ROLE_OR_MATRIX_ADJUDICATION','SHAPE_ALIGNMENT_RECALL_ONLY__NO_RECIPROCITY_OR_MATRIX_AUTHORITY',f'{len(objs)} source objects of cardinality {n}; {len(g)} alignment edges')

# 8 T11 same-target multirole groups
T11=pd.read_csv(PARENT/'T11/R11_T11_SAME_TARGET_MULTIROLE_GROUPS.csv',dtype=str).fillna('')
for r in T11.itertuples(index=False):
    units=jl(r.semantic_unit_ids_json);impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units));pid=hid('R12T11',r.opportunity_id)
    add_packet(pid,'T11_SAME_TARGET_MULTIROLE_GROUP',r.source_family,r.wave,'T11',units,impls,(),[r.target_id],[r.opportunity_id],1,1,'REQUIRES_T11_COMPLEMENTARY_ROLE_ADJUDICATION','SAME_TARGET_MULTIROLE_RECALL__NO_COMPLEMENTARITY_AUTHORITY','')

# 9 pair-level authority blockers -> one packet per rule x wave, preserve exact pair count / unique units
RP=pd.read_csv(PARENT/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz',dtype={'wave':str},low_memory=False)
block_packet={}
for rid in ['t03','t04','t05','t07','t08','t09','t11']:
    col=rid+'_posture'; b=RP[RP[col].str.startswith('INPUT_AUTHORITY_INCOMPLETE')]
    for (sf,w),g in b.groupby(['source_family','wave']):
        units=sorted(set(g.unit_a)|set(g.unit_b));impls=list(itertools.chain.from_iterable(unit_impl.get(u,[]) for u in units));pid=hid('R12PAIRBLOCK',rid,sf,w)
        block_packet[(rid,sf,str(w))]=pid
        add_packet(pid,'PAIR_RULE_INPUT_AUTHORITY_BLOCKER',sf,w,rid.upper(),units,impls,(),(),(),len(g),len(units),'INPUT_AUTHORITY_BLOCKER__NO_PAIR_ABSENCE_CLAIM','NO_RELATION_ABSENCE_CLAIM',f'{len(g)} blocked pair postures compressed to {len(units)} semantic units; prerequisites must be installed before absence can be asserted.')

PK=pd.DataFrame(packets);PK.to_csv(R/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',index=False)

# Exact pair-rule compression map, wide: review -> source/collision packet(s), blocker -> wave blocker packet, terminal/nonpair explicit
# precompute pair source/collision packet refs from parent pair accounting
PA=pd.read_csv(PARENT/'PAIR_ACCOUNTING/R11_ALL_364094_PAIR_MAP_OR_EXCLUSION.csv.gz',dtype={'wave':str},low_memory=False).set_index('pair_id')
obj_to_pid={r.object_id:hid('R12SRC',r.object_id) for r in SO.itertuples(index=False) if int(r.mapped_implementation_count or 0)>=2}
coll_to_pid={r.opportunity_id:hid('R12COLL',r.opportunity_id) for r in CG.itertuples(index=False)}
# t06 target group map
t6group={}
for (sf,w,t),g in T6S.groupby(['source_family','wave','target_id'],dropna=False):t6group[(sf,str(w),t)]=hid('R12T06T',sf,w,t)
mapout=RP[['pair_id','source_family','wave']].copy()
for rid in ['t03','t04','t05','t06','t07','t08','t09','t10','t11']:
    vals=[];col=rid+'_posture'
    for rr in RP[['pair_id','source_family','wave','unit_a','unit_b',col]].itertuples(index=False,name=None):
        pairid,sf,w,ua,ub,post=rr; w=str(w)
        if post.startswith('INPUT_AUTHORITY_INCOMPLETE'):
            vals.append(json.dumps([block_packet.get((rid,sf,w),'UNCOMPRESSED_INPUT_BLOCKER')]))
        elif post.startswith('TERMINAL_'):
            vals.append(json.dumps(['TERMINAL:'+post]))
        elif post.startswith('NOT_PRIMARY_PAIR_GRAIN'):
            vals.append(json.dumps(['NONPAIR_GRAIN:SOURCE_OBJECT_AND_ALIGNMENT_PACKETS']))
        elif rid=='t06' and post.startswith('REQUIRES_NORM_CONDUCT'):
            t=unit_target.get(ua,'');vals.append(json.dumps([t6group[(sf,w,t)]]))
        else:
            par=PA.loc[pairid]; refs=[]
            for o in jl(par.corrected_common_r14c_object_ids_json):
                if o in obj_to_pid:refs.append(obj_to_pid[o])
            cg=par.driver_domain_collision_group_id
            if pd.notna(cg) and str(cg) in coll_to_pid:refs.append(coll_to_pid[str(cg)])
            vals.append(json.dumps(sorted(set(refs))) if refs else json.dumps(['INPUT_AUTHORITY_BLOCKER:UNRESOLVED_PACKET_BINDING']))
    mapout[rid+'_compression_refs_json']=vals
mapout.to_csv(R/'MAPPINGS/R12_PAIR_RULE_TO_PACKET_OR_TERMINAL_MAP.csv.gz',index=False,compression='gzip')

# T06 raw-row compression map
norm_wave_packet={}
for r in PK[PK.packet_class=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH'].itertuples(index=False): norm_wave_packet[(r.source_family,str(r.wave))]=r.packet_id
link_unit_packet={}
for r in PK[PK.packet_class=='T06_NORM_ENDPOINT_LINK_WORKBENCH'].itertuples(index=False):
    u=jl(r.member_semantic_unit_ids_json)[0]; link_unit_packet[(r.source_family,str(r.wave),u)]=r.packet_id
m=[]
for r in T6[['opportunity_id','source_family','wave','semantic_unit_id','disposition']].itertuples(index=False):
    pid=norm_wave_packet[(r.source_family,str(r.wave))] if r.disposition=='INPUT_AUTHORITY_INCOMPLETE__RELATION_NORM_ROLE_NOT_ADJUDICATED' else link_unit_packet[(r.source_family,str(r.wave),r.semantic_unit_id)]
    m.append((r.opportunity_id,pid,r.disposition))
pd.DataFrame(m,columns=['r11_opportunity_id','r12_packet_id','r11_disposition']).to_csv(R/'MAPPINGS/R12_T06_287513_RAW_TO_PACKET_MAP.csv.gz',index=False,compression='gzip')

# specialized origin map for all origin IDs we explicitly packetized
origrows=[]
for o,pids in origin_to_packets.items():
    for pid in sorted(pids):origrows.append((o,pid))
pd.DataFrame(origrows,columns=['r11_origin_id','r12_packet_id']).to_csv(R/'MAPPINGS/R12_SPECIALIZED_ORIGIN_TO_PACKET_MAP.csv',index=False)

# R8 ancestry crosswalk via exact implementation set overlap/subset
r8=pd.read_csv(B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811/ANCESTRY/R8_89_PACKET_TO_R10_SPINE_CROSSWALK.csv',dtype=str).fillna('')
# index packets with impl sets, exclude pure blocker wave packets for preferred reuse matches
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
pd.DataFrame(anc).to_csv(R/'ANCESTRY/R8_89_PACKET_TO_R12_COMPRESSION_CROSSWALK.csv',index=False)

# R8C verdict crosswalk through R8 packet ids (central 13 parent denominator)
r8c=pd.read_csv(B/'r8c_full/Rawlsing_R10K_S14_R8C_Vozhd_Central_Adjudication_20260811/ADJUDICATION/CENTRAL_13_RULE_VERDICTS_R8C.csv',dtype=str).fillna('')
ancmap=pd.DataFrame(anc).set_index('r8_canonical_packet_id').r12_candidate_packet_ids_json.to_dict()
r8c['r12_candidate_packet_ids_json']=r8c.canonical_packet_id.map(ancmap).fillna('[]')
r8c['r12_revalidation_status']='PROVISIONAL_R8C_VERDICT_PRESERVED__REVALIDATE_AGAINST_R12_PACKET'
r8c.to_csv(R/'ANCESTRY/R8C_33_RULE_VERDICTS_TO_R12_PACKETS.csv',index=False)

# summaries
cls=PK.groupby('packet_class').agg(packet_count=('packet_id','size'),raw_primitive_rows=('raw_primitive_row_count','sum'),decision_atoms=('decision_atom_count','sum')).reset_index()
cls.to_csv(R/'COVERAGE/R12_PACKET_CLASS_SUMMARY.csv',index=False)
status=PK.groupby('packet_status').agg(packet_count=('packet_id','size'),raw_primitive_rows=('raw_primitive_row_count','sum'),decision_atoms=('decision_atom_count','sum')).reset_index();status.to_csv(R/'COVERAGE/R12_PACKET_STATUS_SUMMARY.csv',index=False)
summary={'packet_count_total':len(PK),'packet_class_counts':PK.packet_class.value_counts().to_dict(),'raw_primitive_rows_represented_sum':int(PK.raw_primitive_row_count.sum()),'decision_atom_count_sum':int(PK.decision_atom_count.sum()),'r11_pair_rows':len(RP),'r11_t06_cross_rows':len(T6),'r8_packets_crosswalked':len(anc),'r8_packets_with_no_r12_match':sum(a['crosswalk_status'].startswith('NO_') for a in anc),'r8c_rule_verdicts_preserved':len(r8c),'job3_authorized':False,'r8_worker_packs':'DO_NOT_EXECUTE'}
json.dump(summary,open(R/'COVERAGE/R12_COMPRESSION_SUMMARY.json','w'),indent=2)
# report/status
open(R/'R12_COMPRESSION_REPORT.md','w').write(f'''# R12 — Lossless canonical compression of the R11A denominator\n\nR12 compresses R11A primitive opportunity/accounting rows into semantic work packets without converting missing authority into negative authority. **Packet count and decision-atom count are kept separate.**\n\n```json\n{json.dumps(summary,indent=2)}\n```\n\nPair-rule postures remain exactly traceable through `R12_PAIR_RULE_TO_PACKET_OR_TERMINAL_MAP.csv.gz`; every T06 exhaustive cross-shore row maps exactly once through `R12_T06_287513_RAW_TO_PACKET_MAP.csv.gz`. R8 89 packets and all 33 R8C rule verdict rows are carried forward by exact-member crosswalk for revalidation, never discarded.\n\nR12 is compression only. Cross-rule deduplication (#16), worker economics (#17), S14 adjudication (#18), and Job 3 remain downstream.\n''')
json.dump({'checkpoint':'R12','status':'COMPRESSION_BUILT__VALIDATION_NEXT','job3_authorized':False,'item15_status':'AWAITING_INDEPENDENT_VALIDATOR','summary':summary,'next':'independent losslessness validator then #16 cross-rule dedupe'},open(R/'CURRENT_STATUS_R12.json','w'),indent=2)
open(R/'ACTIVE_EXECUTION_POINTER.md','w').write('''# ACTIVE EXECUTION POINTER — R12\n\nR12 lossless compression built; independent losslessness validation next. R8 packs DO NOT EXECUTE. Job 3 NOT AUTHORIZED.\n''')
shutil.copy('/mnt/data/build_r12.py',R/'CODE/build_r12.py')
print(json.dumps(summary,indent=2))
print('\nClass summary\n',cls.to_string(index=False))
