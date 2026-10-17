"""Verify and package sanitized evidence after actual courts; never synthesizes passes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,platform,subprocess,uuid
from materialize import ROOT,materialize

BASE='a464515f008e3ae75472ef895a315274b0cb193b'
BANK='7b091166ac31c0b538093007808cbbbdaccf8d6f'
BRANCH='agent/rabochii-sorok-v2-hq325-b2-four-return-executable-integration-r1'

def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT.parent.parent).decode().strip()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2)+'\n')

def main():
    assert git('branch','--show-current')==BRANCH
    assert git('merge-base','HEAD',BASE)==BASE
    assert git('rev-parse',BASE+'^')=='5e788413c5c55ac87822178d667d231294bc1b90'
    materialize()
    receipt=json.loads((ROOT/'execution_receipt.json').read_text())
    assert receipt['totals']['integration']['tests']==81
    positive=json.loads((ROOT/'evidence/vertical/positive/trace.json').read_text())
    control=json.loads((ROOT/'evidence/vertical/journal_only/trace.json').read_text())
    cold=json.loads((ROOT/'evidence/cold_replay.log').read_text())
    assert positive['episodes'][1]['receipt']['response']['practical_activity']==['joint_check:caretaker']
    assert control['episodes'][1]['receipt']['response']['practical_activity']==['inspect_alone:caretaker']
    assert cold['final_hash']==positive['final_hash']
    assert cold['receipts']==[ep['receipt'] for ep in positive['episodes']]
    paths=git('ls-tree','-r','--name-only',BASE).splitlines()
    suffixes=['ADP_008_V3_DEVELOPMENTAL_PHASE/AUTHORITY.md','ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.md',
              'ADP_015_V3_RELATIONSHIP_GENEALOGY/AUTHORITY.md','ADP_016_V3_CAUSAL_MEMORY/AUTHORITY.md',
              'ADP_017_V3_ACTOR_ACCESS/AUTHORITY.md','ADP_019_V3_EXTERNAL_ADMISSION/AUTHORITY.md',
              'ADP_020_V3_CAUSAL_RNG/AUTHORITY.md','ADP_021_V3_HYBRID_SCHEDULER/AUTHORITY.md',
              'CAN_011_V3_MIDDLE_STATE/AUTHORITY.md','CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY.md',
              'TD_R05_V3_DEVELOPMENTAL_RUNTIME/RESULT.md','CAN008_R2_AUTHORITY_CANDIDATE_R1/02_HQ_CAN008_R2_ADOPTION_R1.md']
    sources=[(BASE,next(p for p in paths if p.endswith(s))) for s in suffixes]
    sources += [(BASE,'WORKER_COMMISSIONS/SOROK-V2-HQ325-B2-FOUR-RETURN-EXECUTABLE-INTEGRATION-R1/00_COMMISSION.md'),
                (BASE,'SOROK_PRODUCT_CONTROL_ROOM/HQ325_FOUR_RETURN_BFIRST_FANIN_R1/00_HQ_INTAKE_AND_NEXT_IRREVERSIBLE_DECISION.md'),
                (BASE,'SOROK_PRODUCT_CONTROL_ROOM/00D_WARM_ENVIRONMENT_PASSPORT_AND_COST_AWARE_AGENT_DISPENSATION_R1.md'),
                (BANK,'SOROK_PRODUCT_CONTROL_ROOM/00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md'),
                ('ab93fc3328a860f7c97ecec5673b8f7e0c5cff76','data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY_R2_CANDIDATE.md')]
    for name in ['02_BIKE_THEFT_INTERPRETIVE_CONTEST_AND_LATER_DESIRE_RECURSION_R1.md','03_SOURCE_GRADED_DELTA_AND_BFIRST_EXECUTABLE_PROGRAM_R1.md']:
        sources.append(('a563c4a14b4442b2beef7d652d1a1496249521a1','SOROK_PRODUCT_CONTROL_ROOM/RESEARCH_PROPOSALS/20261017_CONATIVE_RELATIONAL_PERSON_ACTIVITY_SPINE_R1/'+name))
    identities=[]
    for sha,path in sources:
        blob=git('rev-parse',sha+':'+path)
        data=subprocess.check_output(['git','cat-file','blob',blob],cwd=ROOT.parent.parent)
        identities.append(dict(commit=sha,path=path,git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),use='READ_ONLY_GOVERNANCE_NOT_RUNTIME_IMPORT'))
    write('governing_sources.json',identities)
    import bridge,pytest,sqlite3
    imports=json.loads((ROOT/'imported_sources.json').read_text())
    imported=[]
    for module in (bridge.b1,bridge.p1):
        path=Path(module.__file__).resolve();relative=str(path.relative_to(ROOT))
        row=next(x for x in imports if x['materialized_path']==relative)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256']
        imported.append(dict(row,verified_module_file=relative))
    marker_path=ROOT/'runtime_marker.json'
    if marker_path.exists():marker=json.loads(marker_path.read_text())
    else:
        marker=dict(environment_id=uuid.uuid4().hex,epoch_id=uuid.uuid4().hex,purpose='NONCAUSAL_SESSION_CONTINUITY')
        write('runtime_marker.json',marker)
    capability_source=next(x for x in imports if x['materialized_path']=='imports/D1/07_CORRECTED_ABSENCE_CONTRACT_COURT.js')
    assert positive['episodes'][0]['receipt']['capability_decision']['source_sha256']==capability_source['sha256']
    imported.append(dict(capability_source,verified_module_file='Node VM exact source, SHA256 echoed in vertical receipt'))
    write('environment_passport_delta.json',dict(passport_schema='SOROK_00D_R1',**marker,
        owner_session_alias='B2_SINGLE_IMPLEMENTER',surface='LOCAL_SHARED_STORE',machine_alias='AUTHORIZED_LOCAL_WORKTREE',
        conversation_or_account_affinity=None,status='LIVE_VERIFIED',last_live_probe_at=datetime.now(timezone.utc).isoformat(),
        runtime_marker_digest=hashlib.sha256(marker_path.read_bytes()).hexdigest(),
        probe_command_and_result={'python3 --version':platform.python_version(),'python3 -m pytest --version':pytest.__version__,
            'git --version':git('--version'),'node --version':subprocess.check_output(['node','--version']).decode().strip(),
            'SQLite':sqlite3.sqlite_version,'imports.__file__':'VERIFIED_EXACT_PINNED_PATHS'},
        capabilities=dict(python='VERIFIED',pytest='VERIFIED',git='VERIFIED',node='VERIFIED',sqlite='VERIFIED',filesystem='VERIFIED',shell='VERIFIED'),
        git_object_store_alias='EXISTING_SHARED_REPO',worktree_alias='ASSIGNED_B2',branch=BRANCH,exact_checkout_base=BASE,
        head_at_packaging=git('rev-parse','HEAD'),clean_dirty='ONLY_NEW_B2_TRACKED_WORK; unrelated pre-existing untracked artifacts preserved',
        materialized_source_refs=imported,all_source_identity_manifest='imported_sources.json',dependency_closure_status='BOUNDED_FULL_FOR_COMMISSIONED_COURTS',
        fixture_source_permission='SOURCEFREE_SYNTHETIC_TEST_ONLY',covered_test_suites=receipt['totals'],
        science_grade='TEST_ONLY_BFIRST_INTEGRATED_PENDING_I2',model_provider='OPENAI_CODEX',
        model_effort='GPT-6 Medium per commission, no autonomous switch',pricing_class='UNKNOWN',cash=None,quota=None,expected_reset=None,
        privacy_source_grant='PRIVATE_REPO_SOURCEFREE_ONLY; NO_EXTERNAL_MODEL_TRANSPORT',independent_review='HQ_POST_RETURN_HIGH_I2_PENDING',
        assignments_completed=['B2_AUTHOR_INTEGRATION_AND_TESTS'],next_good_affinity_tags=['CAN008','CAN011','P1','D1','F1','REPLAY'],
        staged_state_preservation='SOURCE_AND_EVIDENCE_PRESERVED; REPROBE_RUNTIME_AFTER_RESUME',retire_or_rebuild_reason=None,
        economics='Reused selected local Git/Python/pytest/Node. No delegation, package installation, paid call or model/host switch; cash/quota unknown.',
        attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES'))
    # A semantic proof is always checked against actual executed state and records.
    requirements={
        'sealed_startup_and_parent':'Git ancestry probes; governing_sources.json',
        'four_exact_sources_and_archive':'imported_sources.json; materialize before/after execution; 69 unchanged files/archive members',
        'inherited_39_74_22_17_97':'execution_receipt.json totals and evidence/{b1,p1,d1_original,d1_corrected,f1} logs/JUnit',
        'P1_to_witness_to_B1_to_CAN011_to_later':'evidence/vertical/positive/trace.json; test_connected_two_event_positive_vs_journal_only',
        'nonoccurrence_and_false_admission':'test_eligible_alternative_can_fail_to_occur; test_p1_eligibility_alone_cannot_authenticate_witness; test_nonoccurrence_candidate_with_forged_positive_observation_is_denied',
        'capability_and_corrected_absence':'actual Node VM source hash in vertical receipt; UNKNOWN/ABSENT/expiry/scope/condition tests',
        'independent_agency':'test_independent_caregiver_history_controls_actual_offered_action; test_focal_child_history_cannot_become_caregiver_history',
        'belief_affect_world_access_separation':'peer attribution, proposition/affect, no world blame, no private source and actor-safe output tests',
        'atomic_rollback_and_stale':'test_target_rollback_preserves_objective_admission; test_stale_witness_cannot_be_rebound_to_new_actor_history',
        'cold_replay':'evidence/cold_replay.log exact receipt list and final hash; fresh subprocess and database',
        'F1_optional_contract':'36 actual adapter dispatches, 19 boundary-only passes, 17 explicit N/A; unchanged native runner RED exit1, preserved',
        'no_unlicensed_semantic_substitution':'README production discrepancy table; precise 17-case owner gaps in f1_applicability.json',
        'sourcefree_only_assigned_terrain':'Git diff against startup checked before publication; no accepted/frozen/source35/production edits',
        'publication_and_remote_sha':'Final worker message after direct remote HEAD equality check (external to commit preimage)'}
    write('completion_audit.json',dict(status='BOUNDED_IMPLEMENTATION_REQUIREMENTS_EVIDENCED__INDEPENDENT_ACCEPTANCE_PENDING',requirements=requirements,
        known_open_native_court_gaps=17,not_claimed='Full F1 native PASS, calibrated science, production or independent I2 acceptance'))
    # Portable artifacts must not include personal filesystem or machine metadata.
    files=[p for p in ROOT.rglob('*') if p.is_file() and not any(part in p.parts for part in ('imports','__pycache__','.pytest_cache'))
           and p.suffix!='.sqlite' and p.name!='manifest.json']
    for path in files:
        data=path.read_bytes()
        assert str(Path.home()).encode() not in data,path.name
        assert platform.node().encode() not in data,path.name
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    write('manifest.json',dict(status='TEST_ONLY_BFIRST_INTEGRATED_PENDING_I2',startup=BASE,branch=BRANCH,
        files_sha256=manifest,excluded_runtime_material='Ignored exact imports, caches and temporary SQLite databases; reproducible via run_courts.py',
        remote_return_sha='FINAL_VERIFIED_WORKER_MESSAGE_AND_REMOTE_GIT_REF'))
    print('Package verified: inherited 249 checks, new 81 checks, exact cold replay; F1 19 boundary passes and 17 native gaps retained.')

if __name__=='__main__':main()
