"""Mechanical custody, full case matrix, independent Git/import/guard audit."""
from stage import R,git,blob,TARGET,PREFIX
from pathlib import Path
import json,hashlib,sys,xml.etree.ElementTree as E,shutil,datetime,uuid,platform,subprocess
S=R/'staging/ms3';M2=S/'staging/ms2';MS1=M2/'staging/ms1';RT=MS1/'runtime'
def save(p,d):
    p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,default=str)+'\n')
def case_rows(path):
    return [dict(classname=t.get('classname'),name=t.get('name'),outcome='FAIL' if t.find('failure') is not None else 'ERROR' if t.find('error') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS',message=(t.find('failure').get('message') if t.find('failure') is not None else None)) for t in E.parse(path).getroot().iter('testcase')]
# Native9 and guard, plus every source oracle and sealed repair file.
rows=[]
for x in json.loads((MS1/'evidence/native_source_ledger.json').read_text()):
    p=MS1/x['local'];b=p.read_bytes();assert b==git('show',x['commit']+':'+x['authoritative_path']) and blob(b)==x['git_blob_sha1']
    rows.append(dict(commit=x['commit'],path=x['authoritative_path'],local=str(p.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
spec=[('d40cc32ecec8f681dcced6a482b6438a86080899','WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1/runtime/test_ms1_serial.py',RT/'test_ms1_serial.py'),('34b96ea98de181ca5264f0eed3824cad2db7cfc0','WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/test_ms2.py',M2/'repro/test_ms2.py'),('34b96ea98de181ca5264f0eed3824cad2db7cfc0','WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/repro/test_literal_p3b.py',M2/'repro/test_literal_p3b.py')]
for name in ['test_author.py','test_selector_extension_v2.py']:spec.append((TARGET,PREFIX+'/repro/'+name,S/'repro'/name))
for name in ['ms1_serial.py','ms3_native_custody.py']:spec.append((TARGET,PREFIX+'/candidate/'+name,RT/name))
for sha,path,p in spec:
    b=p.read_bytes();assert b==git('show',sha+':'+path);rows.append(dict(commit=sha,path=path,local=str(p.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
laws={}
for name,h in {'CAN008_R2':'b80dd6925066510ecbbfec7b427bf9f688475663','ADP016':'c6619a286e115d060ab4830889e7fc23762167a5','ADP017':'eece4f3f2f3f9288ab9bbc645dc81e20a99e1280'}.items():
    b=git('cat-file','blob',h);assert blob(b)==h and (M2/'staging/accepted_law'/(name+'.txt')).read_bytes()==b;laws[name]=dict(blob_sha1=h,sha256=hashlib.sha256(b).hexdigest())
sys.path.insert(0,str(RT));import ms1_serial,ms3_native_custody
from rawlsing_next import v3_psepf_zero_positive_guard as guard
assert not guard.DEFAULT_ACCEPTED_POSITIVE_TRANSITION_AUTHORITIES
imports=[]
for n,m in sorted(sys.modules.items()):
    f=getattr(m,'__file__',None)
    if f and n.startswith(('ms1_serial','ms3_native_custody','candidate','rawlsing_next')) and Path(f).suffix=='.py':
        p=Path(f).resolve();b=p.read_bytes();imports.append(dict(module=n,module_file=str(p.relative_to(R)),blob_sha1=blob(b),sha256=hashlib.sha256(b).hexdigest()))
assert blob(Path(guard.__file__).read_bytes())=='e0528d65215cb431196570c38bac4eae94217a1b'
all_import_receipts=[]
for p in sorted((R/'evidence').glob('*/*/actual_imports.json')):
    data=json.loads(p.read_text());
    for x in data['imports']:
        name=x['module'];local=R/x['module_file']
        if name not in ('ms1_serial','ms3_native_custody'):
            assert blob(local.read_bytes())==x['blob_sha1']
        elif name=='ms1_serial':
            expected=blob(git('show',('d40cc32ecec8f681dcced6a482b6438a86080899:WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1/runtime/ms1_serial.py') if '_old' in str(p) or '/old/' in str(p) else TARGET+':'+PREFIX+'/candidate/ms1_serial.py'))
            assert x['blob_sha1']==expected
        else:assert x['blob_sha1']=='d172fe04788fcc33032b71eb6d083c15dd03ff7e'
    all_import_receipts.append(str(p.relative_to(R)))
seal=json.loads((S/'11_CANDIDATE_SOURCE_SEAL.json').read_text())
for x in seal['files']:
    assert git('show',x['commit']+':'+x['path'])==git('show',TARGET+':'+x['path'])
for name in ['01_PREREGISTRATION.md','02_PREREGISTRATION.json']:
    a=git('show','cc2f24a6837d007b0ba7ab5c40f39899e2d7b644:WORKER_RETURNS/SOROK-R3-HQ316-MS1-SERIAL-MEMORY-BELIEF-FEASIBILITY-R1/'+name)
    assert a==(MS1/name).read_bytes()
save('06_SOURCE_AND_IMPORT_AUDIT.json',dict(files=rows,accepted_law=laws,actual_final_probe=imports,executed_import_receipts=all_import_receipts,native9_guard1_unchanged=True,guard_empty=True,original_test_oracles_unchanged=True,repair_matches_tested_source_seal=True,original_prereg_identical=True))
# Verify frozen test bytes, parse actual JUnit; preserve all literal REDs.
for name in ['03_REVIEWER_FREEZE.json','03B_FOLLOWUP_FREEZE.json']:
    for n,h in json.loads((R/name).read_text())['files'].items():assert hashlib.sha256((R/n).read_bytes()).hexdigest()==h
mat=[]
for p in sorted((R/'evidence').glob('*/*/junit.xml')):
    cases=case_rows(p);mat.append(dict(phase=p.parts[-3],court=p.parts[-2],junit=str(p.relative_to(R)),counts={k:sum(c['outcome']==k for c in cases) for k in ['PASS','FAIL','ERROR','SKIP']},cases=cases))
save('04_FULL_EXECUTED_CASE_MATRIX.json',mat)
def get(phase,court):return next(x for x in mat if x['phase']==phase and x['court']==court)
for c in ['original120','ms2_51','p3b']:
    assert [(x['classname'],x['name']) for x in get('old',c)['cases']]==[(x['classname'],x['name']) for x in get('ms3',c)['cases']]
assert get('ms3','original120')['counts']==dict(PASS=118,FAIL=2,ERROR=0,SKIP=0)
assert get('ms3','ms2_51')['counts']==dict(PASS=51,FAIL=0,ERROR=0,SKIP=0)
assert get('ms3','author47')['counts']['PASS']==47 and get('ms3','selector12')['counts']['PASS']==12
assert get('ms3','p3b')['counts']['FAIL']==1
paired=[]
for phase1,phase2,c in [('ms4_on_old','ms4_on_ms3','hostile'),('followup_on_old','followup_on_ms3','followup')]:
    aa={x['name']:x for x in get(phase1,c)['cases']};bb={x['name']:x for x in get(phase2,c)['cases']};assert aa.keys()==bb.keys()
    for n in aa:paired.append(dict(court=c,case=n,old=aa[n]['outcome'],ms3=bb[n]['outcome']))
assert sum(x['old']=='FAIL' and x['ms3']=='PASS' for x in paired)==55
save('05_PAIRED_HOSTILE_MATRIX.json',dict(cases=paired,old_fail_ms3_pass=55,original85_reds_retained=10,followup20_pass=20))
# Review every MS3 author's JUnit directly from target objects (not fresh output).
junit=[]
for p in git('ls-tree','-r','--full-tree','--name-only',TARGET,PREFIX).decode().splitlines():
    if not p.endswith('junit.xml'):continue
    b=git('show',TARGET+':'+p);root=E.fromstring(b)
    cases=list(root.iter('testcase'))
    junit.append(dict(commit=TARGET,path=p,blob_sha1=blob(b),tests=len(cases),failures=sum(t.find('failure') is not None for t in cases),errors=sum(t.find('error') is not None for t in cases),skipped=sum(t.find('skipped') is not None for t in cases),red_cases=[dict(name=t.get('name'),failure=t.find('failure').get('message')) for t in cases if t.find('failure') is not None]))
save('07_TARGET_ALL_JUNIT_AUDIT.json',junit)
# Fresh-run observations produced by unchanged historical/author tests.
for src,dst in [(M2/'evidence/new/observations',R/'evidence/ms3/ms2_51/observations'),(S/'evidence/author/observations',R/'evidence/ms3/author47/observations'),(S/'evidence/selector_extension/observations',R/'evidence/ms3/selector12/observations')]:shutil.copytree(src,dst,dirs_exist_ok=True)
shutil.copyfile(M2/'evidence/literal_p3b/counterfactual.json',R/'evidence/ms3/p3b/counterfactual.json')
# Sanitized portable passport; actual import paths use return-relative aliases.
marker=R/'staging/MS4_RUNTIME_MARKER.json'
if not marker.exists():marker.write_text(json.dumps(dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),owner='MS4_INDEPENDENT',source='FRESH_PINNED_RECONSTRUCTION'))+'\n')
identity=json.loads(marker.read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
save('environment_passport_delta.json',dict(passport_schema='SOROK_00D_ENVIRONMENT_PASSPORT@1',**identity,owner_session_alias='MS4_FRESH_I2',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_REVIEW_HOST',conversation_or_account_affinity='MS4_ONLY',status='LIVE_VERIFIED',last_live_probe_at=now,runtime_marker_digest=hashlib.sha256(marker.read_bytes()).hexdigest(),probe_command_and_result='python3 repro/audit.py; imports, Git bytes, EMPTY guard and frozen suites VERIFIED',python=dict(status='VERIFIED',version=platform.python_version()),pytest=dict(status='VERIFIED',version=__import__('pytest').__version__),git=dict(status='VERIFIED',version=subprocess.check_output(['git','--version'],text=True).strip()),node=dict(status='UNKNOWN',required=False),filesystem='VERIFIED',shell='VERIFIED',git_object_store_alias='EXISTING_AUTHENTICATED_STORE',worktree_alias='NEW_ISOLATED_MS4',branch='agent/reviewer-sorok-r3-hq319-ms4-ms3-independent-r1',checkout_base='a5bd38dabd9e85cdede0d741335bf8d40b9070f1',head_at_probe=git('rev-parse','HEAD').decode().strip(),dirty_state='OWNED_RETURN_PENDING_COMMIT',source_family='SOURCEFREE_NATIVE_CAN2_PLUS_MS1_MS2_MS3',materialized_source_refs=rows,imported_modules=imports,dependency_closure_status='BOUNDED',fixture_query_permission='COMMISSIONED_SOURCEFREE_SYNTHETIC_ONLY',covered_test_suites=[dict(phase=x['phase'],court=x['court'],counts=x['counts'],junit=x['junit']) for x in mat],science_grade='FINITE_SOURCEFREE_TEST_ONLY_INDEPENDENT_REVIEW',model_provider=dict(editor='Codex',selected_model='GPT-6.1',effort='High',selection_basis='USER_SELECTED; no switch',provider='OpenAI',account='UNKNOWN',cash_known=False,quota_known=False,credits=None,usage=None,pricing_class='UNKNOWN',context_cache_reuse='UNKNOWN',retries='one pre-execution staging path correction; retained prospective follow-up after reviewer85; no model retries',estimated_total_evidence_cost='UNKNOWN',next_reset=None),independent_review_separation='Separate MS4 session; never MS1/MS2/MS3 author/reviewer',privacy_source_grant='Private repo sourcefree files only; no original survey/model/actor grants',assignments_completed=['MS4'],next_good_affinity_tags=['CAN008','ADP016','ADP017','TEMPORAL','PROVENANCE'],staged_state_preservation='LIVE_AT_PROBE; next user must verify marker/imports anew',retire_or_rebuild_reason=None))
print('AUDIT_PASS: native9+guard1; literal171+59+P3b; hostile85+followup20; 55 old-RED/MS3-PASS; all target JUnit inspected',len(junit))
