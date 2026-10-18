"""Independent completion audit of the actual replay files, not author tallies."""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
R = Path(os.environ['WG0P11_ROOT']).resolve()
E = Path(os.environ['WG0P11_EVIDENCE']).resolve()
SHA = '89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643'


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2)+'\n')


def copy(src, folder):
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, folder/Path(src).name)


def junit(path, expected):
    t = ET.parse(path)
    actual = tuple(len(t.findall('.//'+x)) for x in ('testcase', 'failure', 'error', 'skipped'))
    assert actual == expected, (str(path), actual, expected)
    return dict(zip(('tests', 'failures', 'errors', 'skips'), actual))


def i03(raw):
    return sum(x['name']=='execute_empirical_query' and x['file'].endswith('pre553_empirical_query.py') for x in raw['calls'])


frozen = read(HERE/'01_PHASE_A_FROZEN_REQUIREMENTS_AND_HASHES.json')
initial = read(HERE/'02_CLEAN_CLONE_MODULE_AND_INPUT_SHA.json')
assert Path(initial['clone']).resolve() == R.parents[1]
assert not initial['initial_status']
assert hashlib.sha256((HERE/'test_independent_publication.py').read_bytes()).hexdigest() == frozen['independent_test_sha256']
for name in ('test_independent_publication.py', '01_PHASE_A_FROZEN_REQUIREMENTS_AND_HASHES.json'):
    raw = subprocess.check_output(['git', 'show', 'cb5484c96325e06b981dea22207e4dadc3d83558:'+str((HERE/name).relative_to(HERE.parents[1]))], cwd=HERE)
    assert raw == (HERE/name).read_bytes(), name
for row in frozen['original_source_rows']:
    p = R/'candidate'/row['staged_path']; raw = p.read_bytes()
    assert not p.is_symlink()
    assert (hashlib.sha256(raw).hexdigest(), len(raw)) == (row['sha256'], row['bytes'])
for row in initial['whole_p10_tracked_closure']:
    if row['path'].endswith('.py'):
        assert hashlib.sha256((R.parents[1]/row['path']).read_bytes()).hexdigest() == row['sha256'], row['path']
historical = R/'reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md'
assert hashlib.sha256(historical.read_bytes()).hexdigest() == frozen['historical_verdict']['sha256']

expected = dict(wg0o17=17, wg0q36=36, wg0m33=33, original65=65, original3=3, j44_k11=55, owners80=80, fresh42=42)
counts = {}
records = read(R/'04_JUNIT_LOGS/run_receipt.json')
assert {x['name'] for x in records} == set(expected)
for x in records:
    assert x['exit_code'] == 0
    assert Path(x['actual_module']['path']).resolve() == R/'candidate/court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py'
    assert x['actual_module']['sha256'] == SHA
    name = x['name']; counts[name] = junit(R/'04_JUNIT_LOGS'/x['junit'], (expected[name], 0, 0, 0))
    for suffix in ('.xml', '.stdout.log', '.stderr.log'):
        copy(R/'04_JUNIT_LOGS'/(name+suffix), E/'published_native_junit')
copy(R/'04_JUNIT_LOGS/run_receipt.json', E/'published_native_junit')
for name, count in [('independent_frozen_D1_D5', 6), ('D3_fresh42', 42), ('D4_pointer', 1), ('transport9', 9)]:
    counts[name] = junit(E/(name+'.xml'), (count, 0, 0, 0))
counts['historical_characterisation'] = junit(E/'historical_characterisation.xml', (3, 2, 0, 0))
counts['historical_five_unconstructible'] = junit(E/'historical_five_unconstructible.xml', (5, 5, 0, 0))
for case in ET.parse(E/'historical_characterisation.xml').findall('.//testcase'):
    failure = case.find('failure')
    if failure is not None:
        assert 'source_edition' in case.attrib['name'] or 'native_item_ids' in case.attrib['name']
        assert 'COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED' in (failure.text or '')
