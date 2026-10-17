"""Expectation-first descriptor court. No WG0P5 imports or remote inspection."""
from pathlib import Path
import hashlib,json,datetime,subprocess
R=Path(__file__).resolve().parents[1]
groups={
'descriptor':['source_edition','native_item_ids','release_tag','risk_name','targets_other_form','member_ids_same_cardinality','member_ids_denominator_drop','grant_withdrawn','grant_foreign','disposition_HELD','full_identity_hash','op_id','swapped_complete_spec','target_domain_same_cardinality','foreign_release_tag'],
'source':['release_source_edition','release_source_artifact','release_universe','release_risk_ref','release_form_ref','owner_revocation','owner_clock_change','owner_epoch_change'],
'fact':['denominator_rehash','numerator_same_total_swap','membership_same_cardinality','native_item_ids_projection','source_edition_projection'],
'copy':['shallow_copied_plan','copied_mapping','self_rehashed_contract','changed_semantic_description','same_cardinality_spec_swap']}
controls=[{'group':g,'case':c,'expected':'TYPED_REFUSAL_BEFORE_NEW_I03_AND_NO_POSITIVE_CONSUMER','allowed_exceptions':['IdentityError','FrontierError','RevocationError','ColdRestartError','NativeDataError','BatchIntegrityError'],'forbid':['SUPPORTED forged provenance','KeyError or other untyped escape','new native query after contradictory descriptor admitted']} for g,cs in groups.items() for c in cs]
paths=['01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json','tests/test_precommitted_phase_b.py','repro/precommitted_contract.py','tests/phase_b/test_additional_descriptor_binding_red.py','tests/phase_b/test_original_j_adapter_v1.py','tests/phase_b/test_original_k_adapter_v1.py']
preserve=[{'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()} for p in paths]
for row in json.loads((R/'observations/phase_b/accepted_owner_test_selector.json').read_text()):preserve.append({'path':row['staged_path'],'sha256':row['sha256']})
value={'schema':'WG0M_PRE_CANDIDATE_DESCRIPTOR_ORACLE@1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'WG0P5_observed':False,'WG0P5_sha':None,'sealed_startup':'b809dd46e4c0003cbef271fdb7490e93714e36fb','prior_court':'bec9a128922e4e431ce2ed862aa7802c902813ed','prior_candidate':'20d781c8502662bf788b60b828e46df55898d687','prior_three_reds_preserved':True,'controls':controls,'preserved_files':preserve,'science':{'original_frontier_count':25,'original_statuses':{'PRODUCED':3,'HELD':16,'INADMISSIBLE':6},'ordinary_conditional':{'yes':1,'no':1,'denominator':2,'exact_people':['R2','R3']},'cold':'Original3-unit manifest; genuine accepted prior receipt; actual exit23; fresh PID;1+2I03 calls; three original consumer results'},'law':'Contradictory copied descriptor/source metadata must be refused by typed admission before a new I03 call. Fact and authority attacks are measured only after constructing the genuine baseline; baseline queries are not attack-time execution. No original respondent/source authority or institutional acceptance is inferred.'}
(R/'01_FROZEN_DESCRIPTOR_EXPECTATIONS.json').write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
print('FROZEN_ADDITIONAL_CONTROLS',len(controls))
