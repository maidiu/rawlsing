import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
rows={}
for p in sorted(R.rglob('*')):
    if p.is_file() and not p.is_symlink() and not any(x in {'.pytest_cache','__pycache__'} for x in p.parts) and p.name not in {'ARTIFACT_SHA256SUMS.json','PUBLICATION_RECEIPT.json'}:
        rows[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'ARTIFACT_SHA256SUMS.json').write_text(json.dumps(dict(schema='WG0X_ARTIFACT_HASHES@1',scope='RELATIVE_RETURN_FILES_EXCLUDING_SELF_AND_LATER_PUBLICATION_RECEIPT',files=rows,relative_symlink=dict(path='sources/native',target='../native')),sort_keys=True,indent=2)+'\n')
print(json.dumps(dict(sealed_files=len(rows))))
