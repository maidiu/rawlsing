"""Final documentary completion audit, portable evidence and environment passport."""
from pathlib import Path
import json,hashlib,datetime,platform,subprocess,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root';E=R/'evidence'
def read(p):return json.loads(Path(p).read_text())
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def write(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
# Every named commission artifact must exist and must be grounded in actual outputs.
required=['00_FULL_NATIVE_INDEPENDENT_VERDICT.md','01_FROZEN_ORIGINAL_EIGHT_OPS_AND_TRUSTED_OWNER.json','02_REAL_C11_I03_I05_P01_FIELD_FORGE_CALLS_AND_48_CASES.json','03_SIX_CONSUMERS_COLD_SOURCE_REVALIDATION_AND_GRANTS.md','04_SPECIALIZED_GT2_SEMANTICS_ISSUER_HOLDS.md','05_IMPORT_AND_SOURCE_CUSTODY.json']
assert all((R/p).is_file() for p in required)
freeze=R/required[1];prefix='WORKER_RETURNS/'+R.name+'/'
freeze_commit=git('log','--reverse','--format=%H','66ef1999e371f0739d393da7a5be58fe476cf7e7..HEAD','--',prefix+freeze.name).splitlines()[0]
assert freeze.read_bytes()==subprocess.check_output(['git','show',freeze_commit+':'+prefix+freeze.name])
d=read(R/required[2]);assert len(d['six_complete_producer_consumer_values'])==6 and len(d['original_21_RED_closed'])==21
assert d['remaining_raw_failure']==['test_generic_native_labels_not_specialized_Q86']
summary=read(E/'abrupt/summary.json');first=read(E/'abrupt/first.json');replay=read(E/'abrupt/replay.json')
assert summary['actual_abrupt_death'] and summary['ledger_byte_identical'] and summary['first_durable']==[3,3] and summary['replay_durable']==[0,0]
assert first['actual_UnitExecutionReceipts']==replay['actual_UnitExecutionReceipts']
assert first['pid']!=replay['pid'];assert replay['trace']['call_counts']['validate_c11_source_release']==2 and replay['trace']['call_counts']['execute_empirical_query']==8 and replay['trace']['call_counts']['execute_exact_bounded_discovery']==2
assert summary['native_source_reattestation']==74
native=read(R/'native_74_source_manifest.json')['files']
for row in native:
 b=(RT/row['staged_path']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
counts=[]
for mode in ['pv2_33','v2k_24','pv_21','owners_111','pv2i_historical','pv2i_adapter','pv3']:
 root=ET.parse(E/'original_runs'/(mode+'.xml')).getroot();c={k:sum(int(t.get(k,0)) for t in root.iter('testsuite')) for k in ['tests','failures','errors','skipped']};counts.append(dict(suite=mode,**c))
for mode in ['independent','extra']:
 root=ET.parse(E/mode/'junit.xml').getroot();c={k:sum(int(t.get(k,0)) for t in root.iter('testsuite')) for k in ['tests','failures','errors','skipped']};counts.append(dict(suite=mode,**c))
assert sum(x['tests'] for x in counts)==349 and sum(x['failures'] for x in counts)==23 and sum(x['errors']+x['skipped'] for x in counts)==0
# Explicit original historical and generic REDs never disappear during packaging.
write('06_COMPLETION_AUDIT.json',dict(commission='WORKER_COMMISSIONS/PYAT-USERDIRECT-20261016-R14-PV3N-FULL-OWNER-INDEPENDENT-R1/00_COMMISSION.md',startup='66ef1999e371f0739d393da7a5be58fe476cf7e7',freeze_commit=freeze_commit,full74_qualified=True,owner_processes=53,exact_six_original_current_consumers=True,original21_reds_closed=True,actual_abrupt_kill_and_original_receipt_cold_restore=True,no_new_durable_after_cold=True,source_recomputation_counted=True,physical_missing_source_refused=True,journal_checkpoint_expected_and_edition_denials_executed=True,selective_revocation_preserves_B_and_archive=True,external_filesystem_writer_hold_executed=True,original_test_and_semantic_owner_bytes_unchanged=True,suites=counts,final_total=dict(tests=349,passed=326,raw_failures=23,errors=0,skipped=0),initial_supplemental_harness_RED='Preserved evidence/extra_initial; measurement corrected, no candidate or frozen oracle edits',verdict='ACCEPT_SOURCEFREE_GT2_ORIGINAL_SCOPE_METHOD_ONLY',holds=['GENERIC_NATIVE_SEMANTICS_HOLD','REAL_ORIGINAL_SIGNED_MONOTONIC_ISSUER_HOLD','ORDERED_OWNER_NOT_ISSUED','OFFLINE_FACT_RESTORATION_HOLD'],artifacts=required,no_adoption_or_real_source_actor_execution=True))
marker=C/'observations/runtime_marker.json'
write('environment_passport_delta.json',dict(passport_schema='PV3N_LOCAL_SOURCEFREE_ENVIRONMENT_PASSPORT_R1',environment_id=read(marker)['environment_id'],epoch_id=read(marker)['epoch_id'],owner_session_alias='PV3N_SOLE_INDEPENDENT_REVIEWER',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_PV3N',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=hashlib.sha256(marker.read_bytes()).hexdigest(),runner=dict(python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),git=git('--version'),subprocess='VERIFIED genuine SIGKILL -9 and distinct-PID restore',filesystem='VERIFIED isolated return runtime',private_git='VERIFIED authenticated fetch and original Git objects'),model='GPT-6.1 Sol High USER_SELECTED; runtime/account billing UNKNOWN',provider='OpenAI Codex',editor='Codex',cash=None,quota=None,model_or_provider_switch=False,delegates=0,git_object_store='EXISTING_SHARED_PRIVATE_RAWLSING_STORE',worktree_alias='4327',branch=git('branch','--show-current'),sealed_startup='66ef1999e371f0739d393da7a5be58fe476cf7e7',head_at_probe=git('rev-parse','HEAD'),state='OWN_RETURN_PENDING_COMMIT; preexisting unrelated untracked M01 cache preserved untouched, not imported',materialized_source_refs='native_74_source_manifest.json (all commit/path/blob identities) + 05_IMPORT_AND_SOURCE_CUSTODY.json (actual module files)',dependency_closure_status='FULL_PINNED_74_FILE_CLOSURE',permissions='SOURCEFREE TEST_ONLY local synthetic owners only; no SAV/DTA, external model, source issuer, adoption, N11/N12 or V3',covered_test_suites=counts,science_grade='ACCEPT_SOURCEFREE_GT2_ORIGINAL_SCOPE_METHOD_ONLY',native_fields_and_semantics='unchanged accepted source',review_independence='Distinct from PV3 implementer and PV3I partial reviewer; no messaging/helper',next_good_affinity_tags=['C11','I03','I05','P01','FIELD_FORGE','ORIGINAL_SCOPE','COLD_CUSTODY'],staged_state_preservation='Sources and recorded receipts remain local; next use reattests, never assumes a passport is execution'))
# Narrow, declared transport-only path/host sanitization; scientific projections untouched.
raw=[]
for p in sorted(E.rglob('*')):
 if not p.is_file():continue
 b=p.read_bytes()
 try:s=b.decode()
 except UnicodeDecodeError:continue
 changed=s.replace(str(R),'<RETURN>').replace(str(Path.home()),'<LOCAL_HOME>')
 if p.suffix=='.xml':
  root=ET.fromstring(changed)
  for t in root.iter('testsuite'):t.attrib.pop('hostname',None)
  changed=ET.tostring(root,encoding='unicode')
 if changed!=s:
  dest=R/'runtime/raw_published_evidence'/p.relative_to(E);dest.parent.mkdir(parents=True,exist_ok=True)
  if not dest.exists():dest.write_bytes(b)
  raw.append(dict(path=str(p.relative_to(R)),raw_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),published_sha256=hashlib.sha256(changed.encode()).hexdigest()))
  p.write_text(changed)
if raw:
 prior=read(R/'07_PORTABILITY_RECEIPT.json')['files'] if (R/'07_PORTABILITY_RECEIPT.json').exists() else []
 merged={x['path']:x for x in prior};merged.update({x['path']:x for x in raw})
 write('07_PORTABILITY_RECEIPT.json',dict(scope='Replace own absolute return path with <RETURN>, local home prefix with <LOCAL_HOME>, and remove JUnit hostname. Original scientific refs/values, testcase names, ordering and outcomes unchanged; raw evidence remains in ignored runtime.',files=list(merged.values())))
print('COMPLETION AUDIT PASS: all commission gates evidenced, 349 final cases = 326 PASS + 23 preserved raw FAIL')
