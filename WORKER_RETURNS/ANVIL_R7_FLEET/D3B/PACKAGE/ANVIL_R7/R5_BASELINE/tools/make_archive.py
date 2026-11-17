#!/usr/bin/env python3
"""Deterministic single-artifact pack with independently recomputed SHA-256 of every payload."""
import hashlib,json,pathlib,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'ANVIL_R5.zip'
# Keep exact recovered interim anthology separately; compile final revised source docs once.
numbered=sorted(p for p in ROOT.iterdir() if p.is_file() and p.name[:2].isdigit() and p.suffix in ('.md','.json'))
full=['# ANVIL R5 — full campaign and all four MCR-lite commissions','','**Campaign pack, not an executed or accredited architecture.** `README.md` is the front door. Revision and recovery scope: `20_RECOVERY_AND_TEST_PROVENANCE.md`.']
for p in numbered:
    full += ['','---','','# FILE: '+p.name,'',p.read_text()]
(ROOT/'ANVIL_FULL_CAMPAIGN_AND_ALL_PROMPTS.md').write_text('\n'.join(full).rstrip()+'\n')
files=[p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='MANIFEST.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'package':'ANVIL','revision':'R5','stage':'PREPARED_SYNTHETIC_CHECKED_NOT_EXECUTED','original_source':'Saved interrupted R5 anthology in the project; executable tools reconstructed and tested','source_cut_scope':'Historical documentary start 7fc00289dd801d2d0a8ce159986c7595fc27a4d9; no claim this is live PRE-MAIN','payloads':{str(p.relative_to(ROOT)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)},'test_scope':'SYNTHETIC_ONLY','github_modified':False,'protected_received':False}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
files.append(ROOT/'MANIFEST.json')
with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):
        info=zipfile.ZipInfo('ANVIL_R5/'+str(p.relative_to(ROOT)),date_time=(2026,11,16,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o644<<16
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
with zipfile.ZipFile(DEST,'r') as z:
    assert z.testzip() is None
    m=json.loads(z.read('ANVIL_R5/MANIFEST.json'))
    assert len(z.namelist())==len(m['payloads'])+1
    for key,data in m['payloads'].items():
        contents=z.read('ANVIL_R5/'+key)
        assert hashlib.sha256(contents).hexdigest()==data['sha256'] and len(contents)==data['bytes'],key
print(json.dumps({'status':'PASS_ZIP_INTEGRITY_AND_PAYLOAD_SHA256','archive':str(DEST),'files_including_manifest':len(files),'payloads_verified':len(manifest['payloads']),'bytes':DEST.stat().st_size,'campaign_source_docs':len(numbered),'source_and_authority_grade':'PREPARED_ONLY'},indent=2))
