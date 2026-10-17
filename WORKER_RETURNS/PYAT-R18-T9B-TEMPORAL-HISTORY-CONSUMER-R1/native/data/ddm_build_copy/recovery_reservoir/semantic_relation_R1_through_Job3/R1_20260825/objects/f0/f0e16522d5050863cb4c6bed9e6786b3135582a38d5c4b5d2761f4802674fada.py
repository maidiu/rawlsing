#!/usr/bin/env python3
from pathlib import Path
import json,csv,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
errs=[]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
required=[
 '00_START_HERE/README_FIRST.md','00_START_HERE/NEW_CHAT_BOOTSTRAP_PROMPT.md','01_CURRENT_STATE/CURRENT_STATE_R5.json',
 '03_REPAIR_STACK/GOVERNING_25_ITEM_STACK_CURRENT_POSTURE_R5.md','04_NEXT_EXECUTION/NEXT_EXECUTION_RUNBOOK_R5.md',
 '05_APP_VIABILITY/APP_GATE_A_ATTITUDE_CLOUD_AND_INTERSTRATA_PRESSURE_PRESERVATION.md',
 '07_CURRENT_AUTHORITY/Rawlsing_R10K_O12_T15_Job3_Candidate_Denominator_Final_R3_20260812.zip',
 '08_ANCESTRY/Rawlsing_DDM_Full_Project_Orientation_Root_20260812_R4.zip',
 '09_VALIDATION/PAYLOAD_SHA256_MANIFEST.csv']
for x in required:
 if not (ROOT/x).exists(): errs.append('MISSING '+x)
state=json.load(open(ROOT/'01_CURRENT_STATE/CURRENT_STATE_R5.json'))
checks={
 'package_id':state.get('package_id')=='RAWLSING_DDM_FULL_PROJECT_ORIENTATION_ROOT_20260812_R5',
 'waves_35':state.get('canonical_active_waves')==35,
 'impl_18276':state.get('exact_implementations')==18276,
 'repair_done_16':state['repair_stack']['done_count']==16,
 'repair_next_25':state['repair_stack']['active_next']==25,
 't06_64':state['t06_t15_semantic_authority']['strict_t06_positive_relations']==64,
 't15_188':state['t06_t15_semantic_authority']['t15_positive_relations']==188,
 'o10_15_17':state['o10']['s14_rules']==15 and state['o10']['s15_je_definitions']==17,
 'o11_525':state['o11_s16']['rule_cells']==525,
 'o12_1264':state['o12']['novel_job3_candidates']==1264,
 'topology_1902':state['o12']['visible_governed_or_review_topology']==1902,
 'job3_not_started':'NOT_STARTED' in state['job3']['status'],
 'app_gate_pending':state['app_gate_a']['required'] and not state['app_gate_a']['passed'],
}
for k,v in checks.items():
 if not v: errs.append('STATE_CHECK '+k)
pins=json.load(open(ROOT/'01_CURRENT_STATE/LIBRARY_DEPENDENCY_PINS_R5.json'))
hash_expect={
 '08_ANCESTRY/Rawlsing_DDM_Full_Project_Orientation_Root_20260812_R4.zip':'5ddd6a14d1ff909667724cba52627809f706e3dce9c3fd343e79298a6c0944d7',
 '07_CURRENT_AUTHORITY/Rawlsing_SourceNative_Questionnaire_Structure_Authority_R1_20260812.zip':'e88cc035ca1d846e68ee208ec991f61f636d67ebbd19312057c8e44c37ff740d',
 '07_CURRENT_AUTHORITY/Rawlsing_R10K_S14_T15_Central_SourceFirst_Authority_Freeze_R1_20260812.zip':'1611fa96a1394c2006aa73ea848ec0b2846c4406cdaa1fbb5875dbe710b52f05',
 '07_CURRENT_AUTHORITY/Rawlsing_R10K_O10_S14_S15_Executable_Grammar_Successor_T15_20260812.zip':'4575eb80995ea08625209acfdc82a1d5cf5bc9960b8184331e2949db2f2e4b65',
 '07_CURRENT_AUTHORITY/Rawlsing_R10K_O11_S16_T15_35Wave_Capability_Successor_R2_20260812.zip':'e2ac16d5c1151de804dbb1df9ec5786a1864357b150fe53f666a7640625d6a19',
 '07_CURRENT_AUTHORITY/Rawlsing_R10K_O12_T15_Job3_Candidate_Denominator_Final_R3_20260812.zip':'33a56598f66f1e8d4596ddc4fec3ad686ec4cc7920ab76266b05470e1c7a3757'}
for rel,exp in hash_expect.items():
 p=ROOT/rel
 if not p.exists(): errs.append('HASH_MISSING '+rel)
 elif sha(p)!=exp: errs.append('HASH_MISMATCH '+rel)
# manifest
mp=ROOT/'09_VALIDATION/PAYLOAD_SHA256_MANIFEST.csv'
if mp.exists():
 for r in csv.DictReader(open(mp,newline='',encoding='utf-8')):
  p=ROOT/r['relative_path']
  if not p.exists(): errs.append('MANIFEST_MISSING '+r['relative_path'])
  elif sha(p)!=r['sha256']: errs.append('MANIFEST_HASH '+r['relative_path'])
print(json.dumps({'status':'PASS' if not errs else 'FAIL','errors':errs,'checks':checks,'manifest_rows':sum(1 for _ in csv.DictReader(open(mp))) if mp.exists() else 0},indent=2))
sys.exit(1 if errs else 0)
