"""Audit the bounded fix evidence without modifying frozen tests or inherited receipts."""
from pathlib import Path
import datetime,hashlib,json,subprocess,uuid
import xml.etree.ElementTree as ET
from verify_repair import ROOT,REPO,R1,B2_PATH,git,digest,dump

def suite(path,n,failures=0):
    s=ET.parse(path).find('testsuite')
    assert int(s.get('tests'))==n and int(s.get('failures'))==failures and int(s.get('errors'))==0
    return s

def main():
    evidence=ROOT/'evidence';after=evidence/'after'
    suite(evidence/'before/e2_strict.xml',2,2)
    suite(after/'e2_strict.xml',2)
    suite(after/'r1.xml',45)
    suite(after/'regression.xml',5)
    suite(after/'e2_full.xml',44,2)
    suite(after/'x2.xml',17,1)
    for label,n in [('b1',39),('p1',74),('f1',97),('integration',81)]:suite(after/'inherited'/(label+'.xml'),n)
    receipt=json.loads((after/'execution_receipt.json').read_text())
    assert receipt['f1']['raw_native_failures']==17 and receipt['f1']['raw_native_exit']==1
    assert receipt['f1']['boundary_negative_deferral_pass']==19 and receipt['f1']['not_applicable']==17
    for label,n in [('d1_original',22),('d1_corrected',17)]:
        assert sum(line.startswith('PASS ') for line in (after/'inherited'/(label+'.log')).read_text().splitlines())==n
    for control in ('positive','journal_only'):
        path='evidence/vertical/'+control+'/trace.json'
        assert (after/'inherited/vertical'/control/'trace.json').read_bytes()==git('show',R1+':'+B2_PATH+'/'+path)
    for phase in ('before','after'):
        for committed in (False,True):
            row=json.loads((evidence/phase/'e2_sql'/('strict_legacy_after_'+str(committed)+'.json')).read_text())
            assert row['before']==row['after'] and len(row['before']['occurrence'])==2
            if phase=='after':
                assert row['receipt']['reason']=='EVENT_IDENTITY_LEDGER_INTEGRITY_FAILURE'
                assert row['receipt']['event_admission']=='NOT_PERFORMED' and not row['receipt']['b1_invoked']
    bridge=REPO/B2_PATH/'bridge.py'
    provenance=json.loads((after/'source_provenance.json').read_text())
    assert provenance['bridge_sha256']==digest(bridge)
    assert len(provenance['inherited'])==69
    before=json.loads((evidence/'before/source_provenance.json').read_text())
    assert before['inherited']==provenance['inherited'] and before['frozen_tests']==provenance['frozen_tests']
    (ROOT/'source_diff.patch').write_bytes(git('diff',R1,'--',B2_PATH+'/bridge.py'))
    dump(ROOT/'verification_receipt.json',dict(grade='SOURCEFREE_LEGACY_REENTRY_REPAIR_CANDIDATE_PENDING_INDEPENDENT_REVIEW',base=R1,bridge_sha256=digest(bridge),strict_e2_before=dict(tests=2,failures=2),strict_e2_after=dict(tests=2,failures=0),unchanged_checks=330,r1_tests=45,new_controls=5,frozen_e2=dict(tests=44,pass_count=42,old_behavior_observation_failures=2),frozen_x2=dict(tests=17,pass_count=16,old_collision_demonstration_failure=1),native_f1=receipt['f1'],positive_control_trace='BYTE_IDENTICAL_TO_R1',journal_only_trace='BYTE_IDENTICAL_TO_R1',scope='B2 replay/admission integrity; committed objective facts preserved'))
    marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),owner_session_alias='B2_legacy_reentry_repair')
    dump(ROOT/'environment_passport_delta.json',dict(passport_schema='SOROK_ENVIRONMENT_PASSPORT_R1',**marker,surface='LOCAL_SHARED_STORE',machine_alias='authorized_local',status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),probe_command_and_result=dict(command='verify_repair.py after',runtime=json.loads((after/'runtime.json').read_text())),git_object_store_alias='existing_shared_store',worktree_alias='isolated_b2_legacy_reentry',branch='codex/b2-legacy-reentry-repair',checkout_base=R1,source_family='sourcefree_B2',materialized_source_refs='evidence/after/source_provenance.json',dependency_closure_status='BOUNDED_FULL',covered_test_suites='verification_receipt.json',science_grade='repair candidate pending independent review',model_provider='OpenAI_Codex',effort='UNKNOWN',pricing_class='UNKNOWN',observed_credits=None,observed_usage=None,independent_review_separation='E2 reviewer now implements user-directed repair; this is NOT independent acceptance',privacy_source_grant='authorized local sourcefree repair',assignments_completed=['USERDIRECT_LEGACY_REENTRY_FIX'],next_good_affinity_tags=['EVENT_CUSTODY','SQLITE'],staged_state_preservation='ignored .runtime staging retained',retire_or_rebuild_reason=None))
    files=[]
    for p in sorted(ROOT.rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or any(v in rel.parts for v in ('.runtime','__pycache__','.pytest_cache')) or p.name=='artifact_manifest.json':continue
        files.append(dict(path=str(rel),sha256=digest(p),bytes=p.stat().st_size))
    dump(ROOT/'artifact_manifest.json',dict(files=files,bridge_sha256=digest(bridge)))
    print('Verified: E2 strict 2 RED -> 2 PASS; 330 unchanged +45 R1 +5 controls PASS; frozen failure identities retained')

if __name__=='__main__':main()
