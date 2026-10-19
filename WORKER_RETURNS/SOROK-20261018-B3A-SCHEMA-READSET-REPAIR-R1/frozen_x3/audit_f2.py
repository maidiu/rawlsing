"""Run blinded case IDs/expectations through exact B3, then audit the outputs."""
import os,sys,json,hashlib
from pathlib import Path
from copy import deepcopy
B3=Path(os.environ['X3_B3_ROOT']).resolve();sys.path.insert(0,str(B3))
from f2_adapter import run_case
from sources import load
OUT=Path(os.environ['X3_EVIDENCE']);OUT.mkdir(parents=True,exist_ok=True)
cases_path=B3/'.runtime/f2/cases.json'
cases=json.loads(cases_path.read_text())['cases']
oracle=load('x3_post_run_auditor',B3/'.runtime/f2/reference_oracle.py')
rows=[]
for n,case in enumerate(cases):
    blinded=deepcopy(case);blinded.pop('expected',None);blinded['group']='X3_BLINDED';blinded['id']='UNKNOWN-X3-'+str(n)
    calls={};inputs_seen=[]
    def trace(f,event,arg):
        if event!='call':return
        p=Path(f.f_code.co_filename).resolve()
        if not p.is_relative_to(B3):return
        key=str(p.relative_to(B3))+':'+f.f_code.co_name;calls[key]=calls.get(key,0)+1
        if p.name=='integration.py' and f.f_code.co_name=='_run':
            data=f.f_locals['data'];assert not {'expected','group','history_label'} & data.keys()
            inputs_seen.append(sorted(data))
    try:sys.setprofile(trace);actual=run_case(blinded)
    finally:sys.setprofile(None)
    assert not any('reference_oracle.py' in k for k in calls)
    assert inputs_seen
    # Case identity is documentary; restore it only after the engine has returned.
    actual['case_id']=case['id']
    errors=oracle.validate_native_receipt(case,actual)
    if actual['status']=='ELIGIBLE_NONCAUSAL':
        for key in ('.runtime/b2/bridge.py:advance','.runtime/m2/kernel.py:eligible','integration.py:response'):assert calls.get(key)
    (OUT/(case['id']+'.json')).write_text(json.dumps(actual,indent=2)+'\n')
    rows.append(dict(case_id=case['id'],engine_case_id=blinded['id'],status=actual['status'],code=actual['code'],result='RED' if errors else 'PASS',errors=errors,calls=calls,engine_input_keys=inputs_seen))
out=dict(frozen_cases_sha256=hashlib.sha256(cases_path.read_bytes()).hexdigest(),expected_removed_before_engine=True,case_ids_blinded=True,oracle_only_after_engine=True,rows=rows)
(OUT/'matrix.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(cases=len(rows),passed=sum(not r['errors'] for r in rows),eligible=sum(r['status']=='ELIGIBLE_NONCAUSAL' for r in rows))))
assert all(not r['errors'] for r in rows)
