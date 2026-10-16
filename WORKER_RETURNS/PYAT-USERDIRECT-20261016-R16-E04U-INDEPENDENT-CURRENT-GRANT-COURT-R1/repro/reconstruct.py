"""Reconstruct ignored pinned evidence, then use the unchanged E04T source stage."""
from pathlib import Path
import subprocess,json,hashlib,sys
R=Path(__file__).resolve().parents[1]
for row in json.loads((R/'input_manifest.json').read_text()):
 b=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=R)
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
 p=R/row['local'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():assert p.read_bytes()==b
 else:p.write_bytes(b)
subprocess.run([sys.executable,str(R/'repro/stage.py')],cwd=R,check=True)
