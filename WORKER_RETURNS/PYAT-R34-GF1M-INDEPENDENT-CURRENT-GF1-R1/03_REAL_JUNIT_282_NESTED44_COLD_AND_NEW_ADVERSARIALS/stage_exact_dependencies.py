"""Materialize exact dependencies from repository root; no candidate edits.
Author git archive assumes execution in a root-layout checkout, whereas this
review seats all bytes under its sole authorized return directory.
"""
import ast,io,subprocess,tarfile,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[1]; repo=R.parents[1]
review=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1'; S=review/'stage'
scope={}
code=ast.parse((review/'repair/reproduce.py').read_text())
for node in code.body:
 if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name) and node.targets[0].id in ('E','G','H','J','K','F','I','PINS'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<pins>','exec'),scope)
def archive(sha,path,dest):
 raw=subprocess.check_output(['git','archive',sha,path],cwd=repo)
 with tarfile.open(fileobj=io.BytesIO(raw)) as t:
  for m in t.getmembers():assert not m.issym() and not m.islnk() and (dest/m.name).resolve().is_relative_to(dest.resolve())
  t.extractall(dest)
for path,sha in scope['PINS'].items(): archive(sha,path,S)
archive('9f4a23cef1482e0a81afb1e7a65df90879931465',scope['E']+'/court',S/'pre')
shutil.copytree(S/'pre'/scope['E']/'court',S/scope['I']/'court',dirs_exist_ok=True)
print('Exact dependencies staged; candidate and tests untouched')
