from pathlib import Path
import sys,json,csv,zipfile,ast
csv.field_size_limit(sys.maxsize)
from collections import Counter
from docx import Document
import yaml
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parents[2]
errs=[];counts=Counter();archives=0;unique=set()
for p in ROOT.rglob('*'):
 if not p.is_file():continue
 if '__pycache__' in p.parts or p.suffix.lower()=='.pyc': errs.append({'file':str(p.relative_to(ROOT)),'error':'generated cache or bytecode debris'}); continue
 ext=p.suffix.lower();counts[ext or '<none>']+=1
 try:
  if ext=='.json':json.loads(p.read_text())
  elif ext in {'.yaml','.yml'}:yaml.safe_load(p.read_text())
  elif ext=='.csv':list(csv.reader(p.open(newline='',encoding='utf-8')))
  elif ext=='.py':ast.parse(p.read_text())
  elif ext=='.docx':Document(p)
  elif ext=='.zip':
   archives+=1
   with zipfile.ZipFile(p) as z:
    bad=z.testzip()
    if bad:raise ValueError(bad)
 except Exception as e:errs.append({'file':str(p.relative_to(ROOT)),'error':repr(e)})
# recurse nested archives, deduplicated by bytes hash
import hashlib,io
def walk(data,label):
 global archives
 h=hashlib.sha256(data).hexdigest()
 if h in unique:return
 unique.add(h)
 try:
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   bad=z.testzip()
   if bad:errs.append({'file':label,'error':'bad member '+bad});return
   for n in z.namelist():
    if n.lower().endswith('.zip'):
     archives+=1;walk(z.read(n),label+'!'+n)
 except Exception as e:errs.append({'file':label,'error':repr(e)})
for p in ROOT.rglob('*.zip'):
 walk(p.read_bytes(),str(p.relative_to(ROOT)))
print(json.dumps({'status':'PASS' if not errs else 'FAIL','files':sum(counts.values()),'type_counts':dict(sorted(counts.items())),'recursive_archive_instances':archives,'unique_archive_payloads':len(unique),'errors':errs},indent=2))
sys.exit(1 if errs else 0)
