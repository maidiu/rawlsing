"""Run the 42 frozen cases on B3; evaluate the reference instrument only afterwards."""
from pathlib import Path
import hashlib,json,sys,time,xml.etree.ElementTree as ET
from materialize import ROOT,RUNTIME,dump
from sources import load
from f2_adapter import run_case


def main():
 cases=json.loads((RUNTIME/'f2/cases.json').read_text())['cases'];out=ROOT/'evidence/f2';out.mkdir(parents=True,exist_ok=True)
 assert len(cases)==42 and hashlib.sha256((RUNTIME/'f2/cases.json').read_bytes()).hexdigest()=='827eada1eb73a131bfb1604f0977dcff08d173fb7eadb9a06d7894010f0e9351'
 oracle=load('b3_frozen_review_instrument',RUNTIME/'f2/reference_oracle.py');matrix=[];suite=ET.Element('testsuite',name='B3_ACTUAL_F2_42',tests='42',failures='0',errors='0',skipped='0')
 for case in cases:
  counts={};start=time.monotonic()
  def trace(frame,event,arg):
   if event=='call':
    file=Path(frame.f_code.co_filename)
    if file.is_relative_to(ROOT):
     key=str(file.relative_to(ROOT))+':'+frame.f_code.co_name
     counts[key]=counts.get(key,0)+1
  try:
   sys.setprofile(trace);actual=run_case(case)
  finally:sys.setprofile(None)
  # No reference function ran during simulation; caller expectations stay in auditor.
  assert not any('reference_oracle.py' in k for k in counts)
  errors=oracle.validate_native_receipt(case,actual)
  grade='NOT_APPLICABLE' if actual.get('status')=='NOT_APPLICABLE_TO_THIS_LAB' else 'RED' if errors else 'PASS'
  if actual.get('status')=='ELIGIBLE_NONCAUSAL':
   for required in ('.runtime/b2/bridge.py:advance','.runtime/m2/kernel.py:eligible','integration.py:response'):
    if not counts.get(required):errors.append('PHYSICAL_IMPORT_NOT_EXECUTED:'+required);grade='RED'
  dump(out/(case['id']+'.json'),actual)
  row=dict(case_id=case['id'],result=grade,actual_status=actual['status'],actual_code=actual['code'],errors=errors,
   receipt='evidence/f2/'+case['id']+'.json',actual_calls=counts,elapsed_seconds=time.monotonic()-start,
   scope='ACTUAL_COUPLING_AND_NONCAUSAL_OPTIONS' if actual['status']=='ELIGIBLE_NONCAUSAL' else 'ACTUAL_INTEGRATION_BOUNDARY',
   missing_owner=[] if grade!='NOT_APPLICABLE' else actual.get('missing_owner',['UNSPECIFIED']))
  matrix.append(row);node=ET.SubElement(suite,'testcase',name=case['id'],classname='B3.actual_f2',time=str(row['elapsed_seconds']))
  if grade=='RED':ET.SubElement(node,'failure',message=';'.join(errors))
  elif grade=='NOT_APPLICABLE':ET.SubElement(node,'skipped',message='NOT_APPLICABLE: '+','.join(row['missing_owner']))
 totals={k:sum(r['result']==k for r in matrix) for k in ('PASS','RED','NOT_APPLICABLE')}
 suite.set('failures',str(totals['RED']));suite.set('skipped',str(totals['NOT_APPLICABLE']))
 ET.ElementTree(suite).write(out/'junit.xml',encoding='utf-8',xml_declaration=True)
 dump(ROOT/'F2_CASE_MATRIX.json',dict(totals=totals,cases=matrix,grade='FROZEN_SOURCEFREE_EVIDENCE_INTERFACE_ONLY_NOT_PSYCHOLOGICAL_ACCEPTANCE',f1_native_red_preserved=17))
 print(json.dumps(totals,sort_keys=True));assert totals['RED']==0
if __name__=='__main__':main()
