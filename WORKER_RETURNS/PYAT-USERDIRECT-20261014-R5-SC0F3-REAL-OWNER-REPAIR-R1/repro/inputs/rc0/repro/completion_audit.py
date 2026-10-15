"""Verify commissioned evidence, not candidate GREEN. Publication is separate."""
import pathlib,json,hashlib,collections,xml.etree.ElementTree as E,subprocess
RET=pathlib.Path(__file__).resolve().parents[1];ROOT=RET.parents[1];RT=RET/'runtime_root'
assert subprocess.check_output(['git','-C',str(ROOT),'branch','--show-current']).decode().strip()=='agent/reviewer-sorok-r3-hq299-rc0-sc0-pe-independent-r1'
start='e140beff621d91ca1092728badf00e538046e3b6'
assert subprocess.check_output(['git','-C',str(ROOT),'rev-parse',start+'^']).decode().strip()=='5c59fb409d5f08312c19b936738eb4410dbd4f26'
assert hashlib.sha256((RET/'01_FROZEN_INDEPENDENT_EXPECTATIONS.json').read_bytes()).hexdigest()=='c9abb1c6fae3d32d7c0f725b107e9fb9169782785ac3ea36bfd40c0278413492'
result=json.loads((RET/'02_EXECUTION_PER_CASE.json').read_text())['results']
for name,count in [('k9',8),('k10',28),('n10e_c1',56),('pe',21)]:assert len(result[name])==count and all(r['status']=='PASS' for r in result[name])
assert collections.Counter(r['status'] for r in result['hq297'])=={'PASS':4,'RED':9}
assert collections.Counter(r['status'] for r in result['independent'])=={'PASS':13,'RED':12}
for n in ['smoke','k9','k10','n10e_c1','pe','hq297','independent']:
 t=E.parse(RET/'repro'/f'{n}.xml').getroot()
 assert sum(int(s.attrib.get('skipped',0)) for s in t.iter('testsuite'))==0
 assert sum(int(s.attrib.get('errors',0)) for s in t.iter('testsuite'))==0
assert len(json.loads((RET/'03_NINE_PE_REDS_ADJUDICATED.json').read_text())['cases'])==9
assert len(json.loads((RET/'04_FROZEN_CASE_COVERAGE.json').read_text())['cases'])==36
assert len(json.loads((RET/'05_OWNER_ACTION_REGISTER.json').read_text())['actions'])==8
selector=json.loads((RET/'source_selector.json').read_text());assert len(selector['files'])==61
for row in selector['files']:
 raw=(RT/row['staging_path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==row['git_blob_sha1']
assert sum(r['family']=='original_27_selector' for r in selector['files'])==27
assert (RT/'independent/test_rc0_hostile.py').read_bytes()==(RET/'reviewer_tests/test_rc0_hostile.py').read_bytes()
connection=json.loads((RET/'repro/connection_probe.json').read_text());assert connection['port_providers_traced']==['ProviderA','ProviderB'] and not connection['port_producer_calls']
assert any(x['module']=='C1' and x['function']=='compose_positioned_subject_possibility' and x['calls']>0 for x in connection['PE_positive_control_calls'])
passport=json.loads((RET/'environment_passport_delta.json').read_text());assert passport['status']=='LIVE_VERIFIED'
encoded=json.dumps(passport);assert '/Users/' not in encoded and '/home/' not in encoded and 'matthew' not in encoded.lower()
marker=(RT/'rc0_runtime_marker.json').read_bytes();assert hashlib.sha256(marker).hexdigest()==passport['runtime_marker_digest']
requirements=[('Exact startup, full commission and Sorok 00C/00D/read band','repro/read_receipt_and_remote_cut.json'),('Independent governed worktree/new epoch/local Python and actual imports','environment_passport_delta.json; repro/live_environment_probe.json'),('Frozen independent matrix before local observation','01_FROZEN_INDEPENDENT_EXPECTATIONS.json; exact digest asserted'),('Genuine 27 blob refs plus transitive source custody, NUL and __file__','source_selector.json; repro/source_custody_summary.json; import_audits'),('Early A/B swap and one actual structural hostile','repro/smoke.xml:2PASS'),('K9 8, K10 28, N10E43+C1 13, PE21, HQ29713 all executed','02_EXECUTION_PER_CASE.json; all exact stdout/JUnit'),('All nine PE REDs independently scientifically adjudicated','03_NINE_PE_REDS_ADJUDICATED.json:1code/5dependencies/3expectationproblems; none hidden'),('Forged reversal, clocks, H1-H3/F1-F2/currentness, denied use and true values read','reviewer_tests/test_rc0_hostile.py; 13PASS/12RED; observations; scoped negatives retained'),('Do not trust author expected class or replace named tests by helper counts','04_FROZEN_CASE_COVERAGE.json; actual schema12negative/probe tests; source-aware not blind'),('Independent verdict/conflict/register/owner action/no adoption','00_RETURN.md; 05_OWNER_ACTION_REGISTER.json'),('Sourcefree port distinguished from operative N9/N10W/actor/original science','00_RETURN.md; passport permissions; zero experimental model/original-source/V3 calls'),('Portable sanitized passport and warm-affinity update','environment_passport_delta.json; local ignored capsule preserved'),('Executable reproduction bundle/minimal commands/full failures/paths','repro/stage.py/run.py/reproduce.sh; all logs/JUnit; changed_paths.txt'),('Only own return, no accepted owner/CURRENT/canonical changes','Publication path audit; original 61 blobs unchanged'),('Assigned branch push plus direct full remote SHA and ancestry','FINAL_EXTERNAL_READBACK_REQUIRED; cannot self-reference future commit')]
(RET/'06_REQUIREMENT_AUDIT.json').write_text(json.dumps(dict(schema='RC0_COMMISSION_COMPLETION_AUDIT@1',court_completed_with_scientific_verdict='CHANGES_REQUIRED',requirements=[dict(requirement=a,evidence=b,status='EVIDENCE_VERIFIED' if i<len(requirements)-1 else 'FINAL_PUBLICATION_EXTERNAL_READBACK_REQUIRED') for i,(a,b) in enumerate(requirements)],candidate_acceptance='NOT_GRANTED',adoption=False),indent=2)+'\n')
print('RC0_REQUIRED_COURT_EVIDENCE_VERIFIED; SCIENTIFIC_CHANGES_REQUIRED; FINAL_PUBLICATION_PENDING')
