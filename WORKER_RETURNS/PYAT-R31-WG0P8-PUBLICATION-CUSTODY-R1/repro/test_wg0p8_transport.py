import hashlib, importlib.util, json, pathlib, subprocess
import pytest

spec=importlib.util.spec_from_file_location('p8',pathlib.Path(__file__).with_name('wg0p8_publication.py'))
p8=importlib.util.module_from_spec(spec);spec.loader.exec_module(p8)

def row(path,raw):
    return dict(staged_path=path,source_path='historical/'+path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob_sha1=p8.git_blob(raw))

@pytest.fixture()
def setup_fixture(tmp_path,monkeypatch):
    root=tmp_path; c=root/'candidate'; c.mkdir(); (root/'repro').mkdir(); (root/'repro'/'wg0p8_publication.py').write_text('synthetic-only')
    subprocess.run(['git','init','-q',str(root)],check=True)
    repaired=b'SYNTHETIC_P5_ONLY'; direct=b'SYNTHETIC_UNREPAIRED'
    paths=[f'court/test_only/f{i:03d}.json' for i in range(185)]+[p8.REPAIRED,p8.DIRECT]
    data=[repaired if x==p8.REPAIRED else direct if x==p8.DIRECT else f'{{"synthetic":{i}}}'.encode() for i,x in enumerate(paths)]
    rows=[row(x,b) for x,b in zip(paths,data)]
    for x,b in zip(paths,data):
        f=c/x;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    rp=next(x for x in rows if x['staged_path']==p8.REPAIRED);rp['source_path']=p8.EXPECTED_MODULE_SOURCE
    (c/'SOURCE_INPUTS.json').write_text(json.dumps(dict(files=rows)))
    (c/'CANDIDATE_CODE_PIN.json').write_text(json.dumps(dict(files=[rp])))
    subprocess.run(['git','-C',str(root),'add','.'],check=True)
    monkeypatch.setattr(p8,'ROOT',root);monkeypatch.setattr(p8,'C',c);monkeypatch.setattr(p8,'COURT',c/'court')
    monkeypatch.setattr(p8,'EXPECTED_P5',rp['sha256']);monkeypatch.setattr(p8,'EXPECTED_BLOB',rp['git_blob_sha1'])
    return c,rows,rp

def test_clean_synthetic_custody(setup_fixture):
    assert p8.verify()['input_count']==187

def test_missing_observation_refused(setup_fixture):
    c,rows,_=setup_fixture;(c/rows[0]['staged_path']).unlink()
    with pytest.raises(RuntimeError,match='MISSING_OR_SYMLINK'):p8.verify()

def test_modified_observation_refused(setup_fixture):
    c,rows,_=setup_fixture;(c/rows[0]['staged_path']).write_text('FORGED')
    with pytest.raises(RuntimeError,match='HASH_OR_BLOB_CHANGED'):p8.verify()

def test_stale_manifest_alias_refused(setup_fixture):
    c,rows,rp=setup_fixture; rp['sha256']='06fadc7eb8c01fa832fa59beccfc2ea2f6e068216fdc8b04c95365065d492723'
    (c/'SOURCE_INPUTS.json').write_text(json.dumps(dict(files=rows)))
    with pytest.raises(RuntimeError,match='STALE_SOURCE_INPUTS_OR_WRONG_MODULE'):p8.verify()

def test_wrong_direct_module_alias_refused(setup_fixture):
    c,rows,rp=setup_fixture;rp['staged_path']='court/runtime_phase_b/candidate/repro/alternate_wrong.py'
    (c/'SOURCE_INPUTS.json').write_text(json.dumps(dict(files=rows)))
    with pytest.raises(RuntimeError,match='P5_MODULE_ALIAS_ABSENT_OR_AMBIGUOUS'):p8.verify()

def test_duplicate_manifest_alias_refused(setup_fixture):
    c,rows,_=setup_fixture;rows[-1]=rows[0].copy()
    (c/'SOURCE_INPUTS.json').write_text(json.dumps(dict(files=rows)))
    with pytest.raises(RuntimeError,match='COUNT_OR_DUPLICATION'):p8.verify()

def test_symlink_refused(setup_fixture):
    c,rows,_=setup_fixture; p=c/rows[1]['staged_path'];p.unlink();p.symlink_to(c/rows[0]['staged_path'])
    with pytest.raises(RuntimeError,match='MISSING_OR_SYMLINK'):p8.verify()

def test_bad_codepin_refused(setup_fixture):
    c,rows,rp=setup_fixture;bad=rp.copy();bad['sha256']='0'*64
    (c/'CANDIDATE_CODE_PIN.json').write_text(json.dumps(dict(files=[bad])))
    with pytest.raises(RuntimeError,match='HASH_OR_BLOB_CHANGED'):p8.verify()

def test_path_escape_refused(setup_fixture):
    c,rows,_=setup_fixture;rows[0]['staged_path']='../outside.txt'
    (c/'SOURCE_INPUTS.json').write_text(json.dumps(dict(files=rows)))
    with pytest.raises(RuntimeError,match='SOURCE_PATH_ESCAPE'):p8.verify()
