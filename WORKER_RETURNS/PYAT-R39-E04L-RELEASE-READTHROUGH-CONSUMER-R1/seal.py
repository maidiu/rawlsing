"""Seal published return files; omit ignored runtime reconstruction and self seals."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;W=R.parents[1]
files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',str(R)],cwd=W,text=True).splitlines()
rows=[]
for name in sorted(set(files)):
    p=W/name
    if p.parent==R and p.name in ('return_manifest.json','SHA256SUMS'):continue
    data=p.read_bytes()
    assert bytes([47])+b'Users'+bytes([47]) not in data,('PERSONAL_HOST_PATH',str(p.relative_to(R)))
    rows.append(dict(path=str(p.relative_to(R)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
manifest=dict(schema='PYAT_R39_E04L_RETURN_SEAL_R1',startup='2e6c189fd54b818556a44419b19691938ea76d5a',claim_grade='SOURCEFREE_TEST_ONLY; CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED',adoption=False,files=rows,exclusions=['self seals','Git-ignored runtime reconstruction/cache'])
(R/'return_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
(R/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows))
print('Sealed',len(rows),'files',sum(x['bytes'] for x in rows),'bytes')
