"""Cold reconstruction of exact immutable sourcefree owner artifact bytes.

Unpack only absent files by default so an intentional proof fault remains
observable. --verify checks every pinned preimage and fails on any alteration.
"""
import hashlib,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def reconstruct(*,verify=False):
    manifest=json.loads((ROOT/'owner_archive_manifest.json').read_text())
    archive=ROOT/'native_owners.tar.gz'
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=manifest['archive_sha256']:
        raise ValueError('OWNER_ARCHIVE_INTEGRITY_FAILURE')
    pins=json.loads((ROOT/'owner_pins.json').read_text())
    allowed={p['local']:p for p in pins}
    with tarfile.open(archive,'r:gz') as stream:
        members=stream.getmembers()
        if {m.name for m in members}!=set(allowed):raise ValueError('OWNER_ARCHIVE_MEMBERSHIP_MISMATCH')
        for member in members:
            if not member.isfile():raise ValueError('NONFILE_OWNER_ARCHIVE_ENTRY')
            path=ROOT/member.name
            if not path.resolve().is_relative_to(ROOT/'owners'):raise ValueError('OUTSIDE_OWNER_TERRAIN')
            if not path.exists():
                data=stream.extractfile(member).read();path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    if verify:
        for rel,pin in allowed.items():
            data=(ROOT/rel).read_bytes()
            blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            if blob!=pin['blob_sha1'] or hashlib.sha256(data).hexdigest()!=pin['sha256']:
                raise ValueError('OWNER_PREIMAGE_MISMATCH:'+rel)
    return len(allowed)

if __name__=='__main__':
    import sys
    print(json.dumps(dict(verified_files=reconstruct(verify='--verify' in sys.argv))))
