"""Recover only pinned committed metadata/code; never opens respondent files."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent


def recover():
    receipts = []
    for spec in json.loads((ROOT / 'source_manifest.json').read_text()):
        data = subprocess.check_output(['git', 'show', spec['commit'] + ':' + spec['path']])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if (len(data), blob, hashlib.sha256(data).hexdigest()) != (
            spec['bytes'], spec['blob_sha1'], spec['sha256']
        ):
            raise ValueError('pinned metadata/code preimage mismatch: ' + spec['path'])
        target = ROOT / spec['local']
        if not target.resolve().is_relative_to((ROOT / '.runtime/inputs').resolve()):
            raise ValueError('input path outside ignored metadata staging')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        receipts.append({'commit': spec['commit'], 'path': spec['path'], 'state': 'EXACT'})
    return receipts


if __name__ == '__main__':
    print(json.dumps({'state': 'PINNED_METADATA_CODE_ONLY', 'inputs': recover()}, indent=2))
