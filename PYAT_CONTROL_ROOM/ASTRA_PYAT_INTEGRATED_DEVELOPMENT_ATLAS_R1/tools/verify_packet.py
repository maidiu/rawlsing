"""Read-only verification of this documentary packet. No Rawlsing execution."""
import hashlib
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'MANIFEST.json').read_text())
expected = {r['path']: r for r in manifest['files']}
actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
          if p.is_file() and p.name != 'MANIFEST.json'
          and not any(part.startswith('_') for part in p.relative_to(root).parts)}
assert actual == set(expected), {'missing': sorted(set(expected)-actual), 'unexpected': sorted(actual-set(expected))}
for name, record in expected.items():
    data = (root / name).read_bytes()
    assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == record['git_blob_sha1'], name
nodes = json.loads((root / 'data/nodes.json').read_text())
by_id = {n['id']: n for n in nodes}
seen, stack = set(), set()
def visit(key):
    assert key not in stack, ('cycle', key)
    if key in seen:
        return
    stack.add(key)
    n = by_id[key]
    for parent in n['requires'] + [e['node'] for e in n['conditional']]:
        assert parent in by_id, parent
        visit(parent)
    stack.remove(key)
    seen.add(key)
for key in by_id:
    visit(key)
assert len(nodes) == 16
assert len(json.loads((root / 'data/accepted53.json').read_text())) == 53
assert len(json.loads((root / 'data/longmemory44.json').read_text())) == 44
sources = json.loads((root / 'data/closed35.json').read_text())
assert len(sources) == 35 and Counter(r[2] for r in sources) == {'P': 20, 'B': 15}
assert json.loads((root / 'data/validation.json').read_text())['status'] == 'PASS'
print(json.dumps({'status': 'PASS', 'files_verified': len(expected), 'dependency_graph': 'ACYCLIC',
                  'scope': 'DOCUMENTARY_PACKET_ONLY__NO_RUNTIME_OR_SOURCE_EXECUTION'}, indent=2))
