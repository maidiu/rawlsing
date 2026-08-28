import hashlib, json
from pathlib import Path
import pandas as pd
import pytest

import importlib.util

MODULE_PATH = Path(__file__).with_name("qsr_lower_level_replay.py")
_spec = importlib.util.spec_from_file_location("qsr_lower_level_replay", MODULE_PATH)
assert _spec and _spec.loader
qsr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qsr)
QSRReplayError = qsr.QSRReplayError
_load_spec = qsr._load_spec
_rewrite_transport_manifest = qsr._rewrite_transport_manifest
_verify_hash = qsr._verify_hash
compare_qsr = qsr.compare_qsr


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_hash_mismatch_fails_closed(tmp_path):
    p=tmp_path/'producer.csv'; p.write_bytes(b'actual')
    with pytest.raises(QSRReplayError, match='producer hash mismatch'):
        _verify_hash(p, h(b'expected'), 'audit:test')


def test_missing_producer_fails_closed(tmp_path):
    with pytest.raises(QSRReplayError, match='missing producer'):
        _verify_hash(tmp_path/'missing.csv', h(b'x'), 'audit:test')


def test_dependency_census_rejects_excluded_asian_w6(tmp_path):
    spec={
      'contract':'QSR_LOWER_LEVEL_REPLAY_DEPENDENCIES@1.0.0',
      'expected_scope_count':1,
      'audit_producers':[{'dataset_id':'Asian_Barometer_Wave_6_Asian_Barometer_Wave_6'}],
    }
    p=tmp_path/'spec.json'; p.write_text(json.dumps(spec))
    with pytest.raises(QSRReplayError, match='W6'):
        _load_spec(p)


def test_transport_rewrite_changes_only_audit_paths(tmp_path):
    source=tmp_path/'manifest.csv'; target=tmp_path/'out.csv'; audit=tmp_path/'audits'; audit.mkdir()
    pd.DataFrame([{
      'dataset_id':'d1','canonical_intended':'true','wave':'w1',
      'audit_csv':'/old/a.csv','audit_yaml':'/old/a.yaml','audit_status':'green'
    }]).to_csv(source,index=False)
    receipt=_rewrite_transport_manifest(source,target,audit)
    a=pd.read_csv(source,dtype=str,keep_default_na=False)
    b=pd.read_csv(target,dtype=str,keep_default_na=False)
    assert a['dataset_id'].tolist()==b['dataset_id'].tolist()
    assert a['canonical_intended'].tolist()==b['canonical_intended'].tolist()
    assert a['audit_status'].tolist()==b['audit_status'].tolist()
    assert b.loc[0,'audit_csv']=='data/ddm_build_copy/reports/source_structure_audits/a.csv'
    assert b.loc[0,'audit_yaml']=='data/ddm_build_copy/reports/source_structure_audits/a.yaml'
    assert receipt['non_path_cells_identical'] is True


def test_carrier_tamper_is_detected_after_generation(tmp_path):
    columns=['needs_manual_review','source_structure_review_required','source_structure_classification']
    generated=tmp_path/'generated.csv'; reference=tmp_path/'reference.csv'
    pd.DataFrame([['yes','True','unknown']],columns=columns).to_csv(generated,index=False)
    pd.DataFrame([['no','True','unknown']],columns=columns).to_csv(reference,index=False)
    frame=pd.read_csv(generated,dtype=str,keep_default_na=False)
    root,_=qsr._row_identity_root(frame)
    expected={
      'rows':1,'columns':3,'sha256':h(generated.read_bytes()),
      'ordered_row_identity_root':root,'manual_review_yes_count':1,
      'source_structure_review_required_count':1,'unknown_classification_count':1,
    }
    result=compare_qsr(generated,reference,expected)
    assert result['pass'] is False
    assert result['differing_rows']==1
    assert result['differing_cells']==1
    assert result['raw_bytes_equal'] is False


def test_exact_35_dependency_census_is_accepted(tmp_path):
    audits=[{'dataset_id':f'dataset_{i:02d}'} for i in range(35)]
    spec={'contract':'QSR_LOWER_LEVEL_REPLAY_DEPENDENCIES@1.0.0','expected_scope_count':35,'audit_producers':audits}
    p=tmp_path/'spec.json'; p.write_text(json.dumps(spec))
    loaded=_load_spec(p)
    assert len(loaded['audit_producers'])==35
