#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys,csv,json,re,hashlib,zipfile,collections
from jsonschema import Draft202012Validator
from referencing import Registry,Resource

root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
sec=root/'44_P3_PLAN_ACCEPTANCE_AUDIT_AND_CORRECTION'
checks=[]
def ck(name,cond,detail=''):
    checks.append({'check':name,'status':'PASS' if cond else 'FAIL','detail':str(detail)})
    if not cond: print('FAIL',name,detail)
def rows(p):
    with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

# Required surface
required=[sec/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v2_20260731.md',sec/'P3_PLAN_LOCK_v2.json',sec/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE.csv',sec/'P3_CONTROLLED_VOCABULARIES_v2.csv',sec/'P3_RELATION_COMPOSITION_MATRIX_v2.csv',sec/'P3_LIFECYCLE_STATE_MACHINE_v2.csv',sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v2.csv',sec/'P3_JSON_SCHEMA_REGISTRY_v2.csv',sec/'sql/p3_postgresql_compatible_ddl_v2.sql',sec/'sql/P3_DDL_VALIDATION_QUERIES_v2.sql',sec/'sql/P3_SHADOW_MIGRATION_SKELETON_v2.sql']
ck('required_v22_files',all(p.exists() for p in required),[str(p.relative_to(root)) for p in required if not p.exists()])

# Upstream exact surface
sem=list(csv.DictReader((root/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE/Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv').open()))
ex=list(csv.DictReader((root/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE/Rawlsing_P2_Global_Exact_Foundation_Authority_Registry_v1.csv').open()))
lin=list(csv.DictReader((root/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv').open()))
def key(r):return '|'.join(sorted((r['left_lineage_id'],r['right_lineage_id'])))
semk={key(r) for r in sem}; exk={key(r) for r in ex}; exonly=[r for r in ex if key(r) not in semk]
propceil={'QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY','QUESTION_PROPOSITION_ONLY','QUESTION_AND_RESPONSE_CONTRACT'}
semprop=[r for r in sem if r['normalized_authority_class']=='PROPOSITION_RELATION_AUTHORITY']
exprop=[r for r in exonly if r['authority_status']=='ACCEPTED_CROSS_SOURCE_CONTINUITY' and r['portability_ceiling'] in propceil]
ck('semantic_priority_count',len(sem)==18831,len(sem));ck('exact_foundation_count',len(ex)==751,len(ex));ck('overlap_count',len(semk&exk)==407,len(semk&exk));ck('exact_only_count',len(exonly)==344,len(exonly));ck('effective_pair_count',len(sem)+len(exonly)==19175,len(sem)+len(exonly));ck('effective_connective_count',len(semprop)+len(exprop)==658,(len(semprop),len(exprop)))
eff=rows(sec/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE.csv');ck('effective_registry_rows',len(eff)==19175,len(eff));ck('effective_pair_keys_unique',len({r['pair_key'] for r in eff})==19175,'');
lineage={r['lineage_id'] for r in lin}; endpoints={r['left_lineage_id'] for r in eff}|{r['right_lineage_id'] for r in eff};ck('all_effective_endpoints_resolve',not(endpoints-lineage),len(endpoints-lineage))
ck('semantic_governs_all_overlaps',all(next(x for x in eff if x['pair_key']==k)['governing_registry']=='SEMANTIC_PRIORITY_CLOSURE' for k in semk&exk),'')
ret=json.loads((sec/'upstream/P3_EFFECTIVE_INPUT_SURFACE_RETURN.json').read_text());ck('input_return_matches',ret['effective_unique_direct_pair_authorities']==19175 and ret['effective_connective_proposition_pairs']==658,ret)
origin=json.loads((sec/'upstream/P3_UPSTREAM_ORIGIN_RESOLUTION_RETURN.json').read_text());ck('semantic_origin_resolution',origin['status']=='PASS' and origin['missing_origin_rulings']==0,origin)

# Inherited payload integrity
baseline=rows(sec/'validation/INHERITED_V21_PAYLOAD_HASHES.csv');bad=[]
for r in baseline:
 p=root/r['relative_path']
 if not p.exists() or p.stat().st_size!=int(r['bytes']) or sha(p)!=r['sha256']:bad.append(r['relative_path'])
ck('inherited_v21_payload_preserved',not bad,bad[:20])

# Vocab and categorical closure
v=rows(sec/'P3_CONTROLLED_VOCABULARIES_v2.csv');pairs=[(r['vocabulary_domain'],r['code']) for r in v];ck('vocab_unique',len(pairs)==len(set(pairs)),len(pairs)-len(set(pairs)))
V=collections.defaultdict(set)
for r in v:V[r['vocabulary_domain']].add(r['code'])
for domain in ['signature_field_name','signature_status','object_type','pair_relation_type','collision_type','candidate_classification','lifecycle_stage','response_topology','adjudication_decision_status','release_status','identity_strategy']:
 ck('vocab_domain_'+domain,domain in V and len(V[domain])>0,len(V.get(domain,set())))
ck('signature_fields_exact',V['signature_field_name']=={'subject_role','operator','target','object_or_outcome','modality','timeframe','condition','population_scope','geographic_scope','polarity','derived_status','parent_context'},V['signature_field_name'])
bind=rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v2.csv');ck('binding_domains_resolve',all(r['vocabulary_domain'] in V for r in bind),[r for r in bind if r['vocabulary_domain'] not in V])

# JSON schemas connected and examples valid
registry=Registry(); schemas={}; ids=[]
for p in sorted((sec/'schemas').glob('*.json')):
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s);ids.append(s.get('$id'));registry=registry.with_resource(s['$id'],Resource.from_contents(s));schemas[p.name]=s
ck('schema_count',len(schemas)==22,len(schemas));ck('schema_ids_unique_complete',None not in ids and len(ids)==len(set(ids)),ids)
ref_fail=[]
for name,s in schemas.items():
 try:list(Draft202012Validator(s,registry=registry).iter_errors({}))
 except Exception as e:ref_fail.append((name,str(e)))
ck('schema_refs_offline_resolve',not ref_fail,ref_fail)
examples=[('adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v2.json','candidate_packet.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v2.json','adjudication_decision_draft.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v2.json','adjudication_decision.schema.json')]
for obj,sch in examples:
 e=list(Draft202012Validator(schemas[sch],registry=registry).iter_errors(json.loads((sec/obj).read_text())));ck('valid_'+Path(obj).stem,not e,[x.message for x in e[:10]])
ps=schemas['proposition_signature.schema.json'];fields=ps['properties']['fields'];ck('signature_schema_fixed_twelve',set(fields['required'])==V['signature_field_name'] and fields.get('additionalProperties') is False,fields.get('required'))
cp=schemas['candidate_packet.schema.json'];generic=[]
for n in ['proposition_signature_matrix','response_contract_matrix','internal_pair_matrix','hard_collisions','unresolved_pairs','unruled_pairs','closure_obligations','proposed_variants','explicit_exclusions']:
 item=cp['properties'][n].get('items',{});
 if item=={'type':'object'}:generic.append(n)
ck('candidate_packet_arrays_typed',not generic,generic)
regrows=rows(sec/'P3_JSON_SCHEMA_REGISTRY_v2.csv');ck('schema_registry_exact',len(regrows)==len(schemas) and all((sec/'schemas'/r['schema_file']).exists() and sha(sec/'schemas'/r['schema_file'])==r['sha256'] for r in regrows),'')

# Composition and lifecycle
comp=rows(sec/'P3_RELATION_COMPOSITION_MATRIX_v2.csv');types=V['pair_relation_type'];ck('composition_8x8',len(comp)==64 and {(r['left_edge_type'],r['right_edge_type']) for r in comp}=={(a,b) for a in types for b in types},len(comp))
ck('composition_no_path_authority',all(r['creates_new_pair_authority'].strip().upper() in {'NO','FALSE','0'} for r in comp),[r for r in comp if r['creates_new_pair_authority'].strip().upper() not in {'NO','FALSE','0'}])
life=rows(sec/'P3_LIFECYCLE_STATE_MACHINE_v2.csv');adj=collections.defaultdict(set)
for r in life:
 if r['allowed']=='YES':adj[r['from_stage']].add(r['to_stage'])
seen={'DISCOVERED'};changed=True
while changed:
 changed=False
 for x in list(seen):
  for y in adj[x]:
   if y not in seen:seen.add(y);changed=True
ck('lifecycle_all_stages_reachable',V['lifecycle_stage']<=seen,(V['lifecycle_stage']-seen))
ck('classification_separate_from_lifecycle',V['candidate_classification'].isdisjoint(V['lifecycle_stage']),'')

# DDL static contract
ddl=(sec/'sql/p3_postgresql_compatible_ddl_v2.sql').read_text();tables=set(re.findall(r'CREATE TABLE\s+(\w+)',ddl,re.I))
needed={'p3_authority_release','p3_runtime_promotion_pointer','p3_object_registry','p3_proposition_signature','p3_pair_fact_bundle','p3_candidate_family','p3_candidate_revision','p3_adjudication_decision','p3_canonical_family','p3_canonical_family_revision','p3_canonical_family_membership','p3_release_object_snapshot','p3_release_change_ledger','p3_dependency_edge','p3_categorical_field_binding'}
ck('ddl_required_tables',needed<=tables,needed-tables);ck('ddl_rollback_only',ddl.strip().endswith('ROLLBACK;'),'');ck('ddl_no_single_promotion_history_index','p3_one_current_promoted_release' not in ddl,'');ck('ddl_current_release_uses_pointer','JOIN p3_runtime_promotion_pointer' in ddl,'');ck('ddl_no_path_authority','CHECK(NOTcreates_endpoint_authority)' in ddl.replace(' ',''),'')
# table columns and refs
blocks=dict(re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.S|re.I));columns={}
for t,b in blocks.items():
 depth=0;cur='';parts=[]
 for ch in b:
  if ch=='(':depth+=1
  elif ch==')':depth-=1
  if ch==',' and depth==0:parts.append(cur.strip());cur=''
  else:cur+=ch
 if cur.strip():parts.append(cur.strip())
 columns[t]={p.split()[0] for p in parts if p and not p.upper().startswith(('PRIMARY KEY','FOREIGN KEY','UNIQUE','CHECK','CONSTRAINT'))}
refbad=[]
for t,b in blocks.items():
 for rt,rc in re.findall(r'REFERENCES\s+(\w+)\s*\((\w+)\)',b,re.I):
  if rt not in columns or rc not in columns[rt]:refbad.append((t,rt,rc))
ck('ddl_foreign_key_targets_declared',not refbad,refbad)
dic=rows(sec/'P3_SCHEMA_DICTIONARY_v2.csv');dset={(r['table_or_artifact'],r['field']) for r in dic};actual={(t,c) for t,cs in columns.items() for c in cs};ck('schema_dictionary_exact_ddl_columns',dset==actual,{'missing':list(actual-dset)[:20],'extra':list(dset-actual)[:20]})
ck('ddl_validation_query_count',(sec/'sql/P3_DDL_VALIDATION_QUERIES_v2.sql').read_text().count(' AS q')>=12,'')
ck('shadow_migration_fail_closed',(sec/'sql/P3_SHADOW_MIGRATION_SKELETON_v2.sql').read_text().strip().endswith('ROLLBACK;'),'')

# Plan and downstream boundaries
plan=(sec/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v2_20260731.md').read_text();ck('plan_version_v2','**Plan version:** v2' in plan,'');ck('plan_effective_counts','19,175' in plan and '658' in plan and '17 exact-only' in plan,'');ck('plan_no_641_only_scope','all 641' not in plan.lower(),'');
for phrase in ['Family membership does not authorize value harmonization','paths create closure obligations','semantic-priority closure','transactional singleton promotion pointer','P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION']:
 ck('plan_phrase_'+re.sub(r'\W+','_',phrase.lower())[:35],phrase.lower() in plan.lower(),phrase)
compat=rows(sec/'P3_UPSTREAM_DOWNSTREAM_COMPATIBILITY_MATRIX_v2.csv');ck('compatibility_interfaces',{'P2_SEMANTIC_PRIORITY','P2_EXACT_FOUNDATION','P4_MEASUREMENT','P5_STRATA','P6_RUNTIME','P7_PERSONA_PRESSURE'}<={r['interface'] for r in compat},'')
ck('downstream_no_authority_leak',all(r['authority_mode'] in {'DOWNSTREAM_SEPARATE_RELEASE','DOWNSTREAM_COMPUTATION'} for r in compat if r['interface'] in {'P4_MEASUREMENT','P5_STRATA','P7_PERSONA_PRESSURE'}),compat)

# Root controls, when finalized
cs=root/'00_START_HERE/CURRENT_STATE.json'
if cs.exists():
 state=json.loads(cs.read_text());ck('root_handoff_version_v22',state.get('handoff_version')=='v22',state.get('handoff_version'));ck('root_next_pass_v2',state.get('next_pass')=='P3A_CONTRACT_AND_PILOT_V2_IMPLEMENTATION',state.get('next_pass'));ck('root_effective_counts',state.get('effective_direct_pair_authorities')==19175 and state.get('effective_connective_proposition_pairs')==658,state)

# No execution overclaim or debris
ck('p3_execution_not_started',not any((sec/x).exists() for x in ['p3_candidate_families.csv','p3_canonical_families.csv']),'')
debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and (p.name.endswith('.pyc') or '__pycache__' in p.parts or '.pytest_cache' in p.parts)]
ck('no_cache_bytecode_debris',not debris,debris[:20])

# Package index if present
idx=root/'PACKAGE_INDEX.csv'
if idx.exists():
 ir=rows(idx);excluded={'PACKAGE_INDEX.csv'};actualfiles=[p for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in excluded]
 imap={r['relative_path']:r for r in ir};bad=[]
 for p in actualfiles:
  rel=p.relative_to(root).as_posix();r=imap.get(rel)
  if not r or int(r['bytes'])!=p.stat().st_size or r['sha256']!=sha(p):bad.append(rel)
 extra=set(imap)-{p.relative_to(root).as_posix() for p in actualfiles}
 ck('package_index_exact',not bad and not extra,{'bad':bad[:20],'extra':list(extra)[:20]})

passed=sum(x['status']=='PASS' for x in checks);out={'status':'PASS' if passed==len(checks) else 'FAIL','checks_passed':passed,'checks_total':len(checks),'failures':[x for x in checks if x['status']=='FAIL'],'checks':checks}
print(json.dumps({'status':out['status'],'checks_passed':passed,'checks_total':len(checks),'failures':out['failures']},indent=2))
sys.exit(0 if out['status']=='PASS' else 1)
