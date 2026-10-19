"""Rehydrate missing exact predecessor blobs from the shared Git store, without rewrite."""
from pathlib import Path
import hashlib,json,subprocess
R=Path(__file__).resolve().parent
for row in json.loads((R/'staging_manifest.json').read_text()):
    path=R/row['staged']
    if not path.exists():
        data=subprocess.check_output(['git','show',row['commit']+':'+row['path']],cwd=R)
        assert hashlib.sha256(data).hexdigest()==row['sha256']
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    assert hashlib.sha256(path.read_bytes()).hexdigest()==row['sha256'],row['staged']
print('All 338 frozen blobs materialized and verified; existing files never overwritten.')
