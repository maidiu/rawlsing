"""Actual original metadata identities; NO claim of original eligible U/E_pre."""
import csv,hashlib,json
from pathlib import Path
import pytest
from native_court import HERE,independent_gate,ScientificHold,jsonkey

EXPECTED=json.loads((HERE/'frozen_metadata_keys.json').read_text())
FROZEN=json.loads((HERE/'PREREGISTERED_EXPECTATIONS.json').read_text())
MATRIX=json.loads((HERE/'01_35_WAVE_ELIGIBLE_ITEM_OPERATION_MATRIX.json').read_text())

def test_frozen_full_metadata_root_independent_of_manifest():
 root=hashlib.sha256(jsonkey(EXPECTED).encode()).hexdigest()
 assert root==FROZEN['metadata_keys_sha256']
 assert len(EXPECTED)==18259
 observed=[]
 for wave in MATRIX['waves']:
  for item in wave['items']:
   observed.append({'source':item['legacy_source'],'wave':item['legacy_wave'],
    'canonical_source':wave['canonical_source_family'],'canonical_wave':wave['canonical_wave'],
    'country_code_scope':item['country_code_scope_as_preserved'],'question_id':item['question_id'],
    'var_code':item['var_code'],'governed_row_payload_hash':item['governed_row_payload_hash']})
 assert independent_gate(EXPECTED,observed)['count']==18259

def test_exact_35_and_unknown_eligibility_never_zero():
 assert len(MATRIX['waves'])==35
 assert {tuple(x) for x in MATRIX['native_resolver']['observed_pairs']}=={(w['canonical_source_family'],w['canonical_wave'],'') for w in MATRIX['waves']}
 assert all(w['eligible_original_count'] is None and w['competent_original_E_pre_ref'] is None for w in MATRIX['waves'])
 assert all(w['dataset_manifest_identity']['recorded_source_sha256'] is None for w in MATRIX['waves'])
 assert all(w['native_original_runs']==0 for w in MATRIX['waves'])

@pytest.mark.parametrize('selected',FROZEN['five_preserved_relation_item_omission_controls'],ids=lambda r:r['question_id'])
def test_each_of_five_original_metadata_items_omitted_is_detected(selected):
 assert selected in EXPECTED
 observed=[r for r in EXPECTED if r!=selected]
 with pytest.raises(ScientificHold,match='missing'):independent_gate(EXPECTED,observed)

def test_extra_inactive_wave_item_detected():
 qra=HERE/'runtime/pinned/data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv'
 row=next(r for r in csv.DictReader(qra.open()) if r['authority_status']=='EXCLUDED_INACTIVE_WAVE')
 extra={k:row[k] for k in EXPECTED[0]}
 with pytest.raises(ScientificHold,match='extra'):independent_gate(EXPECTED,EXPECTED+[extra])

@pytest.mark.parametrize('field,value',[('canonical_source','WVS'),('canonical_wave','1973')])
def test_source_and_edition_substitution_detected(field,value):
 original=next(r for r in EXPECTED if r['question_id']=='GSS:1972:abdefect')
 changed={**original,field:value}
 observed=[changed if r is original else r for r in EXPECTED]
 assert len(EXPECTED)==len(observed)
 with pytest.raises(ScientificHold,match='missing'):independent_gate(EXPECTED,observed)

def test_same_count_partition_substitution_detected():
 original=next(r for r in EXPECTED if r['question_id']=='GSS:1972:abdefect')
 foreign=next(r for r in EXPECTED if r['question_id'].startswith('WVS:W7:'))
 observed=[foreign if r is original else r for r in EXPECTED]
 assert len(EXPECTED)==len(observed)
 with pytest.raises(ScientificHold,match='missing'):independent_gate(EXPECTED,observed)

def test_qra_relation_status_never_grants_source_or_eligibility():
 assert MATRIX['census']['original_measurement_products_this_return']==0
 assert MATRIX['census']['original_E_pre']=='ABSENT_AS_VERIFIED_COMPETENT_CURRENT_ISSUANCE'
 assert FROZEN['original_eligible_item_count'] is None
