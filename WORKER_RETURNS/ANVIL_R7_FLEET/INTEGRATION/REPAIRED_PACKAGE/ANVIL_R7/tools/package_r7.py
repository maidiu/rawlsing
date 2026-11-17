#!/usr/bin/env python3
"""Deterministic R7 package builder + independent ZIP-byte readback.
Always run local quality and curate docs before invoking; never package cached pyc.
"""
import hashlib,json,pathlib,sys,zipfile,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'ANVIL_R7.zip'
for item in ROOT.rglob('__pycache__'):
    if item.is_dir():
        for f in item.glob('*'):f.unlink()
        item.rmdir()
files=sorted((p for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and not p.name.endswith('.pyc')),key=lambda p:p.relative_to(ROOT).as_posix())
# An old manifest may be inside a historical snapshot; retain those. Only root manifest is excluded.
# historical MANIFEST.json are permitted and are primary conservation evidence.
files=sorted((p for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'MANIFEST.json' and not p.name.endswith('.pyc')),key=lambda p:p.relative_to(ROOT).as_posix())
manifest={'schema':'ANVIL_R7_PACKAGE_MANIFEST','revision':'R7','status':'AUTHOR_LOCAL_SYNTHETIC_TESTED_NOT_DISPATCHED',
          'R5_baseline':'R5_BASELINE/MANIFEST.json','mainmac_reference':'MAINMAC_R6_REFERENCE/ANVIL_R6/MANIFEST.json',
          'entrypoint':'00_R7_READ_FIRST.md','scope':'No source-native science, real full-width host measurement, independent C or protected H1',
          'payloads':{p.relative_to(ROOT).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files}}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
allfiles=files+[ROOT/'MANIFEST.json']
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in sorted(allfiles,key=lambda p:p.relative_to(ROOT).as_posix()):
        rel=p.relative_to(ROOT).as_posix();info=zipfile.ZipInfo('ANVIL_R7/'+rel,date_time=(2026,11,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=(0o644<<16)
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=8)
with zipfile.ZipFile(DEST) as z:
    if z.testzip() is not None:raise SystemExit('ZIP_INTEGRITY_FAIL')
    names=set(z.namelist());expected={'ANVIL_R7/'+p.relative_to(ROOT).as_posix() for p in allfiles}
    if names!=expected:raise SystemExit('ZIP_SET_MISMATCH')
    for rel,d in manifest['payloads'].items():
        b=z.read('ANVIL_R7/'+rel)
        if hashlib.sha256(b).hexdigest()!=d['sha256'] or len(b)!=d['bytes']:raise SystemExit('PACKAGE_HASH_MISMATCH:'+rel)
    m2=json.loads(z.read('ANVIL_R7/MANIFEST.json'))
    if m2!=manifest:raise SystemExit('PACKAGE_MANIFEST_SELF_READBACK_MISMATCH')
print(json.dumps({'status':'ZIP_BYTES_AND_ALL_PAYLOADS_VERIFIED','path':str(DEST),'zip_sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
                  'entries':len(allfiles),'payloads':len(files),'bytes':DEST.stat().st_size},indent=2))
