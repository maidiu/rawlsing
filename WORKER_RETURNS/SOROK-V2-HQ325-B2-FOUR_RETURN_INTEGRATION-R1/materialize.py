"""Materialize exact commissioned Git blobs; never regenerate/patch inherited fixtures."""
from pathlib import Path
import hashlib, json, subprocess, tarfile
ROOT=Path(__file__).resolve().parent
PINS={
'B1':('c0f4588c158b40c8903b4aae2f292eae5238b8a0','SOROK-V2-HQ324-B1-COUPLED-DEVELOPMENT-R1'),
'P1':('fb4fa049b6e3dd9df8d25a4f42a2b41e9d737c60','SOROK-V2-HQ324-P1-PROPOSAL-ADMISSION-R1'),
'D1':('2e3f3e48293bdcd5774b9465909f16d537e48e35','SOROK-V2-HQ324-D1-DEVELOPMENTAL-SCIENCE-R1'),
'F1':('ed367d96af66d816a01dd651b91f0af285762c82','SOROK-V2-HQ324-F1-INDEPENDENT-DEVELOPMENTAL-FALSIFIERS-R1')}
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT.parent.parent)
def materialize():
    manifest=[]
    for label,(sha,tree) in PINS.items():
        subprocess.run(['git','cat-file','-e',sha+'^{commit}'],cwd=ROOT.parent.parent,check=True)
        prefix='WORKER_RETURNS/'+tree+'/'
        for row in git('ls-tree','-r',sha,prefix).decode().splitlines():
            metadata,path=row.split('\t'); blob=metadata.split()[2]
            data=git('show',sha+':'+path)
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
            target=ROOT/'imports'/label/path.removeprefix(prefix)
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists(): assert target.read_bytes()==data, target
            else: target.write_bytes(data)
            manifest.append(dict(component=label,commit=sha,source_path=path,git_blob_sha1=blob,
                sha256=hashlib.sha256(data).hexdigest(),materialized_path=str(target.relative_to(ROOT))))
    archive=ROOT/'imports/F1/F1_frozen_court.tar.gz'
    dest=ROOT/'imports/F1/court';dest.mkdir(exist_ok=True)
    with tarfile.open(archive) as tar:
        for item in tar.getmembers():
            assert not item.issym() and not item.islnk()
            path=dest/item.name
            assert path.resolve().is_relative_to(dest.resolve())
            if item.isfile():
                data=tar.extractfile(item).read()
                path.parent.mkdir(parents=True,exist_ok=True)
                if path.exists(): assert path.read_bytes()==data,path
                else: path.write_bytes(data)
                manifest.append(dict(component='F1_ARCHIVE_MEMBER',archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                    archive_member=item.name,materialized_path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(data).hexdigest()))
    (ROOT/'imported_sources.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Verified and materialized',len(manifest),'exact files/archive members')
if __name__=='__main__': materialize()
