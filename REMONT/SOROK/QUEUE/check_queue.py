#!/usr/bin/env python3
"""Execute pinned sourcefree REMONT checks, write additive machine receipts.

Not an independent reviewer, native issuer, protected receiver, or a daemon.
Agent must do the source-level hostile review after this runner exits.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import uuid
from contextlib import contextmanager
import fcntl

HERE = Path(__file__).resolve().parent
DEFAULT_QUEUE = HERE / 'CHECK_QUEUE.json'
REPO_ROOT = HERE.parents[2]  # REMONT/SOROK/QUEUE -> repository root
ALLOWED_VERDICTS = {'ACCEPT_SCOPED', 'REVISE_EXACT_DEFECT', 'HOLD'}


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def atomic_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile('w', encoding='utf-8', dir=path.parent,
                                     prefix='.pending-', delete=False) as h:
        json.dump(obj, h, ensure_ascii=False, sort_keys=True, indent=2)
        h.write('\n')
        tmp = Path(h.name)
    os.replace(tmp, path)


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate_queue(q):
    if q.get('schema') != 'REMONT_LOCAL_MACHINE_QUEUE_V1':
        raise ValueError('UNKNOWN_QUEUE_SCHEMA')
    if q.get('repository') != 'maidiu/rawlsing':
        raise ValueError('UNEXPECTED_REPOSITORY')
    items = q.get('candidates')
    if not isinstance(items, list) or not items:
        raise ValueError('EMPTY_REMONT_QUEUE')
    seen_pr = set()
    for item in items:
        pr, sha, branch = item.get('pr'), item.get('sha'), item.get('branch')
        if type(pr) is not int or pr <= 0 or pr in seen_pr:
            raise ValueError('INVALID_OR_DUPLICATE_QUEUE_PR')
        if type(sha) is not str or len(sha) != 40 or any(c not in '0123456789abcdef' for c in sha):
            raise ValueError('INVALID_PINNED_SHA')
        if (type(branch) is not str or '..' in branch or
                not (branch.startswith('agent/sorok-remont-') or
                     (item.get('joined_first_consumer') is True and
                      branch.startswith('agent/soracle-remont-')))):
            raise ValueError('INVALID_QUEUE_BRANCH')
        if type(item.get('manifest')) is not str or '/' in item['manifest']:
            raise ValueError('INVALID_MANIFEST')
        if (item['manifest'] == 'PINNED_GIT_TREE' and
                item.get('joined_first_consumer') is not True):
            raise ValueError('UNAUTHORIZED_GIT_TREE_MODE')
        if type(item.get('joined_first_consumer', False)) is not bool:
            raise ValueError('INVALID_JOINED_CONSUMER_FLAG')
        if type(item.get('execution_deferred',False)) is not bool:
            raise ValueError('INVALID_EXECUTION_DEFER_FLAG')
        if item.get('execution_deferred') is True and item.get('joined_first_consumer') is not True:
            raise ValueError('DEFER_ONLY_ACTIVE_BUILDER_LANE')
        seen_pr.add(pr)
    return q


def run_process(argv, cwd, timeout=180, env=None):
    try:
        p = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout, env=env,
                           check=False)
        return {'command': [str(x) for x in argv], 'exit_code': p.returncode,
                'output': p.stdout, 'duration_limit_sec': timeout}
    except subprocess.TimeoutExpired as e:
        return {'command': [str(x) for x in argv], 'exit_code': None,
                'output': str(e), 'timed_out': True, 'duration_limit_sec': timeout}
    except OSError as e:
        return {'command': [str(x) for x in argv], 'exit_code': None,
                'output': str(e), 'launch_failed': True}


def require_ok(result, code):
    if result['exit_code'] != 0:
        raise QueueFailure(code, result)
    return result['output'].strip()


class QueueFailure(Exception):
    def __init__(self, code, detail=None):
        super().__init__(code)
        self.code = code
        self.detail = detail


def git(repo: Path, *argv, timeout=90):
    r = run_process(['git', *argv], repo, timeout=timeout)
    return require_ok(r, 'GIT_' + argv[0].replace('-', '_').upper())


def pinned_git_tree_check(src: Path):
    """Verify joined Python source/test bytes against the frozen Git tree.

    Used only for the explicit integration queue. A pinned commit plus
    complete Git blob checking replaces an outdated historical manifest;
    it does not claim an independent precommitted SHA256 manifest.
    """
    root = Path(git(src, 'rev-parse', '--show-toplevel')).resolve()
    try:
        prefix = src.resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise QueueFailure('PINNED_TREE_OUTSIDE_CHECKOUT') from exc
    listing = git(root, 'ls-tree', '-r', 'HEAD', '--', prefix)
    tracked = {}
    for line in listing.splitlines():
        parts = line.split('\t', 1)
        if len(parts) != 2:
            raise QueueFailure('PINNED_TREE_UNREADABLE')
        meta, full = parts
        if not (full.startswith(prefix + '/') and full.endswith('.py')):
            continue
        fields = meta.split()
        if len(fields) != 3 or fields[0] not in ('100644', '100755') or fields[1] != 'blob':
            raise QueueFailure('PINNED_TREE_PYTHON_NOT_REGULAR', full)
        rel = full[len(prefix) + 1:]
        if rel in tracked:
            raise QueueFailure('PINNED_TREE_DUPLICATE_PATH', rel)
        tracked[rel] = fields[2]
    if not tracked:
        raise QueueFailure('PINNED_TREE_EMPTY_PYTHON_COURT')
    disk = {p.relative_to(src).as_posix() for p in src.rglob('*.py')
            if p.is_file() or p.is_symlink()}
    if disk != set(tracked):
        raise QueueFailure('PINNED_TREE_PYTHON_SET_MISMATCH', {
            'untracked': sorted(disk - set(tracked))[:20],
            'missing': sorted(set(tracked) - disk)[:20]})
    digest = hashlib.sha256()
    for rel, expected in sorted(tracked.items()):
        fp = src / rel
        if fp.is_symlink() or not fp.is_file():
            raise QueueFailure('PINNED_TREE_SOURCE_MISSING_OR_SYMLINK', rel)
        raw = fp.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if actual != expected:
            raise QueueFailure('PINNED_TREE_SOURCE_BLOB_MISMATCH', rel)
        digest.update((rel + '\0' + expected + '\0' +
                       hashlib.sha256(raw).hexdigest() + '\n').encode())
    return {'verified_python_files': len(tracked),
            'manifest': 'PINNED_GIT_TREE',
            'sha256': digest.hexdigest(),
            'identity_basis': 'exact_commit_git_tree_and_content_sha1_sha256',
            'precommitted_independent_sha256_manifest': False}


def source_manifest_check(src: Path, filename: str):
    if filename == 'PINNED_GIT_TREE':
        return pinned_git_tree_check(src)
    p = src / filename
    if not p.is_file():
        raise QueueFailure('SOURCE_MANIFEST_MISSING', str(p))
    try:
        m = load_json(p)
    except (ValueError, OSError) as exc:
        raise QueueFailure('SOURCE_MANIFEST_UNREADABLE', str(exc)) from exc
    files = m.get('files')
    if not isinstance(files, dict) or not files:
        raise QueueFailure('INVALID_SOURCE_MANIFEST')
    if m.get('python_file_count') is not None and m['python_file_count'] != len(files):
        raise QueueFailure('SOURCE_MANIFEST_COUNT_CONTRADICTION')
    matches = 0
    for name, data in sorted(files.items()):
        if type(data) is not dict:
            raise QueueFailure('INVALID_SOURCE_MANIFEST_ITEM', name)
        fp = (src / name).resolve()
        if src.resolve() not in fp.parents or not fp.is_file() or fp.is_symlink():
            raise QueueFailure('SOURCE_MANIFEST_PATH_INVALID', name)
        raw = fp.read_bytes()
        if hashlib.sha256(raw).hexdigest() != data.get('sha256'):
            raise QueueFailure('SOURCE_SHA256_MISMATCH', name)
        blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        expected = data.get('git_blob_sha1', data.get('git_blob'))
        if expected and blob != expected:
            raise QueueFailure('SOURCE_GIT_BLOB_MISMATCH', name)
        matches += 1
    return {'verified_python_files': matches, 'manifest': filename,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def demo_and_reopen(python: str, src: Path, temp: Path):
    db = temp / 'remont-queue.sqlite3'
    cmd = [python, '-m', 'um_sorok_organism', 'demo', '--db', str(db)]
    rr = run_process(cmd, src, timeout=160)
    require_ok(rr, 'DEMO_EXECUTION_FAILED')
    try:
        d = json.loads(rr['output'])
        chain = d['sourcefree_chain']
        cold = d['cold_reopen']['chain']
        if not (chain['valid'] is True and cold['valid'] is True and
                chain['last_hash'] == cold['last_hash'] and chain['events'] == cold['events']):
            raise ValueError('DEMO_CHAIN_AND_COLD_MISMATCH')
    except (ValueError, KeyError, TypeError) as exc:
        raise QueueFailure('DEMO_CHAIN_INVALID', str(exc)) from exc
    # A separate Python interpreter independently opens and closes SQLite.
    probe = """import json,sys
