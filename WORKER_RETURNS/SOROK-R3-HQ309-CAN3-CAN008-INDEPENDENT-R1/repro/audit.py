"""Verify independent evidence, sanitize host paths, and create portable custody."""
from pathlib import Path
import subprocess,sys,json,hashlib,uuid,platform,datetime,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];ROOT=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip());SEAL='4605c939cba25addc5b888f07a33218891c0cd52'
def run(*args):return subprocess.check_output(args,text=True).strip()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def put(name,data):(R/name).write_text(json.dumps(data,indent=2)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
# Logs retain full diagnostics with portable root labels; no personal host paths.
for f in (R/'evidence').rglob('*'):
 if not f.is_file() or f.suffix not in ('.log','.json','.xml'):continue
 text=f.read_text().replace(str(ROOT),'<WORKTREE>').replace(str(Path.home()),'<HOST_HOME>')
 if f.suffix=='.xml':
  root=ET.fromstring(text)
  for e in root.iter():
   if 'hostname' in e.attrib:e.set('hostname','LOCAL_REVIEW_HOST')
  text=ET.tostring(root,encoding='unicode')
 # Normalize diagnostic trailing whitespace after host-path sanitization.
 text='\n'.join(line.rstrip() for line in text.splitlines())+'\n'
 f.write_text(text)
rows=[];cases=[]
for suite in ('owners','rsm','candidate','rcp3','author','independent'):
 out=R/'evidence'/suite;root=ET.parse(out/'junit.xml').getroot();ts=list(root.iter('testsuite'))
 counts={k:sum(int(t.get(k,0)) for t in ts) for k in ('tests','failures','errors','skipped')};assert not counts['errors'] and not counts['skipped']
 rows.append(dict(suite=suite,exit_code=1 if counts['failures'] else 0,counts=counts))
 for c in root.iter('testcase'):
  fail=c.find('failure');cases.append(dict(suite=suite,classname=c.get('classname'),name=c.get('name'),result='RED' if fail is not None else 'PASS',failure=fail.get('message') if fail is not None else None))
assert [(r['counts']['tests'],r['counts']['failures']) for r in rows]==[(220,0),(60,0),(37,8),(82,1),(89,0),(97,0)]
put('02_RESULTS.json',rows);put('08_CASE_MATRIX.json',cases)
# Verify immutable test oracles against their original producing commits.
A=R/'runtime/author';custody=[]
refs=[('a11982e6cf135a8ecc72b6152ec796b4a4707093','WORKER_RETURNS/SOROK-R3-HQ303-RCP3-CAN008-COMPLETION-COURT-R1/repro/test_independent.py',A/'runtime_root/court_repaired/repro/test_independent.py'),('a11982e6cf135a8ecc72b6152ec796b4a4707093','WORKER_RETURNS/SOROK-R3-HQ303-RCP3-CAN008-COMPLETION-COURT-R1/repro/causal_probe.py',A/'runtime_root/court_repaired/repro/causal_probe.py'),('ee6a48b40247b113c614fe2099d4c443e8dd7bb7','WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/repro/test_repair.py',A/'repro/test_repair.py')]
for commit,path,local in refs:
 b=subprocess.check_output(['git','show',commit+':'+path]);assert b==local.read_bytes();custody.append(dict(commit=commit,path=path,blob_sha1=blob(b),local=str(local.relative_to(R)),byte_unchanged=True))
for row in json.loads((R/'01_SOURCE_RECEIPTS.json').read_text()):
 if '/tests/test_' in row['path'] or row['path'].endswith(('test_hq300_court.py','test_owner_effect_court.py')):custody.append(dict(**row,byte_unchanged=True))
authorities=[]
for name,ref in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('CAN008_R2_ADOPTION','a6bc1555489271e1adb2271ed02d46bb7f888170'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:
 b=subprocess.check_output(['git','cat-file','blob',ref]);assert blob(b)==ref;authorities.append(dict(authority=name,blob_sha1=ref,sha256=hashlib.sha256(b).hexdigest()))
reads=[]
for path in ['SOROK_PRODUCT_CONTROL_ROOM/00_READ_ME_FIRST.md','SOROK_PRODUCT_CONTROL_ROOM/00B_HQ_COMMUNICATIVE_DISCIPLINE_AND_FEASIBILITY_CLAIM_CONSTITUTION_R1.md','SOROK_PRODUCT_CONTROL_ROOM/00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md','SOROK_PRODUCT_CONTROL_ROOM/00D_WARM_ENVIRONMENT_PASSPORT_AND_COST_AWARE_AGENT_DISPENSATION_R1.md','SOROK_PRODUCT_CONTROL_ROOM/HQ309_OUT4_CAN2_OC2_RETURN_FANIN_AND_INDEPENDENT_REVIEW_DISPATCH_R1.md']:
 parent='7dd4e05990eba8069aa02504777ddd3173524c01';b=subprocess.check_output(['git','show',parent+':'+path]);assert b==(ROOT/path).read_bytes();reads.append(dict(commit=parent,path=path,blob_sha1=blob(b)))
put('05_AUTHORITY_AND_TEST_CUSTODY.json',dict(authorities=authorities,governing_reads=reads,test_custody=custody,prereg_sha256=hashlib.sha256((R/'00_PREREG.json').read_bytes()).hexdigest(),independent_oracles_changed=False))
# Workspace guard as well as each actually imported guard was verified.
gp=ROOT/'rawlsing_next/v3_psepf_zero_positive_guard.py';gb=gp.read_bytes();assert blob(gb)=='e0528d65215cb431196570c38bac4eae94217a1b';assert gb==subprocess.check_output(['git','show',SEAL+':rawlsing_next/v3_psepf_zero_positive_guard.py'])
receipts=[]
for suite in ('owners','rsm','candidate','rcp3','author','independent'):
 e=json.loads((R/'evidence'/suite/'execution.json').read_text());assert e['guard_empty'] and e['guard_byte_unchanged'];receipts.append('evidence/'+suite+'/execution.json')
put('09_GUARD_AND_EXECUTION_AUDIT.json',dict(verdict='REVIEW_PASS_SOURCEFREE_FINITE_HISTORY_CANDIDATE',final_cases=585,pass_count=576,historical_reds=9,guard_blob=blob(gb),workspace_byte_unchanged_from_seal=True,registry='EMPTY_IMMUTABLE_MAPPINGPROXY',per_process_runtime_guard_checks=receipts,claims_not_executed=['production owner registration','original survey data','real model/provider calls','V3 actor/runtime operation','semantic issuance/adoption','general ADP016/017 mediation','distributed crash/concurrency semantics'],independent_session=True,helpers=0,model_switches=0))
marker=R/'runtime/.can3_runtime_marker'
if not marker.exists():marker.write_text(str(uuid.uuid4()))
env_id=hashlib.sha256(marker.read_bytes()).hexdigest()
remote_review=run('git','ls-remote','origin','refs/heads/agent/reviewer-sorok-r3-hq309-can3-can008-independent-r1')
remote_source=run('git','ls-remote','origin','refs/heads/agent/rabochii-sorok-r3-hq308-can2-can008-law-causal-repair-r1');assert remote_source.split()[0]=='ee6a48b40247b113c614fe2099d4c443e8dd7bb7'
put('10_PREPUSH_REMOTE_CUSTODY.json',dict(observed_at_utc=now,startup_direct_ref_verified_at_launch=SEAL,review_branch_direct_result=remote_review,candidate_branch_direct_result=remote_source,source_exact=True,branch=run('git','branch','--show-current')))
import pytest
put('environment_passport_delta.json',dict(passport_schema='SOROK_00D_R1',environment_id=env_id[:24],epoch_id='CAN3_FRESH_INDEPENDENT_R1',owner_session_alias='CAN3_SOLE_REVIEWER',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_REVIEW_HOST',conversation_or_account_affinity='FRESH_CAN3_CHAT; independent of RCP3/CAN2',status='LIVE_VERIFIED',last_live_probe_at=now,runtime_marker_digest=env_id,probe_command_and_result='python3 repro/stage.py; python3 repro/run.py; exact 585-case court reproduced after removing own ignored runtime',capabilities=dict(python='VERIFIED '+platform.python_version(),pytest='VERIFIED '+pytest.__version__,git='VERIFIED '+run('git','--version'),subprocess='VERIFIED',filesystem_shell='VERIFIED',github_authenticated_remote_read='VERIFIED',node='UNKNOWN_NOT_REQUIRED'),git_object_store_alias='EXISTING_REPOSITORY_SHARED_STORE',worktree_alias='ASSIGNED_ISOLATED_CAN3',branch=run('git','branch','--show-current'),exact_checkout_base=SEAL,checkout_head_at_probe=run('git','rev-parse','HEAD'),worktree_state='DIRTY_ONLY_ASSIGNED_REVIEW_RETURN_BEFORE_COMMIT',source_family='PINNED_CAN008_ADP016_ADP017_SOURCEFREE',materialized_source_refs='01_SOURCE_RECEIPTS.json',verified_imported_module_files=receipts,dependency_closure_status='BOUNDED_REQUIRED_64_OBJECT_CLOSURE_PLUS_6_REPAIRED_MODULES',fixture_query_permission='COMMISSION_SOURCEFREE_TEST_ONLY',covered_test_suites=rows,science_grade='INDEPENDENT_SOURCEFREE_FINITE_HISTORY_REVIEW; not accepted owner/actor operation',model_provider='OpenAI/Codex per commission; underlying account telemetry UNKNOWN',user_selected_editor_model_pair='Codex + GPT-6.1 High (commission/user-reported)',effort='High (commission/user-selected)',pricing_class='UNKNOWN',observed_credits_usage=None,cash_known=False,quota_known=False,context_cache_reuse='UNKNOWN',retry_history='Local staging correction and documented independent test-hypothesis corrections; no provider retries measured',independent_review_separation='Fresh sole reviewer; no author chat contact or helper',privacy_source_grant='Private repo sourcefree test closure under commission; no outside provider export',nearest_expected_slot_reset=None,assignments_completed=['CAN3 full independent review'],next_good_affinity_tags=['CAN008','HISTORY_CAUSALITY','ADP016_ADP017_BOUNDARIES'],staged_state_preservation='RECONSTRUCTED_FROM_NATIVE_GIT; fresh marker live at return; next session must probe again',session_available_for_more_work='UNKNOWN_AFTER_RETURN; no persistence asserted',retire_or_rebuild_reason=None))
# Digest all portable artifacts except the digest list itself and separately added remote receipt.
files={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.rglob('*')) if p.is_file() and 'runtime' not in p.relative_to(R).parts and '__pycache__' not in p.relative_to(R).parts and '.pytest_cache' not in p.relative_to(R).parts and p.name not in ('artifact_manifest.json','11_REMOTE_VERIFICATION.json')}
put('artifact_manifest.json',dict(schema='CAN3_PORTABLE_ARTIFACT_SHA256@1',files=files,excluded=['runtime/ ignored reconstructible sources','11_REMOTE_VERIFICATION.json attests evidence commit separately','artifact_manifest.json self'],result='576 PASS / 9 retained historical RED / 585 final cases',no_adoption=True))
print('Evidence verified: 585 cases, 9 historical RED, empty byte-identical guard; portable manifest created')
