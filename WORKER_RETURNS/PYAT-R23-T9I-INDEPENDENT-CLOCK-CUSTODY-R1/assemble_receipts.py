"""Assemble review receipts from actual runs; do not execute or relabel tests."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

RET=Path(__file__).resolve().parent
def read(name):return json.loads((RET/name).read_text())
def sha(name):return hashlib.sha256((RET/name).read_bytes()).hexdigest()
def write(name,obj):(RET/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')

def main():
    expected={'author':(28,0,0),'legacy':(8,0,0),'independent':(48,10,1)}
    suites={}
    pins=read('evidence/staged_source_manifest.json')
    for row in pins:
        assert sha('pinned_candidate/'+row['relative'])==row['sha256']
    for suite,(count,failed,rc) in expected.items():
        x=read(f'evidence/{suite}_execution.json')
        junit=ET.parse(RET/'junit'/f'{suite}.xml').getroot()[0].attrib
        assert (int(junit['tests']),int(junit['failures']),int(junit['errors']),int(junit['skipped']))==(count,failed,0,0)
        assert x['exit']==rc
        assert Path(x['rootdir'])==RET and Path(x['configfile'])==RET/'pytest.ini'
        outcomes=dict(Counter(t['outcome'] for t in x['actual_test_reports']))
        assert outcomes.get('passed',0)==count-failed and outcomes.get('failed',0)==failed
        for m in x['all_loaded_project_modules']:
            assert hashlib.sha256(Path(m['__file__']).read_bytes()).hexdigest()==m['sha256']
        candidate_inventory=[m for m in x['all_imported_module_preimages'] if m.get('pin_status')=='CANDIDATE_EXPECTED_PREIMAGE']
        suites[suite]={'actual_counts':{'collected':count,'passed':count-failed,'failed':failed,'errors':0,'skips':0},
            'process_exit':rc,'rootdir':x['rootdir'],'configfile':x['configfile'],
            'named_loaded_project_modules':len(x['all_loaded_project_modules']),
            'candidate_pinned_file_module_inventory_entries':len(candidate_inventory),
            'all_loaded_runtime_modules':len(x['all_imported_module_preimages']),
            'execution_receipt':f'evidence/{suite}_execution.json','execution_receipt_sha256':sha(f'evidence/{suite}_execution.json'),
            'junit':f'junit/{suite}.xml','junit_sha256':sha(f'junit/{suite}.xml'),
            'stdout_stderr':f'logs/{suite}.log','log_sha256':sha(f'logs/{suite}.log'),
            'loaded_project_modules':x['all_loaded_project_modules']}
    assert sha('01_PRECOMMITTED_CLOCK_ESTIMAND_ORACLE.json')=='4646107ef1b0eae7f5aed3cd4fdb193e361fc7594924aea423dccb9734150aa3'
    git_oracle=subprocess.check_output(['git','-C',str(RET.parents[1]),'show',
        'da06c084fbd51b21482bb3bbb79a0eadec901484:WORKER_RETURNS/PYAT-R23-T9I-INDEPENDENT-CLOCK-CUSTODY-R1/01_PRECOMMITTED_CLOCK_ESTIMAND_ORACLE.json'])
    assert git_oracle==(RET/'01_PRECOMMITTED_CLOCK_ESTIMAND_ORACLE.json').read_bytes()
    audit=read('evidence/source_audit_summary.json')
    write('02_PINNED_NATIVE_MODULE_AND_TEST_REPRO.json',{
        'schema':'T9I_PINNED_NATIVE_REPRO@1','candidate':audit['candidate'],'independent_base':audit['independent_base'],
        'startup':'863a89c4ba03c47b6f50e5ba1144f510d8895a0b','original_oracle_freeze_commit':'da06c084fbd51b21482bb3bbb79a0eadec901484',
        'original_oracle_sha256':sha('01_PRECOMMITTED_CLOCK_ESTIMAND_ORACLE.json'),
        'original_oracle_unchanged_against_freeze_commit':True,'copied_source_audit':audit,
        'full_immutable_source_manifest':{'path':'evidence/immutable_copied_source_manifest.json','sha256':sha('evidence/immutable_copied_source_manifest.json')},
        'staged_source_manifest':{'path':'evidence/staged_source_manifest.json','sha256':sha('evidence/staged_source_manifest.json')},
        'suites':suites,'shadow_controls':{mode:read('evidence/shadow_'+mode+'.json') for mode in
            ['documented-bare-relative','ambient-config-reenactment','bare','bare-without-local-config']},
        'custody_scope':'All copied source hashes verified; all runtime module preimages inventoried. Expected native/candidate preimages checked before module/test exec. Third-party inventory is measured, not independently accepted owner pins.',
        'original_runner_limit':'Original guard checks package prefix only, not each module or test preimage. This review supplies the stronger per-module guard.',
        'reproduce':'python3 -B WORKER_RETURNS/PYAT-R23-T9I-INDEPENDENT-CLOCK-CUSTODY-R1/run_review.py',
        'expected_reproduction_exit':1,'exit_meaning':'RED independent court; author and legacy each exit 0. No xfail/skip laundering.'})
    events=read('evidence/independent_observations.json')
    by_id={x['id']:x['actual'] for x in events}
    stored=read('pinned_candidate/evidence/02_real_temporal_to_selected_world_two_times.json')
    methods=['M0_PIECEWISE_HOLD','M1_LINEAR_INTERPOLATION','M2_UNCERTAINTY_AWARE_BACKOFF']
    actual_compare={m:{'AS_OF':by_id['C1_'+m],'RETROSPECTIVE':by_id['C2_'+m]} for m in methods}
    assert actual_compare==stored['method_comparison_TC1']
    assert by_id['E6_TWO_TIME']['reads']==stored['two_time_reads']
    findings=[
        {'id':'R1','category':'native_authorization_semantics','events':['RED_NATIVE_VS_ADAPTED_AUTHORITY'],'failed_assertions':1,'role':'blocking adapted/native grant conflation'},
        {'id':'R2','category':'missing_not_observed_zero','events':['RED_NULL_'+m for m in methods],'failed_assertions':3,'role':'blocking'},
        {'id':'R3','category':'basis_source_edition_custody','events':['RED_BASIS_PROVENANCE'],'failed_assertions':1,'role':'blocking'},
        {'id':'R4','category':'full_structural_world_identity','events':['RED_STRUCTURAL_EQUALITY'],'failed_assertions':1,'role':'blocking certificate defect; original positive fixture still constant'},
        {'id':'R5','category':'probe_routes_vs_authorized_opportunities','events':['RED_PROBE_OPENS_ROUTE'],'failed_assertions':1,'role':'blocking consumer qualification; no real installation inferred'},
        {'id':'R6','category':'postrupture_estimand_qualification','events':['RED_POSTRUPTURE_'+methods[0],'RED_POSTRUPTURE_'+methods[2]],'failed_assertions':2,'role':'scientific qualification; hypothetical hold could remain with explicit assumptions'},
        {'id':'R7','category':'archive_context_vs_product_basis_lag','events':['RED_NONBASIS_PUBLICATION_LAG'],'failed_assertions':1,'role':'ancillary metadata ambiguity; not a future-value leak'}]
    for finding in findings:finding['actual_observations']={event:by_id[event] for event in finding['events']}
    write('03_ACTUAL_TWO_TIME_CONSUMER_HOSTILES.json',{
        'schema':'T9I_ACTUAL_TEMPORAL_CONSUMER_HOSTILES@1','verdict':'RED_SOURCEFREE_TEMPORAL_CLOCK_CUSTODY_AND_CONSUMER',
        'method_comparison_exactly_matches_original':True,'method_comparison':actual_compare,
        'two_time_exactly_matches_original':True,'two_time':by_id['E6_TWO_TIME'],
        'findings':findings,'actual_failed_assertions':10,'actual_passed_assertions':38,
        'native_controls':{k:v for k,v in by_id.items() if k.startswith('NATIVE_')},
        'independent_uncertainty':by_id['INDEPENDENT_UNCERTAINTY'],
        'clock_rights_actor_capability_limit':by_id['CLOCK_RIGHTS_ACTOR_CAPABILITY_LIMIT'],
        'oracle_crosswalk':{
            'C1_ASOF_1995':'PASS measured .20 and W0 only; persistence is not identified truth',
            'C2_RETRO_1995':'PASS .40 explicitly interpolated/probe; consumer grant qualification fails',
            'C3_NULL_NO_SUPPORT':'PARTIAL: empty vs observed zero passes; NaN -> authorized zero fails',
            'C4_RUPTURE':'PARTIAL: M1 blocks bracket; postrupture M0/M2 have no rupture-specific qualification',
            'C5_GEOGRAPHY':'PASS explicit nonharmonization and wrong country/instrument/cohort refusals',
            'E1_POSTCLOCK_PUBLICATION':'PASS simple asof/retro split; independently bounded retrospective known-at snapshot unavailable',
            'E2_REVOCATION':'PASS current boolean exclusion in both modes; timestamped effective/discovered reconstruction HOLD',
            'E3_NONRENEWAL':'PASS current boolean exclusion in both modes; dated entitlement/current grant separation HOLD',
            'E4_COHORT':'NO PERSON/MEMORY CLAIM ACCEPTED: no exposure/remembered-exposure evidence or actor API',
            'E5_TC_TREND':'PASS linear .04/year model calculation only, no calibration/population inference',
            'E6_STRUCTURAL_WORLD':'PASS original complete world preimage and outputs; FAIL general equality helper',
            'E7_NATIVE_PROVENANCE':'PASS guarded 28+8 provenance and actual native controls; FAIL adapted inherited-grant claim',
            'E8_CLOSURE':'PASS 1259 exact preimages and bounded audit; 22-file runnable native closure'},
        'native_N8E_N8S_N9_execution':False,'actor_exposure_or_memory_proved':False,
        'prohibitions':['no real EE12 source pair','no national inference','no OC05','no N11','no N12','no V3','no method adoption']})
    print(json.dumps({'suites':{s:r['actual_counts'] for s,r in suites.items()},'original_values_and_outputs_exact':True}))

if __name__=='__main__':main()
