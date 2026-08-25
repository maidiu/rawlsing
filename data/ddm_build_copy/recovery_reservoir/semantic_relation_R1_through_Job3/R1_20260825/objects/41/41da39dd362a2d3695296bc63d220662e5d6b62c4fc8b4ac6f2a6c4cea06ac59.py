import pandas as pd,json,hashlib,pathlib,sys
ROOT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811')
R12=pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811')
checks=[]; errors=[]
def ck(name,cond,detail=None):
    checks.append({'check':name,'pass':bool(cond),'detail':detail})
    if not cond: errors.append({'check':name,'detail':detail})
def arr(s):
    if not s:return []
    try:return list(json.loads(s))
    except:return [s]
def canon(s):return json.dumps(sorted(set(map(str,arr(s)))),separators=(',',':'))
def rulelist(s):return sorted(set(x for x in str(s).split(';') if x))

r12=pd.read_csv(R12/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype=str).fillna('')
r13=pd.read_csv(ROOT/'PACKETS/R13_CROSS_RULE_DEDUPED_PACKET_LEDGER.csv',dtype=str).fillna('')
mp=pd.read_csv(ROOT/'MAPPINGS/R12_TO_R13_PACKET_CROSSWALK.csv',dtype=str).fillna('')
status=json.load(open(ROOT/'CURRENT_STATUS_R13.json'))
stack=json.load(open(ROOT/'REPAIR_STACK_R13.json'))
pins=json.load(open(ROOT/'PROVENANCE/PARENT_PINS_R13.json'))

