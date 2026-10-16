"""Materialize exact authorized source-free evidence, all below this return."""
from pathlib import Path
import subprocess, hashlib, json

ROOT = Path(__file__).resolve().parent
WT = ROOT.parents[1]
def git(*args):
    return subprocess.check_output(['git', '-c', 'gc.auto=0', '-C', str(WT), *args])

def main():
    manifest = []
    groups = [
        ('sgi1', '27ca1f2792a5213064c0b5ea2e27b89e8acce0c3', 'WORKER_RETURNS/SOROK-SGI1-SOURCEFREE-K11-LAB-R1'),
        ('sg', 'aec8fecc1ae2e3438ff70c44ce5ce7845d1a4829', 'WORKER_RETURNS/SOROK-PREA0-SG-GENEALOGY-CONSTRUCTION-R1'),
        ('sg_r3', 'ca031ce1d5c56b58b18727f94f41571d6dd763fb', 'WORKER_RETURNS/SOROK-R3-POSTASTRA-SG-ADP015-K11-GENEALOGY-R1'),
        ('g11', '0cb708bbfe522a6c6e359f36d99835d180d5a84d', 'WORKER_RETURNS/SOROK-R3-HQ297-GENEALOGY-K11-INDEPENDENT-COURT-R1'),
        ('astra', '3b2d9a1b644a9fa024ed1bd895b67be5c8789531', 'WORKER_RETURNS/ASTRA-R3-PREA0-PYAT-JOINT-MAXIMUM-DEPTH-WELD-R1'),
    ]
    for alias, commit, prefix in groups:
        for line in git('ls-tree', '-r', commit, prefix).decode().splitlines():
            meta, path = line.split('\t', 1)
            mode, kind, blob = meta.split()
            if kind != 'blob': continue
            # Astra: controlling final/amendment/K11 and source index only.
            if alias == 'astra' and str(Path(path).relative_to(prefix)) not in {
                'FINAL_RETURN.md', '16_CORRECTIVE_AMENDMENT_AND_GENEALOGY.md',
                '07_KILL_TEST_PROGRAM.md', 'FINAL_FREEZE_MANIFEST.json',
                'evidence/FINAL_SOURCE_INDEX.json', 'evidence/primary/ADP007.md',
                'evidence/primary/ADP015.md'}: continue
            data = git('cat-file', 'blob', blob)
            assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == blob
            dest = ROOT/'sources'/alias/Path(path).relative_to(prefix)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            manifest.append(dict(commit=commit,path=path,git_blob_sha1=blob,
                                 sha256=hashlib.sha256(data).hexdigest(),
                                 staged_path=str(dest.relative_to(ROOT))))
    for label, blob in [('ADP015','a4dab0a12102aaa0b584ef6ff4fdc9206a28d456'),
                        ('ADP020','1911352f4bd5b04dfeaa0f26930e6702998bb76d')]:
        data=git('cat-file','blob',blob)
        dest=ROOT/'sources'/'authority'/f'{label}.md'
        dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(data)
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
        manifest.append(dict(git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),
                             staged_path=str(dest.relative_to(ROOT)),commit=None,path=None))
    (ROOT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'verified_blobs':len(manifest),'scope':'source-free exact frozen evidence'}))

if __name__ == '__main__': main()
