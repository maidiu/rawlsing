"""Requirement audit of current source, actual results and causal evidence.

Completion here means author deliverable completed, NOT independent acceptance.
"""
from pathlib import Path
import json,hashlib,subprocess,ast
RET=Path(__file__).resolve().parents[1];PREFIX=str(RET.relative_to(Path.cwd()))+'/'
SOURCE_COMMIT='f9ff05197fb2837c733f8b453c678043e90c77d8'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
prior=(RET/'00_INHERITED_FROZEN_PREREG.json').read_bytes();assert sha(prior)=='056ebe78a4240a6123abcf4f1b390d90d1cf31c077e9085ddf9d0904dc473700'
for name in ('test_independent.py','causal_probe.py','run_suite.py'):
 b=(RET/'inherited/repro'/name).read_bytes();assert b==subprocess.check_output(['git','show','a11982e6cf135a8ecc72b6152ec796b4a4707093:WORKER_RETURNS/SOROK-R3-HQ303-RCP3-CAN008-COMPLETION-COURT-R1/repro/'+name])
for row in json.loads((RET/'01_CANDIDATE_SOURCE_FREEZE.json').read_text())['sources']:
 b=(RET/row['path']).read_bytes();assert sha(b)==row['sha256'] and blob(b)==row['blob_sha1']
 assert subprocess.check_output(['git','rev-parse',SOURCE_COMMIT+':'+PREFIX+row['path']]).decode().strip()==row['blob_sha1']
manifest=json.loads((RET/'lineage/00_ORIGINAL_SOURCE_MANIFEST.json').read_text())
for row in manifest:
 b=(RET/'runtime_root/original'/Path(row['local']).relative_to('runtime_root/source')).read_bytes();assert sha(b)==row['sha256'] and blob(b)==row['blob_sha1']
 assert subprocess.check_output(['git','rev-parse',row['commit']+':'+row['path']]).decode().strip()==row['blob_sha1']
matrix=json.loads((RET/'02_EXECUTED_CASE_MATRIX.json').read_text());runs={r['run']:r for r in matrix['runs']}
expected={'original_owners_initial':(220,0,0,0),'original_rsm_initial':(60,0,0,0),'original_candidate_initial':(37,0,0,0),'original_reviewer_initial':(82,45,0,0),'repaired_owners_sealed2':(220,0,0,0),'repaired_rsm_sealed2':(60,0,0,0),'repaired_candidate_sealed2':(37,8,0,0),'repaired_candidate_unset_sealed2':(37,8,0,1),'repaired_reviewer_sealed2':(82,1,0,0),'repair_sealed2':(89,0,0,0)}
for name,want in expected.items():
 run=runs[name];counts=run['counts'];assert tuple(counts[k] for k in ('tests','failures','errors','skipped'))==want
 assert len(run['cases'])==counts['tests']
 assert run['execution']['exit_code']==(1 if counts['failures'] else 0)
imports=json.loads((RET/'03_ACTUAL_IMPORT_RECEIPTS.json').read_text())['rows'];final=[r for r in imports if r['final']]
assert final and all(r['current_materialized_matches'] for r in final)
for r in final:
 b=(RET/r['canonical_local']).read_bytes();assert sha(b)==r['sha256'] and blob(b)==r['blob_sha1']
