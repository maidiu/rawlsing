"""Read-only completion checks against actual bytes, native records and JUnit.

This proves implementer evidence coverage, not independent WG0N acceptance.
"""
import collections,hashlib,json,subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
P=R/'court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate'
COUNTS={'wg0m33':33,'original65':65,'j44_k11':55,'owners80':80,'original3':3,'author26':26,'author69':69,'fresh':42,'cold_pointer':1}
def git(*a):return subprocess.check_output(['git','-C',str(ROOT),'-c','gc.auto=0',*a])
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 results={}
 for name,n in COUNTS.items():
  xml=R/'observations'/(name+'.xml');tree=ET.parse(xml);terminal=load(R/'observations'/(name+'.terminal.json'))
  row=dict(tests=len(tree.findall('.//testcase')),failures=len(tree.findall('.//failure')),
           errors=len(tree.findall('.//error')),skips=len(tree.findall('.//skipped')),exit=terminal['exit'],
           junit='observations/'+xml.name,junit_sha256=sha(xml),command=terminal['command'])
  assert row['tests']==n and row['failures']==row['errors']==row['skips']==row['exit']==0,(name,row)
  results[name]=row
 assert load(R/'observations/baseline33.terminal.json')['failures']==1
 baseline=load(R/'observations/baseline_source_attack.json')
 assert len(baseline)==2 and all(x['material_digest_unchanged'] and x['new_I03_calls']==3 and x['consumer'] and x['exception'] is None for x in baseline)
 source=load(R/'SOURCE_INPUTS.json')['files'];productive=R/'court/runtime_phase_b/p5_return/review/runtime_phase_b/candidate/repro/wg0p4_workload.py'
 changed=[]
 for row in source:
  path=R/row['staged_path'];b=path.read_bytes()
  original=git('show',row['commit']+':'+row['source_path'])
  assert hashlib.sha256(original).hexdigest()==row['sha256']
  assert hashlib.sha1(b'blob '+str(len(original)).encode()+b'\0'+original).hexdigest()==row['git_blob_sha1']
  if b!=original:changed.append(row['staged_path'])
 assert changed==[str(productive.relative_to(R))],changed
 pin=load(R/'CANDIDATE_CODE_PIN.json')
 for row in pin['files']:
  b=(R/row['staged_path']).read_bytes()
  assert hashlib.sha256(b).hexdigest()==row['sha256']
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
 assert productive.read_bytes()==git('show',pin['code_snapshot_commit']+':'+pin['files'][0]['source_path'])
 freeze_path='WORKER_RETURNS/PYAT-R27-WG0P6-RELEASE-VIEW-SOURCE-ARTIFACT-BINDING-R1/HOSTILE_EXPECTATIONS.json'
 assert (R/'HOSTILE_EXPECTATIONS.json').read_bytes()==git('show','2f2364d17:'+freeze_path)
 nativepins=load(P/'source_selector.json')['files']
 for row in nativepins:
  b=(P/'pinned'/row['staging_path']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
 imported={};physical_roots=set();receipts=list((R/'observations/imports').glob('*.json'))
 for file in receipts:
  for row in load(file)['actually_loaded_modules']:
   if row['module'].startswith('rawlsing_next.'):
    path=Path(row['file'].replace('<WORKTREE>',str(ROOT)).replace('<HOME>',str(Path.home())))
    allowed=[P/'pinned/rawlsing_next',R/'court/runtime_phase_b/candidate/pinned/rawlsing_next']
    assert any(path.is_relative_to(root) for root in allowed),row
    assert sha(path)==row['sha256']
    assert path.read_bytes()==(P/'pinned/rawlsing_next'/path.name).read_bytes(),row
    physical_roots.add(str(path.parent.relative_to(R)))
    imported[row['module']]=row
 assert len(imported)>=12
 cold=load(R/'court/observations/phase_b/controls_v1_final/cold__same_original_manifest.json')
 assert cold['checkpoint_exit']==23 and cold['first_pid']!=cold['second_pid']
 assert cold['first_I03_calls']==1 and cold['second_I03_calls']==2
 assert cold['manifest_units']==3 and cold['manifest_before']==cold['manifest_after']
 assert cold['original_receipt_preimage_verified'] and cold['original_receipt_hash'] in cold['final_receipt_hashes']
 assert cold['all_original_results_resolved'] and all(cold[k] for k in ['fsync_file','fsync_directory','atomic_replace'])
 assert collections.Counter(x['disposition'] for x in cold['frontier'])=={'PRODUCED':3,'HELD':16,'INADMISSIBLE':6}
 old=json.loads(git('show','b91642ce98ec2c74b6d0c5d06ec8b83f67f02e86:WORKER_RETURNS/PYAT-R26-WG0M-ORIGINAL-FRONTIER-INDEPENDENT-DELTA-R1/02_ACTUAL_EXECUTION_OR_TYPED_HOLD.json'))['cold']
 assert old['manifest_before']==cold['manifest_before'] and old['final_receipt_hashes']==cold['final_receipt_hashes']
 cond=load(R/'court/observations/phase_b/controls_v1_final/conditional__ordinary_full_chain_yes1_no1_over2.json')
 assert cond['denominator']==2 and cond['counts']=={'yes':1,'no':1} and cond['same_respondents']==['R2','R3']
 assert cond['second_frontier_verified_against_independent_register'] and cond['separate_demo_function_called'] is False
 assert cond['owner_query_calls']>=1 and cond['owner_batch_calls']>=1
 negative=load(R/'observations/fresh_process_source_pointer_refusal.json')
 assert negative['child_exit']==0 and negative['pid']!=negative['original_crash_pid']
 assert negative['new_I03_calls']==negative['restored_receipts']==0 and negative['error']['type']=='IdentityError'
 assert negative['owner_journal_unchanged'] and negative['custody_unchanged'] and negative['same_original_manifest']
 for file in (R/'court/observations/descriptor_runs/wg0m33').glob('*.json'):
  actual=load(file);assert actual['new_I03_calls']==0 and not actual['served_positive'] and actual['exception_type'] is not None
 custody=dict(original_inputs=len(source),unchanged_original_inputs=len(source)-len(changed),productive_patch=changed,
              accepted_candidate_pins=len(nativepins),staged_native_modules=sum(x['staging_path'].startswith('rawlsing_next/') for x in nativepins),
              actual_imported_native_modules=imported,import_receipts=len(receipts),native_physical_roots=sorted(physical_roots),
              physical_root_limit='Legacy reviewer helpers can resolve optional native modules from either of the two byte-identical pinned closures; every observed file is checked against the accepted P5 owner pin. The six critical C11/I03/Batch owners are separately checked by physical_modules in the P5 closure.',
              original_oracles_and_tests_unchanged=True,code_snapshot_commit=pin['code_snapshot_commit'],
              productive_code_sha256=sha(productive),native_receipt_and_manifest_identities_equal_to_WG0M=True)
 dump(R/'observations/source_custody_final.json',custody)
 dump(R/'02_OLD_COURT_AND_POSITIVES.json',dict(schema='WG0P6_ACTUAL_COURTS_AND_COLD_POSITIVES@1',
      at_utc=datetime.now(timezone.utc).isoformat(),scope='IMPLEMENTER_REGRESSION_ONLY_WG0N_PENDING',
      results=results,cold={k:v for k,v in cold.items() if k not in ['consumer','calls','frontier','physical_module_files']},
      conditional={k:v for k,v in cond.items() if k not in ['consumer','calls','conditional_calls','original_frontier','physical_module_files']},
      native_consumer=cold['consumer'],original_frontier=cold['frontier'],fresh_process_pointer_negative=negative,
      custody_summary={k:v for k,v in custody.items() if k!='actual_imported_native_modules'},
      original_baseline_RED_preserved=True,independent_WG0N_acceptance=False,no_new_original_source_rights=True))
 dump(R/'observations/completion_audit.json',dict(all_author_requirements_proven=True,mandatory_independent_acceptance='WG0N_NOT_PERFORMED_BY_AUTHOR',
      gates=['exact original attack reproduced','prospective freeze preserved','actual release-view/source-artifact binding implemented',
             'all mandatory old courts executed','fresh pointer/copy/rehash/currentness/consumer/restore negatives',
             'original25 unchanged','ordinary conditional over R2/R3','native same-original-manifest1+2 cold recovery',
             'accepted native preimages preserved','actual physical imports measured'],
      publication='VERIFY_DIRECT_REMOTE_BEFORE_FINAL_COMPLETION',rights_unchanged=True))
 print(json.dumps(dict(courts={k:v['tests'] for k,v in results.items()},source_inputs=len(source),unchanged=len(source)-1,
                       native_modules=len(imported),cold='1+2 SAME ORIGINAL MANIFEST',conditional='yes1/no1 over R2/R3',all_pass=True),indent=2))
if __name__=='__main__':main()
