#!/usr/bin/env python3
"""R10 PV2 full reproduction: precommit, then every graded suite.

Usage: PV2_RUNTIME_ROOT=<staged runtime> python3 repro/run_pv2_suites.py

The pinned accepted owners and V2-chain candidates are staged from the pinned
runtime commit 3f91dc22d2eb863bc1d2facccfd33e6c05349503; the register is
precommitted to freezes/ before any owner execution.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPRO = RETURN / 'repro'
RUNTIME = Path(os.environ.get('PV2_RUNTIME_ROOT', '')).resolve()
RESULTS = RETURN / 'observations'
# The frozen independent PV court's return, staged beside the pinned runtime so
# its immutable oracle file can be read back by its own tests.
RETURN_WORKER = Path(os.environ.get('PV_RETURN_ROOT', str(RUNTIME / 'WORKER_RETURNS')))
PY = sys.executable


def run(label, argv, env):
    started = time.time()
    proc = subprocess.run(argv, cwd=RUNTIME, env=env, capture_output=True, text=True)
    elapsed = round(time.time() - started, 2)
    log = RESULTS / f'{label}.log'
    log.write_text(
        f'# command: {" ".join(argv)}\n# cwd: {RUNTIME}\n'
        f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
        f'{proc.stdout}\n{proc.stderr}\n')
    print(f'{label:<28} exit={proc.returncode} elapsed={elapsed}s')
    return proc.returncode


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    if not RUNTIME.is_dir():
        raise SystemExit('PV2_RUNTIME_ROOT must point at the staged pinned runtime')
    env = dict(os.environ)
    sep = os.pathsep
    env['PYTHONPATH'] = sep.join(
        [str(RUNTIME), str(REPRO), str(RETURN / 'tests')])
    env['PV2_RUNTIME_ROOT'] = str(RUNTIME)
    env['PV_RETURN'] = str(RETURN_WORKER)

    # Stage the return's own sourcefree code into the runtime import root.
    for name in ('pv2_original_scope_register.py', 'pv2_sourcefree_fixture.py'):
        shutil.copy2(REPRO / name, RUNTIME / name)

    codes = {}

    # 0. Precommit the independently authored register BEFORE any owner call.
    codes['precommit'] = run(
        'precommit_register',
        [PY, str(REPRO / 'emit_pv2_register.py')], env)

    junits = {
        'pv2_hostiles': [str(RETURN / 'tests' / 'test_pv2_original_scope_binding.py')],
        'v2k_author_baseline': ['rawlsing_next/tests/test_hq295_v2k_original_identity_successor.py'],
        'pv_21_diagnostics': ['rawlsing_next/tests/test_postastra_pv_v2k_independent.py'],
    }
    for label, targets in junits.items():
        codes[label] = run(
            label,
            [PY, '-m', 'pytest', '-q', *targets,
             '--import-mode=importlib', '-p', 'no:cacheprovider',
             f'--junitxml={RESULTS / f"{label}.xml"}'], env)

    owners = [
        'rawlsing_next/tests/test_pre553_v2_durable_consumer_integration_candidate.py',
        'rawlsing_next/tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py',
        'rawlsing_next/tests/test_pre553_route_b_production.py',
        'rawlsing_next/tests/test_pre553_empirical_query.py',
        'rawlsing_next/tests/test_pre553_discovery_exact.py',
    ]
    codes['owner_suites'] = run(
        'owner_suites',
        [PY, '-m', 'pytest', '-q', *owners,
         '--import-mode=importlib', '-p', 'no:cacheprovider',
         f'--junitxml={RESULTS / "owner_suites.xml"}'], env)

    # Genuinely separate Python processes: first, then cold replay.
    cold_root = RESULTS.parent / '.cold-runtime'
    cold_root.mkdir(parents=True, exist_ok=True)
    for outcome, mode in (('cold_first', 'first'), ('cold_replay', 'replay')):
        codes[outcome] = run(
            outcome,
            [PY, str(REPRO / 'pv2_cold_process.py'), str(RETURN), str(cold_root), mode],
            env)
        shutil.copy2(cold_root / 'observations' / f'{mode}.json',
                     RESULTS / f'cold_{mode}.json')
        shutil.copy2(cold_root / 'observations' / 'expected_before_production.json',
                     RESULTS / 'expected_before_production.json')
        shutil.copy2(cold_root / 'observations' / 'register_before_production.json',
                     RESULTS / 'register_before_production.json')
    codes['cold_replay'] = 0 if codes['cold_first'] == 0 and \
        codes['cold_replay'] == 0 else 1

    print('\n--- summary ---')
    for label, code in codes.items():
        print(f'{label:<28} exit={code} {"PASS" if code == 0 else "FAIL"}')
    return 0 if all(c == 0 for c in codes.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
