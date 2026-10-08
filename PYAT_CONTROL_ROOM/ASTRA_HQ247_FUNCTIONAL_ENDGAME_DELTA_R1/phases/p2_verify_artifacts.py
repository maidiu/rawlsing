"""Validate documentary lineage/accounting/terrain; never import project code."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
REL = 'PYAT_CONTROL_ROOM/ASTRA_HQ247_FUNCTIONAL_ENDGAME_DELTA_R1'
BASE = 'b5ec127a763a7f041604b0c96ddb2a906fc3a0e1'
BRANCH = 'agent/astra-pyat-hq247-functional-endgame-delta-audit-r1'
Q = '6f6ab9dfe5ad8f9359630dd05abf43c3fd11a1b5'
QB = 'WORKER_RETURNS/PYAT-C2-02-C4-PROVING-WORKLOAD-R1/'


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def read(commit, path):
    return subprocess.check_output(['git', 'show', commit + ':' + path])


def load(path):
    return json.loads((ROOT / path).read_text())


checks = {}
checks['exact_branch'] = git('branch', '--show-current') == BRANCH
checks['handoff_is_ancestor'] = subprocess.run(
    ['git', 'merge-base', '--is-ancestor', BASE, 'HEAD']).returncode == 0
matrix = load('F1_F8_MATRIX.json')
gates = matrix['gates']
gate_ids = {f'F{i}' for i in range(1, 9)}
dimensions = {'current_owner', 'semantic_authority', 'implemented_producer',
              'positive_productive_proof', 'actual_consumer',
              'release_replay_currentness', 'integration', 'source_occupancy',
              'first_missing_stage'}
tiers = {'local_stage_acceptance', 'integration_realization',
         'estate_occupancy', 'prev3_completion'}
checks['eight_gates_nine_dimensions_four_tiers'] = (
    len(gates) == 8 and {x['gate'] for x in gates} == gate_ids
    and all(set(x['p2_dimensions']) == dimensions
            and all(x['p2_dimensions'].values())
            and set(x['p2_four_level_status']) == tiers for x in gates))
checks['no_prev3_completion_claim'] = all(
    x['p2_four_level_status']['prev3_completion'] == 'NOT_CLAIMED' for x in gates)
expected = load('final/P2_EXPECTED_CAPABILITIES.json')
rows = expected['rows']
primary = json.loads(read(Q, QB + '05_ALL35_HORIZONTAL_ACCOUNTING_PLAN.json'))
selected = json.loads(read(Q, QB + '02_PROPOSED_PROVING_SET.json'))
identity_fields = ['source_id', 'source_file', 'canonical_sha256', 'format',
                   'family', 'wave', 'historical_representation_status',
                   'historical_terminal_classification']
original = {x['source_id']: x for x in primary['rows']}
checks['all35_exact_declared_identities_preserved'] = (
    len(rows) == 35 and {x['source_id'] for x in rows} == set(original)
    and all(all(x[k] == original[x['source_id']][k] for k in identity_fields)
            for x in rows))
roles = {x['source_key']: x for x in selected['sources']}
checks['eight_physical_roles_preserved'] = (
    sum(x['c4_preparation_selected'] for x in rows) == len(roles) == 8
    and all(x['c4_preparation_selected'] == (x['source_key'] in roles)
            and (x['source_key'] not in roles or
                 (x['c4_role'] == roles[x['source_key']]['selection_role']
                  and x['physical_operation_expectations'] ==
                  roles[x['source_key']]['exact_governed_operations'])) for x in rows))
cells = [c for x in rows for c in x['functional_cells']]
checks['all280_cells_accounted'] = (len(cells) == 280
    and all(len(x['functional_cells']) == 8
            and {c['gate'] for c in x['functional_cells']} == gate_ids for x in rows))
checks['no_guessed_values_intrinsic_na_or_source_permission'] = all(
    c['empirical_expected_value'] is None and c['intrinsic_na'] is None
    and c['source_execution_permission_in_p2'] is False for c in cells)
index = load('phases/P2_SOURCE_INDEX.json')
catalog = (ROOT / 'phases/P2_SOURCE_CATALOG.md').read_text()
identity_rows = []
for x in index:
    raw = read(x['commit'], x['path'])
    blob = git('rev-parse', x['commit'] + ':' + x['path'])
    ok = blob == x['blob'] and len(raw.splitlines()) == x['line_count']
    if 'sha256' in x:
        ok = ok and hashlib.sha256(raw).hexdigest() == x['sha256']
    identity_rows.append({'commit': x['commit'], 'path': x['path'],
                          'blob': blob, 'passed': ok})
checks['all_indexed_blob_linecount_and_declared_checksums_match'] = all(
    x['passed'] for x in identity_rows)
checks['catalog_covers_indexed_identities'] = all(
    x['commit'] in catalog and x['path'] in catalog and x['blob'] in catalog for x in index)
native = load('phases/P2_NATIVE_IDENTITY.json')
raw = read(native['commit'], native['path'])
checks['native_byte_identity_only'] = (
    git('rev-parse', native['commit'] + ':' + native['path']) == native['blob']
    and hashlib.sha256(raw).hexdigest() == native['sha256']
    and native['runtime_executed'] is False and native['security_adopted_by_p2'] is False)
continuity = load('phases/P2_C1_BLOB_CONTINUITY.json')
checks['five_adopted_owner_blobs_equal_current'] = len(continuity['rows']) == 5 and all(
    git('rev-parse', continuity['adopted_join'] + ':' + x['path']) ==
    git('rev-parse', continuity['control'] + ':' + x['path']) ==
    x['adopted_join_blob'] == x['control_blob'] for x in continuity['rows'])
report = (ROOT / 'phases/P2_VERIFICATION.md').read_text()
checks['v1_v8_report_sections'] = len(re.findall(r'^## V[1-8] —', report, re.M)) == 8
proposal_paths = sorted((ROOT / 'final/proposed_commissions').glob('D[1-5]_*.md'))
proposal_sections = ['PROPOSED ONLY', 'NOT DISPATCHED', 'Branch/startup tip/worktree: unknown',
                     '**Agent / intelligence:', '**Demanded output:', '**A–G:', '**Stop']
checks['five_bounded_unissued_commission_envelopes'] = len(proposal_paths) == 5 and all(
    all(s in p.read_text() for s in proposal_sections)
    and 'Hostile' in p.read_text() and 'Review trigger' in p.read_text()
    and ('Positive' in p.read_text() or 'Genuine positives' in p.read_text()) for p in proposal_paths)
historical = [p for p in git('ls-tree', '-r', '--name-only', BASE, REL + '/phases').splitlines()
              if Path(p).name.startswith(('P0_', 'P1_'))]
checks['banked_p0_p1_artifact_bytes_unchanged'] = all(
    read(BASE, p) == (ROOT / Path(p).relative_to(REL)).read_bytes() for p in historical)
changed = set(git('diff', '--name-only', BASE).splitlines())
changed.update(git('ls-files', '--others', '--exclude-standard').splitlines())
checks['all_p2_write_terrain_confined_to_audit_root'] = all(
    p.startswith(REL + '/') for p in changed)
state = load('STATE.json')
checks['phase2_complete_phase3_unstarted_hard_stop'] = (
    state['phase'] == 'P2_COMPLETE' and state['p2_completed'] is True
    and state['p3_started'] is False
    and state['pending_model_switch'] == 'STOP_MODEL_SWITCH_TO_ASTRA_FOR_P3')
checks['zero_project_native_source_test_execution_declared'] = (
    state['pipeline_tests_executed'] == matrix['pipeline_tests_executed'] ==
    expected['accounting']['raw_source_executions'] == 0
    and all(x.get('executed') is False for x in index))
stop = load('phases/P2_STOP_CURRENTNESS.json')
checks['stop_packet_checks_pass_no_new_control_delta'] = (
    all(stop['checks'].values()) and not stop['workers']
    and stop['control_head'] == matrix['control_commit'] == state['control_origin_head_observed']
    and stop['handoff_commit'] == state['handoff_commit_observed'])
result = {'schema': 'PYAT_P2_DOCUMENTARY_ARTIFACT_VALIDATION@1',
          'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'candidate_head_before_containing_commit': git('rev-parse', 'HEAD'),
          'checks': checks, 'passed': all(checks.values()),
          'counts': {'gates': len(gates), 'source_rows': len(rows), 'source_gate_cells': len(cells),
                     'index_records': len(index), 'unique_indexed_identities': len({
                         (x['commit'], x['path'], x['blob']) for x in index}),
                     'preserved_p0_p1_artifacts': len(historical), 'proposed_commissions': len(proposal_paths)},
          'verified_index_identities': identity_rows,
          'limits': 'Artifact lineage/accounting/terrain checks only. No project/native build, '
                    'runtime tests, raw source read, independent security qualification or HQ adoption. '
                    'Requested spans and catalog coverage do not certify full semantic review.'}
(ROOT / 'phases/P2_VALIDATION.json').write_text(json.dumps(result, indent=2) + '\n')
lines = ['# P2 documentary artifact validation', '', result['limits'], '',
         '| Check | Result |', '|---|---|']
lines += [f'| {k} | {"PASS" if v else "FAIL"} |' for k, v in checks.items()]
lines += ['', 'Counts: ' + json.dumps(result['counts']), '',
          'Containing commit and direct remote HEAD are verified externally after banking.']
(ROOT / 'phases/P2_VALIDATION.md').write_text('\n'.join(lines) + '\n')
print(json.dumps({'passed': result['passed'], 'checks': checks, 'counts': result['counts']}, indent=2))
if not result['passed']:
    raise SystemExit('Documentary artifact validation failed; inspect saved check results.')
