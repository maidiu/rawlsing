import pandas as pd, json, hashlib, pathlib, csv, os, shutil
from collections import Counter
SRC=pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811')
OUT=pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811')
if OUT.exists(): shutil.rmtree(OUT)
(OUT/'PACKETS').mkdir(parents=True)
(OUT/'MAPPINGS').mkdir()
(OUT/'COVERAGE').mkdir()
(OUT/'VALIDATION').mkdir()
(OUT/'PROVENANCE').mkdir()
(OUT/'CODE').mkdir()

df=pd.read_csv(SRC/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv',dtype=str).fillna('')

def arr(s):
    if not s: return []
    try: return list(json.loads(s))
    except: return [s]
def canon(s): return json.dumps(sorted(set(map(str,arr(s)))),separators=(',',':'))
def rules(s): return [x for x in str(s).split(';') if x]

# Canonicalize identity-bearing fields.
for c in ['member_semantic_unit_ids_json','member_implementation_ids_json','source_object_ids_json','target_ids_json']:
    df[c+'_canon']=df[c].map(canon)

# Dedupe doctrine: preserve classes that encode a distinct governed concept identity; merge only identical evidence containers.
def dedupe_family(row):
    pc=row.packet_class
    if pc=='T07_P2_TARGET_RELATION_CONCEPT':
        # P2 concept identity is the governed structure; empty implementation fields cannot collapse 79 distinct concepts.
        return 'T07_CONCEPT::'+canon(row.raw_origin_ids_json)
    if pc=='SOURCE_NATIVE_OBJECT':
        return 'SOURCE_OBJECT::'+row.source_object_ids_json_canon
    if pc=='T09_T10_PARALLEL_SOURCE_OBJECT_COMPONENT':
        return 'PARALLEL_OBJECT::'+row.source_object_ids_json_canon+'::'+canon(row.raw_origin_ids_json)
    if pc=='T06_NORM_ENDPOINT_LINK_WORKBENCH':
        return 'T06_ENDPOINT_LINK'
    if pc=='T06_NORM_ROLE_ASSIGNMENT_BLOCKER_WORKBENCH':
        return 'T06_NORM_ROLE_BLOCKER'
    # These classes are alternative retrieval/views of the same exact member/target evidence object and may cross-rule merge.
    if pc in {'SEMANTIC_COLLISION_GROUP','T06_SAME_TARGET_SEMANTIC_HYPEREDGE','T08_INSTITUTION_CLASS_GROUP','T11_SAME_TARGET_MULTIROLE_GROUP'}:
        return 'MEMBER_TARGET_EVIDENCE'
    if pc=='PAIR_RULE_INPUT_AUTHORITY_BLOCKER':
        return 'PAIR_AUTHORITY_BLOCKER'
    return pc

df['dedupe_family']=df.apply(dedupe_family,axis=1)
df['dedupe_key']=df.apply(lambda r: '||'.join([
    r['dedupe_family'], r['source_family'], r['wave'], r['member_semantic_unit_ids_json_canon'],
    r['member_implementation_ids_json_canon'], r['source_object_ids_json_canon'], r['target_ids_json_canon']]),axis=1)

rows=[]; mapping=[]
for key,g in df.groupby('dedupe_key',sort=True):
    child_ids=sorted(g.packet_id.tolist())
    classes=sorted(set(g.packet_class))
    rs=sorted(set(x for s in g.rule_hypotheses for x in rules(s)))
    sem=sorted(set(x for s in g.member_semantic_unit_ids_json for x in arr(s)))
    impl=sorted(set(x for s in g.member_implementation_ids_json for x in arr(s)))
    sobj=sorted(set(x for s in g.source_object_ids_json for x in arr(s)))
    targ=sorted(set(x for s in g.target_ids_json for x in arr(s)))
    origins=sorted(set(x for s in g.raw_origin_ids_json for x in arr(s)))
    h=hashlib.sha256(key.encode()).hexdigest()[:16]
    pid='R13DED-'+h
    statuses=sorted(set(g.packet_status)); ceilings=sorted(set(g.authority_ceiling))
    row={
      'packet_id':pid,
      'source_family':g.source_family.iloc[0], 'wave':g.wave.iloc[0],
      'dedupe_family':g.dedupe_family.iloc[0],
      'child_packet_classes_json':json.dumps(classes),
      'rule_hypotheses':';'.join(rs),
      'member_semantic_unit_ids_json':json.dumps(sem),
      'member_implementation_ids_json':json.dumps(impl),
      'source_object_ids_json':json.dumps(sobj),
      'target_ids_json':json.dumps(targ),
      'r12_child_packet_count':str(len(g)),
      'r12_child_packet_ids_json':json.dumps(child_ids),
      'raw_origin_ids_json':json.dumps(origins),
      'raw_origin_count_sum':str(pd.to_numeric(g.raw_origin_count).sum()),
      'raw_primitive_row_count_sum':str(pd.to_numeric(g.raw_primitive_row_count).sum()),
      'decision_atom_count':str(pd.to_numeric(g.decision_atom_count).sum()),
      'packet_statuses_json':json.dumps(statuses),
      'authority_ceilings_json':json.dumps(ceilings),
      'dedupe_disposition':'MERGED_EXACT_EVIDENCE_CONTAINER' if len(g)>1 else 'PRESERVED_SINGLETON',
      'notes':'Cross-rule container dedupe only; rule-specific decision atoms and all R12 child packet ancestry preserved.'
    }
    rows.append(row)
    for _,r in g.iterrows():
        mapping.append({'r12_packet_id':r.packet_id,'r13_packet_id':pid,'r12_packet_class':r.packet_class,'r12_rule_hypotheses':r.rule_hypotheses,'dedupe_disposition':row['dedupe_disposition']})

out=pd.DataFrame(rows).sort_values('packet_id')
mapdf=pd.DataFrame(mapping).sort_values('r12_packet_id')
out.to_csv(OUT/'PACKETS/R13_CROSS_RULE_DEDUPED_PACKET_LEDGER.csv',index=False)
mapdf.to_csv(OUT/'MAPPINGS/R12_TO_R13_PACKET_CROSSWALK.csv',index=False)

summary={
 'r12_packet_count':len(df),'r13_packet_count':len(out),'container_reduction':len(df)-len(out),
 'r12_decision_atom_sum':int(pd.to_numeric(df.decision_atom_count).sum()),
 'r13_decision_atom_sum':int(pd.to_numeric(out.decision_atom_count).sum()),
 'r12_raw_primitive_row_sum':int(pd.to_numeric(df.raw_primitive_row_count).sum()),
 'r13_raw_primitive_row_sum':int(pd.to_numeric(out.raw_primitive_row_count_sum).sum()),
 'merged_r13_packets':int((out.dedupe_disposition=='MERGED_EXACT_EVIDENCE_CONTAINER').sum()),
 'r12_child_rows_in_merged_packets':int(pd.to_numeric(out.loc[out.dedupe_disposition=='MERGED_EXACT_EVIDENCE_CONTAINER','r12_child_packet_count']).sum()),
 'max_child_packets_per_r13':int(pd.to_numeric(out.r12_child_packet_count).max()),
 'dedupe_family_counts':out.dedupe_family.value_counts().to_dict(),
 'job3_authorized':False,'r8_worker_packs':'DO_NOT_EXECUTE'
}
json.dump(summary,open(OUT/'COVERAGE/R13_DEDUPE_SUMMARY.json','w'),indent=2)

report=f'''# R13 — Cross-rule exact-evidence container dedupe\n\n## Verdict\n\n**Repair item #16: DONE at cross-rule container-dedupe scope.** R13 merges only R12 packets that are the same exact governed evidence container under a class-aware identity law. It never merges rule-specific semantic decisions.\n\n- R12 packets: **{summary['r12_packet_count']:,}**\n- R13 deduped containers: **{summary['r13_packet_count']:,}**\n- Container reduction: **{summary['container_reduction']:,}**\n- Rule-specific decision atoms: **{summary['r13_decision_atom_sum']:,} preserved exactly**\n- Raw primitive-row accounting sum: **{summary['r13_raw_primitive_row_sum']:,} preserved exactly**\n- R13 containers that merge >1 R12 packet: **{summary['merged_r13_packets']:,}**\n\n## Identity law\n\nThe default cross-rule identity requires exact source family, active wave, semantic-unit member set, implementation member set, source-object set, target set, plus a class-aware governed-structure family. T07 P2 target-relation concepts remain distinct by exact P2 origin identity even when implementation bindings are empty. Source-native objects remain distinct by exact source-object identity. T09/T10 parallel-object components preserve their exact parallel-object origin identity.\n\nSemantic-collision, same-target T06, T08 institution-class, and T11 same-target-multirole views may merge when their exact member/target evidence identity is identical; all contributing channels and rules remain child annotations. Pair-rule input-authority blockers may merge across rules when they describe the same exact blocked evidence container, while each rule-specific decision atom remains counted.\n\n## Governance\n\nR13 is workload/container dedupe, not S14 relation adjudication. No ACCEPT/REJECT relation truth is created. R8 ancestry and R8C provisional verdicts remain governed through R12 ancestry. Job 3 remains blocked.\n\n## Next\n\nExecute **#17 worker economics** from the exact R13 deduped container ledger and its {summary['r13_decision_atom_sum']:,} decision atoms. Measure independent semantic work versus tightly coupled central work before producing any successor worker packs.\n'''
open(OUT/'R13_DEDUPE_REPORT.md','w').write(report)
status={'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811','status':'R13_CROSS_RULE_DEDUPE_FROZEN__ITEM16_DONE','job3_authorized':False,'item16_status':'DONE__EXACT_EVIDENCE_CONTAINER_DEDUPE','item17_status':'NEXT__WORKER_ECONOMICS','summary':summary}
json.dump(status,open(OUT/'CURRENT_STATUS_R13.json','w'),indent=2)
stack=json.load(open(SRC/'REPAIR_STACK_R12.json'))
if 16 in stack.get('partial',[]): stack['partial'].remove(16)
if 16 not in stack['done']: stack['done'].append(16); stack['done']=sorted(stack['done'])
stack['notes']['16']=f"DONE: {len(df):,} R12 containers -> {len(out):,} exact-evidence deduped containers; {summary['r13_decision_atom_sum']:,} rule-specific decision atoms preserved."
stack['notes']['17']='ACTIVE NEXT: measure worker economics from R13 deduped containers/decision atoms.'
json.dump(stack,open(OUT/'REPAIR_STACK_R13.json','w'),indent=2)
pointer=f'''# ACTIVE EXECUTION POINTER — R13\n\nCanonical active checkpoint: `/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R13_20260811/`\n\nState: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / #17 WORKER ECONOMICS`.\n\n- #2 unified 18,276 spine: DONE.\n- #3 orthogonal relation-role ontology/schema: DONE.\n- #14 denominator-complete accounting: DONE.\n- #15 lossless packet compression: DONE.\n- #16 cross-rule exact-evidence container dedupe: **DONE; {len(df):,} -> {len(out):,} containers; {summary['r13_decision_atom_sum']:,} rule-specific decision atoms preserved.**\n- R8 W01-W04 packs: DO NOT EXECUTE.\n- Job 3: NOT AUTHORIZED.\n\nNext: #17 worker economics. Classify R13 containers by semantic independence/coupling and compare sharding overhead against central adjudication; only then decide whether successor workers are economical.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER.md','w').write(pointer)
open(OUT/'00_README_FIRST.md','w').write('# README FIRST — R13\n\nR13 closes repair item #16 by exact-evidence cross-rule container dedupe over R12. Read `R13_DEDUPE_REPORT.md`, `CURRENT_STATUS_R13.json`, and `ACTIVE_EXECUTION_POINTER.md`. Job 3 remains unauthorized.\n')
# parent pins
pins={'parent_r12_zip_sha256':hashlib.sha256(pathlib.Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R12_20260811.zip').read_bytes()).hexdigest(),'parent_r12_packet_ledger_sha256':hashlib.sha256((SRC/'PACKETS/R12_CANONICAL_COMPRESSED_PACKET_LEDGER.csv').read_bytes()).hexdigest()}
json.dump(pins,open(OUT/'PROVENANCE/PARENT_PINS_R13.json','w'),indent=2)
shutil.copy('/mnt/data/build_r13_dedupe.py',OUT/'CODE/build_r13_dedupe.py')
print(json.dumps(summary,indent=2))
