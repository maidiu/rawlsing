import hashlib, json
from pathlib import Path
R=Path(__file__).resolve().parent.parent
files=[]
for p in sorted(R.rglob("*")):
    if p.is_file() and "evidence/logs" not in p.as_posix() and p.name!="source_manifest.json":
        b=p.read_bytes(); files.append({"path":str(p.relative_to(R)),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
(R/"source_manifest.json").write_text(json.dumps({"schema":"B43_RETURN_SOURCE_MANIFEST@1.0.0","startup":"556dd7e2bf67e2bc0b1772d18880ef0dfaa819e3","files":files},indent=2)+"\n")
print("source manifest:",len(files))
