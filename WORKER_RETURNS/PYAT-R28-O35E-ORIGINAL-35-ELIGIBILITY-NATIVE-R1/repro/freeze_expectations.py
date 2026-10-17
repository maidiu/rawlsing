"""Freeze independent metadata census and prospective TEST_ONLY expectations.

This never calls the candidate and never issues original eligibility.
"""
import csv, hashlib, json, platform, sys
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
PINNED=HERE/'runtime/pinned'
QRA='data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'

def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 out=HERE/'PREREGISTERED_EXPECTATIONS.json'
 assert not out.exists(), 'never silently replace a prospective seal'
 rows=list(csv.DictReader((PINNED/QRA).open()))
 active=[r for r in rows if r['authority_status']!='EXCLUDED_INACTIVE_WAVE']
 keys=[{k:r[k] for k in ('source','wave','canonical_source','canonical_wave','country_code_scope','question_id','var_code','governed_row_payload_hash')} for r in active]
 keys.sort(key=lambda r:json.dumps(r,sort_keys=True))
 assert len(keys)==18259
 selected=[]
 for family in ('Afrobarometer','Arab Barometer','GSS','LiTS','WVS'):
  candidates=[r for r in active if r['canonical_source']==family and r['authority_status'] in ('GOVERNED_QSMV2_RELATION_AUTHORITY','GOVERNED_MANUAL_RELATION_AUTHORITY','FROZEN_ACCEPTED_GSS')]
  r=sorted(candidates,key=lambda x:(x['canonical_wave'],x['question_id'],x['var_code']))[0]
  selected.append({k:r[k] for k in ('source','wave','canonical_source','canonical_wave','country_code_scope','question_id','var_code','governed_row_payload_hash')})
 frozen={
  'schema':'O35E_PROSPECTIVE_EXPECTATIONS@1','original_permission':'HOLD_NO_VERIFIED_SIGNED_WARRANT',
  'original_eligible_item_count':None,'original_native_negative_status':'UNCONSTRUCTIBLE_WITHOUT_COMPETENT_U_E_PRE',
  'metadata_census_count':len(keys),'metadata_keys_sha256':digest(keys),
  'metadata_keys_file':'frozen_metadata_keys.json','five_preserved_relation_item_omission_controls':selected,
  'metadata_negative_controls':['omit_each_of_five','extra_inactive_asian_W6','source_swap','edition_swap','revoked_testonly_grant','same_count_partition_substitution'],
  'metadata_claim_ceiling':'Loss from preserved QRA metadata only; NOT proof of original eligibility/completeness.',
  'testonly_native_positive':{'fixture':'rawlsing_next.tests.test_pre553_route_b_production._fixture',
   'source_kind':'ExactPhysicalCellStream in memory; no actual SAV/DTA decoder or survey source',
   'roles':['raw Y query','governed weighted Y query','exact bounded discovery'],
   'physical_rows':3,'raw_Y_denominator':2,'raw_Y_numerators':{'0':1,'1':1},
   'weighted_Y_denominator':3,'weighted_Y_numerators':{'0':1,'1':2},
   'R3_Y':'NOT_ELIGIBLE; never denominator 3','consumer':'actual OC01 SOURCE_LOCAL_STATISTIC policy, TEST_ONLY refs',
   'positive_requirements':['actual C11 release','actual I03/I05 calls inside Batch callbacks','exact result-ref outer join','literal fact payload retained','fresh-process identical semantic receipts']},
  'native_hostiles':['omit_raw_query','omit_weighted_query','extra_query','source_swap_before_I03','projection_authority_removed','same_count_query_partition_swap','missing_weight_never_value','valid_empty_not_positive_discovery','receipt_result_ref_substitution','missing_discovery_before_consumer'],
  'unexecuted_original_controls':['missing_original_B_1','missing_original_B_2','missing_original_B_3','missing_original_B_4','missing_original_B_5','extra_ineligible_original','wrong_original_source','wrong_original_edition','original_warrant_revocation','same_count_original_partition_swap'],
  'no_promotions':['original_source_pass','original_U_E_pre','N9_grant','OC05','N11','N12','V3'],
 }
 (HERE/'frozen_metadata_keys.json').write_text(json.dumps(keys,ensure_ascii=False,separators=(',',':'))+'\n')
 out.write_text(json.dumps(frozen,indent=2,ensure_ascii=False)+'\n')
 passport={'schema':'O35E_ENVIRONMENT_PASSPORT_DELTA@1','startup':'246fcdf7b25c6b160c0a167e4284e08d04194505',
  'branch':'agent/rabochii-pyat-r28-o35e-original-wave-eligibility-native-positive-r1','canonical_read_cut':'eede2b8bdb9fcdcc1d4187912f8e00773869c22c',
  'surface':'existing isolated local worktree and shared Git object store','python':sys.version,'platform':platform.system(),
  'write_test':'runtime/pinned staged successfully; no external terrain writes',
  'tools':{'git':'VERIFIED','python':'VERIFIED','pytest':'VERIFIED_PRIOR_SESSION','metadata_pandas_runtime':'VERIFIED_PRIOR_SESSION'},
  'model':'current Codex session; exact provider configuration not programmatically verified; no override or helper',
  'money':'UNKNOWN','quota':'UNKNOWN','external_model_calls':0,'subagents':0,
  'access':'SOURCEFREE_METADATA_AND_TESTONLY_NATIVE','private_respondent_or_original_SAV_DTA_opened':False,
  'reuse':'warm existing worktree/object store; staged exact33 files; no broad clone or installs',
  'eligibility':'assigned scientific archaeologist/native experimenter; NOT source/eligibility issuer or adopter'}
 (HERE/'environment_passport_delta.json').write_text(json.dumps(passport,indent=2)+'\n')
 print(json.dumps({'metadata_count':len(keys),'metadata_root':digest(keys),'seal_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'five_items':selected},ensure_ascii=False))

if __name__=='__main__':main()
