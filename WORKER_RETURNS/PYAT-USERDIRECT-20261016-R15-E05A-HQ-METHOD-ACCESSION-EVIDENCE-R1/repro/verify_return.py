from pathlib import Path
import json,hashlib,datetime,subprocess,sys,platform,xml.etree.ElementTree as ET,os
R=Path(__file__).resolve().parents[1];RT=R/'runtime'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads((R/p).read_text())
def dump(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R).decode().strip()
manifest=read('source_manifest.json');assert len(manifest)==401
assert (R/'source_manifest.json').read_bytes()==(R/'inputs/E05S/source_manifest.json').read_bytes()
for x in manifest:
 p=RT/x['local'];b=p.read_bytes();assert sha(p)==x['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
for source in ['input_manifest.json','authority_additional_manifest.json']:
 for x in read(source):assert sha(R/x['local'])==x['sha256']
for p in (R/'frozen_E05S').rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R/'frozen_E05S')
 src=R/'inputs/E05S'/('observations/'+rel.name if rel.parts[0]=='junit' else str(rel))
 assert p.read_bytes()==src.read_bytes(),str(rel)
cross=read('01_PINNED_E05S_METHOD_AND_HQ_AUTHORITY_CROSSWALK.json')
assert cross['status']=='METHOD_CANDIDATE_READY_FOR_COMPETENT_HQ_DECISION' and not cross['adopted']
assert sum(x['tests'] for x in cross['independent_method']['retained_JUnit'])==403 and not cross['independent_method']['court_rerun']
trace=read('observations/native_imports_and_calls.json')
for m in trace['imports']:
 p=R/m['physical_module_file'];assert sha(p)==m['sha256'];assert m['actual_physical_path_verified']
 assert not m['physical_module_file'].startswith('/')
expected={'resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','ingest_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','read_historical_test_only','consume','evaluate'}
assert expected.issubset({x['function'] for x in trace['actual_entries']})
assert trace['same_concrete_C1_evidence_objects_into_F8']>0
x=read('02_EXECUTED_TWO_CONSUMER_SERVICE_HANDOFF.json');assert len(x['packets'])==7
for label,p in x['packets'].items():
 assert p['implementation_commit']=='84485d32c0088995f8dc664dc0517b2d27f2563d'
 assert p['independent_method_acceptance']['commit']=='f524f60781e2e7e72278d04d6377fb1da877698a'
 assert p['status']=='SOURCEFREE_OFF_NOT_INSTALLED' and not any(p['boundary'].values())
 r=p['selected_world_receipt'];check=dict(r);payload=check.pop('receipt_payload_sha256')
 assert hashlib.sha256(json.dumps(check,sort_keys=True,separators=(',',':')).encode()).hexdigest()==payload
 assert r['request_hash']==p['acceptance']['request_hash'] and r['snapshot_hash']==p['acceptance']['snapshot_hash']
 assert p['consumer_values']==r['consumers']
 assert (R/'examples'/(label.lower()+'.json')).read_text()
