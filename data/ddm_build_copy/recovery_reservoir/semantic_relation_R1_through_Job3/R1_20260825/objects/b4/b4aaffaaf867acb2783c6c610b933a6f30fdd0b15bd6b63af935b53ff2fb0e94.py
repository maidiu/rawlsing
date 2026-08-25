import csv,json,sys,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]
errs=[]
rows=list(csv.DictReader(open(R/'PACKETS/ASSIGNED_PACKET_DENOMINATOR.csv'))); ret=list(csv.DictReader(open(R/'RETURN_TEMPLATE.csv'))); pin=json.load(open(R/'PARENT_AND_DENOMINATOR_PIN.json'))
if len(rows)!=pin['assigned_packet_count']: errs.append('assigned count mismatch')
ids=[x['canonical_packet_id'] for x in rows]
if len(ids)!=len(set(ids)): errs.append('duplicate packet id')
if [x['canonical_packet_id'] for x in ret]!=ids: errs.append('return template ids mismatch')
for pid in ids:
 p=R/'EVIDENCE'/pid
 for f in ['PACKET_GUIDE.md','parent_narrowing_rows.csv','current_implementation_rows.csv','exact_r14_source_objects.json']:
  if not (p/f).exists(): errs.append(f'missing {pid}/{f}')
if pin['frozen_parent_zip_sha256']!='394eda4f06b68503317c73a1d22c306b3c5d4b3a5de3cb784de54f36a5a1fa95': errs.append('parent sha mismatch')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','checks':5+4*len(ids),'errors':errs},indent=2))
sys.exit(1 if errs else 0)
