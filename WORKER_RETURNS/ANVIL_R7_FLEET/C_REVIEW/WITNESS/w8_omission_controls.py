#!/usr/bin/env python3
"""Independent C-review control W8: omission of B-10, S-08 or L-08 must be RED.
This is a control, not a defect witness."""
import copy, json, pathlib, shutil, sys, tempfile

ROOT=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
COLD=sorted((ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP').glob('COLD_*'))[-1]
sys.path.insert(0,str(COLD/'ANVIL_R7/tools'))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
out=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W8_OMISSION_CONTROLS'; out.mkdir(parents=True,exist_ok=True)
base=pathlib.Path(tempfile.mkdtemp(prefix='w8_',dir=str(out))); ev=base/'EVIDENCE'; shutil.copytree(INT/'EVIDENCE',ev); source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text()); decision=json.loads((ev/'DECISION.json').read_text()); inv=json.loads((ev/'SOURCE_IDENTITY_INVENTORY.json').read_text())
results={}
for rid in ('B-10','S-08','L-08'):
    d=copy.deepcopy(decision)
    d['identity_dispositions']=[x for x in d['identity_dispositions'] if x['identity_id']!=rid]
    r=check('DECISION',d,ev,source,REPO,ZIP)
    results[rid]={'status':r['status'],'has_incomplete':any('INCOMPLETE_118' in e for e in r['errors']),'errors':r['errors'][:6]}
# one inventory omission with counts left unchanged
inv2=copy.deepcopy(inv); inv2['entries']=[x for x in inv2['entries'] if x['id']!='B-10']
def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/name).write_bytes(b); return {'path':name,'sha256':sha(b)}
put('SOURCE_IDENTITY_INVENTORY.json',inv2); frame['source_inventory']={'path':'SOURCE_IDENTITY_INVENTORY.json','sha256':sha((ev/'SOURCE_IDENTITY_INVENTORY.json').read_bytes())}; put('FRAME.json',frame)
fr=check('FRAME',frame,ev,source,REPO,ZIP)
results['inventory_missing_B-10']={'status':fr['status'],'errors':fr['errors'][:8]}
print(json.dumps(results,indent=2))
(out/'w8_result.json').write_text(json.dumps(results,indent=2)+'\n')
