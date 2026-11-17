#!/usr/bin/env python3
"""Mechanical R5-to-R6 no-drop baseline check; never a substitute for semantic C review."""
import pathlib,hashlib,json,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'R5_BASELINE'
MAN=json.loads((BASE/'MANIFEST.json').read_text())
errors=[];notices=[]
expected=MAN['payloads']
for relative,metadata in expected.items():
    f=BASE/relative
    if not f.is_file():errors.append('R5_SOURCE_MISSING:'+relative);continue
    if hashlib.sha256(f.read_bytes()).hexdigest()!=metadata['sha256']:errors.append('R5_SOURCE_BYTES_CHANGED:'+relative)
    live=ROOT/relative
    if not live.is_file():errors.append('R6_ACTIVE_FUNCTION_MISSING:'+relative)
    elif hashlib.sha256(live.read_bytes()).hexdigest()!=metadata['sha256']:
        notices.append('R6_REVISED_WITH_R5_SOURCE_PRESERVED:'+relative)
if len(expected)!=44:errors.append('R5_MANIFEST_BASELINE_UNEXPECTED')
if len([x for x in BASE.rglob('*') if x.is_file()])!=len(expected)+1:errors.append('R5_BASELINE_FILE_COUNT_MISMATCH')
for file in ('20_R6_MATERIAL_DECISION_CONSTITUTION.json','21_R6_DECISION_AND_PROOF_LAW.md','22_R6_VALUE_AND_FUNCTION_CONSERVATION.md','tools/r6_comparator.py','tools/test_r6.py'):
    if not (ROOT/file).is_file():errors.append('R6_VALUE_REPAIR_MISSING:'+file)
# A valid conditional R6 spine conserves the exact complete inherited projection universe.
cmd=[sys.executable,str(ROOT/'tools/test_r6.py')]
res=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=30)
if res.returncode:errors.append('R6_REGRESSION_OR_POSITIVE_COMPARATOR_FAILED:'+res.stderr[-1000:])
summary={'status':'PASS_MECHANICAL_R5_BYTE_AND_FUNCTION_SURFACE_CONSERVATION' if not errors else 'RED','r5_payloads_verified':len(expected),'changed_active_files_with_original_unchanged':len(notices),'r6_extra_validation':'PASS' if res.returncode==0 else 'FAIL','errors':errors,'notes':notices,'important_limit':'Does not prove full semantic no-loss or external scientific/source/authenticated execution; independent C must assess all original commitments.'}
print(json.dumps(summary,indent=2))
raise SystemExit(0 if not errors else 2)
