from pathlib import Path
import zipfile,io,csv,json,traceback
from collections import Counter
ROOT=Path('/mnt/data/rawlsing_audit/v10/Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731')
OUT=Path('/mnt/data/rawlsing_audit/independent_audit')
records=[]
seen_hashes=set()
import hashlib

def audit_zip_bytes(label,data,depth):
 h=hashlib.sha256(data).hexdigest()
 duplicate=h in seen_hashes
 seen_hashes.add(h)
 try:
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   bad=z.testzip(); infos=z.infolist()
   records.append({'archive':label,'depth':depth,'sha256':h,'duplicate_content':duplicate,'members':len(infos),'compressed_bytes':sum(i.compress_size for i in infos),'uncompressed_bytes':sum(i.file_size for i in infos),'status':'PASS' if bad is None else 'FAIL','bad_member':bad or ''})
   for info in infos:
    if not info.is_dir() and info.filename.lower().endswith('.zip'):
     child=z.read(info)
     audit_zip_bytes(label+'!/'+info.filename,child,depth+1)
 except Exception as e:
  records.append({'archive':label,'depth':depth,'sha256':h,'duplicate_content':duplicate,'members':'','compressed_bytes':'','uncompressed_bytes':'','status':'FAIL','bad_member':repr(e)})

for p in sorted(ROOT.rglob('*.zip')):
 audit_zip_bytes(str(p.relative_to(ROOT)),p.read_bytes(),0)
with (OUT/'recursive_zip_audit.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
summary={'archives_seen':len(records),'unique_zip_payloads':len(seen_hashes),'max_depth':max(int(r['depth']) for r in records),'passed':sum(r['status']=='PASS' for r in records),'failed':sum(r['status']=='FAIL' for r in records),'nested_archives':sum(int(r['depth'])>0 for r in records),'failures':[r for r in records if r['status']=='FAIL']}
(OUT/'recursive_zip_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
