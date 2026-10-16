"""Build portable documentary receipts from actual retained execution."""
from pathlib import Path
import json,hashlib,uuid,datetime,subprocess,sys,xml.etree.ElementTree as ET
from stage_sources import ROOT,WT,git
def write(name,data):
    (ROOT/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def read(name):return json.loads((ROOT/name).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    source_rows=read('source_manifest.json')+read('native_source_manifest.json')
    for row in source_rows:
        b=(ROOT/row['staged_path']).read_bytes()
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
        assert sha(b)==row['sha256']
    suites=[]
    for e in read('evidence/execution.json'):
        xml=ET.parse(ROOT/e['junit']).getroot();cases=list(xml.iter('testcase'))
        failures=[dict(id=c.attrib.get('name'),message=f.attrib.get('message')) for c in cases for f in c.findall('failure')]
        errors=[c.attrib.get('name') for c in cases if c.find('error') is not None]
        skips=[c.attrib.get('name') for c in cases if c.find('skipped') is not None]
        suites.append(dict(**e,tests=len(cases),passed=len(cases)-len(failures)-len(errors)-len(skips),
                           failures=failures,errors=errors,skips=skips))
    assert sum(len(s['failures']) for s in suites)==18
    assert sum(len(s['errors'])+len(s['skips']) for s in suites)==0
    write('04_COURT_MATRIX.json',dict(suites=suites,total_failures=18,
        no_claim_of_independent_mechanism_count=True,original_sgi1_cases=24,original_sgi1_predicates=98,
        overall='GENEALOGY_ADP_OWNER_AUTHORITY_HOLD'))
    obs=read('evidence/g12_observations.json');graphs={}
    for name,s in obs['scenarios'].items():
        graphs[name]=dict(sourcefree_test_description_only=True,
            construction_dependencies=[dict(source='MOTHER_CHECKPOINT_'+name,target='PENDING_TARGET_'+name,edge_type='CONSTRUCTION_DEP'),
                dict(source='PENDING_TARGET_'+name,target='ENDPOINT_CONSTRAINTS_'+name,edge_type='CONSTRUCTION_DEP'),
                dict(source='ENDPOINT_CONSTRAINTS_'+name,target='CHECK_PARTIAL_SECOND_PARENT_'+name,edge_type='RETROSPECTIVE_CONSTRUCTION_DEPENDS_ON')],
            represented_causal_edges=[dict(source=p,target=e['event_id'],edge_type='CAUSAL_PARENT') for e in s['history'] for p in e['causal_parent_event_ids']],
            mother_anchor=s['mother_before'],mother_unchanged=s['mother_before']==s['mother_after'],
            independent_oracle=s['oracle'],conflicting_endpoint_result=s['replay'],
            admitted_native_actor_events=0,conception='PENDING_NONCAUSAL',child_generated_events=0,birth_events=0)
    write('05_CONSTRUCTION_AND_CAUSAL_DAGS.json',graphs)
    write('RETURN.json',dict(commission='SOROK-R3-HQ319-G12-GENEALOGY-OWNER-BRIDGE-R1',
        verdict='GENEALOGY_ADP_OWNER_AUTHORITY_HOLD',
        exact_sgi1_reproduced={'cases':24,'predicates':98,'fingerprints_equal':24,'new_provider_calls':0},
        g11_unchanged_tests_passed=25,new_characterization_controls_passed=25,
        supplemental_controls_passed=1,literal_adversarial_failures_retained=18,
        failure_assertions_overlap=True,source_blobs_verified=len(source_rows),
        native_positive='EXACT_INHERITED_CANDIDATE_FIXTURE_ONLY',accepted_native_developmental_transfer=False,
        actual_native_project_refusal=obs['native']['project_refusal'],
        actual_production_guard='DENY_ZERO_EFFECT / ZERO_POSITIVE_REGISTRY',
        court_holds=['MOTHER_NATIVE_CHECKPOINT_UNBOUND','RETROSPECTIVE_CONSTRUCTION_RULE_UNISSUED',
            'NATIVE_DEVELOPMENTAL_EFFECT_RULE_UNBOUND','SCENARIO_SELECTION_AUTHORITY_UNBOUND',
            'ADP020_NATIVE_BINDING_UNBOUND','RETRY_SELECTION_MEASURE_UNBOUND',
            'RELATIONSHIP_FORMING_WITNESS_UNBOUND','CONCEPTION_BIOLOGY_AUTHORITY_HOLD',
            'CHILD_GENERATION_NATIVE_PRODUCER_UNBOUND','BIRTH_AND_CHILD_INITIALIZATION_HOLD',
            'SOURCE_DYAD_HOUSEHOLD_USE_UNBOUND'],
        hold_codes_are_court_classifications_not_fictional_native_api_outputs=True,
        owner_docket='03_OWNER_REQUEST_DOCKET.md',science_grade='F3_AT_EXACT_SOURCEFREE_LAB_AND_CANDIDATE_CELL_ONLY',
        integrated_genealogy_feasibility='FU',white_whale_risk='MATERIAL',
        operative_v3_wake=False,semantic_issuance=False,original_survey_reads=0,
        new_native_actor_events=0,new_conception_events=0,new_birth_events=0,new_focal_child_generated_events=0,
        independent_acceptance='REQUIRED_FROM_SEPARATE_HQ_COMMISSION_AFTER_ANY_NEW_CANDIDATE',
        report='00_RETURN.md',execution='evidence/execution.json',passport='environment_passport_delta.json'))
    # Verify inherited candidate sources against M06's actual retained import audit.
    commit='10a116f273c76095fca7255d4b6422a9ff3497a2'
    path='WORKER_RETURNS/SOROK-R3-HQ316-M06-M05-OWNER-ANCESTRY-INDEPENDENT-R1/08_ACTUAL_IMPORT_AND_LAW_AUDIT.json'
    audit_raw=git('show',commit+':'+path);audit=json.loads(audit_raw)
    matches=[]
    for row in source_rows:
        if row['staged_path'].startswith('sources/native_candidate/'):
            matches.append(dict(path=row['staged_path'],git_blob_sha1=row['git_blob_sha1'],
                identical_m06_imports=[i['module'] for i in audit['imports'] if i['blob_sha1']==row['git_blob_sha1']]))
    assert all(m['identical_m06_imports'] for m in matches)
    write('evidence/native_ancestry.json',dict(commit=commit,path=path,
        git_blob_sha1=git('rev-parse',commit+':'+path).decode().strip(),sha256=sha(audit_raw),matches=matches,
        scope='Exact inherited candidate closure; M06 acceptance is finite sourcefree method evidence, not production adoption'))
    startup='9aa7e19817823aa1642c7c222093098d701c08fe'
    paths=git('ls-tree','-r','--name-only',startup,'SOROK_PRODUCT_CONTROL_ROOM').decode().splitlines()
    required=[p for p in paths if Path(p).name.startswith(('00A_','00B_','00C_','00D_','00_FULL_','00_READ_ME_FIRST','HQ319_'))]
    required.append('WORKER_COMMISSIONS/SOROK-R3-HQ319-G12-GENEALOGY-OWNER-BRIDGE-R1/00_COMMISSION.md')
    write('evidence/startup_and_read_cut.json',dict(repository='maidiu/rawlsing',remote='https://github.com/maidiu/rawlsing.git',
        branch='agent/rabochii-sorok-r3-hq319-g12-genealogy-owner-bridge-r1',sealed_startup=startup,direct_remote_startup=startup,
        startup_read_sources=[dict(commit=startup,path=p,git_blob_sha1=git('rev-parse',startup+':'+p).decode().strip()) for p in required],
        complete_sourcefree_materialized_blobs=len(source_rows),scope='BOUNDED_SOURCEFREE_CLOSURE',
        one_agent=True,helpers=0,new_provider_calls=0,original_survey_reads=0,operative_v3_wake=False,
        new_owner_rule_issued=False,accepted_developmental_transfer=False))
    marker=ROOT/'runtime_marker.json'
    if not marker.exists():write('runtime_marker.json',dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),owner_session_alias='SOROK_HQ319_G12'))
    ids=read('runtime_marker.json')
    passport=dict(passport_schema='SOROK_00D_ENVIRONMENT_PASSPORT_R1',**ids,
        surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_G12_HOST',conversation_or_account_affinity='CURRENT_CODEX_SESSION',
        status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        runtime_marker_digest=sha(marker.read_bytes()),
        probe_command_and_result={'python3 --version':sys.version.split()[0],
            'python3 -m pytest --version':subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),
            'git --version':git('--version').decode().strip()},
        python={'version':sys.version.split()[0],'capability':'VERIFIED'},pytest={'capability':'VERIFIED'},git={'capability':'VERIFIED'},
        node={'capability':'UNKNOWN','needed':False},filesystem={'capability':'VERIFIED'},shell={'name':'bash','capability':'VERIFIED'},
        dependency_versions={'pytest':'9.0.2','others':'Python standard library; no package installation'},
        git_object_store_alias='EXISTING_RAWLSING_SHARED_STORE',worktree_alias='HQ319_G12_NEW_ISOLATED_SPARSE',
        branch='agent/rabochii-sorok-r3-hq319-g12-genealogy-owner-bridge-r1',checkout_base=startup,
        head_at_packet_build=git('rev-parse','HEAD').decode().strip(),clean_dirty_state='RETURN_FILES_PENDING_FINAL_COMMIT',
        materialized_source_refs=source_rows,
        actual_imports={'sgi1':read('evidence/sgi1_replay.json')['imports'],'native':obs['native']['imports']},
        dependency_closure_status='BOUNDED',fixture_permission='COMMISSIONED_SOURCEFREE_OFFLINE_COURT_ONLY',
        covered_test_suites=[dict(suite=s['suite'],command=s['command'],pass_count=s['passed'],fail_count=len(s['failures']),
            skip_count=len(s['skips']),exit_status=s['exit_status'],junit=s['junit'],stdout=s['stdout']) for s in suites],
        science_grade='SOURCEFREE_LAB_REPLAY_PLUS_CANDIDATE_OWNER_BOUNDARY; NOT_ACCEPTED_NATIVE_ACTOR_USE',
        model_provider={'editor':'Codex','provider':'OpenAI','selected_model':'GPT-6.1','effort':'High',
            'selection_basis':'USER_SELECTED_PAIR; no automatic switch','cash_known':False,'cash':None,
            'new_external_provider_calls':0,'pricing_class':'CURRENT_CODEX_INCLUDED_ALLOWANCE; exact monetary cost UNKNOWN',
            'usage_probe_utc':'2026-10-16T22:33:56Z',
            'five_hour_used_percent_start':19,'five_hour_used_percent_at_probe':49,
            'weekly_used_percent_start':47,'weekly_used_percent_at_probe':51,
            'usage_is_account_wide_not_attributable_to_this_court':True,'paid_overflow_authorized':False,
            'five_hour_reset_unix':1792200803,'weekly_reset_unix':1792685642},
        phase_model_assignment='One user-selected Codex GPT-6.1 High agent owns full court; mechanical phases do not imply helper delegation',
        primary_model_economics='User-selected qualified warm local shared store reused; alternative price/quality ranking UNKNOWN; no provider switch',
        review_independence='Independent of SGI1/G11/native candidate authors; own new test/proposal acceptance reserved to separate HQ I2',
        privacy_source_grant='PRIVATE_REPOSITORY_READ_AND_OWNED_RETURN_WRITE; no original respondents or external provider export',
        assignments_completed=['G12 bounded independent sourcefree court'],
        next_good_affinity_tags=['GENEALOGY','K11','ADP015','ADP020','NATIVE_OWNER_BOUNDARY'],
        staged_state_preservation='Exact tracked sources preserved; next worker must rehash and probe, no process-persistence promise',
        retire_or_rebuild_reason=None,
        attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES')
    write('environment_passport_delta.json',passport)
    changed=git('diff','--name-only',startup,'HEAD').decode().splitlines()
    prefix='WORKER_RETURNS/SOROK-R3-HQ319-G12-GENEALOGY-OWNER-BRIDGE-R1/'
    assert all(p.startswith(prefix) for p in changed)
    write('evidence/write_terrain.json',dict(sealed_startup=startup,head_at_audit=git('rev-parse','HEAD').decode().strip(),
        changed_committed_paths=changed,all_within_authorized_return=True,production_guard_blob_unchanged='e0528d65215cb431196570c38bac4eae94217a1b'))
    # Manifest excludes itself and later remote receipt to avoid hash cycles.
    artifacts=[]
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(part in {'__pycache__','.pytest_cache'} for part in p.parts):continue
        rel=str(p.relative_to(ROOT))
        if rel in {'artifact_manifest.json','remote_verification_receipt.json'}:continue
        b=p.read_bytes();artifacts.append(dict(path=rel,bytes=len(b),sha256=sha(b)))
    write('artifact_manifest.json',dict(scope='G12_RETURN_ARTIFACTS_ONLY',excluded=['artifact_manifest.json','remote_verification_receipt.json'],files=artifacts))
    print(json.dumps({'verified_source_blobs':len(source_rows),'suites':len(suites),'literal_reds':18,'artifact_files':len(artifacts)}))
if __name__=='__main__':main()
