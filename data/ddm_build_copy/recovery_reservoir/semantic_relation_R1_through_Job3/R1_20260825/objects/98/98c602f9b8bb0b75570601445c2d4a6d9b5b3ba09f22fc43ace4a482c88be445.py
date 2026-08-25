#!/usr/bin/env python3
from pathlib import Path
import csv, hashlib, json, sys
root=Path(__file__).resolve().parents[1]
checks={}
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
required=[
 '00_START_HERE/README_FIRST.md','00_START_HERE/NEW_CHAT_BOOTSTRAP_PROMPT.md','00_START_HERE/PARENT_R1_PIN.json',
 '01_PROJECT_IDENTITY/FULL_PROJECT_EXPLAINER.md',
 '02_V5_LAYER_ARCHITECTURE/RAWLSING_V5_INTER_PRESSURING_PERSONHOOD_AND_ABSOLUTE_HORIZON_CURRENT_SYNTHESIS.md',
 '03_SURVEY_DDM_CONTROL/FIVE_JOB_TO_V5_CROSSWALK.md',
 '04_ANCESTRY_R7_R10/POST_R10E_SUCCESSORS/R10F_O03_O04_CENTRAL_INTEGRATION_REPORT.md',
 '04_ANCESTRY_R7_R10/POST_R10E_SUCCESSORS/R10G_O02_S08_REPORT.md',
 '04_ANCESTRY_R7_R10/POST_R10E_SUCCESSORS/CENTRAL_RECONCILIATION_REPORT.md',
 '04_ANCESTRY_R7_R10/POST_R10E_SUCCESSORS/CENTRAL_HOSTILE_EXTERNAL_VALIDATION.json',
 '05_CURRENT_STATE_R10H/CURRENT_STATE_R10H_AND_NEXT.json',
 '10_NEXT_EXECUTION/CURRENT_TRAJECTORY_R10H_TO_RUNTIME.md','10_NEXT_EXECUTION/O09_O10_EXECUTION_ECONOMICS_DECISION.md',
 '08_LIBRARY_DEPENDENCIES/LIBRARY_DEPENDENCY_LEDGER.csv','PACKAGE_INFO.json']
checks['required_files_present']=all((root/p).exists() for p in required)
parent=json.loads((root/'00_START_HERE/PARENT_R1_PIN.json').read_text())
checks['parent_r1_pin_exact']=parent.get('parent_sha256')=='a29eed46d7e40bfa3bcb568436928149bc8719a874fa9bb54f7d9c33554ca1ea'
state=json.loads((root/'05_CURRENT_STATE_R10H/CURRENT_STATE_R10H_AND_NEXT.json').read_text())
checks['state_18276']=state.get('exact_implementations')==18276 and state.get('o06_o07_o08',{}).get('rows_each')==18276
checks['r10h_hash_exact']=state.get('o06_o07_o08',{}).get('release_sha256')=='ffc824f5cf060ac71744913ac4a26a6e0a802fa0644d1d6cb04c92f5129fe8e5'
checks['job3_still_false']=state.get('job3_authority_created') is False
text=(root/'02_V5_LAYER_ARCHITECTURE/RAWLSING_V5_INTER_PRESSURING_PERSONHOOD_AND_ABSOLUTE_HORIZON_CURRENT_SYNTHESIS.md').read_text()
for key,phrase in {
 'has_inter_pressuring':'Inter-pressuring',
 'has_orientation_to_strata':'Orientation-to-strata',
 'has_absolute_horizon':'Absolute Horizon',
 'has_parent_child':'Parent → partner → child',
 'has_v556':'V556 — pressure-flow / vitality / attractor dynamics',
 'has_o09_bridge':'Why O09/P5 is the direct bridge',
 'has_antidrift':'Anti-drift / anti-getting-carried-away law'
}.items(): checks[key]=phrase in text
with open(root/'08_LIBRARY_DEPENDENCIES/LIBRARY_DEPENDENCY_LEDGER.csv',newline='') as f: deps={r['dep_id']:r for r in csv.DictReader(f)}
checks['new_dependency_ids']=all(x in deps for x in ['ORIENT_R1','R10F_CUM','R10G_CUM','R10H_U1_CENTRAL'])
checks['r10h_dependency_hash']=deps.get('R10H_U1_CENTRAL',{}).get('sha256')=='ffc824f5cf060ac71744913ac4a26a6e0a802fa0644d1d6cb04c92f5129fe8e5'
manifest=root/'09_VALIDATION/PAYLOAD_SHA256_MANIFEST.csv'
manifest_errors=[]
if manifest.exists():
 with open(manifest,newline='') as f:
  for r in csv.DictReader(f):
   p=root/r['path']
   if not p.exists() or sha(p)!=r['sha256']: manifest_errors.append(r['path'])
checks['payload_manifest_exact']=manifest.exists() and not manifest_errors
result={'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,'failed_checks':[k for k,v in checks.items() if not v],'manifest_errors':manifest_errors}
(root/'09_VALIDATION/VALIDATION_RESULT.json').write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
sys.exit(0 if result['status']=='PASS' else 1)
