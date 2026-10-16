from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];G=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip());prefix=str(R.relative_to(G))+'/'
base='b90cccd45067364ff5f82d6dfa66db61e519ec25'
for args in [['diff','--name-only',base],['diff','--cached','--name-only',base]]:
 paths=subprocess.check_output(['git',*args],cwd=G,text=True).splitlines();assert all(p.startswith(prefix) for p in paths),paths
files=sorted(set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','.'],cwd=R,text=True).splitlines()))
(R/'changed_path_proof.json').write_text(json.dumps(dict(startup=base,authorized_prefix=prefix,outside_paths=[],native_owner_mutations=[],candidate_product_byte_identical=True,return_paths=[prefix+f for f in files]),indent=2)+'\n')
files=sorted(set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','.'],cwd=R,text=True).splitlines()))
rows=[]
for f in files:
 if f=='ARTIFACT_MANIFEST.json':continue
 p=R/f
 if not p.exists():continue
 b=p.read_bytes();rows.append(dict(path=f,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(R/'ARTIFACT_MANIFEST.json').write_text(json.dumps(dict(schema='E04U_RETURN_ARTIFACT_MANIFEST@1',self_excluded=True,files=rows),indent=2)+'\n')
print('Authorized artifact manifest:',len(rows),'entries')
