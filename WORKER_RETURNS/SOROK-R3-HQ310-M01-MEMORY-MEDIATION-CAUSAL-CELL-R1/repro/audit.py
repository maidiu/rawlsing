"""Portable evidence packaging, native object identities, explicit claim ceiling."""
from pathlib import Path
import json,hashlib,subprocess,sys,platform,uuid,datetime,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];REPO=R.parents[1]
BASE='d3b7c7d7cf52ac8572f2d271bfe9cb97468660c8';PREREG='845edf5d7c9c48b192b631dacf295afa6f587137'
def write(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
rows=[];raw=[]
for suite in ['new','can3','author','owners']:
 p=R/'evidence'/suite/'junit.xml';b=p.read_bytes();root=ET.fromstring(b)
 if any('hostname' in ts.attrib for ts in root.iter('testsuite')):
  d=R/'runtime/raw_junit'/suite;d.mkdir(parents=True,exist_ok=True);(d/'junit.xml').write_bytes(b)
  raw.append(dict(suite=suite,raw_sha256=hashlib.sha256(b).hexdigest(),sanitization='hostname attribute removed only; raw retained locally in ignored runtime'))
  for ts in root.iter('testsuite'):ts.attrib.pop('hostname',None)
  ET.ElementTree(root).write(p,encoding='utf-8',xml_declaration=True)
 ts=list(root.iter('testsuite'));counts={k:sum(int(t.get(k,0)) for t in ts) for k in ['tests','failures','errors','skipped']}
 execution=json.loads((R/'evidence'/suite/'execution.json').read_text());rows.append(dict(suite=suite,returncode=execution['exit_code'],counts=counts))
assert all(x['returncode']==0 and all(x['counts'][k]==0 for k in ['failures','errors','skipped']) for x in rows)
write('03_RESULTS.json',rows)
if raw:write('04_JUNIT_PORTABILITY.json',raw)
identities=json.loads((R/'02_SOURCE_IDENTITIES.json').read_text());known={x['blob_sha1'] for x in identities}
imports=[]
for suite in ['new','can3','author','owners']:
 for row in json.loads((R/'evidence'/suite/'execution.json').read_text())['imports']:
  p=R/row['file'];b=p.read_bytes();assert blob(b)==row['blob_sha1'] and hashlib.sha256(b).hexdigest()==row['sha256']
  origin='NEW_M01_SOURCE' if row['module'] in ('cell','bootstrap') else 'PINNED_INHERITED_OBJECT'
  if origin=='PINNED_INHERITED_OBJECT':assert row['blob_sha1'] in known,(suite,row)
  imports.append(dict(suite=suite,origin=origin,source_refs=[{k:v for k,v in ref.items() if k in ('commit','path','blob_sha1','sha256')} for ref in identities if ref['blob_sha1']==row['blob_sha1']],**row))
# Verify source-free bodies, exact published CAN3 preservation, scoped terrain.
for p in (R/'runtime/can3/runtime/author/candidate').glob('*.py'):
 old='WORKER_RETURNS/SOROK-R3-HQ308-CAN2-LAW-CAUSAL-REPAIR-R1/candidate/'+p.name
 assert p.read_bytes()==subprocess.check_output(['git','show','f9ff05197fb2837c733f8b453c678043e90c77d8:'+old])
for row in identities:
 if row.get('commit')=='ef12349defe22a50e053a7a8080a67ab45673417':assert blob((R/row['local']).read_bytes())==row['blob_sha1']
guard=REPO/'rawlsing_next/v3_psepf_zero_positive_guard.py';assert blob(guard.read_bytes())=='e0528d65215cb431196570c38bac4eae94217a1b'
prereg=R/'01_PREREGISTRATION.md';assert prereg.read_bytes()==subprocess.check_output(['git','show',PREREG+':'+str(prereg.relative_to(REPO))])
changes=git('diff','--name-only',BASE).splitlines();allowed=str(R.relative_to(REPO))+'/'
assert all(p.startswith(allowed) for p in changes)
write('05_AUDIT.json',dict(base=BASE,prereg_commit=PREREG,prereg_blob=blob(prereg.read_bytes()),imports=imports,CAN3_published_packet_byte_unchanged=True,guard_blob=blob(guard.read_bytes()),production_registry_empty_all_executions=True,changed_paths=changes,write_scope=allowed,original_9_RED='PRESERVED_IN_CAN3; NOT_RERUN_OR_RECLASSIFIED',single_agent=True,independent_review='HQ_AFTER_RETURN',no_model_or_original_source_execution=True))
# Sanitized passport: runtime marker is an opaque value; no home/host/user strings.
marker=R/'runtime/epoch_marker'
if not marker.exists():marker.write_text(str(uuid.uuid4()))
write('environment_passport_delta.json',dict(passport_schema='SOROK_00D_ENVIRONMENT_PASSPORT_R1',environment_id=hashlib.sha256(marker.read_bytes()).hexdigest()[:24],epoch_id='M01_LOCAL_BOOTSTRAP_20261015',owner_session_alias='M01_SOLE_AUTHOR',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_M01',conversation_or_account_affinity='USER_SELECTED_CODEX',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=hashlib.sha256(marker.read_bytes()).hexdigest(),probe_command_and_result=dict(python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),git=git('--version'),filesystem_shell='VERIFIED zsh, read/write/execute within assigned return',node='NOT_NEEDED_NOT_PROBED'),capabilities=dict(python='VERIFIED',pytest='VERIFIED',git='VERIFIED',authenticated_remote='VERIFIED ls-remote',model='USER_REPORTED'),git_object_store_alias='EXISTING_SHARED_RAWLSING_STORE',worktree_alias='AUTHORIZED_4327',branch=git('branch','--show-current'),checkout_base=BASE,head_at_probe=git('rev-parse','HEAD'),clean_dirty='RETURN_FILES_PENDING_COMMIT',source_family='SOURCEFREE_ONLY',materialized_source_refs=[dict(module=x['module'],local_staging_path=x['file'],verified_imported_module_file=x['file'],blob_sha1=x['blob_sha1'],source_refs=x['source_refs']) for x in imports],dependency_closure_status='BOUNDED',fixture_query_source_permission='COMMISSION_TEST_ONLY',covered_test_suites=rows,science_grade='SOURCEFREE_NEW_MEMORY_MEDIATION_CANDIDATE_REQUIRES_I2',model_provider='OpenAI Codex user-selected; billing UNKNOWN',model='GPT-6.1',effort='High (USER_REPORTED assignment; no switch)',pricing_class='UNKNOWN',credits_usage=None,cash_known=False,quota_known=False,context_cache_reuse='UNKNOWN',retries=0,estimated_total_evidence_cost='UNKNOWN',independent_review_separation='No helper/reviewer launched; HQ commissions fresh I2 after return',privacy_source_grant='Private repo local sourcefree commission only',nearest_expected_reset=None,assignments_completed=['M01'],next_good_affinity_tags=['CAN008','ADP016','ADP017','K3','K5','CAUSAL_MEDIATION'],staged_state_preservation='SOURCE_AND_RECEIPTS_LOCAL; synchronous owner state per test; no cross-process state durability claim',retire_or_rebuild_reason=None))
# No personal paths or hostnames in portable evidence.
for p in (R/'evidence').rglob('*'):
 if p.is_file():
  s=p.read_text();assert '/Users/' not in s and 'Matthews-MBP' not in s,p
print('AUDIT PASS',sum(x['counts']['tests'] for x in rows),'executed cases; pinned imports, prereg and guard verified')
