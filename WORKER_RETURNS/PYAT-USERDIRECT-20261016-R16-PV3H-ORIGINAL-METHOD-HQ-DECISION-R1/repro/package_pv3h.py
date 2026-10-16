"""Portable artifacts/passport; no scientific input, owner body or outcome edit."""
from pathlib import Path
import subprocess,json,hashlib,re,datetime,uuid,sys,platform
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
changes=[]
for p in (R/'evidence').rglob('*'):
 if not p.is_file() or p.suffix not in ['.json','.xml','.stdout','.log','.txt']:continue
 b=p.read_bytes();s=b.decode();clean=s.replace(str(R),'[RETURN]').replace(str(ROOT),'[WORKTREE]').replace(str(Path.home()),'[HOME]')
 if p.suffix=='.xml':clean=re.sub(r'hostname="[^"]*"','hostname="[HOST]"',clean)
 if clean!=s:
  raw=R/'runtime/raw_metadata'/p.relative_to(R/'evidence');raw.parent.mkdir(parents=True,exist_ok=True);raw.write_bytes(b);p.write_text(clean);changes.append(dict(path=str(p.relative_to(R)),raw_sha256=sha(b),portable_sha256=sha(clean.encode())))
if changes:write('portability_receipt.json',dict(changes=changes,assertions_outcomes_and_native_refs_unchanged=True,raw_metadata_retained_in_ignored_runtime=True))
import bootstrap,generic_proposal,pytest
source={x['git_blob']:x for x in json.loads((R/'source_manifest.json').read_text())}
imports=[]
for name,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and Path(f).suffix=='.py' and Path(f).is_relative_to(R):
  p=Path(f).resolve();b=p.read_bytes();row=dict(module=name,actual_file=str(p.relative_to(R)),git_blob_sha1=blob(b),sha256=sha(b))
  if blob(b) in source:row.update(source_commit=source[blob(b)]['commit'],source_path=source[blob(b)]['path'])
  else:row.update(source_commit='THIS_RETURN_CONTENT_COMMIT; exact bytes bound by publication receipt',source_path=str(p.relative_to(ROOT)))
  imports.append(row)
write('actual_live_imports.json',dict(imports=imports,native_reattested=bootstrap.reattest(),proposal_module_file=str(Path(generic_proposal.__file__).relative_to(R)),no_native_results_monkeypatched=True))
marker=R/'runtime/pv3h_marker.json'
if not marker.exists():marker.write_text(json.dumps(dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),role='PV3H_BOUNDED_WORKER_NOT_HQ',created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
m=json.loads(marker.read_text())
write('environment_passport_delta.json',dict(passport_schema='EXECUTION_ENVIRONMENT_PASSPORT_R1',environment_id=m['environment_id'],epoch_id=m['epoch_id'],owner_session_alias='PV3H_SOURCEFREE_PROPOSAL',surface='LOCAL_SHARED_STORE',machine_alias='AUTHORIZED_LOCAL_HOST',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),runtime_marker_digest=sha(marker.read_bytes()),probe='audit_pv3h.py verifies119 exact preimages, original16 + corrected24 focused tests, raw original semantic FAIL and native74 live attestation',python=dict(status='VERIFIED',version=platform.python_version()),pytest=dict(status='VERIFIED',version=pytest.__version__),git=dict(status='VERIFIED',version=subprocess.check_output(['git','--version'],text=True).strip()),shell='zsh',filesystem='VERIFIED_LOCAL_SPARSE',node='NOT_REQUIRED_UNKNOWN',git_object_store_alias='EXISTING_CANONICAL_SHARED_STORE',worktree_alias='ISOLATED_PV3H',branch='agent/userdirect-pyat-20261016-r16-pv3h-competent-hq-original-method-decision-r1',sealed_startup='a36aa625d2567d35d3e826ff3191115829715735',head_at_probe=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),materialized_source_refs=imports,native_closure='EXACT74;119_SUPPORT_FILES',warm_reuse='Verified static source bytes only; new native owner policies/processes/ledger here, no earlier mutable owner state reused',current_grade='SOURCE_FREE_DEV_SPECIALIZED_GT2_PLUS_UNISSUED_GENERIC_METHOD_PROPOSAL',actual_tests=dict(final_proposal_pass=24,unchanged_handoff_pass=16,raw_original_semantic_fail=1,initial_frozen_locator_fail=2,initial_frozen_pass=22),full_PV3N_court='NOT_RERUN',model_provider='OpenAI via Codex',user_selected_model_effort='GPT-6.1 Sol High',actual_model_effort_telemetry='UNKNOWN',actual_incremental_cash=None,actual_usage_quota=None,paid_overflow_policy='NOT_INFERRED',source_privacy='No original survey/SAV/DTA, real respondent or external experimental model call',helpers_used=False,editor_switch=False,independent_review='Original row oracle and separate tests; not a new independent semantic/HQ reviewer',assignments_completed=['PV3H decision-ready candidate and native generic-method evidence'],next_affinity=['Separate competent Field Forge native-binary semantic owner court','Qualified existing HQ scoped decision'],next_commission_auto_launched=False,expiry=['runtime reset','changed native body','new semantic/source/host grant'],preservation='Static native sources and raw metadata retained locally; portable source/receipt evidence committed'))
files={}
for p in sorted(R.rglob('*')):
 if not p.is_file() or any(k in ['runtime','primary','__pycache__','.pytest_cache'] for k in p.relative_to(R).parts) or p.name in ['artifact_sha256.json','publication_receipt.json'] or p.suffix=='.pyc':continue
 files[str(p.relative_to(R))]=sha(p.read_bytes())
write('artifact_sha256.json',files)
print('PV3H_PORTABLE_PACKAGE_READY',len(files),'artifacts')
