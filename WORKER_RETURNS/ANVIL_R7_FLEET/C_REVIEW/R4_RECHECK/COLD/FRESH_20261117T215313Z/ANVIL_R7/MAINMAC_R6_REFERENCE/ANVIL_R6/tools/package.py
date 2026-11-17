#!/usr/bin/env python3
"""Create reproducible ANVIL R6 archive and verify complete manifest against ZIP bytes."""
import hashlib,json,pathlib,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'ANVIL_R6_FINAL.zip'
paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name not in ('.DS_Store','MANIFEST.json') and not p.suffix=='.pyc')
manifest={'schema':'ANVIL_R6_MANIFEST_1','project':'ANVIL R6 local authored, not launched nor received','files':{p.relative_to(ROOT).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in paths}}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
with zipfile.ZipFile(OUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in paths+[ROOT/'MANIFEST.json']:
  name='ANVIL_R6/'+p.relative_to(ROOT).as_posix();info=zipfile.ZipInfo(name,date_time=(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
  z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(OUT) as z:
 got=set(z.namelist());expected={'ANVIL_R6/'+k for k in manifest['files']}|{'ANVIL_R6/MANIFEST.json'}
 assert got==expected,(got-expected,expected-got)
 internal=json.loads(z.read('ANVIL_R6/MANIFEST.json'))
 assert internal==manifest
 for name,x in internal['files'].items():
  b=z.read('ANVIL_R6/'+name)
  assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],name
print(json.dumps({'archive':str(OUT),'files':len(manifest['files']),'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'integrity':'PASS_ALL_PAYLOADS','grade':'LOCAL_ARTIFACT_ONLY_NOT_SCIENCE_OR_INDEPENDENT_RECEIVING'},indent=2))
