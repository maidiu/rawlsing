#!/usr/bin/env python3
from __future__ import annotations
import csv,json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
PREMAIN=Path(__file__).resolve().parents[2]; GOV=PREMAIN/'GOVERNANCE_PROTOCOLS_R1'; FX=GOV/'fixtures_r2'; VAL=GOV/'tools'/'validate_governance_packet.py'; GEN=GOV/'tools'/'generate_r2_fixtures.py'
def run_one(r):
 p=FX/r['packet_path']; proc=subprocess.run([sys.executable,str(VAL),str(p)],text=True,capture_output=True,timeout=30)
 try: data=json.loads(proc.stdout.strip() or '{}')
 except Exception: data={'parse_error':proc.stdout,'stderr':proc.stderr}
 actual='PASS' if proc.returncode==0 and data.get('PACKET_VALID') is True else 'FAIL'
 return {'fixture_id':r['fixture_id'],'expected':r['expected'],'actual':actual,'match':actual==r['expected'],'attack_class':r['attack_class'],'packet_valid':data.get('PACKET_VALID'),'adoption_eligible':data.get('ADOPTION_ELIGIBLE'),'project_closure_eligible':data.get('PROJECT_CLOSURE_ELIGIBLE'),'false_checks':sorted([k for k,v in data.get('checks',{}).items() if v is False]),'stderr':proc.stderr.strip()}

def main():
 subprocess.run([sys.executable,str(GEN)],check=True,capture_output=True,text=True)
 rows=list(csv.DictReader((FX/'R2_FIXTURE_MANIFEST.tsv').open(encoding='utf-8'),delimiter='\t'))
 with ThreadPoolExecutor(max_workers=8) as ex: out=list(ex.map(run_one,rows))
 summary={'total':len(out),'expected_pass':sum(x['expected']=='PASS' for x in out),'actual_pass':sum(x['actual']=='PASS' for x in out),'expected_fail':sum(x['expected']=='FAIL' for x in out),'actual_fail':sum(x['actual']=='FAIL' for x in out),'mismatches':sum(not x['match'] for x in out),'cases':out}
 (FX/'R2_FIXTURE_RESULTS.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n',encoding='utf-8')
 with (FX/'R2_FIXTURE_MATRIX.tsv').open('w',encoding='utf-8',newline='') as f:
  w=csv.writer(f,delimiter='\t'); w.writerow(['fixture_id','expected','actual','match','attack_class','false_checks'])
  for x in out: w.writerow([x['fixture_id'],x['expected'],x['actual'],'YES' if x['match'] else 'NO',x['attack_class'],';'.join(x['false_checks'])])
 print(json.dumps({k:summary[k] for k in ['total','expected_pass','actual_pass','expected_fail','actual_fail','mismatches']},sort_keys=True))
 return 0 if summary['mismatches']==0 else 1
if __name__=='__main__': raise SystemExit(main())
