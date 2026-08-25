#!/usr/bin/env python3
from pathlib import Path
import csv,hashlib,json,sys,zipfile,pandas as pd,io
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
checks={}
rows=list(csv.DictReader((ROOT/'09_VALIDATION/PAYLOAD_SHA256_MANIFEST.csv').open()))
checks['manifest_nonempty']=len(rows)>30
checks['all_manifest_files_present']=all((ROOT/r['path']).is_file() for r in rows)
checks['all_manifest_hashes_match']=all(sha(ROOT/r['path'])==r['sha256'] and (ROOT/r['path']).stat().st_size==int(r['size_bytes']) for r in rows)
# worker exact set + counts
all_ids=[]; s2={'PRESERVE_SOURCE_TOPOLOGY':0,'REVISE_TOPOLOGY':0,'BLOCKED':0}; s2b={'ACCEPT_ENDPOINT':0,'REJECT_ENDPOINT':0,'BLOCKED':0}
for zp in sorted((ROOT/'06_WORKER_RETURNS').glob('W0*.zip')):
    with zipfile.ZipFile(zp) as z:
        checks[f'{zp.stem}_crc']=z.testzip() is None
        c=[n for n in z.namelist() if n.lower().endswith('.csv') and 'workbench' in n.lower() and ('complete' in n.lower() or 'completed' in n.lower())]
        if not c: checks[f'{zp.stem}_workbench']=False; continue
        df=pd.read_csv(io.BytesIO(z.read(c[0])),low_memory=False)
        all_ids += df.question_implementation_id.astype(str).tolist()
        for k,v in df.s2_topology_disposition.dropna().astype(str).value_counts().items(): s2[k]=s2.get(k,0)+int(v)
        for k,v in df.s2b_terminal_disposition.dropna().astype(str).value_counts().items(): s2b[k]=s2b.get(k,0)+int(v)
checks['six_worker_zips']=len(list((ROOT/'06_WORKER_RETURNS').glob('W0*.zip')))==6
checks['worker_union_6294']=len(all_ids)==6294
checks['worker_unique_6294']=len(set(all_ids))==6294
checks['s2_3667']=sum(s2.values())==3667
checks['s2_no_blocked']=s2.get('BLOCKED',0)==0
checks['s2_counts']=s2.get('PRESERVE_SOURCE_TOPOLOGY',0)==2914 and s2.get('REVISE_TOPOLOGY',0)==753
checks['s2b_2627']=sum(s2b.values())==2627
checks['s2b_counts']=s2b.get('ACCEPT_ENDPOINT',0)==2234 and s2b.get('REJECT_ENDPOINT',0)==335 and s2b.get('BLOCKED',0)==58
state=json.loads((ROOT/'00_START_HERE/CURRENT_STATE_20260810.json').read_text())
checks['job2_3324']=state['job2_semantic_units']['closed']==3324==state['job2_semantic_units']['denominator']
checks['job3_false']=state['job3_authority_created'] is False
checks['o03_o04_false']=state['r10e_p2']['central_o03_o04_integrated'] is False
checks['dependency_ledger_present']=(ROOT/'08_LIBRARY_DEPENDENCIES/LIBRARY_DEPENDENCY_LEDGER.csv').is_file()
status='PASS' if all(checks.values()) else 'FAIL'
out={'status':status,'checks':checks,'derived_s2':s2,'derived_s2b':s2b,'worker_union_rows':len(all_ids),'worker_unique_ids':len(set(all_ids))}
print(json.dumps(out,indent=2))
sys.exit(0 if status=='PASS' else 1)
