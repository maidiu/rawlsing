"""Reconstruct a new reviewer runtime from immutable inputs; refuse to overwrite one."""
from pathlib import Path
import shutil,tarfile,subprocess,os,json,hashlib
ROOT=Path(__file__).resolve().parent

def main():
 src=ROOT/'inputs/b3a';run=ROOT/'.scratch/b3a'
 assert not run.exists(),'Existing runtime: inspect it or choose a new checkout; no implicit reset'
 run.mkdir(parents=True)
 for p in src.iterdir():
  if p.name=='evidence':continue
  if p.is_dir():shutil.copytree(p,run/p.name)
  else:shutil.copyfile(p,run/p.name)
 (run/'evidence').mkdir();(run/'candidate/evidence').mkdir()
 for row in json.loads((ROOT/'evidence/input_transport_manifest.json').read_text()):
  data=(ROOT/row['local']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']
 with tarfile.open(src/'pinned_closure.tar.gz') as t:
  for m in t.getmembers():
   assert m.isfile() and not m.issym() and not m.islnk() and '..' not in Path(m.name).parts and not Path(m.name).is_absolute()
   p=run/'candidate'/m.name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(t.extractfile(m).read())
 common=subprocess.check_output(['git','rev-parse','--path-format=absolute','--git-common-dir'],cwd=ROOT).decode().strip()
 subprocess.run(['python3','materialize.py'],cwd=run/'frozen_b3',env=dict(os.environ,GIT_DIR=common,PYTHONDONTWRITEBYTECODE='1'),check=True)
 shutil.copytree(run/'frozen_b3/.runtime',run/'candidate/.runtime',dirs_exist_ok=True)
 shutil.copyfile(run/'frozen_b3/source_manifest.json',run/'candidate/source_manifest.json')
 print('Fresh source reconstruction complete. No author database or execution log reused.')
if __name__=='__main__':main()
