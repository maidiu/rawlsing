from pathlib import Path
import argparse,zipfile,shutil,csv,hashlib,json,subprocess,sys
P=argparse.ArgumentParser();P.add_argument('--source-v24-zip',default='/mnt/data/Rawlsing_J_Family_Authority_Strategy_Handoff_v24_20260731.zip');P.add_argument('--output-root',required=True);a=P.parse_args()
source=Path(a.source_v24_zip);out=Path(a.output_root).resolve();sec=Path(__file__).resolve().parents[1]
if out.exists():shutil.rmtree(out)
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(source) as z:
 roots={Path(n).parts[0] for n in z.namelist() if n and not n.startswith('__MACOSX')}
 z.extractall(out.parent/'_v25_extract')
 extracted=out.parent/'_v25_extract'/next(iter(roots))
 shutil.move(str(extracted),str(out));shutil.rmtree(out.parent/'_v25_extract')
dst=out/'47_P3_PLAN_FOURTH_IMPLEMENTATION_FALSIFICATION_AND_FINAL_LOCK'
shutil.copytree(sec,dst)
# Mutable controls are copied from the currently accepted v25 package source root adjacent to section.
srcroot=sec.parent
for rel in ['00_START_HERE/CURRENT_STATE.json','00_START_HERE/EXACT_RESUME_POINT.md','00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt','00_START_HERE/README_FIRST.md','00_START_HERE/MASTER_HANDOFF.md','00_START_HERE/SCOPE_LOCK.json','MASTER_HANDOFF.md','README_FIRST.md','VALIDATION.json']:
 p=srcroot/rel
 if p.exists():
  (out/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out/rel)
# Docs are copied as governing release artifacts.
for p in (srcroot/'00_START_HERE').glob('*v25*.docx'):shutil.copy2(p,out/'00_START_HERE'/p.name)
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root,path,exclude):
 rows=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p not in exclude:rows.append({'relative_path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sh(p)})
 with path.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['relative_path','bytes','sha256'],lineterminator='\n');w.writeheader();w.writerows(rows)
manifest(dst,dst/'SECTION_MANIFEST.csv',{dst/'SECTION_MANIFEST.csv'})
manifest(out,out/'PACKAGE_INDEX.csv',{out/'PACKAGE_INDEX.csv',out/'SHA256SUMS.csv'})
rows=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name not in {'PACKAGE_INDEX.csv','SHA256SUMS.csv'}:rows.append(f'{sh(p)}  {p.relative_to(out)}')
(out/'SHA256SUMS.csv').write_text('\n'.join(rows)+'\n')
subprocess.run([sys.executable,str(dst/'validation/verify_handoff_v25.py'),str(out)],check=True,env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'})
print(out)
