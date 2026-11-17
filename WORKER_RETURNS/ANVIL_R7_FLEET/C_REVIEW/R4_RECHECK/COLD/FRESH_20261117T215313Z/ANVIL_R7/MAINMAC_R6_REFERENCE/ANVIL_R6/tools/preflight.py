#!/usr/bin/env python3
"""Fail-close ANVIL R6 author package preflight. Format/static only; cannot authenticate external evidence."""
import hashlib,json,pathlib,py_compile,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];errors=[]
required=[
 'README.md','01_MISSION_DECISION_CONSTITUTION.md','02_EXECUTION_AND_ROLE_LAW.md',
 '03_SCIENTIFIC_BOUNDARIES_AND_NONLOSS.md','04_PHYSICS_COMPARE_AND_BUILD_HANDOFF.md',
 '05_OPERATING_SCHEMAS_AND_VERIFICATION.md','contracts/policy.json','contracts/source_registry.json','contracts/boundaries.json',
 'prompts/00_CODEX_CONTROLLER.md','prompts/01_ARCHITECT_A.md','prompts/02_ARCHITECT_B.md','prompts/03_INDEPENDENT_C.md',
 'prompts/04_H1_OWNER_RECEIVING.md','tools/r6.py','tools/test_r6.py','tools/package.py','tools/preflight.py']
for path in required:
  if not (ROOT/path).is_file():errors.append('REQUIRED_FILE_MISSING:'+path)
try:
 pol=json.loads((ROOT/'contracts/policy.json').read_text());src=json.loads((ROOT/'contracts/source_registry.json').read_text());bound=json.loads((ROOT/'contracts/boundaries.json').read_text())
 if pol['schema']!='ANVIL_R6_POLICY_1':errors.append('WRONG_POLICY_SCHEMA')
 expected=[29,26,14,10,8,8,7,16]
 if [len(v) for v in src['mandatory'].values()]!=expected:errors.append('INHERITED_ID_SET_DRIFT')
 if set(x['id'] for x in bound['boundaries'])!={f'T{i}' for i in range(1,8)}:errors.append('T_BOUNDARY_DRIFT')
 if src['snapshot_sha']!=pol['operating_cut']:errors.append('SOURCE_CUT_MISMATCH')
 if set(pol['stage_verdicts'])!={'H0','A0','B0','A1','B1','P15','P2','C','H1'}:errors.append('STAGE_SET_DRIFT')
except Exception as e:errors.append('INVALID_POLICY_OR_SOURCE:'+repr(e))
for path in sorted((ROOT/'tools').glob('*.py')):
  try:py_compile.compile(str(path),doraise=True)
  except Exception as e:errors.append('PYTHON_COMPILE_FAILED:'+path.name+':'+repr(e))
for path in sorted((ROOT/'prompts').glob('*.md')):
 t=path.read_text()
 for term in ['R6','SOURCE','RETURN']:
  if term not in t.upper():errors.append('INCOMPLETE_LAUNCH_'+term+':'+path.name)
 if 'A_PROVED_AT_SCOPE' in t:errors.append('INHERITED_P15_CONTRADICTORY_VERDICT:'+path.name)
if not errors:
 p=subprocess.run([sys.executable,str(ROOT/'tools/test_r6.py')],capture_output=True,text=True,cwd=ROOT)
 if p.returncode!=0:errors.append('ADVERSARIAL_TESTS_FAIL:'+p.stderr[-1600:])
 count=p.stderr.split('Ran ')[-1].split(' tests')[0] if 'Ran ' in p.stderr else 'unknown'
else:count=0
print(json.dumps({'preflight':'RED' if errors else 'PASS_LOCAL_CONTRACT_AND_ADVERSARIAL_ONLY','tests_run':count,'errors':errors,'file_count_ex_manifest':len([p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name!='MANIFEST.json'])},indent=2))
sys.exit(2 if errors else 0)
