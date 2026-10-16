"""Portable path-only redaction, raw local preservation, complete artifact digest."""
from stage import R,git
from pathlib import Path
import hashlib,json,shutil,xml.etree.ElementTree as ET
ROOT=R.parents[1]
rows=[]
for p in sorted(R.rglob('*')):
    if not p.is_file() or p.is_relative_to(R/'staging') or p.suffix not in ('.json','.xml','.log'):continue
    if p.name in ('11_EVIDENCE_PORTABILITY.json','artifact_manifest.json'):continue
    b=p.read_bytes();s=b.decode();changes=[]
    if str(ROOT) in s:s=s.replace(str(ROOT),'${MS4_WORKTREE}');changes.append('ABSOLUTE_WORKTREE_PREFIX_TO_NONIDENTIFYING_ALIAS')
    if p.suffix=='.xml':
        tree=ET.fromstring(s)
        for e in tree.iter('testsuite'):
            host=e.get('hostname')
            if host and host!='LOCAL_REVIEW_HOST':s=s.replace('hostname="'+host+'"','hostname="LOCAL_REVIEW_HOST"');changes.append('JUNIT_HOSTNAME_TO_NONIDENTIFYING_ALIAS')
        ET.fromstring(s)
    if not changes:continue
    rel=p.relative_to(R);raw=R/'staging/raw_evidence'/rel;raw.parent.mkdir(parents=True,exist_ok=True)
    if not raw.exists():raw.write_bytes(b)
    out=s.encode();p.write_bytes(out)
    rows.append(dict(path=str(rel),raw_local=str(raw.relative_to(R)),raw_sha256=hashlib.sha256(b).hexdigest(),portable_sha256=hashlib.sha256(out).hexdigest(),transformations=changes))
(R/'11_EVIDENCE_PORTABILITY.json').write_text(json.dumps(dict(schema='MS4_PATH_ONLY_PORTABILITY@1',full_stdout_and_junit_preserved_except_path_host_aliases=True,raw_local_preserved_not_committed=True,transforms=rows),indent=2)+'\n')
files=[p for p in sorted(R.rglob('*')) if p.is_file() and not p.is_relative_to(R/'staging') and p.name not in ('artifact_manifest.json','16_REMOTE_CONTENT_VERIFICATION.json') and '__pycache__' not in p.parts]
for p in files:
    assert str(ROOT).encode() not in p.read_bytes(),str(p.relative_to(R))
manifest=[dict(path=str(p.relative_to(R)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
(R/'artifact_manifest.json').write_text(json.dumps(dict(schema='MS4_ARTIFACT_MANIFEST@1',scope='Own return only; self and receipt-only16 excluded',files=manifest),indent=2)+'\n')
print('Portable full-evidence files',len(files),'path-only normalized',len(rows))
