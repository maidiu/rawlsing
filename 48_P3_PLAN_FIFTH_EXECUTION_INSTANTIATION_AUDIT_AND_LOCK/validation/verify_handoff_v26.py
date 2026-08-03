from __future__ import annotations
from pathlib import Path
import sys,json,csv,re,hashlib,ast,subprocess,os
from collections import Counter,defaultdict
import pandas as pd,yaml
from referencing import Registry,Resource
from jsonschema import Draft202012Validator
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
SEC=ROOT/'48_P3_PLAN_FIFTH_EXECUTION_INSTANTIATION_AUDIT_AND_LOCK'
checks=[]
def ck(name,cond,detail=''):
    checks.append((name,bool(cond),str(detail)))
    if not cond:print('FAIL',name,detail)
def loadj(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def manifest_check(root,path,excluded_relpaths):
    rows=list(csv.DictReader(path.open(encoding='utf-8')))
    actual={str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file() and str(p.relative_to(root)) not in excluded_relpaths}
    listed={r['relative_path'] for r in rows}
    return listed==set(actual), all(r['relative_path'] in actual and int(r['bytes'])==actual[r['relative_path']].stat().st_size and r['sha256']==sha(actual[r['relative_path']]) for r in rows),len(rows),len(actual)
# State and lock
st=loadj(ROOT/'00_START_HERE/CURRENT_STATE.json');ck('state_v26',st.get('handoff_version')=='v26' and st.get('plan_version')=='v6' and st.get('p3_plan_status')=='V6_LOCKED_AFTER_FIFTH_EXECUTION_INSTANTIATION_AUDIT' and st.get('next_pass')=='P3A_CONTRACT_AND_PILOT_V6_IMPLEMENTATION')
lock=loadj(SEC/'P3_PLAN_LOCK_v6.json');ck('plan_lock_v6',lock.get('plan_version')=='v6' and lock['effective_input_surface']['effective_unique_direct_pair_authorities']==19175)
val=loadj(ROOT/'VALIDATION.json');ck('release_status_pass',val.get('status')=='PASS' and val.get('handoff_version')=='v26')
# Upstream exactness
eff=pd.read_csv(SEC/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v6.csv',keep_default_na=False)
prop=pd.read_csv(SEC/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v6.csv',keep_default_na=False)
lin=pd.read_csv(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv',keep_default_na=False)
ck('effective_pair_surface',len(eff)==19175 and eff.pair_key.nunique()==19175)
ck('proposition_surface',len(prop)==658 and prop.pair_key.nunique()==658 and (prop.provisional_j_family_eligibility=='J_FAMILY_CANDIDATE_ELIGIBLE').sum()==657)
impl=[]
for x in lin.member_question_implementation_ids_json:impl+=json.loads(x)
ck('lineage_implementation_no_loss',len(lin)==13526 and lin.lineage_id.nunique()==13526 and len(impl)==18276 and len(set(impl))==18276 and int(lin.member_count.sum())==18276)
# Topology
sub=prop[prop.provisional_j_family_eligibility=='J_FAMILY_CANDIDATE_ELIGIBLE'];E1=sub[sub.p3_relation_type=='PROPOSITION_RESPONSE_IDENTITY'];E2=sub[sub.p3_relation_type=='PROPOSITION_IDENTITY_ONLY']
def comps(df):
    adj=defaultdict(set)
    for r in df.itertuples():adj[r.left_lineage_id].add(r.right_lineage_id);adj[r.right_lineage_id].add(r.left_lineage_id)
    seen=set();out=[]
    for n in sorted(adj):
        if n in seen:continue
        stack=[n];seen.add(n);c=set()
        while stack:
            x=stack.pop();c.add(x)
            for y in sorted(adj[x]):
                if y not in seen:seen.add(y);stack.append(y)
        out.append(c)
    return out
c1=comps(E1);idx={n:i for i,c in enumerate(c1) for n in c};cats=Counter();outside=[]
for r in E2.itertuples():
    a=idx.get(r.left_lineage_id);b=idx.get(r.right_lineage_id)
    if a is not None and b is not None and a==b:cats['within_strict_component']+=1
    elif (a is None) ^ (b is None):cats['attaches_orphan_to_strict']+=1
    elif a is not None and b is not None and a!=b:cats['bridges_strict_components']+=1
    else:cats['both_endpoints_outside_strict']+=1;outside.append(r)
outdf=pd.DataFrame([r._asdict() for r in outside])
ck('strict_topology',len(E1)==445 and len({*E1.left_lineage_id,*E1.right_lineage_id})==304 and len(c1)==94)
ck('proposition_only_topology',len(E2)==212 and cats==Counter({'within_strict_component':1,'attaches_orphan_to_strict':85,'bridges_strict_components':70,'both_endpoints_outside_strict':56}) and len(comps(outdf))==25,cats)
pre=loadj(SEC/'upstream/P3_EXECUTION_INSTANTIATION_PREFLIGHT_RETURN_v6.json');ck('preflight_141',pre.get('pre_signature_candidate_records')==141 and pre.get('attachment_review_groups')==22)
# Schemas and examples
schema_files=sorted((SEC/'schemas').glob('*.json'));resources=[]
for p in schema_files:
    o=loadj(p);Draft202012Validator.check_schema(o);resources.append((o['$id'],Resource.from_contents(o)))
reg=Registry().with_resources(resources)
for s,e in [('candidate_packet.schema.json','adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json'),('adjudication_decision_draft.schema.json','adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v6.json'),('adjudication_decision.schema.json','adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v6.json')]:
    Draft202012Validator(loadj(SEC/'schemas'/s),registry=reg).validate(loadj(SEC/e))
ck('schemas_50_offline',len(schema_files)==50)
rr=list(csv.DictReader((SEC/'P3_JSON_SCHEMA_REGISTRY_v6.csv').open(encoding='utf-8')))
ck('schema_registry_exact',len(rr)==50 and {r['schema_file'].split('/')[-1] for r in rr}=={p.name for p in schema_files} and all(r['all_dependencies_local']=='YES' and r['sha256']==sha(SEC/r['schema_file']) for r in rr))
# Semantic packet validator for draft and completed example
cmd=[sys.executable,str(SEC/'validation/validate_p3_candidate_packet_v6.py'),str(SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v6.json'),str(SEC/'adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v6.json')]
pr=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});ck('semantic_packet_validator',pr.returncode==0 and 'PASS' in pr.stdout,pr.stdout+pr.stderr)
# DDL/schema dictionary
ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v6.sql').read_text(encoding='utf-8')
tables=re.findall(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*)',ddl,re.I)
sd=pd.read_csv(SEC/'P3_SCHEMA_DICTIONARY_v6.csv',keep_default_na=False)
ck('ddl_75_tables',len(tables)==75 and len(set(tables))==75)
ck('schema_dictionary_exact_tables',set(sd.table_or_artifact)==set(tables) and sd.table_or_artifact.nunique()==75)
required=['p3_pair_projection','p3_candidate_attachment_projection','p3_adjudication_split_result','p3_variant_promotion','p3_exclusion_promotion','p3_validate_pair_projection','p3_assert_candidate_origin','p3_assert_adjudication_member_partition','p3_assert_split_result_partition','p3_assert_canonical_promotion_closure']
ck('ddl_execution_surfaces',all(x in ddl for x in required))
ck('directional_projection_preserved','CHECK (left_subject_id < right_subject_id)' not in ddl and 'orientation' in ddl.lower())
ck('no_sql_empty_stubs',not re.search(r'BEGIN\s+RETURN\s+(?:NEW|TRUE)\s*;\s*END',ddl,re.I|re.S))
# Contract registries and findings
findings=pd.read_csv(SEC/'P3_FIFTH_PASS_FINDINGS_v6.csv',keep_default_na=False);ck('findings_18',len(findings)==18 and set(findings.detection_stage)=={'V25_INPUT','V26_CORRECTION_QA'})
cat=pd.read_csv(SEC/'P3_ARTIFACT_CATALOG_v6.csv',keep_default_na=False);ck('artifact_catalog_unique',cat.artifact.nunique()==len(cat))
missing=[r.artifact for r in cat[cat.delivery_state.str.startswith('DELIVERED')].itertuples() if not (SEC/r.artifact).exists()];ck('delivered_artifacts_exist',not missing,missing[:5])
future=[r.artifact for r in cat[~cat.delivery_state.str.startswith('DELIVERED')].itertuples() if (SEC/r.artifact).exists()];ck('future_artifacts_absent',not future,future[:5])
# No active scaffolds/stale identities in governing current text
bad=[]
for p in SEC.rglob('*'):
    if not p.is_file() or p.suffix.lower() in {'.docx','.zip','.png','.pdf'} or p.name=='INHERITED_V25_PAYLOAD_HASHES.csv':continue
    try:text=p.read_text(encoding='utf-8',errors='ignore')
    except:continue
    for i,line in enumerate(text.splitlines(),1):
        if re.match(r'^\s*(TODO|TBD|FIXME|PLACEHOLDER)(?:\b|:)',line,re.I):bad.append((str(p.relative_to(SEC)),i))
ck('no_active_scaffolds',not bad,bad[:5])
# Tests
pr=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(SEC/'validation/test_p3_plan_v6.py')],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'});ck('contract_tests_29',pr.returncode==0 and '29 passed' in pr.stdout,pr.stdout+pr.stderr)
# Inherited v25 substantive hash lock
ih=pd.read_csv(SEC/'validation/INHERITED_V25_PAYLOAD_HASHES.csv',keep_default_na=False)
ck('inherited_v25_hash_lock',len(ih)==1246 and set(ih.preserved_in_v26)=={'YES'} and all((ROOT/r.relative_path).exists() and sha(ROOT/r.relative_path)==r.sha256 for r in ih.itertuples(index=False)))
# QA return
qa=loadj(SEC/'validation/P3_DOCUMENT_QA_RETURN_v6.json');ck('document_qa',qa.get('status')=='PASS' and qa.get('total_pages')==30 and qa.get('blank_or_orphan_pages')==0 and qa.get('clipping_or_overlap')==0 and all(d['accessibility']=={'high':0,'medium':0,'low':0} for d in qa['documents']))
# Manifests
x,h,n,a=manifest_check(SEC,SEC/'SECTION_MANIFEST.csv',{'SECTION_MANIFEST.csv'});ck('section_manifest_exact',x and h,(n,a))
x,h,n,a=manifest_check(ROOT,ROOT/'PACKAGE_INDEX.csv',{'PACKAGE_INDEX.csv','SHA256SUMS.csv'});ck('package_index_exact',x and h,(n,a))
ck('root_manifests_identical',(ROOT/'PACKAGE_INDEX.csv').read_bytes()==(ROOT/'SHA256SUMS.csv').read_bytes())
# Scripts parse
for p in [SEC/'validation/build_handoff_v26.py',SEC/'validation/verify_handoff_v26.py',SEC/'validation/whole_tree_type_and_archive_audit_v26.py',SEC/'validation/validate_p3_candidate_packet_v6.py',SEC/'validation/test_p3_plan_v6.py']:ast.parse(p.read_text(encoding='utf-8'))
ck('scripts_parse',True)
fail=[x for x in checks if not x[1]]
res={'status':'PASS' if not fail else 'FAIL','checks_passed':len(checks)-len(fail),'checks_total':len(checks),'failures':[{'name':n,'detail':d} for n,ok,d in fail]}
print(json.dumps(res,indent=2));sys.exit(1 if fail else 0)
