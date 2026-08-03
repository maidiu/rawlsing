#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re,hashlib,pathlib,sys,yaml
from jsonschema import Draft202012Validator, RefResolver
ROOT=pathlib.Path(sys.argv[1]).resolve(); SEC=ROOT/'46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK'
checks=[]
def ck(name,cond,detail=''):
    checks.append((name,bool(cond),detail)); print(('PASS' if cond else 'FAIL'),name,detail)
def rc(p):
    with open(p,newline='',encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def sh(p):
    h=hashlib.sha256();h.update(pathlib.Path(p).read_bytes());return h.hexdigest()
# inherited verifier
import subprocess
p=subprocess.run([sys.executable,str(ROOT/'45_P3_PLAN_SECOND_ACCEPTANCE_AUDIT_AND_HARDENING/validation/verify_handoff_v23.py'),str(ROOT)],capture_output=True,text=True)
ck('inherited_v23_118',p.returncode==0 and '"checks_passed": 118' in p.stdout,p.returncode)
# delivered artifact catalog closure
cat=rc(SEC/'P3_ARTIFACT_CATALOG_v4.csv')
for r in cat:
    if r['delivery_state'].startswith('DELIVERED'):
        ck('delivered_'+re.sub(r'\W+','_',r['artifact']), (SEC/r['artifact']).is_file(),r['artifact'])
ck('no_catalog_duplicate_paths',len(cat)==len({r['artifact'] for r in cat}),len(cat))
# no operative unfinished markers. Negative test descriptions may name marker tokens.
bad=[]
markers={'TODO','TBD','FIXME','PLACEHOLDER'}
for pth in SEC.rglob('*'):
    if not pth.is_file(): continue
    rel=str(pth.relative_to(SEC))
    if any(m in pth.name.upper() for m in markers|{'SKELETON'}): bad.append((rel,'filename'))
    if pth.suffix.lower()=='.csv':
        try:
            for row in rc(pth):
                for k,v in row.items():
                    if str(v).strip().upper() in markers: bad.append((rel,k))
        except Exception: pass
    elif pth.suffix.lower() in {'.md','.sql','.yaml','.json','.txt'}:
        for i,line in enumerate(pth.read_text(errors='ignore').splitlines(),1):
            if re.match(r'^\s*(TODO|TBD|FIXME|PLACEHOLDER)(?:\b|:)',line,re.I): bad.append((rel,i))
ck('no_unfinished_markers',not bad,bad[:5])
# identity coverage
voc=rc(SEC/'P3_CONTROLLED_VOCABULARIES_v4.csv'); obj={r['code'] for r in voc if r['vocabulary_domain']=='object_type'}
ids=rc(SEC/'P3_IDENTITY_KEY_SPEC_v4.csv'); idtypes={r['object_type'] for r in ids}
ck('identity_covers_object_types',obj==idtypes,(len(obj),len(idtypes),sorted(obj-idtypes),sorted(idtypes-obj)))
ck('identity_unique',len(ids)==len(idtypes),len(ids))
# schemas resolve and patterns agree
reg=rc(SEC/'P3_JSON_SCHEMA_REGISTRY_v4.csv'); store={}
for r in reg:
    s=json.loads((SEC/r['schema_file']).read_text());store[s['$id']]=s;ck('schema_hash_'+pathlib.Path(r['schema_file']).stem,sh(SEC/r['schema_file'])==r['sha256'])
for sid,s in store.items(): Draft202012Validator.check_schema(s)
for sid,s in store.items():
    RefResolver.from_schema(s,store=store)
ck('schemas_valid',len(store)>=36,len(store))
# examples
for f,sid in [('adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v4.json','candidate_packet.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_DRAFT_TEMPLATE_v4.json','adjudication_decision_draft.schema.json'),('adjudication/P3_ADJUDICATION_DECISION_EXAMPLE_v4.json','adjudication_decision.schema.json')]:
    inst=json.loads((SEC/f).read_text());sch=store['https://rawlsing.local/schemas/p3/v4/'+sid];errs=list(Draft202012Validator(sch,resolver=RefResolver.from_schema(sch,store=store)).iter_errors(inst));ck('example_'+pathlib.Path(f).stem,not errs,[e.message for e in errs[:2]])
# pair IDs and direct unresolved count
pf=store['https://rawlsing.local/schemas/p3/v4/pair_fact_bundle.schema.json'];ck('pair_fact_hex_pattern',pf['properties']['pair_fact_id']['pattern']=='^P3PF-[0-9a-f]{16}$')
cf=store['https://rawlsing.local/schemas/p3/v4/candidate_family.schema.json'];ipc=cf['properties']['internal_pair_counts'];ck('direct_unresolved_count','direct_unresolved' in ipc['required'])
co=store['https://rawlsing.local/schemas/p3/v4/closure_obligation.schema.json'];ck('closure_type_enum','enum' in co['properties']['obligation_type'])
# object refs and hyperedge roles
refs=rc(SEC/'P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv');ck('object_ref_nontrivial',len(refs)>=24,len(refs))
hr=rc(SEC/'P3_HYPEREDGE_ROLE_TYPE_CONTRACT_v4.csv');ck('all_six_hyperedges',len({r['hyperedge_type'] for r in hr})==6,len(hr))
ck('hyperedge_roles_nonblank',all(r['participant_role'] and r['allowed_object_types'] for r in hr))
# DDL enforcement present
ddl=(SEC/'sql/p3_postgresql_compatible_ddl_v4.sql').read_text()
for token in ['p3_identity_key_contract','p3_hyperedge_role_type_contract','p3_enforce_object_reference_type','p3_forbid_update_delete','p3_validate_candidate_status_event','p3_validate_release_status_event','p3_validate_promotion_pointer','p3_install_contract_triggers']:
    ck('ddl_'+token,token in ddl)
ck('ddl_rollback',ddl.rstrip().endswith('ROLLBACK;'))
# no migration skeleton, explicit block
ck('no_migration_skeleton',not list(SEC.rglob('*SKELETON*')))
block=json.loads((SEC/'release/P3_LIVE_INSTALLATION_BLOCKING_CONTRACT_v4.json').read_text());ck('installation_blocked_honestly',block['status'].startswith('BLOCKED_') and block['not_a_migration'])
# doctrine/version alignment
plan=(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md').read_text();lock=json.loads((SEC/'P3_PLAN_LOCK_v4.json').read_text());seq=yaml.safe_load((SEC/'P3_EXECUTION_SEQUENCE_v4.yaml').read_text())
ck('version_alignment',lock['plan_version']=='v4' and seq['next_execution_point']=='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION' and '`P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION`' in plan)
ck('exclusion_doctrine', (('named exclusions are required when actual rejected near-neighbors exist' in plan.lower()) or ('named exclusions are mandatory whenever there are actually rejected near-neighbors' in plan.lower())) and 'every accepted family has named and rule-based exclusions' not in plan.lower())
# root controls
state=json.loads((ROOT/'00_START_HERE/CURRENT_STATE.json').read_text());ck('root_state_v24',state['handoff_version']=='v24' and state['next_pass']=='P3A_CONTRACT_AND_PILOT_V4_IMPLEMENTATION')
ck('no_p3_execution',state.get('p3_execution_started') is False)
# package no debris
badfiles=[p for p in ROOT.rglob('*') if p.name in {'.pytest_cache','__pycache__'} or p.suffix in {'.pyc','.pyo'}];ck('no_debris',not badfiles,badfiles[:3])
# inherited v23 payload preservation
inh=rc(SEC/'validation/INHERITED_V23_PAYLOAD_HASHES.csv'); mism=[]
for r in inh:
    q=ROOT/r['relative_path']
    if not q.is_file() or q.stat().st_size!=int(r['bytes']) or sh(q)!=r['sha256']: mism.append(r['relative_path'])
ck('inherited_v23_payload_exact',not mism,(len(inh),mism[:5]))
ck('no_stale_inherited_validation',not (SEC/'validation/INHERITED_V22_PAYLOAD_HASHES.csv').exists() and not (SEC/'validation/V22_BASELINE_REVERIFICATION_RETURN.json').exists())
# every actual section file is catalogued except the self-generated section manifest
catalog_paths={r['artifact'] for r in cat}
unclassified=[str(x.relative_to(SEC)) for x in SEC.rglob('*') if x.is_file() and x.name!='SECTION_MANIFEST.csv' and str(x.relative_to(SEC)) not in catalog_paths]
ck('all_actual_artifacts_classified',not unclassified,unclassified[:5])
# all declared registry ID patterns agree with their concrete schemas
idmap={r['object_type']:r['id_pattern'] for r in ids}
schema_id_map={
 'LINEAGE_SEGMENT':('lineage_segment.schema.json','segment_id'),
 'PROPOSITION_SIGNATURE':('proposition_signature.schema.json','signature_id'),
 'RESPONSE_CONTRACT_REFERENCE':('response_contract_reference.schema.json','reference_id'),
 'STRUCTURAL_CONTEXT_REFERENCE':('structural_context_reference.schema.json','reference_id'),
 'PAIR_FACT':('pair_fact_bundle.schema.json','pair_fact_id'),
 'COLLISION':('collision_scope.schema.json','collision_id'),
 'CANDIDATE_COMPONENT':('candidate_component.schema.json','component_id'),
 'CLOSURE_OBLIGATION':('closure_obligation.schema.json','closure_obligation_id'),
 'HYPEREDGE':('hyperedge.schema.json','hyperedge_id'),
 'DEPENDENCY':('dependency_record.schema.json','dependency_id'),
 'CANDIDATE_PACKET':('candidate_packet.schema.json','packet_id'),
 'CANDIDATE_FAMILY':('candidate_family.schema.json','candidate_family_id'),
 'CANDIDATE_REVISION':('candidate_family.schema.json','revision_id'),
 'FAMILY_VARIANT':('candidate_variant.schema.json','variant_id'),
 'FAMILY_VARIANT_REVISION':('candidate_variant.schema.json','variant_revision_id'),
 'FAMILY_EXCLUSION':('family_exclusion.schema.json','exclusion_id'),
 'ADJUDICATION':('adjudication_decision.schema.json','adjudication_id'),
 'CANONICAL_FAMILY':('canonical_family.schema.json','canonical_family_id'),
 'CANONICAL_FAMILY_REVISION':('canonical_family_revision.schema.json','family_revision_id'),
 'DOCTRINE_DELTA':('doctrine_delta.schema.json','doctrine_delta_id'),
 'FAMILY_GENEALOGY':('family_genealogy.schema.json','genealogy_id')}
patbad=[]
for ot,(fn,field) in schema_id_map.items():
    got=store['https://rawlsing.local/schemas/p3/v4/'+fn]['properties'][field].get('pattern')
    exp='^'+idmap[ot]+'$'
    if got!=exp: patbad.append((ot,got,exp))
ck('schema_identity_patterns_complete',not patbad,patbad)
# candidate template closes its actual internal pair matrix and revision identity
pkt=json.loads((SEC/'adjudication/P3_CANDIDATE_PACKET_TEMPLATE_v4.json').read_text())
member_ids=pkt['candidate_family']['member_ids']; n=len(member_ids); expected=n*(n-1)//2
counts=pkt['candidate_family']['internal_pair_counts']; state_to_key={'DIRECT_POSITIVE':'direct_positive','DIRECT_COLLISION':'direct_collision','DIRECT_UNRESOLVED':'direct_unresolved','HIERARCHICAL_ONLY':'hierarchical_only','UNRULED':'unruled','SIGNATURE_CONFLICT':'signature_conflict','SIGNATURE_COMPATIBLE':'signature_compatible'}
actual={k:0 for k in state_to_key.values()}
for r in pkt['internal_pair_matrix']: actual[state_to_key[r['pair_state']]]+=1
ck('packet_pair_matrix_exact',counts['expected_pairs']==expected==len(pkt['internal_pair_matrix']) and sum(counts[k] for k in state_to_key.values())==expected and all(counts[k]==v for k,v in actual.items()),(expected,counts,actual))
rev=pkt['candidate_family']; ck('candidate_revision_ordinal_consistent',rev['revision_id']==f"P3CANDREV-{rev['candidate_family_id'].split('-')[1]}-R{rev['revision_number']:04d}")
ck('decision_ordinal_present',pkt['decision_form']['decision_ordinal']>=1 and 'split_points' in pkt['decision_form'])
# canonical serialization fixed vectors
import unicodedata
def canon(x,set_paths=frozenset(),path=''):
    if isinstance(x,float): raise ValueError('float')
    if x is None or isinstance(x,(bool,int)): return x
    if isinstance(x,str): return unicodedata.normalize('NFC',x.replace('\r\n','\n').replace('\r','\n'))
    if isinstance(x,dict): return {k:canon(x[k],set_paths,(path+'.'+k).strip('.')) for k in sorted(x)}
    if isinstance(x,list):
        vals=[canon(v,set_paths,path) for v in x]
        if path in set_paths:
            ser=[json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')) for v in vals]
            if len(ser)!=len(set(ser)): raise ValueError('duplicate')
            vals=[v for _,v in sorted(zip(ser,vals),key=lambda z:z[0])]
        return vals
    raise ValueError('unsupported')
def cbytes(x,set_paths=frozenset()): return json.dumps(canon(x,set_paths),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
vec=json.loads((SEC/'P3_CANONICAL_SERIALIZATION_TEST_VECTORS_v4.json').read_text()); verr=[]
for v in vec['vectors']:
    try:
        paths={v['path']} if 'path' in v else set(); a=cbytes(v['a'],paths)
        if v.get('must_fail'): verr.append((v['name'],'did_not_fail'))
        elif (a==cbytes(v['b'],paths))!=v['must_match']: verr.append((v['name'],'match_mismatch'))
    except Exception:
        if not v.get('must_fail'): verr.append((v['name'],'unexpected_fail'))
ck('canonical_serialization_vectors',not verr,verr)
# DDL/schema persistence joints
for token in ['revision_number INTEGER','decision_ordinal INTEGER','p3_adjudication_split_point','p3_adjudication_split_member','p3_adjudication_unresolved_boundary','p3_enforce_identity_contract','p3_validate_hyperedge_member_type','p3_validate_hyperedge_cardinality','p3_object_registry_identity_validate','p3_hyperedge_member_cardinality']:
    ck('ddl_final_'+re.sub(r'\W+','_',token),token in ddl)
# contract table/column references actually exist in DDL (simple parser sufficient for logical contract)
def ddl_tables(sql):
    out={}
    for m in re.finditer(r'CREATE TABLE\s+(\w+)\s*\(',sql,re.I):
        name=m.group(1); i=m.end(); depth=1; ins=False
        while i<len(sql) and depth:
            c=sql[i]
            if c=="'":
                if ins and i+1<len(sql) and sql[i+1]=="'": i+=2; continue
                ins=not ins
            elif not ins:
                if c=='(': depth+=1
                elif c==')': depth-=1
            i+=1
        body=sql[m.end():i-1]; parts=[];cur='';d=0;ins=False
        for c in body+',':
            if c=="'": ins=not ins
            if not ins:
                if c=='(':d+=1
                elif c==')':d-=1
            if c==',' and d==0: parts.append(cur.strip());cur='';continue
            cur+=c
        cols=set()
        for part in parts:
            mm=re.match(r'(\w+)\s+',part)
            if mm and mm.group(1).upper() not in {'PRIMARY','FOREIGN','UNIQUE','CHECK','CONSTRAINT'}: cols.add(mm.group(1))
        out[name]=cols
    return out
dtabs=ddl_tables(ddl); contract_missing=[]
for fn in ['P3_CATEGORICAL_FIELD_VOCAB_BINDINGS_v4.csv','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v4.csv']:
    for r in rc(SEC/fn):
        if r['table_name'] not in dtabs or r['column_name'] not in dtabs.get(r['table_name'],set()): contract_missing.append((fn,r['table_name'],r['column_name']))
ck('ddl_contract_columns_exist',not contract_missing,contract_missing[:10])
# governing files contain no stale v3 contract references
stale=[]
for rel in ['Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md','algorithms/P3_ALGORITHMS_AND_PSEUDOCODE_v4.md','sql/P3_DDL_VALIDATION_QUERIES_v4.sql','P3_PLAN_LOCK_v4.json','P3_EXECUTION_SEQUENCE_v4.yaml']:
    txt=(SEC/rel).read_text()
    for x in ['P3_IDENTITY_KEY_SPEC_v3','P3_OBJECT_REFERENCE_TYPE_CONTRACT_v3','P3A_CONTRACT_AND_PILOT_V3_IMPLEMENTATION','v23 validator']:
        if x in txt: stale.append((rel,x))
ck('no_stale_v3_governing_references',not stale,stale)


# Governing-version labels must agree in machine-readable and rendered source text.
_plan_md=(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.md').read_text()
ck('plan_markdown_declares_v4', '**Plan version:** v4' in _plan_md and '**Plan version:** v3' not in _plan_md, '')
from docx import Document as _VDoc
def _all_docx_text(_path):
    _d=_VDoc(_path); _parts=[p.text for p in _d.paragraphs]
    for _s in _d.sections:
        for _c in [_s.header,_s.first_page_header,_s.even_page_header,_s.footer,_s.first_page_footer,_s.even_page_footer]:
            _parts.extend(p.text for p in _c.paragraphs)
    return '\n'.join(_parts)
_plan_doc_text=_all_docx_text(SEC/'Rawlsing_P3_Structure_Articulation_and_Implementation_Plan_v4_20260731.docx')
_master_doc_text=_all_docx_text(ROOT/'00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v24_20260731.docx')
_audit_doc_text=_all_docx_text(SEC/'Rawlsing_P3_Plan_Third_Bounded_Implementation_Readiness_Audit_v1_20260731.docx')
ck('governing_docx_version_labels_current', 'Plan version: v4' in _plan_doc_text and 'P3 Plan v3' not in _plan_doc_text and 'Implementation Plan v3' not in _plan_doc_text and 'Master Handoff v23' not in _master_doc_text and 'Second Acceptance Audit and Hardening' not in _audit_doc_text, '')

# Final release-return validation is activated once root validation advances beyond assembly-pending state.
_root_validation=json.loads((ROOT/'VALIDATION.json').read_text())
_release_expected=_root_validation.get('status')!='BUILD_TREE_PENDING_FINAL_RELEASE_GATE'
if _release_expected:
    _qa_path=SEC/'validation/P3_DOCUMENT_QA_RETURN_v4.json'
    _tree_path=SEC/'validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json'
    _repro_path=SEC/'validation/P3_ASSEMBLY_REPRODUCIBILITY_RETURN_v4.json'
    ck('release_return_files_present', all(p.is_file() for p in [_qa_path,_tree_path,_repro_path]), '')
    if all(p.is_file() for p in [_qa_path,_tree_path,_repro_path]):
        _qa=json.loads(_qa_path.read_text()); _tree=json.loads(_tree_path.read_text()); _repro=json.loads(_repro_path.read_text())
        ck('document_qa_return_pass', _qa.get('status')=='PASS' and _qa.get('total_pages_rendered')==34 and _qa.get('total_pages_visually_inspected')==34 and _qa.get('a11y_findings')=={'high':0,'medium':0,'low':0}, _qa)
        ck('whole_tree_audit_return_pass', _tree.get('status')=='PASS' and not _tree.get('errors') and _tree.get('recursive_archive_instances')==88 and _tree.get('unique_archive_payloads')==77 and _tree.get('cache_debris_count')==0, _tree)
        ck('assembly_reproducibility_return_pass', _repro.get('status')=='PASS' and not _repro.get('differences') and _repro.get('substantive_contract_files_compared')==_repro.get('substantive_contract_files_hash_identical') and _repro.get('clean_rebuild_verifier',{}).get('status')=='PASS', _repro)

fails=[x for x in checks if not x[1]]
print(json.dumps({'status':'PASS' if not fails else 'FAIL','checks_passed':len(checks)-len(fails),'checks_total':len(checks),'failures':[x[0] for x in fails]},indent=2))
sys.exit(1 if fails else 0)
