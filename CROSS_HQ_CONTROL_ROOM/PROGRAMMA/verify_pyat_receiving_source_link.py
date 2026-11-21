"""Fail-closed source/link check for EXISTING PYAT G4 + paired progress, not semantic science."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

G4 = 'PYAT_CONTROL_ROOM/PROGRAMMA_PYAT/05_ROADMAP/'
INDEX = G4 + 'INDEX.jsonl'
GUIDE = G4 + 'README.md'
MD = 'PYAT_CONTROL_ROOM/CURRENT_PROGRESS.md'
JS = 'PYAT_CONTROL_ROOM/CURRENT_PROGRESS.json'
EXTS = {'.py', '.js', '.mjs', '.ts', '.sql', '.sh', '.json'}


def relevant(path: str) -> bool:
    p = Path(path)
    if p.suffix not in EXTS or p.name.startswith('test_') or '/tests/' in '/' + path:
        return False
    return (path.startswith(('rawlsing_next/', 'data/ddm_build_copy/')) or
            (path.startswith('WORKER_RETURNS/') and '/candidate/' in path))


def changed_rows(old: list, new: list) -> list:
    previous = {str(r.get('id')): r for r in old}
    return [r for r in new if previous.get(str(r.get('id'))) != r]


def evaluate(paths: set[str], previous_rows: list, current_rows: list,
             old_rev: int, new_rev: int) -> list[str]:
    changed = sorted(p for p in paths if relevant(p))
    if not changed:
        return []
    problems = []
    required = {GUIDE, INDEX, MD, JS}
    if not required.issubset(paths):
        problems.append('MISSING_SAME_RECEIVING_G4_AND_PAIRED_PROGRESS:' + ','.join(sorted(required - paths)))
    if new_rev != old_rev + 1:
        problems.append(f'PYAT_PROGRESS_REV_NOT_INCREMENTED:{old_rev}->{new_rev}')
    rows = changed_rows(previous_rows, current_rows)
    if not rows:
        problems.append('G4_NO_CHANGED_FUNCTION_SOURCE_ROW')
    for path in changed:
        if not any(path in json.dumps(row, sort_keys=True) for row in rows):
            problems.append('G4_AFFECTED_FUNCTION_SOURCE_NOT_RECONCILED:' + path)
    return problems


def sh(*parts: str) -> str:
    return subprocess.check_output(parts, text=True).strip()


def load_jsonl(text: str) -> list:
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def check(base: str) -> int:
    paths = set(sh('git', 'diff', '--name-only', base, 'HEAD', '--').splitlines())
    previous_rows = load_jsonl(sh('git', 'show', base + ':' + INDEX))
    current_rows = load_jsonl(Path(INDEX).read_text())
    old_rev = json.loads(sh('git', 'show', base + ':' + JS))['revision']
    new_rev = json.loads(Path(JS).read_text())['revision']
    problems = evaluate(paths, previous_rows, current_rows, old_rev, new_rev)
    receipt = {'grade': 'STRUCTURAL_RECEIVING_GUARD_NOT_FUNCTIONAL_VALIDATION',
               'base': base, 'head': sh('git', 'rev-parse', 'HEAD'),
               'changed_source_count': sum(map(relevant, paths)), 'problems': problems}
    print(json.dumps(receipt, sort_keys=True))
    return 1 if problems else 0


def self_test() -> int:
    a = 'rawlsing_next/pre553_s04_uncertain_repertoire.py'
    b = 'rawlsing_next/pre553_s04_determinicity_cycle.py'
    fixtures = [
        ('proper source+G4+pair', {a, GUIDE, INDEX, MD, JS}, [], [{'id': 'ROADMAP:S04', 'source_paths': [a]}], 13, 14, True),
        ('unrelated G4 edit rejected', {a, GUIDE, INDEX, MD, JS}, [], [{'id': 'OTHER', 'source_paths': ['unrelated.py']}], 13, 14, False),
        ('second source not indexed rejected', {a, b, GUIDE, INDEX, MD, JS}, [], [{'id': 'ROADMAP:S04', 'source_paths': [a]}], 13, 14, False),
        ('missing paired update rejected', {a, GUIDE, INDEX}, [], [{'id': 'ROADMAP:S04', 'source_paths': [a]}], 13, 14, False),
        ('stale rev rejected', {a, GUIDE, INDEX, MD, JS}, [], [{'id': 'ROADMAP:S04', 'source_paths': [a]}], 13, 13, False),
        ('test-only change does not force G4', {'rawlsing_next/tests/test_x.py'}, [], [], 13, 13, True),
    ]
    details = []
    for title, paths, before, after, old, new, should_pass in fixtures:
        problems = evaluate(paths, before, after, old, new)
        ok = (not problems) == should_pass
        details.append({'name': title, 'pass': ok, 'problems': problems})
    print(json.dumps({'self_test': details, 'pass': all(d['pass'] for d in details)}))
    return 0 if all(d['pass'] for d in details) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--base')
    opts = parser.parse_args()
    if opts.self_test:
        raise SystemExit(self_test())
    if not opts.base:
        parser.error('check mode requires --base exact Git commit')
    raise SystemExit(check(opts.base))
