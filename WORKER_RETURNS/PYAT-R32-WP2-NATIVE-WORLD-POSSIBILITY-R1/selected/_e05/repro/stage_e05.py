#!/usr/bin/env python3
"""Stage the exact bounded closure R11 E05 runs against.

The accepted owner trees on disk are byte-identical to the pinned cut, so they
are copied (never edited).  Everything that is NOT on the startup tree is
materialised from its own sealed commit and verified blob-for-blob.

Usage: PV2_RUNTIME_ROOT=<dir> python3 repro/stage_e05.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path('/Users/matthewsmith/Desktop/Rawlsing')
RT = Path(os.environ.get('PV2_RUNTIME_ROOT', '/tmp/e05-runtime')).resolve()
E04 = '9c96f201f3530d2dae321201e9a913bb7a61800f'
E03 = '0e0ed50dbce2dd1434d3a3c84b937b9a956adba9'
N9C = '9ab4a0192b7c951bb0b387637e6c74333246766c'
E04_PREFIX = 'WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1/'

# Sealed-by-commit objects that are absent from the startup tree.
OVERRIDES = {
    'rawlsing_next/pre553_n9_n10w_progressive_candidate.py': E03,
    'rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py': E03,
    'rawlsing_next/pre553_hq297_n9c_two_field_reader.py': N9C,
    'tests/test_hq297_n9c_two_field_reader.py': N9C,
    'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json': N9C,
}

# Oracle / canonical fixtures the accepted owner suites read from disk.
ORACLES = [
    'WORKER_RETURNS/PYAT-AT07-SUCCESSOR-SPINE-INDEPENDENT-FREEZE-R1',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R2',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R3',
    'WORKER_RETURNS/PYAT-C1-00-CONTRACT-CORRECTION-R8',
]

if RT.exists():
    shutil.rmtree(RT)


def blob(commit, path):
    out = subprocess.check_output(['git', 'ls-tree', commit, path],
                                  cwd=REPO).decode().strip()
    return out.split()[2] if out else None


manifest = []

# 1. Accepted owner trees, exact copies (never edited).
for tree in ('rawlsing_next', 'tests'):
    shutil.copytree(REPO / tree, RT / tree,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'fixtures'))

# 2. Sealed-by-commit objects, verified blob-for-blob.
for rel, commit in OVERRIDES.items():
    raw = subprocess.check_output(['git', 'show', f'{commit}:{rel}'], cwd=REPO)
    dest = RT / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    row = dict(commit=commit, path=rel, sha1=hashlib.sha1(raw).hexdigest(),
               git_blob=blob(commit, rel))
    manifest.append(row)
    assert row['sha1'] == hashlib.sha1(raw).hexdigest()

# 3. Oracle / canonical fixtures from the repo's tracked returns.
for root in ORACLES:
    source_dir = REPO / root
    for rel in sorted(source_dir.glob('*.json')):
        repo_rel = (source_dir / rel.name).relative_to(REPO).as_posix()
        dest = RT / repo_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rel, dest)
        manifest.append(dict(commit='STARTUP_TREE', path=repo_rel,
                             sha1=hashlib.sha1(rel.read_bytes()).hexdigest(),
                             git_blob=subprocess.check_output(
                                 ['git', 'hash-object', str(rel)],
                                 cwd=REPO).decode().strip()))

# 4. E04's sealed candidate product package, byte-identical to its commit.
product = [r for r in subprocess.check_output(
    ['git', 'ls-tree', '-r', '--name-only', E04], cwd=REPO).decode().split()
    if r.startswith(E04_PREFIX + 'product/')]
for rel in product:
    raw = subprocess.check_output(['git', 'show', f'{E04}:{rel}'], cwd=REPO)
    short = rel[len(E04_PREFIX):]
    dest = RT / short
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    manifest.append(dict(commit=E04, path=short, sha1=hashlib.sha1(raw).hexdigest(),
                         git_blob=blob(E04, rel)))
    assert subprocess.check_output(['git', 'hash-object', str(dest)]
                                   ).decode().strip() == blob(E04, rel)

# 5. E04's sealed candidate author suite, in its own prefix (never edited).
stg = RT / '_e04-candidate'
(stg / 'repro').mkdir(parents=True, exist_ok=True)
(stg / 'runtime_root' / 'source').mkdir(parents=True, exist_ok=True)
for name in ('rawlsing_next', 'tests'):
    (stg / 'runtime_root' / 'source' / name).symlink_to(RT / name)
(stg / 'product').symlink_to(RT / 'product')
raw = subprocess.check_output(
    ['git', 'show', f'{E04}:{E04_PREFIX}repro/test_product.py'], cwd=REPO)
(stg / 'repro' / 'test_product.py').write_bytes(raw)
manifest.append(dict(commit=E04, path='_e04-candidate/repro/test_product.py',
                     sha1=hashlib.sha1(raw).hexdigest(),
                     git_blob=blob(E04, E04_PREFIX + 'repro/test_product.py')))
assert subprocess.check_output(['git', 'hash-object', str(stg / 'repro' / 'test_product.py')]
                               ).decode().strip() == blob(E04, E04_PREFIX +
                                                         'repro/test_product.py')

(RT / 'source_manifest.json').write_text(
    json.dumps(sorted(manifest, key=lambda r: r['path']), indent=2) + '\n')
print('staged runtime:', RT)
print('sealed objects staged:', len(manifest))
for row in manifest:
    print(' ', row['commit'][:9], row['git_blob'][:12], row['path'])
