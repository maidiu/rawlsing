"""Independent exact-Git staging; candidate staging code is never executed."""
import ast, datetime, hashlib, json, pathlib, subprocess, uuid
RET = pathlib.Path(__file__).resolve().parents[1]
ROOT = RET.parents[1]
RT = RET / 'runtime_root'
C = '49992b28becfdbecbd41d9dbead47532bf0b6af9'
CP = 'WORKER_RETURNS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1'
OLDCP = 'WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1'
if RT.exists(): raise SystemExit('EXISTING_RUNTIME_REFUSE_OVERWRITE')
RT.mkdir()
rows, mapped = [], {}
def git(*args): return subprocess.check_output(['git', '-C', str(ROOT), *args])
def put(commit, source, dest, expected=None, family='closure'):
    raw = git('show', commit + ':' + source)
    blob = git('rev-parse', commit + ':' + source).decode().strip()
    assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + bytes([0]) + raw).hexdigest() == blob
    assert expected is None or expected == blob, (source, expected, blob)
    out = RT / dest
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(raw)
    row = dict(commit=commit, source_path=source, staging_path=dest,
               git_blob_sha1=blob, sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw), family=family)
    rows.append(row); mapped[dest] = row
    return raw
manifest = json.loads(put(C, CP + '/staging/staging_manifest.json', CP + '/staging/staging_manifest.json', family='candidate_manifest_metadata'))
assert len(manifest['entries']) == 29
for e in manifest['entries']:
    dest = CP + '/staging/' + e['staged_path']
    raw = put(e['source_rev'], e['repo_path'], dest, e['git_blob_sha1'], 'original_29')
    # Independently check the author's copied object against its actual original.
    assert raw == git('show', C + ':' + dest), dest
for path in git('ls-tree', '-r', '--name-only', C, CP+'/port', CP+'/conftest.py').decode().splitlines():
    put(C, path, path, family='C0_candidate')
# Original RC0 hardcodes these schema paths; mirror original oracle bytes only.
for e in manifest['entries']:
    if e['staged_path'].startswith('oracles/'):
        put(e['source_rev'], e['repo_path'], OLDCP+'/'+e['staged_path'], e['git_blob_sha1'], 'RC0_oracle_layout')
# Exact original K9/K10 source, separate from candidate's revised source.
for name in ['test_k9_provider_swap.py', 'test_k10_structural_conservation.py']:
    put('b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59', OLDCP+'/port/'+name,
        CP+'/original_tests/'+name, family='unchanged_HQ298_K9K10')
queue = [r for r in rows if r['staging_path'].endswith('.py')]
seen = set()
def module(name):
    if not name.startswith('rawlsing_next'): return
    rel = name.replace('.', '/') + '.py'
    if CP+'/staging/ns/'+rel in mapped or rel in mapped: return
    if subprocess.run(['git','-C',str(ROOT),'cat-file','-e',C+':'+rel],capture_output=True).returncode: return
    put(C, rel, rel, family='transitive_import'); queue.append(mapped[rel])
for n in ['rawlsing_next.m4_v557_v558_publication_repository','rawlsing_next.m5_runtime_rsc_peer_prior','rawlsing_next.source_backed_positioned_subject_possibility']: module(n)
while queue:
    row=queue.pop(); rel=row['staging_path']
    if rel in seen: continue
    seen.add(rel)
    tree=ast.parse((RT/rel).read_text())
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            for a in n.names: module(a.name)
        elif isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('rawlsing_next'):
            module(n.module)
            for a in n.names: module(n.module+'.'+a.name)
# Reproduce the frozen RC0 baseline in a separate package namespace/process.
for path in git('ls-tree','-r','--name-only','b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59',OLDCP+'/port').decode().splitlines():
    put('b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59',path,'baseline/port/'+pathlib.Path(path).name,family='frozen_original_RC0_baseline')
for e in manifest['entries']:
    if e['staged_path'].startswith('oracles/'):
        put(e['source_rev'],e['repo_path'],'baseline/'+e['staged_path'],e['git_blob_sha1'],family='frozen_original_RC0_baseline')
put('86bd2a54687b40401f7c4247607bd1873c585619','WORKER_RETURNS/SOROK-R3-HQ299-RC0-SC0-PE-INDEPENDENT-R1/reviewer_tests/test_rc0_hostile.py','baseline/test_rc0_hostile.py',family='frozen_original_RC0_baseline')
marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),role='RSC0_INDEPENDENT_C0_AUTHOR; PRIOR_RC0_REVIEWER_CONTINUITY',permissions='TEST_ONLY_NO_SURVEY_MODEL_OR_ACTOR',candidate=C)
(RT/'runtime_marker.json').write_text(json.dumps(marker,indent=2)+'\n')
(RET/'source_selector.json').write_text(json.dumps(dict(schema='RSC0_GENUINE_GIT_SOURCE_CUSTODY@1',candidate=C,original_pin_count=29,files=rows,actual_NUL_verified=True),indent=2)+'\n')
(RT/'repro/observations').mkdir(parents=True)
print('VERIFIED_ORIGINAL29_AND_TOTAL',len(rows),'EPOCH',marker['epoch_id'])
