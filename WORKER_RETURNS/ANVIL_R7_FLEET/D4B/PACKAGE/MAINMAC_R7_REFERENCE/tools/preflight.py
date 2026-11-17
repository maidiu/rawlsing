#!/usr/bin/env python3
"""R7 authored-package integrity/preflight. Synthetic tests only; never accredits science, reviewers or GitHub."""
import hashlib,json,pathlib,py_compile,subprocess,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1];errors=[]
req=['README.md','01_MISSION_DECISION_CONSTITUTION.md','02_EXECUTION_AND_ROLE_LAW.md',
 '03_SCIENTIFIC_BOUNDARIES_AND_NONLOSS.md','04_PHYSICS_COMPARE_AND_BUILD_HANDOFF.md',
 '05_OPERATING_SCHEMAS_AND_VERIFICATION.md','06_R5_R6_TO_R7_REPAIR_REPORT.md',
 'contracts/policy.json','contracts/source_registry.json','contracts/boundaries.json',
 'prompts/00_CONTROLLER.md','prompts/01_ARCHITECT_A.md','prompts/02_ARCHITECT_B.md',
 'prompts/03_INDEPENDENT_C.md','prompts/04_H1_OWNER.md',
 'reference/ANVIL_R5_IMMUTABLE.zip','reference/SOURCE_ARCHIVE_PIN.json',
 'tools/r7.py','tools/fixtures.py','tools/test_r7.py','tools/preflight.py','tools/package.py']
for f in req:
 if not (ROOT/f).is_file():errors.append('REQUIRED_FILE_MISSING:'+f)
try:
 policy=json.loads((ROOT/'contracts/policy.json').read_text());src=json.loads((ROOT/'contracts/source_registry.json').read_text());bound=json.loads((ROOT/'contracts/boundaries.json').read_text())
 if policy['schema']!='ANVIL_R7_POLICY_1':errors.append('BAD_R7_POLICY_SCHEMA')
 if src.get('snapshot_sha')!=policy.get('operating_cut'):errors.append('SOURCE_CUT_DRIFT')
 if [len(v) for v in src['mandatory'].values()] != [29,26,14,10,8,8,7,16]:errors.append('INHERITED_ID_SET_CHANGED')
 if len(set(sum(src['mandatory'].values(),[])))!=118:errors.append('INHERITED_DUPLICATE_IDS')
 if {x['id'] for x in bound['boundaries']}!={f'T{i}' for i in range(1,8)}:errors.append('BOUNDARY_DRIFT')
 if set(policy['stage_verdicts'])!={'H0','A0','B0','A1','B1','P15','P2','C','H1'}:errors.append('STAGE_VOCAB_DRIFT')
 from importlib.util import spec_from_file_location,module_from_spec
 spec=spec_from_file_location('r7',ROOT/'tools/r7.py');mod=module_from_spec(spec);spec.loader.exec_module(mod)
 if len(mod.required_floor('C11_QUERY_DESIGN'))!=22 or len(mod.required_floor('FF_FIRST_EFFECT_DESIGN'))!=23:errors.append('R7_PHYSICAL_FLOOR_DRIFT')
except Exception as exc:errors.append('INVALID_CONTROLLING_POLICY:'+repr(exc))
try:
 pin=json.loads((ROOT/'reference/SOURCE_ARCHIVE_PIN.json').read_text());archive=ROOT/'reference/ANVIL_R5_IMMUTABLE.zip'
 if hashlib.sha256(archive.read_bytes()).hexdigest()!=pin['sha256']:errors.append('R5_ARCHIVE_HASH_CHANGED')
 with zipfile.ZipFile(archive) as z:
  mf=json.loads(z.read('ANVIL_R5/MANIFEST.json'));payloads=mf['payloads']
  if len(z.namelist())!=45 or len(payloads)!=44:errors.append('R5_UNEXPECTED_PAYLOAD_COUNT')
  for path,details in payloads.items():
   b=z.read('ANVIL_R5/'+path)
   if hashlib.sha256(b).hexdigest()!=details['sha256'] or len(b)!=details['bytes']:errors.append('R5_CHANGED_OR_MISSING_PAYLOAD:'+path)
except Exception as exc:errors.append('R5_BASELINE_VERIFY_FAIL:'+repr(exc))
for f in (ROOT/'tools').glob('*.py'):
 try:py_compile.compile(str(f),doraise=True)
 except Exception as exc:errors.append('PY_COMPILE_FAIL:'+f.name+':'+repr(exc))
for f in (ROOT/'prompts').glob('*.md'):
 txt=f.read_text()
 for term in ['R7','SOURCE','RETURN','FIRST']:
  if term not in txt.upper():errors.append('INCOMPLETE_STANDALONE_LAUNCH:'+f.name+':'+term)
 if 'A_PROVED_AT_SCOPE' in txt or 'B_PROVED_AT_SCOPE' in txt:errors.append('SUPERSEDED_P15_ALIAS_IN_LAUNCH:'+f.name)
if not errors:
 q=subprocess.run([sys.executable,str(ROOT/'tools/test_r7.py'),'-q'],cwd=ROOT,capture_output=True,text=True)
 if q.returncode:errors.append('ADVERSARIAL_SUITE_RED:'+q.stdout[-600:]+q.stderr[-1200:])
 else:tested=q.stderr.split('Ran ')[-1].split(' tests')[0]
else:tested='not-run'
# Test the bundled on-disk fixtures, not just freshly generated fixtures in a temporary test.
# This catches stale content digests, receipt schemas, mismatched frozen heads and
# accidental package regressions that the isolated mutation tests cannot expose.
if not errors:
 fixture_commands=[
  ('check-plan',['check-plan','fixtures/SYNTHETIC_PLAN.json']),
  ('compare',['compare','fixtures/SYNTHETIC_PLAN.json','fixtures/SYNTHETIC_MEASUREMENTS.json','--evidence-root','fixtures']),
  ('check-spine',['check-spine','fixtures/SYNTHETIC_SPINE.json','fixtures/SYNTHETIC_PLAN.json','fixtures/SYNTHETIC_MEASUREMENTS.json','--evidence-root','fixtures']),
 ]
 for label,args in fixture_commands:
  q=subprocess.run([sys.executable,str(ROOT/'tools/r7.py'),*args],cwd=ROOT,capture_output=True,text=True)
  try: outcome=json.loads(q.stdout)
  except json.JSONDecodeError:outcome={}
  if q.returncode or outcome.get('status')!='PASS_STRUCTURAL_ONLY_NOT_AUTHENTICATED':
   errors.append('BUNDLED_FIXTURE_COMMAND_RED:'+label+':'+str(outcome.get('errors',[]))[:350])
print(json.dumps({'status':'RED' if errors else 'PASS_LOCAL_STRUCTURAL_AND_SYNTHETIC_ONLY','tests':tested,
 'r5_full_baseline_verified':'R5_ARCHIVE_HASH_CHANGED' not in errors and not any('R5_' in e for e in errors),
 'errors':errors},indent=2));sys.exit(2 if errors else 0)
