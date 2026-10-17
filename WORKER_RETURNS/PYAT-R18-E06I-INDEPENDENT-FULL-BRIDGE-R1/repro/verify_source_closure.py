"""Independent re-verification of the staged native source closure.

Does not use the candidate's stage_sources.py.  Checks:
  * the candidate source_manifest has 402 entries;
  * every staged file matches its recorded Git NUL-header blob and SHA256;
  * the 401-object E05S manifest at its accepted pin is reproduced exactly;
  * the separately imported E04T owner module matches E04T commit 79cb8244;
  * the five nonempirical E04T product modules are byte-identical to the
    E05S-staged originals (no owner patch).
"""
import hashlib, json, os, subprocess, sys

CAND = os.path.realpath(os.environ['E06_CANDIDATE_ROOT'])
E05S = 'f524f60781e2e7e72278d04d6377fb1da877698a'
E05S_PATH = 'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R14-E05S-INDEPENDENT-SELECTED-WORLD-R1/'
E04T = '79cb8244a5291218bde17142b93fc2419eade396'
E04T_PATH = 'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-E04T-NATIVE-CURRENT-GRANT-REPAIR-R1/'


def blob(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest(), hashlib.sha256(b).hexdigest()


def show(commit, path):
    return subprocess.check_output(['git', 'show', commit + ':' + path], cwd=CAND)


manifest = json.loads(open(os.path.join(CAND, 'source_manifest.json')).read())
assert len(manifest) == 402, len(manifest)
checked = 0
for x in manifest:
    oid, sha = blob(os.path.join(CAND, x['local']))
    assert oid == x['git_blob'], x['local']
    assert sha == x['sha256'], x['local']
    checked += 1

e05s = json.loads(show(E05S, E05S_PATH + 'source_manifest.json'))
assert len(e05s) == 401
for x in e05s:
    local = os.path.join(CAND, 'runtime', x['local'])
    oid, sha = blob(local)
    assert oid == x['git_blob'] and sha == x['sha256'], x['local']
    assert show(x['commit'], x['path']) == open(local, 'rb').read(), x['local']

owner = os.path.join(CAND, 'runtime', 'owners', 'e04t_empirical.py')
assert show(E04T, E04T_PATH + 'product/empirical.py') == open(owner, 'rb').read()
unchanged = []
for name in ('__init__.py', 'service.py', 'world.py', 'nonparent.py', 'scenario.py'):
    assert show(E04T, E04T_PATH + 'product/' + name) == open(os.path.join(CAND, 'runtime', 'product', name), 'rb').read(), name
    unchanged.append(name)

print(json.dumps(dict(schema='E06I_INDEPENDENT_SOURCE_CLOSURE_PROOF@1', manifest_entries=len(manifest),
                      verified_preimages=checked, e05s_objects=len(e05s),
                      e04t_owner_commit=E04T, e05s_commit=E05S,
                      e04t_nonempirical_modules_byte_identical=unchanged,
                      candidate_bridge_sha256=hashlib.sha256(open(os.path.join(CAND, 'bridge.py'), 'rb').read()).hexdigest()),
                 indent=1))
