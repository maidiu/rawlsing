"""Redact host root/hostname from actual logs; record only raw/output digests."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parent
rows=[]
for p in sorted((R/'evidence').glob('*')):
    if p.suffix not in {'.log','.xml'}:continue
    raw=p.read_bytes();s=raw.decode()
    s=s.replace(str(R),'$RETURN')
    s=re.sub(r'/Users/[^/\s<]+(?:/[^\s<>"\']*)?', '$LOCAL_PATH',s)
    s=re.sub(r'hostname="[^"]*"','hostname="LOCAL_EXECUTOR"',s)
    new=s.encode()
    if new!=raw:
        p.write_bytes(new);rows.append(dict(path=str(p.relative_to(R)),raw_sha256=hashlib.sha256(raw).hexdigest(),sanitized_sha256=hashlib.sha256(new).hexdigest(),redactions='HOST_ROOT_AND_HOSTNAME_ONLY__TEST_COUNTS_AND_FAILURE_CONTENT_PRESERVED'))
p=R/'evidence/LOG_SANITIZATION.json'
old=json.loads(p.read_text()) if p.exists() else []
p.write_text(json.dumps(old+rows,indent=2)+'\n')
print(json.dumps(dict(redacted_files=len(rows))))
