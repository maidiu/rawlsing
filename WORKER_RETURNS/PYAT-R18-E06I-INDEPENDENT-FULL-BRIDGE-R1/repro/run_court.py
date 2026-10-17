"""Run the whole E06I court.

  1. candidate author suite (40 cases) as REGRESSION-grade evidence;
  2. independent reviewer hostile court (48 cases) as the acceptance basis.

Author evidence is never counted as independent acceptance.

usage: E06_CANDIDATE_ROOT=<staged candidate return> python3 repro/run_court.py
"""
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
CAND = os.environ.get('E06_CANDIDATE_ROOT')
if not CAND or not os.path.exists(os.path.join(CAND, 'bridge.py')):
    raise SystemExit('set E06_CANDIDATE_ROOT to the staged candidate return directory')
CAND = os.path.abspath(CAND)
OBS = RET / 'observations'
OBS.mkdir(exist_ok=True)


def counts(xml_path):
    suite = ET.parse(xml_path).getroot().find('testsuite')
    if suite is None:
        suite = ET.parse(xml_path).getroot()
    return {k: int(suite.get(k)) for k in ('tests', 'failures', 'errors', 'skipped')}


def run(label, args, cwd, junit):
    t = time.monotonic()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
               E06_CANDIDATE_ROOT=CAND)
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, env=env)
    out = (p.stdout + '\n' + p.stderr)
    (OBS / (label + '.stdout')).write_text(out)
    return dict(argv=[a.replace(CAND, '<CANDIDATE>') for a in args],
                cwd=str(cwd).replace(CAND, '<CANDIDATE>'), seconds=time.monotonic() - t,
                exit=p.returncode, junit=junit.name, counts=counts(junit))


author_xml = OBS / 'author40_regression.xml'
author = run('author40_regression',
             [sys.executable, '-m', 'pytest', '-q', 'tests/test_bridge.py',
              '--import-mode=importlib', '-p', 'no:cacheprovider',
              '--junitxml=' + str(author_xml)],
             cwd=CAND, junit=author_xml)

indep_xml = OBS / 'e06i_independent_court.xml'
indep = run('e06i_independent_court',
            [sys.executable, '-m', 'pytest', '-q', 'tests/test_e06i_independent_court.py',
             '--import-mode=importlib', '-p', 'no:cacheprovider',
             '--junitxml=' + str(indep_xml)],
            cwd=RET, junit=indep_xml)

summary = dict(schema='E06I_COURT_EXECUTION_SUMMARY@1', candidate_sha=os.environ.get('E06_CANDIDATE_SHA',
               'f9c52113de38caececc450f0e54c980f64ed3981'),
               author_regression=author, independent_court=indep,
               independence='author 40 is regression only; acceptance rests on the 48 independent cases')
(OBS / 'junit_summary.json').write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps(summary, indent=1))
