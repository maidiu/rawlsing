"""Seal publishable files only; keep ignored runtime/personal-path source local."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent;W=R.parents[1]
names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','--',str(R)],cwd=W,text=True).splitlines()
rows=[]
for name in sorted(set(names)):
    p=W/name
    if p.name in ('return_manifest.json','SHA256SUMS') and p.parent==R:continue
    data=p.read_bytes()
    personal_prefix=bytes([47])+b'Users'+bytes([47])
    assert personal_prefix not in data and Path.home().name.encode() not in data,('PERSONAL_PATH',p.relative_to(R))
    rows.append(dict(path=str(p.relative_to(R)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
result=dict(schema='SOROK_CLR3R1_INDEPENDENT_I2_RETURN_V1',sealed_startup='6cd39f339849d724c862a2a55af977dcb8e7e011',repair_target='de9a525c362bf58dbb620fcd7db336a4734e7db8',verdict='ACCEPT_SCOPED',native_permission=False,adoption=False,files=rows,exclusions=['return_manifest.json','SHA256SUMS','Git-ignored runtime files and one exact predecessor runner; see README/materialize_frozen.py'])
(R/'return_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows))
print('Sealed',len(rows),'publishable files;',sum(x['bytes'] for x in rows),'bytes')