# Parent integrity
r12zip=pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811.zip')
ck('parent_r12_zip_hash',hashlib.sha256(r12zip.read_bytes()).hexdigest()==pins['parent_r12_zip_sha256'])
ck('parent_r12_ledger_hash',hashlib.sha256((R12/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv').read_bytes()).hexdigest()==pins['parent_r12_packet_ledger_sha256'])
# Mapping and conservation
ck('r12_rows_2846',len(r12)==2846,len(r12))
ck('crosswalk_rows_2846',len(mp)==2846,len(mp))
ck('crosswalk_r12_unique',mp.r12_packet_id.nunique()==2846,mp.r12_packet_id.nunique())
ck('crosswalk_exact_r12_ids',set(mp.r12_packet_id)==set(r12.packet_id))
ck('r13_ids_unique',r13.packet_id.nunique()==len(r13),(r13.packet_id.nunique(),len(r13)))
ck('r13_count_2599',len(r13)==2599,len(r13))
ck('container_reduction_247',len(r12)-len(r13)==247,len(r12)-len(r13))
ck('decision_atoms_preserved',pd.to_numeric(r12.decision_atom_count).sum()==pd.to_numeric(r13.decision_atom_count).sum(),(int(pd.to_numeric(r12.decision_atom_count).sum()),int(pd.to_numeric(r13.decision_atom_count).sum())))
ck('decision_atoms_120970',int(pd.to_numeric(r13.decision_atom_count).sum())==120970,int(pd.to_numeric(r13.decision_atom_count).sum()))
ck('primitive_sum_preserved',pd.to_numeric(r12.raw_primitive_row_count).sum()==pd.to_numeric(r13.raw_primitive_row_count_sum).sum())
# Child membership reconstructs crosswalk exactly
map_groups=mp.groupby('r13_packet_id').r12_packet_id.apply(lambda x:sorted(x)).to_dict()
bad=[]
for _,r in r13.iterrows():
    declared=sorted(arr(r.r12_child_packet_ids_json)); actual=map_groups.get(r.packet_id,[])
    if declared!=actual: bad.append(r.packet_id)
ck('child_packet_membership_exact',not bad,bad[:10])
# Rule union and accounting exact
r12idx=r12.set_index('packet_id')
bad_rules=[];bad_atoms=[];bad_prim=[]
for _,r in r13.iterrows():
    ids=arr(r.r12_child_packet_ids_json); kids=r12idx.loc[ids]
    if isinstance(kids,pd.Series): kids=kids.to_frame().T
    ur=sorted(set(x for s in kids.rule_hypotheses for x in rulelist(s)))
    if ur!=rulelist(r.rule_hypotheses): bad_rules.append(r.packet_id)
    if int(pd.to_numeric(kids.decision_atom_count).sum())!=int(r.decision_atom_count): bad_atoms.append(r.packet_id)
    if int(pd.to_numeric(kids.raw_primitive_row_count).sum())!=int(r.raw_primitive_row_count_sum): bad_prim.append(r.packet_id)
ck('rule_union_exact',not bad_rules,bad_rules[:10])
ck('per_container_atom_sum_exact',not bad_atoms,bad_atoms[:10])
ck('per_container_primitive_sum_exact',not bad_prim,bad_prim[:10])
# Class-aware identity reconstruction
for c in ['member_semantic_unit_ids_json','member_implementation_ids_json','source_object_ids_json','target_ids_json']:
    r12[c+'_canon']=r12[c].map(canon)
def fam(row):
    pc=row.packet_class
    if pc=='T07_P2_TARGET_RELATION_CONCEPT': return 'T07_CONCEPT::'+canon(row.raw_origin_ids_json)
    if pc=='SOURCE_NATIVE_OBJECT': return 'SOURCE_OBJECT::'+row.source_object_ids_json_canon
    if pc=='T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT': return 'PARALLEL_OBJECT::'+row.source_object_ids_json_canon+'::'+canon(row.raw_origin_ids_json)
    if pc=='T06_NORM_ENDPOINT_LINK_WORKBENCH': return 'T06_ENDPOINT_LINK'
    if pc=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH': return 'T06_NORM_ROLE_BLOCKER'
    if pc in {'SEMANTIC_COLLISION_GROUP','T06_SAME_TARGET_SEMANTIC_HYPEREDGE','T08_INSTITUTION_CLASS_GROUP','T11_SAME_TARGET_MULTIROLE_GROUP'}: return 'MEMBER_TARGET_EVIDENCE'
    if pc=='PAIR_RULE_INPUT_AUTHORITY_BLOCKER': return 'PAIR_AUTHORITY_BLOCKER'
    return pc
r12['fam']=r12.apply(fam,axis=1)
r12['key']=r12.apply(lambda r:'||'.join([r['fam'],r.source_family,r.wave,r.member_semantic_unit_ids_json_canon,r.member_implementation_ids_json_canon,r.source_object_ids_json_canon,r.target_ids_json_canon]),axis=1)
expected_groups={k:sorted(g.packet_id) for k,g in r12.groupby('key')}
actual_groups=sorted(sorted(arr(x)) for x in r13.r12_child_packet_ids_json)
expected_list=sorted(expected_groups.values())
ck('independent_group_partition_exact',actual_groups==expected_list,(len(actual_groups),len(expected_list)))
# No cross-source/wave merge
cross=[]
for _,r in r13[r13.r12_child_packet_count.astype(int)>1].iterrows():
    kids=r12idx.loc[arr(r.r12_child_packet_ids_json)]
    if len(set(kids.source_family))!=1 or len(set(kids.wave))!=1: cross.append(r.packet_id)
ck('no_cross_source_wave_merge',not cross,cross)
# Critical identity controls
ck('t07_concepts_preserved_79',sum(r13.dedupe_family.str.startswith('T07_CONCEPT::'))==79,sum(r13.dedupe_family.str.startswith('T07_CONCEPT::')))
ck('source_objects_preserved_598',sum(r13.dedupe_family.str.startswith('SOURCE_OBJECT::'))==598,sum(r13.dedupe_family.str.startswith('SOURCE_OBJECT::')))
ck('parallel_components_preserved_117',sum(r13.dedupe_family.str.startswith('PARALLEL_OBJECT::'))==117,sum(r13.dedupe_family.str.startswith('PARALLEL_OBJECT::')))
ck('t06_endpoint_link_containers_1063',sum(r13.dedupe_family=='T06_ENDPOINT_LINK')==1063,sum(r13.dedupe_family=='T06_ENDPOINT_LINK'))
ck('t06_norm_role_blockers_32',sum(r13.dedupe_family=='T06_NORM_ROLE_BLOCKER')==32,sum(r13.dedupe_family=='T06_NORM_ROLE_BLOCKER'))
ck('pair_blocker_containers_55',sum(r13.dedupe_family=='PAIR_AUTHORITY_BLOCKER')==55,sum(r13.dedupe_family=='PAIR_AUTHORITY_BLOCKER'))
ck('member_target_containers_655',sum(r13.dedupe_family=='MEMBER_TARGET_EVIDENCE')==655,sum(r13.dedupe_family=='MEMBER_TARGET_EVIDENCE'))
# Merge-shape sanity
merged=r13[r13.r12_child_packet_count.astype(int)>1]
ck('merged_containers_91',len(merged)==91,len(merged))
ck('merged_child_rows_338',merged.r12_child_packet_count.astype(int).sum()==338,int(merged.r12_child_packet_count.astype(int).sum()))
ck('max_merge_size_7',merged.r12_child_packet_count.astype(int).max()==7,int(merged.r12_child_packet_count.astype(int).max()))
allowed={
 ('PAIR_RULE_INPUT_AUTHORITY_BLOCKER',),
 ('T06_SAME_TARGET_SEMANTIC_HYPEREDGE','T11_SAME_TARGET_MULTIROLE_GROUP'),
 ('SEMANTIC_COLLISION_GROUP','T08_INSTITUTION_CLASS_GROUP'),
 ('SEMANTIC_COLLISION_GROUP','T06_SAME_TARGET_SEMANTIC_HYPEREDGE'),
 ('SEMANTIC_COLLISION_GROUP','T06_SAME_TARGET_SEMANTIC_HYPEREDGE','T11_SAME_TARGET_MULTIROLE_GROUP')}
badcombo=[]
for _,r in merged.iterrows():
    combo=tuple(json.loads(r.child_packet_classes_json))
    if combo not in allowed: badcombo.append((r.packet_id,combo))
ck('merged_class_combos_allowlisted',not badcombo,badcombo[:10])
# Governance
ck('item16_done',status.get('item16_status','').startswith('DONE'))
ck('item17_next',status.get('item17_status','').startswith('NEXT'))
ck('job3_false',status.get('job3_authorized') is False)
ck('stack_16_done',16 in stack.get('done',[]))
pointer=(ROOT/'ACTIVE_EXECUTION_POINTER.md').read_text()
ck('pointer_r13', 'R13' in pointer and '#17 WORKER ECONOMICS' in pointer)
ck('pointer_job3_blocked','Job 3: NOT AUTHORIZED' in pointer)
ck('pointer_old_workers_poisoned','DO NOT EXECUTE' in pointer)
res={'status':'PASS' if not errors else 'FAIL','check_count':len(checks),'errors':errors,'checks':checks}
json.dump(res,open(ROOT/'VALIDATION/VALIDATION_RESULT_R13.json','w'),indent=2)
print(json.dumps(res,indent=2))
sys.exit(0 if not errors else 1)
