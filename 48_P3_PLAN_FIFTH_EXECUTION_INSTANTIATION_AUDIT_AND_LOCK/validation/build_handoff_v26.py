from __future__ import annotations
from pathlib import Path
import argparse,zipfile,shutil,csv,hashlib,subprocess,sys,os,json

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def write_manifest(root:Path,path:Path,excluded:set[Path]):
    rows=[]
    for p in sorted(root.rglob('*')):
        if p.is_file() and p not in excluded:
            rows.append({'relative_path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)})
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256'],lineterminator='\n');w.writeheader();w.writerows(rows)

def main():
    ap=argparse.ArgumentParser(description='Rebuild the v26 cumulative tree from the accepted v25 ZIP plus the delivered v26 contract section and mutable controls.')
    ap.add_argument('--source-v25-zip',required=True)
    ap.add_argument('--output-root',required=True)
    ap.add_argument('--skip-verify',action='store_true')
    a=ap.parse_args()
    source=Path(a.source_v25_zip).resolve();out=Path(a.output_root).resolve()
    section=Path(__file__).resolve().parents[1];current_root=section.parents[0]
    if hashlib.sha256(source.read_bytes()).hexdigest()!='29448f6a7e800288ca08796003a4b78680a7817aa0f6d40c293b488a95659c03':
        raise SystemExit('source v25 ZIP hash mismatch')
    if out.exists():shutil.rmtree(out)
    tmp=out.parent/(out.name+'_extract_tmp')
    if tmp.exists():shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    with zipfile.ZipFile(source) as z:
        if z.testzip():raise SystemExit('source ZIP integrity failure')
        z.extractall(tmp)
    roots=[p for p in tmp.iterdir() if p.is_dir()]
    if len(roots)!=1:raise SystemExit(f'expected one extracted root, got {roots}')
    shutil.move(str(roots[0]),str(out));shutil.rmtree(tmp)
    # Generated test/cache debris is not substantive inherited payload.
    for d in list(out.rglob('__pycache__'))+list(out.rglob('.pytest_cache')):shutil.rmtree(d,ignore_errors=True)
    for f in out.rglob('*.pyc'):f.unlink(missing_ok=True)
    # Add governing v26 section.
    dst=out/'48_P3_PLAN_FIFTH_EXECUTION_INSTANTIATION_AUDIT_AND_LOCK'
    if dst.exists():shutil.rmtree(dst)
    shutil.copytree(section,dst,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','*.pyc'))
    # Replace mutable restart/release controls with the accepted v26 controls.
    controls=[
      '00_START_HERE/CURRENT_STATE.json','00_START_HERE/EXACT_RESUME_POINT.md','00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt',
      '00_START_HERE/README_FIRST.md','00_START_HERE/MASTER_HANDOFF.md','00_START_HERE/SCOPE_LOCK.json',
      '00_START_HERE/Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v26_20260801.docx',
      'MASTER_HANDOFF.md','README_FIRST.md','VALIDATION.json']
    for rel in controls:
        src=current_root/rel
        if not src.exists():raise SystemExit(f'missing accepted control {rel}')
        dest=out/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    # Regenerate release manifests from the assembled tree.
    for p in [out/'PACKAGE_INDEX.csv',out/'SHA256SUMS.csv',dst/'SECTION_MANIFEST.csv']:
        p.unlink(missing_ok=True)
    write_manifest(dst,dst/'SECTION_MANIFEST.csv',{dst/'SECTION_MANIFEST.csv'})
    exclusions={out/'PACKAGE_INDEX.csv',out/'SHA256SUMS.csv'}
    write_manifest(out,out/'PACKAGE_INDEX.csv',exclusions)
    shutil.copy2(out/'PACKAGE_INDEX.csv',out/'SHA256SUMS.csv')
    if not a.skip_verify:
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
        subprocess.run([sys.executable,str(dst/'validation/verify_handoff_v26.py'),str(out)],check=True,env=env)
    print(out)
if __name__=='__main__':main()
