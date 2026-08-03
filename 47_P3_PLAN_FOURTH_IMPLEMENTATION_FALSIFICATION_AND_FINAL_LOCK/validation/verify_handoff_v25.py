from __future__ import annotations
from pathlib import Path
import sys,json,csv,re,hashlib,zipfile,ast,subprocess,tempfile
from collections import Counter,defaultdict
import pandas as pd,yaml
from referencing import Registry,Resource
from jsonschema import Draft202012Validator
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
SEC=ROOT/'47_P3_PLAN_FOURTH_IMPLEMENTATION_FALSIFICATION_AND_FINAL_LOCK'
checks=[]
def ck(name,cond,detail=''):
 checks.append((name,bool(cond),detail));
 if not cond: print('FAIL',name,detail)
def loadj(p): return json.loads(Path(p).read_text())
def sh(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
# State and immutable upstream
st=loadj(ROOT/'00_START_HERE/CURRENT_STATE.json'); ck('state_v25',st.get('handoff_version')=='v25' and st.get('next_pass')=='P3A_CONTRACT_AND_PILOT_V5_IMPLEMENTATION')
lock=loadj(SEC/'P3_PLAN_LOCK_v5.json'); ck('plan_v5',lock['plan_version']=='v5' and lock['effective_input_surface']['effective_unique_direct_pair_authorities']==19175)
eff=pd.read_csv(SEC/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v5.csv',keep_default_na=False)
prop=pd.read_csv(SEC/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v5.csv',keep_default_na=False)
lin=pd.read_csv(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv',keep_default_na=False)
ck('effective_pairs_19175',len(eff)==19175 and eff.pair_key.nunique()==19175)
ck('proposition_658',len(prop)==658 and prop.pair_key.nunique()==658)
ck('lineages_13526',len(lin)==13526 and lin.lineage_id.nunique()==13526)
impl=[]
for x in lin.member_question_implementation_ids_json: impl+=json.loads(x)
ck('implementations_18276',len(impl)==18276 and len(set(impl))==18276 and int(lin.member_count.sum())==18276)
# Real graph topology
sub=prop[prop.provisional_j_family_eligibility=='J_FAMILY_CANDIDATE_ELIGIBLE'].copy()
E1=sub[sub.p3_relation_type=='PROPOSITION_RESPONSE_IDENTITY']; E2=sub[sub.p3_relation_type=='PROPOSITION_IDENTITY_ONLY']
def comps(df):
 adj=defaultdict(set)
 for r in df.itertuples(): adj[r.left_lineage_id].add(r.right_lineage_id);adj[r.right_lineage_id].add(r.left_lineage_id)
 seen=set();cs=[]
 for n in sorted(adj):
  if n in seen:continue
  stack=[n];seen.add(n);c=[]
  while stack:
   x=stack.pop();c.append(x)
   for y in sorted(adj[x]):
    if y not in seen:seen.add(y);stack.append(y)
  cs.append(set(c))
 return cs
c1=comps(E1); idx={n:i for i,c in enumerate(c1) for n in c}; cats=Counter(); outside=[]
for r in E2.itertuples():
 a=idx.get(r.left_lineage_id);b=idx.get(r.right_lineage_id)
 if a is not None and b is not None and a==b:cats['within_strict_component']+=1
 elif (a is None) ^ (b is None):cats['attaches_orphan_to_strict']+=1
 elif a is not None and b is not None and a!=b:cats['bridges_strict_components']+=1
 else:cats['both_endpoints_outside_strict']+=1;outside.append(r)
outdf=pd.DataFrame([x._asdict() for x in outside])
ck('strict_topology',len(E1)==445 and len({*E1.left_lineage_id,*E1.right_lineage_id})==304 and len(c1)==94)
ck('e2_topology',len(E2)==212 and cats==Counter({'within_strict_component':1,'attaches_orphan_to_strict':85,'bridges_strict_components':70,'both_endpoints_outside_strict':56}) and len(comps(outdf))==25,str(cats))
ck('full_graph_topology',len(comps(sub))==112 and len({*sub.left_lineage_id,*sub.right_lineage_id})==397)
# Schema connected registry, examples
schema_files=sorted((SEC/'schemas').glob('*.json')); resources=[]
for p in schema_files:
 o=loadj(p); Draft202012Validator.check_schema(o); resources.append((o['$id'],Resource.from_contents(o)))
reg=Registry().with_resources(resources)
for schema,example in [('candidate_packet.schema.json','adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v5.json'),('adjudication_decision_draft.schema.json','adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v5.json'),('adjudication_decision.schema.json','adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v5.json')]:
 Draft202012Validator(loadj(SEC/'schemas'/schema),registry=reg).validate(loadj(SEC/example))
ck('schemas_42_offline',len(schema_files)==42)
registry_rows=list(csv.DictReader((SEC/'P3_JSON_SCHEMA_REGISTRY_v5.csv').open()));ck('schema_registry_complete',len(registry_rows)==42 and all(r['all_dependencies_local']=='YES' for r in registry_rows) and {r['schema_file'].split('/')[-1] for r in registry_rows}=={p.name for p in schema_files})
# DDL hard surfaces
ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v5.sql').read_text()
required=['p3_imported_lineage_membership','p3_pair_endpoint_resolution','p3_component_connectivity_edge','p3_internal_pair_collision','p3_internal_pair_closure','p3_adjudication_split_member','p3_adjudication_unresolved_boundary','p3_validate_candidate_status_event','p3_validate_component_closure','p3_validate_internal_pair_closure','p3_validate_adjudication_completeness','p3_validate_genealogy_cardinality','p3_validate_segment_membership','p3_guard_object_registry_mutation','p3_candidate_revision_current_stage']
ck('ddl_required_surfaces',all(x in ddl for x in required))
ck('revision_lifecycle_derived','lifecycle_stage TEXT' not in ddl and 'WHERE e.candidate_revision_id=r.candidate_revision_id' in ddl)
ck('rollback_transition',((pd.read_csv(SEC/'P3_RELEASE_LIFECYCLE_STATE_MACHINE_v5.csv',keep_default_na=False).from_status=='SUPERSEDED') & (pd.read_csv(SEC/'P3_RELEASE_LIFECYCLE_STATE_MACHINE_v5.csv',keep_default_na=False).to_status=='PROMOTED')).any())
# schema dictionary exact tables/columns
sd=pd.read_csv(SEC/'P3_SCHEMA_DICTIONARY_v5.csv',keep_default_na=False); tables=set(re.findall(r'CREATE TABLE\s+(\w+)',ddl,re.I));ck('schema_dictionary_tables',set(sd.table_or_artifact)==tables and len(tables)==69)
# contract closure
vocab=pd.read_csv(SEC/'P3_CONTROLLED_VOCABULARIES_v5.csv',keep_default_na=False);ck('candidate_membership_no_decision_leak',not set(vocab[vocab.vocabulary_domain.isin(['candidate_membership_role','membership_role'])].code)&{'ACCEPTED_MEMBER','EXCLUDED_MEMBER'})
refs=pd.read_csv(SEC/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v5.csv',keep_default_na=False);ck('reference_contract_new_surfaces',{'p3_imported_lineage_membership','p3_pair_endpoint_resolution','p3_component_connectivity_edge','p3_internal_pair_collision','p3_internal_pair_closure'}<=set(refs.table_name))
# artifact catalog exact delivered paths
cat=pd.read_csv(SEC/'P3_ARTIFACT_CATALOG_v5.csv',keep_default_na=False); delivered=cat[cat.delivery_state.str.startswith('DELIVERED')]
missing=[x for x in delivered.artifact if not (SEC/x).exists()]; ck('artifact_catalog_delivered_exist',not missing,str(missing[:5]))
# no active markers / stale current identity
bad=[]
for p in SEC.rglob('*'):
 if not p.is_file() or p.suffix.lower() in {'.docx','.png','.pdf','.zip'} or p.name=='INHERITED_V24_PAYLOAD_HASHES.csv':continue
 try:t=p.read_text(errors='ignore')
 except:continue
 for i,line in enumerate(t.splitlines(),1):
  if re.match(r'^\s*(TODO|TBD|FIXME|PLACEHOLDER)(?:\b|:)',line,re.I):bad.append((str(p.relative_to(SEC)),i))
ck('no_active_scaffolds',not bad,str(bad[:5]))
# manifests/package state
for mf in ['SECTION_MANIFEST.csv']:
 rows=list(csv.DictReader((SEC/mf).open())); actual={str(p.relative_to(SEC)):p for p in SEC.rglob('*') if p.is_file() and p.name!=mf}; listed={r['relative_path'] for r in rows};ck('section_manifest_exact',listed==set(actual));ck('section_manifest_hashes',all(int(r['bytes'])==actual[r['relative_path']].stat().st_size and r['sha256']==sh(actual[r['relative_path']]) for r in rows))
# Builder/verifier parse
for p in [SEC/'validation/build_handoff_v25.py',SEC/'validation/verify_handoff_v25.py',SEC/'validation/whole_tree_type_and_archive_audit_v25.py']:
 ast.parse(p.read_text())
ck('scripts_parse',True)
pr=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(SEC/'validation/test_p3_plan_v5.py')],capture_output=True,text=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
ck('contract_tests_21',pr.returncode==0 and '21 passed' in pr.stdout,pr.stdout+pr.stderr)
# inherited v24 substantive payload hash lock
ih=pd.read_csv(SEC/'validation/INHERITED_V24_PAYLOAD_HASHES.csv',keep_default_na=False)
ck('inherited_v24_hash_lock',len(ih)==1165 and set(ih.preserved_in_v25)=={'YES'} and all((ROOT/r.relative_path).exists() and sh(ROOT/r.relative_path)==r.sha256 for r in ih.itertuples(index=False)))
# delivered/future catalog is disjoint and exact at the path level
ck('artifact_catalog_unique',cat.artifact.nunique()==len(cat))
ck('future_artifacts_absent',all(not (SEC/r.artifact).exists() for r in cat[~cat.delivery_state.str.startswith('DELIVERED')].itertuples(index=False)))
fail=[x for x in checks if not x[1]]
print(json.dumps({'status':'PASS' if not fail else 'FAIL','checks_passed':len(checks)-len(fail),'checks_total':len(checks),'failures':[{'name':x[0],'detail':x[2]} for x in fail]},indent=2))
sys.exit(1 if fail else 0)
