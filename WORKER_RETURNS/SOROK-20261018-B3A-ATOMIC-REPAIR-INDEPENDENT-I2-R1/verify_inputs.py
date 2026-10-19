"""Compare actual staged bytes to immutable Git or Git-attested archive members."""
from pathlib import Path
import subprocess,json,hashlib,tarfile,io
ROOT=Path(__file__).resolve().parent;SRC=ROOT/'inputs/b3a';RUN=ROOT/'.scratch/b3a'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
 rows=json.loads((SRC/'verified_sources.json').read_text());result=[]
 for row in rows:
  path=RUN/row['local'];data=path.read_bytes();assert sha(data)==row['sha256'],row['local']
  if 'commit' in row:
   assert git('show',row['commit']+':'+row['path'])==data
   assert git('rev-parse',row['commit']+':'+row['path']).decode().strip()==row['git_blob_sha1']
  else:
   archive=RUN/'candidate/.runtime/b2/imports/F1/F1_frozen_court.tar.gz'
   assert sha(archive.read_bytes())==row['archive_sha256']
   with tarfile.open(archive) as t:assert t.extractfile(row['archive_member']).read()==data
  result.append(dict(row,independently_verified=True))
 changes=[]
 for p in (SRC/'candidate').iterdir():
  if p.is_file() and p.suffix=='.py':
   old=git('show','47b46a85b9ebb633754866f1e6f1b12db3bd2012:WORKER_RETURNS/SOROK-V2-HQ329-B3-COUPLED-INTERPRETATION-R1/'+p.name)
   if old!=p.read_bytes():changes.append(p.name)
 assert sorted(changes)==['fixture_authority.py','integration.py']
 for row in json.loads((SRC/'candidate_version.json').read_text())['altered_files']:
  data=(RUN/'candidate'/row['path']).read_bytes();assert sha(data)==row['sha256'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
 assert sha((SRC/'pinned_closure.tar.gz').read_bytes())==json.loads((SRC/'candidate_version.json').read_text())['pinned_closure_sha256']
 (ROOT/'evidence/source_verification.json').write_text(json.dumps({'verified_source_count':len(result),'rows':result,'candidate_only_modified_files':sorted(changes),'pinned_tar_verified':True},indent=2)+'\n')
 print('Verified',len(result),'Git/archive sources; candidate diff:',sorted(changes))
if __name__=='__main__':main()
