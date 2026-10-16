#!/usr/bin/env python3
"""OC6 — one-shot reproducible pipeline: stage, before, repair, after, adjudicate.

    PV2_RUNTIME_ROOT=<dir> python3 repro/reproduce.py

Phase 1 stages the sealed closure (blob verified) and runs the UNCHANGED
349-case court against the unrepaired pinned blob.
Phase 2 applies the A1-A6 repairs to the staged copy and re-runs the identical
349-case court plus the new OC6 author controls.
Phase 3 writes the per-case adjudication and the sanitized 00D passport.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPRO = RETURN / 'repro'
RUNTIME = Path(os.environ.get('PV2_RUNTIME_ROOT', '/tmp/oc6-runtime')).resolve()
PY = sys.executable
PINNED = '0caaec590f6a8bf6744f22dc9c948c5fe233bc94'
PINNED_PATH = ('WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/'
               'repro/custody_protocol.py')


def run(label, argv, **kw):
    proc = subprocess.run(argv, capture_output=True, text=True, **kw)
    print(f'{label:<26} exit={proc.returncode}')
    if proc.returncode not in (0, 1):
        print(proc.stdout[-3000:])
        print(proc.stderr[-3000:])
        raise SystemExit(f'{label} failed with exit {proc.returncode}')
    return proc


def main() -> int:
    env = dict(os.environ)
    env['PV2_RUNTIME_ROOT'] = str(RUNTIME)

    print('=== phase 1: stage sealed closure + BEFORE (unrepaired pinned blob) ===')
    run('stage_source', [PY, str(REPRO / 'stage_source.py'), str(RUNTIME)], env=env)
    subprocess.run(['git', 'show', f'{PINNED}:{PINNED_PATH}'],
                   cwd='/Users/matthewsmith/Desktop/Rawlsing',
                   stdout=(RUNTIME / 'source' / 'custody_protocol.py').open('wb'),
                   check=True)
    assert subprocess.check_output(
        ['git', 'hash-object', str(RUNTIME / 'source' / 'custody_protocol.py')]
    ).decode().strip() == 'af2b7e943018077cb36808b5af1cd67704624bec'
    run('court before', [PY, str(REPRO / 'run_court.py'), 'before'], env=env)
    # Preserve the BEFORE phase separately: adjudicate.py and build_passport.py
    # compare the unrepaired pinned-blob run against the repaired run.
    stash = Path('/tmp/oc6-before/observations')
    if stash.exists():
        import shutil
        shutil.rmtree(Path('/tmp/oc6-before'))
    stash.mkdir(parents=True, exist_ok=True)
    for src in sorted((RETURN / 'observations').iterdir()):
        (stash / src.name).write_bytes(src.read_bytes())

    print('\n=== phase 2: apply A1-A6 repairs + AFTER ===')
    run('apply_repair', [PY, str(REPRO / 'apply_repair.py')], env=env)
    run('court after', [PY, str(REPRO / 'run_court.py'), 'after'], env=env)

    print('\n=== phase 3: adjudicate + passport ===')
    run('adjudicate', [PY, str(REPRO / 'adjudicate.py')])
    run('build_passport', [PY, str(REPRO / 'build_passport.py'), str(RUNTIME),
                           str(RETURN)], env=env)
    print('\n--- repair complete ---')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
