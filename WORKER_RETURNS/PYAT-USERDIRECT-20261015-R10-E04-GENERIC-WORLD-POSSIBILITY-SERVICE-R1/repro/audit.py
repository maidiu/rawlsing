"""Completion is unproven until current source and actual receipts agree."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,ast
from fractions import Fraction
RET=Path(__file__).resolve().parents[1];SOURCE_COMMIT='c2bc29af1128ff550b2ab61a876e1c97076e7b1f';PREFIX=str(RET.relative_to(Path.cwd()))+'/'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def load(n):return json.loads((RET/n).read_text())
for row in load('source_manifest.json'):
 b=(RET/row['local']).read_bytes();assert sha(b)==row['sha256'] and blob(b)==row['blob_sha1']
 assert subprocess.check_output(['git','rev-parse',row['commit']+':'+row['path']]).decode().strip()==row['blob_sha1']
for row in load('product_source_freeze.json')['sources']:
 b=(RET/row['path']).read_bytes();assert sha(b)==row['sha256'] and blob(b)==row['blob_sha1']
 assert subprocess.check_output(['git','rev-parse',SOURCE_COMMIT+':'+PREFIX+row['path']]).decode().strip()==row['blob_sha1']
primary={'tests_product_sanction_final':37,'tests_native_final':231};observed_imports=0
for name,count in primary.items():
 suites=list(ET.parse(RET/'outputs'/name/'junit.xml').getroot().iter('testsuite'))
 assert sum(int(x.get('tests',0)) for x in suites)==count
 assert all(sum(int(x.get(k,0)) for x in suites)==0 for k in ('failures','errors','skipped'))
 execution=load('outputs/'+name+'/execution.json');assert execution['exit_code']==0
 for row in execution['imports']:
  b=(RET/row['file']).read_bytes();assert sha(b)==row['sha256'] and blob(b)==row['blob_sha1'];observed_imports+=1
packet=load('03_TWO_GENERIC_CONSUMERS_AND_INDEPENDENT_INTERVENTIONS.json');summary=load('outputs/experiment_summary.json')
assert sha((RET/'03_TWO_GENERIC_CONSUMERS_AND_INDEPENDENT_INTERVENTIONS.json').read_bytes())==summary['packet_sha256']
w=lambda r:r['nonparent']['material'];sc=lambda r:r['conception_proposals']['material']['scenarios']
a=packet['baseline'];b=packet['empirical_source_cell_intervention'];c=packet['structural_access_exit_intervention'];s=packet['structural_sanction_only_intervention']
assert [x['denominator'] for x in w(a)['empirical']['steps']]==[32,16,8]
for result,expected in [(a,[18,10,6]),(b,[19,11,7])]:
 steps=w(result)['empirical']['steps'];assert len({json.dumps(x['release_ref'],sort_keys=True) for x in steps})==1
 assert len({json.dumps(x['risk_set_ref'],sort_keys=True) for x in steps})==1
 assert [x['binding_order'] for x in steps]==[['a'],['a','b'],['a','b','c']]
 for step,n1 in zip(steps,expected):
  cells={x['cell']:x for x in step['cells']};assert cells['1']['raw_numerator_support']==n1
  assert sum(v['raw_numerator_support'] for v in cells.values())==step['denominator'] and min(v['raw_numerator_support'] for v in cells.values())>0
  for cell in cells.values():
   fraction=Fraction(cell['raw_numerator_support'],step['denominator']);assert cell['raw_probability_exact_fraction']['$exact_fraction']==[fraction.numerator,fraction.denominator]
  assert step['uncertainty']=='UNCERTAINTY_UNQUANTIFIED' and step['authority_refs'] and step['provenance_refs'] and step['model_rule_hash']
assert w(a)['structural_routes']==w(b)['structural_routes']
assert [x['source_balance_count'] for x in w(a)['source_balance_reads']]==[4,4,4]
assert [x['source_balance_count'] for x in w(b)['source_balance_reads']]==[6,6,6]
assert w(a)['empirical']==w(c)['empirical']==w(s)['empirical']
assert w(c)['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE' and w(c)['structural_routes']['exit_constraint']['state']=='RESOURCE_CONSTRAINED'
assert w(a)['structural_routes']['civil']==w(c)['structural_routes']['civil']
assert w(s)['structural_routes']['civil']['state']=='BLOCKED_BY_MODELED_RULE' and w(s)['structural_routes']['training']==w(a)['structural_routes']['training']
assert sc(c)[0]['feasibility']=='INFEASIBLE_MODELED_PREMISE' and sc(s)[1]['feasibility']=='INFEASIBLE_MODELED_PREMISE'
assert packet['null_control']==a
assert w(packet['irrelevant_field_control'])['structural_routes']==w(a)['structural_routes'] and w(packet['irrelevant_field_control'])['empirical']==w(a)['empirical']
reverse=packet['legal_reverse']['steps'][0];assert reverse['denominator']==29 and next(x['raw_numerator_support'] for x in reverse['cells'] if x['cell']=='1')==18
assert reverse['target_ref']!=w(a)['empirical']['steps'][0]['target_ref']
assert packet['same_marginal_different_conditional']['steps'][0]['denominator']==29
loss=packet['measured_support_loss']['steps'];assert [x['denominator'] for x in loss]==[24,8,0] and loss[-1]['state']=='ZERO_SUPPORT' and loss[-1]['geometry'] is None
assert packet['after_structural_revoke']['material']['structural_routes']['training']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
assert packet['after_empirical_revoke']['material']['empirical']['state']=='REVOKED'
assert packet['after_empirical_revoke']['material']['structural_routes']['civil']==w(a)['structural_routes']['civil']
assert packet['historical_receipt_retained']['material']==a['nonparent']['material'] and packet['historical_receipt_retained']['fresh_use_authorized'] is False
clocks=packet['publication_clock_selections'];assert clocks['HISTORICAL']['fields']['training_access']['value'] is True and clocks['AS_OF']['fields']['training_access']['value'] is True and clocks['TEST_CURRENT']['fields']['training_access']['value'] is False
assert len(packet['native_owner_trace'])==summary['actual_native_calls']==408
assert len({r['function'] for r in packet['native_owner_trace']})==8
for row in packet['native_owner_trace']:assert (RET/row['file']).exists() and row['module'].startswith('rawlsing_next.')
assert any(r['input_evidence_refs'] and r.get('consumed_evidence_ref') for r in packet['native_owner_trace'] if r['function']=='evaluate_positioned_subject_possibility')
assert summary['OC05_actual_installation']['current_applicability']=='NOT_YET_APPLICABLE' and summary['OC05_actual_installation']['consumer_seam'] is None
for pair in (a,b,c,s):
 for output in pair.values():
  m=output['material'];assert m['grade']=='TEST_ONLY_SOURCEFREE_CANDIDATE' and not m['new_issuer'] and not m['operative_N9'] and not m['operative_N10W'] and m['model_calls']==m['actor_executions']==0
for name in ('00_RETURN.md','01_COHERENT_WORLD_SNAPSHOT_AND_CLOCKS.json','02_REAL_N10E_C1_F8_AND_N9_BOUNDARY_TRACE.md','03_TWO_GENERIC_CONSUMERS_AND_INDEPENDENT_INTERVENTIONS.json','04_PRODUCTIVE_ADEQUACY_AND_ISSUER_CEILING.md','environment_passport_delta.json'):assert (RET/name).is_file()
for f in [*RET.joinpath('product').glob('*.py'),*RET.joinpath('repro').glob('*.py')]:ast.parse(f.read_text())
paths=subprocess.check_output(['git','diff','--name-only','47c7d3e77413e8fe3c83cbf70b371597cfb96e38','HEAD']).decode().splitlines();assert all(x.startswith(PREFIX) for x in paths)
result=dict(schema='E04_REQUIREMENT_COMPLETION_AUDIT@1',author_goal_complete=True,independent_acceptance=False,claim_grade='PRODUCTIVE_TEST_ONLY_SOURCEFREE_CANDIDATE',source_commit=SOURCE_COMMIT,native_preimage_objects=51,primary_tests='37+231=268 PASS; no failures/errors/skips',verified_actual_import_rows=observed_imports,actual_native_profile_calls=408,clock_correction_explicit=True,generic_forward_reverse_multi_condition=True,two_separate_consumers=True,actual_values_read=True,numeric_structural_sanction_and_null_interventions=True,minority_and_measured_support_loss=True,selective_permission_invalidation_and_history_retention=True,OC05='NOT_YET_APPLICABLE; seam None',operative_N9_N10W='NOT_CLAIMED; new candidate boundary only',original_respondent_imports=0,external_model_calls=0,parent_actor_generation=0,new_issuers=0,canonical_adoption=False,changed_terrain='ONLY assigned return',remaining_publication='Final push/direct remote readback recorded separately')
(RET/'completion_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
