"""Supplemental actual ingest and independent cold tamper/physical-source controls."""
from physical import *
import pytest,subprocess,shutil,copy
from dataclasses import replace
from rawlsing_next.pre553_c11_ingest import ingest_c11_source_release
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_source_backed_c11_facade import project_c11_candidate_from_physical_cells
E=R/'evidence/extra';E.mkdir(parents=True,exist_ok=True)

def child(root,mode):
 cmd=[sys.executable,str(R/'repro/abrupt_child.py'),str(root),mode]
 env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[R/'repro',C/'repro',RT,RT/'candidate/repro',C/'frozen_pv2i/repro'])),PYTHONDONTWRITEBYTECODE='1')
 p=subprocess.run(cmd,capture_output=True,text=True,env=env)
 return p,dict(argv=cmd,exit=p.returncode,stdout=p.stdout,stderr=p.stderr)

def test_actual_original_C11_ingestion_both_namespaces(tmp_path):
 owner,api,fx,installation=prepare(tmp_path/'source')
 rows=[]
 with Trace() as trace:
  for i,data in enumerate(fx['inputs']):
   stream=data['fx']['stream'];candidate=project_c11_candidate_from_physical_cells(source_sha256=stream.source_sha256,row_count=stream.row_count,cells=stream.iter_cells(),projection=data['projection']);repo=C11Repository()
   ingested=ingest_c11_source_release(candidate,repo);assert ingested.accepted
   assert ingested.release_ref in fx['plans'][i].p01_kwargs['session'].identity.release_refs
   rows.append(dict(namespace=data['universe'].respondent_namespace,accepted=ingested.accepted,release=ingested.release_ref.as_dict(),class_name=type(ingested).__module__+'.'+type(ingested).__name__))
 assert trace.data()['call_counts']['ingest_c11_source_release']==2
 write(E/'actual_ingestion.json',dict(installation=installation,results=rows,trace=trace.data()))

@pytest.mark.parametrize('attack',['none','journal_result_refs','journal_side_effect','checkpoint','expected','edition'])
def test_original_abrupt_receipt_cold_attacks(tmp_path,attack):
 # New independently installed TEST_ONLY fixture per attack, BEFORE caller replay.
 root=tmp_path/'cold';shutil.copytree(R/'runtime/abrupt_court',root)
 policy=root/'selected_current_owner.json';policy.unlink();owner=FixtureOwnerControl(policy_path=policy,provision=True)
 baseline=json.loads((root/'first.json').read_text());assert owner.installation.expected_root==baseline['installed_before_fixture']['expected_root']
 if attack.startswith('journal'):
  p=root/'ledger/0/b01e_side_effects.jsonl';lines=p.read_text().splitlines();d=json.loads(lines[0])
  if attack=='journal_result_refs':d['result_refs'][0]['content_hash']='e'*64
  else:d['PV3N_FORGED_SIDE_EFFECT']={'support':999}
  lines[0]=json.dumps(d);p.write_text('\n'.join(lines)+'\n')
 if attack=='checkpoint':
  p=root/'ledger/0/b01e_checkpoint.json';d=json.loads(p.read_text());d['identity']['manifest_hash']='e'*64;p.write_text(json.dumps(d))
 if attack=='edition':owner.advance('PV2-ADULT-A',edition='PV3N_NEW_NATIVE_EDITION')
 # Expected injection passes an actual forged expected set to full owner request.
 if attack=='expected':
  with Trace() as trace:
   o,a,fx,installed=prepare(root/'ledger',policy=policy)
   from rawlsing_next.pre553_original_identity_v2k_successor_candidate import FrozenOriginalExpected,ORIGIN
   e=FrozenOriginalExpected.from_records(tuple(x for x in fx['records'] if x.legacy.is_runnable),input_origin=ORIGIN)
   with pytest.raises(ValueError,match='ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT'):a.run_sourcefree_with_register(**dict(args(fx),expected=e))
  assert [len(x) for x in fx['calls']]==[0,0]
  write(E/'cold_expected.json',dict(code='ORIGINAL_EXPECTED_NOT_INSTALLED_ROOT',new_durable=[len(x) for x in fx['calls']],trace=trace.data()));return
 p,receipt=child(root,'attack')
 if attack=='none':
  assert p.returncode==0,p.stderr;d=json.loads((root/'attack.json').read_text());assert d['durable_calls']==[0,0];receipt['actual']=d
 else:
  assert p.returncode!=0
  expected={'journal_result_refs':'JOURNAL_RECEIPT_PROVENANCE_MISMATCH','journal_side_effect':'JOURNAL_RECEIPT_PROVENANCE_MISMATCH','checkpoint':'checkpoint','edition':'CURRENT_SOURCE_WITHDRAWN_OR_CHANGED'}[attack]
  assert expected.lower() in p.stderr.lower(),p.stderr
  d=json.loads((root/'attack_failure.json').read_text());assert d['trace']['actual_durable_executor_callbacks']==[]
  if d['durable_calls'] is not None:assert d['durable_calls']==[0,0]
  receipt['actual_failure']=d
 write(E/('cold_'+attack+'.json'),receipt)

def test_physical_missing_pinned_source_blocks_cold_before_import(tmp_path):
 # Inherited orchestration is terminal before this test. Only our staged copy moves.
 target=RT/'rawlsing_next/pre553_c11_ingest.py';missing=target.with_suffix('.physically_absent');assert target.is_file() and not missing.exists()
 target.rename(missing)
 try:p,receipt=child(tmp_path/'missing','attack')
 finally:missing.rename(target)
 assert p.returncode!=0 and 'MISSING_NATIVE_SOURCE_ATTESTATION:rawlsing_next/pre553_c11_ingest.py' in p.stderr
 assert reattest()==74
 write(E/'physical_missing_native_source.json',dict(**receipt,scope='ACTUAL file absent in this staged 74-object runtime; child refused before importing owner; original file restored',restored_all_74=True))