for name,expected_blob in [('CAN008_R2','b80dd6925066510ecbbfec7b427bf9f688475663'),('ADP016','c6619a286e115d060ab4830889e7fc23762167a5'),('ADP017','eece4f3f2f3f9288ab9bbc645dc81e20a99e1280')]:assert blob((RET/'runtime_root/law'/(name+'.txt')).read_bytes())==expected_blob
mapping=json.loads((RET/'06_REPAIR_LAW_AND_OWNER_ACTIONS.json').read_text());assert len(mapping['can008_23'])==23 and len(mapping['adp016_7'])==7 and len(mapping['adp016_17'])==17
base=json.loads((RET/'evidence/causal/baseline.json').read_text());result=base['result'];ledger=base['ledger_entries'][0]
for row in ledger:
 assert row['entry_hash']==sha(json.dumps({k:v for k,v in row.items() if k!='entry_hash'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
 if 'response_receipt' in row['payload']:
  receipt=row['payload']['response_receipt'];assert receipt['receipt_hash']==sha(json.dumps({k:v for k,v in receipt.items() if k!='receipt_hash'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
material=dict(receipt=ledger[0]['payload']['response_receipt'],trace=next(x['returned'] for x in base['calls'] if x['function']=='adp016_form_causal_trace'),epi=next(x['returned'] for x in base['calls'] if x['function']=='adp017_apply_epistemic_effect'),later=result['later_event_response'],ledger=ledger,state=result['state'])
assert sha(json.dumps(material,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())==result['full_replay_digest']
for mode in ('published_control','actual_absent_effect','physical_absent_effect'):
 d=json.loads((RET/'evidence/causal'/(mode+'.json')).read_text());assert d['result']['later_event_response']['effect_kind']=='AMPLIFY' and d['result']['later_event_response']['prior_effect_read'] is False
 if mode!='actual_absent_effect':assert not any(x['kind']=='CAN008_CURRENT_RESPONSE_EFFECT' and x['effective_causal_time']=='1998-10-03T16:00:00Z' for x in d['ledger_entries'][0])
for mode in ('forged_issuer','unadmitted','fake_event_hash'):
 d=json.loads((RET/'evidence/causal'/(mode+'.json')).read_text());assert d['result']['terminal']=='FIRST_EVENT_REFUSED' and d['ledger_entries'][0]==[] and not d['result']['state']['memories'] and not d['result']['state']['stances']
assert json.loads((RET/'evidence/causal/corrupt_stored_effect.json').read_text())['result']['terminal']=='LATER_EVENT_REFUSED'
ablation=json.loads((RET/'evidence/state_ref_ablation.json').read_text());assert ablation['baseline']['later_event_response']['effect_kind']==ablation['ablated']['later_event_response']['effect_kind']=='DEFLECT'
assert result['production_owner_hold']=='HOLD_NO_ACCEPTED_DESTINATION_OWNER_AUTHORITY' and result['public_standing_hold']=='HOLD_NO_PUBLIC_RATIFICATION_OWNER'
assert subprocess.check_output(['git','rev-parse','HEAD:rawlsing_next/v3_psepf_zero_positive_guard.py']).decode().strip()=='e0528d65215cb431196570c38bac4eae94217a1b'
for f in [*RET.joinpath('candidate').glob('*.py'),*RET.joinpath('repro').glob('*.py')]:ast.parse(f.read_text())
changed=subprocess.check_output(['git','diff','--name-only','79b22aea1254aefc191fedcf737c4f52ce5f8135','HEAD']).decode().splitlines();assert all(x.startswith(PREFIX) and '/runtime_root/' not in x for x in changed)
audit=dict(schema='CAN2_COMPLETION_AUDIT@1',author_deliverable_complete=True,independent_acceptance=False,source_commit=SOURCE_COMMIT,original_317='317 PASS',original_RCP3='37 PASS/45 RED',final_owners=220,final_rsm=60,final_candidate='29 PASS/8 RED',final_RCP3='81 PASS/1 RED',new_author_controls='89 PASS',primary_total='488 =479PASS/9RED; no errors/skips',conditional_features='5 N/A, not capability passes',inherited_tests_and_prereg_unchanged=True,final_actual_import_rows_verified=len(final),native_source_files_verified=len(manifest),law23_gate7_state17=True,causal_history_contrast=True,genuine_absent_controls=True,replay_reconstructed_from_actual_receipts=result['full_replay_digest'],memory_mediation_claim=False,accepted_destination_and_public_owners='TYPED_HOLD',production_guard='EMPTY_MAPPINGPROXY_EXACT_UNCHANGED',all_committed_paths_authorized=True,real_model_calls=0,original_respondent_data=0,V3_operation=0,semantic_issuance=0,adoption=False,remaining_steps='Publication and final direct remote readback recorded separately')
(RET/'completion_audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