from um_sorok_organism.storage import ResearchLedger
s=ResearchLedger(sys.argv[1]); v=s.verify_chain()
r=s.events(); ok=s.conn.execute('PRAGMA integrity_check').fetchone()[0]
print(json.dumps({'valid':v['valid'], 'events':v['events'], 'last_hash':v['last_hash'],
  'event_ids':[x['id'] for x in r], 'event_hashes':[x['chain_hash'] for x in r],
  'sqlite_integrity':ok},sort_keys=True)); s.close()
"""
    probes = []
    for _ in range(2):
        r = run_process([python, '-c', probe, str(db)], src, timeout=60)
        require_ok(r, 'COLD_SQLITE_REOPEN_FAILED')
        try:
            probes.append(json.loads(r['output']))
        except ValueError as exc:
            raise QueueFailure('COLD_REOPEN_NOT_JSON', r['output'][-1000:]) from exc
    if probes[0] != probes[1] or probes[0]['sqlite_integrity'] != 'ok' or not probes[0]['valid']:
        raise QueueFailure('COLD_SQLITE_INTEGRITY_INCONSISTENT', probes)
    if probes[0]['last_hash'] != chain['last_hash'] or probes[0]['events'] != chain['events']:
        raise QueueFailure('DEMO_AND_SEPARATE_COLD_CHAIN_DIVERGE')
    return {'events': chain['events'], 'last_hash': chain['last_hash'],
            'cold_reopen_valid': True, 'sqlite_integrity': 'ok',
            'two_process_identical_event_ids_and_hashes': True}



def joined_nadia_and_reopen(python: str, src: Path, temp: Path):
    """Execute two real counterfactual Nadia lives and separate cold reopens."""
    target = temp / 'joined-life'
    cmd = [python, '-m', 'um_sorok_organism.joined_longitudinal_demo',
           '--directory', str(target), '--days', '14', '--beats', '12']
    run = run_process(cmd, src, timeout=300)
    require_ok(run, 'JOINED_LONGITUDINAL_EXECUTION_FAILED')
    try:
        result = json.loads(run['output'])
        yes = result['contrast']['spoken']
        no = result['contrast']['unspoken']
        if not (result['early_historical_cultural_divergence_observed'] is True
                and result['nadia_action_not_externally_requested'] is True
                and result['external_pyat_correspondence'] == 'NOT_ISSUED'
                and yes['father_source_action'] == 'SPEAK'
                and no['father_source_action'] == 'REST'
                and yes['actor_selected_nadia_action'] == 'INSPECT'
                and yes['actor_selected_nadia_status'] == 'PERFORMED'
                and len(yes['early_nadia_after']['cultural_practice_refs']) == 1
                and no['early_nadia_after']['cultural_practice_refs'] == []
                and yes['independent_beats_reported'] == 12
                and no['independent_beats_reported'] == 12):
            raise ValueError('JOINED_COUNTERFACTUAL_CAUSAL_PRECONDITIONS_FAILED')
    except (ValueError, KeyError, TypeError) as exc:
        raise QueueFailure('JOINED_LONGITUDINAL_INVALID', str(exc)) from exc
    probe = """import json,sys
