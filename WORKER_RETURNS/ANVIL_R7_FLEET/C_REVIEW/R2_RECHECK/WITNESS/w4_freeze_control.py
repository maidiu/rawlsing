#!/usr/bin/env python3
"""R2 recheck W4 control: changing the authored inventory source_semantics or
negative_meaning while preserving exact excerpts/row hashes must be RED at the
semantic freeze. This verifies D7 closure, not a defect."""
import json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W4_FREEZE_CONTROL'; OUT.mkdir(parents=True,exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w4_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text()); decision=json.loads((ev/'DECISION.json').read_text()); inv=json.loads((ev/'SOURCE_IDENTITY_INVENTORY.json').read_text())
for e in inv['entries']:
 if e['id']=='K1-CAP-11': e['source_semantics']='Pairwise marginal equality is a complete substitute for the true three-way joint.'
 if e['id']=='K1-CAP-17': e['negative_meaning']='The I07 guard is the numeric F6 bound and determines all intervals.'
def put(n,o):
 b=(json.dumps(o,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (ev/n).write_bytes(b); return {'path':n,'sha256':sha(b)}
put('SOURCE_IDENTITY_INVENTORY.json',inv); frame['source_inventory']={'path':'SOURCE_IDENTITY_INVENTORY.json','sha256':sha((ev/'SOURCE_IDENTITY_INVENTORY.json').read_bytes())}; put('FRAME.json',frame); decision['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())}; decision['frame_sha256']=digest(frame); put('DECISION.json',decision)
fr=check('FRAME',frame,ev,source,REPO,ZIP); de=check('DECISION',decision,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_R2_W4_FREEZE_CONTROL','FRAME':fr,'DECISION':de,
 'verdict':'FREEZE_CONTROL_RED_AS_EXPECTED' if fr['status']=='RED' and any('SEMANTIC_SUMMARY_FREEZE' in x for x in fr['errors']) else 'FREEZE_NOT_ENFORCED'}
(OUT/'w4_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
