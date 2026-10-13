#!/usr/bin/env python3
"""Validate the R3 amendment's conservation, identity and planning invariants."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
R3 = Path(__file__).resolve().parents[1]
R2 = R3.parent / 'ASTRA_PERSONA_FIRST_PREV3_COMPLETION_REPLAN_R2'
BASE = '0d38dae68ff4016c47d1af809d2e85cb160bab0c'
ORIGINAL = 'a70a069fa948e0f3c041b389edcc732b6b948a4f'
checks = []


def read(path):
    return json.loads(path.read_text())


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def check(name, value, detail):
    if not value:
        raise AssertionError(name)
    checks.append({'check': name, 'status': 'PASS', 'detail': detail})


def run():
    required = ['00_SCOPE_AND_INDEPENDENT_VERDICT.md', '01_PREV3_ONLY_COMPLETION_PLAN.md',
                '02_SOCIOLOGICAL_PRODUCT_AND_SEAM_CONTRACT.md', '03_R2_T00_T11_REDISPOSITION.json',
                '04_ORIGINAL_25_PACKAGE_CROSSWALK.json', '05_FIRST_PREV3_PRODUCT_AND_NEXT_COMMISSIONS.md',
                '06_EVIDENCE_AND_RESOURCE_VERIFICATION.md', 'EXECUTION_DAG.json']
    check('required_artifacts', all((R3 / f).is_file() for f in required), len(required))
    dag = read(R3 / 'EXECUTION_DAG.json')
    ids = {n['id'] for n in dag['nodes']}
    check('unique_dag_nodes', len(ids) == len(dag['nodes']) == 11, sorted(ids))
    todo = {n['id']: set(n['depends_on']) for n in dag['nodes']}
    check('dag_dependency_references', all(v <= ids for v in todo.values()), 'All targets exist')
    done = set()
    while todo:
        ready = {k for k, v in todo.items() if v <= done}
        if not ready:
            raise AssertionError('cycle')
        done.update(ready)
        todo = {k: v for k, v in todo.items() if k not in ready}
    check('dag_acyclic', done == ids, '11 nodes topologically resolved')
    conditional = {n['id']: set(n['depends_on']) | {e['node'] for e in n.get('conditional_dependencies', [])} for n in dag['nodes']}
    check('conditional_dependency_references', all(v <= ids for v in conditional.values()), 'Mode-specific S06 gates resolve')
    done_conditional = set()
    while conditional:
        ready = {k for k, v in conditional.items() if v <= done_conditional}
        if not ready:
            raise AssertionError('conditional cycle')
        done_conditional.update(ready)
        conditional = {k: v for k, v in conditional.items() if k not in ready}
    check('conditional_graph_acyclic', done_conditional == ids, 'Protected-mode paths cannot deadlock')
    check('bounded_and_full_paths_distinct', dag['first_bounded_path'] == ['S00', 'S01', 'S02'] and dag['full_completion_terminal'] == 'S10', 'No actor node')
    check('unissued_assignments', all(not n['issued'] and n['actual_assignee'] is None and not n['source_execution_authorized'] for n in dag['nodes']), 'No invented dispatch/source grant')
    red = read(R3 / '03_R2_T00_T11_REDISPOSITION.json')['rows']
    old = {x['id']: x for x in read(R2 / 'PROGRAM.json')['tasks']}
    check('all12_exact', len(red) == 12 and {x['r2_id'] for x in red} == set(old) and all(x['r2_task_exact'] == old[x['r2_id']] for x in red), 'T00–T11 retained')
    check('disposition_enum', all(x['disposition'] in {'retained','revised','merged','removed-from-scope','deferred-after-seam'} for x in red), 'Explicit scope dispositions')
    cross = read(R3 / '04_ORIGINAL_25_PACKAGE_CROSSWALK.json')
    original_path = 'PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/TASKS.json'
    original = json.loads(git('show', ORIGINAL + ':' + original_path))
    tasks = {x['id']: x for x in original['tasks']}
    check('all25_original_objects_exact', len(cross['rows']) == 25 and {x['original_id'] for x in cross['rows']} == set(tasks) and all(x['original_task_exact'] == tasks[x['original_id']] for x in cross['rows']), 'Compared directly with original baseline Git object')
    check('original_conditional_edges_exact', cross['original_conditional_edges_exact'] == original['conditional_edges'], 'Original conditional edges preserved as history')
    check('all35_sources_exact', cross['all35']['original_exact'] == read(R2 / 'SOURCE35_RETAINED.json')['original_exact'], 'Entire inherited source object unchanged')
    source_baseline = json.loads(git('show', ORIGINAL + ':PYAT_CONTROL_ROOM/WHOLE_MACHINE_ASSESSMENT_AND_PLAN_20261011_R1/SOURCE35_RECONCILIATION.json'))
    check('all35_matches_original_git', cross['all35']['original_exact'] == source_baseline, 'Source queue compared with exact October 11 baseline')
    source_ids = {x['source_id'] for x in cross['all35']['original_exact']['sources']}
    check('all35_active_routes', len(source_ids) == 35 and len(cross['all35']['source_obligations']) == 35 and {x['source_id'] for x in cross['all35']['source_obligations']} == source_ids, 'Per-source obligation routes retained')
    for key, count, prefix in [('functional_gates', 8, 'F'), ('acceptance_cases', 35, 'AT')]:
        rows = cross[key]
        expected = {f'{prefix}{i:02d}' if prefix == 'AT' else f'{prefix}{i}' for i in range(1, count+1)}
        check(key+'_identities', len(rows) == count and {x['id'] for x in rows} == expected, count)
        check(key+'_original_definitions_exact', all(git('show', x['original_ref']).decode() == x['original_definition_exact'] for x in rows), 'Compared with original commit, not generated summaries')
    methods = read(R3 / 'METHOD_REDISPOSITION.json')['rows']
    m2 = {x['id']: x for x in read(R2 / 'METHOD_LEDGER.json')['methods']}
    check('all15_methods_exact', len(methods) == 15 and {x['id'] for x in methods} == set(m2) and all(x['r2_exact'] == m2[x['id']] for x in methods), 'Comparisons, fallbacks and evidence preserved')
    lm = read(R3 / 'LONG_MEMORY_REDISPOSITION.json')['rows']
    l2 = {x['id']: x for x in read(R2 / 'LONG_MEMORY_CROSSWALK.json')['rows']}
    check('all74_long_memory_exact', len(lm) == 74 and {x['id'] for x in lm} == set(l2) and all(x['r2_row_exact'] == l2[x['id']] for x in lm), '44 LMX + 30 LMQ')
    routes = [x['r3_tasks'] for x in red + cross['rows'] + cross['functional_gates'] + cross['acceptance_cases'] + methods]
    routes += [x['r3_review_routes'] for x in lm]
    check('all_crosswalk_routes_exist', all(set(x) <= ids for x in routes), 'No stale T IDs in active routes')
    check('r2_files_unchanged', all(git('show', BASE + ':' + str(f.relative_to(ROOT))) == f.read_bytes() for f in R2.iterdir() if f.is_file()), 'Every inherited R2 artifact byte-identical')
    ev = read(R3 / 'EVIDENCE_VERIFICATION.json')
    check('178_inherited_evidence_identities', len(ev['inherited_git_object_checks']) == 178 and all(x['matches_inherited'] for x in ev['inherited_git_object_checks']), 'Recorded fresh Git blob/SHA-256/length verification; no semantic review claim')
    probe = read(R3 / 'repro/seam_contract_probe_result.json')
    check('source_free_probe_cases', len(probe['cases']) == 10 and all(x['status'] == 'PASS_SOURCE_FREE_ONLY' for x in probe['cases']) and not probe['v3_executed'] and not probe['real_source_evidence'], '10 author-run source-free case groups')
    tree = ast.parse((R3 / 'repro/seam_contract_probe.py').read_text())
    imports = {n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)} | {a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    check('probe_standard_library_only', imports <= {'hashlib', 'json', 'pathlib'}, sorted(imports))
    modified = git('diff', '--name-only', BASE).decode().splitlines()
    untracked = git('ls-files', '--others', '--exclude-standard').decode().splitlines()
    prefix = str(R3.relative_to(ROOT)) + '/'
    check('only_r3_terrain_changed', all(x.startswith(prefix) for x in modified + untracked), 'Canonical/production/R2/HQ_HANDOFF unchanged')
    result = {'schema':'R3_DOCUMENTARY_VERIFICATION', 'status':'PASS_AUTHOR_CHECKS_ONLY',
              'checked_base': BASE, 'checks':checks, 'independent_review':False,
              'production_tests_executed':False, 'source_data_runs':0, 'v3_runs':0,
              'scope':'Artifact conservation and synthetic acceptance oracle; not full PRE-V3 qualification'}
    (R3 / 'VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n')
    print(f'{len(checks)} artifact checks passed; no production/source/V3 execution.')


if __name__ == '__main__':
    run()
