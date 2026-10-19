"""Requirement-level evidence audit. Verdict REDs are required preserved evidence."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,re
ROOT=Path(__file__).resolve().parent;E=ROOT/'evidence';SEAL='87325cc7914dbbd77499f33190111589d5ed6d7c';BRANCH='agent/reviewer-sorok-20261018-b3a-atomic-repair-independent-i2-r1'
def sha(data):return hashlib.sha256(data).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def main():
 assert git('branch','--show-current').decode().strip()==BRANCH
 assert git('merge-base','--is-ancestor',SEAL,'HEAD')==b''
 audit=[]
 def checked(name,evidence):audit.append(dict(requirement=name,status='PROVEN',evidence=evidence))
 for row in read('evidence/input_transport_manifest.json'):
  data=(ROOT/row['local']).read_bytes();assert sha(data)==row['sha256'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
 assert len(read('evidence/input_transport_manifest.json'))==509
 assert read('evidence/source_verification.json')['verified_source_count']==228
 assert len(read('evidence/loaded_modules.json'))==11
 checked('Exact startup, input Git/archive/source/import identity','custody_receipt.json; input_transport_manifest.json; source_verification.json; loaded_modules.json')
 suites=read('evidence/suite_results.json')
 expected={'frozen_b3.xml':(71,0),'candidate_b3.xml':(71,0),'original_x3.xml':(28,8),'candidate_x3.xml':(28,4),'atomic.xml':(63,0),'e3.xml':(26,0),'candidate_execution/f2/junit.xml':(42,0),'reviewer_hostiles.xml':(20,2),'original_seeded.xml':(4,4),'candidate_seeded.xml':(4,0),'inherited/r1_45.xml':(45,0),'inherited/repair_5.xml':(5,0),'inherited/e2_full.xml':(44,2),'inherited/e2_strict.xml':(2,0),'inherited/x2.xml':(17,1),'inherited/m2_41.xml':(41,0),'inherited/m1_37_on_m2.xml':(37,19),'inherited/i2_23_on_m2.xml':(23,10),'inherited/m3_source_preimage_3_red.xml':(3,3),'inherited/b2/b1.xml':(39,0),'inherited/b2/p1.xml':(74,0),'inherited/b2/f1.xml':(97,0),'inherited/b2/integration.xml':(81,0)}
 for name,counts in expected.items():
  s=suites[name];assert (s['tests'],s['failures'])==counts and s['errors']==s['skipped']==0,name
  t=ET.parse(E/name).getroot();assert sum(1 for x in t.iter('testcase') if x.find('failure') is not None)==counts[1]
 checked('All required unchanged and new suite executions, historical REDs literal','suite_results.json and original JUnit/logs; duplicated copies excluded from counts')
 d=read('evidence/inherited/b2_execution_receipt.json');assert d['f1']['raw_native_failures']==17 and d['f1']['raw_native_exit']==1
 for label,count in [('d1_original',22),('d1_corrected',17)]:
  text=(E/'inherited/b2'/(label+'.log')).read_text();assert sum(line.startswith('PASS ') for line in text.splitlines())==count
  assert next(x for x in d['commands'] if x['label']==label)['exit_code']==0
 native=json.loads((E/'inherited/b2/f1_native_gate.log').read_text());assert len(native['failures'])==17 and native['status']=='RED'
 checked('Independent 249 inherited and native17 distinction','inherited/b2_execution_receipt.json; d1 logs; raw f1_native_gate.log')
 f2=read('evidence/f2_blinded/matrix.json');assert len(f2['rows'])==42 and f2['expected_removed_before_engine'] and f2['case_ids_blinded'] and f2['oracle_only_after_engine']
 for x in f2['rows']:
  assert not x['errors'];assert not any('reference_oracle.py' in k for k in x['calls'])
  if x['status']=='ELIGIBLE_NONCAUSAL':
   for call in ('.runtime/b2/bridge.py:advance','.runtime/m2/kernel.py:eligible','integration.py:response'):assert x['calls'].get(call)
 assert sum(x['status']=='ELIGIBLE_NONCAUSAL' for x in f2['rows'])==20
 checked('Unchanged and blinded F2, real imports rather than labels/oracle routing','candidate_execution/f2/junit.xml; f2_blinded/matrix.json')
 prereg=read('preregistration.json');assert prereg['before_any_reviewer_test_execution']
 for path,digest in prereg['files'].items():assert sha((ROOT/path).read_bytes())==digest
 assert sha((ROOT/'test_seeded_refusals.py').read_bytes())==read('preregistration_seeded.json')['sha256']
 checked('At least five independently preregistered hostile categories before execution','preregistration.json; preregistration_seeded.json; frozen test hashes')
 for family in ('candidate_seeded_sql',):
  for p in (E/family).glob('*.json'):
   x=json.loads(p.read_text());assert x['before']['tables']==x['after']['tables'] and x['before']['schema']==x['after']['schema']
 x=read('evidence/reviewer_sql/external_row.json');assert x['result']['status']=='REFUSED' and x['result']['code']=='PUBLICATION_READSET_CHANGED' and not x['result']['no_mutation']
 assert x['external']['snapshot']['tables']==x['after']['tables'] and not x['after']['tables']['b3_transition']
 checked('Five repaired X3 identities, clean/seeded equality, independent objective facts preserved','x3_adjudication.json; table_case_matrix.json; original/candidate_seeded_sql; reviewer_sql/external_row.json')
 x=read('evidence/candidate_x3_sql/privileged_guard_to_commit_race.json');assert x['result']['status']=='REFUSED' and x['result']['code']=='PUBLICATION_READSET_CHANGED' and not x['result']['no_mutation']
 assert [k for k,v in x['before'].items() if x['after'][k]!=v]==['b3_preimage']
 checked('Obsolete fourth X3 assertion separately classified','candidate_x3_sql/privileged_guard_to_commit_race.json')
 for p in (E/'reviewer_sql').glob('late_target_*.json'):
  x=json.loads(p.read_text());assert x['before']['tables']==x['after']['tables'] and not x['result']['owner_effect_committed'] and 'independent_owner_receipt' not in x['result']
 x=read('evidence/atomic_sql/independent_exact_then_permission_denied.json');assert x['result']['status']=='ELIGIBLE_NONCAUSAL' and x['result']['CAN011_transition']['status']=='DENIED'
 checked('Target denial/empty, late validation failure, public no-partial-effect boundary','atomic_sql/independent_exact_then_permission_denied.json; reviewer_sql/late_target_*.json')
 k=read('evidence/process_death_summary.json')['new_reviewer_process_kills'];assert len(k)==10
 for x in k:assert x['exit']==-9 and x['ready_pid']!=x['inspector_pid'] and (x['stage']=='after_successful_return' or x['tables_unchanged'])
 assert len(list((E/'atomic_sql').glob('kill_*.json')))==12
 sql=read('evidence/sql_cold_audit.json')
 for version in ('original','candidate'):
  for label in ('positive','permission_absent'):assert sql[version+'/'+label]['snapshot_sha256']==sql[version+'/'+label+'_cold']['snapshot_sha256']
 checked('Real cross-process death, cold success/refusal/crash, no power-loss promotion','process_death_summary.json; atomic_sql/kill_*; sql_cold_audit.json; cold replay logs')
 for name in ('schema_only_race','schema_refusal_flag'):
  x=read('evidence/reviewer_sql/'+name+'.json');assert x['before']['schema']!=x['after']['schema']
 x=read('evidence/reviewer_sql/schema_only_race.json');assert x['result']['status']=='ELIGIBLE_NONCAUSAL'
 x=read('evidence/reviewer_sql/schema_refusal_flag.json');assert x['result']['status']=='REFUSED' and x['result']['no_mutation'] is True
 assert set(suites['reviewer_hostiles.xml']['failed_tests'])=={'test_schema_only_race_is_rejected','test_schema_change_on_refusal_sets_no_mutation_false'}
 checked('New schema REDs preserved and distinguished from privileged-writer universal immunity','reviewer_hostiles.xml; reviewer_sql/schema*.json; 02_REQUIREMENTS_AND_LIMITATIONS.md')
 commands=read('evidence/commands.json');assert all(x['exit']==x['expected'] for x in commands)
 assert {'inherited','frozen_b3','candidate_b3','original_x3','candidate_x3','atomic','e3','f2','f2_blinded','b3_mutants','original_loop','candidate_loop','original_positive_cold','original_permission_absent_cold','candidate_positive_cold','candidate_permission_absent_cold','reviewer_hostiles','original_seeded','candidate_seeded'}<={x['label'] for x in commands}
 for f in ('00_RETURN.md','02_REQUIREMENTS_AND_LIMITATIONS.md','environment_passport_delta.json','README.md'):assert (ROOT/f).is_file()
 checked('Scoped verdict, scientific qualifications, owner permissions, portable passport','00_RETURN.md; 02_REQUIREMENTS_AND_LIMITATIONS.md; environment_passport_delta.json')
 for p in ROOT.rglob('*'):
  if '.scratch' in p.parts or not p.is_file():continue
  if p.suffix in ('.py','.json','.md','.log','.xml','.txt'):
   data=p.read_bytes();assert not re.search(rb'/Users/[A-Za-z0-9_.-]+/',data),str(p)
  if p.suffix=='.py' and 'inputs' not in p.parts:compile(p.read_bytes(),p.name,'exec')
 checked('Frozen inputs intact; new source compilation and portable path hygiene','input_transport_manifest.json; source verification; this audit')
 (E/'completion_audit.json').write_text(json.dumps({'review_execution_and_artifacts_complete':True,'candidate_qualification':'REVISE','requirements':audit,'transport_and_remote_verification':'Performed after final commit; exact SHA reported externally, never self-referenced in preimage'},indent=2)+'\n')
 print(json.dumps({'audit_requirements_proven':len(audit),'qualification':'REVISE','review_complete':True}))
if __name__=='__main__':main()
