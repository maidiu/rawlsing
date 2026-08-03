from __future__ import annotations
from pathlib import Path
import argparse, hashlib, zipfile, shutil, csv
SOURCE_SHA='872cbff62dc03f964d0f09b8b2f545126700899e1377c4aa426f9827560d1fae'
ROOT_NAME='Rawlsing_J_Family_Authority_Strategy_Handoff_v27_20260801'
SECTION='49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK'
def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root:Path, out:Path, excluded:set[str]):
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_file():
            rel=p.relative_to(root).as_posix()
            if rel not in excluded: rows.append((rel,p.stat().st_size,sha(p)))
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['relative_path','bytes','sha256']);w.writerows(rows)
def main():
    ap=argparse.ArgumentParser(description='Rebuild cumulative Rawlsing handoff v27 from the accepted v26 ZIP and explicit v27 release overlay.')
    ap.add_argument('--source-v26-zip',required=True);ap.add_argument('--overlay-zip',default=None);ap.add_argument('--output-parent',required=True)
    a=ap.parse_args();source=Path(a.source_v26_zip).resolve();out_parent=Path(a.output_parent).resolve()
    overlay=Path(a.overlay_zip).resolve() if a.overlay_zip else Path(__file__).with_name('V27_RELEASE_OVERLAY.zip')
    if sha(source)!=SOURCE_SHA:raise SystemExit('source v26 ZIP hash mismatch')
    if not overlay.exists():raise SystemExit('v27 overlay ZIP missing')
    if out_parent.exists():out_parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(source) as z:
        bad=z.testzip()
        if bad:raise SystemExit('source ZIP corrupt: '+bad)
        names=[n for n in z.namelist() if not n.endswith('/')];old_root=names[0].split('/')[0]
        tmp=out_parent/old_root
        if tmp.exists():shutil.rmtree(tmp)
        z.extractall(out_parent)
    root=out_parent/ROOT_NAME
    old=out_parent/old_root
    if root.exists():shutil.rmtree(root)
    old.rename(root)
    with zipfile.ZipFile(overlay) as z:
        bad=z.testzip()
        if bad:raise SystemExit('overlay ZIP corrupt: '+bad)
        for info in z.infolist():
            if info.is_dir():continue
            target=root/info.filename
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(z.read(info.filename))
    overlay_dst=root/SECTION/'validation'/'V27_RELEASE_OVERLAY.zip'
    overlay_dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(overlay,overlay_dst)
    manifest(root/SECTION,root/SECTION/'SECTION_MANIFEST.csv',{'SECTION_MANIFEST.csv'})
    manifest(root,root/'PACKAGE_INDEX.csv',{'PACKAGE_INDEX.csv','SHA256SUMS.csv'})
    shutil.copy2(root/'PACKAGE_INDEX.csv',root/'SHA256SUMS.csv')
    print(root)
if __name__=='__main__':main()
