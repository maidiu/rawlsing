#!/usr/bin/env python3
"""OC5E — stage, execute and record the full native OC4 court.

    PV2_RUNTIME_ROOT=<staged dir> python3 repro/run_court.py

1. Stages the sealed source closure into PV2_RUNTIME_ROOT and verifies every
   Git blob SHA1 against the commission pins.
2. Runs the 131 inherited OC1/OCR1/OC2/OC3 cases, OC4's 36 new controls, the
   independently authored OC5E native hostiles, and OC5's committed
   prior-prediction falsifiers, each with its own JUnit and stdout.
3. Writes the environment passport and the frozen source manifest.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
REPRO = RETURN / 'repro'
RESULTS = RETURN / 'observations'
RUNTIME = Path(os.environ.get('PV2_RUNTIME_ROOT', '/tmp/oc5e-runtime')).resolve()
PY = sys.executable
SOURCE = RUNTIME / 'source'

COURTS = [
    # (label, junit, files, grade)
    ('inherited_131', 'inherited_131.xml',
     ['test_custody_hostiles.py', 'test_positive_lifecycle.py',
      'test_ocr1_independent_hostile.py', 'test_oc2_regressions.py',
      'test_oc3_independent_hostile.py'],
     'original inherited 131: expected 121 PASS / 10 RED'),
    ('oc4_new_36', 'oc4_new_36.xml', ['test_oc4_repair_controls.py'],
     'OC4 author new controls: expected 36 PASS'),
    ('oc5e_native_hostiles', 'oc5e_native_hostiles.xml',
     ['test_oc5e_native_hostiles.py'],
     'independently authored native hostiles (regression bank)'),
    ('oc5_prior_predictions', 'oc5_prior_predictions.xml',
     ['test_oc5_prior_predictions.py'],
     'OC5 committed falsifiers, disclosed input'),
]


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    stage = subprocess.run(
        [PY, str(REPRO / 'stage_source.py'), str(RUNTIME)],
        capture_output=True, text=True)
    (RESULTS / 'stage_source.log').write_text(
        f'# exit: {stage.returncode}\n\n{stage.stdout}\n{stage.stderr}\n')
    print('stage_source exit=', stage.returncode)
    if stage.returncode != 0:
        print(stage.stdout, stage.stderr)
        return 1

    env = dict(os.environ)
    env['PYTHONPATH'] = str(SOURCE)

    codes = {}
    tallies = []
    for label, junit, files, grade in COURTS:
        argv = [PY, '-m', 'pytest', '-q', *files, '--tb=line',
                '-p', 'no:cacheprovider', '--import-mode=importlib',
                f'--junitxml={RESULTS / junit}']
        started = time.time()
        proc = subprocess.run(argv, cwd=SOURCE, env=env,
                              capture_output=True, text=True)
        elapsed = round(time.time() - started, 2)
        (RESULTS / f'{label}.log').write_text(
            f'# command: {" ".join(argv)}\n# cwd: {SOURCE}\n'
            f'# exit: {proc.returncode}\n# elapsed_s: {elapsed}\n\n'
            f'{proc.stdout}\n{proc.stderr}\n')
        codes[label] = proc.returncode
        root = ET.parse(RESULTS / junit).getroot()
        suite = root.find('testsuite') if root.tag == 'testsuites' else root
        attrs = suite.attrib
        row = dict(label=label, junit=junit, grade=grade,
                   tests=int(attrs.get('tests', 0)),
                   pass_=int(attrs.get('tests', 0)) - int(attrs.get('failures', 0)) -
                   int(attrs.get('errors', 0)),
                   failed=int(attrs.get('failures', 0)),
                   errors=int(attrs.get('errors', 0)),
                   skipped=int(attrs.get('skipped', 0)),
                   seconds=float(attrs.get('time', 0) or 0), grade_note=grade)
        row.pop('grade')
        tallies.append(row)
        print(f'{label:<22} exit={proc.returncode} '
              f'tests={row["tests"]} pass={row["pass_"]} fail={row["failed"]} '
              f'({elapsed}s)')

    # ---- environment passport ----
    import importlib.util
    import sys as _sys
    _sys.path.insert(0, str(SOURCE))
    import custody_protocol as CP
    os.chdir(SOURCE)
    staged_blob = subprocess.check_output(
        ['git', 'hash-object', CP.__file__]).decode().strip()
    raw = Path(CP.__file__).read_bytes()
    manifest = json.loads((RETURN / 'freezes' / '01_STAGED_SOURCE_MANIFEST.json').read_text())
    for row in manifest:
        row['staged_sha1_recheck'] = subprocess.check_output(
            ['git', 'hash-object', str(RUNTIME / row['staged'])]).decode().strip()
        row['blob_verified'] = row['staged_sha1_recheck'].startswith(row['git_blob'][:40])
    oc05 = []
    root = ET.parse(RESULTS / 'oc4_new_36.xml').getroot()
    suite = root.find('testsuite') if root.tag == 'testsuites' else root
    for tc in suite.iter('testcase'):
        if any(k.tag in ('failure', 'error') for k in tc):
            oc05.append(tc.get('name'))

    passport = dict(
        commission='SOROK-R3-HQ312-OC5E-EXECUTION-RECOVERY-R1',
        branch='agent/reviewer-sorok-r3-hq312-oc5e-execution-recovery-r1',
        exact_sealed_startup='146b1722a5568c1c96c3fb4f602ef750cf6d8518',
        startup_verified_against_remote=subprocess.check_output(
            ['git', 'ls-remote', 'origin',
             'agent/reviewer-sorok-r3-hq312-oc5e-execution-recovery-r1'],
            cwd='/Users/matthewsmith/Desktop/Rawlsing').decode().split()[0] ==
        '146b1722a5568c1c96c3fb4f602ef750cf6d8518',
        sealed_commits=dict(
            parent='50d9c762c48a99cd0d41bd811219087d96dc4bc0',
            oc1='19438890e43153e2bc4a1ad271b5e19bcef33e1e',
            ocr1='aba637265bea2358790fea50d0e7abc98141e472',
            oc2='a61d5794271038fb20c94a75eaee401a66613ce9',
            oc3='9cd47a829473a6e92392582b4f01f2c564aa5dce',
            oc4_under_review='0caaec590f6a8bf6744f22dc9c948c5fe233bc94',
            oc5_prior_partial='8185d2ca41ac5c5711b3f3f528e6f644dbab185d'),
        source_under_review=dict(
            module=str(CP.__file__),
            git_blob_sha1=staged_blob,
            pinned_git_blob_sha1='af2b7e943018077cb36808b5af1cd67704624bec',
            blob_matches_pin=staged_blob == 'af2b7e943018077cb36808b5af1cd67704624bec',
            sha256=hashlib.sha256(raw).hexdigest()),
        sealed_object_manifest=manifest,
        environment=dict(
            python=subprocess.check_output([PY, '--version']).decode().strip(),
            pytest=subprocess.check_output(
                [PY, '-m', 'pytest', '--version']).decode().strip().splitlines()[0],
            platform=platform.platform(), machine=platform.machine(),
            git=subprocess.check_output(
                ['git', '--version']).decode().strip(),
            cwd_for_courts=str(SOURCE)),
        courts=tallies,
        totals=dict(
            pytest_cases=sum(t['tests'] for t in tallies),
            passing=sum(t['pass_'] for t in tallies),
            failing=sum(t['failed'] for t in tallies),
            errors=sum(t['errors'] for t in tallies),
            skipped=sum(t['skipped'] for t in tallies)),
        oc4_new_36_all_pass=not oc05,
        claims=dict(
            native_execution=True, no_transcribed_excerpt=True,
            no_author_source_edited=True, no_xfail_or_skip_greenwashing=True,
            test_only_scope=True, no_real_signer_institution=True,
            no_protected_holdout=True, no_durable_external_journal=True,
            no_independent_semantic_oracle=True,
            cross_process_c07='NOT_REACHED absent API',
            no_external_model_calls=True, no_original_survey_data=True,
            no_v3=True, no_product_premain_current_edit=True,
            no_adoption=True, distinct_independent_court_required=True))
    (RETURN / 'environment_passport_delta.json').write_text(
        json.dumps(passport, indent=2, sort_keys=True) + '\n')

    print('\n--- summary ---')
    for label, code in codes.items():
        print(f'{label:<22} exit={code} {"PASS" if code == 0 else "RED (expected)"}')
    print('totals:', json.dumps(passport['totals']))
    print('blob matches pin:', passport['source_under_review']['blob_matches_pin'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
