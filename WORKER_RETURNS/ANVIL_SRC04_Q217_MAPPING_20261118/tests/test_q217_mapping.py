import json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from residual_check import residual_check

def load(n): return json.loads((HERE/'evidence'/n).read_text())

def test_aggregate_correction_and_exact_38_unlabeled_cells():
    d=load('q217_aggregate.json')
    assert d['source_rows']==7337
    assert d['q217']['codes']['7.0']==38
    assert d['q217']['codes']['None']==187
    known=sum(v for k,v in d['q217']['codes'].items() if k!='7.0' and k!='None')
    assert known==7112
    assert d['q217']['missing_states']=={'OBSERVED_STORAGE_VALUE':7150,'SYSTEM_MISSING':187}

def test_v3_is_actual_selectable_successor_and_180_columns_stable():
    v=load('q217_v3_validation.json')
    assert v['status']=='SELECTABLE_SUCCESSOR_NOT_LIVE_SELECTED'
    assert v['physical_slots_total']==181 and v['physical_slots_unchanged']==181
    assert v['field_diff']['physical_slots_byte_equivalent'] is True
    assert v['response_slots_total']==178 and v['response_slots_unchanged']==177
    assert all(v['field_diff'].values())
    assert v['live_selection_changed'] is False and v['original_source_file_touched'] is False
    assert v['v3']['file_sha256']=='f007afdc0cbcd58a3f856121e265a5069f2145cce6c9ce0c112aff1f9c7d7855'
    assert v['v3']['canonical_sha256']=='a3d3267cc37f7f6d2f6267d777c414f285be58ff5e7ea88b8bc9ac0d74c1269f'

def test_only_q217_states_changed():
    v=load('q217_v3_validation.json'); q=v['q217']
    assert q['labels_added']=={}
    assert q['physical_code_7_label_present'] is False
    assert q['questionnaire_label']=={'7.0':'Other'}
    assert q['physical_metadata_q217_labels'].get('10.0')=='others'
    assert q['code_7_state']=='SOURCE_SPECIFIC_SPECIAL'
    assert q['code_7_canonical'] is None
    assert q['code_99_state']=='REFUSAL' and q['code_97_98_state']=='DK'
    assert q['system_missing_state']=='MISSING'
    assert q['substantive_known_codes']==['1.0','2.0','3.0','4.0','5.0','6.0','10.0']
    cfg=json.loads((HERE/'source.config.repaired.v3.json').read_text())
    rs=next(x for x in cfg['response_slots'] if x.get('question_id')=='q217')
    states={str(x['raw_value']):(x['response_state'],x.get('canonical_value')) for x in rs['values']}
    assert states['7.0']==('SOURCE_SPECIFIC_SPECIAL',None)
    assert states['99.0']==('REFUSAL',None)
    assert '7.0' not in next(x for x in cfg['physical_slots'] if x.get('name')=='q217')['value_labels']
    assert states['97.0']==('DK',None) and states['98.0']==('DK',None)
    assert states['None']==('MISSING',None)
    assert states['1.0']==('SUBSTANTIVE_RESPONSE','1')
    assert states['10.0']==('SUBSTANTIVE_RESPONSE','10')

def test_questionnaire_page_5_corroborates_only_code_7_other():
    s=load('questionnaire_q217_scan.json')
    assert s['q217_page']==5
    assert '7 = Other' in s['exact_scan_lines']
    assert s['code_7_label_corroborated']=='Other'
    assert s['code_99_label_corroborated']=='Decline to Answer'
    assert 'NO_CROSS_WAVE_OR_FREQUENCY_INFERENCE' in s['use_scope']

def test_native_projection_retains_raw_7_and_states():
    n=load('q217_native_witness.json')
    assert n['native_projection_completed'] is True
    assert n['event_count']==12
    assert n['response_rules']=='source.config.repaired.v3.json q217 values'
    by_bits={e['raw_bits']:e for e in n['projection_events'] if e['raw_bits']}
    assert by_bits['3ff0000000000000']['response_state']=='SUBSTANTIVE_RESPONSE'
    assert by_bits['3ff0000000000000']['canonical_value']=='1'
    assert by_bits['401c000000000000']['response_state']=='SOURCE_SPECIFIC_SPECIAL'
    assert by_bits['401c000000000000']['canonical_value'] is None
    assert by_bits['4058c00000000000']['response_state']=='REFUSAL'
    assert by_bits['4058400000000000']['response_state']=='DK'
    assert by_bits['4058800000000000']['response_state']=='DK'
    assert any(e['raw_kind']=='none' and e['response_state']=='MISSING' for e in n['projection_events'])
    assert n['raw_7_identity'].startswith('RETAINED_AS_FLOAT64_BITS_401c000000000000')

def test_generic_residual_check_separates_known_unknown_missing():
    d=load('q217_aggregate.json'); r=residual_check(d['q217']['codes'],d['config']['q217_labels'])
    assert r['unlabeled_observed']=={'7.0':38}
    assert r['system_missing']=={'None':187}
    assert r['all_observed_accounted'] is True
