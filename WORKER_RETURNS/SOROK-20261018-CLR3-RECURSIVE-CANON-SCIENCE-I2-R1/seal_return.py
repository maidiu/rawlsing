"""Hash the portable reviewer return; dependencies/caches remain local."""
import hashlib,json
from reconstruct import ROOT,START,TARGET,PRIOR

excluded={'return_manifest.json','SHA256SUMS'}
files=[]
for p in sorted(ROOT.rglob('*')):
    rel=p.relative_to(ROOT)
    if not p.is_file() or str(rel) in excluded or any(s in {'.runtime','__pycache__','.pytest_cache'} for s in rel.parts) or p.suffix=='.pyc':continue
    data=p.read_bytes()
    files.append(dict(path=str(rel),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
manifest=dict(schema='CLR3_INDEPENDENT_I2_RETURN_MANIFEST_R1',sealed_startup=START,review_target=TARGET,prior=PRIOR,write_only='WORKER_RETURNS/SOROK-20261018-CLR3-RECURSIVE-CANON-SCIENCE-I2-R1/',file_count=len(files),files=files,excluded=['ignored runtime packages and caches','manifest/checksum self hashes'],publication='ordinary non-force push of commissioned branch; exact final commit/readback delivered separately; any committed checkpoint readback is explicitly named')
(ROOT/'return_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'SHA256SUMS').write_text(''.join(r['sha256']+'  '+r['path']+'\n' for r in files))
print('Sealed',len(files),'portable files;',sum(r['bytes'] for r in files),'bytes')