required_files=['00_ACCESSION_READY_NOT_ADOPTED.md','01_PINNED_E05S_METHOD_AND_HQ_AUTHORITY_CROSSWALK.json','02_EXECUTED_TWO_CONSUMER_SERVICE_HANDOFF.json','03_OC05_N9_N10W_RIGHTS_AND_INSTALLATION_GATE.md','04_NEXT_COMPETENT_ISSUER_AND_PRODUCTIVE_EDGE.md']
for f in required_files:assert (R/f).is_file(),f
ss=list(ET.parse(R/'observations/handoff.xml').getroot().iter('testsuite'))
counts={k:sum(int(s.attrib.get(k,0)) for s in ss) for k in ['tests','failures','errors','skipped']}
assert counts==dict(tests=15,failures=0,errors=0,skipped=0)
assert read('observations/handoff.terminal.json')['exit']==0
assert read('observations/examples.terminal.json')['exit']==0
assert len(read('observations/cli_current.json')['consumer_values'])==2
request=read('decision/REQUEST_FOR_COMPETENT_HQ_DECISION.json');warrant=read('decision/PROPOSED_NEXT_POSITIVE_WARRANT.json')
assert request['decision'] is None and request['reviewer_identity'] is None and request['no_outbound_message']
assert not warrant['issued'] and not warrant['auto_dispatch']
assert cross['hq']['active_principal_authenticated_in_this_runtime'] is False
marker=json.loads((RT/'live_epoch.json').read_text());assert marker['status']=='LIVE_VERIFIED_IN_THIS_PYTHON_PROCESS'
# Current shell/interpreter are probed again; an old marker is not a live lease.
live=dict(interpreter_probe=dict(command='python3 --version',exit=0,version=sys.version.split()[0]),pytest_version=subprocess.check_output([sys.executable,'-m','pytest','--version']).decode().strip(),git_version=git('--version'),observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
passport=dict(schema='E05A_SANITIZED_ENVIRONMENT_PASSPORT@1',environment_id=marker['environment_id'],epoch_id=marker['epoch_id'],session_alias='E05A_BOUNDED_HANDOFF',surface='LOCAL_CODEX_S2',machine_alias='GOVERNED_SHARED_STORE_LOCAL_HOST',status='LIVE_VERIFIED__RECONSTRUCTED_EXACT_ACCEPTED_CLOSURE',last_live_probe_at=live['observed_at_utc'],scope='Sourcefree only; current probe proves this execution, not a future active-session lease',runtime_continuity='No previous chat/process continuity assumed. Known accepted Git closure reused and imported in fresh verified Python; no duplicate clone.',worktree_alias='Rawlsing_Worktrees/r15-e05a-handoff',return_path_alias=R.name,branch=git('branch','--show-current'),sealed_startup='c44367ee7734160b7387d3f3956158a3c4a00e12',HEAD_at_audit=git('rev-parse','HEAD'),origin=git('remote','get-url','origin'),live_capabilities=live,writable_marker='runtime/live_epoch.json (local ignored)',source_imports=trace['imports'],dependency_closure='FULL_ACCEPTED_E05S401_AT_SOURCEFREE_SCOPE',tests=dict(fresh_handoff=counts,prior_independent403='PRESERVED_NOT_RERUN',command='python3 repro/run_tests.py',junit='observations/handoff.xml',exit=0),model=dict(provider='Codex per user assignment',requested='GPT-6.1 Sol Medium',actual_model_setting='NOT_INDEPENDENTLY_INSPECTED'),quota_at_start=dict(primary_used_percent=45,weekly_used_percent=26,plan='plus',ordinary_usage_allowed=True),incremental_cash='UNKNOWN_NOT_MEASURED__NO_PAID_API_OR_MODEL_CALL',installed_packages='No install performed; Python and pytest existing capability probed',assignments_completed=['E05A sourcefree method handoff/dossier'],domain_affinity=['selected-world sourcefree serving','request/acceptance/receipt transport','native field permission/clock provenance'],next_related_commission='Prospective N9/OC05 sourcefree interface handoff after competent owner permission; NOT automatically authorized',review_conflicts='This worker authors the E05A transport and previously authored E05R; it is not the independent E05S reviewer or competent HQ adopter',retirement_triggers=['runtime reset','source pin drift','unrelated scope','missing use authority','required independent review of authored code'],privacy='No original survey/PDF/credentials/actor data accessed; absolute personal __file__ roots verified locally then represented as relative aliases')
text=json.dumps(passport,indent=2)+'\n';assert '/Users/' not in text and '/private/' not in text
(R/'environment_passport_delta.json').write_text(text)
audit=dict(schema='E05A_REQUIREMENT_COMPLETION_AUDIT@1',verified_at_utc=live['observed_at_utc'],status=cross['status'],requirements=[dict(requirement='Exact remote E05S acceptance and E05R pin, retained403 and11 closures',evidence='01 crosswalk; frozen_E05S exact Git tests/JUnit; input_manifest.json',proven=True),dict(requirement='Current canonical laws, HQ historical accession and scoped currentness',evidence='authority/; authority_additional_manifest.json; 01 crosswalk',proven=True),dict(requirement='Executable versioned sourcefree request/acceptance/receipt/client handoff without fork',evidence='handoff.py; repro/demo.py; 02 execution;15 JUnit checks',proven=True),dict(requirement='Actual full native pipeline and both positive original clients',evidence='33 verified imports and433 owner entries; examples; native call trace',proven=True),dict(requirement='Historical/current clocks, source changes, native separation/rights, partials/archive/ZERO_SUPPORT and reverse',evidence='Seven actual packets; distinct15 checks; source401 manifest',proven=True),dict(requirement='Competent HQ decision packet, source rights/install holds, smallest lawful next positive edge/owners/tests',evidence='decision/;03/04; status READY_NOT_ADOPTED',proven=True),dict(requirement='E04 cache lane separated; completed E05S not reopened',evidence='Pinned E04S status; E05R direct serving only; prior403 not executed anew',proven=True),dict(requirement='Authorized return-only diff and directly verified remote final SHA',evidence='publication_receipt.json plus final direct remote verification performed after commit',proven='PUBLICATION_REQUIRED_AFTER_LOCAL_AUDIT')],fresh_JUnit=counts,accepted_independent_JUnit=403,prior_court_rerun=False,hq_adoption=False,OC05_installed=False,source_issued=False,all35_occupancy=False,N11_N12_V3=False)
dump('completion_audit.json',audit)
print('VERIFIED all local commissioned deliverables: preserved403, fresh15 PASS, real accepted owner pipeline and pending competent decision; publication verification remains')
