#!/usr/bin/env python3
from pathlib import Path
import hashlib,csv,json,sys
root=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()
errors=[]; checks=0
manifest=root/'99_R3_VALIDATION'/'PAYLOAD_SHA256_MANIFEST.csv'
with open(manifest,newline='') as f:
 for r in csv.DictReader(f):
  p=root/r['relative_path']; checks+=1
  if not p.exists(): errors.append('missing:'+r['relative_path']); continue
  checks+=1
  if sha(p)!=r['sha256']: errors.append('sha:'+r['relative_path'])
# hard pins
pins=[
 ('98_ANCESTRY_PACKAGES/R2/Rawlsing_DDM_Full_Project_Orientation_Root_20260810_R2.zip','4fcb2fcfc6218c8ba5867d565c88b3794ebd38f5b29e6700eadbf0f274820216'),
 ('11_20260811_SUCCESSOR/EMBEDDED_AUTHORITY/Rawlsing_R10K_O10_Input_Contract_Coverage_Audit_R1_20260811.zip','c2c0d2d087d4fa4759545240f2c7e36f909937622fb02af4b939918f58cfdd87'),
 ('11_20260811_SUCCESSOR/CHECKPOINT/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R1_20260811.zip','c9a80eef807fff4edaa66051b40e0c2bf82f230741a96147cc8d861335d632cd')]
for rel,expected in pins:
 checks+=1
 p=root/rel
 if not p.exists() or sha(p)!=expected: errors.append('pin:'+rel)
# semantic state assertions
state=json.loads((root/'00_START_HERE'/'CURRENT_STATE_20260811_R3.json').read_text())
asserts=[state['exact_implementations']==18276,state['job2_semantic_meaning']['closed']==3324,state['o12_r2']['rows']==811,state['o12_r2']['job3_launch_authorized'] is False,state['active_execution']=='R10K_PRE_JOB3_S14_RELATION_ROLE_BRIDGE_REPAIR']
for i,a in enumerate(asserts):
 checks+=1
 if not a: errors.append('state_assert:'+str(i))
print(json.dumps({'status':'PASS' if not errors else 'FAIL','checks':checks,'errors':errors},indent=2))
sys.exit(1 if errors else 0)