from um_sorok_organism.storage import ResearchLedger
s=ResearchLedger(sys.argv[1])
try:
 c=s.verify_chain()
 p=s.conn.execute('PRAGMA integrity_check').fetchone()[0]
 events=s.events()
 print(json.dumps({'valid':c['valid'],'events':c['events'],
  'last_hash':c['last_hash'],'sqlite_integrity':p,
  'event_ids':[x['id'] for x in events],
  'event_hashes':[x['chain_hash'] for x in events]},sort_keys=True))
finally:s.close()
"""
    summary = {}
    for label, file in (('spoken', 'speaking.sqlite3'),
                        ('unspoken', 'silent.sqlite3')):
        case = result['contrast'][label]
        if case['cold_nadia'] != case['later_nadia']:
            raise QueueFailure('JOINED_NADIA_COLD_PSYCHIC_MISMATCH', label)
        checks = []
        for _ in range(2):
            rr = run_process([python, '-c', probe, str(target / file)],
                             src, timeout=80)
            require_ok(rr, 'JOINED_INDEPENDENT_COLD_REOPEN_FAILED')
            try:
                checks.append(json.loads(rr['output']))
            except ValueError as exc:
                raise QueueFailure('JOINED_COLD_REOPEN_NOT_JSON', label) from exc
        if (checks[0] != checks[1] or checks[0]['valid'] is not True or
                checks[0]['sqlite_integrity'] != 'ok' or
                checks[0]['last_hash'] != case['cold_integrity']['last_hash'] or
                checks[0]['events'] != case['cold_integrity']['events']):
            raise QueueFailure('JOINED_INDEPENDENT_COLD_REOPEN_DIVERGED', label)
        summary[label] = {
            'events': checks[0]['events'],
            'last_hash': checks[0]['last_hash'],
            'sqlite_integrity': checks[0]['sqlite_integrity'],
            'two_process_event_identity_match': True,
            'nadia_cold_state_equal': True,
            'child_cultural_practice_count':
                len(case['early_nadia_after']['cultural_practice_refs']),
        }
    return {'days':14,'beats':12,
            'early_historical_cultural_divergence_observed': True,
            'sourcefree_not_human_science': True,
            'contrasts':summary}


def ensure_machine_version(py: str, workdir: Path):
    test = run_process([py, '-c',
                        'import json,sys;print(json.dumps(list(sys.version_info[:3])))'], workdir)
    require_ok(test, 'PYTHON_EXECUTABLE_MISSING')
    try:
        version = json.loads(test['output'])
    except ValueError as exc:
        raise QueueFailure('PYTHON_VERSION_UNREADABLE') from exc
    if version[:2] != [3, 11]:
        raise QueueFailure('PYTHON_3_11_REQUIRED', str(version))
    return version


def verify_source_ref(repo: Path, item):
    # The user must reconcile a moved live branch; never silently upgrade SHA.
    remote = git(repo, 'ls-remote', 'origin', 'refs/heads/' + item['branch'])
    rows = [x.split() for x in remote.splitlines() if x.strip()]
    if len(rows) != 1 or rows[0][0] != item['sha']:
        raise QueueFailure('LIVE_BRANCH_HEAD_CHANGED_HOLD', remote or 'REMOTE_BRANCH_MISSING')
    return remote


def run_candidate(repo: Path, item, py: str, q, *, fetch=False):
    receipt = {'kind': 'REMONT_LOCAL_MACHINE_COMPATIBILITY_V1',
               'pr': item['pr'], 'label': item['label'], 'sha': item['sha'],
               'started_at_utc': utc_now(), 'status': 'STARTED',
               'independent_acceptance': False, 'protected_received': False,
               'tests': [], 'review': 'HOSTILE_INDEPENDENT_REVIEW_NOT_PERFORMED_BY_RUNNER'}
    with tempfile.TemporaryDirectory(prefix='remont-pr-%s-' % item['pr']) as temp:
        base = Path(temp)
        wt = base / 'frozen'
        try:
            verify_source_ref(repo, item)
            if fetch:
                probe = run_process(['git','cat-file','-e',item['sha']+'^{commit}'],repo,timeout=30)
                if probe['exit_code'] != 0:
                    git(repo, 'fetch', '--no-tags', 'origin',
                        'refs/heads/' + item['branch'], timeout=180)
            git(repo, 'worktree', 'add', '--detach', str(wt), item['sha'], timeout=120)
            exact = git(wt, 'rev-parse', 'HEAD')
            if exact != item['sha']:
                raise QueueFailure('DETACHED_HEAD_MISMATCH', exact)
            candidate = wt / q['candidate_root']
            if not candidate.is_dir():
                raise QueueFailure('CANDIDATE_RUNTIME_MISSING')
            receipt['python_version'] = ensure_machine_version(py, candidate)
            receipt['source_manifest'] = source_manifest_check(candidate, item['manifest'])
            if item.get('joined_first_consumer') is True:
                compile_result = run_process(
                    [py, '-m', 'compileall', '-q', 'um_sorok_organism'],
                    candidate, timeout=120)
                receipt['tests'].append({'kind':'joined_compile', **compile_result})
                require_ok(compile_result, 'JOINED_SOURCE_COMPILE_FAILED')
                focused = [
                    'tests.test_r3_r18_joined_faults',
                    'tests.test_r3_r16_joined_first_consumer',
                    'tests.test_joined_longitudinal_demo',
                    'tests.test_r17_source_preflight',
                    'tests.test_remontathon_r18_p004_selected_means',
                    'tests.test_remontathon_r13',
                    'tests.test_cultural_mediation_r3',
                    'tests.test_social_vocal_development_r3',
                ]
                for optimized in (False, True):
                    cmd = [py] + (['-O'] if optimized else []) + [
                        '-m', 'unittest', '-v', *focused]
                    result = run_process(cmd, candidate, timeout=300)
                    kind = 'joined_focused_optimized' if optimized else 'joined_focused'
                    receipt['tests'].append({'kind':kind, **result})
                    require_ok(result, 'TEST_COURT_FAILED_' + kind.upper())
            suite = (
                [py, '-m', 'unittest', 'discover', '-s', 'tests', '-q'],
                [py, '-O', '-m', 'unittest', 'discover', '-s', 'tests', '-q'],
                [py, '-m', 'pytest', '-q'],
            )
            for i, cmd in enumerate(suite):
                r = run_process(cmd, candidate, timeout=240)
                receipt['tests'].append({'kind': ('unittest','unittest_optimized','pytest')[i], **r})
                require_ok(r, 'TEST_COURT_FAILED_' + ('NORMAL','OPTIMIZED','PYTEST')[i])
            receipt['sqlite_demo'] = demo_and_reopen(py, candidate, base)
            if item.get('joined_first_consumer') is True:
                receipt['joined_counterfactual'] = joined_nadia_and_reopen(py, candidate, base)
            tracked = git(wt, 'status', '--porcelain', '--untracked-files=no')
            if tracked:
                raise QueueFailure('TESTS_MUTATED_TRACKED_SOURCE', tracked)
            receipt['status'] = 'COMPAT_PASS__HOSTILE_REVIEW_PENDING'
        except QueueFailure as e:
            receipt['status'] = e.code
            receipt['failure_detail'] = e.detail
        except (ValueError, OSError, KeyError, TypeError) as e:
            receipt['status'] = 'UNEXPECTED_EXECUTION_ERROR__HOLD'
            receipt['failure_detail'] = repr(e)
        finally:
            if wt.exists():
                run_process(['git', 'worktree', 'remove', '--force', str(wt)], repo, timeout=45)
    receipt['finished_at_utc'] = utc_now()
    return receipt


def state_key(item):
    return f"{item['pr']}@{item['sha']}"


@contextmanager
def state_lock(results: Path):
    """Serialize local ledger writers; never lock or alter tracked repository files."""
    results.mkdir(parents=True, exist_ok=True)
    with (results / ".ledger.lock").open("a+") as h:
        fcntl.flock(h.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(h.fileno(), fcntl.LOCK_UN)


def load_state(path):
    if not path.exists():
        return {'schema': 'REMONT_LOCAL_MACHINE_LEDGER_V1', 'items': {}}
    obj = load_json(path)
    if obj.get('schema') != 'REMONT_LOCAL_MACHINE_LEDGER_V1':
        raise ValueError('INVALID_LOCAL_RESULTS_SCHEMA')
    return obj


def record_receipt(results: Path, key: str, receipt):
    state_path = results / 'ledger.json'
    rid = utc_now().replace(':','').replace('+','_') + '_' + uuid.uuid4().hex[:12]
    target = results / 'runs' / ('pr' + key.split('@')[0] + '_' + rid + '.json')
    with state_lock(results):
        state = load_state(state_path)
        atomic_json(target, receipt)
        item_state = state['items'].setdefault(key, {'reviews': []})
        item_state['last_execution'] = str(target.relative_to(results))
        item_state['last_status'] = receipt['status']
        state['last_updated_at_utc'] = utc_now()
        atomic_json(state_path, state)
    return target


def pick(q, arg):
    items = q['candidates']
    if arg.pr:
        items = [x for x in items if x['pr'] in set(arg.pr)]
        if len(items) != len(set(arg.pr)):
            raise ValueError('UNKNOWN_REQUESTED_PR')
    return items


def needs_execution(state, key, force=False):
    if force:
        return True
    r = state['items'].get(key, {})
    if r.get('last_status') != 'COMPAT_PASS__HOSTILE_REVIEW_PENDING':
        return True
    return not (r.get('last_execution') and (state['_results_path']/r['last_execution']).is_file())


def print_queue(items, state):
    for i in items:
        key = state_key(i)
        row = state['items'].get(key, {})
        reviews = row.get('reviews', [])
        disposition = reviews[-1].get('verdict') if reviews else 'HOSTILE_REVIEW_PENDING'
        grade = ('DEFERRED_TO_BUILDER__HISTORICAL_RED' if i.get('execution_deferred') is True
                 else row.get('last_status', 'COMPAT_NOT_RUN'))
        print(f"#{i['pr']} {i['sha'][:12]} {grade} | {disposition} | {i['label']}")


def publish_compat(repo: Path, item, receipt, path):
    if shutil.which('gh') is None:
        return 'GH_NOT_INSTALLED__PUBLISH_PENDING'
    result = run_process(['gh', 'pr', 'comment', str(item['pr']), '--repo', 'maidiu/rawlsing',
                          '--body-file', str(path)], repo, timeout=60)
    if result['exit_code'] != 0:
        return 'GH_PUBLISH_FAILED__' + result['output'][-250:]
    return 'GH_COMMENT_PUBLISHED__' + result['output'].strip()


def review_template(item, receipt_rel):
    return ('# Independent hostile receiving — PR #' + str(item['pr']) + '\n'
            '\nSource HEAD: `' + item['sha'] + '`\n'
            'Machine execution receipt: `' + receipt_rel + '`\n'
            'Verdict: HOLD until a distinct reviewer completes this record.\n'
            '\n## Source owner inspection\n'
            'Inspect exact historical first fault, source function, original test and inherited law.\n'
            '\n## New adversarial probes\n'
            'Name fresh independently authored negative/positive tests and record actual outputs.\n'
            '\n## Code reading and causal analysis\n'
            'Explain why code does or does not close the first fault and conserve older behavior.\n'
            '\n## Independence and limits\n'
            'Identify author separation, original P070/P071 author conflict, GitHub credential conflicts, native E holds.\n'
            '\n## Verdict\n'
            'ACCEPT_SCOPED / REVISE_EXACT_DEFECT / HOLD. Do not auto-accept.\n'
            '\n## Evidence\n'
            'Exact SHA, raw test file paths, command logs, cold SQLite receipts, red/green.\n')


def main(argv=None):
    ap = argparse.ArgumentParser(description='REMONT sourcefree machine verification queue')
    ap.add_argument('command', nargs='?', default='run', choices=['run','list','record-review','summary'])
    ap.add_argument('--queue', type=Path, default=DEFAULT_QUEUE)
    ap.add_argument('--repo', type=Path, default=REPO_ROOT)
    ap.add_argument('--results', type=Path)
    ap.add_argument('--python', default=None)
    ap.add_argument('--pr', type=int, action='append', help='restrict to one or several PR numbers')
    ap.add_argument('--force', action='store_true', help='repeat even if exact-head compatibility already PASS')
    ap.add_argument('--publish', action='store_true', help='publish the sourcefree verification receipt via gh pr comment')
    ap.add_argument('--reviewer', help='reviewer identity, for record-review')
    ap.add_argument('--independence-basis', help='specific reviewer/author separation, for record-review')
    ap.add_argument('--evidence', type=Path, help='complete independently written hostile review file')
    ap.add_argument('--verdict', choices=sorted(ALLOWED_VERDICTS))
    args = ap.parse_args(argv)
    q = validate_queue(load_json(args.queue))
    repo = args.repo.resolve()
    results = args.results.resolve() if args.results else repo / q['local_results_path']
    state = load_state(results / 'ledger.json')
    state['_results_path'] = results
    items = pick(q, args)
    if args.command in ('list','summary'):
        print_queue(items,state)
        return 0
    if args.command == 'record-review':
        if len(items) != 1 or not args.reviewer or not args.independence_basis or not args.evidence or not args.verdict:
            ap.error('record-review requires a single --pr, --reviewer, --independence-basis, --evidence and --verdict')
        item = items[0]
        if args.verdict == 'ACCEPT_SCOPED' and not state['items'].get(state_key(item),{}).get('last_status') == 'COMPAT_PASS__HOSTILE_REVIEW_PENDING':
            ap.error('cannot ACCEPT_SCOPED without green source-identical 3.11 execution at exact head')
        text = args.evidence.read_text(encoding='utf-8')
        headings = ('## Source owner inspection', '## New adversarial probes',
                    '## Code reading and causal analysis', '## Independence and limits',
                    '## Verdict', '## Evidence')
        if (len(text) < 700 or any(h not in text for h in headings) or
                item['sha'] not in text or
                (args.verdict == 'ACCEPT_SCOPED' and
                 ('Verdict: HOLD until a distinct reviewer' in text or
                  'Name fresh independently authored negative/positive tests' in text or
                  not any(word in text for word in ('test_', 'negative probe', 'Negative probe'))))):
            ap.error('review evidence incomplete or untouched template; attach real independent probes')
        evidence_copy = results / 'reviews' / f"pr{item['pr']}_{uuid.uuid4().hex[:12]}_evidence.md"
        evidence_copy.parent.mkdir(parents=True, exist_ok=True)
        evidence_copy.write_text(text, encoding='utf-8')
        record = {'kind': 'REMONT_INDEPENDENT_HOSTILE_REVIEW_CANDIDATE_V1',
                  'evidence_file': str(evidence_copy.relative_to(results)),
                  'pr': item['pr'], 'sha': item['sha'], 'reviewer': args.reviewer,
                  'independence_basis': args.independence_basis, 'verdict': args.verdict,
                  'original_author_or_credential_independence_not_self_certified': True,
                  'native_receiving': False, 'protected_receiving': False,
                  'evidence_sha256': hashlib.sha256(text.encode()).hexdigest(),
                  'recorded_at_utc': utc_now()}
        output = results / 'reviews' / f"pr{item['pr']}_{uuid.uuid4().hex[:12]}.json"
        atomic_json(output,record)
        with state_lock(results):
            live_state = load_state(results/'ledger.json')
            row = live_state['items'].setdefault(state_key(item),{'reviews': []})
            row.setdefault('reviews', []).append({'file':str(output.relative_to(results)), **record})
            live_state['last_updated_at_utc'] = utc_now()
            atomic_json(results/'ledger.json',live_state)
        print(f"Review recorded: {output}\nThis is local independent engineering evidence, NOT protected or native acceptance.")
        if args.publish:
            msg = results / 'reviews' / f"pr{item['pr']}_{uuid.uuid4().hex[:12]}_comment.md"
            msg.parent.mkdir(parents=True,exist_ok=True)
            msg.write_text('# REMONT exact-head hostile review\n\n'+text+'\n',encoding='utf-8')
            print(publish_compat(repo,item,record,msg))
        return 0
    py = args.python or q['default_python']
    if not shutil.which(py) and not Path(py).is_file():
        print(f"HOLD: {py} not found; install Python 3.11 or pass --python /path/to/python3.11",file=sys.stderr)
        return 2
    if not (repo/'.git').exists():
        print(f"HOLD: {repo} is not a local Git worktree",file=sys.stderr)
        return 2
    # Sync remote refs once, but never change tracked source/queue head.
    fetched = run_process(['git','fetch','--no-tags','origin'],repo,timeout=180)
    if fetched['exit_code'] != 0:
        print('HOLD: git fetch origin failed: '+fetched['output'][-500:],file=sys.stderr)
        return 2
    any_failed=False
    for item in items:
        key = state_key(item)
        # A builder-owned source RED with an actively moving construction HEAD
        # must not consume the default independent-repair batch repeatedly.
        # Explicit --pr still permits deliberate historical exact-SHA replay.
        if item.get('execution_deferred') is True and not args.pr:
            print(f"#{item['pr']} DEFERRED_TO_SORACLE_BUILDER__HISTORICAL_RED__PIN_UNCHANGED: "
                  f"{item.get('defer_reason','builder source not frozen')}")
            continue
        if not needs_execution(state,key,args.force):
            print(f"#{item['pr']} pinned compatibility PASS already recorded; hostile review still required unless independently received")
            continue
        print(f"Checking #{item['pr']} exact {item['sha']} ...",flush=True)
        receipt = run_candidate(repo,item,py,q,fetch=True)
        path = record_receipt(results,key,receipt)
        state = load_state(results/'ledger.json')
        state['_results_path']=results
        print(f"#{item['pr']} {receipt['status']} -> {path}")
        if receipt['status'] == 'COMPAT_PASS__HOSTILE_REVIEW_PENDING':
            templ = results / 'review_templates' / ('pr'+str(item['pr'])+'_'+item['sha'][:12]+'.md')
            templ.parent.mkdir(parents=True, exist_ok=True)
            if not templ.exists():
                templ.write_text(review_template(item,str(path.relative_to(results))),encoding='utf-8')
            print('HOSTILE REVIEW NEXT: inspect source and invent additional tests; fill '+str(templ))
        else:
            any_failed=True
        if args.publish:
            # gh expects a Markdown body, not raw JSON; title and exact status stay explicit.
            comment = results / 'runs' / ('pr'+str(item['pr'])+'_'+uuid.uuid4().hex[:12]+'_comment.md')
            lines = ['## REMONT local exact-head Python compatibility check',
                     '', 'PR: #' + str(item['pr']),
                     'Immutable source SHA: `' + item['sha'] + '`',
                     'Status: **' + receipt['status'] + '**',
                     'Interpreter: `' + str(receipt.get('python_version','NOT_VERIFIED')) + '`',
                     'Source manifest: `' + str(receipt.get('source_manifest',{}).get('verified_python_files',0)) + '` Python files independently hashed.',
                     '', '### Executed courts']
            for test in receipt.get('tests',[]):
                lines.extend(['- `' + ' '.join(test['command']) + '` => exit ' + str(test['exit_code']),
                              '  ' + test.get('output','').strip()[-900:].replace('\n',' | ')])
            if 'sqlite_demo' in receipt:
                lines.extend(['', '### SQLite cold-reopen',
                    '```json', json.dumps(receipt['sqlite_demo'],indent=2), '```'])
            if receipt.get('failure_detail'):
                lines.extend(['', 'Failure/hold: `'+str(receipt['failure_detail'])[-1000:]+'`'])
            lines.extend(['', 'Complete raw local transcript: `'+str(path.relative_to(results))+'`.',
                '**Automatic compatibility results only. No hostile review, native G5, protected receiving, or scientific accreditation is issued.**'])
            comment.write_text('\n'.join(lines)+'\n',encoding='utf-8')
            print('Publish:',publish_compat(repo,item,receipt,comment))
    print('\nQueue test runs completed. Independently authored hostile reviews still require agent execution; tests alone DO NOT ACCEPT.')
    return 1 if any_failed else 0


if __name__ == '__main__':
    sys.exit(main())
