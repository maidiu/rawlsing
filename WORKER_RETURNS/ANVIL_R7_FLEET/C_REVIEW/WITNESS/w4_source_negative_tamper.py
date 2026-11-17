#!/usr/bin/env python3
"""Independent C-review witness W4: source-negative/semantic tamper in the
source-authenticated inventory. Exact excerpt/origin hash, all IDs and counts are
preserved; only the authored source semantics and negative are replaced with a
false pairwise-marginal claim. The candidate gate should reject a false source
negative but passes it."""
import json, pathlib, shutil, sys, tempfile, hashlib

ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT = ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
COLD = sorted((ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/TEMP').glob('COLD_*'))[-1]
TOOLS = COLD/'ANVIL_R7/tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402

REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W4_SOURCE_NEGATIVE_TAMPER'
OUT.mkdir(parents=True, exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w4_',dir=str(OUT)))
ev=tmp/'EVIDENCE'; shutil.copytree(INT/'EVIDENCE',ev)
source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text())
decision=json.loads((ev/'DECISION.json').read_text())
inv=json.loads((ev/'SOURCE_IDENTITY_INVENTORY.json').read_text())

# Keep exact source_excerpt and origin_sha256; invert the negative and semantics.
changed=[]
for e in inv['entries']:
    if e['id']=='K1-CAP-11':
        e['source_semantics']='Pairwise marginal equality is a complete substitute for the true same-person three-way joint.'
        e['negative_meaning']='No F4 three-way reader is needed; pairwise marginals are sufficient and the odd/even distinction may be collapsed.'
        changed.append(e['id'])
    if e['id']=='K1-CAP-17':
        e['source_semantics']='The I07 guard is itself the F6 numeric interval and fully determines all bounds and uncovered mass.'
        e['negative_meaning']='No separate F6 numeric uncertainty computation is required; the guard supplies the numeric result.'
        changed.append(e['id'])

def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    (ev/name).write_bytes(b); return {'path':name,'sha256':sha(b)}
put('SOURCE_IDENTITY_INVENTORY.json',inv)
frame['source_inventory']={'path':'SOURCE_IDENTITY_INVENTORY.json','sha256':sha((ev/'SOURCE_IDENTITY_INVENTORY.json').read_bytes())}
put('FRAME.json',frame)
decision['common_frame']={'path':'FRAME.json','sha256':sha((ev/'FRAME.json').read_bytes())}
decision['frame_sha256']=digest(frame)
put('DECISION.json',decision)
fr=check('FRAME',frame,ev,source,REPO,ZIP)
de=check('DECISION',decision,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_WITNESS_W4','changed':changed,
        'mutations':['K1-CAP-11 source_semantics/negative_meaning replaced by pairwise-adequate false claim',
                     'K1-CAP-17 source_semantics/negative_meaning replaced by guard-equals-numeric false claim'],
        'excerpt_and_row_hash_unchanged':True,
        'FRAME':fr,'DECISION':de,
        'verdict':'WITNESS_CONFIRMED_IF_BOTH_PASS' if fr['status'].startswith('PASS') and de['status'].startswith('PASS') else 'WITNESS_REFUTED'}
(OUT/'w4_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
