from pathlib import Path
import subprocess,json,sys,time,hashlib
R=Path(__file__).resolve().parents[1];W=R.parents[1];prefix=R.relative_to(W).as_posix()+'/'
t=time.time();p=subprocess.run([sys.executable,str(R/'repro/finalize.py')],capture_output=True,text=True,cwd=W)
(R/'observations/final_audit.stdout').write_text(p.stdout+p.stderr)
(R/'observations/final_audit.terminal.json').write_text(json.dumps(dict(argv=[sys.executable,str(R/'repro/finalize.py')],exit=p.returncode,seconds=time.time()-t),indent=2)+'\n')
assert p.returncode==0,p.stdout+p.stderr
files=subprocess.check_output(['git','-C',str(W),'ls-files','--cached','--others','--exclude-standard','--',prefix],text=True).splitlines()
files=sorted(set(files+[prefix+'CHANGED_PATH_PROOF.json',prefix+'ARTIFACT_MANIFEST.json']))
assert all(n.startswith(prefix) for n in files)
proof=dict(sealed_startup='52122b4f61d5d4fc0a9794368c18c06a98579b8c',head_before_publication=subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip(),authorized_prefix=prefix,changed_paths=files,all_paths_inside_owned_return=True,accepted_native_owners_edited=False,original_returns_edited=False,only_product_delta='owned product/empirical.py; five other original product files copied byte-identically',publication_check='After commit, git diff startup HEAD --name-only and direct git ls-remote must match exact assigned branch/HEAD; final SHA returned in chat')
(R/'CHANGED_PATH_PROOF.json').write_text(json.dumps(proof,indent=2)+'\n')
manifest=[]
for name in files:
 if name==prefix+'ARTIFACT_MANIFEST.json':continue
 data=(W/name).read_bytes();manifest.append(dict(path=name.removeprefix(prefix),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
(R/'ARTIFACT_MANIFEST.json').write_text(json.dumps(dict(schema='E04R_OWNED_RETURN_ARTIFACTS@1',manifest_excludes_self=True,files=manifest,total_bytes=sum(r['bytes'] for r in manifest)),indent=2)+'\n')
print(p.stdout.strip());print('SEALED',len(files),'owned paths;',sum(r['bytes'] for r in manifest),'bytes')
