"""Frozen before P10 implementation. Set WG0P11_ROOT to published return root.

These are acceptance tests: five failures against untouched P8 are expected RED,
not xfails. Never create candidate directories or restore missing candidate files.
Run after the candidate's own published preparation/runner for P10 acceptance.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

R = Path(os.environ['WG0P11_ROOT']).resolve()
C = R / 'candidate'
COURT = C / 'court'
EVIDENCE = Path(os.environ['WG0P11_EVIDENCE']).resolve()
EVIDENCE.mkdir(parents=True, exist_ok=True)
P5 = 'court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py'
SHA = '89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643'


def child(label, args, cwd=COURT, bootstrap=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
               PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    env.pop('PYTHONPATH', None)
    if bootstrap:
        env.update(PYTHONPATH=os.pathsep.join([str(COURT/'bootstrap_p6'), str(COURT/'repro')]),
                   WG0M_RUN='phase_b_P5', WG0L_PHASE_B_ADAPTER='phase_b_adapter_v1',
                   WG0O_WG0N_ROOT=str(R/'reviewer_frozen/03_INHERITED/WG0N'))
    p = subprocess.run([sys.executable, '-B', *args], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=600)
    (EVIDENCE/(label+'.json')).write_text(json.dumps(dict(
        command=p.args, cwd=str(cwd), exit=p.returncode,
        stdout=p.stdout, stderr=p.stderr), indent=2)+'\n')
    return p


def test_original_187_exact_source_preimages():
    frozen = json.loads((Path(__file__).parent/'01_PHASE_A_FROZEN_REQUIREMENTS_AND_HASHES.json').read_text())
    assert len(frozen['original_source_rows']) == 187
    for row in frozen['original_source_rows']:
        p = C/row['staged_path']
        assert p.is_file() and not p.is_symlink(), str(p)
        raw = p.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256'], str(p)
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest() == row['git_blob_sha1'], str(p)
        assert len(raw) == row['bytes'], str(p)


def test_D1_published_probe_accepts_exact_repaired_module():
    script = Path(os.environ.get('WG0P11_RUNNER', str(R/'repro/wg0p8_publication.py')))
    p = child('D1_probe', [str(script), 'probe-import'], cwd=R)
    assert p.returncode == 0, p.stderr
    result = json.loads(p.stdout)
    assert Path(result['path']).resolve() == (C/P5).resolve()
    assert result['sha256'] == SHA
    assert result['version'] == 'WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1'


def test_D2_observed_fresh_atexit_receipt():
    folder = C/'observations/imports'
    before = set(folder.glob('*.json'))
    p = child('D2_import', ['-c', 'import wg0p4_workload; print(wg0p4_workload.VERSION)'], bootstrap=True)
    assert p.returncode == 0, p.stderr
    assert 'WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1' in p.stdout
    assert 'Exception ignored in atexit callback' not in p.stderr, p.stderr
    added = set(folder.glob('*.json'))-before
    assert added, 'No new atexit receipt'
    receipts = [json.loads(f.read_text()) for f in added]
    assert any(r.get('actually_loaded_modules') and r.get('native_modules') and r.get('pid') for r in receipts)


def suite(label, path):
    return child(label, ['-m', 'pytest', '-c', str(COURT/'runtime_phase_b/candidate/pytest.ini'),
                        '-q', str(path), '--junitxml='+str(EVIDENCE/(label+'.xml'))], bootstrap=True)


def test_D3_fresh42_without_manual_directories():
    p = suite('D3_fresh42', C/'tests/test_source_view_binding.py')
    assert p.returncode == 0, p.stdout+p.stderr


def test_D4_published_cold_pointer_fixture_works_without_overlay():
    p = suite('D4_pointer', C/'tests/test_cold_pointer_process.py')
    assert p.returncode == 0, p.stdout+p.stderr


def test_D5_exact_historical_verdict_preserves_not_green():
    p = R/'reviewer_frozen/03_INHERITED/WG0N/02_PHASE_B_VERDICT.md'
    raw = p.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '839adc7508fcd81bd0a59af8f0fc8793b8ea075c80661683b776124cb90a228b'
    assert b'5 of my own controls are untested' in raw
    assert b'2 inherited characterisation tests fail' in raw
