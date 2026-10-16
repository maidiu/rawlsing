#!/usr/bin/env python3
"""Stage the exact OC4 executable closure, verified blob-for-blob.

Every object is materialised from its own sealed Git commit and its Git blob
SHA1 is checked against the commission pin before any test runs.  Nothing is
hand-transcribed.
"""
from __future__ import annotations

import hashlib
import json
import lzma
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path('/Users/matthewsmith/Desktop/Rawlsing')
RT = Path(sys.argv[1])
RETURN = REPO / 'WORKER_RETURNS/SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1'

OC4 = '0caaec590f6a8bf6744f22dc9c948c5fe233bc94'
OC1 = '19438890e43153e2bc4a1ad271b5e19bcef33e1e'
OCR1 = 'aba637265bea2358790fea50d0e7abc98141e472'
OC2 = 'a61d5794271038fb20c94a75eaee401a66613ce9'
OC3 = '9cd47a829473a6e92392582b4f01f2c564aa5dce'
OC5 = '8185d2ca41ac5c5711b3f3f528e6f644dbab185d'

# (commit, repo path, expected git blob SHA1, staged name)
STAGED = [
    # THE SOURCE UNDER REVIEW — the pinned OC4 native blob.
    (OC4, 'WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/custody_protocol.py',
     'af2b7e943018077cb36808b5af1cd67704624bec', 'source/custody_protocol.py'),
    (OC4, 'WORKER_RETURNS/SOROK-R3-HQ310-OC4-CUSTODY-TEN-RED-REPAIR-R1/repro/test_oc4_repair_controls.py',
     'c139a877aa4586ec5ab729d333c40037840721d4', 'source/test_oc4_repair_controls.py'),
    # OC1 author court (31) plus the OC1 module + corpus it exercises.
    (OC1, 'WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_custody_hostiles.py',
     '94ad944997cb9d1a8d6527e91c17416120c5108d', 'source/test_custody_hostiles.py'),
    (OC1, 'WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/test_positive_lifecycle.py',
     '4b665a2a9d6999071624d580f2d2ae193daf59f4', 'source/test_positive_lifecycle.py'),
    (OC1, 'WORKER_RETURNS/SOROK-R3-HQ306-OC1-ORACLE-CUSTODY-READINESS-R1/repro/dummy_corpus.py',
     '770efe72190e35d1bc34065b5a55c183bf1320f5', 'source/dummy_corpus.py'),
    # OC2 regression court (19).
    (OC2, 'WORKER_RETURNS/SOROK-R3-HQ308-OC2-CUSTODY-RED-REPAIR-R1/repro/test_oc2_regressions.py',
     '402f04ef7d6b8119f72df9355b554e797b9a501e', 'source/test_oc2_regressions.py'),
]


def git_blob(commit, path):
    out = subprocess.check_output(['git', 'ls-tree', commit, path],
                                   cwd=REPO).decode().strip()
    return out.split()[2] if out else None


def git_raw(commit, path):
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=REPO)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


manifest = []

for commit, path, expected, staged_name in STAGED:
    actual = git_blob(commit, path)
    assert actual == expected, f'BLOB MISMATCH {path}: {actual} != {expected}'
    raw = git_raw(commit, path)
    dest = RT / staged_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(raw)
    # The staged bytes must hash to exactly the same git blob.
    assert subprocess.check_output(['git', 'hash-object', str(dest)]).decode().strip() == expected
    manifest.append(dict(commit=commit, path=path, git_blob=expected,
                         sha256=sha256(raw), staged=staged_name,
                         bytes=len(raw)))

# OCR1 (45) and OC3 (36) courts live inside sealed tar.xz evidence archives.
archives = [
    (OCR1, 'WORKER_RETURNS/SOROK-R3-HQ307-OCR1-CUSTODY-HOSTILE-INDEPENDENT-R1/OCR1_EXECUTED_EVIDENCE.tar.xz',
     '9725b39e0e7f5cf98f94c090bbf84428b29eed2c',
     'source/test_ocr1_independent_hostile.py', 'source/test_ocr1_independent_hostile.py'),
    (OC3, 'WORKER_RETURNS/SOROK-R3-HQ309-OC3-CUSTODY-INDEPENDENT-R1/OC3_REMOTE_CORE_EVIDENCE.tar.xz',
     '068b158363b96d5a7cdc03eb059efb8a8d159b26',
     'source/test_oc3_independent_hostile.py', 'source/test_oc3_independent_hostile.py'),
]
for commit, path, expected_archive, inner, staged_name in archives:
    actual_archive = git_blob(commit, path)
    assert actual_archive == expected_archive, f'ARCHIVE MISMATCH {path}'
    raw = git_raw(commit, path)
    buf = __import__('io').BytesIO(raw)
    with tarfile.open(fileobj=buf, mode='r:xz') as tar:
        members = {m.name: m for m in tar.getmembers()}
        assert inner in members, f'missing {inner} in {path}: {sorted(members)}'
        payload = tar.extractfile(members[inner]).read()
    dest = RT / staged_name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(payload)
    manifest.append(dict(commit=commit, path=path + '!' + inner,
                         git_blob=expected_archive + ' (archive)',
                         sha256=sha256(payload), staged=staged_name,
                         bytes=len(payload)))

# The prior OC5 partial review's committed falsifiers, kept as disclosed input.
oc5_path = 'WORKER_RETURNS/SOROK-R3-HQ311-OC5-OC4-INDEPENDENT-R1/03_TESTS/test_oc5_candidate_hostiles.py'
raw = git_raw(OC5, oc5_path)
(RT / 'source' / 'test_oc5_prior_predictions.py').write_bytes(raw)
manifest.append(dict(commit=OC5, path=oc5_path, git_blob=git_blob(OC5, oc5_path),
                     sha256=sha256(raw), staged='source/test_oc5_prior_predictions.py',
                     bytes=len(raw)))

(RETURN / 'freezes' / '01_STAGED_SOURCE_MANIFEST.json').write_text(
    json.dumps(sorted(manifest, key=lambda r: r['staged']), indent=2) + '\n')
print('staged', len(manifest), 'objects into', RT)
for row in manifest:
    print(' ', row['git_blob'][:12], row['bytes'], row['staged'])
