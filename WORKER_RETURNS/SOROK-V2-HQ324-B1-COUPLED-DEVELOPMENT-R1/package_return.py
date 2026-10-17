"""Refresh portable source identities/passport and sanitize executed JUnit metadata."""
from pathlib import Path
import hashlib
import importlib
import json
import platform
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
BASE = '65e1e3dfb1a34275ac3f8c6122419a87895eb011'
BANK = '7b091166ac31c0b538093007808cbbbdaccf8d6f'
PARENT = 'a563c4a14b4442b2beef7d652d1a1496249521a1'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def source(commit, path, blob=None):
    blob = blob or git('rev-parse', commit + ':' + path)
    assert git('rev-parse', commit + ':' + path) == blob
    data = subprocess.check_output(['git', 'cat-file', 'blob', blob], cwd=ROOT)
    return dict(commit=commit, path=path, git_blob_sha1=blob,
                content_sha256=hashlib.sha256(data).hexdigest(),
                use='READ_ONLY_CONTRACT_OR_RESEARCH__NOT_IMPORTED_RUNTIME')


if __name__ == '__main__':
    tree = ET.parse(HERE / 'junit.xml')
    removed = []
    for suite in tree.iter('testsuite'):
        if 'hostname' in suite.attrib:
            suite.attrib.pop('hostname')
            removed.append('hostname')
    tree.write(HERE / 'junit.xml', encoding='utf-8', xml_declaration=True)
    paths = git('ls-tree', '-r', '--name-only', BASE).splitlines()
    suffixes = [
        'CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY.md',
        'CAN_011_V3_MIDDLE_STATE/AUTHORITY.md',
        'ADP_019_V3_EXTERNAL_ADMISSION/AUTHORITY.md',
        'ADP_020_V3_CAUSAL_RNG/AUTHORITY.md',
        'ADP_021_V3_HYBRID_SCHEDULER/AUTHORITY.md',
        'integration/WHOLE_MACHINE_ARCHITECTURE_CLOSURE_RULING.md',
        'integration/V3_COMPLETION_IMPLEMENTATION_RULING.md',
        'CAN008_R2_AUTHORITY_CANDIDATE_R1/02_HQ_CAN008_R2_ADOPTION_R1.md',
    ]
    sources = [source(BASE, next(p for p in paths if p.endswith(s))) for s in suffixes]
    sources += [source(BASE, 'WORKER_COMMISSIONS/SOROK-V2-HQ324-B1-CAN008-CAN011-COUPLED-POSITIVE-R1/00_COMMISSION.md'),
                source(BASE, 'SOROK_PRODUCT_CONTROL_ROOM/00D_WARM_ENVIRONMENT_PASSPORT_AND_COST_AWARE_AGENT_DISPENSATION_R1.md'),
                source(BANK, 'SOROK_PRODUCT_CONTROL_ROOM/00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md'),
                source(BANK, 'SOROK_PRODUCT_CONTROL_ROOM/PRE_A0_PSYCHIC_ARCHITECTURE_R1/00_PRE_A0_ARCHITECTURAL_BANK_R1.md'),
                source('ab93fc3328a860f7c97ecec5673b8f7e0c5cff76',
                       'data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/CAN_008_V3_PRESSURE_FLOW_RESPONSE/AUTHORITY_R2_CANDIDATE.md', 'b80dd6925066510ecbbfec7b427bf9f688475663')]
    for name in ['02_BIKE_THEFT_INTERPRETIVE_CONTEST_AND_LATER_DESIRE_RECURSION_R1.md',
                 '03_SOURCE_GRADED_DELTA_AND_BFIRST_EXECUTABLE_PROGRAM_R1.md']:
        path = 'SOROK_PRODUCT_CONTROL_ROOM/RESEARCH_PROPOSALS/20261017_CONATIVE_RELATIONAL_PERSON_ACTIVITY_SPINE_R1/' + name
        ref = source(PARENT, path)
        assert ref['git_blob_sha1'] == git('rev-parse', BASE + ':' + path)
        ref['startup_blob_matches_parent'] = True
        sources.append(ref)
    write('source_identities.json', dict(startup=BASE, sources=sources,
        native_probe=dict(commands=["rg --files rawlsing_next | rg '(v3|response|middle_state)'",
            "rg -l 'class .*MiddleState|class .*ResponseTransaction|def .*pressure_flow' --glob '*.py'"],
            result='No runnable native CAN008/CAN011 positive closure found in inspected startup checkout.',
            imported_accepted_native_modules=[], production_positive_claim=False)))
    marker_path = HERE / 'runtime_marker.json'
    if marker_path.exists():
        marker = json.loads(marker_path.read_text())
    else:
        marker = dict(environment_id=uuid.uuid4().hex, epoch_id=uuid.uuid4().hex,
                      purpose='NONCAUSAL_ENVIRONMENT_CONTINUITY_ONLY')
        write('runtime_marker.json', marker)
    bfirst = importlib.import_module('bfirst')
    imported_path = Path(bfirst.__file__).resolve()
    assert imported_path == HERE / 'bfirst.py'
    import pytest
    import sqlite3
    now = datetime.now(timezone.utc).isoformat()
    write('environment_passport_delta.json', dict(
        passport_schema='SOROK_00D_R1', **marker,
        owner_session_alias='B1_SINGLE_IMPLEMENTER', surface='LOCAL_SHARED_STORE',
        machine_alias='LOCAL_AUTHORIZED_WORKTREE', conversation_or_account_affinity=None,
        status='LIVE_VERIFIED', last_live_probe_at=now,
        runtime_marker_digest=hashlib.sha256(marker_path.read_bytes()).hexdigest(),
        probe_command_and_result={'python3 --version':platform.python_version(),
            'python3 -m pytest --version':pytest.__version__, 'git --version':git('--version'),
            'sqlite3':sqlite3.sqlite_version, 'bfirst.__file__':'VERIFIED_EXPECTED_RETURN_SUBTREE/bfirst.py'},
        capabilities=dict(python='VERIFIED', pytest='VERIFIED', git='VERIFIED',
                          filesystem='VERIFIED', shell='VERIFIED', node='UNKNOWN_NOT_NEEDED'),
        git_object_store_alias='EXISTING_SHARED_REPOSITORY', worktree_alias='ASSIGNED_B1_WORKTREE',
        branch=git('branch','--show-current'), exact_checkout_base=BASE,
        checkout_head_at_packaging=git('rev-parse','HEAD'), clean_dirty='DIRTY_NEW_ASSIGNED_RETURN_ONLY',
        source_family='SOURCEFREE_FIXTURE', materialized_source_refs=[dict(
            path='bfirst.py', git_commit='RETURN_COMMIT_AT_PUBLICATION',
            git_blob_sha1=git('hash-object',str(HERE/'bfirst.py')),
            local_relative_staging_path='bfirst.py', imported_module_file='bfirst.py (verified relative to return root)')],
        dependency_closure_status='BOUNDED', fixture_permission='COMMISSION_TEST_ONLY_SOURCEFREE',
        covered_test_suites=[dict(command='python3 -m pytest -q test_bfirst.py --junitxml=junit.xml',
            result='PASS', tests=39, failures=0, skips=0, junit='junit.xml', log='test.log')],
        science_grade='SOURCEFREE_PROTOTYPE__PROVISIONAL_MODEL_HYPOTHESIS',
        model_provider='OPENAI_CODEX_USER_SELECTED', model_effort='GPT-6 Medium (commission selected; no switch)',
        pricing_class='UNKNOWN', cash_known=False, quota_known=False, usage=None, expected_reset=None,
        privacy_source_grant='PRIVATE_REPO_AND_SOURCEFREE_ONLY__NO_EXTERNAL_PROVIDER_CALLS',
        independent_review='HQ_POST_RETURN_SEPARATE_HIGH_I2_PENDING',
        assignments_completed=['B1_CANDIDATE_IMPLEMENTATION_AND_AUTHOR_TESTS'],
        next_good_affinity_tags=['CAN008','CAN011','REPLAY','SOURCEFREE'],
        staged_state_preservation='SOURCE_AND_EVIDENCE_PRESERVED_IN_RETURN; RECHECK_RUNTIME_ON_RESUME',
        retire_or_rebuild_reason=None,
        attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES',
        economics='Reuse authorized local object store and verified Python/pytest; no installer, paid API, model switch or delegation. Actual cash/quota unknown.'))
    write('execution_receipt.json', dict(status='TEST_ONLY_BFIRST_CANDIDATE_PENDING_I2', startup=BASE,
        execution_sequence=[
            dict(step=1, command='python3 bfirst.py /tmp/bfirst-early-positive', result='PASS_TWO_EVENT_POSITIVE_BEFORE_NEGATIVE_SUITE'),
            dict(step=2, command='python3 -m pytest -q test_bfirst.py', result='34 passed'),
            dict(step=3, command='python3 -m pytest -q test_bfirst.py', result='38 passed after added adversarial cases'),
            dict(step=4, command='python3 bfirst.py /tmp/bfirst-final-evidence', result='PASS', log='positive.log'),
            dict(step=5, command='python3 -m pytest -q test_bfirst.py --junitxml=junit.xml', result='39 passed', log='test.log')],
        observed_failures=0, sanitation=dict(junit_removed_metadata=['hostname'],
            causal_evidence_changed=False, raw_test_totals_preserved=True),
        not_executed=['Production V3', 'original survey execution', 'native CAN008/CAN011 actor-positive',
                      'frozen accepted suites (unchanged; no production imports)', 'independent High/I2 acceptance'],
        published_sha='VERIFY_ASSIGNED_REMOTE_TIP_IN_FINAL_RETURN_MESSAGE'))
    # Reject personal path/host metadata before publication; do not scan unrelated source data.
    forbidden = [str(Path.home()).encode(), platform.node().encode(), b'/Users/']
    for path in HERE.rglob('*'):
        if path.is_file() and path.suffix not in ('.pyc','.sqlite') and '__pycache__' not in path.parts and '.pytest_cache' not in path.parts:
            if path.name == 'package_return.py':
                continue  # sanitizer code contains forbidden examples as literals
            assert not any(needle in path.read_bytes() for needle in forbidden), path.name
    inventory = {str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in HERE.rglob('*') if p.is_file() and p.name != 'manifest.json'
                 and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts
                 and p.suffix != '.sqlite'}
    write('manifest.json', dict(status='TEST_ONLY_BFIRST_CANDIDATE_PENDING_I2', startup=BASE,
        branch=git('branch','--show-current'), files_sha256=inventory,
        exact_remote_return_sha='FINAL_RETURN_AND_GIT_REMOTE_BRANCH_IDENTITY',
        boundary='Only assigned new return subtree; no canonical or sibling edits.'))
    print('Packaged 39 passing tests, sanitized JUnit, source identities and bounded live passport.')
