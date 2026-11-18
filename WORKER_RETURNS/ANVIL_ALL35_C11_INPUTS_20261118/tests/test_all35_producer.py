from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCER = ROOT / 'producer.py'
MATRIX = ROOT / 'evidence' / '35_row_source_rights_matrix.json'

def run(tmp_path, *extra):
    out = tmp_path / 'result.json'; bundles = tmp_path / 'bundles'
    cmd = [sys.executable, '-B', str(PRODUCER), '--matrix', str(MATRIX),
           '--out', str(out), '--bundles', str(bundles), *map(str, extra)]
    p = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    return p, out, bundles

def test_all35_metadata_positive_and_typed_holds(tmp_path):
    p, out, bundles = run(tmp_path)
    assert p.returncode == 0, p.stderr
    d = json.loads(out.read_text())
    assert d['source_count'] == 35
    assert d['metadata_bundles_validated'] == 35
    assert d['q2_executable_bundles'] == 0
    assert d['q2_held_bundles'] == 35
    assert d['witness_config_loaded'] == 'SRC04'
    assert d['sourcefree_transfer_example'] == 'SRC01'
    assert len(json.loads((bundles/'SRC04.json').read_text())['accepted_c11_reference']['semantic_release_hash']) == 64
    assert json.loads((bundles/'SRC01.json').read_text())['sourcefree_fixture']['status'].startswith('SOURCEFREE_FIXTURE_PIN_ONLY')
    assert all(json.loads((bundles/f'SRC{i:02d}.json').read_text())['original_source_bodies_read'] is False for i in range(1,36))

def test_codebook_hash_drift_refused(tmp_path):
    m = json.loads(MATRIX.read_text()); m['sources'][0]['custody_refs']['codebook_sha256'] = '0'*64
    matrix = tmp_path/'matrix.json'; matrix.write_text(json.dumps(m))
    out=tmp_path/'out.json'; bundles=tmp_path/'bundles'
    p=subprocess.run([sys.executable,'-B',str(PRODUCER),'--matrix',str(matrix),'--out',str(out),'--bundles',str(bundles)],cwd=str(ROOT),text=True,capture_output=True)
    assert p.returncode != 0
    assert 'CODEBOOK_HASH_NOT_FOUND' in p.stderr

def test_data_path_drift_refused(tmp_path):
    m=json.loads(MATRIX.read_text()); m['sources'][0]['host_custody']['artifact_relpath']='Data/DOES_NOT_EXIST.sav'
    matrix=tmp_path/'matrix.json'; matrix.write_text(json.dumps(m)); out=tmp_path/'out.json'; bundles=tmp_path/'bundles'
    p=subprocess.run([sys.executable,'-B',str(PRODUCER),'--matrix',str(matrix),'--out',str(out),'--bundles',str(bundles)],cwd=str(ROOT),text=True,capture_output=True)
    assert p.returncode != 0
    assert 'DATA_PATH_MISSING' in p.stderr

def test_src04_config_drift_refused(tmp_path):
    bad=tmp_path/'bad.config.json'; bad.write_text('{}')
    out=tmp_path/'out.json'; bundles=tmp_path/'bundles'
    p=subprocess.run([sys.executable,'-B',str(PRODUCER),'--src04-config',str(bad),'--out',str(out),'--bundles',str(bundles)],cwd=str(ROOT),text=True,capture_output=True)
    assert p.returncode != 0
    assert 'SRC04_CONFIG_FILE_DRIFT' in p.stderr


def test_src17_source_read_c11_authorized_but_i03_i05_held(tmp_path):
    p, out, bundles = run(tmp_path)
    assert p.returncode == 0, p.stderr
    d = json.loads((bundles/'SRC17.json').read_text())
    assert d['rights_decision'] == 'AUTHORIZED_FOR_THIS_HOST_PURPOSE'
    assert d['q2_input_status'] == 'HELD'
    assert d['metadata_bundle_status'].startswith('SOURCE_READ_C11_AUTHORIZED')
    assert any('I03/I05' in x for x in d['missing_q2_inputs'])
