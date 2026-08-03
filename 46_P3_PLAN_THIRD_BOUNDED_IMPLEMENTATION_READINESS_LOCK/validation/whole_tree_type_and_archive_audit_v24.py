from __future__ import annotations
import ast, csv, io, json, py_compile, sys, zipfile, hashlib
from collections import Counter
from pathlib import Path
try:
    import yaml
except Exception:
    yaml=None
from docx import Document

root=Path(sys.argv[1]).resolve()
try:
    csv.field_size_limit(sys.maxsize)
except OverflowError:
    csv.field_size_limit(2**31-1)
errors=[]
counts=Counter()
RETURN_REL=Path('46_P3_PLAN_THIRD_BOUNDED_IMPLEMENTATION_READINESS_LOCK/validation/P3_WHOLE_TREE_TYPE_AND_ARCHIVE_AUDIT_RETURN_v4.json')
files=[p for p in root.rglob('*') if p.is_file() and p.relative_to(root)!=RETURN_REL]

def err(path, kind, exc):
    errors.append({'path':str(path.relative_to(root)) if isinstance(path,Path) and path.is_relative_to(root) else str(path),'kind':kind,'error':repr(exc)})

for p in files:
    ext=p.suffix.lower()
    counts[ext or '<none>'] += 1
    try:
        if ext=='.csv':
            with p.open('r',encoding='utf-8-sig',newline='') as f:
                list(csv.reader(f))
        elif ext=='.json':
            json.loads(p.read_text(encoding='utf-8-sig'))
        elif ext in {'.yaml','.yml'}:
            if yaml is None: raise RuntimeError('PyYAML unavailable')
            yaml.safe_load(p.read_text(encoding='utf-8-sig'))
        elif ext=='.py':
            ast.parse(p.read_text(encoding='utf-8-sig'), filename=str(p))
        elif ext=='.docx':
            Document(str(p))
        elif ext=='.zip':
            with zipfile.ZipFile(p) as z:
                bad=z.testzip()
                if bad: raise RuntimeError(f'bad member {bad}')
        elif ext in {'.md','.txt','.sql'}:
            p.read_text(encoding='utf-8-sig')
    except Exception as e:
        err(p,'type_parse',e)

# recursively test every ZIP instance, including nested ZIP payloads
archive_instances=0
unique_payloads=set()
max_depth=0

def audit_zip_bytes(data: bytes, label: str, depth: int):
    global archive_instances, max_depth
    archive_instances += 1
    max_depth=max(max_depth,depth)
    digest=hashlib.sha256(data).hexdigest()
    unique_payloads.add(digest)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            bad=z.testzip()
            if bad: raise RuntimeError(f'bad member {bad}')
            for info in z.infolist():
                if info.is_dir(): continue
                if info.filename.lower().endswith('.zip'):
                    audit_zip_bytes(z.read(info), label+'!'+info.filename, depth+1)
    except Exception as e:
        errors.append({'path':label,'kind':'recursive_zip','error':repr(e)})

for p in files:
    if p.suffix.lower()=='.zip':
        audit_zip_bytes(p.read_bytes(),str(p.relative_to(root)),1)

# no test/cache debris
cache=[str(p.relative_to(root)) for p in root.rglob('*') if p.name in {'__pycache__','.pytest_cache'} or p.suffix in {'.pyc','.pyo'}]
if cache:
    errors.append({'path':'<tree>','kind':'cache_debris','error':cache[:50]})

result={
 'status':'PASS' if not errors else 'FAIL',
 'root':str(root),
 'file_count_excluding_this_return':len(files),
 'type_counts':dict(sorted(counts.items())),
 'recursive_archive_instances':archive_instances,
 'unique_archive_payloads':len(unique_payloads),
 'max_archive_depth':max_depth,
 'cache_debris_count':len(cache),
 'errors':errors,
}
print(json.dumps(result,indent=2))
if errors: sys.exit(1)
