#!/usr/bin/env python3
"""O-INDEX live intake anti-staleness verifier. No scientific or receiving authority.

Run offline: python3 check_live_receiving.py --snapshot authenticated_observation.json
Run live:    GITHUB_TOKEN=... python3 check_live_receiving.py --live
This tool never makes changes to GitHub or the existing REMONT queues.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
BASE_SHA = 'fbc2080403607d85cd67a025b8a9a4ebd41e70c1'
PINNED_FILES = {
    '00_START_HERE.md': 'd3bd3eb39059e087004f04456aab4961d9dec5aa',
    '01_SOURCE_OF_TRUTH_REGISTRY.json': 'f530cf193cc0f8c3d93324b5e2b865a4efa3bd34',
    '02_L0_L5_LINKED_ORCHESTRATION_INDEX.json': 'c819ce08edc709e325fb124b92371f83fb7198a5',
    '03_RECOVERY_AND_FOUR_RETURN_ASSET_INDEX.md': '459cd1024280b18106c6125bfd6ecaa195208705',
    '04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json': 'c6a872f85ed52aad1a0bde61f1132cde99fbb7dc',
    '05_VALIDATOR_AND_READBACK.md': 'fd562f0f0382aabb5969046fdc475be9caa29a38',
    '06_PRIMARY_SOURCE_CORRECTION_AND_HQ_ADJUDICATION.md': '8904a562de851286858b59bd8b81cc00a6372842',
    'source_manifest.json': 'dd100bc114a29f12a655aa6c7ee69258c14c55ec',
    'test_validate_index.py': '03894a24ca3b270330039da22db603dc839b183a',
    'validate_index.py': 'f62e0d0eddafcc65a955b5a24acbdf7312b08e51',
    'verify_source_manifest.py': '9530f3bd04676fb7d42715e9df95700fe85d4191',
}
RELEVANT = re.compile(r'SOROK|SORACLE|SOROK REMONT|UM.SOROK|SEAM|MULCH|MECHANISM|O.INDEX|PROGRAMMA', re.I)
SHA = re.compile(r'^[0-9a-f]{40}$')


def sha_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def verify_inherited_files(directory=ROOT):
    problems = []
    for path, sha in PINNED_FILES.items():
        f = directory / path
        if not f.is_file() or sha_blob(f.read_bytes()) != sha:
            problems.append('R3_SOURCE_BLOB_MISSING_OR_CHANGED:' + path)
    for path, count, key in [('01_SOURCE_OF_TRUTH_REGISTRY.json', 144, 'rows'),
                             ('02_L0_L5_LINKED_ORCHESTRATION_INDEX.json', 219, 'nodes'),
                             ('source_manifest.json', 167, 'rows'),
                             ('04_UNDECIDED_SCIENCE_DEPENDENCY_AND_OWNER_SLOTS.json', 46, 'slots')]:
        try:
            d = json.loads((directory / path).read_text())
            if len(d[key]) != count:
                problems.append('R3_SOURCE_DENOMINATOR_CHANGED:' + path)
            if path.startswith('02_') and (d['edge_count'] != 461 or len(d['edges']) != 461):
                problems.append('R3_GRAPH_EDGE_LOSS')
        except (ValueError, KeyError, FileNotFoundError) as exc:
            problems.append('R3_SOURCE_UNREADABLE:' + path + ':' + str(exc))
    return problems


def verify_readable_status(directory=ROOT):
    """The readable candidate-status view must pin the exact current ledger blob."""
    try:
        raw = (directory / 'LIVE_RECEIVING_LEDGER.json').read_bytes()
        status = (directory / 'READABLE_CANDIDATE_STATUS_20261121.md').read_text()
    except OSError:
        return ['READABLE_LEDGER_VIEW_MISSING']
    m = re.search(r'exact Git \*\*blob `([0-9a-f]{40})`', status)
    if not m or m.group(1) != sha_blob(raw):
        return ['READABLE_LEDGER_VIEW_STALE']
    return []


def progress_errors(md, state):
    problems = []
    m = re.search(r'current progress revision\s*(\d+)', md, re.I)
    if not m:
        problems.append('PROGRESS_MD_REVISION_MISSING')
    elif int(m.group(1)) != state.get('revision'):
        problems.append('MD_JSON_REVISION_CONTRADICTION')
    if state.get('owner') != 'Sorok':
        problems.append('WRONG_PROGRESS_OWNER')
    return problems


def audit(ledger, snapshot, md='', progress=None):
    errors, holds = [], []
    if progress is not None:
        errors += progress_errors(md, progress)
    if ledger.get('schema') != 'SOROK_O_INDEX_LIVE_RECEIVING@1':
        errors.append('WRONG_LEDGER_SCHEMA')
    frozen = ledger.get('protected_baseline', {}).get('sha')
    if frozen != BASE_SHA:
        errors.append('LEDGER_PROTECTED_BASELINE_CHANGED_UNREVIEWED')
    if snapshot.get('protected_sha') != frozen:
        errors.append('PROTECTED_HEAD_MOVED_OR_UNOBSERVED')
    if not snapshot.get('scope_complete'):
        errors.append('DISCOVERY_SCOPE_INCOMPLETE_OR_UNAUTHENTICATED')
    records = ledger.get('records', [])
    indexed = {}
    for r in records:
        n = r.get('pr')
        if n in indexed:
            errors.append('DUPLICATE_PR:' + str(n))
        indexed[n] = r
        if not SHA.fullmatch(r.get('head_sha', '')):
            errors.append('INVALID_HEAD_SHA:' + str(n))
        if not r.get('originating_owner_lane') or not r.get('next_receiving_owner') or not r.get('smallest_next_action'):
            errors.append('MISSING_OWNER_OR_NEXT_ACTION:' + str(n))
        if not r.get('disposition'):
            errors.append('MISSING_RECEIVING_FATE:' + str(n))
        if r.get('pr_state') == 'closed' and not r.get('merged'):
            fate = r.get('disposition', '')
            if not any(s in fate for s in ('HELD', 'SUPERSEDED', 'REJECTED')):
                errors.append('UNRECEIVED_CLOSED_PR:' + str(n))
            if 'SUPERSEDED' in fate:
                target = r.get('successor_pr')
                if target not in indexed and not any(x.get('pr') == target for x in records):
                    errors.append('SUPERSEDED_WITHOUT_TRACKED_SUCCESSOR:' + str(n))
                if not r.get('retained_capabilities'):
                    errors.append('SUPERSEDED_WITHOUT_FUNCTION_CONSERVATION:' + str(n))
            if 'HELD' in fate:
                holds.append('CLOSED_UNMERGED_CONSERVATION_HELD:' + str(n))
        for evidence in ('test', 'review'):
            e = r.get(evidence, {})
            pin = e.get('executed_sha') if evidence == 'test' else e.get('sha')
            if e.get('applied_to_head') and pin != r.get('head_sha'):
                errors.append('FALSE_GREEN_STALE_' + evidence.upper() + ':' + str(n))
        a = r.get('authorities', {})
        for permission in ('science', 'actor', 'source', 'human'):
            if 'ISSUED' in str(a.get(permission, '')).upper() and 'NOT_ISSUED' not in str(a.get(permission, '')).upper():
                if not r.get('competent_authority_receipt'):
                    errors.append('FALSE_NATIVE_OR_SCIENCE_PROMOTION:' + str(n) + ':' + permission)
        if r.get('disposition', '').startswith('INDEPENDENTLY_REVIEWED') and not (r.get('review', {}).get('sha') and 'ACCEPT' in str(r.get('review', {}).get('verdict'))):
            errors.append('UNSUPPORTED_INDEPENDENT_REVIEW_CLAIM:' + str(n))
        if 'PROTECTED_RECEIVED' in r.get('disposition', '') and not r.get('merged'):
            errors.append('UNMERGED_ASSERTED_PROTECTED:' + str(n))
    observed = {p.get('pr'): p for p in snapshot.get('prs', [])}
    for n, r in indexed.items():
        p = observed.get(n)
        if p is None:
            errors.append('TRACKED_PR_NOT_LIVE_OBSERVED:' + str(n))
            continue
        if p.get('head_sha') != r.get('head_sha'):
            errors.append('MOVED_HEAD_STALE_LEDGER:' + str(n))
        if p.get('state') != r.get('pr_state') or bool(p.get('merged')) != bool(r.get('merged')):
            errors.append('CHANGED_BRANCH_FATE_STALE_LEDGER:' + str(n))
    routed = {}
    for route in ledger.get('discovery_routes', []):
        n = route.get('pr')
        if (n in routed or n in indexed
                or route.get('route') not in {'PYAT_G4_CROSSLINK_ONLY', 'OUT_OF_SCOPE'}
                or not route.get('reason') or not route.get('evidence')
                or not SHA.fullmatch(route.get('head_sha', ''))):
            errors.append('INVALID_DISCOVERY_ROUTE:' + str(n))
            continue
        routed[n] = route
        current = observed.get(n, {})
        if (current.get('head_sha') != route['head_sha']
                or current.get('state') != route.get('pr_state')
                or bool(current.get('merged')) != bool(route.get('merged'))):
            errors.append('STALE_DISCOVERY_ROUTE:' + str(n))
    proposal = observed.get(1258, {})
    proposal_matches = (
        proposal.get('head_branch') == 'receiving/sorok-o-index-baseline-20261121'
        and proposal.get('base_branch') == 'agent/sorok-programma-live-receiving-ledger-20261121-r1'
        and (
            (proposal.get('state'), proposal.get('draft'), proposal.get('merged'))
            in {('open', True, False), ('closed', False, True)}
        )
    )
    for n, p in observed.items():
        if n == 1258 and proposal_matches:
            continue
        if n not in indexed and n not in routed and RELEVANT.search(p.get('title', '')):
            errors.append('UNRECORDED_NEW_RELEVANT_PR:' + str(n))
    for event in ledger.get('event_history', []):
        n, sha = event.get('pr'), event.get('immutable_sha')
        if n not in indexed or not SHA.fullmatch(str(sha or '')):
            errors.append('EVENT_ORPHAN_OR_INVALID_CUT:' + str(event.get('id')))
        if event.get('protected_received') is True and not indexed[n].get('merged'):
            errors.append('FALSE_EVENT_PROTECTED_RECEIVING:' + str(n))
    return sorted(set(errors)), sorted(set(holds))


def fetch_live(repo, ledger):
    token = os.getenv('GITHUB_TOKEN') or os.getenv('GH_TOKEN')
    if not token:
        raise RuntimeError('GITHUB_TOKEN_OR_GH_TOKEN_MISSING: live verification unavailable; HOLD')
    def get(url):
        req = Request('https://api.github.com/' + url.lstrip('/'),
                      headers={'Authorization': 'Bearer ' + token,
                               'Accept': 'application/vnd.github+json',
                               'X-GitHub-Api-Version': '2022-11-28'})
        with urlopen(req, timeout=25) as response:
            return json.load(response)
    ref = get('repos/' + repo + '/git/ref/heads/integration/pre-main-reconciliation-r1')
    observed = {}
    for r in ledger['records'] + ledger.get('discovery_routes', []):
        p = get('repos/' + repo + '/pulls/' + str(r['pr']))
        observed[r['pr']] = dict(pr=r['pr'], title=p['title'], head_sha=p['head']['sha'], state=p['state'], merged=p['merged'])
    proposal = get('repos/' + repo + '/pulls/1258')
    observed[1258] = dict(pr=1258, title=proposal['title'], head_sha=proposal['head']['sha'],
                          state=proposal['state'], merged=proposal['merged'], draft=proposal['draft'],
                          head_branch=proposal['head']['ref'], base_branch=proposal['base']['ref'])
    page = 1
    while True:
        q = quote('repo:' + repo + ' is:pr updated:>=2026-11-18')
        search = get('search/issues?q=' + q + '&per_page=100&page=' + str(page))
        for p in search['items']:
            n = p['number']
            if n not in observed:
                observed[n] = dict(pr=n, title=p['title'], head_sha='UNKNOWN', state=p['state'], merged=False)
        if len(search['items']) < 100:
            break
        page += 1
        if page > 10:
            raise RuntimeError('LIVE_DISCOVERY_PAGINATION_EXCEEDED: cannot establish complete scoped scan')
    return dict(protected_sha=ref['object']['sha'], scope_complete=True, prs=list(observed.values()))


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--live', action='store_true')
    mode.add_argument('--snapshot', type=Path)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--progress-dir', type=Path, default=ROOT.parent.parent)
    args = ap.parse_args()
    problems = verify_inherited_files(args.root) + verify_readable_status(args.root)
    try:
        ledger = json.loads((args.root / 'LIVE_RECEIVING_LEDGER.json').read_text())
        if args.live:
            snapshot = fetch_live('maidiu/rawlsing', ledger)
        else:
            snapshot = json.loads(args.snapshot.read_text())
        md = (args.progress_dir / 'CURRENT_PROGRESS.md').read_text()
        pj = json.loads((args.progress_dir / 'CURRENT_PROGRESS.json').read_text())
        e, h = audit(ledger, snapshot, md, pj)
        problems += e
    except (OSError, ValueError, RuntimeError, KeyError) as exc:
        problems.append('SOURCE_OR_LIVE_OBSERVATION_HOLD:' + str(exc))
        h = []
    print(json.dumps({'status': 'RED_HQ_CURRENTNESS_HOLD' if problems else
                      ('PASS_SCOPED_WITH_HELD_CLOSED_BRANCHES' if h else 'PASS_SCOPED_SOURCE_AND_HEADS'),
                      'mode': 'AUTHENTICATED_LIVE' if args.live else 'SNAPSHOT_ONLY_NOT_LIVE',
                      'errors': sorted(set(problems)), 'holds': h}, indent=2))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
