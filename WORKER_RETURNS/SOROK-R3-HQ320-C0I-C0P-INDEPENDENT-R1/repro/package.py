"""Portable path-only normalization; preserve raw outputs locally; hash all artifacts."""
from stage import R,ROOT
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E
rows=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.is_relative_to(R/'staging') or p.suffix not in ('.json','.xml','.log'):continue
 if p.name in ('11_EVIDENCE_PORTABILITY.json','artifact_manifest.json'):continue
 raw=p.read_bytes();s=raw.decode();trans=[]
 if str(ROOT) in s:s=s.replace(str(ROOT),'${C0I_WORKTREE}');trans.append('ABSOLUTE_WORKTREE_PREFIX_TO_NONIDENTIFYING_ALIAS')
 if p.suffix=='.xml':
  for item in E.fromstring(s).iter('testsuite'):
   host=item.get('hostname')
   if host and host!='LOCAL_C0I_HOST':s=s.replace('hostname="'+host+'"','hostname="LOCAL_C0I_HOST"');trans.append('JUNIT_HOSTNAME_TO_NONIDENTIFYING_ALIAS')
  E.fromstring(s)
 if trans:
  rel=p.relative_to(R);d=R/'staging/raw_evidence'/rel;d.parent.mkdir(parents=True,exist_ok=True)
  if not d.exists():d.write_bytes(raw)
  result=s.encode();p.write_bytes(result);rows.append(dict(path=str(rel),raw_local=str(d.relative_to(R)),raw_sha256=hashlib.sha256(raw).hexdigest(),portable_sha256=hashlib.sha256(result).hexdigest(),transformations=trans))
(R/'11_EVIDENCE_PORTABILITY.json').write_text(json.dumps(dict(schema='C0I_PATH_ONLY_PORTABILITY@1',full_stdout_junit_preserved_except_path_host_aliases=True,raw_local_preserved_not_committed=True,files=rows),indent=2)+'\n')
files=[p for p in sorted(R.rglob('*')) if p.is_file() and not p.is_relative_to(R/'staging') and '__pycache__' not in p.parts and p.name not in ('artifact_manifest.json','16_REMOTE_CONTENT_VERIFICATION.json')]
manifest=[]
for p in files:
 b=p.read_bytes();assert str(ROOT).encode() not in b,str(p.relative_to(R));manifest.append(dict(path=str(p.relative_to(R)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(R/'artifact_manifest.json').write_text(json.dumps(dict(schema='C0I_ARTIFACT_MANIFEST@1',scope='Owned return only; manifest and receipt-only16 excluded',files=manifest),indent=2)+'\n')
print('PACKAGED',len(files),'files; path-only normalizations',len(rows))
