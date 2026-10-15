"""Path/hostname aliases only; original source/oracles and science unchanged."""
from pathlib import Path
import json,hashlib,re
RET=Path(__file__).resolve().parents[1];ROOT=Path.cwd().resolve();changes=[]
for f in sorted(RET.rglob('*')):
 if not f.is_file() or any(x in f.relative_to(RET).parts for x in ('runtime_root','__pycache__','.pytest_cache','product')) or f.name in ('.runtime_marker','receipt_portability.json'):continue
 if f.suffix not in ('.json','.xml','.log','.md','.py'):continue
 before=f.read_bytes();s=before.decode();s=s.replace(str(RET),'RETURN_ROOT').replace(str(ROOT),'REPOSITORY_ROOT')
 if f.suffix=='.xml':s=re.sub(r'hostname="[^"]*"','hostname="LOCAL_HOST"',s)
 after=s.encode()
 if before!=after:f.write_bytes(after);changes.append(dict(path=str(f.relative_to(RET)),raw_sha256=hashlib.sha256(before).hexdigest(),portable_sha256=hashlib.sha256(after).hexdigest()))
p=RET/'receipt_portability.json';previous=json.loads(p.read_text())['changes'] if p.exists() else []
p.write_text(json.dumps(dict(schema='E04_PORTABLE_RECEIPT_TRANSFORM@1',policy='Root paths/hostname only, not test outcomes, timings, source hashes or oracles',changes=previous+changes),indent=2)+'\n');print('portable aliases',len(changes))
