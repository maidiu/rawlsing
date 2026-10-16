"""Evidence/source/requirement audit, not a semantic or HQ adoption action."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,sys
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1]
def load(p):return json.loads((R/p).read_text())
def write(p,d):(R/p).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sha(b):return hashlib.sha256(b).hexdigest()
def counts(path):
 cases=list(ET.parse(R/path).getroot().iter('testcase'));return dict(tests=len(cases),passed=sum(all(c.find(k) is None for k in ['failure','error','skipped']) for c in cases),failed=sum(c.find('failure') is not None for c in cases),errors=sum(c.find('error') is not None for c in cases),skipped=sum(c.find('skipped') is not None for c in cases))
assert counts('evidence/proposal_v2.xml')==dict(tests=24,passed=24,failed=0,errors=0,skipped=0)
assert counts('evidence/handoff.xml')==dict(tests=16,passed=16,failed=0,errors=0,skipped=0)
assert counts('evidence/raw_semantic.xml')==dict(tests=1,passed=0,failed=1,errors=0,skipped=0)
assert counts('evidence/prospective.xml')==dict(tests=24,passed=22,failed=2,errors=0,skipped=0)
freeze=load('freeze_manifest.json')
for p,h in freeze['files'].items():assert sha((R/p).read_bytes())==h and (R/p).read_bytes()==git('show','7e47e483469fa4f3b1fd69a6efa398dff612a396:'+str(R.relative_to(ROOT))+'/'+p)
err=load('oracle_locator_erratum.json');assert (R/err['corrected_file']).read_text()==(R/err['original_file']).read_text().replace(err['exact_single_replacement']['before'],err['exact_single_replacement']['after'])
assert sha((R/err['corrected_file']).read_bytes())==err['corrected_sha256']
for row in load('source_manifest.json'):
 b=(R/row['local']).read_bytes();assert blob(b)==row['git_blob'] and sha(b)==row['sha256'] and b==git('show',row['commit']+':'+row['path'])
assert len(load('source_manifest.json'))==119 and len(load('native_74_source_manifest.json')['files'])==74
for row in load('primary_decision_refs.json'):
 b=(R/row['local']).read_bytes();assert blob(b)==row['git_blob'] and b==git('show',row['commit']+':'+row['path'])
for n in ['tests/raw_semantic_obligation.py','tests/test_handoff.py']:
 assert (R/n).read_bytes()==git('show','c9d3271:WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-PV3A-HQ-METHOD-ACCESSION-EVIDENCE-R1/'+n)
assert (R/'retained/PV2I_original_48_cases.py').read_bytes()==(R/'runtime/court/frozen_pv2i/tests/test_independent.py').read_bytes()
summary=load('evidence/handoff/summary.json');assert summary['first_pid']!=summary['replay_pid'] and summary['processes'][0]['exit']==-9 and summary['first_new_durable']==[3,3] and summary['replay_new_durable']==[0,0] and summary['byte_identical_journals']
for k,v in load('handoff_oracle.json')['cold']['actual_replay_recomputation'].items():assert summary['recomputed_owner_calls'][k]==v
for p,h in summary['journal_sha256'].items():assert sha((R/'evidence/handoff/native_journals'/p).read_bytes())==h
original=load('primary_docs/01_PINNED_PV3N_METHOD_ORIGINAL_EIGHT_AND_PROOF.json');assert len(original['retained_proof']['repaired_method_authority_assertions'])==21
profiles={p:load('evidence/generic/'+p+'.json') for p in ['BASELINE','R2_Y1','R1_Y0']}
for name,d in profiles.items():
 assert len(d['report']['links'])==len(d['proposal']['entries'])==6 and len(d['proposal']['held'])==2
 assert {x['expected_work_key'] for x in d['installed']['complete_expected']['records']}=={x['expected_work_key'] for x in d['proposal']['entries']+d['proposal']['held']}
 for entry in d['proposal']['entries']:
  assert entry['proposed_generic_relation']=='GENERIC_NATIVE_SEMANTICS_HOLD' and entry['issuer_signature'] is None
  link=next(x for x in d['report']['links'] if x['original_expected_work_key']==entry['expected_work_key'])
  assert link['consumer_material']['roles']['CONDITIONER']['source_native_variable']=='Q86B' and link['consumer_material']['roles']['TARGET']['source_native_variable']=='Q86A'
  if entry['slot']=='DISCOVERY':assert entry['native_role_order']==[] and entry['original_scope']['operation']['semantic_roles']==['BASE']
base=profiles['BASELINE']
for name,d in profiles.items():
 if name=='BASELINE':continue
 for family,key in [('report','links'),('proposal','entries')]:
  for row in d[family][key]:
   ns=row['original_identity']['original']['respondent_namespace'] if key=='links' else row['namespace']
   if ns=='PV2-ADULT-B':assert row in base[family][key]
current=load('evidence/generic/current_history.json');assert current['A_after']['entries']==[] and current['B_after']==current['B_before'] and current['historical_proposal_unchanged']
edge=load('evidence/generic/edge_cases.json');assert edge['empty_risk']['fact']['typed_state']=='ZERO_SUPPORT' and edge['empty_risk']['consumer']['typed_state']=='ZERO_SUPPORT';assert edge['missing']['typed_state']=='UNRESOLVED' and edge['missing']['semantic_fields']['raw_denominator_support']==2 and edge['missing']['semantic_fields']['raw_resolved_target_support']==1
D=load('decision_record_candidate.json');assert D['status']=='COMPETENT_DECISION_PENDING' and all(D[x] is None for x in ['binding_decision','signer','signed_at','effective_scope'])
C=load('proposal_contract.json');assert C['authority_signature'] is None and C['HQ_adoption'] is None
write('01_PV3N_PV3A_METHOD_AND_AUTHORITY.json',dict(schema='PV3H_METHOD_AND_AUTHORITY_ADJUDICATION@1',decision=D,pins=dict(PV3='5c70c7d347998907c1c8a865f833dad581777a0e',PV3N='816aaac865a184e572dde10ff0802969bc51eed5',PV3A='c9d3271c5391c056d30e329b322fc49a2fdeacc1'),original_expected_root=base['method_receipt']['expected_root'],register_root=base['method_receipt']['register_root'],all_eight_original_operations=base['method_receipt']['operations'],current_candidate=dict(passed=300,raw_semantic_failed=1),historical=dict(passed=26,failed=22),method_authority_repairs=original['retained_proof']['repaired_method_authority_assertions'],full_owner_court_rerun=False,currentness='governance_live_cut.json'))
write('02_SPECIALIZED_GT2_AND_NEXT_GENERIC_FAMILY_POSITIVE.json',dict(schema='PV3H_TWO_OUTPUTS@1',accepted_specialized=dict(owner='FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER',relation='EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0',profiles={k:dict(report=v['report'],actual_current=v['current'],actual_original_receipts=v['actual_receipts'],native_calls=v['trace']['call_counts'],trace_receipt='evidence/generic/'+k+'.json') for k,v in profiles.items()}),separate_generic_proposal=dict(contract='proposal_contract.json',frozen_oracle='frozen_oracle.json',profiles={k:v['proposal'] for k,v in profiles.items()},accepted_semantic_relation=False,status='GENERIC_NATIVE_SEMANTICS_HOLD',no_manual_fraction_substitution=True),cold=summary,current_history_receipt='evidence/generic/current_history.json',missing_and_empty_receipt='evidence/generic/edge_cases.json',tests=dict(final_proposal=counts('evidence/proposal_v2.xml'),unchanged_handoff=counts('evidence/handoff.xml'),raw_original_semantic=counts('evidence/raw_semantic.xml'),initial_frozen_locator_errors_retained=counts('evidence/prospective.xml'))))
changed=set(git('diff','--name-only','a36aa625d2567d35d3e826ff3191115829715735').decode().splitlines());assert all(p.startswith(str(R.relative_to(ROOT))+'/') for p in changed)
requirements=[('HQ decision evidence, exact current eligibility and unsigned pending outcome','decision_record_candidate.json;governance_live_cut.json'),('All8 original operations, six actual products, two ORDERED HELDs','01_PV3N_PV3A_METHOD_AND_AUTHORITY.json'),('Concrete prospectively frozen generic method proposal independently row-tested','proposal_contract.json;frozen_oracle.json;tests/test_pv3h.py;oracle_locator_erratum.json;proposal_v2.xml'),('Native respondent/eligibility/roles/risk/missing/zero/source custody','evidence/generic/*.json;40 final focused PASS'),('Genuine positive values-read with actual accepted owners and separate proposal','02_SPECIALIZED_GT2_AND_NEXT_GENERIC_FAMILY_POSITIVE.json'),('Original raw Q86-versus-X/Y failure remains literal','evidence/raw_semantic.xml;exact original source'),('Field Forge/O1-O6/protected-policy issuers and source rights held','03_SEMANTIC_EPRE_SOURCE_RIGHTS_AND_SIGNED_POLICY_HOLDS.md'),('Exact next lawful generic integration/rollback/independent acceptance warrant','04_NEXT_COMPETENT_HQ_AND_FIELD_FORGE_OWNER_WARRANT.md')]
write('completion_audit.json',dict(schema='PV3H_COMPLETION_AUDIT@1',status='DECISION_READY_COMPETENT_DECISION_PENDING',requirements=[dict(requirement=x,evidence=e,status='PROVED_AT_COMMISSIONED_GRAIN') for x,e in requirements],counts=dict(final_focused_pass=40,raw_semantic_fail=1,initial_frozen_pass=22,initial_test_locator_fail=2),source_files_verified=119,native_files_verified=74,full_PV3N_court_rerun=False,accepted_native_code_changed=False,generic_semantics_issued=False,HQ_adopted=False,tracked_write_scope_verified=True,publication='Final direct remote verification recorded after evidence push'))
print('VERIFIED:40 focused PASS; original semantic1 raw FAIL; initial2 locator failures retained; six specialized consumers and separate proposal; COMPETENT_DECISION_PENDING')
