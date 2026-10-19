"""Independent Git/source/container audit. No extraction of unrelated archive data."""
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile,difflib
R=Path(__file__).resolve().parent;F=R/'frozen';C=F/'reconstructed/clr3'
BASE='68873526efe5a39a0849aa401666ac997870f156'
TARGET='de9a525c362bf58dbb620fcd7db336a4734e7db8'
ORIGINAL='4076dcc7c944723b8eea449c0753e535b79d1aa5'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(name,obj):(R/'evidence'/name).write_text(json.dumps(obj,indent=2)+'\n')
def main(archive):
    staging=json.loads((R/'staging_manifest.json').read_text())
    for row in staging:
        data=(R/row['staged']).read_bytes()
        assert sha(data)==row['sha256'] and blob(data)==row['blob_sha1']
        assert git('show',row['commit']+':'+row['path'])==data
    reconstruct=json.loads((F/'evidence/reconstruction_manifest.json').read_text())
    for row in reconstruct:
        data=(F/row['local_path']).read_bytes()
        assert data==git('show',row['commit']+':'+row['path'])
        assert sha(data)==row['sha256'] and blob(data)==row['blob_sha1']
    td=json.loads((C/'sources/TD_R05_source_manifest.json').read_text());tdmap={x['path']:x for x in td['selected_sources']}
    inventory=json.loads((C/'sources/legacy_source_inventory.json').read_text())
    prefix='Rawlsing_code_bundle_staging/';selected=[];runtime=[]
    with zipfile.ZipFile(archive) as z:
        for row in td['selected_sources']:
            data=z.read(prefix+row['path']);staged=F/'sources/selected_archive_members'/row['path']
            assert sha(data)==row['sha256'] and len(data)==row['bytes'] and staged.read_bytes()==data
            alternate=prefix+'rawlsing_essentials_bundle/'+row['path']
            selected.append(dict(**row,member=prefix+row['path'],blob_sha1=blob(data),local='frozen/sources/selected_archive_members/'+row['path'],verified=True,alternate_matches=alternate in z.namelist() and sha(z.read(alternate))==row['sha256']))
        for row in inventory['files']:
            data=(C/'sources/legacy'/row['path']).read_bytes()
            original_path='WORKER_RETURNS/SOROK-20261018-CLR3-RECURSIVE-FORMATION-CANON-COURT-R1/sources/legacy/'+row['path']
            assert data==git('show',ORIGINAL+':'+original_path)==z.read(prefix+row['path'])
            assert len(data)==row['bytes'] and sha(data)==row['sha256'] and blob(data)==row['materialized_git_blob_sha1']
            historical=row['path'] in tdmap
            if historical:assert sha(data)==tdmap[row['path']]['sha256']
            runtime.append(dict(**row,commit=ORIGINAL,source_path=original_path,blob_sha1=blob(data),historical_grade='TD_R05_MEMBER_MATCH_ONLY' if historical else 'LOCAL_PIN_ONLY_UNQUALIFIED_HISTORICALLY'))
        container=dict(alias='available-sourcefree-code-archive',bytes=archive.stat().st_size,entries=len(z.infolist()),expected_sha256=td['archive_sha256'],observed_sha256=sha(archive.read_bytes()),historical_container_disposition='HOLD')
        container['container_match']=container['expected_sha256']==container['observed_sha256']
    # Independently dereference every authority pin; compare current commission-base content.
    authorities=[]
    for row in json.loads((F/'evidence/authority_manifest.json').read_text())['files']:
        data=git('show',row['commit']+':'+row['path']);assert data==(F/row['local_path']).read_bytes()
        assert sha(data)==row['sha256'] and blob(data)==row['blob_sha1']
        current=subprocess.run(['git','show',BASE+':'+row['path']],cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        dest=R/'authority'/row['local_path'].removeprefix('authority/')
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
        authorities.append(dict(**row,review_local=str(dest.relative_to(R)),commission_base=BASE,base_exists=current.returncode==0,base_blob_sha1=blob(current.stdout) if current.returncode==0 else None,base_identical=current.stdout==data if current.returncode==0 else None))
    # Exact patch reconstruction, excluding the patch's documentary filename labels.
    old=(C/'recursive_court.py').read_text();new=(F/'repair_r1/candidate/recursive_court.py').read_text()
    patch=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='frozen_clr3/recursive_court.py',tofile='repair_r1/candidate/recursive_court.py'))
    assert patch==(F/'repair_r1/candidate.patch').read_text()
    summary=dict(staging_blobs=len(staging),original_reconstruction_blobs=len(reconstruct),container=container,selected_count=len(selected),selected=selected,runtime_file_count=len(runtime),runtime_bytes=sum(x['bytes'] for x in runtime),historical_matched_runtime=sum(x['historical_grade']=='TD_R05_MEMBER_MATCH_ONLY' for x in runtime),local_only_runtime=sum(x['historical_grade']=='LOCAL_PIN_ONLY_UNQUALIFIED_HISTORICALLY' for x in runtime),runtime=runtime,patch_exact=True,patch_sha256=sha(patch.encode()),frozen_sources_unchanged=True)
    dump('source_audit.json',summary);dump('authority_audit.json',authorities)
    print(json.dumps({k:summary[k] for k in ('staging_blobs','original_reconstruction_blobs','container','selected_count','runtime_file_count','runtime_bytes','historical_matched_runtime','local_only_runtime','patch_exact')}))
if __name__=='__main__':main(Path(sys.argv[1]))
