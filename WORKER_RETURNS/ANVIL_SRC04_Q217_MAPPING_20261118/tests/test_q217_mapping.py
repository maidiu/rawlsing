import json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(HERE))
from residual_check import residual_check

def load(n): return json.loads((HERE/'evidence'/n).read_text())

def test_aggregate_has_exact_38_unlabeled_code_7_cells():
    d=load('q217_aggregate.json')
    assert d['source_rows']==7337
    assert d['q217']['codes']['7.0']==38
    assert d['q217']['codes']['None']==187
    assert d['q217']['missing_states']=={'OBSERVED_STORAGE_VALUE':7150,'SYSTEM_MISSING':187}

def test_only_corroborated_labels_are_used():
    c=load('source_codebook_q217.json'); p=load('physical_metadata_q217.json')
    assert c['file_sha256']=='8ad1af17b782d1ff3beb84c2d2331977195ac3bb48dbcc94a94a08ca725b288f'
    assert c['row']['value_labels_count']=='10'
    assert p['value_labels']['99.0']=='decline to answer'
    assert '7.0' not in p['value_labels']
    assert p['missing_ranges'] is None and p['missing_user_values'] is None

def test_residual_check_separates_known_unknown_and_missing():
    d=load('q217_aggregate.json')
    r=residual_check(d['q217']['codes'], d['config']['q217_labels'])
    assert r['unlabeled_observed']=={'7.0':38}
    assert r['system_missing']=={'None':187}
    assert r['labeled']['6.0']=={'count':37,'label':'sms messages'}
    assert r['all_observed_accounted'] is True

def test_candidate_retains_code_7_as_typed_unknown_and_marks_refusal():
    v=load('q217_candidate_validation.json')
    assert v['status']=='CANDIDATE_VALIDATED_NOT_APPLIED'
    assert v['q217_states']['7.0']=={'canonical':None,'missing':'OBSERVED_STORAGE_VALUE','state':'INVALID_UNRESOLVED'}
    assert v['q217_states']['99.0']['state']=='REFUSAL'
    assert v['policy']['code_7_labeled_or_substantive_refused'] is True
    assert v['policy']['unauthorized_label_or_frequency_inference_refused'] is True

def test_generic_residual_check_does_not_infer_new_codes():
    r=residual_check({'1.0':2,'8.0':3,'None':1},{'1.0':'yes'})
    assert r['labeled']=={'1.0':{'count':2,'label':'yes'}}
    assert r['unlabeled_observed']=={'8.0':3}
    assert r['system_missing']=={'None':1}
