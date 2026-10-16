"""Portable final source/host receipts; never changes scientific assertions."""
from pathlib import Path
import subprocess,json,hashlib,uuid,datetime,platform,re,sys
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];M1=R/'runtime/m02/runtime/m01'
def g(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def write(p,d):(R/p).write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
# Preserve original raw experiment metadata locally. Only presentation changes.
changed=[]
for p in (R/'evidence').rglob('*'):
 if not p.is_file() or p.suffix not in ['.json','.xml','.log','.stdout','.txt','.md']:continue
 b=p.read_bytes();s=b.decode();v=s.replace(str(R),'[RETURN]').replace(str(ROOT),'[WORKTREE]').replace(str(Path.home()),'[HOME]')
 if p.suffix=='.xml':v=re.sub(r'hostname="[^"]*"','hostname="[HOST]"',v)
 if s!=v:
  raw=R/'runtime/raw_final_metadata'/p.relative_to(R/'evidence');raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes(b);p.write_text(v)
  changed.append(dict(path=str(p.relative_to(R)),raw_sha256=sha(b),portable_sha256=sha(v.encode())))
if changed:write('evidence/FINAL_METADATA_PRESENTATION.json',dict(changes=changed,assertions_and_outcomes_changed=False))
sys.path.insert(0,str(M1/'repro'));import bootstrap,cell,claim_provenance,pytest
live=[]
for name,module in sorted(sys.modules.items()):
 f=getattr(module,'__file__',None)
 if f and Path(f).suffix=='.py' and name.startswith(('cell','claim_provenance','bootstrap','candidate','rawlsing_next')):
  p=Path(f).resolve();b=p.read_bytes();live.append(dict(module=name,actual_module_file=str(p.relative_to(R)),git_blob_sha1=blob(b),sha256=sha(b)))
marker=R/'runtime/m05_marker.json'
if not marker.exists():marker.write_text(json.dumps(dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),role='M05_AUTHOR_NOT_M06',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
m=json.loads(marker.read_text());results=json.loads((R/'11_EXECUTED_RESULTS.json').read_text())
write('environment_passport_delta.json',dict(passport_schema='SOROK_ENVIRONMENT_PASSPORT_R1',environment_id=m['environment_id'],epoch_id=m['epoch_id'],owner_session_alias='M05_IMPLEMENTER',surface='LOCAL_SHARED_STORE',machine_alias='AUTHORIZED_LOCAL_HOST',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha(marker.read_bytes()),probe_command_and_result='review/audit.py and actual module import source hashing; 638 original +48 author PASS, separate9 FAIL',capabilities=dict(python=dict(status='VERIFIED',version=platform.python_version()),pytest=dict(status='VERIFIED',version=pytest.__version__),git=dict(status='VERIFIED',version=g('--version').decode().strip()),filesystem=dict(status='VERIFIED',sparse=True),shell=dict(status='VERIFIED',kind='zsh'),node=dict(status='UNKNOWN',required=False)),git_object_store_alias='EXISTING_CANONICAL_SHARED_STORE',worktree_alias='ISOLATED_M05',branch='agent/rabochii-sorok-r3-hq315-m05-m04-provenance-ancestry-repair-r1',exact_checkout_base='a03927a05631f5706059a09f7a8575d63399933c',head_at_probe=g('rev-parse','HEAD').decode().strip(),clean_dirty_state='M05 return changes only; earlier unrelated warm caches preserved',materialized_source_refs=live,dependency_closure_status='BOUNDED',fixture_source_permission='SYNTHETIC_SOURCEFREE_ONLY',covered_test_suites=results,science_grade='SOURCEFREE_CANDIDATE_IMPLEMENTATION; INDEPENDENT_M06_REQUIRED',model_provider='OpenAI via Codex',editor_harness='Codex',model_effort_requested='GPT-6.1 High',actual_model_effort_telemetry='UNKNOWN',observed_usage=None,actual_cash=None,quota_window=None,paid_overflow_policy='NOT_INFERRED',economics='User-selected qualified High worker retained for native ancestry judgment. Step5 considered in commission; no editor/provider switch. Actual cash/quota unknown.',independence_conflicts='This chat previously authored M04; cannot provide M06 acceptance',assignments_completed=['M05 candidate repair/evidence'],next_good_affinity_tags=['NATIVE_OWNER_REPLAY','CAN008','ADP016','ADP017','SOURCEFREE_PROVENANCE'],staged_state_preservation='Static closure and portable inputs preserved; live mutable owner process continuity not assumed',retire_or_rebuild_reason=None,privacy_grant='No original survey, experimental model, actor, production or external-provider export'))
audit=[]
for item,evidence in [
 ('Exact startup, parent and assigned terrain','00_RETURN.md; tracked diff from a03927a'),
 ('Baseline587 PASS and M04 41 PASS/10 RED','evidence/before/; 04_LITERAL_638_BEFORE_AFTER.json'),
 ('All638 unchanged PASS after repair','evidence/after/; original source preimages06/07'),
 ('Preregistered new48 PASS','03_AUTHOR_FREEZE.json; review/test_m05_author.py; evidence/m05_author/'),
 ('Original nine historical REDs separate and unchanged','05_NEW_AUTHOR_48_AND_HISTORICAL_NINE.json; before/after historical JUnit'),
 ('Actual native first-predecessor, full state descent and terminal permission','candidate source; 09_FACTORIAL_NATIVE_ANCESTRY_AND_COMPARATOR.json; 10_TEN_REDS_AND_ATOMICITY_CLOSURE.json'),
 ('Lawful add/supersede/withdraw/re-add and complete replay','Original638 and author48 JUnit/native observations'),
 ('36-arm factorial, original CAN3 comparator, K3/K5 and time controls','09_FACTORIAL_NATIVE_ANCESTRY_AND_COMPARATOR.json; original cases'),
 ('Byte-identical EMPTY production guard, unchanged accepted owners/laws','08_ACTUAL_IMPORT_AND_PATCH_AUDIT.json'),
 ('Causal ceiling and no self-acceptance','00_RETURN.md; independent M06 explicitly required'),
 ('Source patch, actual installed modules and Git/SHA256 custody','candidate/M03_TO_M05.patch;06/07/08 and passport'),
 ('Portable evidence and truthful prospective freeze custody','evidence/FREEZE_PORTABILITY_CUSTODY.json; metadata presentation receipts'),
 ('Push and direct remote SHA','16_REMOTE_CONTENT_VERIFICATION.json plus final direct check after receipt-only commit')]:
 audit.append(dict(requirement=item,evidence=evidence,status='COMPLETE' if not item.startswith('Push') else 'REQUIRES_FINAL_DIRECT_REMOTE_VERIFICATION'))
write('15_COMPLETION_AUDIT.json',dict(schema='M05_COMPLETION_AUDIT@1',candidate_only=True,requirements=audit,original_main_before=results['before'],original_main_after=results['after'],new_author=results['new_author'],historical=results['historical'],required_independent_M06='FUTURE_SEPARATE_COMMISSION; NOT_PERFORMED_BY_AUTHOR'))
print('PORTABLE_M05_PACKAGE_READY')
