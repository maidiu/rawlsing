#!/usr/bin/env python3
from pathlib import Path
import sys,csv,json,re,hashlib,collections
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
root=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
sec=root/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING'
checks=[]
def ck(n,c,d=''): checks.append((n,bool(c),d)); print(('PASS ' if c else 'FAIL ')+n+((' '+str(d)) if d else ''))
def rows(p):
 with p.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Core counts
ret=json.loads((sec/'upstream/P3_EFFECTIVE_INPUT_AND_COVERAGE_RETURN_v3.json').read_text())
ck('effective_19175',ret['effective_unique_direct_pair_authorities']==19175,ret)
ck('proposition_658',ret['proposition_relation_pairs']==658,ret)
ck('admin_preflight_1',ret['administrative_metadata_proposition_pairs_preflight']==1,ret)
ck('substantive_preflight_657',ret['provisional_substantive_j_family_candidate_edges']==657,ret)
ck('lineage_partition',ret['lineage_participation_counts']=={'CONSTRAINT_ONLY_INCIDENT':2897,'NO_CURRENT_DIRECT_PAIR_AUTHORITY':10230,'PROPOSITION_GRAPH_INCIDENT':399},ret['lineage_participation_counts'])
part=rows(sec/'upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v3.csv');ck('lineage_rows_13526',len(part)==13526,len(part));ck('lineage_unique',len({r['lineage_id'] for r in part})==13526,'')
source=rows(sec/'upstream/P3_EFFECTIVE_PAIR_SOURCE_AUTHORITY_SURFACE_v3.csv');ck('source_authority_rows_19582',len(source)==19582,len(source))
by=collections.defaultdict(list)
for r in source:by[r['pair_key']].append(r)
ck('one_governing_each',len(by)==19175 and all(sum(x['authority_role']=='GOVERNING' for x in v)==1 for v in by.values()),'')
ck('407_superseded',sum(r['authority_role']=='SUPERSEDED_PROVENANCE' for r in source)==407,'')
# input manifest
for r in rows(sec/'upstream/P3_UPSTREAM_INPUT_MANIFEST_v3.csv'):
 p=root/r['relative_path'];ck('input_'+r['input_code'],p.exists() and sha(p)==r['sha256'] and (not r['actual_rows'] or int(r['actual_rows'])==int(r['expected_rows'])),r)
# vocab/bindings
v=rows(sec/'P3_CONTROLLED_VOCABULARIES_v3.csv');V=collections.defaultdict(set)
for r in v:V[r['vocabulary_domain']].add(r['code'])
ck('vocab_unique',len(v)==len({(r['vocabulary_domain'],r['code']) for r in v}),len(v))
ddl=(sec/'sql/p3_postgresql_compatible_ddl_v3.sql').read_text();blocks=dict(re.findall(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.S|re.I))
def parse_cols(b):
 depth=0;cur='';ps=[]
 for ch in b:
  if ch=='(':depth+=1
  elif ch==')':depth-=1
  if ch==',' and depth==0:ps.append(cur.strip());cur=''
  else:cur+=ch
 if cur.strip():ps.append(cur.strip())
 return {p.split()[0] for p in ps if p and not p.upper().startswith(('PRIMARY KEY','FOREIGN KEY','UNIQUE','CHECK','CONSTRAINT'))}
cols={t:parse_cols(b) for t,b in blocks.items()}
for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv'):
 ck('binding_'+r['table_name']+'_'+r['column_name'],r['table_name'] in cols and r['column_name'] in cols[r['table_name']] and r['vocabulary_domain'] in V,r)
