import pandas as pd, json, hashlib, zipfile, sys
from pathlib import Path
B=Path(__file__).resolve().parent
idx=pd.read_csv(B/'WORKER_PACK_INDEX.csv')
a=pd.read_csv(B/'SOURCE_WAVE_ASSIGNMENT.csv')
errs=[]
if len(a)!=35 or len(a[['source_family','wave']].drop_duplicates())!=35: errs.append('SOURCE_WAVE_PARTITION')
if len(idx)!=6: errs.append('PACK_COUNT')
for _,r in idx.iterrows():
 p=B/'PACKS'/r.pack_filename
 if not p.exists(): errs.append('MISSING '+r.pack_filename); continue
 if hashlib.sha256(p.read_bytes()).hexdigest()!=r.sha256: errs.append('SHA '+r.pack_filename)
 with zipfile.ZipFile(p) as z:
  names=z.namelist()
  req=[f"{r.worker_id}/00_README_FIRST.md",f"{r.worker_id}/CODE/validate_return.py",f"{r.worker_id}/TEMPLATES/SEMANTIC_ROLE_ASSIGNMENT.csv",f"{r.worker_id}/AUTHORITY/IMPLEMENTATION_SPINE.csv.gz"]
  for x in req:
   if x not in names: errs.append('ZIP_MISSING '+x)
qa=pd.read_csv(B/'PROGRAM_HOSTILE_QA.csv')
if not qa['pass'].all(): errs.append('HOSTILE_QA')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','errors':errs,'workers':len(idx),'source_waves':len(a)},indent=2))
sys.exit(1 if errs else 0)
