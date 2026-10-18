"""Portable replay of this completed review; all writes stay in this return.
Run from any cwd with this reviewed Git object closure available. Historical
setup-failure logs are retained; this seats the two known harness prerequisites.
The independent RED is expected to persist until a separately reviewed repair.
"""
import io,subprocess,tarfile,sys
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent;repo=R.parents[1]
source='WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';dest=R/'stage';dest.mkdir(exist_ok=True)
raw=subprocess.check_output(['git','archive','d97a5df8c03d02ca3c7433937550cdb6774537b5',source],cwd=repo)
with tarfile.open(fileobj=io.BytesIO(raw)) as t:
 for m in t.getmembers():assert not m.issym() and not m.islnk() and (dest/m.name).resolve().is_relative_to(dest.resolve())
 t.extractall(dest)
subprocess.run([sys.executable,str(O/'stage_exact_dependencies.py')],check=True,cwd=repo)
v=dest/source;s=v/'stage'
e=s/'WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1/court/runtime_root/gf1_pair_support_consumer.py'
i=s/'WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1/court/runtime_root/gf1_pair_support_consumer.py'
i.write_bytes(e.read_bytes())
with (O/'portable_qualify.log').open('w') as log:
 subprocess.run([sys.executable,str(v/'repair/qualify.py')],check=True,cwd=repo,stdout=log,stderr=subprocess.STDOUT)
for script in ('audit_science.py','run_independent.py','run_cold.py','collect_evidence.py'):
 subprocess.run([sys.executable,str(O/script)],check=True,cwd=repo)
print('Review replay complete. Inspect independent_execution.json/JUnit: 24 pass / 2 fail is the retained RED, not a successful acceptance gate.')
