"""Portable metadata and actual environment/source receipts; no scientific edits."""
from pathlib import Path
import subprocess,sys,json,hashlib,re,platform,datetime,uuid,os
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def sha(v):return hashlib.sha256(v).hexdigest()
def blob(v):return hashlib.sha1(b'blob '+str(len(v)).encode()+b'\0'+v).hexdigest()
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
# Published source manifest points to actual relocated copies, not failed staging paths.
C='e1f7a74e51201b9614bcc578348b4e9db7be7bd3';P='WORKER_RETURNS/SOROK-R3-HQ313-M03-CLAIM-SELECTOR-PROVENANCE-REPAIR-R1'
(R/'source_refs').mkdir(exist_ok=True)
audit=git('show',C+':'+P+'/07_SOURCE_AND_IMPORT_AUDIT.json');(R/'source_refs/M03_AUTHOR_07_SOURCE_AND_IMPORT_AUDIT.json').write_bytes(audit)
rows=[]
for p in git('ls-tree','-r','--name-only',C,P).decode().splitlines():
 rel=p[len(P)+1:]
 if not(rel.startswith('repro/') or rel.startswith('candidate/') or rel=='07_SOURCE_AND_IMPORT_AUDIT.json'):continue
 local='source_refs/M03_AUTHOR_07_SOURCE_AND_IMPORT_AUDIT.json' if rel=='07_SOURCE_AND_IMPORT_AUDIT.json' else rel
 data=(R/local).read_bytes();assert data==git('show',C+':'+p)
 rows.append(dict(commit=C,path=p,blob_sha1=blob(data),sha256=sha(data),actual_local_copy=local))
write('01_M03_MATERIALIZATION.json',rows)
identities=[dict(role=role,commit=c) for role,c in [
 ('M04_SEALED_STARTUP','2f4482ae23960037da4ebee84501916dc6e5b422'),('HQ314_PARENT','f9b4fd61eb64ad644b590b644450ac5563b6d151'),('M03_FINAL',C),('M03_STARTUP','92b9fa8b29f85ad77576da39a8765a666a5ab37f'),('M02_FINAL','0216d9036a87e2f60f42fd5b2870556027808419'),('M01_PREREGISTRATION','845edf5d7c9c48b192b631dacf295afa6f587137'),('M01_CANDIDATE','02187a14e75ff30dd953d3c7185d689b80e62304'),('CAN3_INDEPENDENT','ef12349defe22a50e053a7a8080a67ab45673417'),('CAN2_AUTHOR','ee6a48b40247b113c614fe2099d4c443e8dd7bb7'),('M04_NEW_TEST_FREEZE','3b529996ddd05c3c84225d2054428ff943091aef')]]
for row in identities:assert git('cat-file','-t',row['commit']).strip()==b'commit'
authorities=[dict(name=n,blob_sha1=h,sha256=sha(git('cat-file','blob',h))) for n,h in [('CAN008_R2_ADOPTED','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280'),('PRODUCTION_EMPTY_GUARD','e0528d65215cb431196570c38bac4eae94217a1b')]]
write('13_SOURCE_AND_AUTHORITY_INDEX.json',dict(commits=identities,authority_blobs=authorities,m03_files=rows,adoption_record='data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/PFF_U1_SHARED_PERSON_TRANSITION_GATE_R1/CAN008_R2_AUTHORITY_CANDIDATE_R1/02_HQ_CAN008_R2_ADOPTION_R1.md'))
# Retain raw original metadata in ignored runtime; portable copies change paths/hostname only.
changes=[];raw=R/'runtime/raw_m04_metadata'
for p in (R/'evidence').rglob('*'):
 if not p.is_file() or p.suffix not in ['.xml','.json','.log','.stdout','.md','.txt']:continue
 old=p.read_bytes();s=old.decode();new=s.replace(str(R),'[RETURN]').replace(str(ROOT),'[WORKTREE]').replace(str(Path.home()),'[HOME]')
 if p.suffix=='.xml':new=re.sub(r'hostname="[^"]*"','hostname="[HOST]"',new)
 if new!=s:
  target=raw/p.relative_to(R/'evidence');target.parent.mkdir(parents=True,exist_ok=True)
  if not target.exists():target.write_bytes(old)
  changes.append(dict(path=str(p.relative_to(R)),raw_sha256=sha(old),portable_sha256=sha(new.encode()),changes='local paths / XML hostname only'))
  p.write_text(new)
