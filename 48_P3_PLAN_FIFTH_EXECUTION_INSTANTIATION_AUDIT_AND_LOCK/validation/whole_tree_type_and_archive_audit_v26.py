from __future__ import annotations
from pathlib import Path
import sys,json,csv,zipfile,ast,hashlib,io,re
from collections import Counter
from docx import Document
import yaml
csv.field_size_limit(sys.maxsize)
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else None
errors=[];counts=Counter();archive_instances=0;unique_payloads=set()
for p in sorted(ROOT.rglob('*')):
    if not p.is_file():continue
    rel=str(p.relative_to(ROOT))
    if '__pycache__' in p.parts or p.suffix.lower()=='.pyc' or '.pytest_cache' in p.parts:
        errors.append({'file':rel,'error':'generated cache or bytecode debris'});continue
    ext=p.suffix.lower();counts[ext or '<none>']+=1
    try:
        if ext=='.json':json.loads(p.read_text(encoding='utf-8'))
        elif ext in {'.yaml','.yml'}:yaml.safe_load(p.read_text(encoding='utf-8'))
        elif ext=='.csv':
            with p.open(newline='',encoding='utf-8') as f:list(csv.reader(f))
        elif ext=='.py':ast.parse(p.read_text(encoding='utf-8'))
        elif ext=='.docx':Document(p)
        elif ext=='.zip':
            archive_instances+=1
            with zipfile.ZipFile(p) as z:
                bad=z.testzip()
                if bad:raise ValueError('bad ZIP member '+bad)
        elif ext in {'.md','.txt','.sql'}:p.read_text(encoding='utf-8')
    except Exception as e:errors.append({'file':rel,'error':repr(e)})
def walk(data:bytes,label:str):
    global archive_instances
    h=hashlib.sha256(data).hexdigest()
    if h in unique_payloads:return
    unique_payloads.add(h)
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            bad=z.testzip()
            if bad:errors.append({'file':label,'error':'bad member '+bad});return
            for n in z.namelist():
                if n.lower().endswith('.zip'):
                    archive_instances+=1;walk(z.read(n),label+'!'+n)
    except Exception as e:errors.append({'file':label,'error':repr(e)})
for p in sorted(ROOT.rglob('*.zip')):walk(p.read_bytes(),str(p.relative_to(ROOT)))
result={'status':'PASS' if not errors else 'FAIL','root':str(ROOT),'files':sum(counts.values()),'type_counts':dict(sorted(counts.items())),'recursive_archive_instances':archive_instances,'unique_archive_payloads':len(unique_payloads),'errors':errors}
text=json.dumps(result,indent=2)+'\n';print(text,end='')
if OUT:OUT.write_text(text,encoding='utf-8')
sys.exit(1 if errors else 0)
