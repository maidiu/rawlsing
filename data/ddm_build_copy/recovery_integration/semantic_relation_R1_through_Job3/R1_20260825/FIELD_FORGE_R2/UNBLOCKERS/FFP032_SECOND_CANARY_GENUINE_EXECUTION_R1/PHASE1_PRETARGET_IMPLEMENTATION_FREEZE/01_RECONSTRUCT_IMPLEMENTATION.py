#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'01_IMPLEMENTATION_CHUNK_MANIFEST.json').read_text())
out=bytearray()
for part in manifest['parts']:
    p=ROOT/'implementation_chunks'/part['name']
    b=p.read_bytes()
    if len(b)!=part['bytes'] or hashlib.sha256(b).hexdigest()!=part['sha256']:
        raise SystemExit(f"FAIL chunk mismatch: {p.name}")
    out.extend(b)
if len(out)!=manifest['reconstructed_bytes'] or hashlib.sha256(out).hexdigest()!=manifest['reconstructed_sha256']:
    raise SystemExit('FAIL reconstructed implementation mismatch')
target=ROOT/manifest['reconstructed_filename']
target.write_bytes(bytes(out))
print(f"PASS {target} sha256:{manifest['reconstructed_sha256']}")
