#!/usr/bin/env python3
"""OC6 — execute the full unchanged 349-case court and record per-case evidence.

    PV2_RUNTIME_ROOT=<staged> python3 repro/run_court.py <label>

<label> is `before` or `after`.  The four courts are byte-identical in both
phases; only the repaired source under `source/custody_protocol.py` differs.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
RUNTIME = Path(os.environ.get('PV2_RUNTIME_ROOT', '/tmp/oc6-runtime')).resolve()
SOURCE = RUNTIME / 'source'
PY = sys.executable
LABEL = sys.argv[1] if len(sys.argv) > 1 else 'before'
# Each phase owns its own subdirectory so the AFTER rerun can never overwrite
# the preserved BEFORE JUnit/stdout evidence.
RESULTS = RETURN / 'observations' / LABEL

COURTS = [
    ('inherited_131', 'inherited_131.xml',
     ['test_custody_hostiles.py', 'test_positive_lifecycle.py',
      'test_ocr1_independent_hostile.py', 'test_oc2_regressions.py',
      'test_oc3_independent_hostile.py'],
     'original inherited 131: expected 121 PASS / 10 historical RED'),
    ('oc4_new_36', 'oc4_new_36.xml', ['test_oc4_repair_controls.py'],
     'OC4 author new controls: expected 36 PASS'),
    ('oc5e_native_hostiles', 'oc5e_native_hostiles.xml',
     ['test_oc5e_native_hostiles.py'],
     'OC5E independently authored native hostiles'),
    ('oc5_prior_predictions', 'oc5_prior_predictions.xml',
     ['test_oc5_prior_predictions.py'],
     'OC5 disclosed prior predictions'),
]

# The OC6 author controls are a post-repair addition and are graded only in the
# AFTER phase, so the unchanged 349-case court stays byte-identical in both
# phases (before: unrepaired pinned blob; after: repaired blob).
if LABEL == 'after':
    COURTS.append((
        'oc6_author_controls', 'oc6_author_controls.xml',
        ['test_oc6_input_contract_controls.py'],
        'OC6 author-side targeted controls (new)'))

FAMILY = (
    ('normalization_equivalent', 'A1_normalization_equivalent_allowed_field_alias'),
    ('confusable_leak_token', 'A2_nfkc_invisible_confusable_leak_token'),
    ('malformed_signature_object', 'A3_malformed_signature_object_untyped'),
    ('non_enum_role', 'A4_non_enum_role_string_untyped'),
    ('unhashable_holder', 'A5_unblind_unhashable_holder_untyped'),
    ('capsule_identity_field_types', 'A6_capsule_identity_field_types_unvalidated'),
    ('semantic_fingerprint', 'A6_capsule_identity_field_types_unvalidated'),
)


def family_of(name):
    for needle, family in FAMILY:
        if needle in name:
            return family
    return 'other'


def cases(junit):
    root = ET.parse(RESULTS / junit).getroot()
    suite = root.find('testsuite') if root.tag == 'testsuites' else root
    out = []
    for tc in suite.iter('testcase'):
        fail = next((k for k in tc if k.tag in ('failure', 'error')), None)
        out.append(dict(
            name=tc.get('name'),
            cls=(tc.get('classname') or '').split('.')[-1],
            outcome='FAIL' if fail is not None else 'PASS',
            type=(fail.get('type') if fail is not None else None),
            reason=((fail.get('message') or '').strip()[:200]
                    if fail is not None else None)))
    return out


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env['PYTHONPATH'] = str(SOURCE)

    codes = {}
    tallies = []
    matrix = {}
    for label, junit, files, grade in COURTS:
        argv = [PY, '-m', 'pytest', '-q', *files, '--tb=line',
                '-p', 'no:cacheprovider', '--import-mode=importlib',
                f'--junitxml={RESULTS / junit}']
        started = time.time()
        proc = subprocess.run(argv, cwd=SOURCE, env=env,
                              capture_output=True, text=True)
        elapsed = round(time.time() - started, 2)
        (RESULTS / f'{label}.log').write_text(
            f'# phase: {LABEL}\n# command: {" ".join(argv)}\n# cwd: {SOURCE}\n'
            f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
            f'{proc.stdout}\n{proc.stderr}\n')
        codes[label] = proc.returncode
        row = cases(junit)
        matrix[label] = row
        passed = sum(1 for c in row if c['outcome'] == 'PASS')
        failed = sum(1 for c in row if c['outcome'] == 'FAIL')
        tallies.append(dict(label=label, junit=junit, grade=grade,
                            tests=len(row), passed=passed, failed=failed,
                            errors=0, skipped=0, seconds=elapsed))
        print(f'{label:<22} exit={proc.returncode} tests={len(row)} '
              f'pass={passed} fail={failed} ({elapsed}s)')

    reds = [c for label in matrix for c in matrix[label] if c['outcome'] == 'FAIL']
    families = {}
    for c in reds:
        families.setdefault(family_of(c['name']), []).append(c['name'])

    # source identity of what was actually imported
    probe = subprocess.run(
        [PY, '-c',
         'import sys,hashlib,subprocess;sys.path.insert(0,%r);'
         'import custody_protocol as CP;'
         'print(CP.__file__);'
         'print(subprocess.check_output(["git","hash-object",CP.__file__]).decode().strip());'
         'print(hashlib.sha256(open(CP.__file__,"rb").read()).hexdigest())' % str(SOURCE)],
        cwd=SOURCE, env=env, capture_output=True, text=True)
    module_path, staged_blob, staged_sha256 = probe.stdout.strip().split('\n')

    payload = dict(
        phase=LABEL,
        source_under_test=dict(
            pinned_commit='0caaec590f6a8bf6744f22dc9c948c5fe233bc94',
            pinned_git_blob_sha1='af2b7e943018077cb36808b5af1cd67704624bec',
            pinned_sha256='447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662e56f846f9e3a',
            imported_module_path=module_path,
            staged_git_blob_sha1=staged_blob,
            staged_sha256=staged_sha256,
            is_pinned_blob=staged_blob == 'af2b7e943018077cb36808b5af1cd67704624bec'),
        courts=tallies,
        totals=dict(cases=sum(t['tests'] for t in tallies),
                    passed=sum(t['passed'] for t in tallies),
                    failed=sum(t['failed'] for t in tallies),
                    errors=sum(t['errors'] for t in tallies),
                    skipped=sum(t['skipped'] for t in tallies)),
        reds=[dict(case=c['name'], family=family_of(c['name']), observed=c['reason'])
              for c in reds],
        red_family_counts={k: len(v) for k, v in sorted(families.items())},
        matrix=matrix)
    (RESULTS / f'case_matrix_{LABEL}.json').write_text(
        json.dumps(payload, indent=2) + '\n')

    print('\n---', LABEL, 'summary ---')
    print('totals:', json.dumps(payload['totals']))
    print('red families:', json.dumps(payload['red_family_counts']))
    print('imported blob is pinned blob:',
          payload['source_under_test']['is_pinned_blob'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
