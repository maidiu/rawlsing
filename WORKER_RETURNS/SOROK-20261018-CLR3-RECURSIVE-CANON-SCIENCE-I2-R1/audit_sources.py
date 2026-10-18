"""Audit exact published code, selected source bytes and qualified lineage."""
import argparse,hashlib,json,zipfile
from collections import Counter
from pathlib import Path
from reconstruct import ROOT,TARGET,CLR,git

def sha(data):return hashlib.sha256(data).hexdigest()
def blobsha(data):return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def audit(archive):
    target=ROOT/'reconstructed/clr3'
    inv=json.loads((target/'sources/legacy_source_inventory.json').read_text())
    td=json.loads((target/'sources/TD_R05_source_manifest.json').read_text())
    tdrows={r['path']:r for r in td['selected_sources']}
    originals=json.loads((ROOT/'evidence/reconstruction_manifest.json').read_text())
    for row in originals:
        data=(ROOT/row['local_path']).read_bytes()
        assert sha(data)==row['sha256'] and blobsha(data)==row['blob_sha1'],row['path']
    authority=json.loads((ROOT/'evidence/authority_manifest.json').read_text())['files']
    upstream=[r for r in authority if r['path'].endswith('LATEST_EXTANT_V3_V2_SOURCE_MANIFEST.json')][0]
    assert (ROOT/upstream['local_path']).read_bytes()==(target/'sources/TD_R05_source_manifest.json').read_bytes()
    rows=[]
    with zipfile.ZipFile(archive) as z:
        prefix='Rawlsing_code_bundle_staging/'
        selected=[]
        for r in td['selected_sources']:
            data=z.read(prefix+r['path'])
            assert sha(data)==r['sha256'] and len(data)==r['bytes'],r['path']
            # Selected code/doc files only, never extract the archive or data.
            dest=ROOT/'sources/selected_archive_members'/r['path']
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
            dup=prefix+'rawlsing_essentials_bundle/'+r['path']
            duplicate=sha(z.read(dup)) if dup in z.namelist() else None
            selected.append(dict(**r,archive_member=prefix+r['path'],match=True,duplicate_sha256=duplicate,duplicate_matches=duplicate==r['sha256'],local_path=str(dest.relative_to(ROOT)),used_for_runtime=False))
        for r in inv['files']:
            data=(target/'sources/legacy'/r['path']).read_bytes()
            gitblob=git('rev-parse',TARGET+':'+CLR+'sources/legacy/'+r['path']).decode().strip()
            assert len(data)==r['bytes'] and sha(data)==r['sha256'] and blobsha(data)==gitblob==r['materialized_git_blob_sha1'],r['path']
            assert z.read(prefix+r['path'])==data,r['path']
            if r['path'] in tdrows:assert sha(data)==tdrows[r['path']]['sha256']
            rows.append(dict(**r,git_blob_verified=True,archive_top_family_byte_match=True,historical_admission='TD_R05_SELECTED_MEMBER_BYTES_ONLY' if r['path'] in tdrows else 'CLR3_LOCAL_PIN_ONLY_NOT_HISTORICALLY_ADMITTED'))
        archive_sha=sha(archive.read_bytes())
        archive_info=dict(archive_alias='local-sourcefree-code-bundle',bytes=archive.stat().st_size,entries=len(z.infolist()),expected_sha256=td['archive_sha256'],observed_sha256=archive_sha,container_match=archive_sha==td['archive_sha256'],matches_author_observed=archive_sha==inv['source_archive_sha256'])
    # The preserved tests, harness, world source match their published R1 preimages.
    preserved=json.loads((target/'preserved/manifest.json').read_text())
    for r in preserved:assert sha((target/r['local_path']).read_bytes())==r['sha256']
    result=dict(target=TARGET,archive=archive_info,selected_count=len(selected),selected=selected,runtime_file_count=len(rows),runtime_bytes=sum(r['bytes'] for r in rows),custody_counts=dict(Counter(r['custody'] for r in rows)),runtime=rows,preserved=preserved,independent_judgment='Exact published closure reconstructs and all source member hashes match. Whole archive lineage remains HOLD; 49 dependency pins are not historical admission.')
    (ROOT/'evidence/source_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['archive','selected_count','runtime_file_count','runtime_bytes','custody_counts']}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path);audit(p.parse_args().archive)
