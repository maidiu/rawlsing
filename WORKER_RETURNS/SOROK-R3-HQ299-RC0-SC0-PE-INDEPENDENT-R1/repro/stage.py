"""Independent minimal Git staging. Parse author selector as data, never execute it."""
import ast,hashlib,json,pathlib,subprocess,uuid,datetime
ROOT=pathlib.Path(__file__).resolve().parents[3];RET=pathlib.Path(__file__).resolve().parents[1]
C='b15dbbc4f07ae79e9ffb71e88e91e3b28b35da59';CP='WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1';RT=RET/'runtime_root';RETURN=RT/CP
if RT.exists():raise SystemExit('EXISTING_RUNTIME_REFUSE_TO_OVERWRITE')
RT.mkdir();rows=[];mapped={}
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args])
def put(commit,source,dest,expected=None,family='closure'):
    raw=git('show',commit+':'+source);blob=git('rev-parse',commit+':'+source).decode().strip()
    observed=hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
    assert observed==blob and (expected is None or expected==blob),(source,blob,expected)
    p=RT/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    row=dict(commit=commit,source_path=source,git_blob_sha1=blob,sha256=hashlib.sha256(raw).hexdigest(),staging_path=dest,bytes=len(raw),family=family,match=True)
    rows.append(row);mapped[dest]=row;return raw
script=git('show',C+':'+CP+'/staging/stage_closure.py').decode();tree=ast.parse(script)
pins=ast.literal_eval(next(n.value for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PINS' for t in n.targets)))
assert len(pins)==27
for commit,path,blob,dst in pins:
    local=CP+'/'+dst if dst.startswith('oracles/') else CP+'/staging/ns/'+dst
    put(commit,path,local,blob,'original_27_selector')
# Exact author package/validators/tests, no result files or author passport.
for path in git('ls-tree','-r','--name-only',C,CP+'/port',CP+'/conftest.py').decode().splitlines():put(C,path,path,family='SC0_candidate')
# Minimal static Python import closure from exact author tree. Staged overrides win.
queue=[row for row in rows if row['staging_path'].endswith('.py')];seen=set()
needed={'rawlsing_next.m4_v557_v558_publication_repository','rawlsing_next.m5_runtime_rsc_peer_prior','rawlsing_next.source_backed_positioned_subject_possibility'}
def stage_module(name):
    if not name.startswith('rawlsing_next'):return
    rel=name.replace('.','/')+'.py'
    if CP+'/staging/ns/'+rel in mapped or rel in mapped:return
    ok=subprocess.run(['git','-C',str(ROOT),'cat-file','-e',C+':'+rel],capture_output=True).returncode==0
    if not ok:return
    put(C,rel,rel,family='transitive_original_import');queue.append(mapped[rel])
for name in needed:stage_module(name)
while queue:
    row=queue.pop();rel=row['staging_path']
    if rel in seen:continue
    seen.add(rel)
    try:tree=ast.parse((RT/rel).read_text())
    except (SyntaxError,UnicodeError):continue
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            for a in n.names:stage_module(a.name)
        elif isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('rawlsing_next'):
            stage_module(n.module)
            for a in n.names:stage_module(n.module+'.'+a.name)
marker=dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),role='RC0_INDEPENDENT',source_permission='TEST_ONLY_NO_SURVEY_OR_ACTOR',candidate=C)
(RT/'rc0_runtime_marker.json').write_text(json.dumps(marker,indent=2)+'\n')
(RET/'source_selector.json').write_text(json.dumps(dict(schema='RC0_INDEPENDENT_GENUINE_GIT_COMPOSITE@1',candidate=C,pinned_selector_count=27,files=rows,actual_nul_header_verified=True,runtime_alias='$RC0_RETURN/runtime_root'),indent=2)+'\n')
print('STAGED_ORIGINAL_27',27,'TOTAL_STATIC_SOURCE_FILES',len(rows),'ENVIRONMENT_EPOCH',marker['epoch_id'])
