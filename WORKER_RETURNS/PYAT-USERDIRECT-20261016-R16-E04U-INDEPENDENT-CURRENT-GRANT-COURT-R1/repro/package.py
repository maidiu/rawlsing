"""Return-only publication inventory; excludes its own recursive digest."""
import pathlib,json,subprocess,hashlib
R=pathlib.Path(__file__).resolve().parents[1];G=pathlib.Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip());prefix=str(R.relative_to(G))+'/'
base='0d551d36ff19dc9806e0ad490ff33a1e4c25e381'
for name in ['CHANGED_PATH_PROOF.json','ARTIFACT_MANIFEST.json']:
 p=R/name
 if not p.exists():p.write_text('{}\n')
files=sorted(set(subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','.'],cwd=R,text=True).splitlines()))
paths=[prefix+f for f in files]
assert all(p.startswith(prefix) for p in paths)
elsewhere=subprocess.check_output(['git','diff','--cached','--name-only',base],cwd=G,text=True).splitlines();assert all(p.startswith(prefix) for p in elsewhere)
(R/'CHANGED_PATH_PROOF.json').write_text(json.dumps(dict(base=base,authorized_prefix=prefix,all_return_paths=paths,path_count=len(paths),outside_owned_paths=[],accepted_native_owner_edits=[],product_delta='Only product/empirical.py differs from E04R',generated_log_whitespace='Captured stdout preserves final blank lines. Source whitespace check uses core.whitespace=-blank-at-eof.'),indent=2)+'\n')
rows=[]
for local in files:
 if local=='ARTIFACT_MANIFEST.json':continue
 b=(R/local).read_bytes();rows.append(dict(path=local,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(R/'ARTIFACT_MANIFEST.json').write_text(json.dumps(dict(schema='E04T_RETURN_ARTIFACT_MANIFEST@1',self_excluded=True,files=rows),indent=2)+'\n')
print('PACKAGED',len(files),'owned return files; no outside staged paths')
