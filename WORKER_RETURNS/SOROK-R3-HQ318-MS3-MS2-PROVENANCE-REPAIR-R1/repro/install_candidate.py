"""Overlay only the owned hypothetical wrapper/helper at the original import path."""
from pathlib import Path
import json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[1];M2=R/'staging/ms2';RT=M2/'staging/ms1/runtime'
rows=[]
for name in ['ms1_serial.py','ms3_native_custody.py']:
    p=R/'candidate'/name;b=p.read_bytes();shutil.copyfile(p,RT/name)
    rows.append(dict(candidate=str(p.relative_to(R)),module_file=str((RT/name).relative_to(R)),blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),sha256=hashlib.sha256(b).hexdigest()))
for row in json.loads((M2/'staging/ms1/evidence/native_source_ledger.json').read_text()):
    b=(M2/'staging/ms1'/row['local']).read_bytes();assert b==subprocess.check_output(['git','show',row['commit']+':'+row['authoritative_path']],cwd=R.parents[1])
(R/'evidence/CANDIDATE_INSTALLATION.json').write_text(json.dumps(dict(files=rows,native9_and_guard_unchanged=True,test_oracle_edits=False),indent=2)+'\n')
print('OWN_CANDIDATE_INSTALLED_NATIVE_AND_TESTS_UNCHANGED')
