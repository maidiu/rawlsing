"""Portable Git-object and unchanged-owner checks; no raw data reads."""
from pathlib import Path
import hashlib, json, subprocess
root = Path(__file__).resolve().parents[3]
ret = Path(__file__).resolve().parents[1]
manifest = json.loads((ret/'05_MANIFEST.json').read_text())
for entry in manifest['materialized_exact_objects']:
    data = (root/entry['path']).read_bytes()
    blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob == entry['blob'], entry['path']
    original = subprocess.check_output(['git','show',entry['commit']+':'+entry.get('source_path',entry['path'])],cwd=root)
    assert data == original, entry['path']
checked = []
for record in subprocess.check_output(['git','ls-tree','-r','-z','712b818e6c0fa87412db7f4edaad1397b2e9f090','rawlsing_next'],cwd=root).split(b'\0'):
    if not record: continue
    metadata, path = record.split(b'\t',1)
    p = root/path.decode()
    if not p.is_file(): continue # sparse exclusions are not materialized
    data = p.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == metadata.split()[2].decode(),str(p)
    checked.append(path.decode())
assert not list(root.rglob('*.sav')) and not list(root.rglob('*.dta'))
print(json.dumps({'exact_materialized_objects':len(manifest['materialized_exact_objects']),
                  'unchanged_existing_checked_files':len(checked),'raw_survey_files':0}))