ck('scope_type_binding',any(r['table_name']=='p3_collision_scope_registry' and r['column_name']=='scope_type' for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')),'')
ck('membership_pk_one_role','PRIMARY KEY(candidate_revision_id,member_object_id));' in ddl,'')
ck('candidate_ranking_table','CREATE TABLE p3_candidate_ranking' in ddl,'')
ck('lineage_participation_table','CREATE TABLE p3_lineage_participation' in ddl,'')
ck('ddl_rollback',ddl.strip().endswith('ROLLBACK;'),'')
# schemas
registry=Registry();schemas={};ids=[]
for p in sorted((sec/'schemas').glob('*.json')):
 s=json.loads(p.read_text());Draft202012Validator.check_schema(s);schemas[p.name]=s;ids.append(s['$id']);registry=registry.with_resource(s['$id'],Resource.from_contents(s))
ck('schema_ids_unique',len(ids)==len(set(ids)),len(ids));ck('schema_count_ge_34',len(schemas)>=34,len(schemas))
referr=[]
for n,s in schemas.items():
 try:list(Draft202012Validator(s,registry=registry,format_checker=FormatChecker()).iter_errors({}))
 except Exception as e:referr.append((n,str(e)))
ck('offline_refs',not referr,referr)
examples=[('adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json','candidate_packet.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v3.json','adjudication_decision_draft.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v3.json','adjudication_decision.schema.json')]
for f,sn in examples:
 errs=list(Draft202012Validator(schemas[sn],registry=registry,format_checker=FormatChecker()).iter_errors(json.loads((sec/f).read_text())));ck('example_'+Path(f).stem,not errs,[e.message for e in errs[:5]])
# Mutation tests
pf=json.loads((sec/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json').read_text())
# two governing authorities should fail
pair={'pair_fact_id':'P3PF-00000001','left_id':'a','right_id':'b','orientation':'SYMMETRIC','relation_type':'PROPOSITION_IDENTITY_ONLY','source_authorities':[{'registry':'SEMANTIC_PRIORITY_CLOSURE','authority_id':'x','authority_role':'GOVERNING','superseded_by_authority_id':None},{'registry':'EXACT_FOUNDATION_CLOSURE','authority_id':'y','authority_role':'GOVERNING','superseded_by_authority_id':None}],'target_relation':None,'operator_relation':None,'timeframe_relation':None,'response_relation':None,'source_portability_ceiling':'QUESTION_PROPOSITION_ONLY','p3_portability_ceiling':'QUESTION_PROPOSITION_ONLY','proposition_graph_allowed':True,'j_family_candidate_eligibility':'J_FAMILY_CANDIDATE_ELIGIBLE','creates_endpoint_authority':False,'evidence_ids':['l','r'],'authority_release_id':'r'}
ck('mutation_two_governing_fails',bool(list(Draft202012Validator(schemas['pair_fact_bundle.schema.json'],registry=registry).iter_errors(pair))),'')
# accepted decision with no canonical family fails
fd=json.loads((sec/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v3.json').read_text());fd['canonical_family_id']=None
ck('mutation_accepted_without_family_fails',bool(list(Draft202012Validator(schemas['adjudication_decision.schema.json'],registry=registry).iter_errors(fd))),'')
# generic object arrays prohibited in critical schemas
def generic(x):
 if isinstance(x,dict):
  if x.get('type')=='array' and x.get('items')=={'type':'object'}:return True
  return any(generic(v) for v in x.values())
 if isinstance(x,list):return any(generic(v) for v in x)
 return False
for n in ['candidate_packet.schema.json','adjudication_decision.schema.json','canonical_family_revision.schema.json']:
 ck('no_generic_'+n,not generic(schemas[n]),'')
# reference type contract
ref=rows(sec/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3.csv');ck('reference_contract_nonempty',len(ref)>=10,len(ref));ck('reference_columns_exist',all(r['table_name'] in cols and r['column_name'] in cols[r['table_name']] for r in ref),'')
# plan phrases
plan=(sec/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v3_20260731.md').read_text().lower()
for phrase in ['10,230','administrative interviewer-metadata','canonical serialization','p3a_contract_and_pilot_v3_implementation','named exclusions are mandatory whenever']:
 ck('plan_'+re.sub(r'\W+','_',phrase),phrase.lower() in plan,phrase)
# inherited payload hashes
inh=rows(sec/'validation/INHERITED_V22_PAYLOAD_HASHES.csv')
ck('inherited_payload_nontrivial',len(inh)>900,len(inh))
ck('inherited_payload_unchanged',all(r['present_in_v23']=='YES' and r['sha256']==r['v23_sha256'] and sha(root/r['relative_path'])==r['sha256'] for r in inh),'')
# DDL structural checks beyond column extraction
table_names=re.findall(r'CREATE TABLE\s+(\w+)\s*\(',ddl,re.I)
ck('ddl_table_names_unique',len(table_names)==len(set(table_names)),[x for x in set(table_names) if table_names.count(x)>1])
constraint_names=re.findall(r'ADD CONSTRAINT\s+(\w+)',ddl,re.I)
ck('ddl_constraint_names_unique',len(constraint_names)==len(set(constraint_names)),constraint_names)
positions={m.group(1):m.start() for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\(',ddl,re.I)}
forward=[];missing=[]
for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\((.*?)\);',ddl,re.I|re.S):
 t,b=m.group(1),m.group(2)
 for ref_t in re.findall(r'REFERENCES\s+(\w+)\s*\(',b,re.I):
  if ref_t not in positions: missing.append((t,ref_t))
  elif positions[ref_t]>m.start(): forward.append((t,ref_t))
ck('ddl_reference_tables_exist',not missing,missing)
ck('ddl_no_forward_inline_references',not forward,forward)
ck('ddl_one_deferred_closure_fk',ddl.count('p3_closure_resolution_adjudication_fk')==1,ddl.count('p3_closure_resolution_adjudication_fk'))
ck('ddl_one_deferred_family_fk',ddl.count('p3_adjudication_canonical_family_fk')==1,ddl.count('p3_adjudication_canonical_family_fk'))
ck('direct_unresolved_governed','DIRECT_UNRESOLVED' in V['pair_state'] and 'DIRECT_UNRESOLVED' in ddl,'')
# packet mutation: incomplete proposition signature must fail
bad=json.loads((sec/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v3.json').read_text())
del bad['proposition_signature_matrix'][0]['fields']['operator']
ck('mutation_missing_signature_field_fails',bool(list(Draft202012Validator(schemas['candidate_packet.schema.json'],registry=registry).iter_errors(bad))),'')
elig=rows(sec/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v3.csv')
ck('eligibility_preflight_658',len(elig)==658,len(elig))
ck('eligibility_admin_one',sum(r['provisional_j_family_eligibility']=='ADMINISTRATIVE_METADATA_ONLY' for r in elig)==1,'')
graph=json.loads((sec/'upstream/P3_PROPOSITION_GRAPH_PREFLIGHT_RETURN_v3.json').read_text())
ck('graph_preflight_counts',graph['all_proposition_edges']==658 and graph['provisional_substantive_edges']==657 and graph['all_proposition_graph']['node_count']==399 and graph['provisional_substantive_graph']['node_count']==397,graph)
ck('lineage_disposition_schema','lineage_disposition.schema.json' in schemas,'')
ck('lineage_disposition_table','CREATE TABLE p3_lineage_disposition' in ddl,'')
ck('lineage_disposition_binding',any(r['table_name']=='p3_lineage_disposition' and r['column_name']=='disposition_status' for r in rows(sec/'P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v3.csv')),'')
ck('plan_no_loss_lineage','zero `unadjudicated` lineages' in plan and '18,276 implementations' in plan,'')
# package cleanliness
ck('no_p3_execution',not any((sec/x).exists() for x in ['p3_candidate_families.csv','p3_canonical_families.csv']),'')
debris=[p for p in root.rglob('*') if p.is_file() and (p.suffix=='.pyc' or '__pycache__' in p.parts or '.pytest_cache' in p.parts)]
ck('no_debris',not debris,[str(x) for x in debris[:10]])
passed=sum(c for _,c,_ in checks)
print(json.dumps({'status':'PASS' if passed==len(checks) else 'FAIL','checks_passed':passed,'checks_total':len(checks),'failures':[n for n,c,d in checks if not c]},indent=2))
sys.exit(0 if passed==len(checks) else 1)
