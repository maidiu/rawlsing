#!/usr/bin/env python3
"""Collect finalized retained evidence; do not rewrite historical execution claims.

SHA256SUMS paths are repository-root-relative. The supersession receipt points
at the manifest, so it is excluded from that manifest and covered by sums.
"""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve()
ROOT=next(p for p in HERE.parents if (p/'.git').exists())
RETURN=HERE.parents[1]
EVID=RETURN/'evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    excluded={RETURN/'manifest.json',EVID/'normalized_manifest.json',EVID/'SHA256SUMS.txt',EVID/'manifest_supersession.json'}
    paths=set()
    for base in [ROOT/'CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py',ROOT/'tests/universal_execution_oracle',RETURN]:
        for p in ([base] if base.is_file() else base.rglob('*')):
            if p.is_file() and p not in excluded and '__pycache__' not in p.parts and p.suffix!='.pyc':paths.add(p)
    rows=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(paths)]
    old=json.loads((RETURN/'manifest.json').read_text())
    old.update(files=rows,file_count=len(rows),branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),excluded_self=[p.relative_to(RETURN).as_posix() for p in sorted(excluded)],note='Finalized evidence only; historical passport and execution witnesses preserved. Supersession receipt and normalized manifest covered by repository-root-relative SHA256SUMS.')
    (RETURN/'manifest.json').write_text(json.dumps(old,indent=2,sort_keys=True)+'\n')
    (EVID/'normalized_manifest.json').write_text(json.dumps({'schema':'R56_R00E_R2_NORMALIZED_MANIFEST@1','files':rows,'manifest_sha256':sha(RETURN/'manifest.json'),'excluded_self':['evidence/normalized_manifest.json','evidence/SHA256SUMS.txt','evidence/manifest_supersession.json']},indent=2,sort_keys=True)+'\n')
    p=EVID/'manifest_supersession.json';s=json.loads(p.read_text());s['successor_manifest_sha256']=sha(RETURN/'manifest.json');s['custody_repair_scope']='Packaging only; retained gate/test/passport/proof witnesses unchanged; historical negative retained at 3d4d77e9b667a1cddac07c3bfdda7d8795de458d';p.write_text(json.dumps(s,indent=2,sort_keys=True)+'\n')
    sums=paths|{RETURN/'manifest.json',EVID/'normalized_manifest.json',EVID/'manifest_supersession.json'}
    (EVID/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}\n' for p in sorted(sums)))
if __name__=='__main__':main()
