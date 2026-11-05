import json, os, pathlib, shutil, subprocess
root = pathlib.Path('/tmp/rawlsing-oct28-p1f1')
source = pathlib.Path('/Users/matthewsmith/.codex/worktrees/f935/Rawlsing/WORKER_RETURNS/PROGRAMMA-OCT28-P1R1-20261104-R1')
packet = root / 'packet'
shutil.copytree(source, packet, dirs_exist_ok=True)
shutil.copytree(source / 'inputs', root / 'inputs', dirs_exist_ok=True)
# The reviewer reflected dataclass storage. Check the documented public handoff
# instead now that the compact implementation stores identity primitives privately.
p = packet / 'test_independent_review.py'
body = p.read_text().replace('from types import MappingProxyType', 'from types import MappingProxyType, SimpleNamespace')
fields = ('ref', 'typed_state', 'native_question_ref', 'canonical_question_ref_if_authorized', 'component_or_subitem_ref', 'authority_snapshot_refs', 'raw_response_value', 'canonical_response_value_if_authorized', 'multiplicity_order_rank_fields', 'response_event_id_or_deterministic_index')
body = body.replace('for f in fields(selected):', f'for f in (SimpleNamespace(name=name) for name in {fields!r}):')
p.write_text(body)
python = '/tmp/rawlsing-oct28-p1r1/venv/bin/python'
env = dict(os.environ, PATH='/tmp/rawlsing-oct28-p1r1/venv/bin:' + os.environ['PATH'], PYTHONPATH='.' + os.pathsep + str(packet), PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1', LC_ALL='C')
base = [python, '-m', 'pytest']
opts = ['-q', '-o', 'addopts=', '-p', 'no:cacheprovider']
focused = ['rawlsing_next/tests/test_pre553_c11_execution_view.py', 'rawlsing_next/tests/test_pre553_route_b_production.py', 'rawlsing_next/tests/test_pre553_source_backed_c11_facade.py', 'rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_r1.py', 'rawlsing_next/tests/test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py']
forced = ['rawlsing_next/tests/test_pre553_empirical_query.py', 'rawlsing_next/tests/test_pre553_query_frontier_hostile.py', 'rawlsing_next/tests/test_pre553_discovery_exact.py']
commands = [
 ('selector-integrity-GREEN', base + [str(source / 'test_selector_ref_integrity.py')] + opts),
 ('related-suite', ['bash', str(root / 'inputs/related-suite-command.sh')]),
 ('focused', base + focused + opts),
 ('independent-tests', base + [str(p)] + opts + ['-s']),
 ('forced-compact', base + forced + ['-p', 'force_compact'] + opts),
 ('cache-red-restore', [python, str(source / 'cache_red_restore.py')]),
 ('p41-first-consumer', base + ['rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41'] + opts),
 ('selector-alias-fixed-original-probe', [python, str(source / 'probe_selector_ref_alias.py')]),
]
results = []
for label, argv in commands:
    active_env = dict(env)
    if label == 'p41-first-consumer':
        active_env['RAWLSING_C11_ACCELERATOR_DIR'] = str(root / 'p41-cache')
    with (root / f'{label}.log').open('w') as output:
        completed = subprocess.run(argv, env=active_env, stdout=output, stderr=subprocess.STDOUT)
    entry = dict(label=label, argv=argv, exit_code=completed.returncode)
    if label == 'selector-alias-fixed-original-probe':
        entry['expected_exit'] = 1
        entry['secure_result'] = 'no exercised selector changed a downstream fact' in (root / f'{label}.log').read_text()
    results.append(entry)
    (root / 'validation.json').write_text(json.dumps(results, indent=2))
    print(json.dumps(entry), flush=True)
