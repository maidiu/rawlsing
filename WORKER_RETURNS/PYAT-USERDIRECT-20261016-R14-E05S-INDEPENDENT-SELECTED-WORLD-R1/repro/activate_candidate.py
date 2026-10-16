"""Explicit module-path compatibility adapter, no frozen test edits."""
import pathlib,json,hashlib,shutil
R=pathlib.Path(__file__).resolve().parents[1]
p=R/'candidate/e05r_selected_world_adapter.py';b=p.read_bytes()
m=json.loads((R/'source_manifest.json').read_text())
if not (R/'original_source_manifest.json').exists():
 shutil.copyfile(R/'source_manifest.json',R/'original_source_manifest.json')
for row in m:
 if row['local']=='e05_n9_selected_world_adapter.py':
  row.update(commit='84485d32c0088995f8dc664dc0517b2d27f2563d',path='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R13-E05R-SELECTED-WORLD-REPAIR-R1/candidate/e05r_selected_world_adapter.py',
    git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),
    sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
(R/'runtime/e05_n9_selected_world_adapter.py').write_bytes(b)
(R/'source_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print('Activated explicit E05R @2 compatibility module',hashlib.sha256(b).hexdigest())