for case in ET.parse(E/'historical_five_unconstructible.xml').findall('.//testcase'):
    name = case.attrib['name']; text = case.find('failure').text or ''
    if 'C3_source_artifact_revocation' in name:
        assert 'UNKNOWN_RELEASE_NO_REVOCATION' in text
    elif 'D3_truncated_or_empty_snapshot' in name:
        assert 'content_hash must be a non-empty string' in text
    else:
        assert any(x in name for x in ('E1_release_issuer_not_registrar', 'E2_unregistered_issuer', 'E3_issuer_epoch_mismatch'))
        assert 'unexpected keyword argument' in text and ('issuer_id' in text or 'issuer_epoch' in text)

hostiles = read(E/'source_hostiles/actual_source_hostiles_summary.json')
assert len(hostiles) == 3
for x in hostiles:
    assert x['verifier_exit'] == x['bootstrap_exit'] == 86
    assert x['payload_started'] is False and x['new_I03_calls'] == 0
    b = read(E/'source_hostiles'/(x['case']+'_bootstrap.json'))
    assert 'PAYLOAD_STARTED' not in b['stdout'] and 'WG0P6_BOOTSTRAP_REFUSE:' in b['stderr']

review = R/'reviewer_frozen/02_WG0P7_STAGED/reviewer'
authority = []; negatives = 0
for sub, key, oracle in [('authority_seam_runs/phase_a_frozen', 'controls', review/'01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json'), ('authority_body_runs/phase_a_wg0p6', 'new_controls', R/'reviewer_frozen/01_FROZEN_AUTHORITY_BODY_AND_EPOCH_ORACLE.json')]:
    for control in read(oracle)[key]:
        src = review/'observations'/sub/(control['group']+'__'+control['case']+'.json'); d = read(src)
        assert str(R) in d['candidate_module'] and d['attempted']
        assert i03(d) == d['new_I03_calls']
        supported = sum(cell.get('state') in ('OBSERVED_POSITIVE', 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET') for entries in d['consumer'].values() for entry in entries for cell in entry.get('cells', []))
        assert supported == d['supported_fact_cells_served']
        if control['kind'] in ('NEGATIVE_REFUSAL', 'NEGATIVE_TYPED_REFUSAL'):
            assert not d['served_supported_original_fact'] and d['new_I03_calls'] == 0
            negatives += 1
        copy(src, E/'authority_raw'/sub)
        authority.append({k:d.get(k) for k in ('group', 'case', 'exception_type', 'exception_reason', 'typed_refusal', 'new_I03_calls', 'supported_fact_cells_served', 'effects_sha256', 'served_supported_original_fact')})
assert negatives == 40 and len(authority) == 48
positives = [x for x in authority if x['group']=='positive_current_body']
for x in positives:
    assert x['supported_fact_cells_served'] == 42
    assert x['effects_sha256'] == '4b9d03246167c93df6dde8d590fac33c24c51ef158d60abd8ee33601ca059550'
    assert x['new_I03_calls'] == (0 if x['case']=='P3_replay_identical' else 4)
save(E/'independent_authority_audit.json', dict(cases=authority, all_40_negatives_zero_new_I03=True))

cold = R/'candidate/court/observations/phase_b/inherited_v1/cold/cold-face4d00952b4460a7c1285c1dd80be5'
a = read(cold/'crash.json'); b = read(cold/'resume.json')
assert a['pid'] != b['pid'] and i03(a) == 1 and i03(b) == 2
assert a['manifest'] == b['manifest'] == 'bcd255228ef35edcb9b59436b76e1eb78947c07180f2936779572f510981c140'
assert a['unit_count'] == b['unit_count'] == 3
assert a['receipt'] == b['restored_receipt'] and a['receipt'] in b['receipts']
assert a['receipt']['receipt_hash'] == 'caac243fc25c521acc10b2e082b55bdb854921dff8f730680d82eeaf2dcabcbd'
for name in ('crash.json', 'resume.json', 'checkpoint.json'):
    copy(cold/name, E/'published_cold')
pointer = read(R/'candidate/observations/fresh_process_source_pointer_refusal.json')
assert pointer['original_crash_pid'] == a['pid'] and pointer['pid'] != a['pid']
assert pointer['child_exit'] == 0 and pointer['error']['type'] == 'IdentityError' and pointer['new_I03_calls'] == 0
assert pointer['same_original_manifest'] and pointer['manifest_units'] == 3 and pointer['restored_receipts'] == 0
assert pointer['owner_journal_unchanged'] and pointer['custody_unchanged']
copy(R/'candidate/observations/fresh_process_source_pointer_refusal.json', E)
comparison = R/'candidate/court/observations/phase_b/inherited_v1/observations/cold_comparison.json'
d = read(comparison); assert Path(d['cold_directory']).resolve() == cold
assert d['regenerated_cold_run']['crash_pid'] == a['pid']
copy(comparison, E)

controls = R/'candidate/court/observations/phase_b/controls_v1_final'
for src in controls.glob('*.json'):
    assert str(R) in str(read(src)), src.name
    copy(src, E/'original65_raw')
f = read(controls/'conditional__original25_unchanged.json')
frontier = dict(Counter(x['disposition'] for x in f['frontier']))
assert frontier == dict(PRODUCED=3, HELD=16, INADMISSIBLE=6)
c = read(controls/'conditional__ordinary_full_chain_yes1_no1_over2.json')
assert c['denominator'] == 2 and c['counts'] == {'yes':1, 'no':1} and c['same_respondents'] == ['R2', 'R3']
native_cold = read(controls/'cold__actual_abrupt_exit23_after_one.json')
assert native_cold['first_pid'] != native_cold['second_pid']
assert native_cold['first_I03_calls'] == 1 and native_cold['second_I03_calls'] == 2
assert native_cold['original_receipt_preimage_verified'] and native_cold['all_original_results_resolved']
folder = Path(native_cold['shared_cold_execution_path'])
assert [x['exit'] for x in read(folder/'commands.json')] == [23, 0]
for name in ('commands.json', 'crash.json', 'resume.json', 'checkpoint.json'):
    copy(folder/name, E/'original65_cold')

tracked = {x['path'] for x in initial['whole_p10_tracked_closure']}; imports = []
for src in (R/'candidate/observations/imports').glob('*.json'):
    if str(src.relative_to(R.parents[1])) in tracked:
        continue
    d = read(src)
    assert len(d['native_modules']) == 6 and d['actually_loaded_modules'] and d['candidate_pin']['sha256'] == SHA
    copy(src, E/'actual_import_audits'); imports.append(dict(pid=d['pid'], receipt=src.name, argv=d['argv']))
assert b['pid'] in {x['pid'] for x in imports}
save(E/'all_actual_import_audits_index.json', imports)
p = subprocess.run([sys.executable, '-B', 'repro/wg0p8_publication.py', 'verify'], cwd=R, capture_output=True, text=True, timeout=120)
assert p.returncode == 0
save(E/'verify_after_all_hostiles.json', dict(exit=p.returncode, stdout=p.stdout, stderr=p.stderr))
initial['final_source_recheck'] = dict(original_187_exact_after_all_tests_and_hostiles=True, all_tracked_P10_python_source_bytes_unchanged=True, all_intentionally_tampered_files_restored=True, published_verifier_exit=0, new_observed_atexit_receipt_count=len(imports))
save(HERE/'02_CLEAN_CLONE_MODULE_AND_INPUT_SHA.json', initial)
summary = dict(p10_head=initial['p10_head'], clone=str(R.parents[1]), git_fetching_disabled=initial['runtime_git_fetching_disabled'], original_source_count=187, restored_original_count=11, initial_git_tree_files=len(initial['whole_p10_tracked_closure']), immutable_phase_a_bytes_unchanged=True, actual_junit=counts, native_total=331, mandatory_total=236, authority_negatives_zero_I03=40, native_positives=positives, published_cold=dict(crash_pid=a['pid'], resume_pid=b['pid'], first_I03=i03(a), resume_I03=i03(b), manifest=a['manifest'], receipt_preimage_equal=True, receipt_hash=a['receipt']['receipt_hash']), original65_cold_pids=[native_cold['first_pid'], native_cold['second_pid']], pointer_pid=pointer['pid'], pointer_new_I03=0, original25=frontier, ordinary_conditional=dict(counts=c['counts'], denominator=2, respondents=c['same_respondents']), fresh_atexit_receipts=len(imports), source_hostiles=hostiles, historical_not_green=dict(unconstructible=5, characterisation_failures=2), missing_required_runtime_evidence=[])
save(E/'independent_completion_audit.json', summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ('actual_junit', 'native_positives', 'source_hostiles')}, indent=2))
