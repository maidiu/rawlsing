from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
for x in json.loads((ROOT/'native_source_manifest.json').read_text()):
 b=subprocess.check_output(['git','-c','gc.auto=0','show',x['commit']+':'+x['path']],cwd=ROOT)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
 assert hashlib.sha256(b).hexdigest()==x['sha256']
 p=ROOT/'inherited_e05a/runtime'/x['local'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('401 exact native blobs verified')
