"""Reuse the accepted E05S exact closure; do not rerun its completed court."""
from pathlib import Path
import subprocess,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];REPO=R.parents[1];RT=R/'runtime';RT.mkdir(exist_ok=True)
m=json.loads((R/'inputs/E05S/source_manifest.json').read_text());assert len(m)==401
for x in m:
 b=subprocess.check_output(['git','-c','gc.auto=0','show',x['commit']+':'+x['path']],cwd=REPO)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 assert hashlib.sha256(b).hexdigest()==x['sha256']
 p=RT/x['local'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
(R/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=R/'frozen_E05S';f.mkdir(exist_ok=True)
for p in (R/'inputs/E05S/tests').glob('*.py'):
 d=f/'tests'/p.name;d.parent.mkdir(exist_ok=True);shutil.copyfile(p,d)
for p in (R/'inputs/E05S/observations').glob('*.xml'):
 d=f/'junit'/p.name;d.parent.mkdir(exist_ok=True);shutil.copyfile(p,d)
for n in ['01_FROZEN_REQUEST_WORLD_NATIVE_ORACLE.json','01_FREEZE_SHA256.txt','01_FROZEN_NATIVE_DEPENDENCY_IDENTITIES.json']:
 shutil.copyfile(R/'inputs/E05S'/n,f/n)
print('Verified and staged accepted E05S closure',len(m),'Git objects; preserved court sources/JUnit, NOT rerun')
