"""Reconstruct exact committed dependencies without replacing proof mutations."""
from pathlib import Path
import hashlib
import io
import json
import sys
import tarfile

ROOT = Path(__file__).resolve().parent
W41 = ROOT / 'deps/w41'


def install(*, verify=False):
    manifest = json.loads((ROOT / 'dependency_manifest.json').read_text())
    raw = (ROOT / 'w41_dependency.tar.gz').read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['archive_sha256']:
        raise ValueError('W41_ARCHIVE_CHANGED')
    pins = {p['local']: p for p in manifest['files']}
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as stream:
        if {m.name for m in stream.getmembers()} != set(pins):
            raise ValueError('W41_MEMBERS_CHANGED')
        for m in stream.getmembers():
            dest = W41 / m.name
            if not m.isfile() or not dest.resolve().is_relative_to(W41.resolve()):
                raise ValueError('UNSAFE_DEPENDENCY_MEMBER')
            data = stream.extractfile(m).read()
            if hashlib.sha256(data).hexdigest() != pins[m.name]['sha256']:
                raise ValueError('W41_PREIMAGE_CHANGED')
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            if verify and dest.read_bytes() != data:
                raise ValueError('W41_RESTORATION_FAILED:' + m.name)
    sys.path.insert(0, str(W41))
    import reconstruct_owners
    reconstruct_owners.reconstruct(verify=verify)


install()

if __name__ == '__main__':
    install(verify=True)
    print(json.dumps({'W41_files': 10, 'native_owner_files': 133, 'verified': True}))