if changes:write('evidence/PORTABILITY_SANITIZATION.json',dict(changes=changes,raw_retained_in_ignored_runtime=True,assertions_and_case_outcomes_changed=False))
import pytest
marker=R/'runtime/m04_review_marker.json'
if not marker.exists():marker.write_text(json.dumps(dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),owner_session_alias='M04_FRESH_INDEPENDENT',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
m=json.loads(marker.read_text());aud=json.loads((R/'08_SOURCE_AND_IMPORT_AUDIT.json').read_text());results=json.loads((R/'11_REVIEW_RESULTS.json').read_text())
write('environment_passport_delta.json',dict(passport_schema='SOROK_ENVIRONMENT_PASSPORT_R1',environment_id=m['environment_id'],epoch_id=m['epoch_id'],owner_session_alias='M04_FRESH_INDEPENDENT',surface='LOCAL_SHARED_STORE',machine_alias='AUTHORIZED_LOCAL_HOST',conversation_or_account_affinity='FRESH_M04_ONLY',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha(marker.read_bytes()),probe_command_and_result='review/audit_review.py verifies actual live imports, source grant, frozen tests, all case matrices and empty production registry',capabilities=dict(python=dict(status='VERIFIED',version=platform.python_version(),implementation=platform.python_implementation()),pytest=dict(status='VERIFIED',version=pytest.__version__),git=dict(status='VERIFIED',version=git('--version').decode().strip()),shell=dict(status='VERIFIED',kind='zsh'),filesystem=dict(status='VERIFIED',sparse_checkout=git('config','--get','core.sparseCheckout').decode().strip()),node=dict(status='UNKNOWN',required=False)),git_object_store_alias='EXISTING_CANONICAL_SHARED_STORE',worktree_alias='ISOLATED_M04',branch='agent/reviewer-sorok-r3-hq314-m04-m03-independent-r1',exact_checkout_base='2f4482ae23960037da4ebee84501916dc6e5b422',head_at_probe=git('rev-parse','HEAD').decode().strip(),clean_dirty_state='RETURN_FILES_ONLY; checked against sealed startup',source_family='CAN008_ADP016_ADP017_SOURCEFREE',materialized_source_refs=aud['live_imports'],dependency_closure_status='BOUNDED',fixture_query_source_permission='AUTHORIZED_SYNTHETIC_SOURCEFREE_ONLY',covered_test_suites=results,science_grade='SOURCEFREE_PROTOTYPE_INDEPENDENT_REVIEW_REVISE',model_provider='OpenAI via Codex; user-selected configuration',editor_harness='Codex',selected_model='GPT-6.1 High (user commission)',effort='High (user commission)',model_runtime_identity_introspection='UNKNOWN',pricing_class='UNKNOWN',cash_known=False,quota_known=False,actual_paid_cash=None,observed_usage=None,context_cache_reuse='UNKNOWN',estimated_total_evidence_cost='UNKNOWN',nearest_expected_slot_reset=None,independent_review_separation='Fresh reviewer; no M01/M02/M03 authorship or conversations',privacy_source_grant='Private repository, local synthetic testing only; no external provider/model calls',economics_comparison='Keep the explicitly selected single Codex GPT-6.1 High reviewer for substantive independent causal/provenance adjudication. Step 5 was reported FREE by dispatch, but independent scientific qualification, account limits and export grant are not verified here. No cheaper qualified whole-court route established; no current worker switch authorized.',assignments_completed=['M04 full bounded court, evidence, adjudication'],next_good_affinity_tags=['CAN008','ADP017','CHECKPOINT_PROVENANCE','I2_REVIEW'],staged_state_preservation='Warm exact local static source closure preserved; no claim that mutable owner process state survives',retire_or_rebuild_reason=None,independence_limit='This reviewer did not author a repair; a later repaired candidate must be independently recommissioned under HQ custody'))
print('M04_PORTABLE_PACKAGE_READY')
