#!/usr/bin/env python3
"""Read-only documentary integrity verification; never imports Rawlsing code."""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'MANIFEST.json').read_text())
for item in manifest['files']:
    data = (root / item['path']).read_bytes()
    assert len(data) == item['bytes'], item['path']
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == item['git_blob_sha1'], item['path']
links = 0
for path in root.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' not in target:
            assert (path.parent / target.split('#')[0]).is_file(), (path, target)
        links += 1
board = json.loads((root / 'data/task_board.json').read_text())
tasks = {x['id']: x for x in board['tasks']}
assert len(tasks) == len(board['tasks'])
seen, active = set(), set()
def visit(key):
    if key in seen:
        return
    assert key not in active, ('cycle', key)
    active.add(key)
    for dep in tasks[key]['required_tasks'] + [x['task'] for x in tasks[key]['conditional_tasks']]:
        assert dep in tasks, dep
        visit(dep)
    active.remove(key)
    seen.add(key)
for key in tasks:
    visit(key)
    assert (root / tasks[key]['spec']).is_file()
    assert tasks[key]['state'] == 'PLANNED'
    assert tasks[key]['owner_session'] is None
policy = json.loads((root / 'data/escalation_policy.json').read_text())
scenarios = json.loads((root / 'data/escalation_scenarios.json').read_text())['scenarios']
for row in scenarios:
    route = policy['routes'].get(row['classified_issue'], policy['default_route'])
    assert route == row['expected_route'], row['id']
assert not policy['astra_silence_is_approval']
assert not policy['astra_can_invent_semantic_authority']
assert not policy['raw_source_permission_from_plan']
assert not policy['actor_implementation_permission_from_plan']
assert not board['new_workers_dispatched']
print(json.dumps({'status': 'PASS_DOCUMENTARY_INTEGRITY_ONLY', 'manifest_files_verified':len(manifest['files']), 'links_checked':links, 'task_nodes':len(tasks), 'graph':'ACYCLIC', 'routing_examples':len(scenarios), 'rawlsing_tests_executed':False}, indent=2))
