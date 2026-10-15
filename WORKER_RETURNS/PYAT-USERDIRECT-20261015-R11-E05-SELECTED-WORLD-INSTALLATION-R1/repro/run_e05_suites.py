#!/usr/bin/env python3
"""R11 E05: precommit, execute every graded suite, keep immutable owners sealed.

Run from the repo root with the staged pinned runtime:

    PV2_RUNTIME_ROOT=<staged> python3 repro/run_e05_suites.py
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
PY = sys.executable

E04_CANDIDATE = '_e04-candidate/repro/test_product.py'
SUITES = [
    ('precommit_expected_values', [PY, str(REPRO / 'emit_e05_expected.py')], 'script'),
    ('e05_adapter_tests', [PY, '-m', 'pytest', '-q',
                           str(RETURN / 'tests' / 'test_e05_n9_selected_world.py'),
                           '--import-mode=importlib', '-p', 'no:cacheprovider'], 'pytest'),
    # Immutable sealed E04 candidate suite (not independently accepted).
    ('e04_candidate_baseline', [PY, '-m', 'pytest', '-q', E04_CANDIDATE,
                                '--import-mode=importlib', '-p', 'no:cacheprovider'],
     'pytest'),
    # Exact accepted-owner suites.
    ('n9c_owner_reader', [PY, '-m', 'pytest', '-q',
                          'tests/test_hq297_n9c_two_field_reader.py',
                          '--import-mode=importlib', '-p', 'no:cacheprovider'], 'pytest'),
    ('m4_m5_owner_publication', [PY, '-m', 'pytest', '-q',
                                 'rawlsing_next/tests/test_m4_v557_v558_publication_repository.py',
                                 'rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py',
                                 '--import-mode=importlib', '-p', 'no:cacheprovider'],
     'pytest'),
    ('empirical_owner_chains', [PY, '-m', 'pytest', '-q',
                                'rawlsing_next/tests/test_pre553_empirical_possibility_provider.py',
                                'rawlsing_next/tests/test_pre553_analytical_composition.py',
                                'rawlsing_next/tests/test_source_backed_positioned_subject_possibility.py',
                                'rawlsing_next/tests/test_pre553_empirical_query.py',
                                '--import-mode=importlib', '-p', 'no:cacheprovider'],
     'pytest'),
    ('e03_n9_n10w_progressive', [PY, '-m', 'pytest', '-q',
                                 'rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py',
                                 '--import-mode=importlib', '-p', 'no:cacheprovider'],
     'pytest'),
]


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    if not RUNTIME.is_dir():
        raise SystemExit('PV2_RUNTIME_ROOT must point at the staged pinned runtime')
    env = dict(os.environ)
    sep = os.pathsep
    env['PYTHONPATH'] = sep.join(
        [str(RUNTIME), str(REPRO), str(RUNTIME / 'rawlsing_next' / 'tests'),
         str(RUNTIME / 'rawlsing_next')])
    env['PV2_RUNTIME_ROOT'] = str(RUNTIME)

    for name in ('e05_n9_selected_world_adapter.py',):
        shutil.copy2(REPRO / name, RUNTIME / name)

    codes: dict = {}
    for label, argv, kind in SUITES:
        started = time.time()
        proc = subprocess.run(argv, cwd=RUNTIME, env=env,
                              capture_output=True, text=True)
        elapsed = round(time.time() - started, 2)
        (RESULTS / f'{label}.log').write_text(
            f'# command: {" ".join(argv)}\n# cwd: {RUNTIME}\n'
            f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
            f'{proc.stdout}\n{proc.stderr}\n')
        if kind == 'pytest':
            argv = [*argv, f'--junitxml={RESULTS / f"{label}.xml"}']
            proc = subprocess.run(argv, cwd=RUNTIME, env=env,
                                  capture_output=True, text=True)
            elapsed = round(time.time() - started, 2)
            (RESULTS / f'{label}.log').write_text(
                f'# command: {" ".join(argv)}\n# cwd: {RUNTIME}\n'
                f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
                f'{proc.stdout}\n{proc.stderr}\n')
        codes[label] = proc.returncode
        print(f'{label:<28} exit={proc.returncode} elapsed={elapsed}s')

    # Genuinely separate Python processes: first, then fresh-interpreter replay.
    cold_root = RESULTS.parent / '.cold-runtime'
    cold_root.mkdir(parents=True, exist_ok=True)
    for outcome, mode in (('cold_first', 'first'), ('cold_replay', 'replay')):
        argv = [PY, str(REPRO / 'e05_cold_process.py'), str(RUNTIME),
                str(cold_root), mode]
        started = time.time()
        proc = subprocess.run(argv, cwd=RUNTIME, env=env,
                              capture_output=True, text=True)
        elapsed = round(time.time() - started, 2)
        (RESULTS / f'{outcome}.log').write_text(
            f'# command: {" ".join(argv)}\n# cwd: {RUNTIME}\n'
            f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
            f'{proc.stdout}\n{proc.stderr}\n')
        codes[outcome] = proc.returncode
        print(f'{outcome:<28} exit={proc.returncode} elapsed={elapsed}s')
        for name in (f'{mode}.json', 'precommitted_before_serving.json'):
            shutil.copy2(cold_root / 'observations' / name,
                         RESULTS / f'cold_{name}')
    codes['cold_replay'] = 0 if codes['cold_first'] == 0 and \
        codes['cold_replay'] == 0 else 1

    print('\n--- summary ---')
    for label, code in codes.items():
        print(f'{label:<28} exit={code} {"PASS" if code == 0 else "FAIL"}')
    return 0 if all(c == 0 for c in codes.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
