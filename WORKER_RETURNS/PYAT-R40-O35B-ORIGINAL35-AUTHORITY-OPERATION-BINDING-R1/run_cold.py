"""Cold sourcefree audit / native boundary probe with sanitized execution receipts."""
import datetime
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))
import authority_binding
from rawlsing_next.fiabc_final_oracle_freeze_producers import _load_lits_materialization_checkpoint
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_batch_runner import BatchExecutionRunner
from rawlsing_next.pre553_learned_empirical_adjudication import adjudicate_learned_empirical

SEAL = '1150e836ef58553255abc0f588e66c1327db4932'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO, text=True).strip()


def sanitize(text):
    return text.replace(str(REPO), 'WORKTREE').replace(str(HERE), 'RETURN').replace(str(Path.home()), 'HOST_HOME')


def checkpoint_probe():
    doc = (HERE / '.runtime/inputs/custody/PREMAIN-FIABC-LITS-FINAL-SUCCESS-DURABLE-CUSTODY-R1_00_RETURN.md').read_text()
    recorded_root = re.search(r'`(/Users/[^`]+SOURCE-RETRY-R1)`', doc).group(1)
    path = Path(os.environ.get('O35B_RETAINED_CHECKPOINT', str(Path(recorded_root) / 'court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json')))
    expected = '2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726'
    receipt = {'expected_file_sha256': expected, 'expected_bytes': 3404445161,
               'locator': 'historical accepted LOCAL_CUSTODY checkpoint (host path redacted)',
               'native_loader': 'rawlsing_next.fiabc_final_oracle_freeze_producers._load_lits_materialization_checkpoint',
               'raw_source_reads': 0, 'current_native_original_positive': 'NOT_PROVED',
               'actual_execution_plan_omission_RED': 'NOT_RUN'}
    if path.is_file():
        # Never accidentally load a substituted 3.4GB artifact, or launch a heavy
        # source operation from this bounded preflight. Exact replay is separate.
        digest = hashlib.sha256()
        with path.open('rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(chunk)
        receipt.update(observed_file_sha256=digest.hexdigest(), observed_bytes=path.stat().st_size,
                       state='RETAINED_PAYLOAD_PRESENT_REPLAY_PENDING')
        if (digest.hexdigest(), path.stat().st_size) != (expected, 3404445161):
            receipt['state'] = 'HOLD_WRONG_RETAINED_PREIMAGE'
    else:
        try:
            _load_lits_materialization_checkpoint(path)
        except FileNotFoundError:
            receipt.update(state='NOT_REACHED_MISSING_RETAINED_PREIMAGE', native_boundary_result='FileNotFoundError')
        else:
            raise AssertionError('missing-path native loader unexpectedly returned')
    return receipt


def main():
    runtime = HERE / '.runtime'
    runtime.mkdir(exist_ok=True)
    marker = runtime / 'live_marker.json'
    if marker.is_file():
        identity = json.loads(marker.read_text())
    else:
        identity = {'environment_id': 'o35b-local-' + uuid.uuid4().hex[:12], 'epoch_id': uuid.uuid4().hex}
        marker.write_text(json.dumps(identity))
    assert json.loads(marker.read_text()) == identity
    authority_binding.main()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    rel = HERE.relative_to(REPO).as_posix()
    commands = [
        ('o35b', [rel + '/test_o35b_binding.py']),
        ('native_owner', ['rawlsing_next/tests/' + n for n in [
            'test_pre553_carrier_execution.py', 'test_pre553_batch_runner.py',
            'test_pre553_empirical_query.py', 'test_pre553_discovery_exact.py',
            'test_pre553_learned_empirical_adjudication.py']]),
    ]
    tests = []
    for label, nodes in commands:
        junit = HERE / 'evidence' / (label + '_junit.xml')
        cmd = [sys.executable, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '--junitxml=' + str(junit), *nodes]
        run = subprocess.run(cmd, cwd=REPO, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (HERE / 'evidence' / (label + '_stdout.txt')).write_text(sanitize(run.stdout))
        if run.returncode:
            raise RuntimeError(label + ' pytest failed; inspect sanitized stdout')
        tree = ET.parse(junit)
        for element in tree.iter():
            if 'hostname' in element.attrib:
                element.set('hostname', 'LOCAL_HOST')
        tree.write(junit, encoding='unicode')
        cases = list(tree.iter('testcase'))
        tests.append({'suite': label, 'command': ['$QUALIFIED_PYTHON', *cmd[1:]],
                      'exit': run.returncode, 'tests': len(cases), 'junit': junit.relative_to(HERE).as_posix(),
                      'grade': 'METADATA_ACCOUNTING_AND_NATIVE_NEGATIVES' if label == 'o35b' else 'EXISTING_SOURCEFREE_NATIVE_OWNER_REGRESSION; NOT_ORIGINAL_DATA'})
    imports = []
    for name, module in sorted(sys.modules.copy().items()):
        file = getattr(module, '__file__', None)
        if not name.startswith('rawlsing_next') or not file:
            continue
        path = Path(file).resolve()
        if not path.is_relative_to(REPO):
            raise AssertionError('native import escaped assigned worktree')
        relative = path.relative_to(REPO).as_posix()
        raw = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if blob != git('rev-parse', SEAL + ':' + relative):
            raise AssertionError('native import differs from seal: ' + relative)
        imports.append({'module': name, 'observed_file_sanitized': 'WORKTREE/' + relative,
                        'commit': SEAL, 'path': relative, 'git_blob_sha1': blob,
                        'sha256': hashlib.sha256(raw).hexdigest()})
    probe = checkpoint_probe()
    (HERE / 'evidence/native_checkpoint_probe.json').write_text(json.dumps(probe, indent=2) + '\n')
    passport = {**identity, 'session_alias': 'O35B_AUTHOR', 'surface': 'CODEX_DESKTOP_LOCAL',
        'machine_alias': 'LOCAL_HOST', 'status': 'LIVE_VERIFIED',
        'last_live_probe_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'writable_marker': 'READ_AFTER_WRITE_VERIFIED_IGNORED_RUNTIME',
        'python': sys.version.split()[0], 'pytest': importlib.metadata.version('pytest'),
        'PyYAML': importlib.metadata.version('PyYAML'), 'git': git('--version'),
        'interpreter': 'REUSED_PREVIOUSLY_QUALIFIED_WARM_VENV; HOST_PATH_REDACTED',
        'worktree': 'NEW_ISOLATED_SPARSE_SHARED_OBJECT_STORE', 'sealed_startup': SEAL,
        'branch': git('branch', '--show-current'), 'head_at_probe': git('rev-parse', 'HEAD'),
        'provider': 'OpenAI', 'model_last_observed_in_this_conversation': 'gpt-6.1-sol',
        'reasoning_last_observed': 'medium', 'autonomous_switch': False,
        'cash_incremental': 'UNKNOWN', 'quota_incremental': 'UNKNOWN', 'account_tier': 'UNKNOWN',
        'packages': 'EXISTING_WARM_RUNTIME_REUSED; NO_INSTALL',
        'native_import_closure': 'BOUNDED_ACTUAL_IMPORTS_OF_PROBED_OWNERS; NOT_ALL_REPOSITORY',
        'native_imports': imports, 'tests': tests, 'checkpoint_probe': probe,
        'raw_original_reads': 0, 'original35_current_permitted': 0,
        'independent_review_conflicts': 'AUTHOR_OF_THIS_O35B_LEDGER; NOT_INDEPENDENT_ACCEPTOR',
        'assignments_completed': ['O35B_BOUNDED_OWNER_ACCOUNTING; NATIVE_ORIGINAL_EDGE_PENDING'],
        'continuation_affinity': ['retained LiTS canonical preimage recovery', 'original35 owner-packet binding'],
        'eligibility': 'REPROBE_BEFORE_REUSE; DOCUMENTARY_PASSPORT_IS_NOT_A_LEASE',
        'expiry_trigger': 'runtime reset, source/import drift, worktree conflict, scope or permission change',
        'source_model_privacy_gate': 'COMMITTED_METADATA_AND_CODE_ONLY; NO_RAW_RESPONDENTS_OR_MODEL_CALLS',
    }
    text = sanitize(json.dumps(passport, indent=2)) + '\n'
    (HERE / 'environment_passport_delta.json').write_text(text)
    print(json.dumps({'native_imports': len(imports), 'tests': [(t['suite'], t['tests']) for t in tests], 'checkpoint': probe['state']}))


if __name__ == '__main__':
    main()
