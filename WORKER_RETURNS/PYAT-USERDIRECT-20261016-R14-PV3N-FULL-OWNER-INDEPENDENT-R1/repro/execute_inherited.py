"""Reviewer launches exact pinned executables in fresh interpreters, honest exits."""
from pathlib import Path
import sys,subprocess,json,xml.etree.ElementTree as ET,os,time
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';E=R/'evidence/inherited';E.mkdir(parents=True,exist_ok=True)
modes=['pv2_33','v2k_24','pv_21','owners_111','historical_cold','pv2i_historical','pv3_probe','cold','cold_receipt_attack','checkpoint_attack','audit_receipts','reconstruct','pv3','pv2i_adapter']
rows=[]
for mode in modes:
 print('EXECUTING',mode,flush=True);t=time.time()
 p=subprocess.run([sys.executable,str(C/'repro/run.py'),mode],capture_output=True,text=True,env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'))
 (E/(mode+'.launcher.stdout')).write_text(p.stdout+p.stderr)
 row=dict(mode=mode,command=['python3','runtime/court/repro/run.py',mode],exit=p.returncode,seconds=time.time()-t)
 j=C/'observations'/(mode+'.xml')
 if j.exists():
  root=ET.parse(j).getroot();row['counts']={k:sum(int(t.get(k,0)) for t in root.iter('testsuite')) for k in ['tests','failures','errors','skipped']}
  row['cases']=[dict(name=t.get('name'),status='FAIL' if t.find('failure') is not None else 'ERROR' if t.find('error') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS') for t in root.iter('testcase')]
 rows.append(row);(R/'inherited_results.json').write_text(json.dumps(rows,indent=2)+'\n');print(row['mode'],row['exit'],row.get('counts'),flush=True)
 # Expected raw REDs remain raw; continue all courts so one result never hides others.
