#!/usr/bin/env python3
from pathlib import Path
import hashlib,csv,json,sys,zipfile
R=Path(__file__).resolve().parents[1]
errs=[]; checks=[]
def ck(n,c,d=''):
    checks.append({'check':n,'pass':bool(c),'detail':str(d)})
    if not c: errs.append(n)
req=['00_START_HERE/README_FIRST.md','01_CURRENT_STATE/CURRENT_STATE_R4.json','02_FORWARD_ITINERARY/FORWARD_WORK_ITINERARY_R4.md','03_APP_VIABILITY/APP_GATE_A_ATTITUDE_CLOUD_AND_INTERSTRATA_PRESSURE_PRESERVATION.md','04_S14_T06_CORRECTNESS/T06_GATE_CORRECTNESS_RECALL_AND_NONARBITRARY_PRUNING.md','05_R15_QUARANTINE/R15_RETURN_ADMISSIBILITY_AUDIT_REPORT.md','06_C4_PROGRAM/C4_R4_DISPATCH_POSTURE.md','08_ARCHITECTURE_REFERENCE/R_T_C_V550_ROSETTA.md','09_ANCESTRY/Rawlsing_DDM_Full_Project_Orientation_Root_20260811_R3.zip']
for x in req: ck('required:'+x,(R/x).exists())
st=json.loads((R/'01_CURRENT_STATE/CURRENT_STATE_R4.json').read_text())
ck('35_waves',st.get('canonical_active_waves')==35,st.get('canonical_active_waves'))
ck('18276_impl',st.get('exact_implementations')==18276,st.get('exact_implementations'))
ck('repair_9_25',st.get('repair_stack',{}).get('done_count')==9,st.get('repair_stack'))
ck('item18_active',st.get('repair_stack',{}).get('active_item')==18,st.get('repair_stack'))
ck('r15_quarantine',str(st.get('r15',{}).get('status','')).startswith('QUARANTINE'),st.get('r15'))
ck('c4_hold',st.get('c4',{}).get('r4_posture')=='HOLD_FULL_DISPATCH_OR_PROMOTION_PENDING_T06_GATE',st.get('c4'))
ck('t06_2of2_gate',st.get('t06_gate',{}).get('known_r6_positive_canaries')==2,st.get('t06_gate'))
ck('app_gate_required',st.get('app_gate_a',{}).get('required') is True,st.get('app_gate_a'))
ck('job3_false',st.get('job3_authorized') is False,st.get('job3_authorized'))
ck('s14_false',st.get('s14_frozen') is False,st.get('s14_frozen'))
p=R/'09_ANCESTRY/Rawlsing_DDM_Full_Project_Orientation_Root_20260811_R3.zip'
h=hashlib.sha256(p.read_bytes()).hexdigest()
ck('parent_r3_sha',h=='ab76c767078df14f06253814c76a9b171553de47003cf051754e351e6c01df07',h)
# payload manifest
man=R/'99_VALIDATION/PAYLOAD_SHA256_MANIFEST.csv'
if man.exists():
    rows=list(csv.DictReader(man.open()))
    for row in rows:
        q=R/row['path']; ck('manifest_exists:'+row['path'],q.exists())
        if q.exists(): ck('manifest_sha:'+row['path'],hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256'])
out={'status':'PASS' if not errs else 'FAIL','checks':len(checks),'errors':errs,'details':checks}
(R/'99_VALIDATION/VALIDATION_RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'checks':len(checks),'errors':len(errs)},indent=2))
sys.exit(1 if errs else 0)
