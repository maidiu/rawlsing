"""Seal or verify this return's actual artifact bytes."""
import pathlib,hashlib,json,sys
R=pathlib.Path(__file__).resolve().parents[1]
skip={'artifact_sha256.json','publication_receipt.json'}
files=[p for p in sorted(R.rglob('*')) if p.is_file() and not any(z in ('runtime','primary','__pycache__','.pytest_cache') for z in p.relative_to(R).parts) and p.name not in skip and p.suffix!='.pyc']
actual={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
p=R/'artifact_sha256.json'
if '--write' in sys.argv:p.write_text(json.dumps(actual,indent=2)+'\n')
else:assert json.loads(p.read_text())==actual
print('Verified',len(actual),'return artifact SHA256 digests')
