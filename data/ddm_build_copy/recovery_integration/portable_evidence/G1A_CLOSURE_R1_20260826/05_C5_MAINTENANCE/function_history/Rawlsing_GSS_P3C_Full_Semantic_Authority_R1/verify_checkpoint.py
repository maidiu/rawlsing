from pathlib import Path
import csv,hashlib,sys
root=Path(__file__).resolve().parent
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
rows=list(csv.DictReader((root/'FILE_MANIFEST.csv').open()))
bad=[]
for r in rows:
 p=root/r['relative_path']
 if not p.exists() or not p.is_file() or p.stat().st_size!=int(r['size_bytes']) or sha(p)!=r['sha256']:
  bad.append(r['relative_path'])
print('PASS' if not bad else 'FAIL',len(rows),'files')
if bad:
 print('\n'.join(bad));sys.exit(1)
