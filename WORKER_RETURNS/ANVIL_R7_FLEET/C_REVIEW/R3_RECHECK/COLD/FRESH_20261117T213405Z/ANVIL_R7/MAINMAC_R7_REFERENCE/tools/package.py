#!/usr/bin/env python3
"""Deterministic R7 zip, complete payload SHA and byte-count readback. No source/native/reviewer claim."""
import hashlib,json,pathlib,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'ANVIL_R7_FINAL.zip'
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.suffix!='.pyc' and p.name!='MANIFEST.json')
manifest={'schema':'ANVIL_R7_PACKAGE_MANIFEST_1','grade':'AUTHOR_LOCAL_STRUCTURAL_ONLY_NOT_RECEIVED','source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9',
  'files':{p.relative_to(ROOT).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':len(p.read_bytes())} for p in files}}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
OUT.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(OUT,'w') as z:
 for p in files+[ROOT/'MANIFEST.json']:
  name='ANVIL_R7/'+p.relative_to(ROOT).as_posix()
  info=zipfile.ZipInfo(name,date_time=(2026,11,17,0,0,0));info.external_attr=0o644<<16;info.compress_type=zipfile.ZIP_DEFLATED
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(OUT) as z:
 names=set(z.namelist());expected={'ANVIL_R7/'+f for f in manifest['files']}|{'ANVIL_R7/MANIFEST.json'}
 assert names==expected,(names-expected,expected-names)
 got=json.loads(z.read('ANVIL_R7/MANIFEST.json'));assert got==manifest
 for f,r in got['files'].items():
  b=z.read('ANVIL_R7/'+f);assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],f
print(json.dumps({'archive':str(OUT),'payload_count':len(files),'archive_bytes':OUT.stat().st_size,
 'archive_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'integrity':'PASS_ALL_ZIP_PAYLOADS',
 'grade':'LOCAL_AUTHORING_ONLY__INDEPENDENT_RECEIVING_PENDING'},indent=2))
