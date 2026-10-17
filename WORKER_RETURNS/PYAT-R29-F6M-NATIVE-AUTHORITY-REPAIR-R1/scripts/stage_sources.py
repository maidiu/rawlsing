"""Materialize complete pinned source-free return trees; never follow legacy symlinks."""
from pathlib import Path
import subprocess, hashlib, json
ROOT=Path(__file__).resolve().parents[1]
PINS={
 'F6C':('9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f','PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1'),
 'F6J':('825b2d8050b550f1d52d3129883584fee2ef36c2','PYAT-R27-F6J-INDEPENDENT-F6-EXPERIMENT-COMPLETION-R1'),
 'F6L':('6060adfac10f80020ed8e52cf2736467112d57c1','PYAT-R28-F6L-INDEPENDENT-DECISION-COURT-R1')}
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
def main():
 ledger=[]
 for alias,(commit,name) in PINS.items():
  prefix='WORKER_RETURNS/'+name+'/'
  for row in git('ls-tree','--full-tree','-rz',commit,prefix).split(bytes([0])):
   if not row:continue
   meta,path=row.split(b'\t'); mode,kind,oid=meta.decode().split(); path=path.decode()
   assert kind=='blob'
   raw=git('cat-file','blob',oid);assert blob(raw)==oid
   dest=ROOT/'inherited'/alias/path[len(prefix):]
   # Preserve symlink bytes as a receipt, never a machine-dependent live link.
   if mode=='120000':dest=dest.with_name(dest.name+'.symlink-origin.txt')
   dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
   ledger.append(dict(commit=commit,path=path,git_mode=mode,git_blob=oid,sha256=hashlib.sha256(raw).hexdigest(),materialized=str(dest.relative_to(ROOT))))
 (ROOT/'custody').mkdir(exist_ok=True)
 (ROOT/'custody/original_trees.json').write_text(json.dumps(ledger,indent=2)+'\n')
 print('Verified and staged',len(ledger),'original blobs')
if __name__=='__main__':main()
