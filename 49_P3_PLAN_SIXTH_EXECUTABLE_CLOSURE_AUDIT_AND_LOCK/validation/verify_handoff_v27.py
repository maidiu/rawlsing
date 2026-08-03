from __future__ import annotations
from pathlib import Path
import argparse, ast, csv, hashlib, json, os, re, subprocess, sys, zipfile
from collections import Counter,defaultdict
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry,Resource
SECTION='49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK'
def sha(p:Path):return hashlib.sha256(p.read_bytes()).hexdigest()
def loadj(p:Path):return json.loads(p.read_text(encoding='utf-8'))
def rows(p:Path):return list(csv.DictReader(p.open(encoding='utf-8',newline='')))
def manifest_exact(root:Path,path:Path,excluded:set[str]):
    rr=rows(path);actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in excluded}
    return set(r['relative_path'] for r in rr)==set(actual) and all(int(r['bytes'])==actual[r['relative_path']].stat().st_size and r['sha256']==sha(actual[r['relative_path']]) for r in rr),len(rr),len(actual)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('root');ap.add_argument('--output');a=ap.parse_args();root=Path(a.root).resolve();sec=root/SECTION
    checks=[]
    def ck(name,cond,detail=''):
        checks.append({'name':name,'pass':bool(cond),'detail':str(detail)})
        if not cond:print('FAIL',name,detail,file=sys.stderr)
    st=loadj(root/'00_START_HERE/CURRENT_STATE.json')
    ck('current_state_v27_v7',st.get('handoff_version')=='v27' and st.get('plan_version')=='v7' and st.get('governing_section')==SECTION and st.get('next_pass')=='P3A_CONTRACT_AND_PILOT_V7_IMPLEMENTATION')
    rv=loadj(root/'VALIDATION.json');ck('root_validation_v27_v7',rv.get('handoff_version')=='v27' and rv.get('plan_version')=='v7' and rv.get('governing_section')==SECTION)
    lock=loadj(sec/'P3_PLAN_LOCK_v7.json');ck('plan_lock_v7',lock.get('plan_version')=='v7' and lock.get('exact_next_execution_point')=='P3A_CONTRACT_AND_PILOT_V7_IMPLEMENTATION')
    ck('authority_boundary_not_overclaimed',not st.get('p3_execution_started') and st.get('live_postgresql_execution')=='NOT_RUN_NO_USER_DESIGNATED_TARGET')
    eff=rows(sec/'upstream/P3_EFFECTIVE_UPSTREAM_PAIR_AUTHORITY_SURFACE_v7.csv');keys=[r['pair_key'] for r in eff]
    ck('effective_pair_surface_19175',len(eff)==19175 and len(set(keys))==19175)
    prop=rows(sec/'upstream/P3_PROPOSITION_RELATION_ELIGIBILITY_PREFLIGHT_v7.csv');pkeys=[r['pair_key'] for r in prop]
    eligible=[r for r in prop if r['provisional_j_family_eligibility']=='J_FAMILY_CANDIDATE_ELIGIBLE']
    ck('proposition_surface_658_657',len(prop)==658 and len(set(pkeys))==658 and len(eligible)==657)
    lineage=rows(root/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv')
    impl=[]
    for r in lineage:impl.extend(json.loads(r['member_question_implementation_ids_json']))
    ck('lineage_implementation_no_loss',len(lineage)==13526 and len({r['lineage_id'] for r in lineage})==13526 and len(impl)==18276 and len(set(impl))==18276)
    e1=[r for r in eligible if r['p3_relation_type']=='PROPOSITION_RESPONSE_IDENTITY'];e2=[r for r in eligible if r['p3_relation_type']=='PROPOSITION_IDENTITY_ONLY']
    def comps(rr):
        adj=defaultdict(set)
        for r in rr:adj[r['left_lineage_id']].add(r['right_lineage_id']);adj[r['right_lineage_id']].add(r['left_lineage_id'])
        seen=set();out=[]
        for n in sorted(adj):
            if n in seen:continue
            stack=[n];seen.add(n);c=set()
            while stack:
                x=stack.pop();c.add(x)
                for y in adj[x]:
                    if y not in seen:seen.add(y);stack.append(y)
            out.append(c)
        return out
    c1=comps(e1);idx={n:i for i,c in enumerate(c1) for n in c};cats=Counter();outside=[]
    for r in e2:
        x=idx.get(r['left_lineage_id']);y=idx.get(r['right_lineage_id'])
        if x is not None and y is not None and x==y:cats['within']+=1
        elif (x is None) ^ (y is None):cats['orphan']+=1
        elif x is not None and y is not None:cats['bridge']+=1
        else:cats['outside']+=1;outside.append(r)
    ck('strict_topology',len(e1)==445 and len({x for r in e1 for x in (r['left_lineage_id'],r['right_lineage_id'])})==304 and len(c1)==94)
    ck('proposition_only_topology',len(e2)==212 and cats==Counter({'within':1,'orphan':85,'bridge':70,'outside':56}) and len(comps(outside))==25,cats)
    pre=loadj(sec/'upstream/P3_EXECUTION_INSTANTIATION_PREFLIGHT_RETURN_v7.json');ck('pre_signature_diagnostics',pre.get('attachment_review_groups')==22 and pre.get('pre_signature_candidate_records')==141)
    schema_files=sorted((sec/'schemas').glob('*.json'));resources=[]
    try:
        for p in schema_files:
            o=loadj(p);Draft202012Validator.check_schema(o);resources.append((o['$id'],Resource.from_contents(o)))
        reg=Registry().with_resources(resources)
        ck('schemas_50_connected',len(schema_files)==50)
        sr=rows(sec/'P3_JSON_SCHEMA_REGISTRY_v7.csv')
        ck('schema_registry_exact',len(sr)==50 and {Path(r['schema_file']).name for r in sr}=={p.name for p in schema_files} and all(r['all_dependencies_local']=='YES' and r['sha256']==sha(sec/r['schema_file']) for r in sr))
        for schema,example in [('candidate_packet.schema.json','adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json'),('adjudication_decision.schema.json','adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v7.json'),('adjudication_decision.schema.json','adjudication/status_fixtures/VALID_SPLIT_DECISION_v7.json'),('adjudication_decision.schema.json','adjudication/status_fixtures/VALID_HIERARCHY_DECISION_v7.json')]:
            Draft202012Validator(loadj(sec/'schemas'/schema),registry=reg,format_checker=FormatChecker()).validate(loadj(sec/example))
        ck('schema_examples_validate',True)
    except Exception as e:ck('schema_examples_validate',False,repr(e))
    validator=sec/'validation/validate_p3_candidate_packet_v7.py';packet=sec/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v7.json'
    for name,decision in [('accepted','P3_ADJUDICATION_DECISION_EXAMPLE_v7.json'),('split','status_fixtures/VALID_SPLIT_DECISION_v7.json'),('hierarchy','status_fixtures/VALID_HIERARCHY_DECISION_v7.json')]:
        pr=subprocess.run([sys.executable,str(validator),str(packet),str(sec/'adjudication'/decision)],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        ck('semantic_'+name,pr.returncode==0 and 'PASS' in pr.stdout,pr.stdout+pr.stderr)
    pr=subprocess.run([sys.executable,str(sec/'validation/static_sql_contract_check_v7.py'),str(sec/'sql/p3_postgresql_compatible_ddl_v7.sql'),str(sec/'sql/P3_DDL_VALIDATION_QUERIES_v7.sql')],capture_output=True,text=True,cwd=sec,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    ck('static_sql_contract',pr.returncode==0 and 'PASS' in pr.stdout,pr.stdout+pr.stderr)
    ddl=(sec/'sql/p3_postgresql_compatible_ddl_v7.sql').read_text(encoding='utf-8');tables=re.findall(r'CREATE TABLE\s+(?:IF NOT EXISTS\s+)?([A-Za-z_][A-Za-z0-9_]*)',ddl,re.I)
    ck('ddl_75_tables_one_final_rollback',len(tables)==75 and len(set(tables))==75 and len(re.findall(r'\bROLLBACK\s*;',ddl,re.I))==1 and ddl.rstrip().upper().endswith('ROLLBACK;'))
    required=['origin_key','occurred_at','direct_pair_projection_id','p3_assert_candidate_origin','p3_assert_adjudication_member_partition','p3_assert_split_result_partition','p3_assert_canonical_promotion_closure']
    ck('ddl_required_closure_surfaces',all(x in ddl for x in required))
    f=rows(sec/'P3_SIXTH_PASS_FINDINGS_v7.csv');ck('findings_18',len(f)==18 and {r['detection_stage'] for r in f}=={'V26_EXECUTION','V26_PACKET_VALIDATION','V26_IDENTITY','V26_TESTING'})
    bad_vocab=(sec/'P3_CONTROLLED_VOCABULARIES_v7.csv').read_text(encoding='utf-8')
    ck('current_vocabulary_no_stale_roles','HIERARCHICAL_RELATIVE' not in bad_vocab and 'CANDIDATE_MEMBER' not in bad_vocab and 'PROPOSED_HIERARCHICAL_CONTEXT' in bad_vocab)
    cat=rows(sec/'P3_ARTIFACT_CATALOG_v7.csv');arts=[r['artifact'] for r in cat]
    ck('artifact_catalog_unique',len(arts)==len(set(arts)))
    missing=[a for a in arts if not (sec/a).exists() and next(r for r in cat if r['artifact']==a)['delivery_state'].startswith('DELIVERED')]
    ck('delivered_artifacts_exist',not missing,missing[:10])
    cache=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and ('__pycache__' in p.parts or '.pytest_cache' in p.parts or p.suffix=='.pyc')]
    ck('no_cache_debris',not cache,cache[:10])
    pr=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider',str(sec/'validation/test_p3_plan_v7.py')],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    ck('contract_tests_30',pr.returncode==0 and '30 passed' in pr.stdout,pr.stdout+pr.stderr)
    ih=rows(sec/'validation/INHERITED_V26_PAYLOAD_HASHES.csv');preserved=all((root/r['relative_path']).exists() and (root/r['relative_path']).stat().st_size==int(r['bytes']) and sha(root/r['relative_path'])==r['sha256'] for r in ih)
    ck('inherited_v26_hash_lock',len(ih)>=1380 and preserved,len(ih))
    qa=loadj(sec/'validation/P3_DOCUMENT_QA_RETURN_v7.json');ck('document_qa_34_pages',qa.get('status')=='PASS' and qa.get('total_pages')==34 and qa.get('clipping_or_overlap')==0 and qa.get('footer_version_mismatch')==0)
    wt=loadj(sec/'validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v7.json');ck('whole_tree_audit',wt.get('status')=='PASS' and wt.get('cache_or_bytecode_debris')==0)
    sx=manifest_exact(sec,sec/'SECTION_MANIFEST.csv',{'SECTION_MANIFEST.csv'});ck('section_manifest_exact',sx[0],sx[1:])
    px=manifest_exact(root,root/'PACKAGE_INDEX.csv',{'PACKAGE_INDEX.csv','SHA256SUMS.csv'});ck('package_manifest_exact',px[0],px[1:])
    ck('root_manifests_identical',(root/'PACKAGE_INDEX.csv').read_bytes()==(root/'SHA256SUMS.csv').read_bytes())
    for p in [sec/'validation/build_handoff_v27.py',sec/'validation/verify_handoff_v27.py',sec/'validation/whole_tree_type_and_archive_audit_v27.py',validator,sec/'validation/test_p3_plan_v7.py']:
        ast.parse(p.read_text(encoding='utf-8'))
    ck('governing_scripts_parse',True)
    exact='P3A_CONTRACT_AND_PILOT_V7_IMPLEMENTATION'
    ck('exact_continuation_consistent',all(exact in p.read_text(encoding='utf-8',errors='ignore') for p in [root/'README_FIRST.md',root/'MASTER_HANDOFF.md',root/'00_START_HERE/EXACT_RESUME_POINT.md',sec/'README_FIRST.md']))
    fails=[c for c in checks if not c['pass']]
    result={'status':'PASS' if not fails else 'FAIL','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks),'failures':fails,
            'handoff_version':'v27','plan_version':'v7','scope':'extracted cumulative tree','live_postgresql_execution':'NOT_RUN_NO_USER_DESIGNATED_TARGET'}
    text=json.dumps(result,indent=2)+'\n';print(text,end='')
    if a.output:Path(a.output).write_text(text,encoding='utf-8')
    raise SystemExit(0 if not fails else 1)
if __name__=='__main__':main()
