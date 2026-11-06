"""Actual synthetic response mutation -> current R03/E41/C1/N10E -> restore."""
from pathlib import Path
import copy,hashlib,json,os,subprocess,sys
from probe_conditioned import ROWS
from rawlsing_next.tests.test_universal_source_projection import write_rows
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
source=OUT/'sourcefree-four-item.sav'
trace=OUT/'probe_first_reader.json'
original_source=source.read_bytes(); original_trace=trace.read_bytes()

def replay(label):
    result=subprocess.run([sys.executable,str(OUT/'probe_first_reader.py')],cwd=ROOT,
        env=dict(os.environ,PYTHONPATH=str(ROOT)),capture_output=True,text=True)
    (OUT/(label+'.log')).write_text(result.stdout+result.stderr)
    assert result.returncode==0,(label,result.stderr[-2000:])
    return json.loads(trace.read_text())

def joint_counts(data):
    return {tuple(cell['cell']):cell['raw_numerator_support']
            for cell in data[0]['consumer']['exact_lane']['geometry']['cells']}

baseline=json.loads(original_trace)
assert joint_counts(baseline)[('0','0','0')]==3
try:
    rows=copy.deepcopy(ROWS)
    rows[0]['route_choice']=1.0
    write_rows(source,rows)
    changed=replay('response-mutated')
    assert joint_counts(changed)[('0','0','0')]==2
    assert joint_counts(changed)[('0','0','1')]==1
    try: assert joint_counts(changed)==joint_counts(baseline)
    except AssertionError: expected_failure=True
    else: expected_failure=False
    assert expected_failure
    receipt={'scope':'SOURCEFREE_ONLY','actual_source_response_mutated':True,
       'original_source_sha256':hashlib.sha256(original_source).hexdigest(),
       'mutated_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
       'positive_numerical_assertion':'FAILED_AS_REQUIRED',
       'original_000_count':3,'mutated_000_count':2,'mutated_001_count':1}
finally:
    source.write_bytes(original_source)
restored=replay('response-restored')
assert trace.read_bytes()==original_trace
assert joint_counts(restored)==joint_counts(baseline)
receipt.update(restore='PASS',restored_trace_byte_identical=True,
               restored_trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest())
(OUT/'source-response-mutation-restore.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
