"""Restore the exact original seven-test court locally, without owner edits."""
from pathlib import Path
import subprocess
R=Path(__file__).resolve().parent;W=R.parents[1]
prefix='WORKER_RETURNS/PYAT-R37-E04J-F1F4-NATIVE-CONSUMER-JOIN-R1/'
paths=['tests/test_e04j_native_original_consumer_join.py',*[f'runtime/product/{name}.py' for name in ('__init__','service','nonparent','empirical','world','scenario')],'runtime/aux/pre553_n9_n10w_progressive_candidate.py']
for relative in paths:
    data=subprocess.check_output(['git','show','b39b756564790f4742f28af92e2e7848cf54a419:'+prefix+relative],cwd=W)
    destination=R/'.runtime/e04jr'/relative
    if destination.exists():assert destination.read_bytes()==data
    else:destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(data)
print('Exact original native court ready; no existing source overwritten.')
