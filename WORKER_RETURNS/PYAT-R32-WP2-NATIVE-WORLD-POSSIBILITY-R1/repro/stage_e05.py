"""Exact independently reviewed selected-world closure, confined to this return."""
import json,hashlib,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parents[1]; REPO=R.parents[1]
manifest=json.loads((R/'inherited/E05R/source_manifest.json').read_text()); out=[]
for row in manifest:
 c,p=row['commit'],row['path']
 if c=='E05R_VERSIONED_WORKING_CANDIDATE': c='84485d32c0088995f8dc664dc0517b2d27f2563d';p='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R13-E05R-SELECTED-WORLD-REPAIR-R1/candidate/e05r_selected_world_adapter.py'
 data=subprocess.check_output(['git','show',c+':'+p],cwd=REPO)
 blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 assert blob==row['git_blob'],(p,blob,row['git_blob'])
 target=R/'selected'/row['local'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 out.append(dict(commit=c,source=p,path=str(target.relative_to(R)),blob=blob,sha256=hashlib.sha256(data).hexdigest()))
stg=R/'selected/_e04-candidate';(stg/'runtime_root/source').mkdir(parents=True,exist_ok=True)
for name in ['rawlsing_next','tests']:
 dest=stg/'runtime_root/source'/name
 if not dest.exists():dest.symlink_to(os.path.relpath(R/'selected'/name,dest.parent))
if not (stg/'product').exists():(stg/'product').symlink_to(os.path.relpath(R/'selected/product',stg))
(R/'discovery/selected_manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(out),'reviewed selected-world files staged')
