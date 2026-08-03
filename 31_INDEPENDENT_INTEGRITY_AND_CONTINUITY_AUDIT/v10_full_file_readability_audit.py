from pathlib import Path
import csv,sys,json,zipfile,hashlib,py_compile,traceback
from collections import Counter
from docx import Document
try:
 import yaml
except Exception:
 yaml=None
csv.field_size_limit(sys.maxsize)
ROOT=Path('/mnt/data/rawlsing_audit/v10/Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731')
OUT=Path('/mnt/data/rawlsing_audit/independent_audit')
rows=[]
for p in sorted(x for x in ROOT.rglob('*') if x.is_file()):
 rel=str(p.relative_to(ROOT)); ext=p.suffix.lower(); status='PASS'; detail={}; size=p.stat().st_size
 try:
  if size==0: raise ValueError('empty file')
  if ext=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:
    r=csv.reader(f); header=next(r); n=0; badlen=0; minlen=10**9; maxlen=0
    for row in r:
     n+=1; L=len(row); minlen=min(minlen,L); maxlen=max(maxlen,L)
     if L!=len(header): badlen+=1
   detail={'rows':n,'columns':len(header),'bad_row_lengths':badlen,'header':header}
   if badlen: status='FAIL'
  elif ext=='.json':
   with p.open(encoding='utf-8') as f: obj=json.load(f)
   detail={'type':type(obj).__name__,'length':len(obj) if hasattr(obj,'__len__') else None}
  elif ext in ('.yaml','.yml'):
   if yaml is None: raise RuntimeError('PyYAML unavailable')
   with p.open(encoding='utf-8') as f: obj=yaml.safe_load(f)
   detail={'type':type(obj).__name__,'length':len(obj) if hasattr(obj,'__len__') else None}
  elif ext=='.py':
   py_compile.compile(str(p),doraise=True); detail={'compiled':True,'lines':sum(1 for _ in p.open(encoding='utf-8'))}
  elif ext in ('.md','.txt'):
   t=p.read_text(encoding='utf-8'); detail={'chars':len(t),'lines':t.count('\n')+1}
  elif ext=='.docx':
   d=Document(p); detail={'paragraphs':len(d.paragraphs),'tables':len(d.tables),'table_rows':sum(len(t.rows) for t in d.tables)}
  elif ext=='.zip':
   with zipfile.ZipFile(p) as z:
    bad=z.testzip(); infos=z.infolist(); detail={'members':len(infos),'uncompressed_bytes':sum(i.file_size for i in infos),'bad_member':bad}
    if bad is not None: status='FAIL'
  else:
   with p.open('rb') as f: f.read(1024)
   detail={'readable':True}
 except Exception as e:
  status='FAIL'; detail={'error':repr(e),'trace':traceback.format_exc(limit=2)}
 rows.append({'relative_path':rel,'extension':ext,'bytes':size,'status':status,'detail':json.dumps(detail,ensure_ascii=False)})

with (OUT/'full_file_readability_audit.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'root':str(ROOT),'files':len(rows),'passed':sum(r['status']=='PASS' for r in rows),'failed':sum(r['status']=='FAIL' for r in rows),'by_extension':Counter(r['extension'] for r in rows),'failures':[r for r in rows if r['status']=='FAIL']}
summary['by_extension']=dict(summary['by_extension'])
(OUT/'full_file_readability_audit_summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(summary,indent=2,ensure_ascii=False))
