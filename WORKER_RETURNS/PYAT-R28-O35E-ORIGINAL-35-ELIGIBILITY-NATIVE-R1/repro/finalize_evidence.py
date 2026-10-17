"""Validate, summarize and sanitize experiment evidence without changing science."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,uuid,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parents[1];REPO=HERE.parents[1];OBS=HERE/'observations'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((HERE/p).read_text())
def write(p,v):(HERE/p).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def main():
 for path,record in read('COURT_CODE_PIN.json')['files'].items():
  assert sha((HERE/path).read_bytes())==record['sha256'],path
 for path,record in read('SOURCE_INPUTS.json')['files'].items():
  assert sha((HERE/'runtime/pinned'/path).read_bytes())==record['sha256'],path
 # Publish path-normalized JUnit; preserve byte-exact originals in ignored runtime.
 raw=HERE/'runtime/rawlogs';raw.mkdir(exist_ok=True)
 normalization=read('observations/path_normalization.json')['records'] if (OBS/'path_normalization.json').exists() else []
 for p in OBS.glob('*.xml'):
  b=p.read_bytes();text=b.decode();normalized=text.replace(str(HERE),'$RETURN').replace(str(REPO),'$WORKTREE')
  if normalized!=text:
   (raw/(p.name+'.'+sha(b))).write_bytes(b);p.write_text(normalized)
   normalization.append({'file':str(p.relative_to(HERE)),'raw_sha256':sha(b),'published_sha256':sha(p.read_bytes()),'only_change':'personal worktree prefix normalization'})
 write('observations/path_normalization.json',{'records':normalization,'raw_location':'runtime/rawlogs (ignored, local only)'})
 runs=read('observations/process_receipts.json')['runs']
 suites=[]
 for run in runs:
  root=ET.parse(HERE/run['junit']).getroot();cases=root.findall('.//testcase')
  counts={'testcases':len(cases),'failures':len(root.findall('.//failure')),'errors':len(root.findall('.//error')),'skipped':len(root.findall('.//skipped'))}
  suites.append({**run,**counts})
 assert [(s['testcases'],s['failures'],s['errors'],s['skipped']) for s in suites[:3]]==[(26,0,0,0),(26,0,0,0),(27,0,0,0)]
 assert suites[3]['errors']==1 and suites[3]['exit_code']==2
 pos=read('observations/native_positive.json');subset=read('observations/native_subset_characterization.json')
 matrix=read('01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json');negative=read('source_grant_negative_evidence.json')
 frozen=read('PREREGISTERED_EXPECTATIONS.json')
 values=[]
 for f in pos['facts']:
  s=f['semantic_fields'];values.append({'fact_ref':{'kind':'EmpiricalFact@1.0.0','object_id':f['object_id'],'content_hash':f['content_hash']},
   'measure_kind':s['measure_kind'],'raw_denominator':s['raw_denominator_support'],
   'weighted_denominator':s['weighted_denominator_support_if_authorized'],
   'cells':s['target_topology']['complete_cell_semantic_projection'],
   'uncertainty':s['uncertainty_method_or_typed_state'],'denominator_member_refs':s['denominator_member_refs']})
 out={'schema':'O35E_NATIVE_POSITIVE_AND_INDEPENDENT_ANTIJOIN@1',
  'verdict':'ORIGINAL35_SOURCE_U_E_PRE_HOLD__NATIVE_TESTONLY_POSITIVE',
  'original_source_run':{'status':'NOT_EXECUTED__SOURCE_AND_ISSUER_HOLD','literal_original_item_ids_used':[],
   'new_original_products':0,'signed_rights_verified_for_this_new_run':0,'new_U_or_E_pre_issuance':False,
   'original_negative_controls':negative['original_negative_controls']},
  'preregistration':{'commit':read('COURT_CODE_PIN.json')['preregistration_commit'],
   'sha256':sha((HERE/'PREREGISTERED_EXPECTATIONS.json').read_bytes()),'metadata_root':frozen['metadata_keys_sha256'],
   'chronology':'pushed before first actual native test; no original E_pre implied'},
  'metadata_court':{'waves':35,'censused_active_rows':18259,'original_eligible_count':None,
   'five_actual_preserved_items':frozen['five_preserved_relation_item_omission_controls'],
   'claims':'Loss of exact preserved metadata, not original eligible-job omission proof',
   'historical_header_reconciliation':matrix['historical_structure_manifest']},
  'native_positive':{'grade':pos['claim'],'fixture_native_source_label':'RAW-m01; synthetic W1, not any of the original35',
   'physical_rows':3,'decoder_invoked':False,'source_identity':pos['source_identity'],
   'actual_calls':pos['native_calls'],'release_ref':pos['release_ref'],'manifest_ref':pos['manifest_ref'],
   'batch_summary':pos['batch_summary'],'numeric_values':values,'consumer_receipt':pos['consumer'],
   'limitation':'OC01 policy consumes exact supplied refs/tier declarations; this is not source scientific certification, numeric recomputation, world publication or N9 authority.',
   'full_evidence':'observations/native_positive.json'},
  'antijoin':{'full_positive':pos['work_antijoin'],
   'native_subset':{'batch_full_manifest_coverage':subset['batch_summary']['full_coverage'],'independent_missing':subset['work_antijoin']['missing'],
    'consumer':subset['consumer'],'interpretation':'Manifest coverage alone does not certify E_pre/U coverage; not a Batch contract violation.'},
   'guard':'O35E experimental independent multiset outer join before owner execution and consumer, and exact result-ref join after actual callbacks',
   'native_omissions':'Raw/weighted/discovery omissions each raise ScientificHold; spies verify zero I03/I05/consumer invocations.',
   'not_installed_as_original_governance':True},
  'execution':{'unique_passing_tests':53,'o35e_tests':26,'native_retained_author_tests':27,'cold_repeat_tests':26,
   'optional_author_D07':'NOT_COLLECTED_MISSING_TEST_HELPER__1_ERROR_NOT_PASS','suites':suites,
   'imports':'observations/*_imports.json','earlier_failures_retained':['observations/o35e_combined.xml','observations/native_owners.xml']},
  'effects':{'original35_completion':False,'source_permission':False,'U_E_pre_issuance':False,'F1_F8_estate_completion':False,
   'N9_grant':False,'OC05':False,'EE12':False,'N11':False,'N12':False,'V3':False}}
 write('02_REAL_SOURCE_OR_TESTONLY_NATIVE_POSITIVE_AND_ANTIJOIN.json',out)
 write('STAGING_LIMITATIONS.json',{'schema':'O35E_STAGING_LIMITS@1','pinned_input_files':33,
  'native_core_imports':'BOUNDED_COMPLETE_OBSERVED_AND_BYTE_VERIFIED',
  'optional_D07_author_suite':{'status':'PARTIAL_MISSING_FIXTURE','missing_import':'rawlsing_next.tests.d07_bounded_loss_harness',
   'tracked_in_canonical_pin':False,'actual_attempt':'observations/native_d07_missing_fixture.stdout','junit':'observations/native_d07_missing_fixture.xml',
   'production_consumer_function_actually_tested':True},
  'initial_return_test_repair':{'failure':'Python tuples compared directly with JSON list transport',
   'repair':'Compare exact serialized JSON transport, preserving all values, refs and hashes',
   'native_source_changed':False,'original_expectations_changed':False,'retained_junit':'observations/o35e_combined.xml'}})
 passport=read('environment_passport_delta.json')
 marker=HERE/'runtime/environment_marker.json'
 if not marker.exists():marker.write_text(json.dumps({'environment_id':str(uuid.uuid4()),'epoch_id':str(uuid.uuid4())})+'\n')
 markerdata=json.loads(marker.read_text())
 passport.update({'passport_schema':'PYAT_00D_RETURN_PASSPORT@1',**markerdata,
  'owner_session_alias':'O35E_CURRENT_CODEX_WORKER','surface':'LOCAL_SHARED_STORE','machine_alias':'existing_local_host',
  'status':'LIVE_VERIFIED_AT_RETURN_NOT_A_FUTURE_LEASE','last_live_probe_at':datetime.now(timezone.utc).isoformat(),
  'runtime_marker_digest':sha(marker.read_bytes()),'probe_command_and_result':'run_courts.py: final26 PASS; cold26 PASS; native27 PASS; D07 expected collection2',
  'git_object_store_alias':'existing_shared_repository_store','worktree_alias':'assigned_existing_isolated_worktree',
  'checkout_base':'246fcdf7b25c6b160c0a167e4284e08d04194505','native_python':sys.version,
  'native_pytest':read('observations/o35e_final_imports.json')['pytest_version'],
  'metadata_python':matrix['native_resolver']['python'],'metadata_pandas':matrix['native_resolver']['pandas'],
  'git_version':subprocess.check_output(['git','--version']).decode().strip(),'node':'NOT_NEEDED_NOT_PROBED',
  'materialized_source_refs':'SOURCE_INPUTS.json','actual_imports':'observations/*_imports.json and matrix native_resolver',
  'dependency_closure_status':'BOUNDED_NATIVE_CORE_VERIFIED__OPTIONAL_D07_PARTIAL',
  'covered_test_suites':'observations/process_receipts.json','science_grade':'SOURCEFREE_METADATA_ARCHAEOLOGY_AND_NATIVE_TESTONLY_COMPOSITION',
  'model_provider':'current built-in Codex session; provider/account tier and exact reasoning configuration not independently observed',
  'incremental_money':None,'credits_usage':None,'money_quota_status':'UNKNOWN','installed_new_packages':[],
  'assignments_completed':['O35E bounded commission return; original scientific completion remains HOLD'],
  'next_good_affinity_tags':['ORIGINAL35_METADATA','SOURCE_U_E_PRE_NATIVE_BINDING','NO_DROP_CUSTODY'],
  'independent_review_conflict':'Author of this experimental gate/report; cannot independently accept its own promotion',
  'staged_state_preservation':'pinned sourcefree stage and raw local logs retained under ignored runtime; reconstruct via exact Git inputs',
  'retire_or_rebuild_reason':'Reprobe on reset, marker loss, changed source pins, permission scope, or independent review conflict',
  'original_source_permission':'NOT_VERIFIED_FOR_NEW_RUN','actor_model_calls':0,'subagents':0})
 write('environment_passport_delta.json',passport)
 print(json.dumps({'unique_passing_tests':53,'cold_repeat':26,'original_controls_held':10,'optional_missing_fixture_errors':1,'new_original_products':0}))

if __name__=='__main__':main()
