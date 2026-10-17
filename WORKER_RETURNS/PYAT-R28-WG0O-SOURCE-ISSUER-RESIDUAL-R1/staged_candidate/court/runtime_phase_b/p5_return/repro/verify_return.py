"""Read-only custody/evidence audit. This does not replace a fresh independent run."""
import collections
import hashlib
import json
import pathlib
import subprocess
import xml.etree.ElementTree as ET

R = pathlib.Path(__file__).resolve().parents[1]
REPO = R.parents[1]
PREFIX = R.relative_to(REPO).as_posix()
C = R / 'review/runtime_phase_b/candidate'
CODE = '7499f32abd8d8027a37fe86f090ed3248ec71169'
FREEZE = 'd7833422661b4d8f6b1be728cecf75a8431fbdc8'
START = '7e589c19c693c150d0cf622fc43e84bbc40d1b31'
SHA = '06fadc7eb8c01fa832fa59beccfc2ea2f6e068216fdc8b04c95365065d492723'
FIELDS = ['op_id', 'release_tag', 'risk_name', 'targets', 'member_ids', 'grant',
          'disposition', 'native_item_ids', 'source_edition', 'full_identity_hash',
          'query', 'predicate']

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def read(name):
    return json.loads((R / name).read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def counts(path):
    root = ET.parse(path).getroot()
    return dict(tests=len(root.findall('.//testcase')),
                failures=len(root.findall('.//failure')),
                errors=len(root.findall('.//error')),
                skips=len(root.findall('.//skipped')))

def main():
    m = read('RETURN_MANIFEST.json')
    assert (m['sealed_startup'], m['code_snapshot_commit'], m['prospective_freeze_commit']) == (START, CODE, FREEZE)
    assert not any(m[x] for x in ['new_operative_grants', 'self_adoption', 'reviewer_launched'])
    candidate = C / 'repro/wg0p4_workload.py'
    assert sha(candidate.read_bytes()) == SHA == m['candidate_sha256']
    assert candidate.read_bytes() == git('show', f'{CODE}:{candidate.relative_to(REPO)}')
    frozen = (R / 'HOSTILE_EXPECTATIONS.json').read_bytes()
    assert sha(frozen) == '8c0aa9fedcf5edfc4034d0ccd88797412981b39d33016e7d9ed5acb1bc07d78b'
    assert frozen == git('show', f'{FREEZE}:{PREFIX}/HOSTILE_EXPECTATIONS.json')
    git('merge-base', '--is-ancestor', START, FREEZE)
    git('merge-base', '--is-ancestor', FREEZE, CODE)

    rows = read('source_selector_inputs.json')['files']
    assert len(rows) == 60
    immutable = 0
    for row in rows:
        original = git('show', row['commit'] + ':' + row['path'])
        assert sha(original) == row['sha256'] and blob(original) == row['git_blob_sha1']
        staged = R / 'review' / row['staged_path']
        if staged != candidate:
            assert staged.read_bytes() == original, str(staged)
            immutable += 1
    assert immutable == 59
    native_selector = json.loads((C / 'source_selector.json').read_text())['files']
    assert len(native_selector) == 27
    for row in native_selector:
        data = (C / 'pinned' / row['staging_path']).read_bytes()
        assert sha(data) == row['sha256'] and blob(data) == row['git_blob_sha1']
        assert data == git('show', row['commit'] + ':' + row['source_path'])
    cut = read('review/observations/phase_b/candidate_read_cut.json')
    assert cut['candidate_sha'] == CODE and len(cut['source_rows']) == 43
    for row in cut['source_rows']:
        data = (R / 'review' / row['staged_path']).read_bytes()
        assert sha(data) == row['sha256'] and blob(data) == row['git_blob_sha1']
        assert data == git('show', row['commit'] + ':' + row['path'])

    evidence = read('02_NATIVE_COLD_POSITIVE_AND_FRONTIER.json')
    expected = dict(descriptor=26, frozen65=65, inherited=74, owners80=80,
                    wg0p4=69, historical_p2=29, historical_p3=36)
    total = 0
    for name, n in expected.items():
        directory = R / 'observations' if name in ['descriptor', 'frozen65', 'inherited', 'owners80'] else C / 'observations'
        actual = counts(directory / (name + '.xml'))
        assert actual == dict(tests=n, failures=0, errors=0, skips=0)
        assert actual == evidence['test_runs'][name]
        terminal = json.loads((directory / (name + '.terminal.json')).read_text())
        assert terminal['exit'] == 0 and terminal['candidate_sha256'] == SHA
        assert all(terminal[k] == v for k, v in actual.items())
        assert (directory / (name + '.stdout')).stat().st_size > 0
        total += n
    assert total == 379
    assert counts(R / 'observations/baseline_three_reds.xml') == dict(tests=3, failures=3, errors=0, skips=0)
    assert set(evidence['new_descriptor_refusals']) == set(FIELDS)
    for name in FIELDS:
        obs = read('observations/descriptor_' + name + '.json')
        assert obs == evidence['new_descriptor_refusals'][name]
        assert obs['actual_type'] == 'IdentityError' and obs['refused_before_I03']
        assert obs['bound_fields'] == FIELDS
        assert not any('I03' in c['name'] or c['name'] == 'fact_entry' for c in obs['calls'])

    full = read('01_FULL_BOUND_SOURCE_DESCRIPTOR.json')
    assert full['descriptor_dataclass_fields'] == FIELDS
    assert len(full['actual_registered_contract']['bindings']) == 3
    for binding in full['actual_registered_contract']['bindings'].values():
        assert set(binding['descriptor']) == set(FIELDS)
        for name in ['query', 'predicate']:
            assert set(binding['descriptor'][name]) == {'ref', 'semantic_projection'}
    cold = evidence['original_manifest_cold']
    assert cold['candidate_sha'] == CODE
    assert (cold['first_I03_calls'], cold['second_I03_calls'], cold['checkpoint_exit']) == (1, 2, 23)
    assert cold['first_pid'] != cold['second_pid']
    assert cold['manifest_before'] == cold['manifest_after'] and cold['manifest_units'] == 3
    assert all(cold[x] for x in ['original_receipt_preimage_verified', 'all_original_results_resolved',
                                 'fsync_directory', 'fsync_file', 'atomic_replace'])
    assert len(cold['consumer']) == 3
    conditional = evidence['ordinary_conditional']
    assert conditional['candidate_sha'] == CODE
    assert conditional['counts'] == {'yes': 1, 'no': 1} and conditional['denominator'] == 2
    assert conditional['same_respondents'] == ['R2', 'R3'] and not conditional['separate_demo_function_called']
    assert conditional['route'] == ['WorkloadBuilder', 'build_executable_plan', 'make_executor',
                                    'run_plan', 'accepted_BatchExecutionRunner', 'consumer_effects']
    assert len(conditional['original_frontier']) == 25
    assert collections.Counter(r['disposition'] for r in conditional['original_frontier']) == dict(PRODUCED=3, HELD=16, INADMISSIBLE=6)

    custody = read('observations/source_custody_final.json')
    assert custody['tested_candidate_sha256'] == SHA and custody['immutable_input_files_verified'] == 59
    assert len(custody['pinned_native_blobs']) == custody['staged_native_module_count'] == 14
    assert len(custody['actual_imported_native_modules']) == custody['actually_imported_native_count'] == 12
    for row in custody['actual_imported_native_modules']:
        local = REPO / row['file'].removeprefix('<WORKTREE>/')
        data = local.read_bytes()
        assert sha(data) == row['sha256'] and blob(data) == row['git_blob_sha1']
        assert custody['pinned_native_blobs']['rawlsing_next/' + local.name] == row['git_blob_sha1']
    assert read('environment_passport_delta.json')['schema'] == 'RAWLSING_ENVIRONMENT_PASSPORT@1'
    for path in git('diff', '--name-only', START).decode().splitlines():
        assert path.startswith(PREFIX + '/'), path
    files = sorted(set(git('ls-files', '--cached', '--others', '--exclude-standard', PREFIX).decode().splitlines()))
    for name in files:
        assert '/owner/' not in name and '/runtime/' not in name and not name.endswith('key.bin'), name
        assert pathlib.Path.home().as_posix().encode() not in (REPO / name).read_bytes(), name
    manifest = read('ARTIFACT_MANIFEST.json')
    assert manifest['schema'] == 'WG0P5_GIT_BLOB_ARTIFACT_MANIFEST@1'
    expected_files = {str((REPO / f).relative_to(R)) for f in files} - {'ARTIFACT_MANIFEST.json'}
    assert {r['path'] for r in manifest['files']} == expected_files
    for row in manifest['files']:
        data = (R / row['path']).read_bytes()
        assert (len(data), sha(data), blob(data)) == (row['bytes'], row['sha256'], row['git_blob_sha1']), row['path']
    print(json.dumps(dict(status='PASS', scientific_acceptance='PENDING_INDEPENDENT_WG0M_AND_HQ',
                          final_passed_testcases=total, original_reds_retained=3,
                          immutable_original_inputs=immutable, artifact_files=len(manifest['files']),
                          tested_candidate_sha256=SHA), indent=2))

if __name__ == '__main__':
    main()
