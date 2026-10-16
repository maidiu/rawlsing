"""Separate execution root, original packet untouched; complete pinned native tree."""
from pathlib import Path
import shutil,subprocess,sys,json,hashlib
R=Path(__file__).resolve().parents[1];P=R/'runtime/pv3';C=R/'runtime/court'
if C.exists():raise SystemExit('EXISTING_COURT_REFUSED')
C.mkdir()
for name in ['repro','tests','authority']:shutil.copytree(P/name,C/name)
(C/'observations').mkdir()
p=subprocess.run([sys.executable,str(C/'repro/stage.py')],capture_output=True,text=True)
(R/'evidence').mkdir(exist_ok=True);(R/'evidence/staging.stdout').write_text(p.stdout+p.stderr)
assert p.returncode==0,(p.returncode,p.stderr)
manifest=json.loads((C/'source_selector.json').read_text());assert len(manifest['files'])==74
for row in manifest['files']:
 b=(C/'runtime_root'/row['staged_path']).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_sha1']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
(R/'native_74_source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
# Candidate source and original tests/installer byte custody, before new execution.
for name in ['repro','tests','authority']:
 for p in (P/name).rglob('*'):
  if p.is_file():assert p.read_bytes()==(C/p.relative_to(P)).read_bytes()
print('ACTUAL 74 pinned files staged; original PV3/installer/test bytes verified; trusted fixture owner provisioned')
