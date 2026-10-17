"""Recover exact inherited source bytes within the authorized worker return."""
import subprocess,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parents[1]
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
refs=json.loads((OUT/'discovery/refs.json').read_text())
manifest=[]
def stage(ref,src,dst):
 data=git('show',f'{ref}:{src}'); target=OUT/dst; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
 manifest.append(dict(commit=ref,source=src,path=str(target.relative_to(OUT)),blob=git('rev-parse',f'{ref}:{src}').decode().strip(),sha256=hashlib.sha256(data).hexdigest()))
# Full canonical Python package as an immutable local import closure; no canonical edits.
base='5940793fbf87373dccd99dbc95973785a2b85aee'
for src in git('ls-tree','-r','--name-only',base,'rawlsing_next').decode().splitlines():
 if src.endswith('.py'): stage(base,src,'native/'+src)
for name,ref in refs.items():
 paths=(OUT/'discovery'/f'{name}_tree.txt').read_text().splitlines()
 for src in paths:
  keep=False
  if name in ('I01','PE2') and src.startswith('rawlsing_next/') and src.endswith('.py'):
   # Recover full worker-only source/test differences, leaving canonical owner bytes intact.
   try: same=git('rev-parse',f'{base}:{src}')==git('rev-parse',f'{ref}:{src}')
   except subprocess.CalledProcessError: same=False
   if not same: stage(ref,src,f'inherited/{name}/'+src)
  tags={'E05R':'R13-E05R','E05S':'R14-E05S','W10':'HQ295-W10','I01':'HQ287-I01','PE2':'PE2-GENERIC','F6M':'R29-F6M','F6N':'R29-F6N','GF1G':'R29-GF1G'}
  if src.startswith('WORKER_RETURNS/') and tags[name] in src:
   tail=src.split('/',2)[2]
   if name in ('E05R','E05S','W10'): keep=src.endswith(('.py','.md','.json')) and not any(x in tail for x in ['evidence/','native/'])
   elif name in ('I01','PE2','GF1G'): keep=tail.endswith('.md') and '/' not in tail
   elif name=='F6M': keep=tail.startswith(('candidate/','tests/')) or tail in ('00_IMPLEMENTATION_RESULT.md','03_CONSUMER_RIGHTS_AND_TRANSPORT.md') or tail.endswith('f6c_worlds.py') and 'F6C_AUTHOR' in tail
   elif name=='F6N': keep=tail in ('00_I2_VERDICT.md','03_METHOD_CEILING.md','04_F6N_PHASE_B_REVIEW.md') or tail.startswith('02_PHASE_A/03_SCRIPTS/') or tail.startswith('02_PHASE_A/04_TESTS/')
   if keep: stage(ref,src,f'inherited/{name}/'+tail)
(OUT/'discovery/staged_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(len(manifest),'exact source objects staged')
