"""Portable path/host aliases only; source oracles and freeze remain untouched."""
from pathlib import Path
import re,json,hashlib
RET=Path(__file__).resolve().parents[1];ROOT=Path.cwd().resolve()
records=[]
for f in sorted(RET.rglob('*')):
 if not f.is_file() or any(x in f.relative_to(RET).parts for x in ('runtime_root','__pycache__','.pytest_cache','candidate','inherited','lineage')) or f.name in ('.runtime_marker','00_INHERITED_FROZEN_PREREG.json','receipt_portability.json'):continue
 if f.suffix not in ('.json','.log','.xml','.md','.py'):continue
 before=f.read_bytes()
 try:s=before.decode()
 except UnicodeDecodeError:continue
 s=s.replace(str(RET),'REPAIR_ROOT').replace(str(ROOT),'REPOSITORY_ROOT')
 if f.suffix=='.xml':s=re.sub(r'hostname="[^"]*"','hostname="LOCAL_HOST"',s)
 after=s.encode()
 if before!=after:
  f.write_bytes(after);records.append(dict(path=str(f.relative_to(RET)),raw_sha256=hashlib.sha256(before).hexdigest(),portable_sha256=hashlib.sha256(after).hexdigest()))
p=RET/'receipt_portability.json';old=json.loads(p.read_text())['changes'] if p.exists() else []
p.write_text(json.dumps(dict(schema='CAN2_RECEIPT_PORTABILITY@1',policy='Exact local root paths -> portable aliases; XML host -> LOCAL_HOST. Test outcomes/times, source hashes, oracles and freeze not altered',changes=old+records),indent=2)+'\n');print('portable receipt transformations',len(records))
