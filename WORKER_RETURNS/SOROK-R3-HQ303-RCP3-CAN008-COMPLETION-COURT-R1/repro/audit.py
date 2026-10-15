"""Completion audit from actual sources, current evidence and Git custody."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,ast
RET=Path(__file__).resolve().parents[1]
assert hashlib.sha256((RET/'00_INHERITED_FROZEN_PREREG.json').read_bytes()).hexdigest()=='056ebe78a4240a6123abcf4f1b390d90d1cf31c077e9085ddf9d0904dc473700'
manifest=json.loads((RET/'source_manifest.json').read_text())
for row in manifest:
 p=RET/row['local'];b=p.read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob_sha1']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 assert subprocess.check_output(['git','rev-parse',row['commit']+':'+row['path']]).decode().strip()==row['blob_sha1']
 assert p.is_relative_to(RET/'runtime_root')
for row in json.loads((RET/'law_blob_manifest.json').read_text()):
 b=(RET/row['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob_sha1']
imports=0
for f in (RET/'repro/runs').glob('*/execution.json'):
 d=json.loads(f.read_text());assert d['guard_before_after']=='mappingproxy({}) unchanged'
 for row in d['imports']:
  b=(RET/row['file']).read_bytes();assert hashlib.sha256(b).hexdigest()==row['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob_sha1'];imports+=1
expected={'owners__closed':(220,0,0,0),'rsm__closed':(60,0,0,0),'candidate__closed':(37,0,0,0),'candidate_unset__closed':(37,0,0,1),'reviewer__final':(82,45,0,0)}
for n,w in expected.items():
 ss=list(ET.parse(RET/'repro/runs'/n/'junit.xml').getroot().iter('testsuite'))
 observed=tuple(sum(int(x.attrib.get(k,0)) for x in ss) for k in ('tests','failures','errors','skipped'));assert observed==w,(n,observed)
science=json.loads((RET/'01_CAN008_23_LAW_BINDINGS.json').read_text());assert len(science['rows'])==23
memory=json.loads((RET/'02_ADP016_ADP017_LAW_GATES.json').read_text());assert len(memory['adp016_formation_gates'])==7 and len(memory['adp016_failclosed'])==17
assert len(memory['adp017']['effect_fields'])==12
baseline=json.loads((RET/'repro/causal/baseline.json').read_text());physical=json.loads((RET/'repro/causal/physical_absent_effect.json').read_text())
assert baseline['result']['later_event_response']['effect_kind']=='DEFLECT'
assert physical['result']['later_event_response']['effect_kind']=='AMPLIFY'
assert not any(x['kind']=='CAN008_CURRENT_RESPONSE_EFFECT' and x['effective_causal_time']=='1998-10-03T16:00:00Z' for x in physical['ledger_entries'][0])
assert json.loads((RET/'repro/causal/summary.json').read_text())['exact_replay']
for f in [*RET.glob('*.py'),*RET.joinpath('repro').glob('*.py')]:ast.parse(f.read_text())
assert subprocess.check_output(['git','rev-parse','HEAD:rawlsing_next/v3_psepf_zero_positive_guard.py']).decode().strip()=='e0528d65215cb431196570c38bac4eae94217a1b'
result=dict(schema='RCP3_COMPLETION_AUDIT@1',disposition='REVIEW_REVISE',review_complete=True,scientific_acceptance=False,pinned_source_files_verified=len(manifest),observed_import_rows_verified=imports,inherited_prereg_unchanged=True,law_bindings=23,memory_formation_gates=7,actual_ADP016_failure_entries=17,epistemic_effect_fields=12,independently_reproduced_pinned_tests='220+60+37 PASS',independent_science='37 PASS/45 RED on82 predicates',actual_physical_absent_effect_executed=True,actual_replay=True,production_guard='mappingproxy({}), exact blob unchanged',only_ignored_candidate_copies=True,publication='Separate direct remote receipt required after push',real_model_trials=0,original_source_operations=0,real_V3_actors=0,semantic_issuers=0,adoption=False)
(RET/'completion_audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
