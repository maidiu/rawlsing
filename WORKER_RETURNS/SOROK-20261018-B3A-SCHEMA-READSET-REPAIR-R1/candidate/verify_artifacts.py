"""Read-only verification of delivered hashes; execute run_all.py for fresh proof."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'artifact_manifest.json').read_text())
for row in manifest['files']:
 p=ROOT/row['path'];assert p.is_file() and p.stat().st_size==row['bytes']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],row['path']
print('Verified',len(manifest['files']),'delivered files;',manifest['grade'])
