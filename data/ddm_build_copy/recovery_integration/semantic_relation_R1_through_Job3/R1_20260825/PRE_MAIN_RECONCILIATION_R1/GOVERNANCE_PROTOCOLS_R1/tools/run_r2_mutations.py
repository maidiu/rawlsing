#!/usr/bin/env python3
from __future__ import annotations
import copy,json,subprocess,sys,tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
PREMAIN=Path(__file__).resolve().parents[2]; GOV=PREMAIN/'GOVERNANCE_PROTOCOLS_R1'; FX=GOV/'fixtures_r2'; VAL=GOV/'tools'/'validate_governance_packet.py'; GEN=GOV/'tools'/'generate_r2_fixtures.py'
def load(name): return json.loads((FX/'cases'/name).read_text())
def run(obj):
 with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as f: json.dump(obj,f); path=f.name
 try:
  p=subprocess.run([sys.executable,str(VAL),path],text=True,capture_output=True,timeout=30,env={**__import__('os').environ,'RAWLSING_SCHEMA_ENGINE':'internal_subset'})
  try: data=json.loads(p.stdout or '{}')
  except Exception: data={}
  return p.returncode==0 and data.get('PACKET_VALID') is True, sorted(k for k,v in data.get('checks',{}).items() if v is False)
 finally: Path(path).unlink(missing_ok=True)
def main():
 subprocess.run([sys.executable,str(GEN)],check=True,capture_output=True,text=True)
 base=load('F001_VALID_GROUNDED_GENERAL_DECISION.json'); touched=load('F035_VALID_BLOCKED_RETURN_REMAINS_VISIBLE.json')
 schemas={n:json.loads((GOV/n).read_text()) for n in ['GOVERNANCE_PACKET_SCHEMA_R2.json','GROUNDING_RECEIPT_SCHEMA.json','WORK_RETURN_SCHEMA.json','CENTRAL_STATE_UPDATE_SCHEMA.json']}
 muts=[]
 def add(name,obj): muts.append((name,obj))
 for k in schemas['GOVERNANCE_PACKET_SCHEMA_R2.json']['required']:
  x=copy.deepcopy(base); x.pop(k,None); add('REMOVE_PACKET_'+k,x)
 for k in schemas['GROUNDING_RECEIPT_SCHEMA.json']['required']:
  x=copy.deepcopy(base); x['grounding_receipt'].pop(k,None); add('REMOVE_GROUNDING_'+k,x)
 for k in schemas['WORK_RETURN_SCHEMA.json']['required']:
  x=copy.deepcopy(base); x['work_return'].pop(k,None); add('REMOVE_WORK_RETURN_'+k,x)
 for k in schemas['CENTRAL_STATE_UPDATE_SCHEMA.json']['required']:
  x=copy.deepcopy(base); x['central_state_update'].pop(k,None); add('REMOVE_CENTRAL_UPDATE_'+k,x)
 x=copy.deepcopy(base); x['grounding_receipt']['relevant_state_ids']=['N999']; add('UNKNOWN_STATE_ID',x)
 x=copy.deepcopy(base); x['grounding_receipt']['relevant_obligation_ids']=['OBL999']; add('UNKNOWN_OBLIGATION_ID',x)
 x=copy.deepcopy(base); x['grounding_receipt']['authority_ceiling']='RANDOM_AUTHORITY'; x['central_state_update']['authority_ceiling']='RANDOM_AUTHORITY'; add('RANDOM_AUTHORITY_CEILING',x)
 x=copy.deepcopy(base); x['grounding_receipt']['anti_resurrection_constraints']=['AR99']; add('RANDOM_AR_GATE',x)
 x=copy.deepcopy(base); x['grounding_receipt']['canonical_project_head']='0'*40; x['work_return']['canonical_launch_head']='0'*40; x['central_state_update']['canonical_project_head']='0'*40; add('SELF_CONSISTENT_STALE_CANONICAL_SHA',x)
 s=copy.deepcopy(base); s['requested_effect']='FORENSIC_RETURN'; s['work_return']['reintegration_status']='LOCAL_COMPLETE_UNRECONCILED'; s['central_state_update']['reintegration_status']='LOCAL_COMPLETE_UNRECONCILED'; s['work_return']['spawned_successors']=['A','B']; s['work_return']['return_to_ids']=['N022','N017']; s['central_state_update']['successor_return_paths']=[{'successor_id':'A','return_to':'N017'},{'successor_id':'B','return_to':'N017'}]
 valid,_=run(s)
 if not valid: raise SystemExit('successor mutation baseline invalid')
 x=copy.deepcopy(s); x['central_state_update']['successor_return_paths']=x['central_state_update']['successor_return_paths'][:1]; add('DROP_ONE_SUCCESSOR_RETURN_MAPPING',x)
 valid,_=run(touched)
 if not valid: raise SystemExit('touched mutation baseline invalid')
 x=copy.deepcopy(touched); x['central_state_update']['obligation_dispositions']=[]; add('DROP_ONE_TOUCHED_OBLIGATION_DISPOSITION',x)
 if len(muts)!=65: raise SystemExit(f'expected 65 mutations, got {len(muts)}')
 def one(item):
  name,obj=item; passed,false_checks=run(obj); return {'mutation':name,'expected':'FAIL','actual':'PASS' if passed else 'FAIL','match':not passed,'false_checks':false_checks}
 with ThreadPoolExecutor(max_workers=8) as ex: results=list(ex.map(one,muts))
 out={'total':len(results),'expected_fail':len(results),'actual_fail':sum(r['actual']=='FAIL' for r in results),'unexpected_pass':sum(r['actual']=='PASS' for r in results),'mismatches':sum(not r['match'] for r in results),'mutations':results}
 (FX/'MUTATION_TEST_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:out[k] for k in ['total','expected_fail','actual_fail','unexpected_pass','mismatches']},sort_keys=True))
 return 0 if out['unexpected_pass']==0 else 1
if __name__=='__main__': raise SystemExit(main())
