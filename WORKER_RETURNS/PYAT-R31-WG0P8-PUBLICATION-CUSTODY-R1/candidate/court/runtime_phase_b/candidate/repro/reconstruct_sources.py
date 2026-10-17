"""Verify or reconstruct only manifest-listed exact source-free Git preimages.

Default verifies. --materialize writes missing staged files; existing mismatches
are refused. Uses shared object store; never clones, fetches, resets or adopts.
"""
import hashlib,json,pathlib,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];materialize=sys.argv[1:]==['--materialize'];count=0
for row in json.loads((R/'source_selector.json').read_text())['files']:
    rel=pathlib.PurePosixPath(row['staging_path'])
    if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('INVALID_STAGING_PATH')
    p=R/'pinned'/str(rel)
    if not p.exists():
        if not materialize:raise RuntimeError('MISSING_PINNED_SOURCE:'+str(rel))
        raw=subprocess.check_output(['git','show',row['commit']+':'+row['source_path']])
        if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=row['git_blob_sha1']:raise RuntimeError('GIT_PREIMAGE_MISMATCH')
        p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    raw=p.read_bytes();git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    actual=subprocess.check_output(['git','hash-object',str(p)],text=True).strip()
    assert git_blob==actual==row['git_blob_sha1'] and hashlib.sha256(raw).hexdigest()==row['sha256'],str(rel)
    count+=1
print('EXACT_PINNED_GIT_PREIMAGE_VERIFIED',count)
