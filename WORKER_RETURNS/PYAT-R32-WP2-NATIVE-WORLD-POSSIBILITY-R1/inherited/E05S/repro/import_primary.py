"""Reconstruct exact pinned primary evidence, verifying Git NUL preimages."""
import pathlib,json,subprocess,hashlib
R=pathlib.Path(__file__).resolve().parents[1]
for row in json.loads((R/'primary_input_manifest.json').read_text()):
 b=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=R)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 p=R/row['local'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
print('Verified exact primary inputs')
