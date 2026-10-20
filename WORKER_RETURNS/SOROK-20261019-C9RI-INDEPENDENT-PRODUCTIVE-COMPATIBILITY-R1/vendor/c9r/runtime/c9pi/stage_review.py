"""Exact local Git-object staging. No candidate repairs or external source queries."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
TARGET='38fba47614e82a86fc5a3fa3f50c27048493e808'
SOURCES=[(TARGET,'WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/','frozen/c9p/'),('d80e3ebac7db186f33c073074abc20da25dc041e','WORKER_RETURNS/SOROK-20261019-C9O-ACTOR-RULE-OWNER-SCIENCE-DECISION-R1/','frozen/c9o/'),('0d47fe863671d1e1d57f26102462be6595c5d7ea','WORKER_RETURNS/SOROK-V2-HQ325-S1-INDEPENDENT-BFIRST-SCIENCE-R1/','frozen/s1/')]
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def stage(commit,path,dst):
 b=git('show',commit+':'+path);out=ROOT/dst;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
 h=blob(b);assert h==git('rev-parse',commit+':'+path).decode().strip()
 return dict(commit=commit,path=path,staged=dst,git_blob_sha1=h,sha256=hashlib.sha256(b).hexdigest())
def main():
 rows=[]
 for commit,prefix,dst in SOURCES:
  for path in git('ls-tree','-r','--name-only',commit,prefix).decode().splitlines():rows.append(stage(commit,path,dst+path[len(prefix):]))
 (ROOT/'custody').mkdir(exist_ok=True);(ROOT/'custody/source_preimages.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('Verified',len(rows),'exact source preimages')
if __name__=='__main__':main()
